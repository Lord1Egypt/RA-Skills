#!/usr/bin/env python3
"""kie-audio: generate or extend music with Suno via Kie.ai."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kie_client import (  # noqa: E402
    KieClient,
    KieError,
    KieTaskFailed,
    KieTimeout,
)

GENERATE_ENDPOINT = "/api/v1/generate"
EXTEND_ENDPOINT = "/api/v1/generate/upload-and-extend-audio"
POLL_ENDPOINT = "/api/v1/generate/record-info"


def build_payload(args: argparse.Namespace) -> tuple[str, dict]:
    if args.extend:
        payload: dict = {
            "uploadUrl": args.extend,
            "prompt": args.prompt,
            "model": args.model,
        }
        if args.instrumental:
            payload["instrumental"] = True
        if args.custom_mode:
            payload["customMode"] = True
        return EXTEND_ENDPOINT, payload

    payload = {
        "prompt": args.prompt,
        "model": args.model,
    }
    if args.instrumental:
        payload["instrumental"] = True
    if args.custom_mode:
        payload["customMode"] = True
    return GENERATE_ENDPOINT, payload


def extract_audio_entries(data: dict) -> list[dict]:
    """Return list of {audioUrl, coverImageUrl?, duration?} entries."""
    entries: list[dict] = []
    # Suno callback/record-info shape: data.data = [ {...tracks} ]
    inner = data
    if isinstance(data.get("data"), list):
        inner = {"tracks": data["data"]}
    for key in ("tracks", "resultUrls", "audios", "result", "response"):
        val = inner.get(key) if isinstance(inner, dict) else None
        if isinstance(val, list):
            for item in val:
                if isinstance(item, dict):
                    url = (
                        item.get("audioUrl")
                        or item.get("url")
                        or item.get("audio_url")
                    )
                    if url:
                        entries.append(
                            {
                                "audioUrl": url,
                                "coverImageUrl": item.get("coverImageUrl")
                                or item.get("cover_image_url"),
                                "duration": item.get("duration"),
                            }
                        )
                elif isinstance(item, str):
                    entries.append({"audioUrl": item})
    # some payloads single-track:
    single = data.get("audioUrl") or data.get("audio_url")
    if isinstance(single, str):
        entries.append({"audioUrl": single})
    return entries


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--prompt", required=True)
    p.add_argument(
        "--model",
        default="V5_5",
        choices=["V3_5", "V4", "V4_5", "V4_5PLUS", "V5", "V5_5"],
    )
    p.add_argument("--instrumental", action="store_true")
    p.add_argument("--custom-mode", action="store_true")
    p.add_argument("--extend", metavar="AUDIO_URL",
                   help="upload+extend an existing audio URL")
    p.add_argument("--out", default="./out")
    p.add_argument("--callback-url")
    p.add_argument("--callback-port", type=int, default=8787)
    p.add_argument("--no-wait", action="store_true")
    p.add_argument("--timeout", type=int, default=900)
    return p.parse_args(argv)


def on_progress(state: str, data: dict) -> None:
    print(f"  [state={state}]", file=sys.stderr)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        client = KieClient()
    except KieError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    endpoint, payload = build_payload(args)
    print(f"creating Suno task (model={args.model}, endpoint={endpoint})...", file=sys.stderr)
    try:
        task_id = client.create_task(endpoint, payload, callback_url=args.callback_url)
    except KieError as e:
        print(f"create_task failed: {e}", file=sys.stderr)
        return 1
    print(f"taskId={task_id}", file=sys.stderr)

    if args.no_wait and args.callback_url:
        print(json.dumps({"taskId": task_id, "mode": "fire-and-forget"}))
        return 0

    try:
        if args.callback_url:
            print(
                f"waiting for webhook on 127.0.0.1:{args.callback_port}...", file=sys.stderr
            )
            body = client.wait_for_webhook(
                args.callback_port,
                timeout=args.timeout,
                expected_task_id=task_id,
            )
            data = body.get("data") or body
        else:
            data = client.poll_task(
                task_id,
                endpoint=POLL_ENDPOINT,
                timeout=args.timeout,
                on_progress=on_progress,
            )
    except KieTaskFailed as e:
        print(f"task failed: {e}", file=sys.stderr)
        return 1
    except KieTimeout as e:
        print(f"timeout: {e}", file=sys.stderr)
        return 1
    except KieError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    entries = extract_audio_entries(data if isinstance(data, dict) else {})
    if not entries:
        print("no audio URLs in response. raw payload:", file=sys.stderr)
        print(json.dumps(data, indent=2), file=sys.stderr)
        return 1

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    saved: list[dict] = []
    for i, entry in enumerate(entries, 1):
        url = entry["audioUrl"]
        ext = Path(url.split("?")[0]).suffix or ".mp3"
        audio_path = out_dir / f"{task_id}_{i}{ext}"
        print(f"downloading {url} -> {audio_path}", file=sys.stderr)
        client.download(url, audio_path)
        row = {"audio": str(audio_path), "duration": entry.get("duration")}
        cover = entry.get("coverImageUrl")
        if cover:
            cover_ext = Path(cover.split("?")[0]).suffix or ".jpg"
            cover_path = out_dir / f"{task_id}_{i}_cover{cover_ext}"
            try:
                client.download(cover, cover_path)
                row["cover"] = str(cover_path)
            except Exception as e:
                print(f"warning: cover download failed: {e}", file=sys.stderr)
        saved.append(row)

    print(json.dumps({"taskId": task_id, "tracks": saved}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
