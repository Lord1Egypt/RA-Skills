#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/extraction_guard.py — 数据提取「人工核验闸」守卫

对齐 prisma_bridge.py 的 [MANUAL] 哲学：凡是「自动化产出、但必须经人工确认」的数据，
在进入计算轨之前都要被显式核验。

判定逻辑（check_verified）：
  - 仅对 .csv 数据文件生效（--data-json 内联数据属对话内可信构造，不拦）；
  - 查找同伴文件 <csv>.provenance.json（由 extract_assist.py 生成）：
      * 存在且 verified_by_human == True  → 放行 (ok=True)
      * 存在且 verified_by_human == False → 拦截 (status="unverified_extraction")
      * 不存在                            → 放行但提示（视为人工手搓 CSV，信任）
  - trust=True 时一律放行（run_meta --trust-data 兜底，供用户明确负责的存量/手搓数据）。

返回 (ok, reason, status)：
  ok=False 时 status 用于 run_meta 的 META_STATUS 输出。
"""
import json
import os


def provenance_path(data_path):
    return data_path + ".provenance.json"


def check_verified(data_path, trust=False):
    """Return (ok, reason, status)."""
    if trust:
        return True, "trust-data override: 跳过抽取核验闸", "ok"

    if not data_path or not data_path.lower().endswith(".csv"):
        # 非 CSV（如 .json 内联/文件）→ 不归本守卫管
        return True, "non-csv data, guard skipped", "ok"

    p = provenance_path(data_path)
    if not os.path.exists(p):
        return (True,
                "no companion .provenance.json: 视为人工手搓 CSV，按可信放行（如本表由 extract_assist 生成，请先 stamp --confirm）",
                "ok_trusted_legacy")

    try:
        with open(p, encoding="utf-8") as f:
            prov = json.load(f)
    except Exception as e:
        return False, "provenance 文件解析失败: %s" % e, "provenance_error"

    verified = bool(prov.get("verified_by_human"))
    if verified:
        schema_type = prov.get("schema_type", "?")
        return True, "verified_by_human=YES (type=%s)" % schema_type, "ok"

    # 存在但未核验 → 拦截
    note = prov.get("note", "")
    return (False,
            "数据提取未经人工核验 (verified_by_human=NO)。"
            " 该 CSV 由 extract_assist 生成但尚末 stamp --confirm ——"
            " 抽取精度属医学关键，禁止无人值守直灌计算轨。"
            " 请人工逐行核验（来源页码/表号）后运行："
            " extract_assist.py stamp --csv %s --confirm"
            " （或 run_meta 加 --trust-data 显式担责）。\n  provenance note: %s" % (data_path, note),
            "unverified_extraction")


def main():
    import argparse
    ap = argparse.ArgumentParser(description="检查抽取数据是否通过人工核验闸")
    ap.add_argument("--data", required=True, help="CSV 数据文件路径")
    ap.add_argument("--trust", action="store_true", help="信任兜底（等同 run_meta --trust-data）")
    a = ap.parse_args()
    ok, reason, status = check_verified(a.data, trust=a.trust)
    print("META_STATUS=%s | %s" % (status, reason))
    sys.exit(0) if ok else sys.exit(3)


if __name__ == "__main__":
    import sys
    main()
