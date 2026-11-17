#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本转儿童友好语音 —— 腾讯云 TTS TextToVoice。

用法:
  python tts.py --text "讲解内容" --output out.mp3 [--voice-type 0|1|...]

输出: 生成音频文件, 文件路径写到 stdout。
说明: 默认使用标准女声 (VoiceType=0)。如需更"儿童友好"的音色，可在腾讯云
      控制台查看可用 SpeakerId，并取消下行注释后填入。
"""
import os
import sys
import base64
import argparse


def _load_cred():
    sid = os.environ.get("TENCENTCLOUD_SECRET_ID")
    skey = os.environ.get("TENCENTCLOUD_SECRET_KEY")
    if not sid or not skey:
        sys.stderr.write(
            "请先设置环境变量 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY\n"
        )
        sys.exit(3)
    return sid, skey


def synthesize(text, output, voice_type=0, speaker_id=None):
    try:
        from tencentcloud.common import credential
        from tencentcloud.common.profile.client_profile import ClientProfile
        from tencentcloud.common.profile.http_profile import HttpProfile
        from tencentcloud.tts.v20190823 import tts_client, models
    except ImportError:
        sys.stderr.write(
            "缺少依赖 tencentcloud-sdk-python，请先执行: "
            "pip install -r requirements.txt\n"
        )
        sys.exit(2)

    sid, skey = _load_cred()
    cred = credential.Credential(sid, skey)
    http_profile = HttpProfile()
    http_profile.endpoint = "tts.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    client = tts_client.TtsClient(cred, "ap-guangzhou", client_profile)

    req = models.TextToVoiceRequest()
    req.Text = text
    req.SessionId = "homework-companion-" + str(abs(hash(text)) % 10**8)
    req.VoiceType = voice_type
    req.Codec = "mp3"
    req.SampleRate = 16000
    # 如需指定具体音色（如儿童友好音色），取消下一行注释并填入控制台提供的 SpeakerId：
    # req.SpeakerId = 101005

    resp = client.TextToVoice(req)
    audio = base64.b64decode(resp.Audio)
    with open(output, "wb") as f:
        f.write(audio)
    return output


def main():
    parser = argparse.ArgumentParser(description="文本转语音")
    parser.add_argument("--text", required=True, help="要合成的讲解文本")
    parser.add_argument("--output", required=True, help="输出音频路径 (.mp3)")
    parser.add_argument(
        "--voice-type", type=int, default=0, help="音色类型 (默认 0=标准女声)"
    )
    args = parser.parse_args()
    path = synthesize(args.text, args.output, args.voice_type)
    sys.stdout.write(path + "\n")


if __name__ == "__main__":
    main()
