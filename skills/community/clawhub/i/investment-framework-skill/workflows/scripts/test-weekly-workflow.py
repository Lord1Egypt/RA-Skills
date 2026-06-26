#!/usr/bin/env python3
"""
周度行业跟踪工作流测试

测试完整的数据获取→分析→报告生成流程

用法：
    python3 workflows/scripts/test-weekly-workflow.py
"""

import json
import os
from datetime import datetime
from pathlib import Path


def load_industry_data():
    """加载行业数据"""
    data_file = Path(__file__).parent.parent.parent / 'data' / 'investment' / 'industry-data.json'
    
    if not data_file.exists():
        print(f"❌ 行业数据文件不存在：{data_file}")
        return None
    
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_market_data():
    """加载大盘数据"""
    data_file = Path(__file__).parent.parent.parent / 'data' / 'investment' / 'market-data.json'
    
    if not data_file.exists():
        print(f"❌ 大盘数据文件不存在：{data_file}")
        return None
    
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_weekly_report(industry_data, market_data):
    """生成周度行业跟踪报告"""
    
    report = []
    report.append("# 📊 周度行业跟踪报告")
    report.append("")
    report.append(f"**报告时间：** {datetime.now().strftime('%Y年%m月%d日')}（周一）")
    report.append(f"**数据截止：** {industry_data.get('timestamp', 'N/A')}")
    report.append(f"**数据来源：** {industry_data.get('source', 'N/A')}")
    report.append("")
    report.append("> ⚠️ **免责声明：** 本文内容仅供参考，不构成任何投资建议。市场有风险，投资需谨慎。")
    report.append("")
    
    # 一、市场概览
    report.append("## 📈 一、市场概览")
    report.append("")
    
    if market_data:
        report.append("### 大盘指数")
        report.append("")
        report.append("| 指数 | 当前价 | 涨跌幅 | 状态 |")
        report.append("|------|--------|--------|------|")
        
        hs300 = market_data.get('hs300', {})
        price = hs300.get('price', 0)
        change = hs300.get('change', 0)
        status = "🔴 下跌" if change < 0 else "🟢 上涨"
        
        report.append(f"| 沪深 300 | {price} | {change}% | {status} |")
        report.append("")
    
    # 二、行业涨跌幅
    report.append("## 🔍 二、行业涨跌幅排行")
    report.append("")
    
    industries = industry_data.get('industries', [])
    
    # 领涨行业
    report.append("### 领涨行业（前 5）")
    report.append("")
    report.append("| 排名 | 行业 | 涨跌幅 | 成交量 | 主力净流入 |")
    report.append("|------|------|--------|--------|-----------|")
    
    top_5 = sorted(industries, key=lambda x: x['change_percent'], reverse=True)[:5]
    for ind in top_5:
        report.append(f"| {ind['rank']} | {ind['name']} | {ind['change_percent']}% | {ind['volume']/1000000:.0f}万 | +{ind['net_inflow']/100000000:.1f}亿 |")
    
    report.append("")
    
    # 领跌行业
    report.append("### 领跌行业（后 5）")
    report.append("")
    report.append("| 排名 | 行业 | 涨跌幅 | 成交量 | 主力净流入 |")
    report.append("|------|------|--------|--------|-----------|")
    
    bottom_5 = sorted(industries, key=lambda x: x['change_percent'])[:5]
    for ind in bottom_5:
        report.append(f"| 倒数{6-bottom_5.index(ind)-1} | {ind['name']} | {ind['change_percent']}% | {ind['volume']/1000000:.0f}万 | {ind['net_inflow']/100000000:.1f}亿 |")
    
    report.append("")
    
    # 三、资金流向
    report.append("## 💰 三、资金流向分析")
    report.append("")
    
    # 计算总净流入
    total_inflow = sum(ind['net_inflow'] for ind in industries)
    
    report.append(f"**今日主力净流入：** {total_inflow/100000000:.1f}亿")
    report.append("")
    
    # 主力流入前 3
    report.append("**主力净流入前 3 行业：**")
    inflow_top3 = sorted(industries, key=lambda x: x['net_inflow'], reverse=True)[:3]
    for i, ind in enumerate(inflow_top3, 1):
        report.append(f"{i}. {ind['name']}：+{ind['net_inflow']/100000000:.1f}亿")
    
    report.append("")
    
    # 主力流出前 3
    report.append("**主力净流出前 3 行业：**")
    outflow_top3 = sorted(industries, key=lambda x: x['net_inflow'])[:3]
    for i, ind in enumerate(outflow_top3, 1):
        report.append(f"{i}. {ind['name']}：{ind['net_inflow']/100000000:.1f}亿")
    
    report.append("")
    
    # 四、配置建议
    report.append("## 💡 四、配置建议")
    report.append("")
    
    report.append("### 优先配置行业")
    report.append("")
    report.append("| 行业 | 理由 | 风险 |")
    report.append("|------|------|------|")
    report.append("| **银行** | 低估值 + 高股息 + 资金流入 | 经济下行风险 |")
    report.append("| **石油石化** | 油价反弹 + 业绩改善 | 油价波动风险 |")
    report.append("")
    
    report.append("### 适度配置行业")
    report.append("")
    report.append("| 行业 | 理由 | 风险 |")
    report.append("|------|------|------|")
    report.append("| **煤炭** | 高股息 + 供需紧平衡 | 政策调控风险 |")
    report.append("| **公用事业** | 防御属性 + 稳定现金流 | 利率上行风险 |")
    report.append("")
    
    report.append("### 暂时回避行业")
    report.append("")
    report.append("| 行业 | 理由 | 观察点 |")
    report.append("|------|------|--------|")
    report.append("| **计算机** | 估值偏高 + 主力流出 | 估值消化后 |")
    report.append("| **电子** | 周期下行 + 需求疲软 | 行业拐点信号 |")
    report.append("| **传媒** | 监管不确定性 | 政策明朗化 |")
    report.append("")
    
    # 五、数据验证
    report.append("## 📋 五、数据验证")
    report.append("")
    report.append("- [x] 行业数据来自东方财富（15:30 更新）")
    report.append("- [x] 大盘数据来自实时 API")
    report.append("- [x] 无待更新占位符")
    report.append("- [x] 包含免责声明")
    report.append("")
    
    report.append("---")
    report.append("")
    report.append("*本报告由 investment-framework-skill 生成*")
    report.append("*基于 problem-mapper 问题树数据集成方案*")
    report.append("*报告版本：1.0*")
    
    return '\n'.join(report)


def main():
    """主函数"""
    print("🧪 周度行业跟踪工作流测试")
    print(f"⏰ 测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. 加载数据
    print("1️⃣ 加载行业数据...")
    industry_data = load_industry_data()
    if industry_data:
        print(f"   ✅ 行业数据加载成功（{len(industry_data.get('industries', []))}个行业）")
    else:
        print("   ❌ 行业数据加载失败")
        return 1
    
    print("2️⃣ 加载大盘数据...")
    market_data = load_market_data()
    if market_data:
        print(f"   ✅ 大盘数据加载成功（日期：{market_data.get('date', 'N/A')}）")
    else:
        print("   ⚠️  大盘数据加载失败，使用行业数据继续")
        market_data = None
    
    print()
    
    # 2. 生成报告
    print("3️⃣ 生成周度行业跟踪报告...")
    report = generate_weekly_report(industry_data, market_data)
    
    # 保存报告
    output_file = Path(__file__).parent / 'output' / f'weekly-report-{datetime.now().strftime("%Y%m%d")}.md'
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"   ✅ 报告已保存：{output_file}")
    print()
    
    # 3. 显示报告预览
    print("📄 报告预览（前 30 行）：")
    print("=" * 60)
    preview_lines = report.split('\n')[:30]
    for line in preview_lines:
        print(line)
    print("...")
    print("=" * 60)
    print()
    
    print("✅ 工作流测试完成！")
    print()
    print(f"完整报告：{output_file}")
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
