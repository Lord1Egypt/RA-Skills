#!/usr/bin/env python3
"""
Playwright Browser Installer with Progress Detection

This script installs Playwright Chromium browser with:
1. Progress detection in the first 10 seconds
2. Automatic fallback suggestions if download stalls
3. Mirror source support for Chinese users
4. DNS resolution failure detection and solutions

Installation Priority:
1. Official CDN (cdn.playwright.dev) - Default
2. Mirror sources (taobao, tsinghua) - For users with CDN access issues
3. Docker - For server/headless environments
"""

import subprocess
import sys
import os
import time
import threading
import re
import argparse
import socket
import urllib.request
import urllib.error
from pathlib import Path


# Official CDN endpoint
OFFICIAL_CDN = "cdn.playwright.dev"

# PyPI mirrors for Chinese users (for pip install playwright)
# These are used for installing the Playwright Python package
PYPI_MIRRORS = {
    "aliyun": "https://mirrors.aliyun.com/pypi/simple/",
    "tsinghua": "https://pypi.tuna.tsinghua.edu.cn/simple/",
    "tencent": "https://mirrors.cloud.tencent.com/pypi/simple/",
    "huawei": "https://repo.huaweicloud.com/repository/pypi/simple/",
    "douban": "https://pypi.doubanio.com/simple/",
}

# Default PyPI mirror for Chinese users
DEFAULT_PYPI_MIRROR = "aliyun"

# Mirror sources for browser binaries (for playwright install chromium)
# Note: These mirrors may not have the latest Playwright browser versions
# Format: {name: (url, description)}
MIRROR_SOURCES = {
    "taobao": ("https://registry.npmmirror.com/-/binary/playwright", "淘宝镜像（推荐）"),
    "tsinghua": ("https://mirrors.tuna.tsinghua.edu.cn/playwright", "清华大学镜像"),
}

# DNS servers for fallback resolution
DNS_SERVERS = {
    "google": "8.8.8.8",
    "cloudflare": "1.1.1.1",
    "aliyun": "223.5.5.5",
    "dnspod": "119.29.29.29",
}

# Known IP addresses for cdn.playwright.dev (for hosts file workaround)
KNOWN_CDN_IPS = [
    "13.107.253.39",
    "150.171.110.65",
    "150.171.110.68",
]

# Playwright version to Chromium build number mapping
# Reference: https://github.com/microsoft/playwright/releases
PLAYWRIGHT_CHROMIUM_VERSIONS = {
    "1.58.0": 1208,
    "1.57.1": 1200,
    "1.57.0": 1199,
    "1.56.0": 1194,
    "1.55.0": 1181,
    "1.54.0": 1179,
    "1.53.0": 1169,
    "1.52.0": 1161,
    "1.51.0": 1148,
    "1.50.0": 1139,
    "1.49.0": 1131,
    "1.48.0": 1122,
    "1.47.0": 1117,
    "1.46.0": 1106,
    "1.45.0": 1097,
    "1.44.0": 1084,
    "1.43.0": 1076,
    "1.42.0": 1067,
    "1.41.0": 1059,
    "1.40.0": 1053,
}

# Note: PLAYWRIGHT_DOWNLOAD_HOST only works for older Playwright versions
# Newer versions (1.40+) use cdn.playwright.dev which may not respect this env var

# Progress detection timeout (seconds)
PROGRESS_TIMEOUT = 10


class ProgressDetector:
    """Detects download progress from playwright output."""
    
    def __init__(self, timeout=PROGRESS_TIMEOUT):
        self.timeout = timeout
        self.has_progress = False
        self.start_time = None
        self.last_output = ""
        self.bytes_downloaded = 0
        self.last_percentage = 0
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
    
    def start(self):
        """Start the progress detection timer."""
        self.start_time = time.time()
    
    def check_timeout(self):
        """Check if timeout has been reached without progress."""
        with self._lock:
            if self.has_progress:
                return False
        elapsed = time.time() - self.start_time
        return elapsed >= self.timeout
    
    def update(self, line):
        """Update progress from output line."""
        with self._lock:
            self.last_output = line
            
            # Check for download progress indicators
            # Playwright outputs like: "Downloading Chromium 120.0.6099.28 (playwright build v1053) from https://..."
            # Progress bar: "|■■■■■■■■■■■■■■■■ | 20% of 162.3 MiB"
            # Or: "12,345,678 bytes" or percentage
            
            line_lower = line.lower()
            
            # Check for progress bar format (Playwright's main format)
            # Pattern: "xx% of xxx MiB" or "|■■...| xx%"
            progress_bar_match = re.search(r'(\d+)%\s*(?:of\s+[\d.]+\s*[KMGT]?i?B)?', line)
            if progress_bar_match:
                new_percentage = int(progress_bar_match.group(1))
                if new_percentage > self.last_percentage:
                    self.last_percentage = new_percentage
                    self.has_progress = True
            
            # Check for keywords
            if any(keyword in line_lower for keyword in ["downloading", "bytes", "%", "complete", "download", "mib", "kib", "gib"]):
                self.has_progress = True
            
            # Extract bytes if present
            bytes_match = re.search(r'(\d[\d,]*)\s*bytes', line)
            if bytes_match:
                new_bytes = int(bytes_match.group(1).replace(',', ''))
                if new_bytes > self.bytes_downloaded:
                    self.bytes_downloaded = new_bytes
                    self.has_progress = True


def get_mirror_latest_chromium_version(mirror_url):
    """
    Query the latest chromium version available on a mirror.
    
    Args:
        mirror_url: Base URL of the mirror
    
    Returns:
        int: Latest chromium build number, or 0 if query fails
    """
    import json
    
    try:
        # Query chromium versions from mirror
        chromium_url = f"{mirror_url}/builds/chromium/"
        req = urllib.request.Request(chromium_url)
        req.add_header('Accept', 'application/json')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        # Extract version numbers
        versions = []
        for item in data:
            name = item.get('name', '')
            if name:
                # Remove trailing slash and convert to int
                version_str = name.rstrip('/')
                try:
                    versions.append(int(version_str))
                except ValueError:
                    continue
        
        if versions:
            return max(versions)
        return 0
        
    except Exception as e:
        print(f"⚠️  查询镜像版本失败: {e}")
        return 0


def get_playwright_version():
    """
    Get the installed Playwright version.
    
    Returns:
        str: Playwright version string, or None if not found
    """
    try:
        result = subprocess.run(
            [sys.executable, "-m", "playwright", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            # Output format: "Version 1.58.0"
            version = result.stdout.strip().replace("Version ", "")
            return version
    except Exception:
        pass
    return None


def get_chromium_build_for_playwright(playwright_version):
    """
    Get the chromium build number for a Playwright version.
    
    Args:
        playwright_version: Playwright version string (e.g., "1.58.0")
    
    Returns:
        int: Chromium build number, or 0 if not found
    """
    return PLAYWRIGHT_CHROMIUM_VERSIONS.get(playwright_version, 0)


def find_compatible_playwright_version(chromium_build):
    """
    Find a Playwright version compatible with the given chromium build.
    
    Args:
        chromium_build: Chromium build number
    
    Returns:
        str: Compatible Playwright version, or None if not found
    """
    for pw_version, build in PLAYWRIGHT_CHROMIUM_VERSIONS.items():
        if build == chromium_build:
            return pw_version
    return None


def install_playwright_version(version):
    """
    Install a specific Playwright version.
    
    Args:
        version: Playwright version to install
    
    Returns:
        bool: True if installation successful
    """
    print(f"\n📦 安装 Playwright {version}...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", f"playwright=={version}"],
        capture_output=True,
        text=True
    )
    return result.returncode == 0


def install_playwright_via_pip(version_spec=">=1.40.0", use_mirror=True):
    """
    Install Playwright Python package via pip.
    
    This is the preferred installation method as pip/PyPI is accessible in China
    through various mirrors, unlike the browser binary CDN.
    
    Args:
        version_spec: Version specification (e.g., ">=1.40.0", "==1.57.1")
        use_mirror: Whether to use Chinese PyPI mirror
    
    Returns:
        tuple: (success: bool, version: str or None)
    """
    print("\n" + "=" * 60)
    print("📦 方案1: pip 安装 Playwright")
    print("=" * 60)
    
    # Build pip command
    cmd = [sys.executable, "-m", "pip", "install", f"playwright{version_spec}"]
    
    # Add PyPI mirror for Chinese users
    if use_mirror:
        mirror_url = PYPI_MIRRORS.get(DEFAULT_PYPI_MIRROR)
        if mirror_url:
            cmd.extend(["-i", mirror_url, "--trusted-host", mirror_url.split("//")[1].split("/")[0]])
            print(f"🌐 使用 PyPI 镜像: {DEFAULT_PYPI_MIRROR} ({mirror_url})")
    
    print(f"📋 执行命令: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            # Get installed version
            installed_version = get_playwright_version()
            print(f"\n✅ Playwright {installed_version} 安装成功")
            return True, installed_version
        else:
            print(f"\n❌ pip 安装失败")
            if result.stderr:
                print(f"错误信息: {result.stderr}")
            return False, None
            
    except Exception as e:
        print(f"\n❌ 安装过程出错: {e}")
        return False, None


def get_system_proxy():
    """
    Detect system proxy settings from environment variables.
    
    Checks for proxy settings in the following order:
    1. HTTPS_PROXY / https_proxy
    2. HTTP_PROXY / http_proxy
    3. ALL_PROXY / all_proxy
    4. NO_PROXY / no_proxy (for exclusions)
    
    Returns:
        dict: Dictionary with proxy settings:
            - 'http': HTTP proxy URL or None
            - 'https': HTTPS proxy URL or None
            - 'all': ALL proxy URL or None
            - 'no_proxy': No proxy patterns or None
            - 'has_proxy': True if any proxy is set
    """
    proxy_settings = {
        'http': None,
        'https': None,
        'all': None,
        'no_proxy': None,
        'has_proxy': False
    }
    
    # Check HTTP proxy
    proxy_settings['http'] = os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy')
    
    # Check HTTPS proxy
    proxy_settings['https'] = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
    
    # Check ALL_PROXY (used by some tools like curl)
    proxy_settings['all'] = os.environ.get('ALL_PROXY') or os.environ.get('all_proxy')
    
    # Check NO_PROXY for exclusions
    proxy_settings['no_proxy'] = os.environ.get('NO_PROXY') or os.environ.get('no_proxy')
    
    # Determine if any proxy is set
    proxy_settings['has_proxy'] = bool(
        proxy_settings['http'] or
        proxy_settings['https'] or
        proxy_settings['all']
    )
    
    return proxy_settings


def print_proxy_info():
    """Print detected proxy settings."""
    proxy = get_system_proxy()
    
    if not proxy['has_proxy']:
        print("ℹ️  未检测到系统代理设置")
        return False
    
    print("🔍 检测到系统代理设置:")
    if proxy['https']:
        print(f"   HTTPS_PROXY: {proxy['https']}")
    if proxy['http']:
        print(f"   HTTP_PROXY: {proxy['http']}")
    if proxy['all']:
        print(f"   ALL_PROXY: {proxy['all']}")
    if proxy['no_proxy']:
        print(f"   NO_PROXY: {proxy['no_proxy']}")
    
    return True


def check_dns_resolution(host=OFFICIAL_CDN):
    """
    Check if the official CDN can be resolved via DNS.
    
    Returns:
        tuple: (success: bool, ip: str or None, error: str or None)
    """
    try:
        ip = socket.gethostbyname(host)
        return True, ip, None
    except socket.gaierror as e:
        return False, None, str(e)
    except Exception as e:
        return False, None, str(e)


def test_cdn_connectivity(host=OFFICIAL_CDN, timeout=5):
    """
    Test connectivity to the official CDN.
    
    Returns:
        tuple: (success: bool, error: str or None)
    """
    try:
        # Try to establish a connection
        sock = socket.create_connection((host, 443), timeout=timeout)
        sock.close()
        return True, None
    except socket.timeout:
        return False, "连接超时"
    except socket.gaierror as e:
        return False, f"DNS解析失败: {e}"
    except ConnectionRefusedError:
        return False, "连接被拒绝"
    except Exception as e:
        return False, str(e)


def print_dns_troubleshooting():
    """Print DNS resolution troubleshooting guide."""
    print("\n" + "!" * 60)
    print("📡 DNS 解析失败 - 官方 CDN 无法访问")
    print("!" * 60)
    print("\n🔧 解决方案：")
    print("-" * 40)
    
    print("\n方案1：更换 DNS 服务器（推荐）")
    print("  macOS: 系统偏好设置 → 网络 → 高级 → DNS")
    print("  添加以下 DNS 服务器：")
    for name, ip in DNS_SERVERS.items():
        print(f"    • {name}: {ip}")
    
    print("\n方案2：手动添加 hosts 映射")
    print("  运行以下命令（需要管理员权限）：")
    for ip in KNOWN_CDN_IPS[:1]:  # Only show first IP
        if sys.platform == "darwin" or sys.platform.startswith("linux"):
            print(f'    echo "{ip} {OFFICIAL_CDN}" | sudo tee -a /etc/hosts')
        elif sys.platform == "win32":
            print(f'    echo {ip} {OFFICIAL_CDN} >> %SystemRoot%\\System32\\drivers\\etc\\hosts')
    
    print("\n方案3：使用代理")
    print("  设置环境变量：")
    print('    export HTTPS_PROXY="http://your-proxy:port"')
    print('    export HTTP_PROXY="http://your-proxy:port"')
    
    print("\n方案4：使用国内镜像源（自动切换）")
    print("  本脚本将自动尝试使用镜像源")


def print_banner():
    """Print installation banner."""
    print("\n" + "=" * 60)
    print("🎭 Playwright Chromium Browser Installer")
    print("=" * 60)
    print()


def print_mirrors():
    """Print available mirror sources."""
    print("\n📡 可用的国内镜像源：")
    print("-" * 50)
    for i, (name, (url, desc)) in enumerate(MIRROR_SOURCES.items(), 1):
        print(f"  {i}. {name:12} - {desc}")
        print(f"     {url}")
    print("-" * 50)
    print("⚠️  注意: 镜像源版本可能滞后于官方版本")


def get_playwright_cache_dir():
    """Get Playwright browser cache directory."""
    # Default cache locations
    if sys.platform == "win32":
        return os.path.expandvars(r"%LOCALAPPDATA%\ms-playwright")
    elif sys.platform == "darwin":
        return os.path.expanduser("~/Library/Caches/ms-playwright")
    else:  # Linux
        return os.path.expanduser("~/.cache/ms-playwright")


def get_playwright_download_dirs():
    """Get possible Playwright download directories (temp dirs)."""
    dirs = []
    
    # macOS temp directory
    if sys.platform == "darwin":
        # /var/folders/xxx/T/playwright-download-xxx
        temp_base = os.environ.get("TMPDIR", "/tmp")
        dirs.append(temp_base)
        # Also check /var/folders directly
        import glob
        for pattern in [
            "/var/folders/*/T/playwright-download-*",
            "/tmp/playwright-download-*",
            os.path.join(temp_base, "playwright-download-*")
        ]:
            dirs.extend(glob.glob(pattern))
    
    # Linux
    elif sys.platform.startswith("linux"):
        dirs.extend([
            "/tmp",
            os.environ.get("TMPDIR", "/tmp"),
            "/var/tmp"
        ])
    
    # Windows
    elif sys.platform == "win32":
        temp = os.environ.get("TEMP", "")
        tmp = os.environ.get("TMP", "")
        if temp:
            dirs.append(temp)
        if tmp:
            dirs.append(tmp)
    
    return dirs


def find_downloading_files():
    """Find files currently being downloaded by Playwright."""
    import glob
    found_files = []
    
    # Find all playwright-download directories
    patterns = []
    
    if sys.platform == "darwin":
        # macOS: /var/folders/*/T/playwright-download-*
        patterns.append("/var/folders/*/T/playwright-download-*")
        # Also check TMPDIR
        tmpdir = os.environ.get("TMPDIR", "")
        if tmpdir:
            patterns.append(os.path.join(tmpdir, "playwright-download-*"))
    elif sys.platform.startswith("linux"):
        patterns.append("/tmp/playwright-download-*")
        tmpdir = os.environ.get("TMPDIR", "/tmp")
        patterns.append(os.path.join(tmpdir, "playwright-download-*"))
    elif sys.platform == "win32":
        temp = os.environ.get("TEMP", "")
        tmp = os.environ.get("TMP", "")
        if temp:
            patterns.append(os.path.join(temp, "playwright-download-*"))
        if tmp:
            patterns.append(os.path.join(tmp, "playwright-download-*"))
    
    for pattern in patterns:
        for download_dir in glob.glob(pattern):
            if not os.path.isdir(download_dir):
                continue
            try:
                # Walk through the download directory
                for root, dirs, files in os.walk(download_dir):
                    for file in files:
                        filepath = os.path.join(root, file)
                        try:
                            size = os.path.getsize(filepath)
                            if size > 0:  # Only count non-empty files
                                found_files.append((filepath, size))
                        except OSError:
                            pass
            except (OSError, PermissionError):
                pass
    
    return found_files


def get_download_progress():
    """Get total size of files being downloaded."""
    files = find_downloading_files()
    total_size = sum(size for _, size in files)
    return total_size, len(files)


def run_install_with_mirror(mirror_url=None):
    """
    Run playwright install with optional mirror source.
    
    Args:
        mirror_url: Optional mirror URL for browser download
    
    Returns:
        tuple: (success: bool, had_progress: bool)
    """
    env = os.environ.copy()
    if mirror_url:
        env["PLAYWRIGHT_DOWNLOAD_HOST"] = mirror_url
        print(f"\n🌐 使用镜像源: {mirror_url}")
    
    print("\n⏳ 开始安装 Chromium 浏览器...")
    print("-" * 40)
    print("📊 安装状态: 初始化中...")
    print("📋 这可能需要几分钟时间，请耐心等待")
    print()
    
    detector = ProgressDetector(timeout=PROGRESS_TIMEOUT)
    detector.start()
    
    # Get initial download progress
    initial_size, initial_count = get_download_progress()
    last_size = initial_size
    last_count = initial_count
    start_time = time.time()
    last_progress_time = [time.time()]  # Use list for mutable reference
    progress_count = [0]  # Number of progress updates
    
    # Timeout checker thread
    timeout_triggered = [False]  # Use list for mutable reference in thread
    
    def check_progress_async():
        """Check download progress by monitoring temp download files."""
        nonlocal last_size, last_count
        
        while not timeout_triggered[0]:
            time.sleep(1.0)
            
            # Check temp download files
            current_size, current_count = get_download_progress()
            if current_size > last_size:
                downloaded_mb = current_size / (1024 * 1024)
                size_diff = current_size - last_size
                speed_kbps = (size_diff / 1024) / 1.0  # KB/s
                
                last_size = current_size
                last_progress_time[0] = time.time()
                progress_count[0] += 1
                detector.has_progress = True
                detector.update(f"Downloaded: {downloaded_mb:.1f} MB")
                
                # Progress indicator with speed
                elapsed = time.time() - start_time
                avg_speed = (current_size / 1024) / elapsed if elapsed > 0 else 0
                
                print(f"📥 进度更新 #{progress_count[0]}: {downloaded_mb:.1f} MB | "
                      f"速度: {speed_kbps:.0f} KB/s | 平均: {avg_speed:.0f} KB/s", end="\r")
            
            # Check timeout
            if not detector.has_progress and detector.check_timeout():
                timeout_triggered[0] = True
                break
    
    progress_thread = threading.Thread(target=check_progress_async, daemon=True)
    progress_thread.start()
    
    try:
        # Run playwright install
        print("🚀 启动 Playwright 安装进程...")
        process = subprocess.Popen(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
            text=True,
            bufsize=1
        )
        
        # Read output
        output_lines = []
        while True:
            # Check timeout
            if timeout_triggered[0]:
                process.terminate()
                print("\n" + "!" * 60)
                print("⚠️  检测到下载停滞（前10秒无进度）")
                print("!" * 60)
                return False, False
            
            # Check if process ended
            if process.poll() is not None:
                break
            
            # Try to read output
            try:
                line = process.stdout.readline()
                if line:
                    output_lines.append(line)
                    # Parse and display progress
                    line_stripped = line.rstrip()
                    
                    # Check for download progress in output
                    if "Downloading" in line:
                        print(f"\n📥 {line_stripped}")
                    elif "%" in line:
                        # Extract percentage
                        import re
                        match = re.search(r'(\d+)%', line)
                        if match:
                            pct = int(match.group(1))
                            bar_len = 30
                            filled = int(bar_len * pct / 100)
                            bar = '█' * filled + '░' * (bar_len - filled)
                            print(f"\n📊 下载进度: [{bar}] {pct}%", end="")
                    else:
                        print(f"\n📝 {line_stripped}")
                    
                    detector.update(line)
            except:
                pass
            
            time.sleep(0.1)
        
        # Read remaining output
        remaining = process.stdout.read()
        if remaining:
            print(remaining.rstrip())
            detector.update(remaining)
        
        process.wait()
        success = process.returncode == 0
        
        # Print final download size
        final_size, file_count = get_download_progress()
        total_mb = final_size / (1024 * 1024)
        print(f"\n📦 下载完成: {total_mb:.1f} MB ({file_count} 个文件)")
        
        return success, detector.has_progress
        
    except Exception as e:
        print(f"\n❌ 安装过程出错: {e}")
        return False, detector.has_progress


def prompt_mirror_selection(default_mirror=None):
    """
    Prompt user to select a mirror source.
    
    Args:
        default_mirror: Default mirror to use in non-interactive mode (1-3)
    
    Returns:
        Mirror URL or None
    """
    print_mirrors()
    
    # If in non-interactive mode or default provided
    if default_mirror or not sys.stdin.isatty():
        if default_mirror:
            try:
                choice = int(default_mirror)
                if 1 <= choice <= len(MIRROR_SOURCES):
                    mirror_name = list(MIRROR_SOURCES.keys())[choice - 1]
                    mirror_url, _ = MIRROR_SOURCES[mirror_name]
                    print(f"\n✅ 自动选择镜像源: {mirror_name}")
                    return mirror_url
            except ValueError:
                pass
        
        # Default to taobao (first mirror) in non-interactive mode
        if not sys.stdin.isatty():
            mirror_name = list(MIRROR_SOURCES.keys())[0]
            mirror_url, _ = MIRROR_SOURCES[mirror_name]
            print(f"\n✅ 非交互模式，自动选择镜像源: {mirror_name}")
            return mirror_url
    
    while True:
        try:
            choice = input("\n请选择镜像源 (1-2)，或按 Enter 跳过: ").strip()
            
            if not choice:
                return None
            
            choice = int(choice)
            if 1 <= choice <= len(MIRROR_SOURCES):
                mirror_name = list(MIRROR_SOURCES.keys())[choice - 1]
                mirror_url, _ = MIRROR_SOURCES[mirror_name]
                return mirror_url
            else:
                print(f"❌ 无效选择，请输入 1-{len(MIRROR_SOURCES)}")
        except ValueError:
            print("❌ 请输入数字")
        except KeyboardInterrupt:
            print("\n\n👋 已取消安装")
            sys.exit(0)
        except EOFError:
            # Non-interactive mode, use default
            mirror_name = list(MIRROR_SOURCES.keys())[0]
            mirror_url, _ = MIRROR_SOURCES[mirror_name]
            print(f"\n✅ 自动选择镜像源: {mirror_name}")
            return mirror_url


def check_playwright_installed():
    """Check if playwright is installed."""
    try:
        import playwright
        return True
    except ImportError:
        return False


def check_browser_installed():
    """Check if Chromium browser is already installed."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            # Try to launch browser briefly
            browser = p.chromium.launch(headless=True)
            browser.close()
            return True
    except Exception:
        return False


def main():
    """Main installation flow with DNS detection and fallback support."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Playwright Chromium Browser Installer with Progress Detection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 install_browser.py                    # Interactive mode
  python3 install_browser.py --mirror 1         # Use taobao mirror
  python3 install_browser.py --mirror 2         # Use tsinghua mirror
  python3 install_browser.py --skip-official    # Skip official source, use mirror directly
  python3 install_browser.py --check-dns        # Check DNS resolution only
        """
    )
    parser.add_argument(
        "--mirror", "-m",
        type=int,
        choices=[1, 2],
        help="Mirror source: 1=taobao, 2=tsinghua"
    )
    parser.add_argument(
        "--skip-official", "-s",
        action="store_true",
        help="Skip official source, use mirror directly"
    )
    parser.add_argument(
        "--check-dns",
        action="store_true",
        help="Check DNS resolution for official CDN"
    )
    args = parser.parse_args()
    
    print_banner()
    
    # DNS check only mode
    if args.check_dns:
        print("🔍 检查官方 CDN DNS 解析...")
        success, ip, error = check_dns_resolution()
        if success:
            print(f"✅ DNS 解析成功: {OFFICIAL_CDN} -> {ip}")
            conn_success, conn_error = test_cdn_connectivity()
            if conn_success:
                print("✅ CDN 连接正常")
            else:
                print(f"⚠️  CDN 连接失败: {conn_error}")
        else:
            print(f"❌ DNS 解析失败: {error}")
            print_dns_troubleshooting()
        return 0 if success else 1
    
    # Check if browser is already installed
    if check_browser_installed():
        print("✅ Chromium 浏览器已安装，无需重复安装")
        return 0
    
    # If --skip-official or --mirror specified, go directly to mirror
    if args.skip_official or args.mirror:
        # First ensure playwright is installed
        if not check_playwright_installed():
            install_playwright_via_pip(use_mirror=True)
        
        mirror_url = None
        if args.mirror:
            mirror_name = list(MIRROR_SOURCES.keys())[args.mirror - 1]
            mirror_url, _ = MIRROR_SOURCES[mirror_name]
            print(f"📍 使用指定镜像源: {mirror_name}")
        else:
            mirror_url = prompt_mirror_selection(default_mirror=args.mirror)
        
        if mirror_url:
            success, _ = run_install_with_mirror(mirror_url)
            
            if success:
                print("\n" + "=" * 60)
                print("✅ Chromium 浏览器安装成功！")
                print("=" * 60)
                return 0
    else:
        # === Step 1: Query mirror sources FIRST to determine compatible Playwright version ===
        # 国内镜像源作为主要下载方式，类似 pip 使用 PyPI 镜像
        
        print("\n" + "=" * 60)
        print("🔍 步骤1: 查询国内镜像源可用版本")
        print("=" * 60)
        
        # Query mirror for available versions
        mirror_chromium_versions = {}
        for name, (url, desc) in MIRROR_SOURCES.items():
            print(f"  查询 {name}...", end=" ")
            version = get_mirror_latest_chromium_version(url)
            mirror_chromium_versions[name] = version
            if version:
                print(f"最新版本: v{version}")
            else:
                print("查询失败")
        
        # Find best mirror (highest version)
        best_mirror = None
        best_version = 0
        for name, version in mirror_chromium_versions.items():
            if version > best_version:
                best_version = version
                best_mirror = name
        
        if best_mirror and best_version > 0:
            print(f"\n✅ 镜像源最新版本: v{best_version} ({best_mirror})")
        else:
            print("\n⚠️  无法获取镜像源版本信息，将使用官方 CDN")
        
        # === Step 2: Install/Configure Playwright ===
        # Determine the best Playwright version based on mirror availability
        
        target_pw_version = None
        current_pw_version = get_playwright_version()
        
        if best_mirror and best_version > 0:
            # Check if current Playwright is compatible with mirror
            required_build = get_chromium_build_for_playwright(current_pw_version) if current_pw_version else 0
            
            if current_pw_version and required_build <= best_version:
                print(f"\n✅ 当前 Playwright {current_pw_version} 与镜像源兼容")
                target_pw_version = current_pw_version
            else:
                # Need to find compatible Playwright version
                compatible_pw = find_compatible_playwright_version(best_version)
                if compatible_pw:
                    print(f"\n💡 镜像源支持的最高版本: Chromium v{best_version}")
                    print(f"💡 推荐安装 Playwright {compatible_pw} 以使用国内镜像")
                    
                    if current_pw_version:
                        print(f"📋 当前已安装 Playwright {current_pw_version}，需要降级")
                    
                    # Auto install compatible version
                    if not sys.stdin.isatty():
                        print(f"\n📦 自动安装兼容版本 Playwright {compatible_pw}...")
                        if install_playwright_version(compatible_pw):
                            print(f"✅ Playwright {compatible_pw} 安装成功")
                            target_pw_version = compatible_pw
                        else:
                            print("❌ Playwright 安装失败，将尝试官方 CDN")
                    else:
                        try:
                            response = input("\n是否安装兼容版本? (y/n): ").strip().lower()
                            if response == 'y':
                                print(f"\n📦 安装 Playwright {compatible_pw}...")
                                if install_playwright_version(compatible_pw):
                                    print(f"✅ Playwright {compatible_pw} 安装成功")
                                    target_pw_version = compatible_pw
                                else:
                                    print("❌ Playwright 安装失败")
                            else:
                                print("📋 将使用官方 CDN 下载")
                        except (EOFError, KeyboardInterrupt):
                            print("\n📋 将使用官方 CDN 下载")
                else:
                    print(f"\n⚠️  找不到匹配 Chromium v{best_version} 的 Playwright 版本")
                    print("📋 将使用官方 CDN 下载")
        else:
            # No mirror available, use current or install latest
            if not current_pw_version:
                print("\n📦 安装最新版 Playwright...")
                success, target_pw_version = install_playwright_via_pip(use_mirror=True)
                if not success:
                    print("\n❌ Playwright 安装失败")
                    return 1
            else:
                target_pw_version = current_pw_version
                print(f"\n✅ Playwright 已安装: {current_pw_version}")
        
        # Install Playwright if not installed
        if not check_playwright_installed():
            print("\n" + "=" * 60)
            print("📦 安装 Playwright Python 包")
            print("=" * 60)
            print("💡 pip 安装使用 PyPI 镜像，中国大陆可正常访问")
            
            if target_pw_version:
                success, _ = install_playwright_version(target_pw_version)
            else:
                success, target_pw_version = install_playwright_via_pip(use_mirror=True)
            
            if not success:
                print("\n❌ Playwright Python 包安装失败")
                print("📋 请检查网络连接或手动安装: pip install playwright")
                return 1
        elif target_pw_version and target_pw_version != current_pw_version:
            # Need to install specific version
            print(f"\n📦 切换到 Playwright {target_pw_version}...")
            if not install_playwright_version(target_pw_version):
                print("⚠️  版本切换失败，继续使用当前版本")
        
        # === Step 3: Install Chromium browser ===
        print("\n" + "=" * 60)
        print("📦 步骤2: 安装 Chromium 浏览器")
        print("=" * 60)
        
        current_pw_version = get_playwright_version()
        required_build = get_chromium_build_for_playwright(current_pw_version) if current_pw_version else 0
        
        print(f"\n📋 当前 Playwright 版本: {current_pw_version or '未知'}")
        print(f"📋 需要 Chromium build: v{required_build or '未知'}")
        
        # Try mirror first if available and compatible
        mirror_success = False
        if best_mirror and best_version >= required_build:
            mirror_url, _ = MIRROR_SOURCES[best_mirror]
            print(f"\n🌐 使用国内镜像源: {best_mirror}")
            print("💡 国内镜像源下载速度更快")
            
            success, _ = run_install_with_mirror(mirror_url)
            
            if success:
                print("\n" + "=" * 60)
                print("✅ Chromium 浏览器安装成功！")
                print("=" * 60)
                return 0
            else:
                print("\n⚠️  镜像源下载失败，尝试官方 CDN...")
                mirror_success = False
        
        # === Fallback: Official CDN ===
        print("\n" + "=" * 60)
        print("📍 使用官方 CDN 下载")
        print("=" * 60)
        
        # Check and display system proxy settings
        has_proxy = print_proxy_info()
        if has_proxy:
            print("💡 代理设置将自动用于下载")
        
        dns_success, dns_ip, dns_error = check_dns_resolution()
        
        if dns_success:
            print(f"✅ DNS 解析成功: {OFFICIAL_CDN} -> {dns_ip}")
            if has_proxy:
                print("🌐 通过系统代理下载...")
            success, had_progress = run_install_with_mirror()
            
            if success:
                print("\n" + "=" * 60)
                print("✅ Chromium 浏览器安装成功！")
                print("=" * 60)
                return 0
            
            # If stalled (no progress in first 10 seconds)
            if not had_progress:
                print("\n" + "-" * 60)
                print("⚠️  官方 CDN 下载停滞")
                print("-" * 60)
        else:
            # DNS resolution failed
            print(f"❌ DNS 解析失败: {dns_error}")
            print_dns_troubleshooting()
        
        # Get current Playwright version and required chromium build
        current_pw_version = get_playwright_version()
        required_build = get_chromium_build_for_playwright(current_pw_version) if current_pw_version else 0
        
        print(f"\n📋 当前 Playwright 版本: {current_pw_version or '未知'}")
        print(f"📋 需要 Chromium build: v{required_build or '未知'}")
        
        # Query mirror for available versions
        print("\n🔍 查询镜像源可用版本...")
        mirror_chromium_versions = {}
        for name, (url, desc) in MIRROR_SOURCES.items():
            print(f"  查询 {name}...", end=" ")
            version = get_mirror_latest_chromium_version(url)
            mirror_chromium_versions[name] = version
            if version:
                print(f"最新版本: v{version}")
            else:
                print("查询失败")
        
        # Find best mirror (highest version)
        best_mirror = None
        best_version = 0
        for name, version in mirror_chromium_versions.items():
            if version > best_version:
                best_version = version
                best_mirror = name
        
        if not best_mirror or best_version == 0:
            print("\n❌ 无法获取镜像源版本信息")
            print("\n📋 备选方案：")
            print("  1. 使用 Docker: docker run -it mcr.microsoft.com/playwright/python:v1.40.0-jammy")
            print("  2. 纯 API 模式: 跳过浏览器安装，使用 GitHub REST API 功能")
            return 1
        
        print(f"\n✅ 镜像源最新版本: v{best_version} ({best_mirror})")
        
        # Check version compatibility
        if required_build > best_version:
            print(f"\n⚠️  版本不兼容!")
            print(f"  当前 Playwright {current_pw_version} 需要 Chromium v{required_build}")
            print(f"  镜像源最新版本为 v{best_version}")
            
            # Find compatible Playwright version
            compatible_pw = find_compatible_playwright_version(best_version)
            if compatible_pw:
                print(f"\n💡 建议降级到 Playwright {compatible_pw} (匹配 Chromium v{best_version})")
                
                # Ask user for confirmation
                try:
                    response = input("\n是否自动降级安装? (y/n): ").strip().lower()
                    if response == 'y':
                        print(f"\n📦 降级安装 Playwright {compatible_pw}...")
                        if install_playwright_version(compatible_pw):
                            print(f"✅ Playwright {compatible_pw} 安装成功")
                            # Update required build
                            required_build = best_version
                        else:
                            print("❌ Playwright 降级失败")
                            return 1
                    else:
                        print("❌ 用户取消安装")
                        return 1
                except (EOFError, KeyboardInterrupt):
                    print("\n❌ 用户取消安装")
                    return 1
            else:
                print(f"\n❌ 找不到匹配 Chromium v{best_version} 的 Playwright 版本")
                return 1
        
        # Use best mirror
        mirror_url, _ = MIRROR_SOURCES[best_mirror]
        print(f"\n🌐 使用镜像源: {best_mirror}")
        
        # Install with mirror
        success, _ = run_install_with_mirror(mirror_url)
        
        if success:
            print("\n" + "=" * 60)
            print("✅ Chromium 浏览器安装成功！")
            print("=" * 60)
            return 0
    
    # All attempts failed
    print("\n" + "=" * 60)
    print("❌ 安装失败")
    print("=" * 60)
    print("\n📋 备选方案：")
    print("  1. 使用 Docker: docker run -it mcr.microsoft.com/playwright/python:v1.40.0-jammy")
    print("  2. 纯 API 模式: 跳过浏览器安装，使用 GitHub REST API 功能")
    print("  3. 手动设置镜像: PLAYWRIGHT_DOWNLOAD_HOST=https://registry.npmmirror.com/-/binary/playwright python3 -m playwright install chromium")
    
    return 1


if __name__ == "__main__":
    sys.exit(main())