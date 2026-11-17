#!/usr/bin/env python3
"""Prove a checker rejects a declared matrix of known-bad deliveries.

Standard library only. Copies the directory of a passing contract per mutant,
applies declared edits to one artifact, runs the checker, and requires the
unmutated baseline to pass and every mutant to be rejected (exit 1). Mutants
carry a `class`; `required_classes` must each be covered by a rejected mutant,
so a self-check cannot pass with only one or two kinds of rejection. Reports
mutant ids/classes and failing check ids, never cell values.

Required classes come from canonical profiles in assets/mutation-profiles.json,
declared as "profiles":[...]; the author cannot shrink them. A class that truly
does not apply is excluded only via "not_applicable":{"class":"reason"}, which the
report echoes for human review. Extra "required_classes" may add, never remove.

matrix.json:
{"schema_version":1, "checker":"check_table_claims.py", "contract":"case-good.json",
 "profiles":["table-delivery"], "not_applicable":{"group-wrong":"no grouping in this task"},
 "mutants":[{"id":"m1","class":"unknown-shown-as-raw","file":"actual-good.csv",
   "ops":[{"op":"set","where":{"id":"A02"},"column":"quantity","value":"-3"}]}]}

ops on .csv files: set{where,column,value} | shift_int{where,column,delta} |
delete_row{where} | swap_rows{a,b}; on any file: replace_text{find,replace}.
`where` matches every listed column exactly and must match at least one row.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
PROFILES = SCRIPTS.parent / "assets" / "mutation-profiles.json"
CHILD_ENV = {**__import__("os").environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}


class MatrixError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise MatrixError(message)


def find(rows, where):
    require(isinstance(where, dict) and where, "where required")
    hits = [r for r in rows if all(r.get(k) == v for k, v in where.items())]
    require(hits, "where matched no row")
    return hits


def apply_ops(path: Path, ops):
    require(isinstance(ops, list) and ops, "ops required")
    csv_file = path.suffix.lower() == ".csv"
    if csv_file:
        reader = csv.DictReader(io.StringIO(path.read_text(encoding="utf-8-sig"), newline=""))
        header, rows = reader.fieldnames, list(reader)
    else:
        text = path.read_text(encoding="utf-8")
    for op in ops:
        kind = op.get("op")
        if kind == "replace_text":
            require(not csv_file or True, "")
            if csv_file:
                buffer = io.StringIO(); w = csv.writer(buffer, lineterminator="\n"); w.writerow(header)
                for r in rows: w.writerow([r[h] for h in header])
                text = buffer.getvalue()
            require(op.get("find") and op["find"] in text, "find text absent")
            text = text.replace(op["find"], op.get("replace", ""))
            if csv_file:
                reader = csv.DictReader(io.StringIO(text, newline="")); header, rows = reader.fieldnames, list(reader)
            continue
        require(csv_file, "row ops need a .csv file")
        if kind == "set":
            require(op.get("column") in header, "column absent")
            for r in find(rows, op["where"]): r[op["column"]] = str(op["value"])
        elif kind == "shift_int":
            require(op.get("column") in header and isinstance(op.get("delta"), int), "column and integer delta required")
            for r in find(rows, op["where"]): r[op["column"]] = str(int(r[op["column"]]) + op["delta"])
        elif kind == "delete_row":
            doomed = find(rows, op["where"]); rows = [r for r in rows if not any(r is d for d in doomed)]
        elif kind == "swap_rows":
            a, b = find(rows, op["a"])[0], find(rows, op["b"])[0]
            ia, ib = next(i for i, r in enumerate(rows) if r is a), next(i for i, r in enumerate(rows) if r is b)
            rows[ia], rows[ib] = rows[ib], rows[ia]
        else:
            raise MatrixError("unknown op")
    if csv_file:
        buffer = io.StringIO(); w = csv.writer(buffer, lineterminator="\n"); w.writerow(header)
        for r in rows: w.writerow([r[h] for h in header])
        path.write_text(buffer.getvalue(), encoding="utf-8", newline="")
    else:
        path.write_text(text, encoding="utf-8", newline="")


def run_checker(checker: Path, contract: Path):
    done = subprocess.run([sys.executable, "-B", str(checker), str(contract)], capture_output=True, text=True, encoding="utf-8", env=CHILD_ENV)
    try:
        report = json.loads(done.stdout)
    except json.JSONDecodeError:
        report = {"status": "error"}
    failed = sorted({c["id"] for c in report.get("checks", []) if not c.get("passed")} |
                    {c["id"] for c in report.get("clauses", []) if c.get("status") != "ok"})
    return done.returncode, report.get("status"), failed


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("matrix", type=Path)
    args = parser.parse_args()
    try:
        base = args.matrix.resolve().parent
        matrix = json.loads(args.matrix.read_text(encoding="utf-8-sig"))
        require(matrix.get("schema_version") == 1 and isinstance(matrix.get("mutants"), list) and matrix["mutants"], "matrix needs mutants")
        checker = Path(matrix["checker"]); checker = checker if checker.is_absolute() else SCRIPTS / checker
        require(checker.is_file(), "checker absent")
        contract = base / matrix["contract"]
        require(contract.is_file(), "contract absent")
        catalog = json.loads(PROFILES.read_text(encoding="utf-8"))["profiles"]
        profiles = matrix.get("profiles")
        require(isinstance(profiles, list) and profiles and all(p in catalog for p in profiles),
                "profiles must name canonical profiles (assets/mutation-profiles.json)")
        profile_classes = sorted({c for p in profiles for c in catalog[p]})
        na = matrix.get("not_applicable", {})
        require(isinstance(na, dict) and all(k in profile_classes and isinstance(v, str) and len(v.strip()) >= 8 for k, v in na.items()),
                "not_applicable needs profile classes with a written reason")
        extra = matrix.get("required_classes", [])
        require(isinstance(extra, list) and all(isinstance(x, str) and x for x in extra), "required_classes must be text list")
        required = sorted((set(profile_classes) - set(na)) | set(extra))
        ids = [m.get("id") for m in matrix["mutants"]]
        require(all(isinstance(i, str) and i for i in ids) and len(set(ids)) == len(ids), "unique mutant ids required")
        results, covered = [], set()
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / "case"
            shutil.copytree(base, work, ignore=shutil.ignore_patterns("__pycache__"))
            code, status, _ = run_checker(checker, work / matrix["contract"])
            baseline = {"exit": code, "status": status, "passed": code == 0}
            for mutant in matrix["mutants"]:
                require(isinstance(mutant.get("class"), str) and mutant["class"], "mutant class required")
                run = Path(tmp) / f"m-{mutant['id']}"
                shutil.copytree(base, run, ignore=shutil.ignore_patterns("__pycache__"))
                target = (run / mutant["file"]).resolve()
                require(run.resolve() in target.parents, "mutant file outside case directory")
                apply_ops(target, mutant["ops"])
                code, status, failed = run_checker(checker, run / matrix["contract"])
                rejected = code == 1
                if rejected: covered.add(mutant["class"])
                results.append({"id": mutant["id"], "class": mutant["class"], "exit": code, "status": status,
                                "rejected": rejected, "failed_ids": failed})
        missing = sorted(set(required) - covered)
        survivors = [r["id"] for r in results if not r["rejected"]]
        ok = baseline["passed"] and not survivors and not missing
        print(json.dumps({"schema_version": 1, "status": "pass" if ok else "fail", "baseline": baseline,
                          "classes_rejected": sorted(covered), "required_classes_missing": missing,
                          "survivors": survivors, "profiles": profiles, "not_applicable": na, "mutants": results,
                          "limits": "Shows the checker rejects the declared mutants; says nothing about unlisted defects "
                                    "or whether the contract itself encodes the right rule."}, ensure_ascii=False, indent=2))
        return 0 if ok else 1
    except (MatrixError, KeyError, TypeError, OSError, UnicodeError, json.JSONDecodeError, csv.Error, ValueError) as exc:
        print(json.dumps({"schema_version": 1, "status": "error", "error": str(exc) if isinstance(exc, MatrixError) else "invalid matrix or artifact"},
                         ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
