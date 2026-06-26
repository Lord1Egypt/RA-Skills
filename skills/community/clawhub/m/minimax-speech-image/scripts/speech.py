#!/usr/bin/env python3
"""MiniMax Speech API Client"""
import os, json, base64, argparse
from typing import Optional, Dict, Any, List
import requests

BASE_URL_CN = "https://api.minimaxi.com/v1"
BASE_URL_INT = "https://api.minimax.io/v1"

def get_base_url() -> str:
    return BASE_URL_CN if os.getenv("MINIMAX_REGION", "cn") == "cn" else BASE_URL_INT

def get_headers() -> Dict[str, str]:
    api_key = os.getenv("MINIMAX_API_KEY")
    if not api_key:
        raise ValueError("MINIMAX_API_KEY environment variable is not set")
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

def text_to_speech(text: str, voice_id: str = "female-tianmei",
                   output_file: Optional[str] = None,
                   model: str = "speech-2.8-hd",
                   format: str = "mp3", sample_rate: int = 32000,
                   bitrate: int = 128000) -> str:
    url = f"{get_base_url()}/t2a_v2"
    payload = {"model": model, "text": text, "stream": False,
               "voice_setting": {"voice_id": voice_id},
               "audio_setting": {"sample_rate": sample_rate, "bitrate": bitrate, "format": format}}
    resp = requests.post(url, headers=get_headers(), json=payload, timeout=60)
    resp.raise_for_status()
    result = resp.json()
    audio_b64 = result.get("audio_file") or result.get("data", {}).get("audio")
    if not audio_b64:
        raise ValueError(f"Unexpected API response: {result}")
    if output_file:
        with open(output_file, "wb") as f:
            f.write(base64.b64decode(audio_b64))
        return output_file
    return audio_b64

def text_to_speech_async(text: str, voice_id: str = "female-tianmei",
                         model: str = "speech-2.8-hd",
                         format: str = "mp3", sample_rate: int = 32000,
                         bitrate: int = 128000) -> List[str]:
    url = f"{get_base_url()}/t2a_async_v2"
    payload = {"model": model, "text": text,
               "voice_setting": {"voice_id": voice_id},
               "audio_setting": {"sample_rate": sample_rate, "bitrate": bitrate, "format": format}}
    resp = requests.post(url, headers=get_headers(), json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json().get("task_ids", [])

def query_speech_task(task_id: str) -> Dict[str, Any]:
    url = f"{get_base_url()}/query/t2a_async_query_v2"
    resp = requests.get(url, headers=get_headers(), params={"task_id": task_id}, timeout=30)
    resp.raise_for_status()
    return resp.json()

def clone_voice(audio_file_path: str, title: str, model: str = "speech-2.0-turbo") -> str:
    """音色克隆：先上传音频文件，再调用克隆接口。"""
    # Step 1: 上传音频文件到 /v1/files
    upload_url = f"{get_base_url()}/files/upload"
    headers_upload = {"Authorization": f"Bearer {os.getenv('MINIMAX_API_KEY')}"}
    with open(audio_file_path, "rb") as f:
        files = {"file": (os.path.basename(audio_file_path), f, "audio/mpeg")}
        data = {"purpose": "audio"}
        resp = requests.post(upload_url, headers=headers_upload, files=files, data=data, timeout=120)
    resp.raise_for_status()
    resp_data = resp.json()
    file_id = resp_data.get("file", {}).get("file_id")
    if not file_id:
        raise ValueError(f"File upload failed, no file_id returned: {resp_data}")
    # Step 2: 调用音色克隆接口，voice_id 填上传后的 file_id
    clone_url = f"{get_base_url()}/voice_clone"
    payload = {"model": model, "voice_id": file_id, "title": title}
    resp2 = requests.post(clone_url, headers=get_headers(), json=payload, timeout=120)
    resp2.raise_for_status()
    return resp2.json().get("voice_id") or resp2.json().get("data", {}).get("voice_id")

def design_voice(text: str, style: str = "custom", model: str = "speech-01") -> str:
    url = f"{get_base_url()}/voice_design"
    payload = {"model": model, "text": text, "voice_setting": {"style": style}}
    resp = requests.post(url, headers=get_headers(), json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()["voice_id"]

def list_voices(category: Optional[str] = None) -> List[Dict[str, Any]]:
    url = f"{get_base_url()}/get_voice"
    payload = {} if category is None else {"category": category}
    resp = requests.post(url, headers=get_headers(), json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json().get("voices", [])

def get_voice(voice_id: str) -> Dict[str, Any]:
    url = f"{get_base_url()}/get_voice"
    resp = requests.post(url, headers=get_headers(), json={"voice_id": voice_id}, timeout=30)
    resp.raise_for_status()
    return resp.json()

def delete_voice(voice_id: str) -> bool:
    url = f"{get_base_url()}/delete_voice"
    resp = requests.post(url, headers=get_headers(), json={"voice_id": voice_id}, timeout=30)
    resp.raise_for_status()
    return resp.json().get("success", False)

def main():
    parser = argparse.ArgumentParser(description="MiniMax Speech API Client")
    sub = parser.add_subparsers(dest="command", help="Available commands")
    p = sub.add_parser("tts", help="同步文本转语音")
    p.add_argument("text", help="要转换的文本")
    p.add_argument("-v", "--voice", default="female-tianmei", help="音色ID")
    p.add_argument("-o", "--output", required=True, help="输出文件路径")
    p = sub.add_parser("tts-async", help="异步文本转语音")
    p.add_argument("text", help="要转换的文本")
    p.add_argument("-v", "--voice", default="female-tianmei", help="音色ID")
    p = sub.add_parser("query", help="查询任务状态")
    p.add_argument("task_id", help="任务ID")
    p = sub.add_parser("clone", help="音色克隆")
    p.add_argument("audio", help="参考音频文件路径")
    p.add_argument("-t", "--title", required=True, help="新音色名称")
    p = sub.add_parser("design", help="音色设计")
    p.add_argument("text", help="音色描述文本")
    p.add_argument("-s", "--style", default="custom", help="音色风格")
    p = sub.add_parser("delete", help="删除音色")
    p.add_argument("voice_id", help="音色ID")
    args = parser.parse_args()
    try:
        if args.command == "tts":
            path = text_to_speech(args.text, args.voice, args.output)
            print(f"Audio saved to: {path}")
        elif args.command == "tts-async":
            task_ids = text_to_speech_async(args.text, args.voice)
            print(f"Task IDs: {task_ids}")
        elif args.command == "query":
            print(json.dumps(query_speech_task(args.task_id), indent=2, ensure_ascii=False))
        elif args.command == "clone":
            print(f"Cloned voice ID: {clone_voice(args.audio, args.title)}")
        elif args.command == "design":
            print(f"Designed voice ID: {design_voice(args.text, args.style)}")
        elif args.command == "delete":
            ok = delete_voice(args.voice_id)
            print(f"Delete {'successful' if ok else 'failed'}")
        else:
            parser.print_help()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code}")
        print(e.response.text)
        raise

if __name__ == "__main__":
    main()
