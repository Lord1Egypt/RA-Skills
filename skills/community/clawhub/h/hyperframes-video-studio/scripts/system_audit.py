#!/usr/bin/env python3
"""Preflight audit for Hyperframes Video Studio."""

from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import shutil
import sys
from pathlib import Path


MIN_DISK_BYTES = 5 * 1024**3
MIN_RAM_BYTES = 2 * 1024**3
MAX_CPU_PERCENT = 90.0
REQUIRED_BINS = ["python3", "node", "npm"]
OPTIONAL_BINS = ["hyperframes", "ffmpeg", "ffprobe", "edge-tts", "piper", "piper-tts"]


def _json_print(payload: dict) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def _human_bytes(value: int | float) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(value)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def _run_text(command: list[str]) -> str:
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.DEVNULL, timeout=2).strip()
    except Exception:
        return ""


def _memory_without_psutil() -> dict:
    system = platform.system()
    if system == "Darwin":
        page_size = int(_run_text(["/usr/sbin/sysctl", "-n", "hw.pagesize"]) or "4096")
        vm_stat = _run_text(["/usr/bin/vm_stat"])
        free_pages = 0
        for line in vm_stat.splitlines():
            if any(label in line for label in ["Pages free", "Pages inactive", "Pages speculative"]):
                number = "".join(ch for ch in line.split(":", 1)[-1] if ch.isdigit())
                if number:
                    free_pages += int(number)
        return {"available": free_pages * page_size, "source": "vm_stat"}
    if system == "Linux":
        try:
            values = {}
            for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
                key, raw = line.split(":", 1)
                values[key] = int(raw.strip().split()[0]) * 1024
            return {"available": values.get("MemAvailable", values.get("MemFree", 0)), "source": "/proc/meminfo"}
        except Exception:
            return {"available": 0, "source": "unknown"}
    return {"available": 0, "source": "unknown"}


def _cpu_without_psutil() -> dict:
    cpu_count = os.cpu_count() or 1
    if hasattr(os, "getloadavg"):
        one_minute = os.getloadavg()[0]
        percent = min(100.0, max(0.0, one_minute / cpu_count * 100.0))
        return {"percent": percent, "source": "loadavg"}
    return {"percent": 0.0, "source": "unavailable"}


def _check_tools(base_dir: Path) -> dict:
    local_bin = base_dir / ".cache" / "npm" / "node_modules" / ".bin"
    path_candidates = [local_bin]
    tools = {}
    for name in REQUIRED_BINS + OPTIONAL_BINS:
        candidates = []
        if sys.platform == "win32":
            candidates.append(local_bin / f"{name}.cmd")
        candidates.append(local_bin / name)
        found = next((str(candidate) for candidate in candidates if candidate.exists()), None) or shutil.which(name)
        tools[name] = {
            "ok": bool(found),
            "path": found,
            "required": name in REQUIRED_BINS,
        }
    return tools


def run_audit(cache_dir: Path, cpu_interval: float) -> dict:
    base_dir = Path(__file__).resolve().parents[1]
    psutil_status = "ok"
    try:
        import psutil  # type: ignore
    except Exception as exc:  # pragma: no cover - depends on environment
        psutil = None  # type: ignore
        psutil_status = f"missing: {exc}"

    cache_dir = cache_dir.expanduser().resolve()
    cache_dir.mkdir(parents=True, exist_ok=True)

    disk = shutil.disk_usage(cache_dir)
    if psutil:
        mem_available = int(psutil.virtual_memory().available)
        mem_source = "psutil"
        cpu = float(psutil.cpu_percent(interval=cpu_interval))
        cpu_source = "psutil"
    else:
        mem_info = _memory_without_psutil()
        mem_available = int(mem_info["available"])
        mem_source = str(mem_info["source"])
        cpu_info = _cpu_without_psutil()
        cpu = float(cpu_info["percent"])
        cpu_source = str(cpu_info["source"])
    loadavg = os.getloadavg() if hasattr(os, "getloadavg") else None
    tools = _check_tools(base_dir)

    checks = {
        "disk": {
            "ok": disk.free > MIN_DISK_BYTES,
            "free_bytes": disk.free,
            "free": _human_bytes(disk.free),
            "required": _human_bytes(MIN_DISK_BYTES),
        },
        "memory": {
            "ok": mem_available > MIN_RAM_BYTES,
            "available_bytes": mem_available,
            "available": _human_bytes(mem_available),
            "required": _human_bytes(MIN_RAM_BYTES),
            "source": mem_source,
        },
        "cpu": {
            "ok": cpu < MAX_CPU_PERCENT,
            "percent": cpu,
            "required": f"< {MAX_CPU_PERCENT:.0f}%",
            "source": cpu_source,
        },
        "tools": {
            "ok": all(info["ok"] for info in tools.values() if info["required"]),
            "required": REQUIRED_BINS,
            "optional": OPTIONAL_BINS,
            "items": tools,
        },
    }

    failures = [name for name, result in checks.items() if not result["ok"]]
    status = "hard_stop" if failures else "ok"
    message = (
        "Environment is safe for Video Studio."
        if not failures
        else "Video Studio stopped before heavy work because this machine is currently below the safe rendering threshold."
    )

    return {
        "status": status,
        "hard_stop": bool(failures),
        "message": message,
        "failures": failures,
        "checks": checks,
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python": platform.python_version(),
            "loadavg": loadavg,
        },
        "psutil": psutil_status,
        "install_hints": {
            "psutil": "Optional but recommended: python3 -m pip install --user psutil. If pip is externally managed, use a virtualenv.",
            "hyperframes": f"Local install: npm install --prefix \"{base_dir / '.cache' / 'npm'}\" hyperframes",
            "edge_tts": "Optional zero-cost TTS: python3 -m pip install --user edge-tts, or run with python -m edge_tts when available.",
            "piper": "Optional local TTS: install Piper and pass a local model path as voice.",
            "ffmpeg": "Optional for robust duration probing: place a static ffmpeg/ffprobe binary under .cache/bin or install it on PATH.",
        },
        "paths": {"cache_dir": str(cache_dir)},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit disk, RAM, and CPU before Video Studio rendering.")
    parser.add_argument("--cache-dir", default=str(Path(__file__).resolve().parents[1] / ".cache"))
    parser.add_argument("--cpu-interval", type=float, default=1.0)
    args = parser.parse_args()

    result = run_audit(Path(args.cache_dir), args.cpu_interval)
    _json_print(result)
    return 2 if result.get("hard_stop") else 0


if __name__ == "__main__":
    sys.exit(main())
