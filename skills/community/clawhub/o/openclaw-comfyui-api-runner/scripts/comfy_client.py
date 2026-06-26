"""
Shared HTTP client for ComfyUI.
Loads connection settings from env plus a small user config file.

Supported env vars:
- COMFYUI_PROFILE
- COMFYUI_BASE_URL
- COMFYUI_PORT
- COMFYUI_API_KEY
- COMFYUI_USERNAME
- COMFYUI_PASSWORD
"""

from __future__ import annotations

import base64
import json
import os
import uuid
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import urllib.error
import urllib.request

DEFAULT_PORT = 8188
DEFAULT_BASE = "http://127.0.0.1"
TIMEOUT = 120
USER_CONFIG_PATH = Path.home() / ".config" / "openclaw" / "comfyui-runner.json"


def _load_json(path: Path) -> dict[str, Any]:
    try:
        if not path.is_file():
            return {}
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def _save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def _load_user_config() -> dict[str, Any]:
    cfg = _load_json(USER_CONFIG_PATH)
    cfg.setdefault("active_profile", None)
    cfg.setdefault("default_server", None)
    cfg.setdefault("default_workflow", None)
    cfg.setdefault("profiles", {})
    cfg.setdefault("servers", [])
    if not isinstance(cfg["profiles"], dict):
        cfg["profiles"] = {}
    if not isinstance(cfg["servers"], list):
        cfg["servers"] = []
    return cfg


def _sanitize_port(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return DEFAULT_PORT


def _pick_profile(cfg: dict[str, Any]) -> dict[str, Any]:
    profiles = cfg.get("profiles") if isinstance(cfg.get("profiles"), dict) else {}
    selected = (
        os.environ.get("COMFYUI_SERVER")
        or os.environ.get("COMFYUI_PROFILE")
        or cfg.get("default_server")
        or cfg.get("active_profile")
    )
    if selected and isinstance(profiles, dict):
        profile = profiles.get(str(selected))
        if isinstance(profile, dict):
            return profile
    servers = cfg.get("servers") if isinstance(cfg.get("servers"), list) else []
    if selected:
        for server in servers:
            if isinstance(server, dict) and str(server.get("name") or "") == str(selected):
                return server
    return {}


def resolve_config(skill_root: Path | None = None) -> dict[str, Any]:
    """Resolve effective connection settings, env overrides profile file."""
    user_cfg = _load_user_config()
    profile_cfg = _pick_profile(user_cfg)

    base_url = (
        os.environ.get("COMFYUI_BASE_URL")
        or profile_cfg.get("base_url")
        or user_cfg.get("base_url")
        or DEFAULT_BASE
    )
    port = _sanitize_port(
        os.environ.get("COMFYUI_PORT")
        or profile_cfg.get("port")
        or user_cfg.get("port")
        or DEFAULT_PORT
    )
    api_key = os.environ.get("COMFYUI_API_KEY") or profile_cfg.get("api_key") or user_cfg.get("api_key")
    username = os.environ.get("COMFYUI_USERNAME") or profile_cfg.get("username") or user_cfg.get("username")
    password = os.environ.get("COMFYUI_PASSWORD") or profile_cfg.get("password") or user_cfg.get("password")
    active_profile = os.environ.get("COMFYUI_PROFILE") or user_cfg.get("active_profile")
    default_server = os.environ.get("COMFYUI_SERVER") or user_cfg.get("default_server") or active_profile
    default_workflow = user_cfg.get("default_workflow")

    return {
        "base_url": base_url,
        "port": port,
        "api_key": api_key,
        "username": username,
        "password": password,
        "active_profile": active_profile,
        "default_server": default_server,
        "default_workflow": default_workflow,
        "user_config_path": str(USER_CONFIG_PATH),
    }


def get_base_url(skill_root: Path | None = None) -> str:
    """Return full base URL (e.g. http://127.0.0.1:8188)."""
    cfg = resolve_config(skill_root)
    base = str(cfg["base_url"] or "").rstrip("/")
    port = int(cfg["port"] or DEFAULT_PORT)
    if ":" in base.split("//", 1)[-1]:
        return base
    return f"{base}:{port}"


def _build_headers(api_key: str | None) -> dict[str, str]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def _install_basic_auth(req: urllib.request.Request, username: str | None, password: str | None) -> None:
    if username and password:
        creds = base64.b64encode(f"{username}:{password}".encode()).decode()
        req.add_header("Authorization", f"Basic {creds}")


def _request(
    method: str,
    path: str,
    data: dict[str, Any] | None = None,
    skill_root: Path | None = None,
) -> dict[str, Any] | list[Any]:
    cfg = resolve_config(skill_root)
    base = get_base_url(skill_root)
    url = urljoin(base + "/", path.lstrip("/"))
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body, headers=_build_headers(cfg.get("api_key")), method=method)
    _install_basic_auth(req, cfg.get("username"), cfg.get("password"))
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read().decode("utf-8")
            if not raw:
                return {}
            parsed = json.loads(raw)
            return parsed if isinstance(parsed, (dict, list)) else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        try:
            err_json = json.loads(body) if body else {}
        except json.JSONDecodeError:
            err_json = {"message": body or e.reason}
        raise ComfyAPIError(e.code, err_json) from e
    except urllib.error.URLError as e:
        raise ComfyAPIError(0, {"message": str(e.reason) or "Connection failed"}) from e
    except json.JSONDecodeError as e:
        raise ComfyAPIError(0, {"message": f"Invalid JSON: {e}"}) from e


class ComfyAPIError(Exception):
    """ComfyUI API HTTP or response error."""

    def __init__(self, code: int, body: dict[str, Any]) -> None:
        self.code = code
        self.body = body
        super().__init__(f"ComfyUI API error {code}: {body}")


def list_profiles() -> dict[str, Any]:
    cfg = _load_user_config()
    profiles = cfg.get("profiles") if isinstance(cfg.get("profiles"), dict) else {}
    servers = cfg.get("servers") if isinstance(cfg.get("servers"), list) else []
    return {
        "active_profile": cfg.get("active_profile"),
        "default_server": cfg.get("default_server"),
        "default_workflow": cfg.get("default_workflow"),
        "profiles": {name: profile for name, profile in sorted(profiles.items()) if isinstance(profile, dict)},
        "servers": [server for server in servers if isinstance(server, dict)],
        "config_path": str(USER_CONFIG_PATH),
    }


def save_profile(name: str, profile: dict[str, Any], set_active: bool = True) -> dict[str, Any]:
    if not name or not name.strip():
        raise ValueError("Profile name is required")
    cfg = _load_user_config()
    profiles = cfg.setdefault("profiles", {})
    if not isinstance(profiles, dict):
        profiles = {}
        cfg["profiles"] = profiles
    profiles[name] = {
        "name": name,
        "base_url": profile.get("base_url") or DEFAULT_BASE,
        "port": _sanitize_port(profile.get("port") or DEFAULT_PORT),
        **({"api_key": profile["api_key"]} if profile.get("api_key") else {}),
        **({"username": profile["username"]} if profile.get("username") else {}),
        **({"password": profile["password"]} if profile.get("password") else {}),
    }
    servers = cfg.setdefault("servers", [])
    if not isinstance(servers, list):
        servers = []
        cfg["servers"] = servers
    servers = [s for s in servers if not (isinstance(s, dict) and str(s.get("name") or "") == name)]
    servers.append(profiles[name])
    cfg["servers"] = servers
    if set_active:
        cfg["active_profile"] = name
        cfg["default_server"] = name
    _save_json(USER_CONFIG_PATH, cfg)
    return list_profiles()


def delete_profile(name: str) -> dict[str, Any]:
    cfg = _load_user_config()
    profiles = cfg.get("profiles") if isinstance(cfg.get("profiles"), dict) else {}
    servers = cfg.get("servers") if isinstance(cfg.get("servers"), list) else []
    if name in profiles:
        del profiles[name]
    cfg["servers"] = [s for s in servers if not (isinstance(s, dict) and str(s.get("name") or "") == name)]
    if cfg.get("active_profile") == name:
        cfg["active_profile"] = None
    if cfg.get("default_server") == name:
        cfg["default_server"] = None
    _save_json(USER_CONFIG_PATH, cfg)
    return list_profiles()


def set_active_profile(name: str) -> dict[str, Any]:
    cfg = _load_user_config()
    profiles = cfg.get("profiles") if isinstance(cfg.get("profiles"), dict) else {}
    if name not in profiles:
        raise KeyError(f"Profile not found: {name}")
    cfg["active_profile"] = name
    cfg["default_server"] = name
    _save_json(USER_CONFIG_PATH, cfg)
    return list_profiles()


def set_default_server(name: str) -> dict[str, Any]:
    cfg = _load_user_config()
    profiles = cfg.get("profiles") if isinstance(cfg.get("profiles"), dict) else {}
    servers = cfg.get("servers") if isinstance(cfg.get("servers"), list) else []
    if name not in profiles and not any(isinstance(s, dict) and str(s.get("name") or "") == name for s in servers):
        raise KeyError(f"Server not found: {name}")
    cfg["default_server"] = name
    _save_json(USER_CONFIG_PATH, cfg)
    return list_profiles()


def set_default_workflow(name: str) -> dict[str, Any]:
    cfg = _load_user_config()
    cfg["default_workflow"] = name
    _save_json(USER_CONFIG_PATH, cfg)
    return list_profiles()


def post_prompt(workflow: dict[str, Any], client_id: str | None = None, skill_root: Path | None = None) -> dict[str, Any]:
    """POST /prompt — submit workflow. Returns { prompt_id, number } or error."""
    payload: dict[str, Any] = {"prompt": workflow}
    if client_id is None:
        client_id = str(uuid.uuid4())
    payload["client_id"] = client_id
    out = _request("POST", "/prompt", data=payload, skill_root=skill_root)
    return out if isinstance(out, dict) else {"prompt_id": None, "number": 0}


def get_prompt(skill_root: Path | None = None) -> dict[str, Any]:
    out = _request("GET", "/prompt", skill_root=skill_root)
    return out if isinstance(out, dict) else {}


def get_history(prompt_id: str | None = None, skill_root: Path | None = None) -> dict[str, Any]:
    path = f"/history/{prompt_id}" if prompt_id else "/history"
    out = _request("GET", path, skill_root=skill_root)
    return out if isinstance(out, dict) else {}


def get_queue(skill_root: Path | None = None) -> dict[str, Any]:
    out = _request("GET", "/queue", skill_root=skill_root)
    return out if isinstance(out, dict) else {}


def health_check(skill_root: Path | None = None) -> dict[str, Any]:
    base_url = get_base_url(skill_root)
    try:
        queue_data = get_queue(skill_root=skill_root)
        return {
            "ok": True,
            "base_url": base_url,
            "message": "ComfyUI server is reachable and API responds; generation is possible.",
            "queue_info": queue_data,
        }
    except ComfyAPIError as e:
        return {
            "ok": False,
            "base_url": base_url,
            "message": e.body.get("message", str(e)),
            "code": e.code,
        }


def clear_queue(skill_root: Path | None = None) -> dict[str, Any]:
    out = _request("POST", "/queue", data={"clear": True}, skill_root=skill_root)
    return out if isinstance(out, dict) else {}


def interrupt(skill_root: Path | None = None) -> dict[str, Any]:
    out = _request("POST", "/interrupt", skill_root=skill_root)
    return out if isinstance(out, dict) else {}


def fetch_url(url: str, skill_root: Path | None = None) -> bytes:
    cfg = resolve_config(skill_root)
    req = urllib.request.Request(url, method="GET")
    for name, value in _build_headers(cfg.get("api_key")).items():
        req.add_header(name, value)
    _install_basic_auth(req, cfg.get("username"), cfg.get("password"))
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read()
