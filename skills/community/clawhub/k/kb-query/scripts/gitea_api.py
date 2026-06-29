from __future__ import annotations

import base64
import os
from urllib.parse import quote

import requests


GITEA_URL = os.getenv("GITEA_URL", "").rstrip("/")
ADMIN_TOKEN = os.getenv("GITEA_ADMIN_TOKEN", "")


class GiteaError(RuntimeError):
    pass


def _headers() -> dict[str, str]:
    return {"Authorization": f"token {ADMIN_TOKEN}", "Accept": "application/json"}


def _repo(owner: str, repo: str) -> str:
    return f"{quote(owner, safe='')}/{quote(repo, safe='')}"


def _path(path: str) -> str:
    return "/".join(quote(part, safe="") for part in path.split("/") if part)


def api(method: str, path: str, *, ok=(200, 201, 204)) -> object:
    if not GITEA_URL or not ADMIN_TOKEN:
        raise GiteaError("GITEA_URL and GITEA_ADMIN_TOKEN are required")
    response = requests.request(method, f"{GITEA_URL}{path}", headers=_headers(), timeout=60)
    if response.status_code not in ok:
        raise GiteaError(f"Gitea {method} {path} failed: {response.status_code} {response.text[:500]}")
    if not response.text:
        return {}
    return response.json()


def read_text(owner: str, repo: str, path: str) -> str:
    data = api("GET", f"/api/v1/repos/{_repo(owner, repo)}/contents/{_path(path)}?ref=main")
    content = str(data.get("content", "")).replace("\n", "")
    return base64.b64decode(content).decode("utf-8")


def list_tree(owner: str, repo: str) -> list[dict]:
    branch = api("GET", f"/api/v1/repos/{_repo(owner, repo)}/branches/main")
    sha = branch["commit"]["id"]
    data = api("GET", f"/api/v1/repos/{_repo(owner, repo)}/git/trees/{quote(sha, safe='')}?recursive=true")
    return data.get("tree", [])
