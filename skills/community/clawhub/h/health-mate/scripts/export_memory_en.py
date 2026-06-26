#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render a normalized English memory mirror from existing markdown files."""

import os
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.resolve()
DEFAULT_SOURCE_DIR = PROJECT_ROOT / "memory"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "memory_en"

os.environ.setdefault("MEMORY_DIR", str(DEFAULT_SOURCE_DIR))
sys.path.insert(0, str(SCRIPT_DIR))

from daily_report_pro import load_user_config, parse_memory_file  # noqa: E402


MEAL_LABELS = {
    "breakfast": "Breakfast",
    "lunch": "Lunch",
    "dinner": "Dinner",
    "snack": "Snack",
}
WATER_LABELS = {
    "wake_up": "Wake-up",
    "morning": "Morning",
    "noon": "Noon",
    "afternoon": "Afternoon",
    "evening": "Evening",
}
EXERCISE_LABELS = {
    "cycling": "Cycling",
    "walking": "Walking",
    "running": "Running",
    "workout": "Workout",
    "yoga": "Yoga",
    "swimming": "Swimming",
    "other": "Exercise",
}
SKIP_MEAL_PATTERNS = (
    "营养成分表",
    "营养估算",
    "能量",
    "钠",
    "热量",
    "蛋白质",
    "脂肪",
    "碳水",
    "膳食纤维",
)
SYMPTOM_NOISE_PATTERNS = (
    "全天步数",
    "加餐",
    "蛋白质：",
    "脂肪：",
    "碳水：",
    "膳食纤维：",
    "骑行：",
    "步数：",
    "今日运动总量",
    "运动汇总",
    "总消耗",
    "评估：",
    "当前状态",
    "症状持续时长",
    "可能缓解因素",
    "今日严格低脂饮食",
    "膳食纤维达标",
    "胆汁",
    "少量多餐",
    "无不适感",
    "症状已完全缓解",
    "已恢复",
)


def normalize_punctuation(text):
    replacements = {
        "（": "(",
        "）": ")",
        "，": ", ",
        "：": ": ",
        "→": "->",
        "×": "x",
        "～": "-",
        "。": ".",
    }
    normalized = str(text or "")
    for src, dst in replacements.items():
        normalized = normalized.replace(src, dst)
    return re.sub(r"\s+", " ", normalized).strip()


def extract_grams(text, default=None):
    match = re.search(r"(\d+(?:\.\d+)?)\s*g", normalize_punctuation(text), re.IGNORECASE)
    if match:
        return int(round(float(match.group(1))))
    return default


def approx_heading_time(time_value):
    return f" (around {time_value})" if time_value else ""


def calc_bmi(weight_kg, height_cm):
    if not weight_kg or not height_cm:
        return None
    meters = height_cm / 100
    if meters <= 0:
        return None
    return weight_kg / (meters * meters)


def add_line(block, line=""):
    block.append(line.rstrip())


def contains_cjk(text):
    return bool(re.search(r"[\u4e00-\u9fff]", str(text or "")))


def translate_medication_line(text):
    line = normalize_punctuation(text)
    line = line.replace("胆舒胶囊", "Danshu Capsule")
    line = line.replace("早餐后", "after breakfast")
    line = line.replace("午餐后", "after lunch")
    line = line.replace("晚餐后", "after dinner")
    line = line.replace("已服用", "taken")
    line = line.replace("进度", "Progress")
    line = re.sub(r"(\d+)\s*粒", r"\1 capsule", line)
    line = re.sub(r"x\s*(\d+)\s*次", r" x\1 doses", line)
    line = re.sub(r"第\s*(\d+)\s*天\s*/\s*共\s*(\d+)\s*天", r"Day \1 of \2", line)
    line = line.replace("capsulex", "capsule x")
    line = re.sub(r"capsule\(", "capsule (", line)
    line = re.sub(r"doses\(", "doses (", line)
    line = line.replace("✅", "").strip()
    return re.sub(r"\s+", " ", line).strip()


def translate_symptom_lines(raw_lines):
    cleaned = []
    for item in raw_lines or []:
        line = normalize_punctuation(item)
        if not line or line in {"--", "无记录", "无不适症状", "无不适感"}:
            continue
        if any(pattern in line for pattern in SYMPTOM_NOISE_PATTERNS):
            continue
        cleaned.append(line)

    if not cleaned:
        return ["No symptoms recorded."]

    translated = []
    for line in cleaned:
        updated = line
        replacements = [
            ("昨晚遗留", "From last night"),
            ("昨晚", "Last night"),
            ("当前状态", "Current status"),
            ("当前", "Current status"),
            ("进食后右上腹隐痛", "post-meal right upper abdominal dull pain"),
            ("进食后右上腹痛", "post-meal right upper abdominal pain"),
            ("进食后右上腹不适", "post-meal right upper abdominal discomfort"),
            ("进食后右上腹胀", "post-meal right upper abdominal bloating"),
            ("右上腹隐痛", "right upper abdominal dull pain"),
            ("右上腹痛", "right upper abdominal pain"),
            ("右上腹不适", "right upper abdominal discomfort"),
            ("右上腹胀痛", "right upper abdominal bloating and pain"),
            ("右上腹胀", "right upper abdominal bloating"),
            ("右上腹胀痛已恢复", "Right upper abdominal bloating and pain have resolved."),
            ("症状已完全缓解", "symptoms fully resolved"),
            ("无不适感", "No discomfort at present."),
            ("待评估", "pending evaluation"),
            ("症状持续时长", "Duration"),
            ("可能缓解因素", "Possible relieving factors"),
            ("持续数小时", "lasting several hours"),
            ("持续", "lasting"),
            ("数小时", "several hours"),
            ("严格低脂饮食", "strict low-fat meals"),
            ("膳食纤维达标", "fiber target was met"),
            ("饮水", "hydration"),
            ("骑行运动", "cycling"),
            ("少量多餐", "smaller, more frequent meals"),
        ]
        for src, dst in replacements:
            updated = updated.replace(src, dst)
        if contains_cjk(updated):
            if "右上腹" in line:
                updated = "Right upper abdominal discomfort was recorded in the source note."
            elif "腹胀" in line or "腹痛" in line:
                updated = "Abdominal bloating or pain was recorded in the source note."
            else:
                updated = "A symptom-related note was recorded in the source memory."
        translated.append(updated)
    return translated


def direct_food_label(source):
    line = normalize_punctuation(source)
    simple_patterns = [
        (r"鸡蛋(?:蛋白|白)\s*(\d+)\s*个", lambda m: f"egg white ({int(m.group(1)) * 30}g)"),
        (r"蛋白\s*[xX]?\s*(\d+)", lambda m: f"egg white ({int(m.group(1)) * 30}g)"),
        (r"脱脂牛奶\s*(\d+)\s*ml", lambda m: f"skim milk {m.group(1)}ml"),
        (r"安佳脱脂纯牛奶\s*(\d+)\s*ml", lambda m: f"skim milk {m.group(1)}ml"),
        (r"燕麦(?:片)?\s*\(.*?(\d+)\s*g.*?\)", lambda m: f"oatmeal ({m.group(1)}g)"),
        (r"半个糯玉米\s*\(.*?(\d+)\s*g.*?\)", lambda m: f"glutinous corn ({m.group(1)}g)"),
        (r"糯玉米\s*\d+\s*个\s*\(.*?(\d+)\s*g.*?\)", lambda m: f"glutinous corn ({m.group(1)}g)"),
        (r"半碗米饭.*?(\d+)\s*g", lambda m: f"rice ({m.group(1)}g)"),
        (r"耙耙柑.*?(\d+)\s*g", lambda m: f"ponkan orange ({m.group(1)}g)"),
        (r"苹果.*?(\d+)\s*g", lambda m: f"apple ({m.group(1)}g)"),
        (r"香蕉.*?(\d+)\s*g", lambda m: f"banana ({m.group(1)}g)"),
        (r"卤豆干.*?(\d+)\s*g", lambda m: f"braised dried tofu ({m.group(1)}g)"),
        (r"卤牛肉.*?(\d+)\s*g", lambda m: f"braised beef ({m.group(1)}g)"),
        (r"清汤炖鸡肉.*?(\d+)\s*g", lambda m: f"skinless chicken ({m.group(1)}g)"),
        (r"清炖鸡肉.*?(\d+)\s*g", lambda m: f"skinless chicken ({m.group(1)}g)"),
        (r"去皮卤鸡腿.*?(\d+)\s*g", lambda m: f"skinless braised chicken leg ({m.group(1)}g)"),
        (r"炒青菜.*?(\d+)\s*g", lambda m: f"bok choy ({m.group(1)}g)"),
        (r"青菜.*?(\d+)\s*g", lambda m: f"bok choy ({m.group(1)}g)"),
        (r"炒莴笋.*?(\d+)\s*g", lambda m: f"celtuce ({m.group(1)}g)"),
        (r"炒土豆丝.*?(\d+)\s*g", lambda m: f"potato shreds ({m.group(1)}g)"),
        (r"土豆丝.*?(\d+)\s*g", lambda m: f"potato shreds ({m.group(1)}g)"),
        (r"老面馒头.*?(\d+)\s*g", lambda m: f"steamed bun ({m.group(1)}g)"),
        (r"一个馒头.*?(\d+)\s*g", lambda m: f"steamed bun ({m.group(1)}g)"),
    ]
    for pattern, builder in simple_patterns:
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            return builder(match)
    return None


def expand_complex_foods(source):
    line = normalize_punctuation(source)
    if "青菜豆腐肉片汤" in line:
        return ["bok choy (150g)", "tofu (100g)", "lean meat (30g)", "clear broth"]
    if "豆腐肉片汤" in line:
        return ["tofu (100g)", "lean meat (50g)", "clear broth"]
    if "青菜肉片汤" in line:
        return ["bok choy (150g)", "lean meat (50g)", "clear broth"]
    if "青菜牛肉汤" in line:
        return ["bok choy (100g)", "lean beef (50g)", "clear broth"]
    if "排骨炖藕" in line:
        meat_grams = 60 if "瘦肉" in line else 40
        return [f"lotus root (150g)", f"lean meat ({meat_grams}g)", "clear broth"]
    if "清汤牛肉面" in line:
        noodles = 150 if "150g" in line else 100
        return [f"noodles ({noodles}g)", "lean beef (50g)", "bok choy (50g)", "clear broth"]
    if "牛肉米线" in line:
        return ["rice noodles (250g)", "lean beef (70g)", "clear broth"]
    if "彩椒鸡胸双蛋白热烹沙拉" in line:
        return ["chicken breast (150g)", "egg white (60g)", "bok choy (150g)"]
    return None


def translate_food_entries(source, calories):
    line = normalize_punctuation(source)
    if not line or any(pattern in line for pattern in SKIP_MEAL_PATTERNS):
        return []

    expanded = expand_complex_foods(line)
    if expanded:
        return [(item, None) for item in expanded]

    label = direct_food_label(line)
    if label:
        return [(label, round(calories) if calories else None)]

    replacements = [
        ("凉拌鸡丝", "chicken breast (150g)"),
        ("凉拌鸭肉", "duck (150g)"),
        ("炒青菜", "bok choy"),
        ("青菜", "bok choy"),
        ("菠菜", "spinach"),
        ("莴笋", "celtuce"),
        ("土豆丝", "potato shreds"),
        ("卤牛肉", "braised beef"),
        ("卤豆干", "braised dried tofu"),
        ("脱脂牛奶", "skim milk"),
        ("去皮卤鸡腿", "skinless braised chicken leg"),
        ("鸡胸肉", "chicken breast"),
        ("牛肉", "lean beef"),
        ("瘦肉", "lean meat"),
        ("豆腐", "tofu"),
        ("糯玉米", "glutinous corn"),
        ("苹果", "apple"),
        ("耙耙柑", "ponkan orange"),
        ("米饭", "rice"),
        ("燕麦片", "oatmeal"),
        ("燕麦", "oatmeal"),
        ("清汤", "clear broth"),
        ("馒头", "steamed bun"),
    ]
    for src, dst in replacements:
        line = line.replace(src, dst)

    line = re.sub(r"\(约\s*(\d+)\s*g\)", r"(\1g)", line)
    line = re.sub(r"约\s*(\d+)\s*kcal.*$", "", line)
    line = line.replace("自家卤, ", "")
    line = re.sub(r"\s+", " ", line).strip(" -")

    if not line:
        return []
    if contains_cjk(line):
        grams = extract_grams(source)
        fallback = f"food item ({grams}g)" if grams else "food item"
        return [(fallback, round(calories) if calories else None)]
    return [(line, round(calories) if calories else None)]


def render_weight_section(lines, date_str, record, prev_weight, height_cm):
    add_line(lines, "## Weight Record")
    weight_kg = record.get("weight_morning")
    if weight_kg is None:
        add_line(lines, "(pending)")
        add_line(lines)
        return

    add_line(lines, f"**Morning fasting**: {weight_kg:.1f}kg")
    bmi = calc_bmi(weight_kg, height_cm)
    if bmi is not None:
        add_line(lines, f"- BMI: {bmi:.1f}")
    if prev_weight is not None:
        delta = weight_kg - prev_weight
        add_line(lines, f"- Compared with yesterday: {prev_weight:.1f}kg -> {weight_kg:.1f}kg ({delta:+.1f}kg)")
    add_line(lines)


def render_water_section(lines, record):
    add_line(lines, "## Water Record")
    water_records = record.get("water_records", [])
    if not water_records:
        add_line(lines, "(pending)")
        add_line(lines)
        return

    for item in water_records:
        period = WATER_LABELS.get(item.get("time_label"), "Water")
        add_line(lines, f"### {period}{approx_heading_time(item.get('exact_time'))}")
        add_line(lines, f"- Water intake: {int(item.get('amount_ml', 0))}ml")
        add_line(lines, f"- Cumulative: {int(item.get('cumulative_ml', 0))}ml / {int(record.get('water_target', 2000))}ml")
        add_line(lines)


def render_meal_section(lines, record):
    add_line(lines, "## Meal Record")
    meals = record.get("meals", [])
    if not meals:
        add_line(lines, "(pending)")
        add_line(lines)
        return

    for meal in meals:
        meal_title = MEAL_LABELS.get(meal.get("type"), "Meal")
        add_line(lines, f"### {meal_title}{approx_heading_time(meal.get('time'))}")
        food_items = meal.get("food_nutrition") or [{"name": name, "calories": None} for name in meal.get("foods", [])]
        rendered_any = False
        rendered_entries = []
        for item in food_items:
            for label, cal in translate_food_entries(item.get("name", ""), item.get("calories")):
                rendered_any = True
                rendered_entries.append((label, cal))
                if cal is None:
                    add_line(lines, f"- {label}")
                else:
                    add_line(lines, f"- {label} -> approx {int(round(cal))} kcal")
        if not rendered_any:
            add_line(lines, "- meal item")
        if rendered_entries:
            has_estimated_entries = any(cal is None for _, cal in rendered_entries)
            rendered_total = sum(int(round(cal)) for _, cal in rendered_entries if cal is not None)
            meal_total = int(round(meal.get("total_calories", 0))) if has_estimated_entries else rendered_total
        else:
            meal_total = int(round(meal.get("total_calories", 0)))
        add_line(lines, f"**Meal Total**: approx {meal_total} kcal")
        add_line(lines)


def render_exercise_section(lines, record):
    add_line(lines, "## Exercise Record")
    exercises = record.get("exercise_records", [])
    if not exercises:
        add_line(lines, "(pending)")
        add_line(lines)
        return

    for item in exercises:
        title = EXERCISE_LABELS.get(item.get("type"), "Exercise")
        add_line(lines, f"### {title}{approx_heading_time(item.get('time'))}")
        if item.get("distance_km"):
            add_line(lines, f"- Distance: {item['distance_km']:.2f} km")
        if item.get("duration_min"):
            add_line(lines, f"- Duration: {int(item['duration_min'])} minutes")
        if item.get("calories"):
            add_line(lines, f"- Calories: approx {int(round(item['calories']))} kcal")
        add_line(lines)


def render_symptom_section(lines, record):
    add_line(lines, "## Symptoms / Discomfort")
    for item in translate_symptom_lines(record.get("symptoms", [])):
        add_line(lines, f"- {item}")
    add_line(lines)


def render_medication_section(lines, record):
    add_line(lines, "## Medication Record")
    meds = record.get("medication_records", [])
    if not meds:
        add_line(lines, "(pending)")
        add_line(lines)
        return

    for item in meds:
        add_line(lines, f"- {translate_medication_line(item)}")
    add_line(lines)


def render_steps_section(lines, record):
    add_line(lines, "## Today Steps")
    steps = int(record.get("steps", 0) or 0)
    if steps <= 0:
        add_line(lines, "(pending)")
    else:
        add_line(lines, f"- Total steps: {steps}")
    add_line(lines)


def build_memory_en(date_str, record, prev_weight, height_cm):
    lines = [f"# {date_str} Health Log", ""]
    render_weight_section(lines, date_str, record, prev_weight, height_cm)
    render_water_section(lines, record)
    render_meal_section(lines, record)
    render_exercise_section(lines, record)
    render_symptom_section(lines, record)
    render_medication_section(lines, record)
    render_steps_section(lines, record)
    return "\n".join(lines).rstrip() + "\n"


def iter_source_files(source_dir):
    for path in sorted(source_dir.glob("*.md")):
        if re.match(r"^\d{4}-\d{2}-\d{2}\.md$", path.name):
            yield path


def main():
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
        english_memory = build_memory_en(date_str, record, prev_weight, height_cm)
        (output_dir / source_file.name).write_text(english_memory, encoding="utf-8")
        if record.get("weight_morning") is not None:
            prev_weight = record["weight_morning"]

    print(f"Generated English memory files: {len(parsed)}")
    print(f"Source: {source_dir}")
    print(f"Output: {output_dir}")


if __name__ == "__main__":
    main()
