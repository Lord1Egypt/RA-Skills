#!/usr/bin/env python3
"""
腾讯云 TRTC TextToSpeech API 客户端
- 基于腾讯云 API 签名 v3 (TC3-HMAC-SHA256)
  https://cloud.tencent.com/document/product/213/30654
- base64 解码 → PCM int16 LE → float32 [-1.0, 1.0]
- 24000Hz → 44100Hz 重采样（线性插值）
"""
import base64
import hashlib
import hmac
import json
import sys
import time
import numpy as np
from datetime import datetime, timezone
from pathlib import Path

if sys.version_info[0] <= 2:
    from httplib import HTTPSConnection
else:
    from http.client import HTTPSConnection

try:
    from platform_utils import get_work_dir
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from platform_utils import get_work_dir

# ── 常量 ────────────────────────────────────────────────────
SERVICE = "trtc"
HOST = "trtc.tencentcloudapi.com"
ENDPOINT = f"https://{HOST}"
ACTION = "TextToSpeech"
VERSION = "2019-07-22"
REGION = "ap-guangzhou"      # 腾讯云 TRTC TTS 服务区域（必填）

# 音频参数
VOICE_ID = "v-female-U8aT2yLf"
SPEED = 1                    # 语速 [-2, 6]
VOLUME = 1                   # 音量 [-10, 10]
PITCH = 0                    # 音调
AUDIO_FORMAT = "pcm"         # 音频格式（pcm 直接用于推流，无需解码）
SAMPLE_RATE_API = 24000      # API 输出采样率（PCM 仅支持 16000/24000）
SAMPLE_RATE_STREAM = 44100   # 推流管线采样率
MODEL = "flow_01_turbo"
LANGUAGE = "zh"

# ── TC3-HMAC-SHA256 签名 ─────────────────────────────────────
# 严格基于腾讯云 API 签名 v3 文档实现:
# https://cloud.tencent.com/document/product/213/30654

def _sign(key: bytes, msg: str) -> bytes:
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


# ── TTS 请求 ──────────────────────────────────────────────────

def synthesize(text: str, secret_id: str, secret_key: str,
               sdkappid: int, session_id: str = "") -> np.ndarray | None:
    """
    调用腾讯云 TRTC TextToSpeech API，返回 float32 numpy 数组 (44100Hz mono)

    Args:
        text: 播报文案（≤300 字符）
        secret_id: 腾讯云 CAM SecretId
        secret_key: 腾讯云 CAM SecretKey
        sdkappid: TRTC SDKAppID
        session_id: 会话 ID（可选，用于追踪）

    Returns:
        np.ndarray (float32, mono, 44100Hz) 或 None（失败时）
    """
    # ── 构造请求体 ──
    payload = json.dumps({
        "Text": text,
        "Voice": {
            "VoiceId": VOICE_ID,
            "Speed": SPEED,
            "Volume": VOLUME,
            "Pitch": PITCH,
        },
        "SdkAppId": sdkappid,
        "AudioFormat": {
            "Format": AUDIO_FORMAT,
            "SampleRate": SAMPLE_RATE_API,
        },
        "Model": MODEL,
        "Language": LANGUAGE,
    })

    timestamp = int(time.time())
    date = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d")
    algorithm = "TC3-HMAC-SHA256"

    # ************* 步骤 1：拼接规范请求串 *************
    http_request_method = "POST"
    canonical_uri = "/"
    canonical_querystring = ""
    ct = "application/json; charset=utf-8"
    canonical_headers = "content-type:%s\nhost:%s\nx-tc-action:%s\n" % (ct, HOST, ACTION.lower())
    signed_headers = "content-type;host;x-tc-action"
    hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    canonical_request = (http_request_method + "\n" +
                         canonical_uri + "\n" +
                         canonical_querystring + "\n" +
                         canonical_headers + "\n" +
                         signed_headers + "\n" +
                         hashed_request_payload)

    # ************* 步骤 2：拼接待签名字符串 *************
    credential_scope = date + "/" + SERVICE + "/" + "tc3_request"
    hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    string_to_sign = (algorithm + "\n" +
                      str(timestamp) + "\n" +
                      credential_scope + "\n" +
                      hashed_canonical_request)

    # ************* 步骤 3：计算签名 *************
    secret_date = _sign(("TC3" + secret_key).encode("utf-8"), date)
    secret_service = _sign(secret_date, SERVICE)
    secret_signing = _sign(secret_service, "tc3_request")
    signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"),
                         hashlib.sha256).hexdigest()

    # ************* 步骤 4：拼接 Authorization *************
    authorization = (algorithm + " " +
                     "Credential=" + secret_id + "/" + credential_scope + ", " +
                     "SignedHeaders=" + signed_headers + ", " +
                     "Signature=" + signature)

    # ************* 步骤 5：构造并发起请求 *************
    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json; charset=utf-8",
        "Host": HOST,
        "X-TC-Action": ACTION,
        "X-TC-Timestamp": str(timestamp),
        "X-TC-Version": VERSION,
    }
    if REGION:
        headers["X-TC-Region"] = REGION

    try:
        req = HTTPSConnection(HOST)
        req.request("POST", "/", headers=headers, body=payload.encode("utf-8"))
        resp = req.getresponse()
        result = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"[TTS] API request failed: {e}")
        return None

    response = result.get("Response", {})
    if "Error" in response:
        err = response["Error"]
        print(f"[TTS] API error: {err.get('Code')} - {err.get('Message')}")
        return None

    audio_b64 = response.get("Audio")
    if not audio_b64:
        print("[TTS] No audio data in response")
        return None

    # ── 解码 base64 → PCM int16 → float32 ──
    pcm_bytes = base64.b64decode(audio_b64)
    pcm_int16 = np.frombuffer(pcm_bytes, dtype=np.int16)
    pcm_float = pcm_int16.astype(np.float32) / 32768.0

    # ── 重采样 24000Hz → 44100Hz（线性插值）──
    resampled = _resample(pcm_float, SAMPLE_RATE_API, SAMPLE_RATE_STREAM)

    return resampled


def _resample(audio: np.ndarray, src_rate: int, dst_rate: int) -> np.ndarray:
    """线性插值重采样"""
    if src_rate == dst_rate:
        return audio
    duration = len(audio) / src_rate
    dst_len = int(duration * dst_rate)
    x_src = np.linspace(0, duration, num=len(audio), endpoint=False)
    x_dst = np.linspace(0, duration, num=dst_len, endpoint=False)
    return np.interp(x_dst, x_src, audio).astype(np.float32)


# ── 从 config.json 加载密钥 ──────────────────────────────────

def load_tts_config() -> dict | None:
    """从工作目录 config.json 加载 TTS 配置（优先 cam_ 字段，兼容旧 tts_ 字段）"""
    config_path = get_work_dir() / "config.json"
    if not config_path.exists():
        return None
    try:
        cfg = json.loads(config_path.read_text(encoding="utf-8"))
        secret_id = cfg.get("cam_secret_id") or cfg.get("tts_secret_id", "")
        secret_key = cfg.get("cam_secret_key") or cfg.get("tts_secret_key", "")
        sdkappid = cfg.get("sdkappid", 0)
        if not secret_id or not secret_key or not sdkappid:
            return None
        return {
            "secret_id": secret_id,
            "secret_key": secret_key,
            "sdkappid": sdkappid,
        }
    except Exception:
        return None


# ── CLI 测试 ──────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: tts_client.py <text> [output.npy]")
        print("  Requires config.json with tts_secret_id (CAM SecretId) and tts_secret_key (CAM SecretKey)")
        sys.exit(1)

    text = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "tts_output.npy"

    cfg = load_tts_config()
    if not cfg:
        print("[ERROR] TTS config not found. Set tts_secret_id/tts_secret_key in config.json")
        sys.exit(1)

    print(f"[TTS] Synthesizing: {text}")
    audio = synthesize(text, cfg["secret_id"], cfg["secret_key"], cfg["sdkappid"])
    if audio is not None:
        np.save(output_file, audio)
        duration = len(audio) / SAMPLE_RATE_STREAM
        print(f"[TTS] OK: {len(audio)} samples ({duration:.2f}s) → {output_file}")
    else:
        print("[TTS] Failed")
        sys.exit(1)
