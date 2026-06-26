#!/usr/bin/env python3
import sys
import re

LAWS = [
    "集体力量: 优先数据/团队共识?",
    "规则永恒: 符合铁律无特权?",
    "IV禁令: VIX>10% or 高IV不开?",
    "45min: 有定时杀开关?",
    "自毁锚点: 设反向止损?",
    "零容忍: 无借口执行?"
]

def audit(decision):
    violations = []
    for law in LAWS:
        if not re.search(law.split(':')[1].strip('?'), decision, re.I):
            violations.append(law)
    return violations

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python validate.py 'Your decision here'")
        sys.exit(1)
    decision = ' '.join(sys.argv[1:])
    violations = audit(decision)
    if violations:
        print("🚨 VIOLATIONS:", violations)
        print("EXECUTE KILL SWITCH")
        sys.exit(1)
    else:
        print("✅ CLEARED: Jungle compliant.")
