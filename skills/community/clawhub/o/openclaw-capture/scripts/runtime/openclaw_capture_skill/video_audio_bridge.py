"""STT bridge that picks local mac, local CLI, or remote legacy audio transcription."""

from __future__ import annotations

import argparse
import platform
from pathlib import Path
import shlex
import subprocess
import sys

from .compat import legacy_scripts_dir, require_legacy_project_root
from .config import Settings


def _run(args: list[str]) -> str:
    try:
        result = subprocess.run(args, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or "").strip()
        stdout = (exc.stdout or "").strip()
        msg = stderr or stdout or str(exc)
        raise RuntimeError(msg) from exc
    return (result.stdout or "").strip()


def _run_template(command: str, **kwargs: str) -> str:
    rendered = command.format(**kwargs)
    args = shlex.split(rendered)
    return _run(args)


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--max-seconds", default="0")
    parser.add_argument("--api-key", default="")
    parser.add_argument("--api-base-url", default="")
    return parser.parse_args(argv)


def _legacy_audio_script(legacy_project_root: Path) -> Path:
    scripts_dir = legacy_scripts_dir(legacy_project_root)
    return scripts_dir / "video_audio_asr.py"


def _call_legacy_audio(
    legacy_project_root: Path,
    *,
    backend: str,
    url: str,
    max_seconds: str,
    api_key: str,
    api_base_url: str,
) -> str:
    script_path = _legacy_audio_script(legacy_project_root)
    return _run(
        [
            sys.executable,
            str(script_path),
            "--url",
            url,
            "--max-seconds",
            str(max_seconds),
            "--api-key",
            api_key,
            "--api-base-url",
            api_base_url,
            "--backend",
            backend,
        ]
    )


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    settings = Settings.from_env()
    legacy_root = require_legacy_project_root(settings.legacy_project_root)

    if settings.stt_profile == "mac_local_first" and platform.system() == "Darwin":
        print(
            _call_legacy_audio(
                legacy_root,
                backend="auto",
                url=args.url,
                max_seconds=str(args.max_seconds),
                api_key=args.api_key,
                api_base_url=args.api_base_url,
            )
        )
        return 0

    if settings.stt_profile == "local_cli_then_remote" and settings.local_stt_command.strip():
        try:
            local_output = _run_template(
                settings.local_stt_command,
                url=args.url,
                max_seconds=str(args.max_seconds),
                api_key=args.api_key,
                api_base_url=args.api_base_url,
            )
            if local_output.strip():
                print(local_output)
                return 0
        except Exception:
            pass

    print(
        _call_legacy_audio(
            legacy_root,
            backend="remote",
            url=args.url,
            max_seconds=str(args.max_seconds),
            api_key=args.api_key,
            api_base_url=args.api_base_url,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

