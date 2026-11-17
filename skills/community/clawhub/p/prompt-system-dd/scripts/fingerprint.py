#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEPTH 指纹工具(R07 指纹 v2)

三个子命令:
  parse  解析带后缀的指纹,校验合法性并输出结构化结果
  hash   计算指纹规范哈希,用于缓存命中与复现追溯
  diff   比较两个指纹,输出逐位差异与受影响模块

指纹语法:
  DEPTH: [d1,...,d9] [@model=<id>] [@lang=zh|en|bilingual] [@tokens=<正整数>]

用法:
  python scripts/fingerprint.py parse "DEPTH: [3,3,3,3,3,3,3,3,3] @model=claude @lang=zh"
  python scripts/fingerprint.py hash  "DEPTH: [3,3,3,3,3,3,3,3,3] @model=claude"
  python scripts/fingerprint.py diff  "DEPTH: [3,3,3,3,3,3,3,3,3]" "DEPTH: [4,4,4,4,2,4,4,4,4]"

输出:stdout JSON。退出码 0=成功 / 2=解析失败 / 3=diff 存在降级(仅提示,非错误)
注意:档位位序与 validate_skill.py CORE_ATOM_KEYS 必须一致(门禁 FP003 校验)。
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

# 与 validate_skill.py CORE_ATOM_KEYS 一致(组装顺序),修改需同步两侧
CORE_ATOM_KEYS = [
    "role-anchor", "task-define", "context-inject", "example-shot",
    "format-spec", "think-chain", "constraints", "self-check", "iterate",
]

# 合法后缀键及其取值约束
SUPPORTED_SUFFIXES = {
    "model": {"kind": "enum", "values": None},   # 以 model-adapters/ 目录为准
    "lang": {"kind": "enum", "values": {"zh", "en", "bilingual"}},
    "tokens": {"kind": "int"},
}

# 依赖规则 R1-R5:(条件原子, 条件, 要求原子, 要求)  用于 diff 后提示重跑
DEPENDENCY_RULES = [
    ("think-chain", "=", 4, "self-check", "≥", 3),
    ("constraints", "=", 4, "role-anchor", "≥", 3),
    ("context-inject", "=", 1, "think-chain", "≤", 2),
    ("task-define", "≥", 3, "constraints", "≥", 2),
    ("role-anchor", "=", 4, "constraints", "≥", 3),
]

FP_RE = re.compile(
    r"^(?:DEPTH:\s*)?\[(?P<digits>[\d,\s]+)\](?P<suffixes>(?:\s+@[a-z]+=\S+)*)\s*$"
)
SUF_RE = re.compile(r"@(?P<key>[a-z]+)=(?P<val>[^\s]+)")


def adapters_dir(skill_dir):
    return Path(skill_dir) / "references" / "model-adapters"


def registered_models(skill_dir):
    d = adapters_dir(skill_dir)
    if not d.is_dir():
        return set()
    return {p.stem for p in d.glob("*.md")}


def parse_fp(text, skill_dir="."):
    """返回 (ok, data|error)"""
    s = (text or "").strip()
    if not s:
        return False, {"error": "指纹为空"}
    m = FP_RE.match(s)
    if not m:
        return False, {"error": "指纹格式不匹配 "
                                "'DEPTH: [d1,...,d9] [@k=v ...]'"}
    digits = [d.strip() for d in m.group("digits").split(",") if d.strip()]
    if len(digits) != len(CORE_ATOM_KEYS):
        return False, {"error": f"指纹位数 {len(digits)} 与核心原子数 "
                                f"{len(CORE_ATOM_KEYS)} 不一致"}
    levels = []
    for d in digits:
        if not re.fullmatch(r"\d+", d):
            return False, {"error": f"非法档位值: {d}"}
        v = int(d)
        if not 1 <= v <= 4:
            return False, {"error": f"档位 {v} 越界(应为 1-4)"}
        levels.append(v)

    suffixes = {}
    for sm in SUF_RE.finditer(m.group("suffixes")):
        key, val = sm.group("key"), sm.group("val")
        if key not in SUPPORTED_SUFFIXES:
            return False, {"error": f"未支持的后缀 @{key}=,"
                                    f"合法: {sorted(SUPPORTED_SUFFIXES)}"}
        spec = SUPPORTED_SUFFIXES[key]
        if spec["kind"] == "int":
            if not re.fullmatch(r"\d+", val):
                return False, {"error": f"@{key} 需为正整数,当前 {val}"}
            suffixes[key] = int(val)
        elif spec["values"] is None:
            known = registered_models(skill_dir)
            if val not in known:
                # T24: 注册表缺失/为空时必须拒绝,不得静默放行
                if known:
                    return False, {"error": f"@{key}={val} 未注册,"
                                            f"已注册: {sorted(known)}"}
                return False, {"error": f"@{key}={val} 无法校验:"
                                        f"适配器注册表缺失或为空"
                                        f"({adapters_dir(skill_dir)})"}
            suffixes[key] = val
        else:
            if val not in spec["values"]:
                return False, {"error": f"@{key}={val} 非法,"
                                        f"合法: {sorted(spec['values'])}"}
            suffixes[key] = val

    data = {
        "levels": levels,
        "depths": dict(zip(CORE_ATOM_KEYS, levels)),
        "suffixes": suffixes,
    }
    return True, data


def canonical(data):
    """规范化串:档位 + 排除 tokens 后的排序后缀(tokens 是预算,非产出特征)。
    P2-1:lang=zh 是缺省值,视同未声明,不产生新哈希(与 depth-adaptation.md
    "默认值不产生新哈希"承诺一致)。"""
    parts = ["[%s]" % ",".join(str(x) for x in data["levels"])]
    for k in sorted(data["suffixes"]):
        if k == "tokens":
            continue
        if k == "lang" and data["suffixes"][k] == "zh":
            continue
        parts.append(f"{k}={data['suffixes'][k]}")
    return "|".join(parts)


def fp_hash(data, n=12):
    return hashlib.sha256(canonical(data).encode("utf-8")).hexdigest()[:n]


def check_rules(depths):
    """返回违反的 R 规则列表"""
    def val(atom):
        return depths.get(atom)

    bad = []
    for i, (a, aop, alv, b, bop, blv) in enumerate(DEPENDENCY_RULES, start=1):
        av, bv = val(a), val(b)
        if av is None or bv is None:
            continue
        aok = {"=": av == alv, "≥": av >= alv, "≤": av <= alv}[aop]
        if not aok:
            continue
        bok = {"=": bv == blv, "≥": bv >= blv, "≤": bv <= blv}[bop]
        if not bok:
            bad.append({"rule": f"R{i}",
                        "detail": f"{a}=D{av} 要求 {b}{bop}D{blv},实际 D{bv}"})
    return bad


def diff_fp(a, b):
    la, lb = a["levels"], b["levels"]
    changed = []
    for i, (atom) in enumerate(CORE_ATOM_KEYS):
        if la[i] != lb[i]:
            changed.append({
                "slot": i + 1,
                "atom": atom,
                "from": la[i],
                "to": lb[i],
                "direction": "升档" if lb[i] > la[i] else "降档",
                "delta": lb[i] - la[i],
            })
    sa, sb = a["suffixes"], b["suffixes"]
    suf_changed = []
    for k in sorted(set(sa) | set(sb)):
        if sa.get(k) != sb.get(k):
            suf_changed.append({"key": k, "from": sa.get(k), "to": sb.get(k)})
    return {
        "levels_changed": changed,
        "suffixes_changed": suf_changed,
        "changed_count": len(changed),
        "regenerate_modules": [c["atom"] for c in changed],
        "dependency_violations": check_rules(b["depths"]),
        "hash_from": fp_hash(a),
        "hash_to": fp_hash(b),
    }


def main():
    ap = argparse.ArgumentParser(description="DEPTH 指纹工具(R07)")
    ap.add_argument("command", choices=["parse", "hash", "diff"])
    ap.add_argument("fingerprints", nargs="+")
    ap.add_argument("--skill-dir", default=".")
    args = ap.parse_args()

    if args.command == "diff" and len(args.fingerprints) != 2:
        print(json.dumps({"error": "diff 需恰好两个指纹"},
                         ensure_ascii=False, indent=2))
        sys.exit(2)

    parsed = []
    for raw in args.fingerprints:
        ok, data = parse_fp(raw, args.skill_dir)
        if not ok:
            print(json.dumps({"error": data["error"], "input": raw},
                             ensure_ascii=False, indent=2))
            sys.exit(2)
        parsed.append(data)

    if args.command == "parse":
        d = parsed[0]
        d["canonical"] = canonical(d)
        d["hash"] = fp_hash(d)
        d["dependency_violations"] = check_rules(d["depths"])
        print(json.dumps(d, ensure_ascii=False, indent=2))
        sys.exit(0)

    if args.command == "hash":
        d = parsed[0]
        print(json.dumps({"canonical": canonical(d),
                          "hash": fp_hash(d),
                          "note": "tokens 后缀不计入哈希(预算非产出特征)"},
                         ensure_ascii=False, indent=2))
        sys.exit(0)

    result = diff_fp(parsed[0], parsed[1])
    downgrades = [c for c in result["levels_changed"] if c["delta"] < 0]
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(3 if downgrades else 0)


if __name__ == "__main__":
    main()
