#!/usr/bin/env python3
"""
户型分析工具
分析户型图并生成结构化分析报告
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


def parse_layout(layout: str) -> dict:
    """解析户型描述为房间字典"""
    rooms = {
        "bedrooms": 0,
        "living_rooms": 0,
        "bathrooms": 0,
        "kitchen": 1,
        "balcony": 0
    }
    
    # 使用正则表达式解析
    bedroom_match = re.search(r'(\d+) 室', layout)
    if bedroom_match:
        rooms["bedrooms"] = int(bedroom_match.group(1))
    
    living_match = re.search(r'(\d+) 厅', layout)
    if living_match:
        rooms["living_rooms"] = int(living_match.group(1))
    
    bath_match = re.search(r'(\d+) 卫', layout)
    if bath_match:
        rooms["bathrooms"] = int(bath_match.group(1))
    
    if "阳台" in layout or "阳" in layout:
        rooms["balcony"] = 1
    
    return rooms


def analyze_floor_plan(area: str, layout: str, orientation: str,
                      floor_height: str = "2.8m", rooms: dict = None) -> dict:
    """分析户型并生成报告"""
    
    if rooms is None:
        rooms = parse_layout(layout)
    
    advantages = analyze_advantages(layout, orientation, rooms)
    disadvantages = analyze_disadvantages(layout, orientation, rooms)
    circulation = analyze_circulation(layout, rooms)
    lighting = analyze_lighting(orientation, rooms)
    storage = suggest_storage(rooms)
    
    report = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "basic_info": {
            "area": area,
            "layout": layout,
            "orientation": orientation,
            "floor_height": floor_height,
            "rooms": rooms
        },
        "analysis": {
            "advantages": advantages,
            "disadvantages": disadvantages,
            "circulation": circulation,
            "lighting": lighting,
            "storage": storage
        },
        "recommendations": generate_recommendations(advantages, disadvantages)
    }
    
    return report


def analyze_advantages(layout: str, orientation: str, rooms: dict) -> list:
    """分析户型优势"""
    advantages = []
    
    if rooms["bedrooms"] >= 3:
        advantages.append("房间数量充足，功能分区明确")
    
    if rooms["bathrooms"] >= 2:
        advantages.append("双卫生间设计，早晚高峰不拥堵")
    
    if "南" in orientation:
        advantages.append("主要空间朝南，采光良好")
    
    if "南北" in orientation:
        advantages.append("南北通透，通风效果好")
    
    if rooms["living_rooms"] >= 2:
        advantages.append("客餐厅分离，动静分区合理")
    
    if rooms["balcony"] > 0:
        advantages.append("带阳台，增加使用空间和晾晒区域")
    
    return advantages if advantages else ["户型方正，利用率高"]


def analyze_disadvantages(layout: str, orientation: str, rooms: dict) -> list:
    """分析户型劣势"""
    disadvantages = []
    
    if rooms["bedrooms"] == 1:
        disadvantages.append("单间户型，功能受限")
    
    if rooms["bathrooms"] == 0:
        disadvantages.append("无独立卫生间，使用不便")
    
    if "北" in orientation and "南" not in orientation:
        disadvantages.append("朝北户型，采光相对较弱")
    
    if "西" in orientation and "东" not in orientation:
        disadvantages.append("朝西户型，夏季西晒严重")
    
    if rooms["living_rooms"] == 1 and rooms["bedrooms"] >= 3:
        disadvantages.append("客厅可能较小，活动空间有限")
    
    return disadvantages if disadvantages else ["无明显劣势"]


def analyze_circulation(layout: str, rooms: dict) -> dict:
    """分析动线"""
    circulation = {
        "main_route": "入户→玄关→客厅→餐厅→厨房",
        "secondary_route": "卧室→卫生间",
        "issues": [],
        "suggestions": []
    }
    
    if rooms["bathrooms"] == 1 and rooms["bedrooms"] >= 3:
        circulation["issues"].append("单卫生间，早晚高峰可能拥堵")
        circulation["suggestions"].append("考虑干湿分离，提高使用效率")
    
    if rooms["living_rooms"] == 1:
        circulation["issues"].append("客餐厅可能交叉干扰")
        circulation["suggestions"].append("通过家具布置或地面材质区分功能区域")
    
    return circulation


def analyze_lighting(orientation: str, rooms: dict) -> dict:
    """分析采光"""
    lighting = {
        "orientation": orientation,
        "quality": "良好" if "南" in orientation else "一般",
        "suggestions": []
    }
    
    if "南" not in orientation:
        lighting["suggestions"].append("建议使用浅色系装修，增加空间明亮度")
        lighting["suggestions"].append("增加辅助照明，弥补自然光不足")
    
    if rooms["bedrooms"] > 2:
        lighting["suggestions"].append("次卧可考虑室内窗或玻璃砖，改善采光")
    
    return lighting


def suggest_storage(rooms: dict) -> list:
    """收纳建议"""
    suggestions = [
        "玄关：定制顶天立地鞋柜，容量最大化",
        "客厅：电视墙可做整面收纳柜",
        "卧室：衣柜做到顶，增加换季被褥收纳",
        "厨房：利用墙面做吊柜，增加储物空间",
        "卫生间：镜柜 + 浴室柜组合，收纳洗漱用品"
    ]
    
    if rooms["bedrooms"] >= 3:
        suggestions.append("可考虑将一间次卧改为衣帽间或储物间")
    
    return suggestions


def generate_recommendations(advantages: list, disadvantages: list) -> list:
    """生成装修建议"""
    recommendations = []
    
    if any("朝南" in a for a in advantages):
        recommendations.append("充分利用南向采光，客厅和主卧优先布置在南侧")
    
    if any("通透" in a for a in advantages):
        recommendations.append("保持南北通透格局，避免过多隔断影响通风")
    
    if any("采光" in d for d in disadvantages):
        recommendations.append("采用浅色系装修，增加镜面元素提升明亮度")
    
    if any("西晒" in d for d in disadvantages):
        recommendations.append("西侧窗户使用遮光窗帘，或考虑贴隔热膜")
    
    return recommendations


def format_report(report: dict) -> str:
    """格式化报告为 Markdown"""
    md = f"""# 户型分析报告

**分析时间**: {report['timestamp']}

## 一、基本信息

| 项目 | 内容 |
|------|------|
| 建筑面积 | {report['basic_info']['area']} |
| 户型结构 | {report['basic_info']['layout']} |
| 房屋朝向 | {report['basic_info']['orientation']} |
| 层高 | {report['basic_info']['floor_height']} |

### 房间配置
- 卧室：{report['basic_info']['rooms']['bedrooms']} 间
- 客厅：{report['basic_info']['rooms']['living_rooms']} 间
- 卫生间：{report['basic_info']['rooms']['bathrooms']} 间
- 厨房：{report['basic_info']['rooms']['kitchen']} 间
- 阳台：{report['basic_info']['rooms']['balcony']} 个

## 二、户型分析

### 2.1 优势分析
"""
    
    for adv in report['analysis']['advantages']:
        md += f"- ✅ {adv}\n"
    
    md += "\n### 2.2 劣势分析\n"
    for dis in report['analysis']['disadvantages']:
        md += f"- ⚠️ {dis}\n"
    
    md += f"""
## 三、动线分析

### 3.1 主动线
{report['analysis']['circulation']['main_route']}

### 3.2 次动线
{report['analysis']['circulation']['secondary_route']}
"""
    
    if report['analysis']['circulation']['issues']:
        md += "\n### 3.3 存在问题\n"
        for issue in report['analysis']['circulation']['issues']:
            md += f"- {issue}\n"
        
        md += "\n### 3.4 优化建议\n"
        for sug in report['analysis']['circulation']['suggestions']:
            md += f"- {sug}\n"
    
    md += f"""
## 四、采光分析

**采光质量**: {report['analysis']['lighting']['quality']}

**朝向特点**: {report['analysis']['lighting']['orientation']}
"""
    
    if report['analysis']['lighting']['suggestions']:
        md += "\n**改善建议**:\n"
        for sug in report['analysis']['lighting']['suggestions']:
            md += f"- {sug}\n"
    
    md += "\n## 五、收纳规划\n"
    for sug in report['analysis']['storage']:
        md += f"- {sug}\n"
    
    md += "\n## 六、装修建议\n"
    for rec in report['recommendations']:
        md += f"- {rec}\n"
    
    return md


def main():
    parser = argparse.ArgumentParser(description='分析户型并生成报告')
    parser.add_argument('--area', required=True, help='建筑面积')
    parser.add_argument('--layout', required=True, help='户型结构，如"3 室 2 厅 2 卫"')
    parser.add_argument('--orientation', required=True, help='房屋朝向，如"南北通透"')
    parser.add_argument('--floor-height', default='2.8m', help='层高')
    parser.add_argument('--output', required=True, help='输出文件路径')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    
    args = parser.parse_args()
    
    report = analyze_floor_plan(
        area=args.area,
        layout=args.layout,
        orientation=args.orientation,
        floor_height=args.floor_height
    )
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if args.json:
        output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    else:
        md_content = format_report(report)
        output_path.write_text(md_content, encoding='utf-8')
    
    print(f"户型分析报告已生成：{output_path}")


if __name__ == '__main__':
    main()
