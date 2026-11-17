#!/usr/bin/env python3
"""
scan_risks.py — migration-risk-quick-scan (FREE edition).

Deterministic scanner for raw PostgreSQL SQL migration files only.
Detects the top-10 dangerous migration patterns and prints JSON.
Never connects to a database. Never modifies files.

The full edition (Prisma / Django / Alembic adapters, 20+ patterns,
expand-contract rewrites and rollback plans) is the paid
"Zero-Downtime DB Migration Auditor" skill on PromptBase.

Usage:
    python3 scan_risks.py --path <file-or-directory> [--out results.json]
"""

import argparse
import json
import re
import sys
from pathlib import Path

TOOL = "migration-risk-quick-scan"
VERSION = "1.0.0"

SEVERITY_ORDER = ["BLOCKER", "HIGH", "MEDIUM", "LOW"]


def line_of(text, idx):
    return text.count("\n", 0, idx) + 1


def snippet_of(text, idx):
    start = text.rfind("\n", 0, idx) + 1
    end = text.find("\n", idx)
    if end == -1:
        end = len(text)
    line = re.sub(r"\s+", " ", text[start:end]).strip()
    return line[:107] + "..." if len(line) > 110 else line



def strip_sql_comments(text):
    """Blank out -- line comments (positions preserved) so patterns only
    match executable SQL, never prose that mentions SQL."""
    out = []
    for line in text.split("\n"):
        stripped = line.lstrip()
        if stripped.startswith("--"):
            out.append(" " * len(line))
        else:
            idx = line.find(" --")
            if idx != -1 and line.count("'", 0, idx) % 2 == 0 and line.count('"', 0, idx) % 2 == 0:
                line = line[:idx] + " " * (len(line) - idx)
            out.append(line)
    return "\n".join(out)

def scan_sql_text(text):
    code = strip_sql_comments(text)
    findings = []

    def add(rule_id, severity, category, m, message, recommendation):
        findings.append({
            "rule_id": rule_id,
            "severity": severity,
            "category": category,
            "line": line_of(text, m.start()),
            "snippet": snippet_of(text, m.start()),
            "message": message,
            "recommendation": recommendation,
        })

    # Top-10 pattern set (PostgreSQL raw SQL):
    for m in re.finditer(r"\bDROP\s+TABLE\b", code, re.I):
        add("PG01-DROP-TABLE", "BLOCKER", "data-loss", m,
            "DROP TABLE destroys the table and all its data.",
            "Archive/export first; drop only in a separate later migration after usage is removed.")
    for m in re.finditer(r"\bDROP\s+COLUMN\b", code, re.I):
        add("PG02-DROP-COLUMN", "BLOCKER", "data-loss", m,
            "DROP COLUMN permanently deletes the column's data and breaks still-deployed code that reads it.",
            "Expand-contract: stop reading/writing the column in code first, drop it in a later migration.")
    for m in re.finditer(r"\bTRUNCATE\b", code, re.I):
        add("PG03-TRUNCATE", "BLOCKER", "data-loss", m,
            "TRUNCATE deletes every row in the table.",
            "Do full-table wipes as a reviewed operational step with a verified backup, not in a migration.")
    for m in re.finditer(r"\bDELETE\s+FROM\s+[\w.\"]+", code, re.I):
        seg_end = code.find(";", m.start())
        segment = code[m.start(): seg_end if seg_end != -1 else len(code)]
        if not re.search(r"\bWHERE\b", segment, re.I):
            add("PG04-DELETE-NO-WHERE", "BLOCKER", "data-loss", m,
                "DELETE without a WHERE clause removes every row in the table.",
                "Add a precise WHERE clause.")
    for m in re.finditer(r"\bUPDATE\s+[\w.\"]+\s+SET\b", code, re.I):
        seg_end = code.find(";", m.start())
        segment = code[m.start(): seg_end if seg_end != -1 else len(code)]
        if not re.search(r"\bWHERE\b", segment, re.I):
            add("PG05-UPDATE-NO-WHERE", "HIGH", "data-loss", m,
                "UPDATE without a WHERE clause rewrites every row in the table.",
                "Scope it (e.g. WHERE new_col IS NULL for backfills) so it is resumable and auditable.")
    for m in re.finditer(r"\bALTER\s+TABLE\s+[\w.\"]+\s+RENAME\s+TO\b|\bRENAME\s+TABLE\b", code, re.I):
        add("PG06-RENAME-TABLE", "HIGH", "downtime", m,
            "Renaming a table breaks deployed code, views and jobs that use the old name.",
            "Stage it: new table or compatibility view, migrate data, switch code, drop the old object later.")
    for m in re.finditer(r"\bRENAME\s+COLUMN\b", code, re.I):
        add("PG07-RENAME-COLUMN", "HIGH", "downtime", m,
            "Renaming a column breaks deployed code that still references the old name.",
            "Add the new column, backfill, dual-read, then drop the old column in a later migration.")
    for m in re.finditer(r"ADD\s+COLUMN\s+(?:IF\s+NOT\s+EXISTS\s+)?\"?\w+\"?\s+[^;]*?\bNOT\s+NULL\b", code, re.I | re.S):
        if not re.search(r"\bDEFAULT\b", m.group(0), re.I):
            add("PG08-NOT-NULL-NO-DEFAULT", "HIGH", "lock", m,
                "Adding a NOT NULL column without a DEFAULT fails on non-empty tables (and rewrites/locks on older engines).",
                "Add nullable (or constant DEFAULT on PG 11+), backfill in batches, then SET NOT NULL separately.")
    for m in re.finditer(r"ALTER\s+COLUMN\s+\"?\w+\"?\s+SET\s+NOT\s+NULL\b", code, re.I):
        add("PG08-NOT-NULL-NO-DEFAULT", "HIGH", "lock", m,
            "SET NOT NULL scans the whole table under an ACCESS EXCLUSIVE lock and fails if any NULL remains.",
            "Backfill NULLs first; on PG 12+ use a NOT VALID check constraint, validate it, then SET NOT NULL.")
    for m in re.finditer(r"CREATE\s+(?:UNIQUE\s+)?INDEX\s+(?!CONCURRENTLY\b)", code, re.I):
        add("PG09-CREATE-INDEX-NONCONCURRENT", "MEDIUM", "lock", m,
            "CREATE INDEX without CONCURRENTLY blocks writes to the table while it builds.",
            "Use CREATE INDEX CONCURRENTLY (outside a transaction) for production tables.")
    for m in re.finditer(r"ALTER\s+COLUMN\s+\"?\w+\"?\s+(?:SET\s+DATA\s+)?TYPE\s+(?:(?:VAR)?CHAR\s*\(\s*\d+\s*\)|SMALLINT|INT2\b)", code, re.I):
        add("PG10-TYPE-NARROW", "HIGH", "data-loss", m,
            "Changing a column to a bounded/smaller type can truncate or reject existing values (possible narrowing).",
            "Verify existing data first, or stage through a new column with explicit truncation rules.")
    return findings


def iter_sql_files(root):
    root = Path(root)
    if root.is_file():
        yield root
        return
    skip = {".git", "__pycache__", "node_modules", ".venv", "venv"}
    for p in sorted(root.rglob("*.sql")):
        if any(part in skip for part in p.parts):
            continue
        # Skip paired rollback files; their DROPs are expected (see full edition docs).
        if ".down." in p.name or p.name.startswith("down_") or p.name.endswith("_down.sql"):
            continue
        yield p


def main(argv=None):
    ap = argparse.ArgumentParser(description="Free PostgreSQL migration risk quick-scan (top-10 patterns).")
    ap.add_argument("--path", required=True, help="SQL file or directory to scan.")
    ap.add_argument("--out", default=None, help="Write JSON to this file instead of stdout.")
    args = ap.parse_args(argv)

    root = Path(args.path)
    if not root.exists():
        print("error: path does not exist: %s" % root, file=sys.stderr)
        return 2

    files_out = []
    totals = {s: 0 for s in SEVERITY_ORDER}
    total = 0
    for p in iter_sql_files(root):
        text = p.read_text(encoding="utf-8", errors="replace")
        findings = scan_sql_text(text)
        findings.sort(key=lambda f: (f["line"], f["rule_id"]))
        for f in findings:
            totals[f["severity"]] += 1
            total += 1
        files_out.append({"path": str(p), "framework": "raw-sql-postgresql", "findings": findings})

    verdict = "NO-GO" if totals["BLOCKER"] else ("NEEDS EXPAND-CONTRACT" if totals["HIGH"] else ("GO WITH FIXES" if total else "GO"))
    result = {
        "tool": TOOL,
        "version": VERSION,
        "dialect": "postgres",
        "files": files_out,
        "summary": {
            "files_scanned": len(files_out),
            "findings": total,
            "by_severity": totals,
            "verdict": verdict,
        },
    }
    payload = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.out:
        Path(args.out).write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
