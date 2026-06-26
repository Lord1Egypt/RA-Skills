#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render a normalized Japanese memory mirror from source markdown files."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.resolve()
DEFAULT_SOURCE_DIR = PROJECT_ROOT / "memory"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "memory_jp"

os.environ.setdefault("MEMORY_DIR", str(DEFAULT_SOURCE_DIR))
sys.path.insert(0, str(SCRIPT_DIR))

from daily_report_pro import load_user_config, parse_memory_file  # noqa: E402
from export_memory_en import add_line, calc_bmi, iter_source_files  # noqa: E402
from i18n import exercise_name, localize_free_text, meal_name, water_period_name  # noqa: E402


FOOD_REPLACEMENTS = {
    "鸡蛋蛋白": "卵白",
    "鸡蛋白": "卵白",
    "糯玉米": "もちとうもろこし",
    "脱脂牛奶": "無脂肪牛乳",
    "去皮卤鸡腿": "皮なし鶏もも肉",
    "卤鸡腿": "鶏もも肉",
    "卤豆干": "味付け豆腐干",
    "青菜豆腐肉片汤": "青菜・豆腐・赤身肉のスープ",
    "青菜": "青菜",
    "豆腐": "豆腐",
    "瘦肉": "赤身肉",
    "半碗米饭": "ご飯 半膳",
    "米饭": "ご飯",
    "耙耙柑": "ポンカン",
    "鸡胸肉": "鶏むね肉",
    "牛肉": "牛肉",
    "燕麦片": "オートミール",
    "燕麦": "オートミール",
    "苹果": "りんご",
    "清汤": "澄んだスープ",
}

SYMPTOM_REPLACEMENTS = {
    "右上腹隐痛": "右上腹部の鈍い痛み",
    "右上腹痛": "右上腹部痛",
    "右上腹不适": "右上腹部の違和感",
    "右上腹胀": "右上腹部の張り",
    "腹胀": "腹部膨満感",
    "腹痛": "腹痛",
    "恶心": "吐き気",
    "不适": "不調",
    "无不适感": "不調なし",
}

MEDICATION_REPLACEMENTS = {
    "胆舒胶囊": "胆舒カプセル",
    "早餐后": "朝食後",
    "午餐后": "昼食後",
    "晚餐后": "夕食後",
    "已服用": "服用済み",
    "进度": "進捗",
}


def approx_heading_time(time_value: str | None) -> str:
    return f"（約 {time_value}）" if time_value else ""


def translate_portion_units(text: str) -> str:
    updated = str(text or "")
    updated = re.sub(r"(\d+)\s*个", r"\1個", updated)
    updated = re.sub(r"半碗", "半膳", updated)
    updated = updated.replace("约", "約")
    updated = updated.replace("（", "（").replace("）", "）")
    return updated


def translate_food_label(text: str) -> str:
    updated = str(text or "").strip()
    for source, target in sorted(FOOD_REPLACEMENTS.items(), key=lambda item: len(item[0]), reverse=True):
        updated = updated.replace(source, target)
    updated = translate_portion_units(updated)
    updated = localize_free_text("ja-JP", updated)
    updated = re.sub(r"\s+", " ", updated).strip()
    return updated or "食事項目"


def translate_symptom_line(text: str) -> str:
    updated = str(text or "").strip()
    for source, target in sorted(SYMPTOM_REPLACEMENTS.items(), key=lambda item: len(item[0]), reverse=True):
        updated = updated.replace(source, target)
    updated = localize_free_text("ja-JP", updated)
    return re.sub(r"\s+", " ", updated).strip()


def translate_medication_line(text: str) -> str:
    updated = str(text or "").strip().replace("✅", "")
    for source, target in sorted(MEDICATION_REPLACEMENTS.items(), key=lambda item: len(item[0]), reverse=True):
        updated = updated.replace(source, target)
    updated = re.sub(r"(\d+)\s*粒", r"\1カプセル", updated)
    updated = re.sub(r"×\s*(\d+)\s*次", r"×\1回", updated)
    updated = re.sub(r"第\s*(\d+)\s*天\s*/\s*共\s*(\d+)\s*天", r"\1日目 / 全\2日", updated)
    updated = translate_portion_units(updated)
    updated = localize_free_text("ja-JP", updated)
    return re.sub(r"\s+", " ", updated).strip()


def render_weight_section(lines: list[str], record: dict, prev_weight: float | None, height_cm: float | None) -> None:
    add_line(lines, "## 体重記録")
    weight_kg = record.get("weight_morning")
    if weight_kg is None:
        add_line(lines, "（待記録）")
        add_line(lines)
        return

    add_line(lines, f"**朝の空腹時**：{weight_kg:.1f}kg")
    bmi = calc_bmi(weight_kg, height_cm)
    if bmi is not None:
        add_line(lines, f"- BMI：{bmi:.1f}")
    if prev_weight is not None:
        delta = weight_kg - prev_weight
        add_line(lines, f"- 前日比：{prev_weight:.1f}kg → {weight_kg:.1f}kg ({delta:+.1f}kg)")
    add_line(lines)


def render_water_section(lines: list[str], record: dict) -> None:
    add_line(lines, "## 飲水記録")
    water_records = record.get("water_records", [])
    if not water_records:
        add_line(lines, "（待記録）")
        add_line(lines)
        return

    target = int(record.get("water_target", 2000) or 2000)
    for item in water_records:
        label = water_period_name("ja-JP", item.get("time_label"))
        add_line(lines, f"### {label}{approx_heading_time(item.get('exact_time'))}")
        add_line(lines, f"- 飲水量：{int(item.get('amount_ml', 0) or 0)}ml")
        add_line(lines, f"- 累計：{int(item.get('cumulative_ml', 0) or 0)}ml/{target}ml")
        add_line(lines)


def render_meal_section(lines: list[str], record: dict) -> None:
    add_line(lines, "## 食事記録")
    meals = record.get("meals", [])
    if not meals:
        add_line(lines, "（待記録）")
        add_line(lines)
        return

    for meal in meals:
        title = meal_name("ja-JP", meal.get("type"))
        add_line(lines, f"### {title}{approx_heading_time(meal.get('time'))}")
        food_items = meal.get("food_nutrition") or [{"name": name, "calories": None} for name in meal.get("foods", [])]
        for item in food_items:
            label = translate_food_label(item.get("name", ""))
            calories = item.get("calories")
            if calories is None:
                add_line(lines, f"- {label}")
            else:
                add_line(lines, f"- {label} → 約 {int(round(calories))}kcal")
        add_line(lines, f"**食事合計**：約 {int(round(meal.get('total_calories', 0) or 0))}kcal")
        add_line(lines)


def render_exercise_section(lines: list[str], record: dict) -> None:
    add_line(lines, "## 運動記録")
    exercises = record.get("exercise_records", [])
    if not exercises:
        add_line(lines, "（待記録）")
        add_line(lines)
        return

    for item in exercises:
        title = exercise_name("ja-JP", item.get("type"))
        add_line(lines, f"### {title}{approx_heading_time(item.get('time'))}")
        if item.get("distance_km"):
            add_line(lines, f"- 距離：{item['distance_km']:.2f}km")
        if item.get("duration_min"):
            add_line(lines, f"- 時間：{int(item['duration_min'])}分")
        if item.get("calories"):
            add_line(lines, f"- 消費：約 {int(round(item['calories']))}kcal")
        add_line(lines)


def render_symptom_section(lines: list[str], record: dict) -> None:
    add_line(lines, "## 症状 / 不調")
    symptoms = [translate_symptom_line(item) for item in record.get("symptoms", []) if str(item or "").strip()]
    if not symptoms:
        add_line(lines, "（記録なし）")
        add_line(lines)
        return

    for item in symptoms:
        add_line(lines, f"- {item}")
    add_line(lines)


def render_medication_section(lines: list[str], record: dict) -> None:
    add_line(lines, "## 服薬記録")
    meds = record.get("medication_records", [])
    if not meds:
        add_line(lines, "（待記録）")
        add_line(lines)
        return

    for item in meds:
        add_line(lines, f"- {translate_medication_line(item)}")
    add_line(lines)


def render_steps_section(lines: list[str], record: dict) -> None:
    add_line(lines, "## 今日の歩数")
    steps = int(record.get("steps", 0) or 0)
    if steps <= 0:
        add_line(lines, "（待記録）")
    else:
        add_line(lines, f"- 総歩数：{steps}歩")
    add_line(lines)


def build_memory_jp(date_str: str, record: dict, prev_weight: float | None, height_cm: float | None) -> str:
    lines = [f"# {date_str} 健康記録", ""]
    render_weight_section(lines, record, prev_weight, height_cm)
    render_water_section(lines, record)
    render_meal_section(lines, record)
    render_exercise_section(lines, record)
    render_symptom_section(lines, record)
    render_medication_section(lines, record)
    render_steps_section(lines, record)
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    source_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_SOURCE_DIR.resolve()
    output_dir = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else DEFAULT_OUTPUT_DIR.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    config = load_user_config()
    height_cm = config.get("user_profile", {}).get("height_cm")

    parsed = []
    for source_file in iter_source_files(source_dir):
        parsed.append((source_file, parse_memory_file(str(source_file))))

    prev_weight = None
    for source_file, record in parsed:
        date_str = source_file.stem
        japanese_memory = build_memory_jp(date_str, record, prev_weight, height_cm)
        (output_dir / source_file.name).write_text(japanese_memory, encoding="utf-8")
        if record.get("weight_morning") is not None:
            prev_weight = record["weight_morning"]

    print(f"Generated Japanese memory files: {len(parsed)}")
    print(f"Source: {source_dir}")
    print(f"Output: {output_dir}")


if __name__ == "__main__":
    main()
