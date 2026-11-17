#!/usr/bin/env python3
"""Export a collaboration card to safe CSV, Feishu mapping, or Notion mapping."""
from __future__ import annotations

import csv
import io
import json
import sys
from pathlib import Path
from typing import Any, Iterable

from process import RadarInputError, _load_json, sanitize_and_desensitize, write_output_text


# Spreadsheet applications can interpret =, +, -, or @ prefixes as formulas.
FORMULA_PREFIXES = ("=", "+", "-", "@")


def escape_csv_formula(value: Any) -> str:
    """Prefix formula-like CSV cells so spreadsheet apps treat them as text."""
    s = "" if value is None else str(value)
    if s[:1] in FORMULA_PREFIXES:
        return "'" + s
    return s


# Module key, downstream table name, and stable field order.
MODULE_TABLES = [
    ("project_overview", "Project Overview", ["project_name", "stage", "overall_status", "summary", "evidence"]),
    ("progress", "Progress", ["item", "evidence"]),
    ("confirmed_decisions", "Confirmed Decisions", ["decision", "result", "confirmed_by", "evidence"]),
    ("action_items", "Owner-Deadline Actions", ["task", "owner", "department", "ddl", "deliverable", "status", "evidence", "conflict"]),
    ("risks_dependencies", "Risks-Blockers-Dependencies", ["type", "description", "impact", "mitigation", "owner", "evidence"]),
    ("cross_department_relationships", "Cross-functional Relationships", ["from", "to", "collaboration_item", "status", "evidence"]),
    ("needs_human_confirmation", "Human Review Required", ["item", "reason", "suggested_confirm_with", "evidence"]),
]

# Ordered union of fields for the CSV header.
ALL_FIELDS: list[str] = []
for _k, _t, _f in MODULE_TABLES:
    for f in _f:
        if f not in ALL_FIELDS:
            ALL_FIELDS.append(f)


def _as_rows(items: Any) -> list[dict]:
    """Normalize a module value into a list of object rows."""
    if items is None:
        return []
    if isinstance(items, list):
        return [i for i in items if isinstance(i, dict)]
    if isinstance(items, dict):
        return [items]
    return []


def build_tables(card: dict) -> list[dict]:
    """Split a card into stable downstream table objects."""
    tables: list[dict] = []
    for key, table_name, fields in MODULE_TABLES:
        rows = _as_rows(card.get(key))
        tables.append({
            "name": table_name,
            "module": key,
            "fields": fields,
            "rows": [{f: (r.get(f, "") or "") for f in fields} for r in rows],
        })
    return tables


def export_card(
    card: dict, fmt: str, extra_entities: Iterable[str] | None = None
) -> str:
    """Return a card serialized as CSV, Feishu mapping, or Notion mapping."""
    if not isinstance(card, dict):
        raise RadarInputError(f"Card must be an object, got {type(card).__name__}.")

    safe_card, _ = sanitize_and_desensitize(card, extra_entities)
    tables = build_tables(safe_card)

    if fmt == "csv":
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(["module", "table"] + ALL_FIELDS)
        for key, table_name, _fields in MODULE_TABLES:
            for row in tables_dict(tables)[key]["rows"]:
                cells = [key, table_name] + [row.get(f, "") for f in ALL_FIELDS]
                w.writerow([escape_csv_formula(c) for c in cells])
        return buf.getvalue()

    if fmt in ("feishu", "notion"):
        payload = {
            "format": fmt,
            "tables": [
                {"name": t["name"], "fields": t["fields"], "rows": t["rows"]}
                for t in tables
            ],
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)

    raise RadarInputError(f"Unsupported format: {fmt}; choose csv, feishu, or notion")


def tables_dict(tables: list[dict]) -> dict[str, dict]:
    return {t["module"]: t for t in tables}


def _load_entities(path: str | None) -> list[str]:
    if not path:
        return []
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise RadarInputError(f"Could not read entity list: {path}") from exc
    return [line.strip() for line in text.splitlines() if line.strip()]


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def _cli_entry(argv: list[str]) -> int:
    import argparse

    parser = argparse.ArgumentParser(prog="export_card", description="Collaboration card exporter")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_exp = sub.add_parser("export-card", help="Export a card to csv/feishu/notion")
    p_exp.add_argument("--card", required=True, help="Card JSON path")
    p_exp.add_argument("--format", required=True, choices=["csv", "feishu", "notion"], help="Export format")
    p_exp.add_argument("--entities", help="Optional entity file, one value per line")
    p_exp.add_argument("--out", required=True, help="New output path")
    p_exp.add_argument("--force", action="store_true", help="Replace the named output if it already exists")

    sub.add_parser("selftest", help="Run exporter self-tests")

    args = parser.parse_args(argv)

    if args.cmd == "selftest":
        return selftest()

    if args.cmd == "export-card":
        try:
            card = _load_json(Path(args.card))
            extra = _load_entities(args.entities)
            text = export_card(card, args.format, extra_entities=extra)
            protected_paths = [Path(args.card)]
            if args.entities:
                protected_paths.append(Path(args.entities))
            write_output_text(
                Path(args.out),
                text,
                protected_paths=protected_paths,
                force=args.force,
            )
        except RadarInputError as e:
            print(f"[input error] {e}", file=sys.stderr)
            return 2
        except json.JSONDecodeError as e:
            print(f"[input error] Could not parse {args.card} at line {e.lineno}: {e.msg}", file=sys.stderr)
            return 2
        except FileNotFoundError:
            print(f"[input error] Card file does not exist: {args.card}", file=sys.stderr)
            return 2
        except Exception as e:
            print(f"[unexpected error] {type(e).__name__}: {e}", file=sys.stderr)
            return 1
        print(f"Exported {args.format} -> {args.out}")
        return 0

    return 1


def selftest() -> int:
    print("== Office Collaboration Radar v0.1.5 exporter self-test ==")
    fails = 0
    import tempfile
    from pathlib import Path as _P

    sample = {
        "project_overview": {"project_name": "X", "stage": "Design", "overall_status": "On track", "summary": "Backend owns the API", "evidence": "Confirmed Friday"},
        "progress": [{"item": "Design complete", "evidence": "Review approved"}],
        "confirmed_decisions": [{"decision": "Use option A", "result": "Approved", "confirmed_by": "Alex", "evidence": "Meeting notes"}],
        "action_items": [{"task": "Integration", "owner": "Blair", "department": "Backend", "ddl": "Wednesday", "deliverable": "API", "status": "In progress", "evidence": "Chat", "conflict": ""}],
        "risks_dependencies": [{"type": "Risk", "description": "External dependency", "impact": "Delay", "mitigation": "Fallback", "owner": "Casey", "evidence": "Review"}],
        "cross_department_relationships": [{"from": "Product", "to": "Engineering", "collaboration_item": "Requirement review", "status": "In progress", "evidence": "Meeting"}],
        "needs_human_confirmation": [{"item": "Budget", "reason": "Over plan", "suggested_confirm_with": "Director", "evidence": "Report"}],
    }

    # E1: CSV includes the header and a known value.
    csv_text = export_card(sample, "csv")
    ok = "owner" in csv_text and "Blair" in csv_text and "module" in csv_text
    print(("PASS" if ok else "FAIL"), "E1 CSV export")
    fails += 0 if ok else 1

    # E2: Feishu mapping contains seven tables.
    feishu = json.loads(export_card(sample, "feishu"))
    ok = len(feishu["tables"]) == 7 and feishu["tables"][3]["name"] == "Owner-Deadline Actions"
    print(("PASS" if ok else "FAIL"), "E2 Feishu mapping:", len(feishu["tables"]), "tables")
    fails += 0 if ok else 1

    # E3: Notion uses the same table structure.
    notion = json.loads(export_card(sample, "notion"))
    ok = len(notion["tables"]) == 7
    print(("PASS" if ok else "FAIL"), "E3 Notion mapping")
    fails += 0 if ok else 1

    # E4: Formula-like prefixes are neutralized.
    poison = {
        "action_items": [
            {
                "task": "=SUM(A1:A9)",
                "owner": "+8613800138000",
                "department": "-Unknown",
                "ddl": "@2026-07-20",
                "deliverable": "API",
                "status": "In progress",
                "evidence": "Chat",
                "conflict": "",
            },
        ],
    }
    csv_poison = export_card(poison, "csv")
    ok = (
        "'=SUM(A1:A9)" in csv_poison
        and "'+8613800138000" in csv_poison
        and "'-Unknown" in csv_poison
        and "'@2026-07-20" in csv_poison
    )
    print(("PASS" if ok else "FAIL"), "E4 CSV formula-prefix escaping")
    if not ok:
        lines = [ln for ln in csv_poison.splitlines() if "=SUM" in ln]
        print("   CSV row:", lines[0] if lines else csv_poison.replace("\n", " | "))
    fails += 0 if ok else 1

    # E5: every export format reapplies PII, credential, and entity redaction.
    sensitive = {
        "action_items": [{
            "task": "Email alice@example.com with password=demo-secret",
            "owner": "Morgan Example",
        }],
    }
    exports = [export_card(sensitive, fmt, ["Morgan Example"]) for fmt in ("csv", "feishu", "notion")]
    serialized_exports = "\n".join(exports)
    ok = all(value not in serialized_exports for value in (
        "alice@example.com", "demo-secret", "Morgan Example"
    ))
    print(("PASS" if ok else "FAIL"), "E5 all exports reapply redaction")
    fails += 0 if ok else 1

    # Malformed JSON.
    with tempfile.TemporaryDirectory() as td:
        bad = _P(td) / "bad.json"
        bad.write_text("{broken,,,", encoding="utf-8")
        try:
            _load_json(bad)
            print("FAIL", "A1 malformed JSON was accepted"); fails += 1
        except RadarInputError:
            print("PASS", "A1 malformed JSON -> RadarInputError")
        except Exception as e:
            print("FAIL", f"A1 unexpected {type(e).__name__}"); fails += 1

        # Missing file.
        try:
            _load_json(_P(td) / "nope.json")
            print("FAIL", "A2 missing file was accepted"); fails += 1
        except RadarInputError:
            print("PASS", "A2 missing file -> RadarInputError")
        except Exception as e:
            print("FAIL", f"A2 unexpected {type(e).__name__}"); fails += 1

        # Non-object card.
        try:
            export_card([1, 2, 3], "csv")
            print("FAIL", "A3 non-object card was accepted"); fails += 1
        except RadarInputError:
            print("PASS", "A3 non-object card -> RadarInputError")
        except Exception as e:
            print("FAIL", f"A3 unexpected {type(e).__name__}"); fails += 1

    print("=" * 40)
    if fails == 0:
        print("ALL PASS -- v0.1.5 exporter")
        return 0
    print(f"{fails} checks failed")
    return 1


if __name__ == "__main__":
    raise SystemExit(_cli_entry(sys.argv[1:]))
