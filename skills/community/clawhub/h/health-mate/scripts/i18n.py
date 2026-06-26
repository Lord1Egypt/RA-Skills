#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared locale helpers for Health-Mate."""

from __future__ import annotations

import os
import re
from typing import Dict, Iterable, Optional

DEFAULT_LOCALE = "zh-CN"
SUPPORTED_LOCALES = {"zh-CN", "en-US", "ja-JP"}

LOCALE_ALIASES = {
    "zh": "zh-CN",
    "zh-cn": "zh-CN",
    "zh_hans": "zh-CN",
    "zh-hans": "zh-CN",
    "cn": "zh-CN",
    "chinese": "zh-CN",
    "中文": "zh-CN",
    "简体中文": "zh-CN",
    "en": "en-US",
    "en-us": "en-US",
    "en_us": "en-US",
    "english": "en-US",
    "英文": "en-US",
    "ja": "ja-JP",
    "ja-jp": "ja-JP",
    "ja_jp": "ja-JP",
    "japanese": "ja-JP",
    "日本語": "ja-JP",
    "日文": "ja-JP",
}

TEXTS: Dict[str, Dict[str, str]] = {
    "zh-CN": {
        "security_warning_title": "安全警告",
        "env_validation_failed": "环境校验失败",
        "env_missing_memory_dir": "错误：MEMORY_DIR 环境变量未配置（必填）",
        "env_set_memory_dir": "请在 config/.env 文件中设置 MEMORY_DIR='/path/to/memory'，ClawHub 手动上传时可参考 config/user_config.example.json 中的 env 配置。",
        "env_memory_dir_missing": "错误：MEMORY_DIR 目录不存在：{path}",
        "env_memory_dir_unreadable": "错误：MEMORY_DIR 目录无读取权限：{path}",
        "env_no_webhooks": "警告：未配置任何 Webhook，报告将仅在本地生成 PDF。",
        "env_webhook_hint": "如需推送，请配置 DINGTALK_WEBHOOK/FEISHU_WEBHOOK/TELEGRAM_*。",
        "program_exit": "程序已安全退出。请修复上述问题后重新运行。",
        "config_load_failed": "警告：读取配置文件失败 - {error}",
        "ai_comment_timeout": "AI 点评生成超时（第{attempt}次），重试中...",
        "ai_comment_failed": "AI 点评生成失败（第{attempt}次）：{error}",
        "ai_plan_timeout": "AI 方案生成超时（第{attempt}次），重试中...",
        "ai_plan_failed": "AI 方案生成失败（第{attempt}次）：{error}",
        "tavily_failed": "Tavily 搜索失败（第{attempt}次）：{error}",
        "exercise_score_failed": "警告：运动评分计算失败 - {error}",
        "daily_report_title": "健康日报",
        "weekly_report_title": "健康周报",
        "monthly_report_title": "健康月报",
        "daily_report_heading": "{date} 健康报告",
        "weekly_text_heading": "{start_date} 至 {end_date} 健康周报",
        "overall_score_title": "今日综合评分",
        "item_summary_title": "分项汇总",
        "ai_comment_title": "AI 点评",
        "details_title": "今日详情汇总",
        "render_notice_title": "渲染说明",
        "meal_section": "进食情况",
        "water_section": "饮水情况",
        "exercise_section": "运动情况",
        "next_day_plan_title": "次日优化方案（AI 动态生成）",
        "diet_label": "饮食合规性",
        "water_label": "饮水完成度",
        "weight_label": "体重管理",
        "symptom_label": "症状管理",
        "exercise_label": "运动管理",
        "adherence_label": "健康依从性",
        "score_total_label": "总分",
        "base_score_label": "基础分",
        "exercise_bonus_label": "运动加分",
        "fat_in_range": "脂肪摄入合理",
        "fat_low": "脂肪摄入过低 ({value:.1f}g)",
        "fat_high": "脂肪摄入超标 ({value:.1f}g)",
        "protein_ok": "蛋白质摄入充足",
        "protein_low": "蛋白质不足",
        "completion_status": "{current}ml/{target}ml，完成度 {percent}%",
        "weight_status": "晨起空腹：{weight}，BMI：{bmi:.1f}",
        "no_symptoms": "无不适症状",
        "symptoms_prefix": "症状：{symptoms}",
        "adherence_status": "完成 {meals} 餐，饮水{water_status}",
        "water_goal_met": "达标",
        "water_goal_not_met": "未达标",
        "no_record": "无记录",
        "no_detail_record": "无详细记录",
        "not_recorded": "未记录",
        "not_available": "-",
        "morning_fasting": "晨起空腹",
        "weight_target": "目标：{weight}",
        "bmi_reference": "18.5-24（正常）",
        "recommended_calories_reference": "{condition}安全范围",
        "fiber_reference": "促进胆汁排泄",
        "expert_ai_insights": "专家 AI 点评",
        "daily_baseline_data": "基础健康数据",
        "daily_nutrition_breakdown": "当日营养摄入核算",
        "daily_water_details": "饮水详情",
        "daily_meal_details": "进食详情",
        "daily_exercise_details": "运动详情",
        "extra_monitoring_records": "附加监测记录",
        "risk_alerts": "风险预警",
        "no_risk": "今日无明显风险，继续保持健康生活方式！",
        "action_plan": "次日可执行方案",
        "diet_plan": "饮食计划",
        "water_plan": "饮水计划",
        "exercise_plan": "运动建议",
        "special_attention": "特别关注",
        "generated_at": "报告生成时间：{timestamp}",
        "pdf_saved_local": "未配置公网域名，PDF 仅保存在本地。",
        "pdf_local_path": "本地路径：{path}",
        "pdf_copied": "PDF 已复制到 Web 目录：{path}",
        "pdf_download_url": "下载链接：{url}",
        "pdf_generation_failed": "PDF 生成失败 - {error}",
        "meal_total": "合计 {calories:.0f} kcal",
        "no_water_today": "今日无饮水记录",
        "no_meals_today": "今日无进食记录",
        "no_food_detail": "无详细食物记录",
        "no_exercise_today": "今日无运动记录",
        "risk_label": "风险：{value}",
        "advice_label": "建议：{value}",
        "nutrition_chart_center": "{calories}\nkcal",
        "water_chart_center": "{current}\n/ {target}ml",
        "water_chart_total": "总{amount}",
        "today_steps": "今日步数",
        "step_progress": "{current} / {target} 步",
        "calories_unit": "{value} kcal",
        "minutes_unit": "{value}分钟",
        "steps_unit": "{value}步",
        "distance_unit_km": "{value}km",
        "metric": "指标",
        "value": "数值",
        "reference_range": "参考范围",
        "height": "身高",
        "weight": "体重",
        "bmi": "BMI",
        "bmr": "基础代谢",
        "tdee": "每日消耗",
        "recommended_calories": "推荐热量",
        "protein": "蛋白质",
        "fat": "脂肪",
        "carb": "碳水",
        "fiber": "膳食纤维",
        "nutrient": "营养素",
        "actual_intake": "实际摄入",
        "recommended_intake": "推荐量",
        "food_name": "食物名称",
        "portion": "份量",
        "calories": "热量",
        "duration": "耗时",
        "distance": "距离",
        "burn": "消耗",
        "status": "状态",
        "dimension": "维度",
        "score": "得分",
        "stars": "星级",
        "achieved": "达标",
        "under_target": "未达标",
        "normal": "正常",
        "attention": "关注",
        "symptom_free": "无症状",
        "has_symptoms": "有症状",
        "needs_boost": "待加强",
        "excellent": "优秀",
        "fair": "一般",
        "good": "良好",
        "needs_improvement": "待改进",
        "average_weight": "平均体重",
        "average_calories": "日均摄入",
        "average_water": "日均饮水",
        "average_steps": "日均步数",
        "health_status": "健康状态",
        "stable": "稳定",
        "down": "下降",
        "up": "上升",
        "active": "活跃",
        "low": "偏低",
        "weekly_overview_title": "本周健康指标概览",
        "weekly_trend_title": "核心趋势分析",
        "weekly_ai_review_title": "专家 AI 深度复盘",
        "weekly_next_plan_title": "下周干预方案",
        "weekly_rings_center": "本周\n健康概览",
        "weekly_ring_diet": "饮食评分",
        "weekly_ring_water": "饮水达标率",
        "weekly_ring_exercise": "步数达标率",
        "weekly_ring_label": "{label} {percent:.0f}%",
        "target_line": "目标：{target}",
        "weight_trend_title": "本周体重波动趋势 ({unit})",
        "calorie_trend_title": "本周每日摄入热量 (kcal)",
        "step_trend_title": "本周每日步数分布 (步)",
        "water_trend_title": "本周每日饮水量分布 (ml)",
        "weekly_nutrition_center": "日均摄入\n{calories} kcal",
        "weekly_chart_weight_label": "体重趋势图",
        "weekly_chart_calorie_label": "热量趋势图",
        "weekly_chart_nutrition_label": "营养结构图",
        "weekly_chart_step_label": "步数趋势图",
        "weekly_chart_water_label": "饮水趋势图",
        "weekly_period": "评估周期：{start_date} 至 {end_date} | 监测人：{name}",
        "weekly_summary_title": "本周核心指标",
        "weekly_review_section": "本周复盘",
        "weekly_plan_section": "下周行动",
        "weekly_avg_weight_change": "平均体重变化：{value}",
        "weekly_avg_calories_line": "日均摄入热量：{value:.0f} kcal",
        "weekly_avg_water_line": "日均饮水量：{value:.0f} ml",
        "weekly_avg_steps_line": "日均步数：{value:.0f} 步",
        "weekly_symptom_count_line": "不适症状出现次数：{value} 次",
        "weekly_generated_at": "生成时间：{value}",
        "weekly_anchor_date": "锚点日期：{value}",
        "delivery_daily_pdf": "PDF 完整报告",
        "delivery_weekly_pdf": "PDF 完整周报",
        "delivery_monthly_pdf": "PDF 完整月报",
        "delivery_download": "点击下载",
        "delivery_period": "报告周期：{start_date} 至 {end_date}",
        "font_missing_english_fallback": "未找到中文字体文件 {path}，当前报告已自动切换为英文版。若需中文 PDF，请从 {url} 下载字体并放置到该路径。",
        "condition_balanced": "均衡健康",
        "condition_gallstones": "胆结石管理",
        "condition_diabetes": "糖尿病管理",
        "condition_hypertension": "高血压管理",
        "condition_fat_loss": "健身减脂",
        "meal_breakfast": "早餐",
        "meal_lunch": "午餐",
        "meal_dinner": "晚餐",
        "meal_snack": "加餐",
        "water_wake_up": "晨起",
        "water_morning": "上午",
        "water_noon": "中午",
        "water_afternoon": "下午",
        "water_evening": "晚上",
        "exercise_cycling": "骑行",
        "exercise_walking": "散步",
        "exercise_running": "跑步",
        "exercise_workout": "健身",
        "exercise_yoga": "瑜伽",
        "exercise_swimming": "游泳",
        "exercise_other": "其他运动",
        "default_user": "用户",
        "default_name": "东东",
        "condition_tip_balanced": "均衡饮食、规律作息、稳定活动",
        "condition_tip_gallstones": "低脂（{fat_min}-{fat_max}g/天）、高纤维（≥{fiber_min}g/天）、规律进食",
        "condition_tip_diabetes": "控糖、控精制碳水、高纤维、少量多餐",
        "condition_tip_hypertension": "低盐（<2000mg/天）、高钾、高纤维",
        "condition_tip_fat_loss": "高蛋白、适量碳水、控制脂肪、保持训练",
        "fallback_comment_fat_ok": "脂肪摄入 {value:.1f}g 控制在理想范围内，这对你的健康目标很关键。",
        "fallback_comment_fat_low": "脂肪摄入仅 {value:.1f}g，略低于推荐值。适量健康脂肪仍然有必要。",
        "fallback_comment_fat_high": "脂肪摄入 {value:.1f}g 超标，明日需要严格控油。",
        "fallback_comment_fiber_ok": "膳食纤维 {value:.1f}g 达标，继续保持。",
        "fallback_comment_fiber_low": "膳食纤维仅 {value:.1f}g，建议明日增加蔬菜、豆类和粗粮。",
        "fallback_comment_water_ok": "饮水 {value}ml 已达标，做得很好。",
        "fallback_comment_water_low": "饮水仅 {value}ml，距离 {target}ml 目标还有差距。",
        "fallback_comment_steps_high": "今日 {value} 步，活动量充足。",
        "fallback_comment_steps_mid": "今日 {value} 步，基本合格，但仍有提升空间。",
        "fallback_comment_steps_low": "今日仅 {value} 步，活动量明显不足，建议明日增加步行或骑行。",
        "shortcoming_fat_low": "脂肪摄入过低",
        "shortcoming_fat_high": "脂肪摄入超标",
        "shortcoming_fiber_low": "膳食纤维不足",
        "shortcoming_water_low": "饮水不足",
        "shortcoming_exercise_low": "缺乏运动",
        "fallback_diet_1": "早餐（5 分钟）：燕麦粥 + 煮蛋白 2 个 + 凉拌黄瓜 (300kcal)",
        "fallback_diet_2": "午餐（10 分钟）：米饭 + 卤牛肉 + 白灼青菜 (450kcal)",
        "fallback_diet_3": "晚餐（10 分钟）：杂粮粥 + 凉拌豆腐 + 炒蔬菜 (350kcal)",
        "fallback_water_1": "07:30 晨起温水 300ml",
        "fallback_water_2": "10:00 工作间隙 400ml",
        "fallback_water_3": "14:00 午后 400ml",
        "fallback_water_4": "17:00 下班前 400ml",
        "fallback_water_5": "20:00 晚间 300ml",
        "fallback_water_target": "目标总量：{target}ml",
        "fallback_exercise_1": "早餐后散步 15 分钟（促进消化）",
        "fallback_exercise_2": "晚餐后散步 20 分钟（帮助代谢）",
        "fallback_exercise_3": "本周目标：累计运动 150 分钟",
        "fallback_note_fruits": "今日推荐水果：{fruits}",
        "fallback_note_overeat": "昨日有过饱迹象，今天建议控制到七分饱。",
        "fallback_note_fat_low": "昨日脂肪偏低，今天可适量增加健康脂肪，如橄榄油或坚果。",
        "fallback_note_fat_high": "昨日脂肪偏高，今天请避免油炸、重油和高脂甜点。",
        "fallback_note_fiber_low": "昨日纤维不足，今天请增加蔬菜、豆类和粗粮。",
        "fallback_note_exercise_low": "昨日活动量不足，今天建议安排一次轻中度运动。",
        "weekly_ai_failed": "AI 调用失败：{error}",
        "weekly_fallback_review": "本周数据收集完整，整体趋势平稳，请继续保持。",
        "weekly_fallback_plan_1": "保持每日饮水 2000ml",
        "weekly_fallback_plan_2": "增加餐后轻度活动",
        "weekly_fallback_plan_3": "继续控制脂肪摄入与饮食规律",
    },
    "en-US": {
        "security_warning_title": "Security Warning",
        "env_validation_failed": "Environment validation failed",
        "env_missing_memory_dir": "ERROR: MEMORY_DIR is not configured (required).",
        "env_set_memory_dir": "Set MEMORY_DIR='/path/to/memory' in config/.env. For ClawHub manual uploads, refer to the env block inside config/user_config.example.json.",
        "env_memory_dir_missing": "ERROR: MEMORY_DIR does not exist: {path}",
        "env_memory_dir_unreadable": "ERROR: MEMORY_DIR is not readable: {path}",
        "env_no_webhooks": "WARNING: No webhook is configured. Reports will only be generated locally as PDF.",
        "env_webhook_hint": "Configure DINGTALK_WEBHOOK/FEISHU_WEBHOOK/TELEGRAM_* if you want push delivery.",
        "program_exit": "The program exited safely. Fix the issues above and run it again.",
        "config_load_failed": "WARNING: Failed to read the config file - {error}",
        "ai_comment_timeout": "AI insight generation timed out (attempt {attempt}), retrying...",
        "ai_comment_failed": "AI insight generation failed (attempt {attempt}): {error}",
        "ai_plan_timeout": "AI plan generation timed out (attempt {attempt}), retrying...",
        "ai_plan_failed": "AI plan generation failed (attempt {attempt}): {error}",
        "tavily_failed": "Tavily search failed (attempt {attempt}): {error}",
        "exercise_score_failed": "WARNING: Exercise scoring failed - {error}",
        "daily_report_title": "Daily Health Report",
        "weekly_report_title": "Weekly Health Report",
        "monthly_report_title": "Monthly Health Report",
        "daily_report_heading": "{date} Health Report",
        "weekly_text_heading": "Weekly Health Report ({start_date} to {end_date})",
        "overall_score_title": "Overall Score",
        "item_summary_title": "Category Summary",
        "ai_comment_title": "AI Insight",
        "details_title": "Today's Breakdown",
        "render_notice_title": "Rendering Notice",
        "meal_section": "Meals",
        "water_section": "Hydration",
        "exercise_section": "Exercise",
        "next_day_plan_title": "Action Plan For Tomorrow",
        "diet_label": "Diet Quality",
        "water_label": "Hydration",
        "weight_label": "Weight Management",
        "symptom_label": "Symptom Control",
        "exercise_label": "Exercise",
        "adherence_label": "Routine Adherence",
        "score_total_label": "Total",
        "base_score_label": "Base",
        "exercise_bonus_label": "Exercise Bonus",
        "fat_in_range": "Fat intake is on target",
        "fat_low": "Fat intake is low ({value:.1f}g)",
        "fat_high": "Fat intake is high ({value:.1f}g)",
        "protein_ok": "Protein intake is adequate",
        "protein_low": "Protein intake is low",
        "completion_status": "{current}ml/{target}ml, completion {percent}%",
        "weight_status": "Morning fasting weight: {weight}, BMI: {bmi:.1f}",
        "no_symptoms": "No symptoms recorded",
        "symptoms_prefix": "Symptoms: {symptoms}",
        "adherence_status": "{meals} meal blocks logged, hydration {water_status}",
        "water_goal_met": "on target",
        "water_goal_not_met": "below target",
        "no_record": "No record",
        "no_detail_record": "No detailed record",
        "not_recorded": "Not recorded",
        "not_available": "-",
        "morning_fasting": "Morning fasting",
        "weight_target": "Target: {weight}",
        "bmi_reference": "18.5-24 (normal)",
        "recommended_calories_reference": "{condition} target range",
        "fiber_reference": "Supports healthy digestion",
        "expert_ai_insights": "Expert AI Insight",
        "daily_baseline_data": "Baseline Health Data",
        "daily_nutrition_breakdown": "Nutrition Breakdown",
        "daily_water_details": "Hydration Details",
        "daily_meal_details": "Meal Details",
        "daily_exercise_details": "Exercise Details",
        "extra_monitoring_records": "Additional Tracking",
        "risk_alerts": "Risk Alerts",
        "no_risk": "No major risk was detected today. Keep the routine steady.",
        "action_plan": "Tomorrow's Action Plan",
        "diet_plan": "Diet Plan",
        "water_plan": "Hydration Plan",
        "exercise_plan": "Exercise Plan",
        "special_attention": "Special Attention",
        "generated_at": "Generated at: {timestamp}",
        "pdf_saved_local": "No public report URL is configured, so the PDF was kept locally.",
        "pdf_local_path": "Local file: {path}",
        "pdf_copied": "PDF copied to the web directory: {path}",
        "pdf_download_url": "Download URL: {url}",
        "pdf_generation_failed": "PDF generation failed - {error}",
        "meal_total": "{calories:.0f} kcal total",
        "no_water_today": "No hydration records today",
        "no_meals_today": "No meal records today",
        "no_food_detail": "No detailed food entries",
        "no_exercise_today": "No exercise records today",
        "risk_label": "Risk: {value}",
        "advice_label": "Advice: {value}",
        "nutrition_chart_center": "{calories}\nkcal",
        "water_chart_center": "{current}\n/ {target}ml",
        "water_chart_total": "Total {amount}",
        "today_steps": "Today's Steps",
        "step_progress": "{current} / {target} steps",
        "calories_unit": "{value} kcal",
        "minutes_unit": "{value} min",
        "steps_unit": "{value} steps",
        "distance_unit_km": "{value} km",
        "metric": "Metric",
        "value": "Value",
        "reference_range": "Reference",
        "height": "Height",
        "weight": "Weight",
        "bmi": "BMI",
        "bmr": "BMR",
        "tdee": "Daily Burn",
        "recommended_calories": "Target Calories",
        "protein": "Protein",
        "fat": "Fat",
        "carb": "Carbs",
        "fiber": "Fiber",
        "nutrient": "Nutrient",
        "actual_intake": "Actual",
        "recommended_intake": "Target",
        "food_name": "Food",
        "portion": "Portion",
        "calories": "Calories",
        "duration": "Duration",
        "distance": "Distance",
        "burn": "Burn",
        "status": "Status",
        "dimension": "Category",
        "score": "Score",
        "stars": "Stars",
        "achieved": "On target",
        "under_target": "Below target",
        "normal": "Normal",
        "attention": "Watch",
        "symptom_free": "Clear",
        "has_symptoms": "Symptoms",
        "needs_boost": "Needs work",
        "excellent": "Excellent",
        "fair": "Fair",
        "good": "Good",
        "needs_improvement": "Needs improvement",
        "average_weight": "Average weight",
        "average_calories": "Average calories",
        "average_water": "Average hydration",
        "average_steps": "Average steps",
        "health_status": "Status",
        "stable": "Stable",
        "down": "Down",
        "up": "Up",
        "active": "Active",
        "low": "Low",
        "weekly_overview_title": "Weekly Overview",
        "weekly_trend_title": "Trend Analysis",
        "weekly_ai_review_title": "Expert AI Weekly Review",
        "weekly_next_plan_title": "Plan For Next Week",
        "weekly_rings_center": "Weekly\nOverview",
        "weekly_ring_diet": "Diet score",
        "weekly_ring_water": "Hydration goal rate",
        "weekly_ring_exercise": "Step goal rate",
        "weekly_ring_label": "{label} {percent:.0f}%",
        "target_line": "Target: {target}",
        "weight_trend_title": "Weight Trend This Week ({unit})",
        "calorie_trend_title": "Daily Calories This Week (kcal)",
        "step_trend_title": "Daily Steps This Week",
        "water_trend_title": "Daily Hydration This Week (ml)",
        "weekly_nutrition_center": "Daily avg\n{calories} kcal",
        "weekly_chart_weight_label": "Weight trend chart",
        "weekly_chart_calorie_label": "Calorie trend chart",
        "weekly_chart_nutrition_label": "Macro balance chart",
        "weekly_chart_step_label": "Step trend chart",
        "weekly_chart_water_label": "Hydration trend chart",
        "weekly_period": "Period: {start_date} to {end_date} | User: {name}",
        "weekly_summary_title": "Weekly Metrics",
        "weekly_review_section": "Weekly Review",
        "weekly_plan_section": "Next Week Actions",
        "weekly_avg_weight_change": "Average weight change: {value}",
        "weekly_avg_calories_line": "Average daily calories: {value:.0f} kcal",
        "weekly_avg_water_line": "Average daily hydration: {value:.0f} ml",
        "weekly_avg_steps_line": "Average daily steps: {value:.0f}",
        "weekly_symptom_count_line": "Symptom events: {value}",
        "weekly_generated_at": "Generated at: {value}",
        "weekly_anchor_date": "Anchor date: {value}",
        "delivery_daily_pdf": "Full PDF Report",
        "delivery_weekly_pdf": "Full Weekly PDF",
        "delivery_monthly_pdf": "Full Monthly PDF",
        "delivery_download": "Download",
        "delivery_period": "Report period: {start_date} to {end_date}",
        "font_missing_english_fallback": "The Chinese font file {path} was not found, so this report was rendered in English. If you need Chinese PDF output, download the font from {url} and place it at that path.",
        "condition_balanced": "Balanced Wellness",
        "condition_gallstones": "Gallstone Care",
        "condition_diabetes": "Diabetes Support",
        "condition_hypertension": "Blood Pressure Support",
        "condition_fat_loss": "Fat Loss",
        "meal_breakfast": "Breakfast",
        "meal_lunch": "Lunch",
        "meal_dinner": "Dinner",
        "meal_snack": "Snack",
        "water_wake_up": "Wake-up",
        "water_morning": "Morning",
        "water_noon": "Noon",
        "water_afternoon": "Afternoon",
        "water_evening": "Evening",
        "exercise_cycling": "Cycling",
        "exercise_walking": "Walking",
        "exercise_running": "Running",
        "exercise_workout": "Workout",
        "exercise_yoga": "Yoga",
        "exercise_swimming": "Swimming",
        "exercise_other": "Exercise",
        "default_user": "User",
        "default_name": "Demo User",
        "condition_tip_balanced": "Balanced meals, consistent routines, and steady daily movement",
        "condition_tip_gallstones": "Low fat ({fat_min}-{fat_max}g/day), high fiber (≥{fiber_min}g/day), and regular meals",
        "condition_tip_diabetes": "Moderate carbs, steady blood sugar, high fiber, and balanced portions",
        "condition_tip_hypertension": "Low sodium (<2000mg/day), high potassium, and high fiber",
        "condition_tip_fat_loss": "Higher protein, controlled fat, quality carbs, and regular training",
        "fallback_comment_fat_ok": "Fat intake at {value:.1f}g stayed within the target range, which supports your goal well.",
        "fallback_comment_fat_low": "Fat intake was only {value:.1f}g, a bit lower than planned. A modest amount of healthy fat would help.",
        "fallback_comment_fat_high": "Fat intake reached {value:.1f}g, which is above target. Keep tomorrow lower-fat and simpler.",
        "fallback_comment_fiber_ok": "Fiber reached {value:.1f}g, which is a strong result for today.",
        "fallback_comment_fiber_low": "Fiber was only {value:.1f}g. Add more vegetables, beans, and whole grains tomorrow.",
        "fallback_comment_water_ok": "Hydration hit {value}ml and met the target.",
        "fallback_comment_water_low": "Hydration was only {value}ml, still short of the {target}ml target.",
        "fallback_comment_steps_high": "You reached {value} steps today, which is a strong activity level.",
        "fallback_comment_steps_mid": "You reached {value} steps today. Solid progress, but there is still room to move more.",
        "fallback_comment_steps_low": "You only logged {value} steps today. Add a walk or a short ride tomorrow.",
        "shortcoming_fat_low": "fat too low",
        "shortcoming_fat_high": "fat too high",
        "shortcoming_fiber_low": "fiber too low",
        "shortcoming_water_low": "water intake too low",
        "shortcoming_exercise_low": "exercise too low",
        "fallback_diet_1": "Breakfast (5 min): oatmeal + 2 egg whites + cucumber salad (300kcal)",
        "fallback_diet_2": "Lunch (10 min): rice + lean beef + steamed greens (450kcal)",
        "fallback_diet_3": "Dinner (10 min): mixed-grain porridge + tofu salad + sauteed vegetables (350kcal)",
        "fallback_water_1": "07:30 warm water after waking, 300ml",
        "fallback_water_2": "10:00 work-break water, 400ml",
        "fallback_water_3": "14:00 afternoon water, 400ml",
        "fallback_water_4": "17:00 before leaving work, 400ml",
        "fallback_water_5": "20:00 evening water, 300ml",
        "fallback_water_target": "Daily target: {target}ml",
        "fallback_exercise_1": "15-minute walk after breakfast",
        "fallback_exercise_2": "20-minute walk after dinner",
        "fallback_exercise_3": "Weekly goal: reach 150 active minutes",
        "fallback_note_fruits": "Suggested fruit today: {fruits}",
        "fallback_note_overeat": "There were signs of overeating yesterday. Keep meals around 70% fullness today.",
        "fallback_note_fat_low": "Fat was low yesterday. Add a small amount of healthy fat such as olive oil or nuts.",
        "fallback_note_fat_high": "Fat was high yesterday. Avoid deep-fried food, rich sauces, and heavy desserts today.",
        "fallback_note_fiber_low": "Fiber was low yesterday. Add more vegetables, beans, and whole grains today.",
        "fallback_note_exercise_low": "Activity was low yesterday. Schedule one light-to-moderate session today.",
        "weekly_ai_failed": "AI call failed: {error}",
        "weekly_fallback_review": "Weekly data collection completed. The overall trend looks stable. Keep building consistency.",
        "weekly_fallback_plan_1": "Keep daily hydration at or above 2000ml",
        "weekly_fallback_plan_2": "Add light movement after meals",
        "weekly_fallback_plan_3": "Keep fat intake controlled and meals regular",
    },
}

JA_TEXT_OVERRIDES: Dict[str, str] = {
    "security_warning_title": "セキュリティ警告",
    "env_validation_failed": "環境チェックに失敗しました",
    "env_missing_memory_dir": "エラー: MEMORY_DIR が設定されていません（必須）。",
    "env_set_memory_dir": "config/.env に MEMORY_DIR='/path/to/memory' を設定してください。ClawHub 手動アップロード時は config/user_config.example.json の env ブロックを参照してください。",
    "env_memory_dir_missing": "エラー: MEMORY_DIR が存在しません: {path}",
    "env_memory_dir_unreadable": "エラー: MEMORY_DIR を読み取れません: {path}",
    "env_no_webhooks": "警告: Webhook が未設定のため、レポートはローカル PDF のみ生成されます。",
    "env_webhook_hint": "配信が必要な場合は DINGTALK_WEBHOOK / FEISHU_WEBHOOK / TELEGRAM_* を設定してください。",
    "program_exit": "安全に終了しました。上記を修正してから再実行してください。",
    "config_load_failed": "警告: 設定ファイルの読み込みに失敗しました - {error}",
    "ai_comment_timeout": "AI コメント生成がタイムアウトしました（{attempt} 回目）。再試行します...",
    "ai_comment_failed": "AI コメント生成に失敗しました（{attempt} 回目）: {error}",
    "ai_plan_timeout": "AI プラン生成がタイムアウトしました（{attempt} 回目）。再試行します...",
    "ai_plan_failed": "AI プラン生成に失敗しました（{attempt} 回目）: {error}",
    "tavily_failed": "Tavily 検索に失敗しました（{attempt} 回目）: {error}",
    "exercise_score_failed": "警告: 運動スコアの計算に失敗しました - {error}",
    "daily_report_title": "健康日報",
    "weekly_report_title": "健康週報",
    "monthly_report_title": "健康月報",
    "daily_report_heading": "{date} 健康レポート",
    "weekly_text_heading": "{start_date} から {end_date} の健康週報",
    "overall_score_title": "今日の総合評価",
    "item_summary_title": "項目別サマリー",
    "ai_comment_title": "AI コメント",
    "details_title": "本日の詳細サマリー",
    "render_notice_title": "レンダリング説明",
    "meal_section": "食事詳細",
    "water_section": "飲水詳細",
    "exercise_section": "運動詳細",
    "next_day_plan_title": "翌日の実行プラン（AI 動的生成）",
    "diet_label": "食事コンプライアンス",
    "water_label": "水分達成度",
    "weight_label": "体重管理",
    "symptom_label": "症状管理",
    "exercise_label": "運動管理",
    "adherence_label": "健康ルーティン遵守",
    "score_total_label": "合計",
    "base_score_label": "基本点",
    "exercise_bonus_label": "運動加点",
    "fat_in_range": "脂質摂取は目標範囲内です",
    "fat_low": "脂質摂取がやや少なめです ({value:.1f}g)",
    "fat_high": "脂質摂取が多すぎます ({value:.1f}g)",
    "protein_ok": "たんぱく質は十分です",
    "protein_low": "たんぱく質が不足しています",
    "completion_status": "{current}ml / {target}ml、達成率 {percent}%",
    "weight_status": "朝の空腹時: {weight}、BMI: {bmi:.1f}",
    "no_symptoms": "症状なし",
    "symptoms_prefix": "症状: {symptoms}",
    "adherence_status": "{meals} 食分を記録、水分は {water_status}",
    "water_goal_met": "達成",
    "water_goal_not_met": "未達成",
    "no_record": "記録なし",
    "no_detail_record": "詳細記録なし",
    "not_recorded": "未記録",
    "not_available": "-",
    "morning_fasting": "朝の空腹時",
    "weight_target": "目標体重: {weight}",
    "bmi_reference": "18.5-24.0（標準）",
    "recommended_calories_reference": "{condition} 向け推奨摂取量",
    "fiber_reference": "食物繊維の目標値",
    "expert_ai_insights": "専門 AI コメント",
    "daily_baseline_data": "本日の基礎データ",
    "daily_nutrition_breakdown": "当日の栄養摂取内訳",
    "daily_water_details": "飲水詳細",
    "daily_meal_details": "食事詳細",
    "daily_exercise_details": "運動詳細",
    "extra_monitoring_records": "追加モニタリング記録",
    "risk_alerts": "リスクアラート",
    "no_risk": "現時点で明確な高リスク項目は見当たりません。安定した生活リズムを維持してください。",
    "action_plan": "翌日の実行プラン",
    "diet_plan": "食事プラン",
    "water_plan": "水分プラン",
    "exercise_plan": "運動プラン",
    "special_attention": "特記事項",
    "generated_at": "生成時刻: {timestamp}",
    "pdf_saved_local": "PDF をローカルに保存しました。",
    "pdf_local_path": "ローカル保存先: {path}",
    "pdf_copied": "PDF を公開ディレクトリへコピーしました: {path}",
    "pdf_download_url": "ダウンロード URL: {url}",
    "pdf_generation_failed": "PDF 生成に失敗しました - {error}",
    "meal_total": "合計 {calories:.0f} kcal",
    "no_water_today": "本日の飲水記録はありません",
    "no_meals_today": "本日の食事記録はありません",
    "no_food_detail": "食事の詳細記録はありません",
    "no_exercise_today": "本日の運動記録はありません",
    "risk_label": "リスク: {value}",
    "advice_label": "対応: {value}",
    "nutrition_chart_center": "{calories}\nkcal",
    "water_chart_center": "{current}\n/ {target}ml",
    "water_chart_total": "合計 {amount}",
    "today_steps": "今日の歩数",
    "step_progress": "{current} / {target} 歩",
    "calories_unit": "{value} kcal",
    "minutes_unit": "{value}分",
    "steps_unit": "{value}歩",
    "distance_unit_km": "{value}km",
    "metric": "指標",
    "value": "値",
    "reference_range": "目標範囲",
    "height": "身長",
    "weight": "体重",
    "bmi": "BMI",
    "bmr": "基礎代謝",
    "tdee": "推定消費カロリー",
    "recommended_calories": "推奨カロリー",
    "protein": "たんぱく質",
    "fat": "脂質",
    "carb": "炭水化物",
    "fiber": "食物繊維",
    "nutrient": "栄養素",
    "actual_intake": "実際の摂取量",
    "recommended_intake": "推奨量",
    "food_name": "食品名",
    "portion": "量",
    "calories": "カロリー",
    "duration": "時間",
    "distance": "距離",
    "burn": "消費",
    "status": "状態",
    "dimension": "項目",
    "score": "スコア",
    "stars": "評価",
    "achieved": "達成",
    "under_target": "未達成",
    "normal": "正常",
    "attention": "注意",
    "symptom_free": "症状なし",
    "has_symptoms": "症状あり",
    "needs_boost": "強化が必要",
    "excellent": "優秀",
    "fair": "標準",
    "good": "良好",
    "needs_improvement": "要改善",
    "average_weight": "平均体重",
    "average_calories": "平均摂取カロリー",
    "average_water": "平均飲水量",
    "average_steps": "平均歩数",
    "health_status": "健康状態",
    "stable": "安定",
    "down": "減少",
    "up": "増加",
    "active": "良好",
    "low": "低め",
    "weekly_overview_title": "今週の健康指標サマリー",
    "weekly_trend_title": "主要トレンド分析",
    "weekly_ai_review_title": "専門 AI 深掘りレビュー",
    "weekly_next_plan_title": "来週の介入プラン",
    "weekly_rings_center": "今週の\n健康達成度",
    "weekly_ring_diet": "食事達成度",
    "weekly_ring_water": "飲水達成度",
    "weekly_ring_exercise": "運動達成度",
    "weekly_ring_label": "{label} {percent:.0f}%",
    "target_line": "目標: {target}",
    "weight_trend_title": "週間体重トレンド ({unit})",
    "calorie_trend_title": "週間カロリー摂取 (kcal)",
    "step_trend_title": "週間歩数トレンド (歩)",
    "water_trend_title": "週間飲水トレンド (ml)",
    "weekly_nutrition_center": "平均摂取量\n{calories} kcal",
    "weekly_chart_weight_label": "体重トレンド",
    "weekly_chart_calorie_label": "カロリートレンド",
    "weekly_chart_nutrition_label": "栄養構成",
    "weekly_chart_step_label": "歩数トレンド",
    "weekly_chart_water_label": "飲水トレンド",
    "weekly_period": "期間: {start_date} から {end_date} | 対象者: {name}",
    "weekly_summary_title": "今週の要点",
    "weekly_review_section": "今週のレビュー",
    "weekly_plan_section": "来週の計画",
    "weekly_avg_weight_change": "平均体重変化: {value}",
    "weekly_avg_calories_line": "平均摂取カロリー: {value:.0f} kcal",
    "weekly_avg_water_line": "平均飲水量: {value:.0f} ml",
    "weekly_avg_steps_line": "平均歩数: {value:.0f} 歩",
    "weekly_symptom_count_line": "症状出現回数: {value}",
    "weekly_generated_at": "生成時刻: {value}",
    "weekly_anchor_date": "基準日: {value}",
    "delivery_daily_pdf": "PDF 日報",
    "delivery_weekly_pdf": "PDF 週報",
    "delivery_monthly_pdf": "PDF 月報",
    "delivery_download": "ダウンロード",
    "delivery_period": "レポート期間",
    "font_missing_english_fallback": "{path} が見つからないため英語フォールバックでレンダリングしました。日本語 PDF が必要な場合は {url} を参照してフォントを配置してください。",
    "condition_balanced": "バランス健康管理",
    "condition_gallstones": "胆石管理",
    "condition_diabetes": "糖尿病管理",
    "condition_hypertension": "高血圧管理",
    "condition_fat_loss": "減脂管理",
    "meal_breakfast": "朝食",
    "meal_lunch": "昼食",
    "meal_dinner": "夕食",
    "meal_snack": "間食",
    "water_wake_up": "起床後",
    "water_morning": "午前",
    "water_noon": "正午",
    "water_afternoon": "午後",
    "water_evening": "夜",
    "exercise_cycling": "サイクリング",
    "exercise_walking": "ウォーキング",
    "exercise_running": "ランニング",
    "exercise_workout": "トレーニング",
    "exercise_yoga": "ヨガ",
    "exercise_swimming": "水泳",
    "exercise_other": "その他の運動",
    "default_user": "ユーザー",
    "default_name": "未設定",
    "condition_tip_balanced": "バランスのよい食事、水分補給、軽い運動を安定して継続しましょう。",
    "condition_tip_gallstones": "脂質は 1 日 {fat_min}-{fat_max}g に抑え、食物繊維は {fiber_min}g 以上、少量多回数を意識してください。",
    "condition_tip_diabetes": "炭水化物を分散し、食物繊維を増やし、食後の活動量を確保してください。",
    "condition_tip_hypertension": "塩分を控え、十分な水分と軽い有酸素運動を継続してください。",
    "condition_tip_fat_loss": "適度なカロリー赤字を保ちつつ、高たんぱく・低脂質・継続的な活動を意識してください。",
    "fallback_comment_fat_ok": "脂質摂取 {value:.1f}g は目標範囲内で、現在の方針と整合しています。",
    "fallback_comment_fat_low": "脂質摂取 {value:.1f}g はやや低めです。極端な制限は避け、必要量は確保しましょう。",
    "fallback_comment_fat_high": "脂質摂取 {value:.1f}g は高めです。明日は調理油と高脂肪食品を控えましょう。",
    "fallback_comment_fiber_ok": "食物繊維 {value:.1f}g は良好です。",
    "fallback_comment_fiber_low": "食物繊維 {value:.1f}g は不足しています。野菜、豆類、全粒穀物を増やしましょう。",
    "fallback_comment_water_ok": "飲水量 {value}ml は達成しています。よくできています。",
    "fallback_comment_water_low": "飲水量 {value}ml は目標 {target}ml に届いていません。こまめな補水を意識しましょう。",
    "fallback_comment_steps_high": "歩数 {value} 歩で活動量は十分です。",
    "fallback_comment_steps_mid": "歩数 {value} 歩で基準はおおむね満たしていますが、まだ伸ばせます。",
    "fallback_comment_steps_low": "歩数 {value} 歩は少なめです。明日は短い散歩を追加しましょう。",
    "shortcoming_fat_low": "脂質不足",
    "shortcoming_fat_high": "脂質過多",
    "shortcoming_fiber_low": "食物繊維不足",
    "shortcoming_water_low": "飲水不足",
    "shortcoming_exercise_low": "運動不足",
    "fallback_diet_1": "朝食 08:00-09:00: オートミール + ゆで卵 2 個 + 低脂肪乳",
    "fallback_diet_2": "昼食 12:00-13:00: 鶏むね肉 + 野菜 + 半量の主食",
    "fallback_diet_3": "夕食 18:00-19:00: 蒸し魚または豆腐 + 野菜スープ + 少量の主食",
    "fallback_water_1": "07:30 起床後に 300ml",
    "fallback_water_2": "10:00 午前中に 400ml",
    "fallback_water_3": "14:00 午後に 400ml",
    "fallback_water_4": "17:00 夕方に 400ml",
    "fallback_water_5": "20:00 夜に 300ml",
    "fallback_water_target": "目標合計: {target}ml",
    "fallback_exercise_1": "朝に 15 分の軽いウォーキング",
    "fallback_exercise_2": "夕食後に 20 分の散歩",
    "fallback_exercise_3": "今週の目標: 中強度運動 150 分",
    "fallback_note_fruits": "明日の推奨果物: {fruits}",
    "fallback_note_overeat": "昨日は食べ過ぎ傾向がありました。明日は量と脂質を抑えめにしてください。",
    "fallback_note_fat_low": "昨日は脂質が少なすぎました。健康的な脂質を少量追加してください。",
    "fallback_note_fat_high": "昨日は脂質が高めでした。揚げ物と高脂肪食品を控えてください。",
    "fallback_note_fiber_low": "昨日は食物繊維が不足しました。野菜・豆類・全粒穀物を追加してください。",
    "fallback_note_exercise_low": "昨日は活動量が少なめでした。明日は軽い運動を 1 回追加してください。",
    "weekly_ai_failed": "AI 呼び出しに失敗しました: {error}",
    "weekly_fallback_review": "今週の記録は安定して蓄積されています。継続性を保つことが最優先です。",
    "weekly_fallback_plan_1": "毎日 2000ml 以上の飲水を維持する",
    "weekly_fallback_plan_2": "食後の軽い運動を追加する",
    "weekly_fallback_plan_3": "脂質量を安定してコントロールする",
}

TEXTS["ja-JP"] = dict(TEXTS["en-US"])
TEXTS["ja-JP"].update(JA_TEXT_OVERRIDES)

INLINE_JA_EXACT = {
    "来源：LLM 动态生成": "出典: LLM 動的生成",
    "来源：本地规则": "出典: ローカルルール",
    "来源：Tavily 检索 + 本地规则": "出典: Tavily 検索 + ローカルルール",
    "个人信息": "個人情報",
    "本周要点": "今週の要点",
    "平均综合评分": "平均総合評価",
    "周均综合评分": "週平均総合評価",
    "平均摄入热量": "平均摂取カロリー",
    "平均饮水量": "平均飲水量",
    "平均步数": "平均歩数",
    "饮食达标天数": "食事達成日数",
    "饮水达标天数": "飲水達成日数",
    "步数达标天数": "歩数達成日数",
    "步数进度": "歩数進捗",
    "症状出现次数": "症状出現回数",
    "本周最佳日": "今週のベスト日",
    "重点复盘日": "重点レビュー日",
    "年龄": "年齢",
    "身高": "身長",
    "当前体重": "現在体重",
    "目标体重": "目標体重",
    "饮水目标": "飲水目標",
    "步数目标": "歩数目標",
    "用药记录天数": "服薬記録日数",
    "用药天数": "服薬日数",
    "监测天数": "モニタリング日数",
    "项目": "項目",
    "内容": "内容",
    "监测人": "対象者",
    "管理目标": "管理目標",
    "年龄/身高": "年齢 / 身長",
    "当前/目标体重": "現在 / 目標体重",
    "饮水/步数目标": "飲水 / 歩数目標",
    "本周亮点与重点": "今週のハイライトと重点",
    "本周亮点": "今週の良かった点",
    "待改进项": "改善が必要な項目",
    "下周重点": "来週の重点",
    "额外监测项目": "追加モニタリング項目",
    "记录天数": "記録日数",
    "条目数": "件数",
    "需结合复盘": "あわせて振り返りが必要",
    "健康月报": "健康月報",
    "渲染说明": "レンダリング説明",
    "周期": "期間",
    "未配置": "未設定",
    "月度概览": "月次概要",
    "本月亮点": "今月のハイライト",
    "专项趋势": "病態別トレンド",
    "宏观依从性与状态全景": "マクロ遵守率と状態の全体像",
    "专科病理深度对齐": "病態別ディープダイブ",
    "附加监测模块": "追加モニタリングモジュール",
    "专家会诊与医疗规划": "専門レビューと医療プラン",
    "未配置常居地": "居住地未設定",
    "姓名": "氏名",
    "常居地": "居住地",
    "AI 月度病情研判": "AI 月次レビュー",
    "复查提醒": "再診・再検査リマインド",
    "医院与门诊建议": "病院・外来受診の提案",
    "Additional Monitoring": "追加モニタリング",
    "Hospital and Clinic Suggestions": "病院・外来受診の提案",
    "Macro Overview": "マクロ全体像",
    "Specialty Deep Dive": "病態別ディープダイブ",
    "Medical Action Plan": "医療アクションプラン",
    "Weight And BMR Trend": "体重と基礎代謝の推移",
    "Healthy days": "健康達成日",
    "Diet": "食事",
    "Hydration": "飲水",
    "Exercise": "運動",
    "Medication": "服薬",
    "Monitoring": "モニタリング",
}

INLINE_JA_PREFIXES = {
    "报告生成时间：": "レポート生成時刻：",
    "评估周期：": "評価期間：",
    "监测人：": "対象者：",
    "医院等级：": "病院ランク：",
    "医院优势：": "病院の強み：",
    "医院地址：": "所在地：",
    "挂号方式：": "予約方法：",
    "推荐科室：": "推奨診療科：",
    "推荐医生：": "推奨医師：",
    "医生擅长：": "医師の専門：",
    "挂号费：": "初診費用：",
    "坐诊时间：": "外来日時：",
    "推荐理由：": "推奨理由：",
    "健康无症状：": "健康で無症状：",
    "出现不适：": "不調あり：",
}

INLINE_JA_SUFFIXES = {
    "（首推）": "（最優先）",
}

INLINE_JA_REPLACEMENTS = {
    "健康月报": "健康月報",
    "健康周报": "健康週報",
    "健康日报": "健康日報",
    "饮食": "食事",
    "饮水": "飲水",
    "步数": "歩数",
    "运动": "運動",
    "活动": "活動",
    "医院等级：": "病院ランク：",
    "医院优势：": "病院の強み：",
    "医院地址：": "所在地：",
    "挂号方式：": "予約方法：",
    "推荐科室：": "推奨診療科：",
    "推荐医生：": "推奨医師：",
    "医生擅长：": "医師の専門：",
    "挂号费：": "初診費用：",
    "坐诊时间：": "外来日時：",
    "推荐理由：": "推奨理由：",
    "用药": "服薬",
    "监测": "モニタリング",
    "记录": "記録",
    "条目": "項目",
    "稳定": "安定",
    "用药日": "服薬日",
    "轻度症状": "軽度症状",
    "明显症状": "明確な症状",
    "体重与基础代谢趋势": "体重と基礎代謝の推移",
    "浅色为每日体重，深色为 7 日移动平均，橙色虚线为按当前体重估算的基础代谢。": "淡色は日々の体重、濃色は 7 日移動平均、オレンジの破線は現在体重から推定した基礎代謝です。",
    "热力图右上角 “M” 表示该日有用药记录。": "ヒートマップ右上の「M」は、その日に服薬記録があることを示します。",
    "热力图右上角 M 表示该日有用药记录。": "ヒートマップ右上の M は、その日に服薬記録があることを示します。",
    "指标": "指標",
    "结果": "結果",
    "饮食达标率": "食事達成率",
    "饮水达标率": "飲水達成率",
    "运动达标率": "運動達成率",
    "用药覆盖率": "服薬カバー率",
    "监测覆盖率": "モニタリングカバー率",
    "症状天数": "症状日数",
    "月均综合评分": "月平均総合評価",
    "体重 (kg)": "体重 (kg)",
    "基础代谢 (kcal)": "基礎代謝 (kcal)",
    "每日体重": "日次体重",
    "7 日均线": "7 日平均線",
    "估算基础代谢": "推定基礎代謝",
    "健康达标": "健康達成",
    "脂肪": "脂質",
    "碳水": "炭水化物",
    "脂肪波动": "脂質のばらつき",
    "碳水波动": "炭水化物のばらつき",
    "脂肪摄入": "脂質摂取",
    "症状次数": "症状回数",
    "收缩压": "収縮期血圧",
    "舒张压": "拡張期血圧",
    "体脂率 (%)": "体脂肪率 (%)",
    "当前没有足够的居住地或检索信息来生成医院名单。请在 user_config.json 中补充常居地后再生成月报。": "病院候補を生成するための居住地または検索情報が不足しています。user_config.json に居住地を追加してから月報を再生成してください。",
    "医生": "医師",
    "主任医师": "主任医師",
    "副主任医师": "副主任医師",
    "主治医师": "主治医師",
    "教授": "教授",
}

CONDITION_ALIASES = {
    "balanced": {"balanced", "general health", "general wellness", "none", "均衡健康", "无特殊状况"},
    "gallstones": {"gallstones", "gallstone", "胆结石", "胆石", "胆石症", "慢性胆嚢炎"},
    "diabetes": {"diabetes", "diabetic", "糖尿病"},
    "hypertension": {"hypertension", "blood pressure", "high blood pressure", "高血压", "高血圧"},
    "fat_loss": {"fat loss", "fitness", "cutting", "leaning", "健身减脂", "减脂", "減脂", "ボディメイク"},
}
GENDER_ALIASES = {
    "male": {"male", "man", "m", "男", "男性"},
    "female": {"female", "woman", "f", "女", "女性"},
}
MEAL_ALIASES = {
    "breakfast": {"breakfast", "早餐", "朝食"},
    "lunch": {"lunch", "午餐", "昼食"},
    "dinner": {"dinner", "晚餐", "夕食"},
    "snack": {"snack", "snacks", "加餐", "間食"},
}
WATER_PERIOD_ALIASES = {
    "wake_up": {"wake-up", "wake up", "morning wake-up", "晨起", "早晨", "晨间", "起床後", "起床后"},
    "morning": {"morning", "上午", "午前"},
    "noon": {"noon", "midday", "中午", "正午"},
    "afternoon": {"afternoon", "下午", "午後"},
    "evening": {"evening", "night", "晚上", "晚间", "夜"},
}
EXERCISE_ALIASES = {
    "cycling": {"cycling", "bike", "biking", "骑行", "骑车", "サイクリング", "自転車"},
    "walking": {"walking", "walk", "散步", "步行", "散歩", "ウォーキング"},
    "running": {"running", "run", "跑步", "ランニング", "ジョギング"},
    "workout": {"workout", "strength", "training", "健身", "トレーニング", "筋トレ"},
    "yoga": {"yoga", "瑜伽", "ヨガ"},
    "swimming": {"swimming", "swim", "游泳", "水泳"},
    "other": {"exercise", "其他", "其他运动", "運動", "その他の運動"},
}
EXCLUDE_SECTION_KEYWORDS = {
    "weight",
    "体重",
    "体重記録",
    "water",
    "hydration",
    "饮水",
    "飲水",
    "meal",
    "meals",
    "diet",
    "food",
    "饮食",
    "食事",
    "exercise",
    "workout",
    "运动",
    "運動",
    "symptom",
    "symptoms",
    "不适",
    "症状",
    "不調",
    "服薬",
    "goal",
    "target",
    "目标",
    "steps",
    "步数",
    "歩数",
}

LANGUAGE_LABELS = {
    "zh-CN": "中文",
    "en-US": "English",
    "ja-JP": "日本語",
}

CONFIG_WIZARD_TEXTS = {
    "zh-CN": {
        "title": "欢迎使用 Health-Mate 配置向导",
        "intro": "这个向导会在几分钟内生成你的健康档案。",
        "start": "按 Enter 开始...",
        "language_prompt": "请选择语言（1 中文 / 2 English）",
        "language_retry": "请输入 1 或 2。",
        "name": "你的姓名或昵称？",
        "name_retry": "请输入姓名或昵称。",
        "gender": "性别（1 男 / 2 女）",
        "gender_retry": "请输入 1 或 2。",
        "age": "年龄",
        "age_retry": "请输入有效年龄数字。",
        "height": "身高（厘米，如 172）",
        "height_retry": "请输入有效身高数字。",
        "current_weight": "当前体重（公斤，如 65.5）",
        "current_weight_retry": "请输入有效体重数字。",
        "target_weight": "目标体重（公斤）",
        "target_weight_retry": "请输入有效目标体重数字。",
        "condition": "健康目标或状态（1 胆结石 / 2 糖尿病 / 3 高血压 / 4 健身减脂 / 5 均衡健康）",
        "condition_retry": "请输入 1-5。",
        "water_target": "每日饮水目标（ml）",
        "water_target_retry": "请输入有效的饮水目标数字。",
        "step_target": "每日步数目标",
        "step_target_retry": "请输入有效的步数目标数字。",
        "activity": "活动水平（1 久坐 / 2 轻度 / 3 中度 / 4 重度 / 5 运动员）",
        "activity_retry": "请输入 1-5。",
        "dislike": "不喜欢的食物（多个请用逗号分隔，没有可直接回车）",
        "allergies": "过敏食物（多个请用逗号分隔，没有可直接回车）",
        "saved": "配置完成，已写入：{path}",
        "summary": "已保存语言：{language}，健康目标：{condition}。",
        "next_step": "如需推送消息，请参考 config/user_config.example.json 中的 env 配置块，并手动编辑 config/.env 填写 Webhook。",
    },
    "en-US": {
        "title": "Welcome to the Health-Mate setup wizard",
        "intro": "This wizard creates your health profile in a few minutes.",
        "start": "Press Enter to start...",
        "language_prompt": "Choose a language (1 Chinese / 2 English)",
        "language_retry": "Please enter 1 or 2.",
        "name": "Your name or nickname",
        "name_retry": "Please enter a name or nickname.",
        "gender": "Gender (1 Male / 2 Female)",
        "gender_retry": "Please enter 1 or 2.",
        "age": "Age",
        "age_retry": "Please enter a valid age.",
        "height": "Height in cm (for example 172)",
        "height_retry": "Please enter a valid height.",
        "current_weight": "Current weight in kg (for example 65.5)",
        "current_weight_retry": "Please enter a valid weight.",
        "target_weight": "Target weight in kg",
        "target_weight_retry": "Please enter a valid target weight.",
        "condition": "Condition or goal (1 Gallstones / 2 Diabetes / 3 Hypertension / 4 Fat Loss / 5 Balanced Wellness)",
        "condition_retry": "Please enter a number from 1 to 5.",
        "water_target": "Daily water target in ml",
        "water_target_retry": "Please enter a valid water target.",
        "step_target": "Daily step target",
        "step_target_retry": "Please enter a valid step target.",
        "activity": "Activity level (1 Sedentary / 2 Light / 3 Moderate / 4 Heavy / 5 Athlete)",
        "activity_retry": "Please enter a number from 1 to 5.",
        "dislike": "Foods to avoid (comma-separated, press Enter if none)",
        "allergies": "Allergies (comma-separated, press Enter if none)",
        "saved": "Configuration saved to: {path}",
        "summary": "Saved language: {language}, condition: {condition}.",
        "next_step": "If you want push delivery, review the env block in config/user_config.example.json and then edit config/.env to add your webhooks.",
    },
}

WEIGHT_MORNING_ALIASES = {
    "weight_morning": {
        "晨起空腹",
        "早晨空腹",
        "晨起体重",
        "空腹体重",
        "morning fasting",
        "fasting weight",
        "morning weight",
        "fasting body weight",
        "朝空腹",
        "朝の空腹時",
        "朝の体重",
    }
}

WATER_AMOUNT_ALIASES = {
    "water_amount": {"饮水量", "water intake", "intake", "飲水量", "水分量"},
}

CUMULATIVE_ALIASES = {
    "cumulative": {"累计", "cumulative", "累計"},
}

DISTANCE_ALIASES = {
    "distance": {"距离", "公里数", "distance", "距離"},
}

DURATION_ALIASES = {
    "duration": {"时间", "耗时", "时长", "duration", "time", "時間"},
}

CALORIE_BURN_ALIASES = {
    "burn": {"热量消耗", "消耗", "总消耗", "burn", "calories", "消費"},
}

STEP_LABEL_ALIASES = {
    "steps": {"总步数", "步数", "total steps", "steps", "総歩数", "今日の歩数"},
}

SYMPTOM_SECTION_ALIASES = {
    "symptoms": {"症状", "不适", "symptom", "symptoms", "不調"},
}

TIME_APPROX_PATTERN = r"[\(（](?:约|約|around)?\s*([\d:]+)[\)）]"
OVEREATING_PATTERN = r"(?:吃|感觉).{0,20}?(?:有点饱|过饱|吃撑|吃太饱)|(?:too full|overeat|overate|stuffed)"
SYMPTOM_KEYWORDS = [
    "右上腹涨",
    "腹涨",
    "腹胀",
    "腹痛",
    "涨痛",
    "不舒服",
    "恶心",
    "bloating",
    "nausea",
    "pain",
    "discomfort",
]
PLACEHOLDER_TOKENS = {
    "(待记录)",
    "（待记录）",
    "(待記録)",
    "（待記録）",
    "（記録なし）",
    "(pending)",
    "_（无记录）_",
}
MEAL_SKIP_KEYWORDS = {
    "总计",
    "评估",
    "食事合計",
    "評価",
    "蛋白质：",
    "脂肪：",
    "碳水：",
    "纤维：",
    "维生素",
    "total",
    "assessment",
    "protein:",
    "fat:",
    "carbs:",
    "fiber:",
}
PORTION_UNIT_PATTERN = r"(ml|g|个|個|碗|膳|份|杯|片|本|slice|cup|serving|piece)"
WEIGHT_UNIT_PATTERN = r"(斤|kg|公斤|jin|lbs?|pounds?)"
DISTANCE_UNIT_PATTERN = r"(?:公里|km)"
MINUTE_UNIT_PATTERN = r"(?:分|分钟|min|minutes?)"
CALORIE_UNIT_PATTERN = r"(?:千卡|kcal|卡)"
STEP_UNIT_PATTERN = r"(?:步|歩|steps?)"
APPROXIMATE_MARKERS = {"约", "約", "approx.", "approx"}


def _normalize_token(value: Optional[str]) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def resolve_locale(config: Optional[dict] = None, locale: Optional[str] = None) -> str:
    raw = locale or os.environ.get("HEALTH_MATE_LANG")
    if not raw and config:
        raw = (
            config.get("language")
            or config.get("locale")
            or config.get("user_profile", {}).get("language")
            or config.get("user_profile", {}).get("locale")
        )
    normalized = _normalize_token(raw)
    return LOCALE_ALIASES.get(normalized, raw if raw in SUPPORTED_LOCALES else DEFAULT_LOCALE)


def t(locale: Optional[str], key: str, **kwargs) -> str:
    resolved = resolve_locale(locale=locale)
    template = TEXTS.get(resolved, {}).get(key) or TEXTS[DEFAULT_LOCALE].get(key) or key
    return template.format(**kwargs)


JA_CHARACTER_VARIANTS = str.maketrans(
    {
        "东": "東",
        "动": "動",
        "隐": "隠",
        "个": "個",
        "为": "為",
        "义": "義",
        "书": "書",
        "买": "買",
        "云": "雲",
        "亚": "亜",
        "产": "産",
        "亲": "親",
        "亿": "億",
        "仅": "僅",
        "从": "従",
        "优": "優",
        "价": "価",
        "们": "們",
        "伤": "傷",
        "传": "伝",
        "侧": "側",
        "备": "備",
        "复": "復",
        "头": "頭",
        "妇": "婦",
        "实": "実",
        "审": "審",
        "导": "導",
        "层": "層",
        "岁": "歳",
        "师": "師",
        "带": "帯",
        "应": "応",
        "张": "張",
        "归": "帰",
        "录": "録",
        "总": "総",
        "态": "態",
        "户": "戸",
        "扩": "拡",
        "择": "択",
        "摄": "摂",
        "数": "数",
        "无": "無",
        "时": "時",
        "显": "顕",
        "术": "術",
        "权": "権",
        "构": "構",
        "样": "様",
        "汉": "漢",
        "汤": "湯",
        "测": "測",
        "济": "済",
        "热": "熱",
        "爱": "愛",
        "疗": "療",
        "监": "監",
        "稳": "穏",
        "类": "類",
        "结": "結",
        "综": "総",
        "维": "維",
        "联": "聯",
        "药": "薬",
        "营": "営",
        "补": "補",
        "装": "装",
        "观": "観",
        "觉": "覚",
        "计": "計",
        "认": "認",
        "训": "訓",
        "设": "設",
        "诊": "診",
        "证": "証",
        "评": "評",
        "译": "訳",
        "话": "話",
        "该": "該",
        "语": "語",
        "说": "説",
        "请": "請",
        "调": "調",
        "谋": "謀",
        "谨": "謹",
        "负": "負",
        "贡": "貢",
        "费": "費",
        "资": "資",
        "这": "這",
        "进": "進",
        "远": "遠",
        "适": "適",
        "选": "選",
        "递": "遞",
        "逻": "邏",
        "遗": "遺",
        "销": "銷",
        "锁": "鎖",
        "锻": "鍛",
        "锅": "鍋",
        "阶": "階",
        "际": "際",
        "项": "項",
        "预": "予",
        "颜": "顔",
        "饮": "飲",
        "馆": "館",
        "鱼": "魚",
        "鸡": "鶏",
    }
)

JA_FREE_TEXT_REPLACEMENTS = {
    "东东": "東東",
    "本周": "今週",
    "本月": "今月",
    "右上腹隐痛": "右上腹部痛",
    "活动": "活動",
    "动态": "動的",
    "慢性胆囊炎": "慢性胆嚢炎",
    "胆囊炎": "胆嚢炎",
    "胆囊": "胆嚢",
    "胆结石": "胆石",
    "结石": "結石",
    "综合评分": "総合評価",
    "综合": "総合",
    "评分": "評価",
    "频次": "頻度",
    "次数": "回数",
    "点评": "コメント",
    "日报": "日報",
    "周报": "週報",
    "月报": "月報",
    "报告": "レポート",
    "饮食": "食事",
    "饮水": "飲水",
    "步数": "歩数",
    "运动": "運動",
    "监测": "モニタリング",
    "用药": "服薬",
    "门诊": "外来",
    "医院": "病院",
    "医生": "医師",
    "记录": "記録",
    "条目": "項目",
    "达标率": "達成率",
    "覆盖率": "カバー率",
    "主任医师": "主任医師",
    "副主任医师": "副主任医師",
    "主治医师": "主治医師",
    "推荐": "推奨",
    "建议": "提案",
    "方案": "プラン",
    "风险": "リスク",
    "目标": "目標",
    "复查": "再検査",
    "检索建议：": "外部参考：",
    "运动参考：": "運動メモ：",
    "今日重点围绕 ": "明日の重点: ",
    "检索补充": "検索補足",
}


def localize_free_text(locale: Optional[str], text: Optional[str]) -> str:
    resolved = resolve_locale(locale=locale)
    value = str(text or "")
    if resolved != "ja-JP" or not value:
        return value

    updated = value
    if updated in INLINE_JA_EXACT:
        updated = INLINE_JA_EXACT[updated]
    else:
        for source, target in INLINE_JA_PREFIXES.items():
            if updated.startswith(source):
                updated = target + updated[len(source):]
                break
        for source, target in INLINE_JA_SUFFIXES.items():
            if updated.endswith(source):
                updated = updated[: -len(source)] + target
                break

    for source, target in sorted(INLINE_JA_REPLACEMENTS.items(), key=lambda item: len(item[0]), reverse=True):
        updated = updated.replace(source, target)
    for source, target in sorted(JA_FREE_TEXT_REPLACEMENTS.items(), key=lambda item: len(item[0]), reverse=True):
        updated = updated.replace(source, target)

    updated = updated.translate(JA_CHARACTER_VARIANTS)
    updated = re.sub(r"\s+", " ", updated).strip()
    return updated


def inline_localize(locale: Optional[str], zh_text: str, en_text: str, ja_text: Optional[str] = None) -> str:
    resolved = resolve_locale(locale=locale)
    if resolved == "zh-CN":
        return zh_text
    if resolved == "ja-JP":
        candidate = ja_text if ja_text is not None else zh_text
        localized = localize_free_text(locale, candidate)
        if localized:
            return localized
        return localize_free_text(locale, en_text)
    return en_text


def _canonicalize(value: Optional[str], mapping: Dict[str, Iterable[str]], default: str) -> str:
    token = _normalize_token(value)
    if not token:
        return default
    for canonical, aliases in mapping.items():
        if token == _normalize_token(canonical):
            return canonical
        if any(token == _normalize_token(alias) for alias in aliases):
            return canonical
    return default


def condition_key(value: Optional[str]) -> str:
    return _canonicalize(value, CONDITION_ALIASES, "balanced")


def gender_key(value: Optional[str]) -> str:
    return _canonicalize(value, GENDER_ALIASES, "male")


def meal_key(value: Optional[str]) -> str:
    return _canonicalize(value, MEAL_ALIASES, "snack")


def water_period_key(value: Optional[str]) -> str:
    return _canonicalize(value, WATER_PERIOD_ALIASES, "morning")


def exercise_key(value: Optional[str]) -> str:
    return _canonicalize(value, EXERCISE_ALIASES, "other")


def condition_name(locale: Optional[str], value: Optional[str]) -> str:
    return t(locale, f"condition_{condition_key(value)}")


def meal_name(locale: Optional[str], value: Optional[str]) -> str:
    return t(locale, f"meal_{meal_key(value)}")


def water_period_name(locale: Optional[str], value: Optional[str]) -> str:
    return t(locale, f"water_{water_period_key(value)}")


def exercise_name(locale: Optional[str], value: Optional[str]) -> str:
    return t(locale, f"exercise_{exercise_key(value)}")


def alias_pattern(mapping: Dict[str, Iterable[str]]) -> str:
    values = set()
    for canonical, aliases in mapping.items():
        values.add(canonical)
        values.update(aliases)
    return "|".join(sorted((re.escape(value) for value in values if value), key=len, reverse=True))


def has_excluded_section_keyword(header: str) -> bool:
    token = _normalize_token(header)
    return any(keyword in token for keyword in EXCLUDE_SECTION_KEYWORDS)


def wizard_text(locale: Optional[str], key: str) -> str:
    resolved = resolve_locale(locale=locale)
    return CONFIG_WIZARD_TEXTS.get(resolved, CONFIG_WIZARD_TEXTS[DEFAULT_LOCALE])[key]


def list_separator(locale: Optional[str]) -> str:
    return "、" if resolve_locale(locale=locale) in {"zh-CN", "ja-JP"} else ", "


def and_more(locale: Optional[str]) -> str:
    resolved = resolve_locale(locale=locale)
    if resolved == "zh-CN":
        return "等"
    if resolved == "ja-JP":
        return "など"
    return "and more"


def localized_recipe_query(locale: Optional[str], condition_display: str) -> str:
    resolved = resolve_locale(locale=locale)
    if resolved == "en-US":
        return f"{condition_display} quick low fat high protein meals 2026"
    if resolved == "ja-JP":
        return f"{condition_display} 低脂質 高たんぱく 手軽 レシピ 2026"
    return f"{condition_display} 低脂高蛋白快手菜谱 2026"


def localized_exercise_query(locale: Optional[str], condition_display: str) -> str:
    resolved = resolve_locale(locale=locale)
    if resolved == "en-US":
        return "desk stretching routine for sedentary workers 2026"
    if resolved == "ja-JP":
        return f"座り仕事 向け オフィス ストレッチ {condition_display} に適した運動 2026"
    return f"久坐人群办公室拉伸动作 {condition_display} 适合的运动 2026"


def extract_time_token(text: str) -> str:
    match = re.search(TIME_APPROX_PATTERN, text or "", re.IGNORECASE)
    return match.group(1) if match else ""


def strip_approximate_phrase(value: str) -> str:
    text = str(value or "")
    text = re.sub(r"[(（]\s*(?:约|approx\.?)\s*[)）]", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*(?:约|approx\.?)$", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"[，,]\s*(?:约|approx\.?)\s*[）)]", "）", text, flags=re.IGNORECASE)
    return re.sub(r"[(（]$", "", text).strip()


def strip_parenthetical_details(value: str) -> str:
    text = str(value or "")
    text = re.sub(r"\s*[（(][^（）()]*[)）]\s*", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def markdown_to_plain_text(text: str) -> str:
    plain = str(text or "").replace("\r\n", "\n")
    plain = re.sub(r"(?m)^\s*#{1,6}\s*", "", plain)
    plain = plain.replace("**", "")
    plain = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1: \2", plain)
    plain = re.sub(r"(?m)^\*\s+", "• ", plain)
    return plain.strip()


def weight_unit(locale: Optional[str]) -> str:
    return "斤" if resolve_locale(locale=locale) == "zh-CN" else "kg"


def format_weight(locale: Optional[str], kg_value: Optional[float], precision: int = 1) -> str:
    if kg_value is None:
        return t(locale, "not_recorded")
    if resolve_locale(locale=locale) == "zh-CN":
        return f"{kg_value * 2:.{precision}f}斤"
    return f"{kg_value:.{precision}f}kg"


def format_weight_delta(locale: Optional[str], kg_value: float, precision: int = 1) -> str:
    if resolve_locale(locale=locale) == "zh-CN":
        return f"{kg_value * 2:.{precision}f}斤"
    return f"{kg_value:.{precision}f}kg"


def convert_weight_to_kg(value: float, unit: str, assume_jin: bool = False) -> float:
    token = _normalize_token(unit)
    if token in {"斤", "jin"}:
        return value / 2
    if token in {"lb", "lbs", "pound", "pounds"}:
        return value / 2.2046226218
    if token in {"kg", "kilogram", "kilograms", "公斤"}:
        return value
    return value / 2 if assume_jin else value


def build_condition_tip(locale: Optional[str], condition: Optional[str], fat_min: float, fat_max: float, fiber_min: float) -> str:
    return t(locale, f"condition_tip_{condition_key(condition)}", fat_min=int(fat_min), fat_max=int(fat_max), fiber_min=int(fiber_min))


def build_ai_comment_prompt(locale: Optional[str], context: dict) -> str:
    resolved = resolve_locale(locale=locale)
    if resolved == "en-US":
        return f"""You are a professional personal nutrition coach. Review the following daily health data and write a warm but rigorous insight.

[Profile]
- Name: {context['user_name']}
- Condition / goal: {context['condition_name']}
- Nutrition principle: {context['diet_principle']}

[Today's data]
- Calories: {context['calories']:.0f} kcal
- Protein: {context['protein']:.1f}g
- Fat: {context['fat']:.1f}g (target: {context['fat_min']}-{context['fat_max']}g)
- Carbs: {context['carb']:.1f}g
- Fiber: {context['fiber']:.1f}g (target: >= {context['fiber_min']}g)
- Water: {context['water_total']}ml (target: {context['water_target']}ml)
- Exercise sessions: {context['exercise_count']}
- Steps: {context['steps']}
- Overeating factor: {context['overeating_factor']}
- Symptom keywords: {context['symptom_keywords']}

[Requirements]
1. Sound like a professional private nutrition coach.
2. Start with what went well, then call out the main health risks clearly.
3. Write at least 120 words.
4. Tie the advice to the user's condition or goal.
5. If there was overeating or symptoms, emphasize it.

Output only the insight text with no title or code block."""
    if resolved == "ja-JP":
        return f"""あなたはプロのパーソナル栄養コーチです。以下の1日分の健康データを確認し、専門的で温かみのあるコメントを書いてください。

[プロフィール]
- 名前: {context['user_name']}
- 管理目標 / 病態: {context['condition_name']}
- 食事方針: {context['diet_principle']}

[本日のデータ]
- 総摂取カロリー: {context['calories']:.0f} kcal
- たんぱく質: {context['protein']:.1f}g
- 脂質: {context['fat']:.1f}g (目標: {context['fat_min']}-{context['fat_max']}g)
- 炭水化物: {context['carb']:.1f}g
- 食物繊維: {context['fiber']:.1f}g (目標: {context['fiber_min']}g 以上)
- 飲水量: {context['water_total']}ml (目標: {context['water_target']}ml)
- 運動回数: {context['exercise_count']}
- 歩数: {context['steps']}
- 食べ過ぎ係数: {context['overeating_factor']}
- 症状キーワード: {context['symptom_keywords']}

[出力要件]
1. 専門的でやわらかい口調にしてください。
2. まず良かった点、そのあとに注意点を書いてください。
3. 160〜260字程度にまとめてください。
4. 管理目標や病態に必ず結び付けてください。
5. 食べ過ぎや症状がある場合は、明確に触れてください。

タイトルやコードブロックは不要です。本文だけを出力してください。"""
    return f"""你是一位专业的私人营养师。请根据以下每日健康数据，输出一段专业但温暖的健康点评。

【用户档案】
- 称呼：{context['user_name']}
- 病理/目标：{context['condition_name']}
- 饮食原则：{context['diet_principle']}

【今日数据】
- 总热量：{context['calories']:.0f} kcal
- 蛋白质：{context['protein']:.1f}g
- 脂肪：{context['fat']:.1f}g（目标：{context['fat_min']}-{context['fat_max']}g）
- 碳水：{context['carb']:.1f}g
- 膳食纤维：{context['fiber']:.1f}g（目标：≥{context['fiber_min']}g）
- 饮水：{context['water_total']}ml（目标：{context['water_target']}ml）
- 运动次数：{context['exercise_count']}
- 步数：{context['steps']}
- 过饱系数：{context['overeating_factor']}
- 症状关键词：{context['symptom_keywords']}

【要求】
1. 语气专业、温暖、明确。
2. 先肯定亮点，再指出主要隐患。
3. 不少于 120 字。
4. 必须结合用户病理或目标。
5. 如果出现过饱或症状，需要重点提醒。

请直接输出点评正文，不要加标题或代码块。"""


def build_ai_comment_system_prompt(locale: Optional[str], condition: Optional[str]) -> str:
    resolved = resolve_locale(locale=locale)
    if resolved == "en-US":
        return f"You are a professional nutrition coach specialized in {condition_name(locale, condition)}."
    if resolved == "ja-JP":
        return f"あなたは {condition_name(locale, condition)} の支援を得意とするプロの栄養コーチです。"
    return f"你是一位专业营养师，擅长为{condition_name(locale, condition)}用户提供指导。"


def build_ai_plan_prompt(locale: Optional[str], context: dict) -> str:
    resolved = resolve_locale(locale=locale)
    shortcomings = ", ".join(context["shortcomings"]) if context["shortcomings"] else ("none" if resolved == "en-US" else "なし" if resolved == "ja-JP" else "无")
    if resolved == "en-US":
        return f"""You are a professional health planner. Build tomorrow's action plan for the user below.

[Profile]
- Name: {context['user_name']}
- Condition / goal: {context['condition_name']}
- Nutrition principle: {context['diet_principle']}
- Foods to avoid: {context['avoid_foods'] or 'none'}
- Preferred fruits: {context['favorite_fruits'] or 'none'}

[Today's gaps]
- {shortcomings}

[Search references]
- Recipe notes: {context['recipe_reference']}
- Exercise notes: {context['exercise_reference']}

[Output rules]
Return one valid JSON object only. Do not add markdown or commentary.
The JSON schema must be:
{{
  "diet": [{{"time": "08:00-09:00", "meal": "Breakfast", "menu": "Oatmeal and fruit", "calories": 300, "fat": 6, "fiber": 7}}],
  "water": [{{"time": "07:00-08:00", "amount": "300ml", "note": "Warm water after waking"}}],
  "exercise": [{{"time": "After dinner", "activity": "Walk", "duration": "20 minutes", "details": "Light digestion walk"}}],
  "notes": ["One key reminder"]
}}
Write the plan for {context['condition_name']} and keep it realistic and actionable."""
    if resolved == "ja-JP":
        return f"""あなたはプロの健康プランナーです。以下の情報をもとに、明日実行できる具体的な計画を作成してください。

[プロフィール]
- 名前: {context['user_name']}
- 管理目標 / 病態: {context['condition_name']}
- 食事方針: {context['diet_principle']}
- 避けたい食品: {context['avoid_foods'] or 'なし'}
- 好きな果物: {context['favorite_fruits'] or 'なし'}

[本日の課題]
- {shortcomings}

[検索参考]
- レシピ参考: {context['recipe_reference']}
- 運動参考: {context['exercise_reference']}

[出力ルール]
有効な JSON オブジェクトを1つだけ返してください。Markdown や説明文は不要です。
JSON スキーマは必ず次の形にしてください:
{{
  "diet": [{{"time": "08:00-09:00", "meal": "朝食", "menu": "オートミールと果物", "calories": 300, "fat": 6, "fiber": 7}}],
  "water": [{{"time": "07:00-08:00", "amount": "300ml", "note": "起床後の白湯"}}],
  "exercise": [{{"time": "夕食後", "activity": "散歩", "duration": "20分", "details": "軽い消化サポートの散歩"}}],
  "notes": ["重要な一言メモ"]
}}
{context['condition_name']} に合わせて、現実的で続けやすい内容にしてください。"""
    return f"""你是一位专业健康规划师。请根据以下信息生成用户明日优化方案。

【用户档案】
- 称呼：{context['user_name']}
- 病理/目标：{context['condition_name']}
- 饮食原则：{context['diet_principle']}
- 不爱吃/过敏：{context['avoid_foods'] or '无'}
- 喜欢水果：{context['favorite_fruits'] or '无'}

【今日短板】
- {shortcomings}

【搜索参考】
- 菜谱参考：{context['recipe_reference']}
- 运动参考：{context['exercise_reference']}

【输出规则】
必须只输出一个合法 JSON 对象，绝对不要输出 Markdown 或解释。
格式必须如下：
{{
  "diet": [{{"time": "08:00-09:00", "meal": "早餐", "menu": "燕麦粥等", "calories": 300, "fat": 6, "fiber": 7}}],
  "water": [{{"time": "07:00-08:00", "amount": "300ml", "note": "晨起温水"}}],
  "exercise": [{{"time": "晚餐后", "activity": "散步", "duration": "20分钟", "details": "轻度助消化活动"}}],
  "notes": ["一条重点提醒"]
}}
请输出适用于{context['condition_name']}的明日方案。"""


def build_ai_plan_system_prompt(locale: Optional[str]) -> str:
    resolved = resolve_locale(locale=locale)
    if resolved == "en-US":
        return "You are a professional nutrition coach. Output one pure JSON object only."
    if resolved == "ja-JP":
        return "あなたはプロの健康コーチです。純粋な JSON オブジェクトを1つだけ出力してください。"
    return "你是一位专业营养师。你只能输出一个纯 JSON 对象。"


def build_weekly_ai_prompt(locale: Optional[str], context: dict) -> str:
    resolved = resolve_locale(locale=locale)
    if resolved == "en-US":
        return f"""You are a professional weekly health reviewer. Based on the aggregated 7-day health data below, write a grounded weekly review and a next-week action plan.

Profile summary: {context.get('profile_summary', 'N/A')}
Managed conditions / goals: {context.get('condition_name', 'General health management')}
Primary goal: {context.get('primary_condition', 'General health management')}
Diet principle: {context.get('diet_principle', 'Keep a steady and balanced routine')}
Hydration target: {context.get('water_target', 2000)} ml
Step target: {context.get('step_target', 8000)}

[Weekly summary]
- Weight change: {context.get('weight_change', 'N/A')}
- Average overall score: {context.get('avg_total_score', 0):.1f}/100
- Average diet score: {context.get('avg_diet_score', 0):.1f}/100
- Average daily calories: {context.get('avg_calories', 0):.0f} kcal
- Average daily water: {context.get('avg_water', 0):.0f} ml
- Average daily steps: {context.get('avg_steps', 0):.0f}
- Diet goal days: {context.get('diet_goal_days', 0)}/7
- Hydration goal days: {context.get('water_goal_days', 0)}/7
- Step goal days: {context.get('step_goal_days', 0)}/7
- Symptom days: {context.get('symptom_days', 0)}/7
- Symptom events: {context.get('symptoms_count', 0)}
- Medication log days: {context.get('medication_days', 0)}/7
- Best day: {context.get('best_day', 'N/A')}
- Focus day: {context.get('focus_day', 'N/A')}
- Strengths observed: {context.get('strengths', 'None')}
- Gaps observed: {context.get('gaps', 'None')}
- Suggested focus: {context.get('next_focus', 'Keep the current routine')}
- Extra monitoring sections: {context.get('custom_sections', 'None')}

Output in exactly two parts with no markdown code fence:

---review---
Write 140-220 words. Explicitly cover:
1. what went well this week,
2. what did not go well,
3. what matters most for the managed conditions,
4. what should be prioritized next week.

---plan---
- Provide 3-5 concrete actions for next week.
- Actions must be practical, specific, and aligned with the managed conditions.
"""
    if resolved == "ja-JP":
        return f"""あなたは週次健康レビューの専門家です。以下の7日分の集計データをもとに、現実的な週次レビューと来週の行動計画を作成してください。

プロフィール要約: {context.get('profile_summary', 'N/A')}
管理中の病態 / 目標: {context.get('condition_name', '一般的な健康管理')}
主目標: {context.get('primary_condition', '一般的な健康管理')}
食事方針: {context.get('diet_principle', '安定した生活リズムを維持する')}
飲水目標: {context.get('water_target', 2000)} ml
歩数目標: {context.get('step_target', 8000)}

[週間サマリー]
- 体重変化: {context.get('weight_change', 'N/A')}
- 平均総合スコア: {context.get('avg_total_score', 0):.1f}/100
- 平均食事スコア: {context.get('avg_diet_score', 0):.1f}/100
- 平均摂取カロリー: {context.get('avg_calories', 0):.0f} kcal
- 平均飲水量: {context.get('avg_water', 0):.0f} ml
- 平均歩数: {context.get('avg_steps', 0):.0f}
- 食事目標達成日: {context.get('diet_goal_days', 0)}/7
- 飲水目標達成日: {context.get('water_goal_days', 0)}/7
- 歩数目標達成日: {context.get('step_goal_days', 0)}/7
- 症状日数: {context.get('symptom_days', 0)}/7
- 症状イベント数: {context.get('symptoms_count', 0)}
- 服薬記録日数: {context.get('medication_days', 0)}/7
- ベスト日: {context.get('best_day', 'N/A')}
- 要重点レビュー日: {context.get('focus_day', 'N/A')}
- 良かった点: {context.get('strengths', 'なし')}
- 課題: {context.get('gaps', 'なし')}
- 来週の重点: {context.get('next_focus', '現在の習慣を維持する')}
- 追加モニタリング項目: {context.get('custom_sections', 'なし')}

出力は必ず次の2部構成にしてください。コードブロックは禁止です。

---review---
160〜260字程度で、以下を必ず含めてください。
1. 今週よかった点
2. 今週うまくいかなかった点
3. 管理中の病態にとって重要な意味
4. 来週最優先で取り組むこと

---plan---
- 来週の具体的な行動を 3〜5 個
- 実行しやすく、具体的で、管理目標に沿った内容にしてください
"""
    return f"""你是一位专业的周度健康复盘专家。请根据以下 7 天聚合数据，输出一份可信、可执行的周报复盘与下周行动方案。

个人信息：{context.get('profile_summary', '暂无')}
管理目标：{context.get('condition_name', '综合健康管理')}
主目标：{context.get('primary_condition', '综合健康管理')}
管理原则：{context.get('diet_principle', '保持稳定规律')}
饮水目标：{context.get('water_target', 2000)} ml
步数目标：{context.get('step_target', 8000)}

[周度汇总]
- 体重变化：{context.get('weight_change', '暂无')}
- 周均综合评分：{context.get('avg_total_score', 0):.1f}/100
- 周均饮食评分：{context.get('avg_diet_score', 0):.1f}/100
- 日均热量：{context.get('avg_calories', 0):.0f} kcal
- 日均饮水：{context.get('avg_water', 0):.0f} ml
- 日均步数：{context.get('avg_steps', 0):.0f}
- 饮食达标天数：{context.get('diet_goal_days', 0)}/7
- 饮水达标天数：{context.get('water_goal_days', 0)}/7
- 步数达标天数：{context.get('step_goal_days', 0)}/7
- 症状天数：{context.get('symptom_days', 0)}/7
- 症状次数：{context.get('symptoms_count', 0)}
- 用药记录天数：{context.get('medication_days', 0)}/7
- 最佳日：{context.get('best_day', '暂无')}
- 重点复盘日：{context.get('focus_day', '暂无')}
- 本周亮点：{context.get('strengths', '暂无')}
- 待改进项：{context.get('gaps', '暂无')}
- 下周重点：{context.get('next_focus', '保持当前节奏')}
- 额外监测项目：{context.get('custom_sections', '暂无')}

请严格按以下两部分输出，不要加代码块：

---review---
写 140-220 字，明确说明：
1. 本周做得好的地方，
2. 本周做得不够好的地方，
3. 对当前多病种/目标最关键的影响，
4. 下周最该优先做什么。

---plan---
- 输出 3-5 条下周可执行方案。
- 要求具体、落地，并与当前管理目标保持一致。
"""
    if resolved == "en-US":
        return f"""You are a professional weekly health reviewer. Based on the aggregated 7-day health data below, write a weekly review and next-week action plan.

Condition / goal: {context['condition_name']}
Step target: {context['step_target']}

[Weekly summary]
- Weight change: {context['weight_change']}
- Average daily calories: {context['avg_calories']:.0f} kcal
- Average daily water: {context['avg_water']:.0f} ml
- Average daily steps: {context['avg_steps']:.0f}
- Symptom events: {context['symptoms_count']}

Output in exactly two parts with no markdown code fence:

---review---
Write about 120-180 words. Mention what improved and what still needs work.

---plan---
- List 3 concrete actions for next week
"""
    if resolved == "ja-JP":
        return f"""あなたは週次健康レビューの専門家です。以下の7日集計データをもとに、短いレビューと来週の行動計画を作成してください。

病態 / 目標: {context['condition_name']}
歩数目標: {context['step_target']}

[週間サマリー]
- 体重変化: {context['weight_change']}
- 平均摂取カロリー: {context['avg_calories']:.0f} kcal
- 平均飲水量: {context['avg_water']:.0f} ml
- 平均歩数: {context['avg_steps']:.0f}
- 症状イベント数: {context['symptoms_count']}

出力は次の2部構成にしてください。コードブロックは禁止です。

---review---
120〜180字程度で、改善した点と今後の課題を述べてください。

---plan---
- 来週の具体的な行動を3つ
"""
    return f"""你是一位专业的周度健康复盘专家。请根据以下 7 天聚合数据，输出一份周报复盘和下周计划。

病理/目标：{context['condition_name']}
目标步数：{context['step_target']}

【本周摘要】
- 体重变化：{context['weight_change']}
- 日均摄入热量：{context['avg_calories']:.0f} kcal
- 日均饮水量：{context['avg_water']:.0f} ml
- 日均步数：{context['avg_steps']:.0f}
- 不适症状次数：{context['symptoms_count']}

请严格按以下两部分输出，不要加代码块：

---review---
写 120-180 字左右的复盘，说明亮点和风险。

---plan---
- 列出 3 条下周可执行动作
"""


def build_weekly_ai_system_prompt(locale: Optional[str]) -> str:
    resolved = resolve_locale(locale=locale)
    if resolved == "en-US":
        return "You are a professional health data analyst."
    if resolved == "ja-JP":
        return "あなたは慎重で専門的な健康データアナリストです。"
    return "你是一位专业健康数据分析师。"


def build_fallback_plan(locale: Optional[str], target_water: int, fruits: str) -> dict:
    return {
        "diet": [t(locale, "fallback_diet_1"), t(locale, "fallback_diet_2"), t(locale, "fallback_diet_3")],
        "water": [
            t(locale, "fallback_water_1"),
            t(locale, "fallback_water_2"),
            t(locale, "fallback_water_3"),
            t(locale, "fallback_water_4"),
            t(locale, "fallback_water_5"),
            t(locale, "fallback_water_target", target=target_water),
        ],
        "exercise": [t(locale, "fallback_exercise_1"), t(locale, "fallback_exercise_2"), t(locale, "fallback_exercise_3")],
        "notes": [t(locale, "fallback_note_fruits", fruits=fruits or "-")],
    }


def build_weekly_fallback(locale: Optional[str]) -> tuple[str, str]:
    return (
        t(locale, "weekly_fallback_review"),
        "\n".join(
            [
                f"- {t(locale, 'weekly_fallback_plan_1')}",
                f"- {t(locale, 'weekly_fallback_plan_2')}",
                f"- {t(locale, 'weekly_fallback_plan_3')}",
            ]
        ),
    )


def build_delivery_message(
    locale: Optional[str],
    body: str,
    pdf_url: str,
    report_kind: str,
    generated_at: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    resolved_locale = resolve_locale(locale=locale)
    is_zh = resolved_locale == "zh-CN"
    is_ja = resolved_locale == "ja-JP"
    if report_kind == "daily":
        pdf_label = t(locale, "delivery_daily_pdf")
        if is_zh:
            report_title = "🌅 每日健康速览"
        elif is_ja:
            report_title = "🌅 健康日報ダイジェスト"
        else:
            report_title = "🌅 Daily Health Snapshot"
    elif report_kind == "monthly":
        pdf_label = t(locale, "delivery_monthly_pdf")
        if is_zh:
            report_title = "🗓️ 健康月报速览"
        elif is_ja:
            report_title = "🗓️ 健康月報ダイジェスト"
        else:
            report_title = "🗓️ Monthly Health Snapshot"
    else:
        pdf_label = t(locale, "delivery_weekly_pdf")
        if is_zh:
            report_title = "🗓️ 健康周报速览"
        elif is_ja:
            report_title = "🗓️ 健康週報ダイジェスト"
        else:
            report_title = "🗓️ Weekly Health Snapshot"

    body_text = markdown_to_plain_text(body)
    if is_zh:
        summary_label = "📝 文字版摘要"
        pdf_block_label = "📎 PDF 完整版"
        period_label = "📅 报告周期"
        generated_label = "⏱️ 生成时间"
    elif is_ja:
        summary_label = "📝 テキスト要約"
        pdf_block_label = "📎 PDF 完全版"
        period_label = "📅 レポート期間"
        generated_label = "⏱️ 生成時刻"
    else:
        summary_label = "📝 Text Summary"
        pdf_block_label = "📎 Full PDF"
        period_label = "📅 Report Period"
        generated_label = "⏱️ Generated At"
    divider = "━━━━━━━━━━━━━━━━━━"

    lines = [
        report_title,
        divider,
        "",
        summary_label,
        body_text,
        "",
        divider,
        pdf_block_label,
        f"{pdf_label}: {pdf_url}",
    ]
    if report_kind in {"weekly", "monthly"} and start_date and end_date:
        lines.extend(["", f"{period_label}: {start_date} ~ {end_date}"])
    if generated_at:
        lines.append(f"{generated_label}: {generated_at}")
    return "\n".join(lines).strip()
