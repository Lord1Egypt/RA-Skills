#!/usr/bin/env python3
"""火一五小红书文案打分 + 优化建议。

输入：一篇笔记草稿（markdown 或 json）。
输出：6 维打分（0~100）+ 命中问题 + 修改建议。

用法
----

    # markdown 草稿（# 标题，正文，最后行带 # 话题）
    python3 polish_post.py --in draft.md

    # JSON 草稿（xhs_writer.Draft.to_dict 格式）
    python3 polish_post.py --in draft.json

    # 直接传字符串
    python3 polish_post.py --title "标题" --content "正文..." --tags "护肤,干皮护肤"

    # 输出 JSON 给后续 pipeline 用
    python3 polish_post.py --in draft.md --format json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from xhs_writer import Draft, load_draft, score_post  # noqa: E402
from xhs_profile import ProfileStore  # noqa: E402


def render_text(score) -> str:
    out = []
    out.append(f"=== 打分结果（0~100）：{score.total} ===")
    out.append("")
    grade = "🎉 可发布" if score.total >= 80 else "⚠️ 建议优化" if score.total >= 60 else "❌ 重写"
    out.append(f"等级：{grade}")
    out.append("")
    out.append("子项分（0~10）:")
    labels = {
        "title": "标题钩子",
        "first_lines": "首段抓力",
        "layout": "段落排版",
        "emoji": "emoji 节奏",
        "hashtags": "话题数量",
        "compliance": "合规性",
    }
    for k, v in score.breakdown.items():
        bar = "█" * v + "░" * (10 - v)
        out.append(f"  {labels.get(k, k):<10} {bar} {v}/10")
    out.append("")
    if score.issues:
        out.append("命中问题：")
        for x in score.issues:
            out.append(f"  • {x}")
        out.append("")
    if score.suggestions:
        out.append("修改建议：")
        for x in score.suggestions:
            out.append(f"  → {x}")
    return "\n".join(out)


def main() -> int:
    p = argparse.ArgumentParser(prog="polish_post.py", description="小红书文案打分 + 优化建议")
    p.add_argument("--in", dest="path", default="", help="草稿文件路径 (.md 或 .json)")
    p.add_argument("--title", default="", help="不传文件时直接传标题")
    p.add_argument("--content", default="", help="不传文件时直接传正文")
    p.add_argument("--tags", default="", help="不传文件时直接传话题（逗号分隔）")
    p.add_argument("--format", choices=["text", "json"], default="text")
    p.add_argument("--no-profile", action="store_true",
                   help="跳过个人规则覆盖（profile/rules.json），用纯默认规则")
    args = p.parse_args()

    if args.path:
        draft = load_draft(args.path)
    elif args.title or args.content:
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        draft = Draft(title=args.title, content=args.content, tags=tags)
    else:
        print("必须提供 --in 或 (--title + --content)", file=sys.stderr)
        return 1

    rules = None
    if not args.no_profile:
        rules = ProfileStore().load_rules()

    score = score_post(draft.title, draft.content, draft.tags, rules=rules)

    if args.format == "json":
        print(json.dumps({
            "draft": draft.to_dict(),
            "score": score.to_dict(),
        }, ensure_ascii=False, indent=2))
    else:
        print(render_text(score))

    # 退出码：60 分以下视为失败，方便 CI / pipeline 检查
    return 0 if score.total >= 60 else 2


if __name__ == "__main__":
    sys.exit(main())
