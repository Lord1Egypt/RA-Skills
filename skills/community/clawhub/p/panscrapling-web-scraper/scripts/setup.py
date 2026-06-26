#!/usr/bin/env python3
"""
Panscrapling Web Scraper - 自动安装脚本
自动检测并安装 Python 3.10+、Scrapling 及浏览器依赖
"""
import sys
import os
import subprocess
import platform
import shutil
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
#  配置
# ═══════════════════════════════════════════════════════════════

SKILL_DIR = Path(__file__).parent.parent
WHEELS_DIR = SKILL_DIR / "wheels"
BROWSERS_DIR = SKILL_DIR / "browsers"

# Homebrew 安装路径
BREW_PATHS = [
    "/opt/homebrew/bin/brew",  # Apple Silicon
    "/usr/local/bin/brew",     # Intel Mac
]

# Python 路径优先级
PYTHON_PATHS = [
    "/opt/homebrew/bin/python3.11",
    "/opt/homebrew/bin/python3.12",
    "/opt/homebrew/bin/python3.13",
    "/usr/local/bin/python3.11",
    "/usr/local/bin/python3.12",
    "/usr/local/bin/python3.13",
]

# ═══════════════════════════════════════════════════════════════
#  工具函数
# ═══════════════════════════════════════════════════════════════

def run(cmd, timeout=300, check=True, capture=True):
    """运行命令"""
    print(f"🔧 Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            timeout=timeout,
            check=False
        )
        if check and result.returncode != 0:
            print(f"❌ Error: {result.stderr}")
            return None
        return result
    except subprocess.TimeoutExpired:
        print(f"❌ Timeout after {timeout}s")
        return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def check_python_version(python_path):
    """检查 Python 版本是否 >= 3.10"""
    if not os.path.isfile(python_path):
        return None
    try:
        r = subprocess.run(
            [python_path, "--version"],
            capture_output=True, text=True, timeout=5
        )
        if r.returncode == 0:
            import re
            m = re.search(r"Python (\d+)\.(\d+)", r.stdout)
            if m:
                major, minor = int(m.group(1)), int(m.group(2))
                if major == 3 and minor >= 10:
                    return (major, minor, python_path)
    except:
        pass
    return None


# ═══════════════════════════════════════════════════════════════
#  步骤 1: 检测/安装 Python 3.10+
# ═══════════════════════════════════════════════════════════════

def find_python():
    """查找 Python 3.10+"""
    # 1. 检查预定义路径
    for py in PYTHON_PATHS:
        result = check_python_version(py)
        if result:
            print(f"✅ Found Python {result[0]}.{result[1]} at {result[2]}")
            return result[2]
    
    # 2. 检查系统 PATH 中的 python3
    for py in ["python3", "python3.11", "python3.12", "python3.13"]:
        py_path = shutil.which(py)
        if py_path:
            result = check_python_version(py_path)
            if result:
                print(f"✅ Found Python {result[0]}.{result[1]} at {result[2]}")
                return result[2]
    
    return None


def find_homebrew():
    """查找 Homebrew"""
    for brew in BREW_PATHS:
        if os.path.isfile(brew):
            print(f"✅ Found Homebrew at {brew}")
            return brew
    return None


def install_python_via_homebrew():
    """通过 Homebrew 安装 Python 3.11"""
    print("\n" + "="*60)
    print("📦 Installing Python 3.11 via Homebrew...")
    print("="*60 + "\n")
    
    # 检查 Homebrew
    brew = find_homebrew()
    if not brew:
        print("❌ Homebrew not found. Installing Homebrew first...")
        print("⏳ This may take a few minutes...\n")
        
        # 安装 Homebrew
        install_cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        r = run(["/bin/bash", "-c", 
                 'NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'],
                timeout=600, check=False)
        
        if not r or r.returncode != 0:
            print("❌ Failed to install Homebrew")
            return None
        
        brew = find_homebrew()
        if not brew:
            print("❌ Homebrew still not found after installation")
            return None
    
    # 安装 Python 3.11
    print(f"🔧 Installing python@3.11...")
    r = run([brew, "install", "python@3.11"], timeout=600, check=False)
    
    if not r:
        print("❌ Failed to install Python 3.11")
        return None
    
    # 验证安装
    py_path = "/opt/homebrew/bin/python3.11" if "/opt/homebrew" in brew else "/usr/local/bin/python3.11"
    result = check_python_version(py_path)
    if result:
        print(f"✅ Python {result[0]}.{result[1]} installed at {result[2]}")
        return result[2]
    
    print("❌ Python installed but version check failed")
    return None


def ensure_python():
    """确保有 Python 3.10+"""
    py = find_python()
    if py:
        return py
    
    print("\n⚠️  Python 3.10+ not found!")
    print("🔄 Attempting to install Python 3.11 via Homebrew...\n")
    
    return install_python_via_homebrew()


# ═══════════════════════════════════════════════════════════════
#  步骤 2: 安装 Scrapling 及依赖
# ═══════════════════════════════════════════════════════════════

def install_wheels(python_path):
    """从本地 wheels 目录安装依赖"""
    print("\n" + "="*60)
    print("📦 Installing Scrapling and dependencies...")
    print("="*60 + "\n")
    
    if not WHEELS_DIR.exists():
        print(f"❌ Wheels directory not found: {WHEELS_DIR}")
        return False
    
    wheels = list(WHEELS_DIR.glob("*.whl"))
    if not wheels:
        print(f"❌ No wheel files found in {WHEELS_DIR}")
        return False
    
    print(f"📦 Found {len(wheels)} wheel files")
    
    # 安装所有 wheels
    r = run(
        [python_path, "-m", "pip", "install", "--force-reinstall", 
         "--no-index", "--find-links", str(WHEELS_DIR),
         "scrapling[fetchers]", "playwright", "patchright"],
        timeout=300
    )
    
    if not r:
        print("❌ Failed to install from wheels, trying online...")
        # 降级到在线安装
        r = run(
            [python_path, "-m", "pip", "install", 
             "-i", "https://pypi.tuna.tsinghua.edu.cn/simple",
             "scrapling[fetchers]", "playwright", "patchright"],
            timeout=300
        )
        if not r:
            return False
    
    # 验证安装
    r = run([python_path, "-c", "import scrapling; print(scrapling.__version__)"], 
            check=False, capture=False)
    if r and r.returncode == 0:
        print("✅ Scrapling installed successfully")
        return True
    
    print("❌ Scrapling installation verification failed")
    return False


# ═══════════════════════════════════════════════════════════════
#  步骤 3: 安装浏览器
# ═══════════════════════════════════════════════════════════════

def install_browsers(python_path):
    """安装 Playwright 和 Patchright 浏览器"""
    print("\n" + "="*60)
    print("🌐 Installing browsers (this may take a few minutes)...")
    print("="*60 + "\n")
    
    # 检查是否已有浏览器
    browser_cache = Path.home() / "Library" / "Caches" / "ms-playwright"
    if browser_cache.exists():
        chromium_dirs = list(browser_cache.glob("chromium*"))
        if chromium_dirs:
            print(f"✅ Found existing Playwright browser at {browser_cache}")
            return True
    
    # 安装 Playwright Chromium
    print("📦 Installing Playwright Chromium...")
    r = run([python_path, "-m", "playwright", "install", "chromium"], 
            timeout=600, capture=False)
    
    if not r:
        print("⚠️  Playwright browser install failed, trying patchright...")
    
    # 安装 Patchright Chromium
    print("📦 Installing Patchright Chromium...")
    r = run([python_path, "-m", "patchright", "install", "chromium"], 
            timeout=600, capture=False)
    
    if not r:
        print("⚠️  Patchright browser install warning (may still work)")
    
    print("✅ Browser installation complete")
    return True


# ═══════════════════════════════════════════════════════════════
#  步骤 4: 验证
# ═══════════════════════════════════════════════════════════════

def verify_installation(python_path):
    """验证完整安装"""
    print("\n" + "="*60)
    print("✅ Verifying installation...")
    print("="*60 + "\n")
    
    checks = [
        ("Python version", [python_path, "--version"]),
        ("Scrapling", [python_path, "-c", "import scrapling; print(f'Scrapling {scrapling.__version__}')"]),
        ("Playwright", [python_path, "-c", "from playwright.sync_api import sync_playwright; print('Playwright OK')"]),
        ("Patchright", [python_path, "-c", "from patchright.sync_api import sync_playwright; print('Patchright OK')"]),
    ]
    
    all_ok = True
    for name, cmd in checks:
        r = run(cmd, check=False, capture=False)
        if r and r.returncode == 0:
            print(f"  ✅ {name}")
        else:
            print(f"  ❌ {name}")
            all_ok = False
    
    return all_ok


# ═══════════════════════════════════════════════════════════════
#  主入口
# ═══════════════════════════════════════════════════════════════

def main():
    print("""
╔═══════════════════════════════════════════════════════════════╗
║     Panscrapling Web Scraper - 自动安装脚本                   ║
║                                                               ║
║  此脚本将自动安装：                                           ║
║  1. Python 3.10+ (通过 Homebrew)                              ║
║  2. Scrapling 及所有依赖                                      ║
║  3. Playwright/Patchright 浏览器                              ║
╚═══════════════════════════════════════════════════════════════╝
""")
    
    # 步骤 1: Python
    python_path = ensure_python()
    if not python_path:
        print("\n❌ Failed to install Python 3.10+")
        print("💡 Please install manually: brew install python@3.11")
        return 1
    
    # 步骤 2: Scrapling
    if not install_wheels(python_path):
        print("\n❌ Failed to install Scrapling")
        return 1
    
    # 步骤 3: Browsers
    install_browsers(python_path)
    
    # 步骤 4: 验证
    if verify_installation(python_path):
        print("\n" + "="*60)
        print("🎉 Installation complete!")
        print("="*60)
        print(f"\n📁 Python: {python_path}")
        print(f"📁 Wheels: {WHEELS_DIR}")
        print("\n🚀 You can now use the scraper!")
        return 0
    else:
        print("\n⚠️  Installation completed with warnings")
        return 1


if __name__ == "__main__":
    sys.exit(main())
