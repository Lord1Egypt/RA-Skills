"""CLI commands for Kaipai AI SDK."""

import argparse
import json
import os
import shlex
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from sdk.cli.base import CliCommand
from sdk.cli.runner import TaskRunner
from sdk.core.client import ConsumeDeniedError, SkillClient
from sdk.core.api import safe_url_preview, _progress_log


# Constants
PLACEHOLDER_AK = "your_access_key_here"
PLACEHOLDER_SK = "your_secret_key_here"
SPAWN_DEFAULT_TIMEOUT_SECONDS = 3600
VIDEO_TASKS = frozenset({"videoscreenclear", "hdvideoallinone"})


def _read_ak_sk_from_env_file(env_path: Optional[Path] = None) -> Tuple[str, str]:
    """Read AK/SK from environment or .env file."""
    ak = os.environ.get("MT_AK", "").strip()
    sk = os.environ.get("MT_SK", "").strip()

    if env_path is None:
        env_path = Path(__file__).parent.parent.parent / "scripts" / ".env"

    if not env_path.exists():
        return ak, sk

    try:
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key, value = key.strip(), value.strip().strip("\"'")
                if key == "MT_AK" and not ak:
                    ak = value
                elif key == "MT_SK" and not sk:
                    sk = value
    except OSError:
        pass
    return ak, sk


def _is_video_task(task: str) -> bool:
    return (task or "").strip() in VIDEO_TASKS


def _print_json(obj: Any) -> None:
    print(json.dumps(obj, indent=2, ensure_ascii=False), flush=True)


def _is_failed_result(result: Dict) -> bool:
    """Check if result indicates failure."""
    if result.get("skill_status") == "failed":
        return True
    err = result.get("error")
    if err in (
        "poll_timeout",
        "poll_aborted",
        "task_failed",
        "invalid_result",
        "membership_required",
        "credit_required",
        "consume_param_error",
    ):
        return True
    return False


def _success_envelope(task_name: str, result: Dict, *, resume: bool = False) -> Dict:
    """Wrap successful result with envelope."""
    urls = result.get("output_urls", [])
    if not isinstance(urls, list):
        urls = []
    primary = urls[0] if urls else None

    if resume:
        instruction = (
            "Polling resumed successfully. Use primary_result_url for next stage --input. "
            "Do not re-run run-task for this task_id."
        )
    else:
        instruction = (
            "Task completed. Do not re-run run-task for this task_id; use query-task only "
            "to resume. Next pipeline stage: new run-task with next --task and "
            "--input=primary_result_url."
        )

    return {
        **result,
        "skill_status": "completed",
        "task_name": task_name,
        "primary_result_url": primary,
        "agent_instruction": instruction,
    }


def _envelope_consume_denied(e: ConsumeDeniedError, task_name: str) -> Dict:
    """Structured output for POST /skill/consume.json failures."""
    api_code = e.code
    detail = e.msg

    if api_code == 60001:
        err = "membership_required"
        agent_instruction = (
            "MANDATORY (user-visible): Quota consume failed — membership or eligible subscription "
            "is required (api_code 60001)."
        )
    elif api_code == 60002:
        err = "credit_required"
        agent_instruction = (
            "MANDATORY (user-visible): Quota consume failed — insufficient credits (api_code 60002). "
            "You must tell the user they need more credits or a subscription."
        )
    else:
        err = "consume_param_error"
        agent_instruction = (
            f"Quota consume failed (api_code={api_code}, see detail). "
            "Treat as a parameter or invocation issue: verify --task, --input, and --params."
        )

    return {
        "error": err,
        "skill_status": "failed",
        "failure_stage": "consume_quota",
        "api_code": api_code,
        "detail": detail,
        "task_name": task_name,
        "agent_instruction": agent_instruction,
    }


def _run_task_command_argv(
    task: str, input_src: str, params_json: str, script_path: Optional[Path] = None
) -> List[str]:
    """Build run-task command argv."""
    if script_path is None:
        script_path = Path(__file__).parent.parent.parent / "scripts" / "kaipai_ai.py"
    argv = [
        "python3",
        str(script_path.resolve()),
        "run-task",
        "--task",
        task,
        "--input",
        input_src,
    ]
    if params_json:
        argv.extend(["--params", params_json])
    return argv


def _run_task_command_shell(
    task: str, input_src: str, params_json: str, script_path: Optional[Path] = None
) -> str:
    """Build run-task command as shell string."""
    parts = _run_task_command_argv(task, input_src, params_json, script_path)
    return " ".join(shlex.quote(p) for p in parts)


class PreflightCommand(CliCommand):
    """Check if AK/SK are configured."""

    name = "preflight"
    help = "Print ok or missing (AK/SK)"

    @classmethod
    def register(cls, subparser: argparse._SubParsersAction) -> None:
        p = subparser.add_parser(cls.name, help=cls.help)
        p.set_defaults(func=lambda args: cls().execute(args))

    def execute(self, args: argparse.Namespace) -> int:
        ak, sk = _read_ak_sk_from_env_file()
        ok = (
            bool(ak)
            and bool(sk)
            and ak != PLACEHOLDER_AK
            and sk != PLACEHOLDER_SK
        )
        print("ok" if ok else "missing")
        return 0


class InstallDepsCommand(CliCommand):
    """Install Python dependencies."""

    name = "install-deps"
    help = "Install requirements if needed"

    @classmethod
    def register(cls, subparser: argparse._SubParsersAction) -> None:
        p = subparser.add_parser(cls.name, help=cls.help)
        p.set_defaults(func=lambda args: cls().execute(args))

    def execute(self, args: argparse.Namespace) -> int:
        req = Path(__file__).parent.parent.parent / "scripts" / "requirements.txt"
        if not req.exists():
            print(json.dumps({"error": "requirements.txt not found", "path": str(req)}))
            return 1
        try:
            import requests  # noqa: F401
            import alibabacloud_oss_v2  # noqa: F401
        except ImportError:
            r = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-q", "-r", str(req)],
                cwd=str(req.parent),
            )
            return r.returncode
        return 0


class RunTaskCommand(CliCommand):
    """Run algorithm task."""

    name = "run-task"
    help = "Run algorithm task"

    @classmethod
    def register(
        cls,
        subparser: argparse._SubParsersAction,
        *,
        on_async_submitted: Optional[Callable[[str], None]] = None,
    ) -> None:
        p = subparser.add_parser(cls.name, help=cls.help)
        p.add_argument("--task", required=True, help="task_name e.g. eraser_watermark")
        p.add_argument(
            "--input", required=True, help="Image or video URL or local path"
        )
        p.add_argument(
            "--params",
            dest="params_json",
            default="",
            help='Optional JSON object for invoke params',
        )
        p.set_defaults(func=lambda args: cls(on_async_submitted=on_async_submitted).execute(args))

    def __init__(self, on_async_submitted: Optional[Callable[[str], None]] = None):
        self.on_async_submitted = on_async_submitted

    def execute(self, args: argparse.Namespace) -> int:
        params = {"parameter": {"rsp_media_type": "url"}}
        if args.params_json:
            try:
                params = json.loads(args.params_json)
            except json.JSONDecodeError as e:
                print(json.dumps({"error": "invalid --params JSON", "detail": str(e)}))
                return 1

        client = None
        try:
            client = SkillClient()

            def _on_async_submitted(tid: str) -> None:
                if self.on_async_submitted:
                    self.on_async_submitted(tid)

            result = client.run_task(
                args.task, args.input, params, on_async_submitted=_on_async_submitted
            )

            if not isinstance(result, dict):
                fail = {
                    "error": "invalid_result",
                    "skill_status": "failed",
                    "detail": repr(result),
                }
                _print_json(client.build_pipeline_trace(fail, success=False))
                return 1

            if _is_failed_result(result):
                _print_json(client.build_pipeline_trace(result, success=False))
                return 1

            out = _success_envelope(args.task, result)
            _print_json(client.build_pipeline_trace(out, success=True))

        except ConsumeDeniedError as e:
            fail = _envelope_consume_denied(e, args.task)
            if client is not None:
                client.build_pipeline_trace(fail, success=False)
            _print_json(fail)
            return 1
        except Exception as e:
            err: Dict[str, Any] = {"error": str(e), "skill_status": "failed"}
            if client is not None:
                client.build_pipeline_trace(err, success=False)
            _print_json(err)
            return 1

        return 0


class QueryTaskCommand(CliCommand):
    """Resume async status polling by task_id."""

    name = "query-task"
    help = "Resume async status polling by task_id"

    @classmethod
    def register(cls, subparser: argparse._SubParsersAction) -> None:
        p = subparser.add_parser(cls.name, help=cls.help)
        p.add_argument("--task-id", required=True, dest="task_id", help="Full task id")
        p.add_argument(
            "--task", default="", help="Optional label for task_name in success JSON"
        )
        p.set_defaults(func=lambda args: cls().execute(args))

    def execute(self, args: argparse.Namespace) -> int:
        task_label = (args.task or "").strip() or "query_task"
        client = None
        try:
            client = SkillClient()
            result = client.poll_task_status(args.task_id)

            if not isinstance(result, dict):
                fail = {
                    "error": "invalid_result",
                    "skill_status": "failed",
                    "detail": repr(result),
                }
                _print_json(client.build_pipeline_trace(fail, success=False))
                return 1

            if _is_failed_result(result):
                _print_json(client.build_pipeline_trace(result, success=False))
                return 1

            out = _success_envelope(task_label, result, resume=True)
            _print_json(client.build_pipeline_trace(out, success=True))

        except Exception as e:
            err = {"error": str(e), "skill_status": "failed"}
            if client is not None:
                client.build_pipeline_trace(err, success=False)
            _print_json(err)
            return 1

        return 0


class SpawnRunTaskCommand(CliCommand):
    """Build sessions_spawn payload for video tasks."""

    name = "spawn-run-task"
    help = "Build sessions_spawn payload for video tasks only"

    @classmethod
    def register(cls, subparser: argparse._SubParsersAction) -> None:
        p = subparser.add_parser(cls.name, help=cls.help)
        p.add_argument(
            "--task", required=True, help="Video task_name only: videoscreenclear or hdvideoallinone"
        )
        p.add_argument("--input", required=True, help="Video URL or local path")
        p.add_argument("--params", dest="params_json", default="", help="Optional JSON for --params")
        p.add_argument("--deliver-to", default=None, help="Feishu oc_/ou_, Telegram chat_id, etc.")
        p.add_argument("--deliver-channel", default=None, help="feishu, telegram, discord, or other")
        p.add_argument(
            "--run-timeout-seconds",
            type=int,
            default=SPAWN_DEFAULT_TIMEOUT_SECONDS,
            help="sessions_spawn runTimeoutSeconds",
        )
        p.set_defaults(func=lambda args: cls().execute(args))

    def execute(self, args: argparse.Namespace) -> int:
        task = (args.task or "").strip()
        if not _is_video_task(task):
            _print_json({
                "error": "spawn_video_tasks_only",
                "skill_status": "failed",
                "detail": f"spawn-run-task accepts only video task_name: {sorted(VIDEO_TASKS)}",
            })
            return 1

        payload = self._build_spawn_payload(
            task=task,
            input_src=args.input,
            params_json=getattr(args, "params_json", "") or "",
            deliver_to=getattr(args, "deliver_to", None),
            deliver_channel=getattr(args, "deliver_channel", None),
            run_timeout_seconds=args.run_timeout_seconds,
        )
        _print_json(payload)
        return 0

    def _build_spawn_payload(
        self,
        task: str,
        input_src: str,
        params_json: str,
        deliver_to: Optional[str],
        deliver_channel: Optional[str],
        run_timeout_seconds: int,
    ) -> Dict:
        """Build sessions_spawn payload for async Kaipai run-task."""
        base_dir = Path(__file__).parent.parent.parent
        script_path = base_dir / "scripts" / "kaipai_ai.py"
        deliver_to_str = deliver_to or "<deliver_to>"
        deliver_channel_str = (deliver_channel or "feishu").lower()
        cmd = _run_task_command_shell(task, input_src, params_json, script_path)
        is_video = _is_video_task(task)

        # Delivery instructions
        if deliver_channel_str == "feishu":
            if is_video:
                delivery_instructions = (
                    f"Download and send via Feishu: curl -sL -o /tmp/result.mp4 '<url>' && "
                    f"python3 {base_dir}/scripts/feishu_send_video.py --video /tmp/result.mp4 --to '{deliver_to_str}'"
                )
            else:
                delivery_instructions = (
                    f"python3 {base_dir}/scripts/feishu_send_image.py --image '<url>' --to '{deliver_to_str}'"
                )
        elif deliver_channel_str == "telegram":
            if is_video:
                delivery_instructions = (
                    f"Download and send via Telegram: curl -sL -o /tmp/result.mp4 '<url>' && "
                    f"TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN python3 {base_dir}/scripts/telegram_send_video.py "
                    f"--video /tmp/result.mp4 --to '{deliver_to_str}'"
                )
            else:
                delivery_instructions = (
                    f"TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN python3 {base_dir}/scripts/telegram_send_image.py "
                    f"--image '<url>' --to '{deliver_to_str}'"
                )
        else:
            delivery_instructions = f"Deliver to {deliver_to_str} via {deliver_channel_str}"

        label = f"{task}: {input_src}"
        if len(label) > 72:
            label = label[:69] + "..."

        return {
            "sessions_spawn_args": {
                "task": (
                    f"Run: {cmd}\n\n"
                    f"After completion, {delivery_instructions}\n\n"
                    f"If failed with task_id, resume with: query-task --task-id <id>"
                ),
                "label": "kaipai: " + label,
                "runTimeoutSeconds": run_timeout_seconds,
            },
            "command": cmd,
        }


class LastTaskCommand(CliCommand):
    """Show last run-task/query-task record."""

    name = "last-task"
    help = "Show last run-task/query-task record JSON"

    @classmethod
    def register(cls, subparser: argparse._SubParsersAction) -> None:
        p = subparser.add_parser(cls.name, help=cls.help)
        p.set_defaults(func=lambda args: cls().execute(args))

    def execute(self, args: argparse.Namespace) -> int:
        state_dir = Path.home() / ".openclaw" / "workspace" / "openclaw-kaipai-ai"
        last_task_file = state_dir / "last_task.json"

        if not last_task_file.is_file():
            _print_json({"message": "No saved task yet.", "record": None})
            return 0

        try:
            with open(last_task_file, encoding="utf-8") as f:
                record = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            _print_json({"error": "failed to read last_task.json", "detail": str(e)})
            return 1

        _print_json(record)
        return 0


class HistoryCommand(CliCommand):
    """List recent task records."""

    name = "history"
    help = "List recent task records (up to 50)"

    @classmethod
    def register(cls, subparser: argparse._SubParsersAction) -> None:
        p = subparser.add_parser(cls.name, help=cls.help)
        p.set_defaults(func=lambda args: cls().execute(args))

    def execute(self, args: argparse.Namespace) -> int:
        state_dir = Path.home() / ".openclaw" / "workspace" / "openclaw-kaipai-ai"
        history_dir = state_dir / "history"
        history_dir.mkdir(parents=True, exist_ok=True)

        files = sorted(history_dir.glob("task_*.json"))
        jobs: List[Dict] = []
        for path in files[-50:]:
            try:
                with open(path, encoding="utf-8") as f:
                    jobs.append(json.load(f))
            except (json.JSONDecodeError, OSError):
                continue

        _print_json({"jobs": jobs, "count": len(jobs)})
        return 0


class ResolveInputCommand(CliCommand):
    """Download IM attachment / URL to a local path."""

    name = "resolve-input"
    help = "Download IM attachment / URL to a local path for --input"

    @classmethod
    def register(cls, subparser: argparse._SubParsersAction) -> None:
        p = subparser.add_parser(cls.name, help=cls.help)
        p.add_argument("--file", help="Local file path")
        p.add_argument("--url", help="HTTP(S) URL to download")
        p.add_argument("--telegram-file-id", dest="telegram_file_id", help="Telegram file_id")
        p.add_argument(
            "--feishu-message-id", dest="feishu_message_id", default="", help="Feishu message id"
        )
        p.add_argument("--feishu-image-key", dest="feishu_image_key", help="Feishu image resource key")
        p.add_argument(
            "--feishu-app-token", dest="feishu_app_token", default="", help="Feishu tenant token"
        )
        p.add_argument("--output-dir", default="/tmp", help="Directory for downloaded file")
        p.set_defaults(func=lambda args: cls().execute(args))

    def execute(self, args: argparse.Namespace) -> int:
        try:
            import requests
        except ImportError:
            _print_json({
                "error": "requests not installed",
                "install_command": "pip install -r scripts/requirements.txt",
            })
            return 1

        out_dir = Path(args.output_dir).expanduser()
        out_dir.mkdir(parents=True, exist_ok=True)

        file_bytes: Optional[bytes] = None
        filename = "input.bin"

        if getattr(args, "file", None):
            p = Path(args.file).expanduser()
            if not p.is_file():
                _print_json({"error": f"File not found: {args.file}"})
                return 1
            from sdk.core.config import url_download_max_bytes
            if p.stat().st_size > url_download_max_bytes():
                _print_json({"error": "File too large"})
                return 1
            file_bytes = p.read_bytes()
            filename = p.name

        elif getattr(args, "url", None):
            file_bytes, filename = self._download_url(args.url)
            if file_bytes is None:
                return 1

        elif getattr(args, "telegram_file_id", None):
            file_bytes, filename = self._download_telegram(args.telegram_file_id)
            if file_bytes is None:
                return 1

        elif getattr(args, "feishu_image_key", None):
            file_bytes, filename = self._download_feishu(
                args.feishu_image_key,
                args.feishu_message_id,
                args.feishu_app_token,
            )
            if file_bytes is None:
                return 1

        else:
            _print_json({
                "error": "Provide one of: --file, --url, --telegram-file-id, --feishu-image-key",
            })
            return 1

        dest = out_dir / f"kaipai_in_{uuid.uuid4().hex[:10]}_{filename}"
        dest.write_bytes(file_bytes)
        _print_json({
            "path": str(dest.resolve()),
            "filename": filename,
            "bytes": len(file_bytes),
        })
        return 0

    def _download_url(self, url: str) -> Tuple[Optional[bytes], str]:
        import requests
        from sdk.core.config import url_download_timeout_tuple, url_download_max_bytes, USER_AGENT

        url = url.strip()
        if not url.startswith(("http://", "https://")):
            _print_json({"error": "Only http:// and https:// URLs are allowed"})
            return None, ""

        url_to = url_download_timeout_tuple()
        r = requests.get(
            url,
            stream=True,
            timeout=url_to,
            headers={"User-Agent": USER_AGENT},
        )
        if r.status_code != 200:
            _print_json({"error": f"Download failed: HTTP {r.status_code}"})
            return None, ""

        chunks: List[bytes] = []
        total = 0
        max_b = url_download_max_bytes()
        for chunk in r.iter_content(chunk_size=65536):
            total += len(chunk)
            if total > max_b:
                _print_json({"error": "Downloaded file too large"})
                return None, ""
            chunks.append(chunk)

        file_bytes = b"".join(chunks)

        # Determine filename from URL
        url_path = url.split("?")[0]
        ext_from_url = (
            url_path.rsplit(".", 1)[-1].lower() if "." in url_path else ""
        )
        if ext_from_url in ("jpg", "jpeg", "png", "webp", "gif", "mp4", "mov", "webm"):
            extension = "jpg" if ext_from_url == "jpeg" else ext_from_url
        else:
            ct = (r.headers.get("Content-Type") or "").split(";")[0].strip()
            extension = {
                "image/jpeg": "jpg",
                "image/png": "png",
                "image/webp": "webp",
                "video/mp4": "mp4",
                "video/quicktime": "mov",
            }.get(ct, "bin")
        filename = f"download_{uuid.uuid4().hex[:8]}.{extension}"

        return file_bytes, filename

    def _download_telegram(self, file_id: str) -> Tuple[Optional[bytes], str]:
        import requests
        from sdk.core.config import url_download_max_bytes

        token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
        if not token:
            _print_json({"error": "TELEGRAM_BOT_TOKEN not set"})
            return None, ""

        r = requests.get(
            f"https://api.telegram.org/bot{token}/getFile",
            params={"file_id": file_id},
            timeout=(15, 60),
        )
        r.raise_for_status()
        data = r.json()
        if not data.get("ok"):
            _print_json({"error": "Telegram getFile failed", "detail": data})
            return None, ""

        file_path = data["result"]["file_path"]
        ext_from_path = (
            file_path.rsplit(".", 1)[-1].lower() if "." in file_path else "jpg"
        )
        extension = (
            ext_from_path
            if ext_from_path in ("jpg", "jpeg", "png", "webp", "gif", "mp4", "mov", "webm")
            else "jpg"
        )
        filename = f"tg_{uuid.uuid4().hex[:8]}.{extension}"

        dl_url = f"https://api.telegram.org/file/bot{token}/{file_path}"
        r2 = requests.get(
            dl_url,
            timeout=(15, 120),
            headers={"User-Agent": "kaipai-ai-sdk/1.2.2"},
        )
        r2.raise_for_status()
        file_bytes = r2.content

        max_b = url_download_max_bytes()
        if len(file_bytes) > max_b:
            _print_json({"error": "Telegram file too large"})
            return None, ""

        return file_bytes, filename

    def _download_feishu(
        self, image_key: str, message_id: str, app_token: str
    ) -> Tuple[Optional[bytes], str]:
        import requests
        from sdk.core.config import url_download_timeout_tuple, url_download_max_bytes

        if not message_id:
            _print_json({"error": "--feishu-message-id required with --feishu-image-key"})
            return None, ""

        feishu_token = (app_token or os.environ.get("FEISHU_APP_TOKEN", "")).strip()
        if not feishu_token:
            _print_json({"error": "FEISHU_APP_TOKEN or --feishu-app-token required"})
            return None, ""

        url_to = url_download_timeout_tuple()
        r = requests.get(
            f"https://open.feishu.cn/open-apis/im/v1/messages/{message_id}/resources/{image_key}",
            params={"type": "image"},
            headers={"Authorization": f"Bearer {feishu_token}"},
            timeout=url_to,
        )
        if r.status_code != 200:
            _print_json({"error": f"Feishu download failed: HTTP {r.status_code}"})
            return None, ""

        file_bytes = r.content
        max_b = url_download_max_bytes()
        if len(file_bytes) > max_b:
            _print_json({"error": "Feishu resource too large"})
            return None, ""

        extension = "jpg"
        ct = r.headers.get("Content-Type", "")
        if "png" in ct:
            extension = "png"
        elif "webp" in ct:
            extension = "webp"
        filename = f"feishu_{uuid.uuid4().hex[:8]}.{extension}"

        return file_bytes, filename
