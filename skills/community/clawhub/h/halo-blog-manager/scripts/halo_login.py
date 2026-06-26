#!/usr/bin/env python3
"""
Halo Blog Manager - Login and Session Management

This script handles authentication with Halo CMS:
1. Fetches login page to get CSRF token and RSA public key
2. Encrypts password using RSA
3. Logs in and saves session cookies
"""

import json
import os
import re
import requests
from pathlib import Path

# JSEncrypt-compatible RSA encryption
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5
import base64

CONFIG_DIR = Path.home() / "halo-manager"
CONFIG_FILE = CONFIG_DIR / "config.json"
SESSION_FILE = CONFIG_DIR / "session.json"


def ensure_config_dir():
    """Ensure config directory exists."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def save_config(blog_url: str, username: str, password: str):
    """Save credentials to config file."""
    ensure_config_dir()
    config = {
        "blog_url": blog_url.rstrip("/"),
        "username": username,
        "password": password
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    print(f"✅ Config saved to {CONFIG_FILE}")


def load_config() -> dict:
    """Load credentials from config file."""
    if not CONFIG_FILE.exists():
        return None
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def encrypt_password(public_key_pem: str, password: str) -> str:
    """Encrypt password using RSA public key (PKCS1 v1.5)."""
    # Parse public key
    key = RSA.import_key(public_key_pem)
    cipher = PKCS1_v1_5.new(key)
    
    # Encrypt
    encrypted = cipher.encrypt(password.encode("utf-8"))
    
    # Base64 encode
    return base64.b64encode(encrypted).decode("utf-8")


def login(blog_url: str, username: str, password: str) -> requests.Session:
    """
    Login to Halo blog and return authenticated session.
    """
    session = requests.Session()
    
    # Step 1: Get login page for CSRF token and public key
    login_url = f"{blog_url}/login"
    response = session.get(login_url)
    response.raise_for_status()
    
    html = response.text
    
    # Extract CSRF token
    csrf_match = re.search(r'name="_csrf".*?value="([^"]+)"', html)
    if not csrf_match:
        # Try alternative pattern
        csrf_match = re.search(r'<input[^>]*name="_csrf"[^>]*value="([^"]+)"', html)
    csrf_token = csrf_match.group(1) if csrf_match else None
    
    # Extract RSA public key
    key_match = re.search(r'publicKey\s*=\s*["\']([^"\']+)["\']', html)
    if not key_match:
        # Try to find in script tag
        key_match = re.search(r'-----BEGIN PUBLIC KEY-----[^-]+-----END PUBLIC KEY-----', html, re.DOTALL)
    
    if key_match:
        public_key = key_match.group(1) if key_match.lastindex else key_match.group(0)
    else:
        # Try to get from API
        key_response = session.get(f"{blog_url}/api/public/key")
        if key_response.ok:
            public_key = key_response.json().get("publicKey", "")
        else:
            raise ValueError("Could not retrieve RSA public key")
    
    # Step 2: Encrypt password
    encrypted_password = encrypt_password(public_key, password)
    
    # Step 3: Login
    login_data = {
        "username": username,
        "password": encrypted_password,
        "_csrf": csrf_token
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/html,application/xhtml+xml"
    }
    
    response = session.post(
        login_url,
        data=login_data,
        headers=headers,
        allow_redirects=False
    )
    
    # Check for successful login (302 redirect to /uc or /console)
    if response.status_code == 302:
        location = response.headers.get("Location", "")
        if "/uc" in location or "/console" in location:
            print("✅ Login successful!")
            
            # Save session info
            save_session(session)
            return session
    
    # If we get here, login failed
    raise ValueError(f"Login failed: Status {response.status_code}")


def save_session(session: requests.Session):
    """Save session cookies to file."""
    ensure_config_dir()
    cookies = {}
    for cookie in session.cookies:
        cookies[cookie.name] = {
            "value": cookie.value,
            "domain": cookie.domain,
            "path": cookie.path
        }
    with open(SESSION_FILE, "w") as f:
        json.dump(cookies, f, indent=2)


def load_session(blog_url: str) -> requests.Session:
    """Load session from file or create new one."""
    config = load_config()
    if not config:
        raise ValueError("No config found. Please run setup first.")
    
    if SESSION_FILE.exists():
        session = requests.Session()
        with open(SESSION_FILE, "r") as f:
            cookies = json.load(f)
            for name, data in cookies.items():
                session.cookies.set(name, data["value"], domain=data.get("domain"), path=data.get("path"))
        
        # Verify session is still valid
        try:
            response = session.get(f"{config['blog_url']}/apis/api.console.halo.run/v1alpha1/users/-")
            if response.ok:
                return session
        except:
            pass
    
    # Session invalid or expired, re-login
    return login(config["blog_url"], config["username"], config["password"])


def main():
    """Interactive setup."""
    print("🔧 Halo Blog Manager Setup")
    print("-" * 30)
    
    blog_url = input("Blog URL (e.g., https://blog.example.com): ").strip()
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    # Save config
    save_config(blog_url, username, password)
    
    # Test login
    print("\n🔐 Testing login...")
    try:
        session = login(blog_url, username, password)
        print("✅ Setup complete! You can now use the Halo Manager skill.")
    except Exception as e:
        print(f"❌ Login failed: {e}")
        print("Please check your credentials and try again.")


if __name__ == "__main__":
    main()
