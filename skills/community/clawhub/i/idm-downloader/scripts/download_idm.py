#!/usr/bin/env python3
"""Download files using IDM (Internet Download Manager) via COM interface or command line."""

import subprocess
import sys
import os
import urllib.parse
import tempfile
import shutil

# Try to import idm COM module
IDM_COM_AVAILABLE = False
try:
    import pythoncom
    import win32com.client
    IDM_COM_AVAILABLE = True
except ImportError:
    pass


def get_filename_from_url(url):
    """Extract filename from URL, handling query parameters."""
    parsed = urllib.parse.urlparse(url)
    path = parsed.path
    filename = os.path.basename(path)
    if not filename or '.' not in filename:
        filename = "download"
    if '?' in filename:
        filename = filename.split('?')[0]
    return filename


def resolve_shortcut(shortcut_path):
    """Resolve a .lnk shortcut to get the target executable path."""
    try:
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(shortcut_path)
        return shortcut.Targetpath
    except Exception:
        return None


def find_idman_path():
    """Find IDMan.exe in common installation locations."""
    paths = [
        r"C:\Program Files (x86)\Internet Download Manager\IDMan.exe",
        r"C:\Program Files\Internet Download Manager\IDMan.exe",
        r"D:\Program Files (x86)\Internet Download Manager\IDMan.exe",
        r"D:\Program Files\Internet Download Manager\IDMan.exe",
        r"E:\Program Files (x86)\Internet Download Manager\IDMan.exe",
        r"E:\Program Files\Internet Download Manager\IDMan.exe",
    ]
    for path in paths:
        if os.path.exists(path):
            return path

    # Try to find IDM in registry
    try:
        import winreg
        for root in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
            try:
                key = winreg.OpenKey(root, r"SOFTWARE\Internet Download Manager")
                path, _ = winreg.QueryValueEx(key, "ExePath")
                winreg.CloseKey(key)
                if os.path.exists(path):
                    return path
            except WindowsError:
                pass
    except ImportError:
        pass

    # Search in Start Menu shortcuts
    start_menu_paths = [
        os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"),
        r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
        os.path.expandvars(r"%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs"),
    ]

    for start_menu in start_menu_paths:
        if not os.path.exists(start_menu):
            continue
        for root, dirs, files in os.walk(start_menu):
            # Check if path contains IDM related keywords
            root_lower = root.lower()
            if not any(kw in root_lower for kw in ['idm', 'internet download manager']):
                continue
            for file in files:
                if file.lower().endswith('.lnk'):
                    shortcut_path = os.path.join(root, file)
                    target = resolve_shortcut(shortcut_path)
                    if target and 'idman' in target.lower() and os.path.exists(target):
                        return target

    return None


def download_via_com(url, output_dir, filename):
    """Download using IDM COM interface."""
    try:
        pythoncom.CoInitialize()
        try:
            idm = win32com.client.Dispatch("IDMan.CIDWMControl.1")
            idm.Download(url, output_dir, filename, "", "", False, 0, True, False, True)
            return True
        finally:
            pythoncom.CoUninitialize()
    except Exception as e:
        print(f"COM download failed: {e}")
        return False


def download_via_commandline(url, output_dir, filename):
    """Download using IDM command line."""
    idman_path = find_idman_path()
    if not idman_path:
        print("Error: IDM not found")
        return False

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cmd = [
        idman_path,
        '/d', url,
        '/p', output_dir,
        '/f', filename,
        '/n'  # Start immediately
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("Download started successfully in IDM")
        return True
    else:
        if result.stderr:
            print(f"IDM error: {result.stderr}")
        return False


def download_with_idm(url, output_dir, filename=None):
    """Download file using IDM, trying COM first then command line."""
    if filename is None:
        filename = get_filename_from_url(url)

    print(f"Downloading: {url}")
    print(f"Output: {os.path.join(output_dir, filename)}")

    # Try COM interface first
    if IDM_COM_AVAILABLE:
        print("Trying COM interface...")
        if download_via_com(url, output_dir, filename):
            return True
        print("COM failed, falling back to command line...")

    # Fall back to command line
    print("Using command line interface...")
    return download_via_commandline(url, output_dir, filename)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python download_idm.py <url> [output_directory] [filename]")
        print("  url           - URL to download")
        print("  output_directory - Directory to save file (default: current directory)")
        print("  filename      - Optional filename")
        sys.exit(1)

    url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()
    filename = sys.argv[3] if len(sys.argv) > 3 else None

    success = download_with_idm(url, output_dir, filename)
    sys.exit(0 if success else 1)
