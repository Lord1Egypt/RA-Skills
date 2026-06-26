#!/usr/bin/env python3
"""
远程桌面控制核心模块
支持 UU 远程 CLI 连接和屏幕操作
"""

import os
import subprocess
import time
import argparse
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any


class UURemoteController:
    """UU远程控制器"""
    
    def __init__(
        self,
        session_id: Optional[str] = None,
        host: Optional[str] = None,
        port: int = 18792,
        username: str = "administrator",
        password: Optional[str] = None,
        screenshot_dir: str = "./screenshots"
    ):
        self.session_id = session_id
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.screenshot_dir = Path(screenshot_dir)
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        self.connected = False
        
    def connect(self, timeout: int = 30) -> bool:
        """连接UU远程"""
        if self.session_id:
            # 通过 Session ID 连接
            cmd = ["uu", "connect", self.session_id]
        elif self.host:
            # 通过主机连接
            cmd = ["uu", "connect", self.host, "-p", str(self.port)]
        else:
            raise ValueError("必须提供 session_id 或 host")
        
        if self.password and "-p" not in cmd:
            cmd.extend(["-password", self.password])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            if result.returncode == 0:
                self.connected = True
                return True
            else:
                print(f"连接失败: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("连接超时")
            return False
        except FileNotFoundError:
            print("UU CLI 未安装或不在 PATH 中")
            return False
    
    def disconnect(self) -> bool:
        """断开连接"""
        if not self.connected:
            return True
        
        try:
            result = subprocess.run(
                ["uu", "disconnect"],
                capture_output=True,
                text=True,
                timeout=10
            )
            self.connected = False
            return result.returncode == 0
        except Exception as e:
            print(f"断开连接失败: {e}")
            return False
    
    def screenshot(self, filename: Optional[str] = None) -> Optional[str]:
        """截取屏幕"""
        if not self.connected:
            print("未连接远程")
            return None
        
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        output_path = self.screenshot_dir / filename
        
        try:
            # 使用 UU CLI 截图
            cmd = ["uu", "screenshot", str(output_path)]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and output_path.exists():
                return str(output_path)
            else:
                print(f"截图失败: {result.stderr}")
                return None
        except subprocess.TimeoutExpired:
            print("截图超时")
            return None
    
    def exec_command(self, command: str, timeout: int = 60) -> Tuple[bool, str]:
        """在远程执行命令"""
        if not self.connected:
            return False, "未连接远程"
        
        try:
            # 通过 UU exec 执行命令
            cmd = ["uu", "exec", "--", command]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            success = result.returncode == 0
            output = result.stdout if success else result.stderr
            return success, output
        except subprocess.TimeoutExpired:
            return False, "命令执行超时"
        except Exception as e:
            return False, str(e)
    
    def wait_for_screen(self, target_text: str, timeout: int = 60, interval: int = 2) -> bool:
        """等待屏幕上出现指定内容"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            screenshot_path = self.screenshot()
            if screenshot_path:
                # 返回截图路径供视觉识别使用
                # 实际文字识别由调用方完成
                return True
            time.sleep(interval)
        
        return False
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        return False


def interactive_mode():
    """交互式远程控制模式"""
    print("=" * 60)
    print("UU 远程桌面控制 - 交互式模式")
    print("=" * 60)
    
    # 获取连接信息
    mode = input("\n连接模式:\n  1. Session ID\n  2. 主机地址\n选择 (1/2): ").strip()
    
    if mode == "1":
        session_id = input("请输入 Session ID: ").strip()
        controller = UURemoteController(session_id=session_id)
    else:
        host = input("请输入主机地址: ").strip()
        port = input("端口 [18792]: ").strip() or "18792"
        controller = UURemoteController(host=host, port=int(port))
    
    print("\n正在连接...")
    if not controller.connect():
        print("连接失败!")
        return
    
    print("连接成功!\n")
    
    # 交互式命令循环
    while True:
        cmd = input("uu> ").strip()
        
        if not cmd:
            continue
        
        if cmd in ["exit", "quit", "q"]:
            break
        
        if cmd == "screenshot":
            path = controller.screenshot()
            if path:
                print(f"截图已保存: {path}")
            continue
        
        if cmd.startswith("screenshot "):
            path = controller.screenshot(cmd.split()[1])
            if path:
                print(f"截图已保存: {path}")
            continue
        
        # 执行命令
        success, output = controller.exec_command(cmd)
        if success:
            print(output)
        else:
            print(f"错误: {output}")
    
    controller.disconnect()
    print("\n已断开连接")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UU远程桌面控制器")
    parser.add_argument("--session-id", help="UU Session ID")
    parser.add_argument("--host", help="远程主机地址")
    parser.add_argument("--port", type=int, default=18792, help="端口")
    parser.add_argument("--username", default="administrator", help="用户名")
    parser.add_argument("--command", "-c", help="执行单个命令")
    parser.add_argument("--screenshot", "-s", help="截图保存路径")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    
    args = parser.parse_args()
    
    if args.interactive or (not args.command and not args.screenshot):
        interactive_mode()
    else:
        # 单命令/截图模式
        controller = UURemoteController(
            session_id=args.session_id,
            host=args.host,
            port=args.port,
            username=args.username
        )
        
        if controller.connect():
            if args.screenshot:
                path = controller.screenshot(args.screenshot)
                print(f"截图保存: {path}")
            
            if args.command:
                success, output = controller.exec_command(args.command)
                print(output if success else f"错误: {output}")
            
            controller.disconnect()
