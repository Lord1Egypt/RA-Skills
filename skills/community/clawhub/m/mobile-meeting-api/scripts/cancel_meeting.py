#!/usr/bin/env python3
"""
取消会议脚本
基于references/CancelMeeting.md

用途：取消已预约的会议。
"""

import requests
import sys

# 用户配置
BASE_URL = "https://apigw.125339.com.cn"
ACCESS_TOKEN = input("请输入Access Token (从get_token.py获取): ").strip()

def cancel_meeting(conference_id, force_end=False):
    """取消会议"""
    url = f"{BASE_URL}/v1/mmc/management/conferences"
    headers = {
        "X-Access-Token": ACCESS_TOKEN
    }
    params = {
        "conferenceID": conference_id
    }
    if force_end:
        params["type"] = 1  # 结束正在召开的会议

    try:
        response = requests.delete(url, headers=headers, params=params)
        response.raise_for_status()
        print("会议取消成功")
        return True
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response is not None else None
        if status_code == 403:
            print("请求失败: 403 Forbidden。可能原因：当前Token没有权限取消该会议，或您不是会议创建者／企业管理员，或会议已开始且未使用 type=1 强制结束。")
        elif status_code == 401:
            print("请求失败: 401 Unauthorized。请检查Access Token是否有效或是否已过期。")
        else:
            print(f"请求失败: {e}")
            if e.response is not None:
                print(f"响应内容: {e.response.text}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    conference_id = input("请输入会议ID: ").strip()
    force_end = input("是否强制结束正在召开的会议? (y/n, 默认n): ").strip().lower() == 'y'

    cancel_meeting(conference_id, force_end)