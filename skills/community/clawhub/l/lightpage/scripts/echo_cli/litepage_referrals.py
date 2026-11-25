"""Origin-scoped public referral codes; Python 3.6 compatible."""

import json
import os
import re
import tempfile
from pathlib import Path

from echo_cli.compat import subparsers
from echo_cli.credentials import atomic_json, digest


def path(api):
    return api.store.path.parent / ("referral-" + digest(api.server) + ".json")


def code_path(api):
    # Explicit credential directories also isolate tests and alternate installations.
    credentials = api.store.path.parent
    default_credentials = Path("~/.config/litepage").expanduser()
    root = (
        Path(os.environ["LITEPAGE_CACHE_DIR"]).expanduser()
        if os.getenv("LITEPAGE_CACHE_DIR")
        else (
            Path("~/.cache/lightpage").expanduser()
            if credentials == default_credentials and not os.getenv("LITEPAGE_CONFIG_DIR")
            else credentials / "cache" / "lightpage"
        )
    )
    if api.server != "https://lightpage.hqdx.store":
        root = root / "servers" / digest(api.server)
    return root / "lp_ref"


def public_code(value):
    value = value.strip()
    if value.startswith("lp_ref="):
        value = value[len("lp_ref=") :]
    return (
        value
        if re.fullmatch(r"(?:[a-z0-9]{10}|[A-Za-z0-9]{8}|[A-Za-z0-9_-]{24,32})", value)
        else None
    )


def read_code(api):
    target = code_path(api)
    if target.is_symlink() or target.parent.is_symlink() or not target.is_file():
        return None
    if target.stat().st_size > 128:
        return None
    try:
        return public_code(target.read_text(encoding="utf-8"))
    except (OSError, UnicodeError):
        return None


def save_code(api, code):
    target = code_path(api)
    if target.is_symlink() or target.parent.is_symlink():
        raise RuntimeError("Referral source must not be a symlink")
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, temporary = tempfile.mkstemp(dir=str(target.parent), prefix=".lp-ref-")
    try:
        with os.fdopen(fd, "w") as output:
            output.write(code + "\n")
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, str(target))
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def load(api):
    target = path(api)
    if not target.exists():
        code = read_code(api)
        return {"server": api.server, "lp_ref": code, "status": "pending"} if code else None
    if target.is_symlink() or target.stat().st_mode & 0o077 or target.stat().st_size > 8192:
        raise RuntimeError("Referral source must be a bounded private file, not a symlink")
    value = json.loads(target.read_text())
    if value.get("server") != api.server:
        raise RuntimeError("Referral source belongs to another server")
    return value


def pending(api):
    with api.store.lock():
        value = load(api)
        if value and not path(api).exists():
            # Freeze the first source before registration, including manually written files.
            atomic_json(path(api), value)
        return (
            (value.get("lp_ref") or value.get("receipt"))
            if value and value.get("status") == "pending"
            else None
        )


def fields(value):
    if not value:
        return {}
    return {
        "lp_ref"
        if re.fullmatch(r"(?:[a-z0-9]{10}|[A-Za-z0-9]{8}|[A-Za-z0-9_-]{24,32})", value)
        else "referral_receipt": value
    }


def acknowledge(api, receipt, status):
    with api.store.lock():
        value = load(api)
        if value and (value.get("lp_ref") or value.get("receipt")) == receipt:
            value["status"] = status
            atomic_json(path(api), value)


def commands(root):
    referral = root.add_parser("referral", help="Save install source or manage promotion")
    actions = subparsers(referral, dest="referral_command")
    source = actions.add_parser(
        "source", help="Save the lp_ref promotion code locally; no network or login"
    )
    source.add_argument("receipt")
    actions.add_parser("status", help="Read local referral handoff status without credentials")
    link = actions.add_parser("link", help="Get your stable platform or work promotion link")
    link.add_argument("--site-id")
    link.add_argument("--parent-code")
    configure = actions.add_parser("configure", help="Enable or pause promotion for your work")
    configure.add_argument("site_id")
    configure.add_argument("--enabled", choices=["true", "false"], required=True)
    for name in ("links", "report"):
        listing = actions.add_parser(name)
        listing.add_argument("--cursor")
        listing.add_argument("--limit", type=int, default=10)
        if name == "report":
            listing.add_argument("--site-id")


def execute(api, args, ensure_identity):
    command = args.referral_command
    if command == "source":
        value_to_save = args.receipt
        if value_to_save.startswith("lp_ref="):
            value_to_save = value_to_save[len("lp_ref=") :]
        is_code = bool(public_code(value_to_save))
        if is_code:
            value_to_save = public_code(value_to_save)
        if not is_code and not (
            64 <= len(value_to_save) <= 2048 and re.fullmatch(r"[A-Za-z0-9_=-]+", value_to_save)
        ):
            raise RuntimeError("Use the lp_ref promotion code from the sharing link")
        with api.store.lock():
            value = load(api)
            # A second installation cannot silently replace the first local source.
            if value:
                return {"saved": False, "status": value["status"], "reason": "source_already_saved"}
            if is_code:
                save_code(api, value_to_save)
            atomic_json(
                path(api),
                {
                    "server": api.server,
                    "lp_ref" if is_code else "receipt": value_to_save,
                    "status": "pending",
                },
            )
        return {"saved": True, "status": "pending"}
    if command == "status":
        with api.store.lock():
            value = load(api)
        return {"status": value["status"] if value else "none"}
    if command == "link":
        ensure_identity(api)
        return api.request(
            "POST",
            "/v1/hosting/referrals/links",
            authenticated=True,
            json={"site_id": args.site_id, "parent_code": args.parent_code},
        )
    if command == "configure":
        return api.request(
            "PUT",
            "/v1/hosting/referrals/sites/" + args.site_id,
            authenticated=True,
            json={"enabled": args.enabled == "true"},
        )
    if not 1 <= args.limit <= 20:
        raise RuntimeError("Use a page size from 1 to 20")
    params = {"limit": args.limit}
    if args.cursor:
        params["cursor"] = args.cursor
    if command == "report" and args.site_id:
        params["site_id"] = args.site_id
    return api.request("GET", "/v1/hosting/referrals/" + command, authenticated=True, params=params)
