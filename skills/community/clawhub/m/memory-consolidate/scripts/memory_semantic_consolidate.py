#!/usr/bin/env python3
"""LLM-powered semantic consolidation for V2-lite memory snapshot sections.

Replaces the old deterministic rule engine with a single LLM call (Haiku)
that groups, deduplicates, and rewrites candidates into concise snapshot items.
Falls back to pass-through if the LLM call fails.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.request import Request, urlopen
from urllib.error import URLError

# Ensure memory_consolidate package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent))
import memory_consolidate as mc


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
SECTION_LIMITS = {
    "top_facts": {"items": 6, "chars": 100},
    "chosen_solutions": {"items": 5, "chars": 110},
    "recent": {"items": 6, "chars": 100},
    "active_issues": {"items": 5, "chars": 100},
    "working_patterns": {"items": 5, "chars": 100},
}

# LLM config — read from env or fall back to openclaw.json tui provider
def _load_llm_config() -> Dict[str, str]:
    """Load Anthropic API config from openclaw.json tui provider."""
    base_url = os.environ.get("ANTHROPIC_BASE_URL", "")
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    model = os.environ.get("SEMANTIC_LLM_MODEL", "claude-haiku-4-5-20251001")

    if not base_url or not api_key:
        try:
            cfg_path = Path.home() / ".openclaw" / "openclaw.json"
            cfg = json.loads(cfg_path.read_text("utf-8"))
            tui = cfg.get("models", {}).get("providers", {}).get("tui", {})
            if not base_url:
                base_url = tui.get("baseUrl", "")
            if not api_key:
                api_key = tui.get("apiKey", "")
        except Exception:
            pass

    return {"base_url": base_url.rstrip("/"), "api_key": api_key, "model": model}


# ---------------------------------------------------------------------------
# LLM call
# ---------------------------------------------------------------------------
def _call_anthropic(prompt: str, system: str, cfg: Dict[str, str]) -> Optional[str]:
    """Call Anthropic Messages API. Returns assistant text or None on failure."""
    url = f"{cfg['base_url']}/v1/messages"
    body = json.dumps({
        "model": cfg["model"],
        "max_tokens": 4096,
        "system": system,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "x-api-key": cfg["api_key"],
        "anthropic-version": "2023-06-01",
    }

    try:
        req = Request(url, data=body, headers=headers, method="POST")
        with urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            for block in data.get("content", []):
                if block.get("type") == "text":
                    return block["text"]
    except Exception as exc:
        print(f"[semantic] LLM call failed: {exc}", file=sys.stderr)
    return None


# ---------------------------------------------------------------------------
# Build prompt from candidates
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are a memory consolidation engine for an AI assistant.
Your job: take raw candidate items grouped by section, deduplicate, merge similar items,
and rewrite each into a concise, high-signal bullet point.

Rules:
- Output valid JSON only, no markdown fences
- Each section is a list of objects with "text" and "theme" fields
- Merge semantically similar items into one
- Keep the most specific, actionable version
- Max chars per item: specified per section
- Remove noise: vague statements, status updates, file paths, command outputs
- Preserve decisions, lessons learned, recurring problems, concrete solutions
- Keep the original language (Chinese or English) of each item
- If an item is in Chinese, keep it in Chinese. If English, keep English."""

def _build_prompt(candidates: Dict[str, Any]) -> str:
    sections = candidates.get("sections") or {}
    parts = []
    for key, limits in SECTION_LIMITS.items():
        rows = sections.get(key, [])
        if not rows:
            continue
        items_text = []
        for r in rows[:20]:  # cap input to avoid token bloat
            text = str(r.get("text") or "").strip()
            if text:
                items_text.append(f"  - {text}")
        if not items_text:
            continue
        parts.append(
            f"## {key} (max {limits['items']} items, max {limits['chars']} chars each)\n"
            + "\n".join(items_text)
        )

    return (
        "Consolidate these memory candidates into a compact snapshot.\n"
        "Return JSON: {\"sections\": {\"<section_name>\": [{\"text\": \"...\", \"theme\": \"...\"}]}}\n\n"
        + "\n\n".join(parts)
    )


# ---------------------------------------------------------------------------
# Parse LLM response
# ---------------------------------------------------------------------------
def _parse_llm_response(raw: str) -> Optional[Dict[str, Any]]:
    """Extract sections dict and user_traits from LLM response."""
    # Strip markdown fences if present
    cleaned = re.sub(r"^```(?:json)?\s*\n?", "", raw.strip())
    cleaned = re.sub(r"\n?```\s*$", "", cleaned)
    try:
        data = json.loads(cleaned)
        if isinstance(data, dict):
            result = data.get("sections", {})
            # Attach user_traits at top level for caller to extract
            if "user_traits" in data:
                result["__user_traits__"] = data["user_traits"]
            return result
    except json.JSONDecodeError:
        pass
    return None


# ---------------------------------------------------------------------------
# Fallback: pass-through (no LLM)
# ---------------------------------------------------------------------------
# PLACEHOLDER_FALLBACK
def _fallback_consolidate(candidates: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    """Simple pass-through: take top N candidates per section, no rewriting."""
    sections = candidates.get("sections") or {}
    result: Dict[str, List[Dict[str, Any]]] = {}
    for key, limits in SECTION_LIMITS.items():
        rows = sections.get(key, [])
        items = []
        seen: set = set()
        for r in rows:
            text = mc.normalize_content(str(r.get("text") or ""))
            if not text:
                continue
            norm = mc.normalize_for_match(text)
            if norm in seen:
                continue
            seen.add(norm)
            items.append({"text": text, "theme": key, "rank": len(items) + 1})
            if len(items) >= limits["items"]:
                break
        if items:
            result[key] = items
    return result


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def build_semantic_payload(candidates: Dict[str, Any]) -> Dict[str, Any]:
    llm_cfg = _load_llm_config()
    used_llm = False
    semantic_sections: Dict[str, List[Dict[str, Any]]] = {}
    user_traits: List[Dict[str, Any]] = []

    if llm_cfg["base_url"] and llm_cfg["api_key"]:
        prompt = _build_prompt(candidates)
        system = SYSTEM_PROMPT
        raw_response = _call_anthropic(prompt, system, llm_cfg)

        if raw_response:
            parsed = _parse_llm_response(raw_response)
            if parsed:
                used_llm = True
                for key, limits in SECTION_LIMITS.items():
                    items = parsed.get(key, [])
                    if not isinstance(items, list):
                        continue
                    cleaned = []
                    for idx, item in enumerate(items[:limits["items"]]):
                        text = str(item.get("text") or "") if isinstance(item, dict) else str(item)
                        text = text.strip()
                        if not text:
                            continue
                        if len(text) > limits["chars"]:
                            text = text[:limits["chars"] - 1] + "…"
                        cleaned.append({
                            "rank": idx + 1,
                            "section": key,
                            "text": text,
                            "theme": (item.get("theme") or key) if isinstance(item, dict) else key,
                            "source_count": 1,
                        })
                    if cleaned:
                        semantic_sections[key] = cleaned

                # Extract user_traits from LLM response
                user_traits = parsed.pop("__user_traits__", [])
                if isinstance(user_traits, list):
                    user_traits = [
                        t for t in user_traits
                        if isinstance(t, dict) and t.get("text")
                    ]

    if not used_llm:
        print("[semantic] Falling back to rule-based pass-through", file=sys.stderr)
        fallback = _fallback_consolidate(candidates)
        for key, items in fallback.items():
            semantic_sections[key] = [
                {"rank": i + 1, "section": key, "text": it["text"], "theme": it.get("theme", key), "source_count": 1}
                for i, it in enumerate(items)
            ]

    payload: Dict[str, Any] = {
        "schema": "memory.semantic.v2-lite",
        "generated_at": mc.utc_now_iso(),
        "mode": "llm" if used_llm else "fallback",
        "model": llm_cfg["model"] if used_llm else "none",
        "source_candidates": str(mc.CANDIDATE_LATEST_PATH),
        "active_sections": list(semantic_sections.keys()),
        "sections": semantic_sections,
        "counts": {key: len(value) for key, value in semantic_sections.items()},
    }
    if used_llm and user_traits:
        payload["user_traits"] = user_traits
    return payload


def main() -> int:
    if not mc.CANDIDATE_LATEST_PATH.exists():
        raise FileNotFoundError(mc.CANDIDATE_LATEST_PATH)

    candidates = json.loads(mc.CANDIDATE_LATEST_PATH.read_text("utf-8"))
    payload = build_semantic_payload(candidates)

    mc.SEMANTIC_DIR.mkdir(parents=True, exist_ok=True)
    latest_path = mc.SEMANTIC_LATEST_PATH
    stamp = payload["generated_at"].replace(":", "").replace("-", "")
    history_path = mc.SEMANTIC_DIR / f"semantic-{stamp}.json"

    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    latest_path.write_text(text, "utf-8")
    history_path.write_text(text, "utf-8")

    mode = payload.get("mode", "unknown")
    model = payload.get("model", "none")
    counts = payload.get("counts", {})
    print(f"[semantic] mode={mode} model={model} sections={counts}")
    print(str(latest_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
