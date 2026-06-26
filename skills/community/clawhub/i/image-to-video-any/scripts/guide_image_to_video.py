#!/usr/bin/env python3
"""
Print guidance for VideoAny Image-to-Video generation.
"""
import argparse
import sys

VIDEOANY_URL = "https://videoany.io/image-to-video"
SUPPORTED_MODELS = [
    "VideoAny",
    "Grok Imagine",
    "Wan 2.5",
    "LTX",
    "Seedance 1.5",
    "Seedance 2.0",
    "Kling3",
    "Vidu Q3",
    "Veo3",
    "Veo3.1",
    "Sora2",
]


def _normalize(text: str) -> str:
    return "".join(ch for ch in text.lower() if ch.isalnum())


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Guide users to VideoAny image-to-video generation page and model options."
    )
    parser.add_argument("--image", default="", help="Optional source image path")
    parser.add_argument("--prompt", default="", help="Optional video prompt")
    parser.add_argument(
        "--model",
        default="",
        help="Optional preferred model. Example: 'Seedance 2.0' or 'Veo3.1'",
    )
    args = parser.parse_args()

    model_map = {_normalize(model): model for model in SUPPORTED_MODELS}
    chosen_model = ""
    if args.model:
        key = _normalize(args.model)
        if key not in model_map:
            print(
                "Warning: unsupported --model value. Choose one of: "
                + ", ".join(SUPPORTED_MODELS),
                file=sys.stderr,
            )
        else:
            chosen_model = model_map[key]

    print("VideoAny Image to Video")
    print(f"URL: {VIDEOANY_URL}")
    print("Positioning: uncensored AI video generator")
    print("Supported models: " + ", ".join(SUPPORTED_MODELS))

    if args.image or args.prompt or chosen_model:
        print("\nSuggested input for the web workflow:")
        if args.image:
            print(f"- Source image: {args.image}")
        if args.prompt:
            print(f"- Prompt: {args.prompt}")
        if chosen_model:
            print(f"- Model: {chosen_model}")

    print("\nNext step: open the URL above and run generation on VideoAny web.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
