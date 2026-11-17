#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
topic_gate.py — meta-analysis 选题门控（确定性路由，零 LLM 决策）

判定逻辑（对齐用户规范 2026-09-08）：
  1. 检查 ct-literature 技能是否已安装
     （默认 ~/.workbuddy/skills/ct-literature 存在且含 scripts/ct_literature.py）。
  2. 已安装 → 输出 path=ct_literature，并给出直接调用的完整命令（全面证据基础）。
  3. 未安装 → 输出 path=ct_search_prompt，附带：
       - 提示用户安装 ct-literature 的方式；
       - 询问用户：A) 安装后继续分析 / B) 直接做简单分析；
       - 若选 B，则调用 ct-search 远端服务（ct-search.coze.site/run，
         source=europepmc）直接做选题去重探针（无需安装 ct-literature）。

设计原则（对齐 §0 双轨门控）：零 LLM 决策、零网络、仅本地文件系统判定 + 命令拼装。
agents / 大模型据此输出做用户交互（AskUserQuestion），不在本脚本内做交互。
"""
import argparse
import datetime
import json
import os
import sys

# ct-literature 默认安装位置（与全平台其它 ct- 技能一致）
CT_LIT_DEFAULT = os.path.expanduser("~/.workbuddy/skills/ct-literature")
CT_SEARCH_ENDPOINT = os.environ.get("CT_SEARCH_ENDPOINT", "https://ct-search.coze.site/run")


def _detect_ct_literature(search_dirs=None):
    """返回 (installed:bool, dir:str|None)。

    仅做本地存在性判定：技能目录存在且含 scripts/ct_literature.py。
    不校验运行态 config / 出站授权（那是调用时的事）。
    """
    if search_dirs is None:
        search_dirs = [CT_LIT_DEFAULT]
        # 兼容把技能放在工作区 .workbuddy/skills 的情况
        env = os.environ.get("WORKBUDDY_SKILLS_DIR")
        if env:
            search_dirs.append(os.path.join(env, "ct-literature"))
    for d in search_dirs:
        if not d or not os.path.isdir(d):
            continue
        main_py = os.path.join(d, "scripts", "ct_literature.py")
        if os.path.isfile(main_py):
            return True, os.path.abspath(d)
    return False, None


def _this_year():
    return datetime.date.today().year


def _build_ct_literature_command(ct_lit_dir, topic, year_from=None):
    """已安装 ct-literature 时的全面检索命令（直接调用，无需经本技能中转）。"""
    yf = year_from if year_from else (_this_year() - 5)
    topic_q = json.dumps(topic, ensure_ascii=False)  # 双引号，shell 安全
    # 与 upstream_orchestration.md §2 一致的全面检索参数。
    # --online 必带：默认本地模式不经过 coze 端点、飞书汇总块在 if online: 内会被
    # 整个跳过（2026-09-08 实测踩坑：后台无任何记录）。
    return (
        'cd "%s" && python scripts/ct_literature.py --topic %s '
        "--review-type meta-analysis --with-europepmc --with-semantic-scholar "
        "--year-from %d --online --safety --prisma --run --out-dir ./lit"
        % (ct_lit_dir, topic_q, yf)
    )


def _build_ct_search_command(topic, year_from=None):
    """未安装 ct-literature、用户选「简单分析」时的 ct-search 远端探针命令。

    ct-search.coze.site/run 是 ct-literature 的统一文献检索后端（source 共用），
    直接 POST 即可，无需安装 ct-literature 技能。
    """
    yf = year_from if year_from else (_this_year() - 5)
    topic_q = json.dumps(topic, ensure_ascii=False)
    return (
        "python adapters/ctsearch_client.py search --source europepmc "
        "--keyword %s --year-from %d --run" % (topic_q, yf)
    )


def gate(topic, year_from=None):
    installed, ct_lit_dir = _detect_ct_literature()

    if installed:
        return {
            "ct_literature_installed": True,
            "ct_literature_dir": ct_lit_dir,
            "recommended_path": "ct_literature",
            "ct_literature_command": _build_ct_literature_command(ct_lit_dir, topic, year_from),
            "ct_search_command": None,
            "install_hint": None,
            "ask_user": False,
            "ask_user_prompt": None,
            "note": ("ct-literature 已安装，直接调用做全面文献检索（跨库去重 / 证据溯源 / "
                     "PRISMA），其 .merged.json / Excel / HTML 作为 Stage 4 新颖性证据。"),
        }

    # 未安装：交给 agent 询问用户
    return {
        "ct_literature_installed": False,
        "ct_literature_dir": None,
        "recommended_path": "ct_search_prompt",
        "ct_literature_command": None,
        "ct_search_command": _build_ct_search_command(topic, year_from),
        "install_hint": (
            "安装 ct-literature 技能：WorkBuddy 技能市场搜索 ct-literature 并安装，"
            "或 `git clone <ct-literature 仓库> ~/.workbuddy/skills/ct-literature`。"
        ),
        "ask_user": True,
        "ask_user_prompt": (
            "ct-literature 技能未安装。如何继续选题分析？\n"
            "  A) 安装 ct-literature 后再继续（功能最全：跨库检索 / 去重 / PRISMA 筛选）\n"
            "  B) 直接做简单分析（调用 ct-search 云端做选题去重探针，无需安装）"
        ),
        "note": ("ct-literature 未安装。若用户选 B，直接调用 ct-search 远端服务"
                 "（ct-search.coze.site/run, source=europepmc）获取真实命中数 + 标题，"
                 "作为 Stage 4 去重证据；该路径不需要 ct-literature。"),
    }


def main():
    ap = argparse.ArgumentParser(
        description="meta-analysis 选题门控：检测 ct-literature 安装并给出路由决策")
    ap.add_argument("--topic", required=True, help="选题检索词 / PICO 查询串")
    ap.add_argument("--year-from", type=int, default=None, help="起始年份（命令模板用）")
    ap.add_argument("--human", action="store_true", help="人类可读摘要而非纯 JSON")
    args = ap.parse_args()

    decision = gate(args.topic, args.year_from)

    if args.human:
        print("== 选题门控决策 ==")
        print("ct-literature 已安装 : %s" % decision["ct_literature_installed"])
        print("推荐路径            : %s" % decision["recommended_path"])
        if decision["ct_literature_installed"]:
            print("调用命令            : %s" % decision["ct_literature_command"])
        else:
            print("询问用户            : %s" % ("是" if decision["ask_user"] else "否"))
            print("安装提示            : %s" % decision["install_hint"])
            print("简单分析(ct-search) : %s" % decision["ct_search_command"])
        print("说明                : %s" % decision["note"])
    else:
        print(json.dumps(decision, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
