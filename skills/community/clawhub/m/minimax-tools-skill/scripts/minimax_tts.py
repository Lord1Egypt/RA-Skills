#!/usr/bin/env python3
import argparse
from pathlib import Path

from common import (
    MiniMaxError,
    decode_hex_to_file,
    download_url,
    print_json,
    request_json,
    resolve_output_path,
    add_common_output_args,
    safe_ext_from_url,
)


def main() -> None:
    ap = argparse.ArgumentParser(description="MiniMax TTS wrapper")
    ap.add_argument("--text", required=True)
    ap.add_argument("--model", default="speech-2.8-turbo")
    ap.add_argument("--voice", help="voice_id; if omitted, use built-in default by --voice-lang")
    ap.add_argument("--voice-lang", default="zh", choices=["zh", "en"], help="default voice bucket when --voice is omitted")
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--volume", type=float, default=1.0)
    ap.add_argument("--pitch", type=int, default=0)
    ap.add_argument("--emotion")
    ap.add_argument("--sample-rate", type=int, default=32000)
    ap.add_argument("--bitrate", type=int, default=128000)
    ap.add_argument("--format", default="mp3", choices=["mp3", "wav", "pcm", "flac"])
    ap.add_argument("--channel", type=int, default=1)
    ap.add_argument("--language-boost")
    ap.add_argument("--subtitle", action="store_true")
    ap.add_argument("--stream", action="store_true")
    ap.add_argument("--output-format", default="url", choices=["url", "hex"])
    ap.add_argument("--watermark", action="store_true")
    add_common_output_args(ap, "tts")
    args = ap.parse_args()

    if args.stream and args.output_format == "url":
        raise SystemExit("stream mode only supports hex output")

    default_voices = {
        "zh": "Chinese (Mandarin)_Lyrical_Voice",
        "en": "English_Graceful_Lady",
    }
    voice_id = args.voice or default_voices[args.voice_lang]

    body = {
        "model": args.model,
        "text": args.text,
        "stream": args.stream,
        "voice_setting": {
            "voice_id": voice_id,
            "speed": args.speed,
            "vol": args.volume,
            "pitch": args.pitch,
        },
        "audio_setting": {
            "sample_rate": args.sample_rate,
            "bitrate": args.bitrate,
            "format": args.format,
            "channel": args.channel,
        },
        "subtitle_enable": args.subtitle,
        "output_format": args.output_format,
        "aigc_watermark": args.watermark,
    }
    if args.emotion:
        body["voice_setting"]["emotion"] = args.emotion
    if args.language_boost:
        body["language_boost"] = args.language_boost

    try:
        data = request_json("POST", "/v1/t2a_v2", json_body=body)
    except MiniMaxError as e:
        raise SystemExit(str(e))

    audio = ((data.get("data") or {}).get("audio"))
    trace_id = data.get("trace_id")
    extra = data.get("extra_info") or {}
    subtitle_file = (data.get("data") or {}).get("subtitle_file")

    if not audio:
        raise SystemExit("MiniMax TTS returned no audio")

    out_path = resolve_output_path(args.output, args.prefix, f".{args.format}")
    if args.output_format == "url":
        ext = safe_ext_from_url(audio, f".{args.format}")
        out_path = out_path.with_suffix(ext)
        download_url(audio, out_path)
        source = "url"
    else:
        decode_hex_to_file(audio, out_path)
        source = "hex"

    print_json(
        {
            "ok": True,
            "trace_id": trace_id,
            "voice_id": voice_id,
            "path": str(out_path),
            "subtitle_file": subtitle_file,
            "source": source,
            "meta": extra,
        }
    )


if __name__ == "__main__":
    main()
