#!/usr/bin/env python3
"""Generate structured meeting minutes from meeting audio."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

import requests
from openai import OpenAI

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
OUTPUT_DIR = SKILL_DIR / "outputs"

LLM_BASE_URL = ""
LLM_MODEL = ""
LLM_API_KEY = ""
LLM_TIMEOUT = 60.0

ASR_URL = ""
ASR_MODEL = ""
ASR_API_KEY = ""
ASR_RESPONSE_FORMAT = "verbose_json"
ASR_TIMEOUT = 300.0

TTS_URL = ""
TTS_MODEL = ""
TTS_API_KEY = ""
TTS_VOICE_ID = "male_0004_a"
TTS_TIMEOUT = 60.0

MIN_AUDIO_BYTES = 1024


def load_env() -> None:
    if load_dotenv is None:
        return
    for path in (SKILL_DIR / ".env", Path.cwd() / ".env"):
        if path.exists():
            load_dotenv(path)


def refresh_runtime_settings() -> None:
    global LLM_BASE_URL, LLM_MODEL, LLM_API_KEY, LLM_TIMEOUT
    global ASR_URL, ASR_MODEL, ASR_API_KEY, ASR_RESPONSE_FORMAT, ASR_TIMEOUT
    global TTS_URL, TTS_MODEL, TTS_API_KEY, TTS_VOICE_ID, TTS_TIMEOUT

    LLM_BASE_URL = os.environ.get("MEETING_LLM_BASE_URL", "https://models.audiozen.cn/v1")
    LLM_MODEL = os.environ.get("MEETING_LLM_MODEL", "doubao-seed-2-0-lite-260215")
    LLM_API_KEY = os.environ.get("MEETING_LLM_API_KEY", os.environ.get("IME_MODEL_API_KEY", ""))
    LLM_TIMEOUT = float(os.environ.get("MEETING_LLM_TIMEOUT", "60"))

    ASR_URL = os.environ.get("MEETING_ASR_URL", "https://api.senseaudio.cn/v1/audio/transcriptions")
    ASR_MODEL = os.environ.get("MEETING_ASR_MODEL", "sense-asr-pro")
    ASR_API_KEY = os.environ.get("MEETING_ASR_API_KEY", os.environ.get("SENSEAUDIO_API_KEY", ""))
    ASR_RESPONSE_FORMAT = os.environ.get("MEETING_ASR_RESPONSE_FORMAT", "verbose_json")
    ASR_TIMEOUT = float(os.environ.get("MEETING_ASR_TIMEOUT", "300"))

    TTS_URL = os.environ.get("MEETING_TTS_URL", "https://api.senseaudio.cn/v1/t2a_v2")
    TTS_MODEL = os.environ.get("MEETING_TTS_MODEL", "SenseAudio-TTS-1.0")
    TTS_API_KEY = os.environ.get("MEETING_TTS_API_KEY", os.environ.get("SENSEAUDIO_API_KEY", ""))
    TTS_VOICE_ID = os.environ.get("MEETING_TTS_VOICE_ID", "male_0004_a")
    TTS_TIMEOUT = float(os.environ.get("MEETING_TTS_TIMEOUT", "60"))


def require_env(name: str, value: str) -> str:
    if value:
        return value
    raise SystemExit(f"缺少必要配置: {name}")


def build_client() -> OpenAI:
    return OpenAI(
        api_key=require_env("MEETING_LLM_API_KEY / IME_MODEL_API_KEY", LLM_API_KEY),
        base_url=LLM_BASE_URL,
        timeout=LLM_TIMEOUT,
    )


def extract_message_content(response: Any) -> str:
    content = response.choices[0].message.content
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for item in content:
            text = getattr(item, "text", None)
            if isinstance(text, str):
                parts.append(text)
            elif isinstance(item, dict) and isinstance(item.get("text"), str):
                parts.append(item["text"])
        return "".join(parts).strip()
    raise ValueError("模型响应缺少文本内容")


def extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 3:
            text = "\n".join(lines[1:-1]).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError(f"模型未返回 JSON: {text}")
    return json.loads(text[start : end + 1])


def transcribe_audio(audio_file: Path, language: str) -> str:
    headers = {"Authorization": f"Bearer {require_env('MEETING_ASR_API_KEY / SENSEAUDIO_API_KEY', ASR_API_KEY)}"}
    data: dict[str, Any] = {
        "model": ASR_MODEL,
        "response_format": ASR_RESPONSE_FORMAT,
    }
    if language:
        data["language"] = language
    with audio_file.open("rb") as handle:
        files = {"file": (audio_file.name, handle)}
        response = requests.post(ASR_URL, headers=headers, data=data, files=files, timeout=ASR_TIMEOUT)
    if response.status_code != 200:
        raise RuntimeError("Speech recognition failed")
    payload = response.json()
    text = payload.get("text", "").strip()
    if not text and payload.get("segments"):
        text = " ".join(seg.get("text", "").strip() for seg in payload["segments"]).strip()
    if not text:
        raise RuntimeError("Speech recognition failed")
    return text


def clean_transcript_locally(transcript: str) -> str:
    cleaned = re.sub(r"\b(嗯|啊|这个|那个|就是|然后)\b", "", transcript)
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\n{2,}", "\n", cleaned)
    return cleaned.strip()


def clean_transcript_with_llm(transcript: str) -> str:
    prompt = f"""You are an assistant that cleans meeting transcripts.

Clean the transcript below:
- remove filler words
- remove repeated phrases
- improve readability
- preserve facts, names, numbers, decisions, and action items

Transcript:
{transcript}

Return only the cleaned transcript text.
"""
    client = build_client()
    response = client.chat.completions.create(
        model=LLM_MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": "Return only cleaned transcript text."},
            {"role": "user", "content": prompt},
        ],
    )
    return extract_message_content(response)


def summarize_meeting(transcript: str) -> dict[str, Any]:
    prompt = f"""You are an AI assistant that generates meeting minutes.

Analyze the following meeting transcript and return JSON with these fields:
- topic
- discussion_points
- decisions
- action_items
- voice_summary_text

Rules:
- do not fabricate missing facts
- discussion_points should be concise
- decisions should only include confirmed conclusions
- action_items should include owner if mentioned

Transcript:
{transcript}
"""
    client = build_client()
    response = client.chat.completions.create(
        model=LLM_MODEL,
        temperature=0.3,
        messages=[
            {"role": "system", "content": "Return valid JSON only."},
            {"role": "user", "content": prompt},
        ],
    )
    return extract_json(extract_message_content(response))


def synthesize_tts(text: str) -> str:
    headers = {
        "Authorization": f"Bearer {require_env('MEETING_TTS_API_KEY / SENSEAUDIO_API_KEY', TTS_API_KEY)}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": TTS_MODEL,
        "text": text,
        "stream": False,
        "voice_setting": {"voice_id": TTS_VOICE_ID},
        "audio_setting": {"format": "mp3", "sample_rate": 32000},
    }
    response = requests.post(TTS_URL, headers=headers, json=payload, timeout=TTS_TIMEOUT)
    response.raise_for_status()
    result = response.json()
    if result.get("base_resp", {}).get("status_code") != 0:
        raise RuntimeError("TTS generation failed")
    audio_hex = result.get("data", {}).get("audio", "")
    if not audio_hex:
        raise RuntimeError("TTS generation failed")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / "voice_summary.mp3"
    out_path.write_bytes(bytes.fromhex(audio_hex))
    return str(out_path)


def chunk_text(text: str, max_chars: int = 6000) -> list[str]:
    if len(text) <= max_chars:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start : start + max_chars])
        start += max_chars
    return chunks


def summarize_long_transcript(transcript: str) -> dict[str, Any]:
    chunks = chunk_text(transcript)
    if len(chunks) == 1:
        return summarize_meeting(transcript)

    partials = []
    for chunk in chunks:
        partials.append(summarize_meeting(chunk))

    merged_text = "\n".join(
        [
            f"Topic: {item.get('topic', '')}\n"
            f"Discussion: {'; '.join(item.get('discussion_points', []))}\n"
            f"Decisions: {'; '.join(item.get('decisions', []))}\n"
            f"Actions: {'; '.join(item.get('action_items', []))}"
            for item in partials
        ]
    )
    return summarize_meeting(merged_text)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate meeting minutes from audio")
    parser.add_argument("--audio-file", required=True, help="会议音频路径")
    parser.add_argument("--need-voice-summary", action="store_true", help="是否生成语音摘要")
    parser.add_argument("--language", default="zh", help="ASR 语言，默认 zh")
    parser.add_argument("--output", default="", help="输出 JSON 文件路径")
    return parser.parse_args()


def main() -> None:
    load_env()
    refresh_runtime_settings()
    args = parse_args()

    audio_file = Path(args.audio_file).expanduser()
    if not audio_file.exists():
        raise SystemExit(f"音频文件不存在: {audio_file}")
    if audio_file.stat().st_size < MIN_AUDIO_BYTES:
        raise SystemExit("Meeting audio too short to summarize")

    transcript = transcribe_audio(audio_file, args.language)
    cleaned_transcript = clean_transcript_locally(transcript)
    try:
        cleaned_transcript = clean_transcript_with_llm(cleaned_transcript)
    except Exception:
        pass

    summary = summarize_long_transcript(cleaned_transcript)
    voice_summary_path = None
    if args.need_voice_summary:
        voice_text = summary.get("voice_summary_text") or f"本次会议主题为{summary.get('topic', '未识别')}。"
        voice_summary_path = synthesize_tts(voice_text)

    result = {
        "topic": summary.get("topic", ""),
        "discussion_points": summary.get("discussion_points", []),
        "decisions": summary.get("decisions", []),
        "action_items": summary.get("action_items", []),
        "cleaned_transcript": cleaned_transcript,
        "voice_summary_path": voice_summary_path,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.output) if args.output else OUTPUT_DIR / "meeting_minutes.json"
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()
