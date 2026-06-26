"""
setup.py - 首次安装时运行，自动检测 Chrome 路径并写入 conf.py
用法：python setup.py
"""
import sys
import os
import subprocess
from pathlib import Path

CONF_PATH = Path(__file__).parent / "conf.py"

CHROME_CANDIDATES = [
    # Windows
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    # macOS
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    # Linux
    "/usr/bin/google-chrome",
    "/usr/bin/chromium-browser",
    "/usr/bin/chromium",
]


def find_chrome():
    for path in CHROME_CANDIDATES:
        if os.path.exists(path):
            return path
    return ""


def install_deps():
    print("安装依赖...")
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                           "playwright", "biliup", "loguru", "requests"], stdout=subprocess.DEVNULL)
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    print("依赖安装完成")


def write_chrome_path(chrome_path: str):
    text = CONF_PATH.read_text(encoding="utf-8")
    text = text.replace(
        'LOCAL_CHROME_PATH = os.environ.get("CHROME_PATH", "")',
        f'LOCAL_CHROME_PATH = r"{chrome_path}"'
    )
    CONF_PATH.write_text(text, encoding="utf-8")


def main():
    print("=== video-publisher 安装向导 ===\n")

    # 1. 安装依赖
    install_deps()

    # 2. 检测 Chrome
    chrome = find_chrome()
    if chrome:
        print(f"检测到 Chrome: {chrome}")
        confirm = input("使用此路径？[Y/n] ").strip().lower()
        if confirm in ("", "y"):
            write_chrome_path(chrome)
        else:
            custom = input("请输入 Chrome 路径: ").strip()
            write_chrome_path(custom)
    else:
        custom = input("未检测到 Chrome，请手动输入路径: ").strip()
        write_chrome_path(custom)

    print("\n安装完成！")
    print("下一步：")
    print("  python publish.py login douyin    # 登录抖音")
    print("  python publish.py login bilibili  # 登录B站")
    print("  python publish.py run douyin      # 发布到抖音")
    print("  python publish.py run all         # 发布到所有平台")


if __name__ == "__main__":
    main()
