#!/usr/bin/env python3
"""
remix.py — v3.9 Remix + 多语言（媲美 Gamma Remix）

输入现有 deck JSON → 调 Claude 重写文案 → 输出新 deck，结构不变（slides 数 + type 不变），
仅文字内容按 audience / lang / tone 改写。

3 个维度：
  --audience  受众：client / internal / board / investor / team / public
  --lang      语言：zh / en / ja / es 等（默认保留原语言）
  --tone      语气：formal / casual / passionate / academic / conversational

用法：
    # 改受众（同份内容给不同人）
    python3 scripts/remix.py /path/deck.json \\
        --audience board --output /tmp/board.json

    # 译成英文 + 投资人语气
    python3 scripts/remix.py /path/deck.json \\
        --lang en --audience investor --output /tmp/en.json

    # 一条龙：remix + 出 PPTX
    python3 scripts/remix.py /path/deck.json \\
        --audience client --output /tmp/d.json --build /tmp/d.pptx
"""

from __future__ import annotations
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

AUDIENCE_GUIDE = {
    'client':    '客户视角：强调能解决他们的什么痛点 / 带来什么 ROI / 风险已规避；少自夸，多场景化',
    'internal':  '内部视角：聚焦执行细节 / 落地路径 / 资源需求 / 时间表',
    'board':     '董事会视角：极简、高密度、含数字 + 战略影响 + 风险机会矩阵',
    'investor':  '投资人视角：市场规模 / 增长曲线 / 团队 / 竞争壁垒 / 退出路径',
    'team':      '团队视角：激励 + 共识 + 角色责任清晰 + 庆祝小胜利',
    'public':    '大众视角：去专业术语 / 用类比 / 强调共情而非技术深度',
}

TONE_GUIDE = {
    'formal':         '正式书面、第三人称、避免缩写、敬语',
    'casual':         '日常口语、第一人称"我们"、可用反问、节奏轻快',
    'passionate':     '强烈情感、感叹、隐喻、富有节奏感的短句',
    'academic':       '学术严谨、引用 / 数据驱动 / 客观中立',
    'conversational': '对话式、像在跟朋友讲话、留呼吸感',
}

LANG_GUIDE = {
    'zh': '简体中文（默认）',
    'en': 'English（专业商务级，避免 AI 腔）',
    'ja': '日本語（敬語に注意、丁寧体）',
    'es': 'Español (profesional)',
    'fr': 'Français (professionnel)',
    'de': 'Deutsch (professionell)',
    'ko': '한국어 (격식)',
}


def build_remix_system_prompt(audience: str | None,
                              lang: str | None,
                              tone: str | None) -> str:
    parts = ['你是火一五演示稿 Remix AI。任务：把用户给的 JSON deck 重写为新版本。']
    parts.append('\n# 严格规则\n')
    parts.append('- 输出格式：纯 JSON（不要 markdown 包裹），结构与输入完全一致')
    parts.append('- slides 数量、每张 slide 的 type、字段 key 完全保持不变')
    parts.append('- 只改字段的 value（文字内容）')
    parts.append('- pack 字段保留原值，不要换 pack')

    parts.append('\n# 改写方向\n')
    if audience:
        guide = AUDIENCE_GUIDE.get(audience, audience)
        parts.append(f'- **受众**：{audience} → {guide}')
    if lang:
        guide = LANG_GUIDE.get(lang, lang)
        parts.append(f'- **语言**：{lang} → {guide}')
    if tone:
        guide = TONE_GUIDE.get(tone, tone)
        parts.append(f'- **语气**：{tone} → {guide}')

    parts.append('\n# 反 AI Slop（永远遵守）')
    parts.append('- 不用"提升 / 优化 / 赋能 / 颗粒度 / 闭环"等公司腔')
    parts.append('- 不用"首先 / 其次 / 综上所述 / 众所周知"模板腔')
    parts.append('- 标题宁短勿长，big_stat.value 必须真数字')

    return '\n'.join(parts)


def call_remix(deck: dict, *,
               audience: str | None = None,
               lang: str | None = None,
               tone: str | None = None,
               model: str | None = None) -> dict:
    """调 Claude API 改写 deck"""
    try:
        import anthropic
    except ImportError:
        raise RuntimeError("缺 anthropic SDK：pip install anthropic")

    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        raise RuntimeError("缺 ANTHROPIC_API_KEY")

    from prompt_to_deck import DEFAULT_MODELS
    model = model or os.environ.get('ANTHROPIC_MODEL') or DEFAULT_MODELS['balanced']

    client = anthropic.Anthropic(api_key=api_key)
    system = build_remix_system_prompt(audience, lang, tone)

    user_prompt = f"""请把以下 JSON deck 重写为新版本（按上述方向）。

输入 JSON：
```json
{json.dumps(deck, ensure_ascii=False, indent=2)}
```

输出新的完整 JSON（不要 markdown 包裹，不要任何解释）。"""

    response = client.messages.create(
        model=model,
        max_tokens=8192,
        system=[
            {"type": "text", "text": system,
             "cache_control": {"type": "ephemeral"}},
        ],
        messages=[{"role": "user", "content": user_prompt}],
    )

    text = response.content[0].text.strip()
    if text.startswith('```'):
        text = text.split('```', 2)[1]
        if text.startswith('json'):
            text = text[4:]
        text = text.strip().rstrip('`').strip()

    new_deck = json.loads(text)

    usage = response.usage
    print(f"  📊 token: input={usage.input_tokens} output={usage.output_tokens}",
          file=sys.stderr)
    if hasattr(usage, 'cache_read_input_tokens') and usage.cache_read_input_tokens:
        print(f"  💾 cache 命中: {usage.cache_read_input_tokens} tokens",
              file=sys.stderr)

    return new_deck


def main():
    parser = argparse.ArgumentParser(description='火一五 PPT v3.9 Remix + 多语言')
    parser.add_argument('input_deck', help='输入 JSON deck 路径')
    parser.add_argument('--audience', choices=list(AUDIENCE_GUIDE.keys()),
                        help='目标受众')
    parser.add_argument('--lang', choices=list(LANG_GUIDE.keys()),
                        help='目标语言（默认保留原语言）')
    parser.add_argument('--tone', choices=list(TONE_GUIDE.keys()),
                        help='语气')
    parser.add_argument('--output', '-o', required=True)
    parser.add_argument('--model', default=None)
    parser.add_argument('--build', help='顺便出 PPTX')
    args = parser.parse_args()

    if not (args.audience or args.lang or args.tone):
        print("  ✗ 至少指定 --audience / --lang / --tone 之一", file=sys.stderr)
        sys.exit(1)

    deck = json.loads(Path(args.input_deck).read_text())
    print(f"  📥 原 deck: {len(deck.get('slides', []))} slides, pack={deck.get('pack')}",
          file=sys.stderr)
    print(f"  🎨 remix: audience={args.audience} lang={args.lang} tone={args.tone}",
          file=sys.stderr)

    try:
        new_deck = call_remix(deck, audience=args.audience, lang=args.lang,
                              tone=args.tone, model=args.model)
    except Exception as e:
        print(f"  ✗ {e}", file=sys.stderr)
        sys.exit(1)

    Path(args.output).write_text(json.dumps(new_deck, ensure_ascii=False, indent=2))
    print(f"  ✅ {args.output}", file=sys.stderr)

    if args.build:
        script = Path(__file__).parent / 'create_pptx_combined.py'
        if not script.exists():
            script = Path(__file__).parent / 'create-pptx.py'
        result = subprocess.run([
            sys.executable, str(script),
            '--spec', args.output,
            '--pack', new_deck.get('pack', 'apple-light'),
            '--output', args.build,
        ], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ✗ PPTX 失败: {result.stderr}", file=sys.stderr)
            sys.exit(1)
        print(f"  🎯 PPTX: {args.build}", file=sys.stderr)


if __name__ == '__main__':
    main()
