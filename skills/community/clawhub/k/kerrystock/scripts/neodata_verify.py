#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kerrystock 步骤 2 — 用 neodata 交叉验证历史季节性 / 区间涨跌幅 / 研报观点。

封装两层踩坑经验（见 references/lessons.md 第二节）：
  1) neodata 的 --save-token 在只读/沙盒环境写入失败 → 本脚本强制用 --token 直传；
  2) token 须经 connect_cloud_service 工具获取（约24h有效），每次新会话重取。

用法：
  python3 neodata_verify.py --query "601138 历年月度涨跌幅 季节性统计" --token <tempToken> [--out verify.md]
"""
import os
import sys
import subprocess
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import _builtin_skill_path

# 默认指向内置 neodata 技能目录，可用环境变量 NEODATA_SCRIPT 覆盖
NEODATA = os.environ.get("NEODATA_SCRIPT") or _builtin_skill_path("neodata-financial-search/scripts/query.py")
PY = os.environ.get("PYTHON_BIN", sys.executable)


def main():
    ap = argparse.ArgumentParser(description="Kerrystock 步骤2 季节性交叉验证 (neodata)")
    ap.add_argument("--query", required=True, help="自然语言查询，建议显式要逐月/区间涨跌幅数值")
    ap.add_argument("--token", required=True, help="connect_cloud_service 获取的临时 token（约24h有效）")
    ap.add_argument("--out", default=None, help="可选：结果保存为 .md 供研报引用")
    args = ap.parse_args()

    if not NEODATA or not os.path.exists(NEODATA):
        print(f"[error] neodata 脚本不存在: {NEODATA}\n请设置环境变量 NEODATA_SCRIPT 指向 query.py", file=sys.stderr)
        sys.exit(1)

    # 关键：用 --token 直传，避免 --save-token 在只读环境的写入失败
    cmd = [PY, NEODATA, "--query", args.query, "--token", args.token]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        sys.exit(r.returncode)

    print(r.stdout)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(f"# neodata 验证：{args.query}\n\n")
            f.write(r.stdout)
        print(f"\n[ok] 已保存: {args.out}")


if __name__ == "__main__":
    main()
