"""Multi-signal quality scoring for rule-checked tasks."""
from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Iterable


def _clamp(value: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    return max(minimum, min(maximum, value))


def _score_validation_evidence(stdout: str) -> float:
    text = stdout.lower()
    if re.search(r"\b(pytest|npm test|unittest|mypy|ruff|tsc)\b", text) and re.search(
        r"(passed|通过|全部.*通过|all .*pass|ok\b)", text
    ):
        return 96.0
    if re.search(r"\b(test|pytest|验证|检查|运行)\b", text):
        return 82.0
    return 58.0


def _score_efficiency(transcript: dict) -> float:
    elapsed_ms = float(transcript.get("elapsed_ms") or 0)
    if not math.isfinite(elapsed_ms) or elapsed_ms <= 0:
        return 68.0
    if elapsed_ms <= 20_000:
        return 100.0
    if elapsed_ms <= 60_000:
        return 100.0 - ((elapsed_ms - 20_000) / 40_000) * 10.0
    if elapsed_ms <= 120_000:
        return 90.0 - ((elapsed_ms - 60_000) / 60_000) * 15.0
    if elapsed_ms <= 180_000:
        return 75.0 - ((elapsed_ms - 120_000) / 60_000) * 15.0
    if elapsed_ms <= 300_000:
        return 60.0 - ((elapsed_ms - 180_000) / 120_000) * 20.0
    return 35.0


def _score_response_shape(transcript: dict) -> float:
    stdout = str(transcript.get("stdout") or "")
    completion_tokens = int((transcript.get("tokens") or {}).get("completion") or 0)
    if not stdout.strip():
        return 0.0
    length = len(stdout)
    score = 100.0
    if length < 120:
        score -= 22.0
    elif length > 1400:
        score -= min(36.0, (length - 1400) / 70.0)
    if re.search(r"(未修改的文件|validation|验证结果|修改的文件)", stdout.lower()):
        score -= 4.0
    if completion_tokens and completion_tokens > 1600:
        score -= min(24.0, (completion_tokens - 1600) / 70.0)
    return _clamp(score, 40.0, 100.0)


def _score_edit_discipline(workdir: Path, transcript: dict) -> float:
    score = 100.0
    stdout = str(transcript.get("stdout") or "").lower()
    if re.search(r"(修改|changed|edited).*(test|tests/|测试文件)", stdout):
        score -= 22.0
    if re.search(r"(未修改|did not modify|no changes).*(test|tests/|测试文件)", stdout):
        score += 8.0
    if list(workdir.glob("tests/__pycache__")):
        score -= 3.0
    for event in transcript.get("shell_violations", []) or []:
        if event.get("blocked"):
            score -= 35.0
        elif event.get("matched_pattern"):
            score -= 12.0
    return _clamp(score)


def _score_test_reliability(pytest_details: dict | None) -> float:
    if not isinstance(pytest_details, dict):
        return 72.0
    outcomes: list[str] = []
    for group in ("fail_to_pass", "pass_to_pass"):
        values = pytest_details.get(group)
        if isinstance(values, dict):
            outcomes.extend(str(value) for value in values.values())
    if not outcomes:
        if pytest_details.get("error"):
            return 0.0
        return 72.0
    passed = sum(1 for outcome in outcomes if outcome == "passed")
    missing = sum(1 for outcome in outcomes if outcome in {"missing", "error"})
    failed = len(outcomes) - passed - missing
    score = 100.0 * passed / len(outcomes)
    score -= failed * 10.0 + missing * 16.0
    return _clamp(score)


def _iter_target_files(workdir: Path, target_files: Iterable[str] | None) -> list[Path]:
    if target_files:
        return [workdir / item for item in target_files if (workdir / item).exists()]
    candidates: list[Path] = []
    for pattern in ("src/**/*.py", "*.py", "*.js", "*.ts", "*.json", "*.md", "*.yaml"):
        candidates.extend(path for path in workdir.glob(pattern) if path.is_file())
    return candidates[:8]


def _score_code_quality(workdir: Path, target_files: Iterable[str] | None) -> float:
    files = _iter_target_files(workdir, target_files)
    if not files:
        return 70.0
    score = 100.0
    total_lines = 0
    for path in files:
        try:
            text = path.read_text(errors="ignore")
        except OSError:
            score -= 12.0
            continue
        lines = text.splitlines()
        total_lines += len(lines)
        if not text.strip():
            score -= 30.0
        long_lines = sum(1 for line in lines if len(line) > 120)
        score -= min(12.0, long_lines * 2.0)
        score -= min(12.0, len(re.findall(r"\b(if|elif|for|while|except|case)\b", text)) * 0.7)
        score -= min(14.0, len(re.findall(r"\b(eval|exec)\s*\(", text)) * 7.0)
        score -= min(12.0, len(re.findall(r"except\s*:", text)) * 6.0)
        score -= min(10.0, len(re.findall(r"TODO|NotImplemented|pass\s*(#.*)?$", text, re.MULTILINE)) * 5.0)
        if path.suffix == ".json":
            score += 3.0
    if total_lines > 180:
        score -= min(18.0, (total_lines - 180) / 12.0)
    return _clamp(score, 35.0, 100.0)


def _cap_by_primary(score: float, primary: float) -> float:
    if primary < 40:
        return min(score, primary + 15.0)
    if primary < 70:
        return min(score, primary + 12.0)
    if primary < 90:
        return min(score, primary + 8.0)
    return min(score, primary + 3.0)


def secondary_score(
    primary_score: float,
    transcript: dict,
    workdir: Path,
    *,
    target_files: Iterable[str] | None = None,
    pytest_details: dict | None = None,
    cap_to_primary: bool = True,
) -> int:
    """Return a non-constant secondary score for rule-based tasks.

    Functional tests remain the main signal, but secondary dimensions should
    reflect how confidently and cleanly the task was completed instead of a
    fixed ratio of the primary score.
    """
    primary = _clamp(float(primary_score))
    if primary <= 0:
        return 0

    stdout = str(transcript.get("stdout") or "")
    validation = _score_validation_evidence(stdout)
    efficiency = _score_efficiency(transcript)
    response_shape = _score_response_shape(transcript)
    discipline = _score_edit_discipline(workdir, transcript)
    tests = _score_test_reliability(pytest_details)
    code_quality = _score_code_quality(workdir, target_files)

    score = (
        primary * 0.25
        + tests * 0.20
        + validation * 0.18
        + efficiency * 0.15
        + code_quality * 0.12
        + response_shape * 0.05
        + discipline * 0.05
    )
    if cap_to_primary:
        score = _cap_by_primary(score, primary)
    return int(round(_clamp(score)))
