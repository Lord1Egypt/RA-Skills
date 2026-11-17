#!/usr/bin/env python3
"""
prompt-templates-cli.py - render parameterized prompt templates from a catalog.

Loads a templates.json catalog, fills {{var}} placeholders from --set, and prints the
rendered prompt. Great for shipping consistent agent instructions. Stdlib only.

Usage:
  python prompt-templates-cli.py list
  python prompt-templates-cli.py render <name> --set role=QA --set tone=strict [--json]
  python prompt-templates-cli.py self-test
"""
import argparse
import json
import os
import re
import sys

VAR = re.compile(r"\{\{(\w+)\}\}")


def _default_catalog():
    return {
        "code-review": "You are a {{role}} reviewer. Tone: {{tone}}. Check for bugs, security, and clarity.",
        "summarize": "Summarize the following in {{count}} bullets for a {{audience}} audience.",
    }


def load_catalog(path):
    if path and os.path.isfile(path):
        return json.load(open(path, encoding="utf-8"))
    return _default_catalog()


def render(name, sets, catalog):
    if name not in catalog:
        raise KeyError(f"template '{name}' not found")
    tpl = catalog[name]
    kv = {}
    for s in sets:
        if "=" in s:
            k, v = s.split("=", 1); kv[k] = v
    missing = VAR.findall(tpl)
    missing = [m for m in missing if m not in kv]
    out = VAR.sub(lambda m: kv.get(m.group(1), "{{" + m.group(1) + "}}"), tpl)
    return out, missing


def self_test():
    cat = _default_catalog()
    out, missing = render("code-review", ["role=senior", "tone=strict"], cat)
    ok = "senior" in out and "strict" in out and not missing
    print("self-test:", "PASS" if ok else "FAIL", f"(missing={missing})")
    return 0 if ok else 1


def main():
    p = argparse.ArgumentParser(description="prompt-templates-cli")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    r = sub.add_parser("render"); r.add_argument("name"); r.add_argument("--set", action="append", default=[]); r.add_argument("--catalog")
    sub.add_parser("self-test")
    a = p.parse_args()
    cat = load_catalog(getattr(a, "catalog", None))
    if a.cmd == "list":
        for k in cat: print(" -", k)
    elif a.cmd == "render":
        try:
            out, missing = render(a.name, a.set, cat)
            if missing: print("MISSING VARS:", missing)
            print(out)
        except KeyError as e:
            print("ERROR:", e); return 1
    elif a.cmd == "self-test":
        return self_test()
    return 0


if __name__ == "__main__":
    sys.exit(main())
