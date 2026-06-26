#!/usr/bin/env python3
"""
视频链接匹配器
根据运动计划自动匹配B站教学视频链接
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
VIDEOS_DIR = BASE_DIR / "videos"
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)


# 视频库（可扩展）
VIDEO_LIBRARY = {
    "八段锦": "https://www.bilibili.com/video/BV1gT4y1m7ec/",
    "太极拳": "https://www.bilibili.com/video/BV1iE411c7Ni/",
    "太极": "https://www.bilibili.com/video/BV1iE411c7Ni/",
    "肩颈拉伸": "https://www.bilibili.com/video/BV1vu411e7fC/",
    "肩颈": "https://www.bilibili.com/video/BV1vu411e7fC/",
    "腰椎养护": "https://www.bilibili.com/video/BV1pV4y1C7eu/",
    "腰椎": "https://www.bilibili.com/video/BV1pV4y1C7eu/",
    "全身拉伸": "https://www.bilibili.com/video/BV1n3411x7LG/",
    "拉伸": "https://www.bilibili.com/video/BV1n3411x7LG/",
    "瑜伽": "https://www.bilibili.com/video/BV1Kq4y1d7P4/",
    "散步": None,
    "慢走": None,
    "骑行": "https://www.bilibili.com/video/BV1Wh411Z7Ue/",
    "游泳": "https://www.bilibili.com/video/BV1Lx411Z7D3/",
    "跑步": "https://www.bilibili.com/video/BV1Wh411Z7Ue/",
    "快走": "https://www.bilibili.com/video/BV1Wh411Z7Ue/",
    "跳绳": "https://www.bilibili.com/video/BV1V5411g7pM/",
    "登山": None,
    "徒步": None,
    "小燕飞": "https://www.bilibili.com/video/BV1pV4y1C7eu/",
    "冥想": "https://www.bilibili.com/video/BV1Vx411j7MK/",
    "力量训练": "https://www.bilibili.com/video/BV1iK4y1b7P4/",
    "休息": None
}


def get_video_link(exercise_name):
    """获取运动对应的视频链接"""
    # 精确匹配
    if exercise_name in VIDEO_LIBRARY:
        return VIDEO_LIBRARY[exercise_name]
    
    # 模糊匹配
    for key, url in VIDEO_LIBRARY.items():
        if key in exercise_name or exercise_name in key:
            return url
    
    return None


def match_plan_videos(weekly_plan):
    """为周计划匹配视频链接"""
    matched_plan = {}
    
    for day, plan in weekly_plan.items():
        matched_plan[day] = {}
        for time_slot, details in plan.items():
            exercise = details.get("运动", "")
            video_url = get_video_link(exercise)
            matched_plan[day][time_slot] = {
                **details,
                "video_url": video_url
            }
    
    return matched_plan


def get_today_video(user_id):
    """获取今天运动的视频链接"""
    from exercise_generator import get_today_plan
    
    today_plan = get_today_plan(user_id)
    if not today_plan:
        return None
    
    plan = today_plan["plan"]
    videos = []
    
    for time_slot, details in plan.items():
        exercise = details.get("运动", "")
        video_url = get_video_link(exercise)
        if video_url:
            videos.append({
                "运动": exercise,
                "时间": time_slot,
                "视频": video_url
            })
    
    return {
        "day": today_plan["day"],
        "videos": videos
    }


def add_video(exercise_name, video_url):
    """添加新视频到库"""
    VIDEO_LIBRARY[exercise_name] = video_url
    
    # 保存到文件
    lib_file = VIDEOS_DIR / "video_library.json"
    with open(lib_file, "w", encoding="utf-8") as f:
        json.dump(VIDEO_LIBRARY, f, ensure_ascii=False, indent=2)
    
    return True


def load_video_library():
    """加载视频库"""
    lib_file = VIDEOS_DIR / "video_library.json"
    if lib_file.exists():
        with open(lib_file, encoding="utf-8") as f:
            return json.load(f)
    return VIDEO_LIBRARY


if __name__ == "__main__":
    # 测试
    print("八段锦视频:", get_video_link("八段锦"))
    print("太极拳视频:", get_video_link("太极拳"))
    print("肩颈拉伸视频:", get_video_link("肩颈拉伸"))
    print("散步视频:", get_video_link("散步"))