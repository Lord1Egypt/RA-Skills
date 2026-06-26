from __future__ import annotations

import argparse
import sys
import subprocess
import platform

from bootstrap import ensure_uv_runtime

ensure_uv_runtime(__file__)

from common import GoAIClient, GoAIError, print_error

DEMO_PPT_URL = "https://ai-neuralforge.oss-cn-hangzhou.aliyuncs.com/aippt/ppt/example_ppt/demo.pptx"
EXIT_INSUFFICIENT_CREDITS = 42


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert images to a PowerPoint presentation via GoAI API."
    )
    parser.add_argument(
        "--image",
        action="append",
        default=[],
        required=True,
        help="Required image file path or URL. May be repeated.",
    )
    parser.add_argument(
        "--language",
        default="zh",
        help="Optional language (default: zh).",
    )
    parser.add_argument(
        "--aspect-ratio",
        default="16:9",
        help="Optional aspect ratio (default: 16:9).",
    )
    return parser


def open_local_ppt(path: str) -> None:
    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.run(["open", path], check=True, capture_output=True)
        elif system == "Linux":
            subprocess.run(["xdg-open", path], check=True, capture_output=True)
        elif system == "Windows":
            subprocess.run(["start", "", path], check=True, shell=True, capture_output=True)
    except subprocess.CalledProcessError:
        pass


def main() -> int:
    args = build_parser().parse_args()
    client = GoAIClient(skill_name="goai-image-to-ppt")

    try:
        client.require_api_key()

        image_urls = client.resolve_image_inputs(args.image)

        payload: dict[str, object] = {
            "imageUrls": image_urls,
            "language": args.language,
            "aspectRatio": args.aspect_ratio,
        }

        response = client.json_request(
            "POST",
            f"{client.base_url}/api/v2/convert/images-to-ppt",
            "auth",
            body=payload,
        )
        client.api_assert_ok(response)

        data = response.get("data")
        job_id = str(data.get("jobId") or "") if isinstance(data, dict) else ""
        if not job_id:
            raise GoAIError("jobId missing in convert response")

        download_url = client.poll_task(
            f"{client.base_url}/api/v2/convert/images-to-ppt/{job_id}",
            "downloadUrl",
            interval_seconds=5,
            max_attempts=120,
            timeout_message="Images to PPT conversion timed out",
        )

        output_path = client.download_media(download_url, f"goai-images-{job_id}.pptx")
        open_local_ppt(output_path)

        print(f"MEDIA:{output_path}")
        print(f"MEDIA_URL:{download_url}")
        print(f"RESULT_PATH:{output_path}")
        print(f"RESULT_URL:{download_url}")
        return 0
    except GoAIError as exc:
        msg = str(exc).lower()
        if "insufficient credits" in msg or "积分不足" in msg:
            print(f"\n我们导出的PPT效果如下：{DEMO_PPT_URL}\n")
            print(f"RESULT_URL:{DEMO_PPT_URL}")
            return EXIT_INSUFFICIENT_CREDITS
        print_error(str(exc))
        return 1
    finally:
        client.close()


if __name__ == "__main__":
    sys.exit(main())
