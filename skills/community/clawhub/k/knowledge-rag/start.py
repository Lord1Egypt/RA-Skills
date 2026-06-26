#!/usr/bin/env python3
"""
一键启动知识仓库服务

用法：
  .venv/bin/python3 start.py     # 启动后打开网页（推荐）
  python3 start.py               # 也兼容，但需先建 .venv

启动后访问 http://localhost:5777
"""

import os, sys, time, subprocess, signal, webbrowser, json

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
TS_DIR = os.path.join(SKILL_DIR, "web")
PYTHON_API_PORT = 8768
TS_PORT = 5777

RECOMMENDED_MODEL = "qwen3-embedding:8b"
CONFIG_FILE = os.path.expanduser("~/workspace/knowledge/.knowledge-config.json")

processes = []


def get_python():
    """优先使用 .venv 的 python3，否则退回系统 python3"""
    venv_python = os.path.join(SKILL_DIR, ".venv", "bin", "python3")
    if os.path.exists(venv_python):
        return venv_python
    return sys.executable


def print_status(msg, status="info"):
    icons = {"ok": "✅", "wait": "⏳", "err": "❌", "info": "➡️"}
    print(f"  {icons.get(status, '➡️')} {msg}")


def check_port(port):
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", port))
        s.close()
        return False  # 端口空闲
    except OSError:
        return True   # 端口被占用


def wait_for_port(port, timeout=15):
    for _ in range(timeout * 2):
        if check_port(port):
            return True
        time.sleep(0.5)
    return False


def check_environment():
    """启动前环境检测：Ollama、推荐模型、模型匹配"""
    warnings = []

    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            print_status("Ollama 未安装，请从 https://ollama.com/download 安装后重试", "err")
            return False
    except FileNotFoundError:
        print_status("Ollama 未安装，请从 https://ollama.com/download 安装后重试", "err")
        return False
    except Exception as e:
        print_status(f"无法检测 Ollama: {e}", "err")
        return False

    print_status("Ollama 已安装", "ok")

    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
        installed_models = result.stdout
    except Exception:
        warnings.append("无法查询已安装模型")
        installed_models = ""

    cfg_model = None
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, encoding="utf-8") as f:
                cfg = json.load(f)
            cfg_model = cfg.get("embed_model", "")
        except Exception:
            pass

    expected_model = cfg_model or RECOMMENDED_MODEL
    if expected_model in installed_models:
        print_status(f"推荐模型 {expected_model} 已就绪", "ok")
    else:
        base_name = expected_model.split(":")[0]
        if base_name in installed_models:
            print_status(f"检测到 {expected_model} 变体，将使用已安装版本", "ok")
        else:
            print_status(f"推荐模型 {expected_model} 未安装，正在自动下载...", "wait")
            try:
                subprocess.run(["ollama", "pull", expected_model], check=True, timeout=300)
                print_status(f"模型 {expected_model} 下载完成", "ok")
            except Exception as e:
                warnings.append(f"模型下载失败: {e}，请手动运行: ollama pull {expected_model}")

    model_meta_file = os.path.expanduser("~/workspace/knowledge/.rag_data/model_meta.json")
    if os.path.exists(model_meta_file):
        try:
            with open(model_meta_file, encoding="utf-8") as f:
                meta = json.load(f)
            stored_model = meta.get("model", "")
            if stored_model and stored_model != expected_model:
                print_status(f"检测到模型变化: {stored_model} → {expected_model}，需要重新索引", "info")
                warnings.append("模型已变更，请到管理页面点击「重新索引」")
        except Exception:
            pass

    if warnings:
        print()
        for w in warnings:
            print_status(w, "info")

    return True


def start_python_api():
    if check_port(PYTHON_API_PORT):
        print_status(f"Python API 已在端口 {PYTHON_API_PORT} 运行", "ok")
        return True

    print_status("启动 Python API 服务...", "wait")
    script = os.path.join(SCRIPTS_DIR, "knowledge_api.py")
    log_dir = os.path.join(SCRIPTS_DIR, "..", "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "python_api.log")
    proc = subprocess.Popen(
        [get_python(), script, str(PYTHON_API_PORT)],
        stdout=open(log_file, "a"), stderr=subprocess.STDOUT,
    )
    processes.append(proc)

    if wait_for_port(PYTHON_API_PORT):
        print_status(f"Python API 已就绪 (端口 {PYTHON_API_PORT})", "ok")
        return True
    else:
        print_status("Python API 启动超时", "err")
        return False


def start_ts_server():
    if check_port(TS_PORT):
        print_status(f"网页服务已在端口 {TS_PORT} 运行", "ok")
        return True

    if not os.path.isdir(TS_DIR):
        print_status(f"未找到网页项目目录: {TS_DIR}", "err")
        return False

    node_modules = os.path.join(TS_DIR, "node_modules")
    if not os.path.isdir(node_modules):
        print_status("首次启动，正在安装网页依赖...", "wait")
        try:
            subprocess.run(
                ["npm", "install", "--no-audit", "--no-fund"],
                cwd=TS_DIR, check=True, timeout=120,
            )
            print_status("依赖安装完成", "ok")
        except subprocess.TimeoutExpired:
            print_status("npm install 超时，请手动运行: cd web && npm install", "err")
            return False
        except Exception as e:
            print_status(f"npm install 失败: {e}", "err")
            return False

    print_status("启动网页服务...", "wait")
    env = os.environ.copy()
    env["PORT"] = str(TS_PORT)
    proc = subprocess.Popen(
        ["npx", "tsx", "src/server.ts"],
        cwd=TS_DIR, env=env,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    processes.append(proc)

    if wait_for_port(TS_PORT):
        print_status(f"网页服务已就绪 (http://localhost:{TS_PORT})", "ok")
        return True
    else:
        print_status("网页服务启动超时", "err")
        return False


def cleanup(signum=None, frame=None):
    print_status("正在停止服务...", "info")
    for proc in processes:
        try:
            proc.terminate()
            proc.wait(timeout=3)
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass
    print_status("已停止", "ok")
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    only_ts = "--ts" in sys.argv

    print()
    print("  ╔══════════════════════════════════════╗")
    print("  ║     📖 知识仓库 — 一键启动           ║")
    print("  ╚══════════════════════════════════════╝")
    print()

    if not only_ts:
        print("🔍 检测环境...")
        if not check_environment():
            print_status("环境检测未通过，请修复后重试", "err")
            sys.exit(1)
        print()

        if not start_python_api():
            print_status("Python API 启动失败，请检查端口占用", "err")
            sys.exit(1)
    else:
        if not check_port(PYTHON_API_PORT):
            print_status("Python API 未运行，请先启动", "err")
            sys.exit(1)
        print_status("Python API 已就绪 (跳过)", "ok")

    if not start_ts_server():
        print_status("网页服务启动失败", "err")
        sys.exit(1)

    url = f"http://localhost:{TS_PORT}"
    print()
    print(f"  🎉 服务已全部就绪！")
    print(f"     打开 {url}")
    print(f"     按 Ctrl+C 停止所有服务")
    print()

    try:
        import urllib.request
        check_url = f"http://localhost:{PYTHON_API_PORT}/api/stats"
        req = urllib.request.Request(check_url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            idx = data.get("index", {})
            chunks = idx.get("total_chunks", 0)
            source_stats = idx.get("source_stats", {})
            if chunks:
                srcs = "、".join([f"{k}({v})" for k, v in source_stats.items()])
                print(f"  📊 当前索引: {chunks} 段，{len(source_stats)} 个来源 ({srcs})")
                print()
    except Exception:
        pass

    print_status("正在打开浏览器...", "info")

    # WSL 环境 → 用 Windows 默认浏览器打开
    if os.path.exists("/proc/sys/fs/binfmt_misc/WSLInterop") or os.environ.get("WSL_DISTRO_NAME"):
        try:
            subprocess.run(["cmd.exe", "/c", "start", url],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            pass  # 没有 cmd.exe，回退到 webbrowser
    else:
        old_stderr = os.dup(2)
        try:
            with open(os.devnull, "w") as devnull:
                os.dup2(devnull.fileno(), 2)
                webbrowser.open(url)
        finally:
            os.dup2(old_stderr, 2)
            os.close(old_stderr)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup()


if __name__ == "__main__":
    main()
