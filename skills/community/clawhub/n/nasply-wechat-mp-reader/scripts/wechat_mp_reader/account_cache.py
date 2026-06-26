from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CACHE_PATH = Path(__file__).resolve().parents[1] / "cache" / "account_cache.json"


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def load_account_cache(path: str | None = None) -> dict[str, Any]:
    target = Path(path) if path else CACHE_PATH
    if not target.exists():
        return {"by_biz": {}, "by_name": {}}
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except Exception:
        return {"by_biz": {}, "by_name": {}}
    if not isinstance(data, dict):
        return {"by_biz": {}, "by_name": {}}
    data.setdefault("by_biz", {})
    data.setdefault("by_name", {})
    return data


def save_account_cache(cache: dict[str, Any], path: str | None = None) -> str:
    target = Path(path) if path else CACHE_PATH
    _ensure_parent(target)
    target.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(target)


def get_cached_account(biz: str = "", name: str = "", path: str | None = None) -> dict[str, Any]:
    cache = load_account_cache(path)
    if biz:
        hit = cache.get("by_biz", {}).get(biz)
        if isinstance(hit, dict):
            return hit
    if name:
        hit = cache.get("by_name", {}).get(name)
        if isinstance(hit, dict):
            return hit
    return {}


def put_cached_account(account: dict[str, Any], path: str | None = None) -> str:
    cache = load_account_cache(path)
    record = {
        "name": str(account.get("name", "") or "").strip(),
        "biz": str(account.get("biz", "") or "").strip(),
        "fakeid": str(account.get("fakeid", "") or "").strip(),
        "avatar": str(account.get("avatar", "") or "").strip(),
        "signature": str(account.get("signature", "") or "").strip(),
    }
    biz = record["biz"]
    name = record["name"]
    if biz:
        cache.setdefault("by_biz", {})[biz] = record
    if name:
        cache.setdefault("by_name", {})[name] = record
    return save_account_cache(cache, path)
