"""JSON command-line interface for autonomous agents managing a KeePass database.

This CLI is designed to be operated by AI agents, not humans. Every invocation
prints exactly one JSON object to standard output and communicates outcomes
through structured fields:

- ``{"ok": true, "action": "...", ...}`` on success.
- ``{"ok": false, "error": "message", "error_code": "...", "type": "..."}``
  on failure. ``error_code`` is a stable, machine-matchable string (see
  ``ErrorCode`` below); it is always present on failures.

Exit status: ``0`` on success, ``2`` for expected/handled errors (bad
arguments, selectors, credentials, etc.), ``1`` for unexpected errors.

The database path and password are read from ``KEEPASS_DATABASE_PATH`` and
``KEEPASS_DATABASE_PASSWORD`` (with an optional ``--database`` override),
after loading a local ``.env`` file. Entry passwords are supplied directly as
CLI arguments (``--password`` on ``add-entry``/``edit-entry``). Secrets
(entry passwords/OTP) are never included in a response unless the caller
passes ``--show-secrets``. Timestamps are omitted unless the caller passes
``--include-metadata``. ``delete-entry`` and ``delete-group`` move items to
the database's Recycle Bin by default; pass ``--permanent`` to bypass it.
"""

import argparse
import base64
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from dotenv import load_dotenv

from pykeepass import PyKeePass, create_database
from pykeepass.exceptions import (
    BinaryError,
    CredentialsError,
    HeaderChecksumError,
    PayloadChecksumError,
    UnableToSendToRecycleBin,
)

load_dotenv()


class ErrorCode:
    """Stable, machine-matchable error identifiers returned as ``error_code``."""

    INVALID_ARGUMENT = "invalid_argument"
    INVALID_SELECTOR = "invalid_selector"
    NOT_FOUND = "not_found"
    AMBIGUOUS_SELECTOR = "ambiguous_selector"
    AUTH_FAILURE = "auth_failure"
    DATABASE_NOT_FOUND = "database_not_found"
    DATABASE_EXISTS = "database_exists"
    DATABASE_CORRUPT = "database_corrupt"
    MISSING_ENV_VAR = "missing_env_var"
    ROOT_PROTECTED = "root_protected"
    INVALID_MOVE = "invalid_move"
    FILE_NOT_FOUND = "file_not_found"
    SHARED_RESOURCE = "shared_resource"
    NO_FIELDS_PROVIDED = "no_fields_provided"
    INTERNAL_ERROR = "internal_error"


class CliError(Exception):
    """An expected command-line error that can be returned as JSON."""

    def __init__(self, message: str, error_code: str = ErrorCode.INVALID_ARGUMENT) -> None:
        super().__init__(message)
        self.error_code = error_code


class AgentArgumentParser(argparse.ArgumentParser):
    """An ArgumentParser that reports failures as ``CliError`` instead of
    printing usage text and calling ``sys.exit`` directly, so agents always
    receive a single JSON error object rather than plain-text usage output."""

    def error(self, message: str) -> None:  # type: ignore[override]
        raise CliError(message, ErrorCode.INVALID_ARGUMENT)


def emit(payload: dict[str, Any], status: int = 0) -> int:
    """Write one JSON result and return its intended process status."""
    print(json.dumps(payload, sort_keys=True))
    return status


def emit_error(error: CliError, status: int, type_name: str | None = None) -> int:
    payload: dict[str, Any] = {
        "ok": False,
        "error": str(error),
        "error_code": error.error_code,
    }
    if type_name is not None:
        payload["type"] = type_name
    return emit(payload, status)


def iso(value: datetime | None) -> str | None:
    return value.isoformat() if value is not None else None


def password_from_environment() -> str:
    password = os.environ.get("KEEPASS_DATABASE_PASSWORD")
    if password is None:
        raise CliError(
            f"Password environment variable {"KEEPASS_DATABASE_PASSWORD"!r} is not set.",
            ErrorCode.MISSING_ENV_VAR,
        )
    return password


def resolve_database_path(args: argparse.Namespace) -> Path:
    path = getattr(args, "database", None) or os.environ.get("KEEPASS_DATABASE_PATH")
    if not path:
        raise CliError(
            f"Database path missing; pass --database or set {"KEEPASS_DATABASE_PATH"!r}.",
            ErrorCode.MISSING_ENV_VAR,
        )
    return Path(path)



def open_database(args: argparse.Namespace) -> PyKeePass:
    path = resolve_database_path(args)
    if not path.is_file():
        raise CliError(f"Database does not exist: {path}", ErrorCode.DATABASE_NOT_FOUND)
    return PyKeePass(str(path), password=password_from_environment(), keyfile=args.keyfile)


def group_path(group: Any) -> str:
    path = getattr(group, "path", None)
    if isinstance(path, (list, tuple)):
        return "/".join(str(part) for part in path)
    return str(path or getattr(group, "name", ""))


def group_data(group: Any, include_metadata: bool = False) -> dict[str, Any]:
    data = {
        "uuid": str(group.uuid),
        "name": group.name,
        "path": group_path(group),
        "notes": group.notes,
        "entry_count": len(group.entries),
        "subgroup_count": len(group.subgroups),
    }
    if include_metadata:
        data["created"] = iso(group.ctime)
        data["modified"] = iso(group.mtime)
        data["expires"] = bool(group.expires)
        data["expiry_time"] = iso(group.expiry_time) if group.expires else None
    return data


def attachment_data(attachment: Any, include_data: bool = False) -> dict[str, Any]:
    result = {"id": attachment.id, "filename": attachment.filename}
    if include_data:
        result["data_base64"] = base64.b64encode(attachment.data).decode("ascii")
    return result


def entry_data(
    entry: Any, include_secrets: bool = False, include_metadata: bool = False
) -> dict[str, Any]:
    data = {
        "uuid": str(entry.uuid),
        "title": entry.title,
        "username": entry.username,
        "url": entry.url,
        "notes": entry.notes,
        "group": group_path(entry.group),
        "attachments": [attachment_data(item) for item in entry.attachments],
    }
    if include_secrets:
        data["password"] = entry.password
        data["otp"] = entry.otp
    if include_metadata:
        data["created"] = iso(entry.ctime)
        data["modified"] = iso(entry.mtime)
        data["accessed"] = iso(entry.atime)
        data["expires"] = bool(entry.expires)
        data["expiry_time"] = iso(entry.expiry_time) if entry.expires else None
    return data


def find_entry(kp: PyKeePass, args: argparse.Namespace) -> Any:
    matches = []
    if getattr(args, "entry_uuid", None):
        matches = [entry for entry in kp.entries if str(entry.uuid) == args.entry_uuid]
    elif getattr(args, "title", None):
        matches = [entry for entry in kp.entries if entry.title == args.title]
    else:
        raise CliError(
            "Specify --entry-uuid or --title to select an entry.", ErrorCode.INVALID_SELECTOR
        )

    if not matches:
        raise CliError("No entry matched the supplied selector.", ErrorCode.NOT_FOUND)
    if len(matches) > 1:
        raise CliError(
            "Entry selector is ambiguous; select the entry with --entry-uuid.",
            ErrorCode.AMBIGUOUS_SELECTOR,
        )
    return matches[0]


def find_group(kp: PyKeePass, selector: str | None) -> Any:
    if not selector or selector == "/":
        return kp.root_group

    normalized = selector.strip("/")
    matches = [
        group
        for group in kp.groups
        if str(group.uuid) == selector
        or group_path(group).strip("/") == normalized
    ]
    if not matches:
        raise CliError(f"No group matched {selector!r}.", ErrorCode.NOT_FOUND)
    if len(matches) > 1:
        raise CliError(f"Group selector {selector!r} is ambiguous; use its UUID.", ErrorCode.AMBIGUOUS_SELECTOR)
    return matches[0]


def find_attachment(entry: Any, args: argparse.Namespace) -> Any:
    if getattr(args, "attachment_id", None) is not None:
        matches = [item for item in entry.attachments if item.id == args.attachment_id]
    elif getattr(args, "filename", None):
        matches = [item for item in entry.attachments if item.filename == args.filename]
    else:
        raise CliError(
            "Specify --attachment-id or --filename to select an attachment.",
            ErrorCode.INVALID_SELECTOR,
        )

    if not matches:
        raise CliError("No attachment matched the supplied selector.", ErrorCode.NOT_FOUND)
    if len(matches) > 1:
        raise CliError(
            "Attachment selector is ambiguous; select the attachment with --attachment-id.",
            ErrorCode.AMBIGUOUS_SELECTOR,
        )
    return matches[0]


def validate_group_move(group: Any, destination: Any) -> None:
    """Reject moves that would make a group its own ancestor or descendant."""
    node = destination
    while node is not None:
        if node.uuid == group.uuid:
            raise CliError(
                "Cannot move a group into itself or one of its own descendants.",
                ErrorCode.INVALID_MOVE,
            )
        node = getattr(node, "parentgroup", None)


def _entry_modified_key(entry: Any) -> tuple[datetime, str]:
    mtime = entry.mtime
    if mtime is None:
        mtime = datetime.min.replace(tzinfo=timezone.utc)
    elif mtime.tzinfo is None:
        mtime = mtime.replace(tzinfo=timezone.utc)
    return (mtime, str(entry.uuid))


ENTRY_SORT_KEYS: dict[str, Callable[[Any], Any]] = {
    "uuid": lambda entry: str(entry.uuid),
    "title": lambda entry: (entry.title or "", str(entry.uuid)),
    "group": lambda entry: (group_path(entry.group), str(entry.uuid)),
    "modified": _entry_modified_key,
}

GROUP_SORT_KEYS: dict[str, Callable[[Any], Any]] = {
    "uuid": lambda group: str(group.uuid),
    "name": lambda group: (group.name or "", str(group.uuid)),
    "path": lambda group: (group_path(group), str(group.uuid)),
}


def command_create(args: argparse.Namespace) -> dict[str, Any]:
    path = resolve_database_path(args)
    if path.exists() and not args.force:
        raise CliError(
            f"Database already exists: {path}. Use --force to overwrite it.",
            ErrorCode.DATABASE_EXISTS,
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    create_database(str(path), password=password_from_environment(), keyfile=args.keyfile)
    return {"ok": True, "action": "create", "database": str(path)}


def command_database_info(args: argparse.Namespace) -> dict[str, Any]:
    kp = open_database(args)
    major, minor = kp.version
    return {
        "ok": True,
        "database": {
            "path": str(resolve_database_path(args).resolve()),
            "version": f"{major}.{minor}",
            "encryption_algorithm": kp.encryption_algorithm,
            "group_count": len(kp.groups),
            "entry_count": len(kp.entries),
        },
    }


def command_list_entries(args: argparse.Namespace) -> dict[str, Any]:
    kp = open_database(args)
    entries = kp.entries
    if args.query:
        query = args.query.casefold()
        entries = [
            entry for entry in entries
            if query in entry.title.casefold()
            or query in entry.username.casefold()
            or query in entry.url.casefold()
            or query in entry.notes.casefold()
        ]
    if args.group:
        target_group = find_group(kp, args.group)
        entries = [entry for entry in entries if entry.group.uuid == target_group.uuid]
    entries = sorted(entries, key=ENTRY_SORT_KEYS[args.sort_by])
    return {
        "ok": True,
        "entries": [
            entry_data(entry, include_secrets=args.show_secrets, include_metadata=args.include_metadata)
            for entry in entries
        ],
    }


def command_show_entry(args: argparse.Namespace) -> dict[str, Any]:
    kp = open_database(args)
    entry = find_entry(kp, args)
    return {
        "ok": True,
        "entry": entry_data(
            entry, include_secrets=args.show_secrets, include_metadata=args.include_metadata
        ),
    }


def command_add_entry(args: argparse.Namespace) -> dict[str, Any]:
    kp = open_database(args)
    group = find_group(kp, args.group)
    entry = kp.add_entry(
        group,
        args.title,
        args.username,
        args.password,
        url=args.url,
        notes=args.notes,
    )
    if args.otp is not None:
        entry.otp = args.otp
    kp.save()
    return {
        "ok": True,
        "action": "add-entry",
        "entry": entry_data(
            entry, include_secrets=args.show_secrets, include_metadata=args.include_metadata
        ),
    }


def command_edit_entry(args: argparse.Namespace) -> dict[str, Any]:
    kp = open_database(args)
    entry = find_entry(kp, args)
    fields = {
        "title": args.new_title,
        "username": args.username,
        "url": args.url,
        "notes": args.notes,
        "otp": args.otp,
        "password": args.password,
    }
    changed = [name for name, value in fields.items() if value is not None]
    if not changed:
        raise CliError("Supply at least one field to update.", ErrorCode.NO_FIELDS_PROVIDED)
    for name in changed:
        setattr(entry, name, fields[name])
    kp.save()
    return {
        "ok": True,
        "action": "edit-entry",
        "entry": entry_data(
            entry, include_secrets=args.show_secrets, include_metadata=args.include_metadata
        ),
    }


def command_delete_entry(args: argparse.Namespace) -> dict[str, Any]:
    kp = open_database(args)
    entry = find_entry(kp, args)
    result = entry_data(entry, include_metadata=True)
    if args.permanent:
        kp.delete_entry(entry)
        action = "delete-entry-permanent"
    else:
        try:
            kp.trash_entry(entry)
        except UnableToSendToRecycleBin:
            raise CliError(
                "Entry cannot be moved to the Recycle Bin; use --permanent to delete it.",
                ErrorCode.INVALID_MOVE,
            )
        action = "delete-entry-trash"
    kp.save()
    return {"ok": True, "action": action, "entry": result}


def command_move_entry(args: argparse.Namespace) -> dict[str, Any]:
    kp = open_database(args)
    entry = find_entry(kp, args)
    kp.move_entry(entry, find_group(kp, args.destination_group))
    kp.save()
    return {
        "ok": True,
        "action": "move-entry",
        "entry": entry_data(entry, include_metadata=args.include_metadata),
    }


def command_list_groups(args: argparse.Namespace) -> dict[str, Any]:
    kp = open_database(args)
    groups = sorted(kp.groups, key=GROUP_SORT_KEYS[args.sort_by])
    return {
        "ok": True,
        "groups": [group_data(group, include_metadata=args.include_metadata) for group in groups],
    }


def command_add_group(args: argparse.Namespace) -> dict[str, Any]:
    kp = open_database(args)
    group = kp.add_group(find_group(kp, args.parent_group), args.name, notes=args.notes)
    kp.save()
    return {
        "ok": True,
        "action": "add-group",
        "group": group_data(group, include_metadata=args.include_metadata),
    }


def command_delete_group(args: argparse.Namespace) -> dict[str, Any]:
    kp = open_database(args)
    group = find_group(kp, args.group)
    if group.uuid == kp.root_group.uuid:
        raise CliError("The root group cannot be deleted.", ErrorCode.ROOT_PROTECTED)
    result = group_data(group, include_metadata=True)
    if args.permanent:
        kp.delete_group(group)
        action = "delete-group-permanent"
    else:
        try:
            kp.trash_group(group)
        except UnableToSendToRecycleBin:
            raise CliError(
                "Group cannot be moved to the Recycle Bin; use --permanent to delete it.",
                ErrorCode.INVALID_MOVE,
            )
        action = "delete-group-trash"
    kp.save()
    return {"ok": True, "action": action, "group": result}


def command_move_group(args: argparse.Namespace) -> dict[str, Any]:
    kp = open_database(args)
    group = find_group(kp, args.group)
    destination = find_group(kp, args.destination_group)
    if group.uuid == kp.root_group.uuid:
        raise CliError("The root group cannot be moved.", ErrorCode.ROOT_PROTECTED)
    validate_group_move(group, destination)
    kp.move_group(group, destination)
    kp.save()
    return {
        "ok": True,
        "action": "move-group",
        "group": group_data(group, include_metadata=args.include_metadata),
    }


def command_list_attachments(args: argparse.Namespace) -> dict[str, Any]:
    entry = find_entry(open_database(args), args)
    return {"ok": True, "attachments": [attachment_data(item, args.include_data) for item in entry.attachments]}


def command_add_attachment(args: argparse.Namespace) -> dict[str, Any]:
    kp = open_database(args)
    entry = find_entry(kp, args)
    path = Path(args.file)
    if not path.is_file():
        raise CliError(f"Attachment file does not exist: {path}", ErrorCode.FILE_NOT_FOUND)
    binary_id = kp.add_binary(path.read_bytes())
    attachment = entry.add_attachment(binary_id, args.filename or path.name)
    kp.save()
    return {"ok": True, "action": "add-attachment", "attachment": attachment_data(attachment)}


def command_delete_attachment(args: argparse.Namespace) -> dict[str, Any]:
    kp = open_database(args)
    entry = find_entry(kp, args)
    attachment = find_attachment(entry, args)
    result = attachment_data(attachment)
    binary_id = attachment.id
    entry.delete_attachment(attachment)
    if args.delete_binary:
        reference_count = sum(
            1
            for other_entry in kp.entries
            for other in other_entry.attachments
            if other.id == binary_id
        )
        if reference_count > 0 and not args.force:
            raise CliError(
                f"Binary {binary_id} is referenced by {reference_count} other attachment(s); "
                "use --force to delete it anyway.",
                ErrorCode.SHARED_RESOURCE,
            )
        try:
            kp.delete_binary(binary_id)
        except BinaryError as error:
            raise CliError(str(error), ErrorCode.NOT_FOUND)
    kp.save()
    return {"ok": True, "action": "delete-attachment", "attachment": result}


def add_database_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--database",
        default=None,
        help=f"Path to the .kdbx database; defaults to {"KEEPASS_DATABASE_PATH"}",
    )
    parser.add_argument("--keyfile", help="Optional KeePass keyfile path")


def add_entry_selector(parser: argparse.ArgumentParser) -> None:
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--entry-uuid", help="Entry UUID")
    selector.add_argument("--title", help="Exact entry title; must be unique")


def add_attachment_selector(parser: argparse.ArgumentParser) -> None:
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--attachment-id", type=int, help="Attachment ID, as returned by list-attachments")
    selector.add_argument("--filename", help="Attachment filename; must be unique on the entry")


def add_secrets_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--show-secrets",
        action="store_true",
        help="Include password/otp in the response; omitted by default",
    )


def add_metadata_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--include-metadata",
        action="store_true",
        help="Include created/modified/expiry timestamps in the response",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = AgentArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True, parser_class=AgentArgumentParser)

    create = commands.add_parser("create", help="Create a new database")
    add_database_arguments(create)
    create.add_argument("--force", action="store_true", help="Allow overwriting an existing database")
    create.set_defaults(handler=command_create)

    db_info = commands.add_parser("database-info", help="Show database metadata")
    add_database_arguments(db_info)
    db_info.set_defaults(handler=command_database_info)

    entries = commands.add_parser("list-entries", help="List or search entries")
    add_database_arguments(entries)
    entries.add_argument("--query", help="Case-insensitive text search")
    entries.add_argument("--group", help="Group path or UUID")
    entries.add_argument(
        "--sort-by",
        choices=sorted(ENTRY_SORT_KEYS),
        default="uuid",
        help="Deterministic sort order for results; defaults to uuid",
    )
    add_secrets_flag(entries)
    add_metadata_flag(entries)
    entries.set_defaults(handler=command_list_entries)

    show = commands.add_parser("show-entry", help="Show a single entry")
    add_database_arguments(show)
    add_entry_selector(show)
    add_secrets_flag(show)
    add_metadata_flag(show)
    show.set_defaults(handler=command_show_entry)

    add = commands.add_parser("add-entry", help="Create an entry")
    add_database_arguments(add)
    add.add_argument("--group", help="Destination group path or UUID; root by default")
    add.add_argument("--title", required=True)
    add.add_argument("--username", default="")
    add.add_argument("--url", default="")
    add.add_argument("--notes", default="")
    add.add_argument("--otp", help="otpauth URI")
    add.add_argument("--password", required=True, help="Password to store on the entry")
    add_secrets_flag(add)
    add_metadata_flag(add)
    add.set_defaults(handler=command_add_entry)

    edit = commands.add_parser("edit-entry", help="Update an entry")
    add_database_arguments(edit)
    add_entry_selector(edit)
    edit.add_argument("--new-title")
    edit.add_argument("--username")
    edit.add_argument("--password", help="New password to set on the entry")
    edit.add_argument("--url")
    edit.add_argument("--notes")
    edit.add_argument("--otp")
    add_secrets_flag(edit)
    add_metadata_flag(edit)
    edit.set_defaults(handler=command_edit_entry)

    delete = commands.add_parser("delete-entry", help="Delete an entry (recycle-bin by default)")
    add_database_arguments(delete)
    add_entry_selector(delete)
    delete.add_argument(
        "--permanent", action="store_true", help="Delete permanently instead of using the Recycle Bin"
    )
    delete.set_defaults(handler=command_delete_entry)

    move_entry = commands.add_parser("move-entry", help="Move an entry to a group")
    add_database_arguments(move_entry)
    add_entry_selector(move_entry)
    move_entry.add_argument("--destination-group", required=True, help="Destination group path or UUID")
    add_metadata_flag(move_entry)
    move_entry.set_defaults(handler=command_move_entry)

    groups = commands.add_parser("list-groups", help="List groups")
    add_database_arguments(groups)
    groups.add_argument(
        "--sort-by",
        choices=sorted(GROUP_SORT_KEYS),
        default="uuid",
        help="Deterministic sort order for results; defaults to uuid",
    )
    add_metadata_flag(groups)
    groups.set_defaults(handler=command_list_groups)

    add_group = commands.add_parser("add-group", help="Create a group")
    add_database_arguments(add_group)
    add_group.add_argument("--name", required=True)
    add_group.add_argument("--parent-group", help="Parent group path or UUID; root by default")
    add_group.add_argument("--notes", default="")
    add_metadata_flag(add_group)
    add_group.set_defaults(handler=command_add_group)

    delete_group = commands.add_parser("delete-group", help="Delete a group (recycle-bin by default)")
    add_database_arguments(delete_group)
    delete_group.add_argument("--group", required=True, help="Group path or UUID")
    delete_group.add_argument(
        "--permanent", action="store_true", help="Delete permanently instead of using the Recycle Bin"
    )
    delete_group.set_defaults(handler=command_delete_group)

    move_group = commands.add_parser("move-group", help="Move a group")
    add_database_arguments(move_group)
    move_group.add_argument("--group", required=True, help="Group path or UUID")
    move_group.add_argument("--destination-group", required=True, help="Destination group path or UUID")
    add_metadata_flag(move_group)
    move_group.set_defaults(handler=command_move_group)

    attachments = commands.add_parser("list-attachments", help="List a selected entry's attachments")
    add_database_arguments(attachments)
    add_entry_selector(attachments)
    attachments.add_argument("--include-data", action="store_true", help="Include attachment data as base64")
    attachments.set_defaults(handler=command_list_attachments)

    add_attachment = commands.add_parser("add-attachment", help="Attach a file to an entry")
    add_database_arguments(add_attachment)
    add_entry_selector(add_attachment)
    add_attachment.add_argument("--file", required=True)
    add_attachment.add_argument("--filename", help="Attachment name; source filename by default")
    add_attachment.set_defaults(handler=command_add_attachment)

    delete_attachment = commands.add_parser("delete-attachment", help="Remove an entry attachment")
    add_database_arguments(delete_attachment)
    add_entry_selector(delete_attachment)
    add_attachment_selector(delete_attachment)
    delete_attachment.add_argument("--delete-binary", action="store_true", help="Also remove the underlying binary data")
    delete_attachment.add_argument(
        "--force", action="store_true", help="Delete the binary even if other attachments still reference it"
    )
    delete_attachment.set_defaults(handler=command_delete_attachment)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except CliError as error:
        return emit_error(error, 2)

    try:
        return emit(args.handler(args))
    except CliError as error:
        return emit_error(error, 2)
    except CredentialsError as error:
        return emit_error(CliError(str(error), ErrorCode.AUTH_FAILURE), 2, type(error).__name__)
    except (HeaderChecksumError, PayloadChecksumError) as error:
        return emit_error(CliError(str(error), ErrorCode.DATABASE_CORRUPT), 2, type(error).__name__)
    except BinaryError as error:
        return emit_error(CliError(str(error), ErrorCode.NOT_FOUND), 2, type(error).__name__)
    except Exception as error:
        return emit({"ok": False, "error": str(error), "error_code": ErrorCode.INTERNAL_ERROR, "type": type(error).__name__}, 1)


if __name__ == "__main__":
    sys.exit(main())




