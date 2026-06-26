#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
智能打卡处理器
根据用户输入智能判断是"新增"还是"覆盖"
"""

import json
import re
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
CHECKINS_DIR = BASE_DIR / "data" / "checkins"
CHECKINS_DIR.mkdir(parents=True, exist_ok=True)


def get_checkin_file(user_id, year_month=None):
    if year_month is None:
        year_month = datetime.now().strftime("%Y-%m")
    return CHECKINS_DIR / f"{user_id}_{year_month}.json"


def load_checkins(user_id, year_month=None):
    file = get_checkin_file(user_id, year_month)
    if file.exists():
        with open(file, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_checkins(user_id, checkins, year_month=None):
    file = get_checkin_file(user_id, year_month)
    if year_month is None:
        year_month = datetime.now().strftime("%Y-%m")
    with open(file, "w", encoding="utf-8") as f:
        json.dump(checkins, f, ensure_ascii=False, indent=2)


def detect_checkin_mode(user_input, current_steps=0):
    """
    智能判断打卡模式
    返回: "add" (新增) / "replace" (覆盖) / "unknown" (需要确认)
    """
    user_input = user_input.lower()
    
    # 明确的新增关键词
    add_keywords = ["又", "额外", "再", "加", "新增", "多"]
    # 明确的覆盖关键词
    replace_keywords = ["今天", "共", "总计", "一共", "总共", "现在", "目前", "当前"]
    
    # 检查是否有明确的新增关键词
    for kw in add_keywords:
        if kw in user_input:
            return "add"
    
    # 检查是否有明确的覆盖关键词
    for kw in replace_keywords:
        if kw in user_input:
            return "replace"
    
    # 如果有关键数字，判断大小
    # 提取数字
    numbers = re.findall(r'\d+', user_input)
    if numbers:
        new_steps = int(numbers[0])
        if current_steps > 0:
            # 有历史记录
            if new_steps < current_steps * 0.5:
                # 新数字明显小于一半，可能是新增（比如早上3000，晚上又加了2000）
                return "add"
            elif new_steps > current_steps * 1.2:
                # 新数字明显大于，可能是覆盖（比如早上3000，晚上说总共7000）
                return "replace"
    
    # 无法判断
    return "unknown"


def smart_record_checkin(user_id, user_input, steps=0, duration=0, sport_type="", notes="", **data):
    """
    智能记录打卡
    """
    today = datetime.now().strftime("%Y-%m-%d")
    year_month = today[:7]
    checkins = load_checkins(user_id, year_month)
    
    # 获取当前已有数据
    current_steps = 0
    current_duration = 0
    if today in checkins:
        current_steps = checkins[today].get("总步数", 0)
        current_duration = checkins[today].get("总运动时长", 0)
    
    # 智能判断模式
    mode = detect_checkin_mode(user_input, current_steps)
    
    if mode == "replace" or (mode == "unknown" and current_steps > 0 and steps > current_steps):
        # 覆盖模式：替换当天数据
        checkins[today] = {
            "date": today,
            "records": [{
                "timestamp": datetime.now().isoformat(),
                "运动项目": data.get("运动项目", sport_type),
                "运动时长": duration,
                "运动类型": sport_type,
                "步数": steps,
                "备注": notes,
                "模式": "覆盖"
            }],
            "打卡次数": 1,
            "总运动时长": duration,
            "总步数": steps,
            "完成状态": "已完成"
        }
        action = "已覆盖更新"
    else:
        # 新增模式：追加记录
        if today not in checkins:
            checkins[today] = {
                "date": today,
                "records": [],
                "打卡次数": 0,
                "总运动时长": 0,
                "总步数": 0,
                "完成状态": "已完成"
            }
        
        # 追加新记录
        checkins[today]["records"].append({
            "timestamp": datetime.now().isoformat(),
            "运动项目": data.get("运动项目", sport_type),
            "运动时长": duration,
            "运动类型": sport_type,
            "步数": steps,
            "备注": notes,
            "模式": "新增"
        })
        
        # 更新汇总
        checkins[today]["打卡次数"] = len(checkins[today]["records"])
        checkins[today]["总运动时长"] = sum(r.get("运动时长", 0) for r in checkins[today]["records"])
        checkins[today]["总步数"] = sum(r.get("步数", 0) for r in checkins[today]["records"])
        action = f"已新增（累加步数）"
    
    save_checkins(user_id, checkins, year_month)
    
    return {
        "action": action,
        "mode": mode,
        "打卡次数": checkins[today]["打卡次数"],
        "总步数": checkins[today]["总步数"],
        "总运动时长": checkins[today]["总运动时长"]
    }


def get_today_checkins(user_id):
    today = datetime.now().strftime("%Y-%m-%d")
    year_month = today[:7]
    checkins = load_checkins(user_id, year_month)
    return checkins.get(today, {})


# 测试
if __name__ == "__main__":
    user_id = "test_user"
    
    print("🧪 测试1: 用户说'今天跑了3000步'（覆盖）")
    result = smart_record_checkin(user_id, "今天跑了3000步", steps=3000, duration=30)
    print(f"  结果: {result}")
    print(f"  当前总步数: {get_today_checkins(user_id).get('总步数', 0)}")
    
    print("\n🧪 测试2: 用户说'又跑了2000步'（新增）")
    result = smart_record_checkin(user_id, "又跑了2000步", steps=2000, duration=20)
    print(f"  结果: {result}")
    print(f"  当前总步数: {get_today_checkins(user_id).get('总步数', 0)}")
    
    print("\n🧪 测试3: 用户说'今天一共跑了5000步'（覆盖）")
    result = smart_record_checkin(user_id, "今天一共跑了5000步", steps=5000, duration=45)
    print(f"  结果: {result}")
    print(f"  当前总步数: {get_today_checkins(user_id).get('总步数', 0)}")
    
    print("\n📋 完整记录：")
    print(json.dumps(get_today_checkins(user_id), indent=2, ensure_ascii=False))
