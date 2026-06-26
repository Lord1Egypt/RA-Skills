#!/usr/bin/env python3
"""
AssemblyAI Large Audio Transcription Script
Uses only built-in libraries (urllib) - no pip install needed.
Supports files 100MB+ (up to 1GB / 12 hours)
Usage: python3 transcribe_assemblyai.py <file_path> [language: zh|en|auto]
"""
import sys
import os
import time
import json
import urllib.request
import urllib.error

API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
POLL_INTERVAL = 5
MAX_WAIT = 7200


def _headers():
    return {
        "authorization": API_KEY,
        "User-Agent": "jiadong-assemblyai-transcriber/1.0"
    }


def upload_file(file_path: str) -> str:
    """Upload local file to AssemblyAI, return upload_url."""
    print(f"[上传] {file_path}")
    file_size = os.path.getsize(file_path)
    print(f"[上传] 文件大小: {file_size/1024/1024:.1f} MB")
    with open(file_path, "rb") as f:
        data = f.read()
    req = urllib.request.Request(
        "https://api.assemblyai.com/v2/upload",
        data=data,
        headers=_headers(),
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=max(60, int(file_size / (256 * 1024)))) as resp:
        result = json.loads(resp.read())
    upload_url = result["upload_url"]
    print(f"[上传] 完成")
    return upload_url


def submit_transcription(upload_url: str, language: str = "auto") -> str:
    payload = {
        "audio_url": upload_url,
        "speaker_labels": True,
        "format_text": True,
        "language_detection": True if language == "auto" else False,
    }
    if language != "auto":
        payload["language_code"] = language

    print(f"[提交] 语言={language}, 启用说话人分离...")
    req = urllib.request.Request(
        "https://api.assemblyai.com/v2/transcript",
        data=json.dumps(payload).encode(),
        headers={**_headers(), "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())
    tid = result["id"]
    print(f"[提交] 任务ID: {tid}")
    return tid


def poll_result(transcript_id: str) -> dict:
    url = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    start = time.time()
    while True:
        elapsed = time.time() - start
        req = urllib.request.Request(url, headers=_headers())
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        status = data.get("status")
        print(f"[{elapsed:.0f}s] 状态: {status}")
        if status == "completed":
            duration = data.get("audio_duration", 0)
            print(f"[完成] 时长: {duration:.0f}s ({duration/60:.1f}min)")
            return data
        elif status == "error":
            raise RuntimeError(f"转录失败: {data.get('error')}")
        elif elapsed > MAX_WAIT:
            raise TimeoutError(f"超时（>{MAX_WAIT}s）")
        time.sleep(POLL_INTERVAL)


def format_transcript(result: dict) -> str:
    lang = result.get("language_code", "?")
    duration = result.get("audio_duration", 0)
    lines = []
    lines.append(f"[语言: {lang}] [时长: {duration:.0f}s / {duration/60:.1f}min]")
    lines.append("")

    utterances = result.get("utterances", [])
    if utterances:
        for utt in utterances:
            speaker = utt.get("speaker", "?")
            start_ms = utt.get("start", 0)
            text = utt.get("text", "").strip()
            start_s = start_ms / 1000
            lines.append(f"[{speaker}] {start_s:.1f}s: {text}")
    else:
        lines.append(result.get("text", ""))
    return "\n".join(lines)


def main():
    if not API_KEY:
        print("错误: 请设置 ASSEMBLYAI_API_KEY 环境变量", file=sys.stderr)
        print("或告诉许霸天你的 API Key 进行配置", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) < 2:
        print("用法: python3 transcribe_assemblyai.py <file_path> [language]")
        print("  language: zh (中文), en (英文), auto (自动检测，默认)")
        sys.exit(1)

    file_path = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "auto"

    if not os.path.exists(file_path):
        print(f"错误: 文件不存在: {file_path}", file=sys.stderr)
        sys.exit(1)

    upload_url = upload_file(file_path)
    tid = submit_transcription(upload_url, language)
    print("[等待] 转录处理中（大型文件可能需要数分钟）...")
    result = poll_result(tid)
    output = format_transcript(result)
    print("\n" + "=" * 60)
    print(output)
    print("=" * 60)

    json_path = file_path + ".transcript.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n[存档] JSON原始数据: {json_path}")
    return result


if __name__ == "__main__":
    main()
