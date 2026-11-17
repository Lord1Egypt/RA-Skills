#!/usr/bin/env python3
"""
manifest-diff.py - diff two agent capability manifests and report what changed.

Compares name/version/capabilities/dependencies/memory/tools/api/status between two
manifest JSON files. Stdlib only.

Usage:
  python manifest-diff.py a.json b.json [--json]
  python manifest-diff.py self-test
"""
import argparse
import json
import sys

FIELDS = ["name", "version", "capabilities", "dependencies",
          "memory_requirements", "tools", "api", "status"]


def diff(a_path, b_path, as_json):
    A = json.load(open(a_path, encoding="utf-8"))
    B = json.load(open(b_path, encoding="utf-8"))
    changes = {}
    for f in FIELDS:
        va, vb = A.get(f), B.get(f)
        if va != vb:
            changes[f] = {"from": va, "to": vb}
    added = [k for k in B if k not in A]
    removed = [k for k in A if k not in B]
    res = {"changed_fields": changes, "added_keys": added, "removed_keys": removed,
           "summary": f"{len(changes)} field(s) changed, {len(added)} added, {len(removed)} removed"}
    if as_json:
        print(json.dumps(res, indent=2))
    else:
        print(res["summary"])
        for f, d in changes.items():
            print(f"  ~ {f}: {d['from']} -> {d['to']}")
        for k in added: print(f"  + {k}")
        for k in removed: print(f"  - {k}")
    return res


def self_test():
    import tempfile, os
    a = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
    json.dump({"name": "X", "version": "1.0", "capabilities": ["a"]}, a); a.close()
    b = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
    json.dump({"name": "X", "version": "2.0", "capabilities": ["a", "b"]}, b); b.close()
    r = diff(a.name, b.name, False)
    os.unlink(a.name); os.unlink(b.name)
    ok = "version" in r["changed_fields"] and "capabilities" in r["changed_fields"]
    print("self-test:", "PASS" if ok else "FAIL", f"(changes={list(r['changed_fields'])})")
    return 0 if ok else 1


def main():
    p = argparse.ArgumentParser(description="manifest-diff")
    sub = p.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("diff"); d.add_argument("a"); d.add_argument("b"); d.add_argument("--json", action="store_true")
    sub.add_parser("self-test")
    a = p.parse_args()
    if a.cmd == "self-test": return self_test()
    if a.cmd == "diff": diff(a.a, a.b, a.json); return 0


if __name__ == "__main__":
    sys.exit(main())
