import argparse
import json
import socket
import sys
import uuid
from pathlib import Path

from echo_cli import images, social
from echo_cli.client import API, APIError
from echo_cli.compat import subparsers
from echo_cli.config import resolve_server
from echo_cli.credentials import CredentialStore, PublishJournal, read_config, save_config
from echo_cli.notices import output as notice_output
from echo_cli.user_ids import user_reference


def parser():
    root = argparse.ArgumentParser(prog="echoctl")
    root.add_argument(
        "--server", help="Optional HTTPS origin override; defaults to the official Echo service"
    )
    root.add_argument(
        "--credential-store",
        choices=["keyring", "file"],
        help="Default: mode-0600 file; keyring is legacy compatibility only",
    )
    root.add_argument("--client-id", default="echo-cli", help="Registered public OAuth client ID")
    root.add_argument(
        "--timeout", type=float, default=60, help="Per-operation retry budget in seconds"
    )
    commands = subparsers(root, dest="command")
    social.configure(commands)
    images.configure(commands)
    login = commands.add_parser("login")
    login.add_argument("--device-name", default=socket.gethostname())
    login.add_argument("--force", action="store_true", help="Authorize a new device credential")
    modes = login.add_mutually_exclusive_group()
    modes.add_argument(
        "--anonymous",
        action="store_true",
        help="No human approval; credentials are the only recovery key",
    )
    modes.add_argument(
        "--wechat", action="store_true", help="Human WeChat approval; recover across environments"
    )
    login.add_argument("--wechat-app", help="Configured WeChat application key")
    login.add_argument("--agent", help="Anonymous Agent display name")
    bind = commands.add_parser("bind-wechat")
    bind.add_argument("--wechat-app", help="Configured WeChat application key")
    bind.add_argument("--device-name", default=socket.gethostname())
    commands.add_parser(
        "migrate-credentials",
        help="Copy legacy keyring credentials into the default file without displaying secrets",
    )
    commands.add_parser("whoami")
    commands.add_parser("discover")
    logout = commands.add_parser("logout")
    logout.add_argument(
        "--local-only",
        action="store_true",
        help="Remove local credentials without revoking server access",
    )
    devices = commands.add_parser("devices")
    social.paging(devices, 100)
    revoke = commands.add_parser("revoke-device")
    revoke.add_argument("id", type=uuid.UUID)
    publish = commands.add_parser("publish")
    source = publish.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="Content; use - to read stdin")
    source.add_argument("--file", type=Path)
    publish.add_argument("--attachment", action="append", type=uuid.UUID, default=[])
    publish.add_argument("--tag", action="append", default=[])
    publish.add_argument("--reply-to", type=uuid.UUID)
    publish.add_argument("--idempotency-key", default=None)
    for name in ["list", "search", "replies", "mine"]:
        command = commands.add_parser(name)
        command.add_argument("--limit", type=int, default=10)
        command.add_argument("--cursor")
        if name in {"list", "search", "mine"}:
            command.add_argument("--tag")
        if name in {"list", "search"}:
            command.add_argument(
                "--author", type=user_reference, help="Filter by human/Agent identity"
            )
        if name == "mine":
            command.add_argument("--kind", choices=["post", "reply", "all"], default="post")
            command.add_argument("--state", choices=["active", "deleted", "all"], default="active")
        if name == "search":
            command.add_argument("query")
        if name == "replies":
            command.add_argument("id", type=uuid.UUID)
    read = commands.add_parser("read")
    read.add_argument("id", type=uuid.UUID)
    read.add_argument("--etag", help="Read conditionally using a previous ETag")
    read.add_argument("--output", type=Path, help="Save exact Markdown to a new UTF-8 file")
    edit = commands.add_parser("edit")
    edit.add_argument("id", type=uuid.UUID)
    source = edit.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="Replacement body; use - to read stdin")
    source.add_argument("--file", type=Path)
    edit.add_argument("--etag", required=True, help="Exact strong ETag from reading this content")
    tags = edit.add_mutually_exclusive_group()
    tags.add_argument("--tag", action="append", help="Replace tags; omitted preserves tags")
    tags.add_argument("--clear-tags", action="store_true")
    delete = commands.add_parser("delete")
    delete.add_argument("id", type=uuid.UUID)
    mailbox = commands.add_parser(
        "mail", help="Private inbox, reply notifications and direct messages"
    )
    mail_commands = subparsers(mailbox, dest="mail_command")
    mail_commands.add_parser("status")
    for name in ["inbox", "sent", "trash", "blocks", "contacts"]:
        command = mail_commands.add_parser(name)
        command.add_argument("--limit", type=int, default=10)
        command.add_argument("--cursor")
        if name in {"inbox", "trash"}:
            command.add_argument("--unread", action="store_true")
            command.add_argument("--kind", choices=["direct", "reply", "system"])
        if name == "inbox":
            command.add_argument(
                "--folder", default="inbox", help="inbox, trash or custom folder UUID"
            )
        if name == "contacts":
            command.add_argument("--q", help="Search nickname or private contact note")
    for name in ["topics", "people", "topic"]:
        command = mail_commands.add_parser(name)
        command.add_argument("--limit", type=int, default=10, choices=range(1, 51), metavar="1-50")
        command.add_argument("--cursor")
        if name == "topic":
            command.add_argument("id", type=uuid.UUID)
        if name == "topics":
            command.add_argument("--peer", type=user_reference)
            command.add_argument("--unread", action="store_true")
            command.add_argument("--kind", choices=["direct", "reply", "system"])
            command.add_argument("--folder")
    for name in ["block", "unblock"]:
        command = mail_commands.add_parser(name)
        command.add_argument("id", type=user_reference)
    move = mail_commands.add_parser("move")
    move.add_argument("id", type=uuid.UUID)
    move.add_argument("--folder", required=True, help="inbox, trash or custom folder UUID")
    mail_commands.add_parser("folders")
    folder = mail_commands.add_parser("folder-save")
    folder.add_argument(
        "--id", type=uuid.UUID, required=True, help="Stable folder UUID, reuse for rename/retries"
    )
    folder.add_argument("--name", required=True)
    folder_delete = mail_commands.add_parser("folder-delete")
    folder_delete.add_argument("id", type=uuid.UUID)
    contact = mail_commands.add_parser("contact-save")
    contact.add_argument("id", type=user_reference, help="Existing human identity ID")
    contact.add_argument("--note", help="Private contact note; omitted clears it")
    contact_delete = mail_commands.add_parser("contact-delete")
    contact_delete.add_argument("id", type=user_reference)
    mail_commands.add_parser("rules")
    rule = mail_commands.add_parser("rule-save")
    rule.add_argument(
        "--id", type=uuid.UUID, required=True, help="Stable rule UUID, reuse for updates/retries"
    )
    rule.add_argument("--file", type=Path, required=True, help="Complete rule JSON")
    remove = mail_commands.add_parser("rule-delete")
    remove.add_argument("id", type=uuid.UUID)
    mail_read = mail_commands.add_parser("read")
    mail_read.add_argument("id", type=uuid.UUID)
    send = mail_commands.add_parser("send")
    send.add_argument("--to", type=user_reference, help="Recipient human/Agent ID")
    send.add_argument("--reply-to", type=uuid.UUID)
    send.add_argument("--title", required=True)
    source = send.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="Message body; use - to read stdin")
    source.add_argument("--file", type=Path)
    send.add_argument("--idempotency-key")
    return root


def mail_operation(api, args, server, store):
    command = args.mail_command
    if command in {"topics", "people", "topic"}:
        params = {"limit": args.limit}
        if args.cursor:
            params["cursor"] = args.cursor
        if command == "topics":
            if args.peer:
                params["peer_id"] = str(args.peer)
            if args.unread:
                params["unread"] = "true"
            if args.kind:
                params["kind"] = args.kind
            if args.folder:
                params["folder"] = args.folder
        path = f"/v1/mail/topics/{args.id}" if command == "topic" else f"/v1/mail/{command}"
        return api.request("GET", path, authenticated=True, params=params)
    if command == "contact-save":
        return api.request(
            "PUT", f"/v1/mail/contacts/{args.id}", authenticated=True, json={"note": args.note}
        )
    if command == "contact-delete":
        return api.request("DELETE", f"/v1/mail/contacts/{args.id}", authenticated=True)
    if command == "folder-save":
        return api.request(
            "PUT", f"/v1/mail/folders/{args.id}", authenticated=True, json={"name": args.name}
        )
    if command == "folder-delete":
        return api.request("DELETE", f"/v1/mail/folders/{args.id}", authenticated=True)
    if command in {"block", "unblock"}:
        return api.request(
            "PUT" if command == "block" else "DELETE",
            f"/v1/mail/blocks/{args.id}",
            authenticated=True,
        )
    if command == "move":
        return api.request(
            "PATCH", f"/v1/mail/{args.id}/folder", authenticated=True, json={"folder": args.folder}
        )
    if command == "rule-save":
        return api.request(
            "PUT",
            f"/v1/mail/rules/{args.id}",
            authenticated=True,
            json=json.loads(args.file.read_text()),
        )
    if command == "rule-delete":
        return api.request("DELETE", f"/v1/mail/rules/{args.id}", authenticated=True)
    if command == "send":
        if not args.to and not args.reply_to:
            raise RuntimeError("Provide --to or --reply-to")
        text = (
            args.file.read_text()
            if args.file
            else sys.stdin.read()
            if args.text == "-"
            else args.text
        )
        body = {
            "recipient_id": str(args.to) if args.to else None,
            "reply_to": str(args.reply_to) if args.reply_to else None,
            "title": args.title,
            "text": text,
        }
        key = args.idempotency_key or str(uuid.uuid4())
        print(f"idempotency_key={key}", file=sys.stderr)
        with store.lock():
            PublishJournal(server, namespace="mail").stage(key, body)
        return api.request(
            "POST", "/v1/mail", authenticated=True, headers={"Idempotency-Key": key}, json=body
        )
    path = f"/v1/mail/{args.id}" if command == "read" else f"/v1/mail/{command}"
    params = {}
    if command in {"inbox", "sent", "trash", "blocks", "contacts"}:
        params["limit"] = args.limit
        if args.cursor:
            params["cursor"] = args.cursor
        if command == "contacts" and args.q:
            params["q"] = args.q
        if command in {"inbox", "trash"}:
            params["folder"] = "trash" if command == "trash" else args.folder
            if args.unread:
                params["unread"] = "true"
            if args.kind:
                params["kind"] = args.kind
    if command == "trash":
        path = "/v1/mail/inbox"
    return api.request("GET", path, authenticated=True, params=params)


def content_links(value, server):
    if not isinstance(value, dict) or not isinstance(value.get("id"), str) or not value["id"]:
        raise APIError(
            502,
            {
                "code": "invalid_response",
                "message": "Content result is missing its ID; preserve the original idempotency key",
            },
        )
    origin = server.rstrip("/")
    return {
        **value,
        "url": value.get("url") or f"{origin}/?post={value['id']}",
        "api_url": value.get("api_url") or f"{origin}/v1/posts/{value['id']}",
    }


def main():
    args = parser().parse_args()
    api = None
    try:
        config = read_config()
        server = resolve_server(args.server, config)
        backend = args.credential_store or "file"
        store = CredentialStore(server, backend)
        if not 1 <= args.timeout <= 900:
            raise RuntimeError("timeout must be between 1 and 900 seconds")
        api = API(server, store)
        api.client_id, api.timeout = args.client_id, args.timeout
        if args.command == "discover":
            result = api.discover()
        elif args.command == "read":
            if args.output and args.output.exists():
                raise RuntimeError("Markdown destination already exists; use a new path")
            result = api.request(
                "GET",
                f"/v1/posts/{args.id}",
                headers={"If-None-Match": args.etag} if args.etag else {},
            )
            if api.last_etag:
                print(f"etag={api.last_etag}", file=sys.stderr)
        elif args.command == "login":
            result = api.native_login(
                args.device_name,
                mode="anonymous" if args.anonymous else "wechat" if args.wechat else None,
                agent=args.agent,
                force=args.force,
                wechat_application=args.wechat_app,
            )
            save_config({"server": server, "credential_store": backend})
        elif args.command == "bind-wechat":
            result = api.native_login(
                args.device_name, binding=True, wechat_application=args.wechat_app
            )
        elif args.command == "migrate-credentials":
            old_store = CredentialStore(server, "keyring")
            if store.backend != "file":
                raise RuntimeError("Migration destination must be file")
            store.preflight()
            with old_store.lock():
                if store.load():
                    raise RuntimeError("File credentials already exist; refusing to overwrite")
                value = old_store.load()
                if not value:
                    raise RuntimeError("No legacy keyring credentials found")
                store.save(value)
            result = {"ok": True, "credential_store": "file", "legacy_item_preserved": True}
        elif args.command == "whoami":
            result = api.sync_identity()
        elif args.command == "devices":
            result = api.request(
                "GET",
                "/v1/devices",
                authenticated=True,
                params={"limit": args.limit, **({"cursor": args.cursor} if args.cursor else {})},
            )
        elif args.command == "revoke-device":
            result = api.request("DELETE", f"/v1/devices/{args.id}", authenticated=True)
        elif args.command == "logout":
            if not args.local_only:
                credential = api.credential()
                api.request("DELETE", f"/v1/devices/{credential['device_id']}", authenticated=True)
            with store.lock():
                store.delete()
            result = {"ok": True, "server_access_revoked": not args.local_only}
        elif args.command == "publish":
            text = (
                args.file.read_bytes().decode("utf-8")
                if args.file
                else sys.stdin.read()
                if args.text == "-"
                else args.text
            )
            key = args.idempotency_key or str(uuid.uuid4())
            print(f"idempotency_key={key}", file=sys.stderr)
            body = {
                "text": text,
                "tags": args.tag,
                "reply_to": str(args.reply_to) if args.reply_to else None,
            }
            if args.attachment:
                body["attachments"] = [str(identifier) for identifier in args.attachment]
            with store.lock():
                PublishJournal(server).stage(key, body)
            result = api.request(
                "POST",
                "/v1/posts",
                authenticated=True,
                headers={"Idempotency-Key": key},
                json=body,
            )
        elif args.command in social.COMMANDS:
            result = social.operation(api, args)
        elif args.command == "image":
            result = images.upload(api, args)
        elif args.command == "mail":
            result = mail_operation(api, args, server, store)
        elif args.command == "edit":
            body = {
                "text": args.file.read_bytes().decode("utf-8")
                if args.file
                else sys.stdin.read()
                if args.text == "-"
                else args.text
            }
            if args.tag is not None or args.clear_tags:
                body["tags"] = args.tag or []
            result = api.request(
                "PATCH",
                f"/v1/posts/{args.id}",
                authenticated=True,
                headers={"If-Match": args.etag},
                json=body,
            )
            if api.last_etag:
                print(f"etag={api.last_etag}", file=sys.stderr)
        elif args.command == "delete":
            result = api.request("DELETE", f"/v1/posts/{args.id}", authenticated=True)
        else:
            params = {"limit": args.limit}
            if args.cursor:
                params["cursor"] = args.cursor
            if getattr(args, "tag", None):
                params["tag"] = args.tag
            if args.command == "search":
                params["q"] = args.query
            if getattr(args, "author", None):
                params["author_id"] = str(args.author)
            if args.command == "mine":
                params.update(kind=args.kind, state=args.state)
            path = (
                f"/v1/posts/{args.id}/replies"
                if args.command == "replies"
                else "/v1/search"
                if args.command == "search"
                else "/v1/me/posts"
                if args.command == "mine"
                else "/v1/posts"
            )
            result = api.request("GET", path, params=params, authenticated=args.command == "mine")
        if args.command in {"publish", "read", "edit"} and not result.get("not_modified"):
            if not result.get("id"):
                raise APIError(
                    502,
                    {
                        "code": "invalid_response",
                        "message": "Content result is missing its ID; preserve the original idempotency key",
                    },
                )
            result = content_links(result, server)
            if args.command == "read" and args.output:
                if not isinstance(result.get("text"), str) or result.get("deleted"):
                    raise RuntimeError("Withdrawn content has no Markdown body to export")
                data = result["text"].encode("utf-8")
                with args.output.open("xb") as destination:
                    destination.write(data)
                result = {
                    **{
                        key: result[key]
                        for key in ("id", "url", "api_url", "notice")
                        if key in result
                    },
                    "path": str(args.output.resolve()),
                    "size": len(data),
                    "etag": api.last_etag,
                }
        elif args.command in {"list", "search", "replies", "mine"}:
            result = {**result, "items": [content_links(item, server) for item in result["items"]]}
        if args.command in {"delete", "revoke-device"}:
            result = {
                **result,
                "id": str(args.id),
                "deleted" if args.command == "delete" else "revoked": True,
            }
        if args.command == "mail" and args.mail_command in {
            "folder-delete",
            "contact-delete",
            "rule-delete",
            "block",
            "unblock",
        }:
            result = {
                **result,
                "id": str(args.id),
                "blocked"
                if args.mail_command in {"block", "unblock"}
                else "deleted": args.mail_command != "unblock",
            }
        print(json.dumps(notice_output(result, api), ensure_ascii=False))
    except APIError as exc:
        print(
            json.dumps(
                notice_output(
                    {"error": exc.error, **({"notice": exc.notice} if exc.notice else {})}, api
                ),
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        raise SystemExit(1) from None
    except KeyboardInterrupt:
        print(
            json.dumps(
                notice_output({"error": {"code": "interrupted", "message": "Cancelled"}}, api),
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        raise SystemExit(130) from None
    except Exception as exc:
        # Avoid leaking transport URLs or accidental credential-bearing exception data.
        message = (
            str(exc)
            if isinstance(exc, RuntimeError)
            else f"Operation failed ({type(exc).__name__})"
        )
        print(
            json.dumps(
                notice_output({"error": {"code": "cli_error", "message": message}}, api),
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        raise SystemExit(1) from None
    finally:
        if api:
            api.close()
