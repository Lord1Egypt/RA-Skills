#!/usr/bin/env python3
"""火一五小红书"封面图建议" — 给文字 + 版式 + 配色建议，不直接出图。

为什么不出图
============
图像生成是 Canva / 创客贴 / 美图设计室的赛道。CLI 不是合适载体。
我们做的是给你一份**封面 brief**：
- 主标题文字（≤ 15 字）
- 副标题文字（≤ 25 字，可选）
- 推荐版式（满版字号 / 顶部留白 / 底部色块 / 三段式）
- 配色思路（与赛道情绪挂钩）
- 字体氛围（手写 / 黑体 / 宋体 / 圆体）
- 元素建议（一个 emoji / 一句金句 / 一张产品图）

工作流
======
1. 读笔记草稿（标题 + 首段）
2. 规则模式给 3 套封面 brief（保守 / 平衡 / 大胆）
3. 可选 LLM 增强：根据风格档案 + Allen 范本范，给个性化建议
4. 输出可以直接拿到 Canva / 美图秀秀 / Procreate 落地

用法
----

    python3 cover_brief.py --in draft.md
    python3 cover_brief.py --in draft.md --niche "护肤"
    python3 cover_brief.py --in draft.md --format md --out cover.md
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).parent))

from xhs_writer import load_draft  # noqa: E402

try:
    import llm_helper
except ImportError:
    llm_helper = None  # type: ignore


# ---------- 模板库 ----------


_LAYOUT_PRESETS = {
    "满版大字（标题党）": {
        "structure": "整张图就是字 — 60% 标题 + 20% 副标 + 20% 留白",
        "fits": ["干货", "教程", "金句"],
        "emoji_count": "0~1 个，作为视觉锚点",
        "font": "粗黑体 + 重磅字号（标题 80pt+）",
    },
    "顶部留白 + 底部色块": {
        "structure": "上半留白配场景图 / 纯色，下半色块压字",
        "fits": ["生活", "情绪", "Vlog"],
        "emoji_count": "0~2 个",
        "font": "宋体 / 圆体（柔和），标题 50~60pt",
    },
    "三段式（标题/插图/副标）": {
        "structure": "上 30% 标题 + 中 50% 插图/产品 + 下 20% 副标",
        "fits": ["测评", "好物", "对比"],
        "emoji_count": "1~2 个 + 价格箭头",
        "font": "黑体 + 数字加粗",
    },
    "手写信封（私聊感）": {
        "structure": "整张图像一封信 / 笔记，标题手写感，配 1 张细节图",
        "fits": ["情感", "成长", "心理"],
        "emoji_count": "0",
        "font": "手写体（站酷快乐体 / 优设标题黑）",
    },
    "对比左右": {
        "structure": "左 ❌ 错的方法 / 右 ✅ 对的方法，强对比色块",
        "fits": ["纠错", "避雷", "误区"],
        "emoji_count": "2 个（❌ 和 ✅）",
        "font": "粗黑体",
    },
}


_PALETTE_BY_NICHE = {
    "护肤": ("奶油白 + 莫兰迪粉", "温柔 / 治愈 / 自然"),
    "美妆": ("珍珠白 + 大地色", "高级 / 沉静"),
    "穿搭": ("米色 + 卡其", "通勤 / 都市"),
    "美食": ("奶白 + 日落橙", "诱人 / 烟火气"),
    "旅行": ("海蓝 + 沙黄", "辽阔 / 自由"),
    "健身": ("运动黑 + 荧光绿/橙", "活力 / 燃"),
    "数码": ("深蓝 + 银灰", "理性 / 专业"),
    "育儿": ("奶油黄 + 嫩绿", "温柔 / 萌"),
    "家居": ("米白 + 原木色", "温馨 / 治愈"),
    "学习": ("纸白 + 墨黑", "极简 / 专注"),
    "职场": ("深灰 + 香槟金", "专业 / 利落"),
    "情感": ("夜深蓝 + 月光黄", "温柔 / 细腻"),
    "副业": ("白底 + 香槟金", "积极 / 有质感"),
}


_FONT_VIBES = {
    "黑体": "决心 / 专业 / 干货感",
    "宋体": "文艺 / 沉静 / 文化感",
    "圆体": "亲切 / 治愈 / 朋友感",
    "手写体": "私人 / 温度 / 不完美感",
    "粗体艺术字": "情绪 / 反差 / 喊话感",
}


# ---------- 数据结构 ----------


@dataclass
class CoverBrief:
    main_title: str
    sub_title: str = ""
    layout: str = ""
    layout_structure: str = ""
    palette: str = ""
    palette_mood: str = ""
    font_vibe: str = ""
    emoji_hint: str = ""
    elements: List[str] = field(default_factory=list)
    why: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _shorten(text: str, n: int) -> str:
    return text[:n].rstrip("，,。！？!?")


def build_briefs_rules(title: str, first_line: str, niche: str = "") -> List[CoverBrief]:
    """规则模式：根据标题特征 + 赛道，给 3 套版式建议。"""
    palette, mood = _PALETTE_BY_NICHE.get(niche, ("奶油白 + 莫兰迪粉", "温柔 / 治愈"))

    # 主标题：从原标题里挤出 ≤ 15 字
    main = _shorten(title, 14) or "（待填）"
    # 副标：从首段挑一句关键短语
    sub = _shorten(first_line, 22) if first_line else ""

    briefs: List[CoverBrief] = []

    # 套餐 1：保守（顶部留白 + 底部色块）
    briefs.append(CoverBrief(
        main_title=main,
        sub_title=sub,
        layout="顶部留白 + 底部色块",
        layout_structure=_LAYOUT_PRESETS["顶部留白 + 底部色块"]["structure"],
        palette=palette,
        palette_mood=mood,
        font_vibe="圆体（亲切）",
        emoji_hint="底部 1~2 个 emoji 当锚点（✨ / 🌷 / 📌）",
        elements=["底部色块叠 1 张产品/场景细节图", "标题字与色块同色系强对比"],
        why="保守稳妥，适合大部分账号常态发布",
    ))

    # 套餐 2：平衡（满版大字）
    briefs.append(CoverBrief(
        main_title=main,
        sub_title=_shorten(sub or "（去掉副标）", 16),
        layout="满版大字",
        layout_structure=_LAYOUT_PRESETS["满版大字（标题党）"]["structure"],
        palette=palette,
        palette_mood=mood,
        font_vibe="粗黑体（决心 / 干货感）",
        emoji_hint="0~1 个，作为视觉锚点",
        elements=["标题占 60% 画面", "副标缩进对齐", "右下角小图标"],
        why="点击率最高，适合发布前 3 小时主推",
    ))

    # 套餐 3：大胆（手写信封 / 对比）
    is_correction = any(w in title for w in ["误区", "避雷", "踩雷", "我以为", "结果"])
    if is_correction:
        briefs.append(CoverBrief(
            main_title=main,
            sub_title=sub,
            layout="对比左右",
            layout_structure=_LAYOUT_PRESETS["对比左右"]["structure"],
            palette="灰白 + 对比色（红/绿）",
            palette_mood="冲突 / 反差",
            font_vibe="粗黑体",
            emoji_hint="❌ ✅ 大字号当地标",
            elements=["左侧灰底❌写法", "右侧亮底✅写法", "中间细分割线"],
            why="纠错型内容点击率高",
        ))
    else:
        briefs.append(CoverBrief(
            main_title=main,
            sub_title=sub,
            layout="手写信封（私聊感）",
            layout_structure=_LAYOUT_PRESETS["手写信封（私聊感）"]["structure"],
            palette=palette,
            palette_mood=f"{mood} / 私人",
            font_vibe="手写体（温度 / 不完美感）",
            emoji_hint="0 个 — 让手写本身做装饰",
            elements=["上方一张细节图（草地/咖啡/桌面）", "下方手写感标题", "签名感印章"],
            why="情感共鸣型内容更适合",
        ))

    return briefs


# ---------- LLM 增强 ----------


def enhance_with_llm(briefs: List[CoverBrief], title: str,
                     first_line: str, niche: str = "") -> List[CoverBrief]:
    if not llm_helper or not llm_helper.is_enabled():
        return briefs
    prompt = (
        f"以下是一篇小红书笔记的标题和首段，请基于 Allen 文案体系（缓存里）"
        f"给 3 套封面方案的'金句副标'（≤ 22 字）和'封面 emoji 1 个'。"
        f"金句要走范本范不走攻略范 — 不教读者，是引读者的钩子。\n\n"
        f"标题：{title}\n首段：{first_line}\n赛道：{niche}\n\n"
        f"返回 JSON 数组：[{{\"sub_title\": \"...\", \"emoji\": \"...\"}}, ...]，正好 3 个。"
    )
    data = llm_helper.call_json(
        prompt, tier="fast",
        cached_assets=["allen_method"], max_tokens=400,
    )
    if not isinstance(data, list):
        return briefs
    for i, item in enumerate(data[:len(briefs)]):
        if not isinstance(item, dict):
            continue
        if item.get("sub_title"):
            briefs[i].sub_title = item["sub_title"]
        if item.get("emoji"):
            briefs[i].emoji_hint = f"主 emoji：{item['emoji']}"
    return briefs


# ---------- 渲染 ----------


def render_text(briefs: List[CoverBrief]) -> str:
    parts = ["📐 小红书封面建议（3 套方案，去 Canva / 美图秀秀 / Procreate 落地）", ""]
    for i, b in enumerate(briefs, 1):
        parts.append("━" * 60)
        parts.append(f"方案 {i}：{b.layout}")
        parts.append("━" * 60)
        parts.append(f"  主标题：{b.main_title}")
        if b.sub_title:
            parts.append(f"  副标题：{b.sub_title}")
        parts.append(f"  版式  ：{b.layout_structure}")
        parts.append(f"  配色  ：{b.palette}（{b.palette_mood}）")
        parts.append(f"  字体  ：{b.font_vibe}")
        parts.append(f"  emoji ：{b.emoji_hint}")
        if b.elements:
            parts.append(f"  元素  ：")
            for e in b.elements:
                parts.append(f"           - {e}")
        parts.append(f"  适合  ：{b.why}")
        parts.append("")

    parts.append("─" * 60)
    parts.append("Allen 提醒：")
    parts.append("  • 封面字 ≤ 15 字，副标 ≤ 25 字（手机扫读边界）")
    parts.append("  • 首图必须能独立讲完一件事 — 它是钩子的钩子")
    parts.append("  • 别堆 emoji；要么不放，要么 1 个当锚点")
    return "\n".join(parts)


def render_md(briefs: List[CoverBrief]) -> str:
    parts = ["# 封面建议（3 套）\n"]
    for i, b in enumerate(briefs, 1):
        parts.append(f"## 方案 {i}：{b.layout}\n")
        parts.append(f"- **主标题**: {b.main_title}")
        if b.sub_title:
            parts.append(f"- **副标题**: {b.sub_title}")
        parts.append(f"- **版式**: {b.layout_structure}")
        parts.append(f"- **配色**: {b.palette}（{b.palette_mood}）")
        parts.append(f"- **字体**: {b.font_vibe}")
        parts.append(f"- **emoji**: {b.emoji_hint}")
        for e in b.elements:
            parts.append(f"  - {e}")
        parts.append(f"- **适合**: {b.why}")
        parts.append("")
    return "\n".join(parts) + "\n"


# ---------- 3:4 HTML 封面（v3.3 加） ----------


_HTML_TEMPLATES = {
    "minimal": {
        "bg": "#FAF8F5",
        "text": "#1A1A1A",
        "accent": "#D4A574",
        "font_family": "'PingFang SC', 'Hiragino Sans GB', system-ui, sans-serif",
    },
    "tech": {
        "bg": "linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)",
        "text": "#FFFFFF",
        "accent": "#FFD700",
        "font_family": "system-ui, -apple-system, sans-serif",
    },
    "warm": {
        "bg": "linear-gradient(135deg, #FFE5D9 0%, #FFC8A2 100%)",
        "text": "#3D2C1E",
        "accent": "#C2410C",
        "font_family": "'PingFang SC', system-ui, serif",
    },
    "dark": {
        "bg": "#0F0F12",
        "text": "#F5F5F5",
        "accent": "#FF6B6B",
        "font_family": "system-ui, sans-serif",
    },
    "soft": {
        "bg": "linear-gradient(180deg, #F0F4F8 0%, #D9E2EC 100%)",
        "text": "#243B55",
        "accent": "#6B7B91",
        "font_family": "'PingFang SC', system-ui, serif",
    },
}


def _render_html(brief: CoverBrief, style_key: str = "minimal",
                 highlight: str = "") -> str:
    s = _HTML_TEMPLATES.get(style_key, _HTML_TEMPLATES["minimal"])
    main = brief.main_title.replace("<", "&lt;").replace(">", "&gt;")
    sub = (brief.sub_title or "").replace("<", "&lt;").replace(">", "&gt;")
    if highlight and highlight in main:
        main = main.replace(
            highlight,
            f'<span class="hl">{highlight}</span>',
        )

    css = f"""
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{
    width: 100%;
    height: 100%;
    background: {s['bg']};
    font-family: {s['font_family']};
    color: {s['text']};
}}
.cover {{
    width: 100vw;
    height: 100vh;
    aspect-ratio: 3/4;
    max-width: 100vw;
    max-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 8vh 8vw;
    text-align: center;
}}
.main {{
    font-size: clamp(28px, 6.5vw, 64px);
    font-weight: 800;
    line-height: 1.3;
    letter-spacing: 0.02em;
    margin-bottom: 4vh;
    word-break: keep-all;
}}
.hl {{
    background: {s['accent']};
    color: #FFFFFF;
    padding: 0 0.3em;
    border-radius: 6px;
    display: inline-block;
}}
.sub {{
    font-size: clamp(14px, 2.5vw, 22px);
    line-height: 1.6;
    color: {s['accent']};
    max-width: 80%;
    opacity: 0.9;
}}
.foot {{
    position: absolute;
    bottom: 4vh;
    font-size: clamp(10px, 1.5vw, 14px);
    opacity: 0.5;
}}
@media (max-aspect-ratio: 3/4) {{
    .cover {{ height: calc(100vw * 4 / 3); }}
}}
"""
    foot_text = f"{brief.layout} · {brief.palette_mood}"
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{brief.main_title}</title>
<style>{css}</style>
</head>
<body>
<div class="cover">
    <div class="main">{main}</div>
    <div class="sub">{sub}</div>
    <div class="foot">{foot_text}</div>
</div>
</body>
</html>"""


def _style_for_brief(brief: CoverBrief) -> str:
    """根据 brief 的版式 / 配色推荐 HTML 模板键。"""
    layout = (brief.layout or "").lower()
    palette = (brief.palette or "").lower()
    if "对比" in layout:
        return "tech"
    if "手写" in layout or "信封" in layout:
        return "soft"
    if "夜" in palette or "深蓝" in palette or "黑" in palette:
        return "dark"
    if "暖" in palette or "橙" in palette or "黄" in palette or "香槟" in palette:
        return "warm"
    return "minimal"


def render_html_covers(briefs: List[CoverBrief], out_dir: Path,
                       highlight: str = "") -> List[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: List[Path] = []
    for i, b in enumerate(briefs, 1):
        style = _style_for_brief(b)
        html = _render_html(b, style, highlight)
        path = out_dir / f"cover-{i}-{style}.html"
        path.write_text(html, encoding="utf-8")
        paths.append(path)
    return paths


# ---------- 主流程 ----------


def main() -> int:
    p = argparse.ArgumentParser(prog="cover_brief.py", description="封面文案 + 版式建议")
    p.add_argument("--in", dest="path", required=True)
    p.add_argument("--niche", default="", help="赛道，如 护肤/美妆/穿搭/...，影响配色")
    p.add_argument("--format", choices=["text", "md", "json"], default="text")
    p.add_argument("--out", default="")
    p.add_argument("--no-llm", action="store_true")
    p.add_argument("--html", action="store_true",
                   help="生成 3:4 HTML 封面（F12 手机模式直接截图）")
    p.add_argument("--html-dir", default="",
                   help="HTML 输出目录（默认 ~/.xiaohongshu/covers/<draft-id>/）")
    p.add_argument("--highlight", default="",
                   help="HTML 模式下要高亮的关键词")
    args = p.parse_args()

    draft = load_draft(args.path)
    first_line = ""
    for ln in draft.content.splitlines():
        if ln.strip():
            first_line = ln.strip()
            break

    niche = args.niche
    if not niche:
        from xhs_profile import ProfileStore
        try:
            niche = ProfileStore().load_style().niche
        except Exception:
            pass

    briefs = build_briefs_rules(draft.title, first_line, niche)
    if not args.no_llm:
        briefs = enhance_with_llm(briefs, draft.title, first_line, niche)

    if args.format == "json":
        out_text = json.dumps([b.to_dict() for b in briefs], ensure_ascii=False, indent=2)
    elif args.format == "md":
        out_text = render_md(briefs)
    else:
        out_text = render_text(briefs)

    if args.out:
        Path(args.out).write_text(out_text, encoding="utf-8")
        print(f"✓ 已写入 {args.out}", file=sys.stderr)
    else:
        print(out_text)

    # HTML 封面生成（v3.3 加）
    if args.html:
        if args.html_dir:
            html_dir = Path(args.html_dir).expanduser()
        else:
            from hashlib import sha1
            tag = sha1(args.path.encode("utf-8")).hexdigest()[:8]
            html_dir = Path("~/.xiaohongshu/covers").expanduser() / tag
        paths = render_html_covers(briefs, html_dir, args.highlight)
        print()
        print(f"🎨 生成 {len(paths)} 个 3:4 HTML 封面：")
        for p in paths:
            print(f"   {p}")
        print()
        print("📸 截图方式：")
        print("   1. 浏览器打开 HTML")
        print("   2. F12 / Cmd+Opt+I → 切换设备工具栏（Cmd+Shift+M）")
        print("   3. 选 iPhone 12 Pro 或自定义 750x1000")
        print("   4. 直接截图")
    return 0


if __name__ == "__main__":
    sys.exit(main())
