#!/usr/bin/env python3
"""
Science-backed memorable image generation using Google Gemini + ResMem memorability scoring.

Memorability scoring powered by ResMem
Brain Bridge Lab, University of Chicago
© 2021 The University of Chicago. Non-commercial use license.
https://github.com/Brain-Bridge-Lab/resmem
For commercial licensing: wilma@uchicago.edu
"""

import argparse
import base64
import json
import os
import sys
import tempfile
from pathlib import Path

import requests


def load_api_key(cli_key: str | None) -> str:
    if cli_key:
        return cli_key
    env_key = os.environ.get("GEMINI_API_KEY")
    if env_key:
        return env_key
    config_path = Path.home() / ".config" / "gemini" / "api_key"
    if config_path.exists():
        return config_path.read_text().strip()
    print(
        "Error: Gemini API key not found.\n"
        "Provide it via --api-key, the GEMINI_API_KEY environment variable,\n"
        "or by writing it to ~/.config/gemini/api_key",
        file=sys.stderr,
    )
    sys.exit(1)


def generate_image(prompt: str, api_key: str) -> bytes | None:
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.0-flash-exp:generateContent?key={api_key}"
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }
    response = requests.post(url, json=payload, timeout=60)
    if response.status_code != 200:
        print(
            f"Gemini API error {response.status_code}: {response.text}",
            file=sys.stderr,
        )
        return None
    data = response.json()
    try:
        parts = data["candidates"][0]["content"]["parts"]
        for part in parts:
            if "inlineData" in part:
                return base64.b64decode(part["inlineData"]["data"])
    except (KeyError, IndexError):
        pass
    return None


def score_memorability(image_path: str) -> float:
    try:
        from PIL import Image
        from resmem import ResMem, transformer
        import torch
    except ImportError as e:
        print(
            f"Import error: {e}\n"
            "Install required packages with:\n"
            "  pip install resmem torch torchvision pillow requests",
            file=sys.stderr,
        )
        sys.exit(1)

    model = ResMem(pretrained=True)
    model.eval()
    img = Image.open(image_path).convert("RGB")
    image_x = transformer(img)
    with torch.no_grad():
        score = model(image_x.view(-1, 3, 227, 227)).item()
    return score


def vary_prompt(base_prompt: str, attempt: int) -> str:
    suffixes = {
        2: ", striking composition",
        3: ", vivid colors, memorable focal point",
    }
    return base_prompt + suffixes.get(attempt, "")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a memorable image using Gemini + ResMem scoring."
    )
    parser.add_argument("--prompt", required=True, help="Image description")
    parser.add_argument("--output", default="memorable-image.png", help="Output file path")
    parser.add_argument(
        "--threshold", type=float, default=0.7, help="Memorability threshold (0–1)"
    )
    parser.add_argument("--max-attempts", type=int, default=3, help="Max regeneration attempts")
    parser.add_argument("--api-key", help="Gemini API key")
    parser.add_argument("--verbose", action="store_true", help="Show memorability scores per attempt")
    args = parser.parse_args()

    api_key = load_api_key(args.api_key)
    best_score = 0.0
    best_image: bytes | None = None

    for attempt in range(1, args.max_attempts + 1):
        prompt = vary_prompt(args.prompt, attempt)
        if args.verbose and attempt > 1:
            print(f"Attempt {attempt}/{args.max_attempts}: prompt augmented → \"{prompt}\"")
        elif args.verbose:
            print(f"Attempt {attempt}/{args.max_attempts}: generating image...")

        image_bytes = generate_image(prompt, api_key)
        if image_bytes is None:
            print(f"Warning: no image returned on attempt {attempt}, retrying...")
            continue

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp.write(image_bytes)
            tmp_path = tmp.name

        try:
            score = score_memorability(tmp_path)
        finally:
            os.unlink(tmp_path)

        if args.verbose:
            print(f"  Memorability score: {score:.3f} (threshold: {args.threshold})")

        if score > best_score:
            best_score = score
            best_image = image_bytes

        if score >= args.threshold or attempt == args.max_attempts:
            break

        print(
            f"Score {score:.3f} below threshold {args.threshold}, "
            f"regenerating... (attempt {attempt}/{args.max_attempts})"
        )

    if best_image is None:
        print("Error: failed to generate any image.", file=sys.stderr)
        sys.exit(1)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_bytes(best_image)
    print(f"✓ Saved to {args.output} (memorability score: {best_score:.3f})")


if __name__ == "__main__":
    main()
