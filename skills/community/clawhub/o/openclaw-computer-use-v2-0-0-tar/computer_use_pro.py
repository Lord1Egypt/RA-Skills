#!/usr/bin/env python3
"""
OpenClaw Computer Use Pro - Python API v2.0
让 OpenClaw 像人类一样使用电脑 - 增强版
"""

import os
import sys
import time
import json
import subprocess
import platform
from datetime import datetime
from typing import Optional, Tuple, List, Dict, Union
from pathlib import Path

class Screenshot:
    """增强版截图功能"""
    
    def __init__(self, save_dir: str = "~/Screenshots"):
        self.save_dir = os.path.expanduser(save_dir)
        os.makedirs(self.save_dir, exist_ok=True)
        self.history = []
    
    def full_screen(self, filename: Optional[str] = None, 
                   delay: int = 0) -> str:
        """全屏截图，支持延迟"""
        if delay > 0:
            time.sleep(delay)
        
        if filename is None:
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        save_path = os.path.join(self.save_dir, filename)
        
        # 尝试不同的截图工具
        tools = [
            ("scrot", ["scrot", save_path]),
            ("gnome-screenshot", ["gnome-screenshot", "-f", save_path]),
            ("import", ["import", "-window", "root", save_path]),
        ]
        
        for tool_name, cmd in tools:
            if self._command_exists(tool_name):
                try:
                    subprocess.run(cmd, check=True, capture_output=True)
                    self.history.append({
                        "path": save_path,
                        "type": "full",
                        "time": datetime.now().isoformat()
                    })
                    return save_path
                except subprocess.CalledProcessError:
                    continue
        
        raise RuntimeError("未找到可用的截图工具，请安装 scrot 或 ImageMagick")
    
    def region(self, x: Optional[int] = None, y: Optional[int] = None, 
               width: Optional[int] = None, height: Optional[int] = None,
               interactive: bool = False,
               filename: Optional[str] = None) -> str:
        """区域截图，支持交互式选择"""
        if filename is None:
            filename = f"region_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        save_path = os.path.join(self.save_dir, filename)
        
        if interactive or (x is None):
            # 交互式选择
            if self._command_exists("scrot"):
                subprocess.run(["scrot", "-s", save_path], check=True)
            else:
                raise RuntimeError("交互式截图需要 scrot")
        else:
            # 指定区域
            if self._command_exists("import"):
                subprocess.run([
                    "import", "-window", "root",
                    "-crop", f"{width}x{height}+{x}+{y}",
                    save_path
                ], check=True)
            else:
                raise RuntimeError("区域截图需要 ImageMagick")
        
        self.history.append({
            "path": save_path,
            "type": "region",
            "time": datetime.now().isoformat()
        })
        return save_path
    
    def window(self, title: Optional[str] = None, 
               filename: Optional[str] = None) -> str:
        """窗口截图，自动查找窗口"""
        if filename is None:
            filename = f"window_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        save_path = os.path.join(self.save_dir, filename)
        
        if title:
            # 通过窗口标题截图
            if self._command_exists("import"):
                subprocess.run([
                    "import", "-window", title, save_path
                ], check=True)
        else:
            # 活动窗口
            if self._command_exists("scrot"):
                subprocess.run(["scrot", "-u", save_path], check=True)
        
        self.history.append({
            "path": save_path,
            "type": "window",
            "time": datetime.now().isoformat()
        })
        return save_path
    
    def clipboard(self, filename: Optional[str] = None) -> str:
        """从剪贴板保存截图"""
        if filename is None:
            filename = f"clipboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        save_path = os.path.join(self.save_dir, filename)
        
        if self._command_exists("xclip"):
            # 从剪贴板获取图片
            with open(save_path, 'wb') as f:
                subprocess.run(
                    ["xclip", "-selection", "clipboard", "-t", "image/png", "-o"],
                    stdout=f, check=True
                )
        else:
            raise RuntimeError("剪贴板操作需要 xclip")
        
        return save_path
    
    def get_history(self) -> List[Dict]:
        """获取截图历史"""
        return self.history
    
    @staticmethod
    def _command_exists(cmd: str) -> bool:
        return subprocess.run(["which", cmd], 
                            capture_output=True).returncode == 0


class Mouse:
    """增强版鼠标控制"""
    
    def __init__(self):
        self._check_xdotool()
        self.move_history = []
    
    def _check_xdotool(self):
        if not self._command_exists("xdotool"):
            raise RuntimeError("鼠标控制需要 xdotool")
    
    def move(self, x: int, y: int, duration: float = 0):
        """移动鼠标，支持动画"""
        if duration > 0:
            # 平滑移动
            start_x, start_y = self.get_position()
            steps = int(duration * 60)  # 60fps
            for i in range(steps + 1):
                t = i / steps
                cur_x = int(start_x + (x - start_x) * t)
                cur_y = int(start_y + (y - start_y) * t)
                subprocess.run(["xdotool", "mousemove", str(cur_x), str(cur_y)],
                             check=True, capture_output=True)
                time.sleep(duration / steps)
        else:
            subprocess.run(["xdotool", "mousemove", str(x), str(y)],
                         check=True, capture_output=True)
        
        self.move_history.append({"x": x, "y": y, "time": time.time()})
    
    def click(self, button: int = 1, clicks: int = 1):
        """点击，支持多次点击"""
        for _ in range(clicks):
            subprocess.run(["xdotool", "click", str(button)],
                         check=True, capture_output=True)
            if clicks > 1:
                time.sleep(0.1)
    
    def double_click(self):
        """双击"""
        self.click(1, 2)
    
    def right_click(self):
        """右键点击"""
        self.click(3)
    
    def middle_click(self):
        """中键点击"""
        self.click(2)
    
    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int,
             duration: float = 0.5):
        """拖拽，支持动画"""
        # 移动到起点
        self.move(start_x, start_y)
        time.sleep(0.1)
        
        # 按下鼠标
        subprocess.run(["xdotool", "mousedown", "1"],
                     check=True, capture_output=True)
        
        # 平滑移动到终点
        if duration > 0:
            steps = int(duration * 60)
            for i in range(steps + 1):
                t = i / steps
                cur_x = int(start_x + (end_x - start_x) * t)
                cur_y = int(start_y + (end_y - start_y) * t)
                subprocess.run(["xdotool", "mousemove", str(cur_x), str(cur_y)],
                             check=True, capture_output=True)
                time.sleep(duration / steps)
        else:
            self.move(end_x, end_y)
        
        time.sleep(0.1)
        
        # 释放鼠标
        subprocess.run(["xdotool", "mouseup", "1"],
                     check=True, capture_output=True)
    
    def scroll(self, amount: int, horizontal: bool = False):
        """滚动"""
        button = "6" if horizontal else ("4" if amount > 0 else "5")
        for _ in range(abs(amount)):
            subprocess.run(["xdotool", "click", button],
                         check=True, capture_output=True)
            time.sleep(0.01)
    
    def get_position(self) -> Tuple[int, int]:
        """获取当前鼠标位置"""
        result = subprocess.run(["xdotool", "getmouselocation"],
                              capture_output=True, text=True, check=True)
        parts = result.stdout.strip().split()
        x = int(parts[0].split(":")[1])
        y = int(parts[1].split(":")[1])
        return x, y
    
    def move_to_image(self, image_path: str, confidence: float = 0.9):
        """移动到图片位置（需要 opencv）"""
        try:
            import cv2
            import numpy as np
            from PIL import Image
            
            # 截图
            screenshot_path = "/tmp/find_image_screenshot.png"
            subprocess.run(["scrot", screenshot_path], check=True)
            
            # 加载图片
            screenshot = cv2.imread(screenshot_path)
            template = cv2.imread(image_path)
            
            # 模板匹配
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= confidence:
                h, w = template.shape[:2]
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                self.move(center_x, center_y)
                return True
            return False
        except ImportError:
            raise RuntimeError("图片识别需要 opencv-python 和 pillow")
    
    @staticmethod
    def _command_exists(cmd: str) -> bool:
        return subprocess.run(["which", cmd], 
                            capture_output=True).returncode == 0


class Keyboard:
    """增强版键盘控制"""
    
    def __init__(self):
        self._check_xdotool()
    
    def _check_xdotool(self):
        if not self._command_exists("xdotool"):
            raise RuntimeError("键盘控制需要 xdotool")
    
    def type(self, text: str, interval: float = 0.01):
        """输入文本，支持速度控制"""
        if interval > 0:
            for char in text:
                subprocess.run(["xdotool", "type", char],
                             check=True, capture_output=True)
                time.sleep(interval)
        else:
            subprocess.run(["xdotool", "type", text],
                         check=True, capture_output=True)
    
    def hotkey(self, *keys: str):
        """快捷键"""
        subprocess.run(["xdotool", "key", "+".join(keys)],
                     check=True, capture_output=True)
    
    def press(self, key: str):
        """按下单个按键"""
        subprocess.run(["xdotool", "key", key],
                     check=True, capture_output=True)
    
    def hold(self, key: str):
        """按住按键"""
        subprocess.run(["xdotool", "keydown", key],
                     check=True, capture_output=True)
    
    def release(self, key: str):
        """释放按键"""
        subprocess.run(["xdotool", "keyup", key],
                     check=True, capture_output=True)
    
    def copy(self):
        """复制"""
        self.hotkey('ctrl', 'c')
    
    def paste(self):
        """粘贴"""
        self.hotkey('ctrl', 'v')
    
    def select_all(self):
        """全选"""
        self.hotkey('ctrl', 'a')
    
    def save(self):
        """保存"""
        self.hotkey('ctrl', 's')
    
    @staticmethod
    def _command_exists(cmd: str) -> bool:
        return subprocess.run(["which", cmd], 
                            capture_output=True).returncode == 0


class Application:
    """增强版应用控制"""
    
    def __init__(self):
        self.running_apps = []
    
    def launch(self, name: str, args: Optional[List[str]] = None,
               wait: bool = False, timeout: int = 10):
        """启动应用，支持等待"""
        cmd = [name]
        if args:
            cmd.extend(args)
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        
        self.running_apps.append({
            "name": name,
            "pid": process.pid,
            "start_time": datetime.now().isoformat()
        })
        
        if wait:
            # 等待窗口出现
            for _ in range(timeout * 10):
                windows = self.list_windows()
                for w in windows:
                    if name.lower() in w.get("title", "").lower():
                        return process.pid
                time.sleep(0.1)
        
        return process.pid
    
    def close(self, name: Optional[str] = None, pid: Optional[int] = None,
              force: bool = False):
        """关闭应用，支持强制关闭"""
        if pid:
            if force:
                subprocess.run(["kill", "-9", str(pid)], check=True)
            else:
                subprocess.run(["kill", str(pid)], check=True)
        elif name:
            if force:
                subprocess.run(["pkill", "-9", "-f", name], check=True)
            else:
                subprocess.run(["pkill", "-f", name], check=True)
    
    def focus(self, title: str):
        """聚焦窗口"""
        if self._command_exists("wmctrl"):
            subprocess.run(["wmctrl", "-a", title],
                         check=True, capture_output=True)
        else:
            raise RuntimeError("窗口控制需要 wmctrl")
    
    def minimize(self, title: str):
        """最小化窗口"""
        if self._command_exists("wmctrl"):
            subprocess.run(["wmctrl", "-r", title, "-b", "add,hidden"],
                         check=True, capture_output=True)
    
    def maximize(self, title: str):
        """最大化窗口"""
        if self._command_exists("wmctrl"):
            subprocess.run(["wmctrl", "-r", title, "-b", "add,maximized_vert,maximized_horz"],
                         check=True, capture_output=True)
    
    def list_windows(self) -> List[Dict[str, str]]:
        """列出所有窗口"""
        if not self._command_exists("wmctrl"):
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
    
    def find_window(self, pattern: str) -> Optional[Dict]:
        """查找窗口"""
        windows = self.list_windows()
        for w in windows:
            if pattern.lower() in w.get("title", "").lower():
                return w
        return None
    
    @staticmethod
    def _command_exists(cmd: str) -> bool:
        return subprocess.run(["which", cmd], 
                            capture_output=True).returncode == 0


class FileManager:
    """增强版文件管理"""
    
    def list_directory(self, path: str = ".", 
                      pattern: Optional[str] = None) -> List[Dict]:
        """列出目录内容，返回详细信息"""
        path = os.path.expanduser(path)
        items = []
        
        for item in os.listdir(path):
            if pattern and not self._match_pattern(item, pattern):
                continue
            
            full_path = os.path.join(path, item)
            stat = os.stat(full_path)
            
            items.append({
                "name": item,
                "path": full_path,
                "type": "directory" if os.path.isdir(full_path) else "file",
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "permissions": oct(stat.st_mode)[-3:]
            })
        
        return sorted(items, key=lambda x: (x["type"] != "directory", x["name"]))
    
    def search(self, pattern: str, path: str = ".", 
               recursive: bool = True) -> List[str]:
        """搜索文件"""
        import fnmatch
        
        matches = []
        search_path = os.path.expanduser(path)
        
        if recursive:
            for root, dirnames, filenames in os.walk(search_path):
                for filename in fnmatch.filter(filenames, pattern):
                    matches.append(os.path.join(root, filename))
        else:
            for item in os.listdir(search_path):
                if fnmatch.fnmatch(item, pattern):
                    matches.append(os.path.join(search_path, item))
        
        return matches
    
    def copy(self, src: str, dst: str, progress: bool = False):
        """复制文件/目录，支持进度显示"""
        import shutil
        src = os.path.expanduser(src)
        dst = os.path.expanduser(dst)
        
        if os.path.isdir(src):
            if progress:
                # 计算总大小
                total_size = sum(
                    os.path.getsize(os.path.join(dirpath, filename))
                    for dirpath, dirnames, filenames in os.walk(src)
                    for filename in filenames
                )
                copied = 0
                
                def copy_progress(src, dst):
                    nonlocal copied
                    shutil.copy2(src, dst)
                    copied += os.path.getsize(src)
                    percent = (copied / total_size) * 100
                    print(f"\r复制进度: {percent:.1f}%", end="", flush=True)
                
                shutil.copytree(src, dst, copy_function=copy_progress)
                print()  # 换行
            else:
                shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    
    def move(self, src: str, dst: str):
        """移动文件/目录"""
        import shutil
        shutil.move(os.path.expanduser(src), os.path.expanduser(dst))
    
    def delete(self, path: str, confirm: bool = True):
        """删除文件/目录，支持确认"""
        import shutil
        path = os.path.expanduser(path)
        
        if confirm:
            response = input(f"确定要删除 {path} 吗? (y/N): ")
            if response.lower() != 'y':
                print("取消删除")
                return
        
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    
    def rename(self, src: str, dst: str):
        """重命名"""
        os.rename(os.path.expanduser(src), os.path.expanduser(dst))
    
    def batch_rename(self, path: str, pattern: str, replacement: str):
        """批量重命名"""
        import re
        path = os.path.expanduser(path)
        
        for item in os.listdir(path):
            new_name = re.sub(pattern, replacement, item)
            if new_name != item:
                os.rename(
                    os.path.join(path, item),
                    os.path.join(path, new_name)
                )
    
    def get_info(self, path: str) -> Dict:
        """获取文件/目录详细信息"""
        path = os.path.expanduser(path)
        stat = os.stat(path)
        
        return {
            "name": os.path.basename(path),
            "path": path,
            "type": "directory" if os.path.isdir(path) else "file",
            "size": stat.st_size,
            "size_human": self._human_readable_size(stat.st_size),
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
            "permissions": oct(stat.st_mode)[-3:]
        }
    
    @staticmethod
    def _match_pattern(name: str, pattern: str) -> bool:
        import fnmatch
        return fnmatch.fnmatch(name, pattern)
    
    @staticmethod
    def _human_readable_size(size_bytes: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"


class SystemMonitor:
    """增强版系统监控"""
    
    def cpu_percent(self, interval: float = 1.0) -> float:
        """获取 CPU 使用率"""
        result = subprocess.run(["top", "-bn1"],
                              capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            if "Cpu(s)" in line:
                percent = line.split("%")[0].split()[-1]
                return float(percent)
        return 0.0
    
    def memory_info(self) -> Dict[str, Union[str, float]]:
        """获取内存信息"""
        result = subprocess.run(["free", "-b"],
                              capture_output=True, text=True, check=True)
        
        lines = result.stdout.strip().split("\n")
        if len(lines) >= 2:
            parts = lines[1].split()
            total = int(parts[1])
            used = int(parts[2])
            free = int(parts[3])
            
            return {
                "total": self._human_readable_size(total),
                "used": self._human_readable_size(used),
                "free": self._human_readable_size(free),
                "percent": (used / total) * 100 if total > 0 else 0
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
                "filesystem": parts[0],
                "total": parts[1],
                "used": parts[2],
                "available": parts[3],
                "percent": parts[4],
                "mount": parts[5]
            }
        return {}
    
    def top_processes(self, n: int = 10, sort_by: str = "cpu") -> List[Dict]:
        """获取占用资源最多的进程"""
        sort_key = "-%cpu" if sort_by == "cpu" else "-%mem"
        result = subprocess.run(
            ["ps", "aux", f"--sort={sort_key}"],
            capture_output=True, text=True, check=True
        )
        
        processes = []
        lines = result.stdout.strip().split("\n")[1:n+1]
        
        for line in lines:
            parts = line.split()
            if len(parts) >= 11:
                processes.append({
                    "user": parts[0],
                    "pid": parts[1],
                    "cpu": parts[2],
                    "mem": parts[3],
                    "vsz": parts[4],
                    "rss": parts[5],
                    "tty": parts[6],
                    "stat": parts[7],
                    "start": parts[8],
                    "time": parts[9],
                    "command": " ".join(parts[10:])
                })
        
        return processes
    
    def kill_process(self, pid: int, force: bool = False):
        """结束进程"""
        if force:
            subprocess.run(["kill", "-9", str(pid)], check=True)
        else:
            subprocess.run(["kill", str(pid)], check=True)
    
    def get_system_info(self) -> Dict:
        """获取系统信息"""
        return {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "architecture": platform.architecture()[0],
            "processor": platform.processor(),
            "hostname": platform.node(),
            "python_version": platform.python_version()
        }
    
    @staticmethod
    def _human_readable_size(size_bytes: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"


class Recorder:
    """屏幕录制功能"""
    
    def __init__(self, save_dir: str = "~/Recordings"):
        self.save_dir = os.path.expanduser(save_dir)
        os.makedirs(self.save_dir, exist_ok=True)
        self.recording_process = None
    
    def start(self, filename: Optional[str] = None, 
              fps: int = 30, region: Optional[Tuple[int, int, int, int]] = None):
        """开始录制"""
        if filename is None:
            filename = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        
        save_path = os.path.join(self.save_dir, filename)
        
        # 使用 ffmpeg 录制
        cmd = [
            "ffmpeg",
            "-f", "x11grab",
            "-r", str(fps),
            "-i", ":0.0" if region is None else f":0.0+{region[0]},{region[1]}",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-crf", "23",
            save_path
        ]
        
        self.recording_process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        return save_path
    
    def stop(self):
        """停止录制"""
        if self.recording_process:
            self.recording_process.terminate()
            self.recording_process.wait()
            self.recording_process = None


# 便捷函数
def screenshot(save_path: Optional[str] = None, delay: int = 0) -> str:
    """快速截图"""
    s = Screenshot()
    return s.full_screen(save_path, delay)


def click(x: int, y: int):
    """快速点击"""
    m = Mouse()
    m.move(x, y)
    m.click()


def type_text(text: str, interval: float = 0.01):
    """快速输入"""
    k = Keyboard()
    k.type(text, interval)


def hotkey(*keys: str):
    """快速快捷键"""
    k = Keyboard()
    k.hotkey(*keys)


if __name__ == "__main__":
    print("🖥️ OpenClaw Computer Use Pro API v2.0")
    print("=" * 40)
    
    # 测试所有模块
    tests = [
        ("Screenshot", lambda: Screenshot()),
        ("Mouse", lambda: Mouse()),
        ("Keyboard", lambda: Keyboard()),
        ("Application", lambda: Application()),
        ("FileManager", lambda: FileManager()),
        ("SystemMonitor", lambda: SystemMonitor()),
        ("Recorder", lambda: Recorder()),
    ]
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"✓ {name} 模块加载成功")
        except Exception as e:
            print(f"✗ {name} 模块加载失败: {e}")
    
    print("=" * 40)
    print("API 测试完成！")
