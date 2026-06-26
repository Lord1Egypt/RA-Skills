#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成伊朗局势分析图表
"""

import sys
sys.path.append('scripts')

from scripts.charts import ChartGenerator

# 初始化
generator = ChartGenerator(output_dir="reports/charts")

# 1. 油价对比数据（基于之前 MEMORY.md 中的数据）
oil_price_data = {
    "当前油价": {"DeepSeek": 103, "Qwen": 105, "豆包": 104, "Kimi": 102, "Gemini": 106},
    "冲突前基准": {"DeepSeek": 73, "Qwen": 73, "豆包": 73, "Kimi": 73, "Gemini": 73},
    "峰值预测": {"DeepSeek": 120, "Qwen": 125, "豆包": 118, "Kimi": 122, "Gemini": 128}
}

# 2. 质量评分（基于刚才的分析报告）
quality_scores = {
    "本报告": {"数据完整性": 85, "时效性": 95, "分析深度": 80, "引用来源": 85, "可操作性": 85}
}

# 3. 情景推演数据
scenario_data = {
    "油价 (美元)": {"乐观情景": 90, "基准情景": 107.5, "悲观情景": 150},
    "概率 (%)": {"乐观情景": 30, "基准情景": 50, "悲观情景": 20}
}

print("生成伊朗局势分析图表...")
print("=" * 50)

# 生成图表
try:
    print("\n1. 生成油价对比柱状图...")
    chart1 = generator.generate_comparison_bar_chart(
        oil_price_data, 
        title="伊朗局势 - 油价预测对比（美元/桶）",
        ylabel="油价（美元）",
        filename="iran_oil_price_comparison_20260319"
    )
    print(f"   ✓ 已保存：{chart1}")
    
    print("\n2. 生成质量评分雷达图...")
    chart2 = generator.generate_quality_radar_chart(
        quality_scores,
        title="伊朗局势分析报告 - 质量评分",
        filename="iran_report_quality_20260319"
    )
    print(f"   ✓ 已保存：{chart2}")
    
    print("\n3. 生成情景推演柱状图...")
    chart3 = generator.generate_comparison_bar_chart(
        scenario_data,
        title="伊朗局势 - 情景推演对比",
        ylabel="数值",
        filename="iran_scenario_analysis_20260319"
    )
    print(f"   ✓ 已保存：{chart3}")
    
    print("\n" + "=" * 50)
    print("✅ 图表生成完成！")
    print(f"\n图表位置：reports/charts/")
    print("- iran_oil_price_comparison_20260319.png")
    print("- iran_report_quality_20260319.png")
    print("- iran_scenario_analysis_20260319.png")
    
except Exception as e:
    print(f"\n❌ 图表生成失败：{e}")
    import traceback
    traceback.print_exc()
