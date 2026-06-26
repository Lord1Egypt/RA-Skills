#!/usr/bin/env python3
"""Call Noiz voice-design API to generate a voice from an image and/or description.

Returns the best-matching voice_id and saves preview audio samples.
"""
import argparse
import base64
import binascii
import json
import sys
from pathlib import Path
from typing import Optional

import requests

NOIZ_KEY_FILE = Path.home() / ".noiz_api_key"
DEFAULT_BASE_URL = "https://noiz.ai/v1"


def normalize_api_key_base64(api_key: str) -> str:
    key = api_key.strip()
    if not key:
        return key
    padded = key + ("=" * (-len(key) % 4))
    try:
        decoded = base64.b64decode(padded, validate=True)
        canonical = base64.b64encode(decoded).decode("ascii").rstrip("=")
        if decoded and canonical == key.rstrip("="):
            return key
    except binascii.Error:
        pass
    return base64.b64encode(key.encode("utf-8")).decode("ascii")


def load_api_key() -> Optional[str]:
    import os

    env_key = os.environ.get("NOIZ_API_KEY", "")
    if env_key:
        return normalize_api_key_base64(env_key)
    if NOIZ_KEY_FILE.exists():
        raw = NOIZ_KEY_FILE.read_text(encoding="utf-8").strip()
        if raw:
            return normalize_api_key_base64(raw)
    return None


def voice_design(
    api_key: str,
    base_url: str,
    picture_path: Optional[str] = None,
    voice_description: Optional[str] = None,
    guidance_scale: float = 5,
    loudness: float = 0.5,
    timeout: int = 120,
) -> dict:
    if not picture_path and not voice_description:
        raise ValueError("At least one of --picture or --voice-description is required.")

    url = f"{base_url.rstrip('/')}/voice-design"
    data = {
        "guidance_scale": str(guidance_scale),
        "loudness": str(loudness),
    }
    if voice_description:
        data["voice_description"] = voice_description

    files = None
    if picture_path:
        p = Path(picture_path)
        if not p.exists():
            raise FileNotFoundError(f"Image not found: {picture_path}")
        files = {
            "picture": (p.name, p.open("rb"), "image/jpeg"),
        }

    try:
        resp = requests.post(
            url,
            headers={"Authorization": api_key},
            data=data,
            files=files,
            timeout=timeout,
        )
    finally:
        if files and files["picture"][1]:
            files["picture"][1].close()

    if resp.status_code != 200:
        raise RuntimeError(
            f"/voice-design failed: status={resp.status_code}, body={resp.text}"
        )

    result = resp.json()
    if result.get("code") != 0:
        raise RuntimeError(
            f"/voice-design returned error: code={result.get('code')}, "
            f"message={result.get('message')}"
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Design a voice from an image and/or text description via Noiz API."
    )
    parser.add_argument(
        "--picture", help="Path to an image file of the person"
    )
    parser.add_argument(
        "--voice-description",
        dest="voice_description",
        help="Text description of the desired voice (20-1000 chars)",
    )
    parser.add_argument("--api-key", help="Noiz API key (auto-loaded if not provided)")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument(
        "--guidance-scale",
        dest="guidance_scale",
        type=float,
        default=5,
        help="Guidance scale for voice generation (0-100, default 5)",
    )
    parser.add_argument(
        "--loudness",
        type=float,
        default=0.5,
        help="Loudness level (-1 to 1, default 0.5)",
    )
    parser.add_argument(
        "-o", "--output-dir",
        dest="output_dir",
        default=".",
        help="Directory to save preview audio files",
    )
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()

    api_key = args.api_key
    if not api_key:
        api_key = load_api_key()
    if not api_key:
        print(
            "Error: No API key. Set NOIZ_API_KEY or run:\n"
            "  python3 skills/tts/scripts/tts.py config --set-api-key YOUR_KEY",
            file=sys.stderr,
        )
        return 1
    api_key = normalize_api_key_base64(api_key)

    if not args.picture and not args.voice_description:
        parser.error("At least one of --picture or --voice-description is required.")

    try:
        result = voice_design(
            api_key=api_key,
            base_url=args.base_url,
            picture_path=args.picture,
            voice_description=args.voice_description,
            guidance_scale=args.guidance_scale,
            loudness=args.loudness,
            timeout=args.timeout,
        )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    data = result.get("data", {})
    previews = data.get("previews", [])
    features = data.get("features", {})

    if features:
        print("Voice features detected:")
        for k, v in features.items():
            print(f"  {k}: {v}")

    if not previews:
        print("Warning: No voice previews returned.", file=sys.stderr)
        return 1

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nReceived {len(previews)} voice preview(s):")
    for i, preview in enumerate(previews):
        voice_id = preview.get("voice_id", f"unknown_{i}")
        audio_b64 = preview.get("audio", "")
        print(f"  [{i}] voice_id: {voice_id}")

        if audio_b64:
            audio_bytes = base64.b64decode(audio_b64)
            out_file = out_dir / f"voice_preview_{i}_{voice_id}.wav"
            out_file.write_bytes(audio_bytes)
            print(f"      saved: {out_file}")

    best_voice_id = previews[0].get("voice_id", "")
    print(f"\nBest voice_id: {best_voice_id}")
    print(f"Display name: {features.get('display_name', 'N/A')}")

    voice_id_file = out_dir / "voice_id.txt"
    voice_id_file.write_text(best_voice_id, encoding="utf-8")
    print(f"Voice ID saved to: {voice_id_file}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
