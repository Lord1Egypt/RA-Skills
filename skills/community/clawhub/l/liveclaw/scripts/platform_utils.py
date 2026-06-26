#!/usr/bin/env python3
"""
OpenClaw Agent Live — 跨平台工具模块
封装 Linux / Windows / macOS 间的差异：
  - 工作目录路径
  - 进程查找 / 终止 / 守护化
  - FFmpeg 采集命令 (x11grab vs gdigrab vs avfoundation)
  - 子进程 session 参数
"""
import os
import sys
import signal
import subprocess
import tempfile
from pathlib import Path

# ── 平台判断 ─────────────────────────────────────────────────

def is_windows() -> bool:
    return sys.platform == "win32"

def is_linux() -> bool:
    return sys.platform.startswith("linux")

def is_mac() -> bool:
    return sys.platform == "darwin"

def needs_xvfb() -> bool:
    """Pillow 帧生成模式，不再需要 Xvfb 虚拟屏幕。"""
    return False

def get_platform_tag() -> str:
    """返回当前平台的简短标签，用于日志和 UI 显示"""
    if is_windows():
        return "Windows"
    elif is_mac():
        return "macOS"
    return "Linux"

# ── 工作目录 ─────────────────────────────────────────────────

def get_work_dir() -> Path:
    """跨平台工作目录
    Linux  : /tmp/trtc_stream
    Windows: %TEMP%\\trtc_stream
    macOS  : /tmp/trtc_stream
    """
    if is_windows():
        return Path(tempfile.gettempdir()) / "trtc_stream"
    return Path("/tmp/trtc_stream")

# ── DISPLAY 参数化（仅 Linux 有效）──────────────────────────

def get_display_num() -> int:
    """获取 Xvfb display 编号
    优先读取环境变量 OPENCLAW_DISPLAY，默认 99
    """
    return int(os.environ.get("OPENCLAW_DISPLAY", "99"))

def get_display_str(with_screen: bool = False) -> str:
    """获取 DISPLAY 字符串
    with_screen=False: ':99'    (用于 env["DISPLAY"])
    with_screen=True : ':99.0'  (用于 x11grab -i 参数)
    """
    num = get_display_num()
    if with_screen:
        return f":{num}.0"
    return f":{num}"

def check_display_available(num: int = None) -> bool:
    """检测指定 display 编号是否空闲（仅 Linux 有效）"""
    if is_windows():
        return True
    if num is None:
        num = get_display_num()
    lock_file = Path(f"/tmp/.X{num}-lock")
    return not lock_file.exists()

# ── Python 可执行文件 ────────────────────────────────────────

def get_python_cmd() -> str:
    """当前 Python 解释器路径
    优先使用 sys.executable（当前运行的解释器），确保虚拟环境中的依赖可用。
    仅当 sys.executable 不可用时回退到系统 python3。
    
    修复场景：用户在虚拟环境中安装了 PyAV/numpy 等依赖，
    但系统 python3 指向未安装这些包的系统 Python，
    导致 stream_daemon.py 启动后 import av 失败。
    """
    exe = sys.executable
    if exe and os.path.isfile(exe):
        return exe
    if is_windows():
        return "python.exe"
    return "python3"

def get_pythonw_cmd() -> str:
    """Windows 专用无窗口 Python（用于守护进程化）
    非 Windows 平台与 get_python_cmd() 保持一致，优先使用 sys.executable。
    """
    if is_windows():
        base = Path(sys.executable)
        pythonw = base.parent / "pythonw.exe"
        if pythonw.exists():
            return str(pythonw)
        return sys.executable
    return get_python_cmd()

# ── FFmpeg 采集命令 ──────────────────────────────────────────

def get_ffmpeg_cmd() -> str:
    """FFmpeg 可执行文件路径（Windows 可能需要完整路径）"""
    if is_windows():
        # 尝试从 PATH 查找，或者使用环境变量
        ffmpeg_path = os.environ.get("FFMPEG_PATH", "ffmpeg")
        return ffmpeg_path
    return "ffmpeg"

def get_capture_cmd(fps: int = 15, width: int = 1920, height: int = 1080,
                    display: str = None,
                    window_title: str = "OpenClaw Agent - LIVE") -> list:
    """构建 FFmpeg 屏幕采集命令（三平台）
    Linux  : x11grab 从 Xvfb DISPLAY 采集（虚拟屏幕）
    Windows: gdigrab 按窗口标题采集（桌面窗口）
    macOS  : avfoundation 采集桌面画面（桌面窗口）
    """
    ffmpeg = get_ffmpeg_cmd()

    if is_windows():
        # Windows: gdigrab 按窗口标题采集
        return [
            ffmpeg, '-loglevel', 'error',
            '-f', 'gdigrab',
            '-draw_mouse', '0',
            '-framerate', str(fps),
            '-video_size', f'{width}x{height}',
            '-offset_x', '0', '-offset_y', '0',
            '-i', f'title={window_title}',
            '-f', 'rawvideo', '-pix_fmt', 'rgb24', 'pipe:1'
        ]
    elif is_mac():
        # macOS: avfoundation 采集桌面
        # "1" = 默认屏幕设备索引（Capture screen）
        # 可通过 ffmpeg -f avfoundation -list_devices true -i "" 查看设备列表
        return [
            ffmpeg, '-loglevel', 'error',
            '-f', 'avfoundation',
            '-capture_cursor', '0',
            '-framerate', str(fps),
            '-video_size', f'{width}x{height}',
            '-i', '1:none',
            '-f', 'rawvideo', '-pix_fmt', 'rgb24', 'pipe:1'
        ]
    else:
        # Linux: x11grab 从 Xvfb DISPLAY 采集
        if display is None:
            display = get_display_str(with_screen=True)
        return [
            ffmpeg, '-loglevel', 'error',
            '-f', 'x11grab',
            '-draw_mouse', '0',
            '-r', str(fps),
            '-s', f'{width}x{height}',
            '-i', display,
            '-f', 'rawvideo', '-pix_fmt', 'rgb24', 'pipe:1'
        ]

# ── 进程管理 ─────────────────────────────────────────────────

def find_process_by_script(script_name: str) -> list:
    """按脚本名查找进程 PID 列表
    Linux  : pgrep -f <script_name>
    Windows: psutil 遍历 cmdline
    """
    if is_windows():
        try:
            import psutil
            pids = []
            for proc in psutil.process_iter(['pid', 'cmdline']):
                try:
                    cmdline = proc.info.get('cmdline') or []
                    if any(script_name in arg for arg in cmdline):
                        pids.append(proc.info['pid'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            return pids
        except ImportError:
            return []
    else:
        try:
            result = subprocess.run(
                ["pgrep", "-f", script_name],
                capture_output=True, text=True
            )
            return [int(x) for x in result.stdout.strip().splitlines() if x.strip()]
        except Exception:
            return []

def find_process_by_name(proc_name: str) -> list:
    """按进程名精确查找 PID 列表
    Linux  : pgrep -x <name>
    Windows: psutil 遍历 name
    """
    if is_windows():
        try:
            import psutil
            pids = []
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'] and proc_name.lower() in proc.info['name'].lower():
                        pids.append(proc.info['pid'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            return pids
        except ImportError:
            return []
    else:
        try:
            result = subprocess.run(
                ["pgrep", "-x", proc_name],
                capture_output=True, text=True
            )
            return [int(x) for x in result.stdout.strip().splitlines() if x.strip()]
        except Exception:
            return []

def is_process_alive(pid: int) -> bool:
    """检测进程是否存活（排除 zombie）"""
    if is_windows():
        try:
            import psutil
            proc = psutil.Process(pid)
            return proc.status() != psutil.STATUS_ZOMBIE
        except Exception:
            return False
    else:
        try:
            os.kill(pid, 0)
            # 排除 zombie
            try:
                stat = Path(f"/proc/{pid}/status").read_text()
                if "zombie" in stat.lower():
                    return False
            except FileNotFoundError:
                pass  # macOS 没有 /proc，但 os.kill(0) 成功即可
            return True
        except (ProcessLookupError, PermissionError):
            return False

def kill_process(pid: int, force: bool = False):
    """终止进程
    Linux  : SIGTERM / SIGKILL
    Windows: psutil.terminate() / taskkill /F
    """
    if is_windows():
        try:
            import psutil
            proc = psutil.Process(pid)
            if force:
                proc.kill()
            else:
                proc.terminate()
        except Exception:
            if force:
                subprocess.run(["taskkill", "/F", "/PID", str(pid)],
                               capture_output=True)
    else:
        try:
            sig = signal.SIGKILL if force else signal.SIGTERM
            os.kill(pid, sig)
        except (ProcessLookupError, PermissionError):
            pass

# ── 子进程 session 参数 ──────────────────────────────────────

def new_session_kwargs() -> dict:
    """返回 subprocess.Popen 的跨平台 session 隔离参数
    Linux  : start_new_session=True
    Windows: CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW
    """
    if is_windows():
        CREATE_NEW_PROCESS_GROUP = 0x00000200
        CREATE_NO_WINDOW = 0x08000000
        return {"creationflags": CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW}
    else:
        return {"start_new_session": True}

# ── 守护进程化 ───────────────────────────────────────────────

def daemonize(log_file: str = None):
    """将当前进程守护化
    Linux  : 经典双 fork + setsid
    Windows: 不支持 fork，需用 new_session_kwargs() 在启动时隔离
    """
    if is_windows():
        # Windows 不支持 fork，守护化在启动端用 pythonw + creationflags 处理
        return

    # First fork
    if os.fork() > 0:
        sys.exit(0)
    os.setsid()
    # Second fork
    if os.fork() > 0:
        sys.exit(0)

    # Redirect stdio
    sys.stdout.flush()
    sys.stderr.flush()
    with open(os.devnull, "r") as devnull:
        os.dup2(devnull.fileno(), sys.stdin.fileno())

    if log_file:
        log_fd = open(log_file, "a")
        os.dup2(log_fd.fileno(), sys.stdout.fileno())
        os.dup2(log_fd.fileno(), sys.stderr.fileno())
        log_fd.close()  # dup2 已复制 fd，原始句柄可安全关闭

def start_daemon_process(script_path: str, log_file: str = None,
                         env: dict = None) -> int:
    """以守护方式启动子脚本并返回 PID
    Linux  : start_new_session=True
    Windows: pythonw.exe + CREATE_NO_WINDOW
    """
    python_cmd = get_pythonw_cmd() if is_windows() else get_python_cmd()

    log_fh = open(log_file, "a") if log_file else None
    stdout_target = log_fh if log_fh else subprocess.DEVNULL
    stderr_target = subprocess.STDOUT if log_fh else subprocess.DEVNULL

    proc = subprocess.Popen(
        [python_cmd, script_path],
        stdout=stdout_target,
        stderr=stderr_target,
        env=env,
        **new_session_kwargs()
    )
    if log_fh:
        log_fh.close()  # Popen 已继承 fd，原始句柄可安全关闭
    return proc.pid

# ── Windows DPI 感知 ─────────────────────────────────────────

def enable_dpi_awareness():
    """Windows 下启用 Per-Monitor DPI 感知，防止缩放导致采集分辨率不匹配"""
    if is_windows():
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(2)  # Per-Monitor V2
        except Exception:
            try:
                import ctypes
                ctypes.windll.user32.SetProcessDPIAware()  # fallback
            except Exception:
                pass

# ── 字体回退 ─────────────────────────────────────────────────

def get_font_cn() -> str:
    """中文字体名
    Linux  : Noto Sans CJK SC
    Windows: Microsoft YaHei
    macOS  : PingFang SC
    """
    if is_windows():
        return "Microsoft YaHei"
    elif is_mac():
        return "PingFang SC"
    return "Noto Sans CJK SC"

def get_font_mono() -> str:
    """等宽字体名
    Linux  : Courier
    Windows: Consolas
    macOS  : Menlo
    """
    if is_windows():
        return "Consolas"
    elif is_mac():
        return "Menlo"
    return "Courier"

def validate_font(font_name: str, fallbacks: list = None) -> str:
    """验证字体是否可用，不可用则按 fallbacks 回退
    依赖 tkinter.font.families()（需 Tk 已初始化）。
    如果 Tk 未初始化或无法检测，直接返回原字体名。
    
    Args:
        font_name: 首选字体名
        fallbacks: 回退字体列表，按优先级排序
    Returns:
        实际可用的字体名
    """
    if fallbacks is None:
        fallbacks = []
    try:
        import tkinter as tk
        from tkinter import font as tkfont
        # 需要有一个 Tk 实例才能查询字体
        try:
            root = tk._default_root
            if root is None:
                return font_name  # Tk 未初始化，跳过验证
        except Exception:
            return font_name
        available = set(tkfont.families())
        if font_name in available:
            return font_name
        # 尝试 fallbacks
        for fb in fallbacks:
            if fb in available:
                return fb
        # 都不可用，返回原名（tkinter 会用默认字体兜底）
        return font_name
    except Exception:
        return font_name


# ── 字体自动安装（仅 Linux）─────────────────────────────────

# 中文字体包和对应的字体名映射
_LINUX_CJK_PACKAGES = [
    ("fonts-noto-cjk", "Noto Sans CJK SC"),
    ("fonts-noto-cjk-extra", "Noto Sans CJK SC"),
    ("fonts-wqy-microhei", "WenQuanYi Micro Hei"),
    ("fonts-wqy-zenhei", "WenQuanYi Zen Hei"),
]

# Emoji 字体包（按优先级排列）
# Symbola 是传统 TrueType 单色字形，Tkinter (Xft/freetype) 可直接渲染；
# Noto Color Emoji 是 SVG 彩色字体，Tkinter 不支持彩色渲染但 fontconfig
# 仍可回退到其单色轮廓。优先安装 Symbola 以获得最佳兼容性。
_LINUX_EMOJI_PACKAGES = [
    "fonts-symbola",              # Debian/Ubuntu: 覆盖几乎所有 Unicode emoji
    "fonts-noto-color-emoji",     # Debian/Ubuntu: Google Noto 彩色 emoji
]

def _has_emoji_font_linux() -> bool:
    """检测系统是否已安装可渲染 emoji 的字体（仅 Linux）。
    通过 fc-list 查询 U+1F99E (🦞) 所在的字体族来判断。
    """
    try:
        # 查询龙虾 emoji 是否有对应字体
        result = subprocess.run(
            ["fc-list", ":charset=1f99e"],
            capture_output=True, text=True, timeout=5
        )
        return bool(result.stdout.strip())
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def has_emoji_font() -> bool:
    """跨平台检测当前系统是否支持 emoji 渲染。
    Windows / macOS 自带 emoji 字体，直接返回 True。
    Linux 通过 fontconfig 查询。
    """
    if is_windows() or is_mac():
        return True
    return _has_emoji_font_linux()


def ensure_fonts_installed(verbose: bool = True):
    """检测并自动安装中文字体 + emoji 字体（仅 Linux 有效）

    检测逻辑:
    1. 先检查 fc-list 中是否已有 CJK 字体
    2. 若无，尝试 apt-get install fonts-noto-cjk（需 sudo 权限）
    3. 检查 emoji 字体，若无则尝试安装 fonts-symbola
    4. 若 apt 不可用或无权限，打印手动安装指引

    Windows/macOS 下直接跳过（系统自带中文字体和 emoji 字体）
    """
    if is_windows() or is_mac():
        if verbose:
            print("  [=] Font check skipped (system fonts available)")
        return

    _need_fc_cache = False

    # ── 1. CJK 中文字体检测 ──
    try:
        result = subprocess.run(
            ["fc-list", ":lang=zh"],
            capture_output=True, text=True, timeout=5
        )
        if result.stdout.strip():
            if verbose:
                lines = result.stdout.strip().splitlines()
                print(f"  [=] CJK fonts found ({len(lines)} entries)")
        else:
            if verbose:
                print("  [!] No CJK fonts detected, attempting install...")
            _need_fc_cache |= _try_apt_install("fonts-noto-cjk", verbose)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        _need_fc_cache |= _try_apt_install("fonts-noto-cjk", verbose)

    # ── 2. Emoji 字体检测 ──
    if not _has_emoji_font_linux():
        if verbose:
            print("  [!] No emoji font detected, attempting install...")
        for pkg in _LINUX_EMOJI_PACKAGES:
            if _try_apt_install(pkg, verbose):
                _need_fc_cache = True
                break  # 装上一个即可

    # ── 3. 刷新字体缓存 ──
    if _need_fc_cache:
        try:
            subprocess.run(["fc-cache", "-f"], capture_output=True, timeout=30)
            if verbose:
                print("  [+] Font cache refreshed")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

    # 最终状态
    if verbose:
        emoji_ok = _has_emoji_font_linux()
        print(f"  [{'=' if emoji_ok else '!'}] Emoji font: {'available' if emoji_ok else 'NOT available (emoji will show as ASCII art)'}")


def _try_apt_install(pkg: str, verbose: bool = True) -> bool:
    """尝试通过系统包管理器安装指定包（支持 apt/yum/dnf），返回是否成功"""
    # 按优先级尝试不同包管理器
    for manager in ["apt", "yum", "dnf"]:
        if _try_package_install(pkg, manager, verbose):
            return True

    # yum/dnf 下的中文字体包名与 apt 不同，尝试映射
    _yum_font_map = {
        "fonts-noto-cjk": "google-noto-sans-cjk-sc-fonts",
        "fonts-noto-cjk-extra": "google-noto-sans-cjk-sc-fonts",
        "fonts-wqy-microhei": "wqy-microhei-fonts",
        "fonts-wqy-zenhei": "wqy-zenhei-fonts",
        "fonts-symbola": "gdouros-symbola-fonts",
        "fonts-noto-color-emoji": "google-noto-emoji-color-fonts",
    }
    yum_pkg = _yum_font_map.get(pkg)
    if yum_pkg and yum_pkg != pkg:
        for manager in ["yum", "dnf"]:
            if _try_package_install(yum_pkg, manager, verbose):
                return True

    if verbose:
        print(f"  [!] Auto-install {pkg} failed (no working package manager)")
        print(f"      Manual: sudo apt-get install -y {pkg}")
        print(f"           or: sudo yum install -y {_yum_font_map.get(pkg, pkg)}")
    return False

# ── 日志轮转 ──────────────────────────────────────────────────

def get_rotating_logger(name: str, log_file: str,
                        max_bytes: int = 5 * 1024 * 1024,
                        backup_count: int = 3) -> "logging.Logger":
    """获取带轮转的 logger
    每个日志文件最大 max_bytes (默认 5MB)，保留 backup_count 个备份。
    总占用 <= max_bytes * (backup_count + 1)
    """
    import logging
    from logging.handlers import RotatingFileHandler

    logger = logging.getLogger(name)
    # 避免重复添加 handler
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count,
        encoding="utf-8"
    )
    handler.setFormatter(logging.Formatter(
        '[%(asctime)s][%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    logger.addHandler(handler)

    # 同时输出到 stdout
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter(
        '[%(asctime)s][%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    logger.addHandler(console)

    return logger

# ── 信号处理 ─────────────────────────────────────────────────

def register_signal_handlers(handler):
    """注册退出信号处理器
    Linux  : SIGTERM + SIGINT
    Windows: SIGTERM + SIGINT + SIGBREAK
    """
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)
    if is_windows() and hasattr(signal, 'SIGBREAK'):
        signal.signal(signal.SIGBREAK, handler)


# ── tkinter 可用性检测与自动安装 ─────────────────────────────

def check_tkinter_available() -> bool:
    """检测当前 Python 是否有 tkinter 模块可用"""
    try:
        import tkinter
        return True
    except ImportError:
        return False


def ensure_tkinter_installed(verbose: bool = True) -> bool:
    """检测并自动安装 python3-tkinter（仅 Linux 有效）。

    Dashboard (dashboard_v3.py) 依赖 tkinter 进行窗口渲染。
    在最小化容器环境中 python3-tkinter 通常未预装，
    导致 dashboard 启动即 ImportError 崩溃。

    安装策略（按优先级）：
    1. 检查 tkinter 是否已可用 → 直接返回
    2. apt-get install python3-tk（Debian/Ubuntu 系）
    3. yum install -y python3-tkinter / tk（RHEL/CentOS 系）
    4. 都失败 → 打印手动安装指引

    Windows/macOS 下 tkinter 随 Python 安装自带，直接跳过。

    Returns:
        True 如果 tkinter 可用，False 如果安装失败
    """
    if is_windows() or is_mac():
        return True

    # 已有 tkinter 则跳过
    if check_tkinter_available():
        if verbose:
            print("  [=] tkinter available")
        return True

    if verbose:
        print("  [!] tkinter not found, attempting install...")

    # 尝试 apt-get (Debian/Ubuntu)
    if _try_package_install("python3-tk", "apt", verbose):
        if check_tkinter_available():
            if verbose:
                print("  [+] tkinter installed successfully (apt)")
            return True

    # 尝试 yum (RHEL/CentOS)
    # python3-tkinter 是 CentOS 7/8 的包名，tk 在某些发行版中也有效
    for pkg in ["python3-tkinter", "tk"]:
        if _try_package_install(pkg, "yum", verbose):
            if check_tkinter_available():
                if verbose:
                    print(f"  [+] tkinter installed successfully (yum: {pkg})")
                return True

    # 尝试 dnf (Fedora/RHEL 8+)
    for pkg in ["python3-tkinter", "tk"]:
        if _try_package_install(pkg, "dnf", verbose):
            if check_tkinter_available():
                if verbose:
                    print(f"  [+] tkinter installed successfully (dnf: {pkg})")
                return True

    if verbose:
        print("  [!] Failed to auto-install tkinter")
        print("      Manual install options:")
        print("        Debian/Ubuntu: sudo apt-get install -y python3-tk")
        print("        CentOS/RHEL:  sudo yum install -y python3-tkinter")
        print("        Fedora:       sudo dnf install -y python3-tkinter")
    return False


def _try_package_install(pkg: str, manager: str, verbose: bool = True) -> bool:
    """尝试通过指定的包管理器安装包。

    Args:
        pkg: 包名
        manager: 包管理器名 ("apt", "yum", "dnf")
        verbose: 是否打印日志

    Returns:
        True 如果安装命令成功执行（returncode == 0）
    """
    # 检查包管理器是否存在
    manager_cmd = "apt-get" if manager == "apt" else manager
    try:
        check = subprocess.run(
            ["which", manager_cmd], capture_output=True, text=True
        )
        if check.returncode != 0:
            return False
    except (FileNotFoundError, OSError):
        return False

    # 构建安装命令
    if manager == "apt":
        install_cmd = ["sudo", "-n", "apt-get", "install", "-y", pkg]
    else:
        install_cmd = ["sudo", "-n", manager_cmd, "install", "-y", pkg]

    try:
        result = subprocess.run(
            install_cmd, capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            if verbose:
                print(f"  [+] {pkg} installed via {manager_cmd}")
            return True
        else:
            if verbose:
                print(f"  [!] {manager_cmd} install {pkg} failed (exit {result.returncode})")
            return False
    except (FileNotFoundError, subprocess.TimeoutExpired, PermissionError) as e:
        if verbose:
            print(f"  [!] {manager_cmd} install error: {e}")
        return False
