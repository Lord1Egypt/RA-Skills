#!/usr/bin/env python3
"""
Print guidance for VideoAny Lip Sync workflow.
"""
import argparse
import sys

VIDEOANY_URL = "https://videoany.io/lip-sync"
IMAGE_FORMATS = ["jpg", "png", "webp"]
AUDIO_FORMATS = ["mp3", "wav", "m4a"]
MODEL_OPTIONS = {
    "aurora": "Creatify Aurora",
    "fabric": "VEED Fabric 1.0",
    "omnihuman": "ByteDance OmniHuman v1.5",
}
RESOLUTION_OPTIONS = {"480p", "720p"}


def _normalize(text: str) -> str:
    return "".join(ch for ch in text.lower() if ch.isalnum())


def _resolve_model(model: str) -> str:
    if not model:
        return MODEL_OPTIONS["aurora"]
    key = _normalize(model)
    for short, full in MODEL_OPTIONS.items():
        if key in {_normalize(short), _normalize(full)}:
            return full
    print(
        "Warning: unsupported --model value. Choose one of: "
        + ", ".join(MODEL_OPTIONS.keys()),
        file=sys.stderr,
    )
    return MODEL_OPTIONS["aurora"]


def _resolve_resolution(value: str) -> str:
    if not value:
        return "720p"
    normalized = value.lower()
    if normalized in RESOLUTION_OPTIONS:
        return normalized
    print(
        "Warning: unsupported --resolution value. Choose one of: "
        + ", ".join(sorted(RESOLUTION_OPTIONS)),
        file=sys.stderr,
    )
    return "720p"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Guide users to VideoAny Lip Sync Studio and recommended inputs."
    )
    parser.add_argument("--image", default="", help="Optional local portrait image path")
    parser.add_argument("--image-url", default="", help="Optional direct image URL")
    parser.add_argument("--audio", default="", help="Optional local audio path")
    parser.add_argument("--audio-url", default="", help="Optional direct audio URL")
    parser.add_argument(
        "--model",
        default="aurora",
        help="Model: aurora, fabric, omnihuman",
    )
    parser.add_argument(
        "--resolution",
        default="720p",
        help="Resolution: 480p or 720p",
    )
    parser.add_argument(
        "--prompt",
        default="",
        help="Optional prompt. Not required for fabric model.",
    )
    args = parser.parse_args()

    selected_model = _resolve_model(args.model)
    selected_resolution = _resolve_resolution(args.resolution)

    print("VideoAny Lip Sync Studio")
    print(f"URL: {VIDEOANY_URL}")
    print("Summary: Create a lip-sync video from a portrait image and audio.")
    print("Models: " + ", ".join(MODEL_OPTIONS.values()))
    print("Resolutions: 480p, 720p")
    print("Image input: upload or URL (" + "/".join(IMAGE_FORMATS) + ")")
    print("Audio input: upload or URL (" + "/".join(AUDIO_FORMATS) + ")")
    print("Credits: based on audio duration and selected model/resolution")
    print("Selected model: " + selected_model)
    print("Selected resolution: " + selected_resolution)

    if "Fabric" in selected_model:
        print("Prompt note: Fabric model does not require a prompt.")
    else:
        print("Prompt note: Aurora/OmniHuman can use prompts to guide style and framing.")

    if args.image or args.image_url or args.audio or args.audio_url or args.prompt:
        print("\nSuggested input for the web workflow:")
        if args.image:
            print(f"- Image file: {args.image}")
        if args.image_url:
            print(f"- Image URL: {args.image_url}")
        if args.audio:
            print(f"- Audio file: {args.audio}")
        if args.audio_url:
            print(f"- Audio URL: {args.audio_url}")
        if args.prompt:
            print(f"- Prompt: {args.prompt}")
    else:
        print("\nSuggested workflow:")
        print("- Use a clear portrait with a visible mouth")
        print("- Use clean speech with low background noise")
        print("- Start with a short clip before longer generations")
        print("- Try multiple models/resolutions if sync quality is not ideal")

    print("\nResponsible use reminders:")
    print("- Use only content you own or are authorized to use")
    print("- Do not mislead viewers through deceptive impersonation")
    print("- Respect privacy, consent, and applicable laws/platform policy")

    print("\nNext step: open the URL above and run generation on VideoAny web.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
