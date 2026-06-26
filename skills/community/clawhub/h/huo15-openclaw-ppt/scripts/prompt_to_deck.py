#!/usr/bin/env python3
"""
prompt_to_deck.py — v3.4 AI prompt-to-deck（媲美 Gamma 60 秒一键出 deck）

输入自然语言 prompt → Claude API 自动：
  1. 推断主题（产品发布 / 商业计划 / 内部汇报 / 技术分享 等）
  2. 选 pack（21 套审美方案中匹配最合适的）
  3. 设计 slide 结构（6-12 张，含 cover / section / big_stat / kpi / quote / cta）
  4. 写每张 slide 文案（中文为主，符合反 AI Slop 红线）
  5. 输出 JSON deck → 直接喂 create-pptx.py 出 PPT

特性：
  - Anthropic prompt caching（system prompt 18KB cached，节省 90% token）
  - 默认 Claude Sonnet 4.7（CLAUDE.md 推荐）
  - 自动反 AI Slop（不用紫渐变 / 不用 emoji 当图标 / 字体可读）
  - 流派关键词识别（"水墨"→ ink-wash，"包豪斯"→ bauhaus，等）

用法：
    # 设置 API key（一次）
    export ANTHROPIC_API_KEY='sk-...'

    # 一键出 deck
    python3 scripts/prompt_to_deck.py \\
        "做一份 8 分钟的火一五产品发布演讲，受众是企业 CEO，重点讲 OpenClaw 平台优势" \\
        --output /tmp/deck.json

    # 指定 pack（不让 AI 选）
    python3 scripts/prompt_to_deck.py "公司 2026 年终复盘" \\
        --pack apple-light --slides 8 --output /tmp/yearly.json

    # 一条龙（生成 JSON + 直接出 PPTX）
    python3 scripts/prompt_to_deck.py "..." --output /tmp/d.json --build /tmp/d.pptx

环境变量：
  ANTHROPIC_API_KEY  必填
  ANTHROPIC_MODEL    可选，默认 claude-sonnet-4-5（按 CLAUDE.md 模型选择规则）
"""

from __future__ import annotations
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# ============================================================
# System prompt — Claude 的"知识"，会被 prompt caching 缓存
# ============================================================

SLIDE_TYPES = """\
15 个 slide type（必须严格用这些 type，不要发明新 type）：

1. hero_cover     封面：{eyebrow, title, subtitle, footnote}
2. section_divider 分章：{number "01", title, subtitle}
3. big_stat       单数字大字：{caption, value "2x", unit "比 X 快", footnote, accent: true}
4. kpi_triple     3 宫格 KPI：{title, en_sub, items: [{value, label, caption}, x3]}
5. quote_card     金句：{quote, author, role}
6. content_list   要点列表：{title, items: [{label, desc}]}
7. compare_columns 对比：{title, left: {label, points: []}, right: {label, points: []}}
8. product_shot   产品图：{title, subtitle, image_brief（占位描述）, story_points: []}
9. timeline       时间线（朴素文本式）：{title, nodes: [{date, label, desc}]}
10. call_to_action 封底：{title, subtitle, cta, footnote}
11. code_block    代码：{title, language, filename, code}

【v3.5 Smart Layouts — 用 matplotlib 渲染为视觉 PNG 嵌入 slide】
12. smart_timeline  视觉时间线：{title, nodes: [{date, label}, ...]} — 带圆点编号横向时间线
13. smart_pyramid   金字塔（底→顶）：{title, layers: ["执行","战术","战略","愿景"]} — 用于战略 / OKR
14. smart_funnel    漏斗（顶→底）：{title, layers: ["访问 10万","注册 1万","付费 1千","留存 200"]} — 转化率
15. smart_steps     步骤箭头：{title, steps: ["调研","设计","开发","测试","上线"]} — 流程
"""

PACK_GUIDE = """\
21 套审美方案（pack）选择指南，根据 prompt 主题/受众/调性选最合适：

【企业/科技/产品】
- apple-keynote       Apple 发布会暗场（产品发布 / 高端科技 / 极致留白）
- apple-light         Apple.com 白场（产品介绍 / 轻量科技）
- liquid-glass        Apple 玻璃风（macOS 26 / iOS 26 / 现代科技）
- tech-neon           赛博霓虹（赛博朋克 / 科技黑客 / 游戏）
- tech-minimal        Vercel/Linear 极简（SaaS / 开发者工具 / 极客）
- jobs-dark           Jobs 暗蓝（v1.x 默认，老 Apple 风）

【内容/创作】
- xiaohongshu-creator 小红书博主（生活博主 / 美食 / 旅行）
- xiaohongshu-vintage 复古胶片（怀旧 / 文艺 / 慢生活）
- xhs-fashion         小红书时尚（莫兰迪粉灰 / 高端美妆）
- xiaohongshu         小红书品牌（v2.x 默认营销）
- xiaohongshu-portrait 小红书 9:16 竖版（移动端）

【中式/文化】
- ink-wash            中国水墨（哲学 / 书画 / 古典）
- guofeng             国风故宫（红黄青三色 / 文化 / 节庆）
- muji                原研哉极简（无印良品 / 极简哲学 / 朱红印）

【艺术/创意】
- van-gogh            梵高油画（艺术 / 创意 / 文艺）
- da-vinci            达芬奇手稿（学术 / 研究 / 复古）
- morandi             莫兰迪高级灰（静物 / 高雅 / 艺术）
- memphis             孟菲斯 80s（撞色 / 复古 / 派对）
- bauhaus             包豪斯（设计 / 教育 / 几何）
- wes-anderson        韦斯安德森（对称 / 童话 / 治愈）
- cyberpunk-vivid     赛博朋克绚彩（潮流 / 夜店 / 撞色）

选择优先级：主题匹配 > 受众调性 > 用户明确指令。如 prompt 含"水墨"/"国风"/"赛博"/"梵高"等关键词，必选对应 pack。
"""

ANTI_SLOP_RULES = """\
反 AI Slop 硬红线（生成内容必须遵守）：
- 不用 emoji 当 list 序号或重点标记（用真文字 / 数字编号）
- 文案不要"提升 / 优化 / 赋能 / 颗粒度 / 闭环"等公司腔
- 不要"首先 / 其次 / 综上所述 / 众所周知"等模板腔
- 标题宁短勿长，hero_cover.title 5-15 字最佳
- big_stat.value 必须是真数字（"2x" "192GB" "$100M" 之类，不要 "MORE"）
- quote_card 引文必须真实可考（用 prompt 里提到的人 / 公司 CEO，不要凭空捏造）
- 中文优先，专有名词保留英文
- slides 数量按 prompt 推断：5 分钟 ≈ 5-7 张，10 分钟 ≈ 8-12 张，30 分钟 ≈ 15-25 张
"""

SYSTEM_PROMPT = f"""你是火一五演示稿设计 AI，把用户自然语言 prompt 转成 PPT 的 JSON deck。

# Slide Types Schema

{SLIDE_TYPES}

# Pack 选择指南

{PACK_GUIDE}

# 反 AI Slop 规则

{ANTI_SLOP_RULES}

# 输出格式（必须严格 JSON，不带任何说明文字）

{{
  "pack": "<选中的 pack key，21 套之一>",
  "year": "2026",
  "slides": [
    {{"type": "hero_cover", "title": "...", ...}},
    ...
  ],
  "_reasoning": "<2-3 句话解释为什么选这个 pack 和这个 slide 结构>"
}}

slides 数量 6-12（默认 8），结构推荐：
1. hero_cover（必有，封面）
2. section_divider 或 content_list（介绍 agenda 或第一章）
3-N. 主体内容（kpi_triple / big_stat / compare_columns / quote_card 混搭）
最后. call_to_action（必有，封底）

如果用户指定了 pack（命令行 --pack），照他的，不要换。
"""


# ============================================================
# 调 Claude API
# ============================================================

DEFAULT_MODELS = {
    'fast':     'claude-haiku-4-5-20251001',  # 简单 prompt → 6 张快速 deck
    'balanced': 'claude-sonnet-4-5',           # 默认（成本/质量平衡）
    'deep':     'claude-opus-4-7',             # 复杂主题 / 12+ slide / 高保真
}


def is_llm_enabled() -> tuple[bool, str]:
    """v5.0：通过 llm_provider 检查 6 个 provider 是否至少一个可用"""
    try:
        from llm_provider import is_enabled
    except ImportError:
        return False, "缺 scripts/llm_provider.py"
    return is_enabled()


def call_claude(user_prompt: str, *,
                pack_override: str | None = None,
                slides: int | None = None,
                model: str | None = None,
                api_key: str | None = None,
                provider: str | None = None) -> dict:
    """v5.0：调用 LLM 生成 deck JSON。
    向后兼容名 'call_claude'，但实际通过 llm_provider 支持 6 种 provider
    （anthropic / openai / deepseek / qwen / doubao / openclaw）。"""
    from llm_provider import call_llm  # 延迟 import 避免循环

    full_user = user_prompt
    if pack_override:
        full_user += f"\n\n【强制 pack】: {pack_override}"
    if slides:
        full_user += f"\n\n【强制 slides 数】: {slides}"

    # api_key 是历史参数，新代码用 PPT_LLM_API_KEY / 各 provider 专用 env
    if api_key:
        os.environ.setdefault('ANTHROPIC_API_KEY', api_key)

    result = call_llm(
        system=SYSTEM_PROMPT,
        user=full_user,
        provider=provider,
        model=model,
        max_tokens=4096,
        cache=True,
    )

    text = result['text']
    if text.startswith('```'):
        text = text.split('```', 2)[1]
        if text.startswith('json'):
            text = text[4:]
        text = text.strip().rstrip('`').strip()

    return json.loads(text)


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description='v3.4 AI prompt-to-deck — 自然语言 → JSON deck（媲美 Gamma 60 秒生成）'
    )
    parser.add_argument('prompt', help='主题描述（中文，越具体越好）')
    parser.add_argument('--output', '-o', required=True, help='JSON deck 输出路径')
    parser.add_argument('--pack', help='强制指定 pack（不让 AI 选）')
    parser.add_argument('--slides', type=int, help='强制 slide 数（默认 AI 决定 6-12）')
    parser.add_argument('--model', default=None,
                        help='Claude model（默认 ANTHROPIC_MODEL 或 claude-sonnet-4-5）')
    parser.add_argument('--build', help='生成 JSON 后顺便调 create-pptx.py 出 .pptx')
    parser.add_argument('--print-only', action='store_true',
                        help='只打印 JSON 不写文件（dry run）')
    parser.add_argument('--dry-run', action='store_true',
                        help='不调 LLM，只确认 system prompt + 关键词推断 pack')
    args = parser.parse_args()

    model = args.model or os.environ.get('ANTHROPIC_MODEL') or DEFAULT_MODELS['balanced']

    print(f"  🤖 prompt: {args.prompt[:80]}{'...' if len(args.prompt) > 80 else ''}",
          file=sys.stderr)

    if args.dry_run:
        # 关键词推断 pack（不调 LLM）
        keyword_map = {
            '水墨': 'ink-wash', '国风': 'guofeng', '故宫': 'guofeng',
            '赛博': 'cyberpunk-vivid', '梵高': 'van-gogh',
            '达芬奇': 'da-vinci', '复古': 'xiaohongshu-vintage',
            '莫兰迪': 'morandi', '孟菲斯': 'memphis',
            '包豪斯': 'bauhaus', '韦斯': 'wes-anderson',
            '玻璃': 'liquid-glass', 'liquid glass': 'liquid-glass',
            '苹果': 'apple-keynote', 'Apple': 'apple-keynote',
            '小红书': 'xiaohongshu-creator',
            '极简': 'muji', '原研哉': 'muji',
            'Vercel': 'tech-minimal', 'Linear': 'tech-minimal',
            '霓虹': 'tech-neon', '科技': 'tech-minimal',
        }
        inferred_pack = args.pack
        if not inferred_pack:
            for kw, pack in keyword_map.items():
                if kw.lower() in args.prompt.lower():
                    inferred_pack = pack
                    break
            inferred_pack = inferred_pack or 'apple-light'  # 默认
        print(f"  📌 dry-run 关键词推断 pack: {inferred_pack}", file=sys.stderr)
        print(f"  📊 system prompt 长度: {len(SYSTEM_PROMPT)} chars", file=sys.stderr)
        print(f"  ✅ 骨架可用（实际跑需 ANTHROPIC_API_KEY）", file=sys.stderr)
        return

    enabled, reason = is_llm_enabled()
    if not enabled:
        print(f"  ✗ LLM 未启用：{reason}", file=sys.stderr)
        print(f"  💡 可先用 --dry-run 验证 skill 安装正常", file=sys.stderr)
        sys.exit(1)

    print(f"  🤖 调用 Claude {model}...", file=sys.stderr)

    try:
        deck = call_claude(
            args.prompt,
            pack_override=args.pack,
            slides=args.slides,
            model=model,
        )
    except json.JSONDecodeError as e:
        print(f"  ✗ Claude 输出不是合法 JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"  ✗ {e}", file=sys.stderr)
        sys.exit(1)

    pack = deck.get('pack', '?')
    n_slides = len(deck.get('slides', []))
    reasoning = deck.pop('_reasoning', '')
    print(f"  ✅ 生成 {n_slides} 张 slide，pack={pack}", file=sys.stderr)
    if reasoning:
        print(f"  💭 设计思路: {reasoning}", file=sys.stderr)

    if args.print_only:
        print(json.dumps(deck, ensure_ascii=False, indent=2))
        return

    Path(args.output).write_text(json.dumps(deck, ensure_ascii=False, indent=2))
    print(f"  📄 JSON: {args.output}", file=sys.stderr)

    if args.build:
        # 调 create-pptx.py / create_pptx_combined.py 出 PPTX
        script = Path(__file__).parent / 'create_pptx_combined.py'
        if not script.exists():
            script = Path(__file__).parent / 'create-pptx.py'
        cmd = [
            sys.executable, str(script),
            '--spec', args.output,
            '--pack', pack,
            '--output', args.build,
        ]
        print(f"  ⚙️  跑 {script.name} 出 PPTX...", file=sys.stderr)
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ✗ PPTX 生成失败:\n{result.stderr}", file=sys.stderr)
            sys.exit(1)
        print(f"  🎯 PPTX: {args.build}", file=sys.stderr)


if __name__ == '__main__':
    main()
