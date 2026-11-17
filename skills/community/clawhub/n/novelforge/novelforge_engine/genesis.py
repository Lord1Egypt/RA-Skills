"""Story Genesis, scale benchmarks, and narrative capacity assessment.

Provides standard Chinese webnovel genre taxonomy, scale tier sizing,
and deterministic story capacity evaluation (anti-underpowered and anti-overcomplex).
"""

from __future__ import annotations

import math
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Union

from .io import read_json, safe_id, write_json_atomic
from .state import init_project


SCALE_TIERS: Dict[str, Dict[str, Any]] = {
    "short": {
        "label": "短篇",
        "min_words": 10000,
        "max_words": 50000,
        "default_words": 30000,
        "default_volumes": 1,
        "words_per_chapter": 2500,
        "description": "知乎短篇、微悬疑、单一脑洞；单核心危机，1~2 个反转，无冗余枝节。",
    },
    "novella": {
        "label": "中短篇 / 小长篇",
        "min_words": 100000,
        "max_words": 300000,
        "default_words": 200000,
        "default_volumes": 3,
        "words_per_chapter": 2500,
        "description": "番茄短剧向、轻小说、都市脑洞；单一核心事件 + 3~5 个阶段冲突，人物闭环。",
    },
    "standard": {
        "label": "中长篇连载",
        "min_words": 500000,
        "max_words": 1000000,
        "default_words": 800000,
        "default_volumes": 5,
        "words_per_chapter": 2800,
        "description": "经典升级流、都市异能、末世求生；3~5 个地图/副本切换，完整阶段反派与阶梯成长。",
    },
    "epic": {
        "label": "宏大超长篇",
        "min_words": 1500000,
        "max_words": 3500000,
        "default_words": 2000000,
        "default_volumes": 10,
        "words_per_chapter": 2800,
        "description": "传统仙侠、玄幻争霸、诸天无限；多层世界观，多阵营零和博弈，深层世界真相与史诗群像。",
    },
}

GENRE_ALIASES: Dict[str, str] = {
    "玄幻": "修仙",
    "修真": "修仙",
    "玄幻修仙": "修仙",
    "都市修真": "都市异能",
    "游戏电竞": "电竞",
    "电竞文": "电竞",
    "直播": "直播文",
    "主播": "直播文",
    "直播带货": "直播文",
    "克系": "克苏鲁",
    "克系悬疑": "克苏鲁",
    "规则怪谈文": "规则怪谈",
}

CANONICAL_GENRES = {
    # 玄幻修仙
    "修仙", "系统流", "高武", "西幻", "无限流", "末世", "科幻",
    # 都市现代
    "都市异能", "都市日常", "都市脑洞", "现实题材", "电竞", "直播文",
    # 言情女性向
    "古言", "宫斗宅斗", "青春甜宠", "豪门总裁", "职场婚恋", "民国言情",
    "幻想言情", "现言脑洞", "女频悬疑", "种田", "年代",
    # 悬疑脑洞
    "规则怪谈", "悬疑脑洞", "悬疑灵异", "克苏鲁", "知乎短篇",
}


def normalize_genre(genre_input: Optional[str]) -> str:
    """Normalize input string to canonical single or composite genre (max 2)."""
    if not genre_input or not isinstance(genre_input, str):
        return "通用故事"

    # Split on +, /, 、 , 与
    parts = re.split(r"[+/、与\s]+", genre_input.strip())
    normalized_parts = []
    for part in parts:
        cleaned = part.strip()
        if not cleaned:
            continue
        mapped = GENRE_ALIASES.get(cleaned, cleaned)
        if mapped not in normalized_parts:
            normalized_parts.append(mapped)

    if not normalized_parts:
        return "通用故事"

    # Limit to at most 2 composite genres
    return "+".join(normalized_parts[:2])


def calculate_scale_spec(
    tier: str = "standard",
    target_words: Optional[int] = None,
    words_per_chapter: Optional[int] = None,
    planned_volumes: Optional[int] = None,
) -> Dict[str, Any]:
    """Calculate structured scale boundaries and estimated metrics."""
    tier_clean = tier.lower().strip()
    if tier_clean not in SCALE_TIERS:
        tier_clean = "standard"

    tier_info = SCALE_TIERS[tier_clean]
    actual_words = int(target_words) if target_words and target_words > 0 else tier_info["default_words"]
    actual_wpc = int(words_per_chapter) if words_per_chapter and words_per_chapter > 0 else tier_info["words_per_chapter"]
    actual_vols = int(planned_volumes) if planned_volumes and planned_volumes > 0 else tier_info["default_volumes"]

    estimated_chapters = max(1, math.ceil(actual_words / actual_wpc))

    return {
        "tier": tier_clean,
        "label": tier_info["label"],
        "target_words": actual_words,
        "words_per_chapter": actual_wpc,
        "planned_volumes": actual_vols,
        "estimated_chapters": estimated_chapters,
        "min_words": tier_info["min_words"],
        "max_words": tier_info["max_words"],
        "tier_description": tier_info["description"],
    }


def evaluate_story_capacity(
    scale_tier: str = "standard",
    target_words: Optional[int] = None,
    progression_ranks: int = 1,
    factions_count: int = 1,
    motivations_count: int = 1,
    genre: Optional[str] = None,
) -> Dict[str, Any]:
    """Evaluate whether the story's depth and complexity can sustain the target scale."""
    spec = calculate_scale_spec(scale_tier, target_words=target_words)
    words = spec["target_words"]
    ranks = max(1, int(progression_ranks))
    factions = max(1, int(factions_count))
    motivations = max(1, int(motivations_count))
    norm_genre = normalize_genre(genre)

    diagnostics = []
    recommendations = []
    status = "HEALTHY"

    # Risk A: Underpowered (小马拉大车)
    if words >= 500000:
        underpowered_reasons = []
        if motivations < 2:
            underpowered_reasons.append(f"核心驱动力仅声明了 {motivations} 处，初期目标达成后面临剧情注水断崖")
        if ranks < 4:
            underpowered_reasons.append(f"力量/技术阶梯仅有 {ranks} 阶，难以支撑 50 万字以上的持续升级与换地图节奏")
        if factions < 2:
            underpowered_reasons.append(f"对立或中立阵营仅有 {factions} 个，缺乏多方博弈与外部张力源")

        if underpowered_reasons:
            status = "RISK_UNDERPOWERED"
            diagnostics.append("【小马拉大车警告】当前故事设定偏单薄，难以承载长篇连载规模。")
            diagnostics.extend(underpowered_reasons)
            recommendations.append("补充深层世界危机或主角终极追求，使剧情具备多阶段递进动力。")
            recommendations.append("扩展力量/技术成长阶梯（建议中长篇至少 5-7 阶，超长篇至少 8-10 阶）。")
            recommendations.append("引入多方独立阵营（中立宗门、敌对财阀、异族神魔），创造多线冲突。")
            recommendations.append("或将目标篇幅调低为中短篇 (10~30 万字)。")

    # Risk B: Overcomplex (大马拉小车)
    elif words <= 50000:
        overcomplex_reasons = []
        if ranks >= 8:
            overcomplex_reasons.append(f"短篇设定了 {ranks} 阶宏大等级，正文无篇幅展示成长过程，易变成说明文")
        if factions >= 6:
            overcomplex_reasons.append(f"短篇设定了 {factions} 个阵营势力，读者在有限字数内难以建立认知")

        if overcomplex_reasons:
            status = "RISK_OVERCOMPLEX"
            diagnostics.append("【大马拉小车警告】短篇幅承载了过于庞杂的宏大世界观与繁复阵营，容易产生信息过载与剧情难以展开的风险。")
            diagnostics.extend(overcomplex_reasons)
            recommendations.append("对世界观进行降维剪枝，聚焦 1 个核心冲突地点与 2~3 个核心阵营。")
            recommendations.append("将非即时相关的力量体系留白，作为背景隐喻而非正文主要展开点。")
            recommendations.append("或将目标篇幅提升为中长篇 (50 万字以上)。")

    if status == "HEALTHY":
        diagnostics.append("故事动力层级、世界观体系纵深与阵营复杂度良好匹配目标篇幅规模。")
        recommendations.append("承载力健康，可直接推进分卷大纲与第 1 章蓝图设计。")

    return {
        "status": status,
        "genre": norm_genre,
        "scale": spec,
        "inputs": {
            "progression_ranks": ranks,
            "factions_count": factions,
            "motivations_count": motivations,
        },
        "diagnostics": diagnostics,
        "recommendations": recommendations,
    }


def init_project_with_genesis(
    root: Union[str, Path],
    genre: Optional[str] = None,
    scale_tier: str = "standard",
    target_words: Optional[int] = None,
    words_per_chapter: Optional[int] = None,
    planned_volumes: Optional[int] = None,
    engine: str = "jin-yong",
) -> Dict[str, Any]:
    """Initialize project folder skeleton and populate rich scale & genre metadata."""
    root_path = Path(root).resolve()
    base_profile = init_project(root_path)

    scale_spec = calculate_scale_spec(
        tier=scale_tier,
        target_words=target_words,
        words_per_chapter=words_per_chapter,
        planned_volumes=planned_volumes,
    )
    norm_genre = normalize_genre(genre)

    project_file = root_path / ".novelforge" / "state" / "project.json"
    project_data = read_json(project_file) if project_file.is_file() else base_profile

    project_data["genre"] = norm_genre
    project_data["engine"] = engine if safe_id(engine) else "jin-yong"
    if "engines" not in project_data or not isinstance(project_data["engines"], list):
        project_data["engines"] = [project_data["engine"]]
    elif project_data["engine"] not in project_data["engines"]:
        project_data["engines"].append(project_data["engine"])

    project_data["scale"] = {
        "tier": scale_spec["tier"],
        "target_words": scale_spec["target_words"],
        "words_per_chapter": scale_spec["words_per_chapter"],
        "planned_volumes": scale_spec["planned_volumes"],
        "estimated_chapters": scale_spec["estimated_chapters"],
    }

    write_json_atomic(project_file, project_data)
    return project_data

