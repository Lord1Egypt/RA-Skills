"""
HTTP 授权服务 - 通知机制

支持多通道通知：Web UI、系统通知、飞书
"""

import asyncio
import platform
import subprocess
import webbrowser
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from .models import PendingAuthRequest


class NotificationChannel(ABC):
    """通知通道抽象基类"""
    
    @abstractmethod
    def send(self, request: PendingAuthRequest, port: int) -> bool:
        """发送通知，返回是否成功"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """检查通道是否可用"""
        pass


class WebUINotification(NotificationChannel):
    """Web UI 通知（自动打开浏览器）"""
    
    def __init__(self):
        self._opened_urls: set = set()
    
    def send(self, request: PendingAuthRequest, port: int) -> bool:
        """自动打开浏览器显示授权页面"""
        url = f"http://localhost:{port}/ui/auth/{request.request_id}"
        
        # 避免重复打开同一请求
        if request.request_id in self._opened_urls:
            return True
        
        try:
            webbrowser.open(url, new=2)  # new=2 表示在新标签页打开
            self._opened_urls.add(request.request_id)
            return True
        except Exception as e:
            print(f"[WebUI] 打开浏览器失败: {e}")
            return False
    
    def is_available(self) -> bool:
        return True


class SystemNotification(NotificationChannel):
    """系统通知中心（macOS Notification Center / Windows Toast / Linux notify-send）"""
    
    def __init__(self):
        self.system = platform.system()
    
    def send(self, request: PendingAuthRequest, port: int) -> bool:
        title = "OpenClaw 授权请求"
        message = f"Agent 请求 {request.operation} {request.resource_path}"
        
        if self.system == "Darwin":  # macOS
            return self._send_macos(title, message)
        elif self.system == "Windows":
            return self._send_windows(title, message)
        elif self.system == "Linux":
            return self._send_linux(title, message)
        
        return False
    
    def _send_macos(self, title: str, message: str) -> bool:
        """macOS Notification Center"""
        script = f'display notification "{message}" with title "{title}" sound name "default"'
        
        try:
            subprocess.run(
                ["osascript", "-e", script],
                check=True,
                capture_output=True
            )
            return True
        except:
            return False
    
    def _send_windows(self, title: str, message: str) -> bool:
        """Windows Toast Notification"""
        try:
            # 使用 PowerShell 发送通知
            script = f'''
            Add-Type -AssemblyName System.Windows.Forms
            $global:balloon = New-Object System.Windows.Forms.NotifyIcon
            $path = (Get-Process -id $pid).Path
            $balloon.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon($path)
            $balloon.BalloonTipIcon = [System.Windows.Forms.ToolTipIcon]::Info
            $balloon.BalloonTipText = "{message}"
            $balloon.BalloonTipTitle = "{title}"
            $balloon.Visible = $true
            $balloon.ShowBalloonTip(5000)
            '''
            subprocess.run(
                ["powershell", "-Command", script],
                check=True,
                capture_output=True
            )
            return True
        except:
            return False
    
    def _send_linux(self, title: str, message: str) -> bool:
        """Linux Desktop Notification"""
        try:
            subprocess.run(
                ["notify-send", "--urgency=critical", title, message],
                check=True,
                capture_output=True
            )
            return True
        except:
            return False
    
    def is_available(self) -> bool:
        return True


class ConsoleNotification(NotificationChannel):
    """控制台通知（作为后备）"""
    
    def send(self, request: PendingAuthRequest, port: int) -> bool:
        url = f"http://localhost:{port}/ui/auth/{request.request_id}"
        print("\n" + "="*60)
        print("🔐 需要授权")
        print("="*60)
        print(f"   Agent: {request.agent_id}")
        print(f"   资源: {request.resource_path}")
        print(f"   操作: {request.operation}")
        print(f"   级别: {request.data_level}")
        print("-"*60)
        print(f"   请访问: {url}")
        print("="*60)
        return True
    
    def is_available(self) -> bool:
        return True


class NotificationService:
    """通知服务（组合多个通道）"""
    
    def __init__(self, port: int):
        self.port = port
        self.channels: List[NotificationChannel] = []
        self._register_default_channels()
    
    def _register_default_channels(self):
        """注册默认通知通道"""
        # 按优先级注册
        channels = [
            WebUINotification(),
            SystemNotification(),
            ConsoleNotification(),  # 后备
        ]
        
        for channel in channels:
            if channel.is_available():
                self.channels.append(channel)
    
    def notify(self, request: PendingAuthRequest) -> bool:
        """向所有可用通道发送通知"""
        if not self.channels:
            return False
        
        # 至少有一个通道成功即可
        results = []
        for channel in self.channels:
            try:
                result = channel.send(request, self.port)
                results.append(result)
            except Exception as e:
                print(f"[Notification] 通道失败: {e}")
                results.append(False)
        
        return any(results)
    
    def get_channel_names(self) -> List[str]:
        """获取已注册通道名称"""
        return [type(ch).__name__ for ch in self.channels]
