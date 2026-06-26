#!/usr/bin/env python3
"""
打卡管理器 v2.1
支持同一天多次打卡，自动合并记录（包括步数累加）
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).parent.parent
CHECKINS_DIR = BASE_DIR / "data" / "checkins"
CHECKINS_DIR.mkdir(parents=True, exist_ok=True)


def get_checkin_file(user_id, year_month=None):
    """获取打卡记录文件"""
    if year_month is None:
        year_month = datetime.now().strftime("%Y-%m")
    return CHECKINS_DIR / f"{user_id}_{year_month}.json"


def load_checkins(user_id, year_month=None):
    """加载打卡记录"""
    file = get_checkin_file(user_id, year_month)
    if file.exists():
        with open(file, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_checkins(user_id, checkins, year_month=None):
    """保存打卡记录"""
    file = get_checkin_file(user_id, year_month)
    if year_month is None:
        year_month = datetime.now().strftime("%Y-%m")
    
    with open(file, "w", encoding="utf-8") as f:
        json.dump(checkins, f, ensure_ascii=False, indent=2)


def record_checkin(user_id, date=None, **data):
    """记录打卡（支持同一天多次打卡，自动合并）"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    year_month = date[:7]  # YYYY-MM
    checkins = load_checkins(user_id, year_month)
    
    # 如果当天已有记录，追加新记录
    if date in checkins:
        existing = checkins[date]
        if "records" in existing:
            # 已经是列表形式，追加
            existing["records"].append({
                "timestamp": datetime.now().isoformat(),
                "运动项目": data.get("运动项目", ""),
                "运动时长": data.get("运动时长", 0),
                "运动类型": data.get("运动类型", ""),
                "步数": data.get("步数", 0),
                "备注": data.get("备注", "")
            })
            # 更新汇总数据
            existing["打卡次数"] = len(existing["records"])
            # 累加运动时长和步数
            total_duration = sum(r.get("运动时长", 0) for r in existing["records"])
            total_steps = sum(r.get("步数", 0) for r in existing["records"])
            existing["总运动时长"] = total_duration
            existing["总步数"] = total_steps
        else:
            # 旧格式，转换成新格式
            old_record = {k: v for k, v in existing.items() if k != "records"}
            existing["records"] = [old_record]
            existing["records"].append({
                "timestamp": datetime.now().isoformat(),
                "运动项目": data.get("运动项目", ""),
                "运动时长": data.get("运动时长", 0),
                "运动类型": data.get("运动类型", ""),
                "步数": data.get("步数", 0),
                "备注": data.get("备注", "")
            })
            existing["打卡次数"] = 2
            existing["总运动时长"] = existing.get("运动时长", 0) + data.get("运动时长", 0)
            existing["总步数"] = existing.get("步数", 0) + data.get("步数", 0)
    else:
        # 新建记录
        checkins[date] = {
            "date": date,
            "records": [{
                "timestamp": datetime.now().isoformat(),
                "运动项目": data.get("运动项目", ""),
                "运动时长": data.get("运动时长", 0),
                "运动类型": data.get("运动类型", ""),
                "步数": data.get("步数", 0),
                "备注": data.get("备注", "")
            }],
            "打卡次数": 1,
            "总运动时长": data.get("运动时长", 0),
            "总步数": data.get("步数", 0),
            "完成状态": "已完成"
        }
    
    save_checkins(user_id, checkins, year_month)
    return checkins[date]


def get_checkin_stats(user_id, days=7):
    """获取打卡统计"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    all_checkins = {}
    current = start_date
    
    while current <= end_date:
        year_month = current.strftime("%Y-%m")
        checkins = load_checkins(user_id, year_month)
        date_str = current.strftime("%Y-%m-%d")
        if date_str in checkins:
            all_checkins[date_str] = checkins[date_str]
        current += timedelta(days=1)
    
    return all_checkins


def get_today_checkins(user_id):
    """获取今日打卡记录"""
    today = datetime.now().strftime("%Y-%m-%d")
    year_month = today[:7]
    checkins = load_checkins(user_id, year_month)
    return checkins.get(today, {})


if __name__ == "__main__":
    # 测试
    user_id = "test_user_v2"
    
    # 模拟多次打卡
    print("测试：6点打卡 - 8000步")
    result1 = record_checkin(user_id, 运动项目="走路", 运动时长=60, 运动类型="有氧", 步数=8000)
    print(f"  打卡次数: {result1.get('打卡次数', 1)}")
    print(f"  总步数: {result1.get('总步数', 0)}")
    
    print("测试：20点打卡 - +3000步")
    result2 = record_checkin(user_id, 运动项目="走路", 运动时长=30, 运动类型="有氧", 步数=3000)
    print(f"  打卡次数: {result2.get('打卡次数', 1)}")
    print(f"  总步数: {result2.get('总步数', 0)}分钟")
    
    print("\n完整记录：")
    print(json.dumps(load_checkins(user_id), indent=2, ensure_ascii=False))
