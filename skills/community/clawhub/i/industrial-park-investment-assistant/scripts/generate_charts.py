#!/usr/bin/env python3
"""
园区数据可视化脚本
生成房源面积分布、租金对比等图表（Markdown格式）
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def generate_area_distribution():
    """生成房源面积分布图（ASCII art）"""
    # 模拟数据（实际应从腾讯文档读取）
    area_data = {
        "100㎡以下": 15,
        "100-300㎡": 45,
        "300-500㎡": 30,
        "500㎡以上": 10,
    }
    
    total = sum(area_data.values())
    
    output = "# 📊 房源面积分布图\n\n"
    output += "## 数据概览\n"
    output += f"- **统计时间：** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    output += f"- **房源总数：** {total}间\n\n"
    
    output += "## 面积分布\n\n"
    output += "| 面积区间 | 数量 | 占比 | 可视化 |\n"
    output += "|----------|------|------|----------|\n"
    
    for area_range, count in area_data.items():
        percentage = (count / total) * 100
        bar_length = int(percentage / 2)  # 每2%一个■
        bar = "■" * bar_length
        output += f"| {area_range} | {count} | {percentage:.1f}% | {bar} |\n"
    
    output += "\n## 分析建议\n"
    output += "- **主力户型**：100-300㎡占比最高（45%），符合市场需求\n"
    output += "- **稀缺资源**：500㎡以上大户型仅10%，可重点推介给规模企业\n"
    output += "- **推荐策略**：对300㎡以下客户可推100-300㎡主力户型\n"
    
    return output

def generate_rent_comparison():
    """生成租金报价对比图（ASCII art）"""
    # 模拟数据（实际应从腾讯文档读取）
    rent_data = {
        "低区": {"底价": 1.8, "物业费": 0.8, "总月租": 2.6},
        "中区": {"底价": 2.2, "物业费": 0.8, "总月租": 3.0},
        "高区": {"底价": 2.5, "物业费": 0.8, "总月租": 3.3},
    }
    
    output = "# 💰 租金报价对比图\n\n"
    output += "## 分区报价\n\n"
    output += "| 分区 | 底价(元/㎡/天) | 物业费(元/㎡/月) | 总月租(元/㎡/月) | 可视化 |\n"
    output += "|------|------------------|-------------------|-------------------|----------|\n"
    
    max_rent = max(data["总月租"] for data in rent_data.values())
    
    for zone, data in rent_data.items():
        percentage = (data["总月租"] / max_rent) * 100
        bar_length = int(percentage / 5)  # 每5%一个■
        bar = "■" * bar_length
        output += f"| {zone} | {data['底价']} | {data['物业费']} | {data['总月租']} | {bar} |\n"
    
    output += "\n## 价格分析\n"
    output += f"- **低区优势**：总月租2.6元/㎡/月，性价比最高\n"
    output += f"- **中区平衡**：总月租3.0元/㎡/月，适合大多数企业\n"
    output += f"- **高区景观**：总月租3.3元/㎡/月，适合对形象要求高的企业\n"
    
    output += "\n## 计算示例（300㎡）\n"
    for zone, data in rent_data.items():
        monthly = data["总月租"] * 300
        yearly = monthly * 12
        output += f"- **{zone}**：月租{monthly:.0f}元，年租{yearly:.0f}元\n"
    
    return output

def generate_support_map():
    """生成配套资源地图（文本描述）"""
    # 模拟数据
    support_data = [
        {"类型": "食堂", "名称": "园区餐厅", "位置": "T1栋1楼", "距离": "楼内"},
        {"类型": "公寓", "名称": "人才公寓", "位置": "园区北侧", "距离": "步行5分钟"},
        {"类型": "交通", "名称": "地铁站", "位置": "园区南门", "距离": "步行8分钟"},
        {"类型": "商业", "名称": "便利商店", "位置": "T2栋1楼", "距离": "楼内"},
    ]
    
    output = "# 🗺️ 配套资源地图\n\n"
    output += "## 配套清单\n\n"
    output += "| 类型 | 名称 | 位置 | 距离 |\n"
    output += "|------|------|------|------|\n"
    
    for item in support_data:
        output += f"| {item['类型']} | {item['名称']} | {item['位置']} | {item['距离']} |\n"
    
    output += "\n## 交通指南\n"
    output += "```\n"
    output += "园区出入口布局：\n"
    output += "  🚇 地铁站（南门）← 步行8分钟\n"
    output += "  🚌 公交站（东门）← 步行3分钟\n"
    output += "  🅿️ 停车场（地下）← 直达电梯\n"
    output += "```\n\n"
    
    output += "## 生活配套\n"
    output += "- **餐饮**：园区餐厅（T1栋1楼）+ 便利商店（T2栋1楼）\n"
    output += "- **住宿**：人才公寓（200间，步行5分钟）\n"
    output += "- **银行**：ATM（T1栋大堂）\n"
    
    return output

def save_to_file(content, chart_type, output_dir=None):
    """保存图表到文件"""
    if output_dir is None:
        output_dir = os.path.expanduser("~/.workbuddy/workspace/investment-assistant")
    
    os.makedirs(output_dir, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y%m%d")
    output_file = os.path.join(output_dir, f"图表_{date_str}.md")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
        f.write(f"\n\n---\n*本图表由招商助手自动生成 @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    
    return output_file

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 generate_charts.py <图表类型>")
        print("图表类型: 房源面积分布 / 租金对比 / 配套地图")
        sys.exit(1)
    
    chart_type = sys.argv[1]
    
    print(f"📊 开始生成 {chart_type} 图表...")
    
    if "面积" in chart_type:
        content = generate_area_distribution()
    elif "租金" in chart_type or "对比" in chart_type:
        content = generate_rent_comparison()
    elif "配套" in chart_type or "地图" in chart_type:
        content = generate_support_map()
    else:
        print(f"❌ 不支持的图表类型: {chart_type}")
        sys.exit(1)
    
    # 保存文件
    output_file = save_to_file(content, chart_type)
    
    print(f"✅ 图表已生成: {output_file}")
    print(f"\n📄 内容预览:")
    print(content[:500] + "..." if len(content) > 500 else content)
    
    return output_file

if __name__ == "__main__":
    main()
