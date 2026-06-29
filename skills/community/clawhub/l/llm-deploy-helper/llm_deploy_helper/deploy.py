"""System detection: CPU, RAM, disk, GPU information."""

from __future__ import annotations

import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Any


@dataclass
class SystemInfo:
    """Collected system hardware information."""

    cpu_cores: int
    ram_gb: float
    disk_free_gb: float
    gpu_available: bool
    gpu_name: str = ""
    gpu_vram_gb: float = 0.0
    cuda_version: str = ""
    os_type: str = ""


def _cpu_cores() -> int:
    """Return logical CPU core count."""
    try:
        import psutil
        return psutil.cpu_count(logical=True) or 1
    except ImportError:
        pass

    # Fallback: /proc/cpuinfo
    try:
        with open("/proc/cpuinfo") as f:
            return f.read().count("processor\t:")
    except Exception:
        pass

    # Fallback: os.cpu_count
    import os
    return os.cpu_count() or 1


def _ram_gb() -> float:
    """Return total RAM in GB."""
    try:
        import psutil
        return round(psutil.virtual_memory().total / (1024 ** 3), 1)
    except ImportError:
        pass

    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    kb = int(line.split()[1])
                    return round(kb / (1024 * 1024), 1)
    except Exception:
        pass

    return 0.0


def _disk_free_gb(path: str = "/") -> float:
    """Return free disk space in GB."""
    try:
        usage = shutil.disk_usage(path)
        return round(usage.free / (1024 ** 3), 1)
    except Exception:
        return 0.0


def _gpu_info() -> tuple[bool, str, float, str]:
    """Detect GPU via nvidia-smi.

    Returns
    -------
    tuple[bool, str, float, str]
        (available, name, vram_gb, cuda_version)
    """
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total,driver_version",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode != 0:
            return False, "", 0.0, ""

        parts = result.stdout.strip().split(", ")
        if len(parts) < 3:
            return False, "", 0.0, ""

        name = parts[0].strip()
        vram_mb = float(parts[1].strip())
        driver = parts[2].strip()

        # Get CUDA version via nvcc if available
        cuda_ver = ""
        try:
            nvcc = subprocess.run(
                ["nvcc", "--version"],
                capture_output=True, text=True, timeout=10,
            )
            if nvcc.returncode == 0:
                for line in nvcc.stdout.splitlines():
                    if "release" in line:
                        cuda_ver = line.split("release")[-1].strip().rstrip(",")
                        break
        except Exception:
            pass

        return True, name, round(vram_mb / 1024, 1), cuda_ver or driver
    except FileNotFoundError:
        return False, "", 0.0, ""
    except Exception:
        return False, "", 0.0, ""


def _os_type() -> str:
    """Return OS type string."""
    return f"{sys.platform}"


def detect_system() -> SystemInfo:
    """Detect hardware and OS information.

    Returns
    -------
    SystemInfo
    """
    gpu_available, gpu_name, gpu_vram, cuda_ver = _gpu_info()
    return SystemInfo(
        cpu_cores=_cpu_cores(),
        ram_gb=_ram_gb(),
        disk_free_gb=_disk_free_gb(),
        gpu_available=gpu_available,
        gpu_name=gpu_name,
        gpu_vram_gb=gpu_vram,
        cuda_version=cuda_ver,
        os_type=_os_type(),
    )


def recommend_engine(info: SystemInfo) -> list[tuple[str, str, int]]:
    """Recommend deployment engines based on system capabilities.

    Parameters
    ----------
    info : SystemInfo

    Returns
    -------
    list[tuple[str, str, int]]
        List of ``(engine_name, reason, score)`` sorted by score descending.
        Score is 1-10 (higher = better fit).
    """
    recommendations: list[tuple[str, str, int]] = []

    has_gpu = info.gpu_available
    vram = info.gpu_vram_gb
    ram = info.ram_gb

    # vLLM — best for powerful GPU (>=8 GB VRAM)
    if has_gpu and vram >= 8:
        recommendations.append(("vllm", f"Powerful GPU ({vram:.0f} GB VRAM) – vLLM provides best throughput", 10))
    elif has_gpu and vram > 0:
        recommendations.append(("vllm", f"GPU with {vram:.0f} GB VRAM – vLLM may work for small models", 5))

    # Ollama — good all-around, works with or without GPU
    if has_gpu:
        recommendations.append(("ollama", f"GPU available ({info.gpu_name}) – Ollama auto-uses GPU acceleration", 8))
    else:
        if ram >= 16:
            recommendations.append(("ollama", f"No GPU but {ram:.0f} GB RAM – Ollama runs well on CPU for 7-8B models", 7))
        else:
            recommendations.append(("ollama", f"Limited RAM ({ram:.0f} GB) – Ollama may struggle with larger models", 4))

    # llama.cpp — lightweight, runs everywhere
    if ram >= 32:
        recommendations.append(("llama.cpp", f"Abundant RAM ({ram:.0f} GB) – llama.cpp handles any quantized model", 9))
    elif ram >= 16:
        recommendations.append(("llama.cpp", f"{ram:.0f} GB RAM – llama.cpp runs 7-8B models comfortably", 7))
    else:
        recommendations.append(("llama.cpp", f"Low RAM ({ram:.0f} GB) – use llama.cpp with small/quantized models only", 5))

    # Sort by score descending
    recommendations.sort(key=lambda x: x[2], reverse=True)
    return recommendations
