# -*- coding: utf-8 -*-
"""
pixel-art-processing 部署脚本 / Deploy Script

基于 FrameRonin: https://github.com/systemchester/FrameRonin

用法 / Usage:
    python deploy.py                    # 交互式菜单
    python deploy.py status             # 查看状态
    python deploy.py start [backend]    # 启动 (backend|worker|all)
    python deploy.py stop [backend]     # 停止 (backend|worker|all)
    python deploy.py restart [backend]  # 重启
    python deploy.py check              # 检查环境依赖

依赖 / Dependencies:
    - Python 3.10+
    - FFmpeg (ffprobe, ffmpeg) - 必须 / Required
    - Redis (可选 for worker, 默认内存模式 / in-memory by default)
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

# =============================================================================
# 配置 / Configuration
# =============================================================================

SKILL_DIR = Path(__file__).parent.parent  # skill根目录
FRAME_RONIN_DIR = SKILL_DIR.parent / "pixel-art-processing-reference"
BACKEND_DIR = FRAME_RONIN_DIR / "backend"
FRONTEND_DIR = FRAME_RONIN_DIR / "frontend"

API_HOST = "127.0.0.1"
API_PORT = 8200  # 避免与群晖5000冲突
API_URL = f"http://{API_HOST}:{API_PORT}"

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
USE_REDIS = os.getenv("USE_REDIS", "false").lower() == "true"

# 进程存储 / Process storage
STATE_FILE = Path(__file__).parent / ".deploy_state.json"


# =============================================================================
# 工具函数 / Utilities
# =============================================================================

def log(msg: str, level: str = "INFO"):
    """打印日志 / Print log"""
    prefix = {"INFO": "✅", "WARN": "⚠️", "ERROR": "❌", "OK": "✅"}
    print(f"{prefix.get(level, 'ℹ️')} {msg}")


def run_cmd(cmd: list[str], cwd: Path | None = None, capture: bool = True, timeout: int = 30) -> subprocess.CompletedProcess:
    """执行命令 / Run command"""
    kwargs = {"cwd": cwd or BACKEND_DIR, "capture_output": capture, "text": True, "timeout": timeout}
    return subprocess.run(cmd, **kwargs)


def load_state() -> dict:
    """加载部署状态 / Load deploy state"""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def save_state(state: dict):
    """保存部署状态 / Save deploy state"""
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def is_port_in_use(port: int) -> bool:
    """检查端口是否被占用 / Check if port is in use"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def find_ffmpeg() -> Path | None:
    """查找FFmpeg路径 / Find FFmpeg path"""
    for name in ["ffmpeg", "ffmpeg.exe", "C:\\workspace\\ffmpeg\\win\\ffmpeg.exe"]:
        try:
            result = subprocess.run(
                [name, "-version"], capture_output=True, timeout=5
            )
            if result.returncode == 0:
                return Path(shutil.which(name) or name)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    
    # 检查常见安装路径 / Check common install paths
    common_paths = [
        Path("C:\\workspace\\ffmpeg\\win\\ffmpeg.exe"),
        Path("C:\\ffmpeg\\bin\\ffmpeg.exe"),
        Path("C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe"),
    ]
    for p in common_paths:
        if p.exists():
            return p
    return None


def check_redis() -> bool:
    """检查Redis是否可用 / Check if Redis is available"""
    try:
        import redis
        r = redis.from_url(REDIS_URL)
        r.ping()
        return True
    except Exception:
        return False


def wait_for_api(url: str = API_URL, timeout: int = 30) -> bool:
    """等待API启动 / Wait for API to start"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(f"{url}/docs", timeout=2):
                return True
        except urllib.error.URLError:
            time.sleep(1)
    return False


# =============================================================================
# 环境检查 / Environment Check
# =============================================================================

def check_environment():
    """检查部署环境 / Check deployment environment"""
    print("\n" + "=" * 50)
    print("🔍 环境检查 / Environment Check")
    print("=" * 50)
    
    errors = []
    
    # Python版本 / Python version
    py_ver = sys.version_info
    log(f"Python: {py_ver.major}.{py_ver.minor}.{py_ver.micro}", "OK" if py_ver >= (3, 10) else "ERROR")
    if py_ver < (3, 10):
        errors.append("Python 3.10+ required")
    
    # FFmpeg
    ffmpeg_path = find_ffmpeg()
    if ffmpeg_path:
        log(f"FFmpeg: {ffmpeg_path}", "OK")
        # 检查 ffprobe / Check ffprobe
        ffprobe_path = ffmpeg_path.parent / "ffprobe.exe"
        if ffprobe_path.exists() or shutil.which("ffprobe"):
            log("FFprobe: available", "OK")
        else:
            log("FFprobe: NOT FOUND (frame extraction will fail)", "WARN")
    else:
        log("FFmpeg: NOT FOUND", "ERROR")
        errors.append("FFmpeg not found. Install from: https://ffmpeg.org/download.html")
    
    # Redis
    redis_ok = check_redis()
    if redis_ok:
        log(f"Redis: {REDIS_URL}", "OK")
    else:
        log(f"Redis: NOT AVAILABLE (worker will run in-memory mode)", "WARN")
        log(f"  → Set USE_REDIS=true or install Redis for async job queue", "WARN")
    
    # 依赖检查 / Dependencies check
    try:
        import fastapi
        import PIL
        import rembg
        import cv2
        log("Python packages: all installed", "OK")
    except ImportError as e:
        log(f"Python packages: MISSING - {e}", "ERROR")
        errors.append(f"Missing package: {e}")
    
    # 端口检查 / Port check
    port_in_use = is_port_in_use(API_PORT)
    if port_in_use:
        log(f"Port {API_PORT}: already in use", "WARN")
    else:
        log(f"Port {API_PORT}: available", "OK")
    
    # 参考项目检查 / Reference project check
    if FRAME_RONIN_DIR.exists() and (FRAME_RONIN_DIR / "backend").exists():
        log(f"FrameRonin reference: {FRAME_RONIN_DIR}", "OK")
    else:
        log(f"FrameRonin reference: NOT FOUND at {FRAME_RORONIN_DIR}", "WARN")
        log("  → Backend will use bundled code from this skill", "WARN")
    
    print("=" * 50)
    if errors:
        log(f"检查完成，{len(errors)} 个错误 / {len(errors)} error(s) found", "ERROR")
        for err in errors:
            print(f"   • {err}")
        return False
    else:
        log("环境检查通过 / Environment check passed", "OK")
        return True


# =============================================================================
# 后端启动/停止 / Backend Start/Stop
# =============================================================================

def start_backend():
    """启动FastAPI后端 / Start FastAPI backend"""
    if is_port_in_use(API_PORT):
        log(f"Backend already running on port {API_PORT}", "WARN")
        return
    
    # 准备环境 / Prepare environment
    env = os.environ.copy()
    env["UPLOAD_DIR"] = str(SKILL_DIR / "workspace" / "uploads")
    env["OUTPUT_DIR"] = str(SKILL_DIR / "workspace" / "outputs")
    env["TEMP_DIR"] = str(SKILL_DIR / "workspace" / "temp")
    
    # 创建工作目录 / Create workspace dirs
    for d in ["uploads", "outputs", "temp"]:
        (SKILL_DIR / "workspace" / d).mkdir(parents=True, exist_ok=True)
    
    # 启动uvicorn / Start uvicorn
    cmd = [
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--host", API_HOST,
        "--port", str(API_PORT),
        "--reload",
    ]
    
    log(f"Starting backend: {' '.join(cmd)}", "INFO")
    subprocess.Popen(cmd, cwd=BACKEND_DIR, env=env)
    
    # 等待启动 / Wait for startup
    if wait_for_api():
        log(f"Backend started: {API_URL}", "OK")
        log(f"API docs: {API_URL}/docs", "OK")
    else:
        log(f"Backend failed to start within 30s", "ERROR")


def stop_backend():
    """停止FastAPI后端 / Stop FastAPI backend"""
    import signal
    import psutil
    
    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            cmdline = proc.info.get("cmdline") or []
            if any("uvicorn" in str(c) and "app.main:app" in str(c) for c in cmdline):
                log(f"Stopping backend (PID {proc.pid})", "INFO")
                os.kill(proc.pid, signal.SIGTERM)
        except (psutil.NoSuchProcess, PermissionError):
            pass
    
    if is_port_in_use(API_PORT):
        log(f"Port {API_PORT} still in use, trying force kill", "WARN")
        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                cmdline = proc.info.get("cmdline") or []
                if any("uvicorn" in str(c) for c in cmdline):
                    os.kill(proc.pid, signal.SIGKILL)
            except:
                pass
    
    log("Backend stopped", "OK")


def start_worker():
    """启动RQ Worker / Start RQ worker"""
    if not check_redis():
        log("Redis not available. Worker requires Redis.", "ERROR")
        return
    
    cmd = [
        sys.executable, "-m", "rq", "worker",
        "pixelwork",
        "--url", REDIS_URL,
    ]
    
    log(f"Starting worker: {' '.join(cmd)}", "INFO")
    subprocess.Popen(cmd, cwd=BACKEND_DIR)
    log("Worker started", "OK")


def status():
    """查看部署状态 / Show deployment status"""
    state = load_state()
    
    print("\n" + "=" * 50)
    print("📊 部署状态 / Deployment Status")
    print("=" * 50)
    
    # API状态 / API status
    try:
        with urllib.request.urlopen(f"{API_URL}/docs", timeout=2):
            log(f"Backend API: {API_URL} - RUNNING", "OK")
    except urllib.error.URLError:
        log(f"Backend API: {API_URL} - STOPPED", "WARN")
    
    # Redis状态 / Redis status
    redis_ok = check_redis()
    log(f"Redis: {'AVAILABLE' if redis_ok else 'NOT AVAILABLE'}", "OK" if redis_ok else "WARN")
    
    # FFmpeg状态 / FFmpeg status
    ffmpeg_path = find_ffmpeg()
    log(f"FFmpeg: {'FOUND' if ffmpeg_path else 'NOT FOUND'}", "OK" if ffmpeg_path else "ERROR")
    
    print("=" * 50)


# =============================================================================
# 入口 / Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="pixel-art-processing deploy script / 部署脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd")
    
    sub.add_parser("check", help="检查环境 / Check environment")
    sub.add_parser("status", help="查看状态 / Show status")
    
    start_parser = sub.add_parser("start", help="启动服务 / Start services")
    start_parser.add_argument("target", nargs="?", default="all", choices=["backend", "worker", "all"])
    
    stop_parser = sub.add_parser("stop", help="停止服务 / Stop services")
    stop_parser.add_argument("target", nargs="?", default="all", choices=["backend", "worker", "all"])
    
    restart_parser = sub.add_parser("restart", help="重启服务 / Restart services")
    restart_parser.add_argument("target", nargs="?", default="all", choices=["backend", "worker", "all"])
    
    args = parser.parse_args()
    
    if args.cmd == "check" or args.cmd is None:
        check_environment()
    elif args.cmd == "status":
        status()
    elif args.cmd == "start":
        if args.target in ("backend", "all"):
            start_backend()
        if args.target in ("worker", "all"):
            start_worker()
    elif args.cmd == "stop":
        if args.target in ("backend", "all"):
            stop_backend()
        # worker通过后台进程管理，这里不处理
    elif args.cmd == "restart":
        if args.target in ("backend", "all"):
            stop_backend()
            time.sleep(1)
            start_backend()
        if args.target in ("worker", "all"):
            start_worker()


if __name__ == "__main__":
    main()
