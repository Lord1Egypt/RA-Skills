#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/run_meta.py — meta-analysis 技能「计算轨」一键入口（消除 LLM 中间插手）

设计目标（对齐 §0 双轨门控 + 延迟不变量）：
  - 把 build_request（classify + 列解析 + 装配）与 run_analysis（coze 计算 + HTML 报告）
    合并为 1 次本地调用：agent 只发 1 条命令，中间无决策点、无插手空间。
  - 成功时单独打印 `META_HTML_REPORT=<abs path>`，agent 直接 present_files，
    无需再跑 Bash 用 ls/grep 找报告（物理消灭 §0.2 禁项）。
  - 零 LLM 决策：轨道/任务/measure/model 全由 classify.py 关键词表（build_request 内部调用）决定。
  - 零本地计算：数值全走 coze。

CLI:
  python scripts/run_meta.py --query "..." --data <csv|.json> [--data-json '[...]'] [--out request.json]
"""
import os
import sys
import json
import argparse
import tempfile

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL_DIR, "scripts"))
sys.path.insert(0, os.path.join(SKILL_DIR, "adapters"))

from build_request import build
from run_analysis import run_analysis
from extraction_guard import check_verified


def _resolve_out_dir(arg_out_dir, data_arg):
    """报告输出目录解析（避免报告藏进技能目录 / 用户工作区找不到）。

    - 显式 --out-dir → 直接用；
    - 否则若给了 --data 文件 → 默认落在数据文件同目录（通常就在用户工作区）；
    - 否则 → 当前工作目录（agent 应在用户工作区运行本脚本）。
    若以上都落到技能自身目录（agent 误 cd 进技能目录且没传 --out-dir），
    打印显式告警，提示报告会落在技能目录而非工作区。
    """
    if arg_out_dir:
        return os.path.abspath(arg_out_dir)
    if data_arg:
        return os.path.abspath(os.path.dirname(os.path.abspath(data_arg)))
    cwd = os.path.abspath(os.getcwd())
    if os.path.commonpath([cwd, SKILL_DIR]) == SKILL_DIR:
        sys.stderr.write(
            "\n[run_meta][WARN] 当前工作目录是技能自身目录且未传 --out-dir，"
            "HTML 报告将落在技能目录而非用户工作区。请在用户工作区运行本脚本，"
            "或显式传 --out-dir <用户工作区路径>。\n"
        )
    return cwd


def main():
    ap = argparse.ArgumentParser(description="meta-analysis 计算轨一键入口（build+run，零 LLM 决策）")
    ap.add_argument("--query", required=True, help="用户原始请求（内部调 classify 出 spec）")
    ap.add_argument("--data", help="研究数据文件（.csv / .json）；csv 会自动转换为 JSON 再发 coze")
    ap.add_argument("--data-json", help="研究数据内联 JSON（行数组 / {'rows':[...]}）；免写文件，优先用于对话内数据")
    ap.add_argument("--out-dir", default=None,
                    help="HTML 报告输出目录（默认：--data 同目录 / 当前工作目录）；建议传用户工作区，如 <workspace>/meta_analysis")
    ap.add_argument("--out", default=None, help="内部 request.json 路径（默认系统临时目录，不写工作区）")
    ap.add_argument("--colmap", help="LLM 兜底回灌：列映射 JSON")
    ap.add_argument("--measure", help="LLM 兜底回灌：效应量覆盖")
    ap.add_argument("--model", help="LLM 兜底回灌：模型覆盖")
    ap.add_argument("--language", default=None,
                    help="用户语言（zh/en/...），覆盖自动检测；注入 coze 入参 user_language 备用")
    ap.add_argument("--trust-data", action="store_true",
                    help="显式担责兜底：跳过抽取人工核验闸（仅用于用户确认可信的手搓/存量 CSV）")
    a = ap.parse_args()

    # 抽取核验闸：extract_assist 生成的 CSV 须人工核验（stamp --confirm）后才可进计算轨；
    # 无同伴 .provenance.json 的存量/手搓 CSV 视为可信放行（见 extraction_guard.check_verified）。
    if a.data:
        ok, reason, status = check_verified(a.data, trust=a.trust_data)
        if not ok:
            print("META_STATUS=%s | %s" % (status, reason))
            sys.exit(3)

    # 内部 request.json 默认落临时目录，绝不污染用户工作区
    out_path = a.out or os.path.join(tempfile.gettempdir(), "meta_request.json")
    out_dir = _resolve_out_dir(a.out_dir, a.data)

    try:
        req = build(
            query=a.query,
            data_arg=a.data,
            data_json=a.data_json,
            out_path=out_path,
            colmap_override=a.colmap,
            measure_override=a.measure,
            model_override=a.model,
            language_override=a.language,
        )
    except SystemExit as e:
        # build_request 在选题轨 / 缺字段 / 列解析失败时会 SystemExit 并打印原因
        print("META_STATUS=build_failed | " + str(e))
        sys.exit(2)

    out = run_analysis(req["task"], req["data"], req["params"], req["figure"], out_dir=out_dir)

    hp = out.get("html_report")
    if hp:
        print("META_HTML_REPORT=" + os.path.abspath(hp))
    elif out.get("status") == "error":
        print("META_STATUS=error | " + str(out.get("notes") or "")[:200])
        # 2026-09-13：转印结构化诊断（信封拦截 / coze error），让 agent 直接 relay 给用户
        ea = out.get("_error_analysis") or {}
        guidance = out.get("_error_guidance")
        if guidance:
            print("---- META_ERROR_GUIDANCE ----")
            print(guidance)
        elif ea:
            print("META_ERROR_ANALYSIS=" + json.dumps(ea, ensure_ascii=False)[:600])
    else:
        print("META_STATUS=" + str(out.get("status", "unknown")))


if __name__ == "__main__":
    main()
