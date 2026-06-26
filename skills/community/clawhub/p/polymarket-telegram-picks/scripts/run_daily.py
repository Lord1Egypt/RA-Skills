#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日一键执行：拉取 Polymarket 赔率 → 可选 AI 分析 → 推送到 Telegram。
适用于系统 crontab 或单独执行，不经过 OpenClaw 会话。
若需「AI 分析」，请使用 OpenClaw 定时任务触发技能，由助手执行 fetch → 分析 → send_telegram。
"""
import os
import subprocess
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
FETCH_SCRIPT = SKILL_ROOT / "scripts" / "fetch_polymarket.py"
SEND_SCRIPT = SKILL_ROOT / "scripts" / "send_telegram.py"


def main():
    if not FETCH_SCRIPT.is_file():
        print(f"未找到脚本: {FETCH_SCRIPT}", file=sys.stderr)
        sys.exit(1)
    result = subprocess.run(
        [sys.executable, str(FETCH_SCRIPT)],
        capture_output=True,
        text=True,
        cwd=str(SKILL_ROOT),
        timeout=60,
    )
    summary = result.stdout or "(无输出)"
    if result.returncode != 0:
        summary = (result.stderr or result.stdout or "拉取失败") + "\n\n" + summary

    # 若不配置 LLM，则只把原始摘要推送到 Telegram；用户可改为在 OpenClaw 中由 AI 分析后再推送
    if os.environ.get("POLYMARKET_DAILY_RAW_ONLY") == "1" or not os.environ.get("OPENAI_API_KEY"):
        message = f"【Polymarket 每日摘要】\n\n{summary}"
    else:
        # 可选：在此调用本地/远程 LLM 对 summary 做简短分析，再赋值给 message
        message = f"【Polymarket 每日摘要】\n\n{summary}"

    if not SEND_SCRIPT.is_file():
        print("未找到 send_telegram.py，仅输出摘要：\n", summary)
        return
    send = subprocess.run(
        [sys.executable, str(SEND_SCRIPT), message],
        cwd=str(SKILL_ROOT),
        timeout=15,
    )
    sys.exit(send.returncode)


if __name__ == "__main__":
    main()
