#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from config_loader import get_field_aliases, get_schema_field_names, get_table, load_config

TIMEZONE = ZoneInfo("Asia/Hong_Kong")

NUTRITION = {
    "date": ["Date"],
    "conclusion": ["Daily Conclusion"],
    "calories": ["Total Calories (kcal)"],
    "calories_ref": ["Reference Calories (kcal)"],
    "protein": ["Total Protein (g)"],
    "protein_ref": ["Reference Protein (g)"],
    "sodium": ["Total Sodium (mg)"],
    "sodium_ref": ["Reference Sodium (mg)"],
    "fiber": ["Total Fiber (g)"],
    "fiber_ref": ["Reference Fiber (g)"],
}

SLEEP = {
    "date": ["Date"],
    "score": ["Sleep Score"],
    "recovery": ["Recovery State"],
    "fatigue": ["Fatigue Risk"],
    "summary": ["One-Line Summary"],
}

EXERCISE = {
    "date": ["Logged At"],
    "type": ["Workout Type"],
    "duration": ["Duration Minutes"],
    "calories": ["Calories (kcal)"],
    "load": ["Load"],
}

MONTHLY = {
    "date": ["Date"],
    "month": ["Month Key"],
    "range": ["Month Range"],
    "overall": ["Overall Health Status"],
    "nutrition_status": ["Nutrition Status"],
    "calorie_ratio": ["Calories Achievement (%)"],
    "protein_ratio": ["Protein Achievement (%)"],
    "sodium_ratio": ["Sodium vs Reference (%)"],
    "nutrition_summary": ["Nutrition Summary"],
    "sleep_score": ["Sleep Score"],
    "recovery": ["Recovery State"],
    "fatigue": ["Fatigue Risk"],
    "sleep_summary": ["Sleep Summary"],
    "workout_count": ["Workout Count"],
    "workout_minutes": ["Workout Minutes"],
    "workout_calories": ["Workout Calories (kcal)"],
    "workout_status": ["Workout Status"],
    "workout_summary": ["Workout Summary"],
    "overview": ["Daily Overview"],
}

ENUMS = {
    "missing": ["Missing"],
    "high": ["High"],
    "low": ["Low"],
    "on_target": ["On Target"],
    "rest": ["Rest"],
    "light": ["Light"],
    "medium": ["Medium"],
    "high_load": ["High Load"],
    "alert": ["Alert"],
    "attention": ["Attention"],
    "stable": ["Stable"],
    "current_month": ["Current Month"],
    "history": ["History"],
}

MONTHLY_COPY = {
    "workout_no_records": "No workout records.",
    "workout_fallback_type": "Workout",
    "workout_summary": "{types} | {sessions} sessions, {minutes} min, {kcal} kcal",
    "overview_nutrition": "Nutrition {nutrition_status}",
    "overview_sleep": "Sleep: {sleep_summary}",
    "overview_workout": "Workout: {workout_summary}",
    "overview_nutrition_note": "Nutrition note: {nutrition_summary}",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rebuild monthly health calendar rows.")
    parser.add_argument("config", help="Path to config JSON")
    parser.add_argument("--start-date")
    parser.add_argument("--end-date")
    parser.add_argument("--identity", default="user", choices=["user", "bot"])
    parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    return parser.parse_args()


def get_monthly_copy(config: dict[str, Any]) -> dict[str, str]:
    copy = dict(MONTHLY_COPY)
    source = ((config.get("copy") or {}).get("monthly_health_calendar") or {})
    for key in MONTHLY_COPY:
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


def enum_value(logical_key: str, monthly_fields: dict[str, str]) -> str:
    field_name = monthly_fields.get("overall")
    is_chinese = field_name == "健康关注度"
    choices = ENUMS[logical_key]
    return choices[1] if is_chinese and len(choices) > 1 else choices[0]


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


def midnight_string(date_key: str) -> str:
    return f"{date_key} 00:00:00"


def to_number(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except Exception:
        return None


def ratio_percent(actual: Any, reference: Any) -> float | None:
    actual_num = to_number(actual)
    reference_num = to_number(reference)
    if actual_num is None or reference_num in (None, 0):
        return None
    return round(actual_num / reference_num * 100, 1)


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


def classify_nutrition_status(nutrition_fields: dict[str, Any], nutrition_map: dict[str, str], monthly_map: dict[str, str]) -> str:
    if not nutrition_fields:
        return enum_value("missing", monthly_map)
    calorie_ratio = ratio_percent(nutrition_fields.get(nutrition_map["calories"]), nutrition_fields.get(nutrition_map["calories_ref"]))
    protein_ratio = ratio_percent(nutrition_fields.get(nutrition_map["protein"]), nutrition_fields.get(nutrition_map["protein_ref"]))
    sodium_ratio = ratio_percent(nutrition_fields.get(nutrition_map["sodium"]), nutrition_fields.get(nutrition_map["sodium_ref"]))
    if sodium_ratio is not None and sodium_ratio > 130:
        return enum_value("high", monthly_map)
    if calorie_ratio is not None and calorie_ratio > 125:
        return enum_value("high", monthly_map)
    if calorie_ratio is not None and calorie_ratio < 75:
        return enum_value("low", monthly_map)
    if protein_ratio is not None and protein_ratio < 80:
        return enum_value("low", monthly_map)
    return enum_value("on_target", monthly_map)


def summarize_exercise(rows: list[dict[str, Any]], exercise_map: dict[str, str], monthly_map: dict[str, str], copy: dict[str, str]) -> dict[str, Any]:
    if not rows:
        return {
            monthly_map["workout_count"]: 0,
            monthly_map["workout_minutes"]: 0,
            monthly_map["workout_calories"]: 0,
            monthly_map["workout_status"]: enum_value("rest", monthly_map),
            monthly_map["workout_summary"]: copy["workout_no_records"],
        }

    total_minutes = 0.0
    total_kcal = 0.0
    load_counts = {"Light": 0, "Medium": 0, "High": 0}
    workout_types: list[str] = []

    for row in rows:
        fields = row["fields"]
        total_minutes += to_number(fields.get(exercise_map["duration"])) or 0.0
        total_kcal += to_number(fields.get(exercise_map["calories"])) or 0.0
        load_raw = str(fields.get(exercise_map["load"]) or "").strip()
        if load_raw in load_counts:
            load_counts[load_raw] += 1
        elif load_raw:
            load_counts["High" if to_number(load_raw) and to_number(load_raw) >= 7 else "Medium" if to_number(load_raw) and to_number(load_raw) >= 4 else "Light"] += 1
        workout_type = str(fields.get(exercise_map["type"]) or "").strip()
        if workout_type and workout_type not in workout_types:
            workout_types.append(workout_type)

    if load_counts["High"] > 0 or total_minutes >= 90:
        status = enum_value("high_load", monthly_map)
    elif load_counts["Medium"] > 0 or total_minutes >= 45:
        status = enum_value("medium", monthly_map)
    else:
        status = enum_value("light", monthly_map)

    summary = copy["workout_summary"].format(
        types=", ".join(workout_types) if workout_types else copy["workout_fallback_type"],
        sessions=len(rows),
        minutes=round(total_minutes),
        kcal=round(total_kcal),
    )
    return {
        monthly_map["workout_count"]: len(rows),
        monthly_map["workout_minutes"]: round(total_minutes, 1),
        monthly_map["workout_calories"]: round(total_kcal, 1),
        monthly_map["workout_status"]: status,
        monthly_map["workout_summary"]: summary,
    }


def classify_overall_status(nutrition_status: str, recovery_state: str | None, fatigue_risk: str | None, workout_status: str, monthly_map: dict[str, str]) -> str:
    poor_states = {"Poor"}
    weak_states = {"Weak"}
    high_fatigue = {"High"}
    medium_to_high_fatigue = {"Medium to High"}
    if recovery_state in poor_states or fatigue_risk in high_fatigue:
        return enum_value("alert", monthly_map)
    if nutrition_status in {enum_value("low", monthly_map), enum_value("high", monthly_map)} or recovery_state in weak_states or fatigue_risk in medium_to_high_fatigue or workout_status == enum_value("high_load", monthly_map):
        return enum_value("attention", monthly_map)
    return enum_value("stable", monthly_map)


def build_overview(nutrition_status: str, nutrition_summary: str | None, sleep_summary: str | None, workout_summary: str | None, copy: dict[str, str]) -> str:
    parts = [copy["overview_nutrition"].format(nutrition_status=nutrition_status)]
    if sleep_summary:
        parts.append(copy["overview_sleep"].format(sleep_summary=sleep_summary))
    if workout_summary:
        parts.append(copy["overview_workout"].format(workout_summary=workout_summary))
    if nutrition_summary:
        parts.append(copy["overview_nutrition_note"].format(nutrition_summary=nutrition_summary))
    return " | ".join(parts)


def pick_existing_monthly(target_rows: list[dict[str, Any]], date_key: str, monthly_map: dict[str, str]) -> dict[str, Any] | None:
    matches = [row for row in target_rows if local_date_key(row["fields"].get(monthly_map["date"])) == date_key]
    if not matches:
        return None
    return max(matches, key=lambda row: (sum(1 for value in row["fields"].values() if value not in (None, "", [])), row["record_id"] or ""))


def build_summary_rows(config: dict[str, Any], identity: str, start_date: str | None, end_date: str | None) -> list[tuple[str, dict[str, Any]]]:
    base_token = config["feishu"]["active_base"]["token"]
    nutrition_table = get_table(config, "nutrition_daily_history")
    sleep_table = get_table(config, "sleep_recovery")
    exercise_table = get_table(config, "exercise_workout")

    nutrition_rows, nutrition_fields = list_records(base_token, nutrition_table.get("table_id") or nutrition_table["name"], identity)
    sleep_rows, sleep_fields = list_records(base_token, sleep_table.get("table_id") or sleep_table["name"], identity)
    exercise_rows, exercise_fields = list_records(base_token, exercise_table.get("table_id") or exercise_table["name"], identity)
    monthly_table = get_table(config, "monthly_health_calendar")
    _, monthly_fields_available = list_records(base_token, monthly_table.get("table_id") or monthly_table["name"], identity)

    nutrition_map = resolve_fields(config, "nutrition_daily_history", NUTRITION, nutrition_fields)
    sleep_map = resolve_fields(config, "sleep_recovery", SLEEP, sleep_fields)
    exercise_map = resolve_fields(config, "exercise_workout", EXERCISE, exercise_fields)
    monthly_map = resolve_fields(config, "monthly_health_calendar", MONTHLY, monthly_fields_available)
    monthly_copy = get_monthly_copy(config)

    nutrition_by_date: dict[str, dict[str, Any]] = {}
    for row in nutrition_rows:
        date_key = local_date_key(row["fields"].get(nutrition_map["date"]))
        if date_key:
            nutrition_by_date[date_key] = row["fields"]

    sleep_grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in sleep_rows:
        date_key = local_date_key(row["fields"].get(sleep_map["date"]))
        if date_key:
            sleep_grouped[date_key].append(row)

    exercise_grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in exercise_rows:
        date_key = local_date_key(row["fields"].get(exercise_map["date"]))
        if date_key:
            exercise_grouped[date_key].append(row)

    date_keys = set(nutrition_by_date) | set(sleep_grouped) | set(exercise_grouped)
    if start_date:
        date_keys = {date_key for date_key in date_keys if date_key >= start_date}
    if end_date:
        date_keys = {date_key for date_key in date_keys if date_key <= end_date}

    current_month = datetime.now(TIMEZONE).strftime("%Y-%m")
    rows: list[tuple[str, dict[str, Any]]] = []

    for date_key in sorted(date_keys):
        nutrition_fields = nutrition_by_date.get(date_key, {})
        sleep_record = choose_latest(sleep_grouped.get(date_key, []), sleep_map["date"])
        sleep_fields = sleep_record["fields"] if sleep_record else {}
        workout_fields = summarize_exercise(exercise_grouped.get(date_key, []), exercise_map, monthly_map, monthly_copy)

        nutrition_status = classify_nutrition_status(nutrition_fields, nutrition_map, monthly_map)
        overall_status = classify_overall_status(
            nutrition_status,
            str(sleep_fields.get(sleep_map["recovery"]) or "") or None,
            str(sleep_fields.get(sleep_map["fatigue"]) or "") or None,
            workout_fields[monthly_map["workout_status"]],
            monthly_map,
        )

        nutrition_summary = nutrition_fields.get(nutrition_map["conclusion"]) or None
        sleep_summary = sleep_fields.get(sleep_map["summary"]) or None
        workout_summary = workout_fields[monthly_map["workout_summary"]]
        row = {
            monthly_map["date"]: midnight_string(date_key),
            monthly_map["month"]: date_key[:7],
            monthly_map["range"]: enum_value("current_month", monthly_map) if date_key[:7] == current_month else enum_value("history", monthly_map),
            monthly_map["overall"]: overall_status,
            monthly_map["nutrition_status"]: nutrition_status,
            monthly_map["calorie_ratio"]: ratio_percent(nutrition_fields.get(nutrition_map["calories"]), nutrition_fields.get(nutrition_map["calories_ref"])),
            monthly_map["protein_ratio"]: ratio_percent(nutrition_fields.get(nutrition_map["protein"]), nutrition_fields.get(nutrition_map["protein_ref"])),
            monthly_map["sodium_ratio"]: ratio_percent(nutrition_fields.get(nutrition_map["sodium"]), nutrition_fields.get(nutrition_map["sodium_ref"])),
            monthly_map["nutrition_summary"]: nutrition_summary,
            monthly_map["sleep_score"]: to_number(sleep_fields.get(sleep_map["score"])),
            monthly_map["recovery"]: sleep_fields.get(sleep_map["recovery"]) or None,
            monthly_map["fatigue"]: sleep_fields.get(sleep_map["fatigue"]) or None,
            monthly_map["sleep_summary"]: sleep_summary,
            monthly_map["overview"]: build_overview(nutrition_status, nutrition_summary, sleep_summary, workout_summary, monthly_copy),
            **workout_fields,
        }
        rows.append((date_key, {key: value for key, value in row.items() if value is not None}))

    return rows


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    base_token = config["feishu"]["active_base"]["token"]
    monthly_table = get_table(config, "monthly_health_calendar")
    monthly_ref = monthly_table.get("table_id") or monthly_table["name"]
    target_rows, target_fields = list_records(base_token, monthly_ref, args.identity)
    monthly_map = resolve_fields(config, "monthly_health_calendar", MONTHLY, target_fields)

    summary_rows = build_summary_rows(config, args.identity, args.start_date, args.end_date)

    results = []
    for date_key, payload in summary_rows:
        existing = pick_existing_monthly(target_rows, date_key, monthly_map)
        response = upsert_record(base_token, monthly_ref, args.identity, payload, existing["record_id"] if existing else None)
        record_id = (
            response.get("data", {}).get("record", {}).get("record_id")
            or response.get("data", {}).get("record_id")
            or response.get("data", {}).get("record_id_list", [None])[0]
            or (existing["record_id"] if existing else None)
        )
        results.append({
            "date": date_key,
            "action": "updated" if existing else "created",
            "record_id": record_id,
        })

    result = {
        "ok": True,
        "target_table": monthly_ref,
        "count": len(results),
        "updated_dates": results,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
