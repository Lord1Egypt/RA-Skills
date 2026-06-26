"""
MiMo-V2.5-ASR 语音识别（Gradio API 版）/ Speech Recognition (中文/English)

通过小米官方的 Gradio API 调用 ASR 服务，无需本地模型、无需 API Key。
Call Xiaomi's official ASR service via Gradio API — no local model, no API key needed.

用法 / Usage:
  python scripts/mimo_asr_api.py audio.wav                    # 自动检测 / auto
  python scripts/mimo_asr_api.py audio.wav --language zh       # 中文 / Chinese
  python scripts/mimo_asr_api.py audio.wav --language en       # 英文 / English
  python scripts/mimo_asr_api.py audio.wav --output result.txt # 输出到文件 / to file
"""

import argparse
import sys
import os
import json
import requests

# Windows GBK 兼容
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

API_BASE = "https://xiaomimimo-mimo-v2-5-asr.hf.space"


def upload_audio(filepath):
    """上传音频文件到 Gradio 服务器"""
    with open(filepath, 'rb') as f:
        r = requests.post(f"{API_BASE}/gradio_api/upload", files={'files': f}, timeout=120, verify=False)
    r.raise_for_status()
    data = r.json()
    if isinstance(data, list) and len(data) > 0:
        return data[0]
    return data


def call_transcribe(audio_data_url, language_tag):
    """调用 transcribe API，返回 event_id"""
    payload = {"data": [audio_data_url, None, language_tag]}
    r = requests.post(f"{API_BASE}/gradio_api/call/transcribe", json=payload, timeout=30, verify=False)
    r.raise_for_status()
    data = r.json()
    return data.get('event_id')


def poll_result(event_id):
    """轮询 SSE 端点获取转录结果"""
    url = f"{API_BASE}/gradio_api/call/transcribe/{event_id}"
    # 用 stream 模式读 SSE
    with requests.get(url, stream=True, timeout=180, verify=False) as r:
        for line in r.iter_lines(decode_unicode=True):
            if not line:
                continue
            if line.startswith("data: "):
                payload = line[6:].strip()
                if payload == "[DONE]":
                    break
                try:
                    data = json.loads(payload)
                    outputs = data.get('outputs', {})
                    if 'data' in outputs:
                        return outputs['data']
                except json.JSONDecodeError:
                    continue
    return None


def main():
    parser = argparse.ArgumentParser(
        description="MiMo-V2.5-ASR 语音识别 / Speech Recognition (Gradio API)"
    )
    parser.add_argument("audio", help="音频文件路径 / Audio file path")
    parser.add_argument("--language", choices=["auto", "zh", "en"], default="auto",
                        help="语言 / Language: auto=自动检测, zh=中文, en=英文")
    parser.add_argument("--output", help="输出文本文件路径 / Output text file")

    args = parser.parse_args()

    if not os.path.exists(args.audio):
        print(f"❌ 文件不存在 / File not found: {args.audio}", file=sys.stderr)
        sys.exit(1)

    lang_map = {"auto": "Auto", "zh": "Chinese", "en": "English"}

    print(f"📤 上传音频 / Uploading...", flush=True)
    try:
        audio_url = upload_audio(args.audio)
        print(f"   ✅ 上传成功", flush=True)
    except Exception as e:
        print(f"❌ 上传失败 / Upload failed: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"🎯 开始识别 / Transcribing (lang: {lang_map[args.language]})...", flush=True)
    try:
        event_id = call_transcribe(audio_url, lang_map[args.language])
        if not event_id:
            print("❌ 无法获取 event_id", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"❌ 启动失败: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        result = poll_result(event_id)
        if result and len(result) >= 2:
            transcript = result[0]
            status = result[1]
            if status:
                print(f"   📊 {status}", flush=True)
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(transcript)
                print(f"✅ 已保存到 / Saved to: {args.output}", flush=True)
            else:
                print(f"\n📝 {transcript}", flush=True)
        else:
            print("❌ 未获取到结果 / No result", file=sys.stderr)
    except Exception as e:
        print(f"❌ 获取结果失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
