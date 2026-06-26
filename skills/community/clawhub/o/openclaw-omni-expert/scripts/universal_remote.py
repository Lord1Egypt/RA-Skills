#!/usr/bin/env python3
"""
通用远程控制接口
统一管理多种远程软件：UU远程、RustDesk、ToDesk、向日葵、RDP
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass, field
from enum import Enum


class RemoteSoftware(Enum):
    """支持的远程软件"""
    UU = "uu"
    RUSTDESK = "rustdesk"
    TODESK = "todesk"
    SUNLOGIN = "sunlogin"
    RDP = "rdp"
    WINRM = "winrm"
    UNKNOWN = "unknown"


@dataclass
class ConnectionInfo:
    """连接信息"""
    software: RemoteSoftware
    session_id: Optional[str] = None
    host: Optional[str] = None
    port: int = 0
    username: Optional[str] = None
    password: Optional[str] = None
    remote_id: Optional[str] = None
    relay: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AutomationCapability:
    """自动化能力"""
    mouse_control: bool = False
    keyboard_control: bool = False
    screenshot: bool = False
    file_transfer: bool = False
    command_exec: bool = False
    clipboard: bool = False
    vision_support: bool = False


class UniversalRemoteController:
    """
    通用远程控制器
    支持多种远程软件，统一接口
    """
    
    def __init__(self, connection: ConnectionInfo):
        self.connection = connection
        self.connected = False
        self.automation = None
        self._init_software()
    
    def _init_software(self):
        """初始化对应的远程软件控制器"""
        if self.connection.software == RemoteSoftware.UU:
            from remote_desktop_control import UURemoteController
            self.controller = UURemoteController(
                session_id=self.connection.session_id,
                host=self.connection.host,
                port=self.connection.port,
                username=self.connection.username,
                password=self.connection.password
            )
            self.capability = AutomationCapability(
                mouse_control=True,
                keyboard_control=True,
                screenshot=True,
                file_transfer=True,
                command_exec=True,
                clipboard=True,
                vision_support=True
            )
            
        elif self.connection.software == RemoteSoftware.RUSTDESK:
            from rustdesk_control import RustDeskController
            self.controller = RustDeskController(
                remote_id=self.connection.remote_id,
                host=self.connection.host,
                port=self.connection.port,
                relay=self.connection.relay
            )
            self.capability = AutomationCapability(
                mouse_control=False,  # 需要配合其他工具
                keyboard_control=False,
                screenshot=True,
                file_transfer=True,
                command_exec=True,  # 需要 SSH
                clipboard=True,
                vision_support=True
            )
            
        elif self.connection.software == RemoteSoftware.TODESK:
            self.controller = self._ToDeskController(self.connection)
            self.capability = AutomationCapability(
                mouse_control=False,
                keyboard_control=False,
                screenshot=True,
                file_transfer=True,
                command_exec=False,
                clipboard=True,
                vision_support=True
            )
            
        elif self.connection.software == RemoteSoftware.SUNLOGIN:
            self.controller = self._SunloginController(self.connection)
            self.capability = AutomationCapability(
                mouse_control=False,
                keyboard_control=False,
                screenshot=True,
                file_transfer=True,
                command_exec=False,
                clipboard=True,
                vision_support=True
            )
            
        elif self.connection.software == RemoteSoftware.RDP:
            self.controller = self._RDPController(self.connection)
            self.capability = AutomationCapability(
                mouse_control=False,
                keyboard_control=False,
                screenshot=True,
                file_transfer=True,
                command_exec=True,
                clipboard=True,
                vision_support=True
            )
            
        elif self.connection.software == RemoteSoftware.WINRM:
            self.controller = self._WinRMController(self.connection)
            self.capability = AutomationCapability(
                mouse_control=False,
                keyboard_control=False,
                screenshot=False,
                file_transfer=True,
                command_exec=True,
                clipboard=True,
                vision_support=False
            )
        else:
            raise ValueError(f"不支持的远程软件: {self.connection.software}")
    
    def connect(self) -> bool:
        """建立连接"""
        if hasattr(self.controller, 'connect'):
            return self.controller.connect()
        return False
    
    def disconnect(self):
        """断开连接"""
        if hasattr(self.controller, 'disconnect'):
            self.controller.disconnect()
    
    def screenshot(self, path: Optional[str] = None) -> Optional[str]:
        """截图"""
        if hasattr(self.controller, 'screenshot'):
            return self.controller.screenshot(path)
        return None
    
    def exec_command(self, command: str, timeout: int = 60) -> tuple:
        """执行命令"""
        if hasattr(self.controller, 'exec_command'):
            return self.controller.exec_command(command, timeout)
        return False, "不支持命令执行"
    
    def transfer_file(self, local: str, remote: str) -> bool:
        """上传文件"""
        if hasattr(self.controller, 'transfer_file'):
            return self.controller.transfer_file(local, remote)
        return False
    
    def download_file(self, remote: str, local: str) -> bool:
        """下载文件"""
        if hasattr(self.controller, 'download_file'):
            return self.controller.download_file(remote, local)
        return False
    
    # ========== 内部控制器实现 ==========
    
    class _ToDeskController:
        """ToDesk 控制器"""
        def __init__(self, conn: ConnectionInfo):
            self.conn = conn
        
        def connect(self) -> bool:
            import subprocess
            try:
                cmd = ["todesk", "-c", self.conn.session_id or self.conn.host]
                if self.conn.password:
                    cmd.extend(["-p", self.conn.password])
                subprocess.Popen(cmd)
                time.sleep(2)
                return True
            except Exception as e:
                print(f"ToDesk 连接失败: {e}")
                return False
        
        def disconnect(self):
            import subprocess
            subprocess.run(["todesk", "-q"])
        
        def screenshot(self, path: str = None) -> Optional[str]:
            # ToDesk 截图需要通过 GUI
            return None
        
        def transfer_file(self, local: str, remote: str) -> bool:
            import subprocess
            try:
                result = subprocess.run(
                    ["todesk", "-transfer", local, remote],
                    capture_output=True,
                    timeout=60
                )
                return result.returncode == 0
            except:
                return False
    
    class _SunloginController:
        """向日葵控制器"""
        def __init__(self, conn: ConnectionInfo):
            self.conn = conn
        
        def connect(self) -> bool:
            import subprocess
            try:
                cmd = ["sunlogin", "--control"]
                if self.conn.host:
                    cmd.append(self.conn.host)
                if self.conn.password:
                    cmd.extend(["--pwd", self.conn.password])
                subprocess.Popen(cmd)
                time.sleep(2)
                return True
            except Exception as e:
                print(f"向日葵连接失败: {e}")
                return False
        
        def disconnect(self):
            import subprocess
            subprocess.run(["sunlogin", "--quit"])
        
        def screenshot(self, path: str = None) -> Optional[str]:
            return None
        
        def transfer_file(self, local: str, remote: str) -> bool:
            import subprocess
            try:
                result = subprocess.run(
                    ["sunlogin", "--file", local, remote],
                    capture_output=True,
                    timeout=60
                )
                return result.returncode == 0
            except:
                return False
    
    class _RDPController:
        """RDP 控制器"""
        def __init__(self, conn: ConnectionInfo):
            self.conn = conn
        
        def connect(self) -> bool:
            import subprocess
            try:
                cmd = ["mstsc", "/v:" + (self.conn.host or self.conn.session_id)]
                subprocess.Popen(cmd)
                return True
            except Exception as e:
                print(f"RDP 连接失败: {e}")
                return False
        
        def disconnect(self):
            import subprocess
            subprocess.run(["qwinsta"], capture_output=True)
        
        def exec_command(self, command: str, timeout: int = 60) -> tuple:
            import subprocess
            # RDP 需要配合 PsExec 或 SSH 执行命令
            try:
                result = subprocess.run(
                    ["ssh", f"{self.conn.username}@{self.conn.host}", command],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                return result.returncode == 0, result.stdout
            except Exception as e:
                return False, str(e)
        
        def screenshot(self, path: str = None) -> Optional[str]:
            return None
    
    class _WinRMController:
        """WinRM 控制器"""
        def __init__(self, conn: ConnectionInfo):
            self.conn = conn
        
        def connect(self) -> bool:
            # WinRM 无需显式连接
            return True
        
        def disconnect(self):
            pass
        
        def exec_command(self, command: str, timeout: int = 60) -> tuple:
            import subprocess
            try:
                # 构建 WinRM 命令
                # winrm 需要配置，可使用 pywinrm 库
                cmd = [
                    "powershell",
                    "-Command",
                    f"Invoke-Command -ComputerName {self.conn.host} -Credential (Get-Credential) -ScriptBlock {{{command}}}"
                ]
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                return result.returncode == 0, result.stdout
            except Exception as e:
                return False, str(e)
        
        def transfer_file(self, local: str, remote: str) -> bool:
            import subprocess
            try:
                cmd = [
                    "powershell",
                    "-Command",
                    f"Copy-Item -Path '{local}' -Destination '\\\\{self.conn.host}\\{remote}'"
                ]
                result = subprocess.run(cmd, capture_output=True, timeout=120)
                return result.returncode == 0
            except:
                return False
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        return False


class RemoteSoftwareDetector:
    """检测远程软件"""
    
    @staticmethod
    def detect() -> List[RemoteSoftware]:
        """检测已安装的远程软件"""
        detected = []
        
        # UU
        try:
            import subprocess
            result = subprocess.run(["uu", "--version"], capture_output=True, timeout=5)
            if result.returncode == 0:
                detected.append(RemoteSoftware.UU)
        except:
            pass
        
        # RustDesk
        try:
            result = subprocess.run(["rustdesk", "--version"], capture_output=True, timeout=5)
            if result.returncode == 0 or "RustDesk" in result.stdout.decode():
                detected.append(RemoteSoftware.RUSTDESK)
        except:
            pass
        
        # ToDesk
        try:
            result = subprocess.run(["todesk", "-v"], capture_output=True, timeout=5)
            if result.returncode == 0:
                detected.append(RemoteSoftware.TODESK)
        except:
            pass
        
        # 向日葵
        try:
            result = subprocess.run(["sunlogin", "--version"], capture_output=True, timeout=5)
            if result.returncode == 0:
                detected.append(RemoteSoftware.SUNLOGIN)
        except:
            pass
        
        # RDP (始终可用)
        detected.append(RemoteSoftware.RDP)
        
        return detected
    
    @staticmethod
    def get_capability(software: RemoteSoftware) -> AutomationCapability:
        """获取软件自动化能力"""
        capabilities = {
            RemoteSoftware.UU: AutomationCapability(
                mouse_control=True, keyboard_control=True,
                screenshot=True, file_transfer=True,
                command_exec=True, clipboard=True, vision_support=True
            ),
            RemoteSoftware.RUSTDESK: AutomationCapability(
                mouse_control=False, keyboard_control=False,
                screenshot=True, file_transfer=True,
                command_exec=True, clipboard=True, vision_support=True
            ),
            RemoteSoftware.TODESK: AutomationCapability(
                mouse_control=False, keyboard_control=False,
                screenshot=True, file_transfer=True,
                command_exec=False, clipboard=True, vision_support=True
            ),
            RemoteSoftware.SUNLOGIN: AutomationCapability(
                mouse_control=False, keyboard_control=False,
                screenshot=True, file_transfer=True,
                command_exec=False, clipboard=True, vision_support=True
            ),
            RemoteSoftware.RDP: AutomationCapability(
                mouse_control=False, keyboard_control=False,
                screenshot=True, file_transfer=True,
                command_exec=True, clipboard=True, vision_support=True
            ),
            RemoteSoftware.WINRM: AutomationCapability(
                mouse_control=False, keyboard_control=False,
                screenshot=False, file_transfer=True,
                command_exec=True, clipboard=True, vision_support=False
            ),
        }
        return capabilities.get(software, AutomationCapability())


def create_connection(software: str, **kwargs) -> ConnectionInfo:
    """创建连接信息"""
    software_map = {
        "uu": RemoteSoftware.UU,
        "rustdesk": RemoteSoftware.RUSTDESK,
        "todesk": RemoteSoftware.TODESK,
        "sunlogin": RemoteSoftware.SUNLOGIN,
        "向日葵": RemoteSoftware.SUNLOGIN,
        "rdp": RemoteSoftware.RDP,
        "winrm": RemoteSoftware.WINRM,
    }
    
    return ConnectionInfo(
        software=software_map.get(software.lower(), RemoteSoftware.UNKNOWN),
        **kwargs
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="通用远程控制器")
    parser.add_argument("--software", "-s", 
                       choices=["uu", "rustdesk", "todesk", "sunlogin", "rdp", "winrm"],
                       help="远程软件类型")
    parser.add_argument("--session-id", help="Session ID")
    parser.add_argument("--host", help="主机地址")
    parser.add_argument("--port", type=int, help="端口")
    parser.add_argument("--username", help="用户名")
    parser.add_argument("--password", help="密码")
    parser.add_argument("--remote-id", help="远程 ID (RustDesk)")
    parser.add_argument("--detect", "-d", action="store_true", help="检测已安装软件")
    parser.add_argument("--capability", "-c", help="查看软件能力")
    
    args = parser.parse_args()
    
    if args.detect:
        print("检测已安装的远程软件...")
        detected = RemoteSoftwareDetector.detect()
        if detected:
            print("已安装:")
            for s in detected:
                cap = RemoteSoftwareDetector.get_capability(s)
                print(f"  - {s.value}")
                print(f"    鼠标控制: {'✓' if cap.mouse_control else '✗'}")
                print(f"    键盘控制: {'✓' if cap.keyboard_control else '✗'}")
                print(f"    截图: {'✓' if cap.screenshot else '✗'}")
                print(f"    文件传输: {'✓' if cap.file_transfer else '✗'}")
                print(f"    命令执行: {'✓' if cap.command_exec else '✗'}")
                print(f"    视觉识别: {'✓' if cap.vision_support else '✗'}")
        else:
            print("未检测到支持的远程软件")
    
    elif args.capability:
        software = RemoteSoftware(args.capability)
        cap = RemoteSoftwareDetector.get_capability(software)
        print(f"{args.capability} 自动化能力:")
        print(f"  鼠标控制: {'支持' if cap.mouse_control else '不支持'}")
        print(f"  键盘控制: {'支持' if cap.keyboard_control else '不支持'}")
        print(f"  截图: {'支持' if cap.screenshot else '不支持'}")
        print(f"  文件传输: {'支持' if cap.file_transfer else '不支持'}")
        print(f"  命令执行: {'支持' if cap.command_exec else '不支持'}")
        print(f"  视觉识别: {'支持' if cap.vision_support else '不支持'}")
    
    elif args.software:
        conn = create_connection(
            args.software,
            session_id=args.session_id,
            host=args.host,
            port=args.port or 0,
            username=args.username,
            password=args.password,
            remote_id=args.remote_id
        )
        
        controller = UniversalRemoteController(conn)
        
        print(f"连接到 {args.software}...")
        if controller.connect():
            print("连接成功!")
            
            # 显示能力
            cap = controller.capability
            print(f"\n可用功能:")
            if cap.screenshot:
                print("  - 截图 (screenshot)")
            if cap.file_transfer:
                print("  - 文件传输 (transfer_file)")
            if cap.command_exec:
                print("  - 命令执行 (exec_command)")
            
            input("\n按 Enter 断开...")
            controller.disconnect()
        else:
            print("连接失败!")
    
    else:
        # 显示帮助
        print("通用远程控制器")
        print("=" * 50)
        print("\n用法:")
        print("  检测已安装: --detect")
        print("  查看能力: --capability <software>")
        print("  连接: --software <type> --host <addr>")
        print("\n支持的软件: uu, rustdesk, todesk, sunlogin, rdp, winrm")
