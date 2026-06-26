from __future__ import annotations

import importlib
import json
import re
import subprocess
import sys
from importlib import metadata
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[2]
REQUIREMENTS_FILE = SKILL_DIR / "requirements.txt"
_REQUIREMENT_SPLIT_RE = re.compile(r"\s*(?:\[|===|==|~=|!=|<=|>=|<|>|@)")
_OPTION_PREFIXES = (
    "-r",
    "--requirement",
    "-c",
    "--constraint",
    "-f",
    "--find-links",
    "--index-url",
    "--extra-index-url",
    "--trusted-host",
    "--pre",
    "--prefer-binary",
    "--no-index",
    "--only-binary",
    "--no-binary",
)


def _clean_requirement_line(raw_line: str) -> str:
    line = raw_line.strip()
    if not line or line.startswith("#"):
        return ""
    return re.split(r"\s+#", line, maxsplit=1)[0].strip()


def _extract_distribution_name(line: str) -> str | None:
    if not line or line.startswith(_OPTION_PREFIXES):
        return None

    if line.startswith(("-e ", "--editable ")):
        _, _, editable_target = line.partition(" ")
        editable_target = editable_target.strip()
        if "#egg=" not in editable_target:
            return None
        candidate = editable_target.split("#egg=", maxsplit=1)[1].strip()
    else:
        candidate = line.split(";", maxsplit=1)[0].strip()
        if " @ " in candidate:
            candidate = candidate.split(" @ ", maxsplit=1)[0].strip()
        else:
            candidate = _REQUIREMENT_SPLIT_RE.split(candidate, maxsplit=1)[0].strip()

    if "[" in candidate:
        candidate = candidate.split("[", maxsplit=1)[0].strip()
    return candidate or None


def _required_distributions(requirements_file: Path) -> list[str]:
    names: list[str] = []
    seen: set[str] = set()
    for raw_line in requirements_file.read_text(encoding="utf-8").splitlines():
        line = _clean_requirement_line(raw_line)
        candidate = _extract_distribution_name(line)
        if not candidate:
            continue
        normalized = re.sub(r"[-_.]+", "-", candidate).lower()
        if normalized in seen:
            continue
        seen.add(normalized)
        names.append(candidate)
    return names


def _is_distribution_installed(name: str) -> bool:
    try:
        metadata.version(name)
        return True
    except metadata.PackageNotFoundError:
        return False


def _manual_install_command(requirements_file: Path) -> list[str]:
    return [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)]


def _tail(text: str, *, max_lines: int = 20) -> list[str]:
    lines = [line for line in str(text or "").splitlines() if line.strip()]
    return lines[-max_lines:]


def _print_json_error(message: str, *, details: dict) -> None:
    json.dump({"ok": False, "error": message, "details": details}, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def ensure_requirements_installed(requirements_file: Path | None = None) -> None:
    active_requirements = Path(requirements_file or REQUIREMENTS_FILE)
    if not active_requirements.exists():
        _print_json_error(
            "Automatic dependency bootstrap failed because requirements.txt was not found.",
            details={
                "requirements_file": str(active_requirements),
                "install_command": _manual_install_command(active_requirements),
            },
        )
        raise SystemExit(1)

    required_distributions = _required_distributions(active_requirements)
    if not required_distributions:
        return

    missing_distributions = [name for name in required_distributions if not _is_distribution_installed(name)]
    if not missing_distributions:
        return

    install_command = _manual_install_command(active_requirements)
    sys.stderr.write(
        "[jumpserver-skills] Missing Python dependencies detected: %s. Installing with %s\n"
        % (", ".join(missing_distributions), " ".join(install_command))
    )
    result = subprocess.run(install_command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        _print_json_error(
            "Automatic dependency installation failed.",
            details={
                "requirements_file": str(active_requirements),
                "missing_distributions": missing_distributions,
                "install_command": install_command,
                "pip_exit_code": result.returncode,
                "stderr_tail": _tail(result.stderr),
                "stdout_tail": _tail(result.stdout),
            },
        )
        raise SystemExit(1)

    importlib.invalidate_caches()
    remaining_distributions = [name for name in missing_distributions if not _is_distribution_installed(name)]
    if remaining_distributions:
        _print_json_error(
            "Automatic dependency installation finished but required packages are still unavailable.",
            details={
                "requirements_file": str(active_requirements),
                "missing_distributions": remaining_distributions,
                "install_command": install_command,
            },
        )
        raise SystemExit(1)
