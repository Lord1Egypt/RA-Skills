#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
飞书文档写入器 - 统一格式
"""

import json
from datetime import datetime

# 卡路里计算（估算）
CALORIE_RATE = {
    "走路": 4.5,
    "步行": 4.5,
    "跑步": 11.0,
    "俯卧撑": 8.0,
    "力量训练": 7.0,
    "拉伸": 3.0,
    "瑜伽": 4.0,
    "八段锦": 4.0,
    "太极": 4.0,
    "晒太阳": 1.7,
    "户外活动": 5.0,
    "骑行": 8.0,
    "游泳": 10.0,
}

def calculate_calories(duration, sport_type):
    rate = CALORIE_RATE.get(sport_type, 5.0)
    return int(duration * rate)

def format_checkin_doc(user_id, checkin_data, weight=None):
    weekday_cn = ["一","二","三","四","五","六","日"][datetime.now().weekday()]
    date_str = datetime.now().strftime("%Y-%m-%d") + "（周" + weekday_cn + "）"
    
    # 计算总卡路里
    total_calories = 0
    for record in checkin_data.get("records", []):
        duration = record.get("运动时长", 0)
        sport = record.get("运动类型", "")
        total_calories += calculate_calories(duration, sport)
    
    # 获取运动类型列表
    sports = [r.get("运动项目", "") for r in checkin_data.get("records", [])]
    sports_str = "+".join([s for s in sports if s]) if sports else "-"
    
    # 步数状态
    steps = checkin_data.get("总步数", 0)
    steps_status = "✅ 超额(目标8000)" if steps >= 8000 else "⚠️ 未达标"
    
    # 运动时长状态
    duration = checkin_data.get("总运动时长", 0)
    duration_status = "✅" if duration >= 60 else "⚠️"
    
    # 体重显示
    weight_str = f"{weight} kg" if weight else "-"
    
    # 构建 markdown（表格格式）
    markdown = f"""
---

## {date_str}

**运动数据：**

| 项目 | 数据 | 状态 |
|------|------|------|
| 步数 | {steps} 步 | {steps_status} |
| 运动时长 | {duration} 分钟 | {duration_status} |
| 运动类型 | {sports_str} | - |
| 卡路里消耗 | 约 {total_calories} 卡 | - |
| 打卡次数 | {checkin_data.get('打卡次数', 0)} 次 | - |
| 体重 | {weight_str} | - |

**运动详情：**
"""
    
    for i, record in enumerate(checkin_data.get("records", []), 1):
        sport = record.get("运动项目", "-")
        dur = record.get("运动时长", 0)
        st = record.get("步数", 0)
        notes = record.get("备注", "")
        
        detail = f"\n{i}. {sport}"
        if dur:
            detail += f" - {dur}分钟"
        if st:
            detail += f" - {st}步"
        if notes:
            detail += f" ({notes})"
        
        markdown += detail
    
    markdown += f"\n\n---\n*每天更新*"
    
    return markdown

# 测试
if __name__ == "__main__":
    test_data = {
        "总步数": 10300,
        "总运动时长": 130,
        "打卡次数": 3,
        "records": [
            {"运动项目": "走路", "运动时长": 60, "步数": 10300, "运动类型": "走路"},
            {"运动项目": "俯卧撑", "运动时长": 10, "运动类型": "力量训练"},
            {"运动项目": "晒太阳", "运动时长": 60, "运动类型": "户外活动"},
        ]
    }
    
    result = format_checkin_doc("test", test_data, 68.85)
    print(result)