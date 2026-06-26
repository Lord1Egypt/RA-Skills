#!/usr/bin/env python3
"""
MiniMax Music API Client
音乐生成、歌词生成等功能
"""

import os
import json
import time
import base64
import argparse
from typing import Optional, Dict, Any, List

import requests


# API 配置
BASE_URL_CN = "https://api.minimaxi.com/v1"
BASE_URL_INT = "https://api.minimax.io/v1"


def get_base_url() -> str:
    """获取 API 基础 URL"""
    return BASE_URL_CN if os.getenv("MINIMAX_REGION", "cn") == "cn" else BASE_URL_INT


def get_headers() -> Dict[str, str]:
    """获取请求头"""
    api_key = os.getenv("MINIMAX_API_KEY")
    if not api_key:
        raise ValueError("MINIMAX_API_KEY environment variable is not set")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }


def generate_music(
    lyrics: str,
    description: str,
    output_path: Optional[str] = None,
    model: str = "music-2.5"
) -> str:
    """
    音乐生成并保存到本地

    Args:
        lyrics: 歌词内容
        description: 音乐描述/风格
        output_path: 本地保存路径，如不提供则自动生成
        model: 音乐生成模型

    Returns:
        保存的本地文件路径
    """
    url = f"{get_base_url()}/music_generation"

    payload = {
        "model": model,
        "lyrics": lyrics,
        "description": description
    }

    response = requests.post(url, headers=get_headers(), json=payload, timeout=300)
    response.raise_for_status()

    result = response.json()
    audio_data = result.get("data", {}).get("audio", "")

    if not audio_data:
        raise ValueError("No audio data returned")

    # 自动生成文件名
    if output_path is None:
        import uuid
        output_path = f"music_{uuid.uuid4().hex[:8]}.mp3"

    # 音频数据是 hex 编码的 (ID3/MP3 header: 494433 = "ID3")
    audio_bytes = bytes.fromhex(audio_data)
    with open(output_path, "wb") as f:
        f.write(audio_bytes)

    return output_path


def generate_lyrics(
    description: str,
    keywords: Optional[List[str]] = None,
    model: str = "lyrics-01"
) -> str:
    """
    歌词生成

    Args:
        description: 歌曲描述/主题
        keywords: 关键词列表
        model: 歌词生成模型

    Returns:
        生成的歌词内容
    """
    url = f"{get_base_url()}/lyrics_generation"

    payload = {
        "model": model,
        "description": description
    }

    if keywords:
        payload["keywords"] = keywords

    response = requests.post(url, headers=get_headers(), json=payload, timeout=60)
    response.raise_for_status()

    result = response.json()
    return result.get("lyrics", "")


def query_music_task(task_id: str) -> Dict[str, Any]:
    """
    查询音乐生成任务状态

    Args:
        task_id: 任务ID

    Returns:
        任务状态信息 (包含 status, music_url 等)
    """
    url = f"{get_base_url()}/query/video_generation"
    params = {"task_id": task_id}

    response = requests.get(url, headers=get_headers(), params=params, timeout=30)
    response.raise_for_status()

    return response.json()


def wait_for_music(
    task_id: str,
    poll_interval: int = 10,
    max_wait: int = 600,
    output_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    等待音乐生成完成，并可选自动下载

    Args:
        task_id: 任务ID
        poll_interval: 轮询间隔（秒）
        max_wait: 最大等待时间（秒）
        output_path: 可选，本地保存路径，完成后自动下载

    Returns:
        最终任务状态信息，包含 music_path (如果指定了output_path)

    Raises:
        TimeoutError: 等待超时
    """
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        if elapsed > max_wait:
            raise TimeoutError(f"Music generation timeout after {max_wait} seconds")

        result = query_music_task(task_id)
        status = result.get("status", "")

        print(f"[{elapsed:.0f}s] Status: {status}")

        if status == "Success":
            if output_path:
                music_url = result.get("music_url")
                if music_url:
                    result["music_path"] = download_music(music_url, output_path)
            return result
        elif status == "Fail":
            raise RuntimeError(f"Music generation failed: {result.get('error', 'Unknown error')}")

        time.sleep(poll_interval)


def download_music(
    music_url: str,
    output_path: str
) -> str:
    """
    下载音乐到本地

    Args:
        music_url: 音乐下载URL
        output_path: 保存路径

    Returns:
        保存的文件路径
    """
    response = requests.get(music_url, timeout=300, stream=True)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    return output_path


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="MiniMax Music API Client")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 音乐生成命令
    music_parser = subparsers.add_parser("generate", help="生成音乐")
    music_parser.add_argument("lyrics", help="歌词内容")
    music_parser.add_argument("-d", "--description", required=True, help="音乐描述")
    music_parser.add_argument("-o", "--output", help="输出文件路径，指定后自动下载")

    # 歌词生成命令
    lyrics_parser = subparsers.add_parser("lyrics", help="生成歌词")
    lyrics_parser.add_argument("description", help="歌曲描述/主题")
    lyrics_parser.add_argument("-k", "--keywords", nargs="+", help="关键词列表")

    # 查询命令
    query_parser = subparsers.add_parser("query", help="查询任务状态")
    query_parser.add_argument("task_id", help="任务ID")

    # 等待命令
    wait_parser = subparsers.add_parser("wait", help="等待音乐生成完成")
    wait_parser.add_argument("task_id", help="任务ID")
    wait_parser.add_argument("-i", "--interval", type=int, default=10, help="轮询间隔（秒）")
    wait_parser.add_argument("-o", "--output", help="输出文件路径，指定后自动下载")

    # 下载命令
    dl_parser = subparsers.add_parser("download", help="下载音乐")
    dl_parser.add_argument("url", help="音乐URL")
    dl_parser.add_argument("-o", "--output", required=True, help="保存路径")

    args = parser.parse_args()

    try:
        if args.command == "generate":
            output_path = generate_music(args.lyrics, args.description, args.output)
            print(f"Music saved to: {output_path}")

        elif args.command == "lyrics":
            lyrics = generate_lyrics(args.description, args.keywords)
            print("Generated lyrics:")
            print("-" * 40)
            print(lyrics)
            print("-" * 40)

        elif args.command == "query":
            result = query_music_task(args.task_id)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "wait":
            result = wait_for_music(args.task_id, poll_interval=args.interval, output_path=args.output)
            print("\nMusic ready!")
            print(f"Status: {result.get('status')}")
            if result.get('music_path'):
                print(f"Music saved to: {result.get('music_path')}")
            else:
                print(f"Music URL: {result.get('music_url', 'N/A')}")

        elif args.command == "download":
            output_path = download_music(args.url, args.output)
            print(f"Music saved to: {output_path}")

        else:
            parser.print_help()

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code}")
        print(e.response.text)
        raise


if __name__ == "__main__":
    main()
