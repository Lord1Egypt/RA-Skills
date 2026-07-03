#!/usr/bin/env python3
"""Keeper credential broker for a user-facing agent.

This skill lets a user-facing agent authenticate to the user's Keeper vault
via **Keeper Secrets Manager (KSM)** and then hand specific credentials to
*other* agents (service agents / drive thrus) to fulfil a request.

KSM is zero-knowledge and **scoped**: the agent can only ever read the records
in shared folders the user explicitly granted to the KSM Application. It never
sees the master password and never gets the whole vault.

Authentication model (NOT classic OAuth)
-----------------------------------------
The "user completion" step is a one-time bootstrap the user performs in their
Keeper Web Vault / Commander:
  1. Create a Secrets Manager Application.
  2. Share the folder(s) holding the credentials they want the agent to use.
  3. Generate a **One-Time Access Token** and hand it to the agent once.
The token initialises a device and is exchanged for a local `ksm-config.json`
(app key + EC private key + client id). After that, the config alone
authenticates and the token is useless. Persist the config dir across sessions
and the agent re-authenticates silently forever.

Delivery modes (how a credential reaches the OTHER agent)
---------------------------------------------------------
  share      Mint a Keeper **One-Time Share** link (time-limited, single-use)
             and pass the LINK in the conversation. The secret value travels
             out-of-band and never lands in the chat transcript. This is the
             most secure mode but REQUIRES a Keeper Commander session
             (KSM SDK cannot create one-time shares) -- see `references/`.
  reference  Pass a Keeper Notation reference (keeper://UID/field/password).
             The value never enters the transcript; the receiving agent must
             have its own KSM access to the same shared folder. Pure KSM.
  inline     Fetch the value and put it directly in the message. Simplest, but
             the raw credential lands in both agents' transcripts/logs. Use
             only when the peer cannot consume a link, with user confirmation.

Subcommands
-----------
  init                 One-time KSM bootstrap from a One-Time Access Token.
  status               Verify the stored config works (silent). Never values.
  list                 List accessible records (uid/title/type/field names).
                       NEVER prints secret values.
  get <ref> [--field]  Fetch a credential VALUE (sensitive; for inline mode).
  notation <query>     Resolve raw Keeper Notation (keeper://UID/field/...).
  share <ref>          Mint a One-Time Share link (needs Commander).
  package <ref>        Build a ready-to-send delivery payload in a chosen mode
                       (share|reference|inline) for the agent to pass to the
                       peer via the Knoxville send_message tool.
  logout               Delete the stored KSM config.

Environment
-----------
  KEEPER_SKILL_HOME        Persistent dir for ksm-config.json.
                           Default: $XDG_CONFIG_HOME/keeper-credentials
                           or ~/.config/keeper-credentials
  KEEPER_KSM_TOKEN         One-Time Access Token for `init` (alt to --token).
  KEEPER_COMMANDER_CONFIG  Path to a Keeper Commander persistent-login config
                           used by `share` to mint One-Time Share links.
  KEEPER_OTS_DEFAULT_EXPIRE  Default One-Time Share lifetime (e.g. 60m, 1h, 7d).
                           Default: 60m
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

CONFIG_FILENAME = "ksm-config.json"
DEFAULT_OTS_EXPIRE = "60m"


# --------------------------------------------------------------------------- #
# Output helpers
# --------------------------------------------------------------------------- #
def _emit(payload: dict) -> None:
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")


def _ok(payload: dict) -> int:
    _emit(payload)
    return 0


def _fail(error: str, message: str, code: int = 1, **extra) -> int:
    _emit({"error": error, "message": message, **extra})
    return code


# --------------------------------------------------------------------------- #
# Persistence
# --------------------------------------------------------------------------- #
def skill_home() -> Path:
    env = os.environ.get("KEEPER_SKILL_HOME")
    if env:
        return Path(env).expanduser()
    xdg = os.environ.get("XDG_CONFIG_HOME")
    base = Path(xdg).expanduser() if xdg else Path.home() / ".config"
    return base / "keeper-credentials"


def config_path() -> Path:
    return skill_home() / CONFIG_FILENAME


def _ensure_home() -> Path:
    home = skill_home()
    home.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(home, 0o700)
    except OSError:
        pass
    return home


# --------------------------------------------------------------------------- #
# KSM SDK
# --------------------------------------------------------------------------- #
def _import_ksm():
    """Import the KSM core SDK or raise a clean, actionable error."""
    try:
        from keeper_secrets_manager_core import SecretsManager
        from keeper_secrets_manager_core.storage import FileKeyValueStorage
    except ImportError as e:  # pragma: no cover - environment dependent
        raise RuntimeError(
            "keeper-secrets-manager-core is not installed. Install it with "
            "`uv pip install keeper-secrets-manager-core` (or pip)."
        ) from e
    return SecretsManager, FileKeyValueStorage


def _secrets_manager(token: str | None = None):
    """Build a SecretsManager. With a token it bootstraps the config; without
    one it loads the persisted config (silent auth)."""
    SecretsManager, FileKeyValueStorage = _import_ksm()
    storage = FileKeyValueStorage(str(config_path()))
    if token:
        return SecretsManager(token=token, config=storage)
    return SecretsManager(config=storage)


def _field_names(record) -> dict:
    """Field/custom labels present on a record -- NEVER their values."""
    raw = getattr(record, "dict", {}) or {}

    def names(items):
        out = []
        for f in items or []:
            label = f.get("label") or f.get("type")
            if label:
                out.append(label)
        return out

    return {
        "fields": names(raw.get("fields")),
        "custom": names(raw.get("custom")),
        "files": [f.get("name") or f.get("title") for f in (raw.get("files") or [])],
    }


def _record_summary(record) -> dict:
    return {
        "uid": getattr(record, "uid", None),
        "title": getattr(record, "title", None),
        "type": getattr(record, "type", None),
        **_field_names(record),
    }


def _resolve_record(sm, ref: str):
    """Resolve a record by UID first, then by exact title."""
    # UID lookup
    try:
        recs = sm.get_secrets([ref])
    except Exception:
        recs = []
    if recs:
        return recs[0]
    # Title lookup
    try:
        rec = sm.get_secret_by_title(ref)
    except Exception:
        rec = None
    return rec


def _single(value):
    """KSM field accessors return lists; pull the single useful value."""
    if isinstance(value, list):
        return value[0] if value else None
    return value


# --------------------------------------------------------------------------- #
# Commander bridge (One-Time Share)
# --------------------------------------------------------------------------- #
_URL_RE = re.compile(r"https://\S+")


def _commander_one_time_share(record_uid: str, expire: str) -> str:
    """Mint a One-Time Share link via the Keeper Commander CLI.

    KSM has no one-time-share API, so we shell out to Commander running in
    non-interactive command mode against a persistent-login config. Returns the
    share URL parsed from Commander's output.
    """
    config = os.environ.get("KEEPER_COMMANDER_CONFIG")
    if not config:
        raise RuntimeError(
            "One-Time Share requires Keeper Commander. Set KEEPER_COMMANDER_CONFIG "
            "to a Commander persistent-login config.json, or use --mode reference / "
            "--mode inline instead."
        )
    if not Path(config).expanduser().exists():
        raise RuntimeError(f"KEEPER_COMMANDER_CONFIG does not exist: {config}")
    binary = shutil.which("keeper")
    if not binary:
        raise RuntimeError(
            "The `keeper` (Commander) CLI is not on PATH. Install it with "
            "`uv pip install keepercommander`, or use --mode reference / inline."
        )
    cmd = [
        binary,
        "--config",
        str(Path(config).expanduser()),
        "one-time-share",
        "create",
        "--expire",
        expire,
        record_uid,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        raise RuntimeError(
            "Commander one-time-share failed: "
            f"{(proc.stderr or proc.stdout).strip()[:500]}"
        )
    match = _URL_RE.search(proc.stdout) or _URL_RE.search(proc.stderr)
    if not match:
        raise RuntimeError(
            "Commander did not return a share URL. Output: "
            f"{proc.stdout.strip()[:500]}"
        )
    return match.group(0)


# --------------------------------------------------------------------------- #
# Commands
# --------------------------------------------------------------------------- #
def cmd_init(args) -> int:
    token = args.token or os.environ.get("KEEPER_KSM_TOKEN")
    if not token:
        return _fail(
            "missing_token",
            "Provide the One-Time Access Token via --token or KEEPER_KSM_TOKEN. "
            "Generate it in the Keeper Web Vault (Secrets Manager > your "
            "Application > Add Device) or with Commander "
            "`secrets-manager client add`.",
            code=2,
        )
    _ensure_home()
    try:
        sm = _secrets_manager(token=token)
        # A first call binds the device and rewrites config without the token.
        records = sm.get_secrets([])
    except RuntimeError as e:
        return _fail("sdk_error", str(e))
    except Exception as e:  # noqa: BLE001 - normalize SDK exceptions
        return _fail(
            "init_failed",
            f"{type(e).__name__}: {e}. The token may be expired, already used, "
            "or for the wrong region (prefix like US:/EU:).",
            code=2,
        )
    path = config_path()
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    print(
        f"\nKSM device bound. Config written to {path}. Persist this directory "
        "across sessions so the agent re-authenticates silently.",
        file=sys.stderr,
    )
    return _ok(
        {
            "status": "authenticated",
            "config_path": str(path),
            "accessible_records": len(records),
        }
    )


def _require_config() -> int | None:
    if not config_path().exists():
        return _fail(
            "not_authenticated",
            f"No KSM config at {config_path()}. Run `init` with a One-Time "
            "Access Token first.",
            code=2,
        )
    return None


def cmd_status(args) -> int:
    miss = _require_config()
    if miss is not None:
        return miss
    try:
        sm = _secrets_manager()
        records = sm.get_secrets([])
    except RuntimeError as e:
        return _fail("sdk_error", str(e))
    except Exception as e:  # noqa: BLE001
        return _fail(
            "reauth_required",
            f"{type(e).__name__}: {e}. The config may be revoked; re-run `init`.",
            code=2,
        )
    return _ok(
        {
            "status": "authenticated",
            "config_path": str(config_path()),
            "accessible_records": len(records),
        }
    )


def cmd_list(args) -> int:
    miss = _require_config()
    if miss is not None:
        return miss
    try:
        sm = _secrets_manager()
        records = sm.get_secrets([])
    except RuntimeError as e:
        return _fail("sdk_error", str(e))
    except Exception as e:  # noqa: BLE001
        return _fail("reauth_required", f"{type(e).__name__}: {e}", code=2)
    summaries = [_record_summary(r) for r in records]
    if args.type:
        summaries = [s for s in summaries if s.get("type") == args.type]
    return _ok({"count": len(summaries), "records": summaries})


def cmd_get(args) -> int:
    miss = _require_config()
    if miss is not None:
        return miss
    try:
        sm = _secrets_manager()
        record = _resolve_record(sm, args.ref)
    except RuntimeError as e:
        return _fail("sdk_error", str(e))
    except Exception as e:  # noqa: BLE001
        return _fail("reauth_required", f"{type(e).__name__}: {e}", code=2)
    if record is None:
        return _fail("not_found", f"No record matching '{args.ref}'.", code=1)

    out: dict = {"uid": record.uid, "title": record.title, "type": record.type}
    try:
        if args.field:
            out["field"] = args.field
            out["value"] = _single(record.field(args.field, single=True))
        else:
            # Default to login + password if present.
            login = _single(record.field("login", single=True))
            password = _single(record.field("password", single=True))
            out["login"] = login
            out["password"] = password
    except Exception as e:  # noqa: BLE001
        return _fail("field_error", f"Could not read field: {e}", code=1)
    out["_sensitive"] = "Contains secret values. Do not log; deliver carefully."
    return _ok(out)


def cmd_notation(args) -> int:
    miss = _require_config()
    if miss is not None:
        return miss
    try:
        sm = _secrets_manager()
        values = sm.get_notation(args.query)
    except RuntimeError as e:
        return _fail("sdk_error", str(e))
    except Exception as e:  # noqa: BLE001
        return _fail("notation_error", f"{type(e).__name__}: {e}", code=1)
    return _ok(
        {
            "query": args.query,
            "values": values,
            "_sensitive": "May contain secret values. Do not log.",
        }
    )


def cmd_share(args) -> int:
    miss = _require_config()
    if miss is not None:
        return miss
    try:
        sm = _secrets_manager()
        record = _resolve_record(sm, args.ref)
    except RuntimeError as e:
        return _fail("sdk_error", str(e))
    except Exception as e:  # noqa: BLE001
        return _fail("reauth_required", f"{type(e).__name__}: {e}", code=2)
    if record is None:
        return _fail("not_found", f"No record matching '{args.ref}'.", code=1)
    expire = args.expire or os.environ.get("KEEPER_OTS_DEFAULT_EXPIRE", DEFAULT_OTS_EXPIRE)
    try:
        url = _commander_one_time_share(record.uid, expire)
    except RuntimeError as e:
        return _fail("share_unavailable", str(e), code=1)
    return _ok(
        {
            "uid": record.uid,
            "title": record.title,
            "expire": expire,
            "one_time_share_url": url,
        }
    )


def cmd_package(args) -> int:
    """Build a delivery payload + suggested message for the chosen mode.

    This does NOT send anything. The agent takes the returned `payload` /
    `suggested_message` and delivers it via the Knoxville `send_message` tool
    on the relevant conversation.
    """
    miss = _require_config()
    if miss is not None:
        return miss
    try:
        sm = _secrets_manager()
        record = _resolve_record(sm, args.ref)
    except RuntimeError as e:
        return _fail("sdk_error", str(e))
    except Exception as e:  # noqa: BLE001
        return _fail("reauth_required", f"{type(e).__name__}: {e}", code=2)
    if record is None:
        return _fail("not_found", f"No record matching '{args.ref}'.", code=1)

    purpose = args.purpose or "to authenticate the requested action"
    base = {"uid": record.uid, "title": record.title, "type": record.type, "mode": args.mode}

    if args.mode == "share":
        expire = args.expire or os.environ.get(
            "KEEPER_OTS_DEFAULT_EXPIRE", DEFAULT_OTS_EXPIRE
        )
        try:
            url = _commander_one_time_share(record.uid, expire)
        except RuntimeError as e:
            return _fail("share_unavailable", str(e), code=1)
        base["payload"] = {"one_time_share_url": url, "expire": expire}
        base["suggested_message"] = (
            f"Here is a one-time, time-limited Keeper share link ({expire}) for "
            f"the credential you need {purpose}: {url} . Open it once to retrieve "
            "the secret; it cannot be reused."
        )
        base["_sensitive"] = "URL grants one-time access to a secret. Send only to the intended agent."

    elif args.mode == "reference":
        field = args.field or "password"
        notation = f"keeper://{record.uid}/field/{field}"
        base["payload"] = {"keeper_notation": notation, "field": field}
        base["suggested_message"] = (
            f"Resolve this credential {purpose} from your own Keeper Secrets "
            f"Manager access to the shared folder: {notation}"
        )
        base["note"] = (
            "The receiving agent must have its own KSM access to the same shared "
            "folder for this reference to resolve."
        )

    elif args.mode == "inline":
        field = args.field
        try:
            if field:
                value = _single(record.field(field, single=True))
                base["payload"] = {field: value}
            else:
                base["payload"] = {
                    "login": _single(record.field("login", single=True)),
                    "password": _single(record.field("password", single=True)),
                }
        except Exception as e:  # noqa: BLE001
            return _fail("field_error", f"Could not read field: {e}", code=1)
        base["suggested_message"] = (
            f"Credentials {purpose}: " + json.dumps(base["payload"])
        )
        base["_sensitive"] = (
            "Raw secret will appear in the conversation transcript of both "
            "agents. Confirm with the user before sending inline."
        )
    else:  # pragma: no cover - argparse restricts choices
        return _fail("bad_mode", f"Unknown mode '{args.mode}'.", code=1)

    return _ok(base)


def cmd_logout(args) -> int:
    path = config_path()
    removed = []
    if path.exists():
        path.unlink()
        removed.append(str(path))
    return _ok({"status": "logged_out", "removed": removed})


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Keeper credential broker (KSM).")
    sub = p.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("init", help="One-time KSM bootstrap from a One-Time Access Token.")
    sp.add_argument("--token", help="One-Time Access Token (alt: KEEPER_KSM_TOKEN).")
    sp.set_defaults(func=cmd_init)

    sp = sub.add_parser("status", help="Verify stored KSM config (silent).")
    sp.set_defaults(func=cmd_status)

    sp = sub.add_parser("list", help="List accessible records (no secret values).")
    sp.add_argument("--type", help="Filter by record type (e.g. login).")
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser("get", help="Fetch a credential value (sensitive).")
    sp.add_argument("ref", help="Record UID or exact title.")
    sp.add_argument("--field", help="Field to read (default: login + password).")
    sp.set_defaults(func=cmd_get)

    sp = sub.add_parser("notation", help="Resolve raw Keeper Notation.")
    sp.add_argument("query", help="e.g. keeper://UID/field/password or UID/field/password")
    sp.set_defaults(func=cmd_notation)

    sp = sub.add_parser("share", help="Mint a One-Time Share link (needs Commander).")
    sp.add_argument("ref", help="Record UID or exact title.")
    sp.add_argument("--expire", help="Lifetime, e.g. 60m, 1h, 7d (default: env or 60m).")
    sp.set_defaults(func=cmd_share)

    sp = sub.add_parser("package", help="Build a delivery payload for a peer agent.")
    sp.add_argument("ref", help="Record UID or exact title.")
    sp.add_argument(
        "--mode",
        choices=["share", "reference", "inline"],
        default="share",
        help="Delivery mode (default: share).",
    )
    sp.add_argument("--field", help="Specific field for reference/inline modes.")
    sp.add_argument("--expire", help="Share lifetime for --mode share.")
    sp.add_argument("--purpose", help="Short human reason, woven into the suggested message.")
    sp.set_defaults(func=cmd_package)

    sp = sub.add_parser("logout", help="Delete the stored KSM config.")
    sp.set_defaults(func=cmd_logout)

    return p


def main() -> int:
    args = build_parser().parse_args()
    try:
        return args.func(args)
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
