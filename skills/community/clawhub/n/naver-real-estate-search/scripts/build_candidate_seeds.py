from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import search_real_estate as sre

DEFAULT_INPUT = SCRIPT_DIR.parent / "references" / "seoul-major-complexes.seed-input.json"
DEFAULT_OUTPUT = SCRIPT_DIR.parent / "references" / "candidate-seeds.generated.json"
SEARCH_URL = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={query}"
COMPLEX_PATTERNS = [
    r"https://new\.land\.naver\.com/complexes/(\d+)",
    r"https://new\.land\.naver\.com/houses/(\d+)",
    r"complexNo=(\d+)",
]


def _load_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _dedupe_keep_order(values: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        key = str(value or "").strip()
        if not key or key in seen:
            continue
        out.append(key)
        seen.add(key)
    return out


def build_aliases(name: str, district: str = "", neighborhood: str = "", city: str = "서울특별시", extra: list[str] | None = None) -> list[str]:
    base = str(name or "").strip()
    variants: list[str] = []
    for seed in [base, *(extra or [])]:
        for value in sre.expand_alias_variants(seed):
            variants.append(value)
    place_bits = [x.strip() for x in [city, district, neighborhood] if str(x or "").strip()]
    short_city = city.replace("특별시", "").replace("광역시", "").strip() if city else ""
    if short_city:
        place_bits.append(short_city)
    normalized = sre.normalize_complex_alias(base)
    for prefix in _dedupe_keep_order(place_bits):
        if base:
            variants.extend([f"{prefix} {base}", f"{prefix}{base}"])
        if normalized:
            variants.extend([f"{prefix} {normalized}", f"{prefix}{normalized}"])
    if district and neighborhood:
        variants.extend([f"{district} {neighborhood} {base}", f"{district}{neighborhood}{base}"])
    return _dedupe_keep_order([v for item in variants for v in sre.expand_alias_variants(item)])[:30]


def extract_ids_from_html(query: str, *, limit: int = 8) -> dict[str, Any]:
    url = SEARCH_URL.format(query=urllib.parse.quote(query))
    try:
        html = sre._request_text(url)  # type: ignore[attr-defined]
    except Exception as exc:
        return {"ids": [], "status": "blocked", "error": str(exc), "query": query}
    ids: list[str] = []
    seen: set[str] = set()
    for pattern in COMPLEX_PATTERNS:
        for match in re.finditer(pattern, html):
            cid = match.group(1)
            if cid not in seen:
                ids.append(cid)
                seen.add(cid)
            if len(ids) >= limit:
                break
        if len(ids) >= limit:
            break
    return {"ids": ids, "status": "ok", "query": query}


def verify_candidate(complex_id: str, seed: dict[str, Any]) -> dict[str, Any]:
    try:
        info = sre.fetch_complex_info(complex_id)
        name = str(info.get("name") or "")
        address = str(info.get("address") or "")
        score = 0.0
        reasons: list[str] = []
        seed_name_norm = sre.normalize_complex_alias(seed.get("name") or "")
        found_name_norm = sre.normalize_complex_alias(name)
        district = str(seed.get("district") or "")
        neighborhood = str(seed.get("neighborhood") or "")
        if seed_name_norm and found_name_norm == seed_name_norm:
            score += 0.55
            reasons.append("name-exact")
        elif seed_name_norm and seed_name_norm in found_name_norm:
            score += 0.35
            reasons.append("name-partial")
        if district and district in address:
            score += 0.15
            reasons.append("district-match")
        if neighborhood and neighborhood in address:
            score += 0.15
            reasons.append("neighborhood-match")
        household_count = info.get("household_count")
        try:
            household_count = int(household_count or 0)
        except Exception:
            household_count = 0
        if household_count >= 500:
            score += 0.05
            reasons.append("household-signal")
        status = "verified" if score >= 0.65 else "weak-verified"
        return {
            "status": status,
            "confidence": round(min(1.0, score), 3),
            "verification_reasons": reasons,
            "complex": info,
        }
    except Exception as exc:
        return {
            "status": "unverified",
            "confidence": 0.0,
            "verification_reasons": [f"detail-fetch-failed:{type(exc).__name__}"],
            "error": str(exc),
            "complex": {"complex_id": complex_id},
        }


def build_search_queries(seed: dict[str, Any]) -> list[str]:
    city = str(seed.get("city") or "서울특별시")
    district = str(seed.get("district") or "")
    neighborhood = str(seed.get("neighborhood") or "")
    name = str(seed.get("name") or "")
    aliases = [str(x) for x in (seed.get("aliases") or []) if str(x).strip()]
    queries: list[str] = []
    for label in [name, *aliases]:
        label = label.strip()
        if not label:
            continue
        queries.extend([
            f"{city} {district} {neighborhood} {label} 네이버 부동산",
            f"{district} {neighborhood} {label} 네이버 부동산",
            f"{district} {label} 네이버 부동산",
            f"{label} 네이버 부동산 아파트",
            f"site:new.land.naver.com/complexes {district} {label}",
        ])
    return _dedupe_keep_order([q.strip() for q in queries if q.strip()])[:12]


def build_entry(seed: dict[str, Any], *, pause: float = 0.6) -> dict[str, Any]:
    aliases = build_aliases(
        seed.get("name") or "",
        district=seed.get("district") or "",
        neighborhood=seed.get("neighborhood") or "",
        city=seed.get("city") or "서울특별시",
        extra=[str(x) for x in (seed.get("aliases") or []) if str(x).strip()],
    )
    evidence: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    blocked_reasons: list[str] = []

    baseline_payload = _load_json(SCRIPT_DIR.parent / "references" / "candidate-seeds.json", {"entries": []})
    baseline_entries = baseline_payload.get("entries") if isinstance(baseline_payload, dict) else []
    seed_name_norm = sre.normalize_complex_alias(seed.get("name") or "")
    for row in baseline_entries or []:
        row_name_norm = sre.normalize_complex_alias(row.get("name") or "")
        row_aliases = [sre.normalize_complex_alias(x) for x in (row.get("aliases") or [])]
        if seed_name_norm and (seed_name_norm == row_name_norm or seed_name_norm in row_aliases):
            candidates.append({
                "complex_id": str(row.get("complex_id") or ""),
                "query": seed.get("name") or "",
                "discovery_source": "baseline-seed",
                "status": "verified",
                "confidence": 1.0,
                "verification_reasons": ["baseline-seed-match"],
                "complex": {
                    "complex_id": str(row.get("complex_id") or ""),
                    "name": row.get("name"),
                    "address": row.get("address"),
                    "household_count": row.get("household_count"),
                },
            })
            seen_ids.add(str(row.get("complex_id") or ""))
            evidence.append({"query": seed.get("name") or "", "status": "baseline-seed-hit", "ids": [row.get("complex_id")]})
            break

    def _append_candidate(cid: str, query: str, source: str) -> None:
        if not cid or cid in seen_ids:
            return
        seen_ids.add(cid)
        verified = verify_candidate(cid, seed)
        candidates.append({
            "complex_id": cid,
            "query": query,
            "discovery_source": source,
            **verified,
        })

    for query in build_search_queries(seed):
        try:
            cached = sre.search_cached_candidates(query, candidate_limit=3)
        except Exception as exc:
            cached = []
            evidence.append({"query": query, "status": "cache-error", "error": str(exc)})
        else:
            if cached:
                evidence.append({
                    "query": query,
                    "status": "cache-hit",
                    "source": "candidate-cache",
                    "ids": [row.get("complex_id") for row in cached],
                })
                for row in cached:
                    _append_candidate(str(row.get("complex_id") or ""), query, "candidate-cache")
                if candidates and float(candidates[0].get("confidence") or 0.0) >= 0.8:
                    break

        snapshot = extract_ids_from_html(query, limit=6)
        evidence.append(snapshot)
        if snapshot.get("status") != "ok":
            blocked_reasons.append(str(snapshot.get("error") or snapshot.get("status") or "blocked"))
            time.sleep(pause)
            continue
        for cid in snapshot.get("ids") or []:
            _append_candidate(cid, query, "html-extract")
            time.sleep(pause)
        time.sleep(pause)

    candidates.sort(key=lambda row: (-float(row.get("confidence") or 0.0), str(row.get("complex", {}).get("name") or ""), str(row.get("complex_id") or "")))
    chosen = candidates[0] if candidates else None
    verification_status = "blocked" if (not chosen and blocked_reasons) else (chosen.get("status") if chosen else "unresolved")
    confidence = float(chosen.get("confidence") or 0.0) if chosen else 0.0
    complex_info = (chosen or {}).get("complex") or {}

    return {
        "name": seed.get("name"),
        "district": seed.get("district"),
        "neighborhood": seed.get("neighborhood"),
        "seed_input": seed,
        "complex_id": complex_info.get("complex_id") or (chosen or {}).get("complex_id"),
        "address": complex_info.get("address") or seed.get("address") or "",
        "household_count": complex_info.get("household_count"),
        "aliases": aliases,
        "verification_status": verification_status,
        "confidence": round(confidence, 3),
        "source": "generated:web-search+detail",
        "learned_from": "build_candidate_seeds.py",
        "note": seed.get("note") or "generated candidate seed",
        "candidate_pool": candidates[:5],
        "evidence": evidence[:8],
        "blocked_reasons": _dedupe_keep_order(blocked_reasons)[:5],
    }


def build_generated_payload(seed_items: list[dict[str, Any]], *, pause: float = 0.6) -> dict[str, Any]:
    generated = [build_entry(seed, pause=pause) for seed in seed_items]
    entries = [
        {
            "complex_id": row.get("complex_id"),
            "name": row.get("name"),
            "address": row.get("address"),
            "household_count": row.get("household_count"),
            "aliases": row.get("aliases") or [],
            "note": row.get("note"),
            "source": row.get("source"),
            "learned_from": row.get("learned_from"),
            "confidence": row.get("confidence"),
            "verification_status": row.get("verification_status"),
        }
        for row in generated
        if row.get("complex_id") and row.get("verification_status") in {"verified", "weak-verified"}
    ]
    unresolved = [
        {
            "name": row.get("name"),
            "district": row.get("district"),
            "neighborhood": row.get("neighborhood"),
            "aliases": row.get("aliases") or [],
            "verification_status": row.get("verification_status"),
            "confidence": row.get("confidence"),
            "blocked_reasons": row.get("blocked_reasons") or [],
        }
        for row in generated if not row.get("complex_id")
    ]
    return {
        "kind": "naver-real-estate-candidate-seed-generation",
        "schema_version": 1,
        "generated_at": int(time.time()),
        "source_input": str(DEFAULT_INPUT),
        "entry_count": len(entries),
        "unresolved_count": len(unresolved),
        "entries": entries,
        "unresolved": unresolved,
        "results": generated,
    }


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="네이버 부동산 candidate seed 자동 생성기")
    p.add_argument("--input", default=str(DEFAULT_INPUT), help="seed 입력 JSON 파일")
    p.add_argument("--output", default=str(DEFAULT_OUTPUT), help="생성 결과 JSON 파일")
    p.add_argument("--pause", type=float, default=0.7, help="요청 사이 pause seconds")
    p.add_argument("--print-summary", action="store_true", help="간단 요약 출력")
    return p


def main() -> int:
    args = build_parser().parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    payload = _load_json(input_path, {"seeds": []})
    seed_items = payload.get("seeds") if isinstance(payload, dict) else payload
    if not seed_items:
        raise SystemExit(f"seed 입력이 비어 있습니다: {input_path}")
    generated = build_generated_payload(list(seed_items), pause=max(0.0, float(args.pause)))
    generated["source_input"] = str(input_path)
    _write_json(output_path, generated)
    if args.print_summary:
        print(json.dumps({
            "output": str(output_path),
            "entry_count": generated.get("entry_count"),
            "unresolved_count": generated.get("unresolved_count"),
            "resolved": [
                {
                    "name": row.get("name"),
                    "complex_id": row.get("complex_id"),
                    "confidence": row.get("confidence"),
                    "verification_status": row.get("verification_status"),
                }
                for row in generated.get("results", [])
            ],
        }, ensure_ascii=False, indent=2))
    else:
        print(str(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
