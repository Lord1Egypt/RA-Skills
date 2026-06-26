#!/usr/bin/env python3
"""
Send ebook to Kindle via email.
This script is part of the kindle-download skill for OpenClaw.

SECURITY:
- Supports environment variables for credentials (recommended)
- Validates file paths to prevent directory traversal attacks
- All inputs are sanitized before use

Credentials can be provided via:
1. Environment variables (recommended, higher priority)
2. Configuration file (~/.config/kindle-download/auth.json)
"""

import json
import smtplib
import sys
import os
import re
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from pathlib import Path

# 安全的允许目录列表
ALLOWED_DIRS = [
    Path("/tmp/kindle_downloads"),
    Path.home() / ".config" / "kindle-download",
]

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {".epub", ".pdf", ".mobi", ".azw3"}

def get_config_path():
    """Get config file path, prioritizing user config directory"""
    home = Path.home()
    user_config = home / ".config" / "kindle-download" / "auth.json"
    skill_config = home / ".openclaw" / "workspace" / "skills" / "kindle-download" / "auth.json"
    
    if user_config.exists():
        return str(user_config)
    if skill_config.exists():
        return str(skill_config)
    
    # Default to user config location
    return str(user_config)

def get_credentials():
    """
    Get credentials from environment variables or config file.
    Environment variables take priority.
    
    Environment variables:
        KINDLE_SMTP_EMAIL      - SMTP sender email
        KINDLE_SMTP_AUTH_CODE  - SMTP authorization code
        KINDLE_SMTP_SERVER     - SMTP server (default: smtp.163.com)
        KINDLE_SMTP_PORT       - SMTP port (default: 465)
        KINDLE_RECEIVER_EMAIL  - Kindle receiver email
        KINDLE_PROXY_SERVER    - Proxy server (optional)
    
    Config file fields (fallback):
        email, auth_code, smtp_server, smtp_port, send_kindle_email, proxy_server
    """
    # First try environment variables
    env_creds = {
        "email": os.environ.get("KINDLE_SMTP_EMAIL", ""),
        "auth_code": os.environ.get("KINDLE_SMTP_AUTH_CODE", ""),
        "smtp_server": os.environ.get("KINDLE_SMTP_SERVER", "smtp.163.com"),
        "smtp_port": int(os.environ.get("KINDLE_SMTP_PORT", "465")),
        "send_kindle_email": os.environ.get("KINDLE_RECEIVER_EMAIL", ""),
        "proxy_server": os.environ.get("KINDLE_PROXY_SERVER", ""),
    }
    
    # Check if all required env vars are set
    required = ["email", "auth_code", "send_kindle_email"]
    if all(env_creds[k] for k in required):
        print("LOG: Using credentials from environment variables")
        return env_creds
    
    # Fallback to config file
    print("LOG: Using credentials from config file")
    config_path = get_config_path()
    
    try:
        with open(config_path, "r") as f:
            file_creds = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Configuration file not found at {config_path}")
        print("Please either:")
        print("  1. Set environment variables: KINDLE_SMTP_EMAIL, KINDLE_SMTP_AUTH_CODE, KINDLE_RECEIVER_EMAIL")
        print("  2. Create config file at: " + config_path)
        return None
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in configuration file: {e}")
        return None
    
    # Merge with env vars (env vars take priority)
    return {
        "email": env_creds["email"] or file_creds.get("email", ""),
        "auth_code": env_creds["auth_code"] or file_creds.get("auth_code", ""),
        "smtp_server": env_creds["smtp_server"] or file_creds.get("smtp_server", "smtp.163.com"),
        "smtp_port": env_creds["smtp_port"] or file_creds.get("smtp_port", 465),
        "send_kindle_email": env_creds["send_kindle_email"] or file_creds.get("send_kindle_email", ""),
        "proxy_server": env_creds["proxy_server"] or file_creds.get("proxy_server", ""),
    }

def validate_file_path(file_path):
    """
    验证文件路径的安全性
    
    Returns:
        tuple: (is_valid, resolved_path_or_error)
    """
    if not file_path:
        return False, "文件路径不能为空"
    
    try:
        # 解析路径
        path = Path(file_path).resolve()
    except Exception as e:
        return False, f"无效的文件路径: {e}"
    
    # 检查路径遍历攻击
    if ".." in str(file_path):
        return False, "路径不能包含 '..' 目录遍历字符"
    
    # 检查文件扩展名
    ext = path.suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"不支持的文件类型: {ext}。允许的类型: {', '.join(ALLOWED_EXTENSIONS)}"
    
    # 检查文件是否在允许的目录内
    is_allowed = False
    for allowed_dir in ALLOWED_DIRS:
        try:
            # 检查路径是否在允许目录下
            path.relative_to(allowed_dir.resolve())
            is_allowed = True
            break
        except ValueError:
            continue
    
    if not is_allowed:
        allowed_dirs_str = ", ".join(str(d) for d in ALLOWED_DIRS)
        return False, f"文件路径不在允许的目录内。允许的目录: {allowed_dirs_str}"
    
    # 检查文件是否存在
    if not path.exists():
        return False, f"文件不存在: {path}"
    
    # 检查文件是否是常规文件
    if not path.is_file():
        return False, f"路径不是文件: {path}"
    
    return True, str(path)

def sanitize_filename(filename):
    """
    清理文件名，移除危险字符
    """
    # 只保留安全字符
    sanitized = re.sub(r'[\\/:*?"<>|]', "_", filename)
    # 移除控制字符
    sanitized = re.sub(r"[\x00-\x1f]", "", sanitized)
    # 限制长度
    if len(sanitized) > 255:
        name, ext = os.path.splitext(sanitized)
        sanitized = name[:255-len(ext)] + ext
    
    return sanitized

def send_mail(file_path):
    """发送邮件到 Kindle"""
    
    # 首先验证文件路径
    is_valid, result = validate_file_path(file_path)
    if not is_valid:
        print(f"ERROR: {result}")
        return False
    
    safe_file_path = result
    
    # 加载配置
    config = get_credentials()
    if not config:
        return False
    
    # 验证配置项
    required_keys = ["email", "auth_code", "send_kindle_email"]
    for key in required_keys:
        if not config.get(key):
            print(f"ERROR: Missing required configuration: {key}")
            return False
    
    sender_email = config["email"]
    auth_code = config["auth_code"]
    smtp_server = config["smtp_server"]
    smtp_port = config["smtp_port"]
    receiver_email = config["send_kindle_email"]
    
    # 构建邮件
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = ""
    
    # 使用安全的文件名
    filename = sanitize_filename(os.path.basename(safe_file_path))
    
    try:
        with open(safe_file_path, "rb") as f:
            attachment_data = f.read()
    except IOError as e:
        print(f"ERROR: Cannot read file: {e}")
        return False
    
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment_data)
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment", filename=("utf-8", "", filename))
    msg.attach(part)
    
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, auth_code)
            server.send_message(msg)
        print("SUCCESS: Email sent to Kindle with proper filename.")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"ERROR: SMTP authentication failed: {e}")
        return False
    except smtplib.SMTPException as e:
        print(f"ERROR: SMTP error: {e}")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 send_kindle.py <file_path>")
        print("  file_path: Path to the ebook file (must be in allowed directories)")
        print("")
        print("Credentials can be set via environment variables:")
        print("  KINDLE_SMTP_EMAIL      - SMTP sender email")
        print("  KINDLE_SMTP_AUTH_CODE  - SMTP authorization code")
        print("  KINDLE_RECEIVER_EMAIL  - Kindle receiver email")
        print("  KINDLE_SMTP_SERVER     - SMTP server (default: smtp.163.com)")
        print("  KINDLE_SMTP_PORT       - SMTP port (default: 465)")
        sys.exit(1)
    
    success = send_mail(sys.argv[1])
    sys.exit(0 if success else 1)
