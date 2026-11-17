#!/usr/bin/env python3
"""Generate a human-review Markdown view from JSONL primary data.

Usage:
  python generate_markdown.py knowledge_assets.jsonl knowledge_assets.md
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


def load_items(path: Path) -> list[dict]:
    items = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSONL 第 {line_no} 行无法解析: {exc}") from exc
        items.append(item)
    return items


def text(value) -> str:
    if isinstance(value, list):
        return "、".join(text(v) for v in value)
    if isinstance(value, dict):
        return "; ".join(f"{k}: {text(v)}" for k, v in value.items())
    return str(value if value is not None else "")


def generate(items: list[dict]) -> str:
    modules = Counter(item.get("module", "未分类") for item in items)
    statuses = Counter(item.get("status", "未标注") for item in items)
    lines = [
        "# 知识资产审核视图",
        "",
        "> 本文件由 JSONL 主数据自动生成。请勿直接把本文件作为独立主数据修改或发布。",
        "",
        "## 1. 批次概览",
        "",
        f"- 条目数：{len(items)}",
        f"- 模块数：{len(modules)}",
        f"- 状态分布：{text(dict(statuses))}",
        "- 主数据：`knowledge_assets.jsonl`",
        "- 生成方式：由同一份结构化主数据自动生成",
        "",
        "## 2. 模块目录",
        "",
        "| 模块 | 条目数 |",
        "|---|---:|",
    ]
    lines.extend(f"| {module} | {count} |" for module, count in modules.most_common())
    lines.extend(["", "## 3. 知识条目", ""])

    for item in items:
        tags = item.get("tags", {})
        lines.extend([
            f"### {item.get('id', '未命名')}｜{item.get('question', '')}",
            "",
            f"- **模块**：{item.get('module', '')}",
            f"- **状态**：`{item.get('status', '')}`",
            f"- **版本**：`{item.get('version', '')}`",
            f"- **用户意图**：{item.get('intent', '')}",
            f"- **检索文本**：{item.get('retrieval_text', '')}",
            "",
            "**回答文本**",
            "",
            text(item.get("answer_text", "")),
            "",
            "**标签与边界**",
            "",
            f"- 阶段：{tags.get('stage', '')}",
            f"- 内容类型：{tags.get('content_type', '')}",
            f"- 症状：{tags.get('symptom', '')}",
            f"- 动作：{text(tags.get('action', []))}",
            f"- 适用范围：{tags.get('scope', '')}",
            f"- 同义说法：{text(item.get('aliases', []))}",
            f"- 不能外推：{item.get('negative_scope', '')}",
            "",
            "**来源与关系**",
            "",
            f"- 来源：{item.get('evidence', '')}",
            f"- 来源位置：{text(item.get('source_span', {}))}",
            f"- 相关条目：{text(item.get('related_ids', []))}",
            f"- 冲突条目：{text(item.get('conflict_ids', []))}",
            "",
            "---",
            "",
        ])

    lines.extend([
        "## 4. 冲突与待审核",
        "",
        "以下状态不得在审核视图中隐藏：`conflict`、`pending_review`、`ask_teacher`。",
        "",
    ])
    flagged = [item for item in items if item.get("status") in {"conflict", "pending_review", "ask_teacher"}]
    if flagged:
        lines.extend(f"- `{item.get('id')}`：{item.get('status')}｜{item.get('question', '')}" for item in flagged)
    else:
        lines.append("- 当前没有标记为冲突或待审核的条目。")
    lines.extend(["", "## 5. 人工审核记录", "", "- 发现问题时记录条目 ID、问题类型和修改建议。", "- 修改必须回写 JSONL 主数据，再重新生成本 Markdown。", ""])
    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) != 3:
        print("用法: python generate_markdown.py <input.jsonl> <output.md>", file=sys.stderr)
        return 2
    source, target = map(Path, sys.argv[1:])
    items = load_items(source)
    target.write_text(generate(items), encoding="utf-8")
    print(f"generated {target} from {source}: {len(items)} items")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
