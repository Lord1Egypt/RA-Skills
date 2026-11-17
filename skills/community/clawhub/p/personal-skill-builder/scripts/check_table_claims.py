#!/usr/bin/env python3
"""Check actual tabular delivery, grouping, and exercised sort branches.

Standard library only. Reads authored contracts and artifacts; never invokes a
model, edits data, certifies source truth, or checks semantic privacy. Reports
positions and check names, never cell values. See references/evaluation.md.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path


class ClaimError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ClaimError(message)


def typed(value, kind):
    if value is None or value == "":
        return None
    try:
        if kind == "number":
            require(not isinstance(value, bool), "boolean is not a number")
            result = Decimal(str(value))
            require(result.is_finite(), "non-finite number")
            return result
        if kind == "date":
            require(isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value), "date requires ISO day")
            return date.fromisoformat(value)
        require(kind == "text" and isinstance(value, str), "invalid typed field")
        return value
    except (InvalidOperation, ValueError, TypeError):
        raise ClaimError("invalid value for declared type") from None


def json_object(pairs):
    """Reject ambiguous rule/contract objects without echoing their values."""
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON property")
        result[key] = value
    return result


def read_definition(data):
    return json.loads(data.decode("utf-8-sig"), object_pairs_hook=json_object,
                      parse_constant=lambda _: (_ for _ in ()).throw(ClaimError("non-finite JSON")))


def nonempty_text(value):
    return isinstance(value, str) and bool(value.strip())


DOMAIN_KEYS = {"min", "max", "on_invalid"}


def validate_field_spec(spec):
    """check_fields entry: field/type, plus optional validity/domain.

    on_invalid="unknown" (optionally with min/max) means an unparseable or
    out-of-domain fact is an unknown value: the delivery must show unknown
    there, never the raw value, zero or a clamp. number and date supported.
    """
    require(isinstance(spec, dict) and {"field", "type"} <= set(spec) <= {"field", "type"} | DOMAIN_KEYS,
            "complete typed field specification required")
    require(nonempty_text(spec["field"]) and spec["type"] in {"number", "date", "text"}, "invalid typed field specification")
    if set(spec) & DOMAIN_KEYS:
        require(spec["type"] in {"number", "date"}, "domain applies to number and date fields only")
        require(spec.get("on_invalid") == "unknown", "domain requires on_invalid=unknown")
        for key in ("min", "max"):
            if key in spec:
                typed(spec[key], spec["type"])
                if spec["type"] == "number":
                    require(isinstance(spec[key], (int, float)) and not isinstance(spec[key], bool), "domain bounds must be numbers")
        if "min" in spec and "max" in spec:
            require(typed(spec["min"], spec["type"]) <= typed(spec["max"], spec["type"]), "domain min exceeds max")


def in_domain(value, spec):
    """value is typed (or None = already unknown); None is always in domain."""
    if value is None:
        return True
    if "min" in spec and value < typed(spec["min"], spec["type"]):
        return False
    if "max" in spec and value > typed(spec["max"], spec["type"]):
        return False
    return True


INVALID = object()


def safe_typed(value, kind):
    """typed() that maps an unparseable cell to INVALID instead of raising."""
    try:
        return typed(value, kind)
    except ClaimError:
        return INVALID


def fact_value(value, spec):
    """Fact cell as the delivery must show it: unparseable/out-of-domain -> None."""
    parsed = safe_typed(value, spec["type"])
    return None if parsed is INVALID or not in_domain(parsed, spec) else value


def instantiate_condition(rule, parameters, bindings, used):
    """Only condition operands are parameter slots; structure is never bound."""
    require(isinstance(rule, dict), "condition object required")
    if "all" in rule or "any" in rule:
        require(set(rule) in ({"all"}, {"any"}), "invalid compound condition")
        key = next(iter(rule))
        require(isinstance(rule[key], list) and rule[key], "empty compound condition")
        return {key: [instantiate_condition(item, parameters, bindings, used) for item in rule[key]]}
    require(nonempty_text(rule.get("field")), "condition field required")
    op = rule.get("op")
    require(op in {"lt", "le", "eq", "ne", "ge", "gt", "is_null"}, "invalid condition operator")
    if op == "is_null":
        require(set(rule) == {"field", "op"}, "is_null has no typed operand")
        return dict(rule)
    require(set(rule) == {"field", "op", "type", "value"}, "incomplete or unknown condition property")
    kind, value = rule["type"], rule["value"]
    require(kind in {"number", "date", "text"}, "invalid condition type")
    if isinstance(value, dict):
        require(set(value) == {"param"} and nonempty_text(value["param"]), "invalid parameter slot")
        name = value["param"]
        require(name in parameters, "undeclared parameter slot")
        require(parameters[name]["type"] == kind, "parameter slot type mismatch")
        value = bindings[name]["value"]
        used.add(name)
    typed(value, kind)
    return {**rule, "value": value}


def resolve_rules(contract, base, contract_path):
    """Resolve one independent, revision-bound rule profile before auditing.

    Binding certifies exact referenced bytes/revision, not that an authored
    revision is the latest or that its semantics match the user's request.
    """
    if "rules_ref" not in contract:
        require("bindings" not in contract, "bindings require a rules reference")
        return contract, {"status": "unbound", "reason": "inline rules have no current-rule binding"}
    require(set(contract) <= {"schema_version", "facts", "actual", "rules_ref", "bindings"},
            "referenced case cannot override or add rule properties")
    require(not isinstance(contract.get("schema_version"), bool) and contract.get("schema_version") == 1, "unsupported schema")
    ref = contract["rules_ref"]
    require(isinstance(ref, dict) and set(ref) == {"path", "profile", "revision"}, "complete rules reference required")
    require(all(nonempty_text(ref[key]) for key in ref), "rules reference requires nonempty text")
    rule_path = (base / ref["path"]).resolve()
    require(rule_path != contract_path.resolve(), "rules source must be independent of case contract")
    for key in ("facts", "actual"):
        spec = contract.get(key)
        require(isinstance(spec, dict) and nonempty_text(spec.get("path")), "artifact path required")
        allowed = {"path", "format", "columns", "null_values"} | ({"headings"} if key == "actual" else set())
        require(set(spec) <= allowed, "unknown artifact property in referenced case")
        require(rule_path != (base / spec["path"]).resolve(), "rules source must be independent of artifacts")
    data = rule_path.read_bytes()
    source = read_definition(data)
    require(isinstance(source, dict) and set(source) == {"schema_version", "revision", "source", "profiles"},
            "complete rules source required")
    require(not isinstance(source["schema_version"], bool) and source["schema_version"] == 1, "unsupported rules schema")
    require(nonempty_text(source["revision"]) and source["revision"] == ref["revision"], "rules revision mismatch")
    require(nonempty_text(source["source"]), "rules provenance reference required")
    require(isinstance(source["profiles"], dict) and ref["profile"] in source["profiles"], "rules profile absent")
    profile = source["profiles"][ref["profile"]]
    required = {"id_field", "group_field", "groups", "sort_keys", "check_fields"}
    require(isinstance(profile, dict) and required <= set(profile) <= required | {"parameters"},
            "incomplete or unknown rule profile property")
    require(nonempty_text(profile["id_field"]) and nonempty_text(profile["group_field"]) and
            profile["id_field"] != profile["group_field"], "distinct id and group fields required")
    for name, properties in (("sort_keys", {"field", "type", "direction", "unknowns"}),
                             ("check_fields", {"field", "type"})):
        specs = profile[name]
        require(isinstance(specs, list), "key and field arrays required")
        for spec in specs:
            if name == "check_fields":
                validate_field_spec(spec)
            else:
                require(isinstance(spec, dict) and set(spec) == properties, "complete typed field specification required")
                require(nonempty_text(spec["field"]) and spec["type"] in {"number", "date", "text"}, "invalid typed field specification")
            if name == "sort_keys":
                require(spec["direction"] in {"asc", "desc"}, "invalid sort direction")
                require(spec["unknowns"] == "last", "only unknowns-last ordering is supported")
        require(len({spec["field"] for spec in specs}) == len(specs), "duplicate rule field")
    parameters, bindings = profile.get("parameters", {}), contract.get("bindings", {})
    require(isinstance(parameters, dict) and isinstance(bindings, dict), "parameter and binding maps required")
    require(set(bindings) == set(parameters), "bindings must exactly match declared parameters")
    for name, spec in parameters.items():
        require(nonempty_text(name) and isinstance(spec, dict) and set(spec) == {"type"} and
                spec["type"] in {"number", "date", "text"}, "typed parameter declaration required")
        binding = bindings[name]
        require(isinstance(binding, dict) and set(binding) == {"value", "source"} and nonempty_text(binding["source"]),
                "parameter value and provenance reference required")
        value, kind = binding["value"], spec["type"]
        require(value is not None and value != "", "parameter cannot be unknown")
        require((kind == "number" and isinstance(value, (int, float)) and not isinstance(value, bool)) or
                (kind in {"date", "text"} and isinstance(value, str)), "parameter value has wrong JSON type")
        typed(value, kind)
    require(isinstance(profile["groups"], list) and profile["groups"], "groups required")
    groups, used = [], set()
    for group in profile["groups"]:
        require(isinstance(group, dict) and nonempty_text(group.get("name")), "named group required")
        if "when" in group:
            require(set(group) == {"name", "when"}, "conditional group cannot override other rules")
            groups.append({"name": group["name"], "when": instantiate_condition(group["when"], parameters, bindings, used)})
        else:
            require(set(group) == {"name", "default"} and group["default"] is True, "unique default or group condition required")
            groups.append(dict(group))
    require(used == set(parameters), "every declared parameter must occupy a condition value slot")
    resolved = {"schema_version": 1, **{key: profile[key] for key in required}, "groups": groups,
                "facts": contract["facts"], "actual": contract["actual"]}
    binding = {"status": "bound", "path": ref["path"], "profile": ref["profile"],
               "revision": source["revision"], "sha256": hashlib.sha256(data).hexdigest(),
               "source": source["source"],
               "parameter_sources": {name: value["source"] for name, value in bindings.items()}}
    return resolved, binding


def compare(a, b, spec):
    a, b = typed(a, spec["type"]), typed(b, spec["type"])
    # Unknown sorts last in either direction; this policy must match the task.
    if a is None or b is None:
        return (a is None) - (b is None)
    result = (a > b) - (a < b)
    return -result if spec.get("direction", "asc") == "desc" else result


def condition(row, rule):
    if "all" in rule or "any" in rule:
        require(set(rule) in ({"all"}, {"any"}), "invalid compound condition")
        key = next(iter(rule))
        require(isinstance(rule[key], list) and rule[key], "empty compound condition")
        values = [condition(row, item) for item in rule[key]]
        return all(values) if key == "all" else any(values)
    require(set(rule) <= {"field", "op", "type", "value"}, "unknown condition property")
    require(isinstance(rule.get("field"), str) and rule["field"] in row, "condition field absent")
    op = rule.get("op")
    require(op in {"lt", "le", "eq", "ne", "ge", "gt", "is_null"}, "invalid condition operator")
    if op == "is_null":
        return row[rule["field"]] in (None, "")
    require("value" in rule and rule.get("type") in {"number", "date", "text"}, "incomplete condition")
    a, b = typed(row[rule["field"]], rule["type"]), typed(rule["value"], rule["type"])
    if a is None or b is None:
        return False
    return {"lt": a < b, "le": a <= b, "eq": a == b,
            "ne": a != b, "ge": a >= b, "gt": a > b}[op]


def markdown_rows(text, spec, id_field, group_field):
    """Strict simple pipe tables; declared heading text supplies group labels."""
    headings = spec.get("headings", {})
    require(isinstance(headings, dict), "headings must be a map")
    columns = spec.get("columns", {})
    rows, header, group = [], None, None
    lines = text.splitlines()
    for line_number, line in enumerate(lines):
        stripped = line.strip()
        label = stripped.lstrip("#").strip()
        if label in headings:
            group, header = headings[label], None
            continue
        if stripped.startswith("#"):
            group, header = None, None
        if not (stripped.startswith("|") and stripped.endswith("|")):
            header = None
            continue
        require("\\|" not in stripped, "escaped pipes require CSV or JSON instead")
        cells = [cell.strip() for cell in stripped[1:-1].split("|")]
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        mapped = [columns.get(cell, cell) for cell in cells]
        next_line = lines[line_number + 1].strip() if line_number + 1 < len(lines) else ""
        next_cells = [cell.strip() for cell in next_line[1:-1].split("|")] if next_line.startswith("|") and next_line.endswith("|") else []
        is_header = next_cells and all(re.fullmatch(r":?-{3,}:?", cell) for cell in next_cells)
        if is_header:
            header = None
        if is_header and id_field in mapped:
            require(len(set(mapped)) == len(mapped), "duplicate table columns")
            header = mapped
            continue
        if header is None:
            continue
        require(len(cells) == len(header), "table width mismatch")
        row = dict(zip(header, cells))
        if group_field not in row and group is not None:
            row[group_field] = group
        rows.append(row)
    require(rows, "no matching actual table rows")
    return rows


def read_rows(base, spec, id_field, group_field, actual=False):
    require(isinstance(spec, dict) and isinstance(spec.get("path"), str), "artifact path required")
    path = (base / spec["path"]).resolve()
    data = path.read_bytes()
    text = data.decode("utf-8-sig")
    kind = spec.get("format", "json")
    if kind == "json":
        rows = json.loads(text, parse_constant=lambda _: (_ for _ in ()).throw(ClaimError("non-finite JSON")))
    elif kind == "csv":
        reader = csv.DictReader(io.StringIO(text))
        require(reader.fieldnames and len(reader.fieldnames) == len(set(reader.fieldnames)), "unique CSV columns required")
        rows = list(reader)
        require(all(None not in row and None not in row.values() for row in rows), "CSV row width mismatch")
    elif kind == "markdown" and actual:
        rows = markdown_rows(text, spec, id_field, group_field)
    else:
        raise ClaimError("unsupported artifact format")
    require(isinstance(rows, list) and rows and all(isinstance(row, dict) for row in rows), "nonempty row array required")
    columns = spec.get("columns", {})
    require(isinstance(columns, dict), "columns must be a map")
    if kind != "markdown":
        mapped_rows = []
        for row in rows:
            mapped = {columns.get(key, key): value for key, value in row.items()}
            require(len(mapped) == len(row), "column map collision")
            mapped_rows.append(mapped)
        rows = mapped_rows
    null_values = spec.get("null_values", {})
    require(isinstance(null_values, dict) and all(isinstance(values, list) for values in null_values.values()), "null_values requires per-field arrays")
    for row in rows:
        for field, tokens in null_values.items():
            if field in row and row[field] in tokens:
                row[field] = None
    return rows, {"path": spec["path"], "sha256": hashlib.sha256(data).hexdigest()}


def audit(contract, base):
    require(not isinstance(contract.get("schema_version"), bool) and contract.get("schema_version") == 1, "unsupported schema")
    id_field, group_field = contract.get("id_field"), contract.get("group_field")
    require(isinstance(id_field, str) and isinstance(group_field, str) and id_field != group_field, "distinct id and group fields required")
    groups, keys, fields = contract.get("groups"), contract.get("sort_keys"), contract.get("check_fields", [])
    require(isinstance(groups, list) and groups, "groups required")
    require(all(isinstance(group, dict) for group in groups), "group objects required")
    require(isinstance(keys, list) and isinstance(fields, list), "key and field arrays required")
    names = [group.get("name") for group in groups]
    require(all(isinstance(name, str) and name for name in names) and len(set(names)) == len(names), "unique group names required")
    defaults = [index for index, group in enumerate(groups) if group.get("default") is True]
    require(len(defaults) <= 1 and all(("when" in group) != (group.get("default") is True) for group in groups), "each group needs a condition or unique default")
    for spec in keys:
        require(isinstance(spec, dict) and isinstance(spec.get("field"), str) and spec.get("type") in {"number", "date", "text"}, "typed field specification required")
    for spec in fields:
        validate_field_spec(spec)
    require(len({key["field"] for key in keys}) == len(keys), "duplicate sort key")
    require(all(key.get("direction", "asc") in {"asc", "desc"} for key in keys), "invalid sort direction")
    facts, fact_source = read_rows(base, contract["facts"], id_field, group_field)
    actual, actual_source = read_rows(base, contract["actual"], id_field, group_field, True)
    require(fact_source["path"] != actual_source["path"] and (base / fact_source["path"]).resolve() != (base / actual_source["path"]).resolve(), "facts cannot double as actual output")
    ids = [row.get(id_field) for row in facts]
    require(all(isinstance(item, str) and item for item in ids) and len(set(ids)) == len(ids), "facts require unique nonempty text identities")
    for row in facts:
        for spec in keys + fields:
            require(spec["field"] in row, "fact field absent")
            if spec["field"] not in {f["field"] for f in fields if DOMAIN_KEYS & set(f)}:
                typed(row[spec["field"]], spec["type"])
    # Out-of-domain facts are unknown: grouping, ordering and field checks all
    # use the unknown value, so the raw invalid value can never be "expected".
    domains = {spec["field"]: spec for spec in fields if DOMAIN_KEYS & set(spec)}
    invalid_rows = {name: [i for i, row in enumerate(facts) if fact_value(row[name], spec) is None and row[name] not in (None, "")]
                    for name, spec in domains.items()}
    facts = [{**row, **{name: fact_value(row[name], spec) for name, spec in domains.items()}} for row in facts]
    group_indices = []
    for row in facts:
        matches = [index for index, group in enumerate(groups) if "when" in group and condition(row, group["when"])]
        require(len(matches) <= 1, "overlapping group conditions")
        require(matches or defaults, "unclassified fact row")
        group_indices.append((matches or defaults)[0])
    by_id = {identity: index for index, identity in enumerate(ids)}
    actual_ids = [row.get(id_field) for row in actual]
    identity_ok = all(isinstance(item, str) for item in actual_ids) and len(actual_ids) == len(ids) and len(set(actual_ids)) == len(actual_ids) and set(actual_ids) == set(ids)
    checks = [{"id": "actual-identities", "passed": identity_ok},
              {"id": "fact-classification-if-present", "passed": all(group_field not in row or row[group_field] == names[group_indices[index]] for index, row in enumerate(facts))}]
    if identity_ok:
        classification_ok = all(row.get(group_field) == names[group_indices[by_id[row[id_field]]]] for row in actual)
        checks.append({"id": "actual-classification", "passed": classification_ok})
        for position, spec in enumerate(fields):
            ok = all(spec["field"] in row and safe_typed(row[spec["field"]], spec["type"]) == safe_typed(facts[by_id[row[id_field]]][spec["field"]], spec["type"]) and safe_typed(row[spec["field"]], spec["type"]) is not INVALID for row in actual)
            checks.append({"id": f"actual-field-{position + 1}", "passed": ok})
            if spec["field"] in domains:
                dom_ok = all(safe_typed(row[spec["field"]], spec["type"]) is not INVALID and in_domain(safe_typed(row[spec["field"]], spec["type"]), spec) for row in actual)
                checks.append({"id": f"actual-domain-{position + 1}", "passed": dom_ok})
        def row_compare(left, right):
            result = (group_indices[left] > group_indices[right]) - (group_indices[left] < group_indices[right])
            for key in keys:
                if result:
                    break
                result = compare(facts[left][key["field"]], facts[right][key["field"]], key)
            return result
        actual_indices = [by_id[identity] for identity in actual_ids]
        order_ok = all(row_compare(a, b) <= 0 for a, b in zip(actual_indices, actual_indices[1:]))
        checks.append({"id": "actual-grouped-order", "passed": order_ok})
    branches = []
    def add_branch(name, witness, kind):
        branches.append({"id": name, "kind": kind, "triggered": witness is not None, "witness_positions": witness,
                         "status": "not_run" if witness is None else ("pass" if all(check["passed"] for check in checks) else "fail")})
    for position, spec in enumerate(fields):
        if spec["field"] in domains:
            rows_bad = invalid_rows[spec["field"]]
            add_branch(f"domain-unknown-{position + 1}", [rows_bad[0] + 1] if rows_bad else None, "domain")
    if len(groups) > 1:
        witness = next(([a + 1, b + 1] for a in range(len(facts)) for b in range(a + 1, len(facts)) if group_indices[a] > group_indices[b]), None)
        add_branch("group-order", witness, "group-order")
    for k, key in enumerate(keys):
        witness = None
        for a in range(len(facts)):
            for b in range(a + 1, len(facts)):
                same_prefix = group_indices[a] == group_indices[b] and all(compare(facts[a][prior["field"]], facts[b][prior["field"]], prior) == 0 for prior in keys[:k])
                # Null-placement is a separate boundary, not a witness for value direction.
                both_known = facts[a][key["field"]] not in (None, "") and facts[b][key["field"]] not in (None, "")
                if same_prefix and both_known and compare(facts[a][key["field"]], facts[b][key["field"]], key) > 0:
                    witness = [a + 1, b + 1]
                    break
            if witness:
                break
        add_branch(f"sort-key-{k + 1}", witness, "direction")
    for k in range(len(keys) - 1):
        primary, secondary = keys[k], keys[k + 1]
        witness = None
        for a in range(len(facts)):
            for b in range(a + 1, len(facts)):
                same_prefix = group_indices[a] == group_indices[b] and all(compare(facts[a][prior["field"]], facts[b][prior["field"]], prior) == 0 for prior in keys[:k])
                both_known = all(facts[row][key["field"]] not in (None, "") for row in (a, b) for key in (primary, secondary))
                if not same_prefix or not both_known:
                    continue
                primary_order = compare(facts[a][primary["field"]], facts[b][primary["field"]], primary)
                secondary_order = compare(facts[a][secondary["field"]], facts[b][secondary["field"]], secondary)
                # Opposing key orders distinguish precedence from correlated keys.
                # Actual delivery is still checked using the full ordered tuple above.
                if primary_order * secondary_order < 0:
                    witness = [a + 1, b + 1]
                    break
            if witness:
                break
        add_branch(f"sort-priority-{k + 1}-over-{k + 2}", witness, "priority")
    status = "fail" if not all(check["passed"] for check in checks) else ("not_run" if any(not branch["triggered"] for branch in branches) else "pass")
    return {"schema_version": 1, "status": status, "sources": {"facts": fact_source, "actual": actual_source},
            "checks": checks, "branches": branches,
            "limits": "Checks declared normalized facts, actual table, grouping, fields, out-of-domain-as-unknown witnesses, sort direction witnesses and adjacent-key priority witnesses; not fact provenance, arithmetic, prose, privacy semantics or model authenticity."}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", type=Path)
    args = parser.parse_args()
    try:
        data = args.contract.read_bytes()
        contract = read_definition(data)
        require(isinstance(contract, dict), "contract object required")
        base = args.contract.resolve().parent
        resolved, binding = resolve_rules(contract, base, args.contract)
        result = audit(resolved, base)
        result["sources"]["contract"] = {"path": str(args.contract), "sha256": hashlib.sha256(data).hexdigest()}
        result["rule_binding"] = binding
    except ClaimError as exc:
        result = {"schema_version": 1, "status": "error", "error": str(exc)}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError):
        result = {"schema_version": 1, "status": "error", "error": "Invalid contract or unreadable/unsupported artifact; no field values echoed."}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
