from __future__ import annotations

import argparse
import base64
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, request
from zipfile import ZIP_DEFLATED, ZipFile

SENSITIVE_ENV_KEYS = (
    "CLAWHUB_API_TOKEN",
    "MOLTBOOK_WEBHOOK_URL",
    "ZHIHU_WEBHOOK_URL",
    "XIAOHONGSHU_WEBHOOK_URL",
    "X_API_KEY",
    "X_API_SECRET",
    "X_ACCESS_TOKEN",
    "X_ACCESS_TOKEN_SECRET",
)

SENSITIVE_KEY_HINTS = ("token", "secret", "password", "api_key", "apikey")
GENERIC_SECRET_PATTERN = re.compile(
    r"(?i)\b(api[_-]?key|access[_-]?token|secret|password)\b\s*[:=]\s*([^\s\"',;]+)"
)
BEARER_PATTERN = re.compile(r"(?i)\bbearer\s+[a-z0-9\-._~+/=]{10,}\b")
QUERY_SECRET_PATTERN = re.compile(
    r"(?i)(token|access_token|api_key|apikey|secret|password)=([^&\s]+)"
)


@dataclass
class PublishResult:
    target: str
    status: str
    detail: str


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _safe_slug(text: str) -> str:
    raw = "".join(ch.lower() if ch.isalnum() else "-" for ch in text.strip())
    while "--" in raw:
        raw = raw.replace("--", "-")
    return raw.strip("-") or "generated-skill"


def _validate_success_case(data: dict[str, Any]) -> None:
    required = ["title", "user_goal", "steps", "outcome"]
    missing = [k for k in required if k not in data]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")
    if not isinstance(data["steps"], list) or not data["steps"]:
        raise ValueError("steps must be a non-empty list")
    if not bool(data.get("outcome", {}).get("completed")):
        raise ValueError("outcome.completed is false; aborting skill extraction")


def _sanitize_text(text: str) -> str:
    text = BEARER_PATTERN.sub("Bearer [REDACTED]", text)
    text = GENERIC_SECRET_PATTERN.sub(r"\1=[REDACTED]", text)
    text = QUERY_SECRET_PATTERN.sub(r"\1=[REDACTED]", text)
    return text


def _sanitize_object(value: Any, parent_key: str = "") -> Any:
    if isinstance(value, dict):
        sanitized: dict[str, Any] = {}
        for k, v in value.items():
            key_lower = str(k).lower()
            if any(hint in key_lower for hint in SENSITIVE_KEY_HINTS):
                sanitized[k] = "[REDACTED]"
            else:
                sanitized[k] = _sanitize_object(v, parent_key=str(k))
        return sanitized
    if isinstance(value, list):
        return [_sanitize_object(item, parent_key=parent_key) for item in value]
    if isinstance(value, str):
        return _sanitize_text(value)
    return value


def _collect_active_secret_values() -> list[str]:
    values: list[str] = []
    for key, raw in os.environ.items():
        if not raw:
            continue
        key_lower = key.lower()
        if key in SENSITIVE_ENV_KEYS or any(hint in key_lower for hint in SENSITIVE_KEY_HINTS):
            values.append(raw)
    # Deduplicate while preserving order.
    return list(dict.fromkeys(values))


def _assert_no_secret_leak(root: Path) -> None:
    active_secret_values = _collect_active_secret_values()
    if not active_secret_values:
        return

    for file_path in root.rglob("*"):
        if not file_path.is_file():
            continue
        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for secret in active_secret_values:
            if secret and secret in text:
                raise ValueError(
                    f"Potential secret leak detected in {file_path}. "
                    "Aborting publish payload generation."
                )
        if BEARER_PATTERN.search(text) or QUERY_SECRET_PATTERN.search(text):
            raise ValueError(
                f"Potential credential pattern detected in {file_path}. "
                "Aborting publish payload generation."
            )


def _require_env(name: str, purpose: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(f"Missing required env `{name}` for {purpose}")
    return value


def _score_step(step: dict[str, Any], idx: int, total: int) -> float:
    success_bonus = 2.0 if step.get("success_signal") else 0.5
    efficiency = 1.0 / max(step.get("duration_minutes", 10), 1)
    position = (total - idx) / max(total, 1)
    return success_bonus + (efficiency * 5) + position


def _build_summary(data: dict[str, Any]) -> str:
    lines = [
        f"# Success Summary: {data['title']}",
        "",
        f"- Goal: {data['user_goal']}",
        f"- Completed: {data.get('outcome', {}).get('completed', False)}",
        f"- Evidence: {data.get('outcome', {}).get('evidence', 'N/A')}",
    ]
    metrics = data.get("outcome", {}).get("metrics", {})
    if metrics:
        lines.append("- Metrics:")
        for k, v in metrics.items():
            lines.append(f"  - {k}: {v}")

    lines.extend(["", "## Step Trace", ""])
    for i, step in enumerate(data["steps"], start=1):
        lines.append(
            f"{i}. {step.get('action', 'unknown action')} -> {step.get('result', 'no result')}"
        )
    return "\n".join(lines) + "\n"


def _build_optimal_path(data: dict[str, Any]) -> str:
    scored: list[tuple[float, dict[str, Any], int]] = []
    total = len(data["steps"])
    for idx, step in enumerate(data["steps"]):
        scored.append((_score_step(step, idx, total), step, idx))

    # Preserve dependency ordering by original index after selecting top confidence steps.
    top = sorted(scored, key=lambda x: x[0], reverse=True)
    keep_n = max(3, min(len(top), 6))
    selected = sorted(top[:keep_n], key=lambda x: x[2])

    lines = [
        f"# Optimal Path: {data['title']}",
        "",
        "This path keeps high-impact steps with the best confidence/efficiency balance.",
        "",
        "## Recommended Sequence",
        "",
    ]
    for i, (score, step, _) in enumerate(selected, start=1):
        duration = step.get("duration_minutes", "?")
        lines.append(
            f"{i}. {step.get('action', 'unknown action')} (score={score:.2f}, {duration} min)"
        )
        lines.append(f"   - Expected outcome: {step.get('result', 'N/A')}")

    lines.extend(
        [
            "",
            "## Reuse Guidelines",
            "",
            "- Keep validation evidence attached to each major step.",
            "- Preserve idempotency and rollback behavior from the original run.",
            "- Stop auto-execution when confidence drops below operational threshold.",
            "",
        ]
    )
    return "\n".join(lines)


def _generated_skill_content(data: dict[str, Any]) -> tuple[str, str]:
    title = data["title"]
    goal = data["user_goal"]
    slug = _safe_slug(title)

    skill_md = f"""---
name: {slug}
description: Reproduce the validated implementation path for: {title}. Use when users want to achieve similar outcomes quickly with proven execution order, validation checkpoints, and rollout guardrails.
---

# {title}

Turn a similar request into a repeatable implementation workflow.

## Goal

- {goal}

## Preconditions

- Confirm acceptance criteria and constraints.
- Confirm required environment and secrets before execution.

## Execution Path
"""
    for i, step in enumerate(data["steps"], start=1):
        skill_md += (
            f"\n{i}. {step.get('action', 'unknown action')}"
            f"\n   - Success signal: {bool(step.get('success_signal'))}"
            f"\n   - Expected result: {step.get('result', 'N/A')}\n"
        )

    skill_md += """
## Guardrails

- Pause before high-impact external operations.
- Keep an audit trail for every execution decision.
- Prefer reversible changes and explicit approval gates.

## Deliverables

- Implementation patch
- Validation report
- Operational runbook
"""

    openai_yaml = f"""display_name: {title}
short_description: Reuse a proven path to deliver the same outcome with less trial-and-error.
default_prompt: Apply this proven workflow to my request, adapt for my constraints, and preserve the same quality gates.
"""
    return skill_md, openai_yaml


def _build_share_payloads(data: dict[str, Any]) -> dict[str, str]:
    title = data["title"]
    goal = data["user_goal"]

    zh = (
        f"# 复盘：{title}\n\n"
        f"目标：{goal}\n"
        "这次和 OpenClaw 的协作中，我们把问题拆成可验证步骤，并在关键节点做了验证闭环。\n"
        "最终不仅完成任务，还沉淀为可复用 skill，可直接复刻到相似场景。\n\n"
        "核心方法：\n"
        "1. 先明确成功标准\n"
        "2. 把路径拆成可验证步骤\n"
        "3. 每步留证据并可回滚\n"
        "4. 任务完成后立即抽象为 skill\n"
    )

    en = (
        f"# Postmortem: {title}\n\n"
        f"Goal: {goal}\n"
        "This OpenClaw collaboration succeeded because we used a validation-first execution loop. "
        "After delivery, we distilled the process into a reusable skill for fast repeatability.\n\n"
        "Method:\n"
        "1. Define success criteria first\n"
        "2. Break execution into verifiable steps\n"
        "3. Keep evidence and rollback-friendly changes\n"
        "4. Convert successful flow into a reusable skill immediately\n"
    )

    return {
        "moltbook": zh + "\n---\n\n" + en,
        "zhihu": zh,
        "xiaohongshu": zh,
    }


def _build_clawhub_bilingual_metadata(data: dict[str, Any]) -> dict[str, str]:
    title_en = str(data.get("title", "Generated Skill")).strip() or "Generated Skill"
    goal_zh = str(data.get("user_goal", "完成目标任务")).strip() or "完成目标任务"

    return {
        "display_name_zh": "OpenClaw 成功流程沉淀发布器",
        "display_name_en": "OpenClaw Success Skill Publisher",
        "short_description_zh": "将成功协作自动沉淀为可复用 Skill，分析最优路径并发布。",
        "short_description_en": "Convert successful collaborations into reusable skills with optimal-path analysis and publishing.",
        "description_zh": (
            f"基于成功案例自动提炼可复用 Skill，目标：{goal_zh}。"
            "支持流程总结、最优路径分析、ClawHub 发布与多平台分发。"
        ),
        "description_en": (
            f"Auto-extract a reusable skill from a successful case. Goal: {title_en}. "
            "Includes process summary, optimal path analysis, ClawHub publishing, and multi-platform distribution."
        ),
    }


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _zip_generated_skill(skill_dir: Path, zip_path: Path) -> None:
    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as archive:
        for file_path in sorted(skill_dir.rglob("*")):
            if file_path.is_file():
                archive.write(file_path, arcname=file_path.relative_to(skill_dir).as_posix())


def _post_json(url: str, token: str | None, payload: dict[str, Any]) -> tuple[bool, str]:
    body = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = request.Request(url=url, data=body, headers=headers, method="POST")
    try:
        with request.urlopen(req, timeout=30) as resp:
            text = resp.read().decode("utf-8", errors="replace")
            return True, f"HTTP {resp.status}: {text[:500]}"
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        return False, f"HTTP {exc.code}: {detail[:500]}"
    except Exception as exc:  # pylint: disable=broad-except
        return False, str(exc)


def _publish_clawhub(
    generated_skill_zip: Path,
    title: str,
    bilingual_metadata: dict[str, str],
    dry_run: bool,
) -> PublishResult:
    base = os.getenv("CLAWHUB_API_BASE", "").rstrip("/")
    token = os.getenv("CLAWHUB_API_TOKEN", "").strip()

    if not dry_run:
        base = _require_env("CLAWHUB_API_BASE", "ClawHub publish").rstrip("/")
        token = _require_env("CLAWHUB_API_TOKEN", "ClawHub publish")
    elif not base:
        return PublishResult("clawhub", "skipped", "CLAWHUB_API_BASE not set (dry-run)")

    payload = {
        "name": _safe_slug(title),
        "title": title,
        "bundle_path": str(generated_skill_zip),
        "bundle_b64": base64.b64encode(generated_skill_zip.read_bytes()).decode("ascii"),
        "i18n": bilingual_metadata,
    }
    if dry_run:
        return PublishResult("clawhub", "dry-run", f"Prepared publish payload for {base}/v1/skills")

    ok, detail = _post_json(f"{base}/v1/skills", token, payload)
    return PublishResult("clawhub", "success" if ok else "failed", detail)


def _share_to_platform(
    platform: str,
    content: str,
    dry_run: bool,
) -> PublishResult:
    mapping = {
        "moltbook": "MOLTBOOK_WEBHOOK_URL",
        "zhihu": "ZHIHU_WEBHOOK_URL",
        "xiaohongshu": "XIAOHONGSHU_WEBHOOK_URL",
    }
    env_name = mapping.get(platform)
    if not env_name:
        return PublishResult(platform, "skipped", "unsupported platform")

    url = os.getenv(env_name)
    if not url:
        if dry_run:
            return PublishResult(platform, "skipped", f"{env_name} not set (dry-run)")
        return PublishResult(platform, "failed", f"{env_name} not set")

    payload = {"platform": platform, "content": content}
    if dry_run:
        return PublishResult(platform, "dry-run", f"Prepared share payload for {platform}")

    ok, detail = _post_json(url, None, payload)
    return PublishResult(platform, "success" if ok else "failed", detail)


def run(args: argparse.Namespace) -> int:
    src = Path(args.input).resolve()
    out_dir = Path(args.output).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    data = _read_json(src)
    _validate_success_case(data)
    safe_data = _sanitize_object(data)

    summary = _build_summary(safe_data)
    optimal = _build_optimal_path(safe_data)
    _write_text(out_dir / "summary.md", summary)
    _write_text(out_dir / "optimal_path.md", optimal)

    skill_md, openai_yaml = _generated_skill_content(safe_data)
    generated_skill_dir = out_dir / "generated_skill"
    _write_text(generated_skill_dir / "SKILL.md", skill_md)
    _write_text(generated_skill_dir / "agents" / "openai.yaml", openai_yaml)
    _assert_no_secret_leak(generated_skill_dir)

    bundle_path = out_dir / "generated_skill.zip"
    _zip_generated_skill(generated_skill_dir, bundle_path)

    share_payloads = _build_share_payloads(safe_data)
    for platform, content in share_payloads.items():
        _write_text(out_dir / "share_payloads" / f"{platform}.md", content)
    _assert_no_secret_leak(out_dir)

    report: list[PublishResult] = []
    bilingual_metadata = _build_clawhub_bilingual_metadata(safe_data)
    if args.publish_clawhub:
        report.append(
            _publish_clawhub(
                bundle_path,
                safe_data["title"],
                bilingual_metadata,
                args.dry_run,
            )
        )

    for platform in args.share:
        content = share_payloads.get(platform)
        if content is None:
            report.append(PublishResult(platform, "skipped", "no generated payload"))
            continue
        report.append(_share_to_platform(platform, content, args.dry_run))

    report_json = [r.__dict__ for r in report]
    _write_text(out_dir / "publish_report.json", json.dumps(report_json, ensure_ascii=False, indent=2))

    print(f"Wrote artifacts to: {out_dir}")
    for row in report_json:
        print(f"- {row['target']}: {row['status']} ({row['detail']})")

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract skill from successful OpenClaw interaction")
    parser.add_argument("--input", required=True, help="Path to successful interaction JSON")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--publish-clawhub", action="store_true", help="Publish generated skill to ClawHub")
    parser.add_argument(
        "--share",
        nargs="*",
        default=[],
        choices=["moltbook", "zhihu", "xiaohongshu"],
        help="Share generated post to selected platforms",
    )
    parser.add_argument("--dry-run", action="store_true", help="Generate payloads without calling remote APIs")
    return parser


if __name__ == "__main__":
    raise SystemExit(run(build_parser().parse_args()))
