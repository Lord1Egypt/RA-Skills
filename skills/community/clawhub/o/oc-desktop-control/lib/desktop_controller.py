#!/usr/bin/env python3
"""
Desktop Controller - Core library for desktop automation

Based on Bytebot's Computer Use pattern
Supports: VNC, RDP, Local display
"""

import base64
import io
import subprocess
import time
from abc import ABC, abstractmethod
from typing import Optional, Tuple, List, Dict, Any
from pathlib import Path


class DesktopController(ABC):
    """Abstract base class for desktop controllers"""

    def __init__(self):
        self.connected = False

    @abstractmethod
    def connect(self) -> bool:
        """Connect to desktop environment"""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from desktop"""
        pass

    @abstractmethod
    def screenshot(self, region: Optional[Tuple[int, int, int, int]] = None) -> bytes:
        """Capture screenshot, returns PNG bytes"""
        pass

    @abstractmethod
    def mouse_move(self, x: int, y: int) -> None:
        """Move mouse to coordinates"""
        pass

    @abstractmethod
    def mouse_click(self, x: Optional[int] = None, y: Optional[int] = None,
                    button: str = "left", clicks: int = 1) -> None:
        """Click mouse button"""
        pass

    @abstractmethod
    def mouse_drag(self, from_x: int, from_y: int, to_x: int, to_y: int,
                   button: str = "left") -> None:
        """Drag mouse from one point to another"""
        pass

    @abstractmethod
    def mouse_scroll(self, direction: str, amount: int = 1,
                     x: Optional[int] = None, y: Optional[int] = None) -> None:
        """Scroll mouse wheel"""
        pass

    @abstractmethod
    def mouse_position(self) -> Tuple[int, int]:
        """Get current mouse position"""
        pass

    @abstractmethod
    def type_text(self, text: str, delay: Optional[float] = None) -> None:
        """Type text string"""
        pass

    @abstractmethod
    def key_press(self, keys: List[str]) -> None:
        """Press key combination"""
        pass

    @abstractmethod
    def key_down(self, key: str) -> None:
        """Hold key down"""
        pass

    @abstractmethod
    def key_up(self, key: str) -> None:
        """Release key"""
        pass

    @abstractmethod
    def open_application(self, name: str) -> None:
        """Open or focus application"""
        pass

    @abstractmethod
    def close_application(self, name: str) -> None:
        """Close application"""
        pass

    @abstractmethod
    def read_file(self, path: str) -> Optional[bytes]:
        """Read file from desktop environment"""
        pass

    @abstractmethod
    def write_file(self, path: str, content: bytes) -> bool:
        """Write file to desktop environment"""
        pass

    def screenshot_base64(self, region: Optional[Tuple[int, int, int, int]] = None) -> str:
        """Capture screenshot and return as base64 string"""
        image_data = self.screenshot(region)
        return base64.b64encode(image_data).decode('utf-8')

    def wait(self, milliseconds: int) -> None:
        """Wait for specified milliseconds"""
        time.sleep(milliseconds / 1000.0)

    def execute_script(self, script_path: str) -> List[Dict[str, Any]]:
        """Execute automation script"""
        results = []
        script_file = Path(script_path)

        if not script_file.exists():
            raise FileNotFoundError(f"Script not found: {script_path}")

        lines = script_file.read_text().strip().split('\n')

        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            result = self._execute_script_line(line)
            results.append({
                'line': line_num,
                'command': line,
                'result': result
            })

        return results

    def _execute_script_line(self, line: str) -> Any:
        """Execute a single script line"""
        parts = line.split()
        command = parts[0].lower()
        args = parts[1:]

        if command == 'screenshot':
            return self.screenshot_base64()

        elif command == 'wait':
            ms = int(args[0]) if args else 1000
            self.wait(ms)
            return f"Waited {ms}ms"

        elif command == 'mouse':
            action = args[0] if args else 'click'
            if action == 'move':
                x, y = int(args[1]), int(args[2])
                self.mouse_move(x, y)
                return f"Moved to ({x}, {y})"
            elif action == 'click':
                x = int(args[1]) if len(args) > 1 else None
                y = int(args[2]) if len(args) > 2 else None
                self.mouse_click(x, y)
                return f"Clicked at ({x}, {y})"

        elif command == 'type':
            text = ' '.join(args)
            self.type_text(text)
            return f"Typed: {text}"

        elif command == 'key':
            action = args[0] if args else 'press'
            if action == 'press':
                keys = args[1].split(',') if len(args) > 1 else []
                self.key_press(keys)
                return f"Pressed: {keys}"

        else:
            return f"Unknown command: {command}"


class LocalDisplayController(DesktopController):
    """Controller for local display (Linux/macOS/Windows)"""

    def __init__(self, display: Optional[str] = None):
        super().__init__()
        self.display = display or ':0'
        self.platform = self._detect_platform()

    def _detect_platform(self) -> str:
        """Detect operating system"""
        import platform
        system = platform.system().lower()
        if system == 'darwin':
            return 'macos'
        elif system == 'windows':
            return 'windows'
        else:
            return 'linux'

    def connect(self) -> bool:
        """Connect to local display"""
        self.connected = True
        return True

    def disconnect(self) -> None:
        """Disconnect (no-op for local)"""
        self.connected = False

    def screenshot(self, region: Optional[Tuple[int, int, int, int]] = None) -> bytes:
        """Capture screenshot using platform-specific tools"""
        if self.platform == 'macos':
            return self._screenshot_macos(region)
        elif self.platform == 'windows':
            return self._screenshot_windows(region)
        else:
            return self._screenshot_linux(region)

    def _screenshot_macos(self, region: Optional[Tuple[int, int, int, int]] = None) -> bytes:
        """Capture screenshot on macOS"""
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            temp_path = f.name

        cmd = ['screencapture', '-x', temp_path]
        if region:
            x, y, w, h = region
            cmd = ['screencapture', '-x', '-R', f'{x},{y},{w},{h}', temp_path]

        subprocess.run(cmd, check=True)
        data = Path(temp_path).read_bytes()
        Path(temp_path).unlink()
        return data

    def _screenshot_linux(self, region: Optional[Tuple[int, int, int, int]] = None) -> bytes:
        """Capture screenshot on Linux"""
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            temp_path = f.name

        # Try gnome-screenshot first, then scrot, then import (ImageMagick)
        if region:
            x, y, w, h = region
            cmd = ['gnome-screenshot', '-f', temp_path, '-a',
                   '-x', str(x), '-y', str(y), '-w', str(w), '-h', str(h)]
        else:
            cmd = ['gnome-screenshot', '-f', temp_path]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback to scrot
            if region:
                x, y, w, h = region
                cmd = ['scrot', '-a', f'{x},{y},{w},{h}', temp_path]
            else:
                cmd = ['scrot', temp_path]
            subprocess.run(cmd, check=True, capture_output=True)

        data = Path(temp_path).read_bytes()
        Path(temp_path).unlink()
        return data

    def _screenshot_windows(self, region: Optional[Tuple[int, int, int, int]] = None) -> bytes:
        """Capture screenshot on Windows"""
        try:
            from PIL import ImageGrab
            if region:
                screenshot = ImageGrab.grab(bbox=region)
            else:
                screenshot = ImageGrab.grab()

            buffer = io.BytesIO()
            screenshot.save(buffer, format='PNG')
            return buffer.getvalue()
        except ImportError:
            raise RuntimeError("PIL required for Windows screenshots")

    def mouse_move(self, x: int, y: int) -> None:
        """Move mouse to coordinates"""
        if self.platform == 'macos':
            subprocess.run(['cliclick', 'm:', f'{x},{y}'], check=False)
        elif self.platform == 'linux':
            subprocess.run(['xdotool', 'mousemove', str(x), str(y)], check=False)
        else:
            # Windows - would need pyautogui or similar
            pass

    def mouse_click(self, x: Optional[int] = None, y: Optional[int] = None,
                    button: str = "left", clicks: int = 1) -> None:
        """Click mouse button"""
        if x is not None and y is not None:
            self.mouse_move(x, y)

        if self.platform == 'macos':
            btn = 'cl' if button == 'left' else 'cr'
            for _ in range(clicks):
                subprocess.run(['cliclick', btn], check=False)
        elif self.platform == 'linux':
            btn_map = {'left': '1', 'middle': '2', 'right': '3'}
            btn = btn_map.get(button, '1')
            for _ in range(clicks):
                subprocess.run(['xdotool', 'click', btn], check=False)

    def mouse_drag(self, from_x: int, from_y: int, to_x: int, to_y: int,
                   button: str = "left") -> None:
        """Drag mouse"""
        if self.platform == 'linux':
            subprocess.run(['xdotool', 'mousemove', str(from_x), str(from_y),
                          'mousedown', '1', 'mousemove', str(to_x), str(to_y),
                          'mouseup', '1'], check=False)

    def mouse_scroll(self, direction: str, amount: int = 1,
                     x: Optional[int] = None, y: Optional[int] = None) -> None:
        """Scroll mouse wheel"""
        if x is not None and y is not None:
            self.mouse_move(x, y)

        if self.platform == 'linux':
            btn = '4' if direction == 'up' else '5'
            for _ in range(amount):
                subprocess.run(['xdotool', 'click', btn], check=False)

    def mouse_position(self) -> Tuple[int, int]:
        """Get mouse position"""
        if self.platform == 'linux':
            result = subprocess.run(['xdotool', 'getmouselocation'],
                                  capture_output=True, text=True, check=False)
            # Parse "x:123 y:456 screen:0 window:789"
            output = result.stdout.strip()
            try:
                x = int(output.split()[0].split(':')[1])
                y = int(output.split()[1].split(':')[1])
                return (x, y)
            except (IndexError, ValueError):
                return (0, 0)
        return (0, 0)

    def type_text(self, text: str, delay: Optional[float] = None) -> None:
        """Type text"""
        if self.platform == 'macos':
            subprocess.run(['cliclick', 't:', text], check=False)
        elif self.platform == 'linux':
            subprocess.run(['xdotool', 'type', text], check=False)

    def key_press(self, keys: List[str]) -> None:
        """Press key combination"""
        if not keys:
            return

        if self.platform == 'linux':
            key_str = '+'.join(keys)
            subprocess.run(['xdotool', 'key', key_str], check=False)
        elif self.platform == 'macos':
            # Convert to cliclick format
            key_map = {
                'ctrl': 'ctrl',
                'alt': 'alt',
                'shift': 'shift',
                'cmd': 'cmd',
                'return': 'return',
                'space': 'space',
                'tab': 'tab'
            }
            key_str = ','.join([key_map.get(k, k) for k in keys])
            subprocess.run(['cliclick', 'kp:' + key_str], check=False)

    def key_down(self, key: str) -> None:
        """Hold key down"""
        if self.platform == 'linux':
            subprocess.run(['xdotool', 'keydown', key], check=False)

    def key_up(self, key: str) -> None:
        """Release key"""
        if self.platform == 'linux':
            subprocess.run(['xdotool', 'keyup', key], check=False)

    def open_application(self, name: str) -> None:
        """Open application"""
        if self.platform == 'linux':
            subprocess.run(['xdotool', 'search', '--name', name,
                          'windowactivate', '2>/dev/null'], check=False)
            # If not found, try to launch
            app_map = {
                'firefox': 'firefox',
                'terminal': 'gnome-terminal',
                'vscode': 'code',
                'chrome': 'google-chrome'
            }
            if name in app_map:
                subprocess.Popen([app_map[name]])

    def close_application(self, name: str) -> None:
        """Close application"""
        if self.platform == 'linux':
            subprocess.run(['xdotool', 'search', '--name', name,
                          'windowkill'], check=False)

    def read_file(self, path: str) -> Optional[bytes]:
        """Read file"""
        try:
            return Path(path).read_bytes()
        except Exception:
            return None

    def write_file(self, path: str, content: bytes) -> bool:
        """Write file"""
        try:
            Path(path).write_bytes(content)
            return True
        except Exception:
            return False
