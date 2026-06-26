#!/usr/bin/env python3
"""
MiniMax 音乐生成脚本
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


def generate_music(prompt: str, model: str = "music-02",
                    lyrics: str = None, output_path: str = "output.mp3") -> str:
    """调用 MiniMax 音乐生成 API"""
    url = f"{API_HOST}/v1/music_generation"

    payload = {
        "model": model,
        "prompt": prompt,
    }
    if lyrics:
        payload["lyrics"] = lyrics

    print(f"🎵 正在生成音乐...")
    print(f"   模型: {model}")
    print(f"   描述: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")
    if lyrics:
        print(f"   歌词: {lyrics[:50]}{'...' if len(lyrics) > 50 else ''}")

    resp = requests.post(url, headers=HEADERS, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    base_resp = data.get("base_resp", {})
    if base_resp.get("status_code") != 0:
        task_id = data.get("task_id")
        if task_id:
            print(f"⏳ 异步任务 ID: {task_id}，开始轮询...")
            file_id = poll_music_task(task_id)
            if file_id:
                download_music(file_id, output_path)
                return output_path
        raise Exception(f"API Error: {base_resp.get('status_msg', 'unknown')}")

    # 同步返回
    raise Exception("音乐生成接口暂不支持同步调用，需使用异步模式")


def poll_music_task(task_id: str, max_wait: int = 600) -> str:
    """轮询音乐生成任务状态"""
    url = f"{API_HOST}/v1/query/music_generation"
    params = {"task_id": task_id}

    for i in range(max_wait // 10):
        time.sleep(10)
        resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        status = data.get("status", "")
        print(f"  状态: {status}")
        if status == "Success":
            return data.get("file_id", "")
        elif status == "Fail":
            raise Exception(f"音乐生成失败: {data.get('error_message', 'unknown')}")
    raise Exception("音乐生成任务超时")


def download_music(file_id: str, output_path: str):
    """下载音乐文件"""
    url = f"{API_HOST}/v1/files/retrieve"
    params = {"file_id": file_id}
    resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
    resp.raise_for_status()
    download_url = resp.json()["file"]["download_url"]

    print(f"📥 正在下载音乐至 {output_path}...")
    with open(output_path, "wb") as f:
        vr = requests.get(download_url, timeout=120)
        vr.raise_for_status()
        f.write(vr.content)
    print(f"✅ 音乐已保存: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="MiniMax 音乐生成")
    parser.add_argument("--model", default="music-02",
                        help="模型: music-02, music-2.5, music-2.5+")
    parser.add_argument("--prompt", required=True, help="音乐描述文本")
    parser.add_argument("--lyrics", help="歌词（可选）")
    parser.add_argument("--output", default="output.mp3", help="输出文件路径")

    args = parser.parse_args()

    try:
        result = generate_music(
            prompt=args.prompt,
            model=args.model,
            lyrics=args.lyrics,
            output_path=args.output,
        )
        print(f"\n📎 输出文件: {result}")
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
