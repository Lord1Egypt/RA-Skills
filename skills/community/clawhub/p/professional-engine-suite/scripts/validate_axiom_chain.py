#!/usr/bin/env python3
r"""推导链公理引用合法性校验：检查推导记录中引用的公理/本构编号是否存在、格式是否合法。
用法: python validate_axiom_chain.py <推导记录.md>
依赖：Python 3 标准库，无第三方依赖；可独立执行。
规则: [U\d{2}] 须在 U01-U22；[L2-<领域>-\d{2}] 领域须为已知分节。
"""
import re, sys

U_MAX = 22
DOMAINS = ["力学", "电学", "热学", "流体", "材料", "光学", "化工", "生物"]

def main():
    if len(sys.argv) != 2:
        print("用法: python validate_axiom_chain.py <推导记录.md>"); sys.exit(2)
    text = open(sys.argv[1], encoding="utf-8").read()
    refs = re.findall(r"\[(U\d{2}|L2-[^-\]]+-\d{2})\]", text)
    if not refs:
        print("FAIL 未发现任何公理/本构编号引用（推导链不可审计）"); sys.exit(1)
    bad = []
    for r in refs:
        if r.startswith("U"):
            n = int(r[1:])
            if n < 1 or n > U_MAX:
                bad.append(f"{r}: 超出 U01-U{U_MAX} 范围")
        else:
            dom = r.split("-")[1]
            if dom not in DOMAINS:
                bad.append(f"{r}: 未知领域 {dom}")
    if bad:
        print("FAIL"); [print(" -", b) for b in bad]; sys.exit(1)
    print(f"PASS 共 {len(refs)} 处引用，编号全部合法")
    sys.exit(0)

if __name__ == "__main__":
    main()
