#!/usr/bin/env python3
"""Resolve entry inputs (image / ASIN / keywords) → exact keyword list for heat analysis.

Usage:
  python resolve_entry.py '{"keywords":["yoga mat"]}'
  python resolve_entry.py '{"asins":["B01LP0V4JY"],"region":"US","top_n":12}'
  python resolve_entry.py '{"imageUrl":"https://...","region":"US","max_keywords":10}'
  python resolve_entry.py '{"image":"/path/to/local.png","region":"US"}'

stdout JSON:
  { success, keywords[], sources: { mode, detail... }, warnings[] }
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
HOME = Path.home()

PATHS = {
    "shell_f": [
        Path("/root/.linkfox/workspaces/.claude/skills/amazon-aba-asin-reverse/scripts/shell_f.py"),
        HOME / ".hermes/skills/amazon-aba-asin-reverse/scripts/shell_f.py",
        Path("/root/.hermes/skills/amazon-aba-asin-reverse/scripts/shell_f.py"),
    ],
    "recognize": [
        Path("/root/.linkfox/workspaces/.claude/skills/linkfox-multimodal-recognize-image/scripts/multimodal_recognize_image.py"),
        HOME / ".hermes/skills/linkfox-multimodal-recognize-image/scripts/multimodal_recognize_image.py",
        Path("/root/.hermes/skills/linkfox-multimodal-recognize-image/scripts/multimodal_recognize_image.py"),
    ],
    "upload": [
        Path("/root/.linkfox/workspaces/.claude/skills/linkfox-multimodal-recognize-image/scripts/upload_image.py"),
        HOME / ".hermes/skills/linkfox-multimodal-recognize-image/scripts/upload_image.py",
        Path("/root/.hermes/skills/linkfox-multimodal-recognize-image/scripts/upload_image.py"),
    ],
}


def which_script(key: str) -> Path:
    for p in PATHS[key]:
        if p.is_file():
            return p
    raise FileNotFoundError(f"missing dependency script for {key}: tried {PATHS[key]}")


def run_json_script(script: Path, payload: dict, timeout: int = 180) -> dict:
    proc = subprocess.run(
        [sys.executable, str(script), json.dumps(payload, ensure_ascii=False)],
        capture_output=True,
        text=True,
        env=os.environ.copy(),
        timeout=timeout,
    )
    out = (proc.stdout or "").strip()
    err = (proc.stderr or "").strip()
    if proc.returncode != 0:
        raise RuntimeError(f"{script.name} rc={proc.returncode}: {err or out[:500]}")
    # some scripts print logs; try last JSON object
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        # find last {...}
        m = None
        for m in re.finditer(r"\{[\s\S]*\}", out):
            pass
        if not m:
            raise RuntimeError(f"non-JSON output from {script.name}: {out[:400]}")
        return json.loads(m.group(0))


def normalize_keywords(items: list, max_n: int = 12) -> list[str]:
    seen = set()
    out = []
    for x in items:
        if not x:
            continue
        s = str(x).strip().lower()
        s = re.sub(r"\s+", " ", s)
        s = s.strip(" .,;:\"'`")
        if len(s) < 2 or len(s) > 80:
            continue
        # drop pure Chinese-only if looking for Amazon US search terms? keep mixed
        if s in seen:
            continue
        seen.add(s)
        out.append(s)
        if len(out) >= max_n:
            break
    return out


def resolve_keywords_direct(params: dict) -> list[str]:
    kws = params.get("keywords") or params.get("keyword") or []
    if isinstance(kws, str):
        kws = [kws]
    return normalize_keywords(kws, int(params.get("max_keywords") or 20))


def resolve_from_asins(params: dict) -> tuple[list[str], dict]:
    asins = params.get("asins") or params.get("asin") or []
    if isinstance(asins, str):
        asins = [a.strip() for a in re.split(r"[,;\s]+", asins) if a.strip()]
    if not asins:
        raise ValueError("asins required")
    region = (params.get("region") or "US").upper()
    top_n = int(params.get("top_n") or params.get("max_keywords") or 12)
    weeks = int(params.get("asin_weeks") or params.get("weeks") or 8)

    shell_f = which_script("shell_f")
    raw = run_json_script(
        shell_f,
        {
            "region": region,
            "asins": asins,
            "weeks": weeks,
            "top_n": max(top_n * 3, 30),  # pull more then rank
            "order_by": "sfr",
        },
        timeout=180,
    )

    # extract terms + best sfr
    term_sfr: dict[str, int] = {}
    tables = raw.get("tables") or []
    rows = []
    for t in tables:
        rows.extend(t.get("data") or [])
    if not rows and isinstance(raw.get("data"), list):
        rows = raw["data"]

    for r in rows:
        rl = {str(k).lower(): v for k, v in r.items()} if isinstance(r, dict) else {}
        term = rl.get("searchterm") or rl.get("search_term") or rl.get("keyword")
        sfr = rl.get("searchfrequencyrank") or rl.get("search_frequency_rank")
        if not term:
            continue
        term = str(term).strip().lower()
        try:
            sfr_i = int(float(sfr)) if sfr is not None else 10**9
        except Exception:
            sfr_i = 10**9
        if term not in term_sfr or sfr_i < term_sfr[term]:
            term_sfr[term] = sfr_i

    ranked = sorted(term_sfr.items(), key=lambda kv: kv[1])  # hotter first
    kws = normalize_keywords([t for t, _ in ranked], top_n)
    detail = {
        "mode": "asin",
        "asins": asins,
        "region": region,
        "weeks": weeks,
        "candidates": [{"keyword": t, "sfr": s} for t, s in ranked[: top_n * 2]],
        "shell_meta": raw.get("_meta"),
        "raw_rows": len(rows),
    }
    return kws, detail


IMAGE_REQUIREMENT = (
    "This is an e-commerce / Amazon product image. "
    "Infer the most likely customer search queries shoppers would type on Amazon. "
    "Return ONLY a JSON object with this schema (no markdown): "
    '{"product_type":"...","search_keywords":["exact query 1","exact query 2",...],'
    '"confidence":"high|medium|low","notes":"..."}. '
    "Rules: search_keywords must be English Amazon-style queries (not brand slogans), "
    "3 to 12 items, ordered by likelihood; prefer category+attribute phrases "
    "(e.g. 'satin slip dress', 'wireless earbuds noise cancelling'); "
    "avoid pure brand names unless the product is brand-led; no numbering."
)


def ensure_image_url(params: dict) -> str:
    url = params.get("imageUrl") or params.get("image_url") or params.get("url")
    local = params.get("image") or params.get("image_path") or params.get("local_image")
    if url and str(url).startswith(("http://", "https://")):
        return str(url)
    if local:
        p = Path(str(local)).expanduser()
        if not p.is_file():
            raise FileNotFoundError(f"image not found: {p}")
        upload = which_script("upload")
        proc = subprocess.run(
            [sys.executable, str(upload), str(p)],
            capture_output=True,
            text=True,
            env=os.environ.copy(),
            timeout=120,
        )
        out = (proc.stdout or "").strip()
        err = (proc.stderr or "").strip()
        if proc.returncode != 0:
            raise RuntimeError(f"upload_image failed: {err or out}")
        # parse URL from output
        try:
            j = json.loads(out)
            for k in ("url", "imageUrl", "publicUrl", "data"):
                if isinstance(j.get(k), str) and j[k].startswith("http"):
                    return j[k]
                if isinstance(j.get(k), dict):
                    for kk in ("url", "imageUrl"):
                        if str(j[k].get(kk, "")).startswith("http"):
                            return j[k][kk]
        except json.JSONDecodeError:
            pass
        m = re.search(r"https?://\S+", out)
        if m:
            return m.group(0).rstrip(")'\"")
        raise RuntimeError(f"upload ok but no URL parsed: {out[:300]}")
    raise ValueError("imageUrl or local image path required")


def parse_keywords_from_vision(text: str, max_n: int) -> list[str]:
    if not text:
        return []
    # try JSON block
    candidates = []
    for m in re.finditer(r"\{[\s\S]*\}", text):
        try:
            obj = json.loads(m.group(0))
            if isinstance(obj, dict) and isinstance(obj.get("search_keywords"), list):
                candidates = obj["search_keywords"]
                break
            if isinstance(obj, dict) and isinstance(obj.get("keywords"), list):
                candidates = obj["keywords"]
                break
        except json.JSONDecodeError:
            continue
    if not candidates:
        # bullet / line list
        for line in text.splitlines():
            line = line.strip()
            line = re.sub(r"^[\-\*\d\.\)\s]+", "", line)
            if 2 <= len(line) <= 80 and re.search(r"[A-Za-z]", line):
                candidates.append(line)
    return normalize_keywords(candidates, max_n)


def resolve_from_image(params: dict) -> tuple[list[str], dict]:
    max_n = int(params.get("max_keywords") or 10)
    image_url = ensure_image_url(params)
    recog = which_script("recognize")
    requirement = params.get("requirement") or IMAGE_REQUIREMENT
    raw = run_json_script(
        recog,
        {"imageUrl": image_url, "requirement": requirement},
        timeout=180,
    )
    # extract text field variants
    text = (
        raw.get("data")
        or raw.get("result")
        or raw.get("content")
        or raw.get("text")
        or raw.get("msg")
        or ""
    )
    if isinstance(text, dict):
        text = (
            text.get("content")
            or text.get("text")
            or text.get("result")
            or json.dumps(text, ensure_ascii=False)
        )
    if not isinstance(text, str):
        text = json.dumps(text, ensure_ascii=False)

    # sometimes nested tables
    if not text or text == raw.get("msg"):
        # walk for longest string
        best = ""
        def walk(o):
            nonlocal best
            if isinstance(o, str) and len(o) > len(best):
                best = o
            elif isinstance(o, dict):
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(raw)
        if len(best) > len(text or ""):
            text = best

    kws = parse_keywords_from_vision(text, max_n)
    detail = {
        "mode": "image",
        "imageUrl": image_url,
        "vision_text_preview": (text or "")[:1200],
        "raw_keys": list(raw.keys()) if isinstance(raw, dict) else [],
    }
    return kws, detail


def resolve(params: dict) -> dict:
    warnings = []
    sources = []
    keywords: list[str] = []

    # priority: explicit keywords always included; image/asin expand
    direct = resolve_keywords_direct(params)
    if direct:
        keywords.extend(direct)
        sources.append({"mode": "keywords", "keywords": direct})

    has_asin = bool(params.get("asins") or params.get("asin"))
    has_image = bool(
        params.get("imageUrl")
        or params.get("image_url")
        or params.get("image")
        or params.get("image_path")
        or params.get("local_image")
    )

    if has_asin:
        try:
            kws, detail = resolve_from_asins(params)
            sources.append(detail)
            for k in kws:
                if k not in keywords:
                    keywords.append(k)
        except Exception as e:
            warnings.append(f"asin_resolve_failed: {e}")

    if has_image:
        try:
            kws, detail = resolve_from_image(params)
            sources.append(detail)
            for k in kws:
                if k not in keywords:
                    keywords.append(k)
        except Exception as e:
            warnings.append(f"image_resolve_failed: {e}")

    max_n = int(params.get("max_keywords") or 12)
    keywords = normalize_keywords(keywords, max_n)

    if not keywords:
        return {
            "success": False,
            "error": "no keywords resolved from inputs",
            "keywords": [],
            "sources": sources,
            "warnings": warnings,
        }

    mode = "keywords"
    if has_image and has_asin:
        mode = "image+asin"
    elif has_image:
        mode = "image"
    elif has_asin:
        mode = "asin"
    elif direct:
        mode = "keywords"

    return {
        "success": True,
        "mode": mode,
        "keywords": keywords,
        "sources": sources,
        "warnings": warnings,
        "region": (params.get("region") or "US").upper(),
    }


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if sys.argv[1:] else 1)
    try:
        params = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(json.dumps({"success": False, "error": f"Invalid JSON: {e}"}, ensure_ascii=False))
        sys.exit(1)
    try:
        out = resolve(params)
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(2)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.exit(0 if out.get("success") else 2)


if __name__ == "__main__":
    main()
