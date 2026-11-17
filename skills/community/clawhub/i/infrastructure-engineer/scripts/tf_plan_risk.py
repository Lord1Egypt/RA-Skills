#!/usr/bin/env python3
"""
tf_plan_risk.py — Terraform 计划 JSON 风险标红（确定性、可复现）

读取 `terraform show -json <plan>` 的输出，统计各资源的 create/update/delete/replace，
并标红删除/替换（破坏面）与 IAM/安全类资源变更。

用法:
    terraform show -json plan.out > plan.json
    python3 tf_plan_risk.py plan.json                 # 人类可读
    python3 tf_plan_risk.py plan.json --json          # 机器可读
    python3 tf_plan_risk.py plan.json --strict        # 有 delete/replace 时退出码 1

不替代人工审查；仅做静态标红。
"""
import argparse
import json
import sys

SECURITY_HINTS = ("iam", "policy", "role", "security", "kms", "secret", "acl", "firewall", "sg_")


def classify(actions):
    if "delete" in actions and "create" in actions:
        return "replace"
    if actions == ["delete"]:
        return "delete"
    if "create" in actions:
        return "create"
    if "update" in actions:
        return "update"
    return "noop"


def analyze(plan):
    rows = []
    for rc in plan.get("resource_changes", []):
        change = rc.get("change", {})
        actions = change.get("actions", [])
        kind = classify(actions)
        if kind == "noop" or not actions:
            continue
        rtype = rc.get("type", "")
        addr = rc.get("address", "")
        is_sec = any(h in (rtype + " " + addr).lower() for h in SECURITY_HINTS)
        rows.append({"address": addr, "type": rtype, "action": kind, "security": is_sec})
    return rows


def main():
    ap = argparse.ArgumentParser(description="Terraform 计划风险标红")
    ap.add_argument("plan", help="terraform show -json 输出的计划文件")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--strict", action="store_true",
                    help="存在 delete/replace 时退出码 1")
    args = ap.parse_args()

    try:
        with open(args.plan, "r", encoding="utf-8") as f:
            plan = json.load(f)
    except (OSError, ValueError) as e:
        print(f"无法读取计划 JSON: {e}", file=sys.stderr)
        return 2

    rows = analyze(plan)
    destructive = [r for r in rows if r["action"] in ("delete", "replace")]

    if args.json:
        print(json.dumps({"total": len(rows),
                          "destructive": len(destructive),
                          "rows": rows}, ensure_ascii=False, indent=2))
    else:
        if not rows:
            print("✅ 计划中无资源变更")
        else:
            from collections import Counter
            c = Counter(r["action"] for r in rows)
            print(f"变更统计: create={c.get('create',0)} "
                  f"update={c.get('update',0)} delete={c.get('delete',0)} "
                  f"replace={c.get('replace',0)}")
            for r in rows:
                tag = "🔴" if r["action"] in ("delete", "replace") else "🟡" if r["security"] else "🟢"
                sec = " [SECURITY]" if r["security"] else ""
                print(f"{tag} {r['action'].upper():8} {r['address']}{sec}")
            if destructive:
                print(f"\n⚠️ {len(destructive)} 个破坏级变更（delete/replace），apply 前需人工确认")

    if args.strict and destructive:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
