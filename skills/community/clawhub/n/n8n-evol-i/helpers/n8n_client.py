import re
from pathlib import Path
from typing import Any, Optional

import requests

_CACHE: dict = {}

_SECRET_FIELDS = frozenset({"apiKey", "api_key", "password", "secret", "token", "X-N8N-API-KEY"})


class N8nClient:
    def __init__(self, base_url: str, api_key: str):
        url = base_url.rstrip("/")
        if not url.startswith("http"):
            url = f"https://{url}"
        self.base_url = url
        self._headers = {
            "X-N8N-API-KEY": api_key,
            "Content-Type": "application/json",
        }

    def _url(self, path: str) -> str:
        return f"{self.base_url}/api/v1/{path.lstrip('/')}"

    def get(self, path: str, params: Optional[dict] = None) -> Any:
        resp = requests.get(self._url(path), headers=self._headers, params=params)
        resp.raise_for_status()
        return resp.json() if resp.content else None

    def post(self, path: str, body: Any = None) -> Any:
        resp = requests.post(self._url(path), headers=self._headers, json=body)
        resp.raise_for_status()
        return resp.json() if resp.content else None

    def put(self, path: str, body: Any) -> Any:
        resp = requests.put(self._url(path), headers=self._headers, json=body)
        resp.raise_for_status()
        return resp.json() if resp.content else None

    def delete(self, path: str) -> Any:
        resp = requests.delete(self._url(path), headers=self._headers)
        resp.raise_for_status()
        return resp.json() if resp.content else None

    def get_workflow(self, workflow_id: str) -> dict:
        return self.get(f"workflows/{workflow_id}")

    def list_workflows(self, filter: Optional[dict] = None) -> list:
        return self.get("workflows", params=filter or {}).get("data", [])


def ensure_client(env_name: str, workspace: Path) -> N8nClient:
    """Return a cached N8nClient for the given env. Cache invalidated on .env mtime change."""
    import os
    from helpers.config import load_env, load_yaml

    env_file = workspace / "n8n-config" / f".env.{env_name}"
    mtime = env_file.stat().st_mtime if env_file.exists() else 0
    cache_key = (env_name, str(workspace), mtime)
    if cache_key not in _CACHE:
        data = load_yaml(env_name, workspace)
        load_env(env_name, workspace)
        api_key = os.environ.get("N8N_API_KEY", "")
        instance = data.get("n8n", {}).get("instanceName", "")
        _CACHE[cache_key] = N8nClient(base_url=instance, api_key=api_key)
    return _CACHE[cache_key]


def redact_for_debug(data: Any) -> Any:
    """Recursively redact known secret fields from a data structure."""
    if isinstance(data, dict):
        return {k: ("[REDACTED]" if k in _SECRET_FIELDS else redact_for_debug(v)) for k, v in data.items()}
    if isinstance(data, list):
        return [redact_for_debug(item) for item in data]
    return data


def _redact_url(url: str) -> str:
    return re.sub(r"(https?://)([^/]+)", r"\1[HOST]", url)
