#!/usr/bin/env python3
"""
slide_polish.py — v4.3 文本辅写（对标 ChatPPT 10+ 编辑模式）

10 种 polish 模式（按用途分类）：

【语言改写】
  refine    润色（保持原意，改通顺）
  shorten   精简（去冗余，砍 30-50% 字数）
  expand    扩写（加细节，补论据）
  rewrite   完全重写（同主题不同表达）

【加内容】
  add-data  加数据（加具体数字 / 百分比 / 案例数据）
  add-quote 加引言（加名人金句 / 行业大咖话）
  add-joke  加冷笑话（加一个轻松点的钩子）

【修辞强化】
  emphasize 加强 / 重音（用排比 / 反问 / 感叹）
  metaphor  加比喻（用自然意象 / 类比）
  elevate   升华（从战术升到战略 / 从产品升到使命）

用法：
    # 改写一张 slide
    python3 scripts/slide_polish.py /tmp/d.json --slide 3 --mode refine \\
        --output /tmp/d-polished.json

    # 改写所有 slide 的标题
    python3 scripts/slide_polish.py /tmp/d.json --field title --mode shorten \\
        --output /tmp/d-shorter-titles.json

    # 一条龙：改 + 重新出 PPTX
    python3 scripts/slide_polish.py /tmp/d.json --slide 3 --mode add-data \\
        --output /tmp/d2.json --build /tmp/d2.pptx
"""

from __future__ import annotations
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


MODES = {
    'refine': '润色：保持原意 + 主旨 + 字数大致不变，只把表达改得更通顺、有节奏',
    'shorten': '精简：砍 30-50% 字数，保留核心信息，去冗余 / 去重复 / 砍废话',
    'expand': '扩写：加 1-2 倍字数，补充细节、数据、对比、案例，保持原观点',
    'rewrite': '完全重写：同主题但完全不同的表达方式（换角度 / 换叙事顺序）',
    'add-data': '加数据：插入具体数字、百分比、案例数据来强化论据',
    'add-quote': '加引言：插入一句名人 / 行业大咖的金句强化论点',
    'add-joke': '加冷笑话：在严肃内容里加一个轻松的钩子（不要尬，要意外感）',
    'emphasize': '加强语气：用排比 / 反问 / 短句节奏让文字更有冲击力',
    'metaphor': '加比喻：用自然意象 / 日常类比把抽象概念变具象',
    'elevate': '升华：从战术升到战略，从产品升到使命，从功能升到价值',
}


def call_claude_polish(text: str, mode: str, *,
                       context: str = '',
                       model: str | None = None) -> str:
    """调 Claude 按 mode 改写单段文字"""
    try:
        import anthropic
    except ImportError:
        raise RuntimeError("pip install anthropic")
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        raise RuntimeError("缺 ANTHROPIC_API_KEY")
    from prompt_to_deck import DEFAULT_MODELS
    model = model or os.environ.get('ANTHROPIC_MODEL') or DEFAULT_MODELS['balanced']

    guide = MODES.get(mode, mode)
    system = f"""你是火一五 PPT 文本辅写 AI。
任务：按 {mode} 模式改写用户给的文字。

模式说明：{guide}

【严格规则】
- 只输出改后的文字，不要解释、不要 markdown 包裹
- 中文为主，保留英文专有名词
- 反 AI Slop：不用"提升 / 优化 / 赋能 / 颗粒度 / 闭环"
- 不用"首先 / 其次 / 综上所述"模板腔
- 不要 emoji 当 list 标记"""

    user = f"""原文：
{text}

{f"上下文：{context}" if context else ""}

输出改后的版本（直接给文字，不要其他）："""

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        system=[{"type": "text", "text": system,
                 "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user}],
    )
    return response.content[0].text.strip().strip('`').strip()


def polish_slide(slide: dict, mode: str, target_field: str | None = None,
                 model: str | None = None) -> dict:
    """改一张 slide 的某字段（或所有字段）"""
    new_slide = dict(slide)

    # 哪些 key 是文字内容（不是 type / number 等元字段）
    TEXT_FIELDS = {'title', 'subtitle', 'eyebrow', 'footnote', 'caption',
                   'value', 'unit', 'quote', 'author', 'role', 'cta',
                   'label', 'desc', 'en_sub'}

    fields_to_change = ([target_field] if target_field
                        else [k for k in new_slide if k in TEXT_FIELDS])

    for field in fields_to_change:
        if field not in new_slide:
            continue
        original = new_slide[field]
        if not isinstance(original, str) or not original.strip():
            continue
        ctx = f"slide type={slide.get('type', '?')}, field={field}"
        try:
            new_text = call_claude_polish(original, mode, context=ctx, model=model)
            print(f"    {field}: {original[:40]!r} → {new_text[:40]!r}",
                  file=sys.stderr)
            new_slide[field] = new_text
        except Exception as e:
            print(f"    {field}: 改写失败 {e}", file=sys.stderr)

    return new_slide


def main():
    parser = argparse.ArgumentParser(description='火一五 PPT v4.3 文本辅写')
    # --list-modes 走快路径（不需 deck/mode/output）
    if '--list-modes' in sys.argv:
        print("\n  10 种 polish 模式：")
        for m, desc in MODES.items():
            print(f"  {m:12} {desc}")
        return

    parser.add_argument('deck', help='deck JSON 路径')
    parser.add_argument('--mode', required=True, choices=list(MODES.keys()))
    parser.add_argument('--slide', type=int,
                        help='只改第 N 张 slide（1-based），不指定则改全部')
    parser.add_argument('--field', help='只改某个字段（title / subtitle / ...）')
    parser.add_argument('--output', '-o', required=True)
    parser.add_argument('--model', default=None)
    parser.add_argument('--build', help='顺便出 PPTX')
    parser.add_argument('--list-modes', action='store_true')
    args = parser.parse_args()

    deck = json.loads(Path(args.deck).read_text())
    slides = deck.get('slides', [])

    print(f"  📥 deck: {len(slides)} slides, mode={args.mode}",
          file=sys.stderr)

    target_indices = ([args.slide - 1] if args.slide
                      else list(range(len(slides))))

    for idx in target_indices:
        if idx < 0 or idx >= len(slides):
            continue
        print(f"  ✏️  slide {idx + 1} ({slides[idx].get('type')})",
              file=sys.stderr)
        slides[idx] = polish_slide(slides[idx], args.mode,
                                   target_field=args.field,
                                   model=args.model)

    deck['slides'] = slides
    Path(args.output).write_text(
        json.dumps(deck, ensure_ascii=False, indent=2))
    print(f"  ✅ {args.output}", file=sys.stderr)

    if args.build:
        scripts = Path(__file__).parent
        script = (scripts / 'create_pptx_combined.py' if (scripts / 'create_pptx_combined.py').exists()
                  else scripts / 'create-pptx.py')
        result = subprocess.run([
            sys.executable, str(script),
            '--spec', args.output,
            '--pack', deck.get('pack', 'apple-light'),
            '--output', args.build,
        ], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ✗ PPTX 失败: {result.stderr}", file=sys.stderr)
            sys.exit(1)
        print(f"  🎯 PPTX: {args.build}", file=sys.stderr)


if __name__ == '__main__':
    main()
