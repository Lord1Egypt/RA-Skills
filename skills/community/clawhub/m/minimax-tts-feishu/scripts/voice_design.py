#!/usr/bin/env python3
import os
"""
MiniMax TTS - 音色设计模块
"""

import requests
from tts import tts_and_send, generate_speech, upload_to_feishu

API_KEY = os.environ.get("MINIMAX_API_KEY", "")
VOICE_DESIGN_URL = "https://api.minimaxi.com/v1/voice_design"


def design_voice(prompt: str, preview_text: str = "测试") -> dict:
    """
    使用 MiniMax voice_design API 设计新音色
    
    Args:
        prompt: 音色描述，如"温柔的女性声音，语速适中"
        preview_text: 试听文本
    
    Returns:
        dict，包含 voice_id 和 preview_audio_bytes
    """
    payload = {
        "prompt": prompt,
        "preview_text": preview_text
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    response = requests.post(VOICE_DESIGN_URL, json=payload, headers=headers, timeout=60)
    data = response.json()
    
    if data.get("base_resp", {}).get("status_code") != 0:
        raise Exception(f"Voice design failed: {data}")
    
    result = {
        "voice_id": data.get("voice_id"),
        "preview_audio": bytes.fromhex(data["trial_audio"]) if "trial_audio" in data and data["trial_audio"] else None
    }
    
    return result


def design_and_send(prompt: str, preview_text: str, text: str) -> dict:
    """
    设计音色 + 生成语音并发送
    
    Args:
        prompt: 音色描述
        preview_text: 试听文本
        text: 要说的内容
    
    Returns:
        dict，包含 voice_id 和发送结果
    """
    # 1. 设计音色
    voice_info = design_voice(prompt, preview_text)
    voice_id = voice_info["voice_id"]
    
    # 2. 用新音色生成语音
    output_path = "/tmp/tts_output.wav"
    generate_speech(text, voice_id=voice_id, output_path=output_path)
    
    # 3. 上传并发送
    file_key = upload_to_feishu(output_path)
    result = send_audio_message(file_key)
    
    return {"voice_id": voice_id, "result": result}


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("用法: python3 voice_design.py <音色描述> <试听文本> <要说的内容>")
        sys.exit(1)
    
    prompt = sys.argv[1]
    preview = sys.argv[2]
    text = sys.argv[3]
    
    print(f"设计音色: {prompt}")
    print(f"试听文本: {preview}")
    print(f"生成内容: {text}")
    result = design_and_send(prompt, preview, text)
    print(f"发送结果: {result}")
