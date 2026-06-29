#!/usr/bin/env python3
"""
Causality Check — 因果链验证
校验大纲/子结构概述的因果逻辑
"""
import json, sys
from pathlib import Path

MIN_SUMMARY_CHARS = 12

# 门禁映射: mode → gate name
GATE_MAP = {
    "outline": "outline_causality",
    "sub-structure": "sub_causality",
}

def check_causality(state_path, mode, chapter=None):
    data = json.loads(Path(state_path).read_text(encoding="utf-8-sig"))
    issues = []

    if mode == "outline":
        # 校验各章概述的因果完整性
        for ch in data.get("chapters", []):
            overview = ch.get("overview", "")
            if len(overview.strip()) < MIN_SUMMARY_CHARS:
                issues.append({
                    "chapter": ch["id"],
                    "desc": f"概述过短 ({len(overview.strip())}字符, 需≥{MIN_SUMMARY_CHARS})",
                    "type": "概述完整性"
                })
            if not any(v in overview for v in ["因为", "所以", "导致", "发现", "决定", "开始", "被迫", "意识到"]):
                issues.append({
                    "chapter": ch["id"],
                    "desc": "概述缺少因果动词",
                    "type": "因果链"
                })
    elif mode == "sub-structure" and chapter:
        for ch in data.get("chapters", []):
            if ch["id"] != chapter:
                continue
            subs = ch.get("sub_structures", {})
            for sk, sv in subs.items():
                summary = sv.get("summary", "")
                if len(summary.strip()) < MIN_SUMMARY_CHARS:
                    issues.append({
                        "chapter": ch["id"],
                        "sub": sk,
                        "desc": f"概述过短 ({len(summary.strip())}字符)",
                        "type": "概述完整性"
                    })
                if sv.get("tone", "").strip() == "":
                    issues.append({
                        "chapter": ch["id"],
                        "sub": sk,
                        "desc": "缺少情绪提示(tone)",
                        "type": "完整性"
                    })

    # 输出报告
    mode_label = f"{mode} {chapter}" if chapter else mode
    print(f"[因果链验证] {mode_label}")
    if not issues:
        print(f"  [OK] 全部通过")
        # 自动 pass 对应门禁
        gate_name = GATE_MAP.get(mode)
        if gate_name:
            try:
                # 动态导入避免循环依赖
                import importlib
                pg = importlib.import_module("novel_pipeline_gate")
                pg.pass_gate(state_path, gate_name)
                print(f"  [门禁自动] {gate_name} [OK] PASS")
            except Exception as e:
                print(f"  [门禁自动] {gate_name} [SKIP] {e}")
    else:
        for issue in issues:
            print(f"  [FAIL] [{issue.get('chapter','')} {issue.get('sub','')}] {issue['type']}: {issue['desc']}")

    return len(issues) == 0

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python novel_causality_check.py <outline|sub-structure> <state_path> [chapter]")
        sys.exit(1)
    mode = sys.argv[1]
    sp = sys.argv[2]
    ch = sys.argv[3] if len(sys.argv) > 3 else None
    ok = check_causality(sp, mode, ch)
    if not ok:
        sys.exit(1)
