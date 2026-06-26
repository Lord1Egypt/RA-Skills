#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Weekly report controller for Health-Mate."""

import os
import re
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path


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
    clean_search_excerpt as shared_clean_search_excerpt,
    force_config_locale,
    find_custom_section_items,
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
from i18n import (
    build_delivery_message,
    build_weekly_ai_prompt,
    build_weekly_ai_system_prompt,
    format_weight,
    format_weight_delta,
    inline_localize,
    localize_free_text,
    resolve_locale,
    t,
)
from weekly_pdf_generator import generate_weekly_pdf_report

validate_environment()

MEMORY_DIR = os.environ.get("MEMORY_DIR", "")
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


def localize(locale, zh_text, en_text):
    return inline_localize(locale, zh_text, en_text)


def sanitize_locale_line(locale, text):
    return localize_free_text(locale, text) if resolve_locale(locale=locale) == "ja-JP" else text


def normalize_name(value):
    text = re.sub(r"[*_`]+", "", str(value or "")).strip().lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", text)
    return text


def should_ignore_custom_section(title):
    normalized = normalize_name(title)
    return any(normalize_name(hint) in normalized for hint in CUSTOM_SECTION_IGNORE_HINTS if hint)


def section_matches(title, aliases):
    normalized_title = normalize_name(title)
    return any(normalize_name(alias) in normalized_title for alias in aliases if alias)


def read_text(file_path):
    try:
        return Path(file_path).read_text(encoding="utf-8")
    except OSError:
        return ""


def extract_structured_metrics(file_path, daily_data):
    content = read_text(file_path)
    custom_sections = daily_data.get("custom_sections", {})
    metrics = {
        "body_fat_percent": None,
        "blood_pressure": [],
    }

    body_fat_match = re.search(r"(?:体脂率|body\s*fat(?:\s*percentage)?)\s*[:：]\s*(\d+(?:\.\d+)?)\s*%", content, re.IGNORECASE)
    if body_fat_match:
        metrics["body_fat_percent"] = float(body_fat_match.group(1))

    bp_aliases = ["血压", "blood pressure", "bp"]
    bodyfat_aliases = ["体脂", "body fat", "body composition", "身体成分"]
    for header, items in custom_sections.items():
        if should_ignore_custom_section(header):
            continue
        if section_matches(header, bp_aliases):
            for item in items:
                bp_match = re.search(r"(\d{2,3})\s*/\s*(\d{2,3})\s*(?:mmhg)?", str(item), re.IGNORECASE)
                if not bp_match:
                    continue
                metrics["blood_pressure"].append(
                    {
                        "raw": item,
                        "systolic": int(bp_match.group(1)),
                        "diastolic": int(bp_match.group(2)),
                    }
                )
        elif section_matches(header, bodyfat_aliases):
            for item in items:
                bodyfat_match = re.search(r"(?:体脂率|body\s*fat(?:\s*percentage)?)\s*[:：]?\s*(\d+(?:\.\d+)?)\s*%", str(item), re.IGNORECASE)
                if bodyfat_match:
                    metrics["body_fat_percent"] = float(bodyfat_match.group(1))
    return metrics


def safe_average(values):
    cleaned = [value for value in values if value is not None]
    return sum(cleaned) / len(cleaned) if cleaned else 0


def dedupe_preserve_order(items):
    seen = set()
    output = []
    for item in items:
        normalized = str(item or "").strip()
        if not normalized or normalized in seen:
            continue
        output.append(normalized)
        seen.add(normalized)
    return output


def clean_search_excerpt(text, locale, max_length=160):
    return shared_clean_search_excerpt(text, locale, max_length=max_length)


def get_week_dates(target_date_str):
    target_date = datetime.strptime(target_date_str, "%Y-%m-%d")
    monday = target_date - timedelta(days=target_date.weekday())
    return [(monday + timedelta(days=offset)).strftime("%Y-%m-%d") for offset in range(7)]


def summarize_day(record, locale):
    if not record:
        return "記録なし" if resolve_locale(locale=locale) == "ja-JP" else localize(locale, "暂无", "N/A")
    if resolve_locale(locale=locale) == "ja-JP":
        return f"{record['date']}（{record['score']:.0f}/100、飲水 {record['water_total']}ml、歩数 {record['steps']}）"
    return localize(
        locale,
        f"{record['date']}（{record['score']:.0f} 分，饮水 {record['water_total']}ml，步数 {record['steps']}）",
        f"{record['date']} ({record['score']:.0f}/100, water {record['water_total']}ml, steps {record['steps']})",
    )


def build_custom_section_rollup(config):
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
        }
    return rollup


def merge_dynamic_custom_sections(rollup, custom_sections):
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
            }


def build_weekly_observations(weekly_data, profile, locale):
    strengths = []
    gaps = []
    next_focus = []
    gap_topics = []
    resolved_locale = resolve_locale(locale=locale)

    def tr(zh_text, en_text, ja_text):
        return inline_localize(locale, zh_text, en_text, ja_text)

    step_target = int(profile.get("step_target", 8000) or 8000)
    water_target = int(profile.get("water_target_ml", 2000) or 2000)
    primary_condition = weekly_data.get("primary_condition", "balanced")
    observed_days = weekly_data.get("observed_days", 0)
    review_days = max(1, observed_days)

    if weekly_data.get("avg_total_score", 0) >= 80:
        strengths.append(tr(
            f"周均综合评分 {weekly_data['avg_total_score']:.1f} 分，整体执行稳定。",
            f"Average overall score reached {weekly_data['avg_total_score']:.1f}, showing stable execution.",
            f"週平均総合評価は {weekly_data['avg_total_score']:.1f} 点で、全体の実行状況は安定していました。",
        ))
    elif observed_days:
        gaps.append(tr(
            f"周均综合评分 {weekly_data['avg_total_score']:.1f} 分，仍有提升空间。",
            f"Average overall score was {weekly_data['avg_total_score']:.1f}, leaving room to improve.",
            f"週平均総合評価は {weekly_data['avg_total_score']:.1f} 点で、まだ改善の余地があります。",
        ))

    if weekly_data.get("water_goal_days", 0) >= 5:
        strengths.append(tr(
            f"饮水达标 {weekly_data['water_goal_days']}/7 天，基础补水比较稳定。",
            f"Hydration target was met on {weekly_data['water_goal_days']}/7 days, which is a steady baseline habit.",
            f"飲水目標は {weekly_data['water_goal_days']}/7 日で達成できており、基礎的な補水習慣は安定しています。",
        ))
    else:
        gaps.append(tr(
            f"饮水仅达标 {weekly_data['water_goal_days']}/7 天，距离每日 {water_target}ml 还有差距。",
            f"Hydration target was met on only {weekly_data['water_goal_days']}/7 days, still short of the daily {water_target}ml goal.",
            f"飲水目標の達成は {weekly_data['water_goal_days']}/7 日にとどまり、1日 {water_target}ml の目標にはまだ差があります。",
        ))
        next_focus.append(tr(
            "把饮水拆成 4-5 次完成，优先保证工作日上午和下午各一次补水。",
            "Split hydration into 4-5 checkpoints and make sure at least one refill happens in both the morning and afternoon work blocks.",
            "飲水を 4〜5 回に分け、午前と午後にそれぞれ 1 回ずつ補水する流れを固定してください。",
        ))
        gap_topics.append("hydration")

    if weekly_data.get("step_goal_days", 0) >= 4:
        strengths.append(tr(
            f"步数目标达标 {weekly_data['step_goal_days']}/7 天，活动量保持不错。",
            f"Step target was achieved on {weekly_data['step_goal_days']}/7 days, which kept activity volume in a good place.",
            f"歩数目標は {weekly_data['step_goal_days']}/7 日で達成できており、活動量は良好でした。",
        ))
    else:
        gaps.append(tr(
            f"步数目标仅达标 {weekly_data['step_goal_days']}/7 天，离每日 {step_target} 步还有距离。",
            f"Step target was achieved on only {weekly_data['step_goal_days']}/7 days, still below the daily {step_target}-step goal.",
            f"歩数目標の達成は {weekly_data['step_goal_days']}/7 日で、1日 {step_target} 歩にはまだ届いていません。",
        ))
        next_focus.append(tr(
            "固定 3 次 15-20 分钟餐后步行或晚间快走，优先补足低活动日。",
            "Lock in three 15-20 minute post-meal or evening walks next week to recover the lower-activity days.",
            "食後や夕方に 15〜20 分のウォーキングを 3 回固定し、活動量の少ない日を埋めてください。",
        ))
        gap_topics.append("activity")

    if weekly_data.get("avg_diet_score", 0) >= 80:
        strengths.append(tr(
            f"饮食周均得分 {weekly_data['avg_diet_score']:.1f} 分，饮食结构整体较稳。",
            f"Average diet score was {weekly_data['avg_diet_score']:.1f}, suggesting a generally stable meal structure.",
            f"食事の週平均評価は {weekly_data['avg_diet_score']:.1f} 点で、食事構成は概ね安定していました。",
        ))
    elif weekly_data.get("recorded_meal_days", 0) > 0:
        gaps.append(tr(
            f"饮食周均得分 {weekly_data['avg_diet_score']:.1f} 分，仍需优化脂肪、纤维或餐次结构。",
            f"Average diet score was {weekly_data['avg_diet_score']:.1f}; fat, fiber, or meal structure still need work.",
            f"食事の週平均評価は {weekly_data['avg_diet_score']:.1f} 点で、脂質・食物繊維・食事リズムの調整がまだ必要です。",
        ))
        next_focus.append(tr(
            "优先把早餐和晚餐结构固定下来，并针对本周短板补纤维或控制脂肪。",
            "Stabilize breakfast and dinner first, then correct this week's main gaps in fiber or fat intake.",
            "まず朝食と夕食の型を安定させ、今週の弱点に応じて食物繊維の補強や脂質調整を進めてください。",
        ))
        gap_topics.append("diet")
    elif observed_days:
        gaps.append(tr(
            "本周饮食记录不足，导致饮食趋势判断有限。",
            "Meal logging was too sparse this week, so diet trend analysis is limited.",
            "今週は食事記録が少なく、食事トレンドの判断材料が不足しています。",
        ))
        next_focus.append(tr(
            "至少连续记录 5 天三餐或主要两餐，方便生成更可靠的趋势判断。",
            "Log at least 5 days of meals next week so the trend analysis becomes more reliable.",
            "来週は少なくとも 5 日分、3 食または主要 2 食を連続記録し、トレンド判断の精度を上げてください。",
        ))
        gap_topics.append("logging")

    weight_change = weekly_data.get("weight_change", 0)
    if primary_condition == "fat_loss":
        if weight_change <= -0.2:
            strengths.append(tr(
                f"体重较周初下降 {abs(weight_change):.2f}kg，方向与减脂目标一致。",
                f"Weight moved down by {abs(weight_change):.2f}kg from the start of the week, which aligns with the fat-loss goal.",
                f"体重は週初から {abs(weight_change):.2f}kg 減少し、減脂目標と同じ方向に進んでいます。",
            ))
        elif weight_change > 0.5:
            gaps.append(tr(
                f"体重较周初上升 {weight_change:.2f}kg，需要复查晚餐份量和活动量。",
                f"Weight rose by {weight_change:.2f}kg from the start of the week, so dinner portions and activity deserve a closer look.",
                f"体重は週初より {weight_change:.2f}kg 増えており、夕食量と活動量の見直しが必要です。",
            ))
            next_focus.append(tr(
                "晚餐主食和零食份量先减一点，同时补足 2-3 次餐后活动。",
                "Trim dinner carbs and snacks slightly, then add 2-3 extra post-meal activity blocks.",
                "夕食の主食と間食を少し抑え、食後の活動を 2〜3 回追加してください。",
            ))
            gap_topics.append("weight")
    else:
        if abs(weight_change) <= 0.5 and weekly_data.get("valid_weight_days", 0) >= 2:
            strengths.append(tr(
                f"体重波动控制在 {abs(weight_change):.2f}kg 内，整体较平稳。",
                f"Weight fluctuation stayed within {abs(weight_change):.2f}kg, which is relatively stable.",
                f"体重変動は {abs(weight_change):.2f}kg 以内に収まり、全体として安定していました。",
            ))
        elif weekly_data.get("valid_weight_days", 0) >= 2:
            gaps.append(tr(
                f"体重波动达到 {abs(weight_change):.2f}kg，建议结合饮食与活动进一步排查。",
                f"Weight fluctuation reached {abs(weight_change):.2f}kg, so diet and activity patterns should be reviewed together.",
                f"体重変動は {abs(weight_change):.2f}kg に達しており、食事と活動をあわせて見直す必要があります。",
            ))
            gap_topics.append("weight")

    if weekly_data.get("symptom_days", 0) == 0:
        strengths.append(tr(
            "本周未记录明显不适症状，整体状态较平稳。",
            "No clear symptom days were logged this week, suggesting a steady overall state.",
            "今週は目立った不調症状の記録がなく、全体状態は安定していました。",
        ))
    else:
        gaps.append(tr(
            f"本周有 {weekly_data['symptom_days']} 天记录症状，共 {weekly_data['symptom_events']} 次，需要关注诱因。",
            f"Symptoms were recorded on {weekly_data['symptom_days']} days ({weekly_data['symptom_events']} events), so triggers deserve attention.",
            f"今週は {weekly_data['symptom_days']} 日で症状が記録され、合計 {weekly_data['symptom_events']} 回ありました。誘因の確認が必要です。",
        ))
        next_focus.append(tr(
            "把症状出现前的饮食、作息和活动一起记录，便于下周定位诱因。",
            "Log meals, sleep, and activity around symptom episodes next week so likely triggers are easier to identify.",
            "症状の前後にある食事、睡眠、活動もあわせて記録し、来週の誘因特定につなげてください。",
        ))
        gap_topics.append("symptoms")

    if weekly_data.get("medication_enabled"):
        if weekly_data.get("medication_days", 0) >= max(1, min(review_days, 5)):
            strengths.append(tr(
                f"用药记录覆盖 {weekly_data['medication_days']} 天，依从性追踪比较完整。",
                f"Medication was logged on {weekly_data['medication_days']} days, giving decent adherence visibility.",
                f"服薬記録は {weekly_data['medication_days']} 日分あり、遵守状況の確認材料として十分です。",
            ))
        else:
            gaps.append(tr(
                f"用药模块已启用，但本周仅记录 {weekly_data['medication_days']} 天。",
                f"Medication tracking is enabled, but only {weekly_data['medication_days']} days were logged this week.",
                f"服薬モジュールは有効ですが、今週の記録は {weekly_data['medication_days']} 日分にとどまりました。",
            ))
            next_focus.append(tr(
                "如果有服药安排，请同步记录时间、药名与剂量，便于周报一起复盘。",
                "If medication is part of the routine, log time, medicine name, and dosage so it can be reviewed in the weekly report.",
                "服薬がある日は、時間・薬剤名・用量もあわせて記録し、週報で振り返れるようにしてください。",
            ))
            gap_topics.append("medication")

    custom_stats = weekly_data.get("custom_section_stats", [])
    for section in custom_stats[:3]:
        if section.get("days_recorded", 0) > 0:
            if resolved_locale == "ja-JP":
                strengths.append(f"{section['title']} は今週 {section['days_recorded']} 日記録され、他指標とあわせて判断できます。")
            else:
                strengths.append(localize(locale, f"{section['title']} 本周记录 {section['days_recorded']} 天，可用于联合判断。", f"{section['title']} was recorded on {section['days_recorded']} days and can now be used in combined review."))
        elif section.get("configured"):
            if resolved_locale == "ja-JP":
                gaps.append(f"{section['title']} は有効ですが、今週の記録がありませんでした。")
                next_focus.append(f"{section['title']} が重要な監視項目であれば、来週は少なくとも 1〜2 回記録してください。")
            else:
                gaps.append(localize(locale, f"已启用 {section['title']}，但本周暂无记录。", f"{section['title']} is enabled, but no entries were recorded this week."))
                next_focus.append(localize(locale, f"若 {section['title']} 是重点监测项，请至少补齐 1-2 次记录。", f"If {section['title']} matters for ongoing management, add at least 1-2 entries next week."))
            gap_topics.append(section["title"])

    strengths = dedupe_preserve_order(strengths)[:5]
    gaps = dedupe_preserve_order(gaps)[:5]
    next_focus = dedupe_preserve_order(next_focus)[:5]
    gap_topics = dedupe_preserve_order(gap_topics)[:4]

    if not strengths and observed_days:
        strengths.append(tr(
            "本周至少完成了基础记录，为后续分析保留了数据。",
            "Basic tracking was completed this week, which still preserves usable data for later analysis.",
            "今週は最低限の基礎記録が残っており、次回分析につながる土台は確保できています。",
        ))
    if not gaps and observed_days:
        gaps.append(tr(
            "目前没有特别突出的短板，重点是继续保持稳定执行。",
            "No single major gap stands out right now; the main task is to keep execution steady.",
            "現時点で大きく目立つ弱点はなく、次週も安定して続けることが最優先です。",
        ))
    if not next_focus:
        next_focus.append(tr(
            "延续当前节奏，围绕饮食、饮水和活动保持稳定。",
            "Keep the current rhythm and stay consistent with meals, hydration, and activity.",
            "現在のリズムを維持し、食事・飲水・活動の安定を優先してください。",
        ))

    return strengths, gaps, next_focus, gap_topics


def aggregate_weekly_data(week_dates, config, locale=None, memory_dir=None):
    """Collect one week of metrics from the daily markdown files."""
    locale = resolve_locale(config, locale=locale)
    memory_dir = memory_dir or MEMORY_DIR
    profile = config.get("user_profile", {})
    conditions = get_profile_conditions(profile)
    primary_condition = get_primary_condition(profile)
    condition_text = get_conditions_display_name(locale, conditions)
    standards = get_condition_standards(config, conditions)
    custom_rollup = build_custom_section_rollup(config)
    medication_enabled = any(
        module.get("id") == "medication" and module.get("enabled", True)
        for module in get_scoring_modules(config)
    )

    weekly_data = {
        "start_date": week_dates[0],
        "end_date": week_dates[-1],
        "dates": week_dates,
        "conditions": conditions,
        "condition_text": condition_text,
        "primary_condition": primary_condition,
        "diet_principle": build_multi_condition_tip(locale, conditions, standards),
        "weights": [],
        "water_intakes": [],
        "steps": [],
        "calories": [],
        "protein": [],
        "fat": [],
        "carb": [],
        "fiber": [],
        "daily_records": [],
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
        "population_branch": get_population_branch(config=config, user_profile=profile, primary_condition=primary_condition),
    }

    first_weight = None
    last_weight = None
    water_target = int(profile.get("water_target_ml", 2000) or 2000)
    step_target = int(profile.get("step_target", 8000) or 8000)

    for date_str in week_dates:
        file_path = os.path.join(memory_dir, f"{date_str}.md")
        daily_data = parse_memory_file(file_path)
        daily_data["date"] = daily_data.get("date") or date_str
        filtered_custom_sections = {
            header: items
            for header, items in (daily_data.get("custom_sections", {}) or {}).items()
            if not should_ignore_custom_section(header)
        }
        daily_data["custom_sections"] = filtered_custom_sections

        merge_dynamic_custom_sections(custom_rollup, filtered_custom_sections)
        for stats in custom_rollup.values():
            items = find_custom_section_items(filtered_custom_sections, stats.get("section_title", stats.get("title", "")))
            if items:
                stats["days_recorded"] += 1
                stats["items"] += len(items)

        structured = extract_structured_metrics(file_path, daily_data)
        score_report = build_score_report(daily_data, config)
        water_total = int(daily_data.get("water_total", 0) or 0)
        steps = int(daily_data.get("steps", 0) or 0)
        exercise_calories = sum(float(item.get("calories", 0) or 0) for item in daily_data.get("exercise_records", []))
        symptom_keywords = daily_data.get("symptom_keywords", [])
        medication_records = daily_data.get("medication_records", [])
        weight_value = daily_data.get("weight_morning")
        body_fat_percent = structured.get("body_fat_percent")
        bp_readings = structured.get("blood_pressure", [])
        bp_peak_systolic = max((item.get("systolic", 0) for item in bp_readings), default=None)
        monitoring_present = any([weight_value is not None, body_fat_percent is not None, bool(filtered_custom_sections), bool(bp_readings)])
        has_data = any([
            bool(daily_data.get("meals")),
            bool(daily_data.get("water_records")),
            bool(daily_data.get("exercise_records")),
            bool(daily_data.get("custom_sections")),
            bool(medication_records),
            bool(symptom_keywords),
            water_total > 0,
            steps > 0,
            weight_value is not None,
            monitoring_present,
        ])

        if has_data:
            weekly_data["observed_days"] += 1

        if daily_data.get("meals"):
            weekly_data["recorded_meal_days"] += 1
        if daily_data.get("exercise_records") or steps > 0:
            weekly_data["exercise_days"] += 1
        if symptom_keywords:
            weekly_data["symptom_days"] += 1
            weekly_data["symptom_events"] += len(symptom_keywords)
        if medication_records:
            weekly_data["medication_days"] += 1
        if monitoring_present:
            weekly_data["monitoring_days"] += 1
        if water_total >= water_target:
            weekly_data["water_goal_days"] += 1
        if steps >= step_target:
            weekly_data["step_goal_days"] += 1

        diet_score = score_report.get("module_map", {}).get("diet", {}).get("raw", 0)
        if diet_score >= 80:
            weekly_data["diet_goal_days"] += 1

        weekly_data["weights"].append(weight_value)
        if weight_value is not None:
            weekly_data["valid_weight_days"] += 1
            if first_weight is None:
                first_weight = weight_value
            last_weight = weight_value

        weekly_data["water_intakes"].append(water_total)
        weekly_data["steps"].append(steps)
        weekly_data["calories"].append(daily_data.get("total_calories", 0))
        weekly_data["protein"].append(daily_data.get("total_protein", 0))
        weekly_data["fat"].append(daily_data.get("total_fat", 0))
        weekly_data["carb"].append(daily_data.get("total_carb", 0))
        weekly_data["fiber"].append(daily_data.get("total_fiber", 0))
        weekly_data["daily_records"].append({
            "date": date_str,
            "has_data": has_data,
            "score": score_report.get("total", 0),
            "diet_score": diet_score,
            "water_total": water_total,
            "steps": steps,
            "calories": daily_data.get("total_calories", 0),
            "exercise_calories": exercise_calories,
            "exercise_count": len(daily_data.get("exercise_records", [])),
            "fat": daily_data.get("total_fat", 0),
            "protein": daily_data.get("total_protein", 0),
            "carb": daily_data.get("total_carb", 0),
            "weight": weight_value,
            "body_fat_percent": body_fat_percent,
            "symptom_count": len(symptom_keywords),
            "medication_count": len(medication_records),
            "monitoring_count": sum(len(items) for items in filtered_custom_sections.values()) + (1 if weight_value is not None else 0) + len(bp_readings),
            "bp_peak_systolic": bp_peak_systolic,
        })

    divisor = max(1, weekly_data["observed_days"])
    valid_weights = [value for value in weekly_data["weights"] if value is not None]
    scored_days = [record["score"] for record in weekly_data["daily_records"] if record.get("has_data")]
    diet_days = [record["diet_score"] for record in weekly_data["daily_records"] if record.get("diet_score", 0) > 0]

    weekly_data["avg_weight"] = safe_average(valid_weights)
    weekly_data["latest_weight"] = last_weight
    weekly_data["weight_change"] = (last_weight - first_weight) if (last_weight is not None and first_weight is not None) else 0
    weekly_data["avg_calories"] = sum(weekly_data["calories"]) / divisor
    weekly_data["avg_water"] = sum(weekly_data["water_intakes"]) / divisor
    weekly_data["avg_steps"] = sum(weekly_data["steps"]) / divisor
    weekly_data["avg_protein"] = sum(weekly_data["protein"]) / divisor
    weekly_data["avg_fat"] = sum(weekly_data["fat"]) / divisor
    weekly_data["avg_carb"] = sum(weekly_data["carb"]) / divisor
    weekly_data["avg_fiber"] = sum(weekly_data["fiber"]) / divisor
    weekly_data["avg_total_score"] = safe_average(scored_days)
    weekly_data["avg_diet_score"] = safe_average(diet_days)
    medication_expected = medication_enabled or weekly_data["medication_days"] > 0
    weekly_data["macro_scores"] = {
        "diet": round(weekly_data["avg_diet_score"], 1),
        "water": round(weekly_data["water_goal_days"] / divisor * 100, 1),
        "exercise": round(((weekly_data["step_goal_days"] / divisor) * 0.65 + (weekly_data["exercise_days"] / divisor) * 0.35) * 100, 1),
        "medication": 100.0 if not medication_expected else round(weekly_data["medication_days"] / divisor * 100, 1),
        "monitoring": round(weekly_data["monitoring_days"] / divisor * 100, 1),
    }
    weekly_data["custom_section_stats"] = sorted(
        custom_rollup.values(),
        key=lambda item: (item.get("days_recorded", 0), item.get("items", 0), item.get("title", "")),
        reverse=True,
    )

    ranked_days = [record for record in weekly_data["daily_records"] if record.get("has_data")]
    weekly_data["best_day"] = max(ranked_days, key=lambda item: item.get("score", 0), default=None)
    weekly_data["focus_day"] = min(ranked_days, key=lambda item: item.get("score", 0), default=None)

    strengths, gaps, next_focus, gap_topics = build_weekly_observations(weekly_data, profile, locale)
    weekly_data["strengths"] = strengths
    weekly_data["gaps"] = gaps
    weekly_data["next_focus"] = next_focus
    weekly_data["gap_topics"] = gap_topics
    return weekly_data


def build_weekly_fallback_insights(weekly_data, profile, locale):
    condition_text = weekly_data.get("condition_text", localize(locale, "综合健康管理", "general health management"))
    strengths = weekly_data.get("strengths", [])
    gaps = weekly_data.get("gaps", [])
    focus = weekly_data.get("next_focus", [])
    best_day_text = summarize_day(weekly_data.get("best_day"), locale)
    focus_day_text = summarize_day(weekly_data.get("focus_day"), locale)
    is_ja = resolve_locale(locale=locale) == "ja-JP"

    if weekly_data.get("observed_days", 0) == 0:
        review = (
            "今週は分析に使える記録がほとんどなく、週報の骨組みは出力できていますが、結論の信頼度は低めです。まずは毎日の食事、飲水、歩数、症状を記録してください。"
            if is_ja
            else localize(
                locale,
                "本周几乎没有可用于分析的记录，周报已保留基础结构，但结论可信度较低。建议先把每日饮食、饮水、步数和症状记录补齐。",
                "There were almost no usable records this week. The weekly report was still generated, but the conclusions are low-confidence. Please fill in daily meals, hydration, steps, and symptoms first.",
            )
        )
        plan = "\n".join([
            f"- {('5〜7 日連続で基礎データを記録してから、次回の週報を生成してください。' if is_ja else localize(locale, '连续记录 5-7 天基础数据，再生成下一次周报。', 'Log 5-7 consecutive days of core data before generating the next weekly report.'))}",
            f"- {('最低でも体重、飲水、歩数、主要な食事を記録してください。' if is_ja else localize(locale, '至少记录体重、饮水、步数和主要餐次。', 'At minimum, log weight, hydration, steps, and main meals.'))}",
            f"- {('症状や服薬がある場合は、それもあわせて残してください。' if is_ja else localize(locale, '如有症状或用药，也请同步记录。', 'If symptoms or medication are involved, record them as well.'))}",
        ])
        return review, plan, "fallback"

    if is_ja:
        review_lines = [
            f"今週の管理テーマは {condition_text} でした。良かった点は次のとおりです。",
            *[f"- {item}" for item in strengths[:3]],
            "引き続き注意したい点はこちらです。",
            *[f"- {item}" for item in gaps[:3]],
            f"今週もっとも安定していた日は {best_day_text}、重点的に振り返りたい日は {focus_day_text} です。",
        ]
    else:
        review_lines = [
            localize(locale, f"本周管理重点为 {condition_text}。本周做得较好的地方：", f"This week's management focus was {condition_text}. The stronger areas were:"),
            *[f"- {item}" for item in strengths[:3]],
            localize(locale, "本周仍需重点关注：", "The main gaps that still need attention are:"),
            *[f"- {item}" for item in gaps[:3]],
            localize(locale, f"最佳状态日：{best_day_text}。需要重点复盘的一天：{focus_day_text}。", f"Best day: {best_day_text}. Day that needs the most review: {focus_day_text}."),
        ]

    plan_lines = [f"- {item}" for item in focus[:4]]
    source = "fallback"

    if has_tavily_api_key(config) and weekly_data.get("gap_topics"):
        if is_ja:
            query = f"{condition_text} 患者教育 週間セルフマネジメント {' '.join(weekly_data['gap_topics'][:3])} 提案"
        else:
            query = localize(
                locale,
                f"{condition_text} 患者教育 一周健康管理 {' '.join(weekly_data['gap_topics'][:3])} 建议",
                f"{condition_text} patient education weekly self-management tips {' '.join(weekly_data['gap_topics'][:3])}",
            )
        search_results = tavily_search(query, max_results=2, config=config)
        snippets = []
        for result in search_results:
            content = clean_search_excerpt(str(result.get("content", "") or ""), locale, max_length=160)
            if is_ja and content and not re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", content):
                continue
            if content:
                snippets.append(content)
        if snippets:
            review_lines.append("外部参考：" if is_ja else localize(locale, "检索补充观点：", "Retrieved external note:"))
            review_lines.extend([f"- {snippet}" for snippet in snippets[:1]])
            plan_lines.append(f"- 外部提案として参考になる点: {snippets[0]}" if is_ja else localize(locale, f"- 可参考外部建议：{snippets[0]}", f"- External idea to consider: {snippets[0]}"))
            source = "fallback_tavily"

    review = "\n".join(review_lines).strip()
    plan = "\n".join(plan_lines).strip()
    return review, plan, source


def parse_weekly_ai_output(output):
    clean_output = str(output or "").strip()
    if not clean_output:
        return "", ""
    review_match = re.search(r"---review---\s*(.*?)\s*---plan---", clean_output, re.DOTALL | re.IGNORECASE)
    plan_match = re.search(r"---plan---\s*(.*)", clean_output, re.DOTALL | re.IGNORECASE)
    if review_match and plan_match:
        return review_match.group(1).strip(), plan_match.group(1).strip()
    parts = clean_output.split("---plan---")
    if len(parts) == 2:
        return parts[0].replace("---review---", "").strip(), parts[1].strip()
    return "", ""


def get_ai_weekly_insights(weekly_data, profile, config, locale):
    """Generate weekly review text and action items."""
    is_ja = resolve_locale(locale=locale) == "ja-JP"
    context = {
        "condition_name": weekly_data.get("condition_text", ""),
        "primary_condition": weekly_data.get("primary_condition", ""),
        "profile_summary": (
            f"{profile.get('name', t(locale, 'default_name'))}、{profile.get('age', '-')}歳、身長 {profile.get('height_cm', '-')}cm、現在体重 {format_weight(locale, weekly_data.get('latest_weight') or profile.get('current_weight_kg'))}、目標体重 {format_weight(locale, profile.get('target_weight_kg'))}"
            if is_ja
            else localize(
                locale,
                f"{profile.get('name', t(locale, 'default_name'))}，{profile.get('age', '-')} 岁，身高 {profile.get('height_cm', '-')}cm，当前体重 {format_weight(locale, weekly_data.get('latest_weight') or profile.get('current_weight_kg'))}，目标体重 {format_weight(locale, profile.get('target_weight_kg'))}",
                f"{profile.get('name', t(locale, 'default_name'))}, age {profile.get('age', '-')}, height {profile.get('height_cm', '-')}cm, current weight {format_weight(locale, weekly_data.get('latest_weight') or profile.get('current_weight_kg'))}, target weight {format_weight(locale, profile.get('target_weight_kg'))}",
            )
        ),
        "diet_principle": weekly_data.get("diet_principle", ""),
        "step_target": profile.get("step_target", 8000),
        "water_target": profile.get("water_target_ml", 2000),
        "weight_change": format_weight_delta(locale, weekly_data.get("weight_change", 0)),
        "avg_total_score": weekly_data.get("avg_total_score", 0),
        "avg_diet_score": weekly_data.get("avg_diet_score", 0),
        "avg_calories": weekly_data.get("avg_calories", 0),
        "avg_water": weekly_data.get("avg_water", 0),
        "avg_steps": weekly_data.get("avg_steps", 0),
        "water_goal_days": weekly_data.get("water_goal_days", 0),
        "step_goal_days": weekly_data.get("step_goal_days", 0),
        "diet_goal_days": weekly_data.get("diet_goal_days", 0),
        "symptom_days": weekly_data.get("symptom_days", 0),
        "symptoms_count": weekly_data.get("symptom_events", 0),
        "medication_days": weekly_data.get("medication_days", 0),
        "best_day": summarize_day(weekly_data.get("best_day"), locale),
        "focus_day": summarize_day(weekly_data.get("focus_day"), locale),
        "strengths": " | ".join(weekly_data.get("strengths", [])) or ("なし" if is_ja else localize(locale, "暂无", "None")),
        "gaps": " | ".join(weekly_data.get("gaps", [])) or ("なし" if is_ja else localize(locale, "暂无", "None")),
        "next_focus": " | ".join(weekly_data.get("next_focus", [])) or ("現在のリズムを維持" if is_ja else localize(locale, "保持稳定", "Keep the current routine")),
        "custom_sections": " | ".join(
            f"{section['title']}:{section.get('days_recorded', 0)}"
            for section in weekly_data.get("custom_section_stats", [])
            if section.get("days_recorded", 0) > 0
        ) or ("なし" if is_ja else localize(locale, "暂无", "None")),
    }
    prompt = build_weekly_ai_prompt(locale, context)
    output = run_local_llm(
        prompt=prompt,
        system_prompt=build_weekly_ai_system_prompt(locale),
        settings=get_generation_settings(config, "expert_commentary"),
        locale=locale,
        timeout_key="ai_comment_timeout",
        failure_key="weekly_ai_failed",
    )
    if output:
        review, plan = parse_weekly_ai_output(output)
        if review and plan:
            return review, plan, "llm", "llm"

    review, plan, source = build_weekly_fallback_insights(weekly_data, profile, locale)
    return review, plan, source, source


def generate_weekly_text_report(weekly_data, profile, ai_review, ai_plan, locale, review_source, plan_source):
    """Render the weekly text message body."""
    def heading(title, icon):
        return f"{icon} {title}"

    render_notice = str(weekly_data.get("render_notice") or "").strip()
    profile_lines = [
        f"- 👤 {localize(locale, '监测人', 'Name')}: {profile.get('name', t(locale, 'default_name'))}",
        f"- 🎯 {localize(locale, '管理目标', 'Conditions')}: {weekly_data.get('condition_text', localize(locale, '综合健康管理', 'General health management'))}",
        f"- 🧬 {localize(locale, '年龄', 'Age')}: {profile.get('age', '-')}",
        f"- 📏 {localize(locale, '身高', 'Height')}: {profile.get('height_cm', '-')}cm",
        f"- ⚖️ {localize(locale, '当前体重', 'Current weight')}: {format_weight(locale, weekly_data.get('latest_weight') or profile.get('current_weight_kg'))}",
        f"- 🥅 {localize(locale, '目标体重', 'Target weight')}: {format_weight(locale, profile.get('target_weight_kg'))}",
        f"- 💧 {localize(locale, '饮水目标', 'Hydration target')}: {profile.get('water_target_ml', 2000)}ml",
        f"- 👟 {localize(locale, '步数目标', 'Step target')}: {profile.get('step_target', 8000)}",
    ]

    summary_lines = [
        f"- 🏆 {localize(locale, '周均综合评分', 'Average overall score')}: {weekly_data.get('avg_total_score', 0):.1f}/100",
        f"- ⚖️ {t(locale, 'weekly_avg_weight_change', value=format_weight_delta(locale, weekly_data['weight_change']))}",
        f"- 🔥 {t(locale, 'weekly_avg_calories_line', value=weekly_data['avg_calories'])}",
        f"- 💧 {t(locale, 'weekly_avg_water_line', value=weekly_data['avg_water'])}",
        f"- 👟 {t(locale, 'weekly_avg_steps_line', value=weekly_data['avg_steps'])}",
        f"- 🍽️ {localize(locale, '饮食达标天数', 'Diet goal days')}: {weekly_data.get('diet_goal_days', 0)}/7",
        f"- 🚰 {localize(locale, '饮水达标天数', 'Hydration goal days')}: {weekly_data.get('water_goal_days', 0)}/7",
        f"- 🏃 {localize(locale, '步数达标天数', 'Step goal days')}: {weekly_data.get('step_goal_days', 0)}/7",
        f"- 🩺 {localize(locale, '症状天数', 'Symptom days')}: {weekly_data.get('symptom_days', 0)}/7",
        f"- 📍 {t(locale, 'weekly_symptom_count_line', value=weekly_data['symptom_events'])}",
    ]
    if weekly_data.get("medication_enabled"):
        summary_lines.append(f"- 💊 {localize(locale, '用药记录天数', 'Medication log days')}: {weekly_data.get('medication_days', 0)}/7")
    if weekly_data.get("best_day"):
        summary_lines.append(f"- 🌟 {localize(locale, '本周最佳日', 'Best day')}: {summarize_day(weekly_data.get('best_day'), locale)}")
    if weekly_data.get("focus_day"):
        summary_lines.append(f"- 🎯 {localize(locale, '重点复盘日', 'Focus day')}: {summarize_day(weekly_data.get('focus_day'), locale)}")

    custom_lines = []
    for section in weekly_data.get("custom_section_stats", []):
        if section.get("days_recorded", 0) <= 0:
            continue
        if resolve_locale(locale=locale) == "ja-JP":
            custom_lines.append(f"- 🧪 {section['title']}: 記録日数 {section['days_recorded']} 日、項目数 {section.get('items', 0)}")
        else:
            custom_lines.append(f"- 🧪 {section['title']}: {localize(locale, '记录', 'logged')} {section['days_recorded']} {localize(locale, '天', 'days')}, {localize(locale, '条目', 'items')} {section.get('items', 0)}")

    report_lines = [
        f"## {heading(t(locale, 'weekly_text_heading', start_date=weekly_data['start_date'], end_date=weekly_data['end_date']), '🗓️')}",
        "",
        f"### {heading(localize(locale, '个人信息', 'Profile'), '👤')}",
        *profile_lines,
        "",
        f"### {heading(t(locale, 'weekly_summary_title'), '📊')}",
        *summary_lines,
    ]

    if render_notice:
        report_lines.extend([
            "",
            f"### {heading(t(locale, 'render_notice_title'), 'ℹ️')}",
            render_notice,
        ])

    report_lines.extend([
        "",
        f"### {heading(localize(locale, '本周亮点', 'Strengths This Week'), '🌟')}",
        *[f"- {item}" for item in weekly_data.get("strengths", [])],
        "",
        f"### {heading(localize(locale, '待改进项', 'Needs Attention'), '⚠️')}",
        *[f"- {item}" for item in weekly_data.get("gaps", [])],
        "",
        f"### {heading(localize(locale, '下周重点', 'Focus For Next Week'), '🎯')}",
        *[f"- {item}" for item in weekly_data.get("next_focus", [])],
    ])

    if custom_lines:
        report_lines.extend([
            "",
            f"### {heading(localize(locale, '额外监测项目', 'Additional Monitoring'), '🧪')}",
            *custom_lines,
        ])

    report_lines.extend([
        "",
        f"### {heading(t(locale, 'weekly_review_section'), '🧠')}",
        ai_review.strip(),
        f"_{generation_source_label(locale, review_source)}_",
        "",
        f"### {heading(t(locale, 'weekly_plan_section'), '🗺️')}",
        ai_plan.strip(),
        f"_{generation_source_label(locale, plan_source)}_",
    ])
    report_lines = [line for line in report_lines if line is not None]
    if resolve_locale(locale=locale) == "ja-JP":
        report_lines = [sanitize_locale_line(locale, line) for line in report_lines]
    return "\n".join(report_lines).strip()


def publish_weekly_pdf(local_pdf_path):
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
        print("Usage: python3 weekly_report_pro.py <YYYY-MM-DD>")
        sys.exit(1)

    target_date = sys.argv[1]
    base_config = load_user_config()
    week_dates = get_week_dates(target_date)
    week_files = [os.path.join(MEMORY_DIR, f"{date_str}.md") for date_str in week_dates]
    requested_locale = resolve_report_locale(base_config, week_files)
    fallback_context = prepare_font_compatible_memory(
        requested_locale=requested_locale,
        source_dir=MEMORY_DIR,
    )
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

        weekly_data = aggregate_weekly_data(week_dates, config, locale=locale, memory_dir=memory_dir)
        if render_notice:
            weekly_data["render_notice"] = render_notice

        ai_review, ai_plan, review_source, plan_source = get_ai_weekly_insights(weekly_data, profile_payload, config, locale)

        locale_tag = resolve_locale(locale=locale).replace("-", "_")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        pdf_filename = f"weekly_report_{locale_tag}_{timestamp}.pdf"
        local_output_path = os.path.join(REPORTS_DIR, pdf_filename)

        generate_weekly_pdf_report(
            weekly_data,
            profile_payload,
            ai_review,
            ai_plan,
            local_output_path,
            locale=locale,
            review_source=review_source,
            plan_source=plan_source,
        )
        pdf_url = publish_weekly_pdf(local_output_path)
        text_report = generate_weekly_text_report(weekly_data, profile_payload, ai_review, ai_plan, locale, review_source, plan_source)
        delivery_message = build_delivery_message(
            locale=locale,
            body=text_report,
            pdf_url=pdf_url,
            report_kind="weekly",
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            start_date=weekly_data["start_date"],
            end_date=weekly_data["end_date"],
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
