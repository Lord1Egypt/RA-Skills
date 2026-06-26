#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Monthly report controller for Health-Mate."""

from __future__ import annotations

import json
import os
import re
import shutil
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable, List, Optional


def console_print(*args, sep=" ", end="\n", file=sys.stdout, flush=False):
    """Print safely even when the active terminal encoding cannot render CJK text."""
    text = sep.join(str(arg) for arg in args) + end
    try:
        file.write(text)
    except UnicodeEncodeError:
        encoding = getattr(file, "encoding", None) or "utf-8"
        buffer = getattr(file, "buffer", None)
        if buffer is not None:
            buffer.write(text.encode(encoding, errors="replace"))
        else:
            file.write(text.encode("ascii", errors="backslashreplace").decode("ascii"))
    if flush:
        file.flush()


print = console_print

from daily_report_pro import (
    REPORTS_DIR,
    build_multi_condition_tip,
    build_score_report,
    find_custom_section_items,
    force_config_locale,
    generation_source_label,
    has_tavily_api_key,
    get_condition_standards,
    get_conditions_display_name,
    get_generation_settings,
    get_population_branch,
    get_primary_condition,
    get_profile_conditions,
    get_scoring_modules,
    load_user_config,
    parse_memory_file,
    prepare_font_compatible_memory,
    resolve_report_locale,
    run_local_llm,
    tavily_search,
    validate_environment,
)
from i18n import build_delivery_message, format_weight, inline_localize, localize_free_text, resolve_locale
from monthly_pdf_generator import generate_monthly_pdf_report

validate_environment()

MEMORY_DIR = os.environ.get("MEMORY_DIR", "")
MAX_HOSPITAL_RECOMMENDATIONS = 5
TOP_TIER_HOSPITAL_KEYWORDS = (
    "华西医院",
    "协和医院",
    "湘雅医院",
    "瑞金医院",
    "中山医院",
    "华山医院",
    "仁济医院",
    "齐鲁医院",
    "西京医院",
    "同济医院",
)
CUSTOM_SECTION_IGNORE_HINTS = (
    "今日目标",
    "dailytarget",
    "目标",
    "review",
    "昨日回顾",
    "今日汇总",
    "summary",
    "系统开发与优化记录",
    "工作日志",
    "suggestion",
    "建议",
    "提醒",
    "note",
    "备注",
    "午餐建议记录",
    "午餐选择确认",
    "优化讨论",
    "工作地点",
)
MONITORING_SECTION_HINTS = (
    "血压",
    "bloodpressure",
    "bp",
    "血糖",
    "glucose",
    "bloodsugar",
    "体脂",
    "bodyfat",
    "bodycomposition",
    "生化",
    "化验",
    "检验",
    "实验室",
    "lab",
    "biochemistry",
    "monitor",
    "监测",
    "睡眠",
    "sleep",
    "心率",
    "heartrate",
)
SEARCH_NOISE_TERMS = (
    "返回顶部按钮",
    "返回顶部",
    "倍速",
    "播放",
    "收藏",
    "分享",
    "关注",
    "交流",
    "视频",
    "门诊好评",
    "累计挂号",
    "精选内容",
    "点击展开",
    "展开全文",
    "阅读全文",
    "相关推荐",
    "立即预约",
    "在线问诊",
    "广告",
)
SEARCH_BAD_PATTERNS = (
    r"(?:\[\d+\]){2,}",
    r"(?:表|图)\s*\d",
    r"(?:Table|Figure)\s*\d",
    r"注释[:：]",
    r"\bDOI\b",
    r"\bet al\.\b",
    r"[Α-Ωα-ω]",
    r"[Ѐ-ӿ]",
)


def localize(locale: str, zh_text: str, en_text: str) -> str:
    return inline_localize(locale, zh_text, en_text)


def sanitize_locale_line(locale: str, text: str) -> str:
    return localize_free_text(locale, text) if resolve_locale(locale=locale) == "ja-JP" else text


def localize_three(locale: str, zh_text: str, en_text: str, ja_text: Optional[str] = None) -> str:
    resolved = resolve_locale(locale=locale)
    if resolved == "zh-CN":
        return zh_text
    if resolved == "ja-JP" and ja_text is not None:
        return ja_text
    return en_text


def is_lifestyle_mode(primary_condition: Optional[str], population_branch: Optional[str] = None) -> bool:
    normalized_branch = str(population_branch or "").strip().lower()
    if normalized_branch in {"lifestyle", "disease"}:
        return normalized_branch == "lifestyle"
    return str(primary_condition or "").strip() in {"balanced", "fat_loss"}


def monthly_section_label(locale: str, primary_condition: Optional[str], key: str, population_branch: Optional[str] = None) -> str:
    lifestyle_mode = is_lifestyle_mode(primary_condition, population_branch)
    mappings = {
        "deep_dive": (
            ("核心体征与习惯洞察", "Core Vitals & Habit Insights", "コア指標と習慣インサイト"),
            ("专科病理深度对齐", "Specialty Deep Dive", "病態別ディープダイブ"),
        ),
        "action_plan": (
            ("月度健康复盘与行动策略", "Monthly Review & Action Strategy", "月間レビューと行動戦略"),
            ("专家会诊与医疗规划", "Medical Action Plan", "医療アクションプラン"),
        ),
        "ai_review": (
            ("AI 综合健康研判", "AI Comprehensive Assessment", "AI 総合健康評価"),
            ("AI 月度病情研判", "AI Monthly Review", "AI 月次レビュー"),
        ),
        "follow_up": (
            ("周期性体测与筛查建议", "Periodic Screening Suggestions", "定期測定・スクリーニング提案"),
            ("复查提醒", "Follow-up Reminders", "フォローアップ提案"),
        ),
        "hospital": (
            ("医院与门诊建议", "Hospital and Clinic Suggestions", "病院・外来提案"),
            ("医院与门诊建议", "Hospital and Clinic Suggestions", "病院・外来提案"),
        ),
        "trend_block": (
            ("核心体征与习惯洞察", "Core Vitals & Habit Insights", "コア指標と習慣インサイト"),
            ("专科趋势分析", "Specialty Trends", "病態トレンド"),
        ),
    }
    lifestyle_titles, default_titles = mappings[key]
    chosen = lifestyle_titles if lifestyle_mode else default_titles
    return localize_three(locale, *chosen)


def get_monthly_review_blueprint(primary_condition: Optional[str], population_branch: Optional[str] = None) -> List[dict]:
    if is_lifestyle_mode(primary_condition, population_branch):
        return [
            {"zh": "核心发现", "en": "Core Findings", "ja": "【主要な発見】"},
            {"zh": "体态与习惯预警", "en": "Body Composition & Habit Watch", "ja": "【体組成と習慣の注意点】"},
            {"zh": "次月高阶干预清单", "en": "Advanced Next-Month Checklist", "ja": "【来月の高度アクションリスト】"},
        ]
    return [
        {"zh": "关键发现", "en": "Key Findings", "ja": "【主要な発見】"},
        {"zh": "风险关注", "en": "Risk Watch", "ja": "【リスク観察】"},
        {"zh": "下月调整", "en": "Next-Month Actions", "ja": "【来月の調整】"},
    ]


def safe_average(values: Iterable[Optional[float]]) -> float:
    cleaned = [value for value in values if value is not None]
    return sum(cleaned) / len(cleaned) if cleaned else 0.0


def dedupe_preserve_order(items: Iterable[str]) -> List[str]:
    seen = set()
    output = []
    for item in items:
        normalized = str(item or "").strip()
        if not normalized or normalized in seen:
            continue
        output.append(normalized)
        seen.add(normalized)
    return output


def get_month_dates(target_date_str: str) -> List[str]:
    target_date = datetime.strptime(target_date_str, "%Y-%m-%d")
    start_date = target_date.replace(day=1)
    if start_date.month == 12:
        next_month = start_date.replace(year=start_date.year + 1, month=1, day=1)
    else:
        next_month = start_date.replace(month=start_date.month + 1, day=1)
    day_count = (next_month - start_date).days
    return [(start_date + timedelta(days=offset)).strftime("%Y-%m-%d") for offset in range(day_count)]


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", str(text or "").lower()).strip("_") or "metric"


def build_custom_section_rollup(config: dict) -> Dict[str, dict]:
    rollup = {}
    for module in get_scoring_modules(config):
        if not module.get("enabled", True):
            continue
        if module.get("type") != "section_presence" or module.get("id") == "medication":
            continue
        section_title = module.get("section_title", module.get("title", module.get("id", ""))).strip()
        key = module.get("id", section_title)
        rollup[key] = {
            "id": key,
            "title": module.get("title", section_title),
            "section_title": section_title,
            "days_recorded": 0,
            "items": 0,
            "configured": True,
            "latest_items": [],
        }
    return rollup


def merge_dynamic_custom_sections(rollup: Dict[str, dict], custom_sections: dict) -> None:
    for header, items in (custom_sections or {}).items():
        matched = False
        for stats in rollup.values():
            if find_custom_section_items({header: items}, stats.get("section_title", stats.get("title", ""))):
                matched = True
                break
        if matched:
            continue
        key = f"dynamic::{header}".strip()
        if key not in rollup:
            rollup[key] = {
                "id": key,
                "title": header,
                "section_title": header,
                "days_recorded": 0,
                "items": 0,
                "configured": False,
                "latest_items": [],
            }


def read_text(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()
    except OSError:
        return ""


def normalize_name(value: str) -> str:
    text = re.sub(r"[*_`]+", "", str(value or "")).strip().lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", text)
    return text


def should_ignore_custom_section(title: str) -> bool:
    normalized = normalize_name(title)
    return any(normalize_name(hint) in normalized for hint in CUSTOM_SECTION_IGNORE_HINTS if hint)


def is_monitoring_section_title(title: str, allowed_titles: Optional[set] = None) -> bool:
    normalized = normalize_name(title)
    if allowed_titles and normalized in allowed_titles:
        return True
    return any(normalize_name(hint) in normalized for hint in MONITORING_SECTION_HINTS if hint)


def section_matches(title: str, aliases: Iterable[str]) -> bool:
    normalized_title = normalize_name(title)
    return any(normalize_name(alias) in normalized_title for alias in aliases if alias)


def parse_numeric_item(item: str) -> Optional[dict]:
    text = str(item or "").strip()
    pattern = re.compile(
        r"(?P<label>[A-Za-z\u4e00-\u9fff][A-Za-z0-9\u4e00-\u9fff /%_-]{0,32})\s*[:：]\s*(?P<value>-?\d+(?:\.\d+)?)\s*(?P<unit>[A-Za-z%/._\-\u4e00-\u9fff]*)"
    )
    match = pattern.search(text)
    if not match:
        return None
    label = match.group("label").strip()
    if normalize_name(label) in {"bmi", "kcal", "calories", "steps", "步数", "饮水量", "累计"}:
        return None
    return {
        "label": label,
        "value": float(match.group("value")),
        "unit": (match.group("unit") or "").strip(),
    }


def extract_structured_metrics(file_path: str, daily_data: dict) -> dict:
    content = read_text(file_path)
    custom_sections = daily_data.get("custom_sections", {})
    metrics = {
        "body_fat_percent": None,
        "blood_pressure": [],
        "glucose": [],
        "custom_numeric_metrics": [],
    }

    body_fat_match = re.search(r"(?:体脂率|body\s*fat(?:\s*percentage)?)\s*[:：]\s*(\d+(?:\.\d+)?)\s*%", content, re.IGNORECASE)
    if body_fat_match:
        metrics["body_fat_percent"] = float(body_fat_match.group(1))

    bp_aliases = ["血压", "blood pressure", "bp"]
    glucose_aliases = ["血糖", "blood sugar", "glucose"]
    bodyfat_aliases = ["体脂", "body fat", "body composition", "身体成分"]

    for header, items in custom_sections.items():
        if should_ignore_custom_section(header):
            continue
        if section_matches(header, bp_aliases):
            for item in items:
                bp_match = re.search(r"(\d{2,3})\s*/\s*(\d{2,3})\s*(?:mmhg)?", str(item), re.IGNORECASE)
                if not bp_match:
                    continue
                heart_rate_match = re.search(r"(?:心率|heart rate|hr)\s*[:：]?\s*(\d{2,3})", str(item), re.IGNORECASE)
                metrics["blood_pressure"].append(
                    {
                        "raw": item,
                        "systolic": int(bp_match.group(1)),
                        "diastolic": int(bp_match.group(2)),
                        "heart_rate": int(heart_rate_match.group(1)) if heart_rate_match else None,
                    }
                )
        elif section_matches(header, glucose_aliases):
            for item in items:
                glucose_match = re.search(r"(?:血糖|glucose|blood sugar)\s*[:：]?\s*(\d+(?:\.\d+)?)\s*(mmol/l|mg/dl)?", str(item), re.IGNORECASE)
                if not glucose_match:
                    continue
                metrics["glucose"].append(
                    {
                        "raw": item,
                        "value": float(glucose_match.group(1)),
                        "unit": (glucose_match.group(2) or "mmol/L").upper(),
                    }
                )
        elif section_matches(header, bodyfat_aliases):
            for item in items:
                bodyfat_match = re.search(r"(?:体脂率|body\s*fat(?:\s*percentage)?)\s*[:：]?\s*(\d+(?:\.\d+)?)\s*%", str(item), re.IGNORECASE)
                if bodyfat_match:
                    metrics["body_fat_percent"] = float(bodyfat_match.group(1))
                numeric_item = parse_numeric_item(item)
                if numeric_item:
                    metrics["custom_numeric_metrics"].append({"section": header, **numeric_item})
        else:
            for item in items:
                numeric_item = parse_numeric_item(item)
                if numeric_item:
                    metrics["custom_numeric_metrics"].append({"section": header, **numeric_item})

    return metrics


def daily_symptom_count(daily_data: dict) -> int:
    symptoms = extract_relevant_symptom_lines(daily_data)
    if not symptoms:
        return 0
    symptom_text = " ".join(symptoms).lower()
    if any(token in symptom_text for token in ["无不适", "无症状", "none", "no symptom", "no discomfort"]):
        return 0
    labels = extract_symptom_labels(daily_data, "zh-CN")
    if labels:
        return len(labels)
    return len(symptoms)


def extract_relevant_symptom_lines(daily_data: dict) -> List[str]:
    raw_items = [str(item or "").strip() for item in daily_data.get("symptoms", []) if str(item or "").strip()]
    if not raw_items:
        return []

    skip_hints = [
        "无记录",
        "待记录",
        "--",
        "早餐",
        "午餐",
        "晚餐",
        "加餐",
        "饮水",
        "步数",
        "骑行",
        "运动",
        "千卡",
        "kcal",
        "膳食纤维",
        "蛋白质",
        "脂肪：",
        "碳水：",
        "评估：",
        "总计：",
        "状态：",
        "总消耗",
        "有氧运动",
        "少量多餐",
        "胆汁",
        "维生素",
        "全天步数",
        "可能缓解因素",
        "症状持续时长",
        "当前：待评估",
        "current status",
        "possible relieving factors",
        "duration",
        "source note",
        "source memory",
        "strict low-fat meals",
        "fiber target",
        "smaller, more frequent meals",
        "hydration",
        "cycling",
        "exercise",
        "steps",
        "症状持続時間",
        "現在状態",
        "不調なし",
    ]
    positive_hints = [
        "右上腹",
        "右上腹部",
        "腹胀",
        "腹涨",
        "腹痛",
        "胀痛",
        "隐痛",
        "绞痛",
        "恶心",
        "不适",
        "張り",
        "痛み",
        "違和感",
        "吐き気",
        "pain",
        "bloating",
        "distension",
        "nausea",
        "discomfort",
    ]
    resolved_hints = ["无不适", "无症状", "无不适感", "完全缓解", "症状已完全缓解", "recovered", "resolved", "不調なし", "症状なし", "完全に緩解", "完全に改善", "已恢复", "已恢復"]

    relevant = []
    for item in raw_items:
        lowered = item.lower()
        if any(hint.lower() in lowered for hint in skip_hints):
            continue
        if any(hint.lower() in lowered for hint in resolved_hints):
            continue
        if any(hint.lower() in lowered for hint in positive_hints):
            relevant.append(item)
    return dedupe_preserve_order(relevant)


def extract_symptom_labels(daily_data: dict, locale: str) -> List[str]:
    symptoms = extract_relevant_symptom_lines(daily_data)
    if not symptoms:
        return []
    if resolve_locale(locale=locale) == "ja-JP":
        symptoms = [sanitize_locale_line(locale, item) for item in symptoms]

    symptom_text = " ".join(symptoms).lower()
    if any(token in symptom_text for token in ["无不适", "无症状", "none", "no symptom", "no discomfort"]):
        return []

    label_map = [
        (
            localize(locale, "右上腹隐痛", "Right upper abdominal pain"),
            [
                "右上腹隐痛",
                "右上腹痛",
                "右上腹疼",
                "右上腹不适",
                "右上腹胀",
                "右上腹胀痛",
                "right upper abdominal pain",
                "right upper quadrant pain",
                "ruq pain",
                "right upper abdominal discomfort",
                "right upper abdominal bloating",
                "post-meal right upper abdominal bloating",
                "post-meal right upper quadrant discomfort",
                "右上腹部の張り",
                "右上腹部の痛み",
                "右上腹部の違和感",
            ],
        ),
        (
            localize(locale, "餐后腹胀", "Post-meal bloating"),
            ["餐后腹胀", "饭后腹胀", "饭后发胀", "post-meal bloating", "postprandial bloating", "食後の腹部膨満", "食後の張り"],
        ),
        (
            localize(locale, "腹胀", "Bloating"),
            ["腹胀", "腹涨", "bloating", "distension", "腹部膨満", "張り"],
        ),
        (
            localize(locale, "恶心", "Nausea"),
            ["恶心", "nausea", "吐き気"],
        ),
        (
            localize(locale, "绞痛", "Colic"),
            ["绞痛", "colic", "疝痛"],
        ),
        (
            localize(locale, "腹痛", "Abdominal pain"),
            ["腹痛", "胃痛", "abdominal pain", "abdomen pain", "腹痛", "胃の痛み"],
        ),
        (
            localize(locale, "不适", "Discomfort"),
            ["不适", "discomfort", "不調", "違和感"],
        ),
    ]

    matched = []
    for label, aliases in label_map:
        if any(alias in symptom_text for alias in aliases):
            matched.append(label)

    dominant_ruq_label = localize(locale, "右上腹隐痛", "Right upper abdominal pain")
    generic_bloating_label = localize(locale, "腹胀", "Bloating")
    generic_discomfort_label = localize(locale, "不适", "Discomfort")
    if dominant_ruq_label in matched:
        matched = [label for label in matched if label not in {generic_bloating_label, generic_discomfort_label}]
    elif len(matched) > 1 and generic_discomfort_label in matched:
        matched = [label for label in matched if label != generic_discomfort_label]

    if matched:
        return dedupe_preserve_order(matched)

    fallback_labels = []
    for item in symptoms:
        cleaned = re.sub(r"^[\-\s•*]+", "", item)
        cleaned = re.sub(r"[:：].*$", "", cleaned).strip()
        cleaned = sanitize_locale_line(locale, cleaned)
        if 0 < len(cleaned) <= 24:
            fallback_labels.append(cleaned)
    return dedupe_preserve_order(fallback_labels)


def format_monthly_review_sections(locale: str, sections: Iterable[dict]) -> str:
    parts = []
    resolved = resolve_locale(locale=locale)
    for section in sections:
        if isinstance(section, tuple):
            zh_title = section[0] if len(section) > 0 else ""
            en_title = section[1] if len(section) > 1 else zh_title
            body = section[2] if len(section) > 2 else ""
            section = {"zh": zh_title, "en": en_title, "body": body}
        clean_body = str(section.get("body") or "").strip()
        if not clean_body:
            continue
        if resolved == "zh-CN":
            title = f"【{section.get('zh', '')}】"
        elif resolved == "ja-JP":
            title = section.get("ja") or f"【{sanitize_locale_line(locale, section.get('zh', ''))}】"
        else:
            title = f"[{section.get('en', '')}]"
        parts.append(f"**{title}**\n{clean_body}")
    return "\n\n".join(parts).strip()


def ensure_monthly_review_sections(text: str, monthly_data: dict, locale: str, primary_condition: Optional[str] = None) -> str:
    cleaned = str(text or "").strip()
    if not cleaned:
        return ""

    blueprint = get_monthly_review_blueprint(primary_condition, monthly_data.get("population_branch"))
    tokens = []
    for item in blueprint:
        tokens.extend([item.get("zh", ""), item.get("en", ""), str(item.get("ja", "")).replace("【", "").replace("】", "")])
    if any(token and token in cleaned for token in tokens):
        return cleaned

    sentences = [item.strip() for item in re.split(r"(?<=[。！？!?])\s+|(?<=\.)\s+", cleaned) if item.strip()]
    findings = " ".join(sentences[:2]) or cleaned
    risk = " ".join(sentences[2:4]).strip()
    plan = " ".join(sentences[4:]).strip()
    low_scores = [
        label
        for key, label in [
            ("diet", localize(locale, "饮食", "diet")),
            ("water", localize(locale, "饮水", "hydration")),
            ("exercise", localize(locale, "运动", "exercise")),
            ("monitoring", localize(locale, "监测", "monitoring")),
        ]
        if monthly_data.get("macro_scores", {}).get(key, 0) < 70
    ]

    if is_lifestyle_mode(primary_condition, monthly_data.get("population_branch")):
        if not risk:
            watch_items = []
            if low_scores:
                watch_items.append(
                    localize_three(
                        locale,
                        f"当前执行偏弱的维度集中在：{'、'.join(low_scores)}。",
                        f"The weakest adherence dimensions are: {', '.join(low_scores)}.",
                        f"弱い実行項目は主に {'、'.join(low_scores)} です。",
                    )
                )
            if abs(float(monthly_data.get("weight_change", 0) or 0)) > 2.5:
                watch_items.append(
                    localize_three(
                        locale,
                        "本月体重波动偏大，建议复盘热量波动、恢复质量与记录连续性。",
                        "Weight changed quickly this month, so calorie swings, recovery quality, and logging consistency should be reviewed.",
                        "今月の体重変動はやや大きく、摂取量の揺れや回復の質、記録の連続性を見直す価値があります。",
                    )
                )
            if monthly_data.get("avg_body_fat_percent") and monthly_data.get("valid_weight_days", 0) >= 5:
                watch_items.append(
                    localize_three(
                        locale,
                        "若体重下降但体脂改善不明显，说明仍需提高蛋白质量、力量训练占比与恢复质量。",
                        "If weight falls without clear body-fat improvement, protein quality, resistance training, and recovery still need work.",
                        "体重が落ちても体脂肪率の改善が鈍い場合は、たんぱく質・筋力トレーニング・回復の質を見直してください。",
                    )
                )
            if not watch_items:
                watch_items.append(
                    localize_three(
                        locale,
                        "整体风险不高，但仍需持续关注作息稳定性、三大营养素分配与训练单一化问题。",
                        "Overall risk is modest, but sleep regularity, macro balance, and overly single-pattern training still deserve attention.",
                        "全体リスクは高くありませんが、睡眠の安定、栄養バランス、運動の単調さには引き続き注意が必要です。",
                    )
                )
            risk = " ".join(watch_items)

        if not plan:
            current_weight = float(monthly_data.get("latest_weight") or monthly_data.get("avg_weight") or 60)
            protein_target = max(90, int(round(current_weight * (1.6 if str(primary_condition) == "fat_loss" else 1.3))))
            calorie_target = int(round(monthly_data.get("avg_calories", 0) or 0))
            plan = "\n".join(
                [
                    localize_three(
                        locale,
                        f"1. 饮食宏观结构微调：优先把日均蛋白稳定到约 {protein_target}g；若本月热量起伏较大，先把工作日与周末的热量差控制在 300kcal 内。",
                        f"1. Nutrition structure: stabilize daily protein near {protein_target}g, and keep weekday-vs-weekend calorie swings within about 300 kcal when intake has been inconsistent.",
                        f"1. 栄養構成の微調整: 1日のたんぱく質をおよそ {protein_target}g に安定させ、摂取のばらつきが大きい場合は平日と休日の差を 300kcal 以内に抑えます。",
                    ),
                    localize_three(
                        locale,
                        "2. 运动负荷建议：将有氧与力量训练拆分规划，至少保证每周 2-3 次力量训练，并让步数/骑行等有氧承担日常消耗基础。",
                        "2. Training load: separate cardio from strength work, keep at least 2-3 resistance sessions each week, and use steps or cycling as the aerobic base.",
                        "2. 運動負荷の提案: 有酸素と筋力トレーニングを分けて計画し、週 2-3 回の筋力トレーニングを確保しつつ、歩数やサイクリングを日常の消費基盤にします。",
                    ),
                    localize_three(
                        locale,
                        f"3. 作息与补剂建议：优先修复睡眠窗口与进餐节律；如近期热量约 {calorie_target}kcal 且训练频率较高，可结合日常饮食评估 Omega-3、维生素D 或电解质补充是否需要常规化。",
                        f"3. Recovery and supplements: stabilize sleep and meal timing first; if training volume is high, review whether routine omega-3, vitamin D, or electrolytes make sense alongside your usual diet.",
                        f"3. 生活リズムと補助栄養: まず睡眠時間帯と食事リズムを安定させ、運動量が高い場合は日常食に合わせて Omega-3・ビタミンD・電解質の補助を検討します。",
                    ),
                ]
            )
    else:
        if not risk:
            if low_scores:
                risk = localize(locale, f"当前仍需重点关注：{'、'.join(low_scores)}。", f"The main watch-outs remain: {', '.join(low_scores)}.")
            else:
                risk = localize(locale, "本月整体风险信号不高，但仍需继续保持记录完整性。", "Overall risk signals stayed modest this month, but tracking consistency still matters.")

        if not plan:
            plan = localize(
                locale,
                "下月建议继续优先稳定饮食节奏、补齐专项监测，并把高风险触发因素写进每日记录，便于继续做趋势对照。",
                "Next month, prioritize steadier meal timing, more complete specialty monitoring, and explicit trigger notes in daily logs so trends stay comparable.",
            )

    return format_monthly_review_sections(
        locale,
        [
            {**blueprint[0], "body": findings},
            {**blueprint[1], "body": risk},
            {**blueprint[2], "body": plan},
        ],
    )


def get_profile_residence(profile: dict, locale: str) -> dict:
    residence = profile.get("residence", {}) if isinstance(profile.get("residence"), dict) else {}
    country = str(residence.get("country") or profile.get("country") or "").strip()
    province = str(residence.get("province") or profile.get("province") or "").strip()
    city = str(residence.get("city") or profile.get("city") or "").strip()
    district = str(residence.get("district") or profile.get("district") or "").strip()
    display_name = str(residence.get("display_name") or "").strip()
    parts = [part for part in [province, city, district] if part]
    if not display_name and parts:
        display_name = "".join(parts) if locale == "zh-CN" else ", ".join(parts)
    return {
        "country": country,
        "province": province,
        "city": city,
        "district": district,
        "display_name": display_name,
    }


def extract_gallstone_ultrasound_summary(memory_dir: str) -> dict:
    path = os.path.join(memory_dir, "gallstone_ultrasound_records.md")
    content = read_text(path)
    if not content:
        return {}

    records = []
    for date_str, size_str in re.findall(r"(\d{4}-\d{2}-\d{2}).*?(\d+(?:\.\d+)?)\s*cm", content):
        try:
            records.append((date_str, float(size_str)))
        except ValueError:
            continue
    if not records:
        return {}
    records.sort(key=lambda item: item[0])
    latest_date, latest_size = records[-1]
    return {
        "latest_date": latest_date,
        "latest_size_cm": latest_size,
        "max_size_cm": max(size for _, size in records),
        "wall_warning": any(token in content for token in ["毛糙", "增厚", "壁厚", "炎症"]),
    }


def aggregate_monthly_data(month_dates: List[str], config: dict, locale: Optional[str] = None, memory_dir: Optional[str] = None) -> dict:
    locale = resolve_locale(config, locale=locale)
    memory_dir = memory_dir or MEMORY_DIR
    profile = config.get("user_profile", {})
    conditions = get_profile_conditions(profile)
    primary_condition = get_primary_condition(profile)
    condition_text = get_conditions_display_name(locale, conditions)
    standards = get_condition_standards(config, conditions)
    custom_rollup = build_custom_section_rollup(config)
    allowed_monitoring_titles = {
        normalize_name(module.get("section_title", module.get("title", "")))
        for module in get_scoring_modules(config)
        if module.get("enabled", True) and module.get("type") == "section_presence" and module.get("id") != "medication"
    }
    residence = get_profile_residence(profile, locale)
    medication_enabled = any(
        module.get("id") == "medication" and module.get("enabled", True)
        for module in get_scoring_modules(config)
    )

    monthly_data = {
        "start_date": month_dates[0],
        "end_date": month_dates[-1],
        "month_key": month_dates[0][:7],
        "dates": month_dates,
        "calendar_days": len(month_dates),
        "conditions": conditions,
        "condition_text": condition_text,
        "primary_condition": primary_condition,
        "diet_principle": build_multi_condition_tip(locale, conditions, standards),
        "residence_text": residence.get("display_name", ""),
        "weights": [],
        "body_fat_percent": [],
        "water_intakes": [],
        "steps": [],
        "calories": [],
        "protein": [],
        "fat": [],
        "carb": [],
        "fiber": [],
        "daily_records": [],
        "blood_pressure_records": [],
        "glucose_records": [],
        "custom_numeric_metrics": defaultdict(lambda: {"label": "", "unit": "", "section": "", "points": []}),
        "symptom_distribution": defaultdict(int),
        "observed_days": 0,
        "recorded_meal_days": 0,
        "valid_weight_days": 0,
        "water_goal_days": 0,
        "step_goal_days": 0,
        "diet_goal_days": 0,
        "exercise_days": 0,
        "symptom_days": 0,
        "symptom_events": 0,
        "medication_days": 0,
        "monitoring_days": 0,
        "medication_enabled": medication_enabled,
        "residence": residence,
        "population_branch": get_population_branch(config=config, user_profile=profile, primary_condition=primary_condition),
    }

    first_weight = None
    last_weight = None
    water_target = int(profile.get("water_target_ml", 2000) or 2000)
    step_target = int(profile.get("step_target", 8000) or 8000)

    for date_str in month_dates:
        file_path = os.path.join(memory_dir, f"{date_str}.md")
        daily_data = parse_memory_file(file_path)
        daily_data["date"] = daily_data.get("date") or date_str
        filtered_custom_sections = {
            header: items
            for header, items in (daily_data.get("custom_sections", {}) or {}).items()
            if not should_ignore_custom_section(header) and is_monitoring_section_title(header, allowed_monitoring_titles)
        }
        daily_data["custom_sections"] = filtered_custom_sections

        merge_dynamic_custom_sections(custom_rollup, filtered_custom_sections)
        monitoring_items_today = 0
        for stats in custom_rollup.values():
            items = find_custom_section_items(filtered_custom_sections, stats.get("section_title", stats.get("title", "")))
            if items:
                stats["days_recorded"] += 1
                stats["items"] += len(items)
                stats["latest_items"] = items[-4:]
                monitoring_items_today += len(items)

        structured = extract_structured_metrics(file_path, daily_data)
        score_report = build_score_report(daily_data, config)
        water_total = int(daily_data.get("water_total", 0) or 0)
        steps = int(daily_data.get("steps", 0) or 0)
        exercise_calories = sum(float(item.get("calories", 0) or 0) for item in daily_data.get("exercise_records", []))
        symptom_count = daily_symptom_count(daily_data)
        symptom_labels = extract_symptom_labels(daily_data, locale)
        medication_records = daily_data.get("medication_records", [])
        weight_value = daily_data.get("weight_morning")
        body_fat_percent = structured.get("body_fat_percent")

        monitoring_present = any(
            [
                weight_value is not None,
                body_fat_percent is not None,
                monitoring_items_today > 0,
                bool(structured.get("blood_pressure")),
                bool(structured.get("glucose")),
                bool(structured.get("custom_numeric_metrics")),
            ]
        )
        has_data = any(
            [
                bool(daily_data.get("meals")),
                bool(daily_data.get("water_records")),
                bool(daily_data.get("exercise_records")),
                bool(daily_data.get("custom_sections")),
                bool(medication_records),
                symptom_count > 0,
                water_total > 0,
                steps > 0,
                weight_value is not None,
                monitoring_present,
            ]
        )

        if has_data:
            monthly_data["observed_days"] += 1
        if daily_data.get("meals"):
            monthly_data["recorded_meal_days"] += 1
        if daily_data.get("exercise_records") or steps > 0:
            monthly_data["exercise_days"] += 1
        if symptom_count > 0:
            monthly_data["symptom_days"] += 1
            monthly_data["symptom_events"] += symptom_count
        for label in symptom_labels:
            monthly_data["symptom_distribution"][label] += 1
        if medication_records:
            monthly_data["medication_days"] += 1
        if monitoring_present:
            monthly_data["monitoring_days"] += 1
        if water_total >= water_target:
            monthly_data["water_goal_days"] += 1
        if steps >= step_target:
            monthly_data["step_goal_days"] += 1

        diet_score = score_report.get("module_map", {}).get("diet", {}).get("raw", 0)
        if diet_score >= 80:
            monthly_data["diet_goal_days"] += 1

        monthly_data["weights"].append(weight_value)
        monthly_data["body_fat_percent"].append(body_fat_percent)
        if weight_value is not None:
            monthly_data["valid_weight_days"] += 1
            if first_weight is None:
                first_weight = weight_value
            last_weight = weight_value

        for item in structured.get("blood_pressure", []):
            monthly_data["blood_pressure_records"].append({"date": date_str, **item})
        for item in structured.get("glucose", []):
            monthly_data["glucose_records"].append({"date": date_str, **item})
        for item in structured.get("custom_numeric_metrics", []):
            key = f"{slugify(item.get('section'))}:{slugify(item.get('label'))}:{item.get('unit', '')}"
            monthly_data["custom_numeric_metrics"][key]["label"] = item.get("label", "")
            monthly_data["custom_numeric_metrics"][key]["unit"] = item.get("unit", "")
            monthly_data["custom_numeric_metrics"][key]["section"] = item.get("section", "")
            monthly_data["custom_numeric_metrics"][key]["points"].append(
                {
                    "date": date_str,
                    "value": item.get("value"),
                }
            )

        monthly_data["water_intakes"].append(water_total)
        monthly_data["steps"].append(steps)
        monthly_data["calories"].append(daily_data.get("total_calories", 0))
        monthly_data["protein"].append(daily_data.get("total_protein", 0))
        monthly_data["fat"].append(daily_data.get("total_fat", 0))
        monthly_data["carb"].append(daily_data.get("total_carb", 0))
        monthly_data["fiber"].append(daily_data.get("total_fiber", 0))
        monthly_data["daily_records"].append(
            {
                "date": date_str,
                "has_data": has_data,
                "score": score_report.get("total", 0),
                "diet_score": diet_score,
                "water_total": water_total,
                "steps": steps,
                "calories": daily_data.get("total_calories", 0),
                "exercise_calories": exercise_calories,
                "exercise_count": len(daily_data.get("exercise_records", [])),
                "protein": daily_data.get("total_protein", 0),
                "carb": daily_data.get("total_carb", 0),
                "fiber": daily_data.get("total_fiber", 0),
                "weight": weight_value,
                "body_fat_percent": body_fat_percent,
                "fat": daily_data.get("total_fat", 0),
                "symptom_count": symptom_count,
                "symptom_labels": symptom_labels,
                "medication_count": len(medication_records),
                "monitoring_count": monitoring_items_today + len(structured.get("blood_pressure", [])) + len(structured.get("glucose", [])),
            }
        )

    divisor = max(1, monthly_data["observed_days"])
    valid_weights = [value for value in monthly_data["weights"] if value is not None]
    valid_bodyfat = [value for value in monthly_data["body_fat_percent"] if value is not None]
    scored_days = [record["score"] for record in monthly_data["daily_records"] if record.get("has_data")]
    diet_days = [record["diet_score"] for record in monthly_data["daily_records"] if record.get("diet_score", 0) > 0]

    monthly_data["avg_weight"] = safe_average(valid_weights)
    monthly_data["latest_weight"] = last_weight
    monthly_data["weight_change"] = (last_weight - first_weight) if (last_weight is not None and first_weight is not None) else 0
    monthly_data["avg_body_fat_percent"] = safe_average(valid_bodyfat)
    monthly_data["avg_calories"] = sum(monthly_data["calories"]) / divisor
    monthly_data["avg_water"] = sum(monthly_data["water_intakes"]) / divisor
    monthly_data["avg_steps"] = sum(monthly_data["steps"]) / divisor
    monthly_data["avg_protein"] = sum(monthly_data["protein"]) / divisor
    monthly_data["avg_fat"] = sum(monthly_data["fat"]) / divisor
    monthly_data["avg_carb"] = sum(monthly_data["carb"]) / divisor
    monthly_data["avg_fiber"] = sum(monthly_data["fiber"]) / divisor
    monthly_data["avg_total_score"] = safe_average(scored_days)
    monthly_data["avg_diet_score"] = safe_average(diet_days)
    monthly_data["custom_section_stats"] = sorted(custom_rollup.values(), key=lambda item: (item.get("days_recorded", 0), item.get("items", 0), item.get("title", "")), reverse=True)
    monthly_data["symptom_distribution"] = dict(
        sorted(monthly_data["symptom_distribution"].items(), key=lambda item: (-item[1], item[0]))
    )

    medication_expected = medication_enabled or monthly_data["medication_days"] > 0
    monthly_data["macro_scores"] = {
        "diet": round(monthly_data["diet_goal_days"] / divisor * 100, 1),
        "water": round(monthly_data["water_goal_days"] / divisor * 100, 1),
        "exercise": round(((monthly_data["step_goal_days"] / divisor) * 0.65 + (monthly_data["exercise_days"] / divisor) * 0.35) * 100, 1),
        "medication": 100.0 if not medication_expected else round(monthly_data["medication_days"] / divisor * 100, 1),
        "monitoring": round(monthly_data["monitoring_days"] / divisor * 100, 1),
    }

    # 构建头部卡片数据
    valid_weights = [w for w in monthly_data["weights"] if w is not None]
    first_weight = valid_weights[0] if valid_weights else None
    last_weight = valid_weights[-1] if valid_weights else None
    weight_change = (last_weight - first_weight) if (last_weight is not None and first_weight is not None) else 0
    
    monthly_data["overview"] = {
        "avg_score": monthly_data.get("avg_total_score", 0),
        "trend": "stable",
        "total_days": monthly_data["observed_days"],
        "condition": primary_condition,
    }
    
    monthly_data["weight_summary"] = {
        "start": first_weight or 0,
        "end": last_weight or 0,
        "change": weight_change,
    }
    
    monthly_data["medication_summary"] = {
        "total_days": monthly_data["medication_days"],
        "expected_days": monthly_data["observed_days"] if medication_enabled else 0,
        "adherence_rate": (monthly_data["medication_days"] / max(1, monthly_data["observed_days"])) * 100 if medication_enabled else 0,
    }
    
    monthly_data["symptom_summary"] = {
        "total_symptom_days": monthly_data["symptom_days"],
        "total_symptom_events": monthly_data["symptom_events"],
        "symptom_distribution": monthly_data["symptom_distribution"],
    }

    monthly_data["ultrasound_summary"] = extract_gallstone_ultrasound_summary(memory_dir)
    return monthly_data


def build_monthly_highlights(monthly_data: dict, profile: dict, locale: str) -> List[str]:
    highlights = []
    macro_scores = monthly_data.get("macro_scores", {})
    is_ja = resolve_locale(locale=locale) == "ja-JP"
    score_pairs = [
        ("diet", localize(locale, "饮食", "diet")),
        ("water", localize(locale, "饮水", "hydration")),
        ("exercise", localize(locale, "运动", "exercise")),
        ("medication", localize(locale, "用药", "medication")),
        ("monitoring", localize(locale, "监测", "monitoring")),
    ]
    best_key, best_label = max(score_pairs, key=lambda item: macro_scores.get(item[0], 0))
    if is_ja:
        highlights.append(f"今月は {best_label} の達成率がもっとも高く、およそ {macro_scores.get(best_key, 0):.0f}% でした。")
    else:
        highlights.append(
            localize(
                locale,
                f"本月 {best_label} 维度完成度最高，约 {macro_scores.get(best_key, 0):.0f}%。",
                f"{best_label.capitalize()} was the strongest adherence dimension this month at about {macro_scores.get(best_key, 0):.0f}%.",
            )
        )

    if monthly_data.get("symptom_days", 0) == 0:
        highlights.append("今月は目立った症状の記録がなく、全体状態は比較的安定していました。" if is_ja else localize(locale, "本月未记录明显症状，整体状态比较平稳。", "No clear symptom day was recorded this month, suggesting a steady overall state."))
    else:
        highlights.append(
            f"今月は {monthly_data['symptom_days']} 日で不調があり、合計 {monthly_data['symptom_events']} 回記録されました。誘因の振り返りが必要です。"
            if is_ja
            else localize(
                locale,
                f"本月有 {monthly_data['symptom_days']} 天出现不适，共 {monthly_data['symptom_events']} 次，需重点复盘诱因。",
                f"Symptoms were logged on {monthly_data['symptom_days']} days ({monthly_data['symptom_events']} events) and deserve closer trigger review.",
            )
        )

    weight_change = monthly_data.get("weight_change", 0)
    primary_condition = monthly_data.get("primary_condition")
    if monthly_data.get("latest_weight") is not None:
        if primary_condition == "fat_loss" and weight_change < 0:
            highlights.append(f"体重は月初より {abs(weight_change):.2f}kg 減少し、減脂目標と同じ方向に進んでいます。" if is_ja else localize(locale, f"体重较月初下降 {abs(weight_change):.2f}kg，方向与减脂目标一致。", f"Weight moved down by {abs(weight_change):.2f}kg from the start of the month, which aligns with fat-loss goals."))
        elif abs(weight_change) <= 0.6:
            highlights.append(f"今月の体重変動は約 {abs(weight_change):.2f}kg で、比較的安定していました。" if is_ja else localize(locale, f"体重月内波动约 {abs(weight_change):.2f}kg，整体比较稳定。", f"Weight fluctuated by about {abs(weight_change):.2f}kg this month and stayed relatively stable."))
        else:
            highlights.append(f"今月の体重変動は {abs(weight_change):.2f}kg に達しており、食事と活動をあわせて振り返る価値があります。" if is_ja else localize(locale, f"体重月内波动达到 {abs(weight_change):.2f}kg，建议和饮食、活动一起复盘。", f"Weight fluctuated by {abs(weight_change):.2f}kg this month, so meals and activity deserve a joint review."))

    if monthly_data.get("medication_enabled"):
        highlights.append(
            f"服薬記録は {monthly_data.get('medication_days', 0)} 日分あり、月報では遵守状況とリスク評価に反映されています。"
            if is_ja
            else localize(
                locale,
                f"用药记录覆盖 {monthly_data.get('medication_days', 0)} 天，月报已纳入依从性与风险评估。",
                f"Medication was logged on {monthly_data.get('medication_days', 0)} days and is now part of the adherence and risk review.",
            )
        )

    if monthly_data.get("monitoring_days", 0) > 0:
        highlights.append(
            f"モニタリング項目は {monthly_data.get('monitoring_days', 0)} 日分記録されており、複数指標を横断した傾向判断に使えます。"
            if is_ja
            else localize(
                locale,
                f"监测模块有 {monthly_data.get('monitoring_days', 0)} 天记录，可用于联合判断趋势。",
                f"Monitoring modules were logged on {monthly_data.get('monitoring_days', 0)} days, which gives us cross-metric trend visibility.",
            )
        )

    return dedupe_preserve_order(highlights)[:5]


def build_specialty_charts(monthly_data: dict, config: dict, locale: str) -> List[dict]:
    charts = []
    standards = get_condition_standards(config, monthly_data.get("conditions", []))
    daily_records = monthly_data.get("daily_records", [])
    conditions = monthly_data.get("conditions", [])
    primary_condition = monthly_data.get("primary_condition")
    lifestyle_mode = is_lifestyle_mode(primary_condition, monthly_data.get("population_branch"))
    is_ja = resolve_locale(locale=locale) == "ja-JP"

    if lifestyle_mode:
        deficit_target = 350 if str(primary_condition) == "fat_loss" else 150
        charts.extend(
            [
                {
                    "type": "energy_deficit",
                    "title": localize_three(
                        locale,
                        "能量收支与代谢缺口",
                        "Energy Balance And Deficit",
                        "エネルギー収支と代謝ギャップ",
                    ),
                    "subtitle": localize_three(
                        locale,
                        "绿色柱代表估算总消耗，橙色或红色柱代表当日摄入，虚线表示本月建议的热量目标线。",
                        "Green bars show estimated total expenditure, orange or red bars show daily intake, and the dashed line marks the suggested intake ceiling.",
                        "緑の棒は推定総消費、オレンジまたは赤の棒は当日の摂取量、破線は今月の推奨摂取目安です。",
                    ),
                    "records": daily_records,
                    "deficit_target_kcal": deficit_target,
                    "summary": localize_three(
                        locale,
                        f"本月日均摄入约 {monthly_data.get('avg_calories', 0):.0f} kcal，对照估算总消耗后，可以直接看出哪些日期维持平衡、哪些日期真正形成了热量赤字。",
                        f"Average intake was about {monthly_data.get('avg_calories', 0):.0f} kcal this month, so the chart shows which days stayed near maintenance and which days created a real deficit.",
                        f"今月の平均摂取量は約 {monthly_data.get('avg_calories', 0):.0f} kcal で、推定総消費と重ねることで維持日と赤字日を見分けやすくなります。",
                    ),
                },
                {
                    "type": "weekly_progression",
                    "title": localize_three(
                        locale,
                        "四周习惯养成趋势对比",
                        "Four-Week Habit Progression",
                        "4週間の習慣推移比較",
                    ),
                    "subtitle": localize_three(
                        locale,
                        "按 W1-W4 拆分本月节奏，分别比较步数、饮水与热量的阶段性变化。",
                        "This compares weekly averages for steps, hydration, and calories across W1-W4.",
                        "W1-W4 に分けて、歩数・飲水量・カロリーの週次変化を比較します。",
                    ),
                    "records": daily_records,
                    "summary": localize_three(
                        locale,
                        "如果前半月执行更稳、后半月明显回落，这组图会比单日曲线更容易看出习惯松动的位置。",
                        "These weekly bars make it easier to spot whether habits improved over time or faded in the second half of the month.",
                        "日次推移よりも、月前半で安定していたのか、後半で崩れたのかを見分けやすい構成です。",
                    ),
                },
            ]
        )

        body_comp_records = [
            record
            for record in daily_records
            if record.get("weight") is not None and record.get("body_fat_percent") is not None
        ]
        if len(body_comp_records) >= 2:
            charts.append(
                {
                    "type": "body_composition_area",
                    "title": localize_three(
                        locale,
                        "去脂体重与脂肪重量变化",
                        "Lean Mass And Fat Mass Trend",
                        "除脂肪体重と脂肪量の推移",
                    ),
                    "subtitle": localize_three(
                        locale,
                        "根据体重和体脂率拆分出瘦体重与脂肪重量，帮助判断减下来的到底是什么。",
                        "Weight and body-fat records are decomposed into lean mass and fat mass so the quality of progress is easier to judge.",
                        "体重と体脂率から除脂肪体重と脂肪量を分けて、何が減っているのかを判断しやすくします。",
                    ),
                    "records": body_comp_records,
                    "summary": localize_three(
                        locale,
                        "若体重下降主要来自脂肪层收缩，说明策略更健康；若瘦体重同步下滑，则要重新检查蛋白质、力量训练与恢复质量。",
                        "If the decline is driven mainly by fat mass, progress is usually healthier; if lean mass also drops, protein, resistance work, and recovery need a closer look.",
                        "脂肪量の縮小が中心なら順調ですが、除脂肪体重も落ちている場合はたんぱく質・筋トレ・回復の見直しが必要です。",
                    ),
                }
            )

        for metric in sorted(monthly_data.get("custom_numeric_metrics", {}).values(), key=lambda item: len(item.get("points", [])), reverse=True):
            if len(metric.get("points", [])) < 2:
                continue
            charts.append(
                {
                    "type": "custom_metric",
                    "title": localize(locale, f"额外监测：{metric.get('section')} · {metric.get('label')}", f"Additional monitoring: {metric.get('section')} · {metric.get('label')}"),
                    "subtitle": localize(locale, "来自自定义监测模块的数值趋势。", "Numeric trend extracted from a custom monitoring module."),
                    "section": metric.get("section"),
                    "label": metric.get("label"),
                    "unit": metric.get("unit"),
                    "points": metric.get("points", []),
                    "summary": localize(locale, f"该指标来自“{metric.get('section')}”模块，当前已有 {len(metric.get('points', []))} 个数值点，后续会继续参与月度趋势分析。", f"This metric comes from the '{metric.get('section')}' module and already has {len(metric.get('points', []))} numeric points for monthly trend analysis."),
                }
            )
        if resolve_locale(locale=locale) == "ja-JP":
            for chart in charts:
                for key in ("title", "subtitle", "summary", "healthy_legend", "symptom_legend", "section", "label", "unit"):
                    if chart.get(key):
                        chart[key] = sanitize_locale_line(locale, str(chart.get(key)))
        return charts[:6]

    if "gallstones" in conditions:
        symptom_days = [record for record in daily_records if record.get("symptom_count", 0) > 0]
        fat_on_symptom = safe_average([record.get("fat") for record in symptom_days]) if symptom_days else 0
        fat_on_calm = safe_average([record.get("fat") for record in daily_records if record.get("symptom_count", 0) == 0 and record.get("fat", 0) > 0])
        charts.append(
            {
                "type": "gallstones",
                "title": "胆石: 脂質摂取量と症状頻度" if is_ja else localize(locale, "胆结石：脂肪摄入 vs 症状频次", "Gallstones: Fat intake vs symptom frequency"),
                "subtitle": "左軸は日ごとの脂質量、右軸はその日の症状回数です。" if is_ja else localize(locale, "双轴对照：左轴为每日脂肪克数，右轴为当天症状次数。", "Dual-axis view: daily fat grams on the left axis, symptom count on the right."),
                "records": daily_records,
                "fat_target": standards.get("fat_max_g"),
                "summary": (
                    f"症状があった日の平均脂質摂取は約 {fat_on_symptom:.1f}g、落ち着いていた日は約 {fat_on_calm:.1f}g でした。差が広がる場合は、脂質管理と症状の関連を重点的に見直してください。"
                    if is_ja
                    else localize(
                        locale,
                        f"症状日的平均脂肪摄入约 {fat_on_symptom:.1f}g，平稳日约 {fat_on_calm:.1f}g。若两者差距持续扩大，说明油脂控制与症状关系更值得重点关注。",
                        f"Average fat intake was about {fat_on_symptom:.1f}g on symptom days versus {fat_on_calm:.1f}g on calmer days. If that gap keeps widening, fat control is likely a major trigger to review.",
                    )
                ),
            }
        )
        intake_records = [record for record in daily_records if record.get("fat", 0) > 0 or record.get("carb", 0) > 0]
        if len(intake_records) >= 3:
            fat_values = [float(record.get("fat", 0) or 0) for record in intake_records if record.get("fat", 0) > 0]
            carb_values = [float(record.get("carb", 0) or 0) for record in intake_records if record.get("carb", 0) > 0]
            if len(fat_values) >= 3 and len(carb_values) >= 3:
                charts.append(
                    {
                        "type": "intake_boxplot",
                        "title": "胆石: 脂質 / 炭水化物のばらつき" if is_ja else localize(locale, "胆结石：脂肪 / 碳水摄入离散度", "Gallstones: Fat and carb intake spread"),
                        "subtitle": "箱ひげ図で、普段は安定していても一部の日だけ摂取量が跳ねるパターンを見つけます。" if is_ja else localize(locale, "用箱线图识别“平时很稳、偶尔暴冲”的摄入异常日。", "A boxplot helps spot unusually high-intake days that averages can hide."),
                        "records": intake_records,
                        "summary": (
                            f"今月の脂質平均は約 {safe_average(fat_values):.1f}g、炭水化物平均は約 {safe_average(carb_values):.1f}g でした。外れ値が高い日は、夕食と間食の内容を見直してください。"
                            if is_ja
                            else localize(
                                locale,
                                f"本月脂肪均值约 {safe_average(fat_values):.1f}g，碳水均值约 {safe_average(carb_values):.1f}g。若离群点明显偏高，建议回看对应日期的晚餐和加餐。",
                                f"Typical fat intake stayed around {safe_average(fat_values):.1f}g and carbs around {safe_average(carb_values):.1f}g. If outliers rise far above the box, revisit those dinner and snack days.",
                            )
                        ),
                    }
                )

    symptom_distribution = monthly_data.get("symptom_distribution", {})
    total_days = int(monthly_data.get("calendar_days", len(monthly_data.get("dates", [])) or 0) or 0)
    symptom_days_count = int(monthly_data.get("symptom_days", 0) or 0)
    healthy_days = max(total_days - symptom_days_count, 0)
    top_labels = list(symptom_distribution.items())[:3]
    top_symptom_text = (
        "、".join(f"{label} {count}次" for label, count in top_labels)
        if resolve_locale(locale=locale) == "zh-CN"
        else "、".join(f"{label} {count}回" for label, count in top_labels) if is_ja else ", ".join(f"{label} {count}x" for label, count in top_labels)
    )
    if total_days > 0:
        completion_rate = int(healthy_days / max(total_days, 1) * 100)
        symptom_legend_text = (
            (f"不調あり: {symptom_days_count} 日（{top_symptom_text or '今月は詳細な症状分類なし'}）" if is_ja else localize(locale, f"出现不适：{symptom_days_count} 天（{top_symptom_text or '本月未细分症状'}）", f"Symptoms present: {symptom_days_count} days ({top_symptom_text or 'no symptom subtype logged'})"))
            if symptom_days_count > 0
            else ("不調あり: 0 日" if is_ja else localize(locale, "出现不适：0 天", "Symptoms present: 0 days"))
        )
        charts.append(
            {
                "type": "symptom_distribution",
                "title": "健康達成ドーナツ: 健康日数と不調日数" if is_ja else localize(locale, "健康达标环形图：本月健康天数 vs 出现不适天数", "Healthy-day donut: symptom-free days vs symptom days"),
                "subtitle": "今月の総日数を基準に、無症状の日数と不調日数の比率を確認します。" if is_ja else localize(locale, "以当月总天数为基数，直观看清健康无症状天数与出现不适天数的比例。", "This donut uses the full month as the baseline so healthy days and symptom days are easier to compare."),
                "distribution": symptom_distribution,
                "calendar_days": total_days,
                "healthy_days": healthy_days,
                "symptom_days": symptom_days_count,
                "completion_rate": completion_rate,
                "healthy_legend": f"健康で無症状: {healthy_days} 日" if is_ja else localize(locale, f"健康无症状：{healthy_days} 天", f"Healthy symptom-free: {healthy_days} days"),
                "symptom_legend": symptom_legend_text,
                "summary": (
                    f"今月は {total_days} 日中 {healthy_days} 日が無症状で、健康達成率は約 {completion_rate:.0f}% でした。"
                    + (f" 不調があった {symptom_days_count} 日では、主に {top_symptom_text} が見られました。" if top_symptom_text else "")
                    if is_ja
                    else localize(
                        locale,
                        f"本月共 {total_days} 天，其中 {healthy_days} 天未记录不适，健康达标约 {completion_rate:.0f}%。{f'出现不适的 {symptom_days_count} 天主要表现为：{top_symptom_text}。' if top_symptom_text else ''}",
                        f"There were {total_days} days this month, with {healthy_days} symptom-free days and a healthy-day completion rate of about {completion_rate:.0f}%. {f'Symptom days were mainly driven by: {top_symptom_text}.' if top_symptom_text else ''}",
                    )
                ),
            }
        )

    if "hypertension" in conditions and monthly_data.get("blood_pressure_records"):
        bp_records = monthly_data.get("blood_pressure_records", [])
        systolic = [item["systolic"] for item in bp_records if item.get("systolic")]
        diastolic = [item["diastolic"] for item in bp_records if item.get("diastolic")]
        charts.append(
            {
                "type": "hypertension",
                "title": localize(locale, "高血压：30 天血压波动箱线图", "Hypertension: 30-day blood pressure boxplot"),
                "subtitle": localize(locale, "观察收缩压与舒张压的中位数、离散度与极值范围。", "This highlights median values, spread, and outlier range for systolic and diastolic pressure."),
                "bp_records": bp_records,
                "summary": localize(
                    locale,
                    f"本月收缩压均值约 {safe_average(systolic):.0f} mmHg，舒张压均值约 {safe_average(diastolic):.0f} mmHg。箱体越宽，说明波动越大，越需要结合作息、盐分和服药时间复盘。",
                    f"Average systolic pressure was about {safe_average(systolic):.0f} mmHg and average diastolic pressure was about {safe_average(diastolic):.0f} mmHg. A wider box means greater variability and a stronger need to review sleep, sodium, and medication timing.",
                ),
            }
        )

    if "diabetes" in conditions and monthly_data.get("glucose_records"):
        glucose_records = monthly_data.get("glucose_records", [])
        avg_glucose = safe_average([item.get("value") for item in glucose_records])
        charts.append(
            {
                "type": "diabetes",
                "title": localize(locale, "糖尿病：血糖监测趋势", "Diabetes: Glucose monitoring trend"),
                "subtitle": localize(locale, "用于观察月内血糖波动与高值出现频率。", "Use this to inspect intra-month glucose swings and the frequency of elevated readings."),
                "glucose_records": glucose_records,
                "summary": localize(
                    locale,
                    f"本月已记录 {len(glucose_records)} 次血糖，均值约 {avg_glucose:.1f} mmol/L。建议结合餐后时点和主食份量一起看高值出现的位置。",
                    f"{len(glucose_records)} glucose readings were logged this month with an average of about {avg_glucose:.1f} mmol/L. Elevated points should be reviewed together with meal timing and carb portions.",
                ),
            }
        )

    if "fat_loss" in conditions and any(record.get("weight") is not None for record in daily_records):
        bodyfat_days = sum(1 for record in daily_records if record.get("body_fat_percent") is not None)
        charts.append(
            {
                "type": "fat_loss",
                "title": localize(locale, "健身减脂：体重与体脂率平滑趋势", "Fat loss: Smoothed weight and body-fat trend"),
                "subtitle": localize(locale, "粗线表示平滑后的趋势，便于识别真实变化方向。", "The thicker line shows a smoothed trend so the real direction is easier to read."),
                "records": daily_records,
                "summary": localize(
                    locale,
                    f"本月共有 {monthly_data.get('valid_weight_days', 0)} 天体重记录，{bodyfat_days} 天体脂记录。若体重下降但体脂不降，说明仍需优化蛋白、力量训练与恢复。",
                    f"There were {monthly_data.get('valid_weight_days', 0)} weight days and {bodyfat_days} body-fat days this month. If weight drops but body fat does not, protein intake, strength training, and recovery still need work.",
                ),
            }
        )

    for metric in sorted(monthly_data.get("custom_numeric_metrics", {}).values(), key=lambda item: len(item.get("points", [])), reverse=True):
        if len(metric.get("points", [])) < 2:
            continue
        charts.append(
            {
                "type": "custom_metric",
                "title": localize(locale, f"附加监测：{metric.get('section')} · {metric.get('label')}", f"Additional monitoring: {metric.get('section')} · {metric.get('label')}"),
                "subtitle": localize(locale, "来自自定义监测模块的数值趋势。", "Numeric trend extracted from a custom monitoring module."),
                "section": metric.get("section"),
                "label": metric.get("label"),
                "unit": metric.get("unit"),
                "points": metric.get("points", []),
                "summary": localize(locale, f"该指标来自“{metric.get('section')}”模块，当前已累计 {len(metric.get('points', []))} 个数值点，后续可继续用于月度趋势分析。", f"This metric comes from the '{metric.get('section')}' module and already has {len(metric.get('points', []))} numeric points for monthly trend analysis."),
            }
        )
    if resolve_locale(locale=locale) == "ja-JP":
        for chart in charts:
            for key in ("title", "subtitle", "summary", "healthy_legend", "symptom_legend", "section", "label", "unit"):
                if chart.get(key):
                    chart[key] = sanitize_locale_line(locale, str(chart.get(key)))
    return charts[:6]


def build_follow_up_reminders(monthly_data: dict, profile: dict, locale: str) -> List[str]:
    reminders = []
    conditions = monthly_data.get("conditions", [])
    symptom_days = monthly_data.get("symptom_days", 0)
    ultrasound = monthly_data.get("ultrasound_summary", {})
    primary_condition = monthly_data.get("primary_condition")
    is_ja = resolve_locale(locale=locale) == "ja-JP"

    if is_lifestyle_mode(primary_condition, monthly_data.get("population_branch")):
        reminders.append(
            localize_three(
                locale,
                "建议每 4-6 周固定复盘一次体重、体脂率、围度、睡眠与训练恢复，避免只看体重单一指标。",
                "Review weight, body fat, measurements, sleep, and training recovery every 4-6 weeks instead of relying on weight alone.",
                "体重だけでなく、体脂率・囲み寸法・睡眠・回復も含めて 4〜6 週ごとに見直すのがおすすめです。",
            )
        )
        reminders.append(
            localize_three(
                locale,
                "可把血压、空腹血糖、血脂、肝肾功能等基础体测安排为季度或年度筛查，用来验证当前饮食和运动习惯是否真正稳住。",
                "Basic screening such as blood pressure, fasting glucose, lipids, and liver-kidney markers can be scheduled quarterly or annually to validate whether current habits are truly sustainable.",
                "血圧・空腹時血糖・脂質・肝腎機能などの基礎チェックを四半期または年次で行うと、今の習慣が本当に安定しているかを確認しやすくなります。",
            )
        )
        if monthly_data.get("valid_weight_days", 0) < max(4, monthly_data.get("observed_days", 0) // 4):
            reminders.append(
                localize_three(
                    locale,
                    "当前体重/体脂记录还不够密，建议下月固定每周至少 2-3 次在同一时段测量，避免趋势图被稀疏数据拉偏。",
                    "Weight and body-fat logging are still sparse, so next month should include at least 2-3 measurements per week at a consistent time.",
                    "体重や体脂率の記録密度がまだ低いため、来月は毎週 2〜3 回以上、同じ時間帯で測ると推移が安定します。",
                )
            )
        if str(primary_condition) == "fat_loss":
            if abs(float(monthly_data.get("weight_change", 0) or 0)) > 2.5:
                reminders.append(
                    localize_three(
                        locale,
                        "若月内减重过快，建议把下月目标调回更温和的赤字，并同步关注睡眠、疲劳感和训练表现，必要时做一次基础营养评估。",
                        "If weight is dropping too quickly, ease the deficit next month and monitor sleep, fatigue, and training performance together with a basic nutrition check.",
                        "減量ペースが速すぎる場合は、来月の赤字を少し緩めて、睡眠・疲労感・トレーニングの質も一緒に確認してください。",
                    )
                )
            else:
                reminders.append(
                    localize_three(
                        locale,
                        "减脂模式下可每月检查一次去脂体重与脂肪重量走势，确认掉下来的主要是脂肪而不是肌肉。",
                        "In fat-loss mode, review lean mass and fat mass at least monthly to confirm that progress is driven mainly by fat loss rather than muscle loss.",
                        "減脂モードでは、月 1 回は除脂肪体重と脂肪量を見直し、筋肉ではなく脂肪が主に減っているかを確認しましょう。",
                    )
                )
        else:
            reminders.append(
                localize_three(
                    locale,
                    "健康维持模式下，建议把作息、步数、饮水和三大营养素的月均稳定性放在首位，再逐步增加力量训练或灵活性训练模块。",
                    "In balanced-wellness mode, prioritize the month-to-month stability of sleep, steps, hydration, and macro intake before expanding strength or mobility work.",
                    "バランス重視モードでは、まず睡眠・歩数・飲水・三大栄養素の安定性を整えてから、筋トレや柔軟性トレーニングを広げるのがおすすめです。",
                )
            )
        return dedupe_preserve_order(reminders)[:6]

    if "gallstones" in conditions:
        reminders.append("空腹での肝胆膵脾エコーと肝機能検査は、少なくとも四半期に 1 回を目安に再確認してください。" if is_ja else localize(locale, "肝胆胰脾彩超（空腹）+ 肝功能，建议按季度完成一次复查。", "A fasting hepatobiliary ultrasound plus liver-function labs should be reviewed at least once per quarter."))
        if symptom_days >= 3 or ultrasound.get("latest_size_cm", 0) >= 2 or ultrasound.get("wall_warning"):
            reminders.append("今月は高リスクのサインが見られるため、肝胆外科または一般外科の専門外来を早めに予約し、追加介入の要否を確認してください。" if is_ja else localize(locale, "本月已出现较高风险信号，建议尽快预约肝胆外科或普外科专家门诊评估是否需要进一步干预。", "Higher-risk signals appeared this month, so a hepatobiliary or general-surgery specialist visit should be arranged soon to evaluate further intervention."))
        elif ultrasound.get("latest_size_cm"):
            reminders.append(f"直近のエコーでは最大結石径が約 {ultrasound.get('latest_size_cm'):.1f}cm でした。症状が再び増える場合は、次の四半期を待たずに再評価してください。" if is_ja else localize(locale, f"最近一次超声记录最大结石约 {ultrasound.get('latest_size_cm'):.1f}cm，若症状重新增多，不要拖到下季度再评估。", f"The latest ultrasound recorded a largest stone of about {ultrasound.get('latest_size_cm'):.1f}cm. If symptoms pick up again, do not wait until next quarter to re-evaluate."))

    if "hypertension" in conditions:
        reminders.append(localize(locale, "建议保留连续 7 天晨起和睡前家庭血压记录，复诊时一并带给医生。", "Keep a 7-day home blood-pressure log with morning and bedtime readings and bring it to follow-up visits."))
        high_bp_count = sum(1 for item in monthly_data.get("blood_pressure_records", []) if item.get("systolic", 0) >= 140 or item.get("diastolic", 0) >= 90)
        if high_bp_count >= 3:
            reminders.append(localize(locale, "本月多次出现偏高血压，建议 2-4 周内复诊心内科或高血压门诊。", "Repeated high blood-pressure readings were logged this month, so a cardiology or hypertension-clinic follow-up within 2-4 weeks is reasonable."))

    if "diabetes" in conditions:
        reminders.append(localize(locale, "建议至少每 3 个月复查 HbA1c，并结合空腹血糖与餐后血糖一起判断。", "Review HbA1c at least every 3 months and interpret it together with fasting and post-meal glucose readings."))
        high_glucose_count = sum(1 for item in monthly_data.get("glucose_records", []) if item.get("value", 0) >= 10)
        if high_glucose_count >= 3:
            reminders.append(localize(locale, "本月已多次出现高血糖点位，建议尽快和内分泌门诊讨论饮食、运动与用药方案。", "Multiple high glucose readings appeared this month, so an endocrinology follow-up to review meals, activity, and medication is worth arranging soon."))

    if "fat_loss" in conditions:
        reminders.append(localize(locale, "减脂管理建议每 4-6 周复盘一次体重、体脂率、围度和训练恢复情况。", "For fat-loss management, review weight, body fat, measurements, and recovery every 4-6 weeks."))
        if abs(monthly_data.get("weight_change", 0)) < 0.2:
            reminders.append(localize(locale, "如果体重和体脂连续平台超过 4 周，可考虑营养门诊或运动康复门诊做一次结构化复盘。", "If both weight and body fat plateau for more than 4 weeks, a structured review with a nutrition or sports-medicine clinic may help."))

    if monthly_data.get("monitoring_days", 0) < max(5, monthly_data.get("observed_days", 0) // 3):
        reminders.append(localize(locale, "关键监测记录偏少，建议下个月优先补齐体重、症状和专项指标，再看月报会更有参考价值。", "Key monitoring data were still sparse. Next month, prioritize weight, symptoms, and specialty metrics so the monthly report becomes more actionable."))

    return dedupe_preserve_order(reminders)[:6]


def extract_doctor_name(text: str) -> str:
    raw_text = str(text or "")
    patterns = [
        r"([一-鿿]{2,4}?)\s*(副主任医师|主任医师|主治医师|副教授|教授|主任|副主任|医生|医师)",
        r"(Dr\.\s+[A-Z][a-z]+\s+[A-Z][a-z]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, raw_text)
        if match:
            if len(match.groups()) == 2:
                return "".join(match.groups())
            return match.group(1)
    return ""


def extract_hospital_name(text: str) -> str:
    raw_text = str(text or "")
    patterns = [
        r"([一-鿿]{2,24}(?:大学附属医院|附属医院|医院|医学中心|中医院|人民医院|妇幼保健院|医疗中心))",
        r"([A-Z][A-Za-z\s]+(?:Hospital|Medical Center|Clinic))",
    ]
    for pattern in patterns:
        match = re.search(pattern, raw_text)
        if match:
            hospital = match.group(1).strip()
            hospital = re.sub(r"^[一-鿿]{1,12}(?:主任医师|副主任医师|医生|医师)", "", hospital).strip()
            return hospital
    return ""


def trim_text(value: str, max_length: int) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    if len(text) <= max_length:
        return text
    clipped = text[: max_length - 1].rstrip(" ,.;，；、")
    return f"{clipped}…"


def strip_search_noise(text: str) -> str:
    raw = str(text or "")
    if not raw:
        return ""
    raw = re.sub(r"https?://\S+|www\.\S+", "", raw)
    raw = re.sub(r"(?:\b\d+:\d+\b\s*){1,3}", " ", raw)
    raw = re.sub(r"^\s*(?:\d+[.)、]\s*)+", "", raw)
    raw = re.sub(r"^\s*\d+\s+", "", raw)
    raw = re.sub(r"\[\d+\]", "", raw)
    raw = re.sub(r"(?:表|图|Table|Figure)\s*[-\d.]+", " ", raw, flags=re.IGNORECASE)
    raw = re.sub("|".join(re.escape(term) for term in SEARCH_NOISE_TERMS), " ", raw, flags=re.IGNORECASE)
    raw = re.sub(r"[|<>#@]+", " ", raw)
    raw = re.sub(r"[•·]{2,}", " ", raw)
    raw = re.sub(r"[.。…]{4,}", "…", raw)
    raw = re.sub(r"\s+", " ", raw).strip(" |，,.;；、-")
    return raw


def matches_locale_text(text: str, locale: str) -> bool:
    cleaned = str(text or "").strip()
    if not cleaned:
        return False
    resolved = resolve_locale(locale=locale)
    if resolved == "zh-CN":
        return len(re.findall(r"[一-鿿]", cleaned)) >= 4
    if resolved == "ja-JP":
        return bool(re.search(r"[\u3040-\u30ff]", cleaned)) or len(re.findall(r"[一-鿿]", cleaned)) >= 4
    return len(re.findall(r"[A-Za-z]{3,}", cleaned)) >= 5


def is_readable_text(value: str, locale: str) -> bool:
    text = strip_search_noise(value)
    if not text:
        return False
    if text.lstrip().startswith(("+", "•")):
        return False
    if text.rstrip().endswith(("e.g.", "e.g", "for example", "for exampl…")):
        return False
    compact = re.sub(r"\s+", "", text)
    if len(compact) < 14:
        return False
    if any(re.search(pattern, text, re.IGNORECASE) for pattern in SEARCH_BAD_PATTERNS):
        return False
    useful_chars = len(re.findall(r"[A-Za-z0-9一-鿿]", compact))
    weird_chars = len(re.findall(r"[^A-Za-z0-9一-鿿.,;:!?%()（）/+℃ \\-]", text))
    if useful_chars / max(1, len(compact)) < 0.62:
        return False
    if weird_chars > max(3, len(compact) // 16):
        return False
    if re.search(r"(?:\b\d{2,3}\b[\s,.;]*){3,}", text):
        return False
    if len(re.findall(r"[，、, ]", text)) >= 6 and not re.search(r"[。！？.!?；;:：]", text):
        return False
    if re.search(r"(好评率|接诊量|平均响应|福報購|人間福報|蔬食譜|蔬知識|蔬新聞|蔬視頻)", text, re.IGNORECASE):
        return False
    return matches_locale_text(text, locale)


def clean_search_excerpt(text: str, locale: str, max_length: int = 120) -> str:
    raw = strip_search_noise(text)
    if not raw:
        return ""

    sentences = re.split(r"(?<=[。！？!?])\s+|(?<=[.;；])\s+", raw)
    for sentence in sentences:
        candidate = sentence.strip(" -")
        if candidate and is_readable_text(candidate, locale):
            return trim_text(candidate, max_length)

    return trim_text(raw, max_length) if is_readable_text(raw, locale) else ""


def is_valid_hospital_name(name: str) -> bool:
    hospital = str(name or "").strip()
    if not hospital:
        return False
    if any(token in hospital for token in ["推荐医院", "推荐专家", "精选内容", "在线问诊", "科室动态"]):
        return False
    if re.search(r"^(?:那么|如果|还是|最好|建议|需要|可以|先去|应当|应该|是否|先到)", hospital):
        return False
    if re.search(r"(?:去医院|去门诊|看医生|挂号|就诊)$", hospital):
        return False
    if len(re.findall(r"[一-鿿A-Za-z]", hospital)) < 4:
        return False
    return bool(re.search(r"(医院|医学中心|中医院|医疗中心|Hospital|Medical Center|Clinic)", hospital, re.IGNORECASE))


def is_authoritative_hospital_candidate(hospital: str, context_text: str) -> bool:
    hospital_name = str(hospital or "").strip()
    blob = f"{hospital_name} {context_text}".strip()
    if not hospital_name:
        return False
    if re.search(r"(胆结石|胆囊炎|高血压|糖尿病|减脂|瘦身).{0,4}(医院|clinic|hospital)", hospital_name, re.IGNORECASE):
        return False
    if re.search(r"(在线问诊|就医指南|医院咨询|挂号平台|推荐专家|推荐医院|相关问诊)", blob, re.IGNORECASE):
        return False
    authority_markers = (
        r"(三级甲等|三甲|大学附属医院|附属医院|医学院附属|人民医院|中医院|医学中心|医疗中心|"
        r"public tertiary|tertiary hospital|affiliated hospital|medical center)"
    )
    return bool(re.search(authority_markers, blob, re.IGNORECASE))


def clean_hospital_reason(text: str, locale: str, max_length: int = 100) -> str:
    raw = clean_search_excerpt(text, locale, max_length=max_length)
    if not raw:
        return ""
    if re.search(r"(推荐专家|推荐医院|相关问诊|在线问诊|医院咨询|挂号平台|医院介绍)", raw, re.IGNORECASE):
        return ""
    list_segments = [segment.strip() for segment in re.split(r"[;；]", raw) if segment.strip()]
    if len(list_segments) >= 3 and all(len(segment) <= 12 for segment in list_segments[:5]):
        return ""
    if len(raw) > 42 and not re.search(r"[。！？.!?；;:：]", raw):
        return ""
    if re.search(r"(好评率|接诊量|平均响应|国内一流|全国领先|top\s*ranked)", raw, re.IGNORECASE):
        return ""
    sentences = re.split(r"(?<=[。！？!?])\s+|(?<=[.;；])\s+", raw)
    clean = sentences[0].strip() if sentences else raw
    return trim_text(clean, max_length)


def clean_hospital_doctor(text: str, locale: str) -> str:
    doctor = trim_text(strip_search_noise(extract_doctor_name(text) or ""), 24)
    if doctor and not re.search(r"(外科|内科|门诊|中心|肝胆|心内|内分泌|营养科|运动医学).*(医生|医师|专家)$", doctor):
        return doctor
    direct = trim_text(strip_search_noise(str(text or "")), 24)
    if re.fullmatch(r"[一-鿿]{2,4}(?:\s*(?:主任医师|副主任医师|主任|副主任|教授|副教授|医生|医师))?", direct):
        return re.sub(r"\s+", "", direct)
    if re.fullmatch(r"[一-鿿]{2,4}(?:主任医师|副主任医师|主任|副主任|教授|副教授|医生|医师)?", direct):
        return direct
    if re.fullmatch(r"Dr\.\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2}", direct):
        return direct
    cleaned = strip_search_noise(text)
    if re.search(r"(专家|specialist|主任医师|副主任医师|教授|副教授)", cleaned, re.IGNORECASE):
        name_match = re.search(r"([一-鿿]{2,4}\s*(?:主任医师|副主任医师|主任|副主任|教授|副教授|医生|医师))", cleaned)
        if name_match:
            return trim_text(re.sub(r"\s+", "", name_match.group(1)), 24)
    return localize(locale, "优先预约专家门诊", "Prioritize specialist clinic")


def is_placeholder_doctor_name(text: str) -> bool:
    token = str(text or "").strip().lower()
    placeholders = {
        "",
        "优先预约专家门诊",
        "优先预约专病门诊",
        "先做门诊评估，再决定是否转上级医院",
        "prioritize specialist clinic",
        "prioritize specialty clinic",
        "start with clinic evaluation and escalate if needed",
    }
    return token in placeholders


def has_named_doctor(text: str) -> bool:
    doctor = str(text or "").strip()
    if is_placeholder_doctor_name(doctor):
        return False
    # 允许中文姓名（2-4 个汉字）或带职称的姓名
    if re.search(r"^[\u4e00-\u9fff]{2,4}$", doctor):
        return True
    return bool(
        re.search(r"[\u4e00-\u9fff]{2,4}\s*(?:主任医师 | 副主任医师 | 主任 | 副主任 | 教授 | 副教授 | 医生 | 医师)", doctor)
        or re.search(r"Dr\.\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2}", doctor)
    )


def clean_doctor_specialty(text: str, locale: str, max_length: int = 72) -> str:
    raw = strip_search_noise(text)
    if not raw:
        return ""
    raw = re.sub(r"^(?:医生擅长|擅长方向|擅长|Doctor specialty|Specialty|Expertise)[:：]?\s*", "", raw, flags=re.IGNORECASE)
    raw = trim_text(raw, max_length)
    if len(raw) < 6:
        return ""
    if re.search(r"(推荐医院|医院介绍|在线问诊|相关问诊|挂号平台)", raw, re.IGNORECASE):
        return ""
    if not matches_locale_text(raw, locale):
        return ""
    return raw


def clean_doctor_title(text: str, locale: str, max_length: int = 40) -> str:
    raw = strip_search_noise(text)
    if not raw:
        return ""
    raw = re.sub(r"^(?:医生职称|职称|Title)[:：]?\s*", "", raw, flags=re.IGNORECASE)
    raw = trim_text(raw, max_length)
    if re.search(r"(挂号|门诊|排班|schedule|fee|费用)", raw, re.IGNORECASE):
        return ""
    return raw


def clean_registration_fee(text: str, locale: str, max_length: int = 42) -> str:
    raw = strip_search_noise(text)
    if not raw:
        return localize(locale, "以医院最新挂号页面为准", "Check the hospital's latest registration page")
    raw = re.sub(r"^(?:挂号费|费用|Fee|Registration fee)[:：]?\s*", "", raw, flags=re.IGNORECASE)
    raw = trim_text(raw, max_length)
    if re.search(r"(http|www\.|返回顶部|倍速|播放)", raw, re.IGNORECASE):
        return localize(locale, "以医院最新挂号页面为准", "Check the hospital's latest registration page")
    return raw


def clean_clinic_schedule(text: str, locale: str, max_length: int = 48) -> str:
    raw = strip_search_noise(text)
    if not raw:
        return localize(locale, "以医院最新排班为准", "Check the hospital's latest clinic schedule")
    raw = re.sub(r"^(?:坐诊时间|门诊时间|排班|Schedule|Clinic schedule)[:：]?\s*", "", raw, flags=re.IGNORECASE)
    raw = trim_text(raw, max_length)
    if re.search(r"(http|www\.|返回顶部|倍速|播放)", raw, re.IGNORECASE):
        return localize(locale, "以医院最新排班为准", "Check the hospital's latest clinic schedule")
    return raw


def clean_hospital_grade(text: str, locale: str, max_length: int = 48) -> str:
    raw = strip_search_noise(text)
    if not raw:
        return ""
    raw = re.sub(r"^(?:医院等级|等级|Grade|Hospital grade)[:：]?\s*", "", raw, flags=re.IGNORECASE)
    return trim_text(raw, max_length)


def clean_hospital_address(text: str, locale: str, max_length: int = 72) -> str:
    raw = strip_search_noise(text)
    if not raw:
        return ""
    raw = re.sub(r"^(?:地址|医院地址|Address)[:：]?\s*", "", raw, flags=re.IGNORECASE)
    if re.search(r"(http|www\.|返回顶部|倍速|播放)", raw, re.IGNORECASE):
        return ""
    return trim_text(raw, max_length)


def clean_booking_method(text: str, locale: str, max_length: int = 56) -> str:
    raw = strip_search_noise(text)
    if not raw:
        return localize(locale, "建议查看医院官方挂号平台", "Check the hospital's official booking channel")
    raw = re.sub(r"^(?:挂号方式|预约方式|Booking|Booking method)[:：]?\s*", "", raw, flags=re.IGNORECASE)
    if re.search(r"(http|www\.|返回顶部|倍速|播放)", raw, re.IGNORECASE):
        return localize(locale, "建议查看医院官方挂号平台", "Check the hospital's official booking channel")
    return trim_text(raw, max_length)


def split_doctor_identity(doctor_text: str, explicit_title: str = "") -> tuple[str, str]:
    raw = strip_search_noise(doctor_text)
    title = clean_doctor_title(explicit_title, "zh-CN")
    if not raw and not title:
        return "", ""
    match = re.match(
        r"^([一-鿿]{2,4}?)\s*(一级专家|二级专家|副主任医师|主任医师|主治医师|住院医师|副教授|教授|医师|医生)$",
        raw,
    )
    if match:
        name = match.group(1)
        inferred_title = match.group(2)
        return name, title or inferred_title
    if raw.startswith("Dr. "):
        return raw, title
    return raw, title


def star_string(level: int) -> str:
    count = max(1, min(int(level or 0), 5))
    return "★" * count


def infer_hospital_star_rating(item: dict, primary_condition: str) -> int:
    score = hospital_authority_score(item, primary_condition)
    if score >= 180:
        return 5
    if score >= 100:
        return 4
    return 3


def infer_doctor_star_rating(doctor_title: str, doctor_text: str = "") -> int:
    blob = f"{doctor_title} {doctor_text}".strip()
    if re.search(r"(副主任医师|副教授)", blob):
        return 4
    if re.search(r"(一级专家|主任医师|教授)", blob):
        return 5
    if re.search(r"(主治医师|医师|医生)", blob):
        return 3
    return 3 if has_named_doctor(doctor_text) else 2


def infer_hospital_grade(hospital: str, hospital_strength: str, locale: str) -> str:
    blob = f"{hospital} {hospital_strength}"
    if any(keyword in hospital for keyword in TOP_TIER_HOSPITAL_KEYWORDS) or re.search(r"(顶级三甲|全国顶尖|国家医学中心)", blob):
        return localize(locale, "三级甲等（全国顶尖）", "Top-tier public tertiary hospital")
    if re.search(r"(省级|大学附属|附属医院|三甲)", blob):
        return localize(locale, "三级甲等（省级重点）", "Provincial or university-affiliated tertiary hospital")
    return localize(locale, "三级甲等", "Public tertiary hospital")


def group_hospital_recommendations(recommendations: List[dict], primary_condition: str, locale: str) -> List[dict]:
    groups: List[dict] = []
    index_map: Dict[str, int] = {}
    for item in recommendations[:MAX_HOSPITAL_RECOMMENDATIONS]:
        hospital = str(item.get("hospital", "") or "").strip()
        if not hospital:
            continue
        group_index = index_map.get(hospital)
        if group_index is None:
            hospital_stars = int(item.get("hospital_rating") or infer_hospital_star_rating(item, primary_condition))
            groups.append(
                {
                    "hospital": hospital,
                    "hospital_stars": star_string(hospital_stars),
                    "hospital_grade": item.get("hospital_grade") or infer_hospital_grade(hospital, str(item.get("hospital_strength", "") or ""), locale),
                    "hospital_strength": item.get("hospital_strength", "") or item.get("reason", ""),
                    "hospital_address": item.get("hospital_address", ""),
                    "booking_method": item.get("booking_method") or localize(locale, "建议查看医院官方挂号平台", "Check the hospital's official booking channel"),
                    "doctors": [],
                    "_seen_doctors": set(),
                }
            )
            index_map[hospital] = len(groups) - 1
            group_index = index_map[hospital]

        group = groups[group_index]
        if not group.get("hospital_address") and item.get("hospital_address"):
            group["hospital_address"] = item.get("hospital_address")
        if (not group.get("booking_method") or "官方挂号平台" in str(group.get("booking_method"))) and item.get("booking_method"):
            group["booking_method"] = item.get("booking_method")
        if not group.get("hospital_strength") and item.get("hospital_strength"):
            group["hospital_strength"] = item.get("hospital_strength")
        doctor_text = str(item.get("doctor", "") or "").strip()
        doctor_name, inferred_title = split_doctor_identity(doctor_text, str(item.get("doctor_title", "") or ""))
        doctor_title = clean_doctor_title(item.get("doctor_title", "") or inferred_title, locale) or inferred_title
        doctor_name = doctor_name or doctor_text
        doctor_stars = star_string(int(item.get("doctor_rating") or infer_doctor_star_rating(doctor_title, doctor_text)))
        doctor_key = f"{doctor_name}|{doctor_title}|{item.get('department', '')}"
        if doctor_key in group["_seen_doctors"]:
            continue
        group["_seen_doctors"].add(doctor_key)
        group["doctors"].append(
            {
                "department": item.get("department", ""),
                "doctor_name": doctor_name,
                "doctor_title": doctor_title,
                "doctor_stars": doctor_stars,
                "doctor_display": localize(
                    locale,
                    f"{doctor_name}【{doctor_title or '医生'}】（{doctor_stars}）",
                    f"{doctor_name} [{doctor_title or 'Doctor'}] ({doctor_stars})",
                ),
                "doctor_specialty": item.get("doctor_specialty", ""),
                "registration_fee": item.get("registration_fee") or localize(locale, "以医院最新挂号页面为准", "Check the hospital's latest registration page"),
                "clinic_schedule": item.get("clinic_schedule") or localize(locale, "以医院最新排班为准", "Check the hospital's latest clinic schedule"),
                "reason": item.get("reason", ""),
            }
        )

    for group in groups:
        group.pop("_seen_doctors", None)
    return groups


def contains_generic_hospital_label(text: str) -> bool:
    raw = str(text or "").strip().lower()
    if not raw:
        return False
    return bool(
        re.search(
            r"(省级三甲综合医院|医学院附属三甲医院|区域医疗中心|key hospital|regional medical center|"
            r"provincial tertiary hospital|university-affiliated tertiary hospital|tertiary hospital in)",
            raw,
            re.IGNORECASE,
        )
    )


def build_hospital_strength(hospital: str, primary_condition: str, locale: str) -> str:
    name = str(hospital or "")
    lowered = name.lower()
    teaching = any(token in name for token in ("大学", "附属", "医学院")) or "affiliated" in lowered
    national = any(token in name for token in ("国家医学中心", "国家区域医疗中心"))
    medical_center = any(token in name for token in ("医学中心", "医疗中心")) or "medical center" in lowered
    tertiary = any(token in name for token in ("三甲", "三级甲等", "省级")) or "tertiary" in lowered

    if primary_condition == "gallstones":
        if national:
            return localize(locale, "国家级或区域级肝胆专科资源更强，复杂胆囊疾病与手术评估经验通常更充足。", "National or regional hepatobiliary centers usually offer deeper experience for complex gallbladder disease and surgical decision-making.")
        if teaching:
            return localize(locale, "教学型三甲医院通常具备更完整的肝胆影像、微创外科与多学科协作能力。", "Teaching tertiary hospitals usually provide stronger hepatobiliary imaging, minimally invasive surgery, and multidisciplinary support.")
        if medical_center or tertiary:
            return localize(locale, "公立三甲综合检查与外科资源较全，便于把彩超、肝功能和门诊复盘放在同一条路径里完成。", "Public tertiary hospitals offer stronger diagnostics and surgical support, which helps keep ultrasound, liver tests, and clinic review on one coordinated pathway.")
        return localize(locale, "综合专科能力较稳，适合先完成门诊评估再决定后续复查或干预节奏。", "This hospital offers stable multidisciplinary capacity for an initial specialist review before deciding on further follow-up or intervention.")
    if primary_condition == "hypertension":
        if teaching or national:
            return localize(locale, "心血管专科与长期随访资源更成熟，适合复杂血压波动和多药方案评估。", "Cardiovascular subspecialty and long-term follow-up resources are stronger here for complex blood-pressure variability and multi-drug management.")
        return localize(locale, "适合完成高血压门诊复盘、靶器官风险筛查和后续用药调整。", "This hospital is suitable for hypertension-clinic review, target-organ risk screening, and medication adjustment.")
    if primary_condition == "diabetes":
        if teaching or national:
            return localize(locale, "内分泌、营养与并发症筛查协作更完整，适合做系统化糖代谢管理。", "Endocrinology, nutrition, and complication-screening coordination are usually stronger here for structured diabetes management.")
        return localize(locale, "适合完成血糖趋势复盘、HbA1c 优化和并发症筛查安排。", "This hospital fits glucose-trend review, HbA1c optimization, and complication-screening planning.")
    if primary_condition == "fat_loss":
        return localize(locale, "临床营养与运动医学协作更适合平台期、恢复不足或体脂管理复盘。", "Clinical nutrition and sports-medicine support is a better fit for plateau review, recovery issues, and body-fat management.")
    return localize(locale, "综合诊疗能力较稳，适合先做门诊评估后再决定复查或转诊路径。", "This hospital offers stable general specialty support for an initial clinic review before deciding on follow-up or referral.")


def build_doctor_specialty(primary_condition: str, department: str, locale: str) -> str:
    department_text = str(department or "")
    if primary_condition == "gallstones":
        return localize(locale, "胆结石与慢性胆囊炎评估、腹腔镜胆囊手术、围手术期管理。", "Gallstones and chronic cholecystitis assessment, laparoscopic gallbladder surgery, and perioperative management.")
    if primary_condition == "hypertension":
        return localize(locale, "高血压分层管理、动态血压解读、联合降压方案调整。", "Hypertension stratification, ambulatory blood-pressure interpretation, and combination therapy adjustment.")
    if primary_condition == "diabetes":
        return localize(locale, "血糖分层管理、药物方案优化、并发症筛查与长期随访。", "Glucose stratification, medication optimization, complication screening, and long-term follow-up.")
    if primary_condition == "fat_loss":
        return localize(locale, "体重体脂平台期评估、营养处方、训练恢复与代谢管理。", "Weight and body-fat plateau review, nutrition prescription, training recovery, and metabolic management.")
    return localize(locale, f"{department_text} 相关门诊评估与长期管理。", f"{department_text} clinic review and longer-term management.")


def build_region_specific_hospital_fallbacks(
    residence_text: str,
    primary_condition: str,
    default_department: str,
    locale: str,
) -> List[dict]:
    normalized_residence = str(residence_text or "")
    if "成都" in normalized_residence and primary_condition == "gallstones" and resolve_locale(locale=locale) == "ja-JP":
        return [
            {
                "hospital": "四川大学華西病院",
                "department": "肝胆膵外科 / 肝胆外科",
                "doctor": "王文涛主任医師",
                "doctor_title": "主任医師 / 教授",
                "hospital_strength": "全国トップクラスの三甲教学病院で、肝胆膵外科、画像診断、麻酔、低侵襲手術の体制が非常に充実しています。",
                "hospital_grade": "三級甲等（全国トップクラス）",
                "hospital_address": "成都市武侯区国学巷 37 号",
                "booking_method": "華医通アプリ / WeChat公式アカウント",
                "doctor_specialty": "複雑な胆道結石、胆嚢結石、慢性胆嚢炎、および肝胆膵外科手術の評価。",
                "registration_fee": "特需外来（約 300-500 元）",
                "clinic_schedule": "華医通の最新外来表を優先確認し、MDT 外来があれば優先予約してください。",
                "reason": "超音波の継続フォロー、慢性胆嚢炎のコントロール、手術タイミングの判断を一つの病院でまとめて見たいケースに最適です。",
                "url": "",
            },
            {
                "hospital": "四川大学華西病院",
                "department": "肝胆膵外科 / 肝胆外科",
                "doctor": "胡佳副主任医師",
                "doctor_title": "副主任医師 / 副教授",
                "hospital_strength": "難治性の胆嚢・胆道疾患や低侵襲外科評価の経験が豊富なトップ級三甲教学病院です。",
                "hospital_grade": "三級甲等（全国トップクラス）",
                "hospital_address": "成都市武侯区国学巷 37 号",
                "booking_method": "華医通アプリ / WeChat公式アカウント",
                "doctor_specialty": "複雑な胆嚢・胆道疾患、腹腔鏡手術、ロボット支援手術の評価。",
                "registration_fee": "専門外来（約 100-200 元）",
                "clinic_schedule": "華医通の最新外来表を確認し、肝胆膵外科の専門外来を優先してください。",
                "reason": "症状が再発し、低侵襲手術の適応や保存的治療との比較をより詳しく相談したい場合に相性が良い候補です。",
                "url": "",
            },
            {
                "hospital": "四川大学華西病院",
                "department": "肝胆膵外科 / 肝胆外科",
                "doctor": "徐珽副主任医師",
                "doctor_title": "副主任医師",
                "hospital_strength": "胆膵領域の専門性が高く、複雑な胆道病変の総合判断に強いトップ級三甲教学病院です。",
                "hospital_grade": "三級甲等（全国トップクラス）",
                "hospital_address": "成都市武侯区国学巷 37 号",
                "booking_method": "華医通アプリ / WeChat公式アカウント",
                "doctor_specialty": "胆道結石、胆膵疾患、複雑な胆道外科評価。",
                "registration_fee": "専門外来（約 50-100 元）",
                "clinic_schedule": "華医通の最新外来表を確認してください。初診は専門外来でも十分なことが多いです。",
                "reason": "胆道結石リスク、画像変化、胆嚢炎の再燃状況、今後の外科戦略をまとめて整理したい患者に向いています。",
                "url": "",
            },
            {
                "hospital": "四川省人民病院",
                "department": "肝胆外科 / 一般外科",
                "doctor": "周永碧主任医師",
                "doctor_title": "主任医師",
                "hospital_strength": "省級の公立三甲病院で、肝胆外科の成熟度が高く、低侵襲手術と周術期連携が安定しています。",
                "hospital_grade": "三級甲等（省級重点）",
                "hospital_address": "成都市青羊区一環路西二段 32 号",
                "booking_method": "WeChat公式アカウント / 現地受付",
                "doctor_specialty": "胆嚢結石、低侵襲の胆嚢温存治療、胆嚢炎の外科評価。",
                "registration_fee": "専門外来（約 80-150 元）",
                "clinic_schedule": "病院の最新外来表を確認し、肝胆外科専門外来を優先してください。",
                "reason": "省級三甲でまず外来評価、超音波、肝機能の情報を整理し、保存的治療継続か手術評価へ進むかを判断したい場合に実用的です。",
                "url": "",
            },
            {
                "hospital": "成都市第三人民病院",
                "department": "肝胆外科 / 一般外科",
                "doctor": "李毅医師",
                "doctor_title": "医師",
                "hospital_strength": "市内で通いやすい三甲総合病院で、再診、追加検査、術前の基礎評価をまとめやすいのが利点です。",
                "hospital_grade": "三級甲等（通院しやすい地域中核）",
                "hospital_address": "病院公式サイトで最新の院区情報を確認してください。",
                "booking_method": "病院公式の予約窓口を確認してください。",
                "doctor_specialty": "胆石症、胆道外科、外来フォローアップ評価。",
                "registration_fee": "一般 / 専門外来（病院の最新受付ページを確認）",
                "clinic_schedule": "病院の最新外来表をご確認ください。",
                "reason": "近隣での再診を優先しつつ、超音波や肝機能を補完してから上位病院に紹介したい場合に使いやすい候補です。",
                "url": "",
            },
        ]
    if "成都" in normalized_residence and primary_condition == "gallstones":
        return [
            {
                "hospital": localize(locale, "四川大学华西医院", "West China Hospital, Sichuan University"),
                "department": localize(locale, "肝胆胰外科 / 肝胆外科", "Hepatopancreatobiliary surgery / hepatobiliary surgery"),
                "doctor": localize(locale, "王文涛主任医师", "Dr. Wang Wentao"),
                "doctor_title": localize(locale, "主任医师 / 教授", "Chief physician / professor"),
                "hospital_strength": localize(locale, "顶级三甲教学医院，肝胆胰外科、影像、麻醉和微创手术平台都很强。", "Top-tier tertiary teaching hospital with elite hepatobiliary imaging, anesthesia, and minimally invasive surgery support."),
                "hospital_grade": localize(locale, "三级甲等（全国顶尖）", "Top-tier public tertiary hospital"),
                "hospital_address": localize(locale, "成都市武侯区国学巷 37 号", "No. 37 Guoxue Alley, Wuhou District, Chengdu"),
                "booking_method": localize(locale, "华医通 APP / 微信公众号", "Huayitong app / WeChat official account"),
                "doctor_specialty": localize(locale, "复杂肝胆管结石、胆囊结石、慢性胆囊炎与肝胆胰外科手术评估。", "Focuses on complex biliary stones, gallbladder disease, chronic cholecystitis, and hepatobiliary surgical planning."),
                "registration_fee": localize(locale, "特需门诊（约 300-500 元）", "Premium clinic (about CNY 300-500)"),
                "clinic_schedule": localize(locale, "建议优先查看华医通最新排班；如开放 MDT 门诊可优先预约。", "Check the latest Huayitong schedule first; prioritize MDT clinic slots when available."),
                "reason": localize(locale, "适合像当前这样既要结合彩超连续随访，又要评估慢性胆囊炎是否进入手术窗口的情况；如果后续出现反复发作，也更适合在这里统一做影像、门诊和手术时机判断。", "A strong fit when ultrasound follow-up, chronic cholecystitis control, and surgical timing all need review together."),
                "url": "",
            },
            {
                "hospital": localize(locale, "四川大学华西医院", "West China Hospital, Sichuan University"),
                "department": localize(locale, "肝胆胰外科 / 肝胆外科", "Hepatopancreatobiliary surgery / hepatobiliary surgery"),
                "doctor": localize(locale, "胡佳副教授", "Dr. Hu Jia"),
                "doctor_title": localize(locale, "副教授 / 副主任医师", "Associate professor / associate chief physician"),
                "hospital_strength": localize(locale, "顶级三甲教学医院，疑难胆囊胆道疾病和微创外科评估经验丰富。", "Top-tier tertiary teaching hospital with deep experience in complex gallbladder disease and minimally invasive surgery."),
                "hospital_grade": localize(locale, "三级甲等（全国顶尖）", "Top-tier public tertiary hospital"),
                "hospital_address": localize(locale, "成都市武侯区国学巷 37 号", "No. 37 Guoxue Alley, Wuhou District, Chengdu"),
                "booking_method": localize(locale, "华医通 APP / 微信公众号", "Huayitong app / WeChat official account"),
                "doctor_specialty": localize(locale, "复杂胆囊胆道疾病、腹腔镜与机器人微创外科评估。", "Specializes in complex gallbladder and biliary disease, including laparoscopic and robotic surgery."),
                "registration_fee": localize(locale, "专家门诊（约 100-200 元）", "Specialist clinic (about CNY 100-200)"),
                "clinic_schedule": localize(locale, "建议查看华医通最新排班，优先关注肝胆胰外科专病门诊。", "Check the latest Huayitong schedule and monitor hepatopancreatobiliary specialty clinic slots."),
                "reason": localize(locale, "如果后续症状反复、需要重点评估微创手术路径，或者想更细地比较保守治疗与腹腔镜方案，这类病例与该医生的专长更契合。", "Especially suitable if symptoms recur and a minimally invasive surgical pathway needs closer evaluation."),
                "url": "",
            },
            {
                "hospital": localize(locale, "四川大学华西医院", "West China Hospital, Sichuan University"),
                "department": localize(locale, "肝胆胰外科 / 肝胆外科", "Hepatopancreatobiliary surgery / hepatobiliary surgery"),
                "doctor": localize(locale, "徐珽副主任医师", "Dr. Xu Ting"),
                "doctor_title": localize(locale, "副主任医师", "Associate chief physician"),
                "hospital_strength": localize(locale, "顶级三甲教学医院，胆胰专病与复杂胆道问题的综合判断能力更强。", "Top-tier tertiary teaching hospital with stronger integrated review for biliary and pancreatic complexity."),
                "hospital_grade": localize(locale, "三级甲等（全国顶尖）", "Top-tier public tertiary hospital"),
                "hospital_address": localize(locale, "成都市武侯区国学巷 37 号", "No. 37 Guoxue Alley, Wuhou District, Chengdu"),
                "booking_method": localize(locale, "华医通 APP / 微信公众号", "Huayitong app / WeChat official account"),
                "doctor_specialty": localize(locale, "胆道结石、胆胰疾病与复杂胆道外科评估。", "Focuses on biliary stones, pancreatobiliary disease, and complex biliary surgical evaluation."),
                "registration_fee": localize(locale, "专科门诊（约 50-100 元）", "Specialty clinic (about CNY 50-100)"),
                "clinic_schedule": localize(locale, "建议查看华医通最新排班；首诊通常先挂专科门诊即可。", "Check the latest Huayitong schedule; a specialty clinic slot is usually enough for the first visit."),
                "reason": localize(locale, "适合需要把胆道结石风险、影像变化、胆囊炎反复情况和后续外科策略放在一起复盘的患者，尤其适合先做结构化评估再决定是否升级到更高阶专家门诊。", "Useful when biliary-stone risk, imaging findings, and downstream surgical strategy need to be reviewed together."),
                "url": "",
            },
            {
                "hospital": localize(locale, "四川省人民医院", "Sichuan Provincial People's Hospital"),
                "department": localize(locale, "肝胆外科 / 普外科", "Hepatobiliary surgery / general surgery"),
                "doctor": localize(locale, "周永碧主任医师", "Dr. Zhou Yongbi"),
                "doctor_title": localize(locale, "主任医师", "Chief physician"),
                "hospital_strength": localize(locale, "省级公立三甲，肝胆外科成熟，微创和围手术期协作比较稳定。", "Provincial public tertiary hospital with mature hepatobiliary surgery and steady perioperative coordination."),
                "hospital_grade": localize(locale, "三级甲等（省级重点）", "Provincial key tertiary hospital"),
                "hospital_address": localize(locale, "成都市青羊区一环路西二段 32 号", "No. 32 Section 2 West 1st Ring Road, Qingyang District, Chengdu"),
                "booking_method": localize(locale, "微信公众号 / 现场挂号", "WeChat official account / on-site registration"),
                "doctor_specialty": localize(locale, "胆囊结石、微创保胆取石与胆囊炎外科评估。", "Focuses on gallbladder stones, minimally invasive gallbladder-preserving care, and cholecystitis surgery evaluation."),
                "registration_fee": localize(locale, "专家门诊（约 80-150 元）", "Specialist clinic (about CNY 80-150)"),
                "clinic_schedule": localize(locale, "建议查看医院最新排班，优先关注肝胆外科专家门诊。", "Check the hospital's latest clinic schedule and prioritize hepatobiliary specialist slots."),
                "reason": localize(locale, "适合先在省级三甲完成门诊复盘、彩超与肝功能资料整合，再判断是继续保守治疗、尝试更细化的微创方案，还是进入正式手术评估通道。", "A practical tertiary option for deciding between continued conservative care and escalation toward surgery."),
                "url": "",
            },
            {
                "hospital": localize(locale, "成都市第三人民医院", "Chengdu Third People's Hospital"),
                "department": localize(locale, "肝胆外科 / 普外科", "Hepatobiliary surgery / general surgery"),
                "doctor": localize(locale, "李毅医生", "Dr. Li Yi"),
                "doctor_title": localize(locale, "医生", "Doctor"),
                "hospital_strength": localize(locale, "本地三甲综合医院，适合就近复诊、补齐检查和术前基础评估。", "Local tertiary general hospital that works well for nearby follow-up, additional testing, and baseline pre-op review."),
                "hospital_grade": localize(locale, "三级甲等（本地便捷复诊）", "Local tertiary hospital for convenient follow-up"),
                "hospital_address": localize(locale, "建议查看医院官方地址与院区信息", "Check the hospital's official location and campus details"),
                "booking_method": localize(locale, "建议查看医院官方挂号平台", "Check the hospital's official booking channel"),
                "doctor_specialty": localize(locale, "胆石症、胆道外科和门诊随访评估。", "Focuses on gallstone care, biliary surgery, and outpatient follow-up evaluation."),
                "registration_fee": localize(locale, "普通 / 专科门诊（以医院最新挂号页面为准）", "General or specialty clinic; check the latest hospital registration page"),
                "clinic_schedule": localize(locale, "以医院最新排班为准", "Check the hospital's latest clinic schedule"),
                "reason": localize(locale, "适合想兼顾就近复诊和基础外科评估的人群，先把彩超、肝功能和近期症状记录补齐；如果后续需要更复杂的手术决策，再转到更强的上级医院也更顺畅。", "Useful when the patient wants convenient local follow-up first, with escalation to a stronger center if needed."),
                "url": "",
            },
        ]
    return []


def build_condition_care_question(monthly_data: dict, locale: str) -> str:
    residence_text = monthly_data.get("residence_text", "")
    primary_condition = monthly_data.get("primary_condition") or (monthly_data.get("conditions") or ["balanced"])[0]
    ultrasound = monthly_data.get("ultrasound_summary", {}) or {}
    symptom_days = monthly_data.get("symptom_days", 0)
    latest_size = ultrasound.get("latest_size_cm")
    wall_warning = ultrasound.get("wall_warning")
    is_ja = resolve_locale(locale=locale) == "ja-JP"

    if primary_condition == "gallstones":
        if resolve_locale(locale=locale) == "zh-CN":
            details = []
            if latest_size:
                details.append(f"最近结石约 {latest_size:.1f}cm")
            if symptom_days:
                details.append(f"本月症状 {symptom_days} 天")
            if wall_warning:
                details.append("胆囊壁存在炎症或增厚提示")
            suffix = f"（{', '.join(details)}）" if details else ""
            return f"请帮我推荐 {residence_text} 做胆结石或慢性胆囊炎评估/手术比较好的医院和医生，优先肝胆胰外科或肝胆外科{suffix}。"
        if is_ja:
            details = []
            if latest_size:
                details.append(f"最新の結石サイズは約 {latest_size:.1f}cm")
            if symptom_days:
                details.append(f"今月の症状日は {symptom_days} 日")
            if wall_warning:
                details.append("胆嚢壁の炎症または肥厚の示唆あり")
            suffix = f"（{'、'.join(details)}）" if details else ""
            return f"{residence_text} で胆石または慢性胆嚢炎の評価・手術に強い病院と医師を推薦してください。肝胆膵外科または肝胆外科を優先してください{suffix}。"
        return f"Please recommend strong hospitals and doctors in {residence_text} for gallstone or chronic cholecystitis evaluation or surgery, prioritizing hepatobiliary surgery."
    if primary_condition == "hypertension":
        if is_ja:
            return f"{residence_text} で高血圧診療に強い病院と医師を推薦してください。循環器内科または高血圧専門外来を優先してください。"
        return localize(locale, f"请帮我推荐 {residence_text} 看高血压比较好的医院和医生，优先心内科或高血压专病门诊。", f"Please recommend strong hospitals and doctors in {residence_text} for hypertension care, prioritizing cardiology or hypertension clinics.")
    if primary_condition == "diabetes":
        if is_ja:
            return f"{residence_text} で糖尿病診療に強い病院と医師を推薦してください。内分泌内科または糖尿病専門外来を優先してください。"
        return localize(locale, f"请帮我推荐 {residence_text} 看糖尿病比较好的医院和医生，优先内分泌科或糖尿病专病门诊。", f"Please recommend strong hospitals and doctors in {residence_text} for diabetes care, prioritizing endocrinology or diabetes clinics.")
    if primary_condition == "fat_loss":
        if is_ja:
            return f"{residence_text} で体重・体脂肪管理に強い病院と医師を推薦してください。臨床栄養科またはスポーツ医学外来を優先してください。"
        return localize(locale, f"请帮我推荐 {residence_text} 做体重体脂管理比较好的医院和医生，优先临床营养科或运动医学门诊。", f"Please recommend strong hospitals and doctors in {residence_text} for weight and body-fat management, prioritizing clinical nutrition or sports medicine.")
    if is_ja:
        return f"{residence_text} で健康管理評価に強い病院と医師を推薦してください。"
    return localize(locale, f"请帮我推荐 {residence_text} 做健康管理评估比较好的医院和医生。", f"Please recommend strong hospitals and doctors in {residence_text} for general health-management evaluation.")


def build_condition_hospital_reason(hospital: str, primary_condition: str, locale: str) -> str:
    name = str(hospital or "")
    lowered = name.lower()
    teaching = any(token in name for token in ("大学", "附属")) or "teaching" in lowered
    medical_center = any(token in name for token in ("医学中心", "医疗中心")) or "medical center" in lowered
    peoples_hospital = "人民医院" in name or "people" in lowered

    if primary_condition == "gallstones":
        if teaching:
            return localize(locale, "教学医院通常具备更完整的肝胆影像与多学科协作资源，适合结合彩超、肝功能和手术时机一起评估。", "Teaching hospitals usually offer stronger hepatobiliary imaging and multidisciplinary support for ultrasound, liver tests, and surgical-timing review.")
        if peoples_hospital or medical_center:
            return localize(locale, "综合检查资源较全，适合先完成肝胆彩超、肝功能和症状复盘，再决定是否需要外科进一步评估。", "Broader diagnostic access makes this a practical place to complete ultrasound, liver tests, and symptom review before deciding on surgical follow-up.")
        return localize(locale, "适合先做肝胆专科门诊评估，并结合症状频次与影像结果判断后续复查或治疗节奏。", "This is a sensible option for an initial hepatobiliary clinic review tied to symptom frequency and imaging results.")
    if primary_condition == "hypertension":
        if teaching:
            return localize(locale, "教学医院更适合联合评估血压波动、用药副作用和靶器官风险，便于后续长期随访。", "Teaching hospitals are a stronger fit for blood-pressure variability, medication side effects, and target-organ risk over longer follow-up.")
        return localize(locale, "适合完成血压波动、并发症风险和长期降压方案的系统复盘。", "This is suitable for a structured review of blood-pressure variability, complication risk, and longer-term medication planning.")
    if primary_condition == "diabetes":
        if teaching:
            return localize(locale, "教学医院更利于把 HbA1c、血糖监测、营养管理和并发症筛查放在一次复盘里完成。", "Teaching hospitals are better suited to combine HbA1c, glucose logs, nutrition planning, and complication screening in one review.")
        return localize(locale, "适合联合复盘血糖趋势、饮食结构和后续并发症筛查安排。", "This option fits a combined review of glucose trends, meal structure, and complication-screening plans.")
    if primary_condition == "fat_loss":
        return localize(locale, "适合结合体重、体脂和训练恢复状态进行结构化复盘，必要时再追加营养或运动医学评估。", "This clinic can support a structured review of weight, body fat, and recovery before escalating to nutrition or sports medicine when needed.")
    return localize(locale, "适合先完成门诊评估，再根据检查结果决定后续复查或转诊。", "This is appropriate for an initial clinic review before deciding on further follow-up or referral.")


def normalize_hospital_recommendation(
    item: dict,
    primary_condition: str,
    default_department: str,
    locale: str,
    fallback_reason: str = "",
) -> Optional[dict]:
    is_ja = resolve_locale(locale=locale) == "ja-JP"
    hospital = extract_hospital_name(item.get("hospital", "")) or str(item.get("hospital", "")).strip()
    if not is_valid_hospital_name(hospital):
        return None

    department = trim_text(
        strip_search_noise(item.get("department") or default_department or localize(locale, "肝胆外科 / 普外科", "Hepatobiliary surgery / general surgery")),
        28,
    )
    doctor = clean_hospital_doctor(item.get("doctor", "") or item.get("source_excerpt", ""), locale)
    _, inferred_doctor_title = split_doctor_identity(doctor, str(item.get("doctor_title", "") or ""))
    doctor_title = clean_doctor_title(item.get("doctor_title", "") or inferred_doctor_title, locale, max_length=42)
    source_excerpt = clean_search_excerpt(item.get("source_excerpt", ""), locale, max_length=140)
    hospital_strength = clean_hospital_reason(
        item.get("hospital_strength", "") or item.get("hospital_advantage", "") or "",
        locale,
        max_length=96,
    )
    if not hospital_strength:
        hospital_strength = build_hospital_strength(hospital, primary_condition, locale)
    doctor_specialty = clean_doctor_specialty(
        item.get("doctor_specialty", "") or item.get("doctor_advantage", "") or item.get("doctor_strength", "") or "",
        locale,
        max_length=80,
    )
    if not doctor_specialty:
        doctor_specialty = build_doctor_specialty(primary_condition, department, locale)
    reason = clean_hospital_reason(item.get("reason", "") or item.get("fit_reason", "") or source_excerpt, locale, max_length=150)
    if not reason:
        reason = fallback_reason or build_condition_hospital_reason(hospital, primary_condition, locale)
    hospital_grade = clean_hospital_grade(item.get("hospital_grade", "") or item.get("grade", ""), locale, max_length=48)
    if not hospital_grade:
        hospital_grade = infer_hospital_grade(hospital, hospital_strength, locale)
    hospital_address = clean_hospital_address(item.get("hospital_address", "") or item.get("address", ""), locale, max_length=80)
    booking_method = clean_booking_method(item.get("booking_method", "") or item.get("booking", ""), locale, max_length=60)
    registration_fee = clean_registration_fee(item.get("registration_fee", "") or item.get("fee", ""), locale, max_length=46)
    clinic_schedule = clean_clinic_schedule(item.get("clinic_schedule", "") or item.get("schedule", ""), locale, max_length=52)

    if is_ja:
        hospital = sanitize_locale_line(locale, hospital)
        department = sanitize_locale_line(locale, department)
        doctor = sanitize_locale_line(locale, doctor)
        doctor_title = sanitize_locale_line(locale, doctor_title)
        hospital_strength = sanitize_locale_line(locale, hospital_strength)
        hospital_grade = sanitize_locale_line(locale, hospital_grade)
        hospital_address = sanitize_locale_line(locale, hospital_address)
        booking_method = sanitize_locale_line(locale, booking_method)
        doctor_specialty = sanitize_locale_line(locale, doctor_specialty)
        registration_fee = sanitize_locale_line(locale, registration_fee)
        clinic_schedule = sanitize_locale_line(locale, clinic_schedule)
        reason = sanitize_locale_line(locale, reason)

    return {
        "hospital": trim_text(hospital, 32),
        "department": department,
        "doctor": doctor,
        "doctor_title": doctor_title,
        "hospital_strength": hospital_strength,
        "hospital_grade": hospital_grade,
        "hospital_address": hospital_address,
        "booking_method": booking_method,
        "doctor_specialty": doctor_specialty,
        "registration_fee": registration_fee,
        "clinic_schedule": clinic_schedule,
        "reason": reason,
        "url": "",
        "source_excerpt": source_excerpt,
    }


def parse_llm_json_array(output: str) -> List[dict]:
    raw = str(output or "").strip()
    if not raw:
        return []
    try:
        match = re.search(r"\[.*\]", raw, re.DOTALL)
        parsed = json.loads(match.group(0) if match else raw)
    except Exception:
        return []
    return [item for item in parsed if isinstance(item, dict)] if isinstance(parsed, list) else []


def get_condition_department_keywords(condition: str) -> tuple[str, ...]:
    mapping = {
        "gallstones": ("肝胆", "普外", "胆囊", "hepatobiliary", "general surgery"),
        "hypertension": ("心内", "高血压", "cardiology", "hypertension"),
        "diabetes": ("内分泌", "糖尿病", "endocrinology", "diabetes"),
        "fat_loss": ("营养", "运动医学", "减脂", "nutrition", "sports medicine", "weight"),
    }
    return mapping.get(condition or "", ())


def hospital_authority_score(item: dict, primary_condition: str) -> int:
    hospital = str(item.get("hospital", "") or "")
    department = str(item.get("department", "") or "")
    doctor = str(item.get("doctor", "") or "")
    reason = str(item.get("reason", "") or "")
    excerpt = str(item.get("source_excerpt", "") or "")
    hospital_strength = str(item.get("hospital_strength", "") or "")
    blob = " ".join([hospital, department, doctor, reason, excerpt]).lower()

    score = 0
    if any(keyword in hospital for keyword in TOP_TIER_HOSPITAL_KEYWORDS):
        score += 130
    if re.search(r"(三级甲等|三甲)", blob):
        score += 80
    if re.search(r"(国家医学中心|国家区域医疗中心|国家临床重点专科)", blob):
        score += 60
    if re.search(r"(顶级三甲|全国顶尖|top[- ]tier tertiary|top tertiary)", hospital_strength, re.IGNORECASE):
        score += 42
    if re.search(r"(大学附属医院|附属医院|医学院附属)", hospital):
        score += 48
    if re.search(r"(医学中心|医疗中心)", hospital):
        score += 30
    if re.search(r"(省人民医院|省立医院|人民医院|中医院)", hospital):
        score += 18
    if has_named_doctor(doctor):
        score += 18
    if contains_generic_hospital_label(hospital):
        score -= 120

    for keyword in get_condition_department_keywords(primary_condition):
        if keyword.lower() in department.lower():
            score += 12
            break

    if re.search(
        r"(重点医院|key hospital|当地.+医院|本地.+医院|tertiary general hospital|teaching hospital|regional medical center)",
        hospital,
        re.IGNORECASE,
    ):
        score -= 30
    return score


def rank_hospital_recommendations(recommendations: List[dict], primary_condition: str) -> List[dict]:
    scored = []
    for index, item in enumerate(recommendations):
        scored.append((hospital_authority_score(item, primary_condition), index, item))
    scored.sort(key=lambda entry: (-entry[0], entry[1]))
    return [item for _, _, item in scored]


def merge_hospital_recommendations(primary_items: List[dict], fallback_items: List[dict], limit: int = MAX_HOSPITAL_RECOMMENDATIONS) -> List[dict]:
    merged = []
    seen = set()
    for collection in (primary_items, fallback_items):
        for item in collection:
            hospital = str(item.get("hospital", "") or "").strip()
            if not hospital:
                continue
            doctor = str(item.get("doctor", "") or "").strip()
            dedupe_key = f"{hospital.lower()}|{doctor.lower()}" if has_named_doctor(doctor) else hospital.lower()
            if dedupe_key in seen:
                continue
            merged.append(item)
            seen.add(dedupe_key)
            if len(merged) >= limit:
                return merged
    return merged


def merge_and_rank_hospital_recommendations(
    primary_items: List[dict],
    secondary_items: List[dict],
    primary_condition: str,
    limit: int = MAX_HOSPITAL_RECOMMENDATIONS,
) -> List[dict]:
    merged = merge_hospital_recommendations(primary_items, secondary_items, limit=limit * 2)
    ranked = rank_hospital_recommendations(merged, primary_condition)
    return ranked[:limit]


def build_local_rule_hospital_recommendations(
    residence_label: str,
    residence_text: str,
    primary_condition: str,
    default_department: str,
    locale: str,
) -> List[dict]:
    region_specific = build_region_specific_hospital_fallbacks(residence_text, primary_condition, default_department, locale)
    if len(region_specific) >= MAX_HOSPITAL_RECOMMENDATIONS:
        return region_specific[:MAX_HOSPITAL_RECOMMENDATIONS]
    fallback = [
        {
            "hospital": localize(locale, f"{residence_label} 省级三甲综合医院", f"Provincial tertiary hospital in {residence_label}"),
            "department": default_department,
            "doctor": localize(locale, "优先预约专家门诊", "Prioritize specialist clinic"),
            "hospital_strength": build_hospital_strength(localize(locale, f"{residence_label} 省级三甲综合医院", f"Provincial tertiary hospital in {residence_label}"), primary_condition, locale),
            "doctor_specialty": build_doctor_specialty(primary_condition, default_department, locale),
            "reason": build_condition_hospital_reason(localize(locale, f"{residence_label} 省级三甲综合医院", f"Provincial tertiary hospital in {residence_label}"), primary_condition, locale),
            "url": "",
        },
        {
            "hospital": localize(locale, f"{residence_label} 医学院附属三甲医院", f"University-affiliated tertiary hospital in {residence_label}"),
            "department": default_department,
            "doctor": localize(locale, "优先预约专病门诊", "Prioritize specialty clinic"),
            "hospital_strength": build_hospital_strength(localize(locale, f"{residence_label} 医学院附属三甲医院", f"University-affiliated tertiary hospital in {residence_label}"), primary_condition, locale),
            "doctor_specialty": build_doctor_specialty(primary_condition, default_department, locale),
            "reason": build_condition_hospital_reason(localize(locale, f"{residence_label} 医学院附属三甲医院", f"University-affiliated tertiary hospital in {residence_label}"), primary_condition, locale),
            "url": "",
        },
        {
            "hospital": localize(locale, f"{residence_label} 区域医疗中心", f"Regional medical center in {residence_label}"),
            "department": default_department,
            "doctor": localize(locale, "先做门诊评估，再决定是否转上级医院", "Start with clinic evaluation and escalate if needed"),
            "hospital_strength": build_hospital_strength(localize(locale, f"{residence_label} 区域医疗中心", f"Regional medical center in {residence_label}"), primary_condition, locale),
            "doctor_specialty": build_doctor_specialty(primary_condition, default_department, locale),
            "reason": build_condition_hospital_reason(localize(locale, f"{residence_label} 区域医疗中心", f"Regional medical center in {residence_label}"), primary_condition, locale),
            "url": "",
        },
    ]
    return merge_hospital_recommendations(region_specific, fallback, limit=MAX_HOSPITAL_RECOMMENDATIONS)


def build_llm_hospital_recommendations(
    monthly_data: dict,
    locale: str,
    config: dict,
    condition_queries: Dict[str, dict],
    evidence_candidates: Optional[List[dict]] = None,
) -> List[dict]:
    primary_condition = monthly_data.get("primary_condition") or monthly_data.get("conditions", ["gallstones"])[0]
    primary_meta = condition_queries.get(primary_condition, next(iter(condition_queries.values())))
    ordered_conditions = [primary_condition] + [item for item in monthly_data.get("conditions", []) if item != primary_condition]
    department_hints = [
        {
            "condition": condition,
            "department": condition_queries.get(condition, primary_meta).get("department", primary_meta["department"]),
        }
        for condition in ordered_conditions
    ]
    evidence_payload = [
        {
            "hospital": item.get("hospital", ""),
            "department": item.get("department", ""),
            "doctor_hint": item.get("doctor", "") if has_named_doctor(item.get("doctor", "")) else "",
            "doctor_title_hint": item.get("doctor_title", ""),
            "registration_fee_hint": item.get("registration_fee", ""),
            "clinic_schedule_hint": item.get("clinic_schedule", ""),
            "snippet": item.get("source_excerpt", ""),
        }
        for item in (evidence_candidates or [])[:8]
    ]
    care_question = build_condition_care_question(monthly_data, locale)
    prompt = localize(
        locale,
        f"""请基于以下信息，输出 5 条“医院优先、医生其次”的就诊建议，且必须优先推荐权威公立三甲医院。

模拟用户原始提问：
{care_question}

硬性要求：
1. 推荐顺序必须严格满足：顶级三甲医院 > 省级/大学附属三甲医院 > 其他三甲医院/区域医疗中心。
2. 第 1 条推荐必须是当地最强或最具代表性的顶级三甲医院。
3. 推荐流程必须先确定医院，再匹配科室，再补充医生。
4. hospital 字段只能写规范医院名称，禁止写描述语、导航词、链接或“当地三甲医院”这类泛称。
5. doctor 字段必须输出真实医生姓名 + 职称；严禁输出“优先预约专家门诊”或类似占位词。如果某条没有把握给出医生姓名，请换另一位更有把握的医生。
6. hospital_strength 必须概括医院的专科/平台优势，并尽量体现“顶级三甲”或“三甲”层级，不超过 60 字。
7. hospital_grade 输出医院等级描述，例如“三级甲等（全国顶尖）”。
8. hospital_address 输出简洁院区地址；booking_method 输出挂号方式。
9. doctor_title 单独输出医生职称，doctor_specialty 概括该医生擅长方向，不超过 60 字。
10. registration_fee 尽量输出挂号费区间；clinic_schedule 尽量输出门诊时间。如果不能确认，必须写“以医院最新挂号页面为准”或“以医院最新排班为准”，不要编造具体时间。
11. reason 必须说明为什么这个“医院 + 医生”组合适合当前患者，突出症状、复查需求或多病种管理契合度，可更详细一些但不超过 140 字。
12. 如果提供了检索候选，请优先使用其中出现的医院和医生姓名；若检索候选不足，你可以基于你掌握的公开常识补充当地最知名的顶级三甲医院与专家。
13. 如果用户存在多病种管理，请优先推荐能覆盖主要风险的综合三甲医院。
14. 若主要病种与手术评估强相关，请优先推荐成熟的外科团队与微创经验丰富的医生。
15. 只返回 JSON 数组，不要 Markdown，不要解释。

返回字段只能是：
- hospital
- department
- doctor
 - doctor_title
 - hospital_strength
 - hospital_grade
 - hospital_address
 - booking_method
 - doctor_specialty
 - registration_fee
 - clinic_schedule
 - reason

用户信息：
- 常居地：{monthly_data.get('residence_text', '')}
- 当前管理目标：{monthly_data.get('condition_text', '')}
- 主要病种：{primary_condition}
- 症状天数：{monthly_data.get('symptom_days', 0)}
- 用药天数：{monthly_data.get('medication_days', 0)}
- 监测天数：{monthly_data.get('monitoring_days', 0)}
- 推荐科室提示：{json.dumps(department_hints, ensure_ascii=False)}
- 复查提醒：{json.dumps(monthly_data.get('follow_up_reminders', [])[:3], ensure_ascii=False)}
- 检索候选（如有）：{json.dumps(evidence_payload, ensure_ascii=False)}
""",
        f"""Generate 5 care recommendations in a hospital-first, doctor-second order, and prioritize authoritative public tertiary hospitals.

Simulated user request:
{care_question}

Hard rules:
1. The order must strictly be: top-tier tertiary hospital > major provincial or university-affiliated tertiary hospital > other tertiary or regional centers.
2. The first recommendation must be the strongest or most iconic top-tier tertiary hospital in that city.
3. Choose the hospital first, then the department, then the doctor.
4. The hospital field must contain a real hospital name only. No generic labels, navigation text, or links.
5. The doctor field must contain a real doctor name plus title. Never output placeholders such as "Prioritize specialist clinic". If confidence is low for one doctor, replace that item with another doctor you know better.
6. hospital_strength must summarize the hospital platform or specialty advantage and should ideally reflect whether it is a top-tier tertiary or tertiary center, under 60 characters.
7. hospital_grade should output the hospital grade, such as "top-tier public tertiary hospital".
8. hospital_address should be a concise address; booking_method should describe the main booking channel.
9. doctor_title should be the doctor's title, and doctor_specialty should summarize the doctor's strongest focus in under 60 characters.
10. registration_fee should provide a fee range when possible; clinic_schedule should provide clinic timing when possible. If either one is uncertain, explicitly say to check the hospital's latest registration page or clinic schedule instead of fabricating details.
11. reason must explain why this hospital-plus-doctor combination matches the patient, referencing symptoms, follow-up needs, or mixed-condition management, and may be slightly more detailed but stay under 140 characters.
12. If retrieval candidates are provided, prefer those hospital and doctor names. If those candidates are too thin, you may supplement with widely known public medical knowledge for that city.
13. If several conditions coexist, favor hospitals that can cover the main combined risks.
14. If the condition is surgery-oriented, prioritize mature surgical teams and doctors with minimally invasive experience.
15. Return JSON array only. No markdown. No explanation.

Allowed keys only:
- hospital
- department
- doctor
 - doctor_title
 - hospital_strength
 - hospital_grade
 - hospital_address
 - booking_method
 - doctor_specialty
 - registration_fee
 - clinic_schedule
 - reason

User context:
- Residence: {monthly_data.get('residence_text', '')}
- Condition focus: {monthly_data.get('condition_text', '')}
- Primary condition: {primary_condition}
- Symptom days: {monthly_data.get('symptom_days', 0)}
- Medication days: {monthly_data.get('medication_days', 0)}
- Monitoring days: {monthly_data.get('monitoring_days', 0)}
- Department hints: {json.dumps(department_hints, ensure_ascii=False)}
- Follow-up reminders: {json.dumps(monthly_data.get('follow_up_reminders', [])[:3], ensure_ascii=False)}
- Retrieval candidates (if any): {json.dumps(evidence_payload, ensure_ascii=False)}
""",
    )
    output = run_local_llm(
        prompt=prompt,
        system_prompt=localize(
            locale,
            "你是医疗就诊路径规划助手。优先从医院层级做筛选，只推荐权威公立三甲医院或大学附属医院。输出必须是 JSON，保守、克制、不编造。",
            "You are a medical care-routing assistant. Filter by hospital authority first and recommend authoritative public tertiary or university-affiliated hospitals only. Output JSON only. Be conservative and do not fabricate.",
        ),
        settings=get_generation_settings(config, "expert_commentary"),
        locale=locale,
        timeout_key="ai_comment_timeout",
        failure_key="ai_comment_failed",
    )
    items = parse_llm_json_array(output)
    recommendations = []
    for item in items:
        normalized = normalize_hospital_recommendation(
            item,
            primary_condition,
            item.get("department") or primary_meta["department"],
            locale,
            fallback_reason=build_condition_hospital_reason(item.get("hospital", ""), primary_condition, locale),
        )
        if normalized and has_named_doctor(normalized.get("doctor", "")):
            recommendations.append(normalized)
    return rank_hospital_recommendations(recommendations, primary_condition)[:MAX_HOSPITAL_RECOMMENDATIONS]


def collect_tavily_hospital_evidence(
    monthly_data: dict,
    locale: str,
    config: dict,
    condition_queries: Dict[str, dict],
    location_hints: List[str],
    residence_text: str,
) -> List[dict]:
    if not has_tavily_api_key(config):
        return []

    primary_condition = monthly_data.get("primary_condition") or monthly_data.get("conditions", ["gallstones"])[0]
    ordered_conditions = [primary_condition] + [item for item in monthly_data.get("conditions", []) if item != primary_condition]
    seen = set()
    evidence = []

    for condition in ordered_conditions:
        meta = condition_queries.get(condition)
        if not meta:
            continue
        results = tavily_search(meta["query"], max_results=4, config=config)
        for result in results:
            raw_title = str(result.get("title") or "").strip()
            content = strip_search_noise(str(result.get("content", "") or ""))
            hospital = extract_hospital_name(f"{raw_title} {content}") or raw_title or localize(locale, f"{residence_text} 重点医院", f"{residence_text} key hospital")
            raw_blob = f"{raw_title} {content} {hospital}"
            if location_hints and not any(hint in raw_blob for hint in location_hints):
                continue
            if not is_valid_hospital_name(hospital):
                continue
            if not is_authoritative_hospital_candidate(hospital, raw_blob):
                continue
            dedupe_key = hospital.lower()
            if dedupe_key in seen:
                continue
            evidence.append(
                {
                    "hospital": trim_text(hospital, 32),
                    "department": meta["department"],
                    "doctor": extract_doctor_name(raw_blob),
                    "reason": clean_hospital_reason(content, locale, max_length=100),
                    "source_excerpt": clean_search_excerpt(content, locale, max_length=160),
                    "condition": condition,
                }
            )
            seen.add(dedupe_key)
            if len(evidence) >= 8:
                break
        if len(evidence) >= 8:
            break

    return evidence


def build_tavily_hospital_recommendations(
    evidence_candidates: List[dict],
    monthly_data: dict,
    locale: str,
    condition_queries: Dict[str, dict],
) -> List[dict]:
    primary_condition = monthly_data.get("primary_condition") or monthly_data.get("conditions", ["gallstones"])[0]
    primary_meta = condition_queries.get(primary_condition, next(iter(condition_queries.values())))
    recommendations = []
    for item in evidence_candidates:
        condition = item.get("condition") or primary_condition
        meta = condition_queries.get(condition, primary_meta)
        normalized = normalize_hospital_recommendation(
            item,
            condition,
            meta["department"],
            locale,
            fallback_reason=build_condition_hospital_reason(item.get("hospital", ""), condition, locale),
        )
        if not normalized:
            continue
        recommendations.append(normalized)
    return rank_hospital_recommendations(recommendations, primary_condition)[:MAX_HOSPITAL_RECOMMENDATIONS]


def refine_hospital_recommendations_with_llm(
    candidates: List[dict], monthly_data: dict, config: dict, locale: str
) -> List[dict]:
    if not candidates:
        return []

    payload = [
        {
            "hospital": item.get("hospital", ""),
            "department": item.get("department", ""),
            "doctor": item.get("doctor", ""),
            "doctor_title": item.get("doctor_title", ""),
            "hospital_strength": item.get("hospital_strength", ""),
            "hospital_grade": item.get("hospital_grade", ""),
            "hospital_address": item.get("hospital_address", ""),
            "booking_method": item.get("booking_method", ""),
            "doctor_specialty": item.get("doctor_specialty", ""),
            "registration_fee": item.get("registration_fee", ""),
            "clinic_schedule": item.get("clinic_schedule", ""),
            "reason": item.get("reason", ""),
            "source_excerpt": item.get("source_excerpt", ""),
        }
        for item in candidates[:8]
    ]
    prompt = localize(
        locale,
        f"""请把以下医院候选严格清洗并补全成 JSON 数组，字段只能保留 hospital、department、doctor、doctor_title、hospital_strength、hospital_grade、hospital_address、booking_method、doctor_specialty、registration_fee、clinic_schedule、reason。

要求：
1. 你在推荐医院时，必须进行严格的数据清洗。
2. 严禁输出网页导航文本、视频时间轴或冗长的追踪链接。
3. 优先级必须严格满足：顶级三甲医院 > 三甲医院 > 区域医疗中心。
4. doctor 必须尽量输出真实医生姓名 + 职称；如果该候选无法可靠给出医生姓名，请直接丢弃该候选，不要用“优先预约专家门诊”之类的占位词。
5. hospital_strength 概括医院平台或专科优势，不超过 60 字；doctor_specialty 概括医生擅长方向，不超过 60 字；reason 说明和当前患者的契合度，不超过 140 字。
6. 如果能确认，请补 hospital_grade、hospital_address、booking_method、registration_fee、clinic_schedule；如果不能确认挂号费或坐诊时间，必须写“以医院最新挂号页面为准”或“以医院最新排班为准”，不要编造。
7. 可以优先利用候选中的真实医院/医生信息；如果候选太弱，可以结合你掌握的公开常识补充同城更权威的公立三甲医院与医生。
8. 只返回 JSON 数组，不要返回 Markdown，不要解释。
9. 管理目标：{monthly_data.get('condition_text', '')}；常居地：{monthly_data.get('residence_text', '')}。

候选数据：
{json.dumps(payload, ensure_ascii=False, indent=2)}""",
        f"""Clean and enrich the following hospital candidates into a strict JSON array. Allowed keys: hospital, department, doctor, doctor_title, hospital_strength, hospital_grade, hospital_address, booking_method, doctor_specialty, registration_fee, clinic_schedule, reason.

Rules:
1. You must aggressively clean the data.
2. Never output navigation text, video timeline text, or long tracking links.
3. The ranking must strictly follow: top-tier tertiary hospital > tertiary hospital > regional medical center.
4. The doctor field should contain a real doctor name plus title whenever possible. If one candidate cannot support a reliable named doctor, drop that candidate instead of using a placeholder clinic label.
5. hospital_strength should summarize the hospital advantage in under 60 characters; doctor_specialty should summarize the doctor's focus in under 60 characters; reason should explain patient fit in under 140 characters.
6. Fill hospital_grade, hospital_address, booking_method, registration_fee, and clinic_schedule when you can. If fee or schedule cannot be confirmed, explicitly say to check the latest hospital registration page or clinic schedule instead of fabricating details.
7. Prefer the real hospitals and doctors already present in the candidate pool. If the candidate pool is thin, you may supplement with widely known public tertiary hospitals and doctors in the same city.
8. Return JSON only. No markdown. No explanation.
9. Condition focus: {monthly_data.get('condition_text', '')}; residence: {monthly_data.get('residence_text', '')}.

Candidate data:
{json.dumps(payload, ensure_ascii=False, indent=2)}""",
    )
    output = run_local_llm(
        prompt=prompt,
        system_prompt=localize(
            locale,
            "你是医疗信息清洗助手。你只做结构化提取和数据去噪，不添加宣传语，不输出链接，不编造信息。",
            "You are a medical data-cleaning assistant. Only extract and denoise structured data. No links, no hype, no fabrication.",
        ),
        settings=get_generation_settings(config, "expert_commentary"),
        locale=locale,
        timeout_key="ai_comment_timeout",
        failure_key="ai_comment_failed",
    )
    if not output:
        return []

    cleaned = []
    primary_condition = monthly_data.get("primary_condition") or monthly_data.get("conditions", ["gallstones"])[0]
    for item in parse_llm_json_array(output):
        normalized = normalize_hospital_recommendation(
            item,
            primary_condition,
            item.get("department") or localize(locale, "肝胆外科 / 普外科", "Hepatobiliary surgery / general surgery"),
            locale,
            fallback_reason=build_condition_hospital_reason(item.get("hospital", ""), primary_condition, locale),
        )
        if normalized and has_named_doctor(normalized.get("doctor", "")):
            cleaned.append(normalized)
    return rank_hospital_recommendations(cleaned, primary_condition)[:MAX_HOSPITAL_RECOMMENDATIONS]


def build_hospital_recommendations(monthly_data: dict, profile: dict, locale: str, config: Optional[dict] = None) -> tuple[List[dict], str]:
    primary_condition = monthly_data.get("primary_condition")
    if is_lifestyle_mode(primary_condition, monthly_data.get("population_branch")):
        return [], "local"

    # 基于用户个人档案的就医分析（胆结石专属）
    user_recommendations = []
    if primary_condition == "gallstones" and profile.get("medical_history", {}).get("gallstones"):
        gallstones_history = profile["medical_history"]["gallstones"]
        ultrasound_records = gallstones_history.get("ultrasound_records", [])
        recent_visits = profile.get("recent_medical_visits", [])
        
        # 分析是否需要就医
        needs_followup = False
        followup_reason = ""
        
        # 检查最近彩超记录
        if ultrasound_records:
            latest = ultrasound_records[-1]
            stone_size = float(latest.get("max_stone_cm", 0) or 0)
            wall_thickness = latest.get("gallbladder_wall", "")
            
            # 结石>1cm 或胆囊壁毛糙/增厚 → 建议复查
            if stone_size >= 1.0 or "毛糙" in wall_thickness or "增厚" in wall_thickness:
                needs_followup = True
                followup_reason = localize(
                    locale,
                    f"最近彩超显示结石{stone_size}cm，胆囊壁{wall_thickness}，建议 3 个月内复查彩超和肝功能。",
                    f"Recent ultrasound shows {stone_size}cm gallstone with gallbladder wall {wall_thickness}. Follow-up ultrasound and liver function test recommended within 3 months."
                )
        
        # 检查是否有近期就医记录
        if recent_visits:
            latest_visit = recent_visits[-1]
            follow_up_plan = latest_visit.get("follow_up_plan", {})
            next_visit_date = follow_up_plan.get("next_visit_date", "")
            
            # 如果复查日期临近（30 天内），提醒就医
            if next_visit_date:
                try:
                    from datetime import datetime, timedelta
                    next_date = datetime.strptime(next_visit_date, "%Y-%m-%d")
                    days_until = (next_date - datetime.now()).days
                    if 0 <= days_until <= 30:
                        needs_followup = True
                        followup_reason = localize(
                            locale,
                            f"医生建议{next_visit_date}复查（{days_until}天后），请按时进行腹部彩超和肝功能检查。",
                            f"Doctor recommended follow-up on {next_visit_date} ({days_until} days). Please schedule abdominal ultrasound and liver function test."
                        )
                except:
                    pass
        
        # 如果需要就医，生成推荐
        if needs_followup and recent_visits:
            latest_visit = recent_visits[-1]
            user_recommendations.append({
                "hospital": latest_visit.get("hospital", ""),
                "department": latest_visit.get("department", ""),
                "doctor_name": latest_visit.get("doctor", {}).get("name", "") if isinstance(latest_visit.get("doctor"), dict) else latest_visit.get("doctor", ""),
                "doctor_title": localize(locale, "复诊", "Follow-up"),
                "reason": followup_reason,
                "priority": "high",
                "source": "user_medical_history"
            })

    residence = monthly_data.get("residence", {}) or {}
    residence_text = residence.get("display_name", "")
    residence_label = residence.get("city") or residence_text
    if not residence_text:
        # 如果没有居住地信息，但用户档案有就医推荐，返回用户档案推荐
        if user_recommendations:
            return user_recommendations, "user_medical_history"
        return [], "fallback"
    location_hints = [str(item or "").strip() for item in [residence.get("province"), residence.get("city"), residence_text] if str(item or "").strip()]

    condition_queries = {
        "gallstones": {
            "department": localize(locale, "肝胆外科 / 普外科", "Hepatobiliary surgery / general surgery"),
            "query": localize(locale, f"{residence_text} 胆结石 慢性胆囊炎 公立三甲医院 肝胆外科 专家门诊 三级甲等", f"{residence_text} gallstones chronic cholecystitis public tertiary hospital hepatobiliary surgery specialist clinic"),
            "reason": localize(locale, "适合需要结合彩超、症状频次和胆囊炎风险一起评估的情况。", "This fits cases that need combined review of ultrasound, symptom frequency, and chronic gallbladder inflammation risk."),
        },
        "hypertension": {
            "department": localize(locale, "心内科 / 高血压门诊", "Cardiology / hypertension clinic"),
            "query": localize(locale, f"{residence_text} 高血压 公立三甲医院 心内科 高血压门诊 专家 三级甲等", f"{residence_text} hypertension public tertiary hospital cardiology hypertension clinic specialist"),
            "reason": localize(locale, "更适合评估血压波动、靶器官风险和长期用药调整。", "This is a better fit for blood-pressure variability, target-organ risk, and long-term medication adjustment."),
        },
        "diabetes": {
            "department": localize(locale, "内分泌科 / 糖尿病门诊", "Endocrinology / diabetes clinic"),
            "query": localize(locale, f"{residence_text} 糖尿病 公立三甲医院 内分泌科 专家门诊 三级甲等", f"{residence_text} diabetes public tertiary hospital endocrinology specialist clinic"),
            "reason": localize(locale, "更适合联合评估血糖、HbA1c、并发症筛查与饮食用药方案。", "This fits combined review of glucose, HbA1c, complication screening, and treatment planning."),
        },
        "fat_loss": {
            "department": localize(locale, "临床营养科 / 运动医学门诊", "Clinical nutrition / sports medicine"),
            "query": localize(locale, f"{residence_text} 公立三甲医院 临床营养科 运动医学 减脂 门诊 三级甲等", f"{residence_text} public tertiary hospital clinical nutrition sports medicine fat loss clinic"),
            "reason": localize(locale, "更适合平台期、体脂管理和训练恢复问题的结构化复盘。", "This is a stronger fit for plateau review, body-fat management, and training recovery."),
        },
    }

    meta = condition_queries.get(primary_condition, next(iter(condition_queries.values())))
    fallback = build_local_rule_hospital_recommendations(residence_label, residence_text, primary_condition, meta["department"], locale)
    if resolve_locale(locale=locale) == "ja-JP" and fallback:
        return fallback, "fallback"

    tavily_evidence = collect_tavily_hospital_evidence(
        monthly_data,
        locale,
        config or {},
        condition_queries,
        location_hints,
        residence_text,
    )

    llm_evidence_candidates = merge_hospital_recommendations(tavily_evidence, fallback, limit=8)
    llm_recommendations = build_llm_hospital_recommendations(
        monthly_data,
        locale,
        config or {},
        condition_queries,
        evidence_candidates=llm_evidence_candidates,
    )
    tavily_recommendations = build_tavily_hospital_recommendations(
        tavily_evidence,
        monthly_data,
        locale,
        condition_queries,
    )
    refined_recommendations = []
    if not llm_recommendations:
        refined_recommendations = refine_hospital_recommendations_with_llm(
            llm_evidence_candidates,
            monthly_data,
            config or {},
            locale,
        )
    
    if llm_recommendations:
        named_tavily = [item for item in tavily_recommendations if has_named_doctor(item.get("doctor", ""))]
        secondary = named_tavily if named_tavily else []
        # 合并用户档案推荐
        all_recommendations = user_recommendations + llm_recommendations + secondary
        return merge_and_rank_hospital_recommendations(all_recommendations, [], primary_condition, limit=MAX_HOSPITAL_RECOMMENDATIONS), "llm"
    if refined_recommendations:
        secondary = [item for item in tavily_recommendations if has_named_doctor(item.get("doctor", ""))]
        if not secondary:
            secondary = [item for item in fallback if has_named_doctor(item.get("doctor", ""))]
        # 合并用户档案推荐
        all_recommendations = user_recommendations + refined_recommendations + secondary
        return merge_and_rank_hospital_recommendations(all_recommendations, [], primary_condition, limit=MAX_HOSPITAL_RECOMMENDATIONS), "llm"
    if tavily_recommendations:
        # 合并用户档案推荐
        all_recommendations = user_recommendations + tavily_recommendations + fallback
        return merge_and_rank_hospital_recommendations(all_recommendations, [], primary_condition, limit=MAX_HOSPITAL_RECOMMENDATIONS), "fallback_tavily"

    # 合并用户档案推荐
    all_recommendations = user_recommendations + fallback
    print(f"[DEBUG] Returning fallback recommendations with source='fallback'", file=sys.stderr)
    return merge_and_rank_hospital_recommendations(all_recommendations, [], primary_condition, limit=MAX_HOSPITAL_RECOMMENDATIONS), "fallback"


def build_monthly_fallback_review(monthly_data: dict, profile: dict, locale: str, config: Optional[dict] = None) -> tuple[str, str]:
    macro_scores = monthly_data.get("macro_scores", {})
    primary_condition = monthly_data.get("primary_condition")
    is_ja = resolve_locale(locale=locale) == "ja-JP"
    low_dims = [
        label
        for key, label in [
            ("diet", localize(locale, "饮食", "diet")),
            ("water", localize(locale, "饮水", "hydration")),
            ("exercise", localize(locale, "运动", "exercise")),
            ("monitoring", localize(locale, "监测", "monitoring")),
        ]
        if macro_scores.get(key, 0) < 70
    ]
    symptom_distribution = monthly_data.get("symptom_distribution", {})
    top_symptoms = list(symptom_distribution.items())[:2]
    symptom_text = (
        "、".join(f"{label} {count}次" for label, count in top_symptoms)
        if resolve_locale(locale=locale) == "zh-CN"
        else "、".join(f"{label} {count}回" for label, count in top_symptoms) if is_ja else ", ".join(f"{label} {count}x" for label, count in top_symptoms)
    )

    if is_lifestyle_mode(primary_condition, monthly_data.get("population_branch")):
        weakest_text = "、".join(low_dims) if resolve_locale(locale=locale) in {"zh-CN", "ja-JP"} else ", ".join(low_dims)
        findings = localize_three(
            locale,
            f"本月平均综合评分约 {monthly_data.get('avg_total_score', 0):.1f}/100，月均热量 {monthly_data.get('avg_calories', 0):.0f} kcal、饮水 {monthly_data.get('avg_water', 0):.0f} ml、步数 {monthly_data.get('avg_steps', 0):.0f} 步。"
            + (
                f" 体重月内变化 {monthly_data.get('weight_change', 0):.2f}kg。"
                if monthly_data.get("latest_weight") is not None
                else ""
            ),
            f"The average overall score was about {monthly_data.get('avg_total_score', 0):.1f}/100, with roughly {monthly_data.get('avg_calories', 0):.0f} kcal, {monthly_data.get('avg_water', 0):.0f} ml hydration, and {monthly_data.get('avg_steps', 0):.0f} steps per day."
            + (
                f" Weight changed by {monthly_data.get('weight_change', 0):.2f} kg across the month."
                if monthly_data.get("latest_weight") is not None
                else ""
            ),
            f"今月の平均総合スコアは約 {monthly_data.get('avg_total_score', 0):.1f}/100 で、平均摂取量は {monthly_data.get('avg_calories', 0):.0f} kcal、平均飲水量は {monthly_data.get('avg_water', 0):.0f} ml、平均歩数は {monthly_data.get('avg_steps', 0):.0f} 歩でした。"
            + (
                f" 体重変化は月内で {monthly_data.get('weight_change', 0):.2f} kg です。"
                if monthly_data.get("latest_weight") is not None
                else ""
            ),
        )

        watch_parts = []
        if weakest_text:
            watch_parts.append(
                localize_three(
                    locale,
                    f"当前最弱的执行维度是：{weakest_text}。",
                    f"The weakest execution dimensions right now are: {weakest_text}.",
                    f"現在もっとも弱い実行項目は {weakest_text} です。",
                )
            )
        if monthly_data.get("valid_weight_days", 0) < max(4, monthly_data.get("observed_days", 0) // 4):
            watch_parts.append(
                localize_three(
                    locale,
                    "体重与体脂记录密度偏低，趋势判断容易被偶然波动放大。",
                    "Weight and body-fat logging are still sparse, so trends may be distorted by one-off fluctuations.",
                    "体重と体脂率の記録密度が低く、単発の変動に引っ張られやすい状態です。",
                )
            )
        if str(primary_condition) == "fat_loss":
            if float(monthly_data.get("weight_change", 0) or 0) >= 0:
                watch_parts.append(
                    localize_three(
                        locale,
                        "减脂模式下体重没有形成稳定下行，说明热量缺口、训练负荷或作息恢复至少有一项还不够稳定。",
                        "In fat-loss mode the trend is not yet moving down consistently, which usually means the calorie deficit, training load, or recovery routine is still unstable.",
                        "減脂モードで体重が安定して下がっていないため、赤字設定・運動負荷・回復習慣のどれかがまだ不安定です。",
                    )
                )
            elif abs(float(monthly_data.get("weight_change", 0) or 0)) > 2.5:
                watch_parts.append(
                    localize_three(
                        locale,
                        "本月下降速度偏快，除了继续关注体脂，也要警惕恢复不足和瘦体重流失。",
                        "The rate of loss was relatively fast this month, so body-fat progress should be tracked together with recovery quality and lean-mass protection.",
                        "今月は減少ペースがやや速く、体脂肪だけでなく回復不足や除脂肪体重の低下にも注意が必要です。",
                    )
                )
        elif symptom_text:
            watch_parts.append(
                localize_three(
                    locale,
                    f"本月也出现过不适记录，主要集中在：{symptom_text}。",
                    f"There were still some discomfort entries this month, mainly: {symptom_text}.",
                    f"今月は不調記録もあり、主な内容は {symptom_text} でした。",
                )
            )
        if not watch_parts:
            watch_parts.append(
                localize_three(
                    locale,
                    "整体执行面比较平稳，但作息规律、三大营养素比例和训练结构仍值得持续微调。",
                    "Execution was broadly steady overall, but sleep timing, macro balance, and training structure still deserve fine-tuning.",
                    "全体としては安定していますが、睡眠リズム・三大栄養素の配分・運動構成は引き続き微調整する価値があります。",
                )
            )

        current_weight = float(monthly_data.get("latest_weight") or monthly_data.get("avg_weight") or profile.get("current_weight_kg") or 60)
        protein_target = max(90, int(round(current_weight * (1.6 if str(primary_condition) == "fat_loss" else 1.3))))
        water_target = int(profile.get("water_target_ml", 2000) or 2000)
        plan = "\n".join(
            [
                localize_three(
                    locale,
                    f"1. 饮食宏观结构微调：把蛋白质稳定到每天约 {protein_target}g，控制工作日与周末之间的热量波动，并优先保证蔬菜、全谷物和优质脂肪的稳定出现。",
                    f"1. Macro adjustment: keep protein near {protein_target}g per day, reduce weekday-versus-weekend calorie swings, and keep vegetables, whole grains, and quality fats consistently present.",
                    f"1. 食事マクロ調整：たんぱく質を 1 日 {protein_target}g 前後で安定させ、平日と週末のカロリー差を抑えつつ、野菜・全粒穀物・良質な脂質を欠かさないようにします。",
                ),
                localize_three(
                    locale,
                    "2. 运动负荷建议：把有氧与力量训练分开规划，优先保证每周 2-3 次力量训练，再用步数或骑行去补足基础活动量。",
                    "2. Training load: plan cardio and resistance work separately, protect 2-3 strength sessions per week first, and use steps or cycling to fill the aerobic base.",
                    "2. 運動負荷の提案：有酸素運動と筋力トレーニングを分けて設計し、まず週 2〜3 回の筋トレを確保したうえで、歩数やサイクリングで基礎活動量を補います。",
                ),
                localize_three(
                    locale,
                    f"3. 作息与补剂建议：优先把睡眠、进餐时间和饮水节奏稳定下来，饮水目标至少维持在 {water_target}ml；若训练量偏高，再结合日常饮食评估 Omega-3、维生素 D 或电解质是否需要补充。",
                    f"3. Recovery and supplements: stabilize sleep, meal timing, and hydration first, keeping at least {water_target} ml of fluid daily; only then review whether omega-3, vitamin D, or electrolytes make sense for your routine.",
                    f"3. 生活リズムと補助提案：まず睡眠・食事時間・飲水リズムを安定させ、飲水量は少なくとも {water_target} ml を目安に保ちます。そのうえで、運動量が高い場合のみ Omega-3・ビタミンD・電解質の補助を検討します。",
                ),
            ]
        )

        source = "fallback"
        if has_tavily_api_key(config):
            query = localize_three(
                locale,
                f"{monthly_data.get('condition_text')} 月度健康复盘 饮食 运动 睡眠 体脂 管理建议",
                f"{monthly_data.get('condition_text')} monthly health review diet exercise sleep body fat management advice",
                f"{monthly_data.get('condition_text')} 月次レビュー 食事 運動 睡眠 体脂肪 管理アドバイス",
            )
            search_results = tavily_search(query, max_results=2, config=config)
            snippets = []
            for result in search_results:
                content = clean_search_excerpt(str(result.get("content", "") or ""), locale, max_length=140)
                if content:
                    snippets.append(content)
            if snippets:
                plan = f"{plan}\n{localize_three(locale, f'参考观点：{snippets[0]}', f'Reference note: {snippets[0]}', f'参考メモ：{snippets[0]}')}"
                source = "fallback_tavily"

        blueprint = get_monthly_review_blueprint(primary_condition, monthly_data.get("population_branch"))
        return (
            format_monthly_review_sections(
                locale,
                [
                    {**blueprint[0], "body": findings},
                    {**blueprint[1], "body": " ".join(watch_parts)},
                    {**blueprint[2], "body": plan},
                ],
            ),
            source,
        )

    findings = (
        f"今月は {monthly_data.get('condition_text')} を中心に管理し、月平均総合評価は {monthly_data.get('avg_total_score', 0):.1f}/100 でした。"
        f" 食事・飲水・運動・服薬・モニタリングの達成率は {macro_scores.get('diet', 0):.0f}% / {macro_scores.get('water', 0):.0f}% / {macro_scores.get('exercise', 0):.0f}% / {macro_scores.get('medication', 0):.0f}% / {macro_scores.get('monitoring', 0):.0f}% です。"
        if is_ja
        else localize(
            locale,
            f"本月围绕 {monthly_data.get('condition_text')} 进行管理，月均综合评分 {monthly_data.get('avg_total_score', 0):.1f}/100。饮食、饮水、运动、用药、监测完成度分别为 {macro_scores.get('diet', 0):.0f}% / {macro_scores.get('water', 0):.0f}% / {macro_scores.get('exercise', 0):.0f}% / {macro_scores.get('medication', 0):.0f}% / {macro_scores.get('monitoring', 0):.0f}%。",
            f"This month focused on {monthly_data.get('condition_text')} management, with an average overall score of {monthly_data.get('avg_total_score', 0):.1f}/100. Diet, hydration, exercise, medication, and monitoring completion landed at {macro_scores.get('diet', 0):.0f}% / {macro_scores.get('water', 0):.0f}% / {macro_scores.get('exercise', 0):.0f}% / {macro_scores.get('medication', 0):.0f}% / {macro_scores.get('monitoring', 0):.0f}%.",
        )
    )

    risk_parts = [
        (
            f"今月は症状日が {monthly_data.get('symptom_days', 0)} 日、服薬日が {monthly_data.get('medication_days', 0)} 日、モニタリング日が {monthly_data.get('monitoring_days', 0)} 日ありました。"
            if is_ja
            else localize(
                locale,
                f"本月记录到 {monthly_data.get('symptom_days', 0)} 天症状、{monthly_data.get('medication_days', 0)} 天用药、{monthly_data.get('monitoring_days', 0)} 天监测。",
                f"This month included {monthly_data.get('symptom_days', 0)} symptom days, {monthly_data.get('medication_days', 0)} medication days, and {monthly_data.get('monitoring_days', 0)} monitoring days.",
            )
        )
    ]
    if symptom_text:
        risk_parts.append(f"症状は主に {symptom_text} でした。" if is_ja else localize(locale, f"症状以 {symptom_text} 为主。", f"The symptom mix was led by {symptom_text}."))

    primary_condition = monthly_data.get("primary_condition")
    if primary_condition == "gallstones":
        risk_parts.append(
            f"胆石管理では月平均脂質摂取が約 {monthly_data.get('avg_fat', 0):.1f}g でした。高脂質日と不調日が重なる場合は、夕食と間食を重点的に見直してください。"
            if is_ja
            else localize(
                locale,
                f"胆结石专项上，月均脂肪摄入约 {monthly_data.get('avg_fat', 0):.1f}g。若高脂日与不适日重叠，需要重点复盘晚餐和加餐。",
                f"For gallstone care, average fat intake was about {monthly_data.get('avg_fat', 0):.1f}g. If higher-fat days overlap with symptoms, dinner and snack patterns need closer review.",
            )
        )
    elif primary_condition == "hypertension":
        risk_parts.append("血圧箱ひげ図のばらつきが大きい場合は、睡眠、塩分、服薬時間を見直す必要があります。" if is_ja else localize(locale, "若血压箱线图离散度偏大，说明波动仍明显，需要回看作息、盐分与服药时间。", "If the blood-pressure boxplot stays wide, variability remains meaningful and sleep, sodium, and medication timing deserve review."))
    elif primary_condition == "fat_loss":
        risk_parts.append(f"体重の月間変化は約 {monthly_data.get('weight_change', 0):.2f}kg で、減り方が速すぎる場合は回復不足や胆嚢への刺激にも注意が必要です。" if is_ja else localize(locale, f"体重月变化约 {monthly_data.get('weight_change', 0):.2f}kg，若下降过快也要警惕恢复不足与胆囊刺激。", f"Monthly weight change was about {monthly_data.get('weight_change', 0):.2f}kg; if the drop is too fast, recovery strain and gallbladder irritation are still worth watching."))

    plan_parts = [
        "来月はまず低得点の項目を立て直し、そのうえで病態別の比較を続けてください。"
        if is_ja
        else localize(
            locale,
            "下月建议优先把低分维度拉稳，再继续做病种专项对照。",
            "Next month should first stabilize the weaker adherence dimensions, then continue disease-specific comparisons.",
        )
    ]
    if low_dims:
        gap_text = "、".join(low_dims) if is_ja or resolve_locale(locale=locale) == "zh-CN" else ", ".join(low_dims)
        plan_parts.append(f"現在の最優先課題は {gap_text} です。" if is_ja else localize(locale, f"当前优先级最高的是：{gap_text}。", f"The highest-priority gaps now are: {gap_text}."))
    plan_parts.append(
        "誘因、症状の持続時間、再検査結果を引き続き日記に残すと、次回の月報グラフがより判断しやすくなります。"
        if is_ja
        else localize(
            locale,
            "建议把诱因、症状持续时间、复查结果继续写进日记，月报中的趋势图会更有判断价值。",
            "Keep logging triggers, symptom duration, and follow-up results so next month's charts become more clinically useful.",
        )
    )

    sections = [
        ("核心发现", "Key Findings", " ".join(findings.split())),
        ("风险提示", "Risk Watch", " ".join(" ".join(risk_parts).split())),
        ("下月调整", "Next-Month Actions", " ".join(" ".join(plan_parts).split())),
    ]

    source = "fallback"
    gap_topics = []
    for key, label in [("diet", "diet"), ("water", "hydration"), ("exercise", "exercise"), ("monitoring", "monitoring")]:
        if macro_scores.get(key, 0) < 70:
            gap_topics.append(label)
    if has_tavily_api_key(config) and gap_topics:
        query = (
            f"{monthly_data.get('condition_text')} 患者教育 月間セルフマネジメント {' '.join(gap_topics[:3])} 振り返り提案"
            if is_ja
            else localize(
                locale,
                f"{monthly_data.get('condition_text')} 患者教育 月度管理 {' '.join(gap_topics[:3])} 复盘建议",
                f"{monthly_data.get('condition_text')} patient education monthly self-management review {' '.join(gap_topics[:3])}",
            )
        )
        search_results = tavily_search(query, max_results=2, config=config)
        snippets = []
        for result in search_results:
            content = clean_search_excerpt(str(result.get("content", "") or ""), locale, max_length=150)
            if is_ja and content and not re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", content):
                continue
            if re.search(r"(責任著者|corresponding author|doi|figure|table)", str(content or ""), re.IGNORECASE):
                continue
            if content:
                snippets.append(content)
        if snippets:
            sections.append(("检索补充", "Retrieved Note", snippets[0]))
            source = "fallback_tavily"

    return format_monthly_review_sections(locale, sections), source


def get_ai_monthly_review(monthly_data: dict, profile: dict, config: dict, locale: str) -> tuple[str, str]:
    primary_condition = monthly_data.get("primary_condition")
    if is_lifestyle_mode(primary_condition, monthly_data.get("population_branch")):
        if resolve_locale(locale=locale) == "ja-JP":
            prompt = f"""次の 30 日分の健康データをもとに、生活習慣レビューを作成してください。余計な前置きは禁止です。以下の見出しをこの順番でそのまま使ってください。
**【核心发现】**
2-3 文で、今月の全体傾向・実行度・体重または体脂肪の方向性を要約する。

**【体态与习惯预警】**
2 文で、睡眠・食事バランス・運動構成・記録不足など、来月に持ち越したくない注意点を書く。

**【次月高阶干预清单】**
以下の 3 行を必ず含めること。各行は具体的な行動にする。
1. 饮食宏观结构微调：
2. 运动负荷建议：
3. 作息与补剂建议：

ユーザー: {profile.get('name', 'User')}
主目標: {monthly_data.get('condition_text')}
月平均総合スコア: {monthly_data.get('avg_total_score', 0):.1f}
達成率: {json.dumps(monthly_data.get('macro_scores', {}), ensure_ascii=False)}
月平均カロリー: {monthly_data.get('avg_calories', 0):.0f} kcal
月平均飲水量: {monthly_data.get('avg_water', 0):.0f} ml
月平均歩数: {monthly_data.get('avg_steps', 0):.0f}
体重変化: {monthly_data.get('weight_change', 0):.2f} kg
平均体脂率: {monthly_data.get('avg_body_fat_percent', 0):.1f}%
症状日数: {monthly_data.get('symptom_days', 0)}
ハイライト: {" | ".join(monthly_data.get('macro_highlights', []))}
"""
        else:
            prompt = localize(
                locale,
                f"""请基于最近 30 天的数据，输出一份生活方式导向的月度复盘，不要写任何额外开场白，且必须严格使用以下结构：
**【核心发现】**
2-3 句，总结本月整体趋势、依从性，以及体重/体脂方向。

**【体态与习惯预警】**
2 句，指出睡眠、三大营养素、训练结构、记录密度等最需要警惕的问题。

**【次月高阶干预清单】**
必须包含下面 3 行，并给出非常具体的行动点：
1. 饮食宏观结构微调：
2. 运动负荷建议：
3. 作息与补剂建议：

用户：{profile.get('name', '用户')}
主目标：{monthly_data.get('condition_text')}
月均综合评分：{monthly_data.get('avg_total_score', 0):.1f}
达标率：{json.dumps(monthly_data.get('macro_scores', {}), ensure_ascii=False)}
月均热量：{monthly_data.get('avg_calories', 0):.0f} kcal
月均饮水：{monthly_data.get('avg_water', 0):.0f} ml
月均步数：{monthly_data.get('avg_steps', 0):.0f}
体重变化：{monthly_data.get('weight_change', 0):.2f} kg
平均体脂率：{monthly_data.get('avg_body_fat_percent', 0):.1f}%
症状天数：{monthly_data.get('symptom_days', 0)}
亮点：{" | ".join(monthly_data.get('macro_highlights', []))}
""",
                f"""Write a lifestyle-oriented monthly review from the last 30 days with no extra introduction and keep this exact structure:
**[Core Findings]**
2-3 sentences summarizing overall trend, adherence, and body-composition direction.

**[Body Composition & Habit Watch]**
2 sentences on the biggest warnings around sleep, macro balance, training structure, or missing logs.

**[Advanced Next-Month Checklist]**
You must include the following three lines with concrete actions:
1. Macro adjustment:
2. Training load:
3. Recovery and supplements:

User: {profile.get('name', 'User')}
Primary goal: {monthly_data.get('condition_text')}
Average overall score: {monthly_data.get('avg_total_score', 0):.1f}
Goal rates: {json.dumps(monthly_data.get('macro_scores', {}), ensure_ascii=False)}
Average calories: {monthly_data.get('avg_calories', 0):.0f} kcal
Average hydration: {monthly_data.get('avg_water', 0):.0f} ml
Average steps: {monthly_data.get('avg_steps', 0):.0f}
Weight change: {monthly_data.get('weight_change', 0):.2f} kg
Average body fat: {monthly_data.get('avg_body_fat_percent', 0):.1f}%
Symptom days: {monthly_data.get('symptom_days', 0)}
Highlights: {" | ".join(monthly_data.get('macro_highlights', []))}
""",
            )
    elif resolve_locale(locale=locale) == "ja-JP":
        prompt = f"""以下の 30 日分の健康データをもとに、月次の病状レビューを約 260-320 文字で作成してください。余計な前置きは不要で、必ず次の構成を守ってください。
**【主要な所見】**
2-3 文で、今月の全体状態、遵守状況、主要トレンドを要約する。

**【注意点】**
2 文で、今月もっとも注意すべき誘因またはモニタリング不足を示す。

**【来月の調整】**
2-3 文で、来月に実行しやすい調整方針を提示する。

利用者: {profile.get('name', '利用者')}
病種・目標: {monthly_data.get('condition_text')}
月平均総合評価: {monthly_data.get('avg_total_score', 0):.1f}
達成率: {json.dumps(monthly_data.get('macro_scores', {}), ensure_ascii=False)}
月平均カロリー: {monthly_data.get('avg_calories', 0):.0f} kcal
月平均飲水量: {monthly_data.get('avg_water', 0):.0f} ml
月平均歩数: {monthly_data.get('avg_steps', 0):.0f}
症状日数: {monthly_data.get('symptom_days', 0)}
症状回数: {monthly_data.get('symptom_events', 0)}
服薬日数: {monthly_data.get('medication_days', 0)}
モニタリング日数: {monthly_data.get('monitoring_days', 0)}
ハイライト: {" | ".join(monthly_data.get('macro_highlights', []))}
症状分布: {json.dumps(monthly_data.get('symptom_distribution', {}), ensure_ascii=False)}
必ず上の 3 見出しで返してください。"""
    else:
        prompt = localize(
            locale,
            f"""请根据以下 30 天健康数据生成一段约 260-320 字的月度病情研判，并严格按以下结构输出，不要添加其他标题或前言：
**【核心发现】**
2-3 句，总结本月整体状态、依从性、关键趋势。

**【风险提示】**
2 句，指出本月最需要警惕的触发因素或监测不足。

**【下月调整】**
2-3 句，给出下个月最可执行的调整方向。

用户：{profile.get('name', '用户')}
病种/目标：{monthly_data.get('condition_text')}
月均综合评分：{monthly_data.get('avg_total_score', 0):.1f}
饮食/饮水/运动/用药/监测达标率：{json.dumps(monthly_data.get('macro_scores', {}), ensure_ascii=False)}
月均热量：{monthly_data.get('avg_calories', 0):.0f} kcal
月均饮水：{monthly_data.get('avg_water', 0):.0f} ml
月均步数：{monthly_data.get('avg_steps', 0):.0f}
症状天数：{monthly_data.get('symptom_days', 0)}
症状次数：{monthly_data.get('symptom_events', 0)}
用药天数：{monthly_data.get('medication_days', 0)}
监测天数：{monthly_data.get('monitoring_days', 0)}
专项亮点：{" | ".join(monthly_data.get('macro_highlights', []))}
症状分布：{json.dumps(monthly_data.get('symptom_distribution', {}), ensure_ascii=False)}
请务必按上述 3 个小标题输出。""",
            f"""Write an approximately 180-230 word monthly clinical-style review and follow this exact structure with no extra intro:
**[Key Findings]**
2-3 sentences on overall status, adherence, and trend direction.

**[Risk Watch]**
2 sentences on the biggest watch-outs or missing monitoring.

**[Next-Month Actions]**
2-3 sentences on the most actionable adjustments for next month.

User: {profile.get('name', 'User')}
Conditions/goals: {monthly_data.get('condition_text')}
Average overall score: {monthly_data.get('avg_total_score', 0):.1f}
Goal rates: {json.dumps(monthly_data.get('macro_scores', {}), ensure_ascii=False)}
Average calories: {monthly_data.get('avg_calories', 0):.0f} kcal
Average hydration: {monthly_data.get('avg_water', 0):.0f} ml
Average steps: {monthly_data.get('avg_steps', 0):.0f}
Symptom days: {monthly_data.get('symptom_days', 0)}
Symptom events: {monthly_data.get('symptom_events', 0)}
Medication days: {monthly_data.get('medication_days', 0)}
Monitoring days: {monthly_data.get('monitoring_days', 0)}
Highlights: {" | ".join(monthly_data.get('macro_highlights', []))}
Symptom mix: {json.dumps(monthly_data.get('symptom_distribution', {}), ensure_ascii=False)}
Return the review with those exact three section headings.""",
        )

    output = run_local_llm(
        prompt=prompt,
        system_prompt=(
            (
                "あなたは生活習慣データを整理する慎重な健康アナリストです。見出し構造を厳守し、余計な導入は書かないでください。"
                if is_lifestyle_mode(primary_condition, monthly_data.get("population_branch")) and resolve_locale(locale=locale) == "ja-JP"
                else "あなたは慎重で専門的な健康データ分析者です。"
                if resolve_locale(locale=locale) == "ja-JP"
                else localize(
                    locale,
                    "你是一位严谨的健康数据分析师。请严格遵守指定结构，不要输出额外寒暄。",
                    "You are a careful and professional health data analyst. Follow the requested structure exactly and do not add small talk.",
                )
            )
        ),
        settings=get_generation_settings(config, "expert_commentary"),
        locale=locale,
        timeout_key="ai_comment_timeout",
        failure_key="weekly_ai_failed",
    )
    if output and len(output.strip()) > 60:
        return ensure_monthly_review_sections(output.strip(), monthly_data, locale, primary_condition=primary_condition), "llm"
    return build_monthly_fallback_review(monthly_data, profile, locale, config=config)


def build_custom_monitoring_summary(monthly_data: dict, locale: str) -> List[dict]:
    summary = []
    for section in monthly_data.get("custom_section_stats", []):
        if section.get("days_recorded", 0) <= 0:
            continue
        lines = [
            localize(locale, f"记录天数：{section.get('days_recorded', 0)} 天", f"Recorded on {section.get('days_recorded', 0)} days"),
            localize(locale, f"累计条目：{section.get('items', 0)} 条", f"Total items: {section.get('items', 0)}"),
        ]
        for item in section.get("latest_items", [])[:2]:
            lines.append(localize(locale, f"最近记录：{item}", f"Latest entry: {item}"))
        summary.append({"title": section.get("title", ""), "lines": lines})
    return summary[:4]


def generate_monthly_text_report(monthly_data: dict, profile: dict, ai_review: str, locale: str, review_source: str, recommendation_source: str) -> str:
    def section(title: str, icon: str) -> str:
        return f"{icon} {title}"

    primary_condition = monthly_data.get("primary_condition")
    population_branch = monthly_data.get("population_branch")
    lifestyle_mode = is_lifestyle_mode(primary_condition, population_branch)
    deep_dive_title = monthly_section_label(locale, primary_condition, "deep_dive", population_branch)
    ai_review_title = monthly_section_label(locale, primary_condition, "ai_review", population_branch)
    follow_up_title = monthly_section_label(locale, primary_condition, "follow_up", population_branch)
    hospital_title = monthly_section_label(locale, primary_condition, "hospital", population_branch)

    profile_lines = [
        f"- 👤 {localize(locale, '姓名', 'Name')}: {profile.get('name', '-')}",
        f"- 🎯 {localize(locale, '管理目标', 'Conditions')}: {monthly_data.get('condition_text', '-')}",
        f"- 🗓️ {localize(locale, '周期', 'Period')}: {monthly_data.get('start_date')} ~ {monthly_data.get('end_date')}",
        f"- 📍 {localize(locale, '常居地', 'Residence')}: {monthly_data.get('residence_text') or localize(locale, '未配置', 'Not configured')}",
    ]
    summary_lines = [
        f"- 🏆 {localize(locale, '月均综合评分', 'Average overall score')}: {monthly_data.get('avg_total_score', 0):.1f}/100",
        f"- 🍽️ {localize(locale, '饮食达标率', 'Diet goal rate')}: {monthly_data.get('macro_scores', {}).get('diet', 0):.0f}%",
        f"- 💧 {localize(locale, '饮水达标率', 'Hydration goal rate')}: {monthly_data.get('macro_scores', {}).get('water', 0):.0f}%",
        f"- 🏃 {localize(locale, '运动达标率', 'Exercise goal rate')}: {monthly_data.get('macro_scores', {}).get('exercise', 0):.0f}%",
        f"- 💊 {localize(locale, '用药覆盖率', 'Medication coverage')}: {monthly_data.get('macro_scores', {}).get('medication', 0):.0f}%",
        f"- 🧪 {localize(locale, '监测覆盖率', 'Monitoring coverage')}: {monthly_data.get('macro_scores', {}).get('monitoring', 0):.0f}%",
        f"- 🩺 {localize(locale, '症状天数', 'Symptom days')}: {monthly_data.get('symptom_days', 0)}",
        f"- 💊 {localize(locale, '用药天数', 'Medication days')}: {monthly_data.get('medication_days', 0)}",
        f"- 🧪 {localize(locale, '监测天数', 'Monitoring days')}: {monthly_data.get('monitoring_days', 0)}",
    ]
    specialty_lines = [f"- 📈 {chart.get('title')}: {chart.get('summary')}" for chart in monthly_data.get("specialty_charts", [])[:4]]
    followup_lines = [f"- 🗓️ {item}" for item in monthly_data.get("follow_up_reminders", [])]
    recommendation_lines = []
    recommendation_groups = monthly_data.get("hospital_recommendation_groups", [])
    for group in recommendation_groups:
        recommendation_lines.extend(
            [
                f"- 🏥 {group.get('hospital')}（{group.get('hospital_stars', '★★★')}）",
                localize(locale, f"  🧱 医院等级：{group.get('hospital_grade', '-')}", f"  🧱 Hospital grade: {group.get('hospital_grade', '-')}"),
                localize(locale, f"  🏛 医院优势：{group.get('hospital_strength', '-')}", f"  🏛 Hospital strengths: {group.get('hospital_strength', '-')}"),
            ]
        )
        if group.get("hospital_address"):
            recommendation_lines.append(localize(locale, f"  📍 医院地址：{group.get('hospital_address')}", f"  📍 Address: {group.get('hospital_address')}"))
        if group.get("booking_method"):
            recommendation_lines.append(localize(locale, f"  🎫 挂号方式：{group.get('booking_method')}", f"  🎫 Booking: {group.get('booking_method')}"))
        recommendation_lines.append("")
        for doctor in group.get("doctors", []):
            recommendation_lines.extend(
                [
                    localize(locale, f"  ■ 推荐科室：{doctor.get('department')}", f"  ■ Recommended department: {doctor.get('department')}"),
                    localize(locale, f"  ■ 推荐医生：{doctor.get('doctor_display')}", f"  ■ Recommended doctor: {doctor.get('doctor_display')}"),
                    localize(locale, f"  ■ 医生擅长：{doctor.get('doctor_specialty')}", f"  ■ Doctor specialty: {doctor.get('doctor_specialty')}"),
                    localize(locale, f"  ■ 挂号费：{doctor.get('registration_fee')}", f"  ■ Registration fee: {doctor.get('registration_fee')}"),
                    localize(locale, f"  ■ 坐诊时间：{doctor.get('clinic_schedule')}", f"  ■ Clinic schedule: {doctor.get('clinic_schedule')}"),
                    localize(locale, f"  ■ 推荐理由：{doctor.get('reason')}", f"  ■ Recommendation reason: {doctor.get('reason')}"),
                    "",
                ]
            )

    report_heading = f"{localize(locale, '健康月报', 'Monthly Health Report')} ({monthly_data.get('month_key')})"
    lines = [
        f"## {section(report_heading, '🗓️')}",
        "",
        f"### {section(localize(locale, '个人信息', 'Profile'), '👤')}",
        *profile_lines,
        "",
        f"### {section(localize(locale, '月度概览', 'Monthly Overview'), '🌐')}",
        *summary_lines,
        "",
        f"### {section(localize(locale, '本月亮点', 'Highlights'), '✨')}",
        *[f"- 🌟 {item}" for item in monthly_data.get("macro_highlights", [])],
        "",
        f"### {section(deep_dive_title, '📈')}",
        *(specialty_lines or [f"- 📉 {localize(locale, '当前专项图表数据仍不足，后续可通过血压/血糖/体脂/生化模块自动补齐。', 'Specialty chart data are still limited this month. Blood pressure, glucose, body-fat, and lab modules will automatically enrich future reports.')}"]),
        "",
        f"### {section(ai_review_title, '🧠')}",
        ai_review.strip(),
        f"_{generation_source_label(locale, review_source)}_",
        "",
        f"### {section(follow_up_title, '📌')}",
        *(followup_lines or [f"- 📭 {localize(locale, '当前没有额外复查提醒。', 'There are no extra follow-up reminders for now.')}"]),
    ]
    if not lifestyle_mode:
        lines.extend(
            [
                "",
                f"### {section(hospital_title, '🏥')}",
                *(recommendation_lines or [f"- 📍 {localize(locale, '请先在 user_config.json 中补充常居地后再生成更具体的医院推荐。', 'Add residence details to user_config.json to unlock more specific hospital recommendations.')}"]),
                f"_{generation_source_label(locale, recommendation_source)}_",
            ]
        )
    render_notice = str(monthly_data.get("render_notice") or "").strip()
    if render_notice:
        lines.extend(["", f"### {section(localize(locale, '渲染说明', 'Rendering Notice'), 'ℹ️')}", render_notice])
    if resolve_locale(locale=locale) == "ja-JP":
        lines = [sanitize_locale_line(locale, line) for line in lines]
    return "\n".join(lines).strip()


def publish_monthly_pdf(local_pdf_path: str) -> str:
    web_dir = os.environ.get("REPORT_WEB_DIR", "")
    base_url = os.environ.get("REPORT_BASE_URL", "").rstrip("/")
    if web_dir and os.path.exists(web_dir) and base_url:
        filename = os.path.basename(local_pdf_path)
        web_pdf_path = os.path.join(web_dir, filename)
        shutil.copy2(local_pdf_path, web_pdf_path)
        return f"{base_url}/{filename}"
    return local_pdf_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 monthly_report_pro.py <YYYY-MM-DD>")
        sys.exit(1)

    target_date = sys.argv[1]
    base_config = load_user_config()
    month_dates = get_month_dates(target_date)
    month_files = [os.path.join(MEMORY_DIR, f"{date_str}.md") for date_str in month_dates]
    requested_locale = resolve_report_locale(base_config, month_files)
    fallback_context = prepare_font_compatible_memory(requested_locale=requested_locale, source_dir=MEMORY_DIR)
    temp_memory_dir = fallback_context.get("temp_dir")

    try:
        locale = fallback_context.get("locale") or requested_locale
        config = force_config_locale(base_config, locale)
        profile = config.get("user_profile", {})
        memory_dir = fallback_context.get("memory_dir") or MEMORY_DIR
        render_notice = str(fallback_context.get("render_notice") or "").strip()

        conditions = get_profile_conditions(profile)
        profile_payload = dict(profile)
        profile_payload["condition"] = get_primary_condition(profile)
        profile_payload["conditions"] = conditions
        profile_payload["condition_display"] = get_conditions_display_name(locale, conditions)

        monthly_data = aggregate_monthly_data(month_dates, config, locale=locale, memory_dir=memory_dir)
        monthly_data["macro_highlights"] = build_monthly_highlights(monthly_data, profile_payload, locale)
        monthly_data["specialty_charts"] = build_specialty_charts(monthly_data, config, locale)
        monthly_data["follow_up_reminders"] = build_follow_up_reminders(monthly_data, profile_payload, locale)
        monthly_data["hospital_recommendations"], recommendation_source = build_hospital_recommendations(monthly_data, profile_payload, locale, config=config)
        monthly_data["hospital_recommendation_groups"] = group_hospital_recommendations(
            monthly_data["hospital_recommendations"],
            monthly_data.get("primary_condition", "balanced"),
            locale,
        )
        monthly_data["custom_monitoring_summary"] = build_custom_monitoring_summary(monthly_data, locale)
        if render_notice:
            monthly_data["render_notice"] = render_notice

        ai_review, review_source = get_ai_monthly_review(monthly_data, profile_payload, config, locale)

        locale_tag = resolve_locale(locale=locale).replace("-", "_")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        pdf_filename = f"monthly_report_{locale_tag}_{timestamp}.pdf"
        local_output_path = os.path.join(REPORTS_DIR, pdf_filename)

        generate_monthly_pdf_report(
            monthly_data,
            profile_payload,
            ai_review,
            local_output_path,
            locale=locale,
            review_source=review_source,
            recommendation_source=recommendation_source,
        )
        pdf_url = publish_monthly_pdf(local_output_path)
        text_report = generate_monthly_text_report(monthly_data, profile_payload, ai_review, locale, review_source, recommendation_source)
        delivery_message = build_delivery_message(
            locale=locale,
            body=text_report,
            pdf_url=pdf_url,
            report_kind="monthly",
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            start_date=monthly_data["start_date"],
            end_date=monthly_data["end_date"],
        )

        print("=== TEXT_REPORT_START ===")
        print(text_report)
        print("=== TEXT_REPORT_END ===")
        print("=== PDF_URL ===")
        print(pdf_url)
        print("=== DELIVERY_MESSAGE_START ===")
        print(delivery_message)
        print("=== DELIVERY_MESSAGE_END ===")
    finally:
        if temp_memory_dir:
            temp_memory_dir.cleanup()
