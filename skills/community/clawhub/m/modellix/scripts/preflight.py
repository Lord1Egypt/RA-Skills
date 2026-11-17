#!/usr/bin/env python3
"""
Cross-platform preflight check for CLI-first routing.

Refreshes `modellix-cli` from the public npm latest tag, then runs doctor.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from typing import Any

from cli_runtime import CliRuntime, resolve_cli_runtime


def _run_doctor(
    cli_path: str, profile: str | None = None
) -> tuple[bool, dict[str, Any] | None, str]:
    """Return (ok, parsed_json_or_none, raw_or_error)."""
    try:
        command = [cli_path, "doctor", "--json"]
        if profile:
            command.extend(["--profile", profile])
        proc = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, None, str(exc)

    raw = (proc.stdout or "").strip() or (proc.stderr or "").strip()
    parsed: dict[str, Any] | None = None
    if proc.stdout:
        try:
            parsed = json.loads(proc.stdout)
        except json.JSONDecodeError:
            parsed = None
    return proc.returncode == 0, parsed, raw


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Modellix CLI and API key readiness.")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    parser.add_argument("--profile", help="Optional Modellix CLI profile for doctor")
    args = parser.parse_args()

    notes: list[str] = []
    runtime: CliRuntime = resolve_cli_runtime()
    cli_available = runtime.available
    env_key_available = bool((os.getenv("MODELLIX_API_KEY") or "").strip())
    api_key_available = env_key_available
    doctor_ok: bool | None = None
    doctor_payload: dict[str, Any] | None = None

    if runtime.updated:
        notes.append(
            f"Updated modellix-cli to {runtime.installed_version} before this workflow."
        )
    elif runtime.source == "installed-current" and runtime.installed_version:
        notes.append(f"modellix-cli {runtime.installed_version} is current.")
    elif runtime.source == "installed-newer" and runtime.installed_version:
        notes.append(
            f"Installed modellix-cli {runtime.installed_version} is newer than npm latest "
            f"{runtime.latest_version}; kept the installed version."
        )
    if runtime.update_warning:
        notes.append(runtime.update_warning)

    if not cli_available:
        notes.append(
            "modellix-cli is unavailable after the automatic update check. "
            "REST fallback requires MODELLIX_API_KEY."
        )
    else:
        doctor_ok, doctor_payload, doctor_raw = _run_doctor(
            runtime.path or "modellix-cli", args.profile
        )
        if doctor_payload is not None:
            notes.append("Ran modellix-cli doctor --json.")
        elif doctor_raw:
            notes.append("doctor output was not valid JSON; inspect `modellix-cli doctor` directly.")
        if doctor_ok:
            notes.append(
                "CLI path ready. Canonical flow: model run --wait -> task download."
            )
            # Doctor success implies usable auth even if env var is unset (saved profile).
            api_key_available = True
        else:
            notes.append(
                "doctor reported failures. Fix auth with auth login/init "
                "or set MODELLIX_API_KEY, then re-run doctor."
            )

    if not api_key_available:
        notes.append(
            "No discoverable API key (env or CLI profile). "
            "Configure MODELLIX_API_KEY or run: modellix-cli auth login"
        )

    recommended_mode = "none"
    if cli_available and doctor_ok is True:
        recommended_mode = "cli"
        notes.append(
            "Defaults when user omits model: T2I=google/nano-banana-2-lite, "
            "T2V=bytedance/seedance-2.0-mini-t2v, "
            "TTS=alibaba/qwen-audio-3.0-tts-flash, "
            "STT=openai/whisper-1, "
            "STS=alibaba/cosyvoice-clone."
        )
    elif not cli_available and env_key_available:
        recommended_mode = "rest"
        notes.append("REST fallback is available because an API key exists.")
    elif cli_available and doctor_ok is False:
        notes.append("No execution mode is recommended until the failed doctor checks are fixed.")
    else:
        notes.append("Neither CLI-auth nor REST-auth is ready. Configure API key first.")

    result = {
        "cli_available": cli_available,
        "cli_missing": not cli_available,
        "cli_path": runtime.path,
        "cli_version": runtime.installed_version,
        "cli_latest_version": runtime.latest_version,
        "cli_source": runtime.source,
        "cli_updated": runtime.updated,
        "cli_update_warning": runtime.update_warning,
        "api_key_available": api_key_available,
        "doctor_ok": doctor_ok,
        "doctor": doctor_payload,
        "recommended_mode": recommended_mode,
        "notes": notes,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"cli_available      : {result['cli_available']}")
        print(f"cli_version        : {result['cli_version']}")
        print(f"cli_latest_version : {result['cli_latest_version']}")
        print(f"cli_source         : {result['cli_source']}")
        print(f"api_key_available  : {result['api_key_available']}")
        print(f"doctor_ok          : {result['doctor_ok']}")
        print(f"recommended_mode   : {result['recommended_mode']}")
        if notes:
            print("notes:")
            for note in notes:
                print(f"- {note}")
    # Exit 0 only when the preflight can recommend a usable execution path.
    return 0 if recommended_mode != "none" else 1


if __name__ == "__main__":
    raise SystemExit(main())
