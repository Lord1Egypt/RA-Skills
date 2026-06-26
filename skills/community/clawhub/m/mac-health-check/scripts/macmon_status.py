#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shlex
import shutil
import subprocess
import sys
from typing import Any


DEFAULT_INTERVAL_MS = 200


def load_payload(raw: str) -> dict[str, Any]:
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise RuntimeError("Expected a single JSON object from macmon.")
    return data


def run_macmon(interval_ms: int) -> dict[str, Any]:
    binary = shutil.which("macmon") or "/opt/homebrew/bin/macmon"
    cmd = [binary, "pipe", "-s", "1", "-i", str(interval_ms)]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=15)
    except FileNotFoundError:
        proc = run_macmon_via_login_shell(interval_ms)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("macmon timed out.") from exc
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or "").strip()
        suffix = f": {stderr}" if stderr else ""
        if should_retry_in_login_shell(stderr):
            proc = run_macmon_via_login_shell(interval_ms)
        else:
            raise RuntimeError(f"macmon failed{suffix}") from exc

    lines = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    if not lines:
        raise RuntimeError("macmon returned no output.")
    return load_payload(lines[-1])


def should_retry_in_login_shell(stderr: str) -> bool:
    normalized = stderr.lower()
    return "no such file or directory" in normalized


def run_macmon_via_login_shell(interval_ms: int) -> subprocess.CompletedProcess[str]:
    shell = shutil.which("zsh") or "/bin/zsh"
    binary = shutil.which("macmon") or "/opt/homebrew/bin/macmon"
    shell_cmd = f"{shlex.quote(binary)} pipe -s 1 -i {int(interval_ms)}"

    try:
        return subprocess.run(
            [shell, "-lic", shell_cmd],
            capture_output=True,
            text=True,
            check=True,
            timeout=20,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("macmon not found on PATH, and zsh login-shell fallback is unavailable.") from exc
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("macmon timed out.") from exc
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or "").strip()
        suffix = f": {stderr}" if stderr else ""
        raise RuntimeError(f"macmon failed{suffix}") from exc


def load_from_input(path: str) -> dict[str, Any]:
    if path == "-":
        raw = sys.stdin.read()
    else:
        with open(path, "r", encoding="utf-8") as handle:
            raw = handle.read()

    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    if not lines:
        raise RuntimeError("No JSON input provided.")
    return load_payload(lines[-1])


def fmt_temp(value: Any) -> str:
    return "—" if not isinstance(value, (int, float)) else f"{value:.1f}°C"


def fmt_power(value: Any) -> str:
    return "—" if not isinstance(value, (int, float)) else f"{value:.2f} W"


def fmt_pct(value: Any) -> str:
    return "—" if not isinstance(value, (int, float)) else f"{value * 100:.1f}%"


def fmt_bytes(value: Any) -> str:
    if not isinstance(value, (int, float)):
        return "—"

    units = ["B", "KB", "MB", "GB", "TB"]
    scaled = float(value)
    idx = 0
    while scaled >= 1024 and idx < len(units) - 1:
        scaled /= 1024
        idx += 1
    return f"{scaled:.1f} {units[idx]}"


def pair_usage(pair: Any) -> tuple[Any, Any]:
    if isinstance(pair, list) and len(pair) >= 2:
        return pair[0], pair[1]
    return None, None


def verdict(data: dict[str, Any]) -> str:
    temp = data.get("temp", {}) if isinstance(data.get("temp"), dict) else {}
    memory = data.get("memory", {}) if isinstance(data.get("memory"), dict) else {}
    cpu_temp = temp.get("cpu_temp_avg")
    sys_power = data.get("sys_power")
    swap_usage = memory.get("swap_usage")

    if isinstance(cpu_temp, (int, float)) and cpu_temp >= 85:
        return "Hot: clear thermal load right now."
    if isinstance(cpu_temp, (int, float)) and cpu_temp >= 60:
        return "Warm but normal for active work."
    if isinstance(swap_usage, (int, float)) and swap_usage > 512 * 1024 * 1024:
        return "Temperatures look fine, but memory pressure is starting to show."
    if isinstance(sys_power, (int, float)) and sys_power >= 25:
        return "The system is working actively, but one sample alone is not a concern."
    return "Looks calm: light to moderate load."


def build_summary(data: dict[str, Any]) -> str:
    temp = data.get("temp", {}) if isinstance(data.get("temp"), dict) else {}
    memory = data.get("memory", {}) if isinstance(data.get("memory"), dict) else {}
    pcpu_mhz, pcpu_frac = pair_usage(data.get("pcpu_usage"))
    ecpu_mhz, ecpu_frac = pair_usage(data.get("ecpu_usage"))
    gpu_mhz, gpu_frac = pair_usage(data.get("gpu_usage"))

    lines = ["Mac status", f"Verdict: {verdict(data)}"]
    if data.get("timestamp"):
        lines.append(f"Timestamp: {data['timestamp']}")

    lines.extend(
        [
            f"CPU temp: {fmt_temp(temp.get('cpu_temp_avg'))}",
            f"GPU temp: {fmt_temp(temp.get('gpu_temp_avg'))}",
            f"Performance CPU: {fmt_pct(pcpu_frac)} @ {pcpu_mhz or '—'} MHz",
            f"Efficiency CPU: {fmt_pct(ecpu_frac)} @ {ecpu_mhz or '—'} MHz",
            f"GPU: {fmt_pct(gpu_frac)} @ {gpu_mhz or '—'} MHz",
            f"System power: {fmt_power(data.get('sys_power'))}",
            f"CPU power: {fmt_power(data.get('cpu_power'))}",
            f"GPU power: {fmt_power(data.get('gpu_power'))}",
            f"RAM: {fmt_bytes(memory.get('ram_usage'))} / {fmt_bytes(memory.get('ram_total'))}",
            f"Swap: {fmt_bytes(memory.get('swap_usage'))} / {fmt_bytes(memory.get('swap_total'))}",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize Mac metrics from macmon JSON.")
    parser.add_argument("--input", help="Read JSON from file or '-' for stdin instead of running macmon.")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    parser.add_argument(
        "--interval-ms",
        type=int,
        default=DEFAULT_INTERVAL_MS,
        help="macmon sampling interval in milliseconds for one-shot mode.",
    )
    args = parser.parse_args()

    try:
        data = load_from_input(args.input) if args.input else run_macmon(args.interval_ms)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2 if args.pretty else None, sort_keys=args.pretty))
    else:
        print(build_summary(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
