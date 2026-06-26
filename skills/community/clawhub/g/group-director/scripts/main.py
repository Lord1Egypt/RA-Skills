#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys

from video_api import DEFAULT_INTERVAL, DEFAULT_TIMEOUT, SenseAudioVideoClient, VideoRequest


def cmd_video_create(args: argparse.Namespace) -> int:
    client = SenseAudioVideoClient()
    task_id = client.create_video(
        VideoRequest(final_video_prompt=args.final_video_prompt, orientation=args.orientation)
    )
    print(task_id)
    return 0


def cmd_video_status(args: argparse.Namespace) -> int:
    client = SenseAudioVideoClient()
    status_body = client.get_video_status(args.task_id)
    print(client.format_status_text(status_body))
    return 0


def cmd_video_poll(args: argparse.Namespace) -> int:
    client = SenseAudioVideoClient()
    video_url = client.poll_video_url(args.task_id, interval=args.interval, timeout=args.timeout)
    print(video_url)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Group Director video executor")
    sub = parser.add_subparsers(dest="command", required=True)

    create_p = sub.add_parser("video-create")
    create_p.add_argument("--final-video-prompt", required=True)
    create_p.add_argument("--orientation", choices=["portrait", "landscape"], default="portrait")
    create_p.set_defaults(func=cmd_video_create)

    status_p = sub.add_parser("video-status")
    status_p.add_argument("--task-id", required=True)
    status_p.set_defaults(func=cmd_video_status)

    poll_p = sub.add_parser("video-poll")
    poll_p.add_argument("--task-id", required=True)
    poll_p.add_argument("--interval", type=int, default=DEFAULT_INTERVAL)
    poll_p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    poll_p.set_defaults(func=cmd_video_poll)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        exit_code = args.func(args)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
