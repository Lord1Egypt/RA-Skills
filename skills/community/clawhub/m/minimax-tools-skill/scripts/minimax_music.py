#!/usr/bin/env python3
import argparse

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
    ap = argparse.ArgumentParser(description="MiniMax music generation wrapper")
    ap.add_argument("--model", default="music-2.5+")
    ap.add_argument("--prompt")
    ap.add_argument("--lyrics")
    ap.add_argument("--lyrics-file")
    ap.add_argument("--lyrics-optimizer", action="store_true")
    ap.add_argument("--instrumental", action="store_true")
    ap.add_argument("--stream", action="store_true")
    ap.add_argument("--output-format", default="url", choices=["url", "hex"])
    ap.add_argument("--sample-rate", type=int, default=44100)
    ap.add_argument("--bitrate", type=int, default=256000)
    ap.add_argument("--format", default="mp3", choices=["mp3", "wav", "pcm"])
    ap.add_argument("--watermark", action="store_true")
    add_common_output_args(ap, "music")
    args = ap.parse_args()

    lyrics = args.lyrics
    if args.lyrics_file:
        lyrics = open(args.lyrics_file, "r", encoding="utf-8").read()

    if args.stream and args.output_format == "url":
        raise SystemExit("stream mode only supports hex output")
    if not args.instrumental and not lyrics and not args.lyrics_optimizer:
        raise SystemExit("non-instrumental mode requires --lyrics or --lyrics-file, unless --lyrics-optimizer is used")
    if args.instrumental and args.model != "music-2.5+":
        raise SystemExit("instrumental mode is only documented for music-2.5+")

    body = {
        "model": args.model,
        "stream": args.stream,
        "output_format": args.output_format,
        "audio_setting": {
            "sample_rate": args.sample_rate,
            "bitrate": args.bitrate,
            "format": args.format,
        },
        "aigc_watermark": args.watermark,
        "lyrics_optimizer": args.lyrics_optimizer,
        "is_instrumental": args.instrumental,
    }
    if args.prompt:
        body["prompt"] = args.prompt
    if lyrics:
        body["lyrics"] = lyrics

    try:
        data = request_json("POST", "/v1/music_generation", json_body=body, timeout=600)
    except MiniMaxError as e:
        raise SystemExit(str(e))

    audio = ((data.get("data") or {}).get("audio"))
    trace_id = data.get("trace_id")
    extra = data.get("extra_info") or {}

    if not audio:
        raise SystemExit("MiniMax music API returned no audio")

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
            "path": str(out_path),
            "source": source,
            "meta": extra,
        }
    )


if __name__ == "__main__":
    main()
