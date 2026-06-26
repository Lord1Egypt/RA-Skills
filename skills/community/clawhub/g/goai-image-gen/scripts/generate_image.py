from __future__ import annotations

import argparse
import sys

from bootstrap import ensure_uv_runtime

ensure_uv_runtime(__file__)

from common import GoAIClient, GoAIError, print_error


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate GoAI images with optional reference images."
    )
    parser.add_argument("--prompt", required=True, help="Required image prompt.")
    parser.add_argument("--model", default="", help="Optional model id.")
    parser.add_argument("--aspect-ratio", default="", help="Optional aspect ratio.")
    parser.add_argument("--resolution", default="", help="Optional resolution.")
    parser.add_argument(
        "--reference",
        action="append",
        default=[],
        help="Optional local image path or remote URL. May be repeated.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    client = GoAIClient(skill_name="goai-image-gen")

    try:
        client.require_api_key()

        model = args.model or client.get_default_model("image")
        reference_images = client.resolve_image_inputs(args.reference)

        payload: dict[str, object] = {
            "model": model,
            "prompt": args.prompt,
        }
        if args.aspect_ratio:
            payload["aspect_ratio"] = args.aspect_ratio
        if args.resolution:
            payload["resolution"] = args.resolution
        if reference_images:
            payload["reference_images"] = reference_images

        response = client.json_request(
            "POST",
            f"{client.base_url}/api/v2/images/generate",
            "auth",
            body=payload,
        )
        client.api_assert_ok(response)

        data = response.get("data")
        task_id = str(data.get("task_id") or "") if isinstance(data, dict) else ""
        if not task_id:
            raise GoAIError("task_id missing in generate response")

        media_url = client.poll_task(
            f"{client.base_url}/api/v2/images/tasks/{task_id}",
            "image_url",
            interval_seconds=3,
            max_attempts=0,
            timeout_message="image generation timed out",
        )
        output_path = client.download_media(media_url, f"goai-image-{task_id}.png")

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
