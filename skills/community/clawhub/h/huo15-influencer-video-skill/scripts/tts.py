"""配音模块

两套引擎，按优先级降级：
  1) edge-tts（免费、无 key、Microsoft Azure 神经音色）— 默认
  2) 火山引擎 TTS（付费，音质更好）— 设置 VOLC_TTS_APP_ID / VOLC_TTS_TOKEN / VOLC_TTS_CLUSTER 启用

返回值统一约定：
    {"path": "voice.mp3", "duration": 8.42, "engine": "edge-tts"}
"""

import os
import json
import uuid
import asyncio
import subprocess
from typing import Optional


def _probe_duration(audio_path: str) -> float:
    """用 ffprobe 测时长（秒）"""
    out = subprocess.check_output([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path,
    ], text=True).strip()
    return float(out)


# ============== 1. edge-tts ==============

async def _edge_tts_async(text: str, voice: str, rate: str, pitch: str, output: str):
    import edge_tts  # pip install edge-tts
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(output)


def tts_edge(text: str,
             voice: str = "zh-CN-XiaoqiuNeural",
             rate: str = "+0%",
             pitch: str = "+0Hz",
             output: Optional[str] = None) -> dict:
    """用 edge-tts 合成，返回 {path, duration, engine}"""
    output = output or f"/tmp/voice_{uuid.uuid4().hex[:8]}.mp3"
    asyncio.run(_edge_tts_async(text, voice, rate, pitch, output))
    return {
        "path": output,
        "duration": _probe_duration(output),
        "engine": "edge-tts",
        "voice": voice,
    }


# ============== 2. 火山 TTS ==============

VOLC_HOST = "https://openspeech.bytedance.com"
VOLC_VOICE_MAP = {
    # edge-tts 音色 → 火山 voice_type 的近似映射，调用方传 edge 风格 key 即可
    "zh-CN-XiaoxiaoNeural": "BV007_streaming",      # 通用女声
    "zh-CN-XiaoqiuNeural":  "BV701_streaming",      # 沉稳女声
    "zh-CN-XiaohanNeural":  "BV064_streaming",      # 温暖女声
    "zh-CN-XiaomengNeural": "BV005_streaming",      # 活泼女声
    "zh-CN-YunjianNeural":  "BV002_streaming",      # 中年男声
    "zh-CN-YunhaoNeural":   "BV120_streaming",      # 激情男声
    "zh-CN-YunxiaNeural":   "BV056_streaming",      # 少年男声
    "zh-CN-YunyangNeural":  "BV034_streaming",      # 专业男声
}


def tts_volc(text: str,
             voice: str = "zh-CN-XiaoqiuNeural",
             output: Optional[str] = None,
             speed_ratio: float = 1.0) -> dict:
    """火山 TTS（需环境变量 VOLC_TTS_APP_ID / VOLC_TTS_TOKEN / VOLC_TTS_CLUSTER）"""
    import requests, base64
    app_id = os.environ["VOLC_TTS_APP_ID"]
    token = os.environ["VOLC_TTS_TOKEN"]
    cluster = os.environ.get("VOLC_TTS_CLUSTER", "volcano_tts")
    voice_type = VOLC_VOICE_MAP.get(voice, "BV701_streaming")

    output = output or f"/tmp/voice_{uuid.uuid4().hex[:8]}.mp3"
    body = {
        "app": {"appid": app_id, "token": "access_token", "cluster": cluster},
        "user": {"uid": "huo15"},
        "audio": {
            "voice_type": voice_type,
            "encoding": "mp3",
            "speed_ratio": speed_ratio,
            "rate": 24000,
        },
        "request": {
            "reqid": uuid.uuid4().hex,
            "text": text,
            "operation": "query",
        },
    }
    r = requests.post(
        f"{VOLC_HOST}/api/v1/tts",
        headers={"Authorization": f"Bearer;{token}"},
        json=body, timeout=60,
    )
    data = r.json()
    if "data" not in data:
        raise RuntimeError(f"火山 TTS 失败: {data}")
    with open(output, "wb") as f:
        f.write(base64.b64decode(data["data"]))
    return {
        "path": output,
        "duration": _probe_duration(output),
        "engine": "volc-tts",
        "voice": voice_type,
    }


# ============== 统一入口 ==============

def synthesize(text: str,
               voice: str = "zh-CN-XiaoqiuNeural",
               rate: str = "+0%",
               pitch: str = "+0Hz",
               output: Optional[str] = None,
               engine: str = "auto") -> dict:
    """合成语音，自动选引擎。

    engine: 'auto' | 'edge' | 'volc'
        - auto: 有火山凭证用火山，否则 edge
    """
    if engine == "auto":
        engine = "volc" if os.environ.get("VOLC_TTS_APP_ID") else "edge"

    if engine == "volc":
        return tts_volc(text, voice=voice, output=output)
    return tts_edge(text, voice=voice, rate=rate, pitch=pitch, output=output)


def list_voices() -> list:
    """列出推荐音色"""
    return [
        {"id": "zh-CN-XiaoqiuNeural",  "label": "晓秋（中年女・沉稳）"},
        {"id": "zh-CN-XiaohanNeural",  "label": "晓涵（中年女・温暖）"},
        {"id": "zh-CN-XiaoxiaoNeural", "label": "晓晓（年轻女・通用）"},
        {"id": "zh-CN-XiaomengNeural", "label": "晓梦（年轻女・活泼）"},
        {"id": "zh-CN-YunjianNeural",  "label": "云健（中年男・沉稳）"},
        {"id": "zh-CN-YunhaoNeural",   "label": "云皓（年轻男・激情）"},
        {"id": "zh-CN-YunxiaNeural",   "label": "云夏（少年男・轻快）"},
        {"id": "zh-CN-YunyangNeural",  "label": "云扬（中年男・专业）"},
    ]


if __name__ == "__main__":
    import sys
    text = sys.argv[1] if len(sys.argv) > 1 else "姐妹们看，这款产品真的太好用了！"
    out = synthesize(text)
    print(json.dumps(out, ensure_ascii=False, indent=2))
