#!/usr/bin/env python3
"""
创建会议脚本
基于references/CreateMeeting.md

用途：创建新的会议。
"""

import requests
import sys

# 用户配置
BASE_URL = "https://apigw.125339.com.cn"
ACCESS_TOKEN = input("请输入Access Token (从get_token.py获取): ").strip()

def create_meeting(subject, start_time="", length=30, media_types="HDVideo"):
    """创建会议"""
    url = f"{BASE_URL}/v1/mmc/management/conferences"
    headers = {
        "X-Access-Token": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    payload = {
        "subject": subject,
        "mediaTypes": media_types,
        "length": length
    }
    if start_time:
        payload["startTime"] = start_time

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        print("会议创建成功:")
        if isinstance(data, dict):
            conference_id = data.get('conferenceID') or data.get('conferenceId')
            print(f"会议ID: {conference_id}")
            print(f"会议主题: {data.get('subject')}")
        elif isinstance(data, list) and data:
            first = data[0]
            if isinstance(first, dict):
                conference_id = first.get('conferenceID') or first.get('conferenceId')
                print(f"会议ID: {conference_id}")
                print(f"会议主题: {first.get('subject')}")
            else:
                print(f"返回数据: {data}")
        else:
            print(f"返回数据: {data}")
        return data
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    subject = input("请输入会议主题: ").strip()
    start_time = input("请输入开始时间 (UTC, yyyy-MM-dd HH:mm, 可留空): ").strip()
    length = int(input("请输入持续时长(分钟, 默认30): ") or 30)
    media_types = input("请输入媒体类型 (HDVideo或Voice, 默认HDVideo): ").strip() or "HDVideo"

    create_meeting(subject, start_time, length, media_types)