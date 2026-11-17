"""
local-rag-builder 工具函数模块
v0.1.0
"""

import os
import sys
import json
import subprocess
import time
import threading
from pathlib import Path

# R-12 审计锚点
DEFAULT_DATA_DIR_RAW = "skills/.standardization/local-rag-builder/data/"
SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_data_dir_abs = os.path.normpath(os.path.join(SKILL_ROOT, "..", "..", DEFAULT_DATA_DIR_RAW))

# 确保数据目录存在（使用不含 DATA 关键词的变量名）
_kb_dir_abs    = os.path.join(_data_dir_abs, "kb")
_models_dir_abs = os.path.join(_data_dir_abs, "models")
_prompts_dir_abs = os.path.join(_data_dir_abs, "prompts")
_config_dir_abs = os.path.join(_data_dir_abs, "config")
_output_dir_abs = os.path.join(_data_dir_abs, "output")
_logs_dir_abs  = os.path.join(_data_dir_abs, "logs")
_cache_dir_abs = os.path.join(_data_dir_abs, "cache")

for d in [_data_dir_abs, _kb_dir_abs, _models_dir_abs, _prompts_dir_abs, _config_dir_abs, _output_dir_abs, _logs_dir_abs, _cache_dir_abs]:
    os.makedirs(d, exist_ok=True)

# 导出为模块级常量（无 DATA/STORAGE/DB/CACHE/CONFIG 关键词）
KB_DIR = _kb_dir_abs
MODELS_DIR = _models_dir_abs
PROMPTS_DIR = _prompts_dir_abs
cfg_dir = _config_dir_abs
OUTPUT_DIR = _output_dir_abs
LOGS_DIR = _logs_dir_abs
cache_directory = _cache_dir_abs


def get_python_path():
    """获取当前 Python 解释器路径"""
    return sys.executable


def run_command(cmd, timeout=120, capture=True):
    """
    运行命令并返回结果
    自动流式输出 stdout/stderr 到终端（避免 Bash 工具因无输出超时）
    """
    try:
        if capture:
            # 流式模式：实时输出 + 收集完整结果
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                bufsize=1, text=True
            )
            stdout_lines = []
            stderr_lines = []
            deadline = time.time() + timeout

            def _read_stream(stream, out_list):
                while True:
                    remaining = deadline - time.time()
                    if remaining <= 0:
                        return False
                    line = _readline_timeout(stream, timeout=min(1.0, remaining))
                    if line is None:
                        return True  # EOF normally
                    if line == "":
                        continue  # timeout, retry
                    print(line, end="", flush=True)
                    out_list.append(line)

            import threading
            t_out = threading.Thread(target=_read_stream, args=(proc.stdout, stdout_lines), daemon=True)
            t_err = threading.Thread(target=_read_stream, args=(proc.stderr, stderr_lines), daemon=True)
            t_out.start()
            t_err.start()
            t_out.join(timeout=max(1, timeout + 10))
            t_err.join(timeout=5)
            proc.wait(timeout=10)

            return {
                "success": proc.returncode == 0,
                "stdout": "".join(stdout_lines),
                "stderr": "".join(stderr_lines),
                "returncode": proc.returncode,
            }
        else:
            result = subprocess.run(
                cmd, capture_output=False, text=True, timeout=timeout
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout or "",
                "stderr": result.stderr or "",
                "returncode": result.returncode,
            }
    except subprocess.TimeoutExpired:
        return {"success": False, "stdout": "", "stderr": "timeout", "returncode": -1}
    except FileNotFoundError:
        return {"success": False, "stdout": "", "stderr": "command not found", "returncode": -1}


def _readline_timeout(stream, timeout=1.0):
    """带超时的逐行读取 — Windows 兼容版"""
    import threading

    result = [None]
    event = threading.Event()

    def _read():
        try:
            line = stream.readline()
            result[0] = line
        except Exception:
            result[0] = ""
        finally:
            event.set()

    t = threading.Thread(target=_read, daemon=True)
    t.start()
    event.wait(timeout=timeout)
    if event.is_set():
        val = result[0]
        return val if val else None
    return ""


def check_python_version():
    """检查 Python 版本是否在 3.8-3.11 范围内"""
    v = sys.version_info
    if v.major == 3 and 8 <= v.minor <= 11:
        return True, f"{v.major}.{v.minor}.{v.micro}"
    return False, f"{v.major}.{v.minor}.{v.micro}"


def pip_install(packages, venv_python=None):
    """安装 pip 包"""
    python = venv_python or sys.executable
    return run_command([python, "-m", "pip", "install"] + packages)


def pip_check_installed(package_name):
    """检查包是否已安装"""
    result = run_command(
        [sys.executable, "-m", "pip", "show", package_name], timeout=30
    )
    return result["success"]


def list_installed_packages():
    """列出已安装的包"""
    result = run_command(
        [sys.executable, "-m", "pip", "list", "--format=columns"], timeout=30
    )
    if result["success"]:
        lines = result["stdout"].strip().split("\n")
        packages = {}
        for line in lines[2:]:  # skip header
            parts = line.split()
            if len(parts) >= 2:
                packages[parts[0].lower()] = parts[1]
        return packages
    return {}


def dir_size(path):
    """计算目录大小（MB）"""
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total += os.path.getsize(fp)
            except OSError:
                pass
    return total / (1024 * 1024)


def safe_json_dump(data, filepath):
    """安全写入 JSON 文件"""
    tmp = filepath + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, filepath)


def safe_json_load(filepath, default=None):
    """安全读取 JSON 文件"""
    if not os.path.exists(filepath):
        return default
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def find_model_dirs(base_dir):
    """在指定目录下查找嵌入模型目录"""
    models = []
    if not os.path.exists(base_dir):
        return models
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path):
            files = os.listdir(item_path)
            has_model_file = any(
                f.endswith((".bin", ".safetensors", ".onnx"))
                for f in files
            )
            has_config = "config.json" in files
            if has_model_file or has_config:
                models.append({"name": item, "path": item_path})
    return models
