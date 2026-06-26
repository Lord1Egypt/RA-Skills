#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

from _common import bytes_human, json_dump, machine_meta


SCRIPTS = ["memstat.py", "cpustat.py", "gpustat.py", "powerstat.py", "fanstat.py", "tempstat.py"]


def run_helper(path: Path) -> Tuple[str, Dict[str, Any]]:
    proc = subprocess.run([sys.executable, str(path)], capture_output=True, text=True, timeout=40)
    if proc.returncode != 0:
        return path.name, {"ok": False, "error": (proc.stderr or proc.stdout).strip()}
    try:
        data = json.loads(proc.stdout)
    except Exception as e:
        return path.name, {"ok": False, "error": f"invalid json: {e}", "raw": proc.stdout[:500]}
    return path.name, {"ok": True, "data": data}


def summarize(bundle: Dict[str, Any]) -> str:
    mem = bundle.get("memstat", {})
    cpu = bundle.get("cpustat", {})
    gpu = bundle.get("gpustat", {})
    power = bundle.get("powerstat", {})
    fan = bundle.get("fanstat", {})
    temp = bundle.get("tempstat", {})

    mem_data = mem.get("memory", {})
    pressure = mem.get("pressure", {})
    cpu_data = cpu.get("cpu", {})
    top = cpu.get("top_processes", [])
    gpu_data = gpu.get("gpu", {})
    gpu_util = gpu.get("utilization_percent", {})
    power_watts = power.get("subsystem_power_watts", {})
    fans = fan.get("fans", [])
    temp_summary = temp.get("summary", {})

    parts: List[str] = []
    if cpu_data:
        load_avg = cpu_data.get("load_avg") or []
        load_text = "/".join(f"{x:.2f}" for x in load_avg) if load_avg else "n/a"
        cpu_used = cpu_data.get('used')
        cpu_used_text = f"{cpu_used:.1f}" if isinstance(cpu_used, (int, float)) else "n/a"
        parts.append(f"CPU {cpu_used_text}% used, load {load_text}")
    if mem_data:
        used_ratio = mem_data.get('used_ratio_percent')
        used_ratio_text = f"{used_ratio:.1f}" if isinstance(used_ratio, (int, float)) else "n/a"
        parts.append(
            f"Memory {used_ratio_text}% used est ({bytes_human(mem_data.get('used_estimate_bytes'))}/{mem_data.get('total_human')}), pressure {pressure.get('status', 'n/a')}/{pressure.get('risk', 'n/a')}"
        )
    if gpu_util or gpu_data:
        device = gpu_util.get("device")
        renderer = gpu_util.get("renderer")
        gpu_label = gpu_data.get("model") or "GPU"
        core_count = gpu_data.get("core_count")
        core_text = f"/{core_count}c" if isinstance(core_count, int) else ""
        parts.append(f"{gpu_label}{core_text} dev {device if device is not None else 'n/a'}%, render {renderer if renderer is not None else 'n/a'}%")
    if temp_summary:
        hottest = temp_summary.get("hottest_celsius")
        hottest_label = temp_summary.get("hottest_label")
        cpu_temp = temp_summary.get("cpu_celsius")
        if hottest is not None:
            temp_parts = [f"hottest {hottest:.1f}C ({hottest_label or 'unknown'})"]
            if cpu_temp is not None:
                temp_parts.insert(0, f"CPU {cpu_temp:.1f}C")
            parts.append("Temp " + ", ".join(temp_parts))
    if power_watts:
        cpu_w = power_watts.get("cpu")
        gpu_w = power_watts.get("gpu")
        dram_w = power_watts.get("dram")
        power_parts = [
            f"{name} {value:.2f}W"
            for name, value in [("CPU", cpu_w), ("GPU", gpu_w), ("DRAM", dram_w)]
            if isinstance(value, (int, float))
        ]
        if power_parts:
            parts.append("Power " + ", ".join(power_parts))
    if fans:
        active = [f for f in fans if isinstance(f.get("actual_rpm"), (int, float))]
        if active:
            fan_text = ", ".join(f"fan{f.get('id')} {f.get('actual_rpm'):.0f}rpm" for f in active)
            parts.append(f"Fans {fan_text}")
    if top:
        hottest = top[0]
        parts.append(f"Top proc {hottest.get('command')} pid {hottest.get('pid')} @ {hottest.get('cpu_percent')}% CPU")
    return " | ".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate mac-system-stat helpers")
    parser.add_argument("--text", action="store_true", help="print human summary only")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    collected: Dict[str, Any] = {}
    errors: Dict[str, Any] = {}
    for name in SCRIPTS:
        _, result = run_helper(root / name)
        key = name.removesuffix(".py")
        if result.get("ok"):
            collected[key] = result["data"]
        else:
            errors[key] = result

    payload = {
        **machine_meta(),
        "kind": "hoststat",
        "summary": summarize(collected),
        "helpers": collected,
        "errors": errors,
    }

    if args.text:
        print(payload["summary"])
    else:
        json_dump(payload)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
