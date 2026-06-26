from __future__ import annotations

import argparse
import sys

from bootstrap import ensure_uv_runtime

ensure_uv_runtime(__file__)

from common import GoAIClient, GoAIError, derive_video_defaults, print_error


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate GoAI videos with optional input images."
    )
    parser.add_argument("--prompt", required=True, help="Required video prompt.")
    parser.add_argument("--model", default="", help="Optional model id.")
    parser.add_argument("--aspect-ratio", default="", help="Optional aspect ratio.")
    parser.add_argument("--duration", type=int, default=None, help="Optional duration in seconds.")
    parser.add_argument("--resolution", default="", help="Optional resolution.")
    parser.add_argument(
        "--video-mode",
        choices=["frames", "subject"],
        default="frames",
        help="Optional video mode: frames or subject.",
    )
    parser.add_argument(
        "--image",
        action="append",
        default=[],
        help="Optional local image path or remote URL. May be repeated.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    client = GoAIClient(skill_name="goai-video-gen")

    try:
        client.require_api_key()

        model = args.model or client.get_default_model("video", mode=args.video_mode)
        aspect_ratio = args.aspect_ratio
        duration = args.duration
        resolution = args.resolution

        if not aspect_ratio or duration is None or not resolution:
            capability = client.get_model_capability(model)
            if capability is None:
                raise GoAIError(f"model capability missing: {model}")
            default_aspect_ratio, default_duration, default_resolution = derive_video_defaults(capability)
            if not aspect_ratio:
                aspect_ratio = default_aspect_ratio
            if duration is None:
                duration = default_duration
            if not resolution:
                resolution = default_resolution

        images = client.resolve_image_inputs(args.image)
        payload: dict[str, object] = {
            "model": model,
            "prompt": args.prompt,
        }
        if aspect_ratio:
            payload["aspect_ratio"] = aspect_ratio
        if duration is not None:
            payload["duration"] = duration
        if resolution:
            payload["resolution"] = resolution
        if args.video_mode:
            payload["video_mode"] = args.video_mode
        if images:
            payload["images"] = images

        response = client.json_request(
            "POST",
            f"{client.base_url}/api/v2/videos/generate",
            "auth",
            body=payload,
        )
        client.api_assert_ok(response)

        data = response.get("data")
        task_id = str(data.get("task_id") or "") if isinstance(data, dict) else ""
        if not task_id:
            raise GoAIError("task_id missing in generate response")

        media_url = client.poll_task(
            f"{client.base_url}/api/v2/videos/tasks/{task_id}",
            "video_url",
            interval_seconds=3,
            max_attempts=0,
            timeout_message="video generation timed out",
        )
        output_path = client.download_media(media_url, f"goai-video-{task_id}.mp4")

        print(f"MEDIA:{output_path}")
        print(f"MEDIA_URL:{media_url}")
        print(f"RESULT_PATH:{output_path}")
        print(f"RESULT_URL:{media_url}")
        return 0
    except GoAIError as exc:
        print_error(str(exc))
        return 1
    finally:
        client.close()


if __name__ == "__main__":
    sys.exit(main())
