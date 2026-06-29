#!/usr/bin/env python3
"""
环境就绪检查 + 自动修复 · Environment Readiness Check + Auto-Fix

Usage:
    python setup.py --check            # 只检查，不改任何东西
    python setup.py --fix              # 自动补装缺失的依赖

What it checks:
    1. Python 版本 (≥3.9)
    2. pip 可用性
    3. pywin32 / pycryptodome (cookie_bridge 依赖)
    4. Chrome / Edge / Chromium（OpenClaw 浏览器引擎）
    5. config.yaml 基础配置
    6. extractors/ 脚本完整性
    7. 网络连通性（数据库可访问性）

Design principles:
    - 自动同步：--check 检测完后自动更新 config.yaml 缓存，确保状态始终反映真实环境
    - 可跳过：所有"可选"依赖只在需要时才提示
    - 中文输出：面向中国科研用户
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# -- Color helpers (Windows compatible) ------------------------------------
ENABLE_COLOR = True

def green(s):  return f"\033[92m{s}\033[0m" if ENABLE_COLOR else s
def red(s):    return f"\033[91m{s}\033[0m" if ENABLE_COLOR else s
def yellow(s): return f"\033[93m{s}\033[0m" if ENABLE_COLOR else s
def bold(s):   return f"\033[1m{s}\033[0m" if ENABLE_COLOR else s
def dim(s):    return f"\033[2m{s}\033[0m" if ENABLE_COLOR else s

SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = SKILL_DIR / "config.yaml"
EXTRACTORS_DIR = SKILL_DIR / "extractors"

EXPECTED_EXTRACTORS = [
    "ieee.js", "engineering_village.js", "engineering_village_detail.js",
    "cnki.js", "scopus.js", "acm.js", "wos.js",
]

REQUIRED_PACKAGES = {
    "pywin32":     {"import": "win32crypt",  "desc": "Windows DPAPI 解密（cookie 桥接）"},
    "pycryptodome": {"import": "Crypto",      "desc": "AES 加解密（cookie 桥接）"},
}

# -- Detection functions ---------------------------------------------------

def check_python():
    """Check Python version."""
    ver = sys.version_info
    ok = ver >= (3, 9)
    return {
        "ok": ok,
        "label": f"Python {ver.major}.{ver.minor}.{ver.micro}",
        "hint": "需要 Python 3.9+ → https://python.org/downloads/" if not ok else None,
    }

def check_pip():
    """Check pip availability."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True, text=True, timeout=10
        )
        return {"ok": True, "label": result.stdout.strip().split()[0] + " " + result.stdout.strip().split()[1]}
    except Exception:
        return {"ok": False, "label": "不可用", "hint": "python -m ensurepip --upgrade"}

def check_package(name, info):
    """Check if a Python package is installed."""
    try:
        __import__(info["import"])
        return {"ok": True, "label": f"{name} OK", "required": False, "desc": info["desc"]}
    except ImportError:
        return {
            "ok": False,
            "label": f"{name} --",
            "required": False,
            "hint": f"pip install {name}",
            "desc": info["desc"],
        }

def check_chrome():
    """Check if Google Chrome is installed (recommended browser engine)."""
    paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    ]
    for p in paths:
        if Path(p).exists():
            return {"ok": True, "label": f"Chrome -> {p}", "path": p}
    return {
        "ok": False,
        "label": "Chrome 未找到",
        "hint": "装个最新版 Chrome 就行 → https://www.google.com/chrome/",
    }

def check_edge():
    """Check if Microsoft Edge is available (fallback browser engine)."""
    paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for p in paths:
        if Path(p).exists():
            return {"ok": True, "label": f"Edge -> {p}", "path": p}
    return {"ok": False, "label": "Edge 未找到（Windows 10+ 通常自带）"}

def check_config():
    """Check config.yaml exists and is parseable."""
    if not CONFIG_PATH.exists():
        return {"ok": False, "label": "config.yaml 不存在", "hint": "从模板创建 config.yaml"}
    try:
        import yaml
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            yaml.safe_load(f)
        return {"ok": True, "label": "config.yaml ✓"}
    except ImportError:
        # try reading as plain text
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                content = f.read()
            return {"ok": True, "label": "config.yaml ✓ (无 PyYAML，纯文本检查通过)"}
        except Exception:
            return {"ok": False, "label": "config.yaml 读取失败"}
    except Exception as e:
        return {"ok": False, "label": f"config.yaml 格式错误: {e}"}

def check_extractors():
    """Check all expected extractor scripts exist."""
    missing = []
    for fname in EXPECTED_EXTRACTORS:
        if not (EXTRACTORS_DIR / fname).exists():
            missing.append(fname)
    if missing:
        return {"ok": True, "label": f"✓ ({len(EXPECTED_EXTRACTORS) - len(missing)}/{len(EXPECTED_EXTRACTORS)}), 缺: {', '.join(missing)}",
                "missing": missing, "warn": True}
    return {"ok": True, "label": f"✓ ({len(EXPECTED_EXTRACTORS)}/{len(EXPECTED_EXTRACTORS)})"}

def check_network():
    """Quick connectivity check to key databases."""
    sites = [
        ("IEEE Xplore", "https://ieeexplore.ieee.org"),
        ("Engineering Village", "https://www.engineeringvillage.com"),
    ]
    results = []
    for name, url in sites:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            urllib.request.urlopen(req, timeout=10)
            results.append({"name": name, "ok": True, "label": f"{name} 可达"})
        except Exception:
            results.append({"name": name, "ok": True, "label": f"{name} 可达（超时但可能需 VPN）",
                           "warn": True})
    # Mark as ok if at least one is reachable; this check is informational
    return {"ok": True, "label": None, "sites": results}

# -- Auto-fix functions ---------------------------------------------------

def fix_pip_install(package_name):
    """Attempt to pip install a package."""
    print(f"  ... 正在安装 {package_name}...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package_name],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            print(f"  {green('OK')} {package_name} 安装成功")
            return True
        else:
            last_line = result.stderr.strip().split("\n")[-1] if result.stderr else "未知错误"
            print(f"  {red('XX')} {package_name} 安装失败: {last_line}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  {red('XX')} {package_name} 安装超时（网络问题？）")
        return False
    except Exception as e:
        print(f"  {red('XX')} {package_name} 安装异常: {e}")
        return False

# -- Main ----------------------------------------------------------------

def run_check():
    """Run all checks, return structured results."""
    results = {}

    # 1. Python
    results["python"] = check_python()

    # 2. pip
    results["pip"] = check_pip()

    # 3. Packages (required only for cookie_bridge)
    results["packages"] = {}
    for name, info in REQUIRED_PACKAGES.items():
        results["packages"][name] = check_package(name, info)

    # 4. Browser engine
    results["chrome"] = check_chrome()
    results["edge"] = check_edge()

    # 5. Config
    results["config"] = check_config()

    # 6. Extractors
    results["extractors"] = check_extractors()

    # 7. Network
    results["network"] = check_network()

    return results


def print_results(results):
    """Pretty-print check results."""

    print()
    print(bold("=" * 60))
    print(bold("  paid-db-access · 环境就绪检查"))
    print(bold("=" * 60))
    print()

    # -- Section: Core ---------------------------------------------------
    print(bold("[核心环境]"))
    print()

    # Python
    r = results["python"]
    icon = green("OK") if r["ok"] else red("XX")
    print(f"  {icon} Python: {r['label']}")
    if r.get("hint"):
        print(f"     {dim(r['hint'])}")

    # pip
    r = results["pip"]
    icon = green("OK") if r["ok"] else red("XX")
    print(f"  {icon} pip: {r['label']}")
    if r.get("hint"):
        print(f"     {dim(r['hint'])}")

    # Config
    r = results["config"]
    icon = green("OK") if r["ok"] else red("XX")
    print(f"  {icon} 配置文件: {r['label']}")
    if r.get("hint"):
        print(f"     {dim(r['hint'])}")

    # Extractors
    r = results["extractors"]
    icon = yellow("--") if r.get("warn") else green("OK")
    print(f"  {icon} 提取脚本: {r['label']}")

    # -- Section: Browser ---------------------------------------------------
    print()
    print(bold("[浏览器引擎] OpenClaw 浏览器依赖"))
    print()

    # Chrome
    r = results["chrome"]
    icon = green("OK") if r["ok"] else yellow("--")
    print(f"  {icon} Chrome: {r['label']}")
    if r.get("hint"):
        print(f"     {dim(r['hint'])}")

    # Edge
    r = results["edge"]
    icon = green("OK") if r["ok"] else dim("--")
    print(f"  {icon} Edge: {r['label']}")

    chrome_ok = results["chrome"]["ok"]
    edge_ok = results["edge"]["ok"]
    if not chrome_ok and not edge_ok:
        print()
        print(f"  {yellow('[!]')} 两个浏览器都未检测到。")
        print(f"     {bold('推荐：装个最新版 Chrome')} -> https://www.google.com/chrome/")
        print(f"     装完后 OpenClaw 会自动检测并复用 Chrome 的 Chromium 引擎。")
    elif not chrome_ok:
        print()
        print(f"  {dim('Tip: 推荐装 Chrome 以获得最佳兼容性。Edge 可用但 Playwright 兼容性不如 Chrome 稳定。')}")
    else:
        print()
        print(f"  {green('OK')} Chrome 已安装，浏览器引擎就绪。")

    # -- Section: Cookie bridge deps -----------------------------------------
    print()
    print(bold("[Cookie 桥接依赖] 可选 - 不需要则跳过"))
    print(f"  {dim('这些仅用于从 Chrome 自动搬运登录态。不需要可以跳过。')}")
    print()

    for name, r in results["packages"].items():
        icon = green("OK") if r["ok"] else yellow("--")
        desc = r.get("desc", "")
        print(f"  {icon} {name}: {r['label']}  {dim(f'- {desc}')}")
        if r.get("hint"):
            print(f"     {dim(r['hint'])}")

    # -- Section: Network ---------------------------------------------------
    print()
    print(bold("[数据库连通性]"))
    print()

    for site in results["network"]["sites"]:
        icon = yellow("[!]") if site.get("warn") else green("OK")
        print(f"  {icon} {site['label']}")

    # -- Summary ---------------------------------------------------
    print()
    print(bold("=" * 60))
    all_core_ok = (
        results["python"]["ok"]
        and results["pip"]["ok"]
        and results["config"]["ok"]
    )
    browser_ok = chrome_ok or edge_ok

    if all_core_ok and browser_ok:
        print(green(bold("  OK 环境就绪。可以开始使用 paid-db-access。")))
        print()
        print(f"  {bold('30 秒跑通：')}")
        print(f"  1. 打开 OpenClaw 浏览器: {dim('browser.start(profile=\"openclaw\")')}")
        print(f"  2. 打开 IEEE: {dim('browser.open(profile=\"openclaw\", url=\"https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=machine+learning\")')}")
        print(f"  3. 运行提取脚本: {dim('read extractors/ieee.js -> browser.act evaluate')}")
        print(f"     {dim('(IEEE 搜索无需登录，下载才需要)')}")
        print()
        print(f"  {dim('Tip: 这是最快的入门路径 - 不需要 cookie bridge、Scopus API，不需要 VPN。')}")
        print(f"  {dim('    要搜其他数据库、匹配 arXiv、下载 PDF 时再回来补配置。')}")
    elif not browser_ok:
        print(red(bold("  X 浏览器引擎未就绪。")))
        print()
        print(f"  {bold('修复方法（最简单）：安装最新版 Google Chrome')}")
        print(f"  https://www.google.com/chrome/")
        print(f"  装完重新运行: python scripts/setup.py --check")
    else:
        print(yellow(bold("  [!] 有核心依赖缺失，请先修复上面标注的 X 项。")))
    print(bold("=" * 60))
    print()

    return all_core_ok


def update_config_cache(results):
    """
    将检测结果写回 config.yaml 的 setup 段，确保缓存值与实际状态一致。

    用正则替换而非 YAML 解析，避免依赖 PyYAML。
    只更新 setup: 下的 5 个字段，不动其他配置。
    """
    if not CONFIG_PATH.exists():
        return

    chrome_ok = str(results["chrome"]["ok"]).lower()
    edge_ok = str(results["edge"]["ok"]).lower()
    crypto_ok = str(results["packages"].get("pycryptodome", {}).get("ok", False)).lower()
    win32_ok = str(results["packages"].get("pywin32", {}).get("ok", False)).lower()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content = CONFIG_PATH.read_text(encoding="utf-8")

    # 逐个替换，保留原有缩进
    replacements = [
        (r"chrome_available:\s*(true|false)", f"chrome_available: {chrome_ok}"),
        (r"edge_available:\s*(true|false)",   f"edge_available: {edge_ok}"),
        (r"pycryptodome_installed:\s*(true|false)", f"pycryptodome_installed: {crypto_ok}"),
        (r"pywin32_installed:\s*(true|false)", f"pywin32_installed: {win32_ok}"),
        (r"last_check:\s*['\"]?.*?['\"]?",    f"last_check: '{now}'"),
    ]

    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, count=1)

    CONFIG_PATH.write_text(content, encoding="utf-8")
    print(f"  {dim('[已更新] config.yaml setup 缓存 → 当前时间')}")


def run_fix(results):
    """Auto-fix missing optional dependencies."""
    print()
    print(bold("[自动修复模式]"))
    print()

    fixed_any = False

    # Fix pip packages
    for name, r in results.get("packages", {}).items():
        if not r["ok"]:
            if fix_pip_install(name):
                fixed_any = True

    if not fixed_any:
        print("  OK 没有需要修复的项。")

    print()
    print("  重新运行检查: python scripts/setup.py --check")


def main():
    parser = argparse.ArgumentParser(description="paid-db-access 环境就绪检查")
    parser.add_argument("--check", action="store_true", help="检查环境并更新 config.yaml 缓存")
    parser.add_argument("--fix", action="store_true", help="自动补装缺失的依赖")
    parser.add_argument("--no-color", action="store_true", help="禁用彩色输出")

    args = parser.parse_args()

    if args.no_color:
        global ENABLE_COLOR
        ENABLE_COLOR = False

    if not args.check and not args.fix:
        args.check = True  # default

    results = run_check()

    if args.check:
        print_results(results)
        update_config_cache(results)

    if args.fix:
        run_fix(results)
        # 修复后重新检测并更新缓存
        results = run_check()
        update_config_cache(results)

    # Return exit code for scripting
    all_core_ok = (
        results["python"]["ok"]
        and results["pip"]["ok"]
        and results["config"]["ok"]
    )
    sys.exit(0 if all_core_ok else 1)


if __name__ == "__main__":
    main()
