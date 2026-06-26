#!/usr/bin/env python3
"""Probe a CUDA training environment and print actionable facts."""

from __future__ import annotations

import argparse
import json
import os
import platform
import sys
from typing import Any

import torch


ENV_KEYS = [
    "CUDA_VISIBLE_DEVICES",
    "CUDA_LAUNCH_BLOCKING",
    "PYTORCH_ALLOC_CONF",
    "TORCH_ALLOW_TF32_CUBLAS_OVERRIDE",
    "TORCH_CUDNN_V8_API_LRU_CACHE_LIMIT",
    "TORCH_NCCL_USE_COMM_NONBLOCKING",
    "NCCL_DEBUG",
    "NCCL_DEBUG_SUBSYS",
    "NCCL_SOCKET_IFNAME",
]


def gib(value: int) -> float:
    return round(value / (1024 ** 3), 2)


def collect_devices() -> list[dict[str, Any]]:
    devices = []
    if not torch.cuda.is_available():
        return devices

    for index in range(torch.cuda.device_count()):
        prop = torch.cuda.get_device_properties(index)
        devices.append(
            {
                "index": index,
                "name": prop.name,
                "compute_capability": f"{prop.major}.{prop.minor}",
                "total_memory_gib": gib(prop.total_memory),
                "multi_processor_count": prop.multi_processor_count,
            }
        )
    return devices


def collect_recommendations(devices: list[dict[str, Any]]) -> list[str]:
    recommendations: list[str] = []
    names = " ".join(device["name"] for device in devices).upper()
    count = len(devices)

    if count == 0:
        recommendations.append("CUDA is unavailable. Verify driver, runtime, and container visibility first.")
        return recommendations

    if any(token in names for token in ("H100", "H200", "B200", "BLACKWELL", "HOPPER")):
        recommendations.append("Prefer BF16 as the baseline precision on Hopper/Blackwell-class GPUs.")
    if any(token in names for token in ("H200", "B200", "BLACKWELL")):
        recommendations.append("Benchmark newer flash attention implementations and cuDNN/TE attention, not only the default SDPA path.")
    if count > 1:
        recommendations.append("Use torchrun with one process per GPU and NCCL for distributed CUDA workloads.")
    recommendations.append("Verify dataloader pinning, worker count, and prefetch before blaming kernels.")
    recommendations.append("Measure with warmup plus synchronized timings before claiming performance wins.")
    return recommendations


def build_report() -> dict[str, Any]:
    devices = collect_devices()
    report = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "torch_version": torch.__version__,
        "torch_cuda_version": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
        "device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
        "cudnn_available": torch.backends.cudnn.is_available(),
        "cudnn_version": torch.backends.cudnn.version(),
        "devices": devices,
        "env": {key: os.environ.get(key) for key in ENV_KEYS if os.environ.get(key) is not None},
        "recommendations": collect_recommendations(devices),
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    args = parser.parse_args()

    report = build_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0

    print(f"Python: {report['python']}")
    print(f"Platform: {report['platform']}")
    print(f"PyTorch: {report['torch_version']} (CUDA {report['torch_cuda_version']})")
    print(f"CUDA available: {report['cuda_available']}")
    print(f"cuDNN: available={report['cudnn_available']} version={report['cudnn_version']}")
    print(f"Device count: {report['device_count']}")
    for device in report["devices"]:
        print(
            f"- GPU {device['index']}: {device['name']} | cc={device['compute_capability']} | "
            f"mem={device['total_memory_gib']} GiB | sm={device['multi_processor_count']}"
        )
    if report["env"]:
        print("Selected env vars:")
        for key, value in report["env"].items():
            print(f"- {key}={value}")
    print("Recommendations:")
    for item in report["recommendations"]:
        print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
