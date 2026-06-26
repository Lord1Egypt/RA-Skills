#!/usr/bin/env python3
"""
OpenClaw autopilot orchestrator for GitHub repositories.

Features:
- Priority CLI orchestration: Codex CLI -> Gemini CLI -> Open Code CLI -> Claude Code CLI.
- Layered timeout controls:
  - 30s no output => terminate/switch.
  - >15min runtime => progress probe; 5min no clear response => terminate/switch.
  - >30min total runtime => terminate/switch.
  - repeated same operation >3 times => terminate/switch.
- Report-only audit (no code-level inspection):
  - run_status == success
  - test_pass_rate >= min threshold (default 90)
- Retry & switch policy:
  - per CLI, 2 consecutive audit failures => switch next CLI.
- Git flow:
  - sync dev branch only
  - commit + push on approved report
  - push failure => pause
- Continuous unattended loop (default 1h interval).
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import queue
import re
import shlex
import shutil
import subprocess
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib import error as urlerror
from urllib import request as urlrequest
from urllib.parse import quote


DEFAULT_CONFIG: Dict[str, Any] = {
    "repo_url": "https://github.com/<owner>/<repo>.git",
    "project_name": "",
    "task_requirement": "请对仓库执行完整迭代升级：分析、优化/重构、运行和全量测试，并给出可验证结果。",
    "caller_name": "自动化编排器",
    "init_slash_command": "/init",
    "branch": "dev",
    "working_root": "./runtime",
    "loop_interval_seconds": 3600,
    "report_min_pass_rate": 90.0,
    "require_code_changes": False,
    "require_non_doc_code_changes": False,
    "minimum_non_doc_files_changed": 0,
    "minimum_non_doc_lines_changed": 0,
    "max_audit_failures_per_cli": 2,
    "log_dir": "./logs",
    "report_path": ".openclaw/optimization_report.json",
    "prompt_path": ".openclaw/openclaw_task_prompt.md",
    "preserve_untracked_paths": [
        ".codex/",
        ".gemini/",
        ".claude/",
        ".open-code/",
    ],
    "never_commit_paths": [
        ".openclaw/openclaw_task_prompt.md",
        ".openclaw/optimization_report.json",
        ".openclaw/openclaw_init_prompt.md",
        ".openclaw/openclaw_init_remediate_prompt.md",
        ".codex/",
        ".gemini/",
        ".claude/",
        ".open-code/",
    ],
    "commit_message_template": "[迭代升级] {project} 核心优化：{core} | 测试通过率{rate}% | 变更：{changes}",
    "error_keywords": [
        "quota exceeded",
        "authentication failed",
        "permission denied",
        "rate limit",
        "invalid api key",
        "command not found",
    ],
    "timeouts": {
        "idle_seconds": 30,
        "progress_probe_after_seconds": 15 * 60,
        "progress_probe_wait_seconds": 5 * 60,
        "max_runtime_seconds": 30 * 60,
    },
    "init_phase": {
        "enabled": True,
        "force_reinit": False,
        "idle_seconds": 60,
        "max_runtime_seconds": 10 * 60,
    },
    "progress_probe_message": "进度校验：你是否仍在正常执行？请给出预计剩余时间和当前进度百分比。",
    "auto_confirm_reply": "yes",
    "fallback_report": {
        "enabled": True,
        "run_tests_on_missing_report": True,
        "test_command_candidates": [
            "python -m pytest -q",
            "pytest -q",
            "python -m unittest discover -q",
            "make test",
        ],
        "test_timeout_seconds": 1800,
    },
    "cli_tools": [
        {
            "name": "Codex CLI",
            "command": "codex exec -s workspace-write -c approval_policy=never -c model_reasoning_effort=high -C {repo_dir} --skip-git-repo-check - < {prompt_path}",
            "interactive_command": "codex --no-alt-screen -c model_reasoning_effort=high -C {repo_dir} \"$(cat {prompt_path})\"",
            "init_command": "codex exec -s workspace-write -c approval_policy=never -c model_reasoning_effort=high -C {repo_dir} --skip-git-repo-check - < {init_prompt_path}",
            "init_required_paths": [
                ".codex",
            ],
            "send_prompt_via_stdin": False,
            "enabled": True,
        },
        {
            "name": "Gemini CLI",
            "command": "gemini -y -o stream-json -p \"$(cat {prompt_path})\"",
            "interactive_command": "gemini",
            "init_command": "gemini -y -o stream-json -p \"$(cat {init_prompt_path})\"",
            "send_prompt_via_stdin": False,
            "enabled": True,
        },
        {
            "name": "Open Code CLI",
            "command": "open-code --cwd {repo_dir} --prompt-file {prompt_path}",
            "interactive_command": "open-code --cwd {repo_dir}",
            "init_command": "open-code --cwd {repo_dir} --prompt-file {init_prompt_path}",
            "send_prompt_via_stdin": False,
            "enabled": True,
        },
        {
            "name": "Claude Code CLI",
            "command": "claude -p \"$(cat {prompt_path})\"",
            "interactive_command": "claude",
            "init_command": "claude -p \"$(cat {init_prompt_path})\"",
            "send_prompt_via_stdin": False,
            "enabled": True,
        },
    ],
    "git_identity": {
        "name": "ai",
        "email": "ai@local",
    },
}

CLI_ALIAS_MAP: Dict[str, str] = {
    "codex": "Codex CLI",
    "gemini": "Gemini CLI",
    "open-code": "Open Code CLI",
    "opencode": "Open Code CLI",
    "open_code": "Open Code CLI",
    "claude": "Claude Code CLI",
    "claude-code": "Claude Code CLI",
    "claude_code": "Claude Code CLI",
}


@dataclasses.dataclass
class CLIConfig:
    name: str
    command: str
    interactive_command: str = ""
    init_command: str = ""
    init_required_paths: List[str] = dataclasses.field(default_factory=list)
    send_prompt_via_stdin: bool = False
    enabled: bool = True


@dataclasses.dataclass
class Timeouts:
    idle_seconds: int
    progress_probe_after_seconds: int
    progress_probe_wait_seconds: int
    max_runtime_seconds: int


@dataclasses.dataclass
class RuntimeConfig:
    repo_url: str
    project_name: str
    task_requirement: str
    caller_name: str
    init_slash_command: str
    branch: str
    working_root: Path
    loop_interval_seconds: int
    report_min_pass_rate: float
    require_code_changes: bool
    require_non_doc_code_changes: bool
    minimum_non_doc_files_changed: int
    minimum_non_doc_lines_changed: int
    max_audit_failures_per_cli: int
    log_dir: Path
    report_path: str
    prompt_path: str
    preserve_untracked_paths: List[str]
    never_commit_paths: List[str]
    commit_message_template: str
    error_keywords: List[str]
    timeouts: Timeouts
    init_enabled: bool
    init_force_reinit: bool
    init_idle_seconds: int
    init_max_runtime_seconds: int
    progress_probe_message: str
    auto_confirm_reply: str
    fallback_enabled: bool
    fallback_run_tests_on_missing_report: bool
    fallback_test_command_candidates: List[str]
    fallback_test_timeout_seconds: int
    cli_tools: List[CLIConfig]
    git_identity_name: str
    git_identity_email: str


@dataclasses.dataclass
class CLIExecutionResult:
    tool_name: str
    terminated: bool
    reason: str
    exit_code: Optional[int]
    duration_seconds: float
    output_lines: List[str]
    saw_error_keyword: Optional[str]
    loop_detected: bool
    progress_probe_sent: bool


@dataclasses.dataclass
class AuditResult:
    approved: bool
    run_success: bool
    test_pass_rate: float
    core_optimization: str
    reason: str


@dataclasses.dataclass
class RoundResult:
    status: str
    round_id: int
    tool_used: Optional[str]
    audit_result: Optional[AuditResult]
    commit_status: str
    commit_hash: Optional[str]
    message: str


class EventLogger:
    def __init__(self, path: Path, secret_mask: Optional[str] = None) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.secret_mask = secret_mask or ""

    def _sanitize(self, value: Any) -> Any:
        if isinstance(value, str):
            if self.secret_mask:
                value = value.replace(self.secret_mask, "***")
                value = value.replace(quote(self.secret_mask), "***")
            return value
        if isinstance(value, list):
            return [self._sanitize(v) for v in value]
        if isinstance(value, dict):
            return {k: self._sanitize(v) for k, v in value.items()}
        return value

    def log(self, event: str, **kwargs: Any) -> None:
        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "event": event,
            **kwargs,
        }
        clean = self._sanitize(record)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(clean, ensure_ascii=False) + "\n")


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(path: Path) -> RuntimeConfig:
    if not path.exists():
        path.write_text(json.dumps(DEFAULT_CONFIG, ensure_ascii=False, indent=2), encoding="utf-8")
    user_cfg = json.loads(path.read_text(encoding="utf-8"))
    cfg = deep_merge(DEFAULT_CONFIG, user_cfg)

    cli_tools = [CLIConfig(**item) for item in cfg["cli_tools"]]
    timeouts = Timeouts(**cfg["timeouts"])
    init_cfg = cfg.get("init_phase", {})
    gi = cfg.get("git_identity", {})
    fb = cfg.get("fallback_report", {})
    project_name = str(cfg.get("project_name", "")).strip() or repo_name_from_url(cfg["repo_url"])
    task_requirement = str(cfg.get("task_requirement", "")).strip()
    if not task_requirement:
        task_requirement = DEFAULT_CONFIG["task_requirement"]
    return RuntimeConfig(
        repo_url=cfg["repo_url"],
        project_name=project_name,
        task_requirement=task_requirement,
        caller_name=str(cfg.get("caller_name", "自动化编排器")),
        init_slash_command=str(cfg.get("init_slash_command", "/init")),
        branch=cfg["branch"],
        working_root=Path(cfg["working_root"]).resolve(),
        loop_interval_seconds=int(cfg["loop_interval_seconds"]),
        report_min_pass_rate=float(cfg["report_min_pass_rate"]),
        require_code_changes=bool(cfg.get("require_code_changes", False)),
        require_non_doc_code_changes=bool(cfg.get("require_non_doc_code_changes", False)),
        minimum_non_doc_files_changed=max(0, int(cfg.get("minimum_non_doc_files_changed", 0))),
        minimum_non_doc_lines_changed=max(0, int(cfg.get("minimum_non_doc_lines_changed", 0))),
        max_audit_failures_per_cli=int(cfg["max_audit_failures_per_cli"]),
        log_dir=Path(cfg["log_dir"]).resolve(),
        report_path=cfg["report_path"],
        prompt_path=cfg["prompt_path"],
        preserve_untracked_paths=[str(x) for x in cfg.get("preserve_untracked_paths", []) if str(x).strip()],
        never_commit_paths=[str(x) for x in cfg.get("never_commit_paths", []) if str(x).strip()],
        commit_message_template=cfg["commit_message_template"],
        error_keywords=[str(x).lower() for x in cfg["error_keywords"]],
        timeouts=timeouts,
        init_enabled=bool(init_cfg.get("enabled", True)),
        init_force_reinit=bool(init_cfg.get("force_reinit", False)),
        init_idle_seconds=int(init_cfg.get("idle_seconds", 60)),
        init_max_runtime_seconds=int(init_cfg.get("max_runtime_seconds", 600)),
        progress_probe_message=cfg["progress_probe_message"],
        auto_confirm_reply=str(cfg.get("auto_confirm_reply", "yes")),
        fallback_enabled=bool(fb.get("enabled", True)),
        fallback_run_tests_on_missing_report=bool(fb.get("run_tests_on_missing_report", True)),
        fallback_test_command_candidates=[str(x) for x in fb.get("test_command_candidates", [])],
        fallback_test_timeout_seconds=int(fb.get("test_timeout_seconds", 1800)),
        cli_tools=cli_tools,
        git_identity_name=gi.get("name", "ai"),
        git_identity_email=gi.get("email", "ai@local"),
    )


def is_placeholder_repo_url(repo_url: str) -> bool:
    value = repo_url.strip()
    return ("<owner>" in value) or ("<repo>" in value) or ("<" in value) or (">" in value)


def split_csv(raw: Optional[str]) -> List[str]:
    if not raw:
        return []
    return [x.strip() for x in raw.split(",") if x.strip()]


def resolve_cli_names(tokens: List[str], available_names: List[str]) -> Tuple[List[str], List[str]]:
    by_lower = {name.lower(): name for name in available_names}
    resolved: List[str] = []
    unknown: List[str] = []
    seen: set[str] = set()
    for token in tokens:
        key = token.strip().lower()
        target = CLI_ALIAS_MAP.get(key) or by_lower.get(key)
        if not target:
            unknown.append(token)
            continue
        if target in seen:
            continue
        seen.add(target)
        resolved.append(target)
    return resolved, unknown


def inject_token_to_https_url(repo_url: str, token: str) -> str:
    if not repo_url.startswith("https://"):
        raise ValueError("Only https:// GitHub URLs are supported for token auth.")
    safe_token = quote(token, safe="")
    return repo_url.replace("https://", f"https://x-access-token:{safe_token}@", 1)


def run_cmd(
    args: List[str],
    cwd: Optional[Path] = None,
    timeout: int = 300,
) -> Tuple[int, str]:
    try:
        proc = subprocess.run(
            args,
            cwd=str(cwd) if cwd else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
        )
        return proc.returncode, proc.stdout or ""
    except subprocess.TimeoutExpired as e:
        out = ""
        if isinstance(e.stdout, bytes):
            out = e.stdout.decode("utf-8", errors="ignore")
        elif isinstance(e.stdout, str):
            out = e.stdout
        return 124, (out or f"timeout after {timeout}s")
    except FileNotFoundError as e:
        return 127, f"command_not_found:{e}"
    except OSError as e:
        return 126, f"os_error:{e}"


def verify_github_token(cfg: RuntimeConfig, token: str, logger: EventLogger) -> bool:
    req = urlrequest.Request(
        "https://api.github.com/user",
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "openclaw-autopilot",
        },
    )
    try:
        with urlrequest.urlopen(req, timeout=20) as resp:
            body = json.loads(resp.read().decode("utf-8", errors="ignore"))
    except urlerror.HTTPError as e:
        logger.log("token.verify", ok=False, reason=f"http_{e.code}")
        return False
    except Exception as e:  # noqa: BLE001
        logger.log("token.verify", ok=False, reason=f"request_failed:{e}")
        return False

    login = str(body.get("login", "")).strip()
    ok = bool(login)
    logger.log("token.verify", ok=ok, github_login=login or "unknown")
    return ok


def repo_name_from_url(repo_url: str) -> str:
    name = repo_url.rstrip("/").split("/")[-1]
    return name[:-4] if name.endswith(".git") else name


def ensure_repo_synced(cfg: RuntimeConfig, token: str, logger: EventLogger) -> Tuple[bool, Path, str]:
    cfg.working_root.mkdir(parents=True, exist_ok=True)
    repo_dir = cfg.working_root / repo_name_from_url(cfg.repo_url)
    auth_url = inject_token_to_https_url(cfg.repo_url, token)

    if not (repo_dir / ".git").exists():
        code, out = run_cmd(["git", "clone", auth_url, str(repo_dir)], timeout=600)
        logger.log("repo.clone", ok=(code == 0), output=out[-800:])
        if code != 0:
            return False, repo_dir, "clone_failed"
        # Remove token from local git config remote.
        run_cmd(["git", "remote", "set-url", "origin", cfg.repo_url], cwd=repo_dir)

    # Git identity
    run_cmd(["git", "config", "user.name", cfg.git_identity_name], cwd=repo_dir)
    run_cmd(["git", "config", "user.email", cfg.git_identity_email], cwd=repo_dir)

    code, out = run_cmd(["git", "fetch", "origin", "--prune"], cwd=repo_dir, timeout=300)
    logger.log("repo.fetch", ok=(code == 0), output=out[-800:])
    if code != 0:
        return False, repo_dir, "fetch_failed"

    # Determine remote dev branch existence.
    code, _ = run_cmd(["git", "show-ref", "--verify", f"refs/remotes/origin/{cfg.branch}"], cwd=repo_dir)
    remote_dev_exists = code == 0

    if remote_dev_exists:
        code, out = run_cmd(["git", "checkout", "-B", cfg.branch, f"origin/{cfg.branch}"], cwd=repo_dir)
        logger.log("repo.checkout_dev", ok=(code == 0), output=out[-500:])
        if code != 0:
            return False, repo_dir, "checkout_dev_failed"
    else:
        # Create local dev from current HEAD.
        code, out = run_cmd(["git", "checkout", "-B", cfg.branch], cwd=repo_dir)
        logger.log("repo.create_dev", ok=(code == 0), output=out[-500:])
        if code != 0:
            return False, repo_dir, "create_dev_failed"
        # Push to remote dev.
        code, out = run_cmd(["git", "push", auth_url, f"{cfg.branch}:{cfg.branch}", "-u"], cwd=repo_dir, timeout=300)
        logger.log("repo.push_create_dev", ok=(code == 0), output=out[-800:])
        if code != 0:
            return False, repo_dir, "push_create_dev_failed"

    # Clean workspace to latest origin/dev baseline.
    run_cmd(["git", "reset", "--hard", f"origin/{cfg.branch}"], cwd=repo_dir)
    if not clean_workspace(cfg, repo_dir, logger, "repo.clean"):
        return False, repo_dir, "clean_failed"

    return True, repo_dir, "ok"


def clean_workspace(cfg: RuntimeConfig, repo_dir: Path, logger: EventLogger, event_name: str) -> bool:
    cmd = ["git", "clean", "-fd"]
    excludes: List[str] = []
    for raw in cfg.preserve_untracked_paths:
        rel = str(raw).strip()
        if not rel:
            continue
        excludes.append(rel)
        cmd.extend(["-e", rel])
    code, out = run_cmd(cmd, cwd=repo_dir)
    logger.log(event_name, ok=(code == 0), excludes=excludes, output=out[-800:])
    return code == 0


def refresh_repo_latest_from_remote(cfg: RuntimeConfig, repo_dir: Path, logger: EventLogger) -> bool:
    code, out = run_cmd(["git", "fetch", "origin", "--prune"], cwd=repo_dir, timeout=300)
    logger.log("repo.refresh.fetch", ok=(code == 0), output=out[-800:])
    if code != 0:
        return False

    code, _ = run_cmd(["git", "show-ref", "--verify", f"refs/remotes/origin/{cfg.branch}"], cwd=repo_dir)
    if code == 0:
        code, out = run_cmd(["git", "checkout", "-B", cfg.branch, f"origin/{cfg.branch}"], cwd=repo_dir)
        logger.log("repo.refresh.checkout", ok=(code == 0), output=out[-500:], source=f"origin/{cfg.branch}")
        if code != 0:
            return False
        run_cmd(["git", "reset", "--hard", f"origin/{cfg.branch}"], cwd=repo_dir)
    else:
        code, out = run_cmd(["git", "checkout", "-B", cfg.branch], cwd=repo_dir)
        logger.log("repo.refresh.checkout", ok=(code == 0), output=out[-500:], source="local_head")
        if code != 0:
            return False

    return clean_workspace(cfg, repo_dir, logger, "repo.refresh.clean")


def normalize_line(line: str) -> str:
    s = line.strip().lower()
    if not s:
        return ""
    s = re.sub(r"\d+", "<n>", s)
    s = re.sub(r"\s+", " ", s)
    return s[:300]


def looks_like_operation(line: str) -> bool:
    keys = [
        "test",
        "testing",
        "run",
        "running",
        "build",
        "generate",
        "fix",
        "optimi",
        "重构",
        "优化",
        "测试",
        "生成",
        "运行",
    ]
    ll = line.lower()
    return any(k in ll for k in keys)


def should_auto_confirm(line: str) -> bool:
    ll = line.lower()
    if "?" not in line and "？" not in line:
        return False
    trigger = ["是否", "确认", "继续", "proceed", "confirm", "y/n", "yes/no"]
    return any(t in ll for t in trigger)


def has_clear_progress(line: str) -> bool:
    ll = line.lower()
    patterns = [
        r"\b\d{1,3}%\b",
        r"eta",
        r"remaining",
        r"预计",
        r"还需",
        r"分钟",
        r"min",
        r"完成了",
        r"progress",
    ]
    return any(re.search(p, ll) for p in patterns)


def prepare_prompt(cfg: RuntimeConfig, round_id: int, report_abs_path: Path, redo_reason: Optional[str]) -> str:
    extra = f"\n上次审核未通过原因：{redo_reason}\n请基于该原因修正后重新执行。\n" if redo_reason else ""
    return f"""你是被{cfg.caller_name}调用的 AI 编程 CLI。

目标项目：{cfg.project_name}（分支：{cfg.branch}）
目标仓库：{cfg.repo_url}
本轮需求：{cfg.task_requirement}
执行范围：全流程迭代升级（分析→优化/重构→运行→全量测试）。

硬性要求：
1) 你可以自主修改任意文件，不受文件数量或模块限制。
2) 必须运行项目并执行自动化测试。
3) 完成后必须生成 JSON 报告到：{report_abs_path}
4) 报告字段必须包含：
   - run_status: success 或 failed
   - test_pass_rate: 数值（0-100）
   - core_optimization: 字符串，核心优化点
   - iteration_value: 字符串，迭代价值说明
   - test_summary: 字符串，测试摘要
5) 报告写入后，在标准输出打印一行：REPORT_READY
6) 不允许只输出计划后就退出；必须在本次进程中完成任务并写出报告。
7) 如果无法达成成功结果，也必须写出 run_status=failed 的报告后再退出。
8) 长任务时每20秒至少输出一条进度信息（例如 HEARTBEAT 30%）。

执行策略：
- 对任何执行确认问题，默认继续执行。
- 优先输出可通过测试的稳定结果。
{extra}
"""


def write_prompt_file(repo_dir: Path, relative_prompt_path: str, prompt_text: str) -> Path:
    p = repo_dir / relative_prompt_path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(prompt_text, encoding="utf-8")
    return p


def load_report(repo_dir: Path, report_rel_path: str) -> Optional[Dict[str, Any]]:
    report_path = repo_dir / report_rel_path
    if not report_path.exists():
        return None
    try:
        data = json.loads(report_path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        return None
    return None


def pick_summary_line(lines: List[str]) -> str:
    skip_prefixes = (
        "tokens used",
        "thinking",
        "plan update",
        "exec",
        "mcp",
        "user",
        "assistant to=",
        "{",
    )
    for raw in reversed(lines):
        line = raw.strip()
        if not line:
            continue
        lower = line.lower()
        if lower.startswith(skip_prefixes):
            continue
        if len(line) > 220:
            line = line[:220].rstrip() + "..."
        return line
    return "CLI执行完成（未输出可用总结）"


def estimate_test_pass_rate(output: str, exit_code: int) -> float:
    text = output.lower()
    pass_hits = re.findall(r"(\d+)\s+passed", text)
    fail_hits = re.findall(r"(\d+)\s+failed", text)
    passed = int(pass_hits[-1]) if pass_hits else None
    failed = int(fail_hits[-1]) if fail_hits else None

    if passed is not None and failed is not None and (passed + failed) > 0:
        return (passed * 100.0) / float(passed + failed)
    if passed is not None and passed > 0:
        return 100.0 if exit_code == 0 else 0.0
    if "ok" in text and exit_code == 0:
        return 100.0
    return 100.0 if exit_code == 0 else 0.0


def run_validation_for_fallback(
    cfg: RuntimeConfig,
    repo_dir: Path,
    logger: EventLogger,
) -> Tuple[str, int, float, str]:
    for cmd in cfg.fallback_test_command_candidates:
        command = cmd.strip()
        if not command:
            continue
        try:
            code, out = run_cmd(
                ["bash", "-lc", command],
                cwd=repo_dir,
                timeout=cfg.fallback_test_timeout_seconds,
            )
        except subprocess.TimeoutExpired:
            logger.log("fallback.test.timeout", command=command, timeout=cfg.fallback_test_timeout_seconds)
            return command, 124, 0.0, "Validation command timeout"
        lower = out.lower()
        if code == 127 and ("command not found" in lower or "not recognized" in lower):
            logger.log("fallback.test.unavailable", command=command)
            continue

        rate = estimate_test_pass_rate(out, code)
        logger.log(
            "fallback.test.ran",
            command=command,
            exit_code=code,
            pass_rate=round(rate, 2),
            output_tail=out.splitlines()[-20:],
        )
        return command, code, rate, out

    return "", 1, 0.0, "No available validation command"


def build_fallback_report(
    cfg: RuntimeConfig,
    tool: CLIConfig,
    repo_dir: Path,
    report_abs_path: Path,
    exec_result: CLIExecutionResult,
    logger: EventLogger,
) -> Optional[Dict[str, Any]]:
    if not cfg.fallback_enabled:
        return None

    summary_line = pick_summary_line(exec_result.output_lines)
    test_command = ""
    test_exit_code = 0
    test_pass_rate = 0.0
    test_output = ""

    if cfg.fallback_run_tests_on_missing_report:
        test_command, test_exit_code, test_pass_rate, test_output = run_validation_for_fallback(cfg, repo_dir, logger)
    else:
        test_exit_code = 0 if (exec_result.exit_code == 0 and not exec_result.terminated) else 1
        test_pass_rate = 100.0 if test_exit_code == 0 else 0.0
        test_output = "Fallback tests disabled by config"

    run_success = (
        exec_result.exit_code == 0
        and (not exec_result.terminated)
        and test_exit_code == 0
    )

    test_tail = test_output.splitlines()[-20:]
    report = {
        "run_status": "success" if run_success else "failed",
        "test_pass_rate": round(float(test_pass_rate), 2),
        "core_optimization": "自动补全报告（CLI未写出报告）",
        "iteration_value": summary_line,
        "test_summary": f"{test_command or 'N/A'} => exit={test_exit_code}; tail={test_tail}",
        "fallback_generated": True,
        "source_cli": tool.name,
        "cli_reason": exec_result.reason,
        "cli_exit_code": exec_result.exit_code,
    }
    report_abs_path.parent.mkdir(parents=True, exist_ok=True)
    report_abs_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    logger.log(
        "fallback.report.generated",
        tool=tool.name,
        run_status=report["run_status"],
        test_pass_rate=report["test_pass_rate"],
        report_path=str(report_abs_path),
    )
    return report


def parse_rate(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        m = re.search(r"(\d+(?:\.\d+)?)", value)
        if m:
            return float(m.group(1))
    return 0.0


def audit_report(report: Dict[str, Any], min_rate: float) -> AuditResult:
    run_status = str(report.get("run_status", "")).strip().lower()
    run_success = run_status in {"success", "ok", "passed", "true"}
    rate = parse_rate(report.get("test_pass_rate", 0))
    core = str(report.get("core_optimization", "未提供核心优化说明")).strip()

    if not run_success:
        return AuditResult(
            approved=False,
            run_success=False,
            test_pass_rate=rate,
            core_optimization=core,
            reason="运行状态非success",
        )
    if rate < min_rate:
        return AuditResult(
            approved=False,
            run_success=True,
            test_pass_rate=rate,
            core_optimization=core,
            reason=f"测试通过率不足（{rate:.2f}% < {min_rate:.2f}%）",
        )
    return AuditResult(
        approved=True,
        run_success=True,
        test_pass_rate=rate,
        core_optimization=core,
        reason="审核通过",
    )


def parse_staged_name_status(status_output: str) -> List[Tuple[str, str]]:
    entries: List[Tuple[str, str]] = []
    for raw in status_output.splitlines():
        line = raw.strip()
        if not line:
            continue
        parts = line.split("\t", 1)
        status_raw = parts[0].strip().upper()
        path = parts[1].strip() if len(parts) > 1 else ""
        if not path:
            continue
        status = status_raw[:1] if status_raw else "M"
        if status not in {"A", "M", "D", "R", "C", "T", "U"}:
            status = "M"
        entries.append((status, path))
    return entries


def summarize_staged_changes(entries: List[Tuple[str, str]], max_items: int = 8) -> str:
    if not entries:
        return "无具体文件变更"

    display = [f"{status} {path}" for status, path in entries[:max_items]]
    summary = ", ".join(display)
    if len(entries) > max_items:
        summary += f", +{len(entries) - max_items}个文件"
    if len(summary) > 180:
        summary = summary[:177].rstrip() + "..."
    return summary


def is_doc_like_path(path: str) -> bool:
    p = path.strip().lower()
    if not p:
        return False

    doc_prefixes = (
        "docs/",
        "doc/",
        ".github/",
    )
    if p.startswith(doc_prefixes):
        return True

    doc_files = {
        "readme.md",
        "changelog.md",
        "contributing.md",
        "code_of_conduct.md",
        "security.md",
        "support.md",
        "license",
        "citation.cff",
    }
    if p.split("/")[-1] in doc_files:
        return True

    doc_exts = {
        ".md",
        ".markdown",
        ".mdx",
        ".rst",
        ".txt",
        ".adoc",
        ".org",
        ".rtf",
        ".pdf",
    }
    return any(p.endswith(ext) for ext in doc_exts)


def parse_staged_numstat(numstat_output: str) -> List[Tuple[str, int, int]]:
    rows: List[Tuple[str, int, int]] = []
    for raw in numstat_output.splitlines():
        line = raw.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        add_s, del_s, path = parts[0].strip(), parts[1].strip(), parts[2].strip()
        if not path:
            continue
        try:
            added = int(add_s)
        except ValueError:
            added = 1
        try:
            deleted = int(del_s)
        except ValueError:
            deleted = 1
        rows.append((path, max(0, added), max(0, deleted)))
    return rows


def has_substantive_threshold(cfg: RuntimeConfig) -> bool:
    return (cfg.minimum_non_doc_files_changed > 0) or (cfg.minimum_non_doc_lines_changed > 0)


def commit_and_push(
    repo_dir: Path,
    cfg: RuntimeConfig,
    token: str,
    audit: AuditResult,
    logger: EventLogger,
) -> Tuple[bool, str, Optional[str]]:
    auth_url = inject_token_to_https_url(cfg.repo_url, token)

    run_cmd(["git", "add", "-A"], cwd=repo_dir)
    # Never commit runtime artifacts (prompts, reports, local CLI metadata, etc.).
    never_commit_paths = [
        cfg.prompt_path,
        cfg.report_path,
        ".openclaw/openclaw_init_prompt.md",
        ".openclaw/init_state",
        *cfg.never_commit_paths,
    ]
    seen: set[str] = set()
    for rel in never_commit_paths:
        key = str(rel).strip()
        if not key or key in seen:
            continue
        seen.add(key)
        run_cmd(["git", "reset", "-q", "HEAD", "--", key], cwd=repo_dir)

    code, status_out = run_cmd(["git", "diff", "--cached", "--name-status", "--no-renames"], cwd=repo_dir)
    if code != 0:
        logger.log("git.status_failed", output=status_out[-800:])
        return False, "git_status_failed", None

    staged_entries = parse_staged_name_status(status_out)
    if not staged_entries:
        logger.log("git.no_changes")
        return True, "no_changes", None

    changes_summary = summarize_staged_changes(staged_entries)

    if cfg.require_non_doc_code_changes:
        non_doc_entries = [(s, p) for s, p in staged_entries if not is_doc_like_path(p)]
        if not non_doc_entries:
            logger.log("git.docs_only_changes", changes=changes_summary)
            return True, "docs_only_changes", None

    if has_substantive_threshold(cfg):
        code, numstat_out = run_cmd(["git", "diff", "--cached", "--numstat", "--no-renames"], cwd=repo_dir)
        if code != 0:
            logger.log("git.numstat_failed", output=numstat_out[-800:])
            return False, "git_numstat_failed", None

        num_rows = parse_staged_numstat(numstat_out)
        non_doc_rows = [(path, add, delete) for path, add, delete in num_rows if not is_doc_like_path(path)]
        non_doc_file_count = len(non_doc_rows)
        non_doc_line_count = sum(add + delete for _, add, delete in non_doc_rows)
        min_files = max(0, int(cfg.minimum_non_doc_files_changed))
        min_lines = max(0, int(cfg.minimum_non_doc_lines_changed))
        if (non_doc_file_count < min_files) or (non_doc_line_count < min_lines):
            logger.log(
                "git.changes_below_threshold",
                non_doc_files=non_doc_file_count,
                non_doc_lines=non_doc_line_count,
                min_non_doc_files=min_files,
                min_non_doc_lines=min_lines,
                changes=changes_summary,
            )
            return True, "changes_below_threshold", None

    core = audit.core_optimization.replace("\n", " ").strip()
    if len(core) > 30:
        core = core[:30].rstrip() + "..."
    rate_str = f"{audit.test_pass_rate:.0f}"
    try:
        message = cfg.commit_message_template.format(
            project=cfg.project_name,
            core=core or "常规优化",
            rate=rate_str,
            changes=changes_summary,
        )
    except Exception as e:  # noqa: BLE001
        message = DEFAULT_CONFIG["commit_message_template"].format(
            project=cfg.project_name,
            core=core or "常规优化",
            rate=rate_str,
            changes=changes_summary,
        )
        logger.log("git.commit_template_invalid", template=cfg.commit_message_template, error=str(e))

    code, out = run_cmd(["git", "commit", "-m", message], cwd=repo_dir)
    logger.log("git.commit", ok=(code == 0), message=message, changes=changes_summary, output=out[-800:])
    if code != 0:
        return False, "commit_failed", None

    code, out = run_cmd(["git", "rev-parse", "HEAD"], cwd=repo_dir)
    commit_hash = out.strip() if code == 0 else None

    code, out = run_cmd(["git", "push", auth_url, f"{cfg.branch}:{cfg.branch}"], cwd=repo_dir, timeout=300)
    logger.log("git.push", ok=(code == 0), output=out[-1000:])
    if code != 0:
        return False, "push_failed", commit_hash

    return True, "pushed", commit_hash


def rollback_repo(repo_dir: Path, cfg: RuntimeConfig, logger: EventLogger) -> None:
    run_cmd(["git", "reset", "--hard", "HEAD"], cwd=repo_dir)
    clean_workspace(cfg, repo_dir, logger, "repo.rollback.clean")
    logger.log("repo.rollback", detail="git reset --hard HEAD && git clean -fd (with preserve list)")


def monitor_cli_process(
    tool: CLIConfig,
    command: str,
    repo_dir: Path,
    prompt_text: str,
    cfg: RuntimeConfig,
    logger: EventLogger,
    timeouts: Optional[Timeouts] = None,
) -> CLIExecutionResult:
    q: "queue.Queue[Optional[Tuple[float, str]]]" = queue.Queue()
    output_lines: List[str] = []

    cmd = ["bash", "-lc", command]
    start = time.monotonic()

    try:
        proc = subprocess.Popen(
            cmd,
            cwd=str(repo_dir),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
    except Exception as e:  # noqa: BLE001
        return CLIExecutionResult(
            tool_name=tool.name,
            terminated=True,
            reason=f"spawn_failed: {e}",
            exit_code=None,
            duration_seconds=0.0,
            output_lines=[],
            saw_error_keyword=None,
            loop_detected=False,
            progress_probe_sent=False,
        )

    def reader_thread() -> None:
        if proc.stdout is None:
            q.put(None)
            return
        for line in proc.stdout:
            q.put((time.monotonic(), line.rstrip("\n")))
        q.put(None)

    t = threading.Thread(target=reader_thread, daemon=True)
    t.start()

    if tool.send_prompt_via_stdin and proc.stdin:
        try:
            proc.stdin.write(prompt_text + "\n")
            proc.stdin.flush()
        except Exception:  # noqa: BLE001
            pass

    timeout_cfg = timeouts or cfg.timeouts
    last_output_time = start
    progress_probe_sent = False
    progress_probe_at = 0.0
    progress_probe_response = False
    progress_probe_clear = False
    loop_detected = False
    saw_error_keyword: Optional[str] = None
    last_signature = ""
    same_sig_count = 0
    last_auto_confirm_at = 0.0

    terminate_reason = "completed"

    while True:
        now = time.monotonic()

        # process output queue
        try:
            item = q.get(timeout=1)
        except queue.Empty:
            item = "_NO_LINE_"

        if item is None:
            # reader finished
            if proc.poll() is not None:
                break
        elif item != "_NO_LINE_":
            ts, line = item
            last_output_time = ts
            output_lines.append(line)

            if len(output_lines) % 20 == 0:
                logger.log("cli.output.progress", tool=tool.name, lines=len(output_lines))

            line_l = line.lower()
            for kw in cfg.error_keywords:
                if kw in line_l:
                    saw_error_keyword = kw
                    terminate_reason = f"error_keyword:{kw}"
                    break
            if saw_error_keyword:
                break

            sig = normalize_line(line)
            if sig and sig == last_signature:
                same_sig_count += 1
            else:
                last_signature = sig
                same_sig_count = 1
            if same_sig_count > 3 and looks_like_operation(sig):
                loop_detected = True
                terminate_reason = "loop_detected"
                break

            if should_auto_confirm(line):
                if proc.stdin and (time.monotonic() - last_auto_confirm_at > 2):
                    try:
                        proc.stdin.write(cfg.auto_confirm_reply + "\n")
                        proc.stdin.flush()
                        last_auto_confirm_at = time.monotonic()
                        logger.log("cli.auto_confirm", tool=tool.name)
                    except Exception:  # noqa: BLE001
                        pass

            if progress_probe_sent and ts >= progress_probe_at:
                progress_probe_response = True
                if has_clear_progress(line):
                    progress_probe_clear = True

        now = time.monotonic()
        runtime = now - start

        # 30s no output
        if runtime > timeout_cfg.idle_seconds and now - last_output_time > timeout_cfg.idle_seconds:
            terminate_reason = "idle_timeout"
            break

        # 15 min probe
        if (not progress_probe_sent) and runtime >= timeout_cfg.progress_probe_after_seconds:
            progress_probe_sent = True
            progress_probe_at = now
            if proc.stdin:
                try:
                    proc.stdin.write(cfg.progress_probe_message + "\n")
                    proc.stdin.flush()
                    logger.log("cli.progress_probe.sent", tool=tool.name)
                except Exception:  # noqa: BLE001
                    logger.log("cli.progress_probe.send_failed", tool=tool.name)

        # 5 min wait after probe
        if progress_probe_sent and (now - progress_probe_at) > timeout_cfg.progress_probe_wait_seconds:
            if not progress_probe_response:
                terminate_reason = "progress_probe_no_response"
                break
            if not progress_probe_clear:
                terminate_reason = "progress_probe_unclear"
                break

        # max 30 min
        if runtime > timeout_cfg.max_runtime_seconds:
            terminate_reason = "max_runtime_exceeded"
            break

        if proc.poll() is not None:
            break

    terminated = False
    if terminate_reason != "completed":
        terminated = True
        try:
            proc.terminate()
            proc.wait(timeout=8)
        except Exception:  # noqa: BLE001
            try:
                proc.kill()
            except Exception:  # noqa: BLE001
                pass

    exit_code = proc.poll()
    duration = time.monotonic() - start

    return CLIExecutionResult(
        tool_name=tool.name,
        terminated=terminated,
        reason=terminate_reason,
        exit_code=exit_code,
        duration_seconds=duration,
        output_lines=output_lines[-2000:],
        saw_error_keyword=saw_error_keyword,
        loop_detected=loop_detected,
        progress_probe_sent=progress_probe_sent,
    )


def cli_slug(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", name.strip().lower()).strip("_")
    return slug or "cli"


def init_marker_path(cfg: RuntimeConfig, repo_dir: Path, tool: CLIConfig) -> Path:
    return cfg.log_dir / "init_state" / repo_dir.name / f"{cli_slug(tool.name)}.json"


def missing_required_init_paths(tool: CLIConfig, repo_dir: Path) -> List[str]:
    missing: List[str] = []
    for raw in tool.init_required_paths:
        rel = str(raw).strip()
        if not rel:
            continue
        if not (repo_dir / rel).exists():
            missing.append(rel)
    return missing


def format_cli_command(
    template: str,
    repo_dir: Path,
    prompt_path: Path,
    report_abs: Path,
    init_prompt_path: Optional[Path] = None,
) -> str:
    init_path = init_prompt_path or prompt_path
    return template.format(
        repo_dir=shlex.quote(str(repo_dir)),
        prompt_path=shlex.quote(str(prompt_path)),
        init_prompt_path=shlex.quote(str(init_path)),
        report_path=shlex.quote(str(report_abs)),
    )


def prepare_init_prompt(cfg: RuntimeConfig, tool: CLIConfig, repo_dir: Path) -> str:
    required_paths = [str(x).strip() for x in tool.init_required_paths if str(x).strip()]
    if required_paths:
        fallback_detail = (
            f"   - 创建并补全初始化目录（若缺失）：{', '.join(required_paths)}\n"
            "   - 在初始化目录中写入简要项目上下文说明（模块、测试入口、执行建议）"
        )
    else:
        fallback_detail = "   - 完成等效上下文初始化，并写入该CLI默认的本地上下文目录。"
    return f"""{cfg.init_slash_command}

如果你的CLI支持 slash 命令，请先执行上面的 `{cfg.init_slash_command}`。
如果不支持 slash 命令，请执行等效初始化动作，并确保初始化目录就绪。

你是被{cfg.caller_name}调用的 AI 编程 CLI，当前处于项目初始化阶段（INIT PHASE）。

目标项目：{cfg.project_name}（分支：{cfg.branch}）
目标仓库：{cfg.repo_url}
仓库目录：{repo_dir}
当前CLI：{tool.name}

初始化要求：
1) 快速扫描项目结构、README、测试入口与构建命令；
2) 输出你识别到的核心模块与推荐执行路径（简要）；
3) 不要求提交代码，不要求推送；
4) 若 slash 不可用，必须执行“等效初始化”：
{fallback_detail}
5) 初始化完成后，在标准输出打印一行：INIT_READY
6) 若遇到确认提问，默认继续执行。

收尾校验（必须执行并展示结果）：
- 对每个必需目录，执行 `test -d <目录>` 与 `ls -la <目录>`；
- 只有上述校验全部通过，才能打印 `INIT_READY` 并退出。

注意：
- 这是一次性的项目上下文建立步骤，后续正式任务阶段会执行实际优化。
"""


def prepare_init_remediation_prompt(
    cfg: RuntimeConfig,
    tool: CLIConfig,
    repo_dir: Path,
    missing_paths: List[str],
) -> str:
    path_lines = "\n".join([f"- {p}" for p in missing_paths]) if missing_paths else "- (none)"
    path_checks = "\n".join([f"- 执行并回显：test -d {p} && ls -la {p}" for p in missing_paths]) if missing_paths else "- 执行并回显：pwd && ls -la"
    return f"""{cfg.init_slash_command}

你是被{cfg.caller_name}调用的 AI 编程 CLI。
这是初始化补救阶段（INIT REMEDIATION PHASE）。

目标仓库：{cfg.repo_url}
仓库目录：{repo_dir}
当前CLI：{tool.name}

第一次初始化后仍缺失的目录：
{path_lines}

必须立即执行：
1) 如果支持 slash 命令，先执行 `{cfg.init_slash_command}`。
2) 在当前仓库下创建缺失目录，并写入简要上下文文件（例如 PROJECT_CONTEXT.md）。
3) 执行下列校验并回显结果：
{path_checks}
4) 仅当所有校验通过时，打印一行：INIT_READY

注意：
- 不要输出计划后直接结束；必须完成目录创建与校验后再退出。
"""


def run_cli_init_if_needed(
    cfg: RuntimeConfig,
    tool: CLIConfig,
    repo_dir: Path,
    logger: EventLogger,
) -> bool:
    if not cfg.init_enabled:
        return True

    marker = init_marker_path(cfg, repo_dir, tool)
    missing_before = missing_required_init_paths(tool, repo_dir)
    if marker.exists() and (not cfg.init_force_reinit) and (not missing_before):
        logger.log("cli.init.skip", tool=tool.name, marker=str(marker), reason="already_initialized")
        return True
    if marker.exists() and missing_before:
        logger.log(
            "cli.init.marker_stale",
            tool=tool.name,
            marker=str(marker),
            missing_required_paths=missing_before,
        )

    prompt_text = prepare_init_prompt(cfg, tool, repo_dir)
    init_prompt_rel = ".openclaw/openclaw_init_prompt.md"
    init_prompt_path = write_prompt_file(repo_dir, init_prompt_rel, prompt_text)
    report_abs = (repo_dir / cfg.report_path).resolve()
    cmd_tpl = tool.init_command.strip() or tool.command
    cmd = format_cli_command(
        cmd_tpl,
        repo_dir=repo_dir,
        prompt_path=init_prompt_path,
        report_abs=report_abs,
        init_prompt_path=init_prompt_path,
    )

    logger.log("cli.init.start", tool=tool.name, command=cmd, marker=str(marker))
    init_timeouts = Timeouts(
        idle_seconds=max(5, int(cfg.init_idle_seconds)),
        progress_probe_after_seconds=max(int(cfg.init_max_runtime_seconds) + 1, int(cfg.init_idle_seconds) + 1),
        progress_probe_wait_seconds=1,
        max_runtime_seconds=max(int(cfg.init_max_runtime_seconds), int(cfg.init_idle_seconds) + 2),
    )
    result = monitor_cli_process(
        tool=tool,
        command=cmd,
        repo_dir=repo_dir,
        prompt_text=prompt_text,
        cfg=cfg,
        logger=logger,
        timeouts=init_timeouts,
    )
    logger.log(
        "cli.init.finish",
        tool=tool.name,
        terminated=result.terminated,
        reason=result.reason,
        exit_code=result.exit_code,
        duration_seconds=round(result.duration_seconds, 2),
        output_tail=result.output_lines[-20:],
    )

    ok = (not result.terminated) and (result.saw_error_keyword is None) and (result.exit_code in (0, None))
    if not ok:
        logger.log("cli.init.failed", tool=tool.name, reason=result.reason, exit_code=result.exit_code)
        return False

    missing_after = missing_required_init_paths(tool, repo_dir)
    if missing_after:
        logger.log(
            "cli.init.remediate.start",
            tool=tool.name,
            missing_required_paths=missing_after,
        )
        rem_prompt_text = prepare_init_remediation_prompt(cfg, tool, repo_dir, missing_after)
        rem_prompt_path = write_prompt_file(repo_dir, ".openclaw/openclaw_init_remediate_prompt.md", rem_prompt_text)
        rem_cmd = format_cli_command(
            cmd_tpl,
            repo_dir=repo_dir,
            prompt_path=rem_prompt_path,
            report_abs=report_abs,
            init_prompt_path=rem_prompt_path,
        )
        rem_result = monitor_cli_process(
            tool=tool,
            command=rem_cmd,
            repo_dir=repo_dir,
            prompt_text=rem_prompt_text,
            cfg=cfg,
            logger=logger,
            timeouts=init_timeouts,
        )
        logger.log(
            "cli.init.remediate.finish",
            tool=tool.name,
            terminated=rem_result.terminated,
            reason=rem_result.reason,
            exit_code=rem_result.exit_code,
            duration_seconds=round(rem_result.duration_seconds, 2),
            output_tail=rem_result.output_lines[-20:],
        )
        rem_ok = (not rem_result.terminated) and (rem_result.saw_error_keyword is None) and (rem_result.exit_code in (0, None))
        if not rem_ok:
            logger.log(
                "cli.init.failed",
                tool=tool.name,
                reason="remediation_failed",
                exit_code=rem_result.exit_code,
            )
            return False
        missing_after = missing_required_init_paths(tool, repo_dir)
    if missing_after:
        logger.log(
            "cli.init.failed",
            tool=tool.name,
            reason="required_artifacts_missing",
            missing_required_paths=missing_after,
        )
        return False

    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(
        json.dumps(
            {
                "ts": datetime.now(timezone.utc).isoformat(),
                "tool": tool.name,
                "duration_seconds": round(result.duration_seconds, 2),
                "exit_code": result.exit_code,
                "reason": result.reason,
                "required_paths": tool.init_required_paths,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    logger.log("cli.init.marked", tool=tool.name, marker=str(marker))
    return True


def run_cli_attempt(
    cfg: RuntimeConfig,
    tool: CLIConfig,
    repo_dir: Path,
    round_id: int,
    redo_reason: Optional[str],
    logger: EventLogger,
) -> Tuple[CLIExecutionResult, Optional[Dict[str, Any]]]:
    report_abs = (repo_dir / cfg.report_path).resolve()
    report_abs.parent.mkdir(parents=True, exist_ok=True)

    # Remove old report to avoid stale audit.
    if report_abs.exists():
        report_abs.unlink()

    prompt_text = prepare_prompt(cfg, round_id, report_abs, redo_reason)
    prompt_path = write_prompt_file(repo_dir, cfg.prompt_path, prompt_text)

    cmd = format_cli_command(
        tool.command,
        repo_dir=repo_dir,
        prompt_path=prompt_path,
        report_abs=report_abs,
    )

    logger.log("cli.start", tool=tool.name, command=cmd)
    result = monitor_cli_process(tool, cmd, repo_dir, prompt_text, cfg, logger)
    logger.log(
        "cli.finish",
        tool=tool.name,
        terminated=result.terminated,
        reason=result.reason,
        exit_code=result.exit_code,
        duration_seconds=round(result.duration_seconds, 2),
        lines=len(result.output_lines),
        output_tail=result.output_lines[-20:],
    )

    report = load_report(repo_dir, cfg.report_path)
    if report is not None:
        logger.log("report.loaded", tool=tool.name, keys=list(report.keys()))
    else:
        logger.log("report.missing", tool=tool.name)
        fallback = build_fallback_report(cfg, tool, repo_dir, report_abs, result, logger)
        if fallback is not None:
            report = fallback
            logger.log("report.loaded", tool=tool.name, keys=list(report.keys()), source="fallback")
    return result, report


def select_cli_tool(cfg: RuntimeConfig, selector: str) -> Optional[CLIConfig]:
    names = [tool.name for tool in cfg.cli_tools]
    resolved, _ = resolve_cli_names([selector], names)
    if resolved:
        target = resolved[0]
        for tool in cfg.cli_tools:
            if tool.name == target:
                return tool
    selector_l = selector.strip().lower()
    for tool in cfg.cli_tools:
        if tool.name.strip().lower() == selector_l:
            return tool
    return None


def codex_supports_no_alt_screen(repo_dir: Path) -> bool:
    code, out = run_cmd(["bash", "-lc", "codex -h"], cwd=repo_dir, timeout=20)
    return (code == 0) and ("--no-alt-screen" in out)


def apply_interactive_command_compat(
    tool: CLIConfig,
    cmd: str,
    repo_dir: Path,
    logger: EventLogger,
) -> str:
    if "codex" in tool.name.lower() and "--no-alt-screen" in cmd:
        if not codex_supports_no_alt_screen(repo_dir):
            patched = re.sub(r"\s--no-alt-screen(?=\s|$)", "", cmd, count=1)
            logger.log(
                "cli.interactive.compat",
                tool=tool.name,
                action="remove_no_alt_screen",
                reason="flag_unsupported_by_current_codex_binary",
            )
            return patched
    return cmd


def run_cli_attempt_interactive(
    cfg: RuntimeConfig,
    tool: CLIConfig,
    repo_dir: Path,
    round_id: int,
    redo_reason: Optional[str],
    logger: EventLogger,
) -> Tuple[CLIExecutionResult, Optional[Dict[str, Any]]]:
    report_abs = (repo_dir / cfg.report_path).resolve()
    report_abs.parent.mkdir(parents=True, exist_ok=True)
    if report_abs.exists():
        report_abs.unlink()

    prompt_text = prepare_prompt(cfg, round_id, report_abs, redo_reason)
    prompt_path = write_prompt_file(repo_dir, cfg.prompt_path, prompt_text)

    cmd_tpl = tool.interactive_command.strip() or tool.command
    cmd = format_cli_command(
        cmd_tpl,
        repo_dir=repo_dir,
        prompt_path=prompt_path,
        report_abs=report_abs,
    )
    cmd = apply_interactive_command_compat(tool, cmd, repo_dir, logger)

    print(f"[INTERACTIVE] 已进入 {tool.name} 交互模式。")
    print(f"[INTERACTIVE] 任务上下文文件: {prompt_path}")
    print("[INTERACTIVE] 请在CLI内完成任务并写出报告，然后退出CLI返回编排流程。")

    start = time.monotonic()
    logger.log("cli.interactive.start", tool=tool.name, command=cmd, prompt_path=str(prompt_path))
    proc = subprocess.run(["bash", "-lc", cmd], cwd=str(repo_dir))
    duration = time.monotonic() - start
    exit_code = proc.returncode
    reason = "completed" if exit_code == 0 else "interactive_exit_nonzero"
    logger.log(
        "cli.interactive.finish",
        tool=tool.name,
        exit_code=exit_code,
        duration_seconds=round(duration, 2),
    )

    result = CLIExecutionResult(
        tool_name=tool.name,
        terminated=False,
        reason=reason,
        exit_code=exit_code,
        duration_seconds=duration,
        output_lines=[],
        saw_error_keyword=None,
        loop_detected=False,
        progress_probe_sent=False,
    )

    report = load_report(repo_dir, cfg.report_path)
    if report is not None:
        logger.log("report.loaded", tool=tool.name, keys=list(report.keys()), mode="interactive")
        return result, report

    logger.log("report.missing", tool=tool.name, mode="interactive")

    # If interactive session failed to run in the current terminal environment,
    # fall back to non-interactive command mode for this turn.
    if exit_code != 0:
        logger.log(
            "cli.interactive.fallback_noninteractive",
            tool=tool.name,
            exit_code=exit_code,
            reason="interactive_failed_without_report",
        )
        return run_cli_attempt(cfg, tool, repo_dir, round_id, redo_reason, logger)

    fallback = build_fallback_report(cfg, tool, repo_dir, report_abs, result, logger)
    if fallback is not None:
        report = fallback
        logger.log("report.loaded", tool=tool.name, keys=list(report.keys()), source="fallback_interactive")
    return result, report


def run_single_round_interactive(
    round_id: int,
    cfg: RuntimeConfig,
    token: str,
    logger: EventLogger,
    interactive_cli: str,
    interactive_max_turns: int,
) -> RoundResult:
    logger.log("round.start", round_id=round_id, mode="interactive", interactive_cli=interactive_cli)

    ok, repo_dir, reason = ensure_repo_synced(cfg, token, logger)
    if not ok:
        msg = f"仓库同步失败: {reason}"
        logger.log("round.pause", round_id=round_id, reason=msg, mode="interactive")
        return RoundResult(
            status="paused",
            round_id=round_id,
            tool_used=None,
            audit_result=None,
            commit_status="not_started",
            commit_hash=None,
            message=msg,
        )

    tool = select_cli_tool(cfg, interactive_cli)
    if tool is None:
        msg = f"未找到指定CLI: {interactive_cli}"
        logger.log("round.pause", round_id=round_id, reason=msg, mode="interactive")
        return RoundResult(
            status="paused",
            round_id=round_id,
            tool_used=None,
            audit_result=None,
            commit_status="not_started",
            commit_hash=None,
            message=msg,
        )

    if not refresh_repo_latest_from_remote(cfg, repo_dir, logger):
        msg = "执行交互前拉取远端最新代码失败"
        logger.log("round.pause", round_id=round_id, reason=msg, mode="interactive")
        return RoundResult(
            status="paused",
            round_id=round_id,
            tool_used=tool.name,
            audit_result=None,
            commit_status="not_started",
            commit_hash=None,
            message=msg,
        )

    if not run_cli_init_if_needed(cfg, tool, repo_dir, logger):
        msg = f"{tool.name} 初始化失败，无法进入交互任务执行"
        logger.log("round.pause", round_id=round_id, reason=msg, mode="interactive")
        return RoundResult(
            status="paused",
            round_id=round_id,
            tool_used=tool.name,
            audit_result=None,
            commit_status="not_started",
            commit_hash=None,
            message=msg,
        )

    max_turns = max(1, int(interactive_max_turns))
    redo_reason: Optional[str] = None

    for turn in range(1, max_turns + 1):
        if not refresh_repo_latest_from_remote(cfg, repo_dir, logger):
            msg = "交互重试前拉取远端最新代码失败"
            logger.log("round.pause", round_id=round_id, reason=msg, mode="interactive")
            return RoundResult(
                status="paused",
                round_id=round_id,
                tool_used=tool.name,
                audit_result=None,
                commit_status="not_started",
                commit_hash=None,
                message=msg,
            )
        logger.log("interactive.turn.start", round_id=round_id, turn=turn, tool=tool.name)
        exec_result, report = run_cli_attempt_interactive(cfg, tool, repo_dir, round_id, redo_reason, logger)

        if report is None:
            redo_reason = "未检测到有效优化报告（JSON缺失或格式错误）"
            logger.log("audit.fail", tool=tool.name, reason=redo_reason, turn=turn, mode="interactive")
            continue

        audit = audit_report(report, cfg.report_min_pass_rate)
        logger.log(
            "audit.result",
            tool=tool.name,
            approved=audit.approved,
            run_success=audit.run_success,
            test_pass_rate=audit.test_pass_rate,
            reason=audit.reason,
            turn=turn,
            mode="interactive",
        )

        if audit.approved:
            ok_push, push_state, commit_hash = commit_and_push(repo_dir, cfg, token, audit, logger)
            if not ok_push:
                msg = f"提交或推送失败：{push_state}"
                logger.log("round.pause", round_id=round_id, reason=msg, mode="interactive")
                return RoundResult(
                    status="paused",
                    round_id=round_id,
                    tool_used=tool.name,
                    audit_result=audit,
                    commit_status=push_state,
                    commit_hash=commit_hash,
                    message=msg,
                )

            if push_state == "no_changes" and cfg.require_code_changes:
                redo_reason = "本轮未产生代码变更（require_code_changes=true）"
                logger.log("audit.fail", tool=tool.name, reason=redo_reason, turn=turn, mode="interactive", gate="require_code_changes")
                continue
            if push_state == "docs_only_changes" and cfg.require_non_doc_code_changes:
                redo_reason = "本轮仅文档/说明性变更（require_non_doc_code_changes=true）"
                logger.log(
                    "audit.fail",
                    tool=tool.name,
                    reason=redo_reason,
                    turn=turn,
                    mode="interactive",
                    gate="require_non_doc_code_changes",
                )
                continue
            if push_state == "changes_below_threshold" and has_substantive_threshold(cfg):
                redo_reason = (
                    "本轮代码改动幅度不足"
                    f"（minimum_non_doc_files_changed={cfg.minimum_non_doc_files_changed}, "
                    f"minimum_non_doc_lines_changed={cfg.minimum_non_doc_lines_changed}）"
                )
                logger.log(
                    "audit.fail",
                    tool=tool.name,
                    reason=redo_reason,
                    turn=turn,
                    mode="interactive",
                    gate="substantive_change_threshold",
                )
                continue

            if push_state == "pushed":
                msg = "交互会话审核通过并已提交推送"
            elif push_state == "docs_only_changes":
                msg = "交互会话审核通过但仅文档变更"
            else:
                msg = "交互会话审核通过但无代码变更"
            logger.log("round.success", round_id=round_id, tool=tool.name, commit_status=push_state, mode="interactive")
            return RoundResult(
                status="success",
                round_id=round_id,
                tool_used=tool.name,
                audit_result=audit,
                commit_status=push_state,
                commit_hash=commit_hash,
                message=msg,
            )

        redo_reason = audit.reason
        logger.log("audit.fail", tool=tool.name, reason=audit.reason, turn=turn, mode="interactive")

    msg = f"交互会话未通过审核，达到最大重做轮次（{max_turns}）"
    logger.log("round.pause", round_id=round_id, reason=msg, mode="interactive")
    return RoundResult(
        status="paused",
        round_id=round_id,
        tool_used=tool.name,
        audit_result=None,
        commit_status="not_started",
        commit_hash=None,
        message=msg,
    )


def write_round_summary(log_dir: Path, result: RoundResult) -> None:
    out = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "round_id": result.round_id,
        "status": result.status,
        "tool_used": result.tool_used,
        "commit_status": result.commit_status,
        "commit_hash": result.commit_hash,
        "message": result.message,
    }
    if result.audit_result:
        out["audit"] = dataclasses.asdict(result.audit_result)

    p = log_dir / "round_reports.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(out, ensure_ascii=False) + "\n")


def clear_pause_reason_file(log_dir: Path) -> None:
    p = log_dir / "PAUSED_REASON.txt"
    if p.exists():
        p.unlink()


def write_pause_reason_file(log_dir: Path, result: RoundResult) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    p = log_dir / "PAUSED_REASON.txt"
    lines = [
        f"time_utc: {datetime.now(timezone.utc).isoformat()}",
        f"round_id: {result.round_id}",
        f"status: {result.status}",
        f"tool_used: {result.tool_used or 'none'}",
        f"commit_status: {result.commit_status}",
        f"commit_hash: {result.commit_hash or 'none'}",
        f"message: {result.message}",
    ]
    if result.audit_result:
        lines.append(f"audit_reason: {result.audit_result.reason}")
        lines.append(f"audit_run_success: {result.audit_result.run_success}")
        lines.append(f"audit_test_pass_rate: {result.audit_result.test_pass_rate:.2f}")
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")


def render_first_round_report(result: RoundResult) -> str:
    lines = [
        "# 首轮迭代升级报告",
        "",
        f"- 轮次：{result.round_id}",
        f"- 使用CLI工具：{result.tool_used or '无'}",
        f"- 审核结果：{result.audit_result.reason if result.audit_result else '未完成'}",
        f"- 测试通过率：{(f'{result.audit_result.test_pass_rate:.2f}%') if result.audit_result else 'N/A'}",
        f"- 提交状态：{result.commit_status}",
        f"- 提交哈希：{result.commit_hash or 'N/A'}",
        f"- 备注：{result.message}",
    ]
    return "\n".join(lines)


def run_single_round(
    round_id: int,
    cfg: RuntimeConfig,
    token: str,
    logger: EventLogger,
) -> RoundResult:
    logger.log("round.start", round_id=round_id)

    ok, repo_dir, reason = ensure_repo_synced(cfg, token, logger)
    if not ok:
        msg = f"仓库同步失败: {reason}"
        logger.log("round.pause", round_id=round_id, reason=msg)
        return RoundResult(
            status="paused",
            round_id=round_id,
            tool_used=None,
            audit_result=None,
            commit_status="not_started",
            commit_hash=None,
            message=msg,
        )

    # Try CLI tools by priority.
    for tool in cfg.cli_tools:
        if not tool.enabled:
            continue
        if not refresh_repo_latest_from_remote(cfg, repo_dir, logger):
            logger.log("cli.switch", from_tool=tool.name, reason="repo_refresh_failed")
            continue
        if not run_cli_init_if_needed(cfg, tool, repo_dir, logger):
            logger.log("cli.switch", from_tool=tool.name, reason="init_failed")
            continue

        audit_failures = 0
        redo_reason: Optional[str] = None

        while audit_failures < cfg.max_audit_failures_per_cli:
            if not refresh_repo_latest_from_remote(cfg, repo_dir, logger):
                logger.log("cli.call_failed", tool=tool.name, reason="repo_refresh_failed", exit_code=None, error_keyword=None)
                break
            exec_result, report = run_cli_attempt(cfg, tool, repo_dir, round_id, redo_reason, logger)

            call_failure = (
                exec_result.terminated
                or exec_result.saw_error_keyword is not None
                or (exec_result.exit_code not in (0, None))
            )

            if call_failure:
                logger.log(
                    "cli.call_failed",
                    tool=tool.name,
                    reason=exec_result.reason,
                    exit_code=exec_result.exit_code,
                    error_keyword=exec_result.saw_error_keyword,
                )
                break

            if report is None:
                audit_failures += 1
                redo_reason = "未检测到有效优化报告（JSON缺失或格式错误）"
                logger.log(
                    "audit.fail",
                    tool=tool.name,
                    reason=redo_reason,
                    consecutive_failures=audit_failures,
                )
                continue

            audit = audit_report(report, cfg.report_min_pass_rate)
            logger.log(
                "audit.result",
                tool=tool.name,
                approved=audit.approved,
                run_success=audit.run_success,
                test_pass_rate=audit.test_pass_rate,
                reason=audit.reason,
            )

            if audit.approved:
                ok_push, push_state, commit_hash = commit_and_push(repo_dir, cfg, token, audit, logger)
                if not ok_push:
                    msg = f"提交或推送失败：{push_state}"
                    logger.log("round.pause", round_id=round_id, reason=msg)
                    return RoundResult(
                        status="paused",
                        round_id=round_id,
                        tool_used=tool.name,
                        audit_result=audit,
                        commit_status=push_state,
                        commit_hash=commit_hash,
                        message=msg,
                    )

                if push_state == "no_changes" and cfg.require_code_changes:
                    audit_failures += 1
                    redo_reason = "本轮未产生代码变更（require_code_changes=true）"
                    logger.log(
                        "audit.fail",
                        tool=tool.name,
                        reason=redo_reason,
                        consecutive_failures=audit_failures,
                        gate="require_code_changes",
                    )
                    continue
                if push_state == "docs_only_changes" and cfg.require_non_doc_code_changes:
                    audit_failures += 1
                    redo_reason = "本轮仅文档/说明性变更（require_non_doc_code_changes=true）"
                    logger.log(
                        "audit.fail",
                        tool=tool.name,
                        reason=redo_reason,
                        consecutive_failures=audit_failures,
                        gate="require_non_doc_code_changes",
                    )
                    continue
                if push_state == "changes_below_threshold" and has_substantive_threshold(cfg):
                    audit_failures += 1
                    redo_reason = (
                        "本轮代码改动幅度不足"
                        f"（minimum_non_doc_files_changed={cfg.minimum_non_doc_files_changed}, "
                        f"minimum_non_doc_lines_changed={cfg.minimum_non_doc_lines_changed}）"
                    )
                    logger.log(
                        "audit.fail",
                        tool=tool.name,
                        reason=redo_reason,
                        consecutive_failures=audit_failures,
                        gate="substantive_change_threshold",
                    )
                    continue

                if push_state == "pushed":
                    msg = "审核通过并已提交推送"
                elif push_state == "docs_only_changes":
                    msg = "审核通过但仅文档变更"
                else:
                    msg = "审核通过但无代码变更"
                rr = RoundResult(
                    status="success",
                    round_id=round_id,
                    tool_used=tool.name,
                    audit_result=audit,
                    commit_status=push_state,
                    commit_hash=commit_hash,
                    message=msg,
                )
                logger.log("round.success", round_id=round_id, tool=tool.name, commit_status=push_state)
                return rr

            # Audit failed
            audit_failures += 1
            redo_reason = audit.reason
            logger.log(
                "audit.fail",
                tool=tool.name,
                reason=audit.reason,
                consecutive_failures=audit_failures,
            )

            # Rollback if run failed and retries exhausted.
            if (not audit.run_success) and audit_failures >= cfg.max_audit_failures_per_cli:
                rollback_repo(repo_dir, cfg, logger)

        logger.log("cli.switch", from_tool=tool.name, reason="call_failed_or_audit_failed")

    # All CLIs failed/unavailable.
    msg = "无可用AI CLI工具（全部调用失败/挂起/审核不通过）"
    logger.log("round.pause", round_id=round_id, reason=msg)
    return RoundResult(
        status="paused",
        round_id=round_id,
        tool_used=None,
        audit_result=None,
        commit_status="not_started",
        commit_hash=None,
        message=msg,
    )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="OpenClaw GitHub 自动化编排脚本")
    p.add_argument("--config", default="openclaw_config.json", help="配置文件路径（JSON）")
    p.add_argument("--token-env", default="GITHUB_TOKEN", help="GitHub Token 环境变量名（默认 GITHUB_TOKEN）")
    p.add_argument("--repo-url", default=None, help="临时覆盖 repo_url")
    p.add_argument("--project-name", default=None, help="临时覆盖 project_name")
    p.add_argument("--task-requirement", default=None, help="临时覆盖 task_requirement")
    p.add_argument("--branch", default=None, help="临时覆盖目标分支")
    p.add_argument("--cli-order", default=None, help="CLI优先级顺序（逗号分隔，如 codex,gemini,open-code,claude）")
    p.add_argument("--only-cli", default=None, help="仅使用指定CLI（逗号分隔，如 codex 或 gemini）")
    p.add_argument("--interactive-cli", default=None, help="使用指定CLI进入交互会话模式（如 codex/gemini/open-code/claude）")
    p.add_argument("--interactive-max-turns", type=int, default=3, help="交互会话模式下，单任务最大重做轮次")
    p.add_argument("--once", action="store_true", help="只执行一轮")
    p.add_argument("--round-interval", type=int, default=None, help="覆盖配置中的轮询间隔（秒）")
    return p.parse_args()


def filter_available_cli_tools(cfg: RuntimeConfig, logger: EventLogger) -> None:
    kept: List[CLIConfig] = []
    for tool in cfg.cli_tools:
        if not tool.enabled:
            logger.log("cli.disabled", tool=tool.name)
            continue
        try:
            parts = shlex.split(tool.command)
        except ValueError:
            logger.log("cli.command_parse_failed", tool=tool.name, command=tool.command)
            continue
        if not parts:
            logger.log("cli.command_empty", tool=tool.name)
            continue
        binary = parts[0]
        if shutil.which(binary) is None:
            logger.log("cli.binary_missing", tool=tool.name, binary=binary)
            continue
        kept.append(tool)
    cfg.cli_tools = kept


def apply_cli_preferences(
    cfg: RuntimeConfig,
    cli_order_spec: Optional[str],
    only_cli_spec: Optional[str],
    logger: EventLogger,
) -> None:
    if not cli_order_spec and not only_cli_spec:
        return

    selected = list(cfg.cli_tools)
    all_names = [tool.name for tool in selected]

    if only_cli_spec:
        wanted, unknown = resolve_cli_names(split_csv(only_cli_spec), all_names)
        if unknown:
            logger.log("cli.only.unknown", requested=unknown)
        if wanted:
            by_name = {tool.name: tool for tool in selected}
            selected = [by_name[name] for name in wanted if name in by_name]
            logger.log("cli.only.applied", order=[tool.name for tool in selected])
        else:
            selected = []
            logger.log("cli.only.applied", order=[], warning="no_valid_cli_selected")

    if cli_order_spec and selected:
        selected_names = [tool.name for tool in selected]
        ordered_names, unknown = resolve_cli_names(split_csv(cli_order_spec), selected_names)
        if unknown:
            logger.log("cli.order.unknown", requested=unknown)
        if ordered_names:
            by_name = {tool.name: tool for tool in selected}
            ordered_set = set(ordered_names)
            selected = [by_name[name] for name in ordered_names if name in by_name] + [
                tool for tool in selected if tool.name not in ordered_set
            ]
            logger.log("cli.order.applied", order=[tool.name for tool in selected])

    cfg.cli_tools = selected


def main() -> int:
    args = parse_args()
    cfg = load_config(Path(args.config).resolve())
    if args.repo_url is not None:
        cfg.repo_url = args.repo_url
        if args.project_name is None:
            cfg.project_name = repo_name_from_url(args.repo_url)
    if args.project_name is not None:
        cfg.project_name = args.project_name.strip() or cfg.project_name
    if args.task_requirement is not None:
        cfg.task_requirement = args.task_requirement.strip() or cfg.task_requirement
    if args.branch is not None:
        cfg.branch = args.branch
    if args.round_interval is not None:
        cfg.loop_interval_seconds = int(args.round_interval)

    if is_placeholder_repo_url(cfg.repo_url):
        print("[FATAL] repo_url 仍是占位值，请设置真实仓库地址（例如 https://github.com/<owner>/<repo>.git）")
        return 2

    token_env = args.token_env.strip() or "GITHUB_TOKEN"
    token = os.getenv(token_env, "").strip()
    if not token:
        print(f"[FATAL] 缺少 GitHub Token 环境变量: {token_env}")
        return 2

    cfg.log_dir.mkdir(parents=True, exist_ok=True)
    logger = EventLogger(cfg.log_dir / "openclaw_runner.log", secret_mask=token)

    logger.log("system.start", config_path=str(Path(args.config).resolve()))
    apply_cli_preferences(cfg, args.cli_order, args.only_cli, logger)
    filter_available_cli_tools(cfg, logger)
    logger.log("cli.available_set", tools=[t.name for t in cfg.cli_tools])
    if not cfg.cli_tools:
        print("[FATAL] 无可用CLI工具（命令不存在或被禁用）")
        logger.log("system.stop", reason="no_cli_available")
        return 5

    if not verify_github_token(cfg, token, logger):
        print("[FATAL] GitHub Token 验证失败")
        logger.log("system.stop", reason="token_invalid")
        return 3

    round_id = 1
    first_round_written = False

    while True:
        if args.interactive_cli:
            result = run_single_round_interactive(
                round_id=round_id,
                cfg=cfg,
                token=token,
                logger=logger,
                interactive_cli=args.interactive_cli,
                interactive_max_turns=args.interactive_max_turns,
            )
        else:
            result = run_single_round(round_id, cfg, token, logger)
        write_round_summary(cfg.log_dir, result)
        if result.status == "paused":
            write_pause_reason_file(cfg.log_dir, result)
            logger.log("pause.file_written", path=str((cfg.log_dir / "PAUSED_REASON.txt")))
        else:
            clear_pause_reason_file(cfg.log_dir)

        if not first_round_written:
            text = render_first_round_report(result)
            p = cfg.log_dir / "first_round_report.md"
            p.write_text(text, encoding="utf-8")
            print(text)
            first_round_written = True

        if args.once:
            logger.log("system.stop", reason="once_done")
            return 4 if result.status == "paused" else 0

        if args.interactive_cli:
            logger.log("system.stop", reason="interactive_done", detail=result.message)
            return 4 if result.status == "paused" else 0

        if result.status == "paused":
            print(f"[PAUSED] {result.message}")
            logger.log("system.stop", reason="paused", detail=result.message)
            return 4

        logger.log("round.sleep", seconds=cfg.loop_interval_seconds)
        time.sleep(cfg.loop_interval_seconds)
        round_id += 1


if __name__ == "__main__":
    raise SystemExit(main())
