#!/usr/bin/env python3
"""
跨平台环境检测模块 (v2.0 — unified edition)

合并 knowledge-engineering 与 make-to-markdown 的检测能力为单一共享版本。
启动时检测 OS / 版本 / 架构 / 可用能力，按平台选择执行路径。
各脚本在 import 后调用 platform_info = detect() 即可获得统一检测结果。

设计原则: 零外部依赖，纯标准库，Windows/Linux/macOS 全覆盖。
"""

import os
import sys
import platform
import shutil
import subprocess
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Dict, List


@dataclass
class PlatformInfo:
    """统一平台检测结果（KE + MTM 字段合并）"""
    # 基础信息
    os_name: str
    os_version: str
    arch: str
    python_version: str
    is_windows: bool
    is_linux: bool
    is_macos: bool
    is_wsl: bool

    # 包管理器
    has_pip: bool
    has_uv: bool

    # 语言模型 / 嵌入（KE 域）
    has_sentence_transformers: bool

    # 办公软件（MTM 域）
    has_office_com: bool          # Word/PowerPoint COM 自动化可用（仅 Windows）
    has_libreoffice: bool         # LibreOffice 命令行可用
    soffice_path: Optional[str] = None
    libreoffice_candidates: List[str] = field(default_factory=list)

    # 其它
    shell_type: str = ""
    warnings: List[str] = field(default_factory=list)

    def __repr__(self):
        return (f"PlatformInfo(os={self.os_name} {self.os_version}, "
                f"arch={self.arch}, py={self.python_version}, "
                f"wsl={self.is_wsl}, pip={self.has_pip}, "
                f"sbert={self.has_sentence_transformers}, "
                f"com={self.has_office_com}, lo={self.has_libreoffice})")


# ──────────────────────────── 检测函数 ────────────────────────────

def _detect_os() -> tuple:
    """检测 OS 基础信息"""
    system = platform.system()
    is_wsl = False

    if system == "Windows":
        os_name = "Windows"
        try:
            build = int(platform.version().split('.')[-1]) if platform.version() else 0
            win_ver = platform.release()
            if win_ver == "10" and build >= 22000:
                os_version = f"Windows 11 (Build {build})"
            else:
                os_version = f"Windows {win_ver} (Build {build})" if build else f"Windows {win_ver}"
        except Exception:
            os_version = f"Windows {platform.release()}"
    elif system == "Linux":
        try:
            with open("/proc/version", "r") as f:
                if "microsoft" in f.read().lower() or "wsl" in f.read().lower():
                    is_wsl = True
        except Exception:
            pass
        os_name = "Linux"
        try:
            result = subprocess.run(
                ["lsb_release", "-ds"], capture_output=True, text=True, timeout=5
            )
            os_version = result.stdout.strip().strip('"')
        except Exception:
            try:
                with open("/etc/os-release") as f:
                    for line in f:
                        if line.startswith("PRETTY_NAME="):
                            os_version = line.split("=", 1)[1].strip().strip('"')
                            break
                    else:
                        os_version = f"Linux {platform.release()}"
            except Exception:
                os_version = f"Linux {platform.release()}"
    elif system == "Darwin":
        os_name = "macOS"
        try:
            result = subprocess.run(["sw_vers", "-productVersion"], capture_output=True, text=True, timeout=5)
            os_version = f"macOS {result.stdout.strip()}"
        except Exception:
            os_version = f"macOS {platform.release()}"
    else:
        os_name = system
        os_version = platform.release()

    return os_name, os_version, is_wsl


def _detect_arch() -> str:
    """检测 CPU 架构"""
    machine = platform.machine().lower()
    mapping = {
        "amd64": "AMD64", "x86_64": "AMD64",
        "arm64": "ARM64", "aarch64": "ARM64",
        "x86": "x86", "i386": "x86", "i686": "x86",
    }
    return mapping.get(machine, machine.upper())


def _detect_libreoffice() -> tuple:
    """检测 LibreOffice 可用性及路径"""
    warnings = []
    candidates = []

    soffice_path = shutil.which("soffice")
    if soffice_path:
        candidates.append(soffice_path)

    env_path = os.environ.get("SOFFICE_PATH")
    if env_path and os.path.exists(env_path) and env_path not in candidates:
        candidates.append(env_path)

    if sys.platform == "win32":
        common = [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        ]
    else:
        common = [
            "/usr/bin/soffice",
            "/usr/lib/libreoffice/program/soffice",
            "/usr/lib64/libreoffice/program/soffice",
            "/opt/libreoffice/program/soffice",
            "/snap/bin/libreoffice.soffice",
        ]
    for p in common:
        if os.path.exists(p) and p not in candidates:
            candidates.append(p)

    has_lo = bool(candidates) and any(
        os.path.exists(p) or shutil.which(p) for p in candidates
    )

    if not has_lo:
        warnings.append(
            "LibreOffice 未安装。.doc / .ppt 旧格式转换将不可用。"
            "安装: Windows → https://libreoffice.org/download ; "
            "Linux → sudo apt install libreoffice; macOS → brew install libreoffice"
        )

    return has_lo, soffice_path or candidates[0] if candidates else None, candidates, warnings


def _detect_office_com() -> bool:
    """检测 Office COM 自动化是否可用（仅 Windows）"""
    if sys.platform != "win32":
        return False
    try:
        import pythoncom
        import win32com.client
        pythoncom.CoInitialize()
        try:
            app = win32com.client.Dispatch("Word.Application")
            app.Quit()
            return True
        except Exception:
            return False
        finally:
            pythoncom.CoUninitialize()
    except ImportError:
        return False


def _detect_package_managers() -> tuple:
    """检测包管理器可用性"""
    has_pip = shutil.which("pip") is not None or shutil.which("pip3") is not None
    has_uv = shutil.which("uv") is not None
    return has_pip, has_uv


def _detect_sentence_transformers() -> bool:
    """检测 sentence-transformers 是否已安装（KE 域）"""
    try:
        import sentence_transformers
        return True
    except ImportError:
        return False


def _detect_shell() -> str:
    """检测当前 Shell 类型"""
    if sys.platform == "win32":
        if "PSModulePath" in os.environ or "POWERSHELL" in os.environ.get("SHELL", "").upper():
            return "powershell"
        return "cmd"
    else:
        shell = os.environ.get("SHELL", "")
        if "zsh" in shell:
            return "zsh"
        if "bash" in shell:
            return "bash"
        return shell or "bash"


# ──────────────────────────── 主入口 ────────────────────────────

def detect(verbose: bool = False) -> PlatformInfo:
    """执行完整平台检测，返回 PlatformInfo 对象。"""
    os_name, os_version, is_wsl = _detect_os()
    arch = _detect_arch()
    has_pip, has_uv = _detect_package_managers()
    has_sbert = _detect_sentence_transformers()
    has_lo, soffice, lo_candidates, lo_warnings = _detect_libreoffice()
    has_com = _detect_office_com()
    shell = _detect_shell()
    warnings = list(lo_warnings)

    if not has_sbert and has_pip:
        warnings.append(
            "sentence-transformers 未安装。将使用 PurePythonEmbedder 降级方案。"
            "如需提升评估精度，请执行: pip install sentence-transformers"
        )

    info = PlatformInfo(
        os_name=os_name,
        os_version=os_version,
        arch=arch,
        python_version=platform.python_version(),
        is_windows=(os_name == "Windows"),
        is_linux=(os_name == "Linux"),
        is_macos=(os_name == "macOS"),
        is_wsl=is_wsl,
        has_pip=has_pip,
        has_uv=has_uv,
        has_sentence_transformers=has_sbert,
        has_office_com=has_com,
        has_libreoffice=has_lo,
        soffice_path=soffice,
        libreoffice_candidates=lo_candidates,
        shell_type=shell,
        warnings=warnings,
    )

    if verbose:
        _print_info(info)

    return info


def _print_info(info: PlatformInfo):
    """打印可读的平台检测报告"""
    print(f"\n{'='*60}")
    print(f"  平台检测报告")
    print(f"{'='*60}")
    print(f"  OS       : {info.os_name} {info.os_version}")
    print(f"  Arch     : {info.arch}")
    print(f"  Python   : {info.python_version}")
    print(f"  Shell    : {info.shell_type}")
    print(f"  WSL      : {'Yes' if info.is_wsl else 'No'}")
    print(f"  SBERT    : {'已安装' if info.has_sentence_transformers else '未安装 (将降级到 PurePythonEmbedder)'}")
    print(f"  Office   : {'COM 可用' if info.has_office_com else 'COM 不可用' if info.is_windows else 'N/A (非Win)'}")
    print(f"  LibreOff : {'可用' if info.has_libreoffice else '未安装'} "
          f"{'→ ' + info.soffice_path if info.soffice_path else ''}")
    print(f"  pip      : {'可用' if info.has_pip else '未找到'}")
    print(f"  uv       : {'可用' if info.has_uv else '未找到'}")
    if info.warnings:
        print(f"\n  ⚠ 警告:")
        for w in info.warnings:
            print(f"    - {w}")
    print(f"{'='*60}\n")


# ──────────────────────────── 便捷函数 ────────────────────────────

def best_office_tool(info: PlatformInfo) -> str:
    """根据平台选择最佳 Office 文档处理工具。
    返回: "com" | "libreoffice" | "none"
    """
    if info.is_windows and info.has_office_com:
        return "com"
    if info.has_libreoffice:
        return "libreoffice"
    return "none"


def run_cmd(cmd: List[str], info: PlatformInfo, **kwargs) -> subprocess.CompletedProcess:
    """跨平台命令执行包装器。自动处理 Windows 下的 shell=True 和 encoding。"""
    if info.is_windows:
        kwargs.setdefault("shell", True)
        kwargs.setdefault("encoding", "utf-8")
    return subprocess.run(cmd, **kwargs)


# ── 模块自测 ──
if __name__ == "__main__":
    detect(verbose=True)
