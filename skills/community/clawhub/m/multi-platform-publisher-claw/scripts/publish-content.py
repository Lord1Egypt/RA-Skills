#!/usr/bin/env python3
"""
多平台内容发布主程序
依赖：python3, selenium, requests
用法：
  python3 publish-content.py --platform douyin --video video.mp4 --title "标题" --desc "描述"
  python3 publish-content.py --all --video video.mp4 --title "标题" --desc "描述"
  python3 publish-content.py --all --video video.mp4 --title "标题" --desc "描述" --schedule "2026-04-02 09:00"
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime

SUPPORTED_PLATFORMS = ["douyin", "xiaohongshu", "shipinhao", "bilibili", "weibo"]

PLATFORM_RULES = {
    "douyin":       {"title_max": 55,  "desc_max": 2200, "cover_ratio": "16:9"},
    "xiaohongshu":  {"title_max": 20,  "desc_max": 1000, "cover_ratio": "3:4"},
    "shipinhao":    {"title_max": 30,  "desc_max": 1000, "cover_ratio": "16:9"},
    "bilibili":     {"title_max": 80,  "desc_max": 2000, "cover_ratio": "16:9"},
    "weibo":        {"title_max": 140, "desc_max": 2000, "cover_ratio": "1:1"},
}


def adapt_content(platform: str, title: str, desc: str) -> dict:
    """根据平台规则适配内容"""
    rules = PLATFORM_RULES[platform]
    adapted_title = title[:rules["title_max"]]
    adapted_desc = desc[:rules["desc_max"]]
    return {
        "platform": platform,
        "title": adapted_title,
        "desc": adapted_desc,
        "cover_ratio": rules["cover_ratio"],
    }


def publish_to_platform(platform: str, content: dict, video_path: str, schedule_time: str = None) -> dict:
    """
    发布内容到指定平台（实际实现需对接各平台API或selenium自动化）
    返回：{"platform": str, "status": "success"|"failed"|"pending", "url": str, "error": str}
    """
    print(f"[{platform}] 正在发布...")
    # TODO: 对接各平台API或selenium自动化脚本
    # 示例：调用平台API
    # response = requests.post(PLATFORM_API[platform], data={...})
    
    # 模拟发布结果（实际使用时替换为真实API调用）
    result = {
        "platform": platform,
        "status": "success",
        "url": f"https://{platform}.example.com/video/mock_id",
        "error": None,
        "schedule_time": schedule_time,
    }
    print(f"[{platform}] 发布成功 ✓ {result['url']}")
    return result


def publish_with_retry(platform: str, content: dict, video_path: str, schedule_time: str = None, max_retries: int = 3) -> dict:
    """带重试机制的发布"""
    for attempt in range(1, max_retries + 1):
        try:
            result = publish_to_platform(platform, content, video_path, schedule_time)
            if result["status"] == "success":
                return result
        except Exception as e:
            print(f"[{platform}] 第{attempt}次尝试失败: {e}")
            if attempt < max_retries:
                time.sleep(2 ** attempt)  # 指数退避
    return {"platform": platform, "status": "failed", "url": None, "error": "超过最大重试次数"}


def main():
    parser = argparse.ArgumentParser(description="多平台内容发布工具")
    parser.add_argument("--platform", help="目标平台，逗号分隔（如 douyin,bilibili）")
    parser.add_argument("--all", action="store_true", help="发布到所有平台")
    parser.add_argument("--video", required=True, help="视频文件路径")
    parser.add_argument("--cover", help="封面图片路径")
    parser.add_argument("--title", required=True, help="内容标题")
    parser.add_argument("--desc", default="", help="内容描述")
    parser.add_argument("--tags", help="话题标签，逗号分隔")
    parser.add_argument("--schedule", help="定时发布时间，格式：YYYY-MM-DD HH:MM")
    args = parser.parse_args()

    # 确定目标平台
    if args.all:
        platforms = SUPPORTED_PLATFORMS
    elif args.platform:
        platforms = [p.strip() for p in args.platform.split(",")]
        invalid = [p for p in platforms if p not in SUPPORTED_PLATFORMS]
        if invalid:
            print(f"不支持的平台: {invalid}，支持的平台: {SUPPORTED_PLATFORMS}")
            sys.exit(1)
    else:
        print("请指定 --platform 或 --all")
        sys.exit(1)

    # 检查视频文件
    if not os.path.exists(args.video):
        print(f"视频文件不存在: {args.video}")
        sys.exit(1)

    print(f"\n📦 内容包信息")
    print(f"  视频: {args.video}")
    print(f"  标题: {args.title}")
    print(f"  目标平台: {', '.join(platforms)}")
    if args.schedule:
        print(f"  定时发布: {args.schedule}")
    print()

    # 逐平台适配并发布
    results = []
    for platform in platforms:
        content = adapt_content(platform, args.title, args.desc)
        result = publish_with_retry(platform, content, args.video, args.schedule)
        results.append(result)

    # 输出汇总报告
    print("\n📊 发布汇总报告")
    print("-" * 40)
    success_count = sum(1 for r in results if r["status"] == "success")
    for r in results:
        status_icon = "✅" if r["status"] == "success" else "❌"
        print(f"{status_icon} {r['platform']}: {r['status']}")
        if r["url"]:
            print(f"   链接: {r['url']}")
        if r["error"]:
            print(f"   错误: {r['error']}")
    print("-" * 40)
    print(f"成功: {success_count}/{len(platforms)} 个平台")

    # 保存发布记录
    record = {
        "timestamp": datetime.now().isoformat(),
        "title": args.title,
        "video": args.video,
        "results": results,
    }
    record_path = f"publish-record-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(record_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"\n📝 发布记录已保存: {record_path}")


if __name__ == "__main__":
    main()
