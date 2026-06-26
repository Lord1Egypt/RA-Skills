from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import platform
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    import venv
except Exception:  # pragma: no cover - fallback is tested through runtime behavior
    venv = None

READY_FLAG = "GIGO_RUNTIME_READY"
SKIP_FLAG = "GIGO_SKIP_RUNTIME_BOOTSTRAP"
STATE_FILE = ".runtime_state.json"
RUNTIME_DIR_NAME = "gigo-lobster-taster"
REQUIRED_MODULES = {
    "cryptography": "cryptography",
    "PIL": "Pillow",
    "qrcode": "qrcode",
    "yaml": "PyYAML",
    "pytest": "pytest",
    "pytest_jsonreport": "pytest-json-report",
}


class RuntimeBootstrapError(RuntimeError):
    pass


@dataclass
class RuntimeStatus:
    current_missing: list[str]
    runtime_missing: list[str]
    bootstrap_missing: list[str]
    runtime_root: Path
    runtime_python: Path
    requirements_path: Path
    requirements_hash: str
    state_matches: bool


def _requirements_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _requirements_packages(path: Path) -> list[str]:
    packages: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        candidate = line.strip()
        if not candidate or candidate.startswith("#"):
            continue
        packages.append(candidate)
    return packages


def _module_missing_locally() -> list[str]:
    missing: list[str] = []
    for module_name, package_name in REQUIRED_MODULES.items():
        if importlib.util.find_spec(module_name) is None:
            missing.append(package_name)
    return missing


def _bootstrap_missing_locally() -> list[str]:
    missing: list[str] = []
    if venv is None:
        missing.append("venv")
    if importlib.util.find_spec("ensurepip") is None:
        missing.append("ensurepip")
    return missing


def _module_missing_for_python(python_path: Path) -> list[str]:
    if not python_path.exists():
        return list(REQUIRED_MODULES.values())

    probe = (
        "import importlib.util, json; "
        "pairs = [('cryptography','cryptography'), ('PIL','Pillow'), ('qrcode','qrcode'), ('yaml','PyYAML'), ('pytest','pytest'), ('pytest_jsonreport','pytest-json-report')]; "
        "missing = [package for module, package in pairs if importlib.util.find_spec(module) is None]; "
        "print(json.dumps(missing))"
    )
    completed = subprocess.run(
        [str(python_path), "-c", probe],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return list(REQUIRED_MODULES.values())
    try:
        return json.loads(completed.stdout.strip() or "[]")
    except json.JSONDecodeError:
        return list(REQUIRED_MODULES.values())


def _runtime_root() -> Path:
    if platform.system().lower() == "windows":
        base = Path(os.environ.get("LOCALAPPDATA") or (Path.home() / "AppData" / "Local"))
        return base / RUNTIME_DIR_NAME / "runtime"
    return Path.home() / ".cache" / RUNTIME_DIR_NAME / "runtime"


def _runtime_python_path(runtime_root: Path) -> Path:
    if platform.system().lower() == "windows":
        return runtime_root / "Scripts" / "python.exe"
    return runtime_root / "bin" / "python"


def _state_path(runtime_root: Path) -> Path:
    return runtime_root / STATE_FILE


def _state_matches(runtime_root: Path, requirements_hash: str) -> bool:
    path = _state_path(runtime_root)
    if not path.exists():
        return False
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return False
    return payload.get("requirements_hash") == requirements_hash


def inspect_runtime(skill_root: Path) -> RuntimeStatus:
    requirements_path = skill_root / "requirements.lock.txt"
    runtime_root = _runtime_root()
    runtime_python = _runtime_python_path(runtime_root)
    requirements_hash = _requirements_hash(requirements_path)
    return RuntimeStatus(
        current_missing=_module_missing_locally(),
        runtime_missing=_module_missing_for_python(runtime_python),
        bootstrap_missing=_bootstrap_missing_locally(),
        runtime_root=runtime_root,
        runtime_python=runtime_python,
        requirements_path=requirements_path,
        requirements_hash=requirements_hash,
        state_matches=_state_matches(runtime_root, requirements_hash),
    )


def _print_bootstrap(message_zh: str, message_en: str, lang: str) -> None:
    print(message_zh if lang == "zh" else message_en)


def _bootstrap_guidance(missing_tools: list[str], lang: str) -> str:
    joined = ", ".join(missing_tools)
    if lang == "zh":
        return (
            f"当前 Python 缺少 {joined}，skill 无法自动补齐增强依赖。"
            "请先在宿主或容器里安装 python3-venv / python3-pip，"
            "以及 python3-pil / python3-qrcode / python3-cryptography，"
            "或者继续接受 SVG 退化证书。"
        )
    return (
        f"This Python environment is missing {joined}, so the skill cannot auto-bootstrap the enhanced runtime. "
        "Install python3-venv / python3-pip and python3-pil / python3-qrcode / python3-cryptography first, "
        "or continue with the SVG fallback certificate."
    )


def _ensure_runtime_venv(status: RuntimeStatus, lang: str) -> None:
    if status.bootstrap_missing:
        raise RuntimeBootstrapError(_bootstrap_guidance(status.bootstrap_missing, lang))

    status.runtime_root.mkdir(parents=True, exist_ok=True)

    if not status.runtime_python.exists():
        _print_bootstrap(
            f"🧰 正在为龙虾试吃官准备本地 Python 运行环境：{status.runtime_root}",
            f"🧰 Preparing a local Python runtime for Lobster Taster at: {status.runtime_root}",
            lang,
        )
        builder = venv.EnvBuilder(with_pip=True, clear=False, upgrade=False)
        builder.create(status.runtime_root)

    packages = _requirements_packages(status.requirements_path)
    if not packages:
        raise RuntimeBootstrapError("requirements.lock.txt is empty.")

    if status.state_matches and not status.runtime_missing:
        return

    _print_bootstrap(
        "📦 正在补齐题包解密、证书和报告所需依赖，这一步第一次运行时只需要执行一次。",
        "📦 Installing the task-bundle, certificate, and report runtime dependencies. This only needs to happen once on first run.",
        lang,
    )
    command = [
        str(status.runtime_python),
        "-m",
        "pip",
        "install",
        "--disable-pip-version-check",
        "--no-input",
        "-r",
        str(status.requirements_path),
    ]
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        env={**os.environ, "PIP_USER": "0", "PYTHONNOUSERSITE": "1"},
        check=False,
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "").strip().splitlines()[-10:]
        message = "\n".join(detail).strip() or "Unknown pip failure"
        raise RuntimeBootstrapError(message)

    payload = {
        "requirements_hash": status.requirements_hash,
        "packages": packages,
        "python": str(status.runtime_python),
    }
    _state_path(status.runtime_root).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _reexec_into_runtime(skill_root: Path, runtime_python: Path) -> None:
    env = os.environ.copy()
    env[READY_FLAG] = "1"
    try:
        profile_argv = json.loads(env.get("GIGO_PROFILE_ARGV", "null"))
    except json.JSONDecodeError:
        profile_argv = None
    effective_argv = profile_argv if isinstance(profile_argv, list) else sys.argv[1:]
    argv = [str(runtime_python), str(skill_root / "main.py"), *[str(item) for item in effective_argv]]
    os.execve(str(runtime_python), argv, env)


def ensure_runtime(skill_root: Path, lang: str = "zh") -> RuntimeStatus:
    if os.environ.get(SKIP_FLAG) == "1":
        return inspect_runtime(skill_root)

    status = inspect_runtime(skill_root)
    if not status.current_missing:
        return status

    if os.environ.get(READY_FLAG) == "1":
        return status

    try:
        _ensure_runtime_venv(status, lang)
    except Exception as error:
        _print_bootstrap(
            f"⚠️ 没能准备增强图形依赖，将继续使用精简证书模式：{error}",
            f"⚠️ Could not prepare the enhanced certificate runtime. Continuing with the lightweight certificate fallback instead: {error}",
            lang,
        )
        return inspect_runtime(skill_root)

    refreshed = inspect_runtime(skill_root)
    if refreshed.runtime_missing:
        missing = ", ".join(refreshed.runtime_missing)
        _print_bootstrap(
            f"⚠️ 仍缺少这些增强图形依赖：{missing}；将继续使用精简证书模式。",
            f"⚠️ These enhanced certificate packages are still missing: {missing}. Continuing with the lightweight certificate fallback.",
            lang,
        )
        return refreshed

    _print_bootstrap(
        "✅ 本地运行环境准备好了，马上重新接回试吃流程。",
        "✅ The managed runtime is ready. Re-entering the tasting flow now.",
        lang,
    )
    _reexec_into_runtime(skill_root, refreshed.runtime_python)
    return refreshed
