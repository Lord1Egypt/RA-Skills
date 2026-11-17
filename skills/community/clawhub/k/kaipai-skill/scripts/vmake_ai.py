#!/usr/bin/env python3
"""
Vmake skill CLI — single entry for agents:
preflight, install-deps, catalog, run-task, query-task, spawn-run-task,
last-task, history, resolve-input.
Run from anywhere: python3 /path/to/scripts/vmake_ai.py <command> ...
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import re
import shlex
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
SKILL_BASE_DIR = SCRIPTS_DIR.parent

import config as skill_config
from agent_info import resolve_agent_info
from delivery import bundled_features, bundled_channels, resolve_channel
from delivery import delivery_instructions as build_delivery_instructions
from params_schema import ParameterValidationError, SchemaConfigurationError, OptionsSourceError
from input_media import InputMediaValidationError

STATE_DIR = Path.home() / ".openclaw" / "workspace" / 'openclaw-kaipai-ai'
LAST_TASK_FILE = STATE_DIR / "last_task.json"
HISTORY_DIR = STATE_DIR / "history"

VIDEO_TASKS = frozenset({"videoscreenclear", "hdvideoallinone"})

CONNECT_TIMEOUT = 15
READ_TIMEOUT = 60

_CONSUME_MEDIA_URL_INVALID_CODE = 10103
_CONSUME_MEDIA_URL_INVALID_MSG = (
    "This media URL is not supported. Please upload the image or video file directly and try again."
)

PLACEHOLDER_AK = "your_access_key_here"
PLACEHOLDER_SK = "your_secret_key_here"

DEFAULT_PARAMS = {"parameter": {"rsp_media_type": "url"}}

# OpenClaw sessions_spawn default; video tasks may poll up to ~1h extended schedule
SPAWN_DEFAULT_TIMEOUT_SECONDS = 3600

_HTTPS_URL_RE = re.compile(r"https://[^\s\])}>\"',]+", re.IGNORECASE)


def _https_urls_from_text(text: str) -> list[str]:
    """Extract https URLs from API msg / detail (e.g. consume.json meta.msg)."""
    if not isinstance(text, str) or not text.strip():
        return []
    out: list[str] = []
    for u in _HTTPS_URL_RE.findall(text):
        u = u.rstrip(".,;)]}>\"'")
        if u and u not in out:
            out.append(u)
    return out


def _pick_pricing_url(urls: list[str]) -> str | None:
    if not urls:
        return None
    for u in urls:
        if "pricing" in u.lower():
            return u
    return urls[0]


def _read_ak_sk_from_env_file() -> tuple[str, str]:
    ak = os.environ.get("MT_AK", "").strip()
    sk = os.environ.get("MT_SK", "").strip()
    env_path = SCRIPTS_DIR / ".env"
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


def _success_envelope(task_name: str, result: dict, *, resume: bool = False) -> dict:
    urls = result.get("output_urls")
    if not isinstance(urls, list):
        urls = []
    primary = urls[0] if urls else None
    if resume:
        instruction = (
            "Polling resumed successfully. Use primary_result_url for Step 4 or the next "
            "stage --input. Do not re-run run-task for this task_id. "
            "Next stage: new job (video: new spawn-run-task per stage). "
            "Details: SKILL.md Step 3 and Multi-stage pipelines."
        )
    else:
        instruction = (
            "Task completed. Do not re-run run-task for this task_id; use query-task only "
            "to resume. Next pipeline stage: new run-task with next --task and "
            "--input=primary_result_url (each video stage: its own spawn-run-task). "
            "Step 4: primary_result_url. Empty output_urls: check data/meta. "
            "Full rules: SKILL.md."
        )
    return {
        **result,
        "skill_status": "completed",
        "task_name": task_name,
        "primary_result_url": primary,
        "agent_instruction": instruction,
    }


def _is_failed_cli_result(result: dict) -> bool:
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
        "consume_denied",
        "consume_param_error",
    ):
        return True
    return False


def _envelope_consume_denied(e, task_name: str) -> dict:
    """Structured stdout for POST /skill/consume.json failures (see docs/errors-and-polling.md)."""
    api_code = e.code
    detail = e.msg
    if (
        api_code == _CONSUME_MEDIA_URL_INVALID_CODE
        and detail == _CONSUME_MEDIA_URL_INVALID_MSG
    ):
        err = "input_unavailable"
        agent_instruction = (
            "The consume service rejected the media URL because its domain is not supported. "
            "Do not retry the same URL. Ask the user to upload the image or video file directly. "
            "The algorithm task was not submitted."
        )
    elif api_code == 60001:
        err = "membership_required"
        agent_instruction = (
            "MANDATORY (user-visible): Quota consume failed — membership or eligible subscription "
            "is required (api_code 60001). You must tell the user clearly, following the server "
            "**detail** (API msg). If this JSON has **pricing_url**, include that link in your reply; "
            "if not, quote or paste the full **detail** so any links in the server message reach the user. "
            "Do not retry run-task expecting success by only changing --task or --params."
        )
    elif api_code == 60002:
        err = "credit_required"
        agent_instruction = (
            "MANDATORY (user-visible): Quota consume failed — insufficient credits (api_code 60002). "
            "You must tell the user they need more credits or a subscription before this API can run, "
            "using the server **detail** (API msg) as the source of truth. If this JSON has **pricing_url**, "
            "include that link; if not, quote or paste the full **detail** so links from the API are visible. "
            "Do not retry run-task or only tweak --task/--params expecting this to clear; do not treat as success."
        )
    elif getattr(e, "notices", None):
        err = "consume_denied"
        agent_instruction = (
            "MANDATORY (user-visible): Quota consume failed. Include every non-empty server "
            "notice message in the reply, including unknown notice codes, and surface any "
            "notice action URL. Follow the server notice/detail for the next action; do not "
            "reinterpret this as a parameter error or retry unchanged."
        )
    else:
        err = "consume_param_error"
        agent_instruction = (
            f"Quota consume failed (api_code={api_code}, see detail). "
            "Treat as a parameter or invocation issue: verify --task, --input, and --params "
            "against SKILL.md and remote config, then fix and retry. Do not tell the user to "
            "recharge unless api_code is 60002."
        )
    out: dict = {
        "error": err,
        "skill_status": "failed",
        "failure_stage": "consume_quota",
        "api_code": api_code,
        "detail": detail,
        "task_name": task_name,
        "agent_instruction": agent_instruction,
    }
    if api_code in (60001, 60002):
        pu = _pick_pricing_url(_https_urls_from_text(detail))
        if pu:
            out["pricing_url"] = pu
    notices = getattr(e, "notices", None)
    if notices:
        out["notices"] = notices
    return out


def _config_failure_envelope(error) -> dict:
    """Return a customer-safe config failure without raw response diagnostics."""
    detail = getattr(error, "msg", None) or str(error)
    out = {
        "error": "config_unavailable",
        "skill_status": "failed",
        "failure_stage": "fetch_config",
        "detail": detail,
        "agent_instruction": (
            "Stop. Do not infer a task from local names, upload media, call consume, "
            "or submit an algorithm job. Retry catalog discovery only after remote "
            "config becomes available."
        ),
    }
    api_code = getattr(error, "original_code", None)
    if api_code not in (None, -1, "-1"):
        out["api_code"] = api_code
    notices = getattr(error, "notices", None)
    if notices:
        out["notices"] = notices
    return out


def _public_catalog(catalog: dict, media_type: str = "") -> dict:
    """Expose task-selection fields, including the V2 execution identity."""
    mode = catalog.get("mode")
    requested_media = (media_type or "").strip().lower()
    tasks = []
    for entry in catalog.get("entries") or []:
        entry_media = entry.get("media_type") or ""
        if requested_media and entry_media and entry_media != requested_media:
            continue
        if mode == "v2":
            name = entry.get("name")
            if not name:
                continue
            item = {
                "material_id": entry.get("material_id"),
                "name": name,
                "description": entry.get("description"),
                "media_type": entry_media,
            }
            if "params_schema" in entry:
                item["params_schema"] = entry["params_schema"]
        else:
            item = {
                "task_name": entry.get("material_id"),
                "media_type": entry_media,
            }
        if "input_media" in entry:
            item["input_media"] = copy.deepcopy(entry["input_media"])
        tasks.append(item)
    return {
        "skill_status": "ready",
        "config_mode": mode,
        "catalog_source": catalog.get("source"),
        "tasks": tasks,
        "count": len(tasks),
        "agent_instruction": (
            "V2: select by name, description, and media_type, then pass the exact "
            "returned material_id to --task. Present name, description, and localized "
            "media_type to the user. Legacy: use an alias only if it "
            "appears in tasks. Never fall back to a local task name when catalog "
            "discovery fails."
        ),
    }


def _attach_client_notices(result: dict, client) -> dict:
    """Attach notices collected from config, consume, or algorithm responses."""
    if not isinstance(result, dict) or client is None:
        return result
    getter = getattr(client, "get_notices", None)
    notices = getter() if callable(getter) else []
    if notices:
        result["notices"] = notices
    return result


def _merge_pipeline_trace(
    result: dict,
    client,
    *,
    success: bool,
) -> dict:
    """Attach upload/download/quota/submit steps for stdout JSON (stderr has [vmake-ai] lines)."""
    if not isinstance(result, dict):
        return result
    trace = list(getattr(client, "_pipeline_trace", None) or [])
    if success:
        urls = result.get("output_urls")
        n = len(urls) if isinstance(urls, list) else 0
        p = result.get("primary_result_url")
        prev = None
        if isinstance(p, str):
            prev = p if len(p) <= 72 else p[:69] + "..."
        trace = trace + [
            {
                "step": "result_download",
                "description": "Download outputs with HTTP GET on primary_result_url or each output_urls item",
                "output_count": n,
                "primary_result_url_preview": prev,
            }
        ]
    result["pipeline_trace"] = trace
    return _attach_client_notices(result, client)


def _print_json(obj) -> None:
    print(json.dumps(obj, indent=2, ensure_ascii=False), flush=True)


def _is_video_task(task: str, media_type: str = "") -> bool:
    if media_type:
        return media_type.strip().lower() == "video"
    return (task or "").strip() in VIDEO_TASKS


def _ensure_state_dir() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)


def _task_record_from_result(
    task_name: str,
    input_src: str,
    result: dict | None,
    *,
    error_message: str | None = None,
) -> dict:
    rec: dict = {
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "task_name": task_name,
        "input": input_src,
    }
    if result and isinstance(result, dict):
        rec["skill_status"] = result.get("skill_status", "unknown")
        tid = result.get("task_id")
        if not tid and isinstance(result.get("data"), dict):
            r = result["data"].get("result")
            if isinstance(r, dict):
                tid = r.get("id")
        if tid:
            rec["task_id"] = tid
        if result.get("primary_result_url"):
            rec["primary_result_url"] = result["primary_result_url"]
        if result.get("output_urls"):
            rec["output_urls"] = result["output_urls"]
        if result.get("error"):
            rec["error"] = result["error"]
        if result.get("notices"):
            rec["notices"] = result["notices"]
    if error_message:
        rec["skill_status"] = "failed"
        rec["error"] = error_message
    return rec


def _save_submitted_checkpoint(task_name: str, input_src: str, task_id: str) -> None:
    """
    Persist task_id to last_task.json as soon as the async job is accepted (before polling).
    Lets agents recover with query-task if the host kills the process mid-poll.
    """
    tid = (task_id or "").strip()
    if not tid:
        return
    rec = {
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "task_name": task_name,
        "input": input_src,
        "task_id": tid,
        "skill_status": "polling",
        "agent_instruction": (
            "Async job submitted; polling in progress. If this process stops before "
            "final JSON on stdout (host timeout, SIGKILL, OOM), use "
            "`vmake_ai.py query-task --task-id` with the task_id above — do not "
            "run-task again for this job. See SKILL.md §3c and docs/errors-and-polling.md."
        ),
    }
    _ensure_state_dir()
    with open(LAST_TASK_FILE, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=2, ensure_ascii=False)


def _save_task_record(record: dict) -> None:
    _ensure_state_dir()
    with open(LAST_TASK_FILE, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    hist_path = HISTORY_DIR / f"task_{ts}.json"
    with open(hist_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    history_files = sorted(HISTORY_DIR.glob("task_*.json"))
    if len(history_files) > 50:
        for old in history_files[:-50]:
            old.unlink(missing_ok=True)


def _run_task_command_argv(
    task: str,
    input_src: str,
    params_json: str,
    agent_info=None,
    profile_json: str = "",
) -> list[str]:
    argv = [
        "python3",
        str((SCRIPTS_DIR / "vmake_ai.py").resolve()),
        "run-task",
        "--task",
        task,
    ]
    sources = [] if not input_src else (input_src if isinstance(input_src, (list, tuple)) else [input_src])
    for source in sources:
        argv.extend(["--input", source])
    if params_json:
        argv.extend(["--params", params_json])
    if profile_json:
        argv.extend(["--profile", profile_json])
    if agent_info is not None:
        for field, value in agent_info.items():
            argv.extend(["--agent-" + field, value])
    return argv


def _run_task_command_shell(
    task: str,
    input_src: str,
    params_json: str,
    agent_info=None,
    profile_json: str = "",
) -> str:
    parts = _run_task_command_argv(
        task, input_src, params_json, agent_info, profile_json
    )
    return " ".join(shlex.quote(p) for p in parts)


def build_spawn_run_task(
    task: str,
    input_src: str,
    params_json: str,
    deliver_to: str | None,
    deliver_channel: str | None,
    run_timeout_seconds: int,
    agent_name=None,
    agent_version=None,
    agent_model=None,
    media_type="",
    profile_json="",
) -> dict:
    """Build sessions_spawn payload for async Vmake run-task (same as Medeo spawn-task pattern)."""
    script_path = str((SCRIPTS_DIR / "vmake_ai.py").resolve())
    deliver_to_str = deliver_to or "<deliver_to>"
    deliver_channel_str = resolve_channel(deliver_channel)
    base_dir = str(SKILL_BASE_DIR)
    # Freeze caller metadata, including unknown fields, across worker environments.
    agent_info = resolve_agent_info(agent_name, agent_version, agent_model)
    cmd = _run_task_command_shell(
        task, input_src, params_json, agent_info, profile_json
    )
    is_video = _is_video_task(task, media_type)

    delivery_instructions = build_delivery_instructions(
        deliver_channel_str, base_dir, deliver_to_str, is_video=is_video,
    )

    timeout_hint = (
        f"Keep `runTimeoutSeconds` at least the payload default ({SPAWN_DEFAULT_TIMEOUT_SECONDS}s); "
        "do not shrink without accepting timeout risk. "
        "SIGKILL / no final JSON, host turn limits, `query-task` / `last-task` / `history`: "
        "see the skill file `docs/errors-and-polling.md` and SKILL.md §3c–§3d.\n\n"
    )
    task_text = (
        f'You are a Kaipai AI worker. Run the following command and complete delivery.\n\nBILLING (MANDATORY): This API consumes paid quota for the MT_AK tenant. Never tell the user the tool is free, costs nothing, or uses no credits; do not invent prices or plans. Use neutral success copy only. On credit/membership errors, follow stdout **detail** and **pricing_url** when present (same as SKILL.md Step 3 quota failures).\nSUBMISSION (MANDATORY): Run only the embedded command below — do not replace it with hand-crafted curl/HTTP to wapi or AIGC invoke (that skips /skill/consume.json). For status on an existing task_id only, use query-task per SKILL.md.\n\nCommand:\n```\n{cmd}\n```\n\nRun install-deps first if this environment never installed requirements:\n`python3 {shlex.quote(script_path)} install-deps`\n\n'
        + timeout_hint
        + "The command blocks until the algorithm finishes (wall time varies; "
        "do NOT background it).\n\n"
        "When the command finishes:\n"
        "- Whenever stdout JSON contains **notices**, include every non-empty notice **message** "
        "in the user-facing reply. Unknown notice codes must still be shown. A warning notice "
        "does not change a completed task into a failure. An error notice follows the accompanying "
        "skill_status/api_code. Do not repeat notices with the same dedupe_key in one reply.\n"
        '- If exit code is 0 and stdout JSON contains "skill_status": "completed":\n'
        "  1. Use output_urls[0] or primary_result_url as the result link.\n"
        f"{delivery_instructions}\n"
        "  3. Reply with a short success summary.\n"
        '- If stdout JSON has "skill_status": "failed" or top-level "error" '
        "(e.g. poll_timeout, poll_aborted, task_failed), or exit code non-zero: explain "
        "to the user; check MT_AK/MT_SK, network; timeouts: larger runTimeoutSeconds if needed.\n"
        "  - If **error** is **credit_required** (api_code 60002) or **failure_stage** is "
        "**consume_quota** with that error: follow stdout **detail** (server msg). Include JSON "
        "**pricing_url** in your reply when present (parsed from the API message); otherwise paste "
        "or quote the full **detail** so the user sees any links the server sent.\n"
        "  - If **error** is **membership_required** (api_code 60001): same — **pricing_url** if "
        "present, else full **detail**.\n"
        "  - If **error** is **consume_denied**: follow every server notice message and action URL; "
        "do not reinterpret an unknown notice code or retry unchanged.\n"
        "  - If **error** is **input_unavailable**: do not retry the same URL; ask the user to "
        "upload the image or video file directly.\n"
        "  - If **error** is **consume_param_error**: fix invocation per agent_instruction; "
        "do not blame credits.\n"
        "- If you have **task_id** and the job may still be running, resume polling only:\n"
        f"  `python3 {shlex.quote(script_path)} query-task --task-id \"<task_id>\"`\n"
    )

    label = f"{task}: {input_src}"
    if len(label) > 72:
        label = label[:69] + "..."

    return {
        "sessions_spawn_args": {
            "task": task_text,
            "label": "vmake: " + label,
            "runTimeoutSeconds": run_timeout_seconds,
        },
        "command": cmd,
    }


def cmd_preflight(_args: argparse.Namespace) -> int:
    ak, sk = _read_ak_sk_from_env_file()
    ok = (
        bool(ak)
        and bool(sk)
        and ak != PLACEHOLDER_AK
        and sk != PLACEHOLDER_SK
    )
    print("ok" if ok else "missing")
    if not ok:
        print(
            '开拍：请向管理员申请凭证，并在 scripts/.env 中配置 MT_AK / MT_SK（参考 .env.example）。',
            file=sys.stderr,
        )
    return 0


def cmd_install_deps(_args: argparse.Namespace) -> int:
    req = SCRIPTS_DIR / "requirements.txt"
    if not req.exists():
        print(json.dumps({"error": "requirements.txt not found", "path": str(req)}))
        return 1
    try:
        import requests  # noqa: F401
        import alibabacloud_oss_v2  # noqa: F401
    except ImportError:
        r = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", "-r", str(req)],
            cwd=str(SCRIPTS_DIR),
        )
        return r.returncode
    return 0


def cmd_catalog(args: argparse.Namespace) -> int:
    """Fetch and print the remote task catalog without upload or consume."""
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    from client import ConfigFetchError, SkillClient

    try:
        client = SkillClient(
            auto_fetch_config=False,
            agent_name=args.agent_name,
            agent_version=args.agent_version,
            agent_model=args.agent_model,
        )
        catalog = client.get_task_catalog(refresh=True)
        out = _public_catalog(catalog, args.media_type)
        _attach_client_notices(out, client)
        if catalog.get("mode") not in ("v2", "legacy") or not out["tasks"]:
            out.update(
                {
                    "error": "config_catalog_empty",
                    "skill_status": "failed",
                    "agent_instruction": (
                        'MANDATORY (user-visible): Tell the user that no matching Kaipai task is currently available. Include any server notice messages. If those notices provide no next step, advise the user to contact Kaipai official support without inventing a support URL or contact method, then stop. Do not infer a local task name, upload, consume, or submit.'
                    ),
                }
            )
            _print_json(out)
            return 1
        _print_json(out)
        return 0
    except ConfigFetchError as e:
        _print_json(_config_failure_envelope(e))
        return 1
    except Exception as e:
        _print_json(_config_failure_envelope(e))
        return 1


def _schema_failure(error, client):
    """Classify server contract failures separately from user parameter errors."""
    return _attach_client_notices({
        "error": "invalid_parameter_schema", "skill_status": "failed",
        "failure_stage": "validate_task_parameters", "detail": str(error),
    }, client)


def _options_failure(error, client):
    return _attach_client_notices({
        "error": "params_options_unavailable", "skill_status": "failed",
        "failure_stage": "fetch_params_field_options", "detail": str(error),
    }, client)


def cmd_params_field_options(args):
    """Discover complete field options without uploading media or consuming quota."""
    from client import SkillClient, ConfigFetchError

    client = None
    try:
        client = SkillClient(agent_name=args.agent_name, agent_version=args.agent_version,
                             agent_model=args.agent_model)
        result = client.get_params_field_options(args.task, args.field_path)
        _print_json(_attach_client_notices(result, client))
        return 0
    except ConfigFetchError as error:
        _print_json(_config_failure_envelope(error))
    except OptionsSourceError as error:
        _print_json(_options_failure(error, client))
    except (ValueError, ParameterValidationError) as error:
        _print_json(_attach_client_notices({
            "error": "invalid_task_parameters", "skill_status": "failed",
            "failure_stage": "validate_options_query", "detail": str(error),
        }, client))
    return 1


def cmd_run_task(args: argparse.Namespace) -> int:
    # Ensure imports resolve (client, ai, sign_sdk live alongside this file)
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    from client import ConfigFetchError, ConsumeDeniedError, SkillClient

    params = DEFAULT_PARAMS
    if args.params_json:
        try:
            params = json.loads(args.params_json)
        except json.JSONDecodeError as e:
            print(json.dumps({"error": "invalid --params JSON", "detail": str(e)}))
            return 1

    profile = None
    if args.profile_json:
        try:
            profile = json.loads(args.profile_json)
        except json.JSONDecodeError as e:
            print(json.dumps({"error": "invalid --profile JSON", "detail": str(e)}))
            return 1
        if not isinstance(profile, dict):
            print(json.dumps({"error": "--profile must be a JSON object"}))
            return 1

    client = None
    try:
        client = SkillClient(
            agent_name=args.agent_name,
            agent_version=args.agent_version,
            agent_model=args.agent_model,
        )

        def _on_async_submitted(tid: str) -> None:
            _save_submitted_checkpoint(args.task, args.input, tid)

        result = client.run_task(
            args.task,
            args.input,
            params,
            on_async_submitted=_on_async_submitted,
            profile=profile,
        )
        if not isinstance(result, dict):
            fail = {
                "error": "invalid_result",
                "skill_status": "failed",
                "detail": repr(result),
                "agent_instruction": (
                    "Unexpected non-object result from the SDK. Treat as failure; "
                    "check logs and retry."
                ),
            }
            _print_json(_merge_pipeline_trace(fail, client, success=False))
            _save_task_record(_task_record_from_result(args.task, args.input, fail))
            return 1
        if _is_failed_cli_result(result):
            _print_json(_merge_pipeline_trace(result, client, success=False))
            _save_task_record(_task_record_from_result(args.task, args.input, result))
            return 1
        out = _success_envelope(args.task, result)
        _print_json(_merge_pipeline_trace(out, client, success=True))
        _save_task_record(_task_record_from_result(args.task, args.input, out))
    except ConfigFetchError as e:
        fail = _config_failure_envelope(e)
        _print_json(fail)
        _save_task_record(_task_record_from_result(args.task, args.input, fail))
        return 1
    except SchemaConfigurationError as e:
        _print_json(_schema_failure(e, client))
        return 1
    except OptionsSourceError as e:
        _print_json(_options_failure(e, client))
        return 1
    except InputMediaValidationError as e:
        _print_json(_attach_client_notices({
            "error": "invalid_input_media", "skill_status": "failed",
            "failure_stage": "validate_input_media", "detail": str(e),
        }, client))
        return 1
    except ParameterValidationError as e:
        _print_json(_attach_client_notices({
            "error": "invalid_task_parameters", "skill_status": "failed",
            "failure_stage": "validate_task_parameters", "detail": str(e),
        }, client))
        return 1
    except ConsumeDeniedError as e:
        fail = _envelope_consume_denied(e, args.task)
        if client is not None:
            _merge_pipeline_trace(fail, client, success=False)
        _print_json(fail)
        _save_task_record(_task_record_from_result(args.task, args.input, fail))
        return 1
    except Exception as e:
        err: dict = {"error": str(e), "skill_status": "failed"}
        if client is not None:
            _merge_pipeline_trace(err, client, success=False)
        _print_json(err)
        _save_task_record(
            _task_record_from_result(
                args.task, args.input, None, error_message=str(e)
            )
        )
        return 1
    return 0


def cmd_query_task(args: argparse.Namespace) -> int:
    """Resume polling by task_id (no upload, no consume)."""
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    from client import SkillClient

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
                "agent_instruction": (
                    "Unexpected non-object result from poll_task_status. Treat as failure."
                ),
            }
            _print_json(_merge_pipeline_trace(fail, client, success=False))
            _save_task_record(_task_record_from_result(task_label, "", fail))
            return 1
        if _is_failed_cli_result(result):
            _print_json(_merge_pipeline_trace(result, client, success=False))
            _save_task_record(
                _task_record_from_result(task_label, "", result)
            )
            return 1
        out = _success_envelope(task_label, result, resume=True)
        _print_json(_merge_pipeline_trace(out, client, success=True))
        _save_task_record(_task_record_from_result(task_label, "", out))
    except Exception as e:
        err = {"error": str(e), "skill_status": "failed"}
        if client is not None:
            _merge_pipeline_trace(err, client, success=False)
        _print_json(err)
        _save_task_record(
            _task_record_from_result(task_label, "", None, error_message=str(e))
        )
        return 1
    return 0


def cmd_spawn_run_task(args: argparse.Namespace) -> int:
    try:
        resolve_channel(getattr(args, "deliver_channel", None))
    except ValueError as error:
        _print_json({"error": "delivery_unavailable", "skill_status": "failed", "detail": str(error)})
        return 1
    params_json = getattr(args, "params_json", "") or ""
    try:
        params = json.loads(params_json) if params_json else DEFAULT_PARAMS
    except json.JSONDecodeError as error:
        print(json.dumps({"error": "invalid --params JSON", "detail": str(error)}))
        return 1
    task = (args.task or "").strip()
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    from client import ConfigFetchError, SkillClient

    client = None
    try:
        client = SkillClient(
            agent_name=args.agent_name,
            agent_version=args.agent_version,
            agent_model=args.agent_model,
        )
        selection = client.resolve_task(task)
        mode = client.task_catalog.get("mode")
    except ConfigFetchError as e:
        _print_json(_config_failure_envelope(e))
        return 1
    except Exception as e:
        out = {
            "error": "task_not_available",
            "skill_status": "failed",
            "failure_stage": "resolve_remote_task",
            "detail": str(e),
            "agent_instruction": (
                "Stop. Run catalog discovery and select only a returned task; "
                "do not use a local fallback."
            ),
        }
        _print_json(_attach_client_notices(out, client))
        return 1

    try:
        client.validate_input_media(selection, args.input)
    except InputMediaValidationError as error:
        _print_json(_attach_client_notices({
            "error": "invalid_input_media", "skill_status": "failed",
            "failure_stage": "validate_input_media", "detail": str(error),
        }, client))
        return 1
    media_type = selection.get("media_type") or ""
    if "params_schema" in selection:
        try:
            client.validate_task_parameters(selection, params)
        except SchemaConfigurationError as error:
            _print_json(_schema_failure(error, client))
            return 1
        except OptionsSourceError as error:
            _print_json(_options_failure(error, client))
            return 1
        except ParameterValidationError as error:
            _print_json(_attach_client_notices({
                "error": "invalid_task_parameters", "skill_status": "failed",
                "failure_stage": "validate_task_parameters", "detail": str(error),
            }, client))
            return 1
    confirmed_legacy_video = mode == "legacy" and task in VIDEO_TASKS
    if not _is_video_task(task, media_type) and not confirmed_legacy_video:
        out = {
            "error": "spawn_video_tasks_only",
            "skill_status": "failed",
            "detail": (
                "spawn-run-task accepts only a V2 catalog entry with "
                "media_type=video, or a server-confirmed legacy video alias."
            ),
            "task_name": task,
            "agent_instruction": (
                "Use run-task in the main session for image tasks. Select the "
                "exact video task name or confirmed legacy alias from catalog output."
            ),
        }
        _print_json(_attach_client_notices(out, client))
        return 1
    payload = build_spawn_run_task(
        task=task,
        input_src=args.input,
        params_json=getattr(args, "params_json", "") or "",
        deliver_to=getattr(args, "deliver_to", None),
        deliver_channel=getattr(args, "deliver_channel", None),
        run_timeout_seconds=args.run_timeout_seconds,
        agent_name=args.agent_name,
        agent_version=args.agent_version,
        agent_model=args.agent_model,
        media_type="video",
        profile_json=getattr(args, "profile_json", "") or "",
    )
    _print_json(_attach_client_notices(payload, client))
    return 0


def cmd_last_task(_args: argparse.Namespace) -> int:
    if not LAST_TASK_FILE.is_file():
        _print_json({"message": "No saved task yet.", "record": None})
        return 0
    try:
        with open(LAST_TASK_FILE, encoding="utf-8") as f:
            record = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        _print_json({"error": "failed to read last_task.json", "detail": str(e)})
        return 1
    _print_json(record)
    return 0


def cmd_history(_args: argparse.Namespace) -> int:
    _ensure_state_dir()
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    files = sorted(HISTORY_DIR.glob("task_*.json"))
    jobs: list = []
    for path in files[-50:]:
        try:
            with open(path, encoding="utf-8") as f:
                jobs.append(json.load(f))
        except (json.JSONDecodeError, OSError):
            continue
    _print_json({"jobs": jobs, "count": len(jobs)})
    return 0


def cmd_resolve_input(args: argparse.Namespace) -> int:
    try:
        import requests
    except ImportError:
        _print_json(
            {
                "error": "requests not installed",
                "install_command": "pip install -r scripts/requirements.txt",
            }
        )
        return 1

    out_dir = Path(args.output_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    file_bytes: bytes | None = None
    filename = "input.bin"

    if getattr(args, "file", None):
        p = Path(args.file).expanduser()
        if not p.is_file():
            _print_json({"error": f'文件不存在：{args.file}'})
            return 1
        max_b = skill_config.url_download_max_bytes()
        if p.stat().st_size > max_b:
            _print_json(
                {"error": '文件过大', "max_bytes": max_b}
            )
            return 1
        file_bytes = p.read_bytes()
        filename = p.name

    elif getattr(args, "url", None):
        url = args.url.strip()
        if not url.startswith(("http://", "https://")):
            _print_json({"error": '仅支持 http:// 和 https:// URL'})
            return 1
        url_to = skill_config.url_download_timeout_tuple()
        r = requests.get(
            url,
            stream=True,
            timeout=url_to,
            headers={
                "User-Agent": skill_config.USER_AGENT,
            },
        )
        if r.status_code != 200:
            _print_json({"error": f'下载失败：HTTP {r.status_code}'})
            return 1
        chunks: list[bytes] = []
        total = 0
        max_b = skill_config.url_download_max_bytes()
        for chunk in r.iter_content(chunk_size=65536):
            total += len(chunk)
            if total > max_b:
                _print_json({"error": '下载的文件过大', "max_bytes": max_b})
                return 1
            chunks.append(chunk)
        file_bytes = b"".join(chunks)
        url_path = url.split("?")[0]
        ext_from_url = (
            url_path.rsplit(".", 1)[-1].lower() if "." in url_path else ""
        )
        if ext_from_url in (
            "jpg",
            "jpeg",
            "png",
            "webp",
            "gif",
            "mp4",
            "mov",
            "webm",
        ):
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

    elif getattr(args, "telegram_file_id", None):
        token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
        if not token:
            _print_json(
                {
                    "error": "TELEGRAM_BOT_TOKEN not set",
                    "hint": '请勿通过命令行参数传递 Bot Token（可被 ps 查看）。',
                }
            )
            return 1
        r = requests.get(
            f"https://api.telegram.org/bot{token}/getFile",
            params={"file_id": args.telegram_file_id},
            timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
        )
        r.raise_for_status()
        data = r.json()
        if not data.get("ok"):
            _print_json({"error": "Telegram getFile failed", "detail": data})
            return 1
        file_path = data["result"]["file_path"]
        ext_from_path = (
            file_path.rsplit(".", 1)[-1].lower() if "." in file_path else "jpg"
        )
        extension = (
            ext_from_path
            if ext_from_path
            in ("jpg", "jpeg", "png", "webp", "gif", "mp4", "mov", "webm")
            else "jpg"
        )
        filename = f"tg_{uuid.uuid4().hex[:8]}.{extension}"
        dl_url = f"https://api.telegram.org/file/bot{token}/{file_path}"
        r2 = requests.get(
            dl_url,
            timeout=skill_config.url_download_timeout_tuple(),
            headers={
                "User-Agent": skill_config.USER_AGENT,
            },
        )
        r2.raise_for_status()
        file_bytes = r2.content
        max_b = skill_config.url_download_max_bytes()
        if len(file_bytes) > max_b:
            _print_json(
                {"error": 'Telegram 文件过大', "max_bytes": max_b}
            )
            return 1

    elif getattr(args, "feishu_image_key", None):
        if not args.feishu_message_id:
            _print_json(
                {"error": '使用 --feishu-image-key 时必须提供 --feishu-message-id'}
            )
            return 1
        feishu_token = (
            args.feishu_app_token or os.environ.get("FEISHU_APP_TOKEN", "")
        ).strip()
        if not feishu_token:
            _print_json(
                {"error": '请配置 FEISHU_APP_TOKEN 或提供 --feishu-app-token'}
            )
            return 1
        r = requests.get(
            f"https://open.feishu.cn/open-apis/im/v1/messages/"
            f"{args.feishu_message_id}/resources/{args.feishu_image_key}",
            params={"type": "image"},
            headers={"Authorization": f"Bearer {feishu_token}"},
            timeout=skill_config.url_download_timeout_tuple(),
        )
        if r.status_code != 200:
            _print_json(
                {"error": f"Feishu download failed: HTTP {r.status_code}"}
            )
            return 1
        file_bytes = r.content
        max_b = skill_config.url_download_max_bytes()
        if len(file_bytes) > max_b:
            _print_json(
                {"error": '飞书资源过大', "max_bytes": max_b}
            )
            return 1
        extension = "jpg"
        ct = r.headers.get("Content-Type", "")
        if "png" in ct:
            extension = "png"
        elif "webp" in ct:
            extension = "webp"
        filename = f"feishu_{uuid.uuid4().hex[:8]}.{extension}"

    else:
        _print_json(
            {
                "error": '请提供以下任一参数：--file、--url、--telegram-file-id、--feishu-image-key（需配合 --feishu-message-id）',
            }
        )
        return 1

    dest = out_dir / f"vmake_in_{uuid.uuid4().hex[:10]}_{filename}"
    dest.write_bytes(file_bytes)  # type: ignore[arg-type]
    _print_json(
        {
            "path": str(dest.resolve()),
            "filename": filename,
            "bytes": len(file_bytes),  # type: ignore[arg-type]
        }
    )
    return 0


def cmd_upload(args: argparse.Namespace) -> int:
    """Preserve the domestic upload command without consuming task quota."""
    from client import SkillClient

    if not os.path.isfile(args.file):
        _print_json({"error": f'文件不存在：{args.file}', "status": "failed"})
        return 1
    try:
        client = SkillClient()
        _print_json({"status": "success", "url_data": client.api.upload_file(args.file)})
        return 0
    except Exception as e:
        _print_json({"error": str(e), "status": "failed"})
        return 1


def cmd_notify(args: argparse.Namespace) -> int:
    """Preserve domestic notification delivery independently of task submission."""
    try:
        cover_url = getattr(args, "cover_url", "") or ""
        duration_ms = getattr(args, "duration_ms", None)
        if args.type == "image" and (cover_url or duration_ms is not None):
            raise ValueError('--cover-url 和 --duration-ms 仅适用于视频')
        from notifications import get_notifier
        notifier = get_notifier(args.channel)
        if args.type == "image":
            result = notifier.send_image(args.source, args.to, args.caption or "")
        else:
            options = {"video_url": args.video_url or "", "caption": args.caption or ""}
            if cover_url:
                options["cover_url"] = cover_url
            if duration_ms is not None:
                options["duration_ms"] = duration_ms
            result = notifier.send_video(args.source, args.to, **options)
        _print_json(result)
        return 0 if result.get("status") == "ok" else 1
    except Exception as e:
        _print_json({"error": str(e), "status": "failed"})
        return 1


def cmd_capabilities(_args):
    """Report bundled modules without fetching config or consuming quota."""
    _print_json(bundled_features())
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description='开拍 Skill 命令行工具')
    parser.add_argument("--ak", help='Access Key（建议使用 MT_AK 或 scripts/.env）')
    parser.add_argument("--sk", help='Secret Key（建议使用 MT_SK 或 scripts/.env）')
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("capabilities", help='查看包内模块（不联网、不扣额度）').set_defaults(func=cmd_capabilities)

    p_pre = sub.add_parser("preflight", help='检查 AK/SK，输出 ok 或 missing')
    p_pre.set_defaults(func=cmd_preflight)

    p_dep = sub.add_parser("install-deps", help='按需安装依赖')
    p_dep.set_defaults(func=cmd_install_deps)

    p_catalog = sub.add_parser(
        "catalog",
        help='仅查询服务端任务目录（不上传、不扣额度、不提交算法任务）',
    )
    p_catalog.add_argument(
        "--media-type",
        default="",
        help='可选的服务端目录筛选条件',
    )
    p_catalog.set_defaults(func=cmd_catalog)

    p_options = sub.add_parser(
        "params-field-options", help='查询已发布参数字段的完整选项列表（不扣额度）')
    p_options.add_argument("--task", required=True)
    p_options.add_argument("--field-path", required=True, help='相对 params 根的 JSON Pointer，例如 /parameter/material_id')
    p_options.set_defaults(func=cmd_params_field_options)

    p_run = sub.add_parser("run-task", help='执行算法任务')
    p_run.add_argument(
        "--task",
        required=True,
        help='准确的 V2 material_id（推荐）、唯一名称或服务端返回的旧版别名',
    )
    p_run.add_argument(
        "--input", action="append", help='图片或视频 URL、本地路径；目录规则允许时可重复传入 --input'
    )
    p_run.add_argument(
        "--params",
        dest="params_json",
        default="",
        help='可选的调用参数 JSON 对象（默认：{"parameter":{"rsp_media_type":"url"}}）',
    )
    p_run.add_argument(
        "--profile",
        dest="profile_json",
        default="",
        help='可选的 JSON 对象，用于覆盖服务端输入 profile',
    )
    p_run.set_defaults(func=cmd_run_task)

    p_query = sub.add_parser(
        "query-task",
        help='按 task_id 恢复轮询（不重新上传，使用提交时的 AK/SK）',
    )
    p_query.add_argument(
        "--task-id",
        required=True,
        dest="task_id",
        help='之前 run-task 或失败 JSON 中的完整任务 ID（task_id 或 data.result.id）',
    )
    p_query.add_argument(
        "--task",
        default="",
        help='成功 JSON 中 task_name 的可选标签（默认：query_task）',
    )
    p_query.set_defaults(func=cmd_query_task)

    p_spawn = sub.add_parser(
        "spawn-run-task",
        help='为服务端目录中的视频任务生成 sessions_spawn 参数',
    )
    p_spawn.add_argument(
        "--task",
        required=True,
        help='准确的 V2 视频 material_id（推荐）、唯一名称或服务端返回的旧版别名',
    )
    p_spawn.add_argument("--input", action="append",
                         help='素材 URL 或本地路径；目录规则允许时可重复传入 --input')
    p_spawn.add_argument(
        "--params",
        dest="params_json",
        default="",
        help='可选的 --params JSON（与 run-task 相同）',
    )
    p_spawn.add_argument(
        "--profile",
        dest="profile_json",
        default="",
        help='可选的 --profile JSON（与 run-task 相同）',
    )
    p_spawn.add_argument(
        "--deliver-to",
        default=None,
        help='飞书 oc_/ou_、Telegram chat_id、Discord channel_id 等接收方',
    )
    p_spawn.add_argument(
        "--deliver-channel",
        default=None,
        help='包内投递渠道：' + (", ".join(bundled_channels()) or "none") + '；也可指定宿主渠道或 none',
    )
    p_spawn.add_argument(
        "--run-timeout-seconds",
        type=int,
        default=SPAWN_DEFAULT_TIMEOUT_SECONDS,
        help=(
            f'sessions_spawn 的 runTimeoutSeconds（默认 {SPAWN_DEFAULT_TIMEOUT_SECONDS}；缩短时间可能导致超时）'
        ),
    )
    p_spawn.set_defaults(func=cmd_spawn_run_task)

    for command in (p_catalog, p_run, p_spawn, p_options):
        for field in ("name", "version", "model"):
            command.add_argument("--agent-" + field, default=None,
                                 help='可选的调用方 ' + field + '；默认读取 SKILL_AGENT_' + field.upper())

    p_last = sub.add_parser("last-task", help='查看最近一次 run-task/query-task 的 JSON 记录')
    p_last.set_defaults(func=cmd_last_task)

    sub.add_parser("history", help='查看最近的任务记录（最多 50 条）').set_defaults(
        func=cmd_history
    )

    p_res = sub.add_parser(
        "resolve-input",
        help='将聊天附件或 URL 下载到本地，供 --input 使用',
    )
    p_res.add_argument("--file", help='本地文件路径（使用唯一名称复制到输出目录）')
    p_res.add_argument("--url", help='需要下载的 HTTP(S) URL')
    p_res.add_argument(
        "--telegram-file-id",
        dest="telegram_file_id",
        help='Telegram file_id（需配置 TELEGRAM_BOT_TOKEN）',
    )
    p_res.add_argument(
        "--feishu-message-id",
        dest="feishu_message_id",
        default="",
        help='飞书消息 ID（配合 --feishu-image-key 使用）',
    )
    p_res.add_argument(
        "--feishu-image-key",
        dest="feishu_image_key",
        help='飞书图片资源 key',
    )
    p_res.add_argument(
        "--feishu-app-token",
        dest="feishu_app_token",
        default="",
        help='飞书 tenant token（也可配置 FEISHU_APP_TOKEN）',
    )
    p_res.add_argument(
        "--output-dir",
        default="/tmp",
        help='下载文件保存目录（默认：/tmp）',
    )
    p_res.set_defaults(func=cmd_resolve_input)

    p_list = sub.add_parser("list-tasks", help='兼容旧版的服务端目录查询命令')
    p_list.add_argument("--media-type", default="")
    p_list.set_defaults(func=cmd_catalog, agent_name=None, agent_version=None, agent_model=None)

    p_upload = sub.add_parser("upload", help='上传本地文件（不扣任务额度）')
    p_upload.add_argument("--file", required=True, help='本地文件路径')
    p_upload.set_defaults(func=cmd_upload)

    if bundled_channels():
        p_notify = sub.add_parser("notify", help='通过包内通知渠道发送结果')
        p_notify.add_argument("--channel", required=True, choices=bundled_channels())
        p_notify.add_argument("--type", required=True, choices=["image", "video"])
        p_notify.add_argument("--source", required=True)
        p_notify.add_argument("--to", required=True)
        p_notify.add_argument("--caption")
        p_notify.add_argument("--video-url")
        p_notify.add_argument("--cover-url", default="", help='视频封面 URL（仅用于视频）')
        p_notify.add_argument("--duration-ms", type=int, default=None,
                              help='视频时长，所有渠道统一使用毫秒（仅用于视频）')
        p_notify.set_defaults(func=cmd_notify)

    args = parser.parse_args()
    if isinstance(getattr(args, "input", None), list) and len(args.input) == 1:
        args.input = args.input[0]
    # Legacy explicit credentials stay within this invocation, never worker payloads.
    previous = {key: os.environ.get(key) for key in ("MT_AK", "MT_SK")}
    try:
        if args.ak is not None:
            os.environ["MT_AK"] = args.ak
        if args.sk is not None:
            os.environ["MT_SK"] = args.sk
        return args.func(args)
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


if __name__ == "__main__":
    raise SystemExit(main())
