#!/usr/bin/env python3
"""Create a privacy-safe, read-only hardware and accelerator report."""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shlex
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

VERSION = "0.1.0"
SCHEMA_VERSION = "1.0"
SCHEMA_URL = "https://raw.githubusercontent.com/dancher00/hardware-inspector/main/schema/hardware-report.schema.json"
MAX_OUTPUT_CHARS = 64_000


@dataclass(frozen=True)
class CommandSpec:
    group: str
    name: str
    argv: Tuple[str, ...]
    timeout: Optional[float] = None


@dataclass(frozen=True)
class FileSpec:
    group: str
    name: str
    path: str


SENSITIVE_LINE_RE = re.compile(
    r"(?im)^(\s*[\"']?(?:serial(?:[ _-]?number)?|uuid|machine[ _-]?id|"
    r"host(?:[ _-]?name)?|mac(?:[ _-]?address)?|ip(?:v4|v6)?(?:[ _-]?address)?|"
    r"token)[\"']?\s*[:=]\s*)(.*)$"
)
MAC_RE = re.compile(r"(?i)\b(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}\b")
IPV4_RE = re.compile(
    r"\b(?:25[0-5]|2[0-4]\d|1?\d?\d)(?:\."
    r"(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}\b"
)
UUID_RE = re.compile(
    r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
    r"[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"
)


def _string(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def redact_text(text: str, enabled: bool = True) -> str:
    """Redact common machine and user identifiers from free-form output."""
    if not enabled or not text:
        return text

    redacted = text
    home = str(Path.home())
    username = os.environ.get("USERNAME") or os.environ.get("USER") or ""
    hostname = platform.node()

    for value, marker in (
        (home, "<home>"),
        (hostname, "<hostname>"),
    ):
        if value and len(value) > 2:
            redacted = re.sub(re.escape(value), marker, redacted, flags=re.IGNORECASE)

    if username and len(username) > 2:
        redacted = re.sub(
            r"(?i)(?<![\w.-])" + re.escape(username) + r"(?![\w.-])",
            "<user>",
            redacted,
        )

    redacted = SENSITIVE_LINE_RE.sub(
        lambda match: match.group(1) + "<redacted>", redacted
    )
    redacted = UUID_RE.sub("<uuid>", redacted)
    redacted = MAC_RE.sub("<mac>", redacted)
    redacted = IPV4_RE.sub("<ip>", redacted)
    return redacted


def _truncate(text: str) -> str:
    if len(text) <= MAX_OUTPUT_CHARS:
        return text
    removed = len(text) - MAX_OUTPUT_CHARS
    return text[:MAX_OUTPUT_CHARS] + "\n... <truncated {} characters>".format(removed)


def _display_command(argv: Sequence[str]) -> str:
    if len(argv) >= 3 and argv[1] in ("-c", "-Command"):
        return "{} {} <embedded read-only probe>".format(
            shlex.quote(argv[0]), shlex.quote(argv[1])
        )
    return " ".join(shlex.quote(part) for part in argv)


def run_command(spec: CommandSpec, timeout: float, redact: bool) -> Dict[str, Any]:
    argv = list(spec.argv)
    executable = argv[0] if os.path.isabs(argv[0]) else shutil.which(argv[0])
    result: Dict[str, Any] = {
        "group": spec.group,
        "name": spec.name,
        "kind": "command",
        "command": _display_command(argv),
        "status": "missing" if not executable else "pending",
        "returncode": None,
        "duration_ms": 0,
        "stdout": "",
        "stderr": "",
    }
    if not executable:
        return result

    argv[0] = executable
    environment = os.environ.copy()
    environment.update(
        {
            "LC_ALL": "C",
            "LANG": "C",
            "NO_COLOR": "1",
            "PAGER": "cat",
            "TERM": "dumb",
        }
    )
    started = time.monotonic()
    try:
        completed = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=spec.timeout or timeout,
            check=False,
            shell=False,
            env=environment,
        )
        result["status"] = "ok" if completed.returncode == 0 else "error"
        result["returncode"] = completed.returncode
        result["stdout"] = _truncate(redact_text(completed.stdout, redact))
        result["stderr"] = _truncate(redact_text(completed.stderr, redact))
    except subprocess.TimeoutExpired as error:
        result["status"] = "timeout"
        result["stdout"] = _truncate(redact_text(_string(error.stdout), redact))
        result["stderr"] = _truncate(redact_text(_string(error.stderr), redact))
    except OSError as error:
        result["status"] = "error"
        result["stderr"] = redact_text(str(error), redact)
    finally:
        result["duration_ms"] = int((time.monotonic() - started) * 1000)
    return result


def read_file(spec: FileSpec, redact: bool) -> Dict[str, Any]:
    path = Path(spec.path)
    result: Dict[str, Any] = {
        "group": spec.group,
        "name": spec.name,
        "kind": "file",
        "source": spec.path,
        "status": "missing",
        "returncode": None,
        "duration_ms": 0,
        "stdout": "",
        "stderr": "",
    }
    started = time.monotonic()
    try:
        data = (
            path.read_text(encoding="utf-8", errors="replace")
            .replace("\x00", "")
            .strip()
        )
        result["status"] = "ok"
        result["stdout"] = _truncate(redact_text(data, redact))
    except FileNotFoundError:
        pass
    except OSError as error:
        result["status"] = "error"
        result["stderr"] = redact_text(str(error), redact)
    result["duration_ms"] = int((time.monotonic() - started) * 1000)
    return result


def _read_short(path: str) -> str:
    try:
        return (
            Path(path)
            .read_text(encoding="utf-8", errors="replace")
            .replace("\x00", "")
            .strip()
        )
    except OSError:
        return ""


def _os_release() -> Dict[str, str]:
    values: Dict[str, str] = {}
    raw = _read_short("/etc/os-release")
    for line in raw.splitlines():
        if "=" not in line or line.lstrip().startswith("#"):
            continue
        key, value = line.split("=", 1)
        values[key] = value.strip().strip('"')
    return values


def _memory_bytes() -> Optional[int]:
    if platform.system() == "Windows":
        try:
            import ctypes

            class MemoryStatus(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_uint32),
                    ("dwMemoryLoad", ctypes.c_uint32),
                    ("ullTotalPhys", ctypes.c_uint64),
                    ("ullAvailPhys", ctypes.c_uint64),
                    ("ullTotalPageFile", ctypes.c_uint64),
                    ("ullAvailPageFile", ctypes.c_uint64),
                    ("ullTotalVirtual", ctypes.c_uint64),
                    ("ullAvailVirtual", ctypes.c_uint64),
                    ("ullAvailExtendedVirtual", ctypes.c_uint64),
                ]

            status = MemoryStatus()
            status.dwLength = ctypes.sizeof(MemoryStatus)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
                return int(status.ullTotalPhys)
        except (AttributeError, OSError):
            pass
    if platform.system() == "Linux":
        for line in _read_short("/proc/meminfo").splitlines():
            if line.startswith("MemTotal:"):
                try:
                    return int(line.split()[1]) * 1024
                except (IndexError, ValueError):
                    return None
    try:
        pages = os.sysconf("SC_PHYS_PAGES")
        page_size = os.sysconf("SC_PAGE_SIZE")
        if isinstance(pages, int) and isinstance(page_size, int):
            return pages * page_size
    except (AttributeError, OSError, ValueError):
        pass
    return None


def _cgroup_candidates(controller: str, filename: str) -> List[Path]:
    base = Path("/sys/fs/cgroup")
    candidates = [base / filename, base / controller / filename]
    for line in _read_short("/proc/self/cgroup").splitlines():
        fields = line.split(":", 2)
        if len(fields) != 3:
            continue
        hierarchy, controllers, relative = fields
        relative_path = relative.lstrip("/")
        if hierarchy == "0" and not controllers:
            candidates.append(base / relative_path / filename)
        elif controller in controllers.split(","):
            candidates.append(base / controller / relative_path / filename)
            candidates.append(base / relative_path / filename)
    unique: List[Path] = []
    seen = set()
    for candidate in candidates:
        key = str(candidate)
        if key not in seen:
            unique.append(candidate)
            seen.add(key)
    return unique


def _cgroup_value(controller: str, filename: str) -> str:
    for candidate in _cgroup_candidates(controller, filename):
        value = _read_short(str(candidate))
        if value:
            return value
    return ""


def _cpu_set_count(value: str) -> Optional[int]:
    if not value:
        return None
    total = 0
    try:
        for section in value.split(","):
            bounds = section.strip().split("-", 1)
            start = int(bounds[0])
            end = int(bounds[1]) if len(bounds) == 2 else start
            if end < start:
                return None
            total += end - start + 1
    except ValueError:
        return None
    return total


def _finite_memory_limit(value: str, host_memory: Optional[int]) -> Optional[int]:
    if not value or value == "max":
        return None
    try:
        limit = int(value)
    except ValueError:
        return None
    if limit <= 0 or limit >= (1 << 60):
        return None
    if host_memory and limit > host_memory * 8:
        return None
    return limit


def _safe_visibility_value(value: str, redact: bool) -> str:
    normalized = value.strip()
    lowered = normalized.lower()
    if lowered in ("all", "none", "void") or not normalized:
        return lowered or "empty"
    devices = [item.strip() for item in normalized.split(",") if item.strip()]
    if all(device.isdigit() for device in devices):
        return ",".join(devices)
    if not redact:
        return normalized
    return "<{} assigned device identifier{}>".format(
        len(devices), "" if len(devices) == 1 else "s"
    )


def _execution_envelope(redact: bool) -> Dict[str, Any]:
    host_cpu_count = os.cpu_count()
    host_memory = _memory_bytes()
    cpu_max = _cgroup_value("cpu", "cpu.max")
    quota_cores: Optional[float] = None
    if cpu_max:
        parts = cpu_max.split()
        if len(parts) == 2 and parts[0] != "max":
            try:
                quota_cores = int(parts[0]) / int(parts[1])
            except (ValueError, ZeroDivisionError):
                pass
    else:
        quota = _cgroup_value("cpu", "cpu.cfs_quota_us")
        period = _cgroup_value("cpu", "cpu.cfs_period_us")
        try:
            if int(quota) > 0 and int(period) > 0:
                quota_cores = int(quota) / int(period)
        except (TypeError, ValueError, ZeroDivisionError):
            pass

    cpuset = _cgroup_value("cpuset", "cpuset.cpus.effective") or _cgroup_value(
        "cpuset", "cpuset.cpus"
    )
    cpuset_count = _cpu_set_count(cpuset)
    cpu_candidates = [
        float(value)
        for value in (host_cpu_count, cpuset_count, quota_cores)
        if value is not None
    ]
    effective_cpu = min(cpu_candidates) if cpu_candidates else None

    memory_raw = _cgroup_value("memory", "memory.max") or _cgroup_value(
        "memory", "memory.limit_in_bytes"
    )
    memory_limit = _finite_memory_limit(memory_raw, host_memory)
    effective_memory = (
        min(value for value in (host_memory, memory_limit) if value is not None)
        if host_memory or memory_limit
        else None
    )

    pids_raw = _cgroup_value("pids", "pids.max")
    try:
        pids_limit = int(pids_raw) if pids_raw and pids_raw != "max" else None
    except ValueError:
        pids_limit = None

    visibility: Dict[str, str] = {}
    for name in (
        "CUDA_VISIBLE_DEVICES",
        "NVIDIA_VISIBLE_DEVICES",
        "ROCR_VISIBLE_DEVICES",
        "HIP_VISIBLE_DEVICES",
        "ZE_AFFINITY_MASK",
    ):
        if name in os.environ:
            visibility[name] = _safe_visibility_value(os.environ[name], redact)

    scheduler: Dict[str, Any] = {}
    if Path("/var/run/secrets/kubernetes.io/serviceaccount").exists() or os.environ.get(
        "KUBERNETES_SERVICE_HOST"
    ):
        scheduler["orchestrator"] = "kubernetes"
    if os.environ.get("SLURM_JOB_ID"):
        scheduler["scheduler"] = "slurm"
        scheduler["allocation"] = {
            name: os.environ[name]
            for name in (
                "SLURM_CPUS_PER_TASK",
                "SLURM_CPUS_ON_NODE",
                "SLURM_MEM_PER_CPU",
                "SLURM_MEM_PER_NODE",
                "SLURM_GPUS",
                "SLURM_GPUS_PER_NODE",
                "SLURM_GPUS_ON_NODE",
            )
            if name in os.environ
        }

    return {
        "cgroup_version": 2
        if Path("/sys/fs/cgroup/cgroup.controllers").exists()
        else (1 if Path("/sys/fs/cgroup").exists() else None),
        "cpu_quota_cores": quota_cores,
        "cpuset": cpuset or None,
        "cpuset_cpu_count": cpuset_count,
        "effective_cpu_cores": effective_cpu,
        "memory_limit_bytes": memory_limit,
        "effective_memory_bytes": effective_memory,
        "pids_limit": pids_limit,
        "accelerator_visibility": visibility,
        "scheduler": scheduler,
    }


def _board_model() -> str:
    for path in (
        "/sys/firmware/devicetree/base/model",
        "/proc/device-tree/model",
        "/sys/class/dmi/id/product_name",
    ):
        value = _read_short(path)
        if value:
            return value
    return ""


def _platform_tags(system: str, model: str) -> List[str]:
    tags: List[str] = []
    lowered_model = model.lower()
    lowered_release = platform.release().lower()
    if Path("/etc/nv_tegra_release").exists() or "jetson" in lowered_model:
        tags.append("nvidia-jetson")
    if "raspberry pi" in lowered_model:
        tags.append("raspberry-pi")
    if "microsoft" in lowered_release:
        tags.append("wsl")
    if Path("/var/run/secrets/kubernetes.io/serviceaccount").exists() or os.environ.get(
        "KUBERNETES_SERVICE_HOST"
    ):
        tags.append("kubernetes-pod")
    if os.environ.get("SLURM_JOB_ID"):
        tags.append("slurm-allocation")
    if Path("/.dockerenv").exists() or Path("/run/.containerenv").exists():
        tags.append("container")
    if system == "Darwin" and platform.machine().lower() in ("arm64", "aarch64"):
        tags.append("apple-silicon")
    return tags


def build_summary(redact: bool = True) -> Dict[str, Any]:
    system = platform.system() or "Unknown"
    model = _board_model()
    release = _os_release()
    operating_system = system
    if system == "Linux" and release:
        operating_system = release.get("PRETTY_NAME") or release.get("NAME") or system
    execution = _execution_envelope(redact)
    return {
        "operating_system": operating_system,
        "os_family": system,
        "kernel_release": platform.release(),
        "architecture": platform.machine() or "unknown",
        "board_model": model or None,
        "logical_cpu_count": os.cpu_count(),
        "memory_bytes": _memory_bytes(),
        "execution_envelope": execution,
        "python_version": platform.python_version(),
        "platform_tags": _platform_tags(system, model),
    }


def _powershell() -> Optional[str]:
    for command in ("pwsh", "powershell.exe", "powershell"):
        resolved = shutil.which(command)
        if resolved:
            return resolved
    return None


def _framework_probe_code() -> str:
    return """
import importlib.util
import json
result = {}
for name in ("torch", "tensorflow", "jax"):
    if importlib.util.find_spec(name) is None:
        result[name] = {"installed": False}
        continue
    try:
        module = __import__(name)
        item = {"installed": True, "version": getattr(module, "__version__", "unknown")}
        if name == "torch":
            item["cuda_available"] = bool(module.cuda.is_available())
            item["cuda_version"] = getattr(module.version, "cuda", None)
            item["hip_version"] = getattr(module.version, "hip", None)
            if item["cuda_available"]:
                item["devices"] = [module.cuda.get_device_name(i) for i in range(module.cuda.device_count())]
        elif name == "tensorflow":
            item["accelerators"] = [device.device_type + ":" + device.name for device in module.config.list_physical_devices() if device.device_type != "CPU"]
        elif name == "jax":
            item["default_backend"] = module.default_backend()
            item["devices"] = [str(device) for device in module.devices()]
        result[name] = item
    except Exception as error:
        result[name] = {"installed": True, "error": type(error).__name__ + ": " + str(error)}
print(json.dumps(result, sort_keys=True))
""".strip()


def command_specs(summary: Dict[str, Any], full: bool) -> List[CommandSpec]:
    system = summary["os_family"]
    tags = set(summary["platform_tags"])
    specs: List[CommandSpec] = []

    if system == "Linux":
        specs.extend(
            [
                CommandSpec("cpu", "CPU topology", ("lscpu",)),
                CommandSpec("memory", "Memory usage", ("free", "--bytes")),
                CommandSpec(
                    "storage",
                    "Block devices",
                    (
                        "lsblk",
                        "--json",
                        "--bytes",
                        "--output",
                        "NAME,TYPE,SIZE,MODEL,ROTA,TRAN,MOUNTPOINT",
                    ),
                ),
                CommandSpec("devices", "PCI devices and drivers", ("lspci", "-nnk")),
                CommandSpec("devices", "USB devices", ("lsusb",)),
                CommandSpec("environment", "Virtualization", ("systemd-detect-virt",)),
                CommandSpec("thermals", "Temperature sensors", ("sensors", "-j")),
            ]
        )
        if "raspberry-pi" in tags:
            specs.extend(
                [
                    CommandSpec(
                        "raspberry-pi", "Throttle flags", ("vcgencmd", "get_throttled")
                    ),
                    CommandSpec(
                        "raspberry-pi", "SoC temperature", ("vcgencmd", "measure_temp")
                    ),
                    CommandSpec(
                        "raspberry-pi",
                        "GPU memory split",
                        ("vcgencmd", "get_mem", "gpu"),
                    ),
                ]
            )
        if "nvidia-jetson" in tags:
            specs.extend(
                [
                    CommandSpec("jetson", "Power mode", ("nvpmodel", "-q")),
                    CommandSpec(
                        "jetson",
                        "Jetson live telemetry sample",
                        ("tegrastats", "--interval", "1000"),
                        timeout=2.5,
                    ),
                    CommandSpec(
                        "jetson", "Jetson release helper", ("jetson_release", "-v")
                    ),
                ]
            )
    elif system == "Darwin":
        specs.extend(
            [
                CommandSpec("system", "macOS version", ("sw_vers",)),
                CommandSpec(
                    "cpu", "CPU model", ("sysctl", "-n", "machdep.cpu.brand_string")
                ),
                CommandSpec(
                    "memory", "Physical memory", ("sysctl", "-n", "hw.memsize")
                ),
                CommandSpec(
                    "devices",
                    "Apple hardware, displays, and storage",
                    (
                        "system_profiler",
                        "SPHardwareDataType",
                        "SPDisplaysDataType",
                        "SPStorageDataType",
                        "-json",
                    ),
                    timeout=20.0,
                ),
                CommandSpec("storage", "Disk layout", ("diskutil", "list")),
            ]
        )
        if full:
            specs.append(
                CommandSpec(
                    "devices",
                    "Apple peripheral inventory",
                    (
                        "system_profiler",
                        "SPUSBDataType",
                        "SPThunderboltDataType",
                        "SPPCIDataType",
                        "-json",
                    ),
                    timeout=30.0,
                )
            )

    elif system == "Windows":
        shell = _powershell()
        if shell:
            inventory = r"""
$ErrorActionPreference = 'SilentlyContinue'
[ordered]@{
  os = Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version,BuildNumber,OSArchitecture
  computer = Get-CimInstance Win32_ComputerSystem | Select-Object Manufacturer,Model,SystemType,TotalPhysicalMemory
  cpu = @(Get-CimInstance Win32_Processor | Select-Object Name,Manufacturer,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed)
  memory = @(Get-CimInstance Win32_PhysicalMemory | Select-Object Manufacturer,PartNumber,Capacity,Speed,ConfiguredClockSpeed)
  gpu = @(Get-CimInstance Win32_VideoController | Select-Object Name,AdapterRAM,DriverVersion,DriverDate,VideoProcessor)
  disks = @(Get-CimInstance Win32_DiskDrive | Select-Object Model,MediaType,InterfaceType,Size,FirmwareRevision)
  baseboard = Get-CimInstance Win32_BaseBoard | Select-Object Manufacturer,Product,Version
  bios = Get-CimInstance Win32_BIOS | Select-Object Manufacturer,SMBIOSBIOSVersion,ReleaseDate
} | ConvertTo-Json -Depth 5
""".strip()
            specs.append(
                CommandSpec(
                    "system",
                    "Windows hardware inventory",
                    (shell, "-NoProfile", "-NonInteractive", "-Command", inventory),
                    timeout=20.0,
                )
            )
            if full:
                pnp = r"""
$ErrorActionPreference = 'SilentlyContinue'
[ordered]@{
  devices = @(Get-PnpDevice -PresentOnly | Select-Object Class,FriendlyName,Manufacturer,Status)
  network = @(Get-NetAdapter | Select-Object InterfaceDescription,DriverDescription,DriverVersion,LinkSpeed,Status)
} | ConvertTo-Json -Depth 5
""".strip()
                specs.append(
                    CommandSpec(
                        "devices",
                        "Windows device and driver inventory",
                        (shell, "-NoProfile", "-NonInteractive", "-Command", pnp),
                        timeout=30.0,
                    )
                )

    specs.extend(
        [
            CommandSpec(
                "accelerators",
                "NVIDIA visible devices and MIG layout",
                ("nvidia-smi", "-L"),
            ),
            CommandSpec(
                "accelerators",
                "NVIDIA GPU capacity and live availability",
                (
                    "nvidia-smi",
                    "--query-gpu=name,driver_version,memory.total,memory.free,memory.used,utilization.gpu,pci.bus_id",
                    "--format=csv,noheader",
                ),
            ),
            CommandSpec("accelerators", "CUDA toolkit", ("nvcc", "--version")),
            CommandSpec(
                "accelerators",
                "AMD ROCm summary",
                (
                    "rocm-smi",
                    "--showproductname",
                    "--showdriverversion",
                    "--showmeminfo",
                    "vram",
                ),
            ),
            CommandSpec(
                "accelerators", "Intel XPU inventory", ("xpu-smi", "discovery")
            ),
            CommandSpec("accelerators", "OpenCL platforms", ("clinfo", "-l")),
            CommandSpec("accelerators", "Vulkan summary", ("vulkaninfo", "--summary")),
        ]
    )
    if full:
        specs.extend(
            [
                CommandSpec(
                    "accelerators", "AMD ROCm agents", ("rocminfo",), timeout=20.0
                ),
                CommandSpec(
                    "frameworks",
                    "Python ML framework readiness",
                    (sys.executable, "-c", _framework_probe_code()),
                    timeout=30.0,
                ),
            ]
        )
    return specs


def file_specs(summary: Dict[str, Any]) -> List[FileSpec]:
    if summary["os_family"] != "Linux":
        return []
    specs = [
        FileSpec("system", "Device-tree model", "/sys/firmware/devicetree/base/model"),
        FileSpec("firmware", "System vendor", "/sys/class/dmi/id/sys_vendor"),
        FileSpec("firmware", "Product model", "/sys/class/dmi/id/product_name"),
        FileSpec("firmware", "Board model", "/sys/class/dmi/id/board_name"),
        FileSpec("firmware", "BIOS version", "/sys/class/dmi/id/bios_version"),
    ]
    if "nvidia-jetson" in set(summary["platform_tags"]):
        specs.append(
            FileSpec("jetson", "Jetson Linux release", "/etc/nv_tegra_release")
        )
    if "raspberry-pi" in set(summary["platform_tags"]):
        specs.append(
            FileSpec(
                "raspberry-pi", "Raspberry Pi CPU and revision details", "/proc/cpuinfo"
            )
        )
    return specs


def collect_report(
    full: bool = False, timeout: float = 8.0, redact: bool = True
) -> Dict[str, Any]:
    summary = build_summary(redact)
    probes: List[Dict[str, Any]] = []
    for spec in file_specs(summary):
        probes.append(read_file(spec, redact))
    for spec in command_specs(summary, full):
        probes.append(run_command(spec, timeout, redact))
    return {
        "schema_version": SCHEMA_VERSION,
        "$schema": SCHEMA_URL,
        "collector_version": VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "privacy": {
            "redaction_enabled": redact,
            "network_requests": False,
            "privilege_elevation": False,
            "redacted_categories": [
                "hostnames",
                "usernames",
                "home paths",
                "serial numbers",
                "UUIDs",
                "MAC addresses",
                "IP addresses",
            ]
            if redact
            else [],
        },
        "summary": summary,
        "probes": probes,
    }


def _human_bytes(value: Optional[int]) -> str:
    if value is None:
        return "unknown"
    number = float(value)
    for suffix in ("B", "KiB", "MiB", "GiB", "TiB"):
        if number < 1024.0 or suffix == "TiB":
            return "{:.1f} {}".format(number, suffix)
        number /= 1024.0
    return str(value)


def _md(value: Any) -> str:
    if value is None or value == "":
        return "unknown"
    if isinstance(value, list):
        value = ", ".join(str(item) for item in value) or "none"
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: Dict[str, Any]) -> str:
    summary = report["summary"]
    privacy = report["privacy"]
    execution = summary.get("execution_envelope", {})
    visibility = execution.get("accelerator_visibility") or {}
    scheduler = execution.get("scheduler") or {}
    lines = [
        "# Hardware Inspector report",
        "",
        "Generated: `{}`  ".format(report["generated_at_utc"]),
        "Privacy redaction: **{}**  ".format(
            "enabled" if privacy["redaction_enabled"] else "disabled"
        ),
        "Collector network requests: **none**",
        "",
        "## Summary",
        "",
        "| Field | Value |",
        "| --- | --- |",
        "| Operating system | {} |".format(_md(summary["operating_system"])),
        "| Architecture | {} |".format(_md(summary["architecture"])),
        "| Kernel | {} |".format(_md(summary["kernel_release"])),
        "| Board/model | {} |".format(_md(summary["board_model"])),
        "| Logical CPUs | {} |".format(_md(summary["logical_cpu_count"])),
        "| Memory | {} |".format(_human_bytes(summary["memory_bytes"])),
        "| CPU available to process | {} |".format(
            _md(execution.get("effective_cpu_cores"))
        ),
        "| Memory available to process | {} |".format(
            _human_bytes(execution.get("effective_memory_bytes"))
        ),
        "| Accelerator visibility | {} |".format(
            _md(
                json.dumps(visibility, sort_keys=True) if visibility else "not declared"
            )
        ),
        "| Scheduler/orchestrator | {} |".format(
            _md(json.dumps(scheduler, sort_keys=True) if scheduler else "not detected")
        ),
        "| Platform tags | {} |".format(_md(summary["platform_tags"])),
        "| Python | {} |".format(_md(summary["python_version"])),
        "",
        "## Probe results",
        "",
    ]

    missing: List[str] = []
    current_group = ""
    for probe in report["probes"]:
        if probe["status"] == "missing":
            missing.append("{}: {}".format(probe["group"], probe["name"]))
            continue
        if probe["group"] != current_group:
            current_group = probe["group"]
            lines.extend(["### {}".format(current_group.replace("-", " ").title()), ""])

        status = probe["status"]
        lines.append("<details>")
        lines.append(
            "<summary>{} — <code>{}</code></summary>".format(_md(probe["name"]), status)
        )
        lines.append("")
        if probe["kind"] == "command":
            lines.append("Command: `{}`  ".format(probe["command"].replace("`", "\\`")))
        else:
            lines.append("Source: `{}`  ".format(probe["source"]))
        lines.append("Duration: `{} ms`".format(probe["duration_ms"]))
        if probe["stdout"].strip():
            lines.extend(
                ["", "```text", probe["stdout"].replace("```", "` ` `").rstrip(), "```"]
            )
        if probe["stderr"].strip():
            lines.extend(
                [
                    "",
                    "Standard error:",
                    "",
                    "```text",
                    probe["stderr"].replace("```", "` ` `").rstrip(),
                    "```",
                ]
            )
        lines.extend(["", "</details>", ""])

    lines.extend(["## Unavailable optional probes", ""])
    if missing:
        lines.extend("- " + item for item in missing)
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "> Missing probes mean that the corresponding operating-system tool was not installed or the source did not exist. They do not prove that the hardware is absent.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a read-only hardware, driver, and accelerator report."
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument(
        "--output", type=Path, help="Write the report to this file instead of stdout."
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Include slower peripheral and ML framework probes; frameworks may initialize accelerators.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=8.0,
        help="Default command timeout in seconds (default: 8).",
    )
    parser.add_argument(
        "--no-redact",
        action="store_true",
        help="Include identifying values. Review before sharing.",
    )
    parser.add_argument("--version", action="version", version="%(prog)s " + VERSION)
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")
    return args


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    report = collect_report(
        full=args.full, timeout=args.timeout, redact=not args.no_redact
    )
    if args.format == "json":
        rendered = (
            json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
        )
    else:
        rendered = render_markdown(report)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
