#!/usr/bin/env python3
import argparse
import base64
import json
import mimetypes
import os
import sys
from collections import defaultdict
from pathlib import Path

import requests


TRANSCRIBE_URL = "https://studio.mosi.cn/v1/audio/transcriptions"


def fail(msg: str, code: int = 1):
    print(f"Error: {msg}", file=sys.stderr)
    raise SystemExit(code)


def file_to_data_url(path: str) -> str:
    p = Path(path)
    if not p.exists() or not p.is_file():
        fail(f"file not found: {path}")
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    raw = p.read_bytes()
    b64 = base64.b64encode(raw).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def normalize_segments(obj):
    segs = (
        obj.get("segments")
        or obj.get("meta_info", {}).get("segments")
        or obj.get("asr_transcription_result", {}).get("segments")
        or []
    )
    out = []
    for s in segs:
        out.append(
            {
                "start": s.get("start") or s.get("start_time") or s.get("start_ms") or s.get("start_s"),
                "end": s.get("end") or s.get("end_time") or s.get("end_ms") or s.get("end_s"),
                "speaker": s.get("speaker") or s.get("speaker_id") or "UNKNOWN",
                "content": s.get("content") or s.get("text") or "",
            }
        )
    return out


def main():
    ap = argparse.ArgumentParser(description="Call MOSS transcribe-diarize and save outputs")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--audio-url")
    src.add_argument("--file")
    src.add_argument("--audio-data")
    ap.add_argument("--model", default="moss-transcribe-diarize")
    ap.add_argument("--meta-info", action="store_true")
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--out", default="transcribe_result.json")
    ap.add_argument("--segments-format", choices=["json", "compact", "text"], default="json")
    args = ap.parse_args()

    api_key = os.getenv("MOSS_API_KEY") or os.getenv("MOSI_TTS_API_KEY") or os.getenv("MOSI_API_KEY")
    if not api_key:
        fail("API key is not set (expected one of: MOSS_API_KEY / MOSI_TTS_API_KEY / MOSI_API_KEY)")

    if args.audio_url:
        audio_data = args.audio_url
    elif args.file:
        audio_data = file_to_data_url(args.file)
    else:
        audio_data = args.audio_data

    payload = {
        "model": args.model,
        "audio_data": audio_data,
        "meta_info": args.meta_info,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        r = requests.post(TRANSCRIBE_URL, headers=headers, json=payload, timeout=args.timeout)
    except requests.RequestException as e:
        fail(f"request failed: {e}")

    try:
        data = r.json()
    except Exception:
        fail(f"Non-JSON response ({r.status_code}): {r.text[:300]}")

    if r.status_code >= 400:
        fail(f"HTTP {r.status_code}: {json.dumps(data, ensure_ascii=False)[:500]}")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    segs = normalize_segments(data)

    if args.segments_format == "json":
        seg_path = str(out_path).replace(".json", ".segments.json")
        Path(seg_path).write_text(json.dumps(segs, ensure_ascii=False, indent=2), encoding="utf-8")
    elif args.segments_format == "compact":
        seg_path = str(out_path).replace(".json", ".segments.compact.json")
        Path(seg_path).write_text(json.dumps(segs, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    else:
        seg_path = str(out_path).replace(".json", ".segments.txt")
        with open(seg_path, "w", encoding="utf-8") as f:
            for s in segs:
                f.write(f"[{s['start']} - {s['end']}] {s['speaker']}: {s['content']}\n")

    by = defaultdict(list)
    for s in segs:
        by[s["speaker"]].append(s["content"])
    by_path = str(out_path).replace(".json", ".by_speaker.txt")
    with open(by_path, "w", encoding="utf-8") as f:
        for spk, parts in by.items():
            f.write(f"## {spk}\n")
            f.write("\n".join(parts) + "\n\n")

    print(
        json.dumps(
            {
                "status": r.status_code,
                "result": str(out_path),
                "segments": seg_path,
                "by_speaker": by_path,
                "segment_count": len(segs),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
