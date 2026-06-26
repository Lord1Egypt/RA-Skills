#!/usr/bin/env python3
from __future__ import annotations

import re
from typing import Any, Dict, Optional

from _common import bytes_human, clamp_percent, json_dump, machine_meta, parse_size_to_bytes, run


def mem_total_bytes() -> Optional[int]:
    out = run(["/usr/sbin/sysctl", "-n", "hw.memsize"])
    try:
        return int(out.strip())
    except Exception:
        return None


def vm_stats() -> Dict[str, int]:
    out = run(["vm_stat"])
    page_size = 4096
    match = re.search(r"page size of (\d+) bytes", out)
    if match:
        page_size = int(match.group(1))
    stats: Dict[str, int] = {"page_size": page_size}
    for line in out.splitlines():
        match = re.match(r"(.+?):\s+(\d+)\.?$", line.strip())
        if not match:
            continue
        key = match.group(1).strip().lower().replace(" ", "_").replace('"', "")
        stats[key] = int(match.group(2))
    return stats


def swap_usage() -> Dict[str, Any]:
    out = run(["/usr/sbin/sysctl", "vm.swapusage"])
    match = re.search(
        r"total = ([0-9.]+(?:[KMGTP]B?|[KMGTP]))\s+used = ([0-9.]+(?:[KMGTP]B?|[KMGTP]))\s+free = ([0-9.]+(?:[KMGTP]B?|[KMGTP]))",
        out,
    )
    if not match:
        return {"raw": out}
    total_s, used_s, free_s = match.groups()
    return {
        "total_bytes": parse_size_to_bytes(total_s),
        "used_bytes": parse_size_to_bytes(used_s),
        "free_bytes": parse_size_to_bytes(free_s),
        "total_human": total_s,
        "used_human": used_s,
        "free_human": free_s,
    }


def memory_pressure() -> Dict[str, Any]:
    out = run(["memory_pressure"])
    percent = None
    for line in out.splitlines():
        if "System-wide memory free percentage" in line:
            try:
                percent = float(line.split(":", 1)[1].strip().rstrip("%"))
            except Exception:
                percent = None
            break
    status = "normal"
    if percent is not None:
        if percent < 10:
            status = "critical"
        elif percent < 20:
            status = "elevated"
    return {"free_percent": percent, "status": status, "raw": out}


def risk_level(total: Optional[int], used_bytes: int, compressed_bytes: int, swap_used_bytes: Optional[int], free_percent: Optional[float]) -> str:
    if total is None:
        return "unknown"
    used_ratio = used_bytes / total if total else 0.0
    compressed_ratio = compressed_bytes / total if total else 0.0
    swap_ratio = (swap_used_bytes or 0) / total if total else 0.0
    if (free_percent is not None and free_percent < 10) or compressed_ratio > 0.12 or used_ratio > 0.92 or swap_ratio > 0.05:
        return "high"
    if (free_percent is not None and free_percent < 20) or compressed_ratio > 0.06 or used_ratio > 0.82 or swap_ratio > 0.01:
        return "medium"
    return "low"


def main() -> int:
    total = mem_total_bytes()
    vm = vm_stats()
    pressure = memory_pressure()
    swap = swap_usage()

    page_size = vm.get("page_size", 4096)
    free = vm.get("pages_free", 0) * page_size
    inactive = vm.get("pages_inactive", 0) * page_size
    speculative = vm.get("pages_speculative", 0) * page_size
    active = vm.get("pages_active", 0) * page_size
    wired = vm.get("pages_wired_down", 0) * page_size
    compressed = vm.get("pages_occupied_by_compressor", 0) * page_size
    purgeable = vm.get("pages_purgeable", 0) * page_size
    app_used = active + wired
    used_estimate = active + wired + compressed
    available = free + inactive + speculative

    payload = {
        **machine_meta(),
        "kind": "memstat",
        "page_size_bytes": page_size,
        "memory": {
            "total_bytes": total,
            "total_human": bytes_human(total),
            "active_bytes": active,
            "wired_bytes": wired,
            "compressed_bytes": compressed,
            "purgeable_bytes": purgeable,
            "app_used_bytes": app_used,
            "used_estimate_bytes": used_estimate,
            "available_estimate_bytes": available,
            "free_bytes": free,
            "inactive_bytes": inactive,
            "speculative_bytes": speculative,
            "used_ratio_percent": clamp_percent((used_estimate / total) * 100 if total else None),
            "available_ratio_percent": clamp_percent((available / total) * 100 if total else None),
        },
        "swap": swap,
        "pressure": {
            "free_percent": pressure.get("free_percent"),
            "status": pressure.get("status"),
            "risk": risk_level(total, used_estimate, compressed, swap.get("used_bytes"), pressure.get("free_percent")),
        },
        "source": {
            "vm_stat": vm,
            "memory_pressure_excerpt": pressure.get("raw", "").splitlines()[:20],
        },
    }
    json_dump(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
