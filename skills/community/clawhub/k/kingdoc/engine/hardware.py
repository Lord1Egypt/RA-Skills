"""KingDoc 硬件自适应性能模块

目标：在「不拖累用户电脑」的前提下，自动采集本机硬件能力，
并据此计算出安全的并发子进程数 / 批量大小，避免把低端机器拖垮。

设计原则：
- 零第三方依赖（仅用标准库），可在任意环境运行
- 保守优先：默认并发不超过物理核心数，且对小内存机器进一步收紧
- 结果可缓存：写入 hardware_profile.json，避免每次调用都重新探测
"""
from __future__ import annotations

import json
import os
import platform
import shutil
import sys
import time
from pathlib import Path
from typing import Dict, Optional


# 缓存文件（与 skill 根目录同级，不进版本库）
_PROFILE_CACHE_NAME = ".kingdoc_hardware_profile.json"


def _logical_cpu_count() -> int:
    try:
        return os.cpu_count() or 1
    except Exception:
        return 1


def _physical_cpu_count() -> int:
    """尽力获取物理核心数；拿不到就退化为逻辑核心数。"""
    system = platform.system()
    try:
        if system == "Linux":
            out = _read_proc_cpuinfo()
            return out or _logical_cpu_count()
        if system == "Darwin":
            out = _run_sysctl("hw.physicalcpu")
            return int(out) if out and out.isdigit() else _logical_cpu_count()
        if system == "Windows":
            out = _run_wmic("CPU", "NumberOfCores")
            if out:
                # WMIC 可能返回多行（多颗 CPU），求和
                total = 0
                for line in out.splitlines():
                    line = line.strip()
                    if line.isdigit():
                        total += int(line)
                if total:
                    return total
    except Exception:
        pass
    return _logical_cpu_count()


def _read_proc_cpuinfo() -> Optional[int]:
    try:
        count = 0
        with open("/proc/cpuinfo", "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if line.lower().startswith("cpu cores"):
                    parts = line.split(":")
                    if len(parts) == 2:
                        v = parts[1].strip()
                        if v.isdigit():
                            count += int(v)
        return count or None
    except Exception:
        return None


def _run_sysctl(key: str) -> Optional[str]:
    if shutil.which("sysctl"):
        try:
            import subprocess
            out = subprocess.run(
                ["sysctl", "-n", key], capture_output=True, text=True, timeout=5
            )
            return out.stdout.strip()
        except Exception:
            return None
    return None


def _run_wmic(table: str, field: str) -> Optional[str]:
    if shutil.which("wmic"):
        try:
            import subprocess
            out = subprocess.run(
                ["wmic", table, "get", field, "/value"],
                capture_output=True, text=True, timeout=5,
            )
            return out.stdout.strip()
        except Exception:
            return None
    return None


def _total_memory_gb() -> float:
    """跨平台获取物理内存总量（GB）。"""
    system = platform.system()
    try:
        if system == "Linux":
            with open("/proc/meminfo", "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if line.lower().startswith("memtotal:"):
                        kb = int(line.split()[1])
                        return round(kb / (1024 ** 2), 1)
        elif system == "Darwin":
            val = _run_sysctl("hw.memsize")
            if val and val.isdigit():
                return round(int(val) / (1024 ** 3), 1)
        elif system == "Windows":
            return _windows_memory_gb()
    except Exception:
        pass
    # 兜底：用 psutil（若用户装了）
    try:
        import psutil
        return round(psutil.virtual_memory().total / (1024 ** 3), 1)
    except Exception:
        return 4.0  # 保守默认值


def _windows_memory_gb() -> float:
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32  # type: ignore
        class MEMORYSTATUS(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("dwTotalPhys", ctypes.c_size_t),
                ("dwAvailPhys", ctypes.c_size_t),
                ("dwTotalPageFile", ctypes.c_size_t),
                ("dwAvailPageFile", ctypes.c_size_t),
                ("dwTotalVirtual", ctypes.c_size_t),
                ("dwAvailVirtual", ctypes.c_size_t),
            ]
        stat = MEMORYSTATUS()
        stat.dwLength = ctypes.sizeof(MEMORYSTATUS)
        kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
        return round(stat.dwTotalPhys / (1024 ** 3), 1)
    except Exception:
        return 4.0


def _is_low_power(physical: int, mem_gb: float) -> bool:
    return physical <= 2 or mem_gb < 4.0


def _is_high_end(physical: int, mem_gb: float) -> bool:
    return physical >= 8 and mem_gb >= 16.0


def detect_hardware(force: bool = False, cache_dir: Optional[str] = None) -> Dict:
    """采集硬件信息并返回完整画像。

    Args:
        force: 为 True 时忽略缓存重新探测。
        cache_dir: 缓存文件目录（默认 skill 根目录）。
    """
    cache_path = _cache_path(cache_dir)
    if not force and cache_path.exists():
        try:
            cached = json.loads(cache_path.read_text(encoding="utf-8"))
            # 30 分钟内复用缓存，避免频繁探测
            if time.time() - cached.get("_ts", 0) < 1800:
                return cached
        except Exception:
            pass

    physical = _physical_cpu_count()
    logical = _logical_cpu_count()
    mem_gb = _total_memory_gb()
    arch = platform.machine() or "unknown"
    system = platform.system()

    profile = {
        "system": system,
        "arch": arch,
        "physical_cores": physical,
        "logical_cores": logical,
        "memory_gb": mem_gb,
        "low_power": _is_low_power(physical, mem_gb),
        "high_end": _is_high_end(physical, mem_gb),
        "_ts": int(time.time()),
    }
    profile.update(_recommend(profile))
    try:
        cache_path.write_text(json.dumps(profile, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass
    return profile


def _recommend(profile: Dict) -> Dict:
    """根据硬件画像计算推荐并发与批量参数（核心：不拖累电脑）。"""
    physical = max(profile["physical_cores"], 1)
    mem_gb = profile["memory_gb"]

    # 1) 并发子进程数：不超过物理核心，且对小内存机器收紧
    if profile["low_power"]:
        max_workers = 1
    elif profile["high_end"]:
        max_workers = min(physical, 8)   # 高端机最多 8，避免把整机占满
    else:
        max_workers = min(physical, 4)   # 普通机最多 4
    max_workers = max(1, max_workers)

    # 2) 批量写入分块大小：内存越小块越小，降低峰值占用
    if mem_gb < 4.0:
        batch_chunk = 50
    elif mem_gb < 8.0:
        batch_chunk = 200
    else:
        batch_chunk = 500

    # 3) 大文件阈值：内存紧张时降低
    big_file_threshold_mb = 100 if mem_gb >= 8.0 else 50

    # 4) 是否启用本地重渲染（思维导图/流程图 SVG）：低端机允许但串行
    local_render_parallel = not profile["low_power"] and max_workers > 1

    return {
        "recommended_workers": max_workers,
        "recommended_batch_chunk": batch_chunk,
        "big_file_threshold_mb": big_file_threshold_mb,
        "local_render_parallel": local_render_parallel,
        "throttle_note": _throttle_note(max_workers, mem_gb),
    }


def _throttle_note(workers: int, mem_gb: float) -> str:
    if workers == 1:
        return f"检测到本机资源紧张（内存 {mem_gb}GB），已自动限制为单线程，确保不卡顿。"
    return f"已按本机硬件自动分配 {workers} 个并发子进程，兼顾速度与流畅。"


def _cache_path(cache_dir: Optional[str]) -> Path:
    if cache_dir:
        return Path(cache_dir) / _PROFILE_CACHE_NAME
    # 默认 skill 根目录（engine 的上两级）
    return Path(__file__).resolve().parent.parent.parent / _PROFILE_CACHE_NAME


def get_recommended_settings(cache_dir: Optional[str] = None) -> Dict:
    """对外的便捷入口：返回推荐的性能参数。"""
    profile = detect_hardware(cache_dir=cache_dir)
    return {
        "workers": profile["recommended_workers"],
        "batch_chunk": profile["recommended_batch_chunk"],
        "big_file_threshold_mb": profile["big_file_threshold_mb"],
        "local_render_parallel": profile["local_render_parallel"],
        "low_power": profile["low_power"],
        "note": profile["throttle_note"],
        "profile": {k: v for k, v in profile.items() if not k.startswith("_")},
    }


def main():
    """命令行：打印硬件画像与推荐参数。"""
    settings = get_recommended_settings()
    print(json.dumps(settings, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
