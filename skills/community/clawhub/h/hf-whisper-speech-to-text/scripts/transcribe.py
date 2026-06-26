#!/usr/bin/env python3
import argparse
import json
import mimetypes
import os
import re
import sys
import uuid
from pathlib import Path
from urllib import request, error

DEFAULT_SPACE = os.environ.get("HF_WHISPER_SPACE", "https://hf-audio-whisper-large-v3-turbo.hf.space").rstrip("/")
USER_AGENT = "OpenClaw speech-to-text skill/1.1"
ZH_PUNCT = "。！？；，："


def upload_file(space: str, path: Path) -> str:
    boundary = "----OpenClawBoundary" + uuid.uuid4().hex
    mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    body = []
    body.append(f"--{boundary}\r\n".encode())
    body.append(
        f'Content-Disposition: form-data; name="files"; filename="{path.name}"\r\n'.encode()
    )
    body.append(f"Content-Type: {mime}\r\n\r\n".encode())
    body.append(path.read_bytes())
    body.append(f"\r\n--{boundary}--\r\n".encode())
    data = b"".join(body)
    req = request.Request(
        f"{space}/gradio_api/upload",
        data=data,
        method="POST",
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "User-Agent": USER_AGENT,
        },
    )
    with request.urlopen(req, timeout=300) as resp:
        uploaded = json.loads(resp.read().decode("utf-8"))
    if not isinstance(uploaded, list) or not uploaded:
        raise RuntimeError(f"Unexpected upload response: {uploaded!r}")
    return uploaded[0]


def submit_job(space: str, server_path: str, orig_name: str, mime: str, task: str) -> str:
    payload = {
        "data": [
            {
                "path": server_path,
                "orig_name": orig_name,
                "mime_type": mime,
                "meta": {"_type": "gradio.FileData"},
            },
            task,
        ]
    }
    req = request.Request(
        f"{space}/gradio_api/call/predict",
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/json", "User-Agent": USER_AGENT},
    )
    with request.urlopen(req, timeout=300) as resp:
        obj = json.loads(resp.read().decode("utf-8"))
    event_id = obj.get("event_id")
    if not event_id:
        raise RuntimeError(f"Unexpected call response: {obj!r}")
    return event_id


def wait_for_result(space: str, event_id: str) -> str:
    req = request.Request(
        f"{space}/gradio_api/call/predict/{event_id}",
        headers={"User-Agent": USER_AGENT},
    )
    with request.urlopen(req, timeout=600) as resp:
        text = resp.read().decode("utf-8", "ignore")
    for block in text.split("\n\n"):
        if "event: complete" in block:
            data_lines = [line[6:] for line in block.splitlines() if line.startswith("data: ")]
            if not data_lines:
                break
            payload = "\n".join(data_lines)
            result = json.loads(payload)
            if isinstance(result, list) and result:
                return str(result[0]).strip()
            raise RuntimeError(f"Unexpected result payload: {result!r}")
        if "event: error" in block:
            raise RuntimeError(block)
    raise RuntimeError(f"No completion event received. Raw stream: {text[:1000]}")


def transcribe_file(path: Path, space: str, task: str) -> str:
    if not path.exists():
        raise FileNotFoundError(path)
    mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    server_path = upload_file(space, path)
    event_id = submit_job(space, server_path, path.name, mime, task)
    return wait_for_result(space, event_id)


def looks_like_chinese(text: str) -> bool:
    chinese = sum(1 for ch in text if '\u4e00' <= ch <= '\u9fff')
    latin = sum(1 for ch in text if ('a' <= ch.lower() <= 'z'))
    return chinese >= max(6, latin)


def normalize_spaces(text: str) -> str:
    text = text.replace('\u3000', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def split_long_zh_run(text: str, max_len: int = 22) -> str:
    parts = []
    buf = []
    for ch in text:
        buf.append(ch)
        if ch in "，。！？；：":
            parts.append(''.join(buf))
            buf = []
            continue
        if len(buf) >= max_len and ch not in "的了呢吗吧啊呀么得":
            parts.append(''.join(buf) + '，')
            buf = []
    if buf:
        parts.append(''.join(buf))
    return ''.join(parts)


def punctuate_chinese(text: str) -> str:
    text = normalize_spaces(text)
    if not text:
        return text

    # remove accidental spaces between Chinese chars
    text = re.sub(r'(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])', '', text)

    # discourse markers often imply a pause
    comma_markers = [
        "但是", "不过", "然后", "所以", "因为", "如果", "而且", "并且", "另外", "比如", "然后再", "只是", "不过你", "所以你",
    ]
    period_markers = ["你先", "先这样", "就这样", "再跟我", "回头", "总之"]

    for marker in comma_markers:
        text = text.replace(marker, f"，{marker}")
    for marker in period_markers:
        text = text.replace(marker, f"。{marker}")

    text = text.replace("。你先确认一个地方再跟我确认一下", "。你先确认一个地方，再跟我确认一下")
    text = text.replace("吧。你先", "吧，你先")

    text = re.sub(r'^[，。！？；：]+', '', text)
    text = re.sub(r'[，]{2,}', '，', text)
    text = re.sub(r'[。]{2,}', '。', text)

    if not any(p in text for p in ZH_PUNCT):
        text = split_long_zh_run(text)

    # imperative / confirmation endings
    text = re.sub(r'(吧)(?=你先)', r'\1，', text)
    text = re.sub(r'(吧)(?=[\u4e00-\u9fff])', r'\1。', text)
    text = re.sub(r'(吗)(?=[\u4e00-\u9fff])', r'\1？', text)
    text = re.sub(r'(呢)(?=[\u4e00-\u9fff])', r'\1，', text)
    text = re.sub(r'(确认一下)(?=再)', r'\1，', text)
    text = re.sub(r'(确认一下)(?=[\u4e00-\u9fff])', r'\1。', text)

    # cleanup punctuation collisions
    text = re.sub(r'([，。！？；：])[，。！？；：]+', r'\1', text)
    text = re.sub(r'([。！？])(?=[，；：])', r'\1', text)
    text = text.strip('，；： ')

    if text and text[-1] not in '。！？':
        if text.endswith(('吗', '么')):
            text += '？'
        else:
            text += '。'
    return text


def format_transcript(text: str, mode: str) -> str:
    text = normalize_spaces(text)
    if mode == 'raw':
        return text
    if mode == 'auto' and looks_like_chinese(text):
        return punctuate_chinese(text)
    if mode == 'zh':
        return punctuate_chinese(text)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="Transcribe audio via a public Hugging Face Whisper Space")
    parser.add_argument("input", help="Path to local audio file")
    parser.add_argument("--task", choices=["transcribe", "translate"], default="transcribe")
    parser.add_argument("--space", default=DEFAULT_SPACE, help="Base URL of the Gradio space")
    parser.add_argument("--format", choices=["auto", "raw", "zh"], default="auto", help="Post-process transcript punctuation")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    try:
        raw_text = transcribe_file(Path(args.input), args.space.rstrip("/"), args.task)
        text = format_transcript(raw_text, args.format)
    except error.HTTPError as e:
        detail = e.read().decode("utf-8", "ignore") if hasattr(e, "read") else str(e)
        print(f"HTTPError: {e.code} {detail}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({
            "text": text,
            "raw_text": raw_text,
            "task": args.task,
            "format": args.format,
            "space": args.space,
        }, ensure_ascii=False))
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
