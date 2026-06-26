#!/usr/bin/env python3
"""火一五小红书"今日推荐" — 解决"打开技能不知道写什么"的空白页焦虑。

综合 4 个信号给 1~3 条选题：
1. **当前节气 / 临近节日**（自动从 data/seasonal_themes.md 命中）
2. **公式轮换**（最近一直用 T2，建议试试别的）
3. **风格档案**（按你的 niche / persona 定制）
4. **栏目化空缺**（如果有 series 沉淀，提醒该更哪个栏目）

每条推荐附：
- 标题候选（1 个）
- 推荐公式 / 骨架
- 推荐理由（为什么是这个选题）
- 一行命令直接起草

用法
----

    python3 today.py                        # 1~3 条推荐
    python3 today.py --n 5                  # 给 5 条
    python3 today.py --format md --out today.md
    python3 today.py --no-llm               # 纯规则
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).parent))

from xhs_profile import ProfileStore, StyleProfile  # noqa: E402
from xhs_writer import generate_titles  # noqa: E402

try:
    import llm_helper
except ImportError:
    llm_helper = None  # type: ignore


_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# =====================================================================
# 节气 / 节日匹配
# =====================================================================


# 大致的节气时间表（公历）— 实际位置以年分小有偏差，但 ±2 天命中率足够
_SOLAR_TERMS = [
    ("立春", 2, 3), ("雨水", 2, 18), ("惊蛰", 3, 5), ("春分", 3, 20),
    ("清明", 4, 4), ("谷雨", 4, 19), ("立夏", 5, 5), ("小满", 5, 20),
    ("芒种", 6, 5), ("夏至", 6, 21), ("小暑", 7, 7), ("大暑", 7, 22),
    ("立秋", 8, 7), ("处暑", 8, 22), ("白露", 9, 7), ("秋分", 9, 22),
    ("寒露", 10, 8), ("霜降", 10, 23), ("立冬", 11, 7), ("小雪", 11, 22),
    ("大雪", 12, 6), ("冬至", 12, 21), ("小寒", 1, 5), ("大寒", 1, 20),
]

# 现代节日
_FESTIVALS = [
    ("元旦", 1, 1), ("情人节", 2, 14), ("妇女节", 3, 8), ("植树节", 3, 12),
    ("愚人节", 4, 1), ("劳动节", 5, 1), ("母亲节", 5, 12),  # 母亲节按 5 月第二周
    ("儿童节", 6, 1), ("父亲节", 6, 16), ("七夕", 8, 17),
    ("教师节", 9, 10), ("国庆", 10, 1), ("万圣节", 10, 31),
    ("光棍节", 11, 11), ("圣诞节", 12, 25),
]


def find_nearest_season(today: dt.date, days_window: int = 7) -> Tuple[str, int]:
    """找到 ± window 天内最近的节气 / 节日。返回 (名字, 距离天数)；若没命中返回 ("", 999)。"""
    candidates: List[Tuple[str, int]] = []
    year = today.year
    for name, m, d in _SOLAR_TERMS + _FESTIVALS:
        try:
            target = dt.date(year, m, d)
        except ValueError:
            continue
        delta = (target - today).days
        if -days_window <= delta <= days_window:
            candidates.append((name, delta))
    if not candidates:
        return ("", 999)
    # 离今天最近的 — 优先未来的（人们倾向提前发节气文）
    candidates.sort(key=lambda x: (abs(x[1]), -x[1]))
    return candidates[0]


def load_season_block(name: str) -> str:
    """从 seasonal_themes.md 抽出对应节气段。"""
    p = _DATA_DIR / "seasonal_themes.md"
    if not p.exists() or not name:
        return ""
    text = p.read_text(encoding="utf-8")
    # 匹配 ### {name} 段
    pat = re.compile(rf"###\s+{re.escape(name)}.*?(?=###\s|\n##\s|\Z)", re.S)
    m = pat.search(text)
    return m.group(0).strip() if m else ""


# =====================================================================
# 公式轮换
# =====================================================================


_ALL_FORMULAS = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11"]


def pick_underused_formulas(profile: StyleProfile, top_n: int = 3) -> List[str]:
    """挑用得最少的公式 — 鼓励轮换。"""
    used = profile.favorite_formulas or {}
    if not used:
        return ["T2", "T3", "T11"]  # 默认推荐起步公式
    # 按使用次数升序
    rest = sorted(_ALL_FORMULAS, key=lambda f: used.get(f, 0))
    return rest[:top_n]


# =====================================================================
# 推荐生成
# =====================================================================


@dataclass
class Suggestion:
    title: str
    formula: str
    skeleton: str
    why: str
    tags: List[str] = field(default_factory=list)
    season_link: str = ""        # 关联到的节气
    command_hint: str = ""        # 一行可执行命令

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def build_suggestions(today: dt.date, profile: StyleProfile, n: int = 3) -> List[Suggestion]:
    season_name, season_delta = find_nearest_season(today)
    underused = pick_underused_formulas(profile)

    persona = profile.persona or ""
    niche = profile.niche or ""
    tags_seed = list(profile.common_tags[:5])

    suggestions: List[Suggestion] = []

    # 推荐 1：节气 / 节日借势（如果命中）
    if season_name:
        # 时间表述
        if season_delta == 0:
            timing = f"今天就是{season_name}"
        elif season_delta > 0:
            timing = f"{season_name}还有 {season_delta} 天，可以提前发"
        else:
            timing = f"{season_name}过了 {-season_delta} 天，余温还在"
        # 用 T7 时间节点公式
        topic = f"{season_name}的{niche or '小日子'}"
        titles = generate_titles(topic, persona=persona, formulas=["T7"], n_each=1)
        title = titles[0]["title"] if titles else f"{season_name}：{topic}"
        suggestions.append(Suggestion(
            title=title,
            formula="T7",
            skeleton="S7",  # 日记 / Vlog 骨架
            why=f"📅 {timing}。节气自带画面感，借一个零件就够了，不要从头造场景。",
            tags=tags_seed + [season_name],
            season_link=season_name,
            command_hint=f"python3 scripts/assistant.py write '{topic}' --formula T7 --skeleton S7",
        ))

    # 推荐 2：公式轮换 — 你最少用的公式
    least_used = underused[0]
    if niche:
        topic = niche
    else:
        topic = "下班后的小事"

    formula_themes = {
        "T1": ("数字对比", "S1"), "T2": ("痛点共情", "S1"), "T3": ("反差冲突", "S6"),
        "T4": ("悬念钩子", "S1"), "T5": ("身份代入", "S2"), "T6": ("福利免费", "S4"),
        "T7": ("时间节点", "S7"), "T8": ("提问诱发", "S6"), "T9": ("极端结果", "S1"),
        "T10": ("步骤指南", "S5"), "T11": ("故事开场", "S2"),
    }
    name, skel = formula_themes.get(least_used, ("通用", "S1"))
    titles = generate_titles(topic, persona=persona, formulas=[least_used], n_each=1)
    title = titles[0]["title"] if titles else f"{topic}（{name}）"
    used_count = (profile.favorite_formulas or {}).get(least_used, 0)
    suggestions.append(Suggestion(
        title=title,
        formula=least_used,
        skeleton=skel,
        why=f"🔄 {least_used}（{name}）你只用过 {used_count} 次 — 试试新视角，避免风格固化。",
        tags=tags_seed,
        command_hint=f"python3 scripts/assistant.py write '{topic}' --formula {least_used} --skeleton {skel}",
    ))

    # 推荐 3：基于风格画像的"安全选择"
    fav_formulas = profile.favorite_formulas or {}
    if fav_formulas:
        top_formula = max(fav_formulas, key=fav_formulas.get)
        name, skel = formula_themes.get(top_formula, ("通用", "S1"))
        topic = f"{niche}的最近一次小发现" if niche else "最近的小发现"
        titles = generate_titles(topic, persona=persona, formulas=[top_formula], n_each=1)
        title = titles[0]["title"] if titles else f"{topic}（{name}）"
        suggestions.append(Suggestion(
            title=title,
            formula=top_formula,
            skeleton=skel,
            why=f"🏠 你最熟练的公式（{top_formula} 用过 {fav_formulas[top_formula]} 次）— "
                f"想要稳定产出就用它。",
            tags=tags_seed,
            command_hint=f"python3 scripts/assistant.py write '{topic}' --formula {top_formula} --skeleton {skel}",
        ))

    return suggestions[:n]


# =====================================================================
# LLM 增强
# =====================================================================


def llm_enhance(suggestions: List[Suggestion],
                today: dt.date,
                profile: StyleProfile) -> List[Suggestion]:
    if not llm_helper or not llm_helper.is_enabled() or not suggestions:
        return suggestions

    prompt = (
        f"今天是 {today.isoformat()}。\n"
        f"创作者画像：{profile.persona or '?'} / 赛道 {profile.niche or '?'}。\n\n"
        f"以下是 {len(suggestions)} 条选题候选（标题 + 公式 + 骨架 + 理由）。\n"
        f"基于 Allen 文案体系（缓存里的 allen_method.md），请给每条：\n"
        f"1. 一句更吸引人的标题改写（≤22 字，符合 Allen 范本范）\n"
        f"2. 一句更具体的'第一段钩子'（≤40 字）\n"
        f"返回 JSON 数组：[{{\"title\": \"...\", \"first_hook\": \"...\"}}, ...]，"
        f"按输入顺序对应。\n\n"
        f"输入：\n"
        f"{json.dumps([{'title': s.title, 'why': s.why} for s in suggestions], ensure_ascii=False)}"
    )
    data = llm_helper.call_json(
        prompt, tier="balanced",
        cached_assets=["allen_method"],
        max_tokens=600,
    )
    if not isinstance(data, list):
        return suggestions
    for i, item in enumerate(data[:len(suggestions)]):
        if not isinstance(item, dict):
            continue
        if item.get("title"):
            suggestions[i].title = item["title"]
        if item.get("first_hook"):
            suggestions[i].why += f"\n   💡 钩子示意：{item['first_hook']}"
    return suggestions


# =====================================================================
# 渲染
# =====================================================================


def render_text(today: dt.date, season: Tuple[str, int], suggestions: List[Suggestion]) -> str:
    parts = []
    parts.append("─" * 60)
    parts.append(f"☕ {today.isoformat()} 今日推荐")
    parts.append("─" * 60)
    parts.append("")

    if season[0]:
        if season[1] == 0:
            parts.append(f"📅 今天恰好是 {season[0]}")
        elif season[1] > 0:
            parts.append(f"📅 临近 {season[0]}（还有 {season[1]} 天）")
        else:
            parts.append(f"📅 {season[0]} 刚过 {-season[1]} 天")
        block = load_season_block(season[0])
        if block:
            # 只取存量画面那 3~5 行
            lines = block.splitlines()
            for ln in lines[:8]:
                if ln.strip().startswith("- "):
                    parts.append(f"   {ln.strip()}")
        parts.append("")

    for i, s in enumerate(suggestions, 1):
        parts.append(f"{i}. {s.title}")
        parts.append(f"   公式 {s.formula} + 骨架 {s.skeleton}")
        parts.append(f"   {s.why}")
        if s.command_hint:
            parts.append(f"   $ {s.command_hint}")
        parts.append("")

    parts.append("─" * 60)
    parts.append("挑一个开始：")
    parts.append("   python3 scripts/assistant.py drafts new --topic '你选中的主题'")
    parts.append("   python3 scripts/assistant.py write '主题' --formula T? --skeleton S?")
    return "\n".join(parts)


def render_md(today: dt.date, season: Tuple[str, int], suggestions: List[Suggestion]) -> str:
    parts = [f"# {today.isoformat()} 今日推荐\n"]
    if season[0]:
        parts.append(f"**临近节气：** {season[0]}\n")
    for i, s in enumerate(suggestions, 1):
        parts.append(f"## {i}. {s.title}\n")
        parts.append(f"- **公式 + 骨架**: {s.formula} + {s.skeleton}")
        parts.append(f"- **推荐理由**: {s.why}")
        if s.tags:
            parts.append(f"- **建议话题**: {' '.join('#' + t for t in s.tags)}")
        parts.append(f"- **起草命令**: `{s.command_hint}`")
        parts.append("")
    return "\n".join(parts) + "\n"


# =====================================================================
# 主流程
# =====================================================================


def main() -> int:
    p = argparse.ArgumentParser(prog="today.py", description="今日选题推荐")
    p.add_argument("--n", type=int, default=3, help="推荐几条（默认 3）")
    p.add_argument("--format", choices=["text", "md", "json"], default="text")
    p.add_argument("--out", default="")
    p.add_argument("--no-llm", action="store_true")
    args = p.parse_args()

    today = dt.date.today()
    profile = ProfileStore().load_style()
    season = find_nearest_season(today)
    suggestions = build_suggestions(today, profile, args.n)

    if not args.no_llm:
        suggestions = llm_enhance(suggestions, today, profile)

    if args.format == "json":
        out_text = json.dumps({
            "date": today.isoformat(),
            "season": {"name": season[0], "delta_days": season[1]} if season[0] else None,
            "profile": {"persona": profile.persona, "niche": profile.niche},
            "suggestions": [s.to_dict() for s in suggestions],
        }, ensure_ascii=False, indent=2)
    elif args.format == "md":
        out_text = render_md(today, season, suggestions)
    else:
        out_text = render_text(today, season, suggestions)

    if args.out:
        Path(args.out).write_text(out_text, encoding="utf-8")
        print(f"✓ 已写入 {args.out}", file=sys.stderr)
    else:
        print(out_text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
