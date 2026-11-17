#!/usr/bin/env python3
"""Deterministic processing layer for Office Collaboration Radar EN.

The module enforces evidence, PII redaction, cross-turn aggregation,
stable schema order, conflict detection, Markdown sanitization, action
priority, and executive-summary generation. It uses only the Python
standard library. CLI:
  python process.py selftest
  python process.py enforce --card card.json --source chat.txt --out safe-card.json
  python process.py aggregate --cards c1.json c2.json --out combined.json
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

# Keep CLI output stable on consoles whose default encoding is not UTF-8.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError, OSError):
    pass

EVIDENCE_MAX_LEN = 80


class RadarInputError(Exception):
    """Expected input error that the CLI can report without a traceback."""

# Canonical seven-module JSON order.
CANONICAL_KEYS = [
    "project_overview",
    "progress",
    "confirmed_decisions",
    "action_items",
    "risks_dependencies",
    "cross_department_relationships",
    "needs_human_confirmation",
]

# Preferred statement fields for evidence grounding and conflict detection.
STATEMENT_FIELDS = [
    "summary", "decision", "result", "task", "description",
    "collaboration_item", "item", "impact",
]

LABELS = {
    "phone_cn": "phone",
    "phone_fixed": "landline",
    "email": "email",
    "id_card": "government-id",
    "bank_card": "bank-card",
    "authorization": "authorization-header",
    "named_secret": "credential",
    "private_key": "private-key",
    "provider_token": "api-token",
    "jwt": "jwt",
    "name": "name",
}

# Common PII and credential patterns. This is a deterministic safety layer,
# not a substitute for a dedicated secret scanner.
PHONE_CN = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
PHONE_FIXED = re.compile(r"(?<!\d)(0\d{2,3}-?\d{7,8})(?!\d)")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
ID_CARD = re.compile(r"(?<!\d)(\d{17}[\dXx])(?!\d)")
BANK_CARD = re.compile(r"(?<!\d)(\d{16,19})(?!\d)")
AUTHORIZATION_HEADER = re.compile(r"(?im)\bauthorization\s*:\s*[^\r\n]+")
NAMED_SECRET = re.compile(
    r"(?i)\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|"
    r"password|passwd|pwd)\b\s*[:=]\s*(?:\"[^\"]+\"|'[^']+'|[^\s\"';,]+)"
)
PRIVATE_KEY = re.compile(
    r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----.*?-----END [A-Z0-9 ]*PRIVATE KEY-----",
    re.DOTALL,
)
PROVIDER_TOKEN = re.compile(
    r"(?<![A-Za-z0-9])(?:sk-[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9]{20,}|"
    r"github_pat_[A-Za-z0-9_]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|"
    r"AKIA[0-9A-Z]{16})(?![A-Za-z0-9])"
)
JWT = re.compile(r"(?<![A-Za-z0-9_-])eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}(?![A-Za-z0-9_-])")

def _luhn_ok(num: str) -> bool:
    """Return whether a numeric value passes the Luhn checksum."""
    digits = [int(c) for c in num if c.isdigit()]
    if len(digits) < 12:
        return False
    total, alt = 0, False
    for d in reversed(digits):
        if alt:
            d *= 2
            if d > 9:
                d -= 9
        total += d
        alt = not alt
    return total % 10 == 0


# Validators are optional; the card pattern uses Luhn to reduce false positives.
DESENSITIZE_RULES = [
    ("private_key", PRIVATE_KEY, None),
    ("authorization", AUTHORIZATION_HEADER, None),
    ("named_secret", NAMED_SECRET, None),
    ("provider_token", PROVIDER_TOKEN, None),
    ("jwt", JWT, None),
    ("phone_cn", PHONE_CN, None),
    ("phone_fixed", PHONE_FIXED, None),
    ("email", EMAIL, None),
    ("id_card", ID_CARD, None),
    ("bank_card", BANK_CARD, _luhn_ok),
]


# --------------------------------------------------------------------------
# Redaction
# --------------------------------------------------------------------------
def desensitize(text: str, extra_entities: Iterable[str] | None = None) -> tuple[str, list[dict]]:
    """Redact supported patterns and return the safe text plus a hit report."""
    if not text:
        return text, []
    report: list[dict] = []
    out = text
    for kind, pat, validator in DESENSITIZE_RULES:
        counter = {"n": 0}

        def _repl(m, k=kind, v=validator, c=counter):
            hit = m.group(0)
            if v is not None and not v(hit):
                return hit
            c["n"] += 1
            return f"[{LABELS[k]}]"

        out = pat.sub(_repl, out)
        if counter["n"]:
            report.append({"type": kind, "count": counter["n"]})
    for ent in (extra_entities or []):
        ent = (ent or "").strip()
        if ent and ent in out:
            count = out.count(ent)
            out = out.replace(ent, f"[{LABELS['name']}]")
            report.append({"type": "name", "count": count})
    return out, report


# --------------------------------------------------------------------------
# Evidence grounding
# --------------------------------------------------------------------------
def _split_sentences(source: str) -> list[str]:
    return [s.strip() for s in re.split(r"[.!?\n;]", source) if s.strip()]


# Similarity below this threshold is not treated as reliable evidence.
EVIDENCE_SIM_THRESHOLD = 0.34


def _char_bigrams(s: str) -> set[str]:
    """Return character bigrams after removing whitespace."""
    s = re.sub(r"\s+", "", s or "")
    if len(s) >= 2:
        return {s[i:i + 2] for i in range(len(s) - 1)}
    return {s} if s else set()


def _dice_similarity(a: str, b: str) -> float:
    """Return a character-bigram Dice similarity from zero to one."""
    A, B = _char_bigrams(a), _char_bigrams(b)
    if not A or not B:
        return 0.0
    return 2 * len(A & B) / (len(A) + len(B))


def attach_evidence(conclusion: str, source: str, max_len: int = EVIDENCE_MAX_LEN) -> str:
    """Find a source-grounded evidence snippet for a conclusion."""
    conclusion = (conclusion or "").strip()
    source = source or ""
    if not conclusion:
        return "Not provided"
    sentences = _split_sentences(source)
    best, best_score = None, 0.0
    for s in sentences:
        if len(s) > 120:
            continue
        # Exact containment is stronger than approximate similarity.
        if conclusion in s or (len(conclusion) >= 4 and s in conclusion):
            score = 1.0
        else:
            score = _dice_similarity(conclusion, s)
        if score > best_score:
            best, best_score = s, score
    if best and best_score >= EVIDENCE_SIM_THRESHOLD:
        best = best.lstrip("-*\t ").strip()
        snippet = best[:max_len]
        return snippet + ("…" if len(best) > max_len else "")
    return "Not provided"


def _statement_of(item: dict) -> str:
    for f in STATEMENT_FIELDS:
        if isinstance(item.get(f), str) and item[f].strip():
            return item[f]
    return ""


def _ground_action_fields(action_items: list[dict], source: str) -> list[dict]:
    """Reset draft owners and deadlines that lack verbatim source support."""
    resets: list[dict] = []
    for item in action_items:
        if not isinstance(item, dict):
            continue
        reset_fields: list[str] = []
        for field in ("owner", "ddl"):
            value = item.get(field)
            if not isinstance(value, str):
                continue
            normalized = value.strip()
            if not normalized or normalized == "Not provided":
                continue
            if normalized not in source:
                item[field] = "Not provided"
                reset_fields.append(field)
        if reset_fields:
            resets.append({
                "task": _statement_of(item) or "Not provided",
                "fields": reset_fields,
            })
    return resets


# --------------------------------------------------------------------------
# Conflict detection
# --------------------------------------------------------------------------
def detect_conflicts(items: list[dict]) -> list[dict]:
    """Return action topics with conflicting owners, deadlines, or statuses."""
    groups: dict[str, list[dict]] = {}
    for it in items:
        key = (_statement_of(it) or "").strip()
        if not key:
            continue
        groups.setdefault(key, []).append(it)
    conflicts: list[dict] = []
    for key, grp in groups.items():
        if len(grp) < 2:
            continue
        owners = {g.get("owner") for g in grp if g.get("owner")}
        ddls = {g.get("ddl") for g in grp if g.get("ddl")}
        statuses = {g.get("status") for g in grp if g.get("status")}
        if len(owners) > 1 or len(ddls) > 1 or len(statuses) > 1:
            conflicts.append({"topic": key, "variants": grp})
    return conflicts


# --------------------------------------------------------------------------
# Action priority
# --------------------------------------------------------------------------
def score_priority(item: dict) -> str:
    """Return P0 for conflicts, P1 for grounded fields, otherwise P2."""
    conflict = item.get("conflict")
    if isinstance(conflict, str) and conflict.strip() and conflict.strip() != "Not provided":
        return "P0"
    owner = (item.get("owner") or "").strip()
    ddl = (item.get("ddl") or "").strip()
    if owner and owner != "Not provided" and ddl and ddl != "Not provided":
        return "P1"
    return "P2"


# --------------------------------------------------------------------------
# Executive summary
# --------------------------------------------------------------------------
def synthesize(card: dict) -> str:
    """Create a two-to-three sentence executive summary."""
    proj = card.get("project_overview") or {}
    stage = proj.get("current_phase") or proj.get("stage") or ""
    if isinstance(stage, str) and stage and stage not in ("Not provided", ""):
        stage_text = str(stage)
    else:
        stage_text = "an unspecified phase"
    status = proj.get("overall_status") or "Not provided"
    if isinstance(status, str) and status not in ("Not provided", ""):
        status_text = str(status)
    else:
        status_text = "Not provided"

    actions = card.get("action_items") or []
    action_count = len(actions) if isinstance(actions, list) else 0
    p0_count = sum(1 for a in (actions if isinstance(actions, list) else [])
                   if isinstance(a, dict) and score_priority(a) == "P0")
    p1_count = sum(1 for a in (actions if isinstance(actions, list) else [])
                   if isinstance(a, dict) and score_priority(a) == "P1")

    risks = card.get("risks_dependencies") or []
    risk_count = len(risks) if isinstance(risks, list) else 0

    nhc = card.get("needs_human_confirmation") or []
    nhc_count = len(nhc) if isinstance(nhc, list) else 0

    lines: list[str] = []

    lines.append(f"Project phase: {stage_text}. Overall status: {status_text}.")

    parts: list[str] = []
    if action_count > 0:
        noun = "action" if action_count == 1 else "actions"
        p = f"{action_count} {noun}"
        if p0_count > 0:
            p += f", including {p0_count} P0"
        parts.append(p)
    if risk_count > 0:
        noun = "risk or blocker" if risk_count == 1 else "risks or blockers"
        parts.append(f"{risk_count} {noun}")
    if parts:
        lines.append("; ".join(parts) + ".")
    elif action_count == 0 and risk_count == 0:
        lines.append("No actions, risks, or blockers are recorded.")

    suggestions: list[str] = []
    if p0_count > 0:
        suggestions.append(f"review {p0_count} P0 action(s) immediately")
    if nhc_count > 0:
        top_item = ""
        if isinstance(nhc, list) and nhc and isinstance(nhc[0], dict):
            top_item = str(nhc[0].get("item", "")).strip()
        if top_item:
            suggestions.append(f"confirm '{top_item}' first")
    if suggestions:
        lines.append("Recommended action: " + "; ".join(suggestions) + ".")

    return " ".join(lines)


# --------------------------------------------------------------------------
# Markdown table injection safeguards
# --------------------------------------------------------------------------
def sanitize_markdown_cell(value: Any) -> str:
    """Escape a user-derived value before placing it in a Markdown table."""
    s = "" if value is None else str(value)
    s = s.replace("\n", " ").replace("\r", " ")
    s = s.replace("\\", "\\\\")
    s = s.replace("|", "\\|")
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    s = s.replace("[", "\\[")
    s = s.replace("]", "\\]")
    return s


def _sanitize_md_recursive(value: Any) -> Any:
    """Sanitize every string in a nested JSON-compatible value."""
    if isinstance(value, str):
        return sanitize_markdown_cell(value)
    if isinstance(value, list):
        return [_sanitize_md_recursive(v) for v in value]
    if isinstance(value, dict):
        return {k: _sanitize_md_recursive(v) for k, v in value.items()}
    return value


# --------------------------------------------------------------------------
# Stable schema validation
# --------------------------------------------------------------------------
def check_schema_stability(card: dict) -> list[str]:
    """Check that all seven modules exist in canonical order."""
    errors: list[str] = []
    if not isinstance(card, dict):
        return ["card must be a JSON object"]
    keys = list(card.keys())
    # Allow extra metadata keys while preserving the canonical order.
    canonical_present = [k for k in CANONICAL_KEYS if k in keys]
    if canonical_present != CANONICAL_KEYS:
        missing = [k for k in CANONICAL_KEYS if k not in keys]
        if missing:
            errors.append(f"missing modules: {missing}")
    positions = [keys.index(k) for k in CANONICAL_KEYS if k in keys]
    if positions != sorted(positions):
        errors.append("module order must match the seven-module schema")
    return errors


# --------------------------------------------------------------------------
# Recursive redaction
# --------------------------------------------------------------------------
def _desensitize_value(value: Any, extra: set[str]) -> tuple[Any, list[dict]]:
    report: list[dict] = []
    if isinstance(value, str):
        new, rep = desensitize(value, extra)
        return new, rep
    if isinstance(value, list):
        out = []
        for v in value:
            nv, rep = _desensitize_value(v, extra)
            out.append(nv)
            report.extend(rep)
        return out, report
    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            nk, _ = _desensitize_value(k, extra)
            nv, rep = _desensitize_value(v, extra)
            out[nk] = nv
            report.extend(rep)
        return out, report
    return value, report


def sanitize_and_desensitize(
    value: Any, extra_entities: Iterable[str] | None = None
) -> tuple[Any, list[dict]]:
    """Return a detached, Markdown-safe, redacted copy of user-derived data."""
    extra = set(extra_entities or [])
    sanitized = _sanitize_md_recursive(copy.deepcopy(value))
    return _desensitize_value(sanitized, extra)


# --------------------------------------------------------------------------
# Deterministic enforcement layer
# --------------------------------------------------------------------------
def enforce(card: dict, source: str, extra_entities: Iterable[str] | None = None) -> tuple[dict, dict]:
    """Apply deterministic safeguards to an extracted card."""
    if not isinstance(card, dict):
        raise RadarInputError(
            f"Card JSON must be an object with seven modules; got {type(card).__name__}."
        )
    extra = set(extra_entities or [])
    meta: dict = {
        "desensitized": [],
        "evidence_filled": 0,
        "evidence_missing": 0,
        "evidence_replaced": 0,
        "conflicts_found": 0,
        "schema_errors": [],
    }

    raw_action_items = card.get("action_items", []) or []
    grounded_resets = _ground_action_fields(raw_action_items, source)

    # Sanitize user-derived Markdown before redaction so generated PII
    # placeholders remain readable.
    card, drep = sanitize_and_desensitize(card, extra)
    safe_grounded_resets, reset_drep = sanitize_and_desensitize(grounded_resets, extra)
    safe_source, _ = desensitize(source, extra)
    meta["desensitized"] = drep + reset_drep
    meta["unsupported_action_fields_reset"] = safe_grounded_resets

    action_items = card.get("action_items", []) or []
    conflict_topics = detect_conflicts(action_items)
    conflict_task_keys = {c["topic"] for c in conflict_topics}
    meta["conflicts_found"] = len(conflict_topics)
    pending_nhc: list[dict] = [
        {
            "item": sanitize_markdown_cell(reset["task"]),
            "reason": "Draft owner or deadline lacked verbatim source support and was reset",
            "suggested_confirm_with": "Relevant stakeholder",
            "evidence": "Not provided",
        }
        for reset in safe_grounded_resets
    ]

    for key in CANONICAL_KEYS:
        section = card.get(key)
        if isinstance(section, list):
            for item in section:
                if not isinstance(item, dict):
                    continue
                stmt = _statement_of(item)
                draft_evidence = item.get("evidence")
                snippet = attach_evidence(stmt, safe_source)
                item["evidence"] = snippet
                if (
                    isinstance(draft_evidence, str)
                    and draft_evidence.strip()
                    and draft_evidence.strip() != "Not provided"
                    and draft_evidence.strip() != snippet
                ):
                    meta["evidence_replaced"] += 1
                if snippet == "Not provided":
                    meta["evidence_missing"] += 1
                else:
                    meta["evidence_filled"] += 1
                # Add one review marker for each conflicting action topic.
                if key == "action_items" and stmt and stmt in conflict_task_keys and "conflict" not in item:
                    item["conflict"] = "Conflict detected; human review required"
                    pending_nhc.append({
                        "item": stmt,
                        "reason": "The same action has conflicting owners, deadlines, or statuses",
                        "suggested_confirm_with": item.get("owner") or "Relevant stakeholder",
                        "evidence": "Conflict detected; human review required",
                    })
        elif isinstance(section, dict) and key == "project_overview":
            stmt = section.get("summary") or section.get("project_name") or ""
            draft_evidence = section.get("evidence")
            snippet = attach_evidence(stmt, safe_source)
            section["evidence"] = snippet
            if (
                isinstance(draft_evidence, str)
                and draft_evidence.strip()
                and draft_evidence.strip() != "Not provided"
                and draft_evidence.strip() != snippet
            ):
                meta["evidence_replaced"] += 1

    if pending_nhc:
        card.setdefault("needs_human_confirmation", []).extend(pending_nhc)

    # Order actions by P0, P1, then P2.
    action_items = card.get("action_items")
    if isinstance(action_items, list) and action_items:
        p0 = sum(1 for a in action_items if isinstance(a, dict) and score_priority(a) == "P0")
        p1 = sum(1 for a in action_items if isinstance(a, dict) and score_priority(a) == "P1")
        p2 = sum(1 for a in action_items if isinstance(a, dict) and score_priority(a) == "P2")
        meta["priority_summary"] = {"P0": p0, "P1": p1, "P2": p2}
        for item in action_items:
            if isinstance(item, dict) and "priority" not in item:
                item["priority"] = score_priority(item)
        action_items.sort(key=lambda a: {"P0": 0, "P1": 1, "P2": 2}.get(
            a.get("priority", "P2") if isinstance(a, dict) else "P2", 2))
    else:
        meta["priority_summary"] = {"P0": 0, "P1": 0, "P2": 0}

    # Executive summary.
    meta["executive_summary"] = synthesize(card)

    # Stable schema order.
    meta["schema_errors"] = check_schema_stability(card)
    return card, meta


# --------------------------------------------------------------------------
# Cross-turn aggregation
# --------------------------------------------------------------------------
def aggregate_cross_turn(
    cards: list[dict], extra_entities: Iterable[str] | None = None
) -> dict:
    """Merge redacted copies of source cards into one deduplicated card."""
    extra = set(extra_entities or [])
    safe_cards = [sanitize_and_desensitize(card, extra)[0] for card in cards]
    merged: dict = {k: [] for k in CANONICAL_KEYS}
    seen_action: set[tuple] = set()
    seen_text: dict[str, set] = {k: set() for k in CANONICAL_KEYS}

    for c in safe_cards:
        for k in CANONICAL_KEYS:
            section = c.get(k)
            if not isinstance(section, list):
                continue
            for item in section:
                if not isinstance(item, dict):
                    continue
                if k == "action_items":
                    sig = (_statement_of(item), item.get("owner"))
                    if sig in seen_action:
                        continue
                    seen_action.add(sig)
                    merged[k].append(item)
                else:
                    stmt = _statement_of(item)
                    if stmt and stmt in seen_text[k]:
                        continue
                    if stmt:
                        seen_text[k].add(stmt)
                    merged[k].append(item)

    merged["sources"] = [c.get("project_overview", {}).get("project_name", "Unnamed") for c in safe_cards]
    merged["aggregation_summary"] = (
        f"Aggregated {len(cards)} source cards into {len(merged['action_items'])} unique actions"
    )
    return merged


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def _read_text_file(path: Path, label: str) -> str:
    """Read UTF-8 text and convert expected failures to RadarInputError."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise RadarInputError(f"{label} file does not exist: {path}")
    except IsADirectoryError:
        raise RadarInputError(f"{label} path is a directory, not a file: {path}")
    except PermissionError:
        raise RadarInputError(f"{label} file is not readable: {path}")
    except UnicodeDecodeError:
        raise RadarInputError(f"{label} file is not valid UTF-8: {path}")
    except OSError as e:
        raise RadarInputError(f"Failed to read {label} file {path}: {e}")


def _load_json(path: Path, *, require_dict: bool = True) -> Any:
    """Load JSON and report malformed input without a traceback."""
    raw = _read_text_file(path, "JSON")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RadarInputError(
            f"Could not parse JSON {path} at line {e.lineno}, column {e.colno}: {e.msg}"
        )
    if require_dict and not isinstance(data, dict):
        raise RadarInputError(
            f"Top-level JSON must be an object, got {type(data).__name__}: {path}"
        )
    return data


def write_output_text(
    path: Path,
    text: str,
    *,
    protected_paths: Iterable[Path] = (),
    force: bool = False,
) -> None:
    """Write a named output without silently replacing input or existing files."""
    output_path = path.resolve(strict=False)
    protected = {item.resolve(strict=False) for item in protected_paths}
    if output_path in protected:
        raise RadarInputError(f"Output path must differ from every input path: {path}")
    if path.exists() and not force:
        raise RadarInputError(
            f"Output already exists: {path}. Choose another path or pass --force explicitly."
        )
    try:
        path.write_text(text, encoding="utf-8")
    except IsADirectoryError:
        raise RadarInputError(f"Output path is a directory, not a file: {path}")
    except FileNotFoundError:
        raise RadarInputError(f"Output directory does not exist: {path.parent}")
    except PermissionError:
        raise RadarInputError(f"Output path is not writable: {path}")
    except OSError as exc:
        raise RadarInputError(f"Failed to write output file {path}: {exc}")


def _selftest() -> int:
    print("== Office Collaboration Radar v0.1.5 core self-test ==")
    fails = 0

    # PII redaction.
    t, rep = desensitize("Contact 13800138000 or alice@corp.com; ID 11010119900101123X")
    ok = ("13800138000" not in t) and ("alice@corp.com" not in t) and ("[phone]" in t) and ("[email]" in t)
    print(("PASS" if ok else "FAIL"), "R2 PII redaction:", t)
    fails += 0 if ok else 1

    secret_text = (
        "api_key=REDACTED-SECRET Authorization: Bearer abcdefghijklmnop "
        "password=hunter2"
    )
    safe_secret_text, _ = desensitize(secret_text)
    ok = "sk-123" not in safe_secret_text and "Bearer" not in safe_secret_text and "hunter2" not in safe_secret_text
    print(("PASS" if ok else "FAIL"), "R2 credential redaction:", safe_secret_text)
    fails += 0 if ok else 1

    # Evidence grounding.
    ev = attach_evidence("Backend owns the API", "The Friday meeting confirmed Backend owns the API")
    ok = (0 < len(ev) <= EVIDENCE_MAX_LEN) and "Backend owns the API" in ev
    print(("PASS" if ok else "FAIL"), "R1 evidence grounding:", ev)
    fails += 0 if ok else 1

    ev_none = attach_evidence("Budget approval is overdue", "The weather is clear today")
    ok = ev_none == "Not provided"
    print(("PASS" if ok else "FAIL"), "R1 missing evidence:", ev_none)
    fails += 0 if ok else 1

    # Conflict detection.
    items = [
        {"task": "Implement sign-in", "owner": "Alex", "ddl": "2026-07-10"},
        {"task": "Implement sign-in", "owner": "Blair", "ddl": "2026-07-12"},
    ]
    cf = detect_conflicts(items)
    ok = len(cf) == 1 and cf[0]["topic"] == "Implement sign-in"
    print(("PASS" if ok else "FAIL"), "R5 conflict detection:", len(cf))
    fails += 0 if ok else 1

    # Schema order.
    bad = {"progress": [], "project_overview": {}}
    ok = len(check_schema_stability(bad)) > 0
    print(("PASS" if ok else "FAIL"), "R4 invalid order detected:", check_schema_stability(bad))
    fails += 0 if ok else 1

    # End-to-end enforcement.
    card = {
        "project_overview": {"project_name": "X", "summary": "Contact Morgan", "evidence": "Fabricated quote"},
        "progress": [{"item": "Design complete", "evidence": "Fabricated quote"}],
        "confirmed_decisions": [],
        "action_items": [
            {"task": "Implement sign-in", "owner": "Alex", "ddl": "2026-07-10"},
            {"task": "Implement sign-in", "owner": "Blair", "ddl": "2026-07-12"},
        ],
        "risks_dependencies": [],
        "cross_department_relationships": [],
        "needs_human_confirmation": [],
    }
    src = "Contact Morgan. Implement sign-in is assigned to Alex for 2026-07-10. A later note assigns it to Blair for 2026-07-12."
    out, meta = enforce(card, src, extra_entities=["Morgan"])
    ok = ("[name]" in json.dumps(out, ensure_ascii=False)) and meta["conflicts_found"] == 1 \
        and any(i.get("conflict") for i in out["action_items"]) and meta["evidence_replaced"] >= 1
    print(("PASS" if ok else "FAIL"), "End-to-end safeguards:", meta)
    fails += 0 if ok else 1

    # Cross-turn aggregation.
    c1 = {"project_overview": {"project_name": "A"}, "progress": [{"item": "p1"}], "confirmed_decisions": [],
         "action_items": [{"task": "t1", "owner": "Alex"}], "risks_dependencies": [],
         "cross_department_relationships": [], "needs_human_confirmation": []}
    c2 = {"project_overview": {"project_name": "B"}, "progress": [{"item": "p2"}], "confirmed_decisions": [],
         "action_items": [{"task": "t1", "owner": "Alex"}], "risks_dependencies": [],
         "cross_department_relationships": [], "needs_human_confirmation": []}
    merged = aggregate_cross_turn([c1, c2])
    ok = merged["aggregation_summary"] and len(merged["action_items"]) == 1 and len(merged["progress"]) == 2
    print(("PASS" if ok else "FAIL"), "R3 cross-turn aggregation:", merged["aggregation_summary"])
    fails += 0 if ok else 1

    raw_secret = "demo-secret"
    raw_entity = "Morgan Example"
    unsafe_card = {
        "project_overview": {"project_name": raw_entity},
        "progress": [], "confirmed_decisions": [],
        "action_items": [{"task": f"Email alice@example.com with password={raw_secret}"}],
        "risks_dependencies": [], "cross_department_relationships": [],
        "needs_human_confirmation": [],
    }
    safe_merged = aggregate_cross_turn([unsafe_card], extra_entities=[raw_entity])
    safe_merged_json = json.dumps(safe_merged, ensure_ascii=False)
    ok = all(value not in safe_merged_json for value in ("alice@example.com", raw_secret, raw_entity))
    print(("PASS" if ok else "FAIL"), "R3 aggregation reapplies redaction")
    fails += 0 if ok else 1

    # Luhn-valid card values are redacted; unrelated long numbers are retained.
    real_card = "6222021234567894"
    t_card, _ = desensitize(f"Card {real_card}")
    ok = "[bank-card]" in t_card
    print(("PASS" if ok else "FAIL"), "R2 card redaction:", t_card)
    fails += 0 if ok else 1

    ts = "1234567890123456"
    t_ts, _ = desensitize(f"Order {ts}")
    ok = ts in t_ts and "[bank-card]" not in t_ts
    print(("PASS" if ok else "FAIL"), "R2 non-card long number retained:", t_ts)
    fails += 0 if ok else 1

    ev_low = attach_evidence("Budget approval is overdue", "The team met for lunch")
    ok = ev_low == "Not provided"
    print(("PASS" if ok else "FAIL"), "R1 low-similarity rejection:", ev_low)
    fails += 0 if ok else 1

    # Malformed-input checks.
    import tempfile
    print("-" * 40)
    print("[Malformed input] Expected failures must raise RadarInputError:")
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        src = tdp / "s.txt"
        src.write_text("Source text", encoding="utf-8")

        # A1: malformed JSON.
        bad = tdp / "bad.json"
        bad.write_text("{broken,,,", encoding="utf-8")
        try:
            _load_json(bad)
            print("FAIL", "A1 malformed JSON was accepted"); fails += 1
        except RadarInputError:
            print("PASS", "A1 malformed JSON -> RadarInputError")
        except Exception as e:
            print("FAIL", f"A1 unexpected {type(e).__name__}"); fails += 1

        # A2: top-level array.
        arr = tdp / "arr.json"
        arr.write_text("[1,2,3]", encoding="utf-8")
        try:
            _load_json(arr)
            print("FAIL", "A2 array JSON was accepted"); fails += 1
        except RadarInputError:
            print("PASS", "A2 array JSON -> RadarInputError")
        except Exception as e:
            print("FAIL", f"A2 unexpected {type(e).__name__}"); fails += 1

        # A3: missing source file.
        try:
            _read_text_file(tdp / "NOPE.txt", "source text")
            print("FAIL", "A3 missing file was accepted"); fails += 1
        except RadarInputError:
            print("PASS", "A3 missing file -> RadarInputError")
        except Exception as e:
            print("FAIL", f"A3 unexpected {type(e).__name__}"); fails += 1

        # A4: non-object card.
        try:
            enforce([1, 2, 3], "Source text")
            print("FAIL", "A4 non-object card was accepted"); fails += 1
        except RadarInputError:
            print("PASS", "A4 non-object card -> RadarInputError")
        except Exception as e:
            print("FAIL", f"A4 unexpected {type(e).__name__}"); fails += 1

        output = tdp / "result.json"
        write_output_text(output, "first")
        try:
            write_output_text(output, "second")
            print("FAIL", "A5 existing output was silently replaced"); fails += 1
        except RadarInputError:
            print("PASS", "A5 existing output requires --force")

        try:
            write_output_text(src, "replacement", protected_paths=[src], force=True)
            print("FAIL", "A6 input path was overwritten"); fails += 1
        except RadarInputError:
            print("PASS", "A6 input path cannot be used as output")

    # Priority scoring.
    print("-" * 40)
    print("[v0.1.5] Priority scoring (P0/P1/P2):")
    ok = score_priority({"task": "Integration", "conflict": "Conflict detected; human review required", "owner": "Alex", "ddl": "Wednesday"}) == "P0"
    print(("PASS" if ok else "FAIL"), "P1 conflict -> P0")
    fails += 0 if ok else 1

    ok = score_priority({"task": "Write docs", "owner": "Blair", "ddl": "Friday"}) == "P1"
    print(("PASS" if ok else "FAIL"), "P2 grounded owner and deadline -> P1")
    fails += 0 if ok else 1

    ok = score_priority({"task": "Research", "owner": "Not provided", "ddl": "Not provided"}) == "P2"
    print(("PASS" if ok else "FAIL"), "P3 missing owner or deadline -> P2")
    fails += 0 if ok else 1

    # Enforcement includes priority ordering.
    mult_action = {
        "project_overview": {"project_name": "X", "summary": "Test"},
        "progress": [],
        "confirmed_decisions": [],
        "action_items": [
            {"task": "Write docs", "owner": "Blair", "ddl": "Friday", "evidence": "Not provided"},
            {"task": "Urgent fix", "owner": "Alex", "ddl": "Today", "evidence": "Not provided",
             "conflict": "Conflict detected; human review required"},
            {"task": "Research", "owner": "Not provided", "ddl": "Not provided", "evidence": "Not provided"},
        ],
        "risks_dependencies": [],
        "cross_department_relationships": [],
        "needs_human_confirmation": [],
    }
    out2, meta2 = enforce(
        mult_action,
        "Blair will write docs by Friday. Alex handles the urgent fix Today. Research has no owner or deadline.",
    )
    ais = out2.get("action_items", [])
    ok = len(ais) == 3 and ais[0].get("priority") == "P0" \
        and ais[1].get("priority") == "P1" and ais[2].get("priority") == "P2" \
        and meta2["priority_summary"] == {"P0": 1, "P1": 1, "P2": 1}
    print(("PASS" if ok else "FAIL"),
          f"P4 priority order: {meta2.get('priority_summary')}, first={ais[0].get('priority') if ais else 'N/A'}")
    fails += 0 if ok else 1

    unsupported_card = {
        "project_overview": {"project_name": "Vendor review"},
        "progress": [], "confirmed_decisions": [],
        "action_items": [
            {"task": "Prepare the review", "owner": "Alex", "ddl": "Friday", "evidence": "Not provided"},
        ],
        "risks_dependencies": [],
        "cross_department_relationships": [], "needs_human_confirmation": [],
    }
    grounded, grounded_meta = enforce(
        unsupported_card,
        "Prepare the review. The owner and deadline have not been assigned.",
    )
    grounded_item = grounded["action_items"][0]
    ok = (
        grounded_item.get("owner") == "Not provided"
        and grounded_item.get("ddl") == "Not provided"
        and grounded_item.get("priority") == "P2"
        and len(grounded_meta.get("unsupported_action_fields_reset", [])) == 1
    )
    print(("PASS" if ok else "FAIL"), "G1 unsupported owner/deadline reset")
    fails += 0 if ok else 1

    sensitive_card = {
        "project_overview": {"project_name": "X"},
        "progress": [], "confirmed_decisions": [],
        "action_items": [{
            "task": "Email alice@example.com with password=demo-secret",
            "owner": "Morgan Example", "ddl": "Friday", "evidence": "Not provided",
        }],
        "risks_dependencies": [], "cross_department_relationships": [],
        "needs_human_confirmation": [],
    }
    safe_card, safe_meta = enforce(
        sensitive_card,
        "Email alice@example.com with password=demo-secret. The owner and deadline are unassigned.",
        extra_entities=["Morgan Example"],
    )
    serialized = json.dumps({"card": safe_card, "meta": safe_meta}, ensure_ascii=False)
    ok = all(value not in serialized for value in (
        "alice@example.com", "demo-secret", "Morgan Example"
    ))
    print(("PASS" if ok else "FAIL"), "G2 enforcement diagnostics stay redacted")
    fails += 0 if ok else 1

    # Executive summary.
    summary = meta2.get("executive_summary", "")
    ok = isinstance(summary, str) and "Project phase:" in summary and "P0" in summary and "Overall status:" in summary
    print(("PASS" if ok else "FAIL"), f"S1 executive summary: {summary[:60]}...")
    fails += 0 if ok else 1

    # Empty-card summary.
    empty_card = {
        "project_overview": {"project_name": "X"},
        "progress": [], "confirmed_decisions": [],
        "action_items": [], "risks_dependencies": [],
        "cross_department_relationships": [], "needs_human_confirmation": [],
    }
    s_empty = synthesize(empty_card)
    ok = "Project phase:" in s_empty and "No actions" in s_empty
    print(("PASS" if ok else "FAIL"), f"S2 empty-card summary: {s_empty}")
    fails += 0 if ok else 1

    # Downstream exporter.
    print("-" * 40)
    print("[Exporter] Running export_card.selftest:")
    try:
        from export_card import selftest as _exp_selftest
        ok_exp = _exp_selftest() == 0
    except Exception as e:
        ok_exp = False
        print("FAIL", "E exporter self-test error:", type(e).__name__, e)
    print(("PASS" if ok_exp else "FAIL"), "E downstream exporter")
    fails += 0 if ok_exp else 1

    # Radar chart.
    print("-" * 40)
    print("[v0.1.5] Radar chart:")
    try:
        from radar_chart import _selftest as _radar_selftest  # type: ignore[import-untyped]
        ok_radar = _radar_selftest() == 0
    except Exception as e:
        ok_radar = False
        print("FAIL", "R radar self-test error:", type(e).__name__, e)
    print(("PASS" if ok_radar else "FAIL"), "R radar visualization")
    fails += 0 if ok_radar else 1

    # Markdown table injection safeguards.
    print("-" * 40)
    print("[v0.1.5] Markdown table safeguards:")
    # M1: pipe escaping.
    ok = sanitize_markdown_cell("a|b") == "a\\|b"
    print(("PASS" if ok else "FAIL"), "M1 pipe -> \\|")
    fails += 0 if ok else 1
    # M2: newline normalization.
    ok = sanitize_markdown_cell("line1\nline2") == "line1 line2"
    print(("PASS" if ok else "FAIL"), "M2 newline -> space")
    fails += 0 if ok else 1
    # M3: HTML entity escaping.
    ok = all(ch in sanitize_markdown_cell("<x>&y")
             for ch in ("&lt;", "&amp;", "&gt;"))
    print(("PASS" if ok else "FAIL"), "M3 <>& -> entities")
    fails += 0 if ok else 1
    # M4: Markdown link syntax neutralization.
    ok = sanitize_markdown_cell("[click](http://evil)") == "\\[click\\](http://evil)"
    print(("PASS" if ok else "FAIL"), "M4 [link] -> \\[link\\]")
    fails += 0 if ok else 1
    # M5: recursive enforcement.
    poison_card = {
        "project_overview": {"project_name": "X", "summary": "a|b", "evidence": "Not provided"},
        "progress": [{"item": "pro\ngress", "evidence": "<script>"}],
        "confirmed_decisions": [],
        "action_items": [{"task": "[link](x)", "owner": "Not provided", "ddl": "Not provided", "evidence": "Not provided"}],
        "risks_dependencies": [],
        "cross_department_relationships": [],
        "needs_human_confirmation": [],
    }
    out_md, meta_md = enforce(poison_card, "Source text")
    ok = (
        "a\\|b" in out_md["project_overview"]["summary"]
        and "pro gress" in out_md["progress"][0]["item"]
        and out_md["progress"][0]["evidence"] == "Not provided"
        and "\\[link\\](x)" in out_md["action_items"][0]["task"]
    )
    print(("PASS" if ok else "FAIL"), "M5 recursive enforcement")
    fails += 0 if ok else 1

    print("=" * 40)
    if fails == 0:
        print("ALL PASS -- v0.1.5 core safeguards, exporter, and radar")
        return 0
    print(f"{fails} checks failed")
    return 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Office Collaboration Radar EN processing layer")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_self = sub.add_parser("selftest")

    p_enf = sub.add_parser("enforce")
    p_enf.add_argument("--card", required=True, help="Draft card JSON path")
    p_enf.add_argument("--source", required=True, help="Source collaboration text path")
    p_enf.add_argument("--entities", help="Optional entity file, one value per line")
    p_enf.add_argument("--out", required=True, help="New output JSON path")
    p_enf.add_argument("--force", action="store_true", help="Replace the named output if it already exists")

    p_agg = sub.add_parser("aggregate")
    p_agg.add_argument("--cards", nargs="+", required=True, help="Card JSON files")
    p_agg.add_argument("--entities", help="Optional entity file, one value per line")
    p_agg.add_argument("--out", required=True, help="New output JSON path")
    p_agg.add_argument("--force", action="store_true", help="Replace the named output if it already exists")

    args = parser.parse_args(argv)

    if args.cmd == "selftest":
        return _selftest()

    if args.cmd == "enforce":
        card = _load_json(Path(args.card))
        source = _read_text_file(Path(args.source), "source text")
        extra = []
        if args.entities:
            extra = [l.strip() for l in _read_text_file(Path(args.entities), "entity list").splitlines() if l.strip()]
        out, meta = enforce(card, source, extra_entities=extra)
        out_path = Path(args.out)
        protected_paths = [Path(args.card), Path(args.source)]
        if args.entities:
            protected_paths.append(Path(args.entities))
        write_output_text(
            out_path,
            json.dumps(out, ensure_ascii=False, indent=2),
            protected_paths=protected_paths,
            force=args.force,
        )
        print(json.dumps(meta, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "aggregate":
        cards = []
        for p in args.cards:
            data = _load_json(Path(p), require_dict=False)
            if not isinstance(data, dict):
                raise RadarInputError(f"Aggregation input must be a card object: {p}")
            cards.append(data)
        if not cards:
            raise RadarInputError("No valid cards were provided for aggregation.")
        extra = []
        if args.entities:
            extra = [l.strip() for l in _read_text_file(Path(args.entities), "entity list").splitlines() if l.strip()]
        merged = aggregate_cross_turn(cards, extra_entities=extra)
        out_path = Path(args.out)
        protected_paths = [Path(item) for item in args.cards]
        if args.entities:
            protected_paths.append(Path(args.entities))
        write_output_text(
            out_path,
            json.dumps(merged, ensure_ascii=False, indent=2),
            protected_paths=protected_paths,
            force=args.force,
        )
        print(f"Aggregated {len(cards)} cards -> {out_path}")
        return 0

    return 1


def _cli_entry(argv: list[str]) -> int:
    """Report expected CLI failures without exposing a traceback."""
    try:
        return main(argv)
    except RadarInputError as e:
        print(f"[input error] {e}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("\n[interrupted]", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"[unexpected error] {type(e).__name__}: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(_cli_entry(sys.argv[1:]))
