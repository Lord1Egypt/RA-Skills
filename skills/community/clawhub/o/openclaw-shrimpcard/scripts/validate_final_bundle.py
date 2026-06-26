#!/usr/bin/env python3
import argparse
import base64
import binascii
import struct
from pathlib import Path

from skill_paths import SHARE_CARD_SCHEMA_PATH, require_live_input
from validate_json import fail, load_json, validate

MIN_IMAGE_WIDTH = 64
MIN_IMAGE_HEIGHT = 64


def png_dimensions_from_bytes(data: bytes) -> tuple[int, int] | None:
    signature = b"\x89PNG\r\n\x1a\n"
    if len(data) < 24 or not data.startswith(signature):
        return None
    return struct.unpack(">II", data[16:24])


def decode_data_url(data_url: str) -> tuple[str, bytes]:
    if not data_url.startswith("data:") or "," not in data_url:
        fail("image.data_url: invalid data URL")
    header, encoded = data_url.split(",", 1)
    if ";base64" not in header:
        fail("image.data_url: only base64 data URLs are supported")
    mime = header[5:].split(";", 1)[0] or "application/octet-stream"
    try:
        raw = base64.b64decode(encoded, validate=True)
    except binascii.Error as exc:
        fail(f"image.data_url: invalid base64 payload ({exc})")
    return mime, raw


def validate_image_dimensions(width: int, height: int, source: str):
    if width < MIN_IMAGE_WIDTH or height < MIN_IMAGE_HEIGHT:
        fail(
            f"{source}: image is too small for a final card "
            f"({width}x{height} < {MIN_IMAGE_WIDTH}x{MIN_IMAGE_HEIGHT})"
        )


def validate_embedded_image(image: dict):
    image_data_url = image.get("data_url")
    if not image_data_url:
        return
    mime, raw = decode_data_url(image_data_url)
    if mime != "image/png":
        fail(f"image.data_url: expected PNG for final 8-bit card image, got {mime}")
    dimensions = png_dimensions_from_bytes(raw)
    if dimensions is None:
        fail("image.data_url: could not read PNG dimensions")
    validate_image_dimensions(dimensions[0], dimensions[1], "image.data_url")


def validate_final_bundle(card: dict, base_dir: Path | None = None):
    validate(card, load_json(SHARE_CARD_SCHEMA_PATH))

    image = card.get("image")
    if not isinstance(image, dict):
        fail("image: final bundle must include an image object")

    image_url = image.get("url")
    image_data_url = image.get("data_url")
    if not (image_url or image_data_url):
        fail("image: final bundle must include either image.url or image.data_url")

    if isinstance(image_url, str) and image_url and not image_url.startswith(("http://", "https://", "data:")):
        candidates = [Path(image_url)]
        if base_dir is not None and not Path(image_url).is_absolute():
            candidates.append(base_dir / image_url)
        existing = next((path for path in candidates if path.exists()), None)
        if existing is None:
            fail(f"image.url: local file does not exist: {image_url}")
        if existing.suffix.lower() == ".png":
            dimensions = png_dimensions_from_bytes(existing.read_bytes())
            if dimensions is None:
                fail(f"image.url: could not read PNG dimensions: {image_url}")
            validate_image_dimensions(dimensions[0], dimensions[1], "image.url")

    validate_embedded_image(image)

    prompt = str(card.get("selfie_prompt", "")).strip().lower()
    if "8-bit" not in prompt and "pixel art" not in prompt and "像素风" not in str(card.get("selfie_prompt", "")):
        fail("selfie_prompt: final bundle must keep explicit 8-bit / pixel-art direction")


def main():
    parser = argparse.ArgumentParser(description="Validate the final share-card bundle, including required image attachment")
    parser.add_argument("share_card_json", help="Path to share-card JSON")
    args = parser.parse_args()

    share_card_path = Path(args.share_card_json)
    require_live_input(share_card_path, "share_card_json")
    payload = load_json(share_card_path)
    validate_final_bundle(payload, share_card_path.parent)
    print("[OK] Final bundle is valid")


if __name__ == "__main__":
    main()
