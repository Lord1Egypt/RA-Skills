#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hermes 宿主钩子示例 —— 任务开始时召回 + 任务结束时回填效果

事件：pre_llm_call（shell hook）
行为：调用 evolver-recall.mjs，把命中的修法**追加到 stdout**，由 Hermes 作为上下文带入。

接入方式：
  1. 放到宿主能执行的位置（示例：~/.hermes/hooks/evox_recall.py）并 chmod +x
  2. 在 Hermes 钩子配置里注册（示例）：
       - name: evox-recall
         command: /usr/bin/python3 <你的家目录>/.hermes/hooks/evox_recall.py
         event: pre_llm_call
  3. 若在允许清单（allowlist）机制下，改动脚本后需刷新 allowlist

对应文档：SKILL.md「宿主接入契约」第 1 步（召回）+ 第 2 步（回填）。
"""

import os
import subprocess
import sys

# ── 按你的实际安装改这三个路径 ──────────────────────────────────────────
RECALL_SCRIPT = os.environ.get("EVOX_RECALL_SCRIPT", "<技能目录>/code/evolver-recall.mjs")
HITS_DIR = os.environ.get("EVOX_HITS_DIR", "<技能目录>/experiments")
# ────────────────────────────────────────────────────────────────────────

HEADER = (
    "## EvoX inherited fixes (auto-recalled)\n\n"
    "Recalled from your validated experience store (approved entries only).\n"
    "Apply them when relevant to the current task.\n\n"
)
TIMEOUT = 15


def collect_fixes(user_message):
    """调用召回，返回修法行列表（无命中返回空列表 —— 此时**不输出任何内容**）。"""
    cmd = ["node", RECALL_SCRIPT, "--agent", "hermes"]
    # 关键：把用户这一轮的真实诉求传进去（对靶）。没有 query 时 recall 不注入——这是对的。
    if user_message:
        cmd += ["--query", str(user_message)[:2000]]
    env = dict(os.environ, EVOX_HITS_DIR=HITS_DIR)
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT, env=env)
    except Exception:
        return []  # 任何异常 → 零注入，绝不影响宿主
    fixes = []
    for line in (out.stdout or "").split("\n"):
        s = line.strip()
        if s.startswith("[#") and "|" in s:
            fixes.append(s)
    return fixes


def main():
    # Hermes shell hook 通常把本轮用户消息放在第一个参数或环境变量里，
    # 按你的宿主版本调整取值方式。
    msg = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("EVOX_QUERY", "")
    fixes = collect_fixes(msg)
    if not fixes:
        return  # 没命中 → 零输出（绝不塞无关内容）
    sys.stdout.write(HEADER + "\n".join(fixes) + "\n")
    # 提示宿主/使用者在任务结束时回填效果（第 2 步）：
    sys.stdout.write(
        "\n（任务结束时请回填：采用了 → `--register-hit --gene <asset_id> --note \"...\"`；"
        "没起作用 → `--negate <N> --note \"...\"`）\n"
    )


if __name__ == "__main__":
    main()
