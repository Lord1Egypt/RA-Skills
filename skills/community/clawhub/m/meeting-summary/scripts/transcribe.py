#!/usr/bin/env python3
"""Transcribe audio files via Step ASR APIs.

Default transport uses the file-upload transcription endpoint, which is more
stable for local meeting recordings. The legacy SSE transport remains available
for explicit fallback or real-time style experiments.
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.request
import uuid

TRANSCRIPTIONS_URL = "https://api.stepfun.com/v1/audio/transcriptions"
SSE_API_URL = "https://api.stepfun.com/v1/audio/asr/sse"
KEY_FILE_CANDIDATES = ("~/.stepfun_api_key", "~/.step_api_key")

FORMAT_MAP = {
    ".pcm": ("pcm", "pcm_s16le"),
    ".raw": ("pcm", "pcm_s16le"),
    ".wav": ("wav", "pcm_s16le"),
    ".mp3": ("mp3", ""),
    ".ogg": ("ogg", ""),
    ".opus": ("ogg", ""),
}

DEFAULT_SSE_MODEL = "step-asr-1.1-stream"
DEFAULT_TRANSCRIPTIONS_MODEL = "step-asr"


def detect_format(filepath, override_type):
    if override_type:
        codec = "pcm_s16le" if override_type == "pcm" else ""
        return override_type, codec
    ext = os.path.splitext(filepath)[1].lower()
    return FORMAT_MAP.get(ext, ("pcm", "pcm_s16le"))


def build_sse_request_body(audio_b64, args):
    fmt_type, codec = detect_format(args.audio_file, args.format_type)

    format_config = {
        "type": fmt_type,
        "rate": args.sample_rate,
        "bits": 16,
        "channel": 1,
    }
    if codec:
        format_config["codec"] = codec

    transcription_config = {
        "model": args.model,
        "language": args.language,
        "full_rerun_on_commit": not args.no_rerun,
        "enable_itn": not args.no_itn,
    }
    if args.prompt:
        transcription_config["prompt"] = args.prompt

    transcription_config["turn_detection"] = {
        "type": "server_vad",
        "silence_duration_ms": 800,
        "threshold": 0.5,
    }

    return {
        "audio": {
            "data": audio_b64,
            "input": {
                "transcription": transcription_config,
                "format": format_config,
            },
        }
    }


def parse_sse_line(line):
    line = line.strip()
    if not line.startswith("data:"):
        return None
    payload = line[len("data:"):].strip()
    if not payload or payload == "[DONE]":
        return None
    return json.loads(payload)


def load_api_key():
    for env_name in ("STEPFUN_API_KEY", "STEP_API_KEY"):
        value = os.environ.get(env_name, "").strip()
        if value:
            return value

    for key_path in KEY_FILE_CANDIDATES:
        expanded = os.path.expanduser(key_path)
        try:
            with open(expanded, "r", encoding="utf-8") as handle:
                value = handle.read().strip()
        except OSError:
            continue
        if value:
            return value

    return ""


def encode_multipart_form(fields, file_field_name, file_path):
    boundary = f"----StepBoundary{uuid.uuid4().hex}"
    body = bytearray()

    for key, value in fields.items():
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(
            f'Content-Disposition: form-data; name="{key}"\r\n\r\n{value}\r\n'.encode("utf-8")
        )

    filename = os.path.basename(file_path)
    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    with open(file_path, "rb") as handle:
        data = handle.read()

    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(
        (
            f'Content-Disposition: form-data; name="{file_field_name}"; '
            f'filename="{filename}"\r\n'
        ).encode("utf-8")
    )
    body.extend(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
    body.extend(data)
    body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode("utf-8"))
    return boundary, bytes(body)


def transcribe_via_transcriptions(args, api_key):
    fields = {
        "model": args.model or DEFAULT_TRANSCRIPTIONS_MODEL,
        "response_format": args.response_format,
    }
    if args.hotwords:
        fields["hotwords"] = args.hotwords

    boundary, body = encode_multipart_form(fields, "file", args.audio_file)
    req = urllib.request.Request(
        TRANSCRIPTIONS_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Accept": "application/json" if args.response_format == "json" else "*/*",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            payload = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {err_body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Connection error: {exc.reason}") from exc

    if args.response_format == "json":
        try:
            data = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Failed to parse transcription JSON: {exc}") from exc
        return {
            "text": data.get("text", ""),
            "usage": data.get("usage", {}),
            "segments": [],
            "transport": "transcriptions",
            "response_format": args.response_format,
        }

    return {
        "text": payload.strip(),
        "usage": {},
        "segments": [],
        "transport": "transcriptions",
        "response_format": args.response_format,
    }


def transcribe_via_sse(args, api_key):
    with open(args.audio_file, "rb") as handle:
        audio_b64 = base64.b64encode(handle.read()).decode("ascii")

    body = build_sse_request_body(audio_b64, args)
    data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(
        SSE_API_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        resp = urllib.request.urlopen(req)
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {err_body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Connection error: {exc.reason}") from exc

    full_text = ""
    usage = {}
    segments = []

    try:
        for raw_line in resp:
            line = raw_line.decode("utf-8", errors="replace")
            event = parse_sse_line(line)
            if event is None:
                continue

            event_type = event.get("type", "")
            if event_type == "transcript.text.delta":
                delta = event.get("delta", "")
                start_time = event.get("start_time")
                end_time = event.get("end_time")
                if not args.no_stream and not args.json:
                    sys.stdout.write(delta)
                    sys.stdout.flush()
                if delta:
                    seg = {"text": delta}
                    if start_time is not None:
                        seg["start_time"] = start_time
                    if end_time is not None:
                        seg["end_time"] = end_time
                    segments.append(seg)
            elif event_type == "transcript.text.done":
                full_text = event.get("text", "")
                usage = event.get("usage", {})
            elif event_type == "error":
                raise RuntimeError(f"API error: {event.get('message', 'Unknown error')}")
    finally:
        resp.close()

    if not segments and full_text:
        segments.append({"text": full_text, "start_time": None, "end_time": None})

    return {
        "text": full_text,
        "usage": usage,
        "segments": segments,
        "transport": "sse",
        "response_format": "json",
    }


def save_output(args, result):
    if not args.out:
        return
    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as handle:
        if args.json:
            json.dump(result, handle, ensure_ascii=False, indent=2)
        else:
            handle.write(result.get("text", ""))
    print(f"Saved to: {args.out}", file=sys.stderr)


def transcribe(args):
    api_key = load_api_key()
    if not api_key:
        print(
            "Error: StepFun API key is not configured. Set STEPFUN_API_KEY "
            "(preferred) or STEP_API_KEY, or save it in ~/.stepfun_api_key.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not os.path.isfile(args.audio_file):
        print(f"Error: File not found: {args.audio_file}", file=sys.stderr)
        sys.exit(1)

    try:
        if args.transport == "transcriptions":
            result = transcribe_via_transcriptions(args, api_key)
        else:
            result = transcribe_via_sse(args, api_key)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)

    if not args.no_stream and not args.json and args.transport == "sse":
        print()

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.no_stream:
        print(result.get("text", ""))

    save_output(args, result)


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio via Step ASR APIs."
    )
    parser.add_argument("audio_file", help="Path to the audio file")
    parser.add_argument(
        "--transport",
        choices=("transcriptions", "sse"),
        default="transcriptions",
        help="Preferred Step API transport. Default: transcriptions",
    )
    parser.add_argument(
        "--language", default="zh",
        help="Language code: zh (Chinese) or en (English). Default: zh",
    )
    parser.add_argument(
        "--model", default="",
        help="ASR model name. Defaults depend on transport.",
    )
    parser.add_argument(
        "--response-format",
        choices=("json", "text", "srt", "vtt"),
        default="json",
        help="Response format for transcriptions transport. Default: json",
    )
    parser.add_argument(
        "--hotwords", default="",
        help="Optional hotwords JSON string for transcriptions transport",
    )
    parser.add_argument(
        "--out", default="",
        help="Save transcription to this file path",
    )
    parser.add_argument(
        "--prompt", default="",
        help="Hint text to improve accuracy for SSE transport",
    )
    parser.add_argument(
        "--format-type", default="",
        help="Audio format type for SSE transport: pcm, mp3, ogg",
    )
    parser.add_argument(
        "--sample-rate", type=int, default=16000,
        help="Audio sample rate in Hz for SSE transport. Default: 16000",
    )
    parser.add_argument(
        "--no-stream", action="store_true",
        help="Disable streaming output, only print final result",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output result as JSON",
    )
    parser.add_argument(
        "--no-rerun", action="store_true",
        help="Disable rerun on commit for SSE transport",
    )
    parser.add_argument(
        "--no-itn", action="store_true",
        help="Disable ITN for SSE transport",
    )
    args = parser.parse_args()

    if not args.model:
        args.model = (
            DEFAULT_TRANSCRIPTIONS_MODEL
            if args.transport == "transcriptions"
            else DEFAULT_SSE_MODEL
        )

    transcribe(args)


if __name__ == "__main__":
    main()
