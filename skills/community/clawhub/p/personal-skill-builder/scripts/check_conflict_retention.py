#!/usr/bin/env python3
"""Check that same-entity source conflicts are delivered with every version kept.

Standard library only. Reads a raw source file and the actual conflict section
of a delivery. For each entity whose raw rows differ on a compared field, every
distinct source version must appear with its true source line number, its
original value for each retained field (out-of-domain numbers shown as the
declared unknown token, never raw), and its ordinary note. Reports entity
line positions and check names, never cell values. See references/tooling.md.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import io
import json
import re
import sys
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path


class ConflictError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ConflictError(message)


def nonempty_text(value):
    return isinstance(value, str) and bool(value.strip())


def json_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON property")
        result[key] = value
    return result


def parse_number(text):
    try:
        value = Decimal(text.strip())
        return value if value.is_finite() else None
    except (InvalidOperation, AttributeError):
        return None


def parse_date(text):
    try:
        text = text.strip()
        return date.fromisoformat(text) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text) else None
    except (ValueError, AttributeError):
        return None


def field_specs(raw_spec):
    """name -> {column, type, min?, max?, unknown?}"""
    fields = raw_spec.get("fields")
    require(isinstance(fields, dict) and fields, "raw fields map required")
    result = {}
    for name, spec in fields.items():
        require(nonempty_text(name) and isinstance(spec, dict) and nonempty_text(spec.get("column")), "field column required")
        require(set(spec) <= {"column", "type", "min", "max", "unknown"}, "unknown field property")
        kind = spec.get("type", "text")
        require(kind in {"text", "number", "date"}, "field type must be text, number or date")
        if {"min", "max", "unknown"} & set(spec):
            require(kind in {"number", "date"} and nonempty_text(spec.get("unknown")), "validity needs number/date type and unknown token")
            for k in ("min", "max"):
                if k in spec:
                    if kind == "number":
                        require(isinstance(spec[k], (int, float)) and not isinstance(spec[k], bool), "domain bounds must be numbers")
                    else:
                        require(parse_date(spec[k]) is not None, "date bounds must be ISO days")
        result[name] = {**spec, "type": kind}
    return result


def expected_display(raw_value, spec):
    """What the delivery must show for a raw cell, per the declared domain."""
    text = raw_value.strip()
    if "unknown" in spec:
        if spec["type"] == "number":
            value, low, high = parse_number(text), (Decimal(str(spec["min"])) if "min" in spec else None), (Decimal(str(spec["max"])) if "max" in spec else None)
        else:
            value, low, high = parse_date(text), (parse_date(spec["min"]) if "min" in spec else None), (parse_date(spec["max"]) if "max" in spec else None)
        if text and (value is None or (low is not None and value < low) or (high is not None and value > high)):
            return spec["unknown"], True
    return text, False


def read_raw(base, raw_spec, specs):
    require(set(raw_spec) <= {"path", "format", "id_column", "line_base", "fields"}, "unknown raw property")
    require(raw_spec.get("format", "csv") == "csv", "raw source must be csv")
    require(nonempty_text(raw_spec.get("id_column")), "id column required")
    require(raw_spec.get("line_base") in {"file", "data"},
            "line_base must be declared: file (header is line 1) or data (first data row is 1)")
    data = (base / raw_spec["path"]).read_bytes()
    reader = csv.reader(io.StringIO(data.decode("utf-8-sig"), newline=""))
    header = next(reader, None)
    require(header and len(set(header)) == len(header), "unique raw header required")
    columns = {raw_spec["id_column"], *(spec["column"] for spec in specs.values())}
    require(columns <= set(header), "declared raw column absent")
    index = {name: header.index(name) for name in columns}
    rows, data_row = [], 0
    previous_line = reader.line_num
    for cells in reader:
        start, previous_line = previous_line + 1, reader.line_num
        if not cells:
            continue
        data_row += 1
        require(len(cells) == len(header), "raw row width mismatch")
        identity = cells[index[raw_spec["id_column"]]].strip()
        if not identity:
            continue
        line = start if raw_spec["line_base"] == "file" else data_row
        rows.append({"id": identity, "line": line,
                     "values": {name: cells[index[spec["column"]]] for name, spec in specs.items()}})
    return rows, {"path": raw_spec["path"], "sha256": hashlib.sha256(data).hexdigest()}


def load_markdown_reader():
    path = Path(__file__).with_name("check_table_claims.py")
    spec = importlib.util.spec_from_file_location("check_table_claims", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.markdown_rows


def read_actual(base, spec, id_field, line_field, fields):
    require(set(spec) <= {"path", "format", "columns", "headings", "id_field", "line_field", "fields"}, "unknown actual property")
    path = (base / spec["path"]).resolve()
    data = path.read_bytes()
    text = data.decode("utf-8-sig")
    kind = spec.get("format", "csv")
    if kind == "json":
        rows = json.loads(text, parse_constant=lambda _: (_ for _ in ()).throw(ConflictError("non-finite JSON")))
    elif kind == "csv":
        reader = csv.DictReader(io.StringIO(text, newline=""))
        require(reader.fieldnames and len(set(reader.fieldnames)) == len(reader.fieldnames), "unique CSV columns required")
        rows = list(reader)
    elif kind == "markdown":
        rows = load_markdown_reader()(text, spec, id_field, "__group__")
    else:
        raise ConflictError("unsupported actual format")
    require(isinstance(rows, list) and rows and all(isinstance(row, dict) for row in rows), "nonempty row array required")
    columns = spec.get("columns", {})
    require(isinstance(columns, dict), "columns must be a map")
    mapped = []
    for row in rows:
        row = {columns.get(key, key): value for key, value in row.items()}
        for needed in (id_field, line_field, *fields):
            require(needed in row, "actual field absent")
        mapped.append(row)
    return mapped, {"path": spec["path"], "sha256": hashlib.sha256(data).hexdigest()}


def audit(contract, base):
    require(not isinstance(contract.get("schema_version"), bool) and contract.get("schema_version") == 1, "unsupported schema")
    require(set(contract) <= {"schema_version", "raw", "actual", "compare", "retain"}, "unknown contract property")
    raw_spec, actual_spec = contract.get("raw"), contract.get("actual")
    require(isinstance(raw_spec, dict) and isinstance(actual_spec, dict), "raw and actual required")
    specs = field_specs(raw_spec)
    compare, retain = contract.get("compare"), contract.get("retain")
    require(isinstance(compare, list) and compare and set(compare) <= set(specs), "compare must name declared fields")
    require(isinstance(retain, list) and retain and set(retain) <= set(specs) and set(compare) <= set(retain),
            "retain must name declared fields and include every compared field")
    actual_fields = actual_spec.get("fields", {name: name for name in retain})
    require(isinstance(actual_fields, dict) and set(actual_fields) == set(retain), "actual fields must map every retained field")
    id_field, line_field = actual_spec.get("id_field", "id"), actual_spec.get("line_field", "source_line")
    require(nonempty_text(id_field) and nonempty_text(line_field) and id_field != line_field, "distinct id and line fields required")
    actual_spec = {**actual_spec, "columns": {**actual_spec.get("columns", {}),
                   **{column: name for name, column in actual_fields.items() if column != name}}}
    raw_rows, raw_source = read_raw(base, raw_spec, specs)
    actual_rows, actual_source = read_actual(base, actual_spec, id_field, line_field, retain)
    require(raw_source["path"] != actual_source["path"] and
            (base / raw_source["path"]).resolve() != (base / actual_source["path"]).resolve(), "raw source cannot double as actual output")

    by_id = {}
    for row in raw_rows:
        by_id.setdefault(row["id"], []).append(row)
    expected = {}  # id -> {version tuple -> {"lines": [...], "values": {...}, "invalid": bool}}
    for identity, rows in by_id.items():
        versions = {}
        for row in rows:
            shown = {name: expected_display(row["values"][name], specs[name]) for name in retain}
            key = tuple(row["values"][name].strip() for name in retain)
            entry = versions.setdefault(key, {"lines": [], "values": {n: shown[n][0] for n in retain},
                                              "invalid": any(shown[n][1] for n in retain)})
            entry["lines"].append(row["line"])
        raw_compare = {tuple(row["values"][name].strip() for name in compare) for row in rows}
        if len(raw_compare) > 1:
            expected[identity] = versions

    actual_by_id = {}
    for position, row in enumerate(actual_rows, 1):
        actual_by_id.setdefault(str(row[id_field]).strip(), []).append((position, row))

    missing_entities, missing_versions, bad_lines = [], [], []
    bad_values = {name: [] for name in retain}
    for identity, versions in expected.items():
        rows = actual_by_id.get(identity, [])
        first_line = min(min(v["lines"]) for v in versions.values())
        if not rows:
            missing_entities.append(first_line)
            continue
        used = set()
        for position, row in rows:
            try:
                line = int(str(row[line_field]).strip())
            except ValueError:
                line = None
            owners = [key for key, v in versions.items() if line in v["lines"]]
            if not owners:
                bad_lines.append(position)
                continue
            key = owners[0]
            used.add(key)
            for name in retain:
                if str(row[actual_fields[name]] if actual_fields[name] in row else row[name]).strip() != versions[key]["values"][name]:
                    bad_values[name].append(position)
        for key, v in versions.items():
            if key not in used:
                missing_versions.append(min(v["lines"]))
    extra = [position for identity, rows in actual_by_id.items() if identity not in expected for position, _ in rows]

    checks = [{"id": "conflict-entities-present", "passed": not missing_entities, "raw_lines": sorted(missing_entities)},
              {"id": "conflict-every-version-kept", "passed": not missing_versions, "raw_lines": sorted(missing_versions)},
              {"id": "source-lines-true", "passed": not bad_lines, "actual_positions": sorted(bad_lines)}]
    checks += [{"id": f"retained-{name}", "passed": not bad_values[name], "actual_positions": sorted(set(bad_values[name]))}
               for name in retain]
    checks.append({"id": "no-non-conflict-entities", "passed": not extra, "actual_positions": sorted(extra)})

    def branch(name, witness_lines):
        passed = all(check["passed"] for check in checks)
        return {"id": name, "triggered": bool(witness_lines), "witness_raw_lines": witness_lines or None,
                "status": "not_run" if not witness_lines else ("pass" if passed else "fail")}

    versions_all = [v for versions in expected.values() for v in versions.values()]
    branches = [branch("conflict-entity", [min(min(v["lines"]) for v in vs.values()) for vs in expected.values()][:1])]
    for name in retain:
        if name in compare:
            continue
        witnesses = [v["lines"][0] for v in versions_all if v["values"][name]]
        branches.append(branch(f"retain-{name}-nonempty", witnesses[:1]))
    if any("unknown" in spec for spec in specs.values()):
        branches.append(branch("conflict-invalid-shown-as-unknown", [v["lines"][0] for v in versions_all if v["invalid"]][:1]))
    status = "fail" if not all(check["passed"] for check in checks) else (
        "not_run" if any(not b["triggered"] for b in branches) else "pass")
    return {"schema_version": 1, "status": status, "sources": {"raw": raw_source, "actual": actual_source},
            "conflict_entities": len(expected), "checks": checks, "branches": branches,
            "limits": "Checks that each distinct raw version of a conflicting entity is delivered with its true source line, "
                      "displayed retained fields and unknown-for-invalid; not which conflicts are authoritative, "
                      "free-text privacy, arithmetic or model authenticity."}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", type=Path)
    args = parser.parse_args()
    try:
        data = args.contract.read_bytes()
        contract = json.loads(data.decode("utf-8-sig"), object_pairs_hook=json_object,
                              parse_constant=lambda _: (_ for _ in ()).throw(ConflictError("non-finite JSON")))
        require(isinstance(contract, dict), "contract object required")
        result = audit(contract, args.contract.resolve().parent)
        result["sources"]["contract"] = {"path": str(args.contract), "sha256": hashlib.sha256(data).hexdigest()}
    except ConflictError as exc:
        print(json.dumps({"schema_version": 1, "status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError, csv.Error):
        print(json.dumps({"schema_version": 1, "status": "error",
                          "error": "Invalid contract or unreadable/unsupported artifact; no field values echoed."},
                         ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
