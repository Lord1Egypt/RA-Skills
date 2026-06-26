#!/usr/bin/env python3
"""Cross-platform Microsoft To Do device-code auth helper."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


SCOPE = "https://graph.microsoft.com/Tasks.ReadWrite offline_access"


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        os.environ.setdefault(key, value)


def default_config_dir() -> Path:
    override = os.environ.get("MS_TODO_CONFIG_DIR")
    if override:
        return Path(override).expanduser()

    if os.name == "nt":
        base = os.environ.get("APPDATA")
        if base:
            return Path(base) / "microsoft-todo"
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "microsoft-todo"

    xdg = os.environ.get("XDG_CONFIG_HOME")
    if xdg:
        return Path(xdg) / "microsoft-todo"
    return Path.home() / ".config" / "microsoft-todo"


SCRIPT_DIR = Path(__file__).resolve().parent
load_dotenv(SCRIPT_DIR / ".env")

CONFIG_DIR = default_config_dir()
TENANT_FILE = Path(os.environ.get("MS_TODO_TENANT_FILE", CONFIG_DIR / "tenant_id"))
CLIENT_FILE = Path(os.environ.get("MS_TODO_CLIENT_FILE", CONFIG_DIR / "client_id"))
DEVICE_FILE = Path(os.environ.get("MS_TODO_DEVICE_FILE", CONFIG_DIR / "device_code.json"))
TOKEN_FILE = Path(os.environ.get("MS_TODO_TOKEN_FILE", CONFIG_DIR / "token.json"))


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def read_value(env_name: str, path: Path) -> str:
    value = os.environ.get(env_name)
    if value:
        return value.strip()
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    fail(f"missing {env_name} or {path}")


def tenant_id() -> str:
    return read_value("MS_TODO_TENANT_ID", TENANT_FILE)


def client_id() -> str:
    return read_value("MS_TODO_CLIENT_ID", CLIENT_FILE)


def post_form(url: str, data: dict[str, str]) -> dict:
    encoded = urllib.parse.urlencode(data).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=encoded,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(body, file=sys.stderr)
        raise SystemExit(exc.code) from exc
    return json.loads(body)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def summarize_payload(payload: dict, redact_tokens: bool) -> dict:
    if not redact_tokens:
        return payload

    redacted = dict(payload)
    for key in ("access_token", "refresh_token", "id_token"):
        if key in redacted:
            redacted[key] = "[redacted]"
    return redacted


def write_and_print_json(path: Path, payload: dict, *, redact_tokens: bool) -> None:
    write_json(path, payload)
    print(json.dumps(summarize_payload(payload, redact_tokens=redact_tokens), indent=2))


def load_json(path: Path, missing_hint: str) -> dict:
    if not path.exists():
        fail(f"missing {path}; {missing_hint}")
    return json.loads(path.read_text(encoding="utf-8"))


def command_device_code() -> None:
    payload = post_form(
        f"https://login.microsoftonline.com/{tenant_id()}/oauth2/v2.0/devicecode",
        {"client_id": client_id(), "scope": SCOPE},
    )
    write_and_print_json(DEVICE_FILE, payload, redact_tokens=False)


def command_poll_token() -> None:
    device_payload = load_json(DEVICE_FILE, "run 'device-code' first")
    payload = post_form(
        f"https://login.microsoftonline.com/{tenant_id()}/oauth2/v2.0/token",
        {
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "client_id": client_id(),
            "device_code": device_payload["device_code"],
        },
    )
    write_and_print_json(TOKEN_FILE, payload, redact_tokens=True)


def command_refresh_token() -> None:
    token_payload = load_json(TOKEN_FILE, "obtain a token first")
    refresh = token_payload.get("refresh_token")
    if not refresh:
        fail(f"refresh_token not found in {TOKEN_FILE}")
    payload = post_form(
        f"https://login.microsoftonline.com/{tenant_id()}/oauth2/v2.0/token",
        {
            "grant_type": "refresh_token",
            "client_id": client_id(),
            "refresh_token": refresh,
            "scope": SCOPE,
        },
    )
    write_and_print_json(TOKEN_FILE, payload, redact_tokens=True)


def command_access_token() -> None:
    token_payload = load_json(TOKEN_FILE, "obtain a token first")
    token = token_payload.get("access_token")
    if not token:
        fail(f"access_token not found in {TOKEN_FILE}")
    print(token)


def command_show_paths() -> None:
    print(
        json.dumps(
            {
                "config_dir": str(CONFIG_DIR),
                "tenant_file": str(TENANT_FILE),
                "client_file": str(CLIENT_FILE),
                "device_file": str(DEVICE_FILE),
                "token_file": str(TOKEN_FILE),
                "dotenv_file": str(SCRIPT_DIR / ".env"),
            },
            indent=2,
        )
    )


def main(argv: list[str]) -> int:
    commands = {
        "device-code": command_device_code,
        "poll-token": command_poll_token,
        "refresh-token": command_refresh_token,
        "access-token": command_access_token,
        "show-paths": command_show_paths,
    }

    if len(argv) != 2 or argv[1] not in commands:
        print(
            "usage: ms_todo_auth.py {device-code|poll-token|refresh-token|access-token|show-paths}",
            file=sys.stderr,
        )
        return 1

    commands[argv[1]]()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
