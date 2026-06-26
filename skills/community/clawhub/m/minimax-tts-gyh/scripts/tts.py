#!/usr/bin/env python3
"""
MiniMax TTS 文字转语音脚本
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


def tts_speech(model: str, text: str, voice_id: str = "female_tianmei",
               speed: float = 1.0, pitch: float = 0, volume: float = 1.0,
               emotion: str = "neutral", language: str = "auto",
               output_path: str = "output.mp3") -> str:
    """
    调用 MiniMax TTS API 生成语音
    返回本地文件路径
    """
    url = f"{API_HOST}/v1/t2a_v2"

    payload = {
        "model": model,
        "text": text,
        "voice_setting": {
            "voice_id": voice_id,
            "speed": speed,
            "pitch": pitch,
            "vol": volume,
            "emotion": emotion,
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1,
        },
        "language": language,
    }

    print(f"🎙️ 正在生成语音...")
    print(f"   模型: {model} | 声音: {voice_id} | 语速: {speed}x")
    print(f"   文本: {text[:50]}{'...' if len(text) > 50 else ''}")

    resp = requests.post(url, headers=HEADERS, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    base_resp = data.get("base_resp", {})
    if base_resp.get("status_code") != 0:
        # 可能是异步任务
        task_id = data.get("task_id")
        if task_id:
            print(f"⏳ 异步任务 ID: {task_id}，开始轮询...")
            file_id = poll_tts_task(task_id)
            if file_id:
                download_file(file_id, output_path)
                return output_path
        raise Exception(f"API Error: {base_resp.get('status_msg', 'unknown')}")

    # 同步返回，直接是音频数据
    audio_data = data.get("data")
    if audio_data:
        with open(output_path, "wb") as f:
            f.write(audio_data.encode('latin1'))
        print(f"✅ 语音已保存: {output_path}")
        return output_path

    raise Exception("未获取到音频数据")


def poll_tts_task(task_id: str, max_wait: int = 300) -> str:
    """轮询 TTS 任务状态"""
    url = f"{API_HOST}/v1/query/t2a_async_query_v2"
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
            raise Exception(f"TTS 任务失败: {data.get('error_message', 'unknown')}")
    raise Exception("TTS 任务超时")


def download_file(file_id: str, output_path: str):
    """下载音频文件"""
    url = f"{API_HOST}/v1/files/retrieve"
    params = {"file_id": file_id}
    resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
    resp.raise_for_status()
    download_url = resp.json()["file"]["download_url"]

    with open(output_path, "wb") as f:
        vr = requests.get(download_url, timeout=60)
        vr.raise_for_status()
        f.write(vr.content)
    print(f"✅ 文件已下载: {output_path}")


def list_voices(model: str = "speech-02-hd"):
    """列出可用声音"""
    url = f"{API_HOST}/v1/voices"
    params = {"model": model}
    resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
    print(resp.text)


def main():
    parser = argparse.ArgumentParser(description="MiniMax TTS 文字转语音")
    parser.add_argument("--model", default="speech-02-hd",
                        help="模型: speech-02-hd, speech-02-turbo, speech-01-hd, speech-01-turbo")
    parser.add_argument("--text", required=True, help="要转换的文本")
    parser.add_argument("--voice_id", default="female_tianmei",
                        help="声音 ID: female_tianmei, male_tianmei, female_healthy, male_healthy 等")
    parser.add_argument("--speed", type=float, default=1.0, help="语速 (0.5-2.0)")
    parser.add_argument("--pitch", type=float, default=0, help="音调调整")
    parser.add_argument("--volume", type=float, default=1.0, help="音量 (0.5-2.0)")
    parser.add_argument("--emotion", default="neutral",
                        help="情感: neutral, happy, sad, angry, fearful, disgusted")
    parser.add_argument("--language", default="auto", help="语言: auto, zh, en, ja, ko 等")
    parser.add_argument("--output", default="output.mp3", help="输出文件路径")

    args = parser.parse_args()

    try:
        result = tts_speech(
            model=args.model,
            text=args.text,
            voice_id=args.voice_id,
            speed=args.speed,
            pitch=args.pitch,
            volume=args.volume,
            emotion=args.emotion,
            language=args.language,
            output_path=args.output,
        )
        print(f"\n📎 输出文件: {result}")
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
