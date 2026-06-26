#!/usr/bin/env python3
import argparse
import base64
import json
import mimetypes
from pathlib import Path

from skill_paths import SHARE_CARD_SCHEMA_PATH, require_live_input
from validate_json import load_json, validate


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def file_to_data_url(path: Path) -> str:
    mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def attach_image(
    share_card: dict,
    image_url: str | None = None,
    image_data_url: str | None = None,
    image_prompt: str | None = None,
) -> dict:
    updated = dict(share_card)
    image_payload = {}
    if image_url:
      image_payload["url"] = image_url
    if image_data_url:
      image_payload["data_url"] = image_data_url
    if not image_payload:
      raise SystemExit("[FAIL] Provide either --image-url or --image-data-url")

    updated["image"] = image_payload
    updated["image_strategy"] = "provided-image"
    if image_prompt:
      updated["selfie_prompt"] = image_prompt
      if isinstance(updated.get("i18n"), dict):
        if isinstance(updated["i18n"].get("en"), dict):
          updated["i18n"]["en"]["selfie_prompt"] = image_prompt
    return updated


def main():
    parser = argparse.ArgumentParser(description="Attach a generated image back into a share-card payload")
    parser.add_argument("share_card_json", help="Path to share-card JSON")
    parser.add_argument("--image-url", help="Generated image URL")
    parser.add_argument("--image-data-url", help="Generated image data URL")
    parser.add_argument("--image-file", help="Local image file to inline as a data URL")
    parser.add_argument("--prompt-file", help="Optional prompt text file to preserve in the payload")
    parser.add_argument("--out", help="Output JSON path; defaults to overwriting input")
    args = parser.parse_args()

    share_card_path = Path(args.share_card_json)
    require_live_input(share_card_path, "share_card_json")
    share_card = load_json(share_card_path)
    prompt_text = load_text(Path(args.prompt_file)) if args.prompt_file else None
    inline_data_url = file_to_data_url(Path(args.image_file)) if args.image_file else None

    updated = attach_image(
        share_card,
        image_url=args.image_url,
        image_data_url=args.image_data_url or inline_data_url,
        image_prompt=prompt_text,
    )
    validate(updated, load_json(SHARE_CARD_SCHEMA_PATH))

    out_path = Path(args.out) if args.out else share_card_path
    out_path.write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[OK] Wrote image-attached share card to {out_path}")


if __name__ == "__main__":
    main()
