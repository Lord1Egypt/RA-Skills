#!/usr/bin/env python3
from __future__ import annotations

import re
from typing import Any, Dict, List

from _common import json_dump, machine_meta, run, run_shell


def parse_top_summary() -> Dict[str, Any]:
    out = run(["top", "-l", "1", "-n", "0"])
    result: Dict[str, Any] = {"raw_excerpt": out.splitlines()[:30]}
    for line in out.splitlines():
        if line.startswith("Load Avg:"):
            match = re.search(r"Load Avg:\s*([0-9.]+),\s*([0-9.]+),\s*([0-9.]+)", line)
            if match:
                result["load_avg"] = [float(match.group(1)), float(match.group(2)), float(match.group(3))]
        elif line.startswith("CPU usage:"):
            match = re.search(r"CPU usage:\s*([0-9.]+)% user,\s*([0-9.]+)% sys,\s*([0-9.]+)% idle", line)
            if match:
                result["cpu_percent"] = {
                    "user": float(match.group(1)),
                    "system": float(match.group(2)),
                    "idle": float(match.group(3)),
                    "used": float(match.group(1)) + float(match.group(2)),
                }
        elif line.startswith("Processes:"):
            match = re.search(r"Processes:\s*(\d+) total,\s*(\d+) running,\s*(\d+) sleeping", line)
            if match:
                result["process_counts"] = {
                    "total": int(match.group(1)),
                    "running": int(match.group(2)),
                    "sleeping": int(match.group(3)),
                }
            thread_match = re.search(r"(\d+) threads", line)
            if thread_match:
                result["thread_count"] = int(thread_match.group(1))
    return result


def top_processes() -> List[Dict[str, Any]]:
    out = run_shell("ps -A -r -o pid=,%cpu=,%mem=,comm= | head -6")
    rows: List[Dict[str, Any]] = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = re.split(r"\s+", line, maxsplit=3)
        if len(parts) != 4:
            continue
        pid, cpu, mem, command = parts
        try:
            rows.append({
                "pid": int(pid),
                "cpu_percent": float(cpu),
                "mem_percent": float(mem),
                "command": command,
            })
        except ValueError:
            continue
    return rows[:5]


def physical_cpu_count() -> Dict[str, Any]:
    logical = run(["/usr/sbin/sysctl", "-n", "hw.logicalcpu"]).strip()
    physical = run(["/usr/sbin/sysctl", "-n", "hw.physicalcpu"]).strip()
    return {
        "logical": int(logical) if logical.isdigit() else None,
        "physical": int(physical) if physical.isdigit() else None,
    }


def main() -> int:
    top = parse_top_summary()
    payload = {
        **machine_meta(),
        "kind": "cpustat",
        "cpu": {
            **top.get("cpu_percent", {}),
            "cores": physical_cpu_count(),
            "load_avg": top.get("load_avg"),
        },
        "scheduler": {
            "process_counts": top.get("process_counts"),
            "thread_count": top.get("thread_count"),
        },
        "top_processes": top_processes(),
        "source": {
            "top_excerpt": top.get("raw_excerpt", []),
        },
    }
    json_dump(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
