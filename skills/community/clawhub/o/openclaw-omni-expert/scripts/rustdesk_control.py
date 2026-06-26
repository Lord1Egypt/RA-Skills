#!/usr/bin/env python3
"""
RustDesk 远程控制模块
支持 RustDesk CLI 连接和基础操作
"""

import os
import subprocess
import time
import argparse
import json
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any


class RustDeskController:
    """RustDesk 远程控制器"""
    
    def __init__(
        self,
        remote_id: Optional[str] = None,
        host: Optional[str] = None,
        port: int = 21117,
        relay: Optional[str] = None,
        screenshot_dir: str = "./screenshots"
    ):
        """
        Args:
            remote_id: 远程设备 ID (如 12345-abcdef-67890)
            host: 主机地址 (当 remote_id 为空时使用)
            port: RustDesk 端口
            relay: 中继服务器地址
            screenshot_dir: 截图保存目录
        """
        self.remote_id = remote_id
        self.host = host
        self.port = port
        self.relay = relay
        self.screenshot_dir = Path(screenshot_dir)
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        self.connected = False
        self.process = None
    
    def check_installed(self) -> bool:
        """检查 RustDesk 是否已安装"""
        # Windows 常见安装路径
        paths = [
            r"C:\Program Files\RustDesk\RustDesk.exe",
            r"C:\Program Files (x86)\RustDesk\RustDesk.exe",
            os.path.expanduser(r"~\AppData\Local\RustDesk\RustDesk.exe"),
            "rustdesk",  # PATH 中的命令
        ]
        
        for path in paths:
            if os.path.exists(path) if not os.path.isabs(path) or os.path.exists(path):
                self.exe_path = path if os.path.isabs(path) else path
                return True
        
        # 尝试命令检查
        try:
            result = subprocess.run(
                ["rustdesk", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 or "RustDesk" in result.stdout:
                self.exe_path = "rustdesk"
                return True
        except:
            pass
        
        return False
    
    def get_id(self, password: Optional[str] = None) -> Optional[str]:
        """获取本机 RustDesk ID"""
        try:
            cmd = ["rustdesk", "--get-id"]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception as e:
            print(f"获取 ID 失败: {e}")
        return None
    
    def get_password(self) -> Optional[str]:
        """获取本机 RustDesk 密码（需要配置文件中读取）"""
        config_paths = [
            Path(os.environ.get("APPDATA", "")) / "RustDesk" / "config.toml",
            Path.home() / ".rustdesk" / "config.toml",
        ]
        
        for config_path in config_paths:
            if config_path.exists():
                try:
                    content = config_path.read_text()
                    for line in content.split("\n"):
                        if "password" in line.lower() and "=" in line:
                            return line.split("=")[1].strip().strip('"')
                except:
                    pass
        return None
    
    def connect(self, password: Optional[str] = None, timeout: int = 30) -> bool:
        """连接远程"""
        if not self.check_installed():
            print("RustDesk 未安装")
            return False
        
        if not self.remote_id and not self.host:
            print("需要提供 remote_id 或 host")
            return False
        
        # 构建连接命令
        if self.remote_id:
            target = self.remote_id
        else:
            target = f"{self.host}:{self.port}" if self.host else ""
        
        cmd = [self.exe_path, target]
        
        # 添加密码
        if password:
            cmd.extend(["--password", password])
        
        # 添加中继服务器
        if self.relay:
            cmd.extend(["--relay", self.relay])
        
        try:
            # RustDesk GUI 模式启动
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # 等待连接建立
            time.sleep(2)
            
            # 检查进程状态
            if self.process.poll() is None:
                self.connected = True
                return True
            else:
                stdout, stderr = self.process.communicate()
                print(f"连接失败: {stderr.decode() if stderr else stdout.decode()}")
                return False
                
        except Exception as e:
            print(f"连接异常: {e}")
            return False
    
    def disconnect(self) -> bool:
        """断开连接"""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
                self.connected = False
                return True
            except:
                self.process.kill()
                self.connected = False
        return True
    
    def exec_command(self, command: str, timeout: int = 60) -> Tuple[bool, str]:
        """
        执行远程命令（通过其他方式，如 SSH）
        注意：RustDesk 本身不直接支持命令执行，需要配合其他方式
        """
        # 尝试通过 SSH 执行（假设目标机器也开启了 SSH）
        if self.host:
            try:
                result = subprocess.run(
                    ["ssh", f"user@{self.host}", command],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                return result.returncode == 0, result.stdout
            except Exception as e:
                return False, str(e)
        
        return False, "需要配置 host 才能执行命令"
    
    def screenshot(self, filename: Optional[str] = None) -> Optional[str]:
        """
        截图（需要远程执行截图命令）
        """
        if not self.host:
            print("需要配置 host 才能截图")
            return None
        
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        output_path = self.screenshot_dir / filename
        
        # 通过 SSH 执行截图命令（Windows）
        ps_script = '''
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$screens = [System.Windows.Forms.Screen]::AllScreens
$bmp = New-Object System.Drawing.Bitmap($screens[0].Bounds.Width, $screens[0].Bounds.Height)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.CopyFromScreen($screens[0].Bounds.Location, [System.Drawing.Point]::Empty, $screens[0].Bounds.Size)
$bmp.Save(@("{path}") -f $env:TEMP + "\\screenshot.png")
$g.Dispose()
$bmp.Dispose()
Write-Output "$env:TEMP\\screenshot.png"
'''.format(path=str(output_path).replace("\\", "\\\\"))
        
        try:
            # 执行 PowerShell 脚本
            result = subprocess.run(
                ["ssh", f"user@{self.host}", f"powershell -Command \"{ps_script}\""],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                remote_path = result.stdout.strip()
                # 下载截图
                subprocess.run(
                    ["scp", f"user@{self.host}:{remote_path}", str(output_path)],
                    timeout=30
                )
                if output_path.exists():
                    return str(output_path)
                    
        except Exception as e:
            print(f"截图失败: {e}")
        
        return None
    
    def transfer_file(self, local_path: str, remote_path: str) -> bool:
        """传输文件到远程"""
        if not self.host:
            print("需要配置 host 才能传输文件")
            return False
        
        try:
            result = subprocess.run(
                ["scp", local_path, f"user@{self.host}:{remote_path}"],
                capture_output=True,
                timeout=300
            )
            return result.returncode == 0
        except Exception as e:
            print(f"文件传输失败: {e}")
            return False
    
    def download_file(self, remote_path: str, local_path: str) -> bool:
        """从远程下载文件"""
        if not self.host:
            print("需要配置 host 才能下载文件")
            return False
        
        try:
            result = subprocess.run(
                ["scp", f"user@{self.host}:{remote_path}", local_path],
                capture_output=True,
                timeout=300
            )
            return result.returncode == 0
        except Exception as e:
            print(f"文件下载失败: {e}")
            return False
    
    def start_service(self) -> bool:
        """启动 RustDesk 服务"""
        try:
            result = subprocess.run(
                [self.exe_path, "--service"],
                capture_output=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False
    
    def set_password(self, password: str) -> bool:
        """设置连接密码"""
        config_path = Path(os.environ.get("APPDATA", "")) / "RustDesk" / "config.toml"
        
        try:
            if not config_path.exists():
                config_path.parent.mkdir(parents=True, exist_ok=True)
                config_path.write_text("")
            
            # 追加密码配置
            with open(config_path, "a") as f:
                f.write(f'\npassword = "{password}"\n')
            return True
        except Exception as e:
            print(f"设置密码失败: {e}")
            return False
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        return False


def setup_relay_server(relay_url: str) -> bool:
    """
    配置自建中继服务器
    """
    config_path = Path(os.environ.get("APPDATA", "")) / "RustDesk" / "config.toml"
    
    try:
        content = config_path.read_text() if config_path.exists() else ""
        
        # 添加或更新 relay 配置
        if "relay" in content:
            content = "\n".join([
                line for line in content.split("\n")
                if "relay" not in line.lower()
            ])
        
        content += f'\nrelay = "{relay_url}"\n'
        
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(content)
        
        print(f"已配置中继服务器: {relay_url}")
        return True
    except Exception as e:
        print(f"配置失败: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RustDesk 远程控制器")
    parser.add_argument("--id", help="远程设备 ID")
    parser.add_argument("--host", help="主机地址")
    parser.add_argument("--port", type=int, default=21117, help="端口")
    parser.add_argument("--password", help="连接密码")
    parser.add_argument("--relay", help="中继服务器")
    parser.add_argument("--get-id", action="store_true", help="获取本机 ID")
    parser.add_argument("--screenshot", "-s", help="截图保存路径")
    parser.add_argument("--exec", "-c", help="执行命令（需 SSH）")
    parser.add_argument("--upload", nargs=2, metavar=("local", "remote"), help="上传文件")
    parser.add_argument("--download", nargs=2, metavar=("remote", "local"), help="下载文件")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    
    args = parser.parse_args()
    
    if args.get_id:
        controller = RustDeskController()
        print(f"本机 ID: {controller.get_id()}")
    
    elif args.interactive:
        print("=" * 60)
        print("RustDesk 远程控制 - 交互模式")
        print("=" * 60)
        
        remote_id = input("远程设备 ID (留空输入 host): ").strip()
        host = None
        
        if not remote_id:
            host = input("主机地址: ").strip()
            port = input("端口 [21117]: ").strip() or "21117"
        
        controller = RustDeskController(
            remote_id=remote_id or None,
            host=host,
            port=int(port) if host else 21117
        )
        
        print("\n连接中...")
        if controller.connect(args.password):
            print("连接成功!")
            
            while True:
                cmd = input("\nrd> ").strip()
                if cmd in ["quit", "exit", "q"]:
                    break
                if cmd == "screenshot":
                    path = controller.screenshot()
                    print(f"截图: {path}")
                elif cmd.startswith("exec "):
                    _, result = controller.exec_command(cmd[5:])
                    print(result)
                else:
                    print("可用命令: screenshot, exec <cmd>, quit")
            
            controller.disconnect()
        else:
            print("连接失败!")
    
    elif args.screenshot:
        controller = RustDeskController(host=args.host)
        path = controller.screenshot(args.screenshot)
        print(f"截图: {path}")
    
    elif args.exec:
        controller = RustDeskController(host=args.host)
        success, output = controller.exec_command(args.exec)
        print(output if success else f"错误: {output}")
    
    elif args.upload:
        controller = RustDeskController(host=args.host)
        success = controller.transfer_file(args.upload[0], args.upload[1])
        print("上传成功!" if success else "上传失败")
    
    elif args.download:
        controller = RustDeskController(host=args.host)
        success = controller.download_file(args.download[0], args.download[1])
        print("下载成功!" if success else "下载失败")
    
    else:
        # 连接模式
        controller = RustDeskController(
            remote_id=args.id,
            host=args.host,
            port=args.port,
            relay=args.relay
        )
        
        if controller.connect(args.password):
            print("连接成功! (RustDesk 窗口已打开)")
            input("按 Enter 断开连接...")
            controller.disconnect()
