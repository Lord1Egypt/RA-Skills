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
        description="Generate a PowerPoint presentation from text/ideas via GoAI API."
    )
    parser.add_argument(
        "--idea",
        required=True,
        help="Required PPT idea/prompt.",
    )
    parser.add_argument(
        "--language",
        default="zh",
        help="Optional language (default: zh).",
    )
    parser.add_argument(
        "--num-pages",
        default="",
        help="Optional number of pages.",
    )
    parser.add_argument(
        "--reference",
        action="append",
        default=[],
        help="Optional reference image path or URL. May be repeated.",
    )
    parser.add_argument(
        "--reference-pdf",
        action="append",
        default=[],
        help="Optional reference PDF URL. May be repeated.",
    )
    parser.add_argument(
        "--reference-content",
        default="",
        help="Optional reference content.",
    )
    parser.add_argument(
        "--aspect-ratio",
        default="16:9",
        help="Optional aspect ratio (default: 16:9).",
    )
    parser.add_argument(
        "--resolution",
        default="2K",
        help="Optional resolution (default: 2K).",
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
    client = GoAIClient(skill_name="goai-ppt-gen")

    try:
        client.require_api_key()

        reference_images = client.resolve_image_inputs(args.reference)

        payload: dict[str, object] = {
            "idea": args.idea,
            "language": args.language,
        }
        if args.num_pages:
            try:
                payload["numPages"] = int(args.num_pages)
            except ValueError:
                pass
        if args.aspect_ratio:
            payload["aspectRatio"] = args.aspect_ratio
        if args.resolution:
            payload["resolution"] = args.resolution
        if args.reference_content:
            payload["referenceContent"] = args.reference_content
        if reference_images:
            payload["referenceImages"] = reference_images
        if args.reference_pdf:
            payload["referencePdfs"] = args.reference_pdf

        response = client.json_request(
            "POST",
            f"{client.base_url}/api/v2/ppt/generate",
            "auth",
            body=payload,
        )
        client.api_assert_ok(response)

        data = response.get("data")
        task_id = str(data.get("taskId") or "") if isinstance(data, dict) else ""
        project_id = str(data.get("projectId") or "") if isinstance(data, dict) else ""
        if not task_id:
            raise GoAIError("taskId missing in generate response")
        if not project_id:
            raise GoAIError("projectId missing in generate response")

        task_response = client.poll_task(
            f"{client.base_url}/api/v2/ppt/tasks/{task_id}",
            "projectId",
            interval_seconds=5,
            max_attempts=60,
            timeout_message="PPT generation timed out",
        )

        completed_data = client.last_payload.get("data") if client.last_payload else None
        if isinstance(completed_data, dict):
            completed_project_id = str(completed_data.get("projectId") or "")
            if completed_project_id:
                project_id = completed_project_id

        export_response = client.json_request(
            "POST",
            f"{client.base_url}/api/v2/projects/{project_id}/export/noteslide-pptx",
            "auth",
            body={},
        )
        client.api_assert_ok(export_response)

        export_data = export_response.get("data")
        job_id = str(export_data.get("jobId") or "") if isinstance(export_data, dict) else ""
        if not job_id:
            raise GoAIError("jobId missing in export response")

        download_url = client.poll_task(
            f"{client.base_url}/api/v2/projects/{project_id}/export/noteslide-pptx/{job_id}",
            "downloadUrl",
            interval_seconds=5,
            max_attempts=120,
            timeout_message="PPT export timed out",
        )

        output_path = client.download_media(download_url, f"goai-ppt-{project_id}.pptx")
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
