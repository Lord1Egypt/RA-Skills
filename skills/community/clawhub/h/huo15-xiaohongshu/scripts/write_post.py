#!/usr/bin/env python3
"""火一五小红书文案生成器 — 给 Claude / 用户一份"骨架草稿"。

工作模式
========
本脚本不调大模型，只输出**骨架 + 候选标题 + 话题建议**；
真正的内容填充由调用它的 LLM（或你本人）完成。

这样设计的好处：
1. 离线可跑、零依赖；
2. Claude 拿到骨架后可以一次性看清"标题公式 + 段落结构 + 强占位"，
   产出会更结构化、不容易跑偏；
3. 不会假装替你"写完"再让你改 — 反而拖慢。

用法
====

    # 1) 列出标题候选（多公式 × 多个）
    python3 write_post.py titles --topic "干皮护肤" --persona "30+ 干皮女生" \\
        --payoff "稳油不闷痘" --formulas T1,T3,T5 --n 2

    # 2) 渲染正文骨架
    python3 write_post.py skeleton --code S1

    # 3) 一键产出 markdown 草稿（标题 + 骨架 + 话题占位）
    python3 write_post.py draft --topic "干皮护肤" --persona "30+" \\
        --payoff "稳油不闷痘" --formula T2 --skeleton S1 \\
        --tags "护肤,干皮护肤,30岁护肤" --out draft.md
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from xhs_writer import (  # noqa: E402
    Draft,
    generate_titles,
    get_skeleton,
    make_draft,
    render_skeleton,
    save_draft,
)


def cmd_titles(args: argparse.Namespace) -> int:
    formulas = [f.strip() for f in args.formulas.split(",")] if args.formulas else None
    titles = generate_titles(
        args.topic,
        persona=args.persona,
        payoff=args.payoff,
        formulas=formulas,
        n_each=args.n,
    )
    if args.format == "json":
        print(json.dumps(titles, ensure_ascii=False, indent=2))
    else:
        for t in titles:
            print(f"[{t['formula']}] {t['title']}")
    return 0


def cmd_skeleton(args: argparse.Namespace) -> int:
    fields = {}
    if args.fields:
        try:
            fields = json.loads(args.fields)
        except json.JSONDecodeError as e:
            print(f"--fields 不是合法 JSON: {e}", file=sys.stderr)
            return 1
    if fields:
        print(render_skeleton(args.code, fields))
    else:
        for line in get_skeleton(args.code):
            print(line)
    return 0


def cmd_draft(args: argparse.Namespace) -> int:
    tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
    draft = make_draft(
        args.topic,
        persona=args.persona,
        payoff=args.payoff,
        formula=args.formula,
        skeleton=args.skeleton,
        tags=tags,
    )
    if args.cover_hint:
        draft.cover_hint = args.cover_hint
    if args.image_hints:
        draft.image_hints = [h.strip() for h in args.image_hints.split("|") if h.strip()]

    text = draft.to_markdown()
    if args.out:
        save_draft(draft, args.out)
        print(f"✓ 草稿已保存到 {args.out}", file=sys.stderr)
    else:
        print(text)
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    """列出所有可用的标题公式 / 正文骨架代号。"""
    print("== 标题公式 ==")
    print("  T1 数字对比      T2 痛点共情     T3 反差冲突     T4 悬念钩子")
    print("  T5 身份代入      T6 福利免费     T7 时间节点     T8 提问诱发")
    print("  T9 极端结果      T10 步骤指南    T11 故事开场")
    print()
    print("== 正文骨架 ==")
    print("  S1 钩子-痛点-方案-金句       S2 故事-感悟-行动")
    print("  S3 测评-对比-结论            S4 清单/列表")
    print("  S5 保姆级教程                S6 观点/反共识")
    print("  S7 日记/Vlog")
    print()
    print("详见 data/title_templates.md 和 data/content_structures.md")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="write_post.py", description="火一五小红书文案生成（骨架版）")
    sub = p.add_subparsers(dest="cmd", required=True)

    pt = sub.add_parser("titles", help="生成标题候选")
    pt.add_argument("--topic", required=True, help="主题关键词，如：干皮护肤")
    pt.add_argument("--persona", default="", help="目标受众，如：30+ 干皮女生")
    pt.add_argument("--payoff", default="", help="利益点 / 结果，如：稳油不闷痘")
    pt.add_argument("--formulas", default="", help="公式代号，逗号分隔；空 = 全部 (T1~T11)")
    pt.add_argument("--n", type=int, default=2, help="每种公式生成几条")
    pt.add_argument("--format", choices=["text", "json"], default="text")
    pt.set_defaults(func=cmd_titles)

    ps = sub.add_parser("skeleton", help="打印正文骨架")
    ps.add_argument("--code", required=True, help="骨架代号 S1~S7")
    ps.add_argument("--fields", default="", help="JSON: {\"hook\":\"...\"} 用于填充占位")
    ps.set_defaults(func=cmd_skeleton)

    pd = sub.add_parser("draft", help="一键生成 markdown 草稿")
    pd.add_argument("--topic", required=True)
    pd.add_argument("--persona", default="")
    pd.add_argument("--payoff", default="")
    pd.add_argument("--formula", default="T2", help="标题公式 T1~T11")
    pd.add_argument("--skeleton", default="S1", help="正文骨架 S1~S7")
    pd.add_argument("--tags", default="", help="话题列表，逗号分隔，不带 #")
    pd.add_argument("--cover-hint", default="", help="封面图说明")
    pd.add_argument("--image-hints", default="", help="多张配图说明，| 分隔")
    pd.add_argument("--out", default="", help="输出 .md 或 .json；不填打印到 stdout")
    pd.set_defaults(func=cmd_draft)

    pl = sub.add_parser("list", help="列出所有公式 / 骨架代号")
    pl.set_defaults(func=cmd_list)

    return p


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
