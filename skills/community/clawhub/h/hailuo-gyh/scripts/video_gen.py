#!/usr/bin/env python3
"""
MiniMax 海螺视频生成 -龚云荷定制版
API Key 已内置，无需配置环境变量
"""

import os
import sys
import time
import argparse
import requests

API_KEY = os.environ.get("MINIMAX_API_KEY")
if not API_KEY:
    print("Error: MINIMAX_API_KEY environment variable not set")
    print("Please set it with: export MINIMAX_API_KEY=\"your-api-key\"")
    sys.exit(1)

HEADERS = {"Authorization": f"Bearer {API_KEY}"}
API_HOST = "https://api.minimaxi.com"


def invoke_text_to_video(prompt: str, duration: int = 6, resolution: str = "768P") -> str:
    """(模式一) 文生视频"""
    url = f"{API_HOST}/v1/video_generation"
    payload = {
        "prompt": prompt,
        "model": "MiniMax-Hailuo-2.3",
        "duration": duration,
        "resolution": resolution,
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    task_id = response.json()["task_id"]
    return task_id


def invoke_image_to_video(prompt: str, image_url: str, duration: int = 6, resolution: str = "768P") -> str:
    """(模式二) 图生视频"""
    url = f"{API_HOST}/v1/video_generation"
    payload = {
        "prompt": prompt,
        "first_frame_image": image_url,
        "model": "MiniMax-Hailuo-2.3",
        "duration": duration,
        "resolution": resolution,
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    task_id = response.json()["task_id"]
    return task_id


def invoke_start_end_to_video(prompt: str, first_image: str, last_image: str, duration: int = 6, resolution: str = "768P") -> str:
    """(模式三) 首尾帧视频"""
    url = f"{API_HOST}/v1/video_generation"
    payload = {
        "prompt": prompt,
        "first_frame_image": first_image,
        "last_frame_image": last_image,
        "model": "MiniMax-Hailuo-02",
        "duration": duration,
        "resolution": resolution,
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    task_id = response.json()["task_id"]
    return task_id


def invoke_subject_reference(prompt: str, subject_image: str, duration: int = 6, resolution: str = "768P") -> str:
    """(模式四) 主体参考视频"""
    url = f"{API_HOST}/v1/video_generation"
    payload = {
        "prompt": prompt,
        "subject_reference": [
            {
                "type": "character",
                "image": [subject_image],
            }
        ],
        "model": "S2V-01",
        "duration": duration,
        "resolution": resolution,
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    task_id = response.json()["task_id"]
    return task_id


def query_task_status(task_id: str) -> str:
    """轮询任务状态，直至成功或失败"""
    url = f"{API_HOST}/v1/query/video_generation"
    params = {"task_id": task_id}

    print(f"🎬 任务已提交，task_id: {task_id}")
    print("⏳ 正在等待视频生成（每10秒查询一次）...")

    while True:
        time.sleep(10)
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        response_json = response.json()
        status = response_json["status"]
        print(f"  状态: {status}")

        if status == "Success":
            return response_json["file_id"]
        elif status == "Fail":
            raise Exception(f"❌ 视频生成失败: {response_json.get('error_message', '未知错误')}")


def fetch_video(file_id: str, output_path: str = "output.mp4"):
    """下载视频到本地"""
    url = f"{API_HOST}/v1/files/retrieve"
    params = {"file_id": file_id}
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    download_url = response.json()["file"]["download_url"]

    print(f"📥 正在下载视频至 {output_path}...")
    with open(output_path, "wb") as f:
        video_response = requests.get(download_url)
        video_response.raise_for_status()
        f.write(video_response.content)
    print(f"✅ 视频已保存: {output_path} ({os.path.getsize(output_path) / 1024:.0f} KB)")


def main():
    parser = argparse.ArgumentParser(description="MiniMax 海螺视频生成（龚云荷定制版）")
    parser.add_argument("--mode", required=True, choices=["text", "image", "start_end", "subject"],
                        help="生成模式: text(图生视频), image(首帧图片+提示词), start_end(首尾帧), subject(主体参考)")
    parser.add_argument("--prompt", required=True, help="视频描述文本（建议英文）")
    parser.add_argument("--image", help="图片URL（image模式使用）")
    parser.add_argument("--first", help="首帧图片URL（start_end模式）")
    parser.add_argument("--last", help="尾帧图片URL（start_end模式）")
    parser.add_argument("--subject", help="人脸图片URL（subject模式）")
    parser.add_argument("--duration", type=int, default=6, choices=[6, 10], help="视频时长，默认6秒")
    parser.add_argument("--resolution", default="768P", choices=["720P", "768P", "1080P"], help="分辨率，默认768P")
    parser.add_argument("--output", default="output.mp4", help="输出文件路径")

    args = parser.parse_args()

    # 验证参数
    if args.mode == "image" and not args.image:
        parser.error("❌ image 模式需要 --image 参数")
    if args.mode == "start_end" and (not args.first or not args.last):
        parser.error("❌ start_end 模式需要 --first 和 --last 参数")
    if args.mode == "subject" and not args.subject:
        parser.error("❌ subject 模式需要 --subject 参数")

    print(f"🎬 MiniMax 海螺视频生成")
    print(f"📋 模式: {args.mode}")
    print(f"📝 描述: {args.prompt[:80]}{'...' if len(args.prompt) > 80 else ''}")
    print(f"⏱️ 时长: {args.duration}秒 | 分辨率: {args.resolution}")
    print()

    if args.mode == "text":
        task_id = invoke_text_to_video(args.prompt, args.duration, args.resolution)
    elif args.mode == "image":
        task_id = invoke_image_to_video(args.prompt, args.image, args.duration, args.resolution)
    elif args.mode == "start_end":
        task_id = invoke_start_end_to_video(args.prompt, args.first, args.last, args.duration, args.resolution)
    else:
        task_id = invoke_subject_reference(args.prompt, args.subject, args.duration, args.resolution)

    file_id = query_task_status(task_id)
    fetch_video(file_id, args.output)


if __name__ == "__main__":
    main()
