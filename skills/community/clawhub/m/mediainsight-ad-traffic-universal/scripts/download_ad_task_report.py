from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from tempfile import NamedTemporaryFile
import time
from zipfile import ZipFile

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import os

from mediainsight_client import (  # noqa: E402
    DEFAULT_BASE_URL,
    DEFAULT_MCP_URL,
    MediaInsightClient,
    MediaInsightError,
    resolve_media_insight_auth,
)
from submit_ad_task import DEFAULT_DEMO_TOKEN  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Download a completed MediaInsight ad-traffic report by internal task id."
    )
    auth = parser.add_mutually_exclusive_group(required=False)
    auth.add_argument(
        "--token",
        dest="token",
        help="MediaInsight MCP token.",
    )
    auth.add_argument(
        "--token-file",
        dest="token_file",
        help="Path to a file containing the MediaInsight token.",
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--mcp-url", default=DEFAULT_MCP_URL, help="MediaInsight MCP streamable HTTP endpoint.")
    parser.add_argument(
        "--mcp-token-type",
        type=int,
        default=0,
        help="Pass-through type for MCP get_ttc_token. Use 1 only after an API 401.",
    )
    parser.add_argument("--tenant-id", type=int, help="Optional tenant id to switch to after login.")
    id_group = parser.add_mutually_exclusive_group(required=True)
    id_group.add_argument("--task-id", type=int, help="Internal MediaInsight task id.")
    id_group.add_argument("--biz-id", type=int, help="External MediaInsight bizId returned by task creation.")
    parser.add_argument(
        "--output",
        help="Optional path for the downloaded report archive. Defaults to ./downloads/task-<id>.zip",
    )
    parser.add_argument(
        "--extract-dir",
        help="Optional directory to extract the downloaded zip contents into after download.",
    )
    parser.add_argument(
        "--wait",
        action="store_true",
        help="Poll file generation status until the report is ready, then download it.",
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=30,
        help="Seconds between status polls when --wait is enabled.",
    )
    parser.add_argument(
        "--wait-timeout",
        type=int,
        default=900,
        help="Maximum seconds to wait for report generation when --wait is enabled.",
    )
    parser.add_argument("--session-file", help="Optional path to persist the login session.")
    return parser


def load_token(args: argparse.Namespace) -> str:
    if args.token:
        return args.token.strip()
    if args.token_file:
        return Path(args.token_file).read_text(encoding="utf-8").strip()
    env_token = os.environ.get("MEDIAINSIGHT_MCP_TOKEN", "").strip()
    if env_token:
        return env_token
    return DEFAULT_DEMO_TOKEN


def using_demo_token(args: argparse.Namespace) -> bool:
    return not (
        args.token
        or args.token_file
        or os.environ.get("MEDIAINSIGHT_MCP_TOKEN", "").strip()
    )


def ensure_success(response: object, action: str) -> dict:
    if not isinstance(response, dict):
        raise MediaInsightError(f"{action} returned an unexpected payload")
    code = response.get("code")
    if code not in (0, "0", None):
        message = response.get("msg") or response.get("message") or "unknown error"
        raise MediaInsightError(f"{action} failed: {message}")
    return response


def derive_output_path(task_id: int, output: str | None) -> Path:
    if output:
        return Path(output)
    return Path.cwd() / "downloads" / f"task-{task_id}.zip"


def safe_name(name: str) -> str:
    return re.sub(r"[\\/:*?\"<>|]+", "-", name).strip() or "report"


def wait_until_report_ready(client: MediaInsightClient, task_id: int, *, interval: int, timeout: int) -> dict:
    if interval <= 0:
        raise MediaInsightError("--poll-interval must be positive")
    if timeout <= 0:
        raise MediaInsightError("--wait-timeout must be positive")

    start = time.monotonic()
    deadline = start + timeout
    while True:
        latest_status = ensure_success(client.task_report_file_gen_status(task_id), "file generation status")
        if latest_status.get("data", {}).get("status") == 2:
            return latest_status
        if time.monotonic() >= deadline:
            raise MediaInsightError("report file was not ready before wait timeout")
        elapsed = int(time.monotonic() - start)
        print(f"Report not ready yet (task_id={task_id}, elapsed={elapsed}s), retrying in {interval}s...", file=sys.stderr)
        time.sleep(interval)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if using_demo_token(args):
            print(
                "Using the public shared demo token with limited permissions. It may expire at any time; switch to your own MEDIAINSIGHT_MCP_TOKEN or --token if download fails.",
                file=sys.stderr,
            )
        auth = resolve_media_insight_auth(load_token(args), mcp_url=args.mcp_url, mcp_token_type=args.mcp_token_type)
        if args.session_file:
            session_file = Path(args.session_file)
        else:
            tmp = NamedTemporaryFile(prefix="mediainsight-download-", suffix=".json", delete=False)
            tmp.close()
            session_file = Path(tmp.name)
        client = MediaInsightClient(
            base_url=args.base_url,
            session_file=session_file,
            ttc_token=auth.get("token"),
        )
        if args.tenant_id:
            ensure_success(client.switch_tenant(args.tenant_id), "switch tenant")

        task_id = args.task_id
        if task_id is None:
            task_id = client.find_internal_task_id(args.biz_id)

        if args.wait:
            status_payload = wait_until_report_ready(
                client,
                task_id,
                interval=args.poll_interval,
                timeout=args.wait_timeout,
            )
        else:
            status_payload = ensure_success(client.task_report_file_gen_status(task_id), "file generation status")
        if status_payload.get("data", {}).get("status") != 2:
            raise MediaInsightError("report file is not ready for download")

        detail_payload = ensure_success(client.task_report_detail(task_id), "report detail")
        detail = detail_payload.get("data", {}) if isinstance(detail_payload.get("data"), dict) else {}

        archive_bytes, headers = client.task_download_report(task_id)
        output_path = derive_output_path(task_id, args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(archive_bytes)

        extracted_files: list[str] = []
        if args.extract_dir:
            extract_dir = Path(args.extract_dir)
            extract_dir.mkdir(parents=True, exist_ok=True)
            with ZipFile(output_path) as archive:
                for info in archive.infolist():
                    target = extract_dir / safe_name(info.filename)
                    target.write_bytes(archive.read(info))
                    extracted_files.append(str(target))

        print(
            json.dumps(
                {
                    "taskId": task_id,
                    "bizId": args.biz_id or detail.get("bizId"),
                    "taskName": detail.get("name"),
                    "status": status_payload.get("data", {}).get("status"),
                    "contentType": headers.get("Content-Type"),
                    "output": str(output_path),
                    "extractedFiles": extracted_files,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    except MediaInsightError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
