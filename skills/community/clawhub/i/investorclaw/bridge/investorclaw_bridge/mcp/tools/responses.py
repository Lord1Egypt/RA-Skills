# SPDX-License-Identifier: Apache-2.0
"""Portfolio-response persistence — store every portfolio_ask result in
MNEMOS so the user (or agent) can search history, retrieve a specific
response by serial number, flag bad responses, and remove them.

Why: each portfolio_ask is expensive (cold-cache asks take 5-15min, hit
multiple paid APIs, generate a deterministic envelope keyed by HMAC).
Throwing the response away after a single render wastes that work and
makes barrage analysis impossible. MNEMOS is the natural store —
queryable, federated, already on the fleet.

The "serial number" the user asked for is the engine's `ic_result.run_id`
(uuid4) — already unique per ask, already returned by the bridge, already
embedded in the narrative footer. We piggyback on it instead of
introducing a parallel ID space.

CRUD model:
  CREATE: portfolio_ask auto-stores after each successful run
  READ:   portfolio_response_get(run_id) / portfolio_response_list(limit)
  UPDATE: portfolio_response_flag_bad(run_id, reason) — adds bad tag
  DELETE: portfolio_response_delete(run_id) — removes from MNEMOS

All operations are best-effort against the MNEMOS endpoint. Failures
are logged and do NOT propagate to the caller — the bridge stays
responsive even if MNEMOS is offline.
"""
from __future__ import annotations

import json
import os
import time
from typing import Any
from urllib import request as urlreq
from urllib.error import HTTPError, URLError

from .._runtime import logger


# Endpoint + auth — both env-configurable. Defaults match serve.py.
def _mnemos_base() -> str:
    return os.environ.get("MNEMOS_BASE", "http://localhost:5002").rstrip("/")


def _mnemos_token() -> str | None:
    return (
        os.environ.get("MNEMOS_TOKEN")
        or os.environ.get("MNEMOS_BEARER")
        or os.environ.get("MNEMOS_API_KEY")
    )


# All portfolio responses are tagged with this so they can be enumerated
# without polluting unrelated MNEMOS searches.
_RESPONSE_TAG = "portfolio_response"
_BAD_TAG = "bad_response"
_CATEGORY = "infrastructure"  # MNEMOS canonical category for fleet artifacts


def _post(path: str, body: dict, timeout: float = 5.0) -> dict | None:
    """POST JSON to MNEMOS. Returns parsed response or None on any failure."""
    base = _mnemos_base()
    token = _mnemos_token()
    if not token:
        logger.debug("mnemos.token.missing — set MNEMOS_TOKEN to enable response persistence")
        return None

    url = f"{base}{path}"
    data = json.dumps(body).encode()
    req = urlreq.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urlreq.urlopen(req, timeout=timeout) as resp:
            text = resp.read().decode("utf-8", errors="replace")
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                logger.warning("mnemos.response.unparseable", url=url, body_head=text[:200])
                return None
    except HTTPError as e:
        logger.warning("mnemos.http_error", url=url, status=e.code, reason=str(e))
        return None
    except URLError as e:
        logger.warning("mnemos.url_error", url=url, reason=str(e))
        return None
    except Exception as e:
        logger.warning("mnemos.unknown_error", url=url, exc=str(e))
        return None


def _delete(path: str, timeout: float = 5.0) -> dict | None:
    """DELETE against MNEMOS. Same best-effort semantics."""
    base = _mnemos_base()
    token = _mnemos_token()
    if not token:
        return None
    req = urlreq.Request(
        f"{base}{path}",
        method="DELETE",
        headers={"Authorization": f"Bearer {token}"},
    )
    try:
        with urlreq.urlopen(req, timeout=timeout) as resp:
            text = resp.read().decode("utf-8", errors="replace")
            try:
                return json.loads(text) if text else {"ok": True}
            except json.JSONDecodeError:
                return {"ok": True}
    except HTTPError as e:
        logger.warning("mnemos.delete_http_error", path=path, status=e.code)
        return None
    except Exception as e:
        logger.warning("mnemos.delete_error", path=path, exc=str(e))
        return None


def _put(path: str, body: dict, timeout: float = 5.0) -> dict | None:
    base = _mnemos_base()
    token = _mnemos_token()
    if not token:
        return None
    req = urlreq.Request(
        f"{base}{path}",
        data=json.dumps(body).encode(),
        method="PUT",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urlreq.urlopen(req, timeout=timeout) as resp:
            text = resp.read().decode("utf-8", errors="replace")
            try:
                return json.loads(text) if text else {"ok": True}
            except json.JSONDecodeError:
                return {"ok": True}
    except Exception as e:
        logger.warning("mnemos.put_error", path=path, exc=str(e))
        return None


# ──────────────────────────────────────────────────────────────────────
# Persistence — called from portfolio_ask after the engine subprocess
# completes. Best-effort; never raises.
# ──────────────────────────────────────────────────────────────────────


def persist_response(
    *,
    question: str,
    narrative: str,
    ic_result: dict | None,
    duration_ms: int | None,
) -> dict | None:
    """Store a portfolio_ask response in MNEMOS.

    Returns the MNEMOS create-memory response (carries the assigned mem_id),
    or None if persistence failed for any reason.
    """
    if not narrative:
        return None
    inner = (ic_result or {}).get("ic_result", {}) if isinstance(ic_result, dict) else {}
    run_id = inner.get("run_id") or "unknown"
    hmac = inner.get("hmac") or ""
    engine_version = inner.get("engine_version") or "unknown"

    body = {
        "content": narrative,
        "category": _CATEGORY,
        "tags": [_RESPONSE_TAG, f"run_id:{run_id}", "investorclaw"],
        "metadata": {
            "run_id": run_id,
            "hmac": hmac,
            "question": question,
            "engine_version": engine_version,
            "duration_ms": duration_ms,
            "stored_at": int(time.time()),
        },
    }
    result = _post("/v1/memories", body)
    if result and result.get("id"):
        logger.info(
            "mnemos.response.stored",
            mem_id=result.get("id"),
            run_id=run_id,
            chars=len(narrative),
        )
    return result


# ──────────────────────────────────────────────────────────────────────
# Tool handlers (transport-agnostic — wired in tools/__init__.py + transport.py)
# ──────────────────────────────────────────────────────────────────────


async def portfolio_response_get(run_id: str) -> dict[str, Any]:
    """Retrieve a previously-stored portfolio response by its run_id (the
    engine's ic_result.run_id, which doubles as the response serial number)."""
    if not run_id:
        return {"error": "run_id required"}
    # Search MNEMOS for the run_id tag
    result = _post(
        "/v1/memories/search",
        {"query": f"run_id:{run_id}", "tags": [_RESPONSE_TAG], "limit": 5},
    )
    if not result:
        return {"error": "search_failed_or_token_missing", "run_id": run_id}
    hits = result.get("results") or result.get("memories") or []
    return {
        "run_id": run_id,
        "found": len(hits),
        "memories": hits,
    }


async def portfolio_response_list(limit: int = 10) -> dict[str, Any]:
    """List recent portfolio responses. Returns mem_id, run_id, question,
    storage timestamp, and a narrative preview for each."""
    limit = max(1, min(int(limit or 10), 50))
    result = _post(
        "/v1/memories/search",
        {"query": _RESPONSE_TAG, "tags": [_RESPONSE_TAG], "limit": limit},
    )
    if not result:
        return {"error": "search_failed_or_token_missing"}
    hits = result.get("results") or result.get("memories") or []
    return {"count": len(hits), "responses": hits}


async def portfolio_response_delete(run_id: str) -> dict[str, Any]:
    """Permanently remove a stored portfolio response by run_id (serial number).
    Use for bad responses you want gone — e.g. ones that hallucinated, returned
    catalog blurbs, or reflect a since-corrected engine version."""
    if not run_id:
        return {"error": "run_id required"}
    # First locate the mem_id
    locator = await portfolio_response_get(run_id)
    hits = locator.get("memories", []) or []
    if not hits:
        return {"deleted": 0, "run_id": run_id, "reason": "not_found"}
    deleted = 0
    for hit in hits:
        mem_id = hit.get("id") or hit.get("mem_id")
        if not mem_id:
            continue
        if _delete(f"/v1/memories/{mem_id}"):
            deleted += 1
    logger.info("mnemos.response.deleted", run_id=run_id, deleted=deleted)
    return {"deleted": deleted, "run_id": run_id}


async def portfolio_response_flag_bad(run_id: str, reason: str = "") -> dict[str, Any]:
    """Tag a stored portfolio response as bad without removing it. Useful for
    keeping a record of failures for later barrage analysis while excluding
    them from default response searches."""
    if not run_id:
        return {"error": "run_id required"}
    locator = await portfolio_response_get(run_id)
    hits = locator.get("memories", []) or []
    if not hits:
        return {"flagged": 0, "run_id": run_id, "reason": "not_found"}
    flagged = 0
    for hit in hits:
        mem_id = hit.get("id") or hit.get("mem_id")
        if not mem_id:
            continue
        # Add bad tag + the operator's reason note
        existing_tags = (hit.get("tags") or []) + [_BAD_TAG]
        body = {
            "tags": list(set(existing_tags)),
            "metadata": {
                **(hit.get("metadata") or {}),
                "bad_flagged_at": int(time.time()),
                "bad_reason": reason or "operator_flagged",
            },
        }
        if _put(f"/v1/memories/{mem_id}", body):
            flagged += 1
    return {"flagged": flagged, "run_id": run_id, "reason": reason}


# ──────────────────────────────────────────────────────────────────────
# Tool descriptors (registered via TOOL_REGISTRY in tools/__init__.py)
# ──────────────────────────────────────────────────────────────────────


def _tool(description: str, parameters: dict, required: list[str], handler) -> dict:
    return {
        "description": description,
        "parameters": parameters,
        "required": required,
        "handler": handler,
    }


RESPONSE_TOOLS: dict[str, dict[str, Any]] = {
    "portfolio_response_get": _tool(
        description=(
            "Retrieve a previously-stored portfolio_ask response by its run_id "
            "(serial number). The run_id is returned in every portfolio_ask "
            "response inside `ic_result.run_id`."
        ),
        parameters={
            "run_id": {
                "type": "string",
                "description": "The engine ic_result.run_id (uuid). Acts as the response serial number.",
            },
        },
        required=["run_id"],
        handler=portfolio_response_get,
    ),
    "portfolio_response_list": _tool(
        description=(
            "List the most recent stored portfolio responses. Returns mem_id, "
            "run_id, question, storage timestamp, and narrative preview per "
            "response."
        ),
        parameters={
            "limit": {
                "type": "integer",
                "description": "Max responses to return (1-50, default 10).",
            },
        },
        required=[],
        handler=portfolio_response_list,
    ),
    "portfolio_response_delete": _tool(
        description=(
            "Permanently delete a stored portfolio response from MNEMOS by "
            "run_id (serial number). Use for bad responses — hallucinations, "
            "catalog blurbs, refusals from a since-corrected engine version."
        ),
        parameters={
            "run_id": {
                "type": "string",
                "description": "The run_id (serial number) of the response to delete.",
            },
        },
        required=["run_id"],
        handler=portfolio_response_delete,
    ),
    "portfolio_response_flag_bad": _tool(
        description=(
            "Tag a stored portfolio response as bad without deleting it. Adds "
            "the `bad_response` tag plus an optional reason note. Useful for "
            "keeping a record of failures while excluding them from default "
            "response searches."
        ),
        parameters={
            "run_id": {
                "type": "string",
                "description": "The run_id (serial number) of the response to flag.",
            },
            "reason": {
                "type": "string",
                "description": "Optional human-readable reason for the bad flag.",
            },
        },
        required=["run_id"],
        handler=portfolio_response_flag_bad,
    ),
}
