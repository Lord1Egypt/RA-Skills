#!/usr/bin/env python3
"""Sample GPU/CPU utilization of a RUNNING job and classify the bottleneck.

Run this WHILE your training/eval job is in its steady phase (not during
startup warm-up):

    python scripts/quick_triage.py --duration 60

It samples every GPU's utilization and system CPU load, then classifies
each GPU into a bottleneck class with concrete tuning advice.
Standard library only (psutil used for CPU if installed).
"""

from __future__ import annotations

import argparse
import json
import platform
import statistics
import subprocess
import sys
import time


def run_command(command: list[str], timeout: float = 5.0) -> str:
    try:
        completed = subprocess.run(
            command, capture_output=True, text=True, timeout=timeout,
            encoding="utf-8", errors="replace",
        )
        return completed.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return ""


def sample_gpus() -> list[dict]:
    """One instantaneous sample of every GPU: util % and VRAM used."""
    output = run_command([
        "nvidia-smi",
        "--query-gpu=index,utilization.gpu,memory.used,memory.total",
        "--format=csv,noheader,nounits",
    ])
    samples = []
    for line in output.splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) >= 4:
            samples.append({
                "index": int(parts[0]),
                "util_percent": float(parts[1]),
                "vram_used_mb": float(parts[2]),
                "vram_total_mb": float(parts[3]),
            })
    return samples


def read_cpu_windows() -> float | None:
    output = run_command(["wmic", "cpu", "get", "LoadPercentage", "/format:list"])
    token = output.replace("LoadPercentage=", "").strip().splitlines()
    for value in token:
        digits = ""
        for char in value.strip():
            if char.isdigit():
                digits += char
            else:
                break
        if digits:
            return float(digits)
    return None


class LinuxCpuSampler:
    """CPU % from /proc/stat deltas between consecutive calls."""

    def __init__(self) -> None:
        self.last = self._read_times()

    @staticmethod
    def _read_times() -> tuple[int, int] | None:
        try:
            with open("/proc/stat", encoding="ascii") as stat_file:
                fields = stat_file.readline().split()[1:]
            values = [int(v) for v in fields]
            idle = values[3] + (values[4] if len(values) > 4 else 0)
            return idle, sum(values)
        except (OSError, ValueError, IndexError):
            return None

    def sample(self) -> float | None:
        current = self._read_times()
        if current is None or self.last is None:
            return None
        idle_delta = current[0] - self.last[0]
        total_delta = current[1] - self.last[1]
        self.last = current
        if total_delta <= 0:
            return None
        return 100.0 * (1.0 - idle_delta / total_delta)


def make_cpu_sampler():
    try:
        import psutil

        psutil.cpu_percent(interval=None)  # prime the first-delta call
        return psutil.cpu_percent
    except ImportError:
        pass
    system = platform.system()
    if system == "Windows":
        return read_cpu_windows
    if system == "Linux":
        return LinuxCpuSampler().sample
    return lambda *args, **kwargs: None


def summarize(series: list[float]) -> dict:
    if not series:
        return {"avg": None}
    return {
        "avg": statistics.mean(series),
        "min": min(series),
        "max": max(series),
        "stdev": statistics.pstdev(series) if len(series) > 1 else 0.0,
        "pct_samples_below_50": 100.0 * sum(1 for s in series if s < 50) / len(series),
    }


def classify_gpu(gpu_stats: dict, cpu_avg: float | None, vram_pct: float) -> str:
    avg = gpu_stats["avg"]
    if avg is None:
        return "no samples collected - check that the job is running and nvidia-smi works"
    spiky = gpu_stats["pct_samples_below_50"] > 30
    cpu_part = f", CPU {cpu_avg:.0f}%" if cpu_avg is not None else ""

    if vram_pct > 95:
        return (
            f"memory-bound (VRAM at {vram_pct:.0f}%). Knobs: gradient accumulation "
            "instead of bigger micro-batch, gradient checkpointing, "
            "PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True."
        )
    if avg >= 85 and not spiky:
        return (
            f"compute-bound and healthy ({avg:.0f}% avg{cpu_part}). For more throughput: "
            "larger batch (if VRAM headroom), AMP/bf16, torch.compile, channels_last, "
            "fused optimizer. See references/tuning-playbook.md."
        )
    if avg >= 85 and spiky:
        return (
            f"compute-bound but spiky ({avg:.0f}% avg, {gpu_stats['pct_samples_below_50']:.0f}% "
            "samples < 50%). Occasional pipeline stalls: raise num_workers/prefetch_factor, "
            "persistent_workers=True."
        )
    if avg >= 50:
        return (
            f"moderately utilized ({avg:.0f}% avg{cpu_part}). Isolate the data pipeline "
            "first: benchmark the DataLoader alone vs GPU consumption rate "
            "(references/profiling.md), then tune num_workers / batch size."
        )
    if cpu_avg is not None and cpu_avg >= 70:
        return (
            f"input-pipeline starvation (GPU {avg:.0f}% avg while CPU {cpu_avg:.0f}%). "
            "Decode/tokenize is eating the cores: raise num_workers toward CPU capacity, "
            "move augmentation to GPU, or PRE-ENCODE the dataset to tensors/shards. "
            "See references/tuning-playbook.md (pre-encode section)."
        )
    return (
        f"under-utilized and idle (GPU {avg:.0f}% avg{cpu_part}). Either the job is too "
        "small for this GPU (increase batch size, pack more independent jobs - "
        "references/experiment-packing.md) or it is I/O-blocked (check disk; "
        "references/profiling.md)."
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sample utilization of a running job and classify the bottleneck."
    )
    parser.add_argument("--duration", type=float, default=30.0,
                        help="sampling window in seconds (default 30)")
    parser.add_argument("--interval", type=float, default=1.0,
                        help="seconds between samples (default 1)")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args()

    cpu_sampler = make_cpu_sampler()
    gpu_utils: dict[int, list[float]] = {}
    vram_percents: dict[int, list[float]] = {}
    cpu_samples: list[float] = []

    deadline = time.monotonic() + args.duration
    sample_count = 0
    while time.monotonic() < deadline:
        loop_start = time.monotonic()
        for gpu in sample_gpus():
            gpu_utils.setdefault(gpu["index"], []).append(gpu["util_percent"])
            if gpu["vram_total_mb"] > 0:
                pct = 100.0 * gpu["vram_used_mb"] / gpu["vram_total_mb"]
                vram_percents.setdefault(gpu["index"], []).append(pct)
        cpu_value = cpu_sampler()
        if cpu_value is not None:
            cpu_samples.append(cpu_value)
        sample_count += 1
        remaining = args.interval - (time.monotonic() - loop_start)
        if remaining > 0:
            time.sleep(remaining)

    gpu_stats = {f"GPU{idx}": summarize(series) for idx, series in sorted(gpu_utils.items())}
    cpu_stats = summarize(cpu_samples)
    cpu_avg = cpu_stats.get("avg")

    verdicts = {}
    for name, stats in gpu_stats.items():
        idx = int(name[3:])
        vram_pct = vram_percents.get(idx, [0.0])
        verdicts[name] = classify_gpu(stats, cpu_avg, statistics.mean(vram_pct))

    report = {
        "duration_seconds": args.duration,
        "samples": sample_count,
        "cpu": cpu_stats,
        "gpus": gpu_stats,
        "vram_percent_used": {f"GPU{i}": summarize(v) for i, v in sorted(vram_percents.items())},
        "diagnosis": verdicts,
    }

    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    print("=" * 62)
    print(f"TRIAGE REPORT  ({sample_count} samples over {args.duration:.0f}s)")
    print("=" * 62)
    if cpu_avg is not None:
        print(f"CPU avg: {cpu_avg:.0f}%  (range {cpu_stats['min']:.0f}-{cpu_stats['max']:.0f}%)")
    else:
        print("CPU avg: unavailable (install psutil for CPU sampling)")
    for name, stats in gpu_stats.items():
        idx = int(name[3:])
        vram = statistics.mean(vram_percents.get(idx, [0.0]))
        print(f"{name}: util avg {stats['avg']:.0f}% "
              f"(min {stats['min']:.0f}%, max {stats['max']:.0f}%), "
              f"{stats['pct_samples_below_50']:.0f}% of samples below 50%, "
              f"VRAM {vram:.0f}%")
    print("-" * 62)
    print("DIAGNOSIS")
    print("-" * 62)
    for name, verdict in verdicts.items():
        print(f"{name}: {verdict}")
    print("-" * 62)
    print("Deep dive: references/profiling.md   Knobs: references/tuning-playbook.md")
    print("=" * 62)
    return 0


if __name__ == "__main__":
    sys.exit(main())
