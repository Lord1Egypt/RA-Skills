#!/usr/bin/env python3
"""行业雷达（Industry Radar）本地启动器 — 跨平台 Python 版。

流程（幂等，可反复执行）：
  1. 在 Skill 根目录创建 .venv 虚拟环境（已存在则直接复用）
  2. 安装 app/backend/requirements.txt 依赖（已安装则秒过）
  3. 在 app/backend 目录下启动 uvicorn（main:app）

用法：
    python3 scripts/run_local.py                 # 默认 http://127.0.0.1:8000
    python3 scripts/run_local.py --port 8001     # 自定义端口
    python3 scripts/run_local.py --host 0.0.0.0  # 允许局域网访问
    python3 scripts/run_local.py --skip-install  # 跳过依赖安装直接启动

启动成功后：
    Web 界面   http://127.0.0.1:8000   （内置演示账号 demo / demo）
    API 文档   http://127.0.0.1:8000/docs

停止服务：终端按 Ctrl+C。
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
BACKEND_DIR = SKILL_ROOT / "app" / "backend"
VENV_DIR = SKILL_ROOT / ".venv"
REQUIREMENTS = BACKEND_DIR / "requirements.txt"


def venv_python() -> Path:
    """虚拟环境内的 Python 解释器路径（兼容 Windows / macOS / Linux）。"""
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def run_cmd(cmd: list) -> int:
    print("+", " ".join(str(c) for c in cmd))
    return subprocess.run([str(c) for c in cmd]).returncode


def main() -> int:
    ap = argparse.ArgumentParser(description="行业雷达（Industry Radar）本地启动器")
    ap.add_argument("--host", default="127.0.0.1", help="监听地址，默认 127.0.0.1")
    ap.add_argument("--port", type=int, default=8000, help="监听端口，默认 8000")
    ap.add_argument("--skip-install", action="store_true", help="跳过依赖安装")
    args = ap.parse_args()

    if sys.version_info < (3, 9):
        print("[错误] 需要 Python 3.9+，当前 " + sys.version.split()[0], file=sys.stderr)
        return 1
    if not BACKEND_DIR.exists():
        print(f"[错误] 未找到后端目录：{BACKEND_DIR}", file=sys.stderr)
        return 1

    py = venv_python()
    if not py.exists():
        print(f"[1/3] 创建虚拟环境 {VENV_DIR} ...")
        if run_cmd([sys.executable, "-m", "venv", VENV_DIR]) != 0:
            print("[错误] venv 创建失败，请确认已安装 Python 3.9+", file=sys.stderr)
            return 1
    else:
        print(f"[1/3] 复用虚拟环境 {VENV_DIR}")

    if args.skip_install:
        print("[2/3] 跳过依赖安装")
    else:
        print("[2/3] 安装依赖（已安装则秒过）...")
        if run_cmd([py, "-m", "pip", "install", "-q", "-r", REQUIREMENTS]) != 0:
            print("[错误] 依赖安装失败，请检查网络后重试，或手动执行：", file=sys.stderr)
            print(f"  {py} -m pip install -r {REQUIREMENTS}", file=sys.stderr)
            return 1

    print(f"[3/3] 启动服务 http://{args.host}:{args.port} （演示账号 demo / demo）")
    print("      首次启动会自动初始化 SQLite 数据库并预置示例订阅，浏览器访问上述地址即可使用。")
    print("      停止服务：Ctrl+C")
    os.chdir(BACKEND_DIR)
    return subprocess.run([
        py, "-m", "uvicorn", "main:app",
        "--host", args.host, "--port", str(args.port),
    ]).returncode


if __name__ == "__main__":
    sys.exit(main())
