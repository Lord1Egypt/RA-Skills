#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run the KeplerJAI news pipeline end-to-end.

Supported modes:
1. Use an existing stage1 output file.
2. Trigger OpenClaw stage1 collection automatically, save the raw reply locally,
   then continue with validate -> publish -> format.
"""

from __future__ import annotations

import argparse
import io
import json
import locale
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

DEFAULT_STAGE1_AGENT_ID = "admin-expert"
DEFAULT_STAGE1_TIMEOUT = 900
SENSITIVE_OPTION_NAMES = {"--bearer-token", "--cookie"}
PREFERRED_BEARER_ENV_KEYS = ("KEPLERAI_API_KEY", "KEPLERJAI_BEARER_TOKEN")
PREFERRED_COOKIE_ENV_KEYS = ("KEPLERAI_COOKIE", "KEPLERJAI_COOKIE")
SENSITIVE_ENV_KEYS = set(PREFERRED_BEARER_ENV_KEYS + PREFERRED_COOKIE_ENV_KEYS)
STATE_NAMESPACE = "keplerjai-bulletin-publish"
DEFAULT_AGENT_WORKSPACE_NAME = "admin-expert"
AGENT_WORKSPACE_ENV_KEY = "OPENCLAW_AGENT_WORKSPACE"
STAGE1_PROMPT_OUTPUT_TOKEN = "__STAGE1_OUTPUT_PATH__"


def fail(message: str, exit_code: int = 1) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(exit_code)


def timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log_line(log_path: Path, message: str) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(f"[{timestamp()}] {message}\n")


def announce(message: str) -> None:
    print(message, flush=True)


def mask_secret(value: str) -> str:
    if not value:
        return ""
    if len(value) <= 8:
        return "***"
    return f"{value[:4]}***{value[-4:]}"


def sanitize_command(cmd: list[str]) -> str:
    sanitized: list[str] = []
    skip_next = False

    for index, part in enumerate(cmd):
        if skip_next:
            skip_next = False
            continue

        if part in SENSITIVE_OPTION_NAMES:
            sanitized.append(part)
            if index + 1 < len(cmd):
                sanitized.append(mask_secret(cmd[index + 1]))
                skip_next = True
            continue

        if part.startswith("--bearer-token="):
            sanitized.append("--bearer-token=" + mask_secret(part.split("=", 1)[1]))
            continue
        if part.startswith("--cookie="):
            sanitized.append("--cookie=" + mask_secret(part.split("=", 1)[1]))
            continue

        sanitized.append(part)

    return " ".join(sanitized)


def sanitize_text(text: str, extra_secrets: list[str] | None = None) -> str:
    sanitized = text
    for env_key in SENSITIVE_ENV_KEYS:
        value = os.getenv(env_key, "").strip()
        if value:
            sanitized = sanitized.replace(value, mask_secret(value))
    for value in extra_secrets or []:
        value = value.strip()
        if value:
            sanitized = sanitized.replace(value, mask_secret(value))
    return sanitized


def first_nonempty_env(keys: tuple[str, ...]) -> str:
    for key in keys:
        value = os.getenv(key, "").strip()
        if value:
            return value
    return ""


def resolve_agent_workspace_name(raw: str | None) -> str:
    value = (raw or "").strip()
    return value or DEFAULT_AGENT_WORKSPACE_NAME


def resolve_external_state_dir(skill_root: Path, agent_workspace_name: str) -> Path:
    return skill_root.parent / resolve_agent_workspace_name(agent_workspace_name) / STATE_NAMESPACE


def decode_subprocess_output(raw: bytes) -> str:
    encodings = [
        "utf-8",
        "utf-8-sig",
        locale.getpreferredencoding(False),
        "gbk",
    ]
    seen: set[str] = set()
    for encoding in encodings:
        if not encoding:
            continue
        encoding = encoding.lower()
        if encoding in seen:
            continue
        seen.add(encoding)
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def run_and_log(
    cmd: list[str],
    log_path: Path,
    step_name: str,
    *,
    extra_secrets: list[str] | None = None,
) -> subprocess.CompletedProcess[str]:
    announce(f"[{step_name}] 开始执行")
    log_line(log_path, f"START {step_name}: {sanitize_command(cmd)}")
    raw_result = subprocess.run(cmd, capture_output=True, text=False)
    result = subprocess.CompletedProcess(
        args=raw_result.args,
        returncode=raw_result.returncode,
        stdout=decode_subprocess_output(raw_result.stdout or b""),
        stderr=decode_subprocess_output(raw_result.stderr or b""),
    )

    if result.stdout.strip():
        log_line(
            log_path,
            f"{step_name} STDOUT:\n{sanitize_text(result.stdout.rstrip(), extra_secrets)}",
        )
    if result.stderr.strip():
        log_line(
            log_path,
            f"{step_name} STDERR:\n{sanitize_text(result.stderr.rstrip(), extra_secrets)}",
        )

    if result.returncode != 0:
        log_line(log_path, f"FAIL {step_name}: exit={result.returncode}")
        fail(f"{step_name} 失败，详情见日志: {log_path}", result.returncode)

    log_line(log_path, f"OK {step_name}")
    announce(f"[{step_name}] 已完成")
    return result


def load_auth_defaults(state_dir: Path) -> dict[str, str]:
    auth: dict[str, str] = {}

    env_token = first_nonempty_env(PREFERRED_BEARER_ENV_KEYS)
    env_cookie = first_nonempty_env(PREFERRED_COOKIE_ENV_KEYS)
    if env_token:
        auth["bearer_token"] = env_token
    if env_cookie:
        auth["cookie"] = env_cookie

    return auth


def read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "gbk"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def resolve_openclaw_command() -> str:
    candidates = [
        "openclaw.cmd",
        "openclaw",
        "openclaw.ps1",
        r"C:\nvm4w\nodejs\openclaw.cmd",
        r"C:\nvm4w\nodejs\openclaw",
        r"C:\nvm4w\nodejs\openclaw.ps1",
    ]

    for candidate in candidates:
        resolved = shutil.which(candidate) if not os.path.isabs(candidate) else candidate
        if resolved and Path(resolved).exists():
            return resolved

    fail("未找到 openclaw 可执行文件，请确认 OpenClaw 已正确安装。")


def collect_stage1_reply_text(agent_result: Any) -> str:
    if isinstance(agent_result, dict):
        if "item_count" in agent_result and "items" in agent_result:
            return json.dumps(agent_result, ensure_ascii=False, indent=2).strip()
        payloads = agent_result.get("payloads")
        if not isinstance(payloads, list):
            result_block = agent_result.get("result")
            if isinstance(result_block, dict):
                payloads = result_block.get("payloads")
        if isinstance(payloads, list):
            parts: list[str] = []
            for payload in payloads:
                if not isinstance(payload, dict):
                    continue
                text = payload.get("text")
                if isinstance(text, str) and text.strip():
                    parts.append(text.strip())
            if parts:
                return "\n\n".join(parts).strip()
    if isinstance(agent_result, str):
        return agent_result.strip()
    return ""


def run_stage1_collection(
    *,
    skill_root: Path,
    stage1_prompt_path: Path,
    stage1_raw_path: Path,
    log_path: Path,
    stage1_agent_id: str,
    stage1_timeout: int,
    stage1_json_response_path: Path | None,
    openclaw_local: bool,
) -> None:
    if not stage1_prompt_path.exists():
        fail(f"未找到 stage1 prompt 文件: {stage1_prompt_path}")

    prompt_text = read_text(stage1_prompt_path).strip()
    if not prompt_text:
        fail(f"stage1 prompt 文件为空: {stage1_prompt_path}")

    prompt_text = prompt_text.replace(STAGE1_PROMPT_OUTPUT_TOKEN, str(stage1_raw_path))
    announce("正在启动 OpenClaw stage1 采集")
    announce("正在注入提示词并开始采集，预计耗时较长，大约 10 分钟，请耐心等待")

    command = [
        resolve_openclaw_command(),
        "agent",
        "--agent",
        stage1_agent_id,
        "--timeout",
        str(stage1_timeout),
        "--message",
        prompt_text,
        "--json",
    ]
    if openclaw_local:
        command.append("--local")

    result = run_and_log(command, log_path, "collect_stage1")

    raw_stdout = result.stdout.strip()
    if not raw_stdout:
        fail("collect_stage1 没有返回任何内容，请查看日志。")

    parsed_response: Any
    try:
        parsed_response = json.loads(raw_stdout)
    except json.JSONDecodeError:
        parsed_response = raw_stdout

    if stage1_json_response_path is not None:
        stage1_json_response_path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(parsed_response, str):
            stage1_json_response_path.write_text(parsed_response + "\n", encoding="utf-8")
        else:
            stage1_json_response_path.write_text(
                json.dumps(parsed_response, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

    reply_text = collect_stage1_reply_text(parsed_response)
    if not reply_text:
        fail("无法从 OpenClaw agent 返回结果中提取 stage1 文本，请查看日志。")

    stage1_raw_path.parent.mkdir(parents=True, exist_ok=True)
    stage1_raw_path.write_text(reply_text + "\n", encoding="utf-8")
    log_line(log_path, f"stage1 raw reply saved: {stage1_raw_path}")
    announce("stage1 采集完成，原始结果已落盘")


def main() -> int:
    skill_root = Path(__file__).resolve().parent.parent
    script_dir = skill_root / "scripts"
    default_agent_workspace = resolve_agent_workspace_name(
        os.getenv(AGENT_WORKSPACE_ENV_KEY, DEFAULT_AGENT_WORKSPACE_NAME)
    )

    parser = argparse.ArgumentParser(description="运行 KeplerJAI 新闻流水线")
    parser.add_argument(
        "--agent-workspace",
        default=default_agent_workspace,
        help=(
            "运行产物写入哪个 agent 工作空间目录；"
            f"默认优先读取环境变量 {AGENT_WORKSPACE_ENV_KEY}，否则使用 {DEFAULT_AGENT_WORKSPACE_NAME}"
        ),
    )
    parser.add_argument(
        "--stage1-raw",
        help="OpenClaw stage1 原始回复文件路径",
    )
    parser.add_argument(
        "--stage1-json",
        help="归一化后的 stage1 JSON 输出路径",
    )
    parser.add_argument(
        "--publish-result",
        help="发布结果文件路径",
    )
    parser.add_argument(
        "--final-message",
        help="最终汇总文案输出路径",
    )
    parser.add_argument(
        "--log-file",
        help="流水线日志文件路径",
    )
    parser.add_argument(
        "--stage1-prompt",
        default=str(skill_root / "stage1-task-prompt.txt"),
        help="stage1 prompt 文件路径",
    )
    parser.add_argument(
        "--stage1-agent-response",
        help="OpenClaw agent JSON 返回落盘路径",
    )
    parser.add_argument(
        "--collect-stage1",
        action="store_true",
        help="先自动触发 OpenClaw stage1 采集，再继续后续步骤",
    )
    parser.add_argument(
        "--collect-only",
        action="store_true",
        help="只执行 OpenClaw stage1 采集并落盘，不继续发布",
    )
    parser.add_argument(
        "--stage1-agent-id",
        default=DEFAULT_STAGE1_AGENT_ID,
        help=f"执行 stage1 的 OpenClaw agent id，默认 {DEFAULT_STAGE1_AGENT_ID}",
    )
    parser.add_argument(
        "--stage1-timeout",
        type=int,
        default=DEFAULT_STAGE1_TIMEOUT,
        help=f"stage1 采集超时秒数，默认 {DEFAULT_STAGE1_TIMEOUT}",
    )
    parser.add_argument(
        "--openclaw-local",
        action="store_true",
        help="调用 openclaw agent 时强制附加 --local",
    )
    parser.add_argument("--api-url", help="覆盖发布接口地址")
    parser.add_argument("--frontend-url", help="覆盖前台链接模板")
    parser.add_argument("--bearer-token", help="Bearer Token")
    parser.add_argument("--cookie", help="Cookie")
    parser.add_argument("--header", action="append", default=[], help="附加请求头，格式 Key: Value")
    parser.add_argument("--timeout", type=int, default=30, help="发布接口超时秒数")
    parser.add_argument("--insecure", action="store_true", help="忽略 HTTPS 证书校验")
    parser.add_argument("--dry-run", action="store_true", help="只校验并生成预览，不真实发布")
    parser.add_argument("--footer", help="覆盖最终文案尾注")
    args = parser.parse_args()

    state_dir = resolve_external_state_dir(skill_root, args.agent_workspace)
    stage1_raw = Path(args.stage1_raw or state_dir / "stage1-output.txt").expanduser().resolve()
    stage1_json = Path(args.stage1_json or state_dir / "stage1-output.normalized.json").expanduser().resolve()
    publish_result = Path(args.publish_result or state_dir / "publish-result.json").expanduser().resolve()
    final_message = Path(args.final_message or state_dir / "final-message.txt").expanduser().resolve()
    log_file = Path(args.log_file or state_dir / "pipeline.log").expanduser().resolve()
    stage1_prompt = Path(args.stage1_prompt).expanduser().resolve()
    stage1_agent_response = Path(
        args.stage1_agent_response or state_dir / "stage1-agent-response.json"
    ).expanduser().resolve()

    state_dir.mkdir(parents=True, exist_ok=True)
    auth_defaults = load_auth_defaults(state_dir)

    log_line(log_file, "==== PIPELINE RUN START ====")
    log_line(log_file, f"stage1 raw: {stage1_raw}")
    log_line(log_file, f"stage1 json: {stage1_json}")
    log_line(log_file, f"publish result: {publish_result}")
    log_line(log_file, f"final message: {final_message}")
    announce("流水线已启动")
    announce(f"日志文件: {log_file}")

    if args.collect_stage1 or args.collect_only:
        run_stage1_collection(
            skill_root=skill_root,
            stage1_prompt_path=stage1_prompt,
            stage1_raw_path=stage1_raw,
            log_path=log_file,
            stage1_agent_id=args.stage1_agent_id,
            stage1_timeout=args.stage1_timeout,
            stage1_json_response_path=stage1_agent_response,
            openclaw_local=args.openclaw_local,
        )

    if args.collect_only:
        log_line(log_file, "SKIP remaining pipeline: collect-only mode")
        log_line(log_file, "==== PIPELINE RUN END ====")
        print("stage1 自动采集完成。")
        print(f"原始回复: {stage1_raw}")
        print(f"agent JSON: {stage1_agent_response}")
        print(f"日志文件: {log_file}")
        return 0

    if not stage1_raw.exists():
        fail(f"未找到 stage1 原始回复文件: {stage1_raw}")

    validate_cmd = [
        sys.executable,
        str(script_dir / "validate_stage1_json.py"),
        str(stage1_raw),
        "-o",
        str(stage1_json),
    ]
    announce("正在校验并归一化 stage1 JSON")
    run_and_log(validate_cmd, log_file, "validate_stage1")

    publish_cmd = [
        sys.executable,
        str(script_dir / "publish_bulletins.py"),
        str(stage1_json),
        "-o",
        str(publish_result),
        "--timeout",
        str(args.timeout),
    ]
    if args.api_url:
        publish_cmd.extend(["--api-url", args.api_url])
    if args.frontend_url:
        publish_cmd.extend(["--frontend-url", args.frontend_url])
    bearer_token = args.bearer_token or auth_defaults.get("bearer_token", "")
    cookie = args.cookie or auth_defaults.get("cookie", "")
    if bearer_token:
        publish_cmd.extend(["--bearer-token", bearer_token])
        log_line(log_file, "auth: using bearer token from cli/auth defaults")
    if cookie:
        publish_cmd.extend(["--cookie", cookie])
        log_line(log_file, "auth: using cookie from cli/auth defaults")
    for header in args.header:
        publish_cmd.extend(["--header", header])
    if args.insecure:
        publish_cmd.append("--insecure")
    if args.dry_run:
        publish_cmd.append("--dry-run")
    announce("正在调用 KeplerJAI API 发布简讯")
    run_and_log(
        publish_cmd,
        log_file,
        "publish_bulletins",
        extra_secrets=[bearer_token, cookie],
    )

    if args.dry_run:
        log_line(log_file, "SKIP format_bulletins: dry-run mode")
        log_line(log_file, "==== PIPELINE RUN END ====")
        print("流水线 dry-run 完成。")
        print(f"原始回复: {stage1_raw}")
        print(f"归一化 JSON: {stage1_json}")
        print(f"发布预演结果: {publish_result}")
        print(f"日志文件: {log_file}")
        return 0

    format_cmd = [
        sys.executable,
        str(script_dir / "format_bulletins.py"),
        str(publish_result),
        "-o",
        str(final_message),
    ]
    if args.frontend_url:
        format_cmd.extend(["--frontend-url", args.frontend_url])
    if args.footer:
        format_cmd.extend(["--footer", args.footer])
    announce("正在生成最终文案")
    run_and_log(format_cmd, log_file, "format_bulletins")

    log_line(log_file, "==== PIPELINE RUN END ====")
    print("流水线执行完成。")
    print(f"原始回复: {stage1_raw}")
    print(f"归一化 JSON: {stage1_json}")
    print(f"发布结果: {publish_result}")
    print(f"最终文案: {final_message}")
    print(f"日志文件: {log_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
