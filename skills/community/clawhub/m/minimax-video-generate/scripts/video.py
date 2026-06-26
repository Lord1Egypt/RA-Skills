#!/usr/bin/env python3
"""
MiniMax Video API Client
视频生成、图生视频、视频查询等功能
"""

import os
import json
import time
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


def generate_video(
    prompt: str,
    model: str = "MiniMax-Hailuo-2.3"
) -> List[str]:
    """
    文生视频 - 根据文本描述生成视频

    Args:
        prompt: 视频描述文本
        model: 视频生成模型

    Returns:
        任务ID列表
    """
    url = f"{get_base_url()}/video_generation"

    payload = {
        "model": model,
        "prompt": prompt
    }

    response = requests.post(url, headers=get_headers(), json=payload, timeout=60)
    response.raise_for_status()

    result = response.json()
    task_id = result.get("task_id")
    return [task_id] if task_id else []


def generate_video_with_image(
    prompt: str,
    image_url: str,
    model: str = "MiniMax-Hailuo-2.3"
) -> List[str]:
    """
    图生视频 - 根据参考图和文本描述生成视频

    Args:
        prompt: 视频描述文本
        image_url: 参考图片URL
        model: 视频生成模型

    Returns:
        任务ID列表
    """
    url = f"{get_base_url()}/video_generation"

    payload = {
        "model": model,
        "prompt": prompt,
        "image_url": image_url
    }

    response = requests.post(url, headers=get_headers(), json=payload, timeout=60)
    response.raise_for_status()

    result = response.json()
    task_id = result.get("task_id")
    return [task_id] if task_id else []


def generate_video_with_frames(
    prompt: str,
    start_image_url: str,
    end_image_url: str,
    model: str = "MiniMax-Hailuo-2.3"
) -> List[str]:
    """
    首尾帧视频 - 根据起始帧、结束帧和描述生成过渡视频

    Args:
        prompt: 视频描述文本
        start_image_url: 起始帧图片URL
        end_image_url: 结束帧图片URL
        model: 视频生成模型

    Returns:
        任务ID列表
    """
    url = f"{get_base_url()}/video_generation"

    payload = {
        "model": model,
        "prompt": prompt,
        "start_image_url": start_image_url,
        "end_image_url": end_image_url
    }

    response = requests.post(url, headers=get_headers(), json=payload, timeout=60)
    response.raise_for_status()

    result = response.json()
    task_id = result.get("task_id")
    return [task_id] if task_id else []


def generate_video_with_subject(
    prompt: str,
    subject_image_url: str,
    model: str = "MiniMax-Hailuo-2.3"
) -> List[str]:
    """
    主体参考视频 - 根据主体参考图和描述生成视频

    Args:
        prompt: 视频描述文本
        subject_image_url: 主体参考图片URL
        model: 视频生成模型

    Returns:
        任务ID列表
    """
    url = f"{get_base_url()}/video_generation"

    payload = {
        "model": model,
        "prompt": prompt,
        "subject_image_url": subject_image_url
    }

    response = requests.post(url, headers=get_headers(), json=payload, timeout=60)
    response.raise_for_status()

    result = response.json()
    task_id = result.get("task_id")
    return [task_id] if task_id else []


def query_video_task(task_id: str) -> Dict[str, Any]:
    """
    查询视频生成任务状态

    Args:
        task_id: 任务ID

    Returns:
        任务状态信息 (包含 status, video_url 等)
    """
    url = f"{get_base_url()}/query/video_generation"
    params = {"task_id": task_id}

    response = requests.get(url, headers=get_headers(), params=params, timeout=30)
    response.raise_for_status()

    return response.json()


def wait_for_video(
    task_id: str,
    poll_interval: int = 10,
    max_wait: int = 600,
    output_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    等待视频生成完成，并可选自动下载

    Args:
        task_id: 任务ID
        poll_interval: 轮询间隔（秒）
        max_wait: 最大等待时间（秒）
        output_path: 可选，本地保存路径，完成后自动下载

    Returns:
        最终任务状态信息，包含 video_path (如果指定了output_path)

    Raises:
        TimeoutError: 等待超时
    """
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        if elapsed > max_wait:
            raise TimeoutError(f"Video generation timeout after {max_wait} seconds")

        result = query_video_task(task_id)
        status = result.get("status", "")

        print(f"[{elapsed:.0f}s] Status: {status}")

        if status == "Success":
            # 自动下载视频
            if output_path:
                file_id = result.get("file_id")
                if file_id:
                    result["video_path"] = download_video(file_id, output_path)
                else:
                    # 从 video_url 下载
                    video_url = result.get("video_url")
                    if video_url:
                        result["video_path"] = _download_from_url(video_url, output_path)
            return result
        elif status == "Fail":
            raise RuntimeError(f"Video generation failed: {result.get('error', 'Unknown error')}")

        time.sleep(poll_interval)


def _download_from_url(url: str, output_path: str) -> str:
    """从 URL 下载视频"""
    response = requests.get(url, timeout=300, stream=True)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    return output_path


def get_file_info(file_id: str) -> Dict[str, Any]:
    """
    获取文件信息

    Args:
        file_id: 文件ID

    Returns:
        文件信息 (包含 download_url)
    """
    url = f"{get_base_url()}/files/retrieve"
    params = {"file_id": file_id}

    response = requests.get(url, headers=get_headers(), params=params, timeout=30)
    response.raise_for_status()

    return response.json()


def download_video(
    file_id: str,
    output_path: Optional[str] = None
) -> str:
    """
    下载视频到本地

    Args:
        file_id: 文件ID
        output_path: 保存路径，如果为None则自动生成

    Returns:
        保存的文件路径
    """
    # 获取文件信息
    file_info = get_file_info(file_id)
    download_url = file_info.get("file", {}).get("download_url")

    if not download_url:
        raise ValueError("No download URL available")

    # 下载文件
    response = requests.get(download_url, timeout=300, stream=True)
    response.raise_for_status()

    # 自动生成文件名
    if output_path is None:
        output_path = f"video_{file_id}.mp4"

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    return output_path


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="MiniMax Video API Client")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 文生视频命令
    gen_parser = subparsers.add_parser("generate", help="文生视频")
    gen_parser.add_argument("prompt", help="视频描述")
    gen_parser.add_argument("-o", "--output", help="输出文件路径，指定后自动下载")

    # 图生视频命令
    img2vid_parser = subparsers.add_parser("from-image", help="图生视频")
    img2vid_parser.add_argument("prompt", help="视频描述")
    img2vid_parser.add_argument("-i", "--image", required=True, help="参考图URL")
    img2vid_parser.add_argument("-o", "--output", help="输出文件路径，指定后自动下载")

    # 首尾帧命令
    frames_parser = subparsers.add_parser("frames", help="首尾帧视频")
    frames_parser.add_argument("prompt", help="视频描述")
    frames_parser.add_argument("-s", "--start", required=True, help="起始帧图片URL")
    frames_parser.add_argument("-e", "--end", required=True, help="结束帧图片URL")
    frames_parser.add_argument("-o", "--output", help="输出文件路径，指定后自动下载")

    # 主体参考命令
    subject_parser = subparsers.add_parser("subject", help="主体参考视频")
    subject_parser.add_argument("prompt", help="视频描述")
    subject_parser.add_argument("-i", "--image", required=True, help="主体参考图URL")
    subject_parser.add_argument("-o", "--output", help="输出文件路径，指定后自动下载")

    # 查询命令
    query_parser = subparsers.add_parser("query", help="查询任务状态")
    query_parser.add_argument("task_id", help="任务ID")

    # 等待命令
    wait_parser = subparsers.add_parser("wait", help="等待视频生成完成")
    wait_parser.add_argument("task_id", help="任务ID")
    wait_parser.add_argument("-i", "--interval", type=int, default=10, help="轮询间隔（秒）")
    wait_parser.add_argument("-o", "--output", help="输出文件路径，指定后自动下载")

    # 下载命令
    dl_parser = subparsers.add_parser("download", help="下载视频")
    dl_parser.add_argument("file_id", help="文件ID")
    dl_parser.add_argument("-o", "--output", help="保存路径")

    args = parser.parse_args()

    try:
        if args.command == "generate":
            task_ids = generate_video(args.prompt)
            print(f"Task IDs: {task_ids}")
            if args.output:
                result = wait_for_video(task_ids[0], output_path=args.output)
                print(f"Video saved to: {result.get('video_path', args.output)}")

        elif args.command == "from-image":
            task_ids = generate_video_with_image(args.prompt, args.image)
            print(f"Task IDs: {task_ids}")
            if args.output:
                result = wait_for_video(task_ids[0], output_path=args.output)
                print(f"Video saved to: {result.get('video_path', args.output)}")

        elif args.command == "frames":
            task_ids = generate_video_with_frames(args.prompt, args.start, args.end)
            print(f"Task IDs: {task_ids}")
            if args.output:
                result = wait_for_video(task_ids[0], output_path=args.output)
                print(f"Video saved to: {result.get('video_path', args.output)}")

        elif args.command == "subject":
            task_ids = generate_video_with_subject(args.prompt, args.image)
            print(f"Task IDs: {task_ids}")
            if args.output:
                result = wait_for_video(task_ids[0], output_path=args.output)
                print(f"Video saved to: {result.get('video_path', args.output)}")

        elif args.command == "query":
            result = query_video_task(args.task_id)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "wait":
            result = wait_for_video(args.task_id, poll_interval=args.interval, output_path=args.output)
            print("\nVideo ready!")
            print(f"Status: {result.get('status')}")
            if result.get('video_path'):
                print(f"Video saved to: {result.get('video_path')}")
            else:
                print(f"Video URL: {result.get('video_url', 'N/A')}")

        elif args.command == "download":
            output_path = download_video(args.file_id, args.output)
            print(f"Video saved to: {output_path}")

        else:
            parser.print_help()

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code}")
        print(e.response.text)
        raise


if __name__ == "__main__":
    main()
