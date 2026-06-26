"""
capabilities.py — Manifest cache and capability discovery

Responsibilities:
- Sync manifest from L2 and do local TTL caching
- Offline degradation
"""

import os
import json
import time
import logging
from pathlib import Path
from typing import Optional

from lib.remote_client import fetch_manifest
from lib.runtime_paths import (
    get_bundled_manifest_path,
    get_manifest_cache_path,
)
from lib.schemas import NetworkError

logger = logging.getLogger(__name__)

_SCRIPTS_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = get_manifest_cache_path()
BUNDLED_MANIFEST_PATH = get_bundled_manifest_path()
DEFAULT_TTL_SECONDS = 3600
STABLE_TOOL_NAMES = frozenset({
    "get_latest_news",
    "get_news_dataset",
    "sync_capabilities",
    "invoke_remote_capability",
})
REQUIRED_TOOL_HINTS = frozenset({
    "get_latest_news",
    "get_news_dataset",
    "invoke_remote_capability",
})


def _extract_manifest(payload: dict) -> Optional[dict]:
    """Accept either a wrapped cache payload or a raw manifest document."""
    if not isinstance(payload, dict):
        return None
    manifest = payload.get("manifest") if isinstance(payload.get("manifest"), dict) else payload
    return manifest if isinstance(manifest, dict) else None


def _extract_recommended_tools(manifest: dict) -> set[str]:
    """Extract normalized tool names from tool_hints."""
    tools = set()
    for hint in manifest.get("tool_hints", []):
        if not isinstance(hint, dict):
            continue
        recommended_tool = hint.get("recommended_tool")
        if not isinstance(recommended_tool, str):
            continue
        tool_name = recommended_tool.split("(", 1)[0].strip()
        tool_name = tool_name.split(" ", 1)[0].strip()
        if tool_name:
            tools.add(tool_name)
    return tools


def is_manifest_compatible(manifest: Optional[dict]) -> bool:
    """Reject stale manifest shapes that route to removed tools."""
    if not isinstance(manifest, dict):
        return False
    if not isinstance(manifest.get("client_policy"), dict):
        return False
    if not isinstance(manifest.get("data_products"), list):
        return False

    recommended_tools = _extract_recommended_tools(manifest)
    if not recommended_tools:
        return False
    if not REQUIRED_TOOL_HINTS.issubset(recommended_tools):
        return False
    return recommended_tools.issubset(STABLE_TOOL_NAMES)


def _read_json_file(path: Path) -> Optional[dict]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None
    return data if isinstance(data, dict) else None


def read_cached_manifest() -> Optional[dict]:
    """Read locally cached manifest, return None if not exists or corrupted"""
    if not MANIFEST_PATH.exists():
        return None
    data = _read_json_file(MANIFEST_PATH)
    if not data or "fetched_at" not in data or "manifest" not in data:
        return None
    manifest = _extract_manifest(data)
    if not is_manifest_compatible(manifest):
        return None
    return data


def read_bundled_manifest() -> Optional[dict]:
    """Read the repository-shipped manifest for deterministic offline behavior."""
    if not BUNDLED_MANIFEST_PATH.exists():
        return None
    payload = _read_json_file(BUNDLED_MANIFEST_PATH)
    manifest = _extract_manifest(payload or {})
    if not is_manifest_compatible(manifest):
        return None
    return manifest


def is_cache_expired(cached: Optional[dict]) -> bool:
    """Check if cache is expired"""
    if cached is None:
        return True
    fetched_at = cached.get("fetched_at", 0)
    ttl = cached.get("ttl_seconds", DEFAULT_TTL_SECONDS)
    return (time.time() - fetched_at) > ttl


def write_manifest_cache(manifest_data: dict) -> bool:
    """Write manifest to local cache"""
    cache_data = {
        "fetched_at": time.time(),
        "ttl_seconds": manifest_data.get("ttl_seconds", DEFAULT_TTL_SECONDS),
        "manifest": manifest_data,
    }
    try:
        tmp_path = MANIFEST_PATH.with_suffix(".tmp")
        tmp_path.parent.mkdir(parents=True, exist_ok=True)
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        tmp_path.replace(MANIFEST_PATH)
        return True
    except OSError:
        return False


def get_capability_metadata(capability_name: str, base_url: Optional[str] = None) -> Optional[dict]:
    """
    Get metadata for a specific capability from manifest.

    Returns capability dict with name, description, tier, requires_token,
    input_schema, result_schema, usage_notes, upgrade_hint, etc.
    """
    manifest = sync_capabilities(base_url=base_url)
    remote_caps = manifest.get("remote_capabilities", [])
    return next((c for c in remote_caps if c.get("name") == capability_name), None)


def get_tool_hints(base_url: Optional[str] = None) -> list:
    """Get tool hints from manifest."""
    manifest = sync_capabilities(base_url=base_url)
    return manifest.get("tool_hints", [])


def get_skill_hints(base_url: Optional[str] = None) -> list:
    """Get skill hints from manifest."""
    manifest = sync_capabilities(base_url=base_url)
    return manifest.get("skill_hints", [])


def get_upgrade_info(base_url: Optional[str] = None) -> dict:
    """Get upgrade information from manifest."""
    manifest = sync_capabilities(base_url=base_url)
    return manifest.get("upgrade", {})


def sync_capabilities(force: bool = False, base_url: Optional[str] = None) -> dict:
    """
    Sync platform capability manifest.

    Flow:
    1. Read local cache
    2. If force=True or cache expired, pull from L2
    3. Return offline degraded data when remote unavailable
    """
    cached = read_cached_manifest()

    if force or is_cache_expired(cached):
        try:
            fresh = fetch_manifest(base_url=base_url)
            if is_manifest_compatible(fresh):
                write_manifest_cache(fresh)
                return fresh
            logger.warning("Fetched manifest is incompatible with the current L3 routing contract")
        except (NetworkError, Exception) as e:
            logger.warning(f"Failed to fetch manifest: {e}")

        bundled = read_bundled_manifest()
        if bundled:
            bundled = dict(bundled)
            bundled["offline"] = True
            return bundled

        if cached and cached.get("manifest"):
            manifest = dict(cached["manifest"])
            manifest["offline"] = True
            return manifest
        return _build_offline_manifest()

    if cached and cached.get("manifest"):
        return cached["manifest"]

    bundled = read_bundled_manifest()
    if bundled:
        return bundled

    return _build_offline_manifest()


def _build_offline_manifest() -> dict:
    """Offline mode degraded manifest (keep same routing semantics as online)"""
    return {
        "ttl_seconds": 300,
        "offline": True,
        "client_policy": {
            "latest_version": "v1.3.1",
            "min_supported_version": "v1.3.1",
            "upgrade_url": "https://www.ainewparadigm.cn/",
            "upgrade_message": "",
        },
        "data_products": [
            {
                "product_name": "news_dataset",
                "schema_version": "v1",
                "available_tiers": ["guest", "pro_core", "pro_plus"],
                "normalization_language": "en",
                "compression": "json.gz",
                "supports_latest": True,
            }
        ],
        "remote_capabilities": [
            {
                "name": "download_original",
                "description": "[Paid Pro Feature] Download the original full article text from the source URL.",
                "requires_token": True,
                "tier": "pro_core",
                "parameters": {
                    "article_id": {"type": "string", "required": True, "description": "Article identifier"},
                },
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "article_id": {
                            "type": "string",
                            "description": "Article identifier from the dataset"
                        }
                    },
                    "required": ["article_id"]
                },
                "result_schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "article_url": {"type": "string"},
                        "original_text": {"type": "string"},
                        "error": {"type": "string"}
                    }
                },
                "usage_notes": "Use this to retrieve the full, unedited article text from the original source.",
                "upgrade_hint": "This is a Pro feature. Configure AINEWS_ACCESS_TOKEN to access it.",
            }
        ],
        "tool_hints": [
            {
                "when_to_use": "Today's AI news, current AI news, latest AI news, recent AI updates",
                "recommended_tool": "get_latest_news",
            },
            {
                "when_to_use": "Specific date requested",
                "recommended_tool": "get_news_dataset",
            },
            {
                "when_to_use": "Advanced analysis, what can you do",
                "recommended_tool": "invoke_remote_capability",
            },
        ],
        "routing_message": "Use get_latest_news for today's/current/latest AI news or recent AI updates (default choice). Use get_news_dataset only when user provides an explicit date for AI news. Do not use these tools for non-AI news such as sports, politics, finance, or general breaking news. Use invoke_remote_capability for advanced analysis and tracking features. Always sync_capabilities first to discover available features.",
        "upgrade": {
            "title": "Unlock AI Daily News Pro",
            "url": "https://www.ainewparadigm.cn/",
            "token_env": "AINEWS_ACCESS_TOKEN",
            "features": [
                "Ranking rationale and editorial analysis",
                "Strategic explainers and secondary classifications",
                "Advanced remote capabilities",
            ],
            "message": "Configure AINEWS_ACCESS_TOKEN to access Pro features.",
        },
    }
