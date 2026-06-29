from __future__ import annotations

import base64
import os
from urllib.parse import quote

import requests


GITEA_URL = os.getenv("GITEA_URL", "").rstrip("/")
ADMIN_TOKEN = os.getenv("GITEA_ADMIN_TOKEN", "")
BOT_USERNAME = os.getenv("GITEA_BOT_USERNAME", "AIFusionBot")


class GiteaError(RuntimeError):
    pass


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"token {ADMIN_TOKEN}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def _repo(owner: str, repo: str) -> str:
    return f"{quote(owner, safe='')}/{quote(repo, safe='')}"


def _path(path: str) -> str:
    return "/".join(quote(part, safe="") for part in path.split("/") if part)


def api(method: str, path: str, *, json_body=None, ok=(200, 201, 204)) -> object:
    if not GITEA_URL or not ADMIN_TOKEN:
        raise GiteaError("GITEA_URL and GITEA_ADMIN_TOKEN are required")
    response = requests.request(method, f"{GITEA_URL}{path}", headers=_headers(), json=json_body, timeout=60)
    if response.status_code not in ok:
        raise GiteaError(f"Gitea {method} {path} failed: {response.status_code} {response.text[:500]}")
    if not response.text:
        return {}
    return response.json()


def get_file(owner: str, repo: str, path: str) -> dict | None:
    try:
        return api("GET", f"/api/v1/repos/{_repo(owner, repo)}/contents/{_path(path)}?ref=main")
    except GiteaError as exc:
        if "404" in str(exc):
            return None
        raise


def read_text(owner: str, repo: str, path: str) -> str:
    data = get_file(owner, repo, path)
    if not data:
        return ""
    content = str(data.get("content", "")).replace("\n", "")
    return base64.b64decode(content).decode("utf-8")


def put_file(owner: str, repo: str, path: str, content: str | bytes, message: str) -> dict:
    raw = content.encode("utf-8") if isinstance(content, str) else content
    existing = get_file(owner, repo, path)
    body = {
        "branch": "main",
        "message": message,
        "content": base64.b64encode(raw).decode("ascii"),
    }
    method = "POST"
    if existing and existing.get("sha"):
        method = "PUT"
        body["sha"] = existing["sha"]
    return api(method, f"/api/v1/repos/{_repo(owner, repo)}/contents/{_path(path)}", json_body=body)


def ensure_file(owner: str, repo: str, path: str, content: str, message: str) -> None:
    if get_file(owner, repo, path):
        return
    put_file(owner, repo, path, content, message)
