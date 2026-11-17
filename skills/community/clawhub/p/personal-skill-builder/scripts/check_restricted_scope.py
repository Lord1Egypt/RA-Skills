#!/usr/bin/env python3
"""Check restricted fragments are gone from EVERY field of EVERY delivery view.

Standard library only. Uses a tested pattern pack (see redact_patterns.py).
Scans each declared output in full (all CSV columns, all text lines), checks
that declared ordinary content survived, and that no amount token from a source
fragment lingers as a bare leftover. Witness branches: a source column with no
restricted fragment is not_run, so a clean-looking sample cannot pass. Reports
output ids, columns and line numbers, never cell text. See references/tooling.md.

contract:
{"schema_version":1, "pattern":{"pack":"@patterns/cn-currency.json"},
 "source":{"path":"raw.csv","format":"csv","columns":["物品","备注"]},
 "outputs":[{"id":"list","path":"list.csv","format":"csv"},
            {"id":"reminder","path":"reminder.md","format":"text"}],
 "keep":[{"output":"list","text":"三元件"}],
 "allow_tokens":[]}
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from redact_patterns import find, load_pack  # noqa: E402

NUMBER = re.compile(r"\d[\d,，]*(?:\.\d+)?|[零〇一二两三四五六七八九十百千万亿]+")


class ScopeError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ScopeError(message)


def nonempty_text(value):
    return isinstance(value, str) and bool(value.strip())


def json_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON property")
        result[key] = value
    return result


def read_csv(path: Path):
    data = path.read_bytes()
    reader = csv.reader(io.StringIO(data.decode("utf-8-sig"), newline=""))
    header = next(reader, None)
    require(header and len(set(header)) == len(header), "unique CSV header required")
    rows, previous = [], reader.line_num
    for cells in reader:
        start, previous = previous + 1, reader.line_num
        if cells:
            require(len(cells) == len(header), "CSV row width mismatch")
            rows.append((start, dict(zip(header, cells))))
    return header, rows, data


def audit(contract, base):
    require(not isinstance(contract.get("schema_version"), bool) and contract.get("schema_version") == 1, "unsupported schema")
    require(set(contract) <= {"schema_version", "pattern", "source", "outputs", "keep", "allow_tokens"}, "unknown contract property")
    pattern = contract.get("pattern")
    require(isinstance(pattern, dict) and set(pattern) == {"pack"} and nonempty_text(pattern["pack"]), "pattern.pack required")
    pack = load_pack(pattern["pack"], base)
    source = contract.get("source")
    require(isinstance(source, dict) and set(source) == {"path", "format", "columns"} and source["format"] == "csv", "csv source required")
    witness_columns = source["columns"]
    require(isinstance(witness_columns, list) and witness_columns and all(nonempty_text(c) for c in witness_columns), "source columns required")
    header, src_rows, src_data = read_csv(base / source["path"])
    require(set(witness_columns) <= set(header), "source column absent")
    allow = contract.get("allow_tokens", [])
    require(isinstance(allow, list) and all(nonempty_text(t) for t in allow), "allow_tokens must be text list")

    tokens, witnesses = set(), {c: None for c in witness_columns}
    for line, row in src_rows:
        for column in header:
            for start, end in find(row[column], pack):
                for token in NUMBER.findall(row[column][start:end]):
                    if token not in allow:
                        tokens.add(token)
                if column in witnesses and witnesses[column] is None:
                    witnesses[column] = line

    outputs = contract.get("outputs")
    require(isinstance(outputs, list) and outputs, "outputs required")
    seen, scans, hashes = set(), {}, {}
    checks = []
    for out in outputs:
        require(isinstance(out, dict) and set(out) == {"id", "path", "format"}, "output needs id, path, format")
        require(nonempty_text(out["id"]) and out["id"] not in seen and out["format"] in {"csv", "text"}, "unique output id and csv/text format required")
        seen.add(out["id"])
        path = base / out["path"]
        require(path.resolve() != (base / source["path"]).resolve(), "source cannot double as output")
        hits, residual, text_all = [], [], []
        if out["format"] == "csv":
            out_header, out_rows, data = read_csv(path)
            for line, row in out_rows:
                for column in out_header:
                    cell = row[column]
                    text_all.append(cell)
                    if find(cell, pack):
                        hits.append(f"{line}:{column}")
                    elif any(re.search(rf"(?<![\d.]){re.escape(t)}(?![\d])", cell) for t in tokens if re.match(r"\d", t)) or \
                            any(t in cell for t in tokens if not re.match(r"\d", t) and len(t) > 1):
                        residual.append(f"{line}:{column}")
        else:
            data = path.read_bytes()
            for number, text_line in enumerate(data.decode("utf-8-sig").splitlines(), 1):
                text_all.append(text_line)
                if find(text_line, pack):
                    hits.append(f"{number}")
                elif any(re.search(rf"(?<![\d.]){re.escape(t)}(?![\d])", text_line) for t in tokens if re.match(r"\d", t)) or \
                        any(t in text_line for t in tokens if not re.match(r"\d", t) and len(t) > 1):
                    residual.append(f"{number}")
        scans[out["id"]] = "\n".join(text_all)
        hashes[out["id"]] = {"path": out["path"], "sha256": hashlib.sha256(data).hexdigest()}
        checks.append({"id": f"clean-{out['id']}", "passed": not hits, "positions": hits})
        checks.append({"id": f"no-residual-amount-{out['id']}", "passed": not residual, "positions": residual})

    keep = contract.get("keep", [])
    require(isinstance(keep, list), "keep must be a list")
    for index, item in enumerate(keep, 1):
        require(isinstance(item, dict) and set(item) == {"output", "text"} and item["output"] in scans and nonempty_text(item["text"]), "keep needs output id and text")
        checks.append({"id": f"keep-{index}", "passed": item["text"] in scans[item["output"]], "output": item["output"]})

    passed = all(c["passed"] for c in checks)
    branches = [{"id": f"source-fragment-in-{c}", "triggered": witnesses[c] is not None, "witness_source_line": witnesses[c],
                 "status": "not_run" if witnesses[c] is None else ("pass" if passed else "fail")} for c in witness_columns]
    status = "fail" if not passed else ("not_run" if any(not b["triggered"] for b in branches) else "pass")
    return {"schema_version": 1, "status": status, "pattern": pattern["pack"], "outputs": hashes,
            "source": {"path": source["path"], "sha256": hashlib.sha256(src_data).hexdigest()},
            "checks": checks, "branches": branches,
            "limits": "Checks the declared pattern pack against every column/line of every declared output, bare leftover amount tokens "
                      "from source fragments, declared kept content and source witnesses; not amounts the pack cannot recognize, "
                      "names or other free-text privacy, or whether the declared outputs are the whole delivery."}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("contract", type=Path)
    args = parser.parse_args()
    try:
        data = args.contract.read_bytes()
        contract = json.loads(data.decode("utf-8-sig"), object_pairs_hook=json_object,
                              parse_constant=lambda _: (_ for _ in ()).throw(ScopeError("non-finite JSON")))
        require(isinstance(contract, dict), "contract object required")
        result = audit(contract, args.contract.resolve().parent)
        result["contract"] = {"path": str(args.contract), "sha256": hashlib.sha256(data).hexdigest()}
    except ScopeError as exc:
        print(json.dumps({"schema_version": 1, "status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError, csv.Error, re.error):
        print(json.dumps({"schema_version": 1, "status": "error", "error": "Invalid contract or unreadable/unsupported artifact; no text echoed."},
                         ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
