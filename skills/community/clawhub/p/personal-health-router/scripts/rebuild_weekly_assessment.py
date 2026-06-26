#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from collections import defaultdict
from datetime import date, datetime, timedelta
from statistics import median
from typing import Any
from zoneinfo import ZoneInfo

from config_loader import get_field_aliases, get_schema_field_names, get_table, get_threshold, load_config

TIMEZONE = ZoneInfo("Asia/Hong_Kong")

NUTRITION = {
    "date": ["Date", "日期"],
    "calories": ["Total Calories (kcal)", "总热量(kcal)"],
    "calories_ref": ["Reference Calories (kcal)", "参考热量(kcal)"],
    "protein": ["Total Protein (g)", "总蛋白质(g)"],
    "protein_ref": ["Reference Protein (g)", "参考蛋白质(g)"],
    "sodium": ["Total Sodium (mg)", "总钠(mg)"],
    "sodium_ref": ["Reference Sodium (mg)", "参考钠(mg)"],
    "fiber": ["Total Fiber (g)", "总膳食纤维(g)"],
    "fiber_ref": ["Reference Fiber (g)", "参考膳食纤维(g)"],
}

SLEEP = {
    "date": ["Date", "日期"],
    "score": ["Sleep Score", "睡眠评分"],
    "recovery": ["Recovery State", "恢复状态"],
    "fatigue": ["Fatigue Risk", "疲劳风险"],
    "summary": ["One-Line Summary", "一句话总结"],
    "minutes": ["Total Sleep Minutes", "总睡眠分钟"],
    "hrv": ["HRV"],
}

EXERCISE = {
    "date": ["Logged At", "日期时间"],
    "type": ["Workout Type", "运动类型"],
    "duration": ["Duration Minutes", "总时长分钟"],
    "calories": ["Calories (kcal)", "热量(kcal)"],
    "load": ["Load", "强度/负荷", "训练负荷分数(计算)"],
}

WEEKLY = {
    "start": ["Week Start", "周开始"],
    "end": ["Week End", "周结束"],
    "key": ["Week Key", "周标识"],
    "status": ["Weekly Health Status", "周健康状态"],
    "record_days": ["Recorded Days", "记录天数"],
    "nutrition_days": ["Nutrition Days", "营养记录天数"],
    "sleep_days": ["Sleep Days", "睡眠记录天数"],
    "workout_days": ["Workout Days", "运动记录天数"],
    "nutrition_balanced_days": ["Nutrition On-Target Days", "营养达标天数"],
    "nutrition_low_days": ["Nutrition Low Days", "营养偏低天数"],
    "nutrition_high_days": ["Nutrition High Days", "营养偏高天数"],
    "attention_days": ["Attention Days", "健康关注天数"],
    "alert_days": ["Alert Days", "预警天数"],
    "avg_sleep_score": ["Average Sleep Score", "平均睡眠评分"],
    "low_recovery_days": ["Low Recovery Days", "低恢复天数"],
    "high_fatigue_days": ["High Fatigue Days", "高疲劳天数"],
    "short_sleep_days": ["Short Sleep Days", "睡眠不足天数"],
    "severe_short_sleep_days": ["Severe Short Sleep Days", "严重睡眠不足天数"],
    "protein_low_days": ["Low Protein Days", "蛋白不足天数"],
    "sodium_high_days": ["High Sodium Days", "高钠天数"],
    "hrv_days": ["HRV Recorded Days", "HRV记录天数"],
    "exercise_active_days": ["Active Workout Days", "运动活跃天数"],
    "high_intensity_days": ["High Load Training Days", "高负荷训练天数"],
    "total_exercise_duration": ["Total Workout Minutes", "总运动时长分钟"],
    "total_exercise_calories": ["Total Workout Calories (kcal)", "总运动热量(kcal)"],
    "equiv_minutes": ["Activity Equivalent Minutes", "活动等效分钟"],
    "fuel_gap_days": ["Underfueled Training Days", "训练供能不足天数"],
    "poor_recovery_count": ["Poor Recovery After Training Count", "训练后恢复欠佳次数"],
    "risk_score": ["Composite Risk Score", "综合风险分数"],
    "nutrition_eval": ["Nutrition Weekly Review", "营养周评"],
    "sleep_eval": ["Sleep Weekly Review", "睡眠周评"],
    "exercise_eval": ["Workout Weekly Review", "运动周评"],
    "cross_eval": ["Cross-Domain Reassessment", "跨域再评估"],
    "risk_focus": ["Risk Focus", "风险聚焦"],
    "suggestions": ["Next-Week Actions", "下周行动建议"],
    "brief": ["Chat Brief", "Telegram简报"],
}

WEEKLY_COPY = {
    "no_nutrition_records": "No nutrition rollup records for this week.",
    "nutrition_headline_stable": "Nutrition was broadly stable.",
    "nutrition_headline_unstable": "Nutrition support was mixed and still unstable.",
    "nutrition_summary": "{headline} Avg calories {avg_calorie}, protein {avg_protein}, fiber {avg_fiber}, sodium {avg_sodium}. Low energy {energy_low_days}d, low protein {protein_low_days}d, high sodium {sodium_high_days}d.",
    "no_sleep_records": "No sleep records for this week.",
    "sleep_quality_solid": "sleep was solid",
    "sleep_quality_shaky": "sleep quality was still shaky",
    "sleep_summary": "Overall {quality}. Avg score {avg_score}, avg sleep {avg_hours}. Short sleep {short_sleep_days}d, severe short sleep {severe_short_sleep_days}d, low recovery {low_recovery_days}d, high fatigue {high_fatigue_days}d.",
    "no_workout_records": "No workout records for this week.",
    "workout_level_met": "activity target was met",
    "workout_level_below": "activity volume was still below target",
    "workout_fallback_types": "Recorded workouts",
    "workout_summary": "{level}. {exercise_types} across {session_count} sessions / {active_days} days, {total_minutes} min total, {equivalent_minutes} equivalent min, {total_kcal} kcal.",
    "cross_headline_alert": "Recovery risk stacked up across domains this week.",
    "cross_headline_attention": "The week stayed functional, but recovery efficiency was not stable.",
    "cross_headline_stable": "Nutrition, sleep, and workouts mostly supported each other this week.",
    "risk_focus_none": "No dominant cross-domain conflict detected.",
    "suggestion_sleep": "Push average sleep back above 7 hours and avoid stacking high-load training after short sleep.",
    "suggestion_training_fuel": "Lock in a carbs + protein meal around training days.",
    "suggestion_sodium_fiber": "Cut heavy sauces and add two higher-fiber food exposures per day.",
    "suggestion_activity_gap": "Spread activity across 3-4 moderate sessions instead of relying on one hard day.",
    "suggestion_keep_current": "Keep the current rhythm and focus on data completeness.",
    "brief_title": "Weekly health reassessment ({start_day} to {end_day})",
    "brief_overall": "Overall: {overall}. {cross_text}",
    "brief_nutrition": "Nutrition: {nutrition_text}",
    "brief_sleep": "Sleep: {sleep_text}",
    "brief_workout": "Workout: {workout_text}",
    "brief_risk_focus": "Risk focus: {risk_focus}",
    "brief_next_actions": "Next-week actions: {next_actions}",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rebuild weekly health assessment rows.")
    parser.add_argument("config", help="Path to config JSON")
    parser.add_argument("--week-end", help="Use this Sunday (YYYY-MM-DD) as the week end")
    parser.add_argument("--identity", default="user", choices=["user", "bot"])
    parser.add_argument("--backfill-full-weeks", action="store_true")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    return parser.parse_args()


def get_weekly_copy(config: dict[str, Any]) -> dict[str, str]:
    copy = dict(WEEKLY_COPY)
    source = ((config.get("copy") or {}).get("weekly_health_assessment") or {})
    for key in WEEKLY_COPY:
        if source.get(key) is not None:
            copy[key] = str(source[key])
    return copy


def normalize_value(value: Any) -> Any:
    if isinstance(value, list):
        if len(value) == 1 and not isinstance(value[0], dict):
            return value[0]
        if value and isinstance(value[0], dict) and "text" in value[0]:
            return "".join(str(item.get("text", "")) for item in value)
    return value


def run_json(args: list[str]) -> dict[str, Any]:
    proc = subprocess.run(args, capture_output=True, text=True, check=True)
    return json.loads(proc.stdout)


def list_records(base_token: str, table_ref: str, identity: str) -> tuple[list[dict[str, Any]], list[str]]:
    offset = 0
    limit = 200
    rows: list[dict[str, Any]] = []
    all_fields: list[str] = []
    while True:
        payload = run_json([
            "lark-cli", "base", "+record-list",
            "--as", identity,
            "--base-token", base_token,
            "--table-id", table_ref,
            "--offset", str(offset),
            "--limit", str(limit),
        ])
        data = payload.get("data", {})
        matrix = data.get("data", []) or []
        fields = data.get("fields", []) or []
        if fields and not all_fields:
            all_fields = list(fields)
        record_ids = data.get("record_id_list", []) or []
        page_rows = []
        for row_index, row in enumerate(matrix):
            field_map = {}
            for field_index, field_name in enumerate(fields):
                field_map[field_name] = normalize_value(row[field_index] if field_index < len(row) else None)
            page_rows.append({
                "record_id": record_ids[row_index] if row_index < len(record_ids) else None,
                "fields": field_map,
            })
        rows.extend(page_rows)
        if not page_rows or not data.get("has_more"):
            break
        offset += len(page_rows)
    return rows, all_fields


def merged_aliases(config: dict[str, Any], table_key: str, defaults: dict[str, list[str]]) -> dict[str, list[str]]:
    merged = {key: list(value) for key, value in defaults.items()}
    for key, aliases in get_field_aliases(config, table_key).items():
        merged[key] = aliases + [alias for alias in merged.get(key, []) if alias not in aliases]
    return merged


def resolve_fields(config: dict[str, Any], table_key: str, defaults: dict[str, list[str]], available_fields: list[str]) -> dict[str, str]:
    aliases = merged_aliases(config, table_key, defaults)
    available = list(dict.fromkeys((available_fields or []) + get_schema_field_names(config, table_key)))
    resolved: dict[str, str] = {}
    for key, candidates in aliases.items():
        resolved[key] = next((candidate for candidate in candidates if candidate in available), candidates[0])
    return resolved


def upsert_record(base_token: str, table_ref: str, identity: str, payload: dict[str, Any], record_id: str | None = None) -> dict[str, Any]:
    cmd = [
        "lark-cli", "base", "+record-upsert",
        "--as", identity,
        "--base-token", base_token,
        "--table-id", table_ref,
        "--json", json.dumps(payload, ensure_ascii=False),
    ]
    if record_id:
        cmd.extend(["--record-id", record_id])
    return run_json(cmd)


def parse_local_dt(value: Any) -> datetime | None:
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        ts = float(value)
        if ts > 10**12:
            ts /= 1000
        return datetime.fromtimestamp(ts, TIMEZONE)
    raw = str(value).strip()
    try:
        ts = float(raw)
        if ts > 10**12:
            ts /= 1000
        return datetime.fromtimestamp(ts, TIMEZONE)
    except ValueError:
        pass
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S", "%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(raw, fmt).replace(tzinfo=TIMEZONE)
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).astimezone(TIMEZONE)
    except Exception:
        return None


def local_date_key(value: Any) -> str | None:
    dt = parse_local_dt(value)
    return dt.date().isoformat() if dt else None


def midnight_string(day: date) -> str:
    return f"{day.isoformat()} 00:00:00"


def to_number(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except Exception:
        return None


def average(values: list[float]) -> float | None:
    if not values:
        return None
    return round(sum(values) / len(values), 1)


def fmt_percent(value: float | None) -> str:
    return f"{value}%" if value is not None else "n/a"


def ratio_percent(actual: Any, reference: Any) -> float | None:
    actual_num = to_number(actual)
    reference_num = to_number(reference)
    if actual_num is None or reference_num in (None, 0):
        return None
    return round(actual_num / reference_num * 100, 1)


def last_completed_sunday(reference_day: date) -> date:
    return reference_day - timedelta(days=(reference_day.weekday() + 1) % 7)


def monday_start(week_end: date) -> date:
    return week_end - timedelta(days=6)


def choose_latest(records: list[dict[str, Any]], field_name: str) -> dict[str, Any] | None:
    best: dict[str, Any] | None = None
    best_dt: datetime | None = None
    for record in records:
        dt = parse_local_dt(record["fields"].get(field_name))
        if dt is None:
            continue
        if best is None or best_dt is None or dt > best_dt:
            best = record
            best_dt = dt
    return best or (records[-1] if records else None)


def unique_join(values: list[str]) -> str:
    seen: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.append(value)
    return ", ".join(seen)


def load_buckets(config: dict[str, Any]) -> dict[str, float]:
    weekly = config.get("weekly_thresholds", {})
    return {
        "protein_low_ratio": float(weekly.get("protein_low_ratio", 90)),
        "severe_protein_low_ratio": float(weekly.get("severe_protein_low_ratio", 75)),
        "fiber_low_ratio": float(weekly.get("fiber_low_ratio", 80)),
        "sodium_high_ratio": float(weekly.get("sodium_high_ratio", 115)),
        "sodium_very_high_ratio": float(weekly.get("sodium_very_high_ratio", 130)),
        "energy_low_ratio": float(weekly.get("energy_low_ratio", 85)),
        "severe_energy_low_ratio": float(weekly.get("severe_energy_low_ratio", 70)),
        "short_sleep_minutes": float(weekly.get("short_sleep_minutes", 420)),
        "severe_short_sleep_minutes": float(weekly.get("severe_short_sleep_minutes", 360)),
        "low_sleep_score": float(weekly.get("low_sleep_score", 75)),
        "good_sleep_score": float(weekly.get("good_sleep_score", 80)),
        "weekly_activity_equiv_target": float(weekly.get("weekly_activity_equiv_target", 150)),
        "weekly_activity_equiv_high": float(weekly.get("weekly_activity_equiv_high", 300)),
    }


def intensity_weight(load: str | None) -> float:
    load = str(load or "").strip()
    numeric = to_number(load)
    if numeric is not None:
        if numeric >= 7:
            return 1.5
        if numeric >= 4:
            return 1.0
        return 0.75
    if load == "High":
        return 1.5
    if load == "Medium":
        return 1.0
    if load == "Light":
        return 0.75
    return 1.0


def build_context(config: dict[str, Any], identity: str) -> tuple[dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]], dict[str, list[dict[str, Any]]], dict[str, str], dict[str, str], dict[str, str]]:
    base_token = config["feishu"]["active_base"]["token"]
    nutrition_table = get_table(config, "nutrition_daily_history")
    sleep_table = get_table(config, "sleep_recovery")
    exercise_table = get_table(config, "exercise_workout")

    nutrition_rows, nutrition_fields = list_records(base_token, nutrition_table.get("table_id") or nutrition_table["name"], identity)
    sleep_rows, sleep_fields = list_records(base_token, sleep_table.get("table_id") or sleep_table["name"], identity)
    exercise_rows, exercise_fields = list_records(base_token, exercise_table.get("table_id") or exercise_table["name"], identity)

    nutrition_map = resolve_fields(config, "nutrition_daily_history", NUTRITION, nutrition_fields)
    sleep_map = resolve_fields(config, "sleep_recovery", SLEEP, sleep_fields)
    exercise_map = resolve_fields(config, "exercise_workout", EXERCISE, exercise_fields)

    nutrition_by_date: dict[str, dict[str, Any]] = {}
    for row in nutrition_rows:
        date_key = local_date_key(row["fields"].get(nutrition_map["date"]))
        if date_key:
            nutrition_by_date[date_key] = row["fields"]

    sleep_by_date: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in sleep_rows:
        date_key = local_date_key(row["fields"].get(sleep_map["date"]))
        if date_key:
            sleep_by_date[date_key].append(row)

    exercise_by_date: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in exercise_rows:
        date_key = local_date_key(row["fields"].get(exercise_map["date"]))
        if date_key:
            exercise_by_date[date_key].append(row)

    return nutrition_by_date, sleep_by_date, exercise_by_date, nutrition_map, sleep_map, exercise_map


def build_profiles(start_day: date, end_day: date, nutrition_by_date: dict[str, dict[str, Any]], sleep_by_date: dict[str, list[dict[str, Any]]], exercise_by_date: dict[str, list[dict[str, Any]]], nutrition_map: dict[str, str], sleep_map: dict[str, str], exercise_map: dict[str, str], thresholds: dict[str, float]) -> list[dict[str, Any]]:
    profiles: list[dict[str, Any]] = []
    current = start_day
    while current <= end_day:
        date_key = current.isoformat()
        nutrition_fields = nutrition_by_date.get(date_key, {})
        sleep_record = choose_latest(sleep_by_date.get(date_key, []), sleep_map["date"])
        sleep_fields = sleep_record["fields"] if sleep_record else {}
        exercises = exercise_by_date.get(date_key, [])

        calorie_ratio = ratio_percent(nutrition_fields.get(nutrition_map["calories"]), nutrition_fields.get(nutrition_map["calories_ref"]))
        protein_ratio = ratio_percent(nutrition_fields.get(nutrition_map["protein"]), nutrition_fields.get(nutrition_map["protein_ref"]))
        fiber_ratio = ratio_percent(nutrition_fields.get(nutrition_map["fiber"]), nutrition_fields.get(nutrition_map["fiber_ref"]))
        sodium_ratio = ratio_percent(nutrition_fields.get(nutrition_map["sodium"]), nutrition_fields.get(nutrition_map["sodium_ref"]))

        sleep_score = to_number(sleep_fields.get(sleep_map["score"]))
        sleep_minutes = to_number(sleep_fields.get(sleep_map["minutes"]))
        hrv = to_number(sleep_fields.get(sleep_map["hrv"]))
        recovery_state = str(sleep_fields.get(sleep_map["recovery"]) or "") or None
        fatigue_risk = str(sleep_fields.get(sleep_map["fatigue"]) or "") or None

        session_count = len(exercises)
        workout_minutes = 0.0
        workout_kcal = 0.0
        equiv_minutes = 0.0
        high_load_sessions = 0
        workout_types: list[str] = []
        for exercise in exercises:
            fields = exercise["fields"]
            minutes = to_number(fields.get(exercise_map["duration"])) or 0.0
            kcal = to_number(fields.get(exercise_map["calories"])) or 0.0
            load = str(fields.get(exercise_map["load"]) or "")
            workout_minutes += minutes
            workout_kcal += kcal
            equiv_minutes += minutes * intensity_weight(load)
            if load == "High":
                high_load_sessions += 1
            workout_type = str(fields.get(exercise_map["type"]) or "").strip()
            if workout_type:
                workout_types.append(workout_type)

        energy_low = calorie_ratio is not None and calorie_ratio < thresholds["energy_low_ratio"]
        severe_energy_low = calorie_ratio is not None and calorie_ratio < thresholds["severe_energy_low_ratio"]
        protein_low = protein_ratio is not None and protein_ratio < thresholds["protein_low_ratio"]
        severe_protein_low = protein_ratio is not None and protein_ratio < thresholds["severe_protein_low_ratio"]
        fiber_low = fiber_ratio is not None and fiber_ratio < thresholds["fiber_low_ratio"]
        sodium_high = sodium_ratio is not None and sodium_ratio > thresholds["sodium_high_ratio"]
        sodium_very_high = sodium_ratio is not None and sodium_ratio > thresholds["sodium_very_high_ratio"]
        short_sleep = sleep_minutes is not None and sleep_minutes < thresholds["short_sleep_minutes"]
        severe_short_sleep = sleep_minutes is not None and sleep_minutes < thresholds["severe_short_sleep_minutes"]
        low_recovery = recovery_state in {"Poor", "Weak"}
        high_fatigue = fatigue_risk in {"Medium to High", "High"}
        low_sleep_score = sleep_score is not None and sleep_score < thresholds["low_sleep_score"]

        workout_day = session_count > 0
        high_stress_training = workout_day and (high_load_sessions > 0 or equiv_minutes >= 45)
        training_fuel_gap = workout_day and (energy_low or protein_low)
        severe_training_fuel_gap = workout_day and (severe_energy_low or severe_protein_low)
        poor_recovery_after_training = workout_day and (short_sleep or low_recovery or high_fatigue or low_sleep_score)
        sodium_recovery_overlap = sodium_high and (low_recovery or high_fatigue or low_sleep_score)

        domain_count = int(energy_low or protein_low or fiber_low or sodium_high) + int(short_sleep or low_recovery or high_fatigue or low_sleep_score) + int(high_stress_training)
        if severe_training_fuel_gap or (severe_short_sleep and workout_day) or (sodium_very_high and (low_recovery or high_fatigue)):
            daily_status = "Alert"
        elif domain_count >= 2:
            daily_status = "Attention"
        else:
            daily_status = "Stable"

        profiles.append({
            "date_key": date_key,
            "nutrition_present": bool(nutrition_fields),
            "sleep_present": bool(sleep_fields),
            "workout_present": workout_day,
            "calorie_ratio": calorie_ratio,
            "protein_ratio": protein_ratio,
            "fiber_ratio": fiber_ratio,
            "sodium_ratio": sodium_ratio,
            "sleep_score": sleep_score,
            "sleep_minutes": sleep_minutes,
            "hrv": hrv,
            "recovery_state": recovery_state,
            "fatigue_risk": fatigue_risk,
            "session_count": session_count,
            "workout_minutes": round(workout_minutes, 1),
            "workout_kcal": round(workout_kcal, 1),
            "equiv_minutes": round(equiv_minutes, 1),
            "high_load_sessions": high_load_sessions,
            "workout_types": workout_types,
            "energy_low": energy_low,
            "severe_energy_low": severe_energy_low,
            "protein_low": protein_low,
            "severe_protein_low": severe_protein_low,
            "fiber_low": fiber_low,
            "sodium_high": sodium_high,
            "sodium_very_high": sodium_very_high,
            "short_sleep": short_sleep,
            "severe_short_sleep": severe_short_sleep,
            "low_recovery": low_recovery,
            "high_fatigue": high_fatigue,
            "low_sleep_score": low_sleep_score,
            "training_fuel_gap": training_fuel_gap,
            "severe_training_fuel_gap": severe_training_fuel_gap,
            "poor_recovery_after_training": poor_recovery_after_training,
            "sodium_recovery_overlap": sodium_recovery_overlap,
            "daily_status": daily_status,
        })
        current += timedelta(days=1)
    return profiles


def summarize_nutrition(profiles: list[dict[str, Any]], copy: dict[str, str]) -> tuple[str, dict[str, Any]]:
    nutrition_profiles = [p for p in profiles if p["nutrition_present"]]
    stats = {
        "record_days": len(nutrition_profiles),
        "avg_calorie": average([p["calorie_ratio"] for p in nutrition_profiles if p["calorie_ratio"] is not None]),
        "avg_protein": average([p["protein_ratio"] for p in nutrition_profiles if p["protein_ratio"] is not None]),
        "avg_fiber": average([p["fiber_ratio"] for p in nutrition_profiles if p["fiber_ratio"] is not None]),
        "avg_sodium": average([p["sodium_ratio"] for p in nutrition_profiles if p["sodium_ratio"] is not None]),
        "balanced_days": sum(1 for p in nutrition_profiles if (p["calorie_ratio"] is not None and 85 <= p["calorie_ratio"] <= 115) and (p["protein_ratio"] is not None and p["protein_ratio"] >= 100) and (p["fiber_ratio"] is None or p["fiber_ratio"] >= 80) and (p["sodium_ratio"] is None or p["sodium_ratio"] <= 110)),
        "energy_low_days": sum(1 for p in nutrition_profiles if p["energy_low"]),
        "severe_energy_low_days": sum(1 for p in nutrition_profiles if p["severe_energy_low"]),
        "protein_low_days": sum(1 for p in nutrition_profiles if p["protein_low"]),
        "fiber_low_days": sum(1 for p in nutrition_profiles if p["fiber_low"]),
        "sodium_high_days": sum(1 for p in nutrition_profiles if p["sodium_high"]),
    }
    if stats["record_days"] == 0:
        return copy["no_nutrition_records"], stats
    headline = copy["nutrition_headline_stable"] if stats["balanced_days"] >= 4 and stats["protein_low_days"] <= 1 and stats["sodium_high_days"] <= 1 else copy["nutrition_headline_unstable"]
    text = copy["nutrition_summary"].format(
        headline=headline,
        avg_calorie=fmt_percent(stats['avg_calorie']),
        avg_protein=fmt_percent(stats['avg_protein']),
        avg_fiber=fmt_percent(stats['avg_fiber']),
        avg_sodium=fmt_percent(stats['avg_sodium']),
        energy_low_days=stats['energy_low_days'],
        protein_low_days=stats['protein_low_days'],
        sodium_high_days=stats['sodium_high_days'],
    )
    return text, stats


def summarize_sleep(profiles: list[dict[str, Any]], thresholds: dict[str, float], copy: dict[str, str]) -> tuple[str, dict[str, Any]]:
    sleep_profiles = [p for p in profiles if p["sleep_present"]]
    hrv_values = [p["hrv"] for p in sleep_profiles if p["hrv"] is not None]
    baseline = median(hrv_values) if len(hrv_values) >= 3 else None
    stats = {
        "record_days": len(sleep_profiles),
        "avg_score": average([p["sleep_score"] for p in sleep_profiles if p["sleep_score"] is not None]),
        "avg_sleep_minutes": average([p["sleep_minutes"] for p in sleep_profiles if p["sleep_minutes"] is not None]),
        "short_sleep_days": sum(1 for p in sleep_profiles if p["short_sleep"]),
        "severe_short_sleep_days": sum(1 for p in sleep_profiles if p["severe_short_sleep"]),
        "low_recovery_days": sum(1 for p in sleep_profiles if p["low_recovery"]),
        "high_fatigue_days": sum(1 for p in sleep_profiles if p["high_fatigue"]),
        "hrv_record_days": len(hrv_values),
        "hrv_suppressed_days": sum(1 for value in hrv_values if baseline is not None and value < baseline * 0.85),
    }
    if stats["record_days"] == 0:
        return copy["no_sleep_records"], stats
    quality = copy["sleep_quality_solid"] if stats["avg_score"] is not None and stats["avg_score"] >= thresholds["good_sleep_score"] and stats["short_sleep_days"] <= 1 else copy["sleep_quality_shaky"]
    avg_hours = f"{stats['avg_sleep_minutes'] / 60:.1f}h" if stats["avg_sleep_minutes"] is not None else "n/a"
    text = copy["sleep_summary"].format(
        quality=quality,
        avg_score=stats['avg_score'],
        avg_hours=avg_hours,
        short_sleep_days=stats['short_sleep_days'],
        severe_short_sleep_days=stats['severe_short_sleep_days'],
        low_recovery_days=stats['low_recovery_days'],
        high_fatigue_days=stats['high_fatigue_days'],
    )
    return text, stats


def summarize_workout(profiles: list[dict[str, Any]], thresholds: dict[str, float], copy: dict[str, str]) -> tuple[str, dict[str, Any]]:
    active = [p for p in profiles if p["workout_present"]]
    total_minutes = round(sum(p["workout_minutes"] for p in active), 1)
    total_kcal = round(sum(p["workout_kcal"] for p in active), 1)
    equiv_minutes = round(sum(p["equiv_minutes"] for p in active), 1)
    high_load_days = sum(1 for p in active if p["high_load_sessions"] > 0)
    stats = {
        "record_days": len(active),
        "active_days": len(active),
        "session_count": sum(p["session_count"] for p in active),
        "total_minutes": total_minutes,
        "total_kcal": total_kcal,
        "equivalent_minutes": equiv_minutes,
        "high_load_days": high_load_days,
        "exercise_types": unique_join([exercise_type for p in active for exercise_type in p["workout_types"]]),
        "post_exercise_poor_recovery_count": sum(1 for p in active if p["poor_recovery_after_training"]),
        "activity_gap": equiv_minutes < thresholds["weekly_activity_equiv_target"],
    }
    if stats["session_count"] == 0:
        return copy["no_workout_records"], stats
    level = copy["workout_level_met"] if equiv_minutes >= thresholds["weekly_activity_equiv_target"] else copy["workout_level_below"]
    text = copy["workout_summary"].format(
        level=level,
        exercise_types=stats['exercise_types'] or copy['workout_fallback_types'],
        session_count=stats['session_count'],
        active_days=stats['active_days'],
        total_minutes=total_minutes,
        equivalent_minutes=equiv_minutes,
        total_kcal=total_kcal,
    )
    return text, stats


def compute_cross_domain(profiles: list[dict[str, Any]], nutrition_stats: dict[str, Any], sleep_stats: dict[str, Any], workout_stats: dict[str, Any], copy: dict[str, str]) -> tuple[str, str, str, str, dict[str, Any]]:
    training_fuel_gap_days = sum(1 for p in profiles if p["training_fuel_gap"])
    severe_training_fuel_gap_days = sum(1 for p in profiles if p["severe_training_fuel_gap"])
    sodium_recovery_overlap_days = sum(1 for p in profiles if p["sodium_recovery_overlap"])
    attention_days = sum(1 for p in profiles if p["daily_status"] in {"Attention", "Alert"})
    alert_days = sum(1 for p in profiles if p["daily_status"] == "Alert")
    stacked_risk_days = sum(1 for p in profiles if sum([int(p["energy_low"] or p["protein_low"] or p["fiber_low"] or p["sodium_high"]), int(p["short_sleep"] or p["low_recovery"] or p["high_fatigue"]), int(p["workout_present"])]) >= 2)
    risk_score = 0
    risk_score += 2 if nutrition_stats["protein_low_days"] >= 3 else 1 if nutrition_stats["protein_low_days"] >= 2 else 0
    risk_score += 2 if sleep_stats["severe_short_sleep_days"] >= 1 else 1 if sleep_stats["short_sleep_days"] >= 2 else 0
    risk_score += 1 if workout_stats["activity_gap"] else 0
    risk_score += 2 if training_fuel_gap_days >= 2 else 1 if training_fuel_gap_days == 1 else 0
    risk_score += 2 if workout_stats["post_exercise_poor_recovery_count"] >= 2 else 1 if workout_stats["post_exercise_poor_recovery_count"] == 1 else 0
    risk_score += 2 if stacked_risk_days >= 2 else 1 if stacked_risk_days == 1 else 0

    if alert_days >= 2 or severe_training_fuel_gap_days >= 2 or risk_score >= 8:
        overall = "Alert"
        headline = copy["cross_headline_alert"]
    elif alert_days >= 1 or risk_score >= 4:
        overall = "Attention"
        headline = copy["cross_headline_attention"]
    else:
        overall = "Stable"
        headline = copy["cross_headline_stable"]

    focus_items = []
    if nutrition_stats["energy_low_days"] >= 2:
        focus_items.append(f"low energy on {nutrition_stats['energy_low_days']} days")
    if nutrition_stats["protein_low_days"] >= 2:
        focus_items.append(f"low protein on {nutrition_stats['protein_low_days']} days")
    if sleep_stats["short_sleep_days"] >= 2:
        focus_items.append(f"short sleep on {sleep_stats['short_sleep_days']} days")
    if workout_stats["post_exercise_poor_recovery_count"] >= 1:
        focus_items.append(f"poor recovery after training on {workout_stats['post_exercise_poor_recovery_count']} days")
    if sodium_recovery_overlap_days >= 1:
        focus_items.append(f"high sodium overlapping weak recovery on {sodium_recovery_overlap_days} days")
    risk_focus = "; ".join(focus_items[:3]) or copy["risk_focus_none"]

    suggestions = []
    if sleep_stats["short_sleep_days"] >= 2:
        suggestions.append(copy["suggestion_sleep"])
    if training_fuel_gap_days >= 1 or nutrition_stats["protein_low_days"] >= 2:
        suggestions.append(copy["suggestion_training_fuel"])
    if nutrition_stats["sodium_high_days"] >= 2 or nutrition_stats["fiber_low_days"] >= 2:
        suggestions.append(copy["suggestion_sodium_fiber"])
    if workout_stats["activity_gap"]:
        suggestions.append(copy["suggestion_activity_gap"])
    next_actions = "; ".join(suggestions[:3]) or copy["suggestion_keep_current"]

    cross_stats = {
        "training_fuel_gap_days": training_fuel_gap_days,
        "severe_training_fuel_gap_days": severe_training_fuel_gap_days,
        "attention_days": attention_days,
        "alert_days": alert_days,
        "stacked_risk_days": stacked_risk_days,
        "sodium_recovery_overlap_days": sodium_recovery_overlap_days,
        "risk_score": risk_score,
        "post_exercise_poor_recovery_count": workout_stats["post_exercise_poor_recovery_count"],
    }
    return headline, risk_focus, next_actions, overall, cross_stats


def render_brief(start_day: date, end_day: date, overall: str, nutrition_text: str, sleep_text: str, workout_text: str, cross_text: str, risk_focus: str, next_actions: str, copy: dict[str, str]) -> str:
    return "\n".join([
        copy["brief_title"].format(start_day=start_day.isoformat(), end_day=end_day.isoformat()),
        copy["brief_overall"].format(overall=overall, cross_text=cross_text),
        "",
        copy["brief_nutrition"].format(nutrition_text=nutrition_text),
        copy["brief_sleep"].format(sleep_text=sleep_text),
        copy["brief_workout"].format(workout_text=workout_text),
        "",
        copy["brief_risk_focus"].format(risk_focus=risk_focus),
        copy["brief_next_actions"].format(next_actions=next_actions),
    ]).strip()


def build_payload(start_day: date, end_day: date, profiles: list[dict[str, Any]], weekly_map: dict[str, str], thresholds: dict[str, float], copy: dict[str, str]) -> tuple[dict[str, Any], str]:
    nutrition_text, nutrition_stats = summarize_nutrition(profiles, copy)
    sleep_text, sleep_stats = summarize_sleep(profiles, thresholds, copy)
    workout_text, workout_stats = summarize_workout(profiles, thresholds, copy)
    cross_text, risk_focus, next_actions, overall, cross_stats = compute_cross_domain(profiles, nutrition_stats, sleep_stats, workout_stats, copy)
    brief = render_brief(start_day, end_day, overall, nutrition_text, sleep_text, workout_text, cross_text, risk_focus, next_actions, copy)
    payload = {
        weekly_map["start"]: midnight_string(start_day),
        weekly_map["end"]: midnight_string(end_day),
        weekly_map["key"]: f"{start_day.isoformat()}~{end_day.isoformat()}",
        weekly_map["status"]: overall,
        weekly_map["record_days"]: sum(1 for p in profiles if p["nutrition_present"] or p["sleep_present"] or p["workout_present"]),
        weekly_map["nutrition_days"]: nutrition_stats["record_days"],
        weekly_map["sleep_days"]: sleep_stats["record_days"],
        weekly_map["workout_days"]: workout_stats["record_days"],
        weekly_map["nutrition_balanced_days"]: nutrition_stats["balanced_days"],
        weekly_map["nutrition_low_days"]: nutrition_stats["energy_low_days"],
        weekly_map["nutrition_high_days"]: nutrition_stats["sodium_high_days"],
        weekly_map["attention_days"]: cross_stats["attention_days"],
        weekly_map["alert_days"]: cross_stats["alert_days"],
        weekly_map["avg_sleep_score"]: sleep_stats["avg_score"],
        weekly_map["low_recovery_days"]: sleep_stats["low_recovery_days"],
        weekly_map["high_fatigue_days"]: sleep_stats["high_fatigue_days"],
        weekly_map["short_sleep_days"]: sleep_stats["short_sleep_days"],
        weekly_map["severe_short_sleep_days"]: sleep_stats["severe_short_sleep_days"],
        weekly_map["protein_low_days"]: nutrition_stats["protein_low_days"],
        weekly_map["sodium_high_days"]: nutrition_stats["sodium_high_days"],
        weekly_map["hrv_days"]: sleep_stats["hrv_record_days"],
        weekly_map["exercise_active_days"]: workout_stats["active_days"],
        weekly_map["high_intensity_days"]: workout_stats["high_load_days"],
        weekly_map["total_exercise_duration"]: workout_stats["total_minutes"],
        weekly_map["total_exercise_calories"]: workout_stats["total_kcal"],
        weekly_map["equiv_minutes"]: workout_stats["equivalent_minutes"],
        weekly_map["fuel_gap_days"]: cross_stats["training_fuel_gap_days"],
        weekly_map["poor_recovery_count"]: cross_stats["post_exercise_poor_recovery_count"],
        weekly_map["risk_score"]: cross_stats["risk_score"],
        weekly_map["nutrition_eval"]: nutrition_text,
        weekly_map["sleep_eval"]: sleep_text,
        weekly_map["exercise_eval"]: workout_text,
        weekly_map["cross_eval"]: cross_text,
        weekly_map["risk_focus"]: risk_focus,
        weekly_map["suggestions"]: next_actions,
        weekly_map["brief"]: brief,
    }
    return {key: value for key, value in payload.items() if value is not None}, brief


def find_existing_record(rows: list[dict[str, Any]], start_day: date, end_day: date, weekly_map: dict[str, str]) -> dict[str, Any] | None:
    for row in rows:
        row_start = local_date_key(row["fields"].get(weekly_map["start"]))
        row_end = local_date_key(row["fields"].get(weekly_map["end"]))
        if row_start == start_day.isoformat() and row_end == end_day.isoformat():
            return row
    return None


def all_source_dates(nutrition_by_date: dict[str, Any], sleep_by_date: dict[str, Any], exercise_by_date: dict[str, Any]) -> list[date]:
    return sorted({date.fromisoformat(d) for d in set(nutrition_by_date) | set(sleep_by_date) | set(exercise_by_date)})


def full_weeks(source_dates: list[date]) -> list[tuple[date, date]]:
    if not source_dates:
        return []
    first = source_dates[0]
    first_monday = first + timedelta(days=(7 - first.weekday()) % 7) if first.weekday() != 0 else first
    last_sunday = last_completed_sunday(source_dates[-1])
    windows = []
    cursor = first_monday
    while cursor + timedelta(days=6) <= last_sunday:
        windows.append((cursor, cursor + timedelta(days=6)))
        cursor += timedelta(days=7)
    return windows


def store_week(config: dict[str, Any], identity: str, start_day: date, end_day: date, nutrition_by_date: dict[str, dict[str, Any]], sleep_by_date: dict[str, list[dict[str, Any]]], exercise_by_date: dict[str, list[dict[str, Any]]], nutrition_map: dict[str, str], sleep_map: dict[str, str], exercise_map: dict[str, str], weekly_map: dict[str, str], thresholds: dict[str, float], target_rows: list[dict[str, Any]], copy: dict[str, str]) -> tuple[dict[str, Any] | None, str]:
    profiles = build_profiles(start_day, end_day, nutrition_by_date, sleep_by_date, exercise_by_date, nutrition_map, sleep_map, exercise_map, thresholds)
    if not any(p["nutrition_present"] or p["sleep_present"] or p["workout_present"] for p in profiles):
        return None, "NO_REPLY"
    payload, brief = build_payload(start_day, end_day, profiles, weekly_map, thresholds, copy)
    weekly_table = get_table(config, "weekly_health_assessment")
    weekly_ref = weekly_table.get("table_id") or weekly_table["name"]
    base_token = config["feishu"]["active_base"]["token"]
    existing = find_existing_record(target_rows, start_day, end_day, weekly_map)
    response = upsert_record(base_token, weekly_ref, identity, payload, existing["record_id"] if existing else None)
    record_id = (
        response.get("data", {}).get("record", {}).get("record_id")
        or response.get("data", {}).get("record_id")
        or response.get("data", {}).get("record_id_list", [None])[0]
        or (existing["record_id"] if existing else None)
    )
    return {
        "week_start": start_day.isoformat(),
        "week_end": end_day.isoformat(),
        "record_id": record_id,
        "action": "updated" if existing else "created",
    }, brief


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    thresholds = load_buckets(config)
    nutrition_by_date, sleep_by_date, exercise_by_date, nutrition_map, sleep_map, exercise_map = build_context(config, args.identity)
    weekly_table = get_table(config, "weekly_health_assessment")
    weekly_ref = weekly_table.get("table_id") or weekly_table["name"]
    base_token = config["feishu"]["active_base"]["token"]
    target_rows, target_fields = list_records(base_token, weekly_ref, args.identity)
    weekly_map = resolve_fields(config, "weekly_health_assessment", WEEKLY, target_fields)
    weekly_copy = get_weekly_copy(config)

    if args.backfill_full_weeks:
        results = []
        for start_day, end_day in full_weeks(all_source_dates(nutrition_by_date, sleep_by_date, exercise_by_date)):
            meta, _ = store_week(config, args.identity, start_day, end_day, nutrition_by_date, sleep_by_date, exercise_by_date, nutrition_map, sleep_map, exercise_map, weekly_map, thresholds, target_rows, weekly_copy)
            if meta:
                results.append(meta)
        print(json.dumps({"ok": True, "count": len(results), "weeks": results}, ensure_ascii=False, indent=2))
        return

    reference_day = date.fromisoformat(args.week_end) if args.week_end else datetime.now(TIMEZONE).date()
    week_end = reference_day
    week_start = monday_start(week_end)
    meta, brief = store_week(config, args.identity, week_start, week_end, nutrition_by_date, sleep_by_date, exercise_by_date, nutrition_map, sleep_map, exercise_map, weekly_map, thresholds, target_rows, weekly_copy)
    if args.json:
        print(json.dumps({
            "ok": brief != "NO_REPLY",
            "week_start": week_start.isoformat(),
            "week_end": week_end.isoformat(),
            "stored": meta,
            "report": brief,
        }, ensure_ascii=False, indent=2))
    else:
        print(brief)


if __name__ == "__main__":
    main()
