#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
align.py —— 宪法式自我对齐引擎（critique → revise 闭环）。

给定可 machine-check 的宪法，对候选输出自我审查+自我修订，迭代到全对齐或达上限，
留完整审计轨迹。纯标准库。

用法：
  python align.py check --constitution C.json --text T.txt
  python align.py selftest
"""
import sys, re, json, argparse

SEV_ORDER = {"critical": 0, "major": 1, "minor": 2}
SEV_WEIGHT = {"critical": 1.0, "major": 0.5, "minor": 0.2}


def critique(text, constitution):
    """逐条检查，返回违宪列表（按严重级排序）。"""
    violations = []
    for p in constitution.get("principles", []):
        pid = p.get("id", "?")
        sev = p.get("severity", "minor")
        # forbid：命中即违宪
        for pat in p.get("forbid_patterns", []):
            for m in re.finditer(pat, text):
                violations.append({
                    "id": pid, "severity": sev, "kind": "forbid",
                    "pattern": pat, "matched": m.group(0),
                    "rule": p.get("rule", "")})
        # require：仅当触发条件命中且必需模式缺失时违宪
        req = p.get("require_patterns", [])
        if req:
            triggers = p.get("trigger_patterns", [])
            triggered = (not triggers) or any(re.search(t, text) for t in triggers)
            if triggered:
                for pat in req:
                    if not re.search(pat, text):
                        violations.append({
                            "id": pid, "severity": sev, "kind": "require",
                            "pattern": pat, "matched": None,
                            "rule": p.get("rule", "")})
    violations.sort(key=lambda v: SEV_ORDER.get(v["severity"], 3))
    return violations


def revise(text, violations, constitution):
    """按严重级顺序自动修订，返回新文本 + 本轮动作。"""
    pmap = {p["id"]: p for p in constitution.get("principles", [])}
    actions = []
    new = text
    for v in violations:
        p = pmap.get(v["id"], {})
        if v["kind"] == "forbid":
            repl = p.get("replace_with", "")
            before = new
            new = re.sub(v["pattern"], repl, new)
            if new != before:
                actions.append({"id": v["id"], "op": "replace" if repl else "delete",
                                "pattern": v["pattern"], "replace_with": repl})
        elif v["kind"] == "require":
            ins = p.get("require_insert", "")
            if ins and ins not in new:
                new = new.rstrip() + " " + ins
                actions.append({"id": v["id"], "op": "insert", "text": ins})
    return new, actions


def alignment_score(violations):
    penalty = sum(SEV_WEIGHT.get(v["severity"], 0.2) for v in violations)
    # 归一：以最坏假设每条 critical 为界，简化为 1/(1+penalty)
    return round(1.0 / (1.0 + penalty), 4)


def check(text, constitution, max_iters=5):
    trace = []
    cur = text
    for it in range(1, max_iters + 1):
        vios = critique(cur, constitution)
        score = alignment_score(vios)
        if not vios:
            trace.append({"iter": it, "violations": 0, "alignment": 1.0, "actions": []})
            break
        cur, actions = revise(cur, vios, constitution)
        trace.append({"iter": it, "violations": len(vios),
                      "alignment": score,
                      "vios": [(v["id"], v["kind"], v.get("matched")) for v in vios],
                      "actions": actions})
        # 若无任何有效修订动作，避免死循环
        if not actions:
            break

    final_vios = critique(cur, constitution)
    has_critical = any(v["severity"] == "critical" for v in final_vios)
    verdict = "ALIGNED" if (not final_vios) else "UNALIGNED"
    return {
        "original": text,
        "revised": cur,
        "final_violations": len(final_vios),
        "final_alignment": alignment_score(final_vios) if final_vios else 1.0,
        "has_unfixed_critical": has_critical,
        "verdict": verdict,
        "iterations": len(trace),
        "trace": trace,
        "needs_human": bool(final_vios),
    }


CONSTITUTION = {"principles": [
    {"id": "P1", "rule": "不得泄露11位手机号", "severity": "critical",
     "forbid_patterns": [r"1\d{10}"], "replace_with": "[已脱敏]"},
    {"id": "P2", "rule": "不得绝对化承诺", "severity": "major",
     "forbid_patterns": ["绝对", "100%保证"], "replace_with": "通常"},
    {"id": "P3", "rule": "投资内容须带风险提示", "severity": "major",
     "require_patterns": ["风险"], "require_insert": "（投资有风险，决策需谨慎）",
     "trigger_patterns": ["投资", "收益"]},
]}


def selftest():
    # 违规文本：含手机号(critical)、绝对化(major)、投资无风险提示(major)
    bad = "联系我13628266076，这个投资绝对赚，收益100%保证。"
    r = check(bad, CONSTITUTION)

    # 1. 首轮应检出至少 3 类违宪
    first = r["trace"][0]
    assert first["violations"] >= 3, f"首轮应≥3违宪，实为 {first['violations']}"
    # 2. 手机号被脱敏
    assert "13628266076" not in r["revised"], "手机号应被脱敏"
    assert "[已脱敏]" in r["revised"], "应插入脱敏标记"
    # 3. 绝对化被替换
    assert "绝对" not in r["revised"] and "100%保证" not in r["revised"], "绝对化应被替换"
    # 4. 补上风险提示
    assert "风险" in r["revised"], "应补风险提示"
    # 5. 最终对齐、无未修复 critical
    assert r["verdict"] == "ALIGNED", f"修订后应 ALIGNED，实为 {r['verdict']}"
    assert r["has_unfixed_critical"] is False, "不应残留 critical"
    assert r["final_violations"] == 0, "最终应 0 违宪"

    # 6. 合规文本：一次通过、0 违宪、1 轮
    good = "这是一段普通说明，投资有风险，决策需谨慎。"
    r2 = check(good, CONSTITUTION)
    assert r2["verdict"] == "ALIGNED", "合规文本应 ALIGNED"
    assert r2["iterations"] == 1, "合规文本应 1 轮通过"
    assert r2["revised"] == good, "合规文本不应被改动"

    # 7. critique 触发条件正确：无投资词则不要求风险提示
    r3_v = critique("今天天气不错。", CONSTITUTION)
    assert all(v["id"] != "P3" for v in r3_v), "未触发投资场景不应报 P3"

    print("revised   :", r["revised"])
    print("verdict   :", r["verdict"], "| iters:", r["iterations"],
          "| final_vios:", r["final_violations"])
    print("good-case :", r2["verdict"], "| iters:", r2["iterations"])
    print("\nSELFTEST: PASS")
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    c = sub.add_parser("check")
    c.add_argument("--constitution", required=True)
    c.add_argument("--text", required=True)
    c.add_argument("--max-iters", type=int, default=5)
    sub.add_parser("selftest")
    args = ap.parse_args()

    if args.cmd == "selftest":
        return selftest()
    elif args.cmd == "check":
        with open(args.constitution, encoding="utf-8") as f:
            cons = json.load(f)
        with open(args.text, encoding="utf-8") as f:
            text = f.read()
        print(json.dumps(check(text, cons, args.max_iters), ensure_ascii=False, indent=2))
        return 0
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
