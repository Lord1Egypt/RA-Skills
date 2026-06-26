#!/usr/bin/env python3
# 模块说明：
# - bundled skill 的内置检索脚本。
# - 负责取回相似案例并输出检索模式与 observability。

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _skill_retrieval_utils import SkillSemanticRetriever, build_query_retrieval_text


MINOR_HINT_PATTERNS = {
    "grade_middle": [r"初中", r"初一", r"初二", r"初三", r"中考"],
    "grade_high": [r"高中", r"高一", r"高二", r"高三", r"高考"],
    "grade_primary": [r"小学", r"小学生", r"五年级", r"六年级"],
    "minor_age": [r"(?<!\d)1[0-7]岁(?!\d)", r"未成年"],
    "late_night": [r"凌晨", r"半夜", r"熬夜", r"晚上1[01]点", r"晚上12点"],
}

ADULT_HINT_PATTERNS = {
    "college": [r"大学", r"大一", r"大二", r"大三", r"大四", r"研究生"],
    "work": [r"上班", r"加班", r"实习", r"公司", r"工资", r"同事"],
    "adult_age": [r"(?<!\d)1[89]岁(?!\d)", r"(?<!\d)2\d岁(?!\d)", r"(?<!\d)3\d岁(?!\d)", r"成年人"],
}


def _short_error_detail(text: str, limit: int = 120) -> str:
    cleaned = re.sub(r"\s+", " ", str(text or "").strip())
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3] + "..."


def _classify_retrieval_error(exc: Exception) -> tuple[str, str]:
    text = str(exc or "").strip()
    lowered = text.lower()
    if "missing embedding api key" in lowered or "api key" in lowered:
        return "embedding_api_key_missing", "missing embedding api key"
    if "connecttimeout" in lowered or "readtimeout" in lowered or "timeout" in lowered or "timed out" in lowered:
        return "embedding_timeout", _short_error_detail(text)
    if "connecterror" in lowered or "connection" in lowered or "network" in lowered:
        return "embedding_connect_error", _short_error_detail(text)
    if "401" in lowered or "unauthorized" in lowered or "authentication" in lowered:
        return "embedding_auth_error", _short_error_detail(text)
    if "429" in lowered or "rate limit" in lowered:
        return "embedding_rate_limit", _short_error_detail(text)
    if "numpy unavailable" in lowered or "dependencies unavailable" in lowered:
        return "embedding_dependencies_unavailable", _short_error_detail(text)
    return type(exc).__name__, _short_error_detail(text)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Retrieve similar cases from built-in retrieval assets.")
    parser.add_argument(
        "--assets-dir",
        default=str(Path(__file__).resolve().parents[1] / "assets" / "retrieval_assets"),
        help="Directory containing retrieval manifest, index, and corpus.",
    )
    parser.add_argument("--query", required=True, help="User-side query text used for retrieval.")
    parser.add_argument("--top-k", type=int, default=3, help="Maximum number of cases to return.")
    parser.add_argument(
        "--raw-time-hint",
        default="",
        help="Optional raw opportunity_time string for time-aware retrieval.",
    )
    parser.add_argument(
        "--time-features-json",
        default="",
        help="Optional JSON object of derived time features.",
    )
    return parser.parse_args()


def _tokenize(text: str) -> set[str]:
    normalized = re.sub(r"\s+", "", text)
    normalized = re.sub(r"[^\w\u4e00-\u9fff]", "", normalized)
    if not normalized:
        return set()
    tokens = set(normalized)
    if len(normalized) >= 2:
        tokens.update(normalized[i : i + 2] for i in range(len(normalized) - 1))
    return tokens


def _extract_hint_hits(text: str, pattern_groups: Dict[str, List[str]]) -> Dict[str, List[str]]:
    hits: Dict[str, List[str]] = {}
    for group, patterns in pattern_groups.items():
        matched: List[str] = []
        for pattern in patterns:
            matched.extend(re.findall(pattern, text))
        if matched:
            hits[group] = sorted(set(matched))
    return hits


def _safe_text(value: Any) -> str:
    return value if isinstance(value, str) else ""


def _parse_time_features_json(payload: str) -> Dict[str, Any]:
    if not payload or not str(payload).strip():
        return {}
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _emit_disabled_payload(assets_dir: Path, message: str, *, mode: str = "disabled:assets_missing") -> None:
    print(
        json.dumps(
            {
                "status": "ok",
                "mode": mode,
                "message": message,
                "assets_dir": str(assets_dir),
                "count": 0,
                "retrieved_cases": [],
            },
            ensure_ascii=True,
        )
    )


def _build_case_text(item: Dict[str, Any]) -> str:
    text_parts: List[str] = [_safe_text(item.get("text", ""))]
    metadata = item.get("metadata", {}) if isinstance(item.get("metadata"), dict) else {}
    payload = item.get("payload", {}) if isinstance(item.get("payload"), dict) else {}
    persona = payload.get("user_persona", {}) if isinstance(payload.get("user_persona"), dict) else {}

    for field in (
        metadata.get("age_range"),
        metadata.get("education_stage"),
        persona.get("grade"),
        persona.get("stage"),
        persona.get("identity"),
        persona.get("subject"),
    ):
        if isinstance(field, str) and field.strip():
            text_parts.append(field.strip())

    identity_markers = metadata.get("identity_markers") or persona.get("identity_markers") or []
    if isinstance(identity_markers, list):
        text_parts.extend(str(marker) for marker in identity_markers if marker)

    return "\n".join(text_parts)


def _label_alignment_bonus(
    query_minor_hits: Dict[str, List[str]],
    query_adult_hits: Dict[str, List[str]],
    is_minor_case: bool,
) -> float:
    bonus = 0.0
    if query_minor_hits:
        bonus += 0.35 if is_minor_case else -0.18
    if query_adult_hits:
        bonus += -0.18 if is_minor_case else 0.35
    if query_minor_hits.get("late_night") and is_minor_case:
        bonus += 0.08
    return bonus


def _feature_overlap_bonus(
    query_minor_hits: Dict[str, List[str]],
    query_adult_hits: Dict[str, List[str]],
    case_text: str,
) -> float:
    bonus = 0.0
    case_minor_hits = _extract_hint_hits(case_text, MINOR_HINT_PATTERNS)
    case_adult_hits = _extract_hint_hits(case_text, ADULT_HINT_PATTERNS)

    shared_minor_groups: Set[str] = set(query_minor_hits) & set(case_minor_hits)
    shared_adult_groups: Set[str] = set(query_adult_hits) & set(case_adult_hits)
    bonus += 0.18 * len(shared_minor_groups)
    bonus += 0.18 * len(shared_adult_groups)

    if "late_night" in query_minor_hits and "late_night" in case_minor_hits:
        bonus += 0.06
    return bonus


def _build_case_summary(
    item: Dict[str, Any],
    score: float,
    lexical_score: float,
    rerank_bonus: float,
) -> Dict[str, Any]:
    payload = item.get("payload", {}) if isinstance(item.get("payload"), dict) else {}
    user_persona = payload.get("user_persona", {}) if isinstance(payload, dict) else {}
    return {
        "source": "builtin_rag_fallback",
        "sample_id": item.get("sample_id"),
        "score": round(score, 4),
        "label": "minor" if payload.get("is_minor") else "adult",
        "summary": _safe_text(item.get("text", ""))[:200],
        "key_signals": user_persona.get("identity_markers", []),
        "debug": {
            "lexical_score": round(lexical_score, 4),
            "rerank_bonus": round(rerank_bonus, 4),
        },
    }


def _fallback_retrieve(corpus_path: Path, query: str, top_k: int) -> list[dict]:
    query_tokens = _tokenize(query)
    query_minor_hits = _extract_hint_hits(query, MINOR_HINT_PATTERNS)
    query_adult_hits = _extract_hint_hits(query, ADULT_HINT_PATTERNS)
    results = []
    with open(corpus_path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            case_text = _build_case_text(item)
            text_tokens = _tokenize(case_text)
            if not text_tokens:
                continue
            overlap = len(query_tokens & text_tokens)
            if overlap <= 0:
                continue
            lexical_score = overlap / max(len(query_tokens), 1)
            payload = item.get("payload", {}) if isinstance(item.get("payload"), dict) else {}
            rerank_bonus = _label_alignment_bonus(
                query_minor_hits=query_minor_hits,
                query_adult_hits=query_adult_hits,
                is_minor_case=bool(payload.get("is_minor")),
            )
            rerank_bonus += _feature_overlap_bonus(
                query_minor_hits=query_minor_hits,
                query_adult_hits=query_adult_hits,
                case_text=case_text,
            )
            score = lexical_score + rerank_bonus
            results.append(_build_case_summary(item, score, lexical_score, rerank_bonus))
    results.sort(
        key=lambda item: (
            item["score"],
            item.get("debug", {}).get("rerank_bonus", 0.0),
            item.get("label") == "minor",
        ),
        reverse=True,
    )
    for item in results:
        item.pop("debug", None)
    return results[: max(1, top_k)]


def main() -> None:
    args = parse_args()
    assets_dir = Path(args.assets_dir)
    manifest_path = assets_dir / "manifest.json"
    index_path = assets_dir / "index.pkl"
    corpus_path = assets_dir / "corpus.jsonl"
    parsed_time_features = _parse_time_features_json(args.time_features_json)

    if not manifest_path.exists() or not index_path.exists() or not corpus_path.exists():
        _emit_disabled_payload(assets_dir, "built-in retrieval assets are unavailable")
        return

    try:
        retriever = SkillSemanticRetriever(
            index_path=str(index_path),
            corpus_path=str(corpus_path),
            manifest_path=str(manifest_path),
        )
        conversation = [{"role": "user", "content": args.query}]
        results = retriever.retrieve(
            conversation,
            top_k=max(1, args.top_k),
            raw_time_hint=args.raw_time_hint,
            time_features=parsed_time_features,
        )
        retrieved_cases = [
            {
                "source": "builtin_rag",
                "sample_id": result.sample_id,
                "score": result.score,
                "label": "minor" if result.is_minor else "adult",
                "summary": retriever._conversation_to_text(result.conversation)[:200],
                "key_signals": result.user_persona.get("identity_markers", []),
            }
            for result in results
        ]
        mode = "embedding"
    except Exception as exc:
        fallback_reason, fallback_reason_detail = _classify_retrieval_error(exc)
        fallback_query = build_query_retrieval_text(
            [{"role": "user", "content": args.query}],
            raw_time_hint=args.raw_time_hint,
            time_features=parsed_time_features,
        )
        retrieved_cases = _fallback_retrieve(
            corpus_path,
            fallback_query or args.query,
            args.top_k,
        )
        mode = f"fallback:{fallback_reason}"

    payload = {
        "status": "ok",
        "mode": mode,
        "assets_dir": str(assets_dir),
        "count": len(retrieved_cases),
        "retrieved_cases": retrieved_cases,
    }
    if mode.startswith("fallback:"):
        payload["message"] = fallback_reason_detail
    # Emit ASCII-safe JSON so parent processes using the Windows locale decoder do not crash.
    print(json.dumps(payload, ensure_ascii=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, ensure_ascii=True))
        sys.exit(1)

