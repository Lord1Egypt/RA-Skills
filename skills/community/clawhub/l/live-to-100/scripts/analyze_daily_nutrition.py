#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from typing import Any


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def pct(value: float, total: float) -> float:
    if total <= 0:
        return 0.0
    return value / total * 100.0


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def category_set(meals: list[dict[str, Any]]) -> set[str]:
    out: set[str] = set()
    for meal in meals:
        cats = meal.get("category", [])
        if isinstance(cats, list):
            for c in cats:
                out.add(str(c).strip().lower())
    return out


def nutrition_score(
    calorie_gap: float,
    calorie_target_gap: float,
    protein_g: float,
    protein_target_g: float,
    fiber_g: float,
    fiber_target_g: float,
    water_ml: float,
    water_target_ml: float,
    p_ratio: float,
    c_ratio: float,
    f_ratio: float,
    diversity: int,
    ultra_processed_ratio: float,
) -> float:
    score = 100.0

    # Calorie target adherence
    score -= clamp(abs(calorie_gap - calorie_target_gap) / 100.0 * 4.0, 0, 20)

    # Protein/fiber/water adequacy
    if protein_target_g > 0:
        score -= clamp((1.0 - protein_g / protein_target_g) * 25.0, 0, 15)
    if fiber_target_g > 0:
        score -= clamp((1.0 - fiber_g / fiber_target_g) * 20.0, 0, 12)
    if water_target_ml > 0:
        score -= clamp((1.0 - water_ml / water_target_ml) * 12.0, 0, 8)

    # Macro balance (rough coaching bands)
    if p_ratio < 20 or p_ratio > 40:
        score -= 8
    if c_ratio < 30 or c_ratio > 60:
        score -= 6
    if f_ratio < 20 or f_ratio > 40:
        score -= 6

    # Diversity + UPF
    if diversity < 4:
        score -= 8
    elif diversity < 5:
        score -= 4
    score -= clamp(ultra_processed_ratio * 20.0, 0, 10)

    return clamp(score, 0, 100)


def calorie_deficit_status(actual_deficit: float, target_deficit: float) -> str:
    if target_deficit <= 0:
        return "未设置缺口目标"
    if actual_deficit < target_deficit - 200:
        return "缺口不足"
    if actual_deficit > target_deficit + 250:
        return "缺口过大"
    return "达标"


def build_suggestions(
    protein_g: float,
    protein_target_g: float,
    fiber_g: float,
    fiber_target_g: float,
    water_ml: float,
    water_target_ml: float,
    upf_ratio: float,
    status: str,
) -> list[str]:
    tips: list[str] = []
    if protein_target_g > 0 and protein_g < protein_target_g:
        tips.append("明天至少加 1 份高蛋白食物（如鸡胸/鱼/豆制品/希腊酸奶），优先放在早餐或训练后。")
    if fiber_target_g > 0 and fiber_g < fiber_target_g:
        tips.append("每餐补 1 份高纤维蔬菜或全谷物，目标多增加 8-12g 膳食纤维。")
    if water_target_ml > 0 and water_ml < water_target_ml:
        tips.append("把饮水分成 6-8 次完成，上午和训练后优先补足。")
    if upf_ratio > 0.3:
        tips.append("减少超加工零食/甜饮，替换为水果、坚果或无糖酸奶。")
    if status == "缺口不足":
        tips.append("将主食或脂肪轻微下调 150-250 kcal，避免一次性大幅削减。")
    if status == "缺口过大":
        tips.append("适当回补 150-250 kcal，优先蛋白质和高纤维碳水，降低疲劳与反弹风险。")

    if not tips:
        tips.append("维持当前饮食结构，继续追踪一周并根据体重/腰围趋势微调。")
    return tips[:3]


def analyze(data: dict[str, Any]) -> str:
    meals_raw = data.get("meals", [])
    meals = meals_raw if isinstance(meals_raw, list) else []

    total_cal = sum(as_float(m.get("calories")) for m in meals)
    total_p = sum(as_float(m.get("protein_g")) for m in meals)
    total_c = sum(as_float(m.get("carbs_g")) for m in meals)
    total_f = sum(as_float(m.get("fat_g")) for m in meals)
    total_fiber = sum(as_float(m.get("fiber_g")) for m in meals)

    # Energy from macros
    kcal_from_p = total_p * 4
    kcal_from_c = total_c * 4
    kcal_from_f = total_f * 9
    macro_kcal = kcal_from_p + kcal_from_c + kcal_from_f

    p_ratio = pct(kcal_from_p, macro_kcal)
    c_ratio = pct(kcal_from_c, macro_kcal)
    f_ratio = pct(kcal_from_f, macro_kcal)

    targets = data.get("targets", {}) if isinstance(data.get("targets"), dict) else {}
    target_cal = as_float(targets.get("target_calories"), 0)
    target_deficit = as_float(targets.get("target_deficit_kcal"), 0)
    protein_target = as_float(targets.get("protein_target_g"), 0)
    fiber_target = as_float(targets.get("fiber_target_g"), 30)
    water_target = as_float(targets.get("water_target_ml"), 2500)
    water_ml = as_float((data.get("hydration") or {}).get("water_ml"), 0)

    # With target calories as maintenance minus target deficit assumption:
    # actual deficit vs target calories baseline
    actual_deficit = target_cal - total_cal if target_cal > 0 else 0
    status = calorie_deficit_status(actual_deficit, target_deficit)

    cats = category_set(meals)
    diversity = len(cats)
    upf_count = 0
    for meal in meals:
        cats_m = meal.get("category", [])
        if isinstance(cats_m, list) and any(str(c).strip().lower() == "ultra-processed" for c in cats_m):
            upf_count += 1
    upf_ratio = upf_count / len(meals) if meals else 0.0

    score = nutrition_score(
        calorie_gap=actual_deficit,
        calorie_target_gap=target_deficit,
        protein_g=total_p,
        protein_target_g=protein_target,
        fiber_g=total_fiber,
        fiber_target_g=fiber_target,
        water_ml=water_ml,
        water_target_ml=water_target,
        p_ratio=p_ratio,
        c_ratio=c_ratio,
        f_ratio=f_ratio,
        diversity=diversity,
        ultra_processed_ratio=upf_ratio,
    )

    tips = build_suggestions(
        protein_g=total_p,
        protein_target_g=protein_target,
        fiber_g=total_fiber,
        fiber_target_g=fiber_target,
        water_ml=water_ml,
        water_target_ml=water_target,
        upf_ratio=upf_ratio,
        status=status,
    )

    lines = [
        "# 每日营养分析",
        "",
        f"- 日期: {data.get('date', 'N/A')}",
        f"- 营养均衡评分: **{score:.1f}/100**",
        "",
        "## 热量与缺口",
        f"- 总热量: **{total_cal:.0f} kcal**",
        f"- 目标热量: **{target_cal:.0f} kcal**",
        f"- 相对目标热量的实际缺口/盈余: **{actual_deficit:+.0f} kcal**",
        f"- 缺口状态: **{status}**",
        "",
        "## 宏量与质量",
        f"- 蛋白质: {total_p:.1f} g（目标 {protein_target:.1f} g）",
        f"- 碳水: {total_c:.1f} g",
        f"- 脂肪: {total_f:.1f} g",
        f"- 宏量占比（按热量 P/C/F）: {p_ratio:.1f}% / {c_ratio:.1f}% / {f_ratio:.1f}%",
        f"- 膳食纤维: {total_fiber:.1f} g（目标 {fiber_target:.1f} g）",
        f"- 饮水: {water_ml:.0f} ml（目标 {water_target:.0f} ml）",
        f"- 食物类别多样性: {diversity}",
        f"- 超加工餐食占比: {upf_ratio * 100:.1f}%",
        "",
        "## 次日调整建议",
    ]
    lines.extend([f"- {tip}" for tip in tips])
    lines.append("")
    lines.append("_本输出仅用于生活方式管理，不构成医疗诊断。_")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze daily nutrition balance and calorie deficit from JSON logs.")
    parser.add_argument("--input", required=True, help="Path to daily nutrition JSON")
    parser.add_argument("--output", help="Path to output markdown (default stdout)")
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = analyze(data)
    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
