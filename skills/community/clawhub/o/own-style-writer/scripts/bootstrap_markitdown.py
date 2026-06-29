#!/usr/bin/env python3
"""Create and verify the bundled MarkItDown runtime."""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path


FULL_EXTRAS = "pdf,docx,pptx,xlsx,xls,outlook"
DEFAULT_EXTRAS = "pdf"


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def vendor_root() -> Path:
    return skill_root() / "vendor" / "markitdown"


def default_runtime_dir() -> Path:
    override = os.environ.get("OWN_STYLE_WRITER_RUNTIME")
    if override:
        return Path(override).expanduser()

    if platform.system() == "Windows":
        base = os.environ.get("LOCALAPPDATA")
        if base:
            return Path(base) / "own-style-writer" / "runtime"

    base = os.environ.get("XDG_CACHE_HOME")
    if base:
        return Path(base).expanduser() / "own-style-writer" / "runtime"

    return Path.home() / ".cache" / "own-style-writer" / "runtime"


def runtime_key() -> str:
    tag = sys.implementation.cache_tag or f"py{sys.version_info.major}{sys.version_info.minor}"
    raw = f"{tag}-{platform.system().lower()}-{platform.machine().lower() or 'unknown'}"
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", raw)


def venv_root(runtime_dir: Path) -> Path:
    return runtime_dir / ".venv" / runtime_key()


def venv_python(runtime_dir: Path) -> Path:
    if platform.system() == "Windows":
        return venv_root(runtime_dir) / "Scripts" / "python.exe"
    return venv_root(runtime_dir) / "bin" / "python"


def target_site_packages(runtime_dir: Path) -> Path:
    return runtime_dir / "site-packages" / runtime_key()


def runtime_info_path(runtime_dir: Path) -> Path:
    return runtime_dir / f"runtime-{runtime_key()}.json"


def parse_extra_set(extras: str | None) -> set[str]:
    if not extras:
        return set()
    if extras.strip().lower() == "full":
        extras = FULL_EXTRAS
    return {item.strip() for item in extras.split(",") if item.strip()}


def normalize_extras(extras: str | None) -> str:
    return ",".join(sorted(parse_extra_set(extras)))


def read_installed_extras(runtime_dir: Path) -> set[str]:
    path = runtime_info_path(runtime_dir)
    if not path.exists():
        return set()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return set()
    return parse_extra_set(payload.get("extras"))


def extras_are_satisfied(runtime_dir: Path, extras: str | None) -> bool:
    requested = parse_extra_set(extras)
    if not requested:
        return True
    return requested.issubset(read_installed_extras(runtime_dir))


def runtime_env(runtime_dir: Path) -> dict[str, str]:
    env = os.environ.copy()
    target = target_site_packages(runtime_dir)
    if target.exists():
        existing = env.get("PYTHONPATH")
        env["PYTHONPATH"] = str(target) if not existing else f"{target}{os.pathsep}{existing}"
    return env


def run(cmd: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> None:
    print("+ " + " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, env=env, check=True)


def has_ensurepip() -> bool:
    result = subprocess.run(
        [sys.executable, "-m", "ensurepip", "--version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.returncode == 0


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def can_import_markitdown(python: Path, runtime_dir: Path) -> bool:
    if not python.exists():
        return False
    probe = (
        "import json, markitdown; "
        "from markitdown import MarkItDown; "
        "print(json.dumps({'file': getattr(markitdown, '__file__', None)}))"
    )
    result = subprocess.run(
        [str(python), "-c", probe],
        env=runtime_env(runtime_dir),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode == 0:
        try:
            payload = json.loads(result.stdout.strip())
            if not payload.get("file"):
                return False
            imported = Path(payload["file"])
        except Exception:
            return False

        target = target_site_packages(runtime_dir)
        vendor = vendor_root()
        if is_relative_to(imported, target) or is_relative_to(imported, vendor):
            print(str(imported), flush=True)
            return True

        print(
            f"Ignoring non-bundled MarkItDown import: {imported}",
            file=sys.stderr,
            flush=True,
        )
    return False


def ensure_runtime(
    runtime_dir: Path | None = None,
    *,
    extras: str = DEFAULT_EXTRAS,
    force: bool = False,
) -> Path:
    root = vendor_root()
    extras = normalize_extras(extras)
    if not (root / "pyproject.toml").exists():
        raise FileNotFoundError(f"Bundled MarkItDown package not found: {root}")

    runtime = runtime_dir or default_runtime_dir()
    runtime.mkdir(parents=True, exist_ok=True)
    python = venv_python(runtime)

    if force:
        if venv_root(runtime).exists():
            shutil.rmtree(venv_root(runtime))
        if target_site_packages(runtime).exists():
            shutil.rmtree(target_site_packages(runtime))

    fallback_python = Path(sys.executable)
    if (
        not force
        and target_site_packages(runtime).exists()
        and can_import_markitdown(fallback_python, runtime)
        and extras_are_satisfied(runtime, extras)
    ):
        write_runtime_info(runtime, fallback_python, extras, installed=False)
        return fallback_python

    if not python.exists() and has_ensurepip():
        try:
            run([sys.executable, "-m", "venv", str(venv_root(runtime))])
        except subprocess.CalledProcessError:
            print(
                "venv creation failed; falling back to pip --target runtime.",
                file=sys.stderr,
                flush=True,
            )
            if venv_root(runtime).exists():
                shutil.rmtree(venv_root(runtime))
            python = fallback_python
    elif not python.exists():
        print(
            "ensurepip is unavailable; using pip --target runtime.",
            file=sys.stderr,
            flush=True,
        )
        python = fallback_python

    if (
        not force
        and can_import_markitdown(python, runtime)
        and extras_are_satisfied(runtime, extras)
    ):
        write_runtime_info(runtime, python, extras, installed=False)
        return python

    package_spec = str(root)
    if extras:
        package_spec = f"{package_spec}[{extras}]"

    if python == Path(sys.executable):
        target = target_site_packages(runtime)
        target.mkdir(parents=True, exist_ok=True)
        run(
            [
                str(python),
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "--upgrade",
                "--target",
                str(target),
                package_spec,
            ],
            env=runtime_env(runtime),
        )
    else:
        run(
            [
                str(python),
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "-e",
                package_spec,
            ]
        )

    if not can_import_markitdown(python, runtime):
        raise RuntimeError("MarkItDown installation finished but import still failed.")

    write_runtime_info(runtime, python, extras, installed=True)
    return python


def write_runtime_info(runtime: Path, python: Path, extras: str, *, installed: bool) -> None:
    installed_extras = read_installed_extras(runtime) | parse_extra_set(extras)
    info = {
        "python": str(python),
        "vendor": str(vendor_root()),
        "extras": ",".join(sorted(installed_extras)),
        "target_site_packages": str(target_site_packages(runtime)),
        "installed_this_run": installed,
    }
    runtime_info_path(runtime).write_text(
        json.dumps(info, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap bundled MarkItDown runtime.")
    parser.add_argument("--runtime-dir", type=Path)
    parser.add_argument(
        "--extras",
        default=DEFAULT_EXTRAS,
        help="Comma-separated MarkItDown extras to install. Use 'full' for pdf,docx,pptx,xlsx,xls,outlook.",
    )
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        python = ensure_runtime(args.runtime_dir, extras=args.extras, force=args.force)
    except Exception as exc:
        print(f"bootstrap failed: {exc}", file=sys.stderr)
        return 1

    payload = {
        "runtime_dir": str((args.runtime_dir or default_runtime_dir()).resolve()),
        "python": str(python.resolve()),
        "vendor": str(vendor_root().resolve()),
        "runtime_key": runtime_key(),
        "target_site_packages": str(target_site_packages(args.runtime_dir or default_runtime_dir()).resolve()),
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"MarkItDown runtime ready: {payload['python']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
