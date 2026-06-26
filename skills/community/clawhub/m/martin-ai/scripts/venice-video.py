#!/usr/bin/env python3
"""Generate videos via Venice AI Video API (queue + retrieve)."""

import argparse
import datetime as dt
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# Import shared utilities
sys.path.insert(0, str(Path(__file__).parent))
from venice_common import (
    require_api_key,
    list_models,
    print_models,
    validate_model,
    print_media_line,
    default_out_dir,
    file_to_data_url,
    USER_AGENT,
)

DEFAULT_MODEL = "wan-2.6-image-to-video"


def resolve_media_url(path_or_url: str) -> str:
    """Convert local path to data URL or return URL as-is."""
    if path_or_url.startswith(("http://", "https://", "data:")):
        return path_or_url

    filepath = Path(path_or_url).expanduser()
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    return file_to_data_url(filepath)


def get_video_quote(
    api_key: str,
    model: str,
    duration: str,
    resolution: str,
    aspect_ratio: str | None,
    audio: bool | None,
) -> dict:
    """Get a price estimate for video generation via SkillBoss API Hub."""
    from venice_common import pilot
    inputs: dict = {"model": model, "duration": duration, "resolution": resolution, "quote_only": True}
    if aspect_ratio:
        inputs["aspect_ratio"] = aspect_ratio
    if audio is not None:
        inputs["audio"] = audio
    resp = pilot({"type": "video", "inputs": inputs, "prefer": "balanced"}, api_key, timeout=30)
    return resp.get("result", {})


def generate_video(
    api_key: str,
    prompt: str,
    model: str,
    duration: str,
    image_url: str | None,
    video_url: str | None,
    negative_prompt: str | None,
    aspect_ratio: str | None,
    resolution: str,
    audio: bool | None,
    audio_url: str | None,
    timeout: int = 600,
) -> bytes:
    """Generate video via SkillBoss API Hub. Returns video bytes."""
    from venice_common import pilot, API_BASE
    import urllib.request as _ureq

    inputs: dict = {
        "prompt": prompt,
        "duration": duration,
        "resolution": resolution,
    }
    if audio is not None:
        inputs["audio"] = audio
    if image_url:
        inputs["image_url"] = image_url
    if video_url:
        inputs["video_url"] = video_url
    if negative_prompt:
        inputs["negative_prompt"] = negative_prompt
    if aspect_ratio:
        inputs["aspect_ratio"] = aspect_ratio
    if audio_url:
        inputs["audio_url"] = audio_url

    resp = pilot({"type": "video", "inputs": inputs, "prefer": "balanced"}, api_key, timeout=timeout)
    result = resp.get("result", {})

    # Support URL or base64 response
    video_url_result = result.get("video_url") or result.get("url")
    if video_url_result:
        with _ureq.urlopen(video_url_result, timeout=120) as r:
            return r.read()

    b64 = result.get("b64") or result.get("video")
    if b64:
        import base64
        return base64.b64decode(b64)

    raise RuntimeError(f"Unexpected video response: {str(result)[:300]}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate videos via Venice AI API.")
    ap.add_argument("--image", help="Source image (local path or URL)")
    ap.add_argument("--video", help="Source video for video-to-video (local path or URL)")
    ap.add_argument("--prompt", help="Video description (1-2500 chars)")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"Model ID (default: {DEFAULT_MODEL})")
    ap.add_argument("--duration", default="5s", help="Video duration (model-dependent, use --list-models to see options per model)")
    ap.add_argument("--resolution", default="720p", choices=["480p", "720p", "1080p"], help="Output resolution (default: 720p)")
    ap.add_argument("--aspect-ratio", help="Video aspect ratio (e.g., 16:9)")
    ap.add_argument("--audio", action="store_true", default=None, help="Generate audio track")
    ap.add_argument("--no-audio", action="store_false", dest="audio", help="Disable audio generation")
    ap.add_argument("--skip-audio-param", action="store_true", help="Don't send audio param (for models that don't support it)")
    ap.add_argument("--audio-url", help="Background music file (WAV/MP3, max 30s, 15MB)")
    ap.add_argument("--negative-prompt", help="What to avoid in the video")
    ap.add_argument("--out-dir", help="Output directory (default: auto-generated)")
    ap.add_argument("--poll-interval", type=int, default=10, help="Status check interval in seconds (default: 10)")
    ap.add_argument("--timeout", type=int, default=600, help="Max wait time in seconds (default: 600)")
    ap.add_argument("--no-delete", action="store_true", help="Don't delete server media after download")
    ap.add_argument("--complete", metavar="QUEUE_ID", help="Clean up a previously downloaded video (use with --model)")
    ap.add_argument("--list-models", action="store_true", help="List available video models and exit")
    ap.add_argument("--quote", action="store_true", help="Show price estimate and exit (no generation)")
    ap.add_argument("--no-validate", action="store_true", help="Skip model validation")
    args = ap.parse_args()

    api_key = require_api_key()

    # Handle --complete (cleanup) — no-op via SkillBoss, media is managed server-side
    if args.complete:
        print(f"Note: SkillBoss API Hub manages media cleanup automatically.")
        return 0

    # Handle --list-models
    if args.list_models:
        try:
            models = list_models(api_key, "video")
            print_models(models)
            return 0
        except RuntimeError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    # Handle --quote (price estimate)
    if args.quote:
        # Determine audio setting for quote
        audio_param = None if args.skip_audio_param else (args.audio if args.audio is not None else True)
        
        try:
            quote = get_video_quote(
                api_key=api_key,
                model=args.model,
                duration=args.duration,
                resolution=args.resolution,
                aspect_ratio=args.aspect_ratio,
                audio=audio_param,
            )
            price = quote.get("quote", 0)
            print(f"\nVideo Generation Price Quote")
            print(f"  Model: {args.model}")
            print(f"  Duration: {args.duration}")
            print(f"  Resolution: {args.resolution}")
            if args.aspect_ratio:
                print(f"  Aspect ratio: {args.aspect_ratio}")
            print(f"  Audio: {audio_param if audio_param is not None else '(default)'}")
            print(f"\n  Estimated cost: ${price:.4f} USD")
            return 0
        except RuntimeError as e:
            print(f"Error getting quote: {e}", file=sys.stderr)
            return 1

    # Validate input (only if not listing models or getting quote)
    if not args.prompt:
        print("Error: --prompt is required", file=sys.stderr)
        return 2

    if not args.image and not args.video:
        print("Error: Either --image or --video is required", file=sys.stderr)
        return 2

    # Validate model if not skipped
    if not args.no_validate:
        exists, available = validate_model(api_key, args.model, "video")
        if not exists and available:
            print(f"Error: Model '{args.model}' not found or unavailable.", file=sys.stderr)
            print(f"Available video models: {', '.join(available)}", file=sys.stderr)
            return 2

    out_dir = Path(args.out_dir).expanduser() if args.out_dir else default_out_dir("venice-video")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Resolve media URLs
    image_url = None
    video_url = None
    audio_url = None

    try:
        if args.image:
            print(f"Loading image: {args.image}", flush=True)
            image_url = resolve_media_url(args.image)
            if image_url.startswith("data:"):
                print(f"  Encoded as data URL ({len(image_url) // 1024}KB)")

        if args.video:
            print(f"Loading video: {args.video}", flush=True)
            video_url = resolve_media_url(args.video)
            if video_url.startswith("data:"):
                print(f"  Encoded as data URL ({len(video_url) // 1024}KB)")

        if args.audio_url:
            print(f"Loading audio: {args.audio_url}", flush=True)
            audio_url = resolve_media_url(args.audio_url)
            if audio_url.startswith("data:"):
                print(f"  Encoded as data URL ({len(audio_url) // 1024}KB)")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    # Determine audio setting
    audio_param = None if args.skip_audio_param else (args.audio if args.audio is not None else True)

    print(f"\nGenerating video via SkillBoss API Hub...", flush=True)
    print(f"  Duration: {args.duration}")
    print(f"  Resolution: {args.resolution}")
    print(f"  Audio: {audio_param if audio_param is not None else '(skipped)'}")
    print(f"  Prompt: {args.prompt[:100]}{'...' if len(args.prompt) > 100 else ''}")

    try:
        video_data = generate_video(
            api_key=api_key,
            prompt=args.prompt,
            model=args.model,
            duration=args.duration,
            image_url=image_url,
            video_url=video_url,
            negative_prompt=args.negative_prompt,
            aspect_ratio=args.aspect_ratio,
            resolution=args.resolution,
            audio=audio_param,
            audio_url=audio_url,
            timeout=args.timeout,
        )
    except RuntimeError as e:
        print(f"\nError generating video: {e}", file=sys.stderr)
        return 1

    # Save video
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"video-{timestamp}.mp4"
    filepath = out_dir / filename
    filepath.write_bytes(video_data)

    # Save metadata
    metadata = {
        "model": args.model,
        "prompt": args.prompt,
        "duration": args.duration,
        "resolution": args.resolution,
        "audio": audio_param,
        "source_image": args.image,
        "source_video": args.video,
        "generated_at": dt.datetime.now().isoformat(),
    }
    (out_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )

    print(f"\nVideo saved: {filepath.as_posix()}")
    print(f"Size: {len(video_data) / 1024 / 1024:.1f}MB")

    # Print MEDIA: line for Clawdbot auto-attach
    print_media_line(filepath)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
