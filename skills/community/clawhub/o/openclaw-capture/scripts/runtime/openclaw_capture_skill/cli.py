"""CLI entrypoint for dispatching payloads through the wrapper."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .config import Settings
from .dispatcher import CaptureDispatcher


def _load_payload(args: argparse.Namespace) -> dict:
    if args.payload_json:
        return json.loads(args.payload_json)
    if args.payload_file == "-":
        return json.loads(sys.stdin.read())
    return json.loads(Path(args.payload_file).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Dispatch OpenClaw capture payloads through the wrapper runtime")
    parser.add_argument("--payload-file", default="-", help="JSON payload path or - for stdin")
    parser.add_argument("--payload-json", help="Inline JSON payload")
    args = parser.parse_args()

    payload = _load_payload(args)
    settings = Settings.from_env()
    dispatcher = CaptureDispatcher(settings)
    job = dispatcher.dispatch(payload)
    print(json.dumps(job, ensure_ascii=False, indent=2))
    return 1 if str(job.get("status")) == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())

