#!/usr/bin/env python3
import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ScoreResult:
    total: int
    subscores: dict[str, int]
    drivers: list[str]
    missing_fields: list[str]


def clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def get(d: dict[str, Any], path: str) -> Any:
    cur: Any = d
    for key in path.split("."):
        if not isinstance(cur, dict) or key not in cur:
            return None
        cur = cur[key]
    return cur


def to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    if isinstance(value, (int, float)):
        return value != 0
    return False


def count_status(supplements: list[dict[str, Any]], status: str) -> int:
    return sum(1 for s in supplements if str(s.get("status", "")).strip() == status)


def ensure_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def calculate_score(data: dict[str, Any]) -> ScoreResult:
    missing: list[str] = []
    contributors: list[tuple[str, int]] = []
    scores = {
        "body_composition": 0,
        "cardiometabolic": 0,
        "sleep_recovery": 0,
        "activity_sedentary": 0,
        "habits": 0,
        "medical_context": 0,
    }

    # 1) Body composition (0-20)
    weight = get(data, "profile.weight_kg")
    height_cm = get(data, "profile.height_cm")
    if isinstance(weight, (int, float)) and isinstance(height_cm, (int, float)) and height_cm > 0:
        bmi = weight / ((height_cm / 100) ** 2)
        if bmi < 18.5 or bmi >= 32:
            scores["body_composition"] += 8
        elif bmi >= 28:
            scores["body_composition"] += 6
        elif bmi >= 25:
            scores["body_composition"] += 3
    else:
        scores["body_composition"] += 4
        missing.extend(["profile.weight_kg", "profile.height_cm"])

    waist = get(data, "profile.waist_cm")
    sex = str(get(data, "profile.sex") or "").lower()
    if isinstance(waist, (int, float)):
        if sex in {"male", "m"}:
            scores["body_composition"] += 8 if waist >= 102 else (4 if waist >= 94 else 0)
        elif sex in {"female", "f"}:
            scores["body_composition"] += 8 if waist >= 88 else (4 if waist >= 80 else 0)
        else:
            scores["body_composition"] += 2
            missing.append("profile.sex")
    else:
        scores["body_composition"] += 4
        missing.append("profile.waist_cm")

    if isinstance(get(data, "profile.rapid_weight_gain_pct_6m"), (int, float)):
        if float(get(data, "profile.rapid_weight_gain_pct_6m")) > 5:
            scores["body_composition"] += 4

    scores["body_composition"] = clamp(scores["body_composition"], 0, 20)
    contributors.append(("体成分", scores["body_composition"]))

    # 2) Cardiometabolic (0-25)
    sys = get(data, "vitals.systolic")
    dia = get(data, "vitals.diastolic")
    if isinstance(sys, (int, float)) and isinstance(dia, (int, float)):
        if sys >= 140 or dia >= 90:
            scores["cardiometabolic"] += 10
        elif sys >= 130 or dia >= 80:
            scores["cardiometabolic"] += 6
    else:
        scores["cardiometabolic"] += 5
        missing.extend(["vitals.systolic", "vitals.diastolic"])

    rhr = get(data, "vitals.resting_hr")
    if isinstance(rhr, (int, float)):
        scores["cardiometabolic"] += 5 if rhr > 90 else (2 if rhr >= 75 else 0)
    else:
        scores["cardiometabolic"] += 2
        missing.append("vitals.resting_hr")

    hba1c = get(data, "vitals.hba1c")
    if isinstance(hba1c, (int, float)):
        scores["cardiometabolic"] += 6 if hba1c >= 6.5 else (3 if hba1c >= 5.7 else 0)
    else:
        fg = get(data, "vitals.fasting_glucose")
        if isinstance(fg, (int, float)):
            scores["cardiometabolic"] += 6 if fg >= 126 else (3 if fg >= 100 else 0)
        else:
            scores["cardiometabolic"] += 3
            missing.extend(["vitals.hba1c", "vitals.fasting_glucose"])

    lipid_abnormality = to_bool(get(data, "vitals.lipid_abnormality"))
    if not lipid_abnormality:
        ldl = get(data, "vitals.ldl")
        hdl = get(data, "vitals.hdl")
        tg = get(data, "vitals.triglycerides")
        if isinstance(ldl, (int, float)) and ldl >= 130:
            lipid_abnormality = True
        if isinstance(hdl, (int, float)) and hdl < 40:
            lipid_abnormality = True
        if isinstance(tg, (int, float)) and tg >= 150:
            lipid_abnormality = True
    scores["cardiometabolic"] += 4 if lipid_abnormality else 0
    scores["cardiometabolic"] = clamp(scores["cardiometabolic"], 0, 25)
    contributors.append(("心代谢", scores["cardiometabolic"]))

    # 3) Sleep and recovery (0-15)
    sleep_h = get(data, "routine.sleep_hours")
    if isinstance(sleep_h, (int, float)):
        scores["sleep_recovery"] += 7 if sleep_h < 6 else (4 if sleep_h < 7 else 0)
    else:
        scores["sleep_recovery"] += 3
        missing.append("routine.sleep_hours")

    shift_h = get(data, "routine.sleep_schedule_shift_hours")
    if isinstance(shift_h, (int, float)) and shift_h > 2:
        scores["sleep_recovery"] += 4
    elif shift_h is None:
        scores["sleep_recovery"] += 2
        missing.append("routine.sleep_schedule_shift_hours")

    if to_bool(get(data, "routine.insomnia_or_daytime_fatigue")):
        scores["sleep_recovery"] += 4
    scores["sleep_recovery"] = clamp(scores["sleep_recovery"], 0, 15)
    contributors.append(("睡眠与恢复", scores["sleep_recovery"]))

    # 4) Activity and sedentary load (0-20)
    steps = get(data, "routine.steps_per_day")
    if isinstance(steps, (int, float)):
        scores["activity_sedentary"] += 8 if steps < 4000 else (4 if steps < 7000 else 0)
    else:
        scores["activity_sedentary"] += 4
        missing.append("routine.steps_per_day")

    ex_days = get(data, "routine.exercise_days_per_week")
    if isinstance(ex_days, (int, float)):
        scores["activity_sedentary"] += 6 if ex_days <= 0 else (3 if ex_days < 3 else 0)
    else:
        scores["activity_sedentary"] += 3
        missing.append("routine.exercise_days_per_week")

    sit = get(data, "routine.sitting_hours_per_day")
    if isinstance(sit, (int, float)):
        scores["activity_sedentary"] += 6 if sit > 9 else (3 if sit >= 7 else 0)
    else:
        scores["activity_sedentary"] += 3
        missing.append("routine.sitting_hours_per_day")

    scores["activity_sedentary"] = clamp(scores["activity_sedentary"], 0, 20)
    contributors.append(("活动与久坐", scores["activity_sedentary"]))

    # 5) Habits (0-10)
    if to_bool(get(data, "habits.smoking_current")):
        scores["habits"] += 5
    if to_bool(get(data, "habits.alcohol_heavy_or_binge")):
        scores["habits"] += 3
    if to_bool(get(data, "habits.late_caffeine_or_late_night_eating")):
        scores["habits"] += 2
    scores["habits"] = clamp(scores["habits"], 0, 10)
    contributors.append(("生活习惯", scores["habits"]))

    # 6) Medical context (0-10)
    chronic = get(data, "medical.chronic_disease_burden")
    if isinstance(chronic, (int, float)):
        scores["medical_context"] += 5 if chronic >= 2 else (3 if chronic == 1 else 0)
    elif to_bool(chronic):
        scores["medical_context"] += 5
    else:
        scores["medical_context"] += 2
        missing.append("medical.chronic_disease_burden")

    if to_bool(get(data, "medical.multi_med_adherence_issues")):
        scores["medical_context"] += 2
    if to_bool(get(data, "medical.strong_family_history")):
        scores["medical_context"] += 3
    scores["medical_context"] = clamp(scores["medical_context"], 0, 10)
    contributors.append(("医疗背景", scores["medical_context"]))

    total = int(sum(scores.values()))
    top = [name for name, _ in sorted(contributors, key=lambda x: x[1], reverse=True)[:3]]
    missing_unique = sorted(set(missing))
    return ScoreResult(total=total, subscores=scores, drivers=top, missing_fields=missing_unique)


def risk_band(total: int) -> str:
    if total <= 20:
        return "当前风险较低"
    if total <= 40:
        return "轻中度风险"
    if total <= 60:
        return "风险偏高"
    return "高风险"


def score_improvement_target(total: int) -> str:
    if total <= 20:
        return "维持当前水平（波动不超过 +/-3 分）"
    if total <= 40:
        return "4 周内下降 5-8 分"
    if total <= 60:
        return "4 周内下降 7-10 分"
    return "4 周内下降 10-15 分，并结合保守调整与医生随访"


def generate_markdown(data: dict[str, Any], score: ScoreResult) -> str:
    def zh_value(v: Any) -> str:
        mapping = {"N/A": "未提供", "up": "上升", "down": "下降", "flat": "持平", "high": "高", "medium": "中", "low": "低"}
        s = str(v)
        return mapping.get(s, s)

    reports = data.get("reports", {}) if isinstance(data.get("reports"), dict) else {}
    supplements = data.get("supplements", [])
    if not isinstance(supplements, list):
        supplements = []

    safe_n = count_status(supplements, "Safe to continue")
    review_n = count_status(supplements, "Needs clinician review")
    avoid_n = count_status(supplements, "Avoid for now")

    weekly_wins = ensure_list(reports.get("wins", []))
    weekly_gaps = ensure_list(reports.get("gaps", []))
    weekly_focus = ensure_list(reports.get("next_week_focus", []))
    blockers = ensure_list(reports.get("blockers", []))

    lines = [
        "# 长寿风险与自动报告",
        "",
        "## 长寿风险评分",
        f"- 总分: **{score.total}/100**（{risk_band(score.total)}）",
        f"- 4周目标: **{score_improvement_target(score.total)}**",
        "- 分项得分:",
        f"  - 体成分: {score.subscores['body_composition']}/20",
        f"  - 心代谢: {score.subscores['cardiometabolic']}/25",
        f"  - 睡眠与恢复: {score.subscores['sleep_recovery']}/15",
        f"  - 活动与久坐: {score.subscores['activity_sedentary']}/20",
        f"  - 生活习惯: {score.subscores['habits']}/10",
        f"  - 医疗背景: {score.subscores['medical_context']}/10",
        f"- 主要风险驱动: {', '.join(score.drivers)}",
    ]
    if score.missing_fields:
        lines.append(f"- 因缺失字段为暂估分: {', '.join(score.missing_fields)}")

    lines.extend(
        [
            "",
            "## 周报",
            f"- 周期: {zh_value(reports.get('week_range', 'N/A'))}",
            f"- 风险分变化（起始 -> 当前）: {zh_value(reports.get('risk_score_start', 'N/A'))} -> {zh_value(reports.get('risk_score_end', score.total))}",
            f"- 平均执行率: {zh_value(reports.get('adherence_avg', 'N/A'))}",
            "",
            "### 本周亮点",
            *(f"- {item}" for item in weekly_wins[:3]),
            "",
            "### 主要不足",
            *(f"- {item}" for item in weekly_gaps[:3]),
            "",
            "### 指标快照",
            f"- 睡眠: 平均 {zh_value(reports.get('sleep_avg_hours', 'N/A'))} 小时，一致性 {zh_value(reports.get('sleep_consistency', 'N/A'))}",
            f"- 日均步数: {zh_value(reports.get('steps_avg', 'N/A'))}",
            f"- 训练完成: {zh_value(reports.get('training_sessions_completed', 'N/A'))}/{zh_value(reports.get('training_sessions_target', 'N/A'))}",
            f"- 腰围变化: {zh_value(reports.get('waist_delta_cm', 'N/A'))} cm",
            f"- 体重变化: {zh_value(reports.get('weight_delta_kg', 'N/A'))} kg",
            "",
            "### 保健品安全事件",
            f"- 可继续: {safe_n}",
            f"- 需医生复核: {review_n}",
            f"- 暂不建议: {avoid_n}",
            *(f"- 阻碍: {item}" for item in blockers[:3]),
            "",
            "### 下周重点",
            *(f"- {item}" for item in weekly_focus[:3]),
            "",
            "## 月报",
            f"- 月份: {zh_value(reports.get('month', 'N/A'))}",
            f"- 风险分趋势: {zh_value(reports.get('risk_score_start', 'N/A'))} -> {zh_value(reports.get('risk_score_end', score.total))}",
            f"- 执行率趋势: {zh_value(reports.get('adherence_trend', 'N/A'))}",
            "",
            "### 进展总结",
        ]
    )

    stable = ensure_list(reports.get("monthly_stable_habits", []))
    improvements = ensure_list(reports.get("monthly_improvements", []))
    regressions = ensure_list(reports.get("monthly_regressions", []))
    plan_keep = ensure_list(reports.get("plan_keep", []))
    plan_reduce = ensure_list(reports.get("plan_reduce", []))
    plan_add = ensure_list(reports.get("plan_add", []))
    follow_up = ensure_list(reports.get("medical_follow_up_flags", []))

    lines.extend(
        [
            *(f"- 已稳定: {item}" for item in stable[:3]),
            *(f"- 明显改善: {item}" for item in improvements[:3]),
            "",
            "### 风险与回退",
            *(f"- {item}" for item in regressions[:3]),
            f"- 恢复/压力关注: {zh_value(reports.get('recovery_stress_concerns', 'N/A'))}",
            "",
            "### 保健品安全汇总",
            f"- 评估总数: {len(supplements)}",
            f"- 可继续: {safe_n}",
            f"- 需医生复核: {review_n}",
            f"- 暂不建议: {avoid_n}",
            "",
            "### 下月计划调整",
            *(f"- 保留: {item}" for item in plan_keep[:3]),
            *(f"- 减少/简化: {item}" for item in plan_reduce[:3]),
            *(f"- 新增/升级: {item}" for item in plan_add[:3]),
            "",
            "### 医疗随访提示",
            *(f"- {item}" for item in follow_up[:5]),
            "",
            "_本输出仅用于生活方式管理，不构成医疗诊断。_",
        ]
    )

    return "\n".join(lines).replace("\n\n\n", "\n\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate longevity risk score and weekly/monthly markdown reports from JSON input."
    )
    parser.add_argument("--input", required=True, help="Path to input JSON")
    parser.add_argument("--output", help="Path to output markdown file (defaults to stdout)")
    args = parser.parse_args()

    input_path = Path(args.input)
    data = json.loads(input_path.read_text(encoding="utf-8"))
    score = calculate_score(data)
    report = generate_markdown(data, score)

    if args.output:
        Path(args.output).write_text(report + "\n", encoding="utf-8")
    else:
        print(report)


if __name__ == "__main__":
    main()
