"""hardware_id.py — 稳定、不可逆、硬件绑定的机器标识 (ct-base §8.6 升级).

替代旧的 ``sha256(socket.gethostname())``：主机名不是硬件，在容器 / 云端环境
会随会话或账号变化，导致「同机换账号 / 网页版」SHA 不稳定，且可被改、可重名。

本模块读取真实硬件令牌，按回退链取第一个可用的，再 sha256：

  Windows:  SMBIOS UUID (Win32_ComputerSystemProduct.UUID，主板级，
            换 Windows 账号 / 改主机名 / 重装系统都不变) → 注册表 MachineGuid
  macOS:    IOPlatformUUID (ioreg)
  Linux:    /etc/machine-id (或 /var/lib/dbus/machine-id)
  兜底:     主机名（仅当上述全部失败，保证永不崩）

返回格式保持 ``"sha256:<64 hex>"``，与旧 query_origin 契约完全兼容。

重要边界（务必知悉）：
  - 本机硬件绑定只在「本地桌面端」真正生效——同一台物理电脑，无论切哪个
    Windows 账号、改不改主机名，输出固定。
  - 网页 / 云端版本若把 Python 跑在服务器或临时容器里，服务端代码读不到你
    本机硬件，只能读到「服务端硬件」；临时容器每次重建 machine-id 仍会变。
    那种环境无法做到「同机固定」，只能退而求其次（绑部署实例或账号）。
"""
from __future__ import annotations

import hashlib
import socket
import subprocess
import sys


def _raw_hw_token() -> str:
    """返回未哈希的硬件令牌字符串；任一来源失败即回退到下一项，最后兜底主机名。"""
    # Windows
    if sys.platform.startswith("win"):
        # 1) SMBIOS UUID（最硬，主板级，跨账号 / 主机名 / 重装都不变）
        try:
            out = subprocess.check_output(
                [r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
                 "-NoProfile", "-Command",
                 "(Get-CimInstance Win32_ComputerSystemProduct).UUID"],
                stderr=subprocess.DEVNULL, text=True, timeout=10)
            s = out.strip()
            if s and s.upper() not in ("UUID", "FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF"):
                return "win:smbios:" + s
        except Exception:
            pass
        # 2) 注册表 MachineGuid（跨账号 / 主机名稳定，仅重装系统变）
        try:
            import winreg
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Cryptography",
            ) as k:
                return "win:machineguid:" + winreg.QueryValueEx(k, "MachineGuid")[0]
        except Exception:
            pass
    # macOS
    elif sys.platform == "darwin":
        try:
            out = subprocess.check_output(
                ["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"],
                stderr=subprocess.DEVNULL, text=True, timeout=10)
            for line in out.splitlines():
                if "IOPlatformUUID" in line:
                    # 形如:   "IOPlatformUUID" = "XXXXXXXX-XXXX-..."
                    parts = line.split('"')
                    if len(parts) >= 4 and parts[3].strip():
                        return "mac:platformuuid:" + parts[3].strip()
        except Exception:
            pass
    # Linux（及其他类 Unix）
    else:
        for p in ("/etc/machine-id", "/var/lib/dbus/machine-id"):
            try:
                with open(p, encoding="utf-8") as f:
                    s = f.read().strip()
                if s:
                    return "linux:machine-id:" + s
            except Exception:
                pass
    # 兜底：主机名（旧行为；容器里仍会变，但保证永不抛异常）
    try:
        return "host:" + socket.gethostname()
    except Exception:
        return "host:unknown"


def hardware_id() -> str:
    """返回稳定、不可逆、硬件绑定的机器标识：``"sha256:<64 hex>"``。"""
    return "sha256:" + hashlib.sha256(_raw_hw_token().encode("utf-8")).hexdigest()


if __name__ == "__main__":
    print(hardware_id())
