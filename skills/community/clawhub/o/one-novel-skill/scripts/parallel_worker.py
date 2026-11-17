#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parallel_worker.py — 并行写入子Agent入口（手动触发）

用法（子Agent执行）:
  python parallel_worker.py --task ./_temp/parallel/ch001_task.json

工作流:
  1. 读取scheduler.prepare_parallel()创建的任务文件
  2. 加载spec + 宪法 + 角色状态
  3. 生成章节正文
  4. 保存结果文件供主Agent收集
"""

import json, sys, argparse
from pathlib import Path


def load_task(task_path: str) -> dict:
    with open(task_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_prompt(task: dict) -> str:
    """为LLM构建章节生成prompt"""
    ch = task.get("chapter", 0)
    spec = task.get("spec", {})
    core = spec.get("core", "")
    constitution = task.get("constitution", "")
    chars = task.get("characters", {})
    last_plot = task.get("last_plot", [])

    lines = ["[并行生成任务]"]
    lines.append(f"章节: 第{ch}章")
    if core:
        lines.append(f"核心: {core}")
    if constitution:
        lines.append(constitution)
    if chars:
        cs = "; ".join(f"{k}: {v}" for k, v in list(chars.items())[:10])
        lines.append(f"当前角色: {cs}")
    if last_plot:
        p = "; ".join(last_plot[-3:])
        lines.append(f"最近情节: {p}")
    lines.append("字数: ~2500字 | 章末: 悬念钩子 | 无markdown标记")
    return "\n".join(lines)


def save_result(task: dict, text: str, output_path: str):
    result = {
        "chapter": task.get("chapter", 0),
        "text": text,
        "word_count": len(text),
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Parallel writing worker")
    parser.add_argument("--task", required=True, help="任务JSON路径")
    args = parser.parse_args()

    task = load_task(args.task)
    op = str(Path(args.task).parent / f"ch{task['chapter']:03d}_result.json")

    prompt = build_prompt(task)
    # TODO: 调用LLM生成。当前用prompt占位，主Agent替换为真实生成。
    save_result(task, prompt, op)
    print(f"[并行] 第{task['chapter']}章任务完成 -> {op}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
