#!/usr/bin/env python3
"""
OpenClaw Computer Use - Python API
让 OpenClaw 像人类一样使用电脑
"""

import os
import sys
import time
import subprocess
from datetime import datetime
from typing import Optional, Tuple, List, Dict

class Screenshot:
    """截图功能"""
    
    def __init__(self, save_dir: str = "~/Screenshots"):
        self.save_dir = os.path.expanduser(save_dir)
        os.makedirs(self.save_dir, exist_ok=True)
    
    def full_screen(self, filename: Optional[str] = None) -> str:
        """全屏截图"""
        if filename is None:
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        save_path = os.path.join(self.save_dir, filename)
        
        # 尝试不同的截图工具
        if self._command_exists("scrot"):
            subprocess.run(["scrot", save_path], check=True)
        elif self._command_exists("gnome-screenshot"):
            subprocess.run(["gnome-screenshot", "-f", save_path], check=True)
        elif self._command_exists("import"):  # ImageMagick
            subprocess.run(["import", "-window", "root", save_path], check=True)
        else:
            raise RuntimeError("未找到截图工具，请安装 scrot 或 ImageMagick")
        
        return save_path
    
    def region(self, x: int, y: int, width: int, height: int, 
               filename: Optional[str] = None) -> str:
        """区域截图"""
        if filename is None:
            filename = f"region_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        save_path = os.path.join(self.save_dir, filename)
        
        if self._command_exists("scrot"):
            # 使用 scrot 的选区模式
            subprocess.run(["scrot", "-s", save_path], check=True)
        else:
            raise RuntimeError("区域截图需要 scrot")
        
        return save_path
    
    def window(self, title: str, filename: Optional[str] = None) -> str:
        """窗口截图"""
        if filename is None:
            filename = f"window_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        save_path = os.path.join(self.save_dir, filename)
        
        if self._command_exists("scrot"):
            subprocess.run(["scrot", "-u", save_path], check=True)
        else:
            raise RuntimeError("窗口截图需要 scrot")
        
        return save_path
    
    @staticmethod
    def _command_exists(cmd: str) -> bool:
        return subprocess.run(["which", cmd], 
                            capture_output=True).returncode == 0


class Mouse:
    """鼠标控制"""
    
    def __init__(self):
        self._check_xdotool()
    
    def _check_xdotool(self):
        if not Screenshot._command_exists("xdotool"):
            raise RuntimeError("鼠标控制需要 xdotool，请安装: sudo apt-get install xdotool")
    
    def move(self, x: int, y: int):
        """移动鼠标到指定位置"""
        subprocess.run(["xdotool", "mousemove", str(x), str(y)], check=True)
    
    def click(self, button: int = 1):
        """点击鼠标"""
        subprocess.run(["xdotool", "click", str(button)], check=True)
    
    def double_click(self):
        """双击"""
        subprocess.run(["xdotool", "click", "--repeat", "2", 
                       "--delay", "100", "1"], check=True)
    
    def right_click(self):
        """右键点击"""
        subprocess.run(["xdotool", "click", "3"], check=True)
    
    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int):
        """拖拽"""
        subprocess.run(["xdotool", "mousemove", str(start_x), str(start_y),
                       "mousedown", "1", "mousemove", str(end_x), str(end_y),
                       "mouseup", "1"], check=True)
    
    def scroll(self, amount: int):
        """滚动"""
        button = "4" if amount > 0 else "5"
        for _ in range(abs(amount)):
            subprocess.run(["xdotool", "click", button], check=True)
    
    def get_position(self) -> Tuple[int, int]:
        """获取当前鼠标位置"""
        result = subprocess.run(["xdotool", "getmouselocation"],
                              capture_output=True, text=True, check=True)
        # 解析输出: x:123 y:456 screen:0 window:789
        parts = result.stdout.strip().split()
        x = int(parts[0].split(":")[1])
        y = int(parts[1].split(":")[1])
        return x, y


class Keyboard:
    """键盘控制"""
    
    def __init__(self):
        self._check_xdotool()
    
    def _check_xdotool(self):
        if not Screenshot._command_exists("xdotool"):
            raise RuntimeError("键盘控制需要 xdotool")
    
    def type(self, text: str):
        """输入文本"""
        subprocess.run(["xdotool", "type", text], check=True)
    
    def hotkey(self, *keys: str):
        """快捷键"""
        subprocess.run(["xdotool", "key", "+".join(keys)], check=True)
    
    def press(self, key: str):
        """按下单个按键"""
        subprocess.run(["xdotool", "key", key], check=True)


class Application:
    """应用控制"""
    
    def launch(self, name: str, args: Optional[List[str]] = None):
        """启动应用"""
        cmd = [name]
        if args:
            cmd.extend(args)
        
        # 后台运行
        subprocess.Popen(cmd, 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
    
    def close(self, name: Optional[str] = None, pid: Optional[int] = None):
        """关闭应用"""
        if pid:
            subprocess.run(["kill", str(pid)], check=True)
        elif name:
            subprocess.run(["pkill", "-f", name], check=True)
    
    def focus(self, title: str):
        """聚焦窗口"""
        if Screenshot._command_exists("wmctrl"):
            subprocess.run(["wmctrl", "-a", title], check=True)
        else:
            raise RuntimeError("窗口控制需要 wmctrl")
    
    def list_windows(self) -> List[Dict[str, str]]:
        """列出所有窗口"""
        if not Screenshot._command_exists("wmctrl"):
            raise RuntimeError("需要 wmctrl")
        
        result = subprocess.run(["wmctrl", "-l"],
                              capture_output=True, text=True, check=True)
        
        windows = []
        for line in result.stdout.strip().split("\n"):
            parts = line.split(None, 3)
            if len(parts) >= 4:
                windows.append({
                    "id": parts[0],
                    "desktop": parts[1],
                    "pid": parts[2],
                    "title": parts[3]
                })
        
        return windows


class FileManager:
    """文件管理"""
    
    def list_directory(self, path: str = ".") -> List[str]:
        """列出目录内容"""
        return os.listdir(os.path.expanduser(path))
    
    def search(self, pattern: str, path: str = ".") -> List[str]:
        """搜索文件"""
        import fnmatch
        
        matches = []
        search_path = os.path.expanduser(path)
        
        for root, dirnames, filenames in os.walk(search_path):
            for filename in fnmatch.filter(filenames, pattern):
                matches.append(os.path.join(root, filename))
        
        return matches
    
    def copy(self, src: str, dst: str):
        """复制文件/目录"""
        import shutil
        src = os.path.expanduser(src)
        dst = os.path.expanduser(dst)
        
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    
    def move(self, src: str, dst: str):
        """移动文件/目录"""
        import shutil
        shutil.move(os.path.expanduser(src), os.path.expanduser(dst))
    
    def delete(self, path: str):
        """删除文件/目录"""
        import shutil
        path = os.path.expanduser(path)
        
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


class SystemMonitor:
    """系统监控"""
    
    def cpu_percent(self) -> float:
        """获取 CPU 使用率"""
        result = subprocess.run(["top", "-bn1"],
                              capture_output=True, text=True)
        # 解析 CPU 使用率
        for line in result.stdout.split("\n"):
            if "Cpu(s)" in line:
                # 提取百分比
                percent = line.split("%")[0].split()[-1]
                return float(percent)
        return 0.0
    
    def memory_info(self) -> Dict[str, str]:
        """获取内存信息"""
        result = subprocess.run(["free", "-h"],
                              capture_output=True, text=True, check=True)
        
        lines = result.stdout.strip().split("\n")
        if len(lines) >= 2:
            parts = lines[1].split()
            return {
                "total": parts[1],
                "used": parts[2],
                "free": parts[3],
                "percent": parts[2]  # 简化
            }
        return {}
    
    def disk_usage(self, path: str = "/") -> Dict[str, str]:
        """获取磁盘使用情况"""
        result = subprocess.run(["df", "-h", path],
                              capture_output=True, text=True, check=True)
        
        lines = result.stdout.strip().split("\n")
        if len(lines) >= 2:
            parts = lines[1].split()
            return {
                "total": parts[1],
                "used": parts[2],
                "available": parts[3],
                "percent": parts[4]
            }
        return {}
    
    def top_processes(self, n: int = 10) -> List[Dict[str, str]]:
        """获取占用资源最多的进程"""
        result = subprocess.run(["ps", "aux", "--sort=-%cpu"],
                              capture_output=True, text=True, check=True)
        
        processes = []
        lines = result.stdout.strip().split("\n")[1:n+1]  # 跳过标题
        
        for line in lines:
            parts = line.split()
            if len(parts) >= 11:
                processes.append({
                    "user": parts[0],
                    "pid": parts[1],
                    "cpu": parts[2],
                    "mem": parts[3],
                    "command": " ".join(parts[10:])
                })
        
        return processes


# 便捷函数
def screenshot(save_path: Optional[str] = None) -> str:
    """快速截图"""
    s = Screenshot()
    return s.full_screen(save_path)


def click(x: int, y: int):
    """快速点击"""
    m = Mouse()
    m.move(x, y)
    m.click()


def type_text(text: str):
    """快速输入"""
    k = Keyboard()
    k.type(text)


def hotkey(*keys: str):
    """快速快捷键"""
    k = Keyboard()
    k.hotkey(*keys)


if __name__ == "__main__":
    # 测试代码
    print("🖥️ OpenClaw Computer Use API")
    print("=" * 40)
    
    # 测试截图
    try:
        s = Screenshot()
        path = s.full_screen("test.png")
        print(f"✓ 截图测试通过: {path}")
    except Exception as e:
        print(f"✗ 截图测试失败: {e}")
    
    # 测试鼠标位置
    try:
        m = Mouse()
        x, y = m.get_position()
        print(f"✓ 鼠标位置: ({x}, {y})")
    except Exception as e:
        print(f"✗ 鼠标测试失败: {e}")
    
    print("=" * 40)
    print("测试完成！")
