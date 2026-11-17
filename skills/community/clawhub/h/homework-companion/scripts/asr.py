#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音口述转写 —— 腾讯云 ASR SentenceRecognition (一句话识别, 单次 <= 60s)。

用法:
  python asr.py --audio <音频路径> [--source 16k|8k]

输出: 转写文本, 写到 stdout。
支持的音频格式: wav / mp3 / pcm / speex / silk / m4a
"""
import os
import sys
import base64
import argparse


ENGINE_TYPE_MAP = {
    "16k": "16k_zh",
    "8k": "8k_zh",
}
SUPPORTED_FMT = {"wav", "mp3", "pcm", "speex", "silk", "m4a"}


def _load_cred():
    sid = os.environ.get("TENCENTCLOUD_SECRET_ID")
    skey = os.environ.get("TENCENTCLOUD_SECRET_KEY")
    if not sid or not skey:
        sys.stderr.write(
            "请先设置环境变量 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY\n"
        )
        sys.exit(3)
    return sid, skey


def transcribe(audio_path, source="16k"):
    try:
        from tencentcloud.common import credential
        from tencentcloud.common.profile.client_profile import ClientProfile
        from tencentcloud.common.profile.http_profile import HttpProfile
        from tencentcloud.asr.v20190614 import asr_client, models
    except ImportError:
        sys.stderr.write(
            "缺少依赖 tencentcloud-sdk-python，请先执行: "
            "pip install -r requirements.txt\n"
        )
        sys.exit(2)

    sid, skey = _load_cred()
    cred = credential.Credential(sid, skey)
    http_profile = HttpProfile()
    http_profile.endpoint = "asr.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    client = asr_client.AsrClient(cred, "ap-guangzhou", client_profile)

    with open(audio_path, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode("utf-8")

    ext = os.path.splitext(audio_path)[1].lower().lstrip(".")
    voice_format = ext if ext in SUPPORTED_FMT else "mp3"

    req = models.SentenceRecognitionRequest()
    req.EngineModelType = ENGINE_TYPE_MAP.get(source, "16k_zh")
    req.ChannelNum = 1
    req.VoiceFormat = voice_format
    req.Data = audio_b64
    req.DataLen = os.path.getsize(audio_path)

    resp = client.SentenceRecognition(req)
    return resp.Result


def main():
    parser = argparse.ArgumentParser(description="语音口述转写")
    parser.add_argument("--audio", required=True, help="音频文件路径")
    parser.add_argument(
        "--source", choices=["16k", "8k"], default="16k", help="采样率 (默认 16k)"
    )
    args = parser.parse_args()
    sys.stdout.write(transcribe(args.audio, args.source) + "\n")


if __name__ == "__main__":
    main()
