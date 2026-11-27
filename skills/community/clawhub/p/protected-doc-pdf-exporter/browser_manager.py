"""
Cross-platform Browser & Profile Manager
Discovers browser binaries, handles session cookies/profiles across Linux, macOS, and Windows,
and manages headless Chrome/Edge processes with DevTools Protocol (CDP).
"""

import os
import sys
import socket
import shutil
import platform
import subprocess
import urllib.request
import json
import asyncio

def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]

def get_platform_name() -> str:
    system = platform.system().lower()
    if 'linux' in system:
        return 'linux'
    elif 'darwin' in system:
        return 'macos'
    elif 'windows' in system:
        return 'windows'
    return 'unknown'

def find_browser_binary(preferred_browser='chrome') -> str:
    plat = get_platform_name()
    candidates = []

    if preferred_browser.lower() == 'edge':
        if plat == 'linux':
            candidates = ['microsoft-edge', 'microsoft-edge-stable', 'microsoft-edge-dev']
        elif plat == 'macos':
            candidates = ['/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge']
        elif plat == 'windows':
            candidates = [
                os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
                os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
            ]
    else:  # Chrome / Chromium / Default
        if plat == 'linux':
            candidates = [
                'google-chrome', 'google-chrome-stable',
                'chromium', 'chromium-browser',
                'brave-browser', 'microsoft-edge'
            ]
        elif plat == 'macos':
            candidates = [
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                '/Applications/Chromium.app/Contents/MacOS/Chromium',
                '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
                '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
            ]
        elif plat == 'windows':
            candidates = [
                os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
                os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
                os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
                os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
            ]

    for candidate in candidates:
        if os.path.isabs(candidate) and os.path.exists(candidate):
            return candidate
        which_path = shutil.which(candidate)
        if which_path:
            return which_path

    raise FileNotFoundError(f"Supported browser (Chrome/Edge/Chromium) binary not found on {plat}.")

def get_default_user_data_dir(preferred_browser='chrome') -> str:
    plat = get_platform_name()
    home = os.path.expanduser('~')

    if preferred_browser.lower() == 'edge':
        if plat == 'linux':
            return os.path.join(home, '.config', 'microsoft-edge')
        elif plat == 'macos':
            return os.path.join(home, 'Library', 'Application Support', 'Microsoft Edge')
        elif plat == 'windows':
            return os.path.expandvars(r"%LocalAppData%\Microsoft\Edge\User Data")
    else:
        if plat == 'linux':
            for name in ['google-chrome', 'chromium', 'microsoft-edge']:
                p = os.path.join(home, '.config', name)
                if os.path.exists(p):
                    return p
            return os.path.join(home, '.config', 'google-chrome')
        elif plat == 'macos':
            return os.path.join(home, 'Library', 'Application Support', 'Google', 'Chrome')
        elif plat == 'windows':
            return os.path.expandvars(r"%LocalAppData%\Google\Chrome\User Data")

    return os.path.join(home, '.config', 'google-chrome')

def clone_session_profile(src_dir: str, dest_dir: str):
    """
    Clones essential session files (Cookies, Preferences, Local State)
    to a temporary user-data-dir so Chrome can run concurrently without locks.
    """
    if os.path.exists(dest_dir):
        try:
            shutil.rmtree(dest_dir)
        except Exception:
            pass

    os.makedirs(os.path.join(dest_dir, 'Default'), exist_ok=True)
    src_default = os.path.join(src_dir, 'Default')

    if os.path.exists(src_default):
        items = ['Cookies', 'Network', 'Preferences', 'Secure Preferences']
        for item in items:
            src_item = os.path.join(src_default, item)
            dest_item = os.path.join(dest_dir, 'Default', item)
            if os.path.exists(src_item):
                try:
                    if os.path.isdir(src_item):
                        shutil.copytree(src_item, dest_item)
                    else:
                        shutil.copy2(src_item, dest_item)
                except Exception:
                    pass

    local_state = os.path.join(src_dir, 'Local State')
    if os.path.exists(local_state):
        try:
            shutil.copy2(local_state, os.path.join(dest_dir, 'Local State'))
        except Exception:
            pass

class BrowserSession:
    def __init__(self, url: str, user_data_dir: str = None, browser_type: str = 'chrome', headless: bool = True, window_size: tuple = (1920, 1080)):
        self.url = url
        self.browser_type = browser_type
        self.headless = headless
        self.window_size = window_size
        self.binary_path = find_browser_binary(browser_type)
        self.orig_user_dir = user_data_dir or get_default_user_data_dir(browser_type)
        self.port = find_free_port()
        self.temp_user_dir = f"/tmp/doc_exporter_profile_{self.port}"
        self.proc = None
        self.ws_url = None

    async def start(self):
        print(f"[*] Initializing browser session with profile from: {self.orig_user_dir}")
        clone_session_profile(self.orig_user_dir, self.temp_user_dir)

        w, h = self.window_size
        cmd = [
            self.binary_path,
            f"--remote-debugging-port={self.port}",
            f"--window-size={w},{h}",
            f"--user-data-dir={self.temp_user_dir}",
            "--disable-gpu",
            "--no-first-run",
            "--no-default-browser-check",
            self.url
        ]

        if self.headless:
            cmd.insert(1, "--headless=new")

        print(f"[*] Spawning {os.path.basename(self.binary_path)} on CDP port {self.port}...")
        self.proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Wait for CDP endpoint
        for _ in range(30):
            await asyncio.sleep(0.5)
            try:
                resp = urllib.request.urlopen(f'http://127.0.0.1:{self.port}/json', timeout=1)
                tabs = json.loads(resp.read().decode())
                page_tabs = [t for t in tabs if t.get('type') == 'page']
                if page_tabs:
                    self.ws_url = page_tabs[0]['webSocketDebuggerUrl']
                    print(f"[✓] Connected to CDP page: {page_tabs[0].get('title', '')[:40]}")
                    return self.ws_url
            except Exception:
                continue

        raise TimeoutError(f"Failed to connect to browser CDP on port {self.port}.")

    async def close(self):
        if self.proc:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=3)
            except Exception:
                self.proc.kill()
            self.proc = None

        if os.path.exists(self.temp_user_dir):
            try:
                shutil.rmtree(self.temp_user_dir)
            except Exception:
                pass
