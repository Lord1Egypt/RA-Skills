#!/usr/bin/env python3
"""
查询会议列表脚本
基于references/SearchMeetings.md

用途：查询尚未结束的会议列表。
"""

import requests
import sys

# 用户配置
BASE_URL = "https://apigw.125339.com.cn"
ACCESS_TOKEN = input("请输入Access Token (从get_token.py获取): ").strip()

def search_meetings(limit=20, search_key=""):
    """查询会议列表"""
    url = f"{BASE_URL}/v1/mmc/management/conferences"
    headers = {
        "X-Access-Token": ACCESS_TOKEN
    }
    params = {
        "limit": limit
    }
    if search_key:
        params["searchKey"] = search_key

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        print("会议查询成功:")
        conferences = []

        if isinstance(data, dict) and "conferences" in data:
            conferences = data.get("conferences", [])
        elif isinstance(data, list):
            conferences = data
        else:
            print("未识别的返回结构：")
            print(data)
            return data

        if not conferences:
            print("没有查询到会议列表。请确认Access Token及查询条件是否正确。")
            print("返回数据：")
            print(data)
            return data

        for conf in conferences:
            conference_id = conf.get("conferenceID") or conf.get("conferenceId")
            print(f"- ID: {conference_id}, 主题: {conf.get('subject')}, 开始时间: {conf.get('startTime')}")
        return data
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    limit = int(input("请输入查询数量 (默认20): ") or 20)
    search_key = input("请输入搜索关键词 (可留空): ").strip()

    search_meetings(limit, search_key)