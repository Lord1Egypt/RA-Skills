"""Local credential storage and localized agent onboarding; no UI side effects."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any

from errors import CredentialRequiredError, ParamError


SUPPORTED_LOCALES = ("zh", "en")
REQUIRED_SCOPES = ("account:read", "task:write", "task:read")
KEY_ENV_NAMES = ("KRE_VIDEO_TRANSLATOR_API_KEY", "KRETRANS_API_KEY")
KEY_FILE_ENV_NAMES = ("KRE_VIDEO_TRANSLATOR_API_KEY_FILE", "KRETRANS_API_KEY_FILE")


def normalize_locale(value: str | None) -> str:
    locale = str(value or "").strip().lower().replace("_", "-").split("-", 1)[0]
    if not locale:
        return ""
    return "zh" if locale == "zh" else "en"


def key_files() -> tuple[Path, ...]:
    configured = [Path(value).expanduser() for name in KEY_FILE_ENV_NAMES if (value := os.getenv(name, "").strip())]
    if configured:
        return tuple(dict.fromkeys(configured))
    if os.name == "nt":
        base = Path(os.getenv("APPDATA") or Path.home() / "AppData" / "Roaming")
        return (base / "KreVideoTranslator" / "api_key", base / "KreTrans" / "api_key")
    base = Path(os.getenv("XDG_CONFIG_HOME") or Path.home() / ".config").expanduser()
    return (base / "kre-video-translator" / "api_key", base / "kretrans" / "api_key")


def _read_key_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return ""
    except (OSError, UnicodeError) as exc:
        raise ParamError(f"Unable to read API key file: {path}") from exc


def resolve_key() -> str:
    for name in KEY_ENV_NAMES:
        if value := os.getenv(name, "").strip():
            return value
    return next((value for path in key_files() if (value := _read_key_file(path))), "")


def status() -> dict[str, Any]:
    for name in KEY_ENV_NAMES:
        if os.getenv(name, "").strip():
            return {"configured": True, "source": "environment", "source_name": name}
    for path in key_files():
        if _read_key_file(path):
            return {"configured": True, "source": "file", "api_key_file": str(path.resolve())}
    return {"configured": False, "source": "none", "api_key_file": str(key_files()[0])}


def guidance(locale: str | None = "") -> dict[str, Any]:
    locale = normalize_locale(locale)
    if not locale:
        return {"error_code": "api_key_required", "locale": None, "message": "Pass --locale zh for Chinese or --locale en for other conversations."}
    registration_url = f"https://kretrans.com/{locale}/"
    api_key_url = f"https://kretrans.com/{locale}/app/developer/api-keys"
    if locale == "zh":
        message = (
            "当前还没有配置 Kre Video Translator API Key。\n\n请先完成以下步骤：\n"
            "1. 注册或登录 Kre Video Translator\n2. 创建 API Key\n3. 确认 Key 包含：\n"
            "   account:read\n   task:write\n   task:read\n\n"
            f"注册地址：[{registration_url}]({registration_url})\n"
            f"创建 Key：[{api_key_url}]({api_key_url})\n\n完成后请回复“已创建”。"
        )
    else:
        message = (
            "Kre Video Translator API key is not configured yet.\n\nPlease complete these steps:\n"
            "1. Register or sign in to Kre Video Translator\n2. Create an API key\n3. Confirm the key includes:\n"
            "   account:read\n   task:write\n   task:read\n\n"
            f"Registration URL: [{registration_url}]({registration_url})\n"
            f"API-key URL: [{api_key_url}]({api_key_url})\n\nWhen finished, reply \"Created\"."
        )
    return {
        "error_code": "api_key_required", "locale": locale, "message": message,
        "registration_url": registration_url, "api_key_url": api_key_url,
        "packages_url": f"https://kretrans.com/{locale}/app/account/packages",
        "docs_url": f"https://kretrans.com/{locale}/api",
        "required_scopes": list(REQUIRED_SCOPES),
    }


def require_key(locale: str | None = "") -> str:
    if key := resolve_key():
        return key
    raise CredentialRequiredError("API key is not configured.", locale=normalize_locale(locale))


def validate_key(value: str) -> str:
    secret = value.strip()
    if not secret or any(character.isspace() for character in secret):
        raise ParamError("API key must be a nonempty value without whitespace.")
    return secret


def write_key(value: str, output_path: Path | None = None) -> Path:
    secret = validate_key(value)
    path = (output_path or key_files()[0]).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(f"{secret}\n")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)
    return path.resolve()
