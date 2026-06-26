#!/usr/bin/env python3
"""
MiniMax Speech API Client
语音合成、语音克隆、语音设计等功能
"""

import os
import json
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


def text_to_speech(
    text: str,
    voice_id: str = "female-tianmei",
    output_file: Optional[str] = None,
    model: str = "speech-2.8-hd",
    format: str = "mp3",
    sample_rate: int = 32000,
    bitrate: int = 128000
) -> str:
    """
    同步语音合成

    Args:
        text: 要转换的文本
        voice_id: 音色ID
        output_file: 输出文件路径，如果为 None 则返回 base64 数据
        model: 语音模型
        format: 音频格式 (mp3, wav, pcm)
        sample_rate: 采样率
        bitrate: 比特率

    Returns:
        输出文件路径或 base64 编码的音频数据
    """
    url = f"{get_base_url()}/t2a_v2"

    payload = {
        "model": model,
        "text": text,
        "stream": False,
        "voice_setting": {
            "voice_id": voice_id
        },
        "audio_setting": {
            "sample_rate": sample_rate,
            "bitrate": bitrate,
            "format": format
        }
    }

    response = requests.post(url, headers=get_headers(), json=payload, timeout=60)
    response.raise_for_status()

    result = response.json()

    # 兼容新旧 API 响应格式
    audio_data_b64 = result.get("audio_file") or result.get("data", {}).get("audio")

    if not audio_data_b64:
        raise ValueError(f"Unexpected API response: {result}")

    if output_file:
        # 解码 base64 并保存
        audio_data = base64.b64decode(audio_data_b64)
        with open(output_file, "wb") as f:
            f.write(audio_data)
        return output_file
    else:
        return audio_data_b64


def text_to_speech_async(
    text: str,
    voice_id: str = "female-tianmei",
    model: str = "speech-2.8-hd",
    format: str = "mp3",
    sample_rate: int = 32000,
    bitrate: int = 128000
) -> List[str]:
    """
    异步语音合成

    Args:
        text: 要转换的文本
        voice_id: 音色ID
        model: 语音模型
        format: 音频格式
        sample_rate: 采样率
        bitrate: 比特率

    Returns:
        任务ID列表
    """
    url = f"{get_base_url()}/t2a_async_v2"

    payload = {
        "model": model,
        "text": text,
        "voice_setting": {
            "voice_id": voice_id
        },
        "audio_setting": {
            "sample_rate": sample_rate,
            "bitrate": bitrate,
            "format": format
        }
    }

    response = requests.post(url, headers=get_headers(), json=payload, timeout=60)
    response.raise_for_status()

    result = response.json()
    return result.get("task_ids", [])


def query_speech_task(task_id: str) -> Dict[str, Any]:
    """
    查询异步语音合成任务状态

    Args:
        task_id: 任务ID

    Returns:
        任务状态信息
    """
    url = f"{get_base_url()}/query/t2a_async_query_v2"
    params = {"task_id": task_id}

    response = requests.get(url, headers=get_headers(), params=params, timeout=30)
    response.raise_for_status()

    return response.json()


def clone_voice(
    audio_file_path: str,
    title: str,
    model: str = "speech-01"
) -> str:
    """
    音色快速复刻

    Args:
        audio_file_path: 音频文件路径
        title: 音色名称
        model: 克隆模型

    Returns:
        新音色的voice_id
    """
    url = f"{get_base_url()}/voice_clone"

    # 读取并编码音频文件
    with open(audio_file_path, "rb") as f:
        audio_data = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "model": model,
        "audios": [audio_data],
        "title": title
    }

    response = requests.post(url, headers=get_headers(), json=payload, timeout=120)
    response.raise_for_status()

    result = response.json()
    return result["voice_id"]


def design_voice(
    text: str,
    style: str = "custom",
    model: str = "speech-01"
) -> str:
    """
    音色设计

    Args:
        text: 音色描述文本
        style: 音色风格
        model: 设计模型

    Returns:
        设计生成的 voice_id
    """
    url = f"{get_base_url()}/voice_design"

    payload = {
        "model": model,
        "text": text,
        "voice_setting": {
            "style": style
        }
    }

    response = requests.post(url, headers=get_headers(), json=payload, timeout=60)
    response.raise_for_status()

    result = response.json()
    return result["voice_id"]


def list_voices(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    获取音色列表

    Args:
        category: 音色类别过滤

    Returns:
        音色列表
    """
    url = f"{get_base_url()}/get_voice"

    # MiniMax API 使用此端点获取单个音色或列表
    # 这里使用 POST 但不传 voice_id 来获取列表
    payload = {}

    response = requests.post(url, headers=get_headers(), json=payload, timeout=30)
    response.raise_for_status()

    result = response.json()
    return result.get("voices", [])


def get_voice(voice_id: str) -> Dict[str, Any]:
    """
    获取单个音色信息

    Args:
        voice_id: 音色ID

    Returns:
        音色信息
    """
    url = f"{get_base_url()}/get_voice"

    payload = {"voice_id": voice_id}

    response = requests.post(url, headers=get_headers(), json=payload, timeout=30)
    response.raise_for_status()

    return response.json()


def delete_voice(voice_id: str) -> bool:
    """
    删除音色

    Args:
        voice_id: 音色ID

    Returns:
        是否删除成功
    """
    url = f"{get_base_url()}/delete_voice"

    payload = {"voice_id": voice_id}

    response = requests.post(url, headers=get_headers(), json=payload, timeout=30)
    response.raise_for_status()

    result = response.json()
    return result.get("success", False)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="MiniMax Speech API Client")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # TTS 命令
    tts_parser = subparsers.add_parser("tts", help="文本转语音")
    tts_parser.add_argument("text", help="要转换的文本")
    tts_parser.add_argument("-v", "--voice", default="female-tianmei", help="音色ID")
    tts_parser.add_argument("-o", "--output", required=True, help="输出文件路径")

    # 异步TTS命令
    async_parser = subparsers.add_parser("tts-async", help="异步文本转语音")
    async_parser.add_argument("text", help="要转换的文本")
    async_parser.add_argument("-v", "--voice", default="female-tianmei", help="音色ID")

    # 查询命令
    query_parser = subparsers.add_parser("query", help="查询任务状态")
    query_parser.add_argument("task_id", help="任务ID")

    # 克隆命令
    clone_parser = subparsers.add_parser("clone", help="音色克隆")
    clone_parser.add_argument("audio", help="音频文件路径")
    clone_parser.add_argument("-t", "--title", required=True, help="音色名称")

    # 设计命令
    design_parser = subparsers.add_parser("design", help="音色设计")
    design_parser.add_argument("text", help="音色描述文本")
    design_parser.add_argument("-s", "--style", default="custom", help="音色风格")

    # 删除音色命令
    delete_parser = subparsers.add_parser("delete", help="删除音色")
    delete_parser.add_argument("voice_id", help="音色ID")

    args = parser.parse_args()

    try:
        if args.command == "tts":
            result = text_to_speech(args.text, args.voice, args.output)
            print(f"Audio saved to: {result}")

        elif args.command == "tts-async":
            task_ids = text_to_speech_async(args.text, args.voice)
            print(f"Task IDs: {task_ids}")

        elif args.command == "query":
            result = query_speech_task(args.task_id)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "clone":
            voice_id = clone_voice(args.audio, args.title)
            print(f"Cloned voice ID: {voice_id}")

        elif args.command == "design":
            voice_id = design_voice(args.text, args.style)
            print(f"Designed voice ID: {voice_id}")

        elif args.command == "delete":
            success = delete_voice(args.voice_id)
            print(f"Delete {'successful' if success else 'failed'}")

        else:
            parser.print_help()

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code}")
        print(e.response.text)
        raise


if __name__ == "__main__":
    main()
