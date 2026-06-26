#!/usr/bin/env python3
"""
MiniMax TTS - 文字转语音模块
"""

import os
import requests
import json
import text_preprocessor

API_KEY = os.environ.get("MINIMAX_API_KEY", "")
FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")
TTS_URL = "https://api.minimaxi.com/v1/t2a_v2"


def generate_speech(
    text: str,
    voice_id: str = "Chinese (Mandarin)_Gentle_Senior",
    speed: float = 1.0,
    vol: float = 1.0,
    pitch: float = 0,
    emotion: str = None,
    output_path: str = "/tmp/tts_output.wav"
) -> str:
    """
    使用 MiniMax TTS API 将文字转语音
    
    Args:
        text: 要转换的文本
        voice_id: 音色ID
        speed: 语速，默认 1.0
        vol: 音量，默认 1.0
        pitch: 音调，默认 0
        emotion: 情绪，happy/sad/angry 等，默认 None 表示自动检测
        output_path: 输出文件路径
    
    Returns:
        输出文件路径
    """
    # 文本预处理：自动检测情绪 + 添加停顿标记
    processed = text_preprocessor.preprocess_for_tts(text)
    detected_emotion = emotion if emotion is not None else processed["emotion"]
    processed_text = processed["text"]

    payload = {
        "model": "speech-2.8-hd",
        "text": processed_text,
        "stream": False,
        "voice_setting": {
            "voice_id": voice_id,
            "speed": speed,
            "vol": vol,
            "pitch": pitch,
            "emotion": detected_emotion
        },
        "audio_setting": {
            "sample_rate": 16000,
            "format": "wav",
            "channel": 1
        },
        "subtitle_enable": False
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    response = requests.post(TTS_URL, json=payload, headers=headers, timeout=30)
    
    if response.status_code != 200:
        raise Exception(f"TTS API error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    if "data" not in data or "audio" not in data.get("data", {}):
        raise Exception(f"Unexpected response: {data}")
    
    audio_hex = data["data"]["audio"]
    audio_bytes = bytes.fromhex(audio_hex)
    
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    
    return output_path


def _get_feishu_token() -> str:
    """获取飞书 access token"""
    req = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET},
        timeout=10
    )
    return req.json()["tenant_access_token"]


def upload_to_feishu(file_path: str) -> str:
    """上传音频到飞书，返回 file_key"""
    token = _get_feishu_token()
    
    with open(file_path, "rb") as f:
        upload_req = requests.post(
            "https://open.feishu.cn/open-apis/im/v1/files",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": f},
            data={
                "file_name": os.path.basename(file_path),
                "file_extension": "wav",
                "file_type": "opus"
            },
            timeout=15
        )
    
    result = upload_req.json()
    if result.get("code") != 0:
        raise Exception(f"Feishu upload failed: {result}")
    
    return result["data"]["file_key"]


def send_audio_message(file_key: str, user_open_id: str = None) -> dict:
    """发送音频消息到飞书
    
    Args:
        file_key: 音频文件 key
        user_open_id: 接收者 open_id，默认从 FEISHU_USER_OPEN_ID 环境变量读取
    """
    if user_open_id is None:
        user_open_id = os.environ.get("FEISHU_USER_OPEN_ID", "")
    
    token = _get_feishu_token()
    
    msg_req = requests.post(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={
            "receive_id": user_open_id,
            "msg_type": "audio",
            "content": json.dumps({"file_key": file_key})
        },
        timeout=15
    )
    
    return msg_req.json()


def tts_and_send(text: str, voice_id: str = "Chinese (Mandarin)_Gentle_Senior", user_open_id: str = None) -> dict:
    """生成 TTS 并发送"""
    output_path = "/tmp/tts_output.wav"
    generate_speech(text, voice_id=voice_id, output_path=output_path)
    file_key = upload_to_feishu(output_path)
    result = send_audio_message(file_key, user_open_id)
    return result


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python3 tts.py <文本> [voice_id]")
        sys.exit(1)
    
    text = sys.argv[1]
    voice = sys.argv[2] if len(sys.argv) > 2 else "Chinese (Mandarin)_Gentle_Senior"
    user_open_id = sys.argv[3] if len(sys.argv) > 3 else None
    
    print(f"生成语音: {text}")
    print(f"音色: {voice}")
    if user_open_id:
        print(f"发送给: {user_open_id}")
    result = tts_and_send(text, voice, user_open_id)
    print(f"发送结果: {result}")
