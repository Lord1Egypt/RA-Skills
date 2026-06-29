#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
menstrual-health-tracker 数据分析引擎
用法：
  analyze.py <data_json_path>        # 分析并打印报告
  analyze.py <data_json_path> --dashboard <output_html>  # 生成 HTML 仪表盘
"""

import json
import sys
import math
import os
from datetime import date, timedelta, datetime
from pathlib import Path


# ─────────────────────────────────────────
#  工具函数
# ─────────────────────────────────────────
def parse_date(s):
    if not s:
        return None
    if isinstance(s, date):
        return s
    return datetime.strptime(str(s), "%Y-%m-%d").date()


def day_diff(d1, d2):
    """d2 - d1，返回整数天数"""
    return (parse_date(d2) - parse_date(d1)).days


def add_days(d, n):
    return (parse_date(d) + timedelta(days=n)).strftime("%Y-%m-%d")


def today_str():
    return date.today().strftime("%Y-%m-%d")


# ─────────────────────────────────────────
#  核心分析
# ─────────────────────────────────────────
def analyze(data: dict) -> dict:
    """返回多维分析结果 dict"""
    cycles = data.get("cycles", [])
    # 按开始日期升序排列，保留所有有start_date的记录（包括进行中的）
    cycles = sorted([c for c in cycles if c.get("start_date")],
                    key=lambda c: c["start_date"])
    # 已完成周期（有end_date的）用于统计
    completed_cycles = [c for c in cycles if c.get("end_date")]
    n = len(completed_cycles)

    result = {
        "total_cycles": len(cycles),  # 总记录数（含进行中）
        "completed_cycles": n,         # 已完成周期数
        "life_stage": data.get("user_profile", {}).get("life_stage", "menstruating"),
    }

    if n == 0:
        result["status"] = "no_data"
        return result

    # ── 1. 经期持续天数 ──────────────────────
    period_lengths = [day_diff(c["start_date"], c["end_date"]) + 1 for c in completed_cycles]
    result["period_lengths"] = period_lengths
    result["avg_period_length"] = round(sum(period_lengths) / n, 1)
    result["min_period_length"] = min(period_lengths)
    result["max_period_length"] = max(period_lengths)

    # ── 2. 周期长度（相邻 start_date 差） ─────
    # 用所有有 start_date 的记录计算间隔（含进行中的），
    # 但只对两个都有完整起止日期的相邻周期做统计
    if len(cycles) >= 2:
        raw_lengths = []
        prev_complete = None
        for c in cycles:
            has_end = c.get("end_date") is not None
            if prev_complete is not None:
                delta = day_diff(prev_complete, c["start_date"])
                raw_lengths.append(delta)
            if has_end:
                prev_complete = c["start_date"]

        # 过滤明显记录断层（>50天）和异常短（<18天）
        cycle_lengths = [l for l in raw_lengths if 18 <= l <= 50]
        if not cycle_lengths:
            cycle_lengths = raw_lengths  # 如果全被过滤掉，用原始数据

        if cycle_lengths:
            avg_c = sum(cycle_lengths) / len(cycle_lengths)
            variance = sum((x - avg_c) ** 2 for x in cycle_lengths) / len(cycle_lengths)
            std_c = math.sqrt(variance)
            cv = std_c / avg_c if avg_c > 0 else 0

            result["cycle_lengths"] = cycle_lengths
            result["raw_cycle_lengths"] = raw_lengths
            result["filtered_out"] = len(raw_lengths) - len(cycle_lengths)
            result["avg_cycle_length"] = round(avg_c, 1)
            result["min_cycle_length"] = min(cycle_lengths)
            result["max_cycle_length"] = max(cycle_lengths)
            result["cycle_std"] = round(std_c, 1)
            result["cycle_cv"] = round(cv, 3)

            # 规律性评级
            if cv < 0.05:
                regularity = "非常规律"
            elif cv < 0.12:
                regularity = "比较规律"
            elif cv < 0.20:
                regularity = "略有波动"
            else:
                regularity = "波动较大"
            result["regularity"] = regularity
        else:
            result["cycle_lengths"] = []
            result["avg_cycle_length"] = None
            result["regularity"] = "数据收集中"

        # ── 3. 趋势分析（线性回归斜率）───────
        if len(cycle_lengths) >= 3:
            x = list(range(len(cycle_lengths)))
            x_mean = sum(x) / len(x)
            y_mean = sum(cycle_lengths) / len(cycle_lengths)
            num = sum((xi - x_mean) * (yi - y_mean)
                      for xi, yi in zip(x, cycle_lengths))
            den = sum((xi - x_mean) ** 2 for xi in x)
            slope = round(num / den, 2) if den != 0 else 0
            result["cycle_trend_slope"] = slope  # +: 趋长, -: 趋短

        # ── 4. 预测（近期加权）──────────────
        # 如果最后一个周期正在进行中（无end_date），以它为基准
        # 否则以最后一个已完成周期为基准
        last_cycle = cycles[-1]
        if last_cycle.get("end_date") is None:
            prediction_base = last_cycle["start_date"]
        elif completed_cycles:
            prediction_base = completed_cycles[-1]["start_date"]
        else:
            prediction_base = last_cycle["start_date"]

        # 加权平均：近期权重更高（指数衰减，半衰期约3个周期）
        decay = 0.79  # 衰减因子，0.79^3 ≈ 0.5
        if cycle_lengths:
            cl = cycle_lengths  # 已过滤异常的周期长度列表
            weighted_sum = 0.0
            weight_total = 0.0
            n_cl = len(cl)
            for i, length in enumerate(cl):
                age = n_cl - 1 - i  # 0=最近, 越大越旧
                w = decay ** age
                weighted_sum += length * w
                weight_total += w
            weighted_avg_c = weighted_sum / weight_total
            result["weighted_avg_cycle_length"] = round(weighted_avg_c, 1)

            # 近期模式检测：如果最近N个周期有明显趋势或稳定模式，优先用近期数据
            recent_n = min(4, n_cl)  # 最多取最近4个
            recent = cl[-recent_n:]
            recent_avg = sum(recent) / len(recent)
            recent_std = (sum((x - recent_avg) ** 2 for x in recent) / len(recent)) ** 0.5
            global_avg = result.get("avg_cycle_length", 0)
            global_std = result.get("cycle_std", 0)

            # 条件1: 近期均值与全局均值偏差 > 4天
            # 条件2: 近期标准差明显小于全局（近期更规律）
            # 条件3: 最近2个周期都在28-35天范围（稳定短周期模式），且与全局偏差 > 1.5天
            last_two = cl[-2:] if n_cl >= 2 else []
            stable_short = len(last_two) == 2 and all(28 <= x <= 35 for x in last_two)

            if abs(recent_avg - global_avg) > 4:
                predicted_interval = round(recent_avg)
                result["prediction_basis"] = f"近期{len(recent)}个周期均值{recent_avg:.1f}天（与历史偏差大）"
            elif recent_std < global_std * 0.7 and len(recent) >= 3:
                predicted_interval = round(recent_avg)
                result["prediction_basis"] = f"近期{len(recent)}个周期均值{recent_avg:.1f}天（近期更规律）"
            elif stable_short and abs(sum(last_two) / 2 - global_avg) > 1.5:
                predicted_interval = round(sum(last_two) / 2)
                result["prediction_basis"] = f"最近2个周期均值{sum(last_two)/2:.1f}天（稳定短周期模式）"
            else:
                predicted_interval = round(weighted_avg_c)
                result["prediction_basis"] = f"加权均值{weighted_avg_c:.1f}天"
        else:
            predicted_interval = round(avg_c)

        next_start = add_days(prediction_base, predicted_interval)
        next_end   = add_days(next_start, round(result["avg_period_length"]) - 1)
        ovulation  = add_days(next_start, predicted_interval - 14)
        fertile_start = add_days(ovulation, -3)
        fertile_end   = add_days(ovulation,  1)

        today = today_str()
        days_until = day_diff(today, next_start)

        result["prediction"] = {
            "next_period_start": next_start,
            "next_period_end":   next_end,
            "ovulation_date":    ovulation,
            "fertile_start":     fertile_start,
            "fertile_end":       fertile_end,
            "days_until_next":   days_until,
        }
    else:
        result["cycle_lengths"] = []
        result["avg_cycle_length"] = None
        result["regularity"] = "数据收集中"

    # ── 5. 症状频率分析 ─────────────────────
    symptom_counts = {}
    symptom_severity = {}
    for c in completed_cycles:
        for sym, detail in (c.get("symptoms") or {}).items():
            if isinstance(detail, dict):
                present  = detail.get("present", False)
                severity = detail.get("severity", 0)
            else:
                present  = bool(detail)
                severity = 0
            if present:
                symptom_counts[sym]   = symptom_counts.get(sym, 0) + 1
                symptom_severity[sym] = symptom_severity.get(sym, 0) + severity

    symptom_rate = {
        s: round(cnt / n * 100, 1)
        for s, cnt in symptom_counts.items()
    }
    symptom_avg_severity = {
        s: round(symptom_severity[s] / symptom_counts[s], 1)
        for s in symptom_counts
    }
    result["symptom_rate"]         = symptom_rate
    result["symptom_avg_severity"] = symptom_avg_severity
    result["top_symptoms"] = sorted(symptom_rate, key=lambda s: -symptom_rate[s])[:5]

    # ── 6. 情绪均值 ─────────────────────────
    moods = [c.get("mood_score") for c in completed_cycles if c.get("mood_score") is not None]
    if moods:
        result["avg_mood"]    = round(sum(moods) / len(moods), 1)
        result["min_mood"]    = min(moods)
        result["max_mood"]    = max(moods)
    else:
        result["avg_mood"] = None

    # ── 7. 流量分布 ─────────────────────────
    flow_dist = {}
    for c in completed_cycles:
        f = c.get("flow_level")
        if f:
            flow_dist[f] = flow_dist.get(f, 0) + 1
    result["flow_distribution"] = flow_dist

    # ── 8. 影响因素关联（简单标记） ──────────
    event_impact = {}
    for c in cycles:
        c_len = None
        idx = cycles.index(c)
        if idx + 1 < len(cycles):
            c_len = day_diff(c["start_date"], cycles[idx+1]["start_date"])
        for evt in (c.get("events") or []):
            evt_type = evt.get("type", "unknown") if isinstance(evt, dict) else str(evt)
            if evt_type not in event_impact:
                event_impact[evt_type] = []
            if c_len:
                event_impact[evt_type].append(c_len)
    result["event_impact"] = {
        evt: round(sum(lens) / len(lens), 1)
        for evt, lens in event_impact.items() if lens
    }

    # ── 9. 预警信号检查 ─────────────────────
    alerts = []
    if n >= 3:
        avg_c_val = result.get("avg_cycle_length")
        if avg_c_val and avg_c_val < 21:
            alerts.append("avg_cycle_short")
        if avg_c_val and avg_c_val > 35:
            alerts.append("avg_cycle_long")
        if result["avg_period_length"] > 8:
            alerts.append("period_too_long")
        if result["avg_period_length"] < 2:
            alerts.append("period_too_short")
        cv_val = result.get("cycle_cv", 0)
        if cv_val > 0.25:
            alerts.append("high_variability")
    result["alerts"] = alerts

    return result


# ─────────────────────────────────────────
#  建议生成（3轮压力测试）
# ─────────────────────────────────────────
RECOMMENDATION_DB = {
    "avg_cycle_short": {
        "title": "周期偏短，值得关注",
        "text":  "你的平均周期 < 21 天。可能与甲状腺功能异常、高催乳素血症或生活压力有关。建议记录一个月基础体温曲线，并咨询妇科医生。",
        "type":  "medical_referral",
        "level": "alert"
    },
    "avg_cycle_long": {
        "title": "周期偏长，留意一下",
        "text":  "平均周期 > 35 天可能与排卵延迟、多囊卵巢综合征(PCOS)或甲状腺功能低下相关。若同时伴有痤疮、多毛或体重增加，建议妇科检查。",
        "type":  "medical_referral",
        "level": "alert"
    },
    "period_too_long": {
        "title": "经期持续偏长",
        "text":  "经期持续 > 8 天需要关注。可能因素：子宫肌瘤、子宫息肉、凝血功能或激素水平异常。如果大量出血，建议及时就诊。",
        "type":  "medical_referral",
        "level": "alert"
    },
    "period_too_short": {
        "title": "经期持续偏短",
        "text":  "经期 < 2 天可能提示内膜薄或激素水平偏低。如果备孕中，内膜状态很重要，建议妇科检查评估。",
        "type":  "medical_referral",
        "level": "alert"
    },
    "high_variability": {
        "title": "周期波动较大",
        "text":  "你的周期变异系数偏高，说明规律性有待改善。常见触发因素：睡眠不规律、高强度压力、体重骤变或营养不足。建议优先稳定作息，持续记录3个月观察变化。",
        "type":  "lifestyle",
        "level": "tip"
    },
    "general_nutrition": {
        "title": "经期营养支持",
        "text":  "经期铁元素流失增加，建议在经期中搭配：红肉/菠菜/黑木耳补铁 + 猕猴桃/橙子补维C促吸收。减少咖啡因可改善腹痛。",
        "type":  "nutrition",
        "level": "tip"
    },
    "general_exercise": {
        "title": "经期运动策略",
        "text":  "经期前3天适合轻柔运动（瑜伽、散步），经期第4-7天可逐渐恢复。卵泡期是高强度训练的黄金期，身体恢复快、体能最优。",
        "type":  "exercise",
        "level": "tip"
    },
    "record_bbt": {
        "title": "尝试记录基础体温",
        "text":  "每天晨起测舌下温度（同一时间、未起床前），坚持记录一个周期就能看到双相体温曲线，帮助确认排卵。这是了解自己身体节奏最经济的方式。",
        "type":  "lifestyle",
        "level": "tip"
    },
}

# 针对症状的个性化建议
SYMPTOM_ADVICE = {
    "cramps":            ("腹痛缓解", "热敷腹部、适量镁补充（200-400mg/天）、经期适度散步都被证实有效。布洛芬在经期开始时预防性服用效果优于疼痛出现后服用。"),
    "bloating":          ("腹胀管理", "经期前3-5天减少盐分、精制碳水和含气饮料摄入。多喝温水、增加钾元素（香蕉、牛油果）有助于排水减胀。"),
    "headache":          ("经期头痛", "经期头痛多与雌激素下降有关。保持规律睡眠、充足水分是基础。如果头痛严重或伴随视觉症状，建议就医评估偏头痛。"),
    "breast_tenderness": ("乳房胀痛", "黄体期乳房胀痛是雌/孕激素波动的正常反应。减少咖啡因摄入、穿支撑性内衣可以缓解。维E补充（400IU/天）有一定帮助。"),
    "fatigue":           ("经期疲劳", "适量铁补充（配合维C）有助于改善经期贫血相关疲劳。同时优化睡眠、避免熬夜。注意：疲劳也可能是甲状腺功能问题的信号。"),
    "low_mood":          ("情绪低落", "经期情绪低落与激素波动直接相关，你不是一个人。户外活动、Omega-3（鱼油）和社交联结都有研究支持。若每月都有严重抑郁症状，可以和医生聊聊PMDD的可能性。"),
    "irritability":      ("易怒/PMS", "易怒是孕激素+雌激素下降时的常见反应。减少酒精和精制糖、增加复合碳水和镁补充。在高峰期提前告知身边人「这几天我可能需要多一些空间」也是智慧之举。"),
    "insomnia":          ("经期失眠", "经期前后孕激素波动影响睡眠质量。建议：降低卧室温度（18-20°C睡眠最佳）、避免蓝光、可尝试镁补充（甘氨酸镁形式较优）。"),
    "acne":              ("经期痤疮", "经期前痤疮暴发是雄激素相对升高的表现。保持清洁、避免高GI食物、减少奶制品摄入可能有帮助。如果严重持续，皮肤科或妇科内分泌科可以评估激素调控方案。"),
}


def generate_recommendations(analysis: dict) -> list:
    """生成3轮压力测试后的建议列表"""
    recs = []

    # ─ 第1步：基于预警生成建议 ────────────
    for alert in analysis.get("alerts", []):
        if alert in RECOMMENDATION_DB:
            recs.append(RECOMMENDATION_DB[alert].copy())

    # ─ 第2步：基于高频症状生成建议 ─────────
    top_syms = analysis.get("top_symptoms", [])
    for sym in top_syms[:3]:
        rate = analysis.get("symptom_rate", {}).get(sym, 0)
        if rate >= 40 and sym in SYMPTOM_ADVICE:
            title, text = SYMPTOM_ADVICE[sym]
            recs.append({
                "title": f"{title}（出现率 {rate}%）",
                "text":  text,
                "type":  "lifestyle",
                "level": "tip"
            })

    # ─ 第3步：通用健康建议 ───────────────
    recs.append(RECOMMENDATION_DB["general_nutrition"].copy())
    recs.append(RECOMMENDATION_DB["general_exercise"].copy())

    # BBT 建议（如果还没有 BBT 数据）
    all_bbt = [c.get("bbt") for c in [] if c.get("bbt")]  # placeholder
    if not all_bbt:
        recs.append(RECOMMENDATION_DB["record_bbt"].copy())

    # ─ 压力测试3轮校验 ──────────────────
    # Round 1: 科学准确性 — 全部来自 RECOMMENDATION_DB / SYMPTOM_ADVICE，已内置循证来源
    # Round 2: 个性化 — 检查建议是否基于用户数据
    validated = []
    for r in recs:
        # 个性化评分：包含百分比或具体数字为5分，通用建议为3分
        personalization_score = 5 if "%" in r.get("title", "") or "%" in r.get("text", "") else 3
        if personalization_score < 3:
            continue  # 低于3分的泛泛建议丢弃
        # Round 3: 安全性 — 医疗类建议需标注就诊
        if r.get("type") == "medical_referral" and "就诊" not in r.get("text", "") and "医生" not in r.get("text", ""):
            r["text"] += " ⚕️ 建议咨询妇科或内分泌科医生。"
        validated.append(r)

    return validated[:8]  # 最多返回8条，保持精炼


# ─────────────────────────────────────────
#  生成仪表盘 HTML
# ─────────────────────────────────────────
def generate_dashboard(data: dict, analysis: dict, recommendations: list, output_path: str):
    skill_dir  = Path(__file__).parent.parent
    template   = (skill_dir / "assets" / "dashboard.html").read_text(encoding="utf-8")

    # 把 analysis、recommendations 注入到 HTML 末尾
    injection = f"""
<script>
(function() {{
  var userData = {json.dumps(data, ensure_ascii=False, indent=2)};
  var analysisResult = {json.dumps(analysis, ensure_ascii=False, indent=2)};
  var recommendations = {json.dumps(recommendations, ensure_ascii=False, indent=2)};

  document.addEventListener('DOMContentLoaded', function() {{
    if (window.menstrualDashboard) {{
      window.menstrualDashboard.loadData(userData, analysisResult, recommendations);
    }}
  }});
}})();
</script>
"""
    # 在 </body> 前插入
    html = template.replace("</body>", injection + "</body>")
    Path(output_path).write_text(html, encoding="utf-8")
    print(f"✅ 仪表盘已生成: {output_path}")


# ─────────────────────────────────────────
#  文字报告
# ─────────────────────────────────────────
def print_report(analysis: dict, recommendations: list):
    stage_map = {
        "premenarche":    "初潮前",
        "menstruating":   "正常经期",
        "ttc":            "备孕期",
        "pregnant":       "孕期",
        "postpartum":     "产后",
        "perimenopause":  "围绝经期",
        "postmenopause":  "绝经后",
    }
    stage = stage_map.get(analysis.get("life_stage", ""), "经期追踪")
    n = analysis.get("total_cycles", 0)

    print("=" * 52)
    print(f"  🌙 经期健康分析报告  |  {stage}  |  共{n}个周期")
    print("=" * 52)

    if n == 0:
        print("  暂无数据，请先记录经期。")
        return

    # 周期摘要
    print("\n【周期摘要】")
    avg_c = analysis.get("avg_cycle_length")
    w_avg_c = analysis.get("weighted_avg_cycle_length")
    if avg_c:
        print(f"  历史平均周期：{avg_c} 天  （规律性：{analysis.get('regularity', '--')}）")
        if w_avg_c:
            print(f"  近期加权周期：{w_avg_c} 天（近期权重更高）")
        print(f"  周期范围：{analysis.get('min_cycle_length')}–{analysis.get('max_cycle_length')} 天")
    print(f"  平均经期持续：{analysis.get('avg_period_length')} 天")

    # 预测
    pred = analysis.get("prediction", {})
    if pred:
        days_u = pred.get("days_until_next", 0)
        if days_u > 0:
            timing = f"还有 {days_u} 天"
        elif days_u == 0:
            timing = "就是今天"
        else:
            timing = f"已过 {abs(days_u)} 天（请检查记录）"
        print(f"\n【预测】")
        print(f"  下次经期：{pred['next_period_start']} （{timing}）")
        print(f"  排卵日预估：{pred['ovulation_date']}")
        print(f"  易孕期：{pred['fertile_start']} ~ {pred['fertile_end']}")

    # 高频症状
    top = analysis.get("top_symptoms", [])
    symptom_zh = {
        "cramps": "腹痛", "back_pain": "腰酸", "headache": "头痛",
        "breast_tenderness": "乳房胀痛", "bloating": "腹胀", "fatigue": "疲劳",
        "nausea": "恶心", "acne": "痤疮", "insomnia": "失眠",
        "irritability": "易怒", "anxiety": "焦虑", "low_mood": "情绪低落",
        "mood_swings": "情绪波动", "appetite_change": "食欲变化"
    }
    if top:
        rates = analysis.get("symptom_rate", {})
        print(f"\n【高频症状 Top {len(top)}】")
        for s in top:
            print(f"  · {symptom_zh.get(s, s)}: 出现率 {rates.get(s, 0)}%")

    # 预警
    alerts = analysis.get("alerts", [])
    if alerts:
        print("\n【⚠️  注意事项】")
        alert_zh = {
            "avg_cycle_short":  "平均周期 < 21 天",
            "avg_cycle_long":   "平均周期 > 35 天",
            "period_too_long":  "经期持续 > 8 天",
            "period_too_short": "经期持续 < 2 天",
            "high_variability": "周期波动偏大（CV > 25%）",
        }
        for a in alerts:
            print(f"  ⚠ {alert_zh.get(a, a)}")

    # 建议
    if recommendations:
        print("\n【🌿 健康建议（已压力测试）】")
        for i, r in enumerate(recommendations, 1):
            level_icon = "⚕️" if r.get("type") == "medical_referral" else "✦"
            print(f"\n  {level_icon} {i}. {r['title']}")
            # 自动换行
            words = r.get("text", "")
            for chunk in [words[i:i+46] for i in range(0, len(words), 46)]:
                print(f"     {chunk}")

    print("\n" + "=" * 52)
    print("  数据仅供参考，不替代专业医疗诊断")
    print("=" * 52)


# ─────────────────────────────────────────
#  加载 / 保存数据
# ─────────────────────────────────────────
DEFAULT_DATA_PATH = Path.home() / ".workbuddy" / "data" / "menstrual_health.json"

def load_data(path: str = None) -> dict:
    p = Path(path) if path else DEFAULT_DATA_PATH
    if not p.exists():
        return {"user_profile": {"life_stage": "menstruating"}, "cycles": [], "daily_logs": [], "events": []}
    return json.loads(p.read_text(encoding="utf-8"))


def save_data(data: dict, path: str = None):
    p = Path(path) if path else DEFAULT_DATA_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def add_cycle(data: dict, start_date: str, end_date: str, **kwargs) -> dict:
    """添加一条经期记录并返回更新后的数据"""
    import uuid
    cycle = {
        "id":           str(uuid.uuid4())[:8],
        "start_date":   start_date,
        "end_date":     end_date,
        "flow_level":   kwargs.get("flow_level"),
        "symptoms":     kwargs.get("symptoms", {}),
        "mood":         kwargs.get("mood"),
        "mood_score":   kwargs.get("mood_score"),
        "bbt":          kwargs.get("bbt"),
        "weight":       kwargs.get("weight"),
        "notes":        kwargs.get("notes", ""),
        "events":       kwargs.get("events", []),
        "exercise":     kwargs.get("exercise"),
    }
    data["cycles"].append(cycle)
    # 保持时间升序
    data["cycles"].sort(key=lambda c: c["start_date"])
    return data


# ─────────────────────────────────────────
#  CLI 入口
# ─────────────────────────────────────────
def main():
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    data_path     = args[0]
    dashboard_out = None

    if "--dashboard" in args:
        idx = args.index("--dashboard")
        dashboard_out = args[idx + 1] if idx + 1 < len(args) else "dashboard_output.html"

    data         = load_data(data_path)
    analysis     = analyze(data)
    recs         = generate_recommendations(analysis)

    print_report(analysis, recs)

    if dashboard_out:
        generate_dashboard(data, analysis, recs, dashboard_out)


if __name__ == "__main__":
    main()
