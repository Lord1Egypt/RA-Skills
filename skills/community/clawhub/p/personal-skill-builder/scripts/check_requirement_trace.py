#!/usr/bin/env python3
"""Check that hard requirements survive into a generated skill without weakening.

Standard library only. A contract lists atomic clauses taken from the upper
requirement (id, strength, anchor phrases) and the files an executor must read
before acting. A clause is ok only if one window of lines in those files holds
all its anchors, carries a strength marker, contains no weakening word, names
every `scope` term (fields/views the rule must cover) and no `narrowing` phrase
(e.g. a rule shrunk to one column). Statuses: ok, missing, weakened, narrowed.
Reports clause ids, files and line numbers, never clause text. Lexical only:
it cannot judge meaning; a human still reads each located line.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

STRONG = ("必须", "不得", "不能", "不可", "禁止", "严禁", "只有", "仅当", "仅在", "一律", "务必", "始终", "永不",
          "must", "never", "only", "always", "shall not")
WEAK = ("建议", "尽量", "可以", "可考虑", "一般", "通常", "酌情", "视情况", "最好", "优先", "原则上", "倾向",
        "should", "may ", "might", "try to", "ideally", "usually", "generally")
STRENGTHS = {"must", "never", "only", "default"}


class TraceError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise TraceError(message)


def nonempty_text(value):
    return isinstance(value, str) and bool(value.strip())


def json_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON property")
        result[key] = value
    return result


def audit(contract, base):
    require(not isinstance(contract.get("schema_version"), bool) and contract.get("schema_version") == 1, "unsupported schema")
    require(set(contract) <= {"schema_version", "skill_dir", "entry_files", "clauses", "strong_markers", "weak_words"},
            "unknown contract property")
    skill_dir = (base / contract.get("skill_dir", ".")).resolve()
    require(skill_dir.is_dir(), "skill directory absent")
    entry = contract.get("entry_files")
    require(isinstance(entry, list) and entry and all(nonempty_text(item) for item in entry) and len(set(entry)) == len(entry),
            "entry_files must list the files read before execution")
    strong = tuple(contract.get("strong_markers", STRONG))
    weak = tuple(contract.get("weak_words", WEAK))
    require(all(nonempty_text(x) for x in strong + weak), "marker lists need nonempty text")
    texts, hashes = {}, {}
    for name in entry:
        path = (skill_dir / name).resolve()
        require(skill_dir in path.parents or path == skill_dir, "entry file outside skill directory")
        data = path.read_bytes()
        texts[name] = data.decode("utf-8-sig").splitlines()
        hashes[name] = hashlib.sha256(data).hexdigest()
    clauses = contract.get("clauses")
    require(isinstance(clauses, list) and clauses, "clauses required")
    seen, results = set(), []
    for clause in clauses:
        require(isinstance(clause, dict) and set(clause) <= {"id", "source", "strength", "anchors", "window", "scope", "narrowing"}, "invalid clause")
        require(nonempty_text(clause.get("id")) and clause["id"] not in seen, "unique clause id required")
        seen.add(clause["id"])
        require(nonempty_text(clause.get("source")), "clause needs a source reference in the upper requirement")
        require(clause.get("strength") in STRENGTHS, "strength must be must/never/only/default")
        anchors = clause.get("anchors")
        require(isinstance(anchors, list) and anchors and all(nonempty_text(a) for a in anchors), "anchors required")
        scope, narrowing = clause.get("scope", []), clause.get("narrowing", [])
        require(isinstance(scope, list) and isinstance(narrowing, list) and all(nonempty_text(x) for x in scope + narrowing),
                "scope and narrowing must be lists of text")
        window = clause.get("window", 1)
        require(isinstance(window, int) and not isinstance(window, bool) and 1 <= window <= 6, "window must be 1..6")
        found, hard_ok, narrowed = [], [], []
        for name, lines in texts.items():
            for start in range(len(lines)):
                chunk = "\n".join(lines[start:start + window])
                if all(anchor in chunk for anchor in anchors):
                    found.append((name, start + 1))
                    lowered = chunk.lower()
                    scope_ok = all(term in chunk for term in scope) and not any(term in chunk for term in narrowing)
                    strong_ok = clause["strength"] == "default" or (
                        any(m in lowered for m in strong) and not any(w in lowered for w in weak))
                    if strong_ok and scope_ok:
                        hard_ok.append((name, start + 1))
                    elif strong_ok and not scope_ok:
                        narrowed.append((name, start + 1))
        if hard_ok:
            status, where = "ok", hard_ok[0]
        elif narrowed:
            status, where = "narrowed", narrowed[0]
        elif found:
            status, where = "weakened", found[0]
        else:
            status, where = "missing", None
        results.append({"id": clause["id"], "strength": clause["strength"], "status": status,
                        "file": where[0] if where else None, "line": where[1] if where else None,
                        "candidate_locations": len(found)})
    ok = all(item["status"] == "ok" for item in results)
    return {"schema_version": 1, "status": "pass" if ok else "fail", "entry_hashes": hashes, "clauses": results,
            "limits": "Lexical check on files read before execution: anchors co-occur in a line window with a strength marker, "
                      "no weakening word, every declared scope term and no declared narrowing phrase. Does not judge meaning, exceptions or whether the clause is correct; "
                      "read each located line. A rule found only outside entry_files counts as missing."}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", type=Path)
    args = parser.parse_args()
    try:
        data = args.contract.read_bytes()
        contract = json.loads(data.decode("utf-8-sig"), object_pairs_hook=json_object,
                              parse_constant=lambda _: (_ for _ in ()).throw(TraceError("non-finite JSON")))
        require(isinstance(contract, dict), "contract object required")
        result = audit(contract, args.contract.resolve().parent)
        result["sources"] = {"contract": {"path": str(args.contract), "sha256": hashlib.sha256(data).hexdigest()}}
    except TraceError as exc:
        print(json.dumps({"schema_version": 1, "status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError):
        print(json.dumps({"schema_version": 1, "status": "error",
                          "error": "Invalid contract or unreadable entry file."}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
