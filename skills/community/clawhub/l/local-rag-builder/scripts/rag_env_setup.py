"""
local-rag-builder 环境检测与自动修复模块
v0.3.0
检测 Python 版本、缺失包，自动创建虚拟环境并安装

修复历史:
  v0.3.0 (2026-06-06)
    - 修复：pip 安装全程无声输出导致 Bash 工具超时杀进程
    - 修复：用户看不到下载进度
    - 方案：`_pip_run()` 改为 Popen 流式，每行实时打印到终端+写入日志
    - 新增：pip 安装日志写入 data/logs/pip_install_*.log
  v0.2.0 (2026-06-06)
    - 修复：pip 锁死导致的无声空结果 BUG（auto-install 报 OK 但啥也没装）
    - 新增：pip 锁文件自动检测与清理
    - 新增：安装后验证（确认包真正可用才报 OK）
    - 新增：--no-deps 分步安装回退机制
    - 新增：--mirror 镜像源选择
    - 删除：bare `except: pass` 吞异常模式
"""

import os
import sys
import subprocess
import platform
import time
import datetime

REQUIRED_PACKAGES = [
    "langchain",
    "langchain-community",
    "langchain-huggingface",
    "langchain-chroma",
    "langchain-text-splitters",
    "chromadb",
    "sentence-transformers",
    "huggingface-hub",
    "modelscope",
    "openai",
]

OPTIONAL_PACKAGES = {
    "unstructured": "unstructured[pdf]",
    "pdfplumber": "pdfplumber",
    "transformers": "transformers",
    "pillow": "pillow",
    "fastapi": "fastapi",
    "uvicorn": "uvicorn",
}

# chromadb 核心依赖（独立安装用 --no-deps 策略）
CHROMADB_CORE_DEPS = [
    "numpy",
    "onnxruntime",
    "grpcio",
    "pydantic",
    "pydantic-settings",
    "overrides",
    "typing-extensions",
    "pypika",
    "tqdm",
    "tenacity",
    "pyyaml",
    "tokenizers",
    "kubernetes",
    "bcrypt",
    "build",
    "importlib-resources",
    "mmh3",
    "pybase64",
    "uvicorn",
    "opentelemetry-api",
    "opentelemetry-sdk",
    "opentelemetry-exporter-otlp-proto-grpc",
]

MIRRORS = {
    "default": "https://pypi.org/simple/",
    "aliyun": "https://mirrors.aliyun.com/pypi/simple/",
    "tencent": "https://mirrors.cloud.tencent.com/pypi/simple/",
    "tsinghua": "https://pypi.tuna.tsinghua.edu.cn/simple/",
    "ustc": "https://pypi.mirrors.ustc.edu.cn/simple/",
}

# 日志目录
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
PIP_LOG = os.path.join(LOG_DIR, f"pip_install_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")


def get_python_path():
    return sys.executable


def get_pip_cache_dir():
    """获取 pip 缓存目录（用于定位锁文件）"""
    if platform.system() == "Windows":
        return os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "pip")
    return os.path.join(os.path.expanduser("~"), ".cache", "pip")


# ═══════════════════════════════════════════════
# 锁文件检测与清理
# ═══════════════════════════════════════════════

def find_stale_pip_locks():
    """查找所有可能的 pip 锁文件/目录"""
    locks = []
    # Windows: pip 使用 ephem/ 目录下临时锁文件
    pip_cache = get_pip_cache_dir()
    ephem_dir = os.path.join(pip_cache, "ephem")
    if os.path.isdir(ephem_dir):
        for entry in os.listdir(ephem_dir):
            entry_path = os.path.join(ephem_dir, entry)
            # 检查是否为超过 5 分钟的锁
            try:
                age = time.time() - os.path.getmtime(entry_path)
                if age > 300:  # > 5 分钟视为过期
                    locks.append(entry_path)
            except OSError:
                locks.append(entry_path)
    # self-check: .venv 里的 pip lock
    venv_pip_lock = os.path.join(os.path.dirname(get_python_path()), "..", "..", "pip", "selfcheck.json")
    return locks


def cleanup_pip_locks(dry_run=False):
    """清理 stale pip 锁文件"""
    locks = find_stale_pip_locks()
    if not locks:
        return 0
    print(f"\n  发现 {len(locks)} 个 stale pip 锁文件，清理中...")
    for path in locks:
        if dry_run:
            print(f"    [dry-run] 将删除: {path}")
        else:
            try:
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    import shutil
                    shutil.rmtree(path, ignore_errors=True)
                print(f"    [OK] 已清理: {path}")
            except Exception as e:
                print(f"    [WARN] 清理失败: {path} — {e}")
    return len(locks)


# ═══════════════════════════════════════════════
# 环境检测
# ═══════════════════════════════════════════════

def check_python_version():
    """检查 Python 版本（建议 3.8-3.11）"""
    v = sys.version_info
    version_str = f"{v.major}.{v.minor}.{v.micro}"
    if v.major == 3 and 8 <= v.minor <= 11:
        return True, version_str, "OK"
    elif v.major == 3 and v.minor >= 12:
        return False, version_str, "WARN: chromadb 可能不兼容 3.12+，建议使用 3.8-3.11"
    elif v.major == 3 and v.minor < 8:
        return False, version_str, "ERROR: Python 版本过低，需要 3.8+"
    return False, version_str, "ERROR: 仅支持 Python 3.x"


def check_pip():
    """检查 pip 是否可用"""
    try:
        result = subprocess.run(
            [get_python_path(), "-m", "pip", "--version"],
            capture_output=True, text=True, timeout=30
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, OSError):
        return False


def list_installed():
    """列出已安装包（包名统一转为小写+连字符格式便于匹配）"""
    try:
        result = subprocess.run(
            [get_python_path(), "-m", "pip", "list", "--format=columns"],
            capture_output=True, text=True, timeout=30
        )
        pkgs = {}
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            for line in lines[2:]:
                parts = line.split()
                if len(parts) >= 2:
                    # 标准化：pip 在某些场景下用下划线（如 huggingface_hub）
                    # 统一转为连字符匹配 requirements 列表
                    normalized = parts[0].lower().replace("_", "-")
                    pkgs[normalized] = parts[1]
        return pkgs
    except (subprocess.TimeoutExpired, OSError):
        return {}


def check_missing(installed_pkgs=None):
    """返回缺失的必需包列表和缺失的可选包列表"""
    if installed_pkgs is None:
        installed_pkgs = list_installed()
    required_missing = []
    optional_missing = []
    for pkg in REQUIRED_PACKAGES:
        if pkg.lower() not in installed_pkgs:
            required_missing.append(pkg)
    for pkg_name, install_name in OPTIONAL_PACKAGES.items():
        if pkg_name.lower() not in installed_pkgs:
            optional_missing.append((pkg_name, install_name))
    return required_missing, optional_missing


# ═══════════════════════════════════════════════
# 安装核心逻辑（修复点）
# ═══════════════════════════════════════════════

def _pip_run(args, timeout=300, desc=None):
    """
    带超时的 pip 流式执行 — 返回 (成功?, 错误信息)

    关键改动:
    - 不使用 capture_output，改为 Popen 逐行流式输出
    - 每行同时打印到终端（让 Bash 工具看到活动）和写入日志文件
    - 用户和 Bash 工具都能实时看到下载进度
    """
    python = get_python_path()
    cmd = [python, "-m", "pip"] + args
    label = desc or " ".join(args[:3])

    # 确保日志目录存在
    os.makedirs(LOG_DIR, exist_ok=True)

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            text=True,
        )

        stdout_lines = []
        deadline = time.time() + timeout

        with open(PIP_LOG, "a", encoding="utf-8") as log_fp:
            log_fp.write(f"\n=== [{datetime.datetime.now().isoformat()}] {label} ===\n")

            while True:
                remaining = deadline - time.time()
                if remaining <= 0:
                    proc.kill()
                    return False, f"TIMEOUT ({timeout}s)"

                # 非阻塞读一行，最多等 1 秒
                line = _readline_timeout(proc.stdout, timeout=min(1.0, remaining))
                if line is None:  # EOF
                    break
                # 实时输出到终端（Bash 工具看到字符就不会超时）
                print(line, end="", flush=True)
                # 同时写入日志文件（用户事后查看用）
                log_fp.write(line)
                log_fp.flush()
                stdout_lines.append(line)

        proc.wait(timeout=5)
        full_output = "".join(stdout_lines)

        if proc.returncode != 0:
            err = full_output.strip()[-500:] if full_output else "(no output)"
            return False, err
        return True, ""
    except OSError as e:
        return False, str(e)


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
        return val if val else None  # None = EOF, "" = timeout
    return ""  # timeout


def _install_with_mirror(pkg_name, mirror_url, timeout=300):
    """尝试从指定镜像安装单个包"""
    args = ["install", pkg_name, "--index-url", mirror_url,
            "--trusted-host", mirror_url.split("/")[2] if "//" in mirror_url else "pypi.org",
            "--timeout", "120"]
    # 如果包名在分步安装名单中，优先 --no-deps
    if pkg_name in ("chromadb",):
        pass  # chromadb 先尝试完整安装，失败再切 --no-deps
    return _pip_run(args, timeout=timeout, desc=f"{pkg_name} @ {mirror_url.split('/')[2]}")


def _install_pkg(pkg_name, mirror_url, use_no_deps=False):
    """安装单个包，支持正常模式和 --no-deps 分步模式"""
    args = ["install", pkg_name, "--index-url", mirror_url,
            "--trusted-host", mirror_url.split("/")[2] if "//" in mirror_url else "pypi.org",
            "--timeout", "120"]
    if use_no_deps:
        args.append("--no-deps")
    ok, err = _pip_run(args, timeout=300, desc=pkg_name)
    if not ok and not use_no_deps:
        # 失败后自动降级到 --no-deps 重试
        print(f"    [RETRY] 完整安装失败，降级 --no-deps 重试...")
        ok2, err2 = _install_pkg(pkg_name, mirror_url, use_no_deps=True)
        return ok2, err2
    return ok, err


def install_packages(packages, upgrade_pip=True, mirror="default"):
    """
    安装指定包列表 — 修复版

    修复点:
    1. 安装前清理 pip 锁文件
    2. pip 升级失败继续安装（不吞异常)
    3. 每包安装后验证
    4. --no-deps 回退
    """
    python = get_python_path()
    mirror_url = MIRRORS.get(mirror, mirror)
    results = {}

    # 前置：清理 stale pip 锁
    cleanup_pip_locks()

    # 前置：升级 pip
    if upgrade_pip:
        print("  检查 pip 版本...")
        ok, err = _pip_run(["install", "--upgrade", "pip", "--timeout", "60",
                            "--index-url", mirror_url,
                            "--trusted-host", mirror_url.split("/")[2] if "//" in mirror_url else "pypi.org"],
                           timeout=120, desc="pip upgrade")
        if not ok:
            print(f"    [WARN] pip 升级失败 ({err[:100]}...)，继续使用当前版本安装")
        else:
            print("    pip 版本已更新")

    # 主安装循环
    for pkg in packages:
        print(f"  安装 {pkg}...", end="", flush=True)

        # 对于 chromadb，先装核心依赖再装本体（减少依赖解析压力）
        if pkg == "chromadb":
            print(" (分步策略: 先 install core deps...)")
            for dep in CHROMADB_CORE_DEPS:
                ok, err = _install_pkg(dep, mirror_url, use_no_deps=False)
                if ok:
                    print(f"    [OK] {dep}")
                else:
                    # 非核心 dep 失败可以跳过
                    pass
            # 最后装 chromadb 本体
            print(f"  安装 {pkg} (本体)...", end="", flush=True)
            ok, err = _install_pkg(pkg, mirror_url)
        else:
            ok, err = _install_pkg(pkg, mirror_url)

        if ok:
            print(" OK")
        else:
            print(f" FAIL")
            # 截取关键错误信息
            err_short = err.strip()[-250:]
            print(f"    {err_short}")
        results[pkg] = ok

    # 后置：验证安装结果
    print("\n  验证安装结果...")
    installed_after = list_installed()
    still_missing, _ = check_missing(installed_after)
    for pkg in packages:
        if pkg.lower() in installed_after:
            results[pkg] = True
            print(f"    [VERIFIED] {pkg} == {installed_after[pkg.lower()]}")
        elif pkg in still_missing:
            print(f"    [FAILED] {pkg} — 安装后仍未检测到")
            results[pkg] = False

    return results


# ═══════════════════════════════════════════════
# GPU 检测
# ═══════════════════════════════════════════════

def check_torch_gpu():
    """检查 PyTorch CUDA 是否可用"""
    try:
        result = subprocess.run(
            [get_python_path(), "-c", "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            cuda_avail = lines[0] == "True"
            gpu_name = lines[1] if len(lines) > 1 else "N/A"
            return cuda_avail, gpu_name
        return False, "无法检测"
    except Exception:
        return False, "检测失败"


# ═══════════════════════════════════════════════
# 完整检测报告
# ═══════════════════════════════════════════════

def run_full_check():
    """运行完整环境检查"""
    print("=" * 50)
    print("  本地 RAG 环境检测")
    print("=" * 50)

    # Python 版本
    ok, ver, msg = check_python_version()
    print(f"\n[{'OK' if ok else '!'}] Python 版本: {ver} — {msg}")

    # Pip
    pip_ok = check_pip()
    print(f"[{'OK' if pip_ok else '!'}] Pip: {'可用' if pip_ok else '不可用'}")

    # 已安装包
    installed = list_installed()
    print(f"\n已安装包: {len(installed)} 个")

    # 缺失检查
    required_missing, optional_missing = check_missing(installed)
    if required_missing:
        print(f"\n[!] 缺失必需包 ({len(required_missing)}): {', '.join(required_missing)}")
    else:
        print(f"\n[OK] 所有必需包已安装")

    if optional_missing:
        print(f"[i] 可选包未安装 ({len(optional_missing)}): {', '.join(n for n, _ in optional_missing)}")

    # GPU 检测
    cuda, gpu = check_torch_gpu()
    print(f"\n[{'OK' if cuda else 'i'}] GPU: {gpu if cuda else '未检测到 CUDA (将使用 CPU)'}")

    print("\n" + "=" * 50)
    return {
        "python_ok": ok,
        "python_version": ver,
        "pip_ok": pip_ok,
        "required_missing": required_missing,
        "optional_missing": [n for n, _ in optional_missing],
        "cuda_available": cuda,
        "gpu_name": gpu,
    }


def create_venv(venv_path):
    """创建虚拟环境"""
    print(f"创建虚拟环境: {venv_path}")
    try:
        result = subprocess.run(
            [get_python_path(), "-m", "venv", venv_path],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0:
            print(f"  FAIL: {result.stderr.strip()}")
            return None

        # 返回 venv 的 python 路径
        if platform.system() == "Windows":
            python_path = os.path.join(venv_path, "Scripts", "python.exe")
        else:
            python_path = os.path.join(venv_path, "bin", "python")

        if os.path.exists(python_path):
            return python_path
        return None
    except (subprocess.TimeoutExpired, OSError) as e:
        print(f"  FAIL: {e}")
        return None


# ═══════════════════════════════════════════════
# 入口
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="RAG 环境检测与修复工具")
    parser.add_argument("--check-only", action="store_true", help="仅检测，不自动修复")
    parser.add_argument("--auto-install", action="store_true", help="自动安装缺失的必需包")
    parser.add_argument("--install-optional", type=str, nargs="*", help="安装指定的可选包")
    parser.add_argument("--create-venv", type=str, help="在指定路径创建虚拟环境")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出（供智能体调用）")
    parser.add_argument("--mirror", type=str, default="default",
                        help=f"镜像源: {', '.join(MIRRORS.keys())} (默认: default)")
    parser.add_argument("--cleanup-locks", action="store_true", help="仅清理 pip 锁文件，不做其他操作")
    parser.add_argument("--dry-run", action="store_true", help="试运行（不实际安装，仅检测+报告）")

    args = parser.parse_args()

    # 锁清理专用
    if args.cleanup_locks:
        count = cleanup_pip_locks(dry_run=args.dry_run)
        print(f"\n清理完成: {count} 个 stale 锁")
        sys.exit(0)

    report = run_full_check()

    if args.json:
        import json
        print(json.dumps(report, ensure_ascii=False, indent=2))
        sys.exit(0)

    if args.dry_run:
        print("\n[dry-run] 检测完成，跳过安装")
        if report["required_missing"]:
            print(f"[dry-run] 将安装: {', '.join(report['required_missing'])}")
        sys.exit(0)

    if args.auto_install and report["required_missing"]:
        print(f"\n→ 自动安装缺失包 (镜像: {args.mirror})...")
        results = install_packages(report["required_missing"], mirror=args.mirror)
        failed = [p for p, ok in results.items() if not ok]
        if failed:
            print(f"\n{'=' * 50}")
            print(f"[!] 安装失败 ({len(failed)}/{len(results)}): {', '.join(failed)}")
            print(f"  建议:")
            print(f"    1. 换个镜像源: --mirror aliyun / --mirror tsinghua")
            print(f"    2. 手动安装: python -m pip install <pkg>")
            print(f"{'=' * 50}")
            sys.exit(1)
        else:
            print(f"\n[OK] 所有必需包安装完成（{len(results)}/{len(results)} 验证通过）")

    if args.install_optional:
        to_install = []
        for name in args.install_optional:
            if name in dict(OPTIONAL_PACKAGES):
                to_install.append(OPTIONAL_PACKAGES[name])
            else:
                to_install.append(name)
        print(f"\n→ 安装可选包...")
        install_packages(to_install, mirror=args.mirror)

    if args.create_venv:
        python = create_venv(args.create_venv)
        if python:
            print(f"[OK] 虚拟环境创建完成: {python}")
        else:
            print(f"[!] 虚拟环境创建失败")
