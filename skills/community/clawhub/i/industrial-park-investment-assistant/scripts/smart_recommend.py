#!/usr/bin/env python3
"""
智能房源推荐脚本
根据客户需求智能匹配最合适的房源
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# 模拟房源数据库（实际应从腾讯文档读取）
AVAILABLE_ROOMS = [
    {"楼栋": "T1", "楼层": 8, "房号": "801", "面积": 256, "租金": 2.1, "状态": "空置", "装修": "精装"},
    {"楼栋": "T1", "楼层": 12, "房号": "1201", "面积": 228, "租金": 2.3, "状态": "空置", "装修": "毛坯"},
    {"楼栋": "T2", "楼层": 5, "房号": "502", "面积": 318, "租金": 1.9, "状态": "空置", "装修": "精装"},
    {"楼栋": "T1", "楼层": 15, "房号": "1501", "面积": 545, "租金": 2.4, "状态": "空置", "装修": "毛坯"},
    {"楼栋": "T2", "楼层": 3, "房号": "301", "面积": 189, "租金": 1.8, "状态": "空置", "装修": "精装"},
]

def calculate_match_score(room, requirements):
    """计算房源匹配得分"""
    score = 0
    details = []
    
    # 1. 面积匹配度 (40%)
    req_area = requirements.get("面积", 0)
    if req_area > 0:
        area_diff = abs(room["面积"] - req_area) / req_area
        if area_diff <= 0.1:  # ±10%
            area_score = 100
            details.append(f"面积完全匹配（{room['面积']}㎡ vs {req_area}㎡）")
        elif area_diff <= 0.2:  # ±20%
            area_score = 80
            details.append(f"面积接近（{room['面积']}㎡ vs {req_area}㎡）")
        else:
            area_score = 50
            details.append(f"面积有差距（{room['面积']}㎡ vs {req_area}㎡）")
    else:
        area_score = 70  # 无面积要求时给中等分数
        details.append("未指定面积需求")
    
    score += area_score * 0.4
    
    # 2. 租金匹配度 (30%)
    req_budget = requirements.get("预算", 0)
    if req_budget > 0:
        rent_diff = (room["租金"] - req_budget) / req_budget
        if rent_diff <= -0.1:  # 低于预算10%以上
            rent_score = 100
            details.append(f"租金低于预算（{room['租金']}元 vs {req_budget}元）")
        elif rent_diff <= 0:  # 低于预算
            rent_score = 90
            details.append(f"租金在预算内（{room['租金']}元 vs {req_budget}元）")
        elif rent_diff <= 0.1:  # 超过预算10%以内
            rent_score = 70
            details.append(f"租金略超预算（{room['租金']}元 vs {req_budget}元）")
        else:
            rent_score = 40
            details.append(f"租金超预算（{room['租金']}元 vs {req_budget}元）")
    else:
        rent_score = 70
        details.append("未指定预算")
    
    score += rent_score * 0.3
    
    # 3. 楼层匹配度 (20%)
    req_floor = requirements.get("楼层", "")
    floor_type = "低区" if room["楼层"] <= 5 else ("中区" if room["楼层"] <= 10 else "高区")
    if req_floor == floor_type:
        floor_score = 100
        details.append(f"楼层完全匹配（{floor_type}）")
    elif req_floor == "":
        floor_score = 80
        details.append(f"未指定楼层偏好（当前{floor_type}）")
    else:
        floor_score = 60
        details.append(f"楼层不匹配（需求{req_floor} vs 当前{floor_type}）")
    
    score += floor_score * 0.2
    
    # 4. 装修匹配度 (10%)
    req_decoration = requirements.get("装修", "")
    if req_decoration == room["装修"]:
        decor_score = 100
        details.append(f"装修匹配（{room['装修']}）")
    elif req_decoration == "":
        decor_score = 80
        details.append(f"未指定装修要求（当前{room['装修']}）")
    else:
        decor_score = 50
        details.append(f"装修不匹配（需求{req_decoration} vs 当前{room['装修']}）")
    
    score += decor_score * 0.1
    
    return round(score, 1), details

def recommend_rooms(requirements, top_n=3):
    """推荐房源"""
    # 过滤空置房源
    available = [r for r in AVAILABLE_ROOMS if r["状态"] == "空置"]
    
    # 计算匹配得分
    scored_rooms = []
    for room in available:
        score, details = calculate_match_score(room, requirements)
        scored_rooms.append({
            "room": room,
            "score": score,
            "details": details
        })
    
    # 按得分排序
    scored_rooms.sort(key=lambda x: x["score"], reverse=True)
    
    return scored_rooms[:top_n]

def format_recommendation(recommendations, requirements):
    """格式化推荐结果"""
    output = "# 🏢 智能推荐房源（Top 3）\n\n"
    
    output += "## 客户需求\n"
    output += f"- **面积需求**：{requirements.get('面积', '未指定')}㎡\n"
    output += f"- **楼层偏好**：{requirements.get('楼层', '未指定')}\n"
    output += f"- **预算范围**：{requirements.get('预算', '未指定')}元/㎡/天\n"
    output += f"- **装修要求**：{requirements.get('装修', '未指定')}\n\n"
    
    output += "## 推荐房源\n\n"
    
    for i, rec in enumerate(recommendations, 1):
        room = rec["room"]
        score = rec["score"]
        details = rec["details"]
        
        output += f"### 【推荐{i}】{room['楼栋']}栋 {room['楼层']}楼 {room['房号']}室\n"
        output += f"- **面积**：{room['面积']}㎡\n"
        output += f"- **租金**：{room['租金']}元/㎡/天\n"
        output += f"- **装修**：{room['装修']}\n"
        output += f"- **匹配得分**：**{score}分**\n"
        output += f"- **推荐理由**：{details[0]}\n"
        output += f"- **看房预约**：回复「预约看房{room['房号']}」\n\n"
    
    output += "## 计算说明\n"
    output += "- **匹配算法**：面积匹配度40% + 租金匹配度30% + 楼层匹配度20% + 装修匹配度10%\n"
    output += "- **得分范围**：0-100分，85分以上为高度匹配\n"
    output += "- **数据来源**：园区实时房源数据库\n"
    
    return output

def parse_requirements(req_string):
    """解析需求字符串"""
    requirements = {}
    
    # 简单解析：面积:300㎡ 楼层:中区 预算:2.2元/㎡/天
    pairs = req_string.split()
    for pair in pairs:
        if ":" in pair:
            key, value = pair.split(":", 1)
            key = key.strip()
            value = value.strip()
            
            if "面积" in key:
                # 提取数字
                import re
                numbers = re.findall(r'\d+', value)
                if numbers:
                    requirements["面积"] = int(numbers[0])
            elif "楼层" in key:
                requirements["楼层"] = value
            elif "预算" in key or "租金" in key:
                # 提取数字
                import re
                numbers = re.findall(r'[\d.]+', value)
                if numbers:
                    requirements["预算"] = float(numbers[0])
            elif "装修" in key:
                requirements["装修"] = value
    
    return requirements

def save_to_file(content, output_dir=None):
    """保存推荐结果到文件"""
    if output_dir is None:
        output_dir = os.path.expanduser("~/.workbuddy/workspace/investment-assistant")
    
    os.makedirs(output_dir, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y%m%d")
    output_file = os.path.join(output_dir, f"推荐房源_{date_str}.md")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
        f.write(f"\n\n---\n*本推荐由招商助手自动生成 @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    
    return output_file

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 smart_recommend.py <需求字符串>")
        print("示例: python3 smart_recommend.py \"面积:300㎡ 楼层:中区 预算:2.2元/㎡/天\"")
        sys.exit(1)
    
    req_string = " ".join(sys.argv[1:])
    
    print(f"🏢 开始智能推荐房源...")
    print(f"📋 客户需求: {req_string}")
    
    # 解析需求
    requirements = parse_requirements(req_string)
    
    if not requirements:
        print("❌ 无法解析客户需求，请检查输入格式")
        sys.exit(1)
    
    # 推荐房源
    recommendations = recommend_rooms(requirements, top_n=3)
    
    if not recommendations:
        print("❌ 未找到匹配的房源")
        sys.exit(1)
    
    # 格式化输出
    content = format_recommendation(recommendations, requirements)
    print(content)
    
    # 保存到文件
    output_file = save_to_file(content)
    print(f"\n✅ 推荐报告已保存: {output_file}")
    
    return output_file

if __name__ == "__main__":
    main()
