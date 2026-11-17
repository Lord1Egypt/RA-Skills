#!/usr/bin/env python3
"""Evidence-first Harness scorecard.

This scanner is deliberately conservative. It reports what can be evidenced
from a repository and separates static evidence, executed checks, and human /
real-host evidence. It never treats a test count as a quality score.
"""

from __future__ import annotations

import argparse
import json
import re
import selectors
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
RUBRIC_PATH = HERE / "references" / "score-rubric.json"
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache", "dist", "build"}
MAX_TEXT_BYTES = 2_000_000
SPINNER_FRAMES = ("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏")
ANSI = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
}


def color_is_enabled(mode: str) -> bool:
    if mode == "always":
        return True
    if mode == "never":
        return False
    return sys.stderr.isatty()


def paint(value: Any, color: str, enabled: bool = True, bold: bool = False) -> str:
    text_value = str(value)
    if not enabled:
        return text_value
    prefix = ANSI[color]
    if bold:
        prefix = ANSI["bold"] + prefix
    return f"{prefix}{text_value}{ANSI['reset']}"


def summarize_activity(line: str) -> str:
    cleaned = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", line).strip()
    if not cleaned:
        return "verifying controls…"
    cleaned = cleaned.replace("==", "").strip()
    if len(cleaned) > 78:
        return cleaned[:75] + "…"
    return cleaned


class LiveConsole:
    """Small presentation layer for terminal demos; it never changes evidence."""

    def __init__(self, enabled: bool, color: str = "auto") -> None:
        self.enabled = enabled
        self.colors = color_is_enabled(color)
        self.interactive = enabled and sys.stderr.isatty()
        self.tick = 0

    def write(self, value: str = "") -> None:
        if self.enabled:
            sys.stderr.write(value + "\n")
            sys.stderr.flush()

    def header(self, target: str) -> None:
        if not self.enabled:
            return
        self.write("")
        self.write(paint("  HEKOUWANG HARNESS DOCTOR", "cyan", self.colors, bold=True))
        self.write(paint(f"  target · {target}", "dim", self.colors))

    def progress(self, label: str, detail: str) -> None:
        if not self.enabled:
            return
        frame = SPINNER_FRAMES[self.tick % len(SPINNER_FRAMES)]
        self.tick += 1
        line = f"  {paint(frame, 'magenta', self.colors)} {paint(label, 'white', self.colors, bold=True):<22} {paint(detail, 'dim', self.colors)}"
        if self.interactive:
            sys.stderr.write("\r\033[2K" + line)
            sys.stderr.flush()
        elif self.tick == 1 or self.tick % 10 == 0:
            self.write(line)

    def clear_progress(self) -> None:
        if self.interactive:
            sys.stderr.write("\r\033[2K")
            sys.stderr.flush()

    def result(self, label: str, passed: bool, detail: str) -> None:
        if not self.enabled:
            return
        self.clear_progress()
        symbol = "✓" if passed else "✕"
        tone = "green" if passed else "red"
        self.write(f"  {paint(symbol, tone, self.colors, bold=True)} {paint(label, tone, self.colors, bold=True)} {paint(detail, 'dim', self.colors)}")

    def note(self, label: str, detail: str) -> None:
        if not self.enabled:
            return
        self.clear_progress()
        self.write(f"  {paint('·', 'blue', self.colors)} {paint(label, 'white', self.colors, bold=True)} {paint(detail, 'dim', self.colors)}")


def load_rubric() -> dict[str, Any]:
    return json.loads(RUBRIC_PATH.read_text(encoding="utf-8"))


def load_profile(profile: str | None) -> dict[str, Any] | None:
    if not profile:
        return None
    candidate = Path(profile).expanduser()
    if not candidate.is_file():
        candidate = HERE / "references" / "profiles" / f"{profile}.json"
    if not candidate.is_file():
        raise FileNotFoundError(f"Unknown scorecard profile: {profile}")
    loaded = json.loads(candidate.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"Scorecard profile must be a JSON object: {candidate}")
    return loaded


def rel(root: Path, path: Path) -> str:
    # Keep the repository-facing path lexical.  A skill directory may be a
    # symlink to a user's global installation; resolving it here would leak a
    # machine path into an otherwise portable scorecard.
    try:
        return path.absolute().relative_to(root.absolute()).as_posix()
    except ValueError:
        try:
            return path.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            return path.as_posix()


def readable(path: Path) -> bool:
    try:
        return path.is_file() and path.stat().st_size <= MAX_TEXT_BYTES
    except OSError:
        return False


def iter_files(root: Path, prefixes: Iterable[Path] | None = None) -> Iterable[Path]:
    roots = list(prefixes) if prefixes is not None else [root]
    seen: set[Path] = set()
    for base in roots:
        if not base.exists():
            continue
        candidates = [base] if base.is_file() else base.rglob("*")
        for path in candidates:
            try:
                resolved = path.resolve()
            except OSError:
                continue
            if resolved in seen or not readable(path):
                continue
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            seen.add(resolved)
            yield path


def text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError):
        return ""


def first_existing(root: Path, candidates: Iterable[str]) -> Path | None:
    for candidate in candidates:
        path = root / candidate
        if path.exists():
            return path
    return None


def glob_existing(root: Path, patterns: Iterable[str]) -> list[Path]:
    result: list[Path] = []
    for pattern in patterns:
        result.extend(sorted(root.glob(pattern)))
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in result:
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        try:
            resolved = path.resolve()
        except OSError:
            continue
        if resolved not in seen:
            seen.add(resolved)
            unique.append(path)
    return unique


def line_for(path: Path, patterns: Iterable[str]) -> int | None:
    compiled = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    for number, line in enumerate(text(path).splitlines(), start=1):
        if any(pattern.search(line) for pattern in compiled):
            return number
    return None


def refs(root: Path, paths: Iterable[Path], patterns: Iterable[str] | None = None) -> list[str]:
    result: list[str] = []
    for path in paths:
        line = line_for(path, patterns) if patterns else None
        suffix = f":{line}" if line else ""
        result.append(f"{rel(root, path)}{suffix}")
    return result


def search(root: Path, patterns: Iterable[str], prefixes: Iterable[Path] | None = None) -> list[str]:
    compiled = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    result: list[str] = []
    for path in iter_files(root, prefixes):
        for number, line in enumerate(text(path).splitlines(), start=1):
            if any(pattern.search(line) for pattern in compiled):
                result.append(f"{rel(root, path)}:{number}")
                break
    return result


def git_state(root: Path) -> dict[str, Any]:
    def run(args: list[str]) -> str:
        result = subprocess.run(args, cwd=root, text=True, capture_output=True, check=False)
        return result.stdout.strip()

    top = run(["git", "rev-parse", "--show-toplevel"])
    head = run(["git", "rev-parse", "HEAD"]) if top else ""
    status = run(["git", "status", "--porcelain=v1"]) if top else ""
    entries = status.splitlines() if status else []
    return {
        "is_git_repo": bool(top),
        "root": top,
        "head": head,
        "dirty": bool(entries),
        "status_count": len(entries),
        "staged_count": sum(1 for item in entries if len(item) >= 2 and item[0] != " "),
        "untracked_count": sum(1 for item in entries if item.startswith("??")),
    }


def execute_verify(root: Path, mode: str, live: bool = False, console: LiveConsole | None = None) -> dict[str, Any]:
    script = root / ".harness" / "scripts" / "verify.sh"
    package_path = root / "package.json"
    package_scripts: dict[str, Any] = {}
    if readable(package_path):
        try:
            package_scripts = json.loads(text(package_path)).get("scripts", {})
        except (TypeError, json.JSONDecodeError):
            package_scripts = {}

    if script.exists():
        command = f"bash .harness/scripts/verify.sh --{mode}"
        argv = ["bash", ".harness/scripts/verify.sh", f"--{mode}"]
    else:
        candidates = {
            "working-tree": ["check:all", "check", "test"],
            "staged": ["check:ci", "check:all", "check", "test"],
            "ci": ["check:ci", "check:all", "test"],
        }[mode]
        script_name = next((name for name in candidates if name in package_scripts), None)
        if not script_name:
            return {"mode": mode, "command": "", "executed": False, "reason": "no verification entrypoint"}
        command = f"pnpm run {script_name}"
        argv = ["pnpm", "run", script_name]

    started = time.monotonic()
    output = ""
    timed_out = False
    if live:
        active_console = console or LiveConsole(True)
        chunks: list[str] = []
        last_activity = "starting verification…"
        try:
            process = subprocess.Popen(
                argv,
                cwd=root,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
            )
            selector = selectors.DefaultSelector()
            if process.stdout is not None:
                selector.register(process.stdout, selectors.EVENT_READ)
            while selector.get_map():
                if not timed_out and time.monotonic() - started >= 900:
                    process.kill()
                    timed_out = True
                    last_activity = "verification timed out after 900 seconds"
                for key, _ in selector.select(timeout=.08):
                    line = key.fileobj.readline()
                    if line:
                        chunks.append(line)
                        last_activity = summarize_activity(line)
                    else:
                        selector.unregister(key.fileobj)
                        key.fileobj.close()
                active_console.progress(f"RUN {mode}", last_activity)
            exit_code = 124 if timed_out else process.wait()
            selector.close()
            output = "".join(chunks)
            if timed_out:
                output += "\nverification timed out after 900 seconds\n"
        except OSError as error:
            output = f"verification could not start: {error}"
            exit_code = 126
    else:
        try:
            result = subprocess.run(argv, cwd=root, text=True, capture_output=True, check=False, timeout=900)
            output = f"{result.stdout}\n{result.stderr}"
            exit_code = result.returncode
        except subprocess.TimeoutExpired as error:
            output = f"{error.stdout or ''}\n{error.stderr or ''}\nverification timed out after 900 seconds"
            exit_code = 124
            timed_out = True
        except OSError as error:
            output = f"verification could not start: {error}"
            exit_code = 126
    elapsed = round(time.monotonic() - started, 3)
    counts = [int(value) for value in re.findall(r"(\d+) 项检查通过", output)]
    labels = []
    for line in output.splitlines():
        stripped = line.strip()
        if "❌" in stripped or re.search(r"\b(?:FAILED|ERROR)\b", stripped) or stripped.startswith("FAIL "):
            labels.append(stripped)
    return {
        "mode": mode,
        "command": command,
        "executed": True,
        "exitCode": exit_code,
        "passed": exit_code == 0,
        "timedOut": timed_out,
        "durationSeconds": elapsed,
        "governanceCounts": counts,
        "failureLabels": labels[:20],
    }


def host_matrix(root: Path) -> list[dict[str, Any]]:
    definitions = {
        "Claude Code": [".claude/settings.json", ".claude/hooks", ".claude/skills"],
        "Cursor": [".cursor/hooks.json", ".cursor/rules", ".cursor/skills"],
        "CodeBuddy": [".codebuddy/settings.json", ".codebuddy/hooks", ".codebuddy/skills"],
        "Codex": [".codex/hooks.json", ".codex/config.toml", ".codex/skills"],
    }
    matrix = []
    for name, candidates in definitions.items():
        found = []
        for candidate in candidates:
            path = root / candidate
            if path.is_file():
                found.append(path)
            elif path.is_dir():
                try:
                    if any(path.iterdir()):
                        found.append(path)
                except OSError:
                    continue
        matrix.append({
            "host": name,
            "configured": bool(found),
            "evidence": refs(root, found),
            "evidenceLevel": "configured" if found else "missing",
            "smokeTest": "unknown",
            "note": "配置存在不等于真实宿主已经触发。",
        })
    return matrix


def add_signal(dimensions: dict[str, dict[str, Any]], dim_id: str, points: int, title: str, detail: str,
               evidence: list[str], strength: str = "direct", severity: str = "info") -> None:
    dimension = dimensions[dim_id]
    remaining = max(0, dimension["weight"] - dimension["earned"])
    # A keyword or prose reference is useful discovery evidence, but it is
    # deliberately worth less than a concrete file, executable check, or
    # runtime result.  This is the anti-README-gaming rule of the scorecard.
    effective_points = max(1, points // 2) if strength == "heuristic" and points else points
    awarded = min(effective_points, remaining)
    dimension["earned"] += awarded
    dimension["signals"].append({
        "title": title,
        "detail": detail,
        "points": awarded,
        "strength": strength,
        "severity": severity,
        "evidence": evidence,
    })


def scan_profile(root: Path, profile: dict[str, Any] | None) -> dict[str, Any] | None:
    if profile is None:
        return None
    controls: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    earned_total = 0
    signal_total = 0
    direct_total = 0
    for control in profile.get("controls", []):
        paths = [root / value for value in control.get("paths", [])]
        existing = [path for path in paths if path.exists()]
        hits = search(root, control.get("patterns", []), existing)
        evidence = refs(root, existing[:8]) + hits[:12]
        evidence_kind = control.get("evidenceKind", "policy")
        if existing and hits:
            earned = int(control["weight"])
            status = "pass"
            signal_total += 1
            if evidence_kind in {"executable", "runtime"}:
                direct_total += 1
        elif existing:
            earned = max(1, int(control["weight"]) // 2)
            status = "partial"
            signal_total += 1
        else:
            earned = 0
            status = "missing"
        earned_total += earned
        controls.append({
            "id": control["id"],
            "name": control["name"],
            "description": control.get("description", ""),
            "weight": control["weight"],
            "earned": earned,
            "status": status,
            "evidenceKind": evidence_kind,
            "evidence": evidence,
        })
        if status != "pass":
            findings.append({
                "severity": "P1" if status == "missing" else "P2",
                "title": f"内容 Profile：{control['name']}",
                "detail": control.get("description", ""),
                "evidence": evidence[:8],
            })
    maximum = int(profile.get("scoreMax", sum(item["weight"] for item in profile.get("controls", []))))
    confidence = 35 + round(65 * direct_total / signal_total) if signal_total else 35
    profile_decision = "READY" if earned_total == maximum and confidence >= 85 else "CONDITIONAL" if earned_total else "BLOCKED"
    return {
        "id": profile.get("id", "custom"),
        "name": profile.get("name", profile.get("id", "Custom profile")),
        "score": {"value": earned_total, "max": maximum, "confidence": confidence, "decision": profile_decision},
        "controls": controls,
        "findings": findings,
        "source": f"references/profiles/{profile.get('id', 'custom')}.json",
    }


def scan(root: Path, modes: list[str] | None = None, profile: str | None = None,
         live: bool = False, color: str = "auto") -> dict[str, Any]:
    root = root.resolve()
    console = LiveConsole(live, color)
    console.header(root.name)
    rubric = load_rubric()
    loaded_profile = load_profile(profile)
    dimensions = {
        item["id"]: {
            "id": item["id"],
            "name": item["name"],
            "description": item["description"],
            "weight": item["weight"],
            "earned": 0,
            "signals": [],
        }
        for item in rubric["dimensions"]
    }

    text_roots = [
        root / "AGENTS.md", root / "CLAUDE.md", root / "README.md", root / "README.zh.md",
        root / ".harness", root / ".github", root / ".agents", root / ".claude", root / ".cursor",
        root / ".codebuddy", root / ".codex", root / "docs",
    ]
    all_text_roots = [path for path in text_roots if path.exists()]

    instructions = [path for path in [root / "AGENTS.md", root / "CLAUDE.md", root / "GEMINI.md", root / "CODEBUDDY.md"] if path.exists()]
    if instructions:
        add_signal(dimensions, "instruction_routing", 4, "运行时入口存在", "发现 Agent 规则真源或宿主入口。", refs(root, instructions))
    if (root / "README.md").exists() and ((root / ".agents").exists() or (root / ".harness").exists()):
        add_signal(dimensions, "instruction_routing", 2, "规则有路由入口", "README 与 Agent / Harness 目录同时存在。", refs(root, [root / "README.md", root / ".harness" if (root / ".harness").exists() else root / ".agents"]))
    route_hits = search(root, [r"route|路由|skill|按需|references|唯一真源"], [path for path in all_text_roots if path.is_dir()])
    if route_hits:
        add_signal(dimensions, "instruction_routing", 2, "规则包含路由或真源声明", "检测到规则路由、Skill 或唯一真源说明。", route_hits[:5], strength="heuristic")

    verify = root / ".harness" / "scripts" / "verify.sh"
    harness_check = root / ".harness" / "scripts" / "harness-check.sh"
    package_path = root / "package.json"
    package_scripts: dict[str, Any] = {}
    if readable(package_path):
        try:
            loaded_package = json.loads(text(package_path))
            if isinstance(loaded_package, dict) and isinstance(loaded_package.get("scripts"), dict):
                package_scripts = loaded_package["scripts"]
        except json.JSONDecodeError:
            package_scripts = {}
    verification_entrypoints: list[str] = []
    if verify.exists():
        verification_entrypoints.append(rel(root, verify))
        add_signal(dimensions, "verification", 5, "唯一验证入口存在", "发现 .harness/scripts/verify.sh。", refs(root, [verify]))
        if verify.stat().st_mode & 0o111:
            add_signal(dimensions, "verification", 2, "验证入口可执行", "verify.sh 具有执行权限。", refs(root, [verify]))
        modes_hit = search(root, [r"--working-tree|--staged|--ci"], [verify])
        if modes_hit:
            add_signal(dimensions, "verification", 3, "验证模式显式声明", "入口包含 working-tree、staged 或 ci 模式。", modes_hit)
    else:
        project_checks = [name for name in ("check:all", "check:ci", "check", "test") if name in package_scripts]
        verification_entrypoints.extend(f"package.json:scripts.{name}" for name in project_checks)
        if project_checks:
            add_signal(dimensions, "verification", 5, "项目验证入口存在", "发现 package.json 中可执行的项目检查脚本。", [f"package.json:scripts.{project_checks[0]}"])
        if "check:ci" in package_scripts or "check:all" in package_scripts:
            add_signal(dimensions, "verification", 3, "验证模式由项目脚本区分", "发现 check:ci 或 check:all 等可复现门禁。", [f"package.json:scripts.{name}" for name in project_checks if name in {"check:ci", "check:all"}])
        elif "test" in package_scripts:
            add_signal(dimensions, "verification", 2, "项目测试入口存在", "发现 test 脚本，但尚未证明有独立 CI/工作区模式。", ["package.json:scripts.test"], strength="heuristic")
    if harness_check.exists():
        verification_entrypoints.append(rel(root, harness_check))
        add_signal(dimensions, "verification", 2, "结构诊断入口存在", "发现 harness-check.sh 结构诊断入口。", refs(root, [harness_check]))

    workflows = glob_existing(root, [".github/workflows/*.yml", ".github/workflows/*.yaml", ".gitlab-ci.yml", "Jenkinsfile"])
    if workflows:
        add_signal(dimensions, "ci_parity", 4, "CI 配置存在", "发现 CI workflow。", refs(root, workflows))
        ci_hits = search(root, [r"verify\.sh|harness-check|runtime-governance|safety-gate|check:ci|check:all|pnpm run test|npm run test"], workflows)
        if ci_hits:
            add_signal(dimensions, "ci_parity", 3, "CI 运行 Harness 检查", "CI 配置引用了 Harness 或验证入口。", ci_hits[:8])
        fixture_hits = search(root, [r"fixture|--ci|working-tree|staged"], [root / ".harness", root / ".github"])
        if fixture_hits:
            add_signal(dimensions, "ci_parity", 3, "CI 有模式或 fixture 边界", "CI 或 Harness fixture 明确区分可复现模式。", fixture_hits[:8], strength="heuristic")

    host_hits = host_matrix(root)
    for host in host_hits:
        if host["configured"]:
            add_signal(dimensions, "host_adapters", 2, f"{host['host']} 适配存在", "发现宿主配置或 Skill 入口。", host["evidence"])

    safety_paths = glob_existing(root, [
        ".harness/hooks/*", ".harness/scripts/*safety*", ".harness/scripts/*policy*", ".harness/scripts/*permission*",
        "**/src/**/*sandbox*", "**/src/**/*permission*", "**/src/**/*approval*", "**/src/**/*guard*", "**/src/**/*hook*",
        "**/hooks/**", "**/sandbox/**", "**/guard/**", "**/permission/**", "**/approval/**",
    ])
    safety_text = search(root, [r"fail[-_ ]?closed|failClosed|allow.*ask.*deny|安全门|Safety Gate|approval|sandbox|permission"], [
        root / ".harness", root / "AGENTS.md", root / "README.md", root / "docs", root / "packages",
    ])
    if safety_paths:
        add_signal(dimensions, "safety_enforcement", 4, "安全执行组件存在", "发现安全门、策略或 Hook 实现。", refs(root, safety_paths[:8]))
    hook_paths = glob_existing(root, [".claude/settings.json", ".cursor/hooks.json", ".codebuddy/settings.json", ".codex/hooks.json", ".harness/hooks/*"])
    if hook_paths:
        add_signal(dimensions, "safety_enforcement", 2, "Hook 挂载配置存在", "发现宿主 Hook 或 Harness Hook 配置。", refs(root, hook_paths[:10]))
    if safety_text:
        add_signal(dimensions, "safety_enforcement", 3, "安全判定语义显式", "发现 fail-closed、allow/ask/deny 或审批语义。", safety_text[:8], strength="heuristic")
    security_negative = search(root, [r"negative|反例|deny|阻断|危险|forbidden|blocked"], [root / ".harness/tests", root / ".harness"])
    if security_negative:
        add_signal(dimensions, "safety_enforcement", 3, "安全反例存在", "发现危险动作或拒绝路径的回归证据。", security_negative[:8])

    contract_paths = glob_existing(root, [
        ".harness/contracts/*", ".harness/*contract*", ".harness/*evidence*",
        "**/src/**/*contract*", "**/src/**/*invariant*", "**/spec/**", "**/tests/**/*contract*", "**/tests/**/*snapshot*",
    ])
    evidence_text = search(root, [r"sha256|evidence|证据|Evaluator|完成门|completion gate|invariant|replay|snapshot"], [
        root / ".harness", root / "AGENTS.md", root / "README.md", root / "docs", root / "packages", root / "scripts",
    ])
    if contract_paths:
        add_signal(dimensions, "evidence_contracts", 3, "契约目录存在", "发现 Harness contracts 或契约文件。", refs(root, contract_paths[:10]))
    if search(root, [r"task.contract|task-contract|evaluate-task|Evaluator"], [root / ".harness", root / "AGENTS.md"]):
        add_signal(dimensions, "evidence_contracts", 3, "任务完成契约和独立评估存在", "发现 Task Contract 或独立 Evaluator。", search(root, [r"task.contract|task-contract|evaluate-task|Evaluator"], [root / ".harness", root / "AGENTS.md"])[:8])
    if evidence_text:
        add_signal(dimensions, "evidence_contracts", 3, "证据摘要语义存在", "发现 SHA-256、证据绑定或完成门声明。", evidence_text[:8], strength="heuristic")
    if search(root, [r"human evidence|人工证据|decision=pass|审阅人|审阅时间"], [root / ".harness", root / "AGENTS.md"]):
        add_signal(dimensions, "evidence_contracts", 3, "人工证据字段存在", "发现人工审阅人的结构化完成条件。", search(root, [r"human evidence|人工证据|decision=pass|审阅人|审阅时间"], [root / ".harness", root / "AGENTS.md"])[:8])

    recovery_paths = glob_existing(root, [
        ".harness/scripts/*episode*", ".harness/scripts/*checkpoint*", ".harness/scripts/*recover*", ".harness/*episode*", ".harness/*checkpoint*",
        "**/src/**/*checkpoint*", "**/src/**/*recover*", "**/src/**/*persistence*", "**/src/**/*resume*",
        "**/tests/**/*checkpoint*", "**/tests/**/*recover*", "**/tests/**/*persistence*", "**/tests/**/*resume*",
    ])
    recovery_text = search(root, [r"checkpoint|resume|恢复|原子|atomic|lock|状态转移|crash recovery"], [
        root / ".harness", root / "AGENTS.md", root / "README.md", root / "docs", root / "packages",
    ])
    if recovery_paths:
        add_signal(dimensions, "recovery_state", 4, "Episode 或恢复组件存在", "发现 Episode、checkpoint 或 recovery 实现。", refs(root, recovery_paths[:8]))
    if recovery_text:
        add_signal(dimensions, "recovery_state", 4, "恢复不变量有证据", "发现 checkpoint、锁、原子写入或状态转移语义。", recovery_text[:10], strength="heuristic")

    observe_paths = glob_existing(root, [
        ".harness/scripts/*observ*", ".harness/scripts/*telemetry*", ".harness/scripts/*observe*", ".harness/tests/*observ*",
        "**/src/**/*observ*", "**/src/**/*telemetry*", "**/telemetry/**", "**/tests/**/*telemetry*", "**/tests/**/*observ*",
    ])
    observe_text = search(root, [r"redact|脱敏|telemetry=0|可观测|trend|事件记录|telemetry|session/event"], [
        root / ".harness", root / "AGENTS.md", root / "README.md", root / "docs", root / "packages",
    ])
    if observe_paths:
        add_signal(dimensions, "observability", 3, "可观测性入口存在", "发现观测、事件或 telemetry 实现。", refs(root, observe_paths[:8]))
    if observe_text:
        add_signal(dimensions, "observability", 5, "可观测性治理语义存在", "发现脱敏、开关、趋势或事件字段。", observe_text[:10], strength="heuristic")

    tests = glob_existing(root, [".harness/tests/*", "tests/*", "test/*", "**/tests/*", "**/test/*", "**/__tests__/*"])
    fixture_paths = glob_existing(root, [".harness/tests/fixtures/*", "tests/fixtures/*", "fixtures/*", "**/fixtures/*", "**/test-fixtures/*"])
    test_dirs = {path.parent for path in tests if path.parent.name in {"tests", "test", "__tests__"}}
    test_prefixes = [root / ".harness/tests", root / "tests", root / "test", *sorted(test_dirs)]
    negative_hits = search(root, [r"negative|反例|bad|invalid|deny|阻断|失败|must be blocked|reject"], test_prefixes)
    if tests:
        add_signal(dimensions, "regression", 2, "测试套件存在", "发现 Harness 或项目测试目录。", refs(root, tests[:10]))
    if fixture_paths:
        add_signal(dimensions, "regression", 2, "fixture 存在", "发现正例或反例 fixture。", refs(root, fixture_paths[:10]))
    if negative_hits:
        add_signal(dimensions, "regression", 2, "反例回归存在", "发现拒绝、非法输入或失败路径测试。", negative_hits[:10])
    evaluator_hits = search(root, [r"independent evaluator|独立 evaluator|正例|反例|assert|expect\("], test_prefixes)
    if evaluator_hits:
        add_signal(dimensions, "regression", 2, "测试包含断言或独立评估", "发现断言、正反例或独立 Evaluator 线索。", evaluator_hits[:10])

    lifecycle_paths = glob_existing(root, [
        ".harness/contracts/component-registry.json", ".harness/contracts/workflow-profiles.json", ".harness/contracts/runtime-contracts.json", ".harness/scripts/sync-agent-adapters.sh",
        "**/src/**/*registry*", "**/src/**/*manifest*", "**/src/**/*profile*", "**/package.json",
    ])
    if lifecycle_paths:
        add_signal(dimensions, "lifecycle_drift", 3, "生命周期契约存在", "发现组件注册、Workflow Profile、运行时契约或适配同步器。", refs(root, lifecycle_paths))
    failure_paths = glob_existing(root, [".harness/scripts/*failure*", ".harness/*failure*", ".harness/tests/*failure*"])
    if failure_paths:
        add_signal(dimensions, "lifecycle_drift", 1, "失败台账存在", "发现失败记录或失败生命周期脚本。", refs(root, failure_paths[:8]))
    drift_hits = search(root, [r"drift|漂移|lifecycle|生命周期|--check"], [root / ".harness", root / "AGENTS.md"])
    if drift_hits:
        add_signal(dimensions, "lifecycle_drift", 2, "漂移检查语义存在", "发现适配链接、漂移或生命周期检查。", drift_hits[:8], strength="heuristic")

    docs = [path for path in [root / "README.md", root / "README.en.md", root / "LICENSE", root / "CHANGELOG.md", root / "CONTRIBUTING.md"] if path.exists()]
    refs_paths = glob_existing(root, ["references/*", "docs/*", ".agents/skills/*/references/*"])
    machine_prefixes = (
        "/" + "Users/",
        "/" + "private/",
        "file:" + "//",
        "/" + "tmp/",
    )
    local_path_hits = search(root, [re.escape(prefix) for prefix in machine_prefixes], [root / "README.md", root / "AGENTS.md", root / ".harness", root / ".agents"])
    if docs:
        add_signal(dimensions, "docs_portability", 2, "发布和使用文档存在", "发现 README、许可证或变更说明。", refs(root, docs))
    if refs_paths:
        add_signal(dimensions, "docs_portability", 1, "参考文档存在", "发现 references 或 docs 目录。", refs(root, refs_paths[:10]))
    if not local_path_hits:
        add_signal(dimensions, "docs_portability", 1, "未发现机器专属路径", "扫描的入口文档和 Harness 文件未发现常见本机路径。", [])
    else:
        dimensions["docs_portability"]["signals"].append({"title": "发现机器专属路径", "detail": "需要确认路径是否会阻碍迁移。", "points": 0, "strength": "direct", "severity": "P1", "evidence": local_path_hits[:8]})

    boundary_hits = search(root, [r"宿主烟测|真实宿主|人工验收|human review|smoke test|不能证明|待补"], [root / "AGENTS.md", root / "README.md", root / ".harness", root / ".agents"])
    smoke_paths = glob_existing(root, [".harness/evidence/*", "evidence/*", "docs/*smoke*", ".harness/*smoke*"])
    smoke_evidence = search(root, [r"decision=pass|smoke.*pass|宿主.*通过|manual.*evidence"], smoke_paths)
    if boundary_hits:
        add_signal(dimensions, "human_boundary", 2, "自动化与人工边界有声明", "文档明确写出自动化不能证明的宿主或人工事项。", boundary_hits[:10])
    if smoke_evidence:
        add_signal(dimensions, "human_boundary", 2, "存在人工或宿主通过证据", "发现结构化的真实宿主或人工通过记录。", smoke_evidence[:10], strength="runtime")

    state = git_state(root)
    if live:
        console.note("STATIC EVIDENCE", f"indexed {len(dimensions)} dimensions · mapped {len(host_hits)} hosts")
    executions: list[dict[str, Any]] = []
    for mode in (modes or []):
        if live:
            console.progress(f"PREPARE {mode}", "opening the target verifier…")
        execution = execute_verify(root, mode, live=live, console=console)
        executions.append(execution)
        if live:
            if execution.get("executed"):
                counts = ", ".join(str(value) for value in execution.get("governanceCounts", [])) or "no count"
                detail = f"exit {execution.get('exitCode')} · {execution.get('durationSeconds')}s · governance {counts}"
                console.result(mode, bool(execution.get("passed")), detail)
            else:
                console.result(mode, False, execution.get("reason", "not executed"))
    for execution in executions:
        if execution.get("executed") and execution.get("passed"):
            add_signal(dimensions, "verification", 0, f"{execution['mode']} 执行通过", "运行时验证通过，增强报告置信度。", [execution["command"]], strength="runtime")
            if execution["mode"] == "ci":
                add_signal(dimensions, "ci_parity", 2, "CI 模式真实执行通过", "目标仓库的 CI 模式验证入口真实返回 0。", [execution["command"]], strength="runtime")
        elif execution.get("executed"):
            dimensions["verification"]["signals"].append({"title": f"{execution['mode']} 执行失败", "detail": "真实退出码非零，不能宣称当前模式通过。", "points": 0, "strength": "runtime", "severity": "P0", "evidence": execution.get("failureLabels", [])})

    score = sum(item["earned"] for item in dimensions.values())
    caps: list[dict[str, Any]] = []
    cap_conditions = [
        ("no_verification_entrypoint", dimensions["verification"]["earned"] == 0),
        ("no_ci_parity", dimensions["ci_parity"]["earned"] == 0),
        ("no_safety_enforcement", dimensions["safety_enforcement"]["earned"] == 0),
        ("no_negative_regression", dimensions["regression"]["earned"] < 4),
        ("no_evidence_contract", dimensions["evidence_contracts"]["earned"] < 6),
    ]
    for cap_id, active in cap_conditions:
        if active:
            definition = next(item for item in rubric["hardCaps"] if item["id"] == cap_id)
            caps.append(definition)
            score = min(score, definition["maxScore"])

    direct = 0
    runtime = 0
    signal_count = 0
    for dimension in dimensions.values():
        for signal in dimension["signals"]:
            if signal["evidence"]:
                signal_count += 1
                if signal["strength"] == "runtime":
                    runtime += 1
                elif signal["strength"] == "direct":
                    direct += 1
    confidence = 35
    if signal_count:
        confidence += round(45 * direct / signal_count)
        confidence += round(20 * runtime / signal_count)
    if not executions:
        confidence = min(confidence, 78)
    if state["dirty"]:
        confidence = min(confidence, 88)

    maturity = next(item for item in rubric["maturityBands"] if item["min"] <= score <= item["max"])
    findings: list[dict[str, Any]] = []
    for cap in caps:
        findings.append({"severity": cap["severity"], "title": cap["id"], "detail": cap["message"], "evidence": []})
    for dimension in dimensions.values():
        status = "pass" if dimension["earned"] >= dimension["weight"] else "partial" if dimension["earned"] else "missing"
        dimension["status"] = status
        if status == "missing":
            findings.append({"severity": "P1", "title": f"缺少：{dimension['name']}", "detail": dimension["description"], "evidence": []})
        elif status == "partial":
            findings.append({"severity": "P2", "title": f"待补：{dimension['name']}", "detail": dimension["description"], "evidence": [ref for signal in dimension["signals"] for ref in signal["evidence"]][:6]})
    if state["dirty"]:
        findings.append({"severity": "P2", "title": "工作区不是干净快照", "detail": f"当前有 {state['status_count']} 个 Git 状态条目，评分针对工作区而非单一提交。", "evidence": []})
    if any(not host["configured"] for host in host_hits):
        findings.append({"severity": "P1", "title": "宿主适配不完整", "detail": "至少一个目标 Agent 宿主没有检测到配置或入口。", "evidence": []})
    decision = "BLOCKED" if caps or any(execution.get("executed") and not execution.get("passed") for execution in executions) else "READY" if score >= 95 and confidence >= 85 and all(item["status"] == "pass" for item in dimensions.values()) else "CONDITIONAL"
    domain_profile = scan_profile(root, loaded_profile)
    if live:
        console.note("SCORECARD", f"bound {len(dimensions)} dimensions · applied {len(caps)} hard caps · decision {decision}")

    return {
        "schemaVersion": "1.0",
        "target": {"path": str(root), "name": root.name, "git": state},
        "score": {"value": score, "max": rubric["scoreMax"], "confidence": confidence, "maturity": maturity, "decision": decision, "caps": caps},
        "dimensions": list(dimensions.values()),
        "findings": findings,
        "profile": domain_profile,
        "hosts": host_hits,
        "executions": executions,
        "verification": {"entrypoints": verification_entrypoints},
        "counts": {"evidenceSignals": signal_count, "directSignals": direct, "runtimeSignals": runtime},
        "rubric": {"source": "references/score-rubric.json", "version": rubric["schemaVersion"]},
    }


def compare_reports(report: dict[str, Any], baseline: dict[str, Any], baseline_path: str) -> dict[str, Any]:
    previous_dimensions = {item.get("id"): item for item in baseline.get("dimensions", [])}
    dimension_deltas = []
    for dimension in report.get("dimensions", []):
        previous = previous_dimensions.get(dimension["id"], {})
        before = previous.get("earned", 0)
        dimension_deltas.append({
            "id": dimension["id"],
            "name": dimension["name"],
            "before": before,
            "after": dimension["earned"],
            "delta": dimension["earned"] - before,
        })
    before_score = baseline.get("score", {}).get("value", 0)
    return {
        "baseline": baseline_path,
        "scoreBefore": before_score,
        "scoreAfter": report["score"]["value"],
        "scoreDelta": report["score"]["value"] - before_score,
        "confidenceBefore": baseline.get("score", {}).get("confidence"),
        "confidenceAfter": report["score"].get("confidence"),
        "dimensionDeltas": dimension_deltas,
    }


def markdown(report: dict[str, Any]) -> str:
    score = report["score"]
    lines = [
        f"# Harness Scorecard — {report['target']['name']}",
        "",
        f"**Score:** {score['value']}/{score['max']}  ",
        f"**Confidence:** {score['confidence']}/100  ",
        f"**Maturity:** {score['maturity']['id']} · {score['maturity']['name']}  ",
        f"**Decision:** `{score['decision']}`",
        "",
        f"Target: `{report['target']['path']}`  ",
        f"HEAD: `{report['target']['git'].get('head') or 'unknown'}`  ",
        f"Dirty: `{report['target']['git'].get('dirty')}`",
        "",
        "## Dimension score",
        "",
        "| Dimension | Score | Status | Evidence signals |",
        "| --- | ---: | --- | ---: |",
    ]
    for dimension in report["dimensions"]:
        lines.append(f"| {dimension['name']} | {dimension['earned']}/{dimension['weight']} | {dimension['status']} | {len(dimension['signals'])} |")
    lines.extend(["", "## Findings", ""])
    if report["findings"]:
        for finding in report["findings"]:
            lines.append(f"- **{finding['severity']} · {finding['title']}**：{finding['detail']}")
            for evidence in finding.get("evidence", [])[:4]:
                lines.append(f"  - evidence: `{evidence}`")
    else:
        lines.append("- No findings.")
    lines.extend(["", "## Host matrix", "", "| Host | Configured | Real smoke test |", "| --- | --- | --- |"])
    for host in report["hosts"]:
        lines.append(f"| {host['host']} | {'yes' if host['configured'] else 'no'} | {host['smokeTest']} |")
    lines.extend(["", "## Executed checks", ""])
    if report["executions"]:
        for execution in report["executions"]:
            result = "pass" if execution.get("passed") else "fail"
            lines.append(f"- `{execution['command']}` → **{result}** (exit `{execution.get('exitCode', 'n/a')}`)")
            if execution.get("governanceCounts"):
                lines.append(f"  - Runtime Governance observed: `{execution['governanceCounts']}`")
    else:
        lines.append("- Static scan only; no target command was executed.")
    if report.get("profile"):
        profile = report["profile"]
        lines.extend(["", f"## Domain profile — {profile['name']}", "", f"**Score:** {profile['score']['value']}/{profile['score']['max']}  ", f"**Confidence:** {profile['score']['confidence']}/100", "", "| Control | Score | Status |", "| --- | ---: | --- |"])
        for control in profile["controls"]:
            lines.append(f"| {control['name']} | {control['earned']}/{control['weight']} | {control['status']} |")
        if profile["findings"]:
            lines.extend(["", "### Profile findings", ""])
            for finding in profile["findings"]:
                lines.append(f"- **{finding['severity']} · {finding['title']}**：{finding['detail']}")
    if report.get("comparison"):
        comparison = report["comparison"]
        lines.extend(["", "## Baseline comparison", "", f"- Score: `{comparison['scoreBefore']}` → `{comparison['scoreAfter']}` (`{comparison['scoreDelta']:+d}`)", f"- Confidence: `{comparison.get('confidenceBefore', 'n/a')}` → `{comparison.get('confidenceAfter', 'n/a')}`"])
        for delta in comparison.get("dimensionDeltas", []):
            if delta["delta"]:
                lines.append(f"- {delta['name']}: `{delta['before']}` → `{delta['after']}` (`{delta['delta']:+d}`)")
    lines.extend(["", "## Evidence rule", "", "This score is not a test-count total. It is a weighted maturity score with hard caps, evidence references, confidence, and an explicit human/real-host boundary."])
    return "\n".join(lines) + "\n"


def terminal_report(report: dict[str, Any], colors: bool = True) -> str:
    """Render a human-facing, color-aware terminal verdict."""
    score = report["score"]
    target = report["target"]
    decision = str(score.get("decision", "CONDITIONAL"))
    decision_tone = {"READY": "green", "CONDITIONAL": "yellow", "BLOCKED": "red"}.get(decision, "white")
    score_value = int(score.get("value", 0))
    score_tone = "green" if score_value >= 90 else "yellow" if score_value >= 70 else "red"
    score_label = paint(f"{score_value}/{score.get('max', 100)}", score_tone, colors, bold=True)
    confidence_tone = "green" if score.get("confidence", 0) >= 85 else "yellow"
    confidence_label = paint(f"{score.get('confidence', 0)}/100", confidence_tone, colors, bold=True)
    maturity = score.get("maturity", {})
    executions = report.get("executions", [])
    hosts = report.get("hosts", [])
    configured = sum(1 for host in hosts if host.get("configured"))
    unknown_smoke = sum(1 for host in hosts if host.get("smokeTest") == "unknown")
    governance: list[str] = []
    for execution in executions:
        counts = execution.get("governanceCounts", [])
        if counts:
            governance.append(f"{execution.get('mode')}: {', '.join(str(value) for value in counts)}")

    lines = [
        "",
        paint("╭─ HEKOUWANG HARNESS DOCTOR ─────────────────────────╮", "cyan", colors, bold=True),
        f"│ TARGET      {target.get('name', 'Harness')}",
        f"│ HEAD        {str(target.get('git', {}).get('head') or 'unknown')[:12]} · dirty={target.get('git', {}).get('dirty')}",
        "├─────────────────────────────────────────────────────┤",
        f"│ SCORE       {score_label}     CONFIDENCE {confidence_label}",
        f"│ DECISION    {paint(decision, decision_tone, colors, bold=True)}     MATURITY {maturity.get('id', '—')} · {maturity.get('name', '—')}",
        f"│ HARD CAPS   {paint(str(len(score.get('caps', []))), 'red' if score.get('caps') else 'green', colors, bold=True)} active",
        "├─ DIMENSIONS ────────────────────────────────────────┤",
    ]
    for dimension in report.get("dimensions", []):
        weight = int(dimension.get("weight", 0))
        earned = int(dimension.get("earned", 0))
        filled = round(10 * earned / weight) if weight else 0
        status = str(dimension.get("status", "missing"))
        tone = {"pass": "green", "partial": "yellow", "missing": "red", "fail": "red"}.get(status, "white")
        bar = paint("█" * filled, "green" if status == "pass" else tone, colors) + paint("░" * (10 - filled), "dim", colors)
        lines.append(f"│ {paint('●', tone, colors)} {dimension.get('name', dimension.get('id'))}  {bar} {earned}/{weight} {paint(status.upper(), tone, colors, bold=True)}")
    lines.extend([
        "├─ RUNTIME EVIDENCE ──────────────────────────────────┤",
    ])
    for execution in executions:
        if not execution.get("executed"):
            lines.append(f"│ {paint('✕', 'red', colors)} {execution.get('mode', 'unknown')} · not executed · {execution.get('reason', 'unknown reason')}")
            continue
        tone = "green" if execution.get("passed") else "red"
        counts = ", ".join(str(value) for value in execution.get("governanceCounts", [])) or "—"
        lines.append(f"│ {paint('✓' if execution.get('passed') else '✕', tone, colors)} {execution.get('mode')} · exit {execution.get('exitCode')} · {execution.get('durationSeconds')}s · governance {counts}")
    if not executions:
        lines.append(f"│ {paint('·', 'yellow', colors)} static scan only · no verifier executed")
    lines.extend([
        f"│ GOVERNANCE  {paint(' · '.join(governance) if governance else 'not observed', 'cyan', colors)}",
        f"│ HOSTS       {configured}/{len(hosts)} configured · {unknown_smoke} smoke tests unknown",
    ])
    profile = report.get("profile")
    if profile:
        profile_score = profile.get("score", {})
        lines.append(f"│ PROFILE     {profile.get('name', profile.get('id', 'profile'))} · {profile_score.get('value', 0)}/{profile_score.get('max', 0)} · confidence {profile_score.get('confidence', 0)}")
    lines.append("╰─────────────────────────────────────────────────────╯")
    findings = report.get("findings", [])
    if findings:
        lines.append("")
        lines.append(paint("FINDINGS", "yellow", colors, bold=True))
        for finding in findings[:4]:
            severity = finding.get("severity", "P2")
            tone = "red" if severity in {"P0", "P1"} else "yellow"
            lines.append(f"  {paint(severity, tone, colors, bold=True)} · {finding.get('title', 'finding')}")
    lines.append("")
    lines.append(paint("Evidence-first · configured ≠ triggered · test count ≠ quality score", "dim", colors))
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate an evidence-first Harness scorecard.")
    parser.add_argument("repo", help="Target Harness repository")
    parser.add_argument("--format", choices=["json", "markdown", "terminal"], default="markdown")
    parser.add_argument("--output", help="Write the report to this path")
    parser.add_argument("--mode", action="append", choices=["working-tree", "staged", "ci"], help="Execute verify.sh in this mode; repeat for multiple modes")
    parser.add_argument("--profile", help="Optional domain profile name or JSON path, for example content-agent")
    parser.add_argument("--baseline", help="Optional previous JSON scorecard for score/dimension deltas")
    parser.add_argument("--live", action="store_true", help="Show animated live verification progress on stderr")
    parser.add_argument("--color", choices=["auto", "always", "never"], default="auto", help="Color policy for live/terminal output")
    args = parser.parse_args(argv)
    root = Path(args.repo).expanduser().resolve()
    if not root.is_dir():
        print(f"Target is not a directory: {root}", file=sys.stderr)
        return 2
    try:
        live = args.live or args.format == "terminal"
        report = scan(root, args.mode, args.profile, live=live, color=args.color)
        if args.baseline:
            baseline_path = Path(args.baseline).expanduser().resolve()
            baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
            report["comparison"] = compare_reports(report, baseline, str(baseline_path))
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as error:
        print(str(error), file=sys.stderr)
        return 2
    if args.format == "json":
        content = json.dumps(report, ensure_ascii=False, indent=2)
    elif args.format == "terminal":
        content = terminal_report(report, colors=color_is_enabled(args.color) and not args.output)
    else:
        content = markdown(report)
    if args.output:
        Path(args.output).expanduser().resolve().write_text(content + ("" if content.endswith("\n") else "\n"), encoding="utf-8")
    else:
        print(content, end="" if content.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
