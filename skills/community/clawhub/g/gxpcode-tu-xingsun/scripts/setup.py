# GxpCode Skill — 环境配置（首次安装本 skill 时必须运行，仅需一次）
# 用法: python scripts/setup.py

import subprocess
import sys
import os
import shutil

# 处理 Windows 控制台 GBK 编码问题
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIREMENTS = os.path.join(SKILL_DIR, "scripts", "requirements.txt")

# 国内镜像加速
PIP_INDEX = "https://mirrors.aliyun.com/pypi/simple/"
PW_DOWNLOAD_HOST = "https://npmmirror.com/mirrors/playwright/"

CHECK = "\u2714"
CROSS = "\u2718"
WARN = "\u26A0"

def _run(cmd: list, desc: str = "", env: dict = None) -> bool:
    """运行命令，返回是否成功"""
    label = desc or " ".join(cmd)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, env=env)
        return result.returncode == 0
    except Exception as e:
        print(f"  {CROSS} {label}: {e}")
        return False


def _pip_install() -> bool:
    """安装 Python 依赖（阿里云镜像）"""
    py = sys.executable
    print(f"\n[1/3] Python 依赖安装（镜像: mirrors.aliyun.com）")
    print(f"  解释器: {py}")
    if not os.path.exists(REQUIREMENTS):
        print(f"  {CROSS} 未找到 {REQUIREMENTS}")
        return False
    cmd = [py, "-m", "pip", "install", "-r", REQUIREMENTS, "-q", "-i", PIP_INDEX, "--trusted-host", "mirrors.aliyun.com"]
    if _run(cmd, "pip install"):
        print(f"  {CHECK} 依赖安装完成")
        return True
    else:
        print(f"  {CROSS} 依赖安装失败，尝试详细输出:")
        subprocess.run([py, "-m", "pip", "install", "-r", REQUIREMENTS, "-i", PIP_INDEX, "--trusted-host", "mirrors.aliyun.com"])
        return False


def _check_deps() -> dict:
    """逐个检查关键包是否可导入"""
    deps = {
        "feedparser": "RSS 解析     ",
        "yaml": "YAML 配置    ",
        "markdown": "Markdown→HTML",
        "playwright": "浏览器自动化  ",
    }
    status = {}
    for pkg, label in deps.items():
        try:
            __import__(pkg)
            status[label] = True
        except ImportError:
            status[label] = False
    return status


def _check_playwright_browser() -> str | None:
    """检查 Chromium 是否已安装，返回路径或 None"""
    # Playwright 默认浏览器缓存路径
    possible_bases = [
        os.path.join(os.environ.get("USERPROFILE", os.path.expanduser("~")),
                     "AppData", "Local", "ms-playwright"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "ms-playwright"),
    ]
    for base in possible_bases:
        if not os.path.isdir(base):
            continue
        for entry in os.listdir(base):
            if entry.startswith("chromium-") and os.path.isdir(os.path.join(base, entry)):
                install_flag = os.path.join(base, entry, "INSTALLATION_COMPLETE")
                chrome_exe = os.path.join(base, entry, "chrome-win64", "chrome.exe")
                if os.path.exists(install_flag) or os.path.exists(chrome_exe):
                    return os.path.join(base, entry)
    return None


def _install_playwright_browser() -> bool:
    """安装 Playwright Chromium（npmmirror 镜像）"""
    py = sys.executable
    print(f"\n[2/3] Playwright 浏览器安装（镜像: npmmirror.com）")
    print(f"  正在下载 Chromium（约 150 MB 压缩包，解压后 ~400 MB）...")
    env = os.environ.copy()
    env["PLAYWRIGHT_DOWNLOAD_HOST"] = PW_DOWNLOAD_HOST
    cmd = [py, "-m", "playwright", "install", "chromium"]
    return _run(cmd, "playwright install chromium", env=env)


def _validate() -> bool:
    """最终校验"""
    print(f"\n[3/3] 环境校验")

    all_ok = True

    # 检查依赖
    dep_status = _check_deps()
    for label, ok in dep_status.items():
        icon = CHECK if ok else CROSS
        print(f"  {icon} {label}")
        if not ok:
            all_ok = False

    # 检查 Playwright 浏览器
    pw_path = _check_playwright_browser()
    if pw_path:
        size = "-"
        try:
            chrome_dir = os.path.join(pw_path, "chrome-win64")
            if os.path.isdir(chrome_dir):
                size_mb = sum(
                    os.path.getsize(os.path.join(dp, f))
                    for dp, _, files in os.walk(chrome_dir)
                    for f in files
                ) // (1024 * 1024)
                size = f"{size_mb} MB"
        except Exception:
            pass
        print(f"  {CHECK} Playwright Chromium  ({size}, {pw_path})")
    else:
        print(f"  {CROSS} Playwright Chromium 未安装")
        all_ok = False

    print()
    if all_ok:
        print(f"{CHECK} 环境就绪，可以执行法规跟踪。")
    else:
        print(f"{WARN} 存在缺失项，请检查上述 {CROSS} 标记的项目。")
    return all_ok


def main():
    print("=" * 55)
    print("  GxpCode-制药法规跟踪 — 环境配置")
    print("=" * 55)

    # Step 1: 安装 pip 依赖
    if not _pip_install():
        print(f"\n{WARN} 依赖安装未完全成功，继续检查...")

    # Step 2: 检查/安装 Playwright 浏览器
    pw_installed = _check_playwright_browser() is not None
    if not pw_installed:
        if not _install_playwright_browser():
            print(f"  {WARN} Chromium 安装失败，Web 抓取和 PDF 生成功能将不可用")
    else:
        print(f"\n[2/3] Playwright 浏览器")
        print(f"  {CHECK} 已安装（跳过下载）")

    # Step 3: 最终校验
    ok = _validate()

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
