#!/usr/bin/env python3
"""
Modeio AI Anonymization Skill local privacy detector (no API required).

This detector is local-first and deterministic:
- regex/pattern matching
- per-type validators (checksum/date/format)
- heuristic detection scoring with profile thresholds
- allowlist/blocklist policy hooks
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Tuple
from modeio_redact.detection.data import (
    BASE_CONFIDENCE_BY_TYPE,
    BASE_THRESHOLDS_BALANCED,
    BUILTIN_ALLOWLIST_RULES,
    CN_ID_CHECK_DIGITS,
    CN_ID_WEIGHTS,
    COMPILED_PATTERNS,
    CONTEXT_KEYWORDS,
    DETECTOR_VERSION,
    HIGH_RISK_TYPES,
    MEDIUM_RISK_TYPES,
    NAME_CONTEXT_PATTERNS,
    NAME_STOPWORDS_CN,
    NAME_STOPWORDS_EN,
    NEGATIVE_CONTEXT_KEYWORDS,
    PLACEHOLDER_MAP,
    PLACEHOLDER_PATTERN,
    PROFILE_CHOICES,
    PROFILE_THRESHOLD_DELTA,
    REQUIRED_VALIDATOR_TYPES,
    RISK_WEIGHTS,
    RULE_KIND_EXACT,
    RULE_KIND_REGEX,
    SCORING_METHOD,
    SENSITIVE_TYPES,
    TYPE_LABELS,
)

RiskLevel = Literal["low", "medium", "high"]


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _digits_only(value: str) -> str:
    return re.sub(r"\D", "", value)


def _infer_risk_level(stype: str) -> RiskLevel:
    if stype in HIGH_RISK_TYPES:
        return "high"
    if stype in MEDIUM_RISK_TYPES:
        return "medium"
    return "low"


def _risk_priority(stype: str) -> int:
    level = _infer_risk_level(stype)
    if level == "high":
        return 3
    if level == "medium":
        return 2
    return 1


def _calculate_risk_score(items: List[Dict[str, Any]]) -> int:
    if not items:
        return 0

    type_count: Dict[str, int] = {}
    for item in items:
        stype = item["type"]
        type_count[stype] = type_count.get(stype, 0) + 1

    score = 0.0
    for stype, count in type_count.items():
        weight = RISK_WEIGHTS.get(stype, 15)
        score += weight + (count - 1) * weight * 0.3

    if len(type_count) >= 2:
        score *= 1 + (len(type_count) - 1) * 0.15

    return int(_clamp(round(score), 0, 100))


def _generate_placeholder(stype: str, index: int) -> str:
    tag = PLACEHOLDER_MAP.get(stype, "PII")
    return f"[{tag}_{index}]"


def _is_overlapping(start: int, end: int, ranges: List[Tuple[int, int]]) -> bool:
    for rs, re_ in ranges:
        if (start >= rs and start < re_) or (end > rs and end <= re_) or (start <= rs and end >= re_):
            return True
    return False


def _is_valid_date(value: str, fmt: str) -> bool:
    try:
        datetime.strptime(value, fmt)
    except ValueError:
        return False
    return True


def _is_luhn_valid(value: str) -> bool:
    digits = _digits_only(value)
    if len(digits) < 13 or len(digits) > 19:
        return False
    if len(set(digits)) == 1:
        return False

    total = 0
    reverse_digits = digits[::-1]
    for idx, char in enumerate(reverse_digits):
        num = int(char)
        if idx % 2 == 1:
            num *= 2
            if num > 9:
                num -= 9
        total += num
    return total % 10 == 0


def _validate_id_card(value: str) -> Tuple[bool, str]:
    raw = value.strip().upper()

    if re.fullmatch(r"[A-Z]{1,2}\d{6}\([0-9A]\)", raw):
        return True, "hk_id_format"
    if re.fullmatch(r"[A-Z][12]\d{8}", raw):
        return True, "tw_id_format"

    if re.fullmatch(r"\d{15}", raw):
        birth = "19" + raw[6:12]
        if _is_valid_date(birth, "%Y%m%d"):
            return True, "cn_15digit_date_valid"
        return False, "cn_15digit_invalid_birth_date"

    if re.fullmatch(r"\d{17}[\dX]", raw):
        birth = raw[6:14]
        if not _is_valid_date(birth, "%Y%m%d"):
            return False, "cn_18digit_invalid_birth_date"
        checksum = sum(int(raw[i]) * CN_ID_WEIGHTS[i] for i in range(17)) % 11
        expected = CN_ID_CHECK_DIGITS[checksum]
        if raw[-1] != expected:
            return False, "cn_18digit_checksum_fail"
        return True, "cn_18digit_checksum_pass"

    return False, "id_format_fail"


def _validate_credit_card(value: str) -> Tuple[bool, str]:
    if _is_luhn_valid(value):
        return True, "luhn_pass"
    return False, "luhn_fail"


def _validate_bank_card(value: str) -> Tuple[bool, str]:
    digits = _digits_only(value)
    if len(digits) < 13 or len(digits) > 19:
        return False, "bank_card_length_fail"
    if _is_luhn_valid(value):
        return True, "luhn_pass"
    return False, "luhn_fail"


def _validate_ssn(value: str) -> Tuple[bool, str]:
    raw = value.strip().upper().replace(" ", "")

    us_match = re.fullmatch(r"(\d{3})-(\d{2})-(\d{4})", raw)
    if us_match:
        area, group, serial = us_match.groups()
        if area in {"000", "666"} or area.startswith("9"):
            return False, "us_ssn_invalid_area"
        if group == "00" or serial == "0000":
            return False, "us_ssn_invalid_group_or_serial"
        return True, "us_ssn_format"

    if re.fullmatch(r"[A-CEGHJ-PR-TW-Z]{2}\d{6}[A-D]", raw):
        return True, "uk_nino_format"

    return False, "ssn_format_fail"


def _validate_passport(value: str) -> Tuple[bool, str]:
    raw = value.strip().upper().replace(" ", "")
    if re.fullmatch(r"[EGDSPH][A-Z]?\d{8}", raw):
        return True, "cn_passport_format"
    if re.fullmatch(r"[A-Z]{2}\d{7}", raw):
        return True, "passport_format"
    return False, "passport_format_fail"


def _run_validator(stype: str, value: str) -> Tuple[bool, str]:
    if stype == "idCard":
        return _validate_id_card(value)
    if stype == "creditCard":
        return _validate_credit_card(value)
    if stype == "bankCard":
        return _validate_bank_card(value)
    if stype == "ssn":
        return _validate_ssn(value)
    if stype == "passport":
        return _validate_passport(value)
    return True, "validator_not_required"


def _normalize_rule(raw_rule: Dict[str, Any], list_name: str) -> Dict[str, Any]:
    if not isinstance(raw_rule, dict):
        raise ValueError(f"{list_name} rule must be an object")

    stype = str(raw_rule.get("type", "*")).strip()
    if stype != "*" and stype not in SENSITIVE_TYPES:
        raise ValueError(f"{list_name} rule has unsupported type: {stype}")
    if list_name == "blocklist" and stype == "*":
        raise ValueError("blocklist rule requires explicit type")

    kind = str(raw_rule.get("kind", RULE_KIND_EXACT)).strip().lower()
    if kind not in {RULE_KIND_EXACT, RULE_KIND_REGEX}:
        raise ValueError(f"{list_name} rule has unsupported kind: {kind}")

    value = raw_rule.get("value")
    if not isinstance(value, str) or not value:
        raise ValueError(f"{list_name} rule must provide non-empty string value")

    case_sensitive = bool(raw_rule.get("caseSensitive", False))
    flags = 0 if case_sensitive else re.IGNORECASE

    normalized: Dict[str, Any] = {
        "__compiled": True,
        "type": stype,
        "kind": kind,
        "value": value,
        "caseSensitive": case_sensitive,
    }

    if kind == RULE_KIND_EXACT:
        normalized["needle"] = value if case_sensitive else value.lower()
        normalized["pattern_search"] = re.compile(re.escape(value), flags)
    else:
        try:
            normalized["pattern_full"] = re.compile(value, flags)
            normalized["pattern_search"] = re.compile(value, flags)
        except re.error as exc:
            raise ValueError(f"{list_name} rule has invalid regex: {value}") from exc

    return normalized


def _normalize_runtime_rules(
    rules: Optional[List[Dict[str, Any]]], list_name: str
) -> List[Dict[str, Any]]:
    if not rules:
        return []

    normalized: List[Dict[str, Any]] = []
    for raw_rule in rules:
        if isinstance(raw_rule, dict) and raw_rule.get("__compiled"):
            normalized.append(raw_rule)
            continue
        normalized.append(_normalize_rule(raw_rule, list_name))
    return normalized


def _load_rules_from_file(path: Optional[str], list_name: str) -> List[Dict[str, Any]]:
    if not path:
        return []
    try:
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except OSError as exc:
        raise ValueError(f"failed to read {list_name} file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {list_name} file: {path}") from exc

    if isinstance(payload, list):
        raw_rules = payload
    elif isinstance(payload, dict):
        if list_name in payload and isinstance(payload[list_name], list):
            raw_rules = payload[list_name]
        elif "rules" in payload and isinstance(payload["rules"], list):
            raw_rules = payload["rules"]
        else:
            raise ValueError(f"{list_name} file must contain a list or '{list_name}'/'rules' array")
    else:
        raise ValueError(f"{list_name} file must contain JSON list/object")

    return _normalize_runtime_rules(raw_rules, list_name)


def _load_threshold_overrides(path: Optional[str]) -> Dict[str, float]:
    if not path:
        return {}

    try:
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except OSError as exc:
        raise ValueError(f"failed to read thresholds file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in thresholds file: {path}") from exc

    if not isinstance(payload, dict):
        raise ValueError("thresholds file must be a JSON object of type->number")

    overrides: Dict[str, float] = {}
    for key, value in payload.items():
        if key not in SENSITIVE_TYPES:
            raise ValueError(f"threshold override has unsupported type: {key}")
        if not isinstance(value, (int, float)):
            raise ValueError(f"threshold override for {key} must be numeric")
        overrides[key] = float(value)
    return overrides


def _build_thresholds(profile: str, overrides: Optional[Dict[str, float]] = None) -> Dict[str, float]:
    if profile not in PROFILE_CHOICES:
        raise ValueError(f"unsupported profile: {profile}")

    delta = PROFILE_THRESHOLD_DELTA[profile]
    thresholds: Dict[str, float] = {}
    for stype in SENSITIVE_TYPES:
        base = BASE_THRESHOLDS_BALANCED.get(stype, 0.7)
        thresholds[stype] = round(_clamp(base + delta, 0.05, 0.99), 3)

    if overrides:
        for stype, value in overrides.items():
            if stype in SENSITIVE_TYPES:
                thresholds[stype] = round(_clamp(float(value), 0.05, 0.99), 3)

    return thresholds


def _rule_matches_value(rule: Dict[str, Any], stype: str, value: str) -> bool:
    if rule["type"] not in {"*", stype}:
        return False

    if rule["kind"] == RULE_KIND_EXACT:
        expected = rule["needle"]
        target = value if rule["caseSensitive"] else value.lower()
        return target == expected

    pattern = rule.get("pattern_full")
    return bool(pattern and pattern.fullmatch(value))


def _matches_any_rule(rules: List[Dict[str, Any]], stype: str, value: str) -> bool:
    for rule in rules:
        if _rule_matches_value(rule, stype, value):
            return True
    return False


def _collect_regex_candidates(text: str) -> List[Dict[str, Any]]:
    candidates: List[Dict[str, Any]] = []
    for entry in COMPILED_PATTERNS:
        stype = entry["type"]
        label = entry["label"]
        for pattern in entry["patterns"]:
            for match in pattern.finditer(text):
                value = match.group(0)
                if not value:
                    continue
                candidates.append(
                    {
                        "type": stype,
                        "label": label,
                        "value": value,
                        "startIndex": match.start(),
                        "endIndex": match.end(),
                        "source": "regex",
                    }
                )
    return candidates


def _is_valid_name_candidate(value: str, lang: str) -> bool:
    cleaned = value.strip().strip("\"'`")
    if not cleaned:
        return False
    lower = cleaned.lower()

    if any(char.isdigit() for char in cleaned):
        return False
    if "@" in cleaned or "http://" in lower or "https://" in lower:
        return False
    if "_" in cleaned or "/" in cleaned:
        return False

    if lang == "cn":
        if not re.fullmatch(r"[\u4e00-\u9fa5·]{2,6}", cleaned):
            return False
        if any(token in cleaned for token in NAME_STOPWORDS_CN):
            return False
        return True

    normalized = re.sub(r"\s+", " ", cleaned)
    if not re.fullmatch(r"[A-Za-z]+(?:[ '-][A-Za-z]+){1,2}", normalized):
        return False
    tokens = [tok for tok in re.split(r"[ '-]+", normalized) if tok]
    if len(tokens) < 2 or len(tokens) > 3:
        return False
    if any(tok.lower() in NAME_STOPWORDS_EN for tok in tokens):
        return False
    if any(len(tok) < 2 for tok in tokens):
        return False
    if any(not tok[0].isupper() for tok in tokens):
        return False
    return True


def _detect_names_by_context(text: str) -> List[Dict[str, Any]]:
    names: List[Dict[str, Any]] = []
    seen: set[Tuple[int, int, str]] = set()
    for entry in NAME_CONTEXT_PATTERNS:
        lang = entry["lang"]
        pattern = entry["pattern"]
        for match in pattern.finditer(text):
            value = match.group(1).strip().strip("\"'`")
            start_index = match.start(1)
            end_index = match.end(1)
            key = (start_index, end_index, value)
            if key in seen:
                continue
            if not _is_valid_name_candidate(value, lang):
                continue
            seen.add(key)
            names.append(
                {
                    "type": "name",
                    "label": TYPE_LABELS["name"],
                    "value": value,
                    "startIndex": start_index,
                    "endIndex": end_index,
                    "source": "name-context",
                }
            )
    return names


def _collect_blocklist_candidates(
    text: str, blocklist_rules: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    candidates: List[Dict[str, Any]] = []
    for rule in blocklist_rules:
        pattern = rule.get("pattern_search")
        if pattern is None:
            continue
        stype = rule["type"]
        label = TYPE_LABELS.get(stype, stype)
        for match in pattern.finditer(text):
            value = match.group(0)
            if not value:
                continue
            candidates.append(
                {
                    "type": stype,
                    "label": label,
                    "value": value,
                    "startIndex": match.start(),
                    "endIndex": match.end(),
                    "source": "blocklist",
                }
            )
    return candidates


def _dedupe_candidates(candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    source_priority = {"blocklist": 3, "name-context": 2, "regex": 1}
    deduped: Dict[Tuple[str, int, int, str], Dict[str, Any]] = {}
    for candidate in candidates:
        key = (
            candidate["type"],
            candidate["startIndex"],
            candidate["endIndex"],
            candidate["value"],
        )
        existing = deduped.get(key)
        if not existing:
            deduped[key] = candidate
            continue
        if source_priority.get(candidate["source"], 0) > source_priority.get(existing["source"], 0):
            deduped[key] = candidate
    return list(deduped.values())


def _context_bonus(text: str, start_index: int, end_index: int, stype: str) -> float:
    left = max(0, start_index - 36)
    right = min(len(text), end_index + 36)
    window = text[left:right].lower()

    bonus = 0.0
    positive_keywords = CONTEXT_KEYWORDS.get(stype, [])
    if any(keyword in window for keyword in positive_keywords):
        bonus += 0.08

    negative_keywords = NEGATIVE_CONTEXT_KEYWORDS.get(stype, [])
    if any(keyword in window for keyword in negative_keywords):
        bonus -= 0.12

    return bonus


def _test_data_penalty(stype: str, value: str) -> float:
    lowered = value.lower()
    if stype in {"apiKey", "password"} and any(token in lowered for token in ["example", "sample", "dummy"]):
        return -0.15

    return 0.0


def _score_candidate(
    candidate: Dict[str, Any],
    text: str,
    validator_passed: bool,
) -> Tuple[float, List[str]]:
    stype = candidate["type"]
    start_index = candidate["startIndex"]
    end_index = candidate["endIndex"]
    source = candidate["source"]

    score = BASE_CONFIDENCE_BY_TYPE.get(stype, 0.65)
    reasons = [f"base:{score:.2f}"]

    if source == "name-context":
        score = max(score, 0.88)
        reasons.append("source:name-context")

    if stype in REQUIRED_VALIDATOR_TYPES and validator_passed:
        score += 0.10
        reasons.append("validator:bonus")

    context_adjustment = _context_bonus(text, start_index, end_index, stype)
    if context_adjustment != 0:
        score += context_adjustment
        reasons.append(f"context:{context_adjustment:+.2f}")

    penalty = _test_data_penalty(stype, candidate["value"])
    if penalty != 0:
        score += penalty
        reasons.append(f"penalty:{penalty:+.2f}")

    score = round(_clamp(score, 0.0, 1.0), 3)
    return score, reasons


def _evaluate_candidates(
    text: str,
    candidates: List[Dict[str, Any]],
    allowlist_rules: List[Dict[str, Any]],
    blocklist_rules: List[Dict[str, Any]],
    thresholds: Dict[str, float],
) -> List[Dict[str, Any]]:
    evaluated: List[Dict[str, Any]] = []

    for candidate in candidates:
        stype = candidate["type"]
        value = candidate["value"].strip()
        if not value:
            continue

        if PLACEHOLDER_PATTERN.fullmatch(value):
            continue

        source = candidate["source"]
        forced_blocklist = source == "blocklist" or _matches_any_rule(blocklist_rules, stype, value)

        if not forced_blocklist and _matches_any_rule(allowlist_rules, stype, value):
            continue

        validator_applied = stype in REQUIRED_VALIDATOR_TYPES
        validator_passed = True
        validator_reason = "validator_not_required"

        if validator_applied and not forced_blocklist:
            validator_passed, validator_reason = _run_validator(stype, value)
            if not validator_passed:
                continue

        if forced_blocklist:
            detection_score = 1.0
            score_reasons = ["source:blocklist"]
        else:
            detection_score, score_reasons = _score_candidate(candidate, text, validator_passed)

        threshold = thresholds.get(stype, 0.70)
        if not forced_blocklist and detection_score < threshold:
            continue

        evaluated.append(
            {
                **candidate,
                "detectionScore": detection_score,
                "scoreThreshold": threshold,
                "scoreReasons": score_reasons,
                "confidence": detection_score,
                "confidenceThreshold": threshold,
                "confidenceReasons": score_reasons,
                "validator": {
                    "applied": validator_applied,
                    "passed": validator_passed,
                    "reason": validator_reason,
                },
                "forcedBlocklist": forced_blocklist,
            }
        )

    return evaluated


def _resolve_overlaps(candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not candidates:
        return []

    sorted_candidates = sorted(
        candidates,
        key=lambda item: (
            -int(item.get("forcedBlocklist", False)),
            -float(item.get("detectionScore", item.get("confidence", 0.0))),
            -_risk_priority(item["type"]),
            -(item["endIndex"] - item["startIndex"]),
            item["startIndex"],
        ),
    )

    selected: List[Dict[str, Any]] = []
    selected_ranges: List[Tuple[int, int]] = []

    for candidate in sorted_candidates:
        start_index = candidate["startIndex"]
        end_index = candidate["endIndex"]
        if _is_overlapping(start_index, end_index, selected_ranges):
            continue
        selected.append(candidate)
        selected_ranges.append((start_index, end_index))

    selected.sort(key=lambda item: item["startIndex"])
    return selected


def _build_items(selected_candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    type_counters: Dict[str, int] = {}
    items: List[Dict[str, Any]] = []
    item_id = 0

    for candidate in selected_candidates:
        stype = candidate["type"]
        type_counters[stype] = type_counters.get(stype, 0) + 1
        masked = _generate_placeholder(stype, type_counters[stype])
        item_id += 1

        items.append(
            {
                "id": str(item_id),
                "type": stype,
                "label": candidate["label"],
                "value": candidate["value"],
                "maskedValue": masked,
                "riskLevel": _infer_risk_level(stype),
                "startIndex": candidate["startIndex"],
                "endIndex": candidate["endIndex"],
                "detectionScore": candidate["detectionScore"],
                "scoreThreshold": candidate["scoreThreshold"],
                "scoreReasons": candidate["scoreReasons"],
                "confidence": candidate["detectionScore"],
                "confidenceThreshold": candidate["scoreThreshold"],
                "detectionSource": candidate["source"],
                "confidenceReasons": candidate["scoreReasons"],
                "validator": candidate["validator"],
                "forcedBlocklist": bool(candidate.get("forcedBlocklist", False)),
            }
        )

    return items


def _sanitize_text(text: str, items: List[Dict[str, Any]]) -> str:
    sanitized = text
    for item in sorted(items, key=lambda entry: -entry["startIndex"]):
        sanitized = sanitized[: item["startIndex"]] + item["maskedValue"] + sanitized[item["endIndex"] :]
    return sanitized


def detect_sensitive_local(
    text: str,
    profile: str = "balanced",
    allowlist_rules: Optional[List[Dict[str, Any]]] = None,
    blocklist_rules: Optional[List[Dict[str, Any]]] = None,
    threshold_overrides: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """
    Local PII detection with validators, heuristic scoring, and policy thresholds.
    """
    if not text or len(text) < 5:
        return {
            "originalText": text or "",
            "sanitizedText": text or "",
            "items": [],
            "riskScore": 0,
            "riskLevel": "low",
            "profile": profile,
            "thresholds": _build_thresholds(profile, threshold_overrides),
            "scoringMethod": SCORING_METHOD,
            "detectorVersion": DETECTOR_VERSION,
        }

    normalized_allowlist = list(_normalize_runtime_rules(BUILTIN_ALLOWLIST_RULES, "allowlist"))
    normalized_allowlist.extend(_normalize_runtime_rules(allowlist_rules, "allowlist"))
    normalized_blocklist = _normalize_runtime_rules(blocklist_rules, "blocklist")
    thresholds = _build_thresholds(profile, threshold_overrides)

    candidates = _collect_regex_candidates(text)
    candidates.extend(_detect_names_by_context(text))
    candidates.extend(_collect_blocklist_candidates(text, normalized_blocklist))
    candidates = _dedupe_candidates(candidates)

    evaluated = _evaluate_candidates(
        text=text,
        candidates=candidates,
        allowlist_rules=normalized_allowlist,
        blocklist_rules=normalized_blocklist,
        thresholds=thresholds,
    )

    selected = _resolve_overlaps(evaluated)
    items = _build_items(selected)
    sanitized = _sanitize_text(text, items)

    risk_score = _calculate_risk_score(items)
    risk_level: RiskLevel = "high" if risk_score >= 60 else "medium" if risk_score >= 30 else "low"

    return {
        "originalText": text,
        "sanitizedText": sanitized,
        "items": items,
        "riskScore": risk_score,
        "riskLevel": risk_level,
        "profile": profile,
        "thresholds": thresholds,
        "scoringMethod": SCORING_METHOD,
        "detectorVersion": DETECTOR_VERSION,
        "stats": {
            "candidateCount": len(candidates),
            "keptCount": len(items),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Local PII detection (no API call): regex + validators + heuristic thresholds. "
            "Outputs masked text by default; use --json for full details."
        )
    )
    parser.add_argument("-i", "--input", type=str, default=None)
    parser.add_argument(
        "--profile",
        type=str,
        choices=PROFILE_CHOICES,
        default="balanced",
        help="Threshold profile for local detection (default: balanced).",
    )
    parser.add_argument(
        "--allowlist-file",
        type=str,
        default=None,
        help="Path to JSON allowlist rule file.",
    )
    parser.add_argument(
        "--blocklist-file",
        type=str,
        default=None,
        help="Path to JSON blocklist rule file.",
    )
    parser.add_argument(
        "--thresholds-file",
        type=str,
        default=None,
        help="Path to JSON per-type threshold override file.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output full JSON; otherwise only output sanitizedText.",
    )
    parser.add_argument(
        "--explain",
        action="store_true",
        help="Include scoring metadata in non-JSON output for troubleshooting.",
    )
    args = parser.parse_args()

    raw = args.input or ""
    if not raw.strip():
        print("Error: input is empty", file=sys.stderr)
        sys.exit(1)

    try:
        allowlist_rules = _load_rules_from_file(args.allowlist_file, "allowlist")
        blocklist_rules = _load_rules_from_file(args.blocklist_file, "blocklist")
        threshold_overrides = _load_threshold_overrides(args.thresholds_file)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)

    result = detect_sensitive_local(
        raw,
        profile=args.profile,
        allowlist_rules=allowlist_rules,
        blocklist_rules=blocklist_rules,
        threshold_overrides=threshold_overrides,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print("Status: local detection done", file=sys.stderr)
    print(f"detectorVersion: {DETECTOR_VERSION}", file=sys.stderr)
    print(f"scoringMethod: {SCORING_METHOD}", file=sys.stderr)
    print(f"profile: {result['profile']}", file=sys.stderr)
    print(f"riskScore: {result['riskScore']}, riskLevel: {result['riskLevel']}", file=sys.stderr)
    print(f"items: {len(result['items'])}", file=sys.stderr)
    if args.explain:
        for item in result["items"]:
            print(
                (
                    f"item={item['id']} type={item['type']} source={item['detectionSource']} "
                    f"score={item['detectionScore']:.3f} threshold={item['scoreThreshold']:.3f}"
                ),
                file=sys.stderr,
            )
    print(result["sanitizedText"])


if __name__ == "__main__":
    main()
