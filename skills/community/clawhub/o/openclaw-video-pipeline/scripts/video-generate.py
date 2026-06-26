#!/usr/bin/env python3
"""
Generate three 10s CogVideoX-3 clips from a storyboard JSON (30s total).
Uses Zhipu open.bigmodel.cn REST API (async submit + poll).
"""

from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_BASE = "https://open.bigmodel.cn/api"
DEFAULT_STORYBOARD_PATH = Path("storyboard/storyboard.json")


def _ssl_context() -> ssl.SSLContext:
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


SEGMENT_DURATION = 10
EXPECTED_SEGMENTS = 3


def _request_json(
    method: str,
    url: str,
    api_key: str,
    body: dict[str, Any] | None = None,
) -> dict[str, Any]:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    ctx = _ssl_context()
    try:
        with urllib.request.urlopen(req, timeout=120, context=ctx) as resp:
            raw = resp.read().decode()
    except urllib.error.HTTPError as e:
        err_body = e.read().decode() if e.fp else ""
        raise RuntimeError(f"HTTP {e.code} {url}: {err_body}") from e
    return json.loads(raw) if raw else {}


def _submit_generation(
    base: str,
    api_key: str,
    prompt: str,
    *,
    duration: int,
    quality: str,
    with_audio: bool,
    size: str,
    fps: int,
) -> str:
    url = f"{base.rstrip('/')}/paas/v4/videos/generations"
    body = {
        "model": "cogvideox-3",
        "prompt": prompt[:512],
        "duration": duration,
        "quality": quality,
        "with_audio": with_audio,
        "size": size,
        "fps": fps,
    }
    out = _request_json("POST", url, api_key, body)
    if "error" in out:
        err = out["error"]
        raise RuntimeError(f"API error: {err.get('code')} {err.get('message')}")
    task_id = out.get("id")
    if not task_id:
        raise RuntimeError(f"Missing task id in response: {out}")
    return str(task_id)


def _poll_result(
    base: str,
    api_key: str,
    task_id: str,
    *,
    poll_interval: float,
    timeout: float,
) -> str:
    url = f"{base.rstrip('/')}/paas/v4/async-result/{task_id}"
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        out = _request_json("GET", url, api_key, None)
        if "error" in out:
            err = out["error"]
            raise RuntimeError(f"Poll error: {err.get('code')} {err.get('message')}")
        status = out.get("task_status") or out.get("taskStatus")
        if status == "FAIL":
            raise RuntimeError(f"Task failed: {out}")
        if status == "SUCCESS":
            videos = out.get("video_result") or []
            if not videos:
                raise RuntimeError(f"No video_result in success payload: {out}")
            u = videos[0].get("url")
            if not u:
                raise RuntimeError(f"No url in video_result: {out}")
            return str(u)
        time.sleep(poll_interval)
    raise TimeoutError(f"Task {task_id} not finished within {timeout}s")


def _download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=300, context=_ssl_context()) as resp:
        dest.write_bytes(resp.read())


def load_segments(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if "segments" in data:
        segs = data["segments"]
        if len(segs) != EXPECTED_SEGMENTS:
            raise ValueError(f"Expected {EXPECTED_SEGMENTS} segments, got {len(segs)}")
        prompts = []
        for i, s in enumerate(segs):
            p = s.get("prompt") if isinstance(s, dict) else None
            if not p or not str(p).strip():
                raise ValueError(f"segments[{i}] missing prompt")
            prompts.append(str(p).strip())
        return prompts
    if "prompts" in data:
        ps = data["prompts"]
        if not isinstance(ps, list) or len(ps) != EXPECTED_SEGMENTS:
            raise ValueError(f"prompts must be a list of length {EXPECTED_SEGMENTS}")
        return [str(p).strip() for p in ps]
    raise ValueError("JSON must contain 'segments' (3 objects with prompt) or 'prompts' (3 strings)")


def main() -> int:
    p = argparse.ArgumentParser(description="CogVideoX-3: 3x10s clips from storyboard JSON")
    p.add_argument(
        "--input",
        "-i",
        type=Path,
        default=DEFAULT_STORYBOARD_PATH,
        help=f"Storyboard JSON (default: {DEFAULT_STORYBOARD_PATH})",
    )
    p.add_argument("--output-dir", "-o", type=Path, default=None, help="Download segment MP4s here")
    p.add_argument("--quality", default="quality", choices=("quality", "speed"))
    p.add_argument("--size", default="1920x1080")
    p.add_argument("--fps", type=int, default=30, choices=(30, 60))
    p.add_argument("--with-audio", action="store_true", default=True)
    p.add_argument("--no-audio", action="store_true")
    p.add_argument("--poll-interval", type=float, default=3.0)
    p.add_argument("--timeout", type=float, default=600.0)
    args = p.parse_args()

    api_key = os.environ.get("ZHIPUAI_API_KEY", "").strip()
    if not api_key:
        print("Missing ZHIPUAI_API_KEY in environment.", file=sys.stderr)
        return 1

    base = os.environ.get("BIGMODEL_API_BASE", DEFAULT_BASE).strip() or DEFAULT_BASE
    with_audio = False if args.no_audio else args.with_audio

    if not args.input.is_file():
        print(f"Input not found: {args.input}", file=sys.stderr)
        return 1

    try:
        prompts = load_segments(args.input)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Invalid storyboard: {e}", file=sys.stderr)
        return 1

    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, Any]] = []
    for idx, prompt in enumerate(prompts, start=1):
        print(f"[segment {idx}/{EXPECTED_SEGMENTS}] submitting ({SEGMENT_DURATION}s)...", flush=True)
        try:
            task_id = _submit_generation(
                base,
                api_key,
                prompt,
                duration=SEGMENT_DURATION,
                quality=args.quality,
                with_audio=with_audio,
                size=args.size,
                fps=args.fps,
            )
            print(f"[segment {idx}/{EXPECTED_SEGMENTS}] task id={task_id} polling...", flush=True)
            video_url = _poll_result(
                base,
                api_key,
                task_id,
                poll_interval=args.poll_interval,
                timeout=args.timeout,
            )
        except (RuntimeError, TimeoutError, OSError) as e:
            print(f"[segment {idx}/{EXPECTED_SEGMENTS}] failed: {e}", file=sys.stderr)
            return 1

        entry: dict[str, Any] = {"index": idx, "url": video_url}
        if args.output_dir:
            out_path = args.output_dir / f"segment_{idx:02d}.mp4"
            print(f"[segment {idx}/{EXPECTED_SEGMENTS}] downloading -> {out_path}", flush=True)
            try:
                _download(video_url, out_path)
            except OSError as e:
                print(f"Download failed: {e}", file=sys.stderr)
                return 1
            entry["path"] = str(out_path)

        results.append(entry)
        print(f"[segment {idx}/{EXPECTED_SEGMENTS}] url={video_url}", flush=True)

    summary = {
        "model": "cogvideox-3",
        "duration_per_segment": SEGMENT_DURATION,
        "total_target_seconds": SEGMENT_DURATION * EXPECTED_SEGMENTS,
        "segments": results,
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
