#!/usr/bin/env python3
"""
Download book from URL with optional proxy support.
This script is part of the kindle-download skill for OpenClaw.
Configuration is read from ~/.config/kindle-download/auth.json
"""
import sys
import os
import json
import requests
import re
from pathlib import Path
from urllib.parse import unquote

def get_config_path():
    """Get config file path, prioritizing user config directory"""
    home = Path.home()
    user_config = home / ".config" / "kindle-download" / "auth.json"
    skill_config = home / ".openclaw" / "workspace" / "skills" / "kindle-download" / "auth.json"
    
    if user_config.exists():
        return str(user_config)
    if skill_config.exists():
        return str(skill_config)
    return str(user_config)

def load_config():
    """Load configuration from auth.json"""
    config_path = get_config_path()
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"WARNING: Could not load config: {e}")
        return {}

def download(url, save_dir, book_title, cookie_str=None):
    """
    Download a book from URL.

    Args:
        url: Download URL
        save_dir: Directory to save the file
        book_title: Title of the book
        cookie_str: Optional cookie string for authentication

    Returns:
        bool: True if download successful, False otherwise
    """
    config = load_config()
    proxy_server = config.get("proxy_server", "")

    proxies = None
    if proxy_server:
        proxies = { "http": proxy_server, "https": proxy_server }

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://zlib.li/"
    }
    if cookie_str:
        headers["Cookie"] = cookie_str

    try:
        os.makedirs(save_dir, exist_ok=True)

        request_kwargs = { "headers": headers, "stream": True, "timeout": 90 }
        if proxies:
            request_kwargs["proxies"] = proxies

        response = requests.get(url, **request_kwargs)
        response.raise_for_status()

        temp_path = os.path.join(save_dir, "downloading.tmp")
        with open(temp_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        with open(temp_path, "rb") as f:
            magic = f.read(4)
            if magic != b"PK\x03\x04" and b"<html" in magic.lower():
                print("ERROR: DOWNLOADED_CONTENT_IS_HTML")
                os.remove(temp_path)
                return False

        content_disposition = response.headers.get("Content-Disposition")
        filename = ""
        if content_disposition:
            fname_match = re.findall("filename\\*?=[\\'\"]?(?:UTF-8\\'\")?([^\\'\"\\n;]+)", content_disposition)
            if fname_match:
                filename = unquote(fname_match[0])

        if not filename:
            filename = f"{book_title}.epub"

        filename = re.sub(r"[\\/:*?\\"<>|]", "_", filename)
        final_path = os.path.join(save_dir, filename)
        os.rename(temp_path, final_path)

        print(f"SUCCESS_PATH:{final_path}")
        return True

    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 download_book.py <url> <save_dir> <book_title> [cookie_str]")
        print("  url: Download URL")
        print("  save_dir: Directory to save the file")
        print("  book_title: Title of the book")
        print("  cookie_str: Optional cookie string for authentication")
    else:
        cookie = sys.argv[4] if len(sys.argv) > 4 else None
        download(sys.argv[1], sys.argv[2], sys.argv[3], cookie)
