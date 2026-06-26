#!/usr/bin/env python3
"""Gemini API Google Search grounding helper for OpenClaw.

Returns synthesized answer text plus grounding/citation URLs when provided by
Gemini. Keeps credentials out of stdout/stderr.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from typing import Any


def _get_attr(obj: Any, name: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def _to_plain(obj: Any) -> Any:
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, list):
        return [_to_plain(x) for x in obj]
    if isinstance(obj, tuple):
        return [_to_plain(x) for x in obj]
    if isinstance(obj, dict):
        return {str(k): _to_plain(v) for k, v in obj.items()}
    for meth in ("to_json_dict", "model_dump", "dict"):
        fn = getattr(obj, meth, None)
        if callable(fn):
            try:
                return _to_plain(fn())
            except Exception:
                pass
    if hasattr(obj, "__dict__"):
        return {k: _to_plain(v) for k, v in vars(obj).items() if not k.startswith("_")}
    return str(obj)


def api_key_from_1password(vault: str, item: str, field: str | None) -> str | None:
    """Read an API key from 1Password without printing it.

    If field is set, use `op read op://vault/item/field`. Otherwise inspect the
    item JSON and choose a likely concealed/password/token/credential field.
    """
    if not vault or not item:
        return None
    if field:
        ref = f"op://{vault}/{item}/{field}"
        try:
            return subprocess.check_output(["op", "read", ref], text=True, stderr=subprocess.PIPE).strip()
        except (subprocess.CalledProcessError, FileNotFoundError) as exc:
            raise RuntimeError(f"Could not read 1Password field {ref}: {exc}") from exc

    try:
        raw = subprocess.check_output(
            ["op", "item", "get", item, "--vault", vault, "--format", "json"],
            text=True,
            stderr=subprocess.PIPE,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise RuntimeError(f"Could not read 1Password item {item!r} in vault {vault!r}: {exc}") from exc

    data = json.loads(raw)
    fields = data.get("fields", []) or []
    preferred_labels = ("api key", "apikey", "gemini api key", "credential", "token", "password")
    concealed_types = {"CONCEALED", "PASSWORD"}

    candidates: list[tuple[int, str]] = []
    for f in fields:
        val = f.get("value")
        if not val:
            continue
        label = str(f.get("label", "")).lower()
        ftype = str(f.get("type", "")).upper()
        score = 0
        if any(p in label for p in preferred_labels):
            score += 10
        if ftype in concealed_types:
            score += 5
        if str(val).startswith("AIza"):
            score += 20
        if score:
            candidates.append((score, str(val)))
    if not candidates:
        raise RuntimeError("No likely API key field found in 1Password item; pass --op-field explicitly")
    candidates.sort(reverse=True, key=lambda x: x[0])
    return candidates[0][1]


def collect_sources(resp: Any) -> list[dict[str, str]]:
    sources: list[dict[str, str]] = []
    seen: set[str] = set()
    candidates = _get_attr(resp, "candidates", []) or []
    for cand in candidates:
        gm = _get_attr(cand, "grounding_metadata") or _get_attr(cand, "groundingMetadata")
        chunks = _get_attr(gm, "grounding_chunks") or _get_attr(gm, "groundingChunks") or []
        for ch in chunks:
            web = _get_attr(ch, "web")
            uri = _get_attr(web, "uri")
            if not uri or uri in seen:
                continue
            seen.add(uri)
            sources.append({"title": _get_attr(web, "title", ""), "url": uri})
    return sources


def main() -> int:
    ap = argparse.ArgumentParser(description="Gemini API Google Search grounding helper")
    ap.add_argument("query", nargs="*", help="Search/query text. Alternative to --query.")
    ap.add_argument("--query", dest="query_opt", help="Search/query text")
    ap.add_argument("--model", default=os.environ.get("GEMINI_SEARCH_MODEL", "gemini-2.5-flash"))
    ap.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown-ish text")
    ap.add_argument("--op-vault", default=os.environ.get("GEMINI_OP_VAULT", ""))
    ap.add_argument("--op-item", default=os.environ.get("GEMINI_OP_ITEM", ""))
    ap.add_argument("--op-field", default=os.environ.get("GEMINI_OP_FIELD", ""))
    args = ap.parse_args()

    query = args.query_opt or " ".join(args.query).strip()
    if not query:
        ap.error("provide a query via positional args or --query")

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key and args.op_item:
        api_key = api_key_from_1password(args.op_vault, args.op_item, args.op_field or None)
    if not api_key:
        raise SystemExit("Missing Gemini API key. Set GEMINI_API_KEY/GOOGLE_API_KEY or pass --op-vault/--op-item.")

    try:
        from google import genai  # type: ignore
        from google.genai import types  # type: ignore
    except ImportError as exc:
        raise SystemExit("Missing dependency: install with `python3 -m pip install google-genai`") from exc

    client = genai.Client(api_key=api_key)
    resp = client.models.generate_content(
        model=args.model,
        contents=query,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
        ),
    )

    text = getattr(resp, "text", "") or ""
    sources = collect_sources(resp)
    grounding = []
    for cand in _get_attr(resp, "candidates", []) or []:
        gm = _get_attr(cand, "grounding_metadata") or _get_attr(cand, "groundingMetadata")
        if gm:
            grounding.append(_to_plain(gm))

    if args.json:
        print(json.dumps({"query": query, "model": args.model, "answer": text, "sources": sources, "grounding_metadata": grounding}, indent=2))
    else:
        print(text.rstrip())
        if sources:
            print("\nSources:")
            for i, s in enumerate(sources, 1):
                title = s.get("title") or s.get("url")
                print(f"{i}. {title} — {s.get('url')}")
        else:
            print("\nSources: no grounding URLs returned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
