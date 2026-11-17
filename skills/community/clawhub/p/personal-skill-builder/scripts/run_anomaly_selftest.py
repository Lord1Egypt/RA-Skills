#!/usr/bin/env python3
"""Run the shipped anomaly fixtures through the three checkers.

Proves each checker accepts the known-good delivery and still rejects every
known-bad one (the mutation rule in references/evaluation.md). Standard
library only; prints one JSON report and exits 0 only when every expectation
holds. Fixtures are synthetic; copy the pattern for a real task, not the data.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIX = ROOT / "assets" / "fixtures" / "anomaly"
SCRIPTS = ROOT / "scripts"
ENV = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}  # children never inherit a console codepage

# (checker, case file, expected exit code, expected failing check/clause ids or None)
EXPECT = [
    ("check_table_claims", "case-good.json", 0, set()),
    ("check_table_claims", "case-bad-negative.json", 1, {"actual-field-1", "actual-domain-1"}),
    ("check_table_claims", "case-bad-zero.json", 1, {"actual-field-1"}),
    ("check_table_claims", "case-bad-order.json", 1, {"actual-grouped-order"}),
    ("check_table_claims", "case-no-witness.json", 1, set()),  # not_run: no invalid row triggered the branch
    ("check_conflict_retention", "conflict-case-good.json", 0, set()),
    ("check_conflict_retention", "conflict-case-bad-line-base.json", 1,
     {"source-lines-true", "conflict-every-version-kept", "retained-quantity", "retained-note"}),
    ("check_conflict_retention", "conflict-case-bad-note.json", 1, {"retained-note"}),
    ("check_conflict_retention", "conflict-case-bad-qty.json", 1, {"retained-quantity"}),
    ("check_conflict_retention", "conflict-case-bad-version.json", 1, {"conflict-every-version-kept"}),
    ("check_conflict_retention", "conflict-case-bad-raw-negative.json", 1, {"retained-quantity"}),
    ("check_conflict_retention", "conflict-case-bad-entity.json", 1, {"conflict-entities-present"}),
    ("check_conflict_retention", "conflict-case-ml-good.json", 0, set()),
    ("check_requirement_trace", "trace-case-good.json", 0, set()),
    ("check_requirement_trace", "trace-case-weak.json", 1, {"R1", "R2", "R3"}),
    ("check_requirement_trace", "trace-case-missing.json", 1, {"R1", "R2", "R3"}),
    ("check_restricted_scope", "money-case-good.json", 0, set()),
]


def run(checker, case):
    done = subprocess.run([sys.executable, "-B", str(SCRIPTS / f"{checker}.py"), str(FIX / case)],
                          capture_output=True, text=True, encoding="utf-8", env=ENV)
    try:
        report = json.loads(done.stdout)
    except json.JSONDecodeError:
        report = {"status": "error"}
    failed = {c["id"] for c in report.get("checks", []) if not c.get("passed")}
    failed |= {c["id"] for c in report.get("clauses", []) if c.get("status") != "ok"}
    return done.returncode, report.get("status"), failed


def conflict_not_run():
    """Conflict present but no note and no invalid number: optional witnesses stay not_run."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "raw.csv").write_text("编号,数量,备注\nB01,3,\nB01,4,\n", encoding="utf-8")
        (tmp / "out.csv").write_text("id,source_line,quantity,note\nB01,2,3,\nB01,3,4,\n", encoding="utf-8")
        (tmp / "case.json").write_text(json.dumps({
            "schema_version": 1,
            "raw": {"path": "raw.csv", "format": "csv", "id_column": "编号", "line_base": "file",
                    "fields": {"quantity": {"column": "数量", "type": "number", "min": 0, "unknown": "未知"},
                               "note": {"column": "备注"}}},
            "actual": {"path": "out.csv", "format": "csv"}, "compare": ["quantity"], "retain": ["quantity", "note"]},
            ensure_ascii=False), encoding="utf-8")
        done = subprocess.run([sys.executable, "-B", str(SCRIPTS / "check_conflict_retention.py"), str(tmp / "case.json")],
                              capture_output=True, text=True, encoding="utf-8", env=ENV)
        return done.returncode, json.loads(done.stdout)["status"]


MATRICES = ["matrix-table.json", "matrix-conflict.json", "matrix-conflict-multiline.json", "matrix-trace.json", "matrix-restricted.json"]


def matrix_results():
    out = []
    for name in MATRICES:
        done = subprocess.run([sys.executable, "-B", str(SCRIPTS / "mutation_matrix.py"), str(FIX / name)],
                              capture_output=True, text=True, encoding="utf-8", env=ENV)
        try:
            report = json.loads(done.stdout)
        except json.JSONDecodeError:
            report = {"status": "error"}
        out.append({"matrix": name, "status": report.get("status"), "survivors": report.get("survivors"),
                    "required_classes_missing": report.get("required_classes_missing"),
                    "mutants": len(report.get("mutants", [])), "as_expected": done.returncode == 0})
    return out


def pattern_pack_result():
    done = subprocess.run([sys.executable, "-B", str(SCRIPTS / "redact_patterns.py"), "--pack", "@patterns/cn-currency.json", "--verify"],
                          capture_output=True, text=True, encoding="utf-8", env=ENV)
    report = json.loads(done.stdout) if done.stdout.strip().startswith("{") else {"status": "error"}
    return {"pack": "cn-currency", **{k: v for k, v in report.items() if k != "status"},
            "as_expected": done.returncode == 0 and report.get("status") == "pass"}


def undersized_matrix_rejected():
    """An author-shrunk matrix (one mutant, no profile coverage) must NOT pass."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for item in FIX.iterdir():
            if item.is_file():
                (tmp / item.name).write_bytes(item.read_bytes())
        matrix = json.loads((FIX / "matrix-table.json").read_text(encoding="utf-8"))
        matrix["mutants"] = matrix["mutants"][:1]
        (tmp / "small.json").write_text(json.dumps(matrix, ensure_ascii=False), encoding="utf-8")
        done = subprocess.run([sys.executable, "-B", str(SCRIPTS / "mutation_matrix.py"), str(tmp / "small.json")],
                              capture_output=True, text=True, encoding="utf-8", env=ENV)
        report = json.loads(done.stdout)
        return done.returncode == 1 and report["status"] == "fail" and bool(report["required_classes_missing"])


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    results, ok = [], True
    for checker, case, code, ids in EXPECT:
        got_code, status, failed = run(checker, case)
        good = got_code == code and (failed == ids if code else not failed)
        ok &= good
        results.append({"checker": checker, "case": case, "expected_exit": code, "exit": got_code,
                        "status": status, "failed_ids": sorted(failed), "as_expected": good})
    code, status = conflict_not_run()
    good = code == 1 and status == "not_run"
    ok &= good
    results.append({"checker": "check_conflict_retention", "case": "(generated) conflict without optional witnesses",
                    "expected_exit": 1, "exit": code, "status": status, "failed_ids": [], "as_expected": good})
    matrices = matrix_results()
    pack = pattern_pack_result()
    shrunk = undersized_matrix_rejected()
    ok &= all(m["as_expected"] for m in matrices) and pack["as_expected"] and shrunk
    print(json.dumps({"schema_version": 1, "status": "pass" if ok else "fail", "results": results,
                      "mutation_matrices": matrices, "pattern_pack": pack,
                      "undersized_matrix_rejected": shrunk}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
