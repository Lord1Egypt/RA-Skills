#!/usr/bin/env python3
"""Stable launcher for host agents such as OpenClaw.

This wrapper uses only the standard library. It picks or bootstraps the
skill-local virtual environment, loads common OpenClaw dotenv files without
overriding existing environment variables, runs preflight checks, then delegates
to auto_review.py.
"""

import argparse
import os
import shutil
import shlex
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
VENV_PYTHON = SKILL_DIR / ".venv" / "bin" / "python"
REQUIREMENTS = SKILL_DIR / "requirements.txt"
REQUIRED_MODULES = ("PIL", "cv2", "numpy")
SKILL_ENV_NAME = "marketing-material-review-business"


def parse_dotenv_line(line):
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        return None
    if line.startswith("export "):
        line = line[len("export "):].strip()
    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()
    if not key:
        return None
    try:
        value = shlex.split(value)[0] if value else ""
    except ValueError:
        value = value.strip("'\"")
    return key, value


def load_dotenv_files(env):
    candidates = [
        Path.cwd() / ".env",
        SKILL_DIR / ".env",
        Path.home() / ".openclaw" / ".env",
        Path.home() / ".config" / "openclaw" / "gateway.env",
    ]
    loaded = []
    for path in candidates:
        if not path.exists():
            continue
        for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            parsed = parse_dotenv_line(raw_line)
            if not parsed:
                continue
            key, value = parsed
            if key not in env:
                env[key] = value
        loaded.append(str(path))
    return loaded


def choose_python():
    if VENV_PYTHON.exists():
        return str(VENV_PYTHON)
    return find_base_python()


def find_base_python():
    candidates = []
    if sys.implementation.name == "cpython":
        candidates.append(sys.executable)
    for name in ("python3.12", "python3.11", "python3.10", "python3"):
        found = shutil.which(name)
        if found:
            candidates.append(found)
    candidates.append(sys.executable)
    seen = set()
    for candidate in candidates:
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        result = subprocess.run(
            [candidate, "-c", "import sys; raise SystemExit(0 if sys.implementation.name == 'cpython' else 1)"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if result.returncode == 0:
            return candidate
    return sys.executable


def venv_python(venv_dir):
    return venv_dir / "bin" / "python"


def venv_candidates(env):
    candidates = []
    override = env.get("MARKETING_REVIEW_VENV_DIR", "").strip()
    if override:
        candidates.append(Path(override).expanduser())
    candidates.append(SKILL_DIR / ".venv")
    candidates.append(Path.home() / ".cache" / "openclaw" / "skill-venvs" / SKILL_ENV_NAME)
    candidates.append(Path(tempfile.gettempdir()) / "openclaw-skill-venvs" / SKILL_ENV_NAME)
    return candidates


def python_has_modules(python_bin):
    code = "import " + ", ".join(REQUIRED_MODULES)
    result = subprocess.run(
        [python_bin, "-c", code],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def ensure_python_env(env):
    if VENV_PYTHON.exists() and python_has_modules(str(VENV_PYTHON)):
        return str(VENV_PYTHON)
    base_python = find_base_python()
    if python_has_modules(base_python):
        return base_python
    if not REQUIREMENTS.exists():
        return base_python

    errors = []
    for venv_dir in venv_candidates(env):
        python_bin = venv_python(venv_dir)
        if python_bin.exists() and python_has_modules(str(python_bin)):
            return str(python_bin)
        if python_bin.exists():
            print(f"发现已有 Python 环境但依赖不完整，正在补装：{venv_dir}", file=sys.stderr)
        else:
            print(f"首次运行：正在创建 Python 环境 {venv_dir} ...", file=sys.stderr)
            try:
                venv_dir.parent.mkdir(parents=True, exist_ok=True)
                subprocess.run([base_python, "-m", "venv", str(venv_dir)], check=True)
            except (OSError, subprocess.CalledProcessError) as exc:
                errors.append(f"{venv_dir}: {exc}")
                continue
        try:
            pip_command = [
                str(python_bin),
                "-m",
                "pip",
                "install",
                "-r",
                str(REQUIREMENTS),
            ]
            subprocess.run(pip_command, env=env, check=True)
            return str(python_bin)
        except (OSError, subprocess.CalledProcessError) as exc:
            errors.append(f"{venv_dir}: {exc}")

    print("依赖安装失败：已尝试以下位置：", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    print(
        "可手动设置 MARKETING_REVIEW_VENV_DIR 到可写目录后重试。",
        file=sys.stderr,
    )
    return base_python


def default_output_dir():
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return Path.home() / ".openclaw" / "workspace" / "output" / "marketing-material-review" / stamp


def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw/Codex 稳定入口：自动选择虚拟环境、自检并运行营销素材审核"
    )
    parser.add_argument("--no-preflight", action="store_true", help="跳过 self_check.py")
    parser.add_argument("--print-env-status", action="store_true", help="只打印运行环境状态，不执行审核")
    parser.add_argument("--self-check", action="store_true", help="用自动选择的 Python 运行 self_check.py 后退出")
    parser.add_argument("--live", action="store_true", help="与 --self-check 搭配，实际调用一次百度 OCR")
    args, passthrough = parser.parse_known_args()

    env = os.environ.copy()
    env.pop("__PYVENV_LAUNCHER__", None)
    loaded_env_files = load_dotenv_files(env)
    python_bin = choose_python()
    has_output_dir = "--output-dir" in passthrough
    has_ocr_json = "--ocr-json" in passthrough

    if args.print_env_status:
        print(f"Python: {python_bin}")
        print(f"Skill: {SKILL_DIR}")
        print(f"dotenv: {', '.join(loaded_env_files) if loaded_env_files else 'none'}")
        print(f"BAIDU_ACCESS_TOKEN: {'present' if env.get('BAIDU_ACCESS_TOKEN') else 'missing'}")
        print(f"BAIDU_API_KEY + BAIDU_SECRET_KEY: {'present' if env.get('BAIDU_API_KEY') and env.get('BAIDU_SECRET_KEY') else 'missing'}")
        return 0

    if args.self_check:
        python_bin = ensure_python_env(env)
        check_command = [python_bin, str(SCRIPT_DIR / "self_check.py")]
        if args.live:
            check_command.append("--live")
        return subprocess.run(check_command, env=env).returncode

    if not passthrough or passthrough[0].startswith("-"):
        print("用法: python3 scripts/run_review.py <图片路径> [auto_review.py 参数...]", file=sys.stderr)
        return 1

    python_bin = ensure_python_env(env)
    command = [python_bin, str(SCRIPT_DIR / "auto_review.py"), *passthrough]
    if not has_output_dir:
        output_dir = default_output_dir()
        output_dir.mkdir(parents=True, exist_ok=True)
        command.extend(["--output-dir", str(output_dir)])

    if not args.no_preflight:
        check_command = [python_bin, str(SCRIPT_DIR / "self_check.py")]
        if has_ocr_json:
            check_command.append("--deps-only")
        check = subprocess.run(check_command, env=env)
        if check.returncode != 0:
            print(
                "预检失败：请先处理依赖或百度 OCR 环境变量，再重新运行。"
                "OpenClaw 可开启 env.shellEnv.enabled 或配置 ~/.openclaw/.env。",
                file=sys.stderr,
            )
            return check.returncode

    return subprocess.run(command, env=env).returncode


if __name__ == "__main__":
    raise SystemExit(main())
