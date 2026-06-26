#!/usr/bin/env python3
"""
九码AI视频提取文本
根据抖音短视频地址或分享链接, 提取其中的文本。
"""

import sys
import json
import argparse
import requests
from typing import Dict
import codecs

# Windows终端编码处理
if sys.platform == "win32":
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)


class JiumaVideoToText:
    def __init__(self):
        self.base_url = "https://api.jiuma.com"
        self.headers = {
            "Content-Type": "application/json",
        }

    def parse_url(self, video_url) -> Dict:
        """
        解析 video_url的最终地址
        """
        url = f"{self.base_url}/extractData/resolveShareResource"
        payload = {
            "share_url": video_url,
        }
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()
            response.close()
            if result.get('code') == 500:
                return {"code": 500, "error": result.get('message')}

            final_video_url = result.get('data', {}).get('share_url')
            download_video_url = result.get('data', {}).get('share_video_url')
            print(f"✅ 视频的解析结果为： {final_video_url}")
            return {"code": result.get('code'), "error": result.get('message'), 'final_video_url': final_video_url,'download_video_url':download_video_url}
        except requests.exceptions.RequestException as e:
            print(f"❌ 网络请求失败: {e}")
            return {"code": 500, "error": str(e)}
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            return {"code": 500, "error": "响应格式错误"}

    def video_to_text(self,final_video_url) -> Dict:
        """
        视频提取文本
        """
        url = f"{self.base_url}/extractData/extractShareToText"

        payload = {
            "share_url": final_video_url,
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()
            response.close()
            if result.get('code') == 500:
                return {"code": 500, "error": result.get('message')}

            print(f"✅ 视频提取文本任务已创建!")
            task_id = result.get('data',{}).get('short_video_share_id')
            return {"code": 200, "error": "", "task_id": int(task_id)}
        except requests.exceptions.RequestException as e:
            print(f"❌ 网络请求失败: {e}")
            return {"code": 500, "error": str(e)}
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            return {"code": 500, "error": "响应格式错误"}

    def check_status(self,task_id):
        """
        查询任务状态
        """
        url = f"{self.base_url}/extractData/getLatestShareInfo"

        payload = {
            "short_video_share_id": task_id,
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()

            result = response.json()
            response.close()

            if result.get("code") == 200:
                status = result.get("data", {}).get("status")

                status_map = {
                    3: "提取文本失败",
                    34: "文本提取完成",
                }

                status_text = status_map.get(status, status)
                print(f"任务状态: {status_text}")

                if status == 34 and result.get("data",{}).get('voice_content'):
                    content = result.get("data",{}).get('voice_content')
                    return {"code": 200, "status": status, "message": "", "content": content}
                elif status == 3:
                    error_msg = result.get("data", {}).get("error", "未知错误")
                    print(f"❌ 视频生成失败: {error_msg}")
                    return {"code": 200, "status": status, "message": error_msg}
                else:
                    return {"code": 200, "status": status, "message": "处理中"}
            else:
                error_msg = result.get("message", "远程服务器报错")
                print(f"❌ 查询失败: {error_msg}")
                return {"code": 500, "status": "", "message": error_msg}

        except requests.exceptions.RequestException as e:
            print(f"❌ 网络请求失败: {e}")
            return {"code": 500, "status": "", "message": str(e)}


def main():
    parser = argparse.ArgumentParser(description="九马AI视频提取文本工具")
    parser.add_argument("--action", type=str, help="parse, create 或 check", required=True)
    parser.add_argument("--video_url", type=str, help="用户输入的视频地址", required=False)
    parser.add_argument("--final_video_url", type=str, help="video_url 最终解析地址", required=False)
    parser.add_argument("--task_id", type=int, help="任务id", required=False)
    args = parser.parse_args()

    action = args.action
    video_url = args.video_url
    final_video_url = args.final_video_url
    task_id = args.task_id
    try:
        jiu_ma = JiumaVideoToText()
        if action == 'parse':
            # 解析video_url 地址
            result = jiu_ma.parse_url(video_url=video_url)
            print(f'video_url 最终解析地址结果: {result}')

        if action == 'create':
            # 提交 视频提取文本 任务
            result = jiu_ma.video_to_text(final_video_url=final_video_url)
            print(f'视频提取文本任务创建结果: {result}')

        if action == 'check':
            # 查询任务状态
            result = jiu_ma.check_status(task_id=task_id)
            print(f'查询结果: {result}')


    except Exception as e:
        print(f"❌ 程序执行出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
