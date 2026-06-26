#!/usr/bin/env python3
import argparse
import base64
import json
import os
from pathlib import Path

import requests

API_URL = "https://api.minimaxi.com/v1/image_generation"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate image with MiniMax image API")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", default="image-01")
    parser.add_argument("--aspect-ratio", default="1:1")
    parser.add_argument("--image-file", default=None)
    parser.add_argument("--n", type=int, default=1)
    args = parser.parse_args()

    api_key = os.environ.get("MINIMAX_API_KEY")
    if not api_key:
        raise SystemExit("MINIMAX_API_KEY is required")

    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "aspect_ratio": args.aspect_ratio,
        "n": args.n,
        "response_format": "base64",
    }
    if args.image_file:
        payload["image_file"] = args.image_file

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    images = data.get("data", {}).get("image_base64") or []
    if not images:
        raise SystemExit(f"No image returned: {json.dumps(data, ensure_ascii=False)}")

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    for index, image_base64 in enumerate(images):
        (output_dir / f"output-{index}.jpeg").write_bytes(base64.b64decode(image_base64))
    print(str(output_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
