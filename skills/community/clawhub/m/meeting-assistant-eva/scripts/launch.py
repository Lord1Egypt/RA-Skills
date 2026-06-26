#!/usr/bin/env python3
"""
Meeting Assistant Launcher — 一键启动入口

功能：
  1. 自动检测并启动 Vexa Docker 服务
  2. 等待 Vexa 健康就绪
  3. 打印就绪提示，等待用户提供会议链接
  4. 加入会议后进入 agent 交互循环

用法：
  python launch.py                     # 启动并等待用户输入 URL
  python launch.py "https://zoom..."   # 直接加入会议
  python launch.py --status            # 检查 Vexa 状态
  python launch.py --stop-vexa         # 停止 Vexa 服务

架构说明：
  本程序作为「数据层」——负责加入会议、采集音视频、收发聊天。
  分析层由上游 Agent (Claude Code) 担任，通过读取 session 文件和调用工具完成。
"""

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = SKILL_DIR / "config.json"
STATE_FILE  = SKILL_DIR / ".assistant_state.json"

# ─── Config ──────────────────────────────────────────────────────────────────

def load_config() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)

def get_python() -> str:
    """Return the conda env Python executable path."""
    config = load_config()
    python = config.get("conda_env", {}).get("python", "")
    if python and Path(python).exists():
        return python
    # Try to find via conda on Windows
    conda_base = _find_conda_base()
    if conda_base:
        candidate = Path(conda_base) / "envs" / "meeting-assistant" / "python.exe"
        if candidate.exists():
            return str(candidate)
    return sys.executable

def _find_conda_base() -> str | None:
    """Search common conda installation locations."""
    # From config
    config = load_config()
    python_path = config.get("conda_env", {}).get("python", "")
    if python_path:
        p = Path(python_path)
        # Walk up to find conda base: .../anaconda/envs/xxx/python.exe → .../anaconda
        for parent in p.parents:
            if (parent / "conda.exe").exists() or (parent / "Scripts" / "conda.exe").exists():
                return str(parent)

    # Common Windows paths
    candidates = [
        r"D:\program\codesupport\anaconda",
        r"C:\ProgramData\anaconda3",
        r"C:\Users\zeron\anaconda3",
        r"C:\Users\zeron\miniconda3",
        os.path.expanduser("~/anaconda3"),
        os.path.expanduser("~/miniconda3"),
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    return None

# ─── Docker / Vexa ────────────────────────────────────────────────────────────

def _find_docker() -> str | None:
    """Find docker executable on Windows or Linux."""
    # Check system PATH first
    docker = shutil.which("docker")
    if docker:
        return docker

    # Check config for explicit docker path
    try:
        cfg = load_config()
        cfg_docker = cfg.get("docker", {}).get("exe", "")
        if cfg_docker and Path(cfg_docker.replace("/", "\\")).exists():
            return cfg_docker.replace("/", "\\")
    except Exception:
        pass

    # Windows common locations
    win_paths = [
        r"C:\Program Files\Docker\Docker\resources\bin\docker.exe",
        r"C:\ProgramData\DockerDesktop\version-bin\docker.exe",
        r"C:\Windows\System32\docker.exe",
    ]
    for p in win_paths:
        if Path(p).exists():
            return p

    # Try via PowerShell (Docker Desktop may add to PATH only for PS)
    try:
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-Command",
             "(Get-Command docker -ErrorAction SilentlyContinue).Source"],
            capture_output=True, text=True, timeout=5
        )
        path = result.stdout.strip()
        if path and Path(path).exists():
            return path
    except Exception:
        pass

    return None

def _find_docker_compose() -> list[str] | None:
    """Return docker compose command (as list). Supports both docker-compose and docker compose."""
    docker = _find_docker()
    if not docker:
        return None

    # Modern: docker compose (plugin)
    try:
        result = subprocess.run(
            [docker, "compose", "version"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return [docker, "compose"]
    except Exception:
        pass

    # Legacy: docker-compose (standalone)
    dc = shutil.which("docker-compose")
    if not dc:
        dc_win = shutil.which("docker-compose.exe")
        if dc_win:
            dc = dc_win
    if dc:
        return [dc]

    return None

def start_vexa(verbose=True) -> bool:
    """
    Start Vexa Docker services (postgres + vexa bot).
    Returns True if successful or already running.
    """
    if verbose:
        print("[Vexa] Checking Docker...")

    docker = _find_docker()
    if not docker:
        print("[Vexa] ERROR: Docker not found.")
        print("[Vexa] Please install Docker Desktop: https://www.docker.com/products/docker-desktop/")
        print("[Vexa] After installing, run: docker compose up -d")
        return False

    compose_cmd = _find_docker_compose()
    if not compose_cmd:
        print("[Vexa] ERROR: docker compose not found.")
        return False

    if verbose:
        print(f"[Vexa] Docker found: {docker}")

    # Check if already running
    config = load_config()
    vexa_url = config.get("bot", {}).get("vexa_url", "http://localhost:8056")
    if _check_vexa_health(vexa_url):
        if verbose:
            print(f"[Vexa] Already running at {vexa_url}")
        return True

    # Start via docker compose
    compose_file = SKILL_DIR / "docker-compose.yml"
    if not compose_file.exists():
        print(f"[Vexa] docker-compose.yml not found at {compose_file}")
        return False

    if verbose:
        print("[Vexa] Starting services (postgres + vexa)...")

    try:
        result = subprocess.run(
            compose_cmd + ["up", "-d"],
            cwd=str(SKILL_DIR),
            capture_output=True,
            text=True,
            timeout=120,
        )
        if verbose:
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)

        if result.returncode != 0:
            print(f"[Vexa] docker compose up failed (exit {result.returncode})")
            return False
    except subprocess.TimeoutExpired:
        print("[Vexa] docker compose timed out")
        return False
    except Exception as e:
        print(f"[Vexa] Error starting Vexa: {e}")
        return False

    # Wait for Vexa to be healthy
    if verbose:
        print("[Vexa] Waiting for Vexa to be ready", end="", flush=True)
    for i in range(30):
        if _check_vexa_health(vexa_url):
            if verbose:
                print(" OK")
                print(f"[Vexa] Ready at {vexa_url}")
            return True
        if verbose:
            print(".", end="", flush=True)
        time.sleep(2)

    if verbose:
        print(" TIMEOUT")
        print("[Vexa] Vexa did not become ready in time. Check: docker compose logs vexa")
    return False

def stop_vexa() -> bool:
    """Stop Vexa Docker services."""
    compose_cmd = _find_docker_compose()
    if not compose_cmd:
        print("[Vexa] docker compose not found")
        return False

    compose_file = SKILL_DIR / "docker-compose.yml"
    result = subprocess.run(
        compose_cmd + ["down"],
        cwd=str(SKILL_DIR),
        capture_output=True, text=True, timeout=30,
    )
    print(result.stdout or result.stderr)
    return result.returncode == 0

def _check_vexa_health(url: str) -> bool:
    """Return True if Vexa API is responding."""
    try:
        import requests
        resp = requests.get(f"{url}/health", timeout=3)
        return resp.status_code < 500
    except Exception:
        return False

def vexa_status() -> dict:
    """Get Vexa status info."""
    config = load_config()
    vexa_url = config.get("bot", {}).get("vexa_url", "http://localhost:8056")
    docker = _find_docker()
    compose_cmd = _find_docker_compose()

    status = {
        "docker_found": docker is not None,
        "docker_path": docker,
        "compose_found": compose_cmd is not None,
        "vexa_url": vexa_url,
        "vexa_running": _check_vexa_health(vexa_url),
    }

    if docker:
        try:
            result = subprocess.run(
                [docker, "ps", "--filter", "name=vexa", "--format", "{{.Names}}: {{.Status}}"],
                capture_output=True, text=True, timeout=5
            )
            status["containers"] = result.stdout.strip().split("\n") if result.stdout.strip() else []
        except Exception:
            status["containers"] = []

    return status

# ─── Bot Operations (wrapper around meeting_bot.py CLI) ──────────────────────

def _run_bot_cmd(*args, timeout=30) -> tuple[int, str, str]:
    """Run a meeting_bot.py command using conda Python. Returns (returncode, stdout, stderr)."""
    python = get_python()
    bot_script = Path(__file__).parent / "meeting_bot.py"
    cmd = [python, str(bot_script)] + list(args)

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(SKILL_DIR),
        env={**os.environ},
    )
    return result.returncode, result.stdout, result.stderr

def join_meeting(url: str, bot_name: str = None, mode: str = "general") -> dict:
    """Join a meeting and return bot info."""
    args = ["join", url]
    if bot_name:
        args += ["--name", bot_name]

    rc, out, err = _run_bot_cmd(*args, timeout=60)
    output = (out + err).strip()
    print(output)

    success = rc == 0 or "Bot ID:" in output or "Joined" in output.lower()
    bot_id = None
    for line in output.split("\n"):
        if "Bot ID:" in line:
            bot_id = line.split("Bot ID:")[-1].strip()
            break

    return {"success": success, "bot_id": bot_id, "output": output}

def send_chat(message: str) -> bool:
    """Send a message to the meeting chat."""
    rc, out, err = _run_bot_cmd("chat", message, timeout=15)
    print(f"[Chat→Meeting] {message[:80]}")
    return rc == 0

def read_chat() -> list[str]:
    """Read meeting chat messages."""
    rc, out, err = _run_bot_cmd("read-chat", timeout=15)
    lines = [l for l in out.strip().split("\n") if l.strip()]
    return lines

def get_transcript() -> str:
    """Get current meeting transcript."""
    rc, out, err = _run_bot_cmd("transcript", timeout=15)
    return out.strip()

def take_screenshot(save_path: str = None) -> str | None:
    """Take a meeting screenshot and return file path."""
    args = ["screenshot"]
    if save_path:
        args += ["--output", save_path]
    rc, out, err = _run_bot_cmd(*args, timeout=20)
    combined = out + err
    for line in combined.split("\n"):
        if "Saved:" in line:
            return line.split("Saved:")[-1].strip()
        if ".png" in line:
            return line.strip()
    return None

def leave_meeting() -> bool:
    """Leave the current meeting."""
    rc, out, err = _run_bot_cmd("leave", timeout=15)
    print(out + err)
    return rc == 0

def bot_status() -> str:
    """Get bot status."""
    rc, out, err = _run_bot_cmd("status", timeout=10)
    return (out + err).strip()

def check_setup() -> bool:
    """Run setup check and return True if Vexa is reachable."""
    rc, out, err = _run_bot_cmd("setup", timeout=10)
    print(out + err)
    return rc == 0

# ─── Interactive Agent Mode ───────────────────────────────────────────────────

def print_banner():
    print("\n" + "="*60)
    print("  OpenClaw Meeting Assistant — Ready")
    print("="*60)
    print("  Python:", get_python())
    config = load_config()
    print("  Vexa:  ", config.get("bot", {}).get("vexa_url", "http://localhost:8056"))
    print("="*60)
    print()
    print("  Bot will join as: OpenClaw 助手")
    print()
    print("  用户交互方式：在会议聊天框直接输入问题")
    print("  Agent 将通过 Claude AI 实时回答")
    print()

def wait_for_url() -> str:
    """Interactively wait for the user to provide a meeting URL."""
    print("[Ready] 请提供会议链接（Zoom/Teams/Google Meet）：")
    print("  例如: https://zoom.us/j/123456789?pwd=xxx")
    print("  或直接输入会议 ID")
    print()
    while True:
        try:
            url = input("Meeting URL > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n[Exit] 用户取消")
            sys.exit(0)

        if not url:
            continue

        # Accept raw meeting IDs too
        if url.isdigit() or (len(url) == 11 and url.replace("-", "").isdigit()):
            url = f"https://zoom.us/j/{url}"

        if any(k in url for k in ["zoom.us", "teams.microsoft", "meet.google", "https://", "http://"]):
            return url
        else:
            print(f"  [?] 无法识别的格式，请确认是 Zoom/Teams/Meet 链接")

def interactive_loop(url: str, mode: str = "general"):
    """
    Main interactive mode: I (Claude Code agent) am the controller.
    The bot handles Vexa/meeting connection; I handle analysis.
    """
    print(f"\n[Joining] {url}")
    print(f"[Mode] {mode}")
    result = join_meeting(url, mode=mode)

    if not result["success"]:
        print(f"\n[ERROR] 无法加入会议: {result['output']}")
        return

    print(f"\n[Joined] Bot ID: {result['bot_id']}")
    print("\n" + "="*60)
    print("  Bot 已加入会议！")
    print("  我（Claude Code）现在作为 Agent 开始监控会议")
    print()
    print("  会议参与者可在聊天框输入问题")
    print("  Ctrl+C 结束会话")
    print("="*60 + "\n")

    # Brief greeting via chat
    send_chat("📝 OpenClaw 助手已加入会议。您可以在聊天中直接提问，我会实时回答！")

    # Print info for the agent (me) to use
    print("\n[Agent Instructions]")
    print("  现在可以调用以下操作：")
    print("  - take_screenshot()   → 截图分析会议画面")
    print("  - get_transcript()    → 读取转录内容")
    print("  - read_chat()         → 读取聊天记录")
    print("  - send_chat('...')    → 向会议聊天发消息")
    print("  - leave_meeting()     → 离开会议")
    print()
    print("  会议 session 目录：")
    print(f"  {SKILL_DIR}/recordings/bot_*/")
    print()

# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Meeting Assistant Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launch.py                              # Start Vexa + wait for URL
  python launch.py "https://zoom.us/j/123"      # Start + join immediately
  python launch.py --status                     # Check Vexa status
  python launch.py --stop-vexa                  # Stop Vexa containers
  python launch.py --no-vexa "https://..."      # Skip Vexa, join directly
        """,
    )
    parser.add_argument("meeting_url", nargs="?", help="Meeting URL to join immediately")
    parser.add_argument("--mode", choices=["general", "medical"], default="general")
    parser.add_argument("--status", action="store_true", help="Check Vexa status and exit")
    parser.add_argument("--stop-vexa", action="store_true", help="Stop Vexa and exit")
    parser.add_argument("--no-vexa", action="store_true", help="Skip Vexa startup (for testing)")
    parser.add_argument("--join-only", action="store_true", help="Join meeting and exit (no interactive loop)")

    args = parser.parse_args()

    # ── Status check ──────────────────────────────────────────────────────
    if args.status:
        st = vexa_status()
        print(json.dumps(st, indent=2, ensure_ascii=False))
        return

    # ── Stop Vexa ─────────────────────────────────────────────────────────
    if args.stop_vexa:
        print("[Vexa] Stopping services...")
        ok = stop_vexa()
        print("[Vexa] Stopped" if ok else "[Vexa] Failed to stop")
        return

    # ── Banner ────────────────────────────────────────────────────────────
    print_banner()

    # ── Start Vexa ────────────────────────────────────────────────────────
    if not args.no_vexa:
        vexa_ok = start_vexa(verbose=True)
        if not vexa_ok:
            print("\n[Warning] Vexa not available. Bot mode requires Vexa Docker.")
            print("  Install Docker Desktop and re-run, or use --no-vexa to skip.")
            ans = input("\n  Continue anyway? (y/N): ").strip().lower()
            if ans != "y":
                sys.exit(1)
    else:
        print("[Vexa] Skipping Vexa startup (--no-vexa)")

    # ── Get URL ───────────────────────────────────────────────────────────
    url = args.meeting_url
    if not url:
        url = wait_for_url()

    # ── Join and run ──────────────────────────────────────────────────────
    if args.join_only:
        result = join_meeting(url, mode=args.mode)
        print(json.dumps(result, ensure_ascii=False))
    else:
        interactive_loop(url, mode=args.mode)


if __name__ == "__main__":
    main()
