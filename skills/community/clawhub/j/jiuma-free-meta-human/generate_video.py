#!/usr/bin/env python3
"""
九码AI数字人视频生成脚本
根据数字人ID、音色ID和文本内容生成视频
"""

import os
import sys
import json
import argparse
import traceback
import uuid
import requests
from typing import Dict
import codecs
from utils import JIUMA_API_KEY_SAVE_PATH, get_jiuma_api_key

# Windows终端编码处理
if sys.platform == "win32":
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)


# 获取mac 地址
# def get_mac():
#     return ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8*6, 8)][::-1])

class JiumaVideoGenerator:
    def __init__(self, api_key):
        self.base_url = "https://api.jiuma.com"
        self.headers = {
            "Content-Type": "application/json",
            "X-Secret-Key": api_key,
        }

    def generate_video(self, human_id: str, voice_id: str, text: str) -> Dict:
        """
        生成数字人视频
        """
        url = f"{self.base_url}/DigitalHumanVideo/createDigitalHumanVideo"

        payload = {
            "human_id": human_id,
            "voice_id": voice_id,
            "text": text,
            "platform": "15",
        }

        try:
            print(f"正在生成视频... 数字人ID: {human_id}, 音色ID: {voice_id}")
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()

            result = response.json()
            response.close()
            if result.get('code') == 500:
                return {"code": 500, "error": result.get('message')}
            if result.get('code') == 401 or result.get('code') == 405:
                # 提示用户必须登录
                return {"code": result.get('code')}
            if result.get('code') == 406:
                return {"code": result.get('code'),"pay_address":result.get('data',{})[0].get('qrcode_url')}

            human_video_id = result.get('data')

            print(f"✅ 视频生成任务已创建!")
            print(f"human_video_id 为: {human_video_id}")
            print("⏳ 视频正在生成中，稍后每分钟会主动返回任务状态...")
            return {"code": 200, "error": "", "human_video_id": int(human_video_id)}

        except requests.exceptions.RequestException as e:
            print(f"❌ 网络请求失败: {e}")
            return {"code": 500, "error": str(e)}
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            return {"code": 500, "error": "响应格式错误"}

    def check_task_status(self, human_video_id) -> Dict:
        """
        检查任务状态
        """
        url = f"{self.base_url}/DigitalHumanVideo/digitalHumanVideoInfo"

        try:
            data = {"human_video_id": str(human_video_id)}
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()

            result = response.json()
            response.close()

            if result.get("code") == 200:
                status = result.get("data", {}).get("check_status")

                status_map = {
                    17: "远程调度制作失败",
                    13: "视频制作中",
                    21: "已完成",
                }

                status_text = status_map.get(status, status)
                print(f"任务状态: {status_text}")

                if status == 21:
                    video_url = result.get("data", {}).get("new_video_file_url")
                    print(f"✅ 视频生成完成!")
                    print(f"视频链接: {video_url}")
                    return {"code": 200, "status": status, "message": "", "video_url": video_url}
                elif status == 17:
                    error_msg = result.get("data", {}).get("error", "未知错误")
                    print(f"❌ 视频生成失败: {error_msg}")
                    return {"code": 200, "status": status, "message": error_msg, "video_url": ""}
                else:
                    return {"code": 200, "status": status, "message": "处理中", "video_url": ""}
            else:
                error_msg = result.get("message", "远程服务器报错")
                print(f"❌ 查询失败: {error_msg}")
                return {"code": 500, "status": "", "message": error_msg, "video_url": ""}

        except requests.exceptions.RequestException as e:
            print(f"❌ 网络请求失败: {e}")
            return {"code": 500, "status": "", "message": str(e), "video_url": ""}


def main():
    try:
        parser = argparse.ArgumentParser(description="九马AI数字人生成工具")
        parser.add_argument("--action", type=str, help="create或check", required=True)
        parser.add_argument("--text", type=str, help="文本那内容", required=False,default='')
        parser.add_argument("--human_id", type=str, help="数字人id", required=False,default='')
        parser.add_argument("--voice_id", type=str, help="音色id", required=False,default='')
        parser.add_argument("--human_video_id", type=int, help="human_video_id", required=False)
        args = parser.parse_args()

        action = args.action
        text = args.text
        human_id = args.human_id
        voice_id = args.voice_id
        human_video_id = args.human_video_id

        if os.path.exists(JIUMA_API_KEY_SAVE_PATH):
            api_key = get_jiuma_api_key()
        else:
            api_key = ''


        generator = JiumaVideoGenerator(api_key)
        if action == 'create':
            # 生成视频
            result = generator.generate_video(human_id, voice_id, text)
            print(f'数字人生成结果: {result}')

        if action == 'check':
            # 查询状态
            result = generator.check_task_status(human_video_id)
            print(f'查询结果: {result}')

    except Exception as e:
        print(traceback.format_exc())
        print(f"❌ 程序执行出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
