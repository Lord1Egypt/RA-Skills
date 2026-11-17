#!/usr/bin/env python3
"""Inspect local compute resources and recommend a parallel execution plan.

Cross-platform (Windows / Linux / macOS), standard library only.
Outputs a human-readable summary by default, or JSON with --json.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys


def run_command(command: list[str], timeout: float = 10.0) -> str:
    """Run a command and return stripped stdout, or empty string on failure."""
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
        )
        return completed.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return ""


def get_cpu_info() -> dict:
    logical = os.cpu_count() or 1
    physical = logical
    model = platform.processor() or platform.machine()

    system = platform.system()
    if system == "Linux":
        lscpu = run_command(["lscpu"])
        if lscpu:
            model_match = re.search(r"Model name:\s*(.+)", lscpu)
            if model_match:
                model = model_match.group(1).strip()
            sockets = int(re.search(r"Socket\(s\):\s*(\d+)", lscpu).group(1)) if re.search(r"Socket\(s\):", lscpu) else 1
            cores_per_socket_match = re.search(r"Core\(s\) per socket:\s*(\d+)", lscpu)
            if cores_per_socket_match:
                physical = sockets * int(cores_per_socket_match.group(1))
    elif system == "Windows":
        wmic_cpus = run_command(["wmic", "cpu", "get", "Name,NumberOfCores,NumberOfLogicalProcessors", "/format:list"])
        if wmic_cpus:
            cores = re.findall(r"NumberOfCores=(\d+)", wmic_cpus)
            if cores:
                physical = sum(int(c) for c in cores)
            names = re.findall(r"Name=(.+)", wmic_cpus)
            if names:
                model = names[0].strip()
    elif system == "Darwin":
        physical_raw = run_command(["sysctl", "-n", "hw.physicalcpu"])
        if physical_raw.isdigit():
            physical = int(physical_raw)
        name_raw = run_command(["sysctl", "-n", "machdep.cpu.brand_string"])
        if name_raw:
            model = name_raw.strip()

    return {"model": model, "physical_cores": physical, "logical_cores": logical}


def get_memory_info() -> dict:
    """Return total/available memory in bytes. Availability is best-effort."""
    system = platform.system()
    total = None
    available = None

    if system == "Linux":
        meminfo = run_command(["free", "-b"])
        if meminfo:
            match = re.search(r"Mem:\s+(\d+)\s+(\d+)\s+(\d+)", meminfo)
            if match:
                total = int(match.group(1))
                available = int(match.group(3))
    elif system == "Windows":
        wmic_os = run_command(["wmic", "OS", "get", "TotalVisibleMemorySize,FreePhysicalMemory", "/format:list"])
        if wmic_os:
            total_kb = re.search(r"TotalVisibleMemorySize=(\d+)", wmic_os)
            free_kb = re.search(r"FreePhysicalMemory=(\d+)", wmic_os)
            if total_kb:
                total = int(total_kb.group(1)) * 1024
            if free_kb:
                available = int(free_kb.group(1)) * 1024
    elif system == "Darwin":
        total_raw = run_command(["sysctl", "-n", "hw.memsize"])
        if total_raw.isdigit():
            total = int(total_raw)
        vm_stat = run_command(["vm_stat"])
        if vm_stat:
            page_size_match = re.search(r"page size of (\d+) bytes", vm_stat)
            free_match = re.search(r"Pages free:\s+(\d+)", vm_stat)
            inactive_match = re.search(r"Pages inactive:\s+(\d+)", vm_stat)
            if page_size_match and free_match:
                page_size = int(page_size_match.group(1))
                available = int(free_match.group(1)) * page_size
                if inactive_match:
                    available += int(inactive_match.group(1)) * page_size

    try:
        import psutil  # optional, more accurate when present

        vm = psutil.virtual_memory()
        total = vm.total
        available = vm.available
    except ImportError:
        pass

    return {"total_bytes": total, "available_bytes": available}


def get_gpu_info() -> list[dict]:
    """Query NVIDIA GPUs via nvidia-smi. Empty list when unavailable."""
    output = run_command([
        "nvidia-smi",
        "--query-gpu=index,name,memory.total,memory.free,utilization.gpu",
        "--format=csv,noheader,nounits",
    ])
    gpus = []
    if output:
        for line in output.splitlines():
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 5:
                gpus.append({
                    "index": int(parts[0]),
                    "name": parts[1],
                    "memory_total_mb": float(parts[2]),
                    "memory_free_mb": float(parts[3]),
                    "utilization_percent": float(parts[4]),
                })
    return gpus


def get_disk_info() -> dict:
    try:
        usage = shutil.disk_usage(os.getcwd())
        return {"total_bytes": usage.total, "free_bytes": usage.free}
    except OSError:
        return {"total_bytes": None, "free_bytes": None}


def build_recommendations(cpu: dict, memory: dict, gpus: list[dict]) -> dict:
    """Derive a concrete parallel-execution plan from the probed hardware."""
    logical = cpu["logical_cores"]
    total_gb = (memory["total_bytes"] or 0) / (1024 ** 3)
    available_gb = (memory["available_bytes"] or 0) / (1024 ** 3)

    cpu_bound_workers = max(1, int(logical * 0.75))
    memory_note = None
    if available_gb > 0:
        # Conservative 256 MB per worker (build/test workers are usually small);
        # never let a transient low-memory reading drop the recommendation
        # below max(2, logical/8) - flag the constraint instead.
        memory_bound_workers = max(1, int((available_gb * 0.75) / 0.25))
        floor_workers = max(2, logical // 8)
        if memory_bound_workers < cpu_bound_workers:
            if memory_bound_workers < floor_workers:
                memory_bound_workers = floor_workers
                memory_note = (
                    f"RAM available is low ({available_gb:.1f} GB); recommendation "
                    f"floored at {floor_workers} workers - free memory or size "
                    "workers per-job memory before going wider"
                )
            else:
                memory_note = (
                    f"RAM available limits workers to {memory_bound_workers} "
                    f"(CPU allows {cpu_bound_workers})"
                )
        cpu_workers = min(cpu_bound_workers, memory_bound_workers)
    else:
        cpu_workers = cpu_bound_workers
        memory_note = "could not read available RAM; using CPU-bound estimate"

    free_gpus = [g["index"] for g in gpus if g["memory_free_mb"] > 1024]
    dataloader_workers = min(max(1, logical // max(1, len(gpus) or 1)), 8) if gpus else 0

    return {
        "cpu_workers_recommended": cpu_workers,
        "cpu_workers_uncapped": cpu_bound_workers,
        "memory_note": memory_note,
        "omp_threads_single_process": logical,
        "free_gpus": free_gpus,
        "dataloader_num_workers_per_gpu": dataloader_workers,
        "torchrun_command_example": (
            f"torchrun --standalone --nproc_per_node={len(free_gpus)} train.py"
            if len(free_gpus) > 1 else None
        ),
    }


def format_size(num_bytes: float | None) -> str:
    if num_bytes is None:
        return "unknown"
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if num_bytes < 1024:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} PB"


def print_report(data: dict) -> None:
    cpu = data["cpu"]
    memory = data["memory"]
    gpus = data["gpus"]
    rec = data["recommendations"]

    print("=" * 62)
    print("RESOURCE REPORT")
    print("=" * 62)
    print(f"OS:            {data['platform']}")
    print(f"CPU:           {cpu['model']}")
    print(f"  physical:    {cpu['physical_cores']} cores")
    print(f"  logical:     {cpu['logical_cores']} threads")
    print(f"RAM total:     {format_size(memory['total_bytes'])}")
    print(f"RAM available: {format_size(memory['available_bytes'])}")
    print(f"Disk (cwd):    {format_size(data['disk']['free_bytes'])} free of "
          f"{format_size(data['disk']['total_bytes'])}")

    print(f"GPUs:          {len(gpus)} NVIDIA device(s) detected")
    for gpu in gpus:
        print(f"  GPU{gpu['index']} {gpu['name']}")
        print(f"      VRAM free/total: {gpu['memory_free_mb']:.0f}/{gpu['memory_total_mb']:.0f} MB")
        print(f"      utilization:     {gpu['utilization_percent']:.0f}%")
    if not gpus:
        print("  (no nvidia-smi found or no NVIDIA GPU)")

    print("-" * 62)
    print("RECOMMENDED EXECUTION PLAN")
    print("-" * 62)
    print(f"CPU workers (build/pytest/proc): {rec['cpu_workers_recommended']}"
          f" (uncapped by RAM: {rec['cpu_workers_uncapped']})")
    if rec.get("memory_note"):
        print(f"NOTE: {rec['memory_note']}")
    print(f"Free GPUs usable right now:      {rec['free_gpus'] or 'none'}")
    if gpus:
        print(f"DataLoader num_workers per GPU:  {rec['dataloader_num_workers_per_gpu']}")
    if rec["torchrun_command_example"]:
        print(f"Multi-GPU launch example:        {rec['torchrun_command_example']}")
    print("Multi-process jobs: set OMP_NUM_THREADS=1 per worker (or "
          f"{rec['omp_threads_single_process']}/N) to avoid thread thrash")
    print("=" * 62)


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect compute resources for maximum-throughput execution.")
    parser.add_argument("--json", action="store_true", help="output machine-readable JSON")
    args = parser.parse_args()

    cpu = get_cpu_info()
    memory = get_memory_info()
    gpus = get_gpu_info()
    disk = get_disk_info()
    recommendations = build_recommendations(cpu, memory, gpus)

    report = {
        "platform": f"{platform.system()} {platform.release()}",
        "cpu": cpu,
        "memory": memory,
        "gpus": gpus,
        "disk": disk,
        "recommendations": recommendations,
    }

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_report(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
