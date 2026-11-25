#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pan-downloader v0.6 — 网盘通入口（本机 + Windows + 远程设备）。

Ponytail full 设计原则：
- 不自己实现各家网盘协议；协议差异交给各网盘已有 CLI / AList / aria2。
- 核心只做四件事：识别链接、管理配置与目录、拼装引擎命令、执行并记录日志。
- 直链 HTTP 下载用系统 curl，开箱即用；分享链接走引擎适配器，未安装引擎时给出安装指引。

免费账号默认：并发 1、重试 3、断点续传、单任务日志。
会员账号可选：在配置里把 tier 设为 vip，引擎按自身能力提高并发，但本工具不做任何限速绕过。

远程设备不绑定品牌：只要目标开放 SSH/SFTP、WebDAV、SMB、S3 或 rclone，即可登记为 remote。
远程执行模式让 NAS 自己跑下载；远程落地模式在本机下载后通过 rclone 写入目标存储。
"""
from __future__ import annotations

import argparse
import copy
import getpass
import json
import os
import platform
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
import threading
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

APP = "pan-downloader"
VALID_TIERS = ("free", "vip", "auto")
KEYCHAIN_SERVICE = "com.example.pan-hub"
SECURITY_BIN = os.environ.get("PAN_SECURITY_BIN", "/usr/bin/security")
SKILL_DIR = Path(__file__).resolve().parent.parent


def platform_paths(system=None, env=None, home=None):
    """返回跨平台配置、状态、日志和默认下载目录。"""
    env = dict(os.environ if env is None else env)
    home = Path(home or env.get("HOME") or Path.home())
    system = (system or env.get("PAN_PLATFORM") or platform.system()).lower()
    if system.startswith("win"):
        appdata = Path(env.get("APPDATA") or (home / "AppData" / "Roaming"))
        local = Path(env.get("LOCALAPPDATA") or (home / "AppData" / "Local"))
        return {
            "config": appdata / APP / "config.json",
            "state": local / APP / "state",
            "log": local / APP / "logs" / (APP + ".log"),
            "download": home / "Downloads" / "网盘下载",
        }
    if system == "darwin":
        return {
            "config": home / ".config" / APP / "config.json",
            "state": home / ".local" / "share" / APP,
            "log": home / "Library" / "Logs" / (APP + ".log"),
            "download": home / "Downloads" / "网盘下载",
        }
    xdg_config = Path(env.get("XDG_CONFIG_HOME") or (home / ".config"))
    xdg_state = Path(env.get("XDG_STATE_HOME") or (home / ".local" / "state"))
    return {
        "config": xdg_config / APP / "config.json",
        "state": xdg_state / APP,
        "log": xdg_state / APP / "logs" / (APP + ".log"),
        "download": home / "Downloads" / "网盘下载",
    }


PATHS = platform_paths()
CONFIG_PATH = Path(os.environ.get("PAN_CONFIG", str(PATHS["config"])))
STATE_DIR = Path(os.environ.get("PAN_STATE_DIR", str(PATHS["state"])))
LOG_PATH = Path(os.environ.get("PAN_LOG", str(PATHS["log"])))
CREDENTIAL_REF_PREFIX = "credential:"

# ---------------------------------------------------------------- 网盘定义
DRIVES = {
    "baidu": {
        "name": "百度网盘",
        "domains": [
            "pan.baidu.com",
            "yun.baidu.com"
        ],
        "engine": "baidupcs",
        "reference": "references/01-百度网盘.md"
    },
    "aliyun": {
        "name": "阿里云盘",
        "domains": [
            "aliyundrive.com",
            "alipan.com",
            "www.aliyundrive.com"
        ],
        "engine": "alist",
        "reference": "references/02-阿里云盘.md"
    },
    "quark": {
        "name": "夸克网盘",
        "domains": [
            "pan.quark.cn"
        ],
        "engine": "quarkcli",
        "reference": "references/03-夸克网盘.md"
    },
    "tianyi": {
        "name": "天翼云盘",
        "domains": [
            "cloud.189.cn"
        ],
        "engine": "alist",
        "reference": "references/04-天翼云盘.md"
    },
    "thunder": {
        "name": "迅雷云盘",
        "domains": [
            "pan.xunlei.com"
        ],
        "engine": "alist",
        "reference": "references/05-迅雷云盘.md"
    },
    "115": {
        "name": "115 网盘",
        "domains": [
            "115.com",
            "anxia.com",
            "115cdn.com",
            "115.com.cn"
        ],
        "engine": "alist",
        "reference": "references/07-115网盘.md"
    },
    "123pan": {
        "name": "123 云盘",
        "domains": [
            "123pan.com",
            "123684.com",
            "123912.com",
            "123865.com"
        ],
        "engine": "alist",
        "reference": "references/08-123云盘.md"
    },
    "139yun": {
        "name": "移动云盘 / 和彩云",
        "domains": [
            "yun.139.com",
            "cloud.139.com",
            "caiyun.139.com"
        ],
        "engine": "alist",
        "reference": "references/09-移动云盘.md"
    },
    "wopan": {
        "name": "联通沃盘",
        "domains": [
            "wopan.wo.cn",
            "pan.wo.cn"
        ],
        "engine": "alist",
        "reference": "references/10-联通沃盘.md"
    },
    "uc": {
        "name": "UC 网盘",
        "domains": [
            "drive.uc.cn",
            "pan.uc.cn",
            "fast.uc.cn"
        ],
        "engine": "alist",
        "reference": "references/11-UC网盘.md"
    },
    "pikpak": {
        "name": "PikPak",
        "domains": [
            "mypikpak.com",
            "pikpak.com"
        ],
        "engine": "alist",
        "reference": "references/12-PikPak.md"
    },
    "jianguoyun": {
        "name": "坚果云",
        "domains": [
            "jianguoyun.com",
            "dav.jianguoyun.com"
        ],
        "engine": "webdav",
        "reference": "references/13-坚果云.md"
    },
    "onedrive": {
        "name": "OneDrive / SharePoint",
        "domains": [
            "onedrive.live.com",
            "1drv.ms",
            "sharepoint.com",
            "sharepoint.cn",
            "onedrive.com"
        ],
        "engine": "alist",
        "reference": "references/14-OneDrive与SharePoint.md"
    },
    "googledrive": {
        "name": "Google Drive",
        "domains": [
            "drive.google.com",
            "docs.google.com",
            "photos.google.com"
        ],
        "engine": "alist",
        "reference": "references/15-GoogleDrive.md"
    },
    "dropbox": {
        "name": "Dropbox",
        "domains": [
            "dropbox.com",
            "db.tt"
        ],
        "engine": "alist",
        "reference": "references/16-Dropbox.md"
    },
    "weiyun": {
        "name": "腾讯微云",
        "domains": [
            "weiyun.com"
        ],
        "engine": "alist",
        "reference": "references/17-腾讯微云.md"
    },
    "lanzou": {
        "name": "蓝奏云 / 新蓝奏",
        "domains": [
            "lanzou.com",
            "lanzoui.com",
            "lanzoux.com",
            "lanzouw.com",
            "lanzoup.com",
            "lanzoub.com",
            "lanzoue.com",
            "lanzous.com",
            "lanzoa.com",
            "lanzn.com",
            "ilanzou.com"
        ],
        "engine": "alist",
        "reference": "references/18-蓝奏云.md"
    },
    "wukong": {
        "name": "悟空网盘",
        "domains": [
            "wukong.com",
            "pan.wukong.com"
        ],
        "engine": "alist",
        "reference": "references/19-其他网盘.md"
    },
    "doubao": {
        "name": "豆包新盘",
        "domains": [
            "doubao.com",
            "pan.doubao.com",
            "www.doubao.com"
        ],
        "engine": "alist",
        "reference": "references/19-其他网盘.md"
    },
    "mega": {
        "name": "Mega",
        "domains": [
            "mega.nz",
            "mega.io"
        ],
        "engine": "alist",
        "reference": "references/19-其他网盘.md"
    },
    "terabox": {
        "name": "TeraBox",
        "domains": [
            "terabox.com",
            "1024terabox.com",
            "teraboxapp.com"
        ],
        "engine": "alist",
        "reference": "references/19-其他网盘.md"
    },
    "pcloud": {
        "name": "pCloud",
        "domains": [
            "pcloud.com",
            "pcloud.link"
        ],
        "engine": "alist",
        "reference": "references/19-其他网盘.md"
    },
    "protondrive": {
        "name": "Proton Drive",
        "domains": [
            "drive.proton.me",
            "proton.me"
        ],
        "engine": "alist",
        "reference": "references/19-其他网盘.md"
    },
    "yandexdisk": {
        "name": "Yandex Disk",
        "domains": [
            "disk.yandex.com",
            "disk.yandex.ru",
            "yadi.sk"
        ],
        "engine": "alist",
        "reference": "references/19-其他网盘.md"
    },
    "mediafire": {
        "name": "MediaFire",
        "domains": [
            "mediafire.com"
        ],
        "engine": "alist",
        "reference": "references/19-其他网盘.md"
    },
    "trainbit": {
        "name": "Trainbit",
        "domains": [
            "trainbit.com"
        ],
        "engine": "alist",
        "reference": "references/19-其他网盘.md"
    },
    "guangyapan": {
        "name": "光雅盘",
        "domains": [
            "guangyapan.com"
        ],
        "engine": "alist",
        "reference": "references/19-其他网盘.md"
    },
    "feijipan": {
        "name": "飞鸡云",
        "domains": [
            "feijipan.com"
        ],
        "engine": "alist",
        "reference": "references/19-其他网盘.md"
    },
    "shandian": {
        "name": "闪电盘",
        "domains": [
            "shandianpan.com"
        ],
        "engine": "alist",
        "reference": "references/19-其他网盘.md"
    },
    "chengtong": {
        "name": "城通网盘",
        "domains": [
            "ctfile.com",
            "400gb.com"
        ],
        "engine": "custom",
        "reference": "references/19-其他网盘.md"
    },
    "direct": {
        "name": "HTTP 直链",
        "domains": [],
        "engine": "http",
        "reference": "references/00-使用说明.md"
    }
}
ENGINE_BINARIES = {
    "alist": ["alist", "AList"],
    "baidupcs": ["BaiduPCS-Go", "baidupcs-go", "BaiduPCS"],
    "quarkcli": ["quark", "quark-cli", "kuake"],
    "aria2": ["aria2c"],
    "rclone": ["rclone"],
    "ssh": ["ssh"],
    "scp": ["scp"],
    "tar": ["tar"],
}
DEFAULT_CONFIG = {
    "version": 5,
    "download_root": "",
    "tier": "auto",
    "smart": {
        "auto_classify": False,
        "classify_root": ""
    },
    "http": {
        "retries": 3,
        "retry_delay": 5,
        "connect_timeout": 30,
        "timeout": 0,
        "max_connections_free": 1,
        "max_connections_vip": 4,
        "report_dir": "",
        "on_complete_hook": "",
        "range_split": False,
        "range_split_connections": 0,
        "live_status": False,
        "live_interval": 1.0,
        "live_dir": "",
        "schedule_at": ""
    },
    "remote": {
        "staging_root": "",
        "keep_staging": False
    },
    "transfer": {
        "allow_company_dest": False,
        "default_transfers": 4,
        "default_checkers": 8
    },
    "notify": {
        "work_weixin_secret": "",
        "bark_secret": "",
        "telegram_secret": "",
        "discord_secret": "",
        "feishu_secret": ""
    },
    "remotes": {},
    "engines": {
        "alist": "",
        "baidupcs": "",
        "quarkcli": "",
        "aria2c": "",
        "rclone": "",
        "alist_url": "",
        "alist_user": "",
        "alist_password_ref": "",
        "rclone_remote": "",
        "webdav_url": "",
        "webdav_user": "",
        "webdav_password_ref": ""
    },
    "drives": {
        "baidu": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": "",
            "save_path": "/网盘下载"
        },
        "aliyun": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "quark": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "tianyi": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "thunder": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "115": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "123pan": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "139yun": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "wopan": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "uc": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "pikpak": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "jianguoyun": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "onedrive": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "googledrive": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "dropbox": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "weiyun": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "lanzou": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "wukong": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "doubao": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "mega": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "terabox": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "pcloud": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "protondrive": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "yandexdisk": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "mediafire": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "trainbit": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "guangyapan": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "feijipan": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "shandian": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "chengtong": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        },
        "direct": {
            "tier": "auto",
            "account_tier": "",
            "tier_detector": "",
            "cookie_file": "",
            "credential_ref": "",
            "engine_command": ""
        }
    },
    "extensions": {}
}
SECRET_RE = re.compile(r"(cookie|token|password|passwd|secret|bduss|credential|authorization|auth|pass)", re.I)
KEYCHAIN_REF_PREFIX = "keychain:"


# ---------------------------------------------------------------- 基础工具
def deep_merge(base, over):
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(path=None):
    path = Path(path or CONFIG_PATH)
    if not path.exists():
        return copy.deepcopy(DEFAULT_CONFIG)
    try:
        user = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return copy.deepcopy(DEFAULT_CONFIG)
    return deep_merge(DEFAULT_CONFIG, user)


def save_config(cfg, path=None):
    path = Path(path or CONFIG_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        os.chmod(path, 0o600)  # 凭据文件只允许本人读写
    except OSError:
        pass
    return path


def mask_value(key, value):
    if isinstance(value, dict):
        return {k: mask_value(k, v) for k, v in value.items()}
    if isinstance(value, list):
        return [mask_value(key, v) for v in value]
    if SECRET_RE.search(str(key)) and value:
        return "***"
    return value


def _valid_secret_name(name):
    name = str(name or "").strip()
    if not re.fullmatch(r"[A-Za-z0-9._@-]{1,80}", name):
        raise ValueError("凭据名只允许字母、数字、点、下划线、@ 和连字符")
    return name


def credential_ref(name):
    return CREDENTIAL_REF_PREFIX + _valid_secret_name(name)


def normalize_secret_ref(value):
    text = str(value or "").strip()
    if is_secret_ref(text):
        return text
    return credential_ref(text)


def keychain_ref(name):
    """兼容旧调用；新配置统一推荐 credential: 引用。"""
    return credential_ref(name)


def is_secret_ref(value):
    return isinstance(value, str) and value.startswith((CREDENTIAL_REF_PREFIX, KEYCHAIN_REF_PREFIX))


def secret_ref_name(ref):
    if not is_secret_ref(ref):
        return ""
    for prefix in (CREDENTIAL_REF_PREFIX, KEYCHAIN_REF_PREFIX):
        if ref.startswith(prefix):
            return ref[len(prefix):].strip()
    return ""


def is_keychain_ref(value):
    return is_secret_ref(value)


def keychain_name(ref):
    return secret_ref_name(ref)


def credential_backend(system=None):
    system = (system or platform.system()).lower()
    if system.startswith("win"):
        return "windows"
    if system == "darwin":
        return "macos"
    if shutil.which("secret-tool"):
        return "secret-tool"
    return "unsupported"


def credential_available(system=None):
    backend = credential_backend(system)
    if backend == "macos":
        return bool(SECURITY_BIN and Path(SECURITY_BIN).exists())
    return backend in ("windows", "secret-tool")


def keychain_available():
    """兼容旧函数名；返回当前平台的系统凭据库是否可用。"""
    return credential_available()


def _secret_name(name):
    return re.sub(r"[^A-Za-z0-9._@-]+", "_", str(name or "").strip())


def _macos_keychain_store(name, value):
    if not (SECURITY_BIN and Path(SECURITY_BIN).exists()):
        raise RuntimeError("macOS security 命令不可用，拒绝保存明文；请在正常终端执行")
    proc = subprocess.run(
        [SECURITY_BIN, "add-generic-password", "-U", "-a", name, "-s", KEYCHAIN_SERVICE, "-w"],
        input=value + "\n" + value + "\n", text=True, capture_output=True,
    )
    if proc.returncode != 0:
        msg = (proc.stderr or proc.stdout or "钥匙串写入失败").strip().splitlines()
        raise RuntimeError(msg[-1] if msg else "钥匙串写入失败")


def _macos_keychain_get(name):
    if not (SECURITY_BIN and Path(SECURITY_BIN).exists()):
        return ""
    proc = subprocess.run(
        [SECURITY_BIN, "find-generic-password", "-a", name, "-s", KEYCHAIN_SERVICE, "-w"],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        return ""
    return proc.stdout.rstrip("\r\n")


def _macos_keychain_delete(name):
    if not (SECURITY_BIN and Path(SECURITY_BIN).exists()):
        return False
    proc = subprocess.run(
        [SECURITY_BIN, "delete-generic-password", "-a", name, "-s", KEYCHAIN_SERVICE],
        capture_output=True, text=True,
    )
    return proc.returncode == 0


def _windows_target(name):
    return "%s:%s" % (APP, name)


def _windows_credential_store(name, value):
    """Windows Credential Manager 写入；密码不经过 argv / stdin。"""
    import ctypes
    from ctypes import wintypes

    class FILETIME(ctypes.Structure):
        _fields_ = [("dwLowDateTime", wintypes.DWORD), ("dwHighDateTime", wintypes.DWORD)]

    class CREDENTIAL_ATTRIBUTE(ctypes.Structure):
        _fields_ = [
            ("Keyword", wintypes.LPWSTR),
            ("Flags", wintypes.DWORD),
            ("ValueSize", wintypes.DWORD),
            ("Value", ctypes.POINTER(ctypes.c_ubyte)),
        ]

    class CREDENTIAL(ctypes.Structure):
        _fields_ = [
            ("Flags", wintypes.DWORD),
            ("Type", wintypes.DWORD),
            ("TargetName", wintypes.LPWSTR),
            ("Comment", wintypes.LPWSTR),
            ("LastWritten", FILETIME),
            ("CredentialBlobSize", wintypes.DWORD),
            ("CredentialBlob", ctypes.POINTER(ctypes.c_ubyte)),
            ("Persist", wintypes.DWORD),
            ("AttributeCount", wintypes.DWORD),
            ("Attributes", ctypes.POINTER(CREDENTIAL_ATTRIBUTE)),
            ("TargetAlias", wintypes.LPWSTR),
            ("UserName", wintypes.LPWSTR),
        ]

    blob = value.encode("utf-16-le")
    buffer = ctypes.create_string_buffer(blob, len(blob))
    cred = CREDENTIAL()
    cred.Type = 1  # CRED_TYPE_GENERIC
    cred.TargetName = _windows_target(name)
    cred.UserName = name
    cred.CredentialBlobSize = len(blob)
    cred.CredentialBlob = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_ubyte))
    cred.Persist = 2  # CRED_PERSIST_LOCAL_MACHINE
    if not ctypes.windll.advapi32.CredWriteW(ctypes.byref(cred), 0):
        raise RuntimeError("Windows 凭据管理器写入失败（错误码 %s）" % ctypes.get_last_error())


def _windows_credential_get(name):
    import ctypes
    from ctypes import wintypes

    class FILETIME(ctypes.Structure):
        _fields_ = [("dwLowDateTime", wintypes.DWORD), ("dwHighDateTime", wintypes.DWORD)]

    class CREDENTIAL_ATTRIBUTE(ctypes.Structure):
        _fields_ = [
            ("Keyword", wintypes.LPWSTR),
            ("Flags", wintypes.DWORD),
            ("ValueSize", wintypes.DWORD),
            ("Value", ctypes.POINTER(ctypes.c_ubyte)),
        ]

    class CREDENTIAL(ctypes.Structure):
        _fields_ = [
            ("Flags", wintypes.DWORD),
            ("Type", wintypes.DWORD),
            ("TargetName", wintypes.LPWSTR),
            ("Comment", wintypes.LPWSTR),
            ("LastWritten", FILETIME),
            ("CredentialBlobSize", wintypes.DWORD),
            ("CredentialBlob", ctypes.POINTER(ctypes.c_ubyte)),
            ("Persist", wintypes.DWORD),
            ("AttributeCount", wintypes.DWORD),
            ("Attributes", ctypes.POINTER(CREDENTIAL_ATTRIBUTE)),
            ("TargetAlias", wintypes.LPWSTR),
            ("UserName", wintypes.LPWSTR),
        ]

    ptr = ctypes.POINTER(CREDENTIAL)()
    if not ctypes.windll.advapi32.CredReadW(_windows_target(name), 1, 0, ctypes.byref(ptr)):
        return ""
    try:
        cred = ptr.contents
        raw = ctypes.string_at(cred.CredentialBlob, cred.CredentialBlobSize)
        return raw.decode("utf-16-le").rstrip("\x00")
    finally:
        ctypes.windll.advapi32.CredFree(ptr)


def _windows_credential_delete(name):
    import ctypes

    return bool(ctypes.windll.advapi32.CredDeleteW(_windows_target(name), 1, 0))


def _secret_tool_store(name, value):
    proc = subprocess.run(
        ["secret-tool", "store", "--label", APP + " " + name, "service", APP, "account", name],
        input=value, text=True, capture_output=True,
    )
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or "secret-tool 写入失败").strip())


def _secret_tool_get(name):
    proc = subprocess.run(
        ["secret-tool", "lookup", "service", APP, "account", name],
        capture_output=True, text=True,
    )
    return proc.stdout.rstrip("\r\n") if proc.returncode == 0 else ""


def _secret_tool_delete(name):
    proc = subprocess.run(
        ["secret-tool", "clear", "service", APP, "account", name],
        capture_output=True, text=True,
    )
    return proc.returncode == 0


def credential_store(name, value):
    """把密码写入当前平台的系统凭据库；不把明文写入 config。"""
    name = _secret_name(name)
    if not name:
        raise ValueError("凭据名为空")
    if not value:
        raise ValueError("凭据为空")
    backend = credential_backend()
    if backend == "macos":
        _macos_keychain_store(name, value)
    elif backend == "windows":
        _windows_credential_store(name, value)
    elif backend == "secret-tool":
        _secret_tool_store(name, value)
    else:
        raise RuntimeError("当前系统没有可用的系统凭据库；拒绝把密码保存为明文")
    return credential_ref(name)


def keychain_store(name, value):
    """兼容旧函数名；实际写入当前平台的系统凭据库。"""
    return credential_store(name, value)


def credential_get(name):
    name = secret_ref_name(name) or _secret_name(name)
    if not name:
        return ""
    backend = credential_backend()
    if backend == "macos":
        return _macos_keychain_get(name)
    if backend == "windows":
        return _windows_credential_get(name)
    if backend == "secret-tool":
        return _secret_tool_get(name)
    return ""


def keychain_get(name):
    """兼容旧函数名。"""
    return credential_get(name)


def credential_delete(name):
    name = secret_ref_name(name) or _secret_name(name)
    if not name:
        return False
    backend = credential_backend()
    if backend == "macos":
        return _macos_keychain_delete(name)
    if backend == "windows":
        return _windows_credential_delete(name)
    if backend == "secret-tool":
        return _secret_tool_delete(name)
    return False


def keychain_delete(name):
    """兼容旧函数名。"""
    return credential_delete(name)


def resolve_secret(value):
    """解析 credential:/keychain: 引用；兼容旧配置里的明文值但不主动展示。"""
    if not value:
        return ""
    if is_secret_ref(value):
        # 通过兼容入口读取，便于旧测试/旧调用方替换 keychain_get。
        return keychain_get(secret_ref_name(value))
    return str(value)


def resolve_engine_secret(cfg, ref_key, legacy_key=""):
    eng = cfg.get("engines") or {}
    return resolve_secret(eng.get(ref_key) or eng.get(legacy_key) or "")


def configured_secret_refs(cfg):
    refs = {}
    eng = cfg.get("engines") or {}
    for key, label in (("alist_password_ref", "engine.alist"), ("webdav_password_ref", "engine.webdav")):
        ref = str(eng.get(key) or "")
        if ref:
            refs[label] = ref
    for drive, entry in (cfg.get("drives") or {}).items():
        ref = str((entry or {}).get("credential_ref") or "")
        if ref:
            refs["drive." + drive] = ref
    for remote, entry in (cfg.get("remotes") or {}).items():
        ref = str((entry or {}).get("credential_ref") or "")
        if ref:
            refs["remote." + remote] = ref
    return refs


def migrate_plaintext_secrets(cfg):
    """迁移已知明文凭据到系统凭据库，返回 (migrated, errors)。"""
    migrated, errors = [], []
    eng = cfg.setdefault("engines", {})
    for plain_key, ref_key, secret_name in (
        ("alist_password", "alist_password_ref", "engine.alist"),
        ("webdav_password", "webdav_password_ref", "engine.webdav"),
    ):
        value = str(eng.get(plain_key) or "")
        if not value:
            continue
        try:
            eng[ref_key] = keychain_store(secret_name, value)
            eng.pop(plain_key, None)
            migrated.append(secret_name)
        except (OSError, ValueError, RuntimeError) as exc:
            errors.append("%s: %s" % (secret_name, exc))
    for drive, entry in (cfg.get("drives") or {}).items():
        if not isinstance(entry, dict) or entry.get("credential_ref"):
            continue
        for plain_key in ("password", "passwd", "token", "cookie", "credential", "bduss"):
            value = str(entry.get(plain_key) or "")
            if not value:
                continue
            secret_name = "drive." + drive
            try:
                entry["credential_ref"] = keychain_store(secret_name, value)
                entry.pop(plain_key, None)
                migrated.append(secret_name)
            except (OSError, ValueError, RuntimeError) as exc:
                errors.append("%s: %s" % (secret_name, exc))
            break
    for remote, entry in (cfg.get("remotes") or {}).items():
        if not isinstance(entry, dict) or entry.get("credential_ref"):
            continue
        for plain_key in ("password", "passwd", "token", "secret", "credential"):
            value = str(entry.get(plain_key) or "")
            if not value:
                continue
            secret_name = "remote." + remote
            try:
                entry["credential_ref"] = keychain_store(secret_name, value)
                entry.pop(plain_key, None)
                migrated.append(secret_name)
            except (OSError, ValueError, RuntimeError) as exc:
                errors.append("%s: %s" % (secret_name, exc))
            break
    return migrated, errors


def all_drives(cfg):
    drives = dict(DRIVES)
    for name, spec in (cfg.get("extensions") or {}).items():
        drives[name] = {
            "name": spec.get("name", name),
            "domains": spec.get("domains", []),
            "engine": spec.get("engine", "custom"),
            "reference": spec.get("reference", "references/06-扩展新网盘.md"),
        }
    return drives


def detect_drive(url, cfg=None):
    """返回 (drive_key, spec)；未知 http(s) 链接回退为 direct。"""
    cfg = cfg or load_config()
    host = (urlparse(url).hostname or "").lower()
    if not host:
        return "direct", all_drives(cfg)["direct"]
    for key, spec in all_drives(cfg).items():
        for domain in spec.get("domains", []):
            d = domain.lower()
            if host == d or host.endswith("." + d):
                return key, spec
    if url.lower().startswith(("http://", "https://")):
        return "direct", all_drives(cfg)["direct"]
    return "", {}


def sanitize(name, fallback="download"):
    name = unquote(name or "").strip()
    name = re.sub(r"[\\/:*?\"<>|\x00-\x1f]", "_", name)
    name = re.sub(r"\s+", " ", name).strip(" .")
    return name[:80] or fallback


def filename_from_url(url):
    path = urlparse(url).path
    base = sanitize(Path(path).name)
    if not base or base in (".", ".."):
        return "download.bin"
    return base


def url_slug(url):
    path = urlparse(url).path.rstrip("/")
    tail = sanitize(Path(path).name, fallback="share")
    return tail or "share"


def default_root(cfg):
    configured = (cfg.get("download_root") or "").strip()
    if configured:
        return Path(os.path.expanduser(configured))
    if platform.system().lower() == "darwin":
        for vol in ("/Volumes/PanDownloads", "/Volumes/PanOffice"):
            p = Path(vol)
            if p.is_dir() and os.access(str(p), os.W_OK):
                return p / "网盘下载"
    return Path(PATHS["download"])


def task_dir(cfg, drive_name, url, to=None):
    if to:
        return Path(os.path.expanduser(to))
    stamp = datetime.now().strftime("%Y%m%d")
    return default_root(cfg) / sanitize(drive_name) / (stamp + "-" + url_slug(url))


CONTENT_CATEGORIES = {
    "影视": (".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".ts"),
    "音乐": (".mp3", ".flac", ".wav", ".aac", ".ogg", ".m4a", ".ape", ".wma"),
    "文档": (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md", ".csv", ".epub"),
    "图片": (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".heic", ".tiff"),
    "压缩包": (".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso"),
}
DEFAULT_CATEGORY = "其他"


def content_category(url):
    """按文件名后缀猜测内容分类（影视/音乐/文档/图片/压缩包/其他）。"""
    name = filename_from_url(url).lower()
    for cat, exts in CONTENT_CATEGORIES.items():
        if name.endswith(exts):
            return cat
    return DEFAULT_CATEGORY


def smart_classify_dir(cfg, drive_name, url):
    """智能默认：把目标目录自动落到 根目录/分类/网盘/日期-文件名。"""
    smart = cfg.get("smart") or {}
    root = str((smart.get("classify_root") or "").strip())
    base = Path(os.path.expanduser(root)) if root else default_root(cfg)
    stamp = datetime.now().strftime("%Y%m%d")
    return base / content_category(url) / sanitize(drive_name or "网盘") / (stamp + "-" + url_slug(url))


def smart_auto_classify_enabled(cfg, classify=None):
    if classify is None:
        return bool((cfg.get("smart") or {}).get("auto_classify"))
    return bool(classify)


def find_engine_binary(engine, cfg):
    configured = ((cfg.get("engines") or {}).get(engine) or "").strip()
    if configured:
        p = Path(os.path.expanduser(configured))
        return str(p) if p.exists() else ""
    for name in ENGINE_BINARIES.get(engine, []):
        found = shutil.which(name)
        if found:
            return found
    return ""


# ---------------------------------------------------------------- 远程设备
REMOTE_KINDS = ("ssh", "rclone", "webdav", "smb", "s3", "mount")


def normalize_remote_kind(value):
    kind = str(value or "").strip().lower()
    aliases = {
        "sftp": "ssh",
        "synology": "ssh",
        "fnos": "ssh",
        "nas": "ssh",
        "ftp": "rclone",
        "nfs": "mount",
        "local-mount": "mount",
    }
    kind = aliases.get(kind, kind)
    return kind if kind in REMOTE_KINDS else ""


def remote_entry(cfg, name):
    name = str(name or "").strip()
    if not name:
        return None
    entry = (cfg.get("remotes") or {}).get(name)
    return entry if isinstance(entry, dict) else None


def validate_remote_profile(name, entry):
    """返回 (normalized_profile, missing)；只校验配置，不触碰网络。"""
    entry = dict(entry or {})
    kind = normalize_remote_kind(entry.get("kind"))
    entry["kind"] = kind
    entry["name"] = str(name or entry.get("name") or "").strip()
    missing = []
    if not entry["name"]:
        missing.append("remote 名称")
    if not kind:
        missing.append("kind（ssh/rclone/webdav/smb/s3/mount）")
    if kind == "ssh":
        for key, label in (("host", "host"), ("user", "user"), ("root", "root")):
            if not str(entry.get(key) or "").strip():
                missing.append(label)
    elif kind == "mount":
        if not str(entry.get("root") or "").strip():
            missing.append("root（本机挂载路径，Windows 示例 Z:\\下载）")
    elif kind in ("rclone", "webdav", "smb", "s3"):
        for key, label in (("remote_name", "remote_name（rclone 配置名）"), ("root", "root")):
            if not str(entry.get(key) or "").strip():
                missing.append(label)
    return entry, missing


def remote_ssh_argv(profile, command):
    host = str(profile["host"]).strip()
    user = str(profile["user"]).strip()
    destination = "%s@%s" % (user, host)
    argv = ["ssh", "-o", "BatchMode=yes"]
    port = str(profile.get("port") or "").strip()
    if port:
        argv += ["-p", port]
    argv += [destination, command]
    return argv


def remote_scp_argv(profile, source, destination):
    host = str(profile["host"]).strip()
    user = str(profile["user"]).strip()
    argv = ["scp", "-q", "-o", "BatchMode=yes"]
    port = str(profile.get("port") or "").strip()
    if port:
        argv += ["-P", port]
    argv += [str(source), "%s@%s:%s" % (user, host, destination)]
    return argv


def remote_display(profile):
    if profile.get("kind") == "ssh":
        return "ssh://%s@%s:%s%s" % (
            profile.get("user", ""), profile.get("host", ""), profile.get("port", "22"), profile.get("root", "")
        )
    if profile.get("kind") == "mount":
        return str(profile.get("root") or "")
    return "%s:%s" % (str(profile.get("remote_name") or "").rstrip(":"), profile.get("root", ""))


def remote_rclone_destination(profile, task_name):
    remote = str(profile.get("remote_name") or "").strip()
    if not remote:
        return ""
    remote = remote.rstrip(":") + ":"
    root = str(profile.get("root") or "").strip().replace("\\", "/").strip("/")
    path = "/".join([p for p in (root, sanitize(task_name)) if p])
    return remote + "/" + path if path else remote


def remote_task_name(drive_name, url):
    return "%s-%s" % (datetime.now().strftime("%Y%m%d"), url_slug(url))


def build_ssh_remote_plan(profile, url, pwd="", to=None, path=None, tier=None, engine=None, live=False):
    """远程执行模式：在 SSH 设备上调用已部署的 pan.py，文件直接落到远程磁盘。"""
    plan = {
        "ok": True,
        "drive": "remote-ssh",
        "drive_name": profile.get("name") or "远程设备",
        "engine": "ssh",
        "tier": tier or "",
        "target": remote_display(profile),
        "steps": [],
        "missing": [],
        "warnings": [],
        "reference": str(SKILL_DIR / "references/21-远程NAS与私有存储.md"),
        "remote_kind": "ssh-execute",
        "remote_name": profile.get("name", ""),
    }
    deploy_dir = str(profile.get("deploy_dir") or ".pan-downloader").strip().strip("/")
    python_bin = str(profile.get("python") or "python3").strip()
    remote_root = str(profile.get("root") or "").strip()
    task_name = remote_task_name(profile.get("name") or "remote", url)
    remote_target = str(to or ("%s/网盘下载/%s" % (remote_root.rstrip("/"), task_name)))
    script = "%s/scripts/pan.py" % deploy_dir
    cmd = "cd %s && %s %s get %s --to %s" % (
        shlex.quote(remote_root), shlex.quote(python_bin), shlex.quote(script),
        shlex.quote(url), shlex.quote(remote_target),
    )
    if live:
        cmd += " --live"
    if pwd:
        cmd += " --pwd " + shlex.quote(pwd)
    if path:
        cmd += " --path " + shlex.quote(path)
    if tier:
        cmd += " --tier " + shlex.quote(tier)
    if engine:
        cmd += " --engine " + shlex.quote(engine)
    cmd += " --force"
    plan["steps"].append({
        "engine": "ssh",
        "argv": remote_ssh_argv(profile, cmd),
        "cwd": str(SKILL_DIR),
        "note": "在远程设备执行 pan.py，下载直接落到 %s（需要预先把 SSH 密钥/agent 配置好）" % remote_target,
    })
    plan["target"] = remote_target
    return plan


def build_remote_sink_plan(profile, url, pwd="", to=None, path=None, tier=None, engine=None, cfg=None):
    """远程落地模式：本机取文件，再通过 rclone 写入 NAS/私有存储。"""
    cfg = cfg or load_config()
    profile = dict(profile)
    name = profile.get("name") or "remote"
    remote_task = remote_task_name(name, url)
    if profile.get("kind") == "mount":
        mount_root = Path(os.path.expanduser(str(profile.get("root") or "")))
        target = Path(to) if to else mount_root / "网盘下载" / remote_task
        local_plan = build_plan(url, pwd=pwd, to=str(target), cfg=cfg, engine=engine, tier=tier, path=path)
        local_plan["remote_kind"] = "mounted-target"
        local_plan["remote_name"] = name
        local_plan["reference"] = str(SKILL_DIR / "references/21-远程NAS与私有存储.md")
        return local_plan

    staging_root = str((cfg.get("remote") or {}).get("staging_root") or "").strip()
    staging = Path(os.path.expanduser(staging_root)) if staging_root else STATE_DIR / "remote-staging" / sanitize(name)
    staging_task = staging / remote_task
    local_plan = build_plan(url, pwd=pwd, to=str(staging_task), cfg=cfg, engine=engine, tier=tier, path=path)
    local_plan["remote_kind"] = "rclone-upload"
    local_plan["remote_name"] = name
    local_plan["staging"] = str(staging_task)
    local_plan["reference"] = str(SKILL_DIR / "references/21-远程NAS与私有存储.md")
    destination = remote_rclone_destination(profile, remote_task)
    if destination:
        local_plan["target"] = destination
    binary = find_engine_binary("rclone", cfg)
    if not binary:
        local_plan["missing"].append("rclone")
    if not destination:
        local_plan["missing"].append("remote_name")
    if binary and destination:
        try:
            conn = int((cfg.get("http") or {}).get(
                "max_connections_vip" if local_plan.get("tier") == "vip" else "max_connections_free", 1
            ))
        except (TypeError, ValueError):
            conn = 1
        conn = max(1, conn)
        argv = [
            binary, "copy", "--progress", "--transfers", str(conn),
            "--checkers", str(max(1, min(conn * 2, 8))),
            str(staging_task), destination,
        ]
        local_plan["steps"].append({
            "engine": "rclone",
            "argv": argv,
            "note": "把 %s 上传到远程存储 %s（tier=%s）" % (staging_task, destination, local_plan.get("tier", "free")),
        })
    return local_plan


def build_remote_plan(profile, url, pwd="", to=None, path=None, tier=None, engine=None, cfg=None):
    cfg = cfg or load_config()
    profile, missing = validate_remote_profile(profile.get("name", ""), profile)
    if missing:
        return {
            "ok": False,
            "error": "远程配置缺少：" + "、".join(missing),
            "missing": missing,
        }
    if profile["kind"] == "ssh":
        return build_ssh_remote_plan(profile, url, pwd=pwd, to=to, path=path, tier=tier, engine=engine, live=bool(profile.get("live", False)))
    return build_remote_sink_plan(profile, url, pwd=pwd, to=to, path=path, tier=tier, engine=engine, cfg=cfg)


def create_remote_deploy_archive():
    """打包技能文本与脚本，不含 config.json、凭据、缓存和用户数据。"""
    fd, tmp_name = tempfile.mkstemp(prefix="pan-downloader-deploy-", suffix=".tar.gz")
    os.close(fd)
    archive = Path(tmp_name)
    include = [SKILL_DIR / "SKILL.md", SKILL_DIR / "config.example.json", SKILL_DIR / "agents", SKILL_DIR / "references", SKILL_DIR / "scripts"]
    with tarfile.open(archive, "w:gz") as tar:
        for source in include:
            if source.is_file():
                tar.add(source, arcname=source.name)
            elif source.is_dir():
                for item in sorted(source.rglob("*")):
                    if item.is_file() and "__pycache__" not in item.parts and item.name not in ("config.json",):
                        tar.add(item, arcname=str(item.relative_to(SKILL_DIR)))
    return archive


def remote_web_access(profile, port=0, web_host="", local_port=0):
    """构造远程 Web 控制页访问信息；不出网，只返回 URL 与隧道命令。"""
    port = int(port or 0) or int(profile.get("web_port") or 0) or 17890
    local_port = int(local_port or 0) or port
    web_host = (web_host or profile.get("web_host") or "127.0.0.1").strip() or "127.0.0.1"
    host = str(profile.get("host") or "NAS").strip()
    user = str(profile.get("user") or "").strip()
    if web_host in ("0.0.0.0", "::"):
        url = "http://%s:%d/" % (host, port)
    else:
        url = "http://127.0.0.1:%d/" % port
    tunnel = ""
    if user:
        ssh_port = (" -p %s" % profile.get("port")) if str(profile.get("port") or "").strip() else ""
        tunnel = "ssh%s -L %d:127.0.0.1:%d %s@%s" % (ssh_port, local_port, port, user, host)
    return {
        "web_port": port,
        "web_host": web_host,
        "url": url,
        "tunnel": tunnel,
        "local_url": ("http://127.0.0.1:%d/" % local_port) if tunnel else "",
        "guide": (
            "局域网直接打开：%s；外网/本机仅监听 127.0.0.1 时，另开终端执行：%s 后打开 http://127.0.0.1:%d/，保持隧道终端运行。" % (url, tunnel, local_port)
            if tunnel else ("远程 Web 已启动（127.0.0.1:%d）。如需局域网访问，重新部署时用 --web-host 0.0.0.0，或在本机保持 SSH 反向隧道。" % port)
        )
    }


def build_remote_deploy_plan(profile, archive_path, web_port=0, web_host=None, web_reports_dir=""):
    """把无凭据技能包部署到 SSH 设备；可选 --web-port 后台启动常驻 Web 控制页。"""
    profile, missing = validate_remote_profile(profile.get("name", ""), profile)
    if missing:
        return {"ok": False, "error": "远程配置缺少：" + "、".join(missing), "steps": []}
    if profile.get("kind") != "ssh":
        return {"ok": False, "error": "remote deploy 只支持 kind=ssh；WebDAV/SMB/S3 请直接用 rclone", "steps": []}
    deploy_dir = str(profile.get("deploy_dir") or ".pan-downloader").strip().strip("/")
    remote_dir = str(profile.get("root") or "").rstrip("/") + "/" + deploy_dir
    remote_root = str(profile.get("root") or "").rstrip("/") or ""
    remote_archive = "/tmp/pan-downloader-deploy-%s.tar.gz" % os.getpid()
    mkdir_cmd = "mkdir -p %s" % shlex.quote(remote_dir)
    extract_cmd = "tar -xzf %s -C %s && rm -f %s" % (
        shlex.quote(remote_archive), shlex.quote(remote_dir), shlex.quote(remote_archive)
    )
    steps = [
        {"engine": "ssh", "argv": remote_ssh_argv(profile, mkdir_cmd), "cwd": str(SKILL_DIR), "note": "创建远程技能目录 %s" % remote_dir},
        {"engine": "scp", "argv": remote_scp_argv(profile, archive_path, remote_archive), "cwd": str(SKILL_DIR), "note": "上传无凭据的部署包"},
        {"engine": "ssh", "argv": remote_ssh_argv(profile, extract_cmd), "cwd": str(SKILL_DIR), "note": "在远程设备解压技能脚本"},
    ]
    try:
        web_port = int(web_port or profile.get("web_port") or 0)
    except (TypeError, ValueError):
        web_port = 0
    web_host = (web_host or profile.get("web_host") or "127.0.0.1").strip() or "127.0.0.1"
    web_info = remote_web_access(profile, port=web_port or 0, web_host=web_host)
    if web_port > 0:
        reports_dir = str(web_reports_dir or remote_root or ".").strip() or "."
        python_bin = str(profile.get("python") or "python3").strip() or "python3"
        name_slug = re.sub(r"[^A-Za-z0-9_.@-]", "_", str(profile.get("name") or "remote"))
        start_cmd = (
            "cd %s && nohup %s scripts/pan.py serve --host %s --port %d --reports-dir %s "
            "</dev/null >/tmp/pan-remote-web-%s.log 2>&1 & echo started"
        ) % (
            shlex.quote(remote_dir), shlex.quote(python_bin), shlex.quote(web_host),
            web_port, shlex.quote(reports_dir), name_slug,
        )
        steps.append({
            "engine": "ssh",
            "argv": remote_ssh_argv(profile, start_cmd),
            "cwd": str(SKILL_DIR),
            "note": "在远程设备后台启动常驻 Web 控制页（scripts/pan.py serve），报告目录=%s，日志 /tmp/pan-remote-web-%s.log" % (reports_dir, name_slug),
        })
    return {
        "ok": True,
        "drive": "remote-deploy",
        "drive_name": profile.get("name", ""),
        "engine": "ssh",
        "tier": "free",
        "target": remote_dir,
        "steps": steps,
        "missing": [],
        "warnings": (["远程设备首次使用仍需在设备本机配置网盘凭据；本工具不会上传本机 config 或密码。"] +
                     (["远程 Web 页面已随部署启动：%s" % web_info["url"]] if web_port > 0 else [])),
        "reference": str(SKILL_DIR / "references/21-远程NAS与私有存储.md"),
        "web_port": web_port,
        "web_host": web_host,
        "web_url": web_info["url"] if web_port > 0 else "",
        "web_guide": web_info["guide"] if web_port > 0 else "",
    }


def log_line(text, path=None):
    path = Path(path or LOG_PATH)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as fh:
            fh.write("[%s] %s\n" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), text))
    except OSError:
        pass


def _redact_argument(item):
    text = str(item)
    text = re.sub(
        r"(?i)(--(?:password|passwd|pwd|cookie|token|secret|credential|bduss|authorization|webdav-pass|alist-password)(?:\s+|=))(\S+)",
        r"\1***", text,
    )
    if re.match(r"(?i)^(--?(?:password|passwd|cookie|token|secret|credential|bduss|authorization)=)", text):
        return "***"
    if re.match(r"(?i)^(--?(?:password|passwd|pwd|cookie|token|secret|credential|bduss|authorization))$", text):
        return text
    if re.match(r"(?i)^(authorization|cookie):", text):
        return "***"
    if re.match(r"(?i)^-bduss=", text):
        return "***"
    return text


def mask_argv(argv):
    """隐藏命令行凭据；真正推荐路径是把密码放系统凭据库并从 stdin 传给引擎。"""
    out = []
    skip_next = False
    secret_flags = {
        "--password", "--passwd", "--pwd", "-p", "--cookie", "--token", "--secret",
        "--credential", "--bduss", "--user", "-u", "--webdav-pass", "--alist-password",
        "--webdav-password", "--alist-pass",
    }
    for i, item in enumerate(argv):
        if skip_next:
            out.append("***")
            skip_next = False
            continue
        current = _redact_argument(item)
        out.append(current)
        if item in secret_flags and i + 1 < len(argv):
            skip_next = True
    return out


def public_plan(plan):
    """给 agent/JSON 输出用的无凭据计划。"""
    steps = []
    for step in plan.get("steps", []):
        steps.append({
            "engine": step.get("engine", ""),
            "note": step.get("note", ""),
            "argv": mask_argv(step.get("argv") or []),
            "uses_stdin_credential": bool(step.get("stdin")),
        })
    return {
        "ok": plan.get("ok", False),
        "drive": plan.get("drive", ""),
        "drive_name": plan.get("drive_name", ""),
        "engine": plan.get("engine", ""),
        "tier": plan.get("tier", ""),
        "tier_source": plan.get("tier_source", ""),
        "target": plan.get("target", ""),
        "remote_kind": plan.get("remote_kind", ""),
        "remote_name": plan.get("remote_name", ""),
        "staging": plan.get("staging", ""),
        "steps": steps,
        "missing": plan.get("missing", []),
        "warnings": plan.get("warnings", []),
        "reference": plan.get("reference", ""),
        "web_port": plan.get("web_port", 0),
        "web_host": plan.get("web_host", ""),
        "web_url": plan.get("web_url", ""),
        "web_guide": plan.get("web_guide", ""),
    }


def curl_basic_auth_step(argv, user, password):
    """用 curl --config - 从 stdin 读取 Basic Auth，避免密码出现在 argv/日志。"""
    step = {"engine": "curl", "argv": list(argv), "note": "curl 下载（凭据通过 stdin，不写入命令行）"}
    if user and password:
        escaped_user = str(user).replace("\\", "\\\\").replace('"', '\\"')
        escaped_pass = str(password).replace("\\", "\\\\").replace('"', '\\"')
        step["stdin"] = 'user = "%s:%s"\n' % (escaped_user, escaped_pass)
        step["argv"].insert(-1, "--config")
        step["argv"].insert(-1, "-")
    return step


# ---------------------------------------------------------------- 账号等级探测
def detect_account_tier(drive_key, drive_cfg, cfg):
    """尽力探测账号等级；无法可靠判断时返回空值，绝不把普通账号当会员。"""
    recorded = str(drive_cfg.get("account_tier") or "").strip().lower()
    if recorded in ("free", "vip"):
        return recorded, "配置记录"

    detector = str(drive_cfg.get("tier_detector") or "").strip()
    if not detector:
        return "", "未配置检测器"

    env = os.environ.copy()
    env["PAN_DRIVE"] = drive_key
    env["PAN_COOKIE_FILE"] = str(drive_cfg.get("cookie_file") or "")
    try:
        cmd = shlex.split(detector.format(drive=drive_key))
        if not cmd:
            return "", "检测器为空"
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10, env=env)
    except subprocess.TimeoutExpired:
        return "", "检测器超时"
    except (OSError, ValueError):
        return "", "检测器不可执行"

    text = ((proc.stdout or "") + "\n" + (proc.stderr or "")).lower()
    if re.search(r"(vip|会员|supervip|svip|premium|pro\b)", text):
        return "vip", "tier_detector（%s）" % detector
    if re.search(r"(free|免费|普通)", text):
        return "free", "tier_detector（%s）" % detector
    return "", "检测器未返回明确等级"


# ---------------------------------------------------------------- 计划构建
def http_step(url, target, cfg, tier):
    filename = filename_from_url(url)
    http = cfg.get("http", {})
    argv = [
        "curl", "-L", "--fail", "--retry", str(http.get("retries", 3)),
        "--retry-delay", str(http.get("retry_delay", 5)),
        "--connect-timeout", str(http.get("connect_timeout", 30)),
        "-C", "-", "-o", str(Path(target) / filename), url,
    ]
    return {"engine": "http", "argv": argv, "note": "curl 断点续传下载（免费/会员参数一致）"}


def build_plan(url, pwd="", to=None, cfg=None, engine=None, tier=None, path=None, classify=None):
    cfg = cfg or load_config()
    key, spec = detect_drive(url, cfg)
    if not key:
        return {"ok": False, "error": "无法识别的链接（既不是已知网盘域名，也不是 http(s) 直链）"}
    drive_cfg = (cfg.get("drives") or {}).get(key, {})
    requested_tier = str(tier or drive_cfg.get("tier") or cfg.get("tier") or "auto").strip().lower()
    if to:
        target = task_dir(cfg, spec["name"], url, to)
    elif smart_auto_classify_enabled(cfg, classify):
        target = smart_classify_dir(cfg, spec["name"], url)
    else:
        target = task_dir(cfg, spec["name"], url, to)
    category = content_category(url) if (not to and smart_auto_classify_enabled(cfg, classify)) else ""
    engine = engine or (cfg.get("extensions", {}).get(key, {}) or {}).get("engine") or spec.get("engine", "http")
    plan = {
        "ok": True,
        "drive": key,
        "drive_name": spec["name"],
        "engine": engine,
        "tier": "",
        "requested_tier": requested_tier,
        "tier_source": "",
        "category": category,
        "target": str(target),
        "reference": str(SKILL_DIR / spec.get("reference", "")),
        "steps": [],
        "missing": [],
        "warnings": [],
    }
    # 常见分享盘常带提取码：未提供 --pwd 时提前用人话提示，避免下载失败后无头绪
    if not pwd and key in ("baidu", "quark", "lanzou", "123pan", "weiyun"):
        plan["warnings"].append(
            "%s 分享链接常见带提取码，未提供 --pwd；若下载失败，请先从分享来源拿到提取码重试。" % spec["name"]
        )

    if requested_tier not in VALID_TIERS:
        plan["warnings"].append("tier=%s 不合法，已按 free 处理" % requested_tier)
        requested_tier = "free"

    if requested_tier == "auto":
        detected, source = detect_account_tier(key, drive_cfg, cfg)
        if detected:
            tier = detected
            plan["tier_source"] = source
            plan["warnings"].append("账号等级自动识别为 %s（%s）" % (detected, source))
        else:
            tier = "free"
            plan["tier_source"] = source
            plan["warnings"].append(
                "账号等级未自动识别（%s），先按免费账号处理；登录后可用"
                " set-drive %s --account-tier free|vip 记录，或本次加 --tier vip 强制" % (source, key)
            )
    else:
        tier = requested_tier

    plan["tier"] = tier

    if category:
        plan["warnings"].append("智能分类已启用：自动保存到「%s」目录" % category)

    custom_cmd = (drive_cfg.get("engine_command") or "").strip()

    if custom_cmd:
        argv = shlex.split(
            custom_cmd.format(url=url, pwd=pwd or "", dir=str(target), name=sanitize(spec["name"]), tier=tier)
        )
        plan["steps"].append({"engine": "custom", "argv": argv, "note": "自定义引擎命令"})
        return plan

    if engine == "http":
        plan["steps"].append(http_step(url, target, cfg, tier))

    elif engine == "aria2":
        binary = find_engine_binary("aria2", cfg)
        if not binary:
            plan["missing"].append("aria2c")
        conn = cfg.get("http", {}).get("max_connections_vip" if tier == "vip" else "max_connections_free", 1)
        filename = filename_from_url(url)
        argv = [binary or "aria2c", "-c", "--retry-wait=5", "-m", str(cfg.get("http", {}).get("retries", 3)),
                "-x", str(conn), "-s", str(conn), "-d", str(target), "-o", filename, url]
        plan["steps"].append({"engine": "aria2", "argv": argv, "note": "aria2 多线程下载（tier=%s，并发 %s）" % (tier, conn)})

    elif engine == "alist":
        server = ((cfg.get("engines") or {}).get("alist_url") or "").strip()
        dav_user = ((cfg.get("engines") or {}).get("alist_user") or "").strip()
        dav_ref = ((cfg.get("engines") or {}).get("alist_password_ref") or "").strip()
        dav_pass = resolve_engine_secret(cfg, "alist_password_ref", "alist_password")
        if dav_ref and not dav_pass:
            plan["warnings"].append("AList 凭据引用无法从系统凭据库读取；请在本机终端运行 secret set engine.alist")
        if not path:
            plan["missing"].append("AList 路径：分享链接需先在 AList 中挂载/转存，再用 --path /挂载名/子目录 指定")
            plan["steps"].append({"engine": "alist", "argv": [], "note": "建议流程：1) AList 添加对应网盘存储 2) 浏览器打开分享链接转存到自己账号 3) 用 --path 指向 AList 中的目录"})
        elif not server:
            plan["missing"].append("alist_url（在 config.json 的 engines.alist_url 填写 AList 地址）")
        else:
            remote = path if path.startswith("/") else "/" + path
            filename = sanitize(Path(remote).name, fallback="download")
            rclone_bin = find_engine_binary("rclone", cfg)
            rclone_remote = ((cfg.get("engines") or {}).get("rclone_remote") or "").strip()
            if rclone_bin and rclone_remote:
                # rclone 远端名必须带冒号；允许用户只填 alist，脚本自动补成 alist:。
                if ":" not in rclone_remote:
                    rclone_remote += ":"
                remote_path = rclone_remote.rstrip("/") + remote
                try:
                    conn = int(cfg.get("http", {}).get("max_connections_vip" if tier == "vip" else "max_connections_free", 1))
                except (TypeError, ValueError):
                    conn = 1
                conn = max(1, conn)
                checkers = max(1, min(conn * 2, 8))
                argv = [
                    rclone_bin, "copy", "--progress",
                    "--transfers", str(conn), "--checkers", str(checkers),
                    remote_path, str(target),
                ]
                plan["steps"].append({"engine": "rclone", "argv": argv,
                                      "note": "通过 rclone/AList WebDAV 递归下载（tier=%s，并发 %s，远端 %s）" % (tier, conn, remote_path)})
            else:
                if rclone_bin and not rclone_remote:
                    plan["warnings"].append("已安装 rclone 但未配置 engines.rclone_remote，回退为 curl 单文件下载")
                elif not rclone_bin:
                    plan["warnings"].append("未安装 rclone；curl 回退只适合单文件，目录请在 Finder 挂载 AList WebDAV 或安装 rclone")
                argv = ["curl", "-L", "--fail", "-C", "-", "-o", str(target / filename), server.rstrip("/") + "/dav" + remote]
                step = curl_basic_auth_step(argv, dav_user, dav_pass)
                step["engine"] = "alist"
                step["note"] = "通过 AList WebDAV 下载单文件（挂载路径 %s；凭据走 stdin）" % remote
                plan["steps"].append(step)

    elif engine == "webdav":
        eng = cfg.get("engines") or {}
        server = (eng.get("webdav_url") or "").strip().rstrip("/")
        dav_user = (eng.get("webdav_user") or "").strip()
        dav_ref = (eng.get("webdav_password_ref") or "").strip()
        dav_pass = resolve_engine_secret(cfg, "webdav_password_ref", "webdav_password")
        if dav_ref and not dav_pass:
            plan["warnings"].append("WebDAV 凭据引用无法从系统凭据库读取；请在本机终端运行 secret set engine.webdav")
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower()
        download_url = ""
        if host == "dav.jianguoyun.com" and parsed.path.startswith("/dav"):
            download_url = url
        elif path and server:
            download_url = server + "/" + path.lstrip("/")
        if not download_url:
            plan["missing"].append("webdav_url + --path，或直接使用 dav.jianguoyun.com 的 WebDAV 文件地址")
        else:
            filename = sanitize(Path(urlparse(download_url).path).name or filename_from_url(url), fallback="download")
            argv = ["curl", "-L", "--fail", "-C", "-", "-o", str(target / filename), download_url]
            step = curl_basic_auth_step(argv, dav_user, dav_pass)
            step["engine"] = "webdav"
            step["note"] = "通过 WebDAV 断点续传下载（坚果云/通用 WebDAV；凭据走 stdin）"
            plan["steps"].append(step)

    elif engine == "baidupcs":
        binary = find_engine_binary("baidupcs", cfg)
        if not binary:
            plan["missing"].append("BaiduPCS-Go")
        save_path = ((cfg.get("drives") or {}).get("baidu", {}).get("save_path") or "/网盘下载").strip()
        binary = binary or "BaiduPCS-Go"
        plan["steps"].append({"engine": "baidupcs", "argv": [binary, "transfer", url, pwd or "", save_path],
                              "note": "转存到自己网盘（需已用 BaiduPCS-Go login 登录）"})
        plan["steps"].append({"engine": "baidupcs", "argv": [binary, "download", save_path, "--saveto", str(target)],
                              "note": "从自己网盘批量下载到本地（断点续传）"})

    elif engine == "quarkcli":
        binary = find_engine_binary("quarkcli", cfg)
        if not binary:
            plan["missing"].append("quark-cli（夸克命令行工具）")
        argv = [binary or "quark", "download", url]
        if pwd:
            argv += ["--pwd", pwd]
        argv += ["--dir", str(target)]
        plan["steps"].append({"engine": "quarkcli", "argv": argv, "note": "夸克分享链接转存并下载（Cookie 登录）"})

    else:
        plan["missing"].append("引擎 %s 未配置 engine_command" % engine)
        plan["steps"].append({"engine": engine, "argv": [], "note": "在 config.json 的 drives.%s.engine_command 配置命令模板" % key})

    return plan


def run_plan(plan, timeout=0, dry_run=True):
    if not plan.get("ok"):
        return 1
    for step in plan["steps"]:
        argv = step.get("argv") or []
        if not argv:
            continue
        if dry_run:
            print("DRY-RUN:", " ".join(shlex.quote(x) for x in mask_argv(argv)))
            continue
        print("RUN:", " ".join(shlex.quote(x) for x in mask_argv(argv)))
        log_line("RUN: " + " ".join(mask_argv(argv)))
        started = time.time()
        try:
            cwd = str(step.get("cwd") or plan.get("run_cwd") or plan.get("target") or "")
            kwargs = {"timeout": timeout or None}
            if cwd and Path(cwd).exists():
                kwargs["cwd"] = cwd
            if step.get("stdin"):
                kwargs["input"] = step["stdin"]
                kwargs["text"] = True
            proc = subprocess.run(argv, **kwargs)
            rc = proc.returncode
        except subprocess.TimeoutExpired:
            print("❌ 超时：%s" % step.get("note", argv[0]))
            log_line("TIMEOUT: " + " ".join(mask_argv(argv)))
            return 124
        except OSError as exc:
            print("❌ 执行失败：%s（%s）" % (argv[0], exc))
            log_line("ERROR: %s %s" % (argv[0], exc))
            return 127
        log_line("EXIT %s (%.1fs): %s" % (rc, time.time() - started, " ".join(mask_argv(argv))))
        if rc != 0:
            print("❌ 步骤失败（exit=%s）：%s" % (rc, step.get("note", "")))
            return rc
    return 0

def humanize_step_error(step, rc):
    """把常见退出码/引擎错误翻译成中文动作提示；无法可靠判断时返回空串。"""
    engine = (step or {}).get("engine", "")
    if rc == 124:
        return "超时：网络慢或文件大。重跑任务会从断点续传（curl -C - / 引擎自带续传）。"
    if rc in (126, 127):
        name = ((step or {}).get("argv") or ["命令"])[0]
        return "找不到或无法执行 %s：请先运行 `pan doctor` 检查并安装依赖。" % (name or "命令",)
    if rc == 7:
        return "连接失败：检查网络是否可用、分享链接是否还在有效期内，必要时重新登录该网盘。"
    if rc == 22:
        return "服务器返回非 2xx（可能是 401/403）：授权过期、提取码错误或无权限，请重新登录该网盘。"
    if engine == "webdav":
        return "WebDAV 授权可能已过期：请用 `pan secret set engine.webdav --stdin` 更新密码后重试。"
    if engine == "baidupcs":
        return "百度网盘未登录或分享链接失效：请先 `pan login baidu`，分享链接需先转存到自己网盘。"
    if engine == "quarkcli":
        return "夸克登录 Cookie 可能已失效：请先 `pan login quark` 后重试。"
    return ""


def run_plan_detailed(plan, timeout=0, dry_run=True, emit_events=False, live=None, task_control=None):
    """执行计划并返回 (rc, 逐步骤结果列表)；用于本机 get 的统计、报告与 JSON 事件流。"""
    if task_control is not None:
        task_control.set_step("")
    results = []
    if not plan.get("ok"):
        return 1, results
    for idx, step in enumerate(plan.get("steps", []), start=1):
        argv = step.get("argv") or []
        entry = {
            "index": idx,
            "engine": step.get("engine", ""),
            "note": step.get("note", ""),
            "argv": mask_argv(argv),
            "uses_stdin_credential": bool(step.get("stdin")),
            "started": datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
            "rc": -1,
            "elapsed": 0.0,
            "error": "",
        }
        results.append(entry)
        if live is not None:
            live.set_step(entry["note"])
        if emit_events:
            print(json.dumps({"event": "step_start", "index": idx, "engine": entry["engine"], "note": entry["note"]}, ensure_ascii=False))
        if not argv:
            entry["error"] = "空步骤（仅配置说明）"
            results[-1] = entry
            if emit_events:
                print(json.dumps({"event": "step_skip", "index": idx}, ensure_ascii=False))
            continue
        if dry_run:
            print("DRY-RUN:", " ".join(shlex.quote(x) for x in mask_argv(argv)))
            entry["rc"] = 0
            entry["dry_run"] = True
            results[-1] = entry
            continue
        print("RUN:", " ".join(shlex.quote(x) for x in mask_argv(argv)))
        log_line("RUN: " + " ".join(mask_argv(argv)))
        started = time.time()
        try:
            cwd = str(step.get("cwd") or plan.get("run_cwd") or plan.get("target") or "")
            kwargs = {"timeout": timeout or None}
            if cwd and Path(cwd).exists():
                kwargs["cwd"] = cwd
            if step.get("stdin"):
                kwargs["input"] = step["stdin"]
                kwargs["text"] = True
            if task_control is not None:
                task_control.set_step(entry["note"])
                rc, _status, _exc = _run_step_controlled(argv, kwargs, task_control, timeout=timeout or 0)
                if _exc:
                    raise _exc
                if _status == "cancelled":
                    print("🛑 任务已取消：%s" % step.get("note", ""))
                    entry["rc"] = 130
                    entry["error"] = "任务已取消"
                    results[-1] = entry
                    if emit_events:
                        print(json.dumps({"event": "step_done", "index": idx, "rc": 130, "error": "任务已取消"}, ensure_ascii=False))
                    return 130, results
                if _status == "timeout":
                    raise subprocess.TimeoutExpired(argv[0], timeout)
            else:
                proc = subprocess.run(argv, **kwargs)
                rc = proc.returncode
        except subprocess.TimeoutExpired:
            print("❌ 超时：%s" % step.get("note", argv[0]))
            log_line("TIMEOUT: " + " ".join(mask_argv(argv)))
            entry["rc"] = 124
            entry["error"] = "超时"
            hint_tmp = humanize_step_error(step, 124)
            if hint_tmp:
                entry["hint"] = hint_tmp
                print("  💡 " + hint_tmp)
            results[-1] = entry
            if emit_events:
                print(json.dumps({"event": "step_done", "index": idx, "rc": 124, "error": "超时", "hint": entry.get("hint", "")}, ensure_ascii=False))
            return 124, results
        except OSError as exc:
            print("❌ 执行失败：%s（%s）" % (argv[0], exc))
            log_line("ERROR: %s %s" % (argv[0], exc))
            entry["rc"] = 127
            entry["error"] = str(exc)
            hint_tmp = humanize_step_error(step, 127)
            if hint_tmp:
                entry["hint"] = hint_tmp
                print("  💡 " + hint_tmp)
            results[-1] = entry
            if emit_events:
                print(json.dumps({"event": "step_done", "index": idx, "rc": 127, "error": str(exc), "hint": entry.get("hint", "")}, ensure_ascii=False))
            return 127, results
        entry["rc"] = rc
        entry["elapsed"] = round(time.time() - started, 2)
        results[-1] = entry
        log_line("EXIT %s (%.1fs): %s" % (rc, entry["elapsed"], " ".join(mask_argv(argv))))
        if emit_events:
            print(json.dumps({
                "event": "step_done",
                "index": idx,
                "engine": entry["engine"],
                "rc": rc,
                "elapsed": entry["elapsed"],
            }, ensure_ascii=False))
        if rc != 0:
            print("❌ 步骤失败（exit=%s）：%s" % (rc, step.get("note", "")))
            hint_tmp = humanize_step_error(step, rc)
            if hint_tmp:
                entry["hint"] = hint_tmp
                print("  💡 " + hint_tmp)
            entry["error"] = "步骤失败 exit=%s" % rc
            results[-1] = entry
            if emit_events:
                print(json.dumps({"event": "step_done", "index": idx, "engine": entry["engine"], "rc": rc, "error": entry["error"], "hint": entry.get("hint", "")}, ensure_ascii=False))
            return rc, results
    return 0, results


def report_path_for_target(cfg, target):
    report_dir = ((cfg.get("http") or {}).get("report_dir") or "").strip()
    base = Path(report_dir).expanduser() if report_dir else Path(target or ".")
    return base / "下载报告.json"


def write_download_report(cfg, plan, results, started, finished, ok, url=""):
    path = report_path_for_target(cfg, plan.get("target", ""))
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        body = {
            "schema": 1,
            "ok": bool(ok),
            "url": url,
            "drive": plan.get("drive", ""),
            "drive_name": plan.get("drive_name", ""),
            "engine": plan.get("engine", ""),
            "tier": plan.get("tier", ""),
            "target": plan.get("target", ""),
            "started": started.isoformat() if hasattr(started, "isoformat") else str(started),
            "finished": finished.isoformat() if hasattr(finished, "isoformat") else str(finished),
            "elapsed": round((finished - started).total_seconds(), 2) if hasattr(finished, "timestamp") else 0.0,
            "steps": results,
            "missing": plan.get("missing", []),
            "warnings": plan.get("warnings", []),
        }
        with path.open("w", encoding="utf-8") as fh:
            json.dump(body, fh, ensure_ascii=False, indent=2)
        return str(path)
    except OSError as exc:
        log_line("REPORT_FAILED %s %s" % (path, exc))
        return ""


def run_completion_hook(cfg, plan, report_path, url=""):
    hook = ((cfg.get("http") or {}).get("on_complete_hook") or "").strip()
    if not hook:
        return ""
    target = plan.get("target", "")
    argv = shlex.split(hook.format(
        target=target, drive=plan.get("drive", ""), engine=plan.get("engine", ""),
        report=report_path or "", url=url, tier=plan.get("tier", ""),
    ))
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=60)
        log_line("HOOK exit=%s argv=%s" % (proc.returncode, " ".join(mask_argv(argv))))
        msg = (proc.stdout or "").strip().splitlines()
        return (msg[0][:200] if msg else "")
    except (OSError, subprocess.TimeoutExpired) as exc:
        log_line("HOOK_FAILED %s %s" % (" ".join(mask_argv(argv)), exc))
        return ""


LIVE_FILE_NAME = "下载速度.live.json"


def live_file_for(cfg, plan, target=None):
    http = cfg.get("http") or {}
    live_dir = (http.get("live_dir") or "").strip()
    if live_dir:
        base = Path(live_dir).expanduser()
    else:
        report_dir = (http.get("report_dir") or "").strip()
        base = Path(report_dir).expanduser() if report_dir else Path(target or plan.get("target") or ".")
    return base / LIVE_FILE_NAME


class LiveMonitor:
    """下载期间周期性采样目标目录字节增量，写入实时速度状态 JSON 文件。"""

    HISTORY_CAP = 300

    def __init__(self, cfg, plan, url="", interval=1.0):
        self.cfg = cfg
        self.plan = plan
        self.url = url or ""
        self.interval = max(0.3, float(interval or 1.0))
        self.target = Path(plan.get("target") or ".")
        self.live_path = live_file_for(cfg, plan)
        self._stop = threading.Event()
        self._thread = None
        self.state = "running"
        self.started = time.time()
        self.last_bytes = 0
        self.last_ts = None
        self.current_step = ""
        self._baseline = self._total_bytes()
        self.total_bytes = 0
        try:
            self.total_bytes = int(plan.get("total_bytes") or 0)
        except (TypeError, ValueError):
            self.total_bytes = 0
        self.history = []  # [(elapsed_seconds, speed_kbps), ...] 画曲线用

    def _total_bytes(self):
        total = 0
        try:
            if self.target.exists():
                for p in self.target.iterdir():
                    if p.is_file() and p.name != LIVE_FILE_NAME:
                        try:
                            total += p.stat().st_size
                        except OSError:
                            pass
        except OSError:
            pass
        return total

    def set_step(self, note=""):
        self.current_step = note or ""

    def set_total_bytes(self, value):
        try:
            value = int(value)
        except (TypeError, ValueError):
            return self.total_bytes
        self.total_bytes = max(0, value)
        return self.total_bytes

    def start(self):
        """启动后台线程：按 interval 周期采样并写入实时速度 JSON，直到 stop() 为止。"""
        if self._thread and self._thread.is_alive():
            return self._thread

        def _loop():
            interval = max(0.3, self.interval)
            while not self._stop.is_set():
                try:
                    self.write(state=self.state)
                except Exception as exc:  # 监控线程异常不应中断下载
                    log_line("LIVE_LOOP_ERR %s" % exc)
                self._stop.wait(interval)

        self._thread = threading.Thread(target=_loop, daemon=True, name="pan-live-monitor")
        self._thread.start()
        return self._thread

    def _sample(self):
        now = time.time()
        cur = self._total_bytes()
        dt = (now - self.last_ts) if self.last_ts else 0.0
        speed = 0.0
        if dt and dt > 0:
            speed = (cur - self.last_bytes) / dt / 1024.0
        self.last_bytes, self.last_ts = cur, now
        elapsed = max(0.0, now - self.started)
        done = max(0, cur - self._baseline)
        avg = (done / elapsed / 1024.0) if elapsed > 0 else 0.0
        self.history.append((round(elapsed, 2), max(speed, 0.0)))
        if len(self.history) > self.HISTORY_CAP:
            self.history = self.history[-self.HISTORY_CAP:]
        return done, max(speed, 0.0), max(avg, 0.0), elapsed

    def write(self, state=None):
        done, speed, avg, elapsed = self._sample()
        body = {
            "schema": 1,
            "state": state or self.state,
            "url": self.url,
            "drive": self.plan.get("drive", ""),
            "drive_name": self.plan.get("drive_name", ""),
            "engine": self.plan.get("engine", ""),
            "tier": self.plan.get("tier", ""),
            "target": str(self.target),
            "started": datetime.fromtimestamp(self.started).strftime("%Y-%m-%dT%H:%M:%S%z"),
            "updated": datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
            "elapsed": round(elapsed, 2),
            "bytes_done": int(done),
            "speed_kbps": round(speed, 2),
            "avg_speed_kbps": round(avg, 2),
            "total_bytes": int(self.total_bytes or 0),
            "percent": round(done * 100.0 / self.total_bytes, 1) if self.total_bytes and self.total_bytes > 0 else None,
            "eta_seconds": round((self.total_bytes - done) / 1024.0 / avg, 1) if (self.total_bytes and self.total_bytes > 0 and avg and avg > 0) else None,
            "history": [[t, v] for (t, v) in self.history],
            "current_step": self.current_step,
        }
        try:
            self.live_path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.live_path.with_suffix(self.live_path.suffix + ".tmp")
            tmp.write_text(json.dumps(body, ensure_ascii=False), encoding="utf-8")
            tmp.replace(self.live_path)
        except OSError as exc:
            log_line("LIVE_WRITE_FAIL %s %s" % (self.live_path, exc))
        return body

    def stop(self, ok=True):
        if self._stop.is_set() and self.state not in ("done", "failed"):
            self.state = "running"
        self.state = "done" if ok else "failed"
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=self.interval * 3 + 1)
        self.write(state=self.state)


# ------------------------------------------------------------------ 任务控制
# 任务登记在 http.live_dir / http.report_dir / 目标目录 的“任务控制.json”，
# 供 serve 任务中心和 `pan task ...` 实现 暂停/继续/取消/删除/重试。
TASK_FILE_NAME = "任务控制.json"


def _task_file_for_dir(reports_dir):
    return Path(reports_dir) / TASK_FILE_NAME


def read_task_records(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        recs = data.get("tasks")
        return recs if isinstance(recs, dict) else {}
    except (OSError, json.JSONDecodeError, AttributeError):
        return {}


def _atomic_write_json(path, body):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(body, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        tmp.chmod(0o600)
    except OSError:
        pass
    tmp.replace(path)


def task_control_file_for(cfg, plan, target=None):
    """任务控制文件与实时速度文件同目录，便于任务中心集中管理。"""
    return live_file_for(cfg, plan, target=target).with_name(TASK_FILE_NAME)


class TaskControl:
    """任务状态机：running / paused / cancelled / done / failed，落盘到任务控制.json。"""

    def __init__(self, cfg, plan, url="", args=None):
        self.cfg = cfg
        self.plan = plan
        self.url = url or ""
        self.args = dict(args or {})
        self.target = plan.get("target") or "."
        self.path = task_control_file_for(cfg, plan)
        self.task_id = _task_id(self.target)
        self._lock = threading.Lock()

    def register(self):
        rec = self._rec()
        rec["state"] = "running"
        self._mutate(lambda recs: recs.update({self.task_id: rec}) or recs)
        return rec

    def _rec(self):
        return {
            "id": self.task_id,
            "schema": 1,
            "state": "running",
            "url": self.url,
            "drive": self.plan.get("drive", ""),
            "drive_name": self.plan.get("drive_name", ""),
            "engine": self.plan.get("engine", ""),
            "tier": self.plan.get("tier", ""),
            "target": str(self.target),
            "pwd_present": bool(self.args.get("pwd")),
            "args": {k: v for k, v in self.args.items() if k != "pwd"},
            "pid": os.getpid(),
            "started": datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
            "updated": datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
            "current_step": "",
            "finished": "",
            "rc": None,
        }

    def _mutate(self, fn):
        with self._lock:
            recs = read_task_records(self.path)
            recs = fn(recs) or recs
            _atomic_write_json(self.path, {"schema": 1, "tasks": recs})

    def read_state(self):
        rec = read_task_records(self.path).get(self.task_id) or {}
        return rec.get("state", "running")

    def set_step(self, note=""):
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
        self._mutate(lambda recs: (recs.get(self.task_id) or {}).update(
            {"current_step": note or "", "updated": now}) or recs)

    def finish(self, ok=True, rc=0):
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
        _rc = int(rc or 0)
        state = "cancelled" if _rc == 130 else ("done" if ok else "failed")
        self._mutate(lambda recs: (recs.get(self.task_id) or {}).update(
            {"state": state, "rc": _rc, "finished": now, "updated": now}) or recs)
        return state


def _signal_group(proc, sig):
    try:
        os.killpg(os.getpgid(proc.pid), sig)
    except (OSError, ProcessLookupError, PermissionError):
        pass


def _terminate_group(proc):
    _signal_group(proc, signal.SIGTERM)
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        _signal_group(proc, signal.SIGKILL)
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            pass


def _wait_controlled(proc, tc):
    """在任务状态机控制下等待单个子进程结束；支持暂停/继续/取消。返回 (rc, status)。"""
    suspended = False
    try:
        while True:
            state = tc.read_state()
            if state == "cancelled":
                _terminate_group(proc)
                return (proc.returncode if proc.poll() is not None else 130), "cancelled"
            if state == "paused":
                if not suspended and proc.poll() is None:
                    _signal_group(proc, signal.SIGSTOP)
                    suspended = True
                if proc.poll() is None:
                    while tc.read_state() == "paused" and proc.poll() is None:
                        time.sleep(0.2)
                    if proc.poll() is None:
                        _signal_group(proc, signal.SIGCONT)
                    suspended = False
            elif suspended:
                if proc.poll() is None:
                    _signal_group(proc, signal.SIGCONT)
                suspended = False
            if proc.poll() is not None:
                return proc.returncode, "ok"
            time.sleep(0.2)
    except KeyboardInterrupt:
        _terminate_group(proc)
        return 130, "cancelled"


def _run_step_controlled(argv, kwargs, tc, timeout=0):
    """以可暂停/取消的方式执行单个子进程；返回 (rc, status, error)。"""
    kwargs = dict(kwargs)
    kwargs.pop("timeout", None)
    input_data = kwargs.pop("input", None)
    kwargs.pop("text", None)
    try:
        proc = subprocess.Popen(argv, stdin=subprocess.PIPE if input_data is not None else None,
                                start_new_session=True, **kwargs)
    except (OSError, ValueError) as exc:
        return 127, "error", exc
    if input_data is not None:
        try:
            data = input_data if isinstance(input_data, bytes) else str(input_data).encode("utf-8")
            proc.stdin.write(data)
            proc.stdin.flush()
            proc.stdin.close()
        except (OSError, ValueError):
            pass
    deadline = (time.time() + timeout) if timeout else None
    rc, status = _wait_controlled(proc, tc)
    if status == "cancelled":
        return rc, status, None
    if deadline and time.time() >= deadline:
        _terminate_group(proc)
        return 124, "timeout", None
    return rc, status, None


def is_http_url(url):
    return str(url or "").lower().startswith(("http://", "https://"))


def probe_http_total_bytes(url, cfg=None, timeout=8):
    """尽力读取直链 Content-Length，用于剩余时间估算；失败返回 0（不阻塞下载）。"""
    cfg = cfg or {}
    connect_timeout = int((cfg.get("http") or {}).get("connect_timeout", 15))
    argv = ["curl", "-sI", "-L", "--connect-timeout", str(connect_timeout), "--max-time", str(timeout), url]
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout + 2)
    except (OSError, subprocess.TimeoutExpired):
        return 0
    text = (proc.stdout or "") + "\n" + (proc.stderr or "")
    # 取最后一次 Content-Length，兼容重定向后真实资源
    value = None
    for line in text.splitlines():
        head = line.split(":", 1)
        if len(head) == 2 and head[0].strip().lower() == "content-length":
            value = head[1].strip()
    try:
        return max(0, int(value or 0))
    except (TypeError, ValueError):
        return 0


def resolve_split_count(cfg, args):
    v = getattr(args, "split", 0) or 0
    try:
        n = int(v)
    except (TypeError, ValueError):
        n = 0
    if n and n > 0:
        return n
    http = cfg.get("http", {})
    if http.get("range_split"):
        try:
            return int(http.get("range_split_connections") or 0)
        except (TypeError, ValueError):
            return 0
    return 0


def probe_http_range(url, timeout=15):
    try:
        proc = subprocess.run(["curl", "-sI", "-L", "--max-time", str(timeout), url],
                              capture_output=True, text=True, timeout=timeout + 5)
    except (OSError, subprocess.TimeoutExpired):
        return None, False
    if proc.returncode != 0:
        return None, False
    length = None
    accept_ranges = False
    for line in (proc.stdout or "").splitlines():
        low = line.lower()
        if low.startswith("content-length:"):
            try:
                length = int(line.split(":", 1)[1].strip())
            except ValueError:
                pass
        elif low.startswith("accept-ranges:"):
            accept_ranges = "bytes" in line.split(":", 1)[1].strip().lower()
    return (length if length and length > 0 else None), accept_ranges


def run_curl_split(url, target_path, split, cfg, emit_events=False, live=None, task_control=None):
    """http 直链单文件 Range 分片并发下载；服务端不支持时返回 (None, [], 说明) 回退整文件。"""
    length, accept_ranges = probe_http_range(url)
    if not length or not accept_ranges or length < 2:
        return None, [], "服务端不支持可探测的 Range/Content-Length，回退整文件下载"
    n = min(int(split), length)
    if n < 2:
        return None, [], "分片数不足，回退整文件下载"
    http = cfg.get("http", {})
    timeout = int(http.get("connect_timeout", 30) or 30)
    retries = str(http.get("retries", 3))
    delay = str(http.get("retry_delay", 5))
    base = length // n
    procs = []
    results = []
    started = time.time()
    for i in range(n):
        start = base * i
        end = (base * (i + 1) - 1) if i < n - 1 else (length - 1)
        part = Path(str(target_path) + ".part%02d" % i)
        argv = ["curl", "-L", "--fail", "--retry", retries, "--retry-delay", delay,
                "--connect-timeout", str(timeout), "-r", "%d-%d" % (start, end),
                "-o", str(part), url]
        entry = {"index": i + 1, "engine": "curl-split", "note": "Range %d-%d" % (start, end),
                 "argv": mask_argv(argv), "uses_stdin_credential": False,
                 "started": datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
                 "rc": -1, "elapsed": 0.0, "error": ""}
        results.append(entry)
        if live is not None:
            live.set_step(entry["note"])
        if task_control is not None:
            task_control.set_step(entry["note"])
        if emit_events:
            print(json.dumps({"event": "segment_start", "index": i + 1, "range": "%d-%d" % (start, end)}, ensure_ascii=False))
        try:
            proc = subprocess.Popen(argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                    start_new_session=bool(task_control is not None))
        except OSError as exc:
            entry["rc"] = 127
            entry["error"] = str(exc)
            return 127, results, "无法启动 curl：%s" % exc
        procs.append((i, start, end, part, proc))
    failed = None
    cancelled = False
    for i, start, end, part, proc in procs:
        if task_control is not None:
            rc, status = _wait_controlled(proc, task_control)
            if status == "cancelled":
                cancelled = True
                for _j, _s, _e, _p, _pr in procs:
                    if _pr.poll() is None:
                        _terminate_group(_pr)
                break
        else:
            rc = proc.wait()
        results[i]["rc"] = rc
        results[i]["elapsed"] = round(time.time() - started, 2)
        if emit_events:
            print(json.dumps({"event": "segment_done", "index": i + 1, "range": "%d-%d" % (start, end), "rc": rc}, ensure_ascii=False))
        if rc != 0 and failed is None:
            failed = (i, rc)
    if cancelled:
        return 130, results, "任务已取消"
    if failed is not None:
        i, rc = failed
        results[i]["error"] = "segment exit=%s" % rc
        return rc, results, "分片下载失败（第 %s 段 exit=%s）" % (i + 1, rc)
    try:
        with Path(target_path).open("wb") as out:
            for i, start, end, part, proc in procs:
                with part.open("rb") as pin:
                    shutil.copyfileobj(pin, out)
                try:
                    part.unlink()
                except OSError:
                    pass
    except OSError as exc:
        return 127, results, "合并写文件失败：%s" % exc
    size = Path(target_path).stat().st_size if Path(target_path).exists() else 0
    if size != length:
        return 127, results, "合并字节数校验失败 expected=%s actual=%s" % (length, size)
    return 0, results, "Range 分片下载完成（%sB，%s 段）" % (length, n)



COMPANY_DEST_MARKERS = ("/volumes/办公", "/volumes/拓展", "/mnt/办公", "/mnt/拓展", r"\\办公", r"\\拓展", "公司知识库")


def is_company_destination(dst):
    low = str(dst or "").lower()
    return any(m in low for m in COMPANY_DEST_MARKERS)


def scan_transfer_dest_guard(cfg, dst, allow_flag):
    if not is_company_destination(dst):
        return ""
    if allow_flag:
        return ""
    if bool((cfg.get("transfer") or {}).get("allow_company_dest")):
        return ""
    return "目标目录命中公司数据红线（只下载不上传默认不开放）：%s；确认允许请加 --allow-company-dest" % dst


def _transfer_args(cfg, args, kind):
    tcfg = cfg.get("transfer", {}) or {}
    transfers = getattr(args, "transfers", None) or tcfg.get("default_transfers", 4)
    checkers = getattr(args, "checkers", None) or tcfg.get("default_checkers", 8)
    return int(transfers), int(checkers)


def run_transfer_sync(kind, args):
    cfg = load_config()
    dst = args.dst
    guard = scan_transfer_dest_guard(cfg, dst, bool(getattr(args, "allow_company_dest", False)))
    if guard:
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "kind": kind, "error": guard, "missing": []}, ensure_ascii=False, indent=2))
        else:
            print("❌ %s" % guard)
        return 4
    if kind == "sync" and not getattr(args, "delete", False):
        msg = "sync 会删除目标多余文件，必须显式加 --delete + --apply"
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "kind": kind, "error": msg, "missing": []}, ensure_ascii=False, indent=2))
        else:
            print("❌ %s" % msg)
        return 3
    rclone = find_engine_binary("rclone", cfg)
    if not rclone:
        msg = "未安装 rclone。跨盘转存/同步依赖 rclone（brew install rclone），先用 pan.py doctor 确认"
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "kind": kind, "error": msg, "missing": ["rclone"]}, ensure_ascii=False, indent=2))
        else:
            print("❌ %s" % msg)
        return 2
    transfers, checkers = _transfer_args(cfg, args, kind)
    argv = [rclone, "copy" if kind == "transfer" else "sync",
            args.src, dst, "--transfers", str(transfers), "--checkers", str(checkers)]
    apply_run = bool(getattr(args, "apply", False))
    if not apply_run:
        argv.append("--dry-run")
    if getattr(args, "json", False):
        print(json.dumps({"ok": True, "kind": kind, "dry_run": not apply_run,
                          "rclone": rclone, "command": argv, "src": args.src, "dst": dst,
                          "transfers": transfers, "checkers": checkers}, ensure_ascii=False, indent=2))
    else:
        print("命令：" + " ".join(mask_argv(argv)))
        print("目标：%s" % dst)
        print("模式：%s" % ("dry-run（未实际执行；确认后加 --apply）" if not apply_run else "实际执行"))
    if not apply_run:
        return 0
    log_line("%s rclone=%s src=%s dst=%s" % (kind.upper(), rclone, args.src, dst))
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=0)
    except (OSError, subprocess.TimeoutExpired) as exc:
        print("❌ rclone 执行失败：%s" % exc)
        return 127
    out = (proc.stdout or "").strip() + ("\n" + (proc.stderr or "").strip() if proc.stderr else "")
    if out:
        print(out[:2000])
    if proc.returncode == 0:
        print("✅ %s 完成：%s -> %s" % (kind, args.src, dst))
    return proc.returncode


def cmd_transfer(args):
    return run_transfer_sync("transfer", args)


def cmd_sync(args):
    return run_transfer_sync("sync", args)



def notify_webhook_url(cfg, channel):
    key = str(((cfg.get("notify") or {}).get(channel + "_secret") or "")).strip() or ("notify." + channel)
    value = keychain_get(key)
    return value, key


def build_notify_payload(channel, title, body):
    if channel == "work_weixin":
        return json.dumps({"msgtype": "text", "text": {"content": (title + "\n" + body).strip()}},
                          ensure_ascii=False)
    return json.dumps({"title": title, "body": body}, ensure_ascii=False)


def cmd_notify_send(args):
    cfg = load_config()
    url, ref = notify_webhook_url(cfg, args.channel)
    if args.channel == "telegram" and not getattr(args, "chat_id", ""):
        msg = "telegram 需要 --chat-id"
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "channel": "telegram", "error": msg}, ensure_ascii=False, indent=2))
        else:
            print("❌ %s" % msg)
        return 1
    payload = build_notify_payload(args.channel, args.title, args.body, getattr(args, "chat_id", "") or "")
    if not url:
        msg = "未配置 %s webhook：请先在本机运行 pan secret set notify.%s --stdin 保存地址" % (args.channel, args.channel)
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "channel": args.channel, "error": msg}, ensure_ascii=False, indent=2))
        else:
            print("❌ %s" % msg)
        return 1
    if getattr(args, "json", False):
        print(json.dumps({"ok": True, "channel": args.channel, "send": bool(args.send),
                          "masked": True, "payload": json.loads(payload)}, ensure_ascii=False, indent=2))
    else:
        print("通知：%s｜发送：%s｜标题：%s" % (args.channel, "是(--send)" if args.send else "否(dry-run；加 --send)", args.title))
    if not args.send:
        return 0
    tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    tmp.write(payload); tmp.close(); Path(tmp.name).chmod(0o600)
    cfg_curl = "url = %s\n-H = \"Content-Type: application/json\"\n--data = \"@%s\"\n" % (json.dumps(url), tmp.name)
    log_line("NOTIFY channel=%s send=1 ref=%s" % (args.channel, ref))
    try:
        proc = subprocess.run(["curl", "-sS", "--config", "-"], input=cfg_curl,
                              capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as exc:
        Path(tmp.name).unlink(missing_ok=True)
        print("❌ 通知发送失败：%s" % exc)
        return 127
    Path(tmp.name).unlink(missing_ok=True)
    if proc.returncode != 0:
        print("❌ 通知发送失败 exit=%s %s" % (proc.returncode, (proc.stderr or proc.stdout or "").strip()[:300]))
        return proc.returncode
    print("✅ 通知已发送：%s" % args.channel)
    return 0



ENV_HINT_CMDS = {
    "rclone": ("rclone", "brew install rclone（目录递归 / 转存 / 同步需要）"),
    "alist": ("AList", "安装 AList（官方脚本或 Docker；或只用直链 / WebDAV）"),
    "aria2": ("aria2", "brew install aria2（可选，大文件多线程）"),
    "baidupcs": ("BaiduPCS-Go", "安装 BaiduPCS-Go（百度分享需要）"),
    "quarkcli": ("quark-cli", "安装 quark-cli（夸克需要）"),
}


def env_install_hints(cfg):
    hints = []
    for engine, (label, hint) in ENV_HINT_CMDS.items():
        if not find_engine_binary(engine, cfg):
            hints.append("%s：%s" % (label, hint))
    return hints


def cmd_init_wizard(args):
    cfg = load_config()
    created = False
    root0 = default_root(cfg)
    hints = env_install_hints(cfg)
    try:
        drives = sorted(all_drives(cfg).keys())
    except Exception:
        drives = []
    plan = {
        "ok": True,
        "config": str(CONFIG_PATH),
        "created": created,
        "download_root": str(root0),
        "hints": hints,
        "drives": drives,
        "next_steps": [
            "python3 scripts/pan.py doctor --json",
            "python3 scripts/pan.py secret set notify.work_weixin --stdin",
            "python3 scripts/pan.py login <盘名>",
        ],
    }
    if getattr(args, "json", False):
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0
    print("向导：只读检测（要创建配置请运行：pan init）")
    print("配置文件：%s" % CONFIG_PATH)
    print("默认下载目录：%s" % root0)
    if hints:
        print("建议安装：")
        for h in hints:
            print("  - %s" % h)
    if drives:
        print("可识别网盘：%s 个" % len(drives))
    print("下一步：doctor 检查 → login 登录 → get 下载")
    return 0


# ------------------------------------------------------------------ 一键安装与配置向导
INSTALL_CMDS = {
    "rclone": {
        "brew": ["brew", "install", "rclone"],
        "apt": ["sudo", "apt-get", "install", "-y", "rclone"],
        "dnf": ["sudo", "dnf", "install", "-y", "rclone"],
        "winget": ["winget", "install", "--id", "Rclone.Rclone", "--accept-source-agreements", "--accept-package-agreements"],
    },
    "aria2": {
        "brew": ["brew", "install", "aria2"],
        "apt": ["sudo", "apt-get", "install", "-y", "aria2"],
        "dnf": ["sudo", "dnf", "install", "-y", "aria2"],
        "winget": ["winget", "install", "--id", "aria2.aria2", "--accept-source-agreements", "--accept-package-agreements"],
    },
}


def detect_pkg_manager():
    """按当前平台返回可用于自动安装的包管理器；找不到返回空。"""
    sys_name = platform.system().lower()
    if sys_name == "darwin":
        return "brew" if shutil.which("brew") else ""
    if sys_name in ("linux",):
        for name in ("apt-get", "dnf", "yum", "apk"):
            if shutil.which(name):
                return name.replace("-get", "") if name in ("apt-get",) else name
        return ""
    if sys_name == "windows":
        for name in ("winget", "choco", "scoop"):
            if shutil.which(name):
                return name
        return ""
    return ""


def setup_install_plan(cfg):
    """生成一键安装计划：缺失依赖 + 可执行命令列表。"""
    missing = []
    commands = []
    pkg = detect_pkg_manager()
    for engine, (label, hint) in ENV_HINT_CMDS.items():
        if find_engine_binary(engine, cfg):
            continue
        item = {"engine": engine, "label": label, "manual": (hint or "").strip()}
        cmd = (INSTALL_CMDS.get(engine) or {}).get(pkg) if pkg else None
        if cmd:
            item["command"] = cmd
            commands.append(cmd)
        missing.append(item)
    return {"pkg_manager": pkg or "", "missing": missing, "commands": commands}


def cmd_setup(args):
    """一键安装 + 配置向导：创建配置、补依赖、输出下一步。"""
    cfg = load_config()
    created = False
    if not CONFIG_PATH.exists() or getattr(args, "force", False):
        if getattr(args, "root", None):
            cfg["download_root"] = os.path.expanduser(args.root)
        save_config(cfg)
        created = True
    elif getattr(args, "root", None):
        cfg["download_root"] = os.path.expanduser(args.root)
        save_config(cfg)
    plan = setup_install_plan(cfg)
    ok = True
    applied = []
    if getattr(args, "apply", False) and plan["commands"]:
        for argv in plan["commands"]:
            print("RUN:", " ".join(shlex.quote(x) for x in mask_argv(argv)))
            try:
                proc = subprocess.run(argv, timeout=180)
            except (OSError, subprocess.TimeoutExpired) as exc:
                ok = False
                applied.append({"argv": mask_argv(argv), "ok": False, "error": str(exc)})
                print("  ❌ %s" % exc)
                continue
            applied.append({"argv": mask_argv(argv), "ok": proc.returncode == 0})
            if proc.returncode != 0:
                ok = False
                print("  ❌ exit=%s" % proc.returncode)
    result = {
        "ok": ok,
        "setup": "complete" if (not plan["missing"] and ok) else "partial",
        "config": str(CONFIG_PATH),
        "created": created,
        "pkg_manager": plan["pkg_manager"],
        "missing": plan["missing"],
        "applied": applied,
        "next_steps": [
            "python3 scripts/pan.py doctor --json",
            "python3 scripts/pan.py login <盘名>",
            "python3 scripts/pan.py get <链接>",
        ],
    }
    if getattr(args, "json", False):
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if ok else 1
    print("pan-downloader setup")
    print("配置文件：%s%s" % (CONFIG_PATH, "（已创建）" if created else ""))
    print("系统包管理器：%s" % (plan["pkg_manager"] or "未识别（按需手动安装）"))
    if plan["missing"]:
        print("待安装：")
        for item in plan["missing"]:
            cmds = "、".join(shlex.quote(x) for x in item.get("command", [])) if item.get("command") else item.get("manual", "手动安装")
            print("  - %s：%s" % (item["label"], cmds))
    if applied:
        print("已执行：%d 条" % len(applied))
        for item in applied:
            print("  - %s → %s" % (" ".join(shlex.quote(x) for x in item["argv"]), "成功" if item["ok"] else "失败"))
    if not plan["missing"]:
        print("✅ 环境已就绪，下一步：login 登录 → get 下载")
    else:
        print("提示：可用 `python3 scripts/pan.py setup --apply` 尝试自动安装；无法自动装的依赖按上面提示手动安装。")
    return 0 if ok else 1


def cmd_mcp_guide(args):
    script = Path(__file__).resolve().parent / "pan_mcp.py"
    ok = script.exists()
    snippet = ("[mcp_servers.pan-cloud-drive]\n"
               "command = %s\n"
               "enabled = true\n" % json.dumps(str(script)))
    body = {
        "ok": ok,
        "script": str(script),
        "config_toml": snippet if ok else "",
        "note": "加到 $CODEX_HOME/config.toml 后重启 Codex；Agent 配置切换工具 接管可能覆盖，需重新注册",
    }
    if getattr(args, "json", False):
        print(json.dumps(body, ensure_ascii=False, indent=2))
    elif not ok:
        print("❌ 未找到 %s" % script)
    else:
        print("MCP 注册片段（写入 $CODEX_HOME/config.toml 的 [mcp_servers] 区）：")
        print(snippet)
        print("提示：重启 Codex 后在对话里应能看到 pan_doctor / pan_detect / pan_dirs / pan_get_plan")
    return 0 if ok else 1


def build_notify_payload(channel, title, body, chat_id=""):
    content = (title + "\n" + body).strip()
    if channel == "work_weixin":
        return json.dumps({"msgtype": "text", "text": {"content": content}}, ensure_ascii=False)
    if channel == "bark":
        return json.dumps({"title": title, "body": body}, ensure_ascii=False)
    if channel == "telegram":
        return json.dumps({"chat_id": chat_id, "text": content}, ensure_ascii=False)
    if channel == "discord":
        return json.dumps({"content": content}, ensure_ascii=False)
    if channel == "feishu":
        return json.dumps({"msg_type": "text", "content": {"text": content}}, ensure_ascii=False)
    return json.dumps({"title": title, "body": body}, ensure_ascii=False)


def read_report_summary(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return {"path": str(path), "ok": data.get("ok"), "engine": data.get("engine"),
            "drive": data.get("drive"), "target": data.get("target"),
            "finished": data.get("finished"), "elapsed": data.get("elapsed")}


def serve_reports_json(reports_dir, limit=50):
    base = Path(reports_dir)
    out = []
    if base.exists():
        for p in sorted(base.glob("**/下载报告.json"))[:limit]:
            item = read_report_summary(p)
            if item:
                out.append(item)
    return out


def serve_live_json(reports_dir, limit=50):
    """扫描实时速度状态文件（下载速度.live.json），返回最近 limit 个。"""
    base = Path(reports_dir)
    out = []
    if not base.exists():
        return out
    files = sorted(base.glob("**/%s" % LIVE_FILE_NAME), key=lambda p: p.stat().st_mtime, reverse=True)
    for f in files[:limit]:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        data["path"] = str(f)
        data["mtime"] = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%dT%H:%M:%S%z")
        out.append(data)
    return out


def _task_id(target):
    import hashlib
    return hashlib.sha1(str(target).encode("utf-8")).hexdigest()[:12]


def serve_unified_tasks(reports_dir, limit=100, state=None):
    """统一任务中心：实时任务 + 历史报告 + 任务控制记录汇总成一张任务表。"""
    control = serve_task_controls(reports_dir, limit=limit * 2)
    tasks = []
    # 实时任务（优先以 live 文件为准）
    live = serve_live_json(reports_dir, limit=limit)
    for item in live:
        st = item.get("state", "")
        ctl = control.get(_task_id(item.get("target", "")))
        if ctl and ctl.get("state") in ("paused", "cancelled"):
            st = ctl["state"]
        if state and st != state:
            continue
        tasks.append({
            "id": _task_id(item.get("target", "")),
            "source": "live",
            "state": st,
            "drive": item.get("drive", ""),
            "drive_name": item.get("drive_name", ""),
            "engine": item.get("engine", ""),
            "tier": item.get("tier", ""),
            "url": item.get("url", ""),
            "target": item.get("target", ""),
            "current_step": item.get("current_step", ""),
            "speed_kbps": item.get("speed_kbps"),
            "avg_speed_kbps": item.get("avg_speed_kbps"),
            "bytes_done": item.get("bytes_done", 0),
            "started": item.get("started", ""),
            "updated": item.get("updated", "") or item.get("mtime", ""),
            "finished": item.get("updated", "") if st in ("done", "failed", "cancelled") else "",
            "elapsed": item.get("elapsed", 0),
            "ok": st not in ("failed", "cancelled"),
        })
    # 历史报告（不在 live 里重复/或已结束的兜底）
    seen = {t["target"] for t in tasks}
    reports = serve_reports_json(reports_dir, limit=limit)
    for r in reports:
        if r.get("target") in seen:
            continue
        st = "done" if r.get("ok") else "failed"
        if state and st != state:
            continue
        tasks.append({
            "id": _task_id(r.get("target", "")),
            "source": "report",
            "state": st,
            "drive": r.get("drive", ""),
            "drive_name": "",
            "engine": r.get("engine", ""),
            "tier": "",
            "url": "",
            "target": r.get("target", ""),
            "current_step": "",
            "speed_kbps": None,
            "avg_speed_kbps": None,
            "bytes_done": 0,
            "started": "",
            "updated": r.get("finished", ""),
            "finished": r.get("finished", ""),
            "elapsed": r.get("elapsed", 0),
            "ok": bool(r.get("ok")),
        })
    # 任务控制记录兜底（paused/cancelled/done/failed 等不在 live/报告中的）
    seen = {t["target"] for t in tasks}
    for tid, rec in sorted(control.items(), key=lambda kv: str(kv[1].get("updated") or ""), reverse=True):
        if rec.get("target") in seen:
            continue
        st = rec.get("state") or "running"
        if state and st != state:
            continue
        tasks.append({
            "id": tid,
            "source": "task",
            "state": st,
            "drive": rec.get("drive", ""),
            "drive_name": rec.get("drive_name", ""),
            "engine": rec.get("engine", ""),
            "tier": rec.get("tier", ""),
            "url": rec.get("url", ""),
            "target": rec.get("target", ""),
            "current_step": rec.get("current_step", ""),
            "speed_kbps": None,
            "avg_speed_kbps": None,
            "bytes_done": 0,
            "started": rec.get("started", ""),
            "updated": rec.get("updated", ""),
            "finished": rec.get("finished", ""),
            "elapsed": 0,
            "ok": st not in ("failed", "cancelled"),
        })
    # 去掉内部用路径字段后返回
    for t in tasks:
        t.pop("_control_path", None)
    # 去语气归一：live 优先，报告/控制记录排后
    tasks.sort(key=lambda t: (t.get("updated") or ""), reverse=True)
    return tasks[:limit]


def _spawn_retry_task(rec):
    """按任务控制记录里的参数重新拉起一个 get 子进程；返回 (pid, 错误)。"""
    url = rec.get("url", "")
    if not url:
        return "", "任务记录缺少 url，无法重试"
    args = rec.get("args") or {}
    argv = [sys.executable, str(Path(__file__).resolve()), "get", url,
            "--to", str(args.get("to") or ""), "--engine", str(args.get("engine") or ""),
            "--tier", str(args.get("tier") or "")]
    if args.get("path"):
        argv += ["--path", str(args["path"])]
    try:
        proc = subprocess.Popen(argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                start_new_session=True)
    except OSError as exc:
        return "", "启动重试失败：%s" % exc
    return str(proc.pid), ""


def serve_task_controls(reports_dir, limit=200):
    """递归收集 reports_dir 下所有任务控制记录（按 target 去重）。"""
    base = Path(reports_dir)
    out = {}
    if base.exists():
        for f in sorted(base.glob("**/" + TASK_FILE_NAME), key=lambda p: p.stat().st_mtime, reverse=True):
            recs = read_task_records(f)
            for k, v in recs.items():
                out.setdefault(k, dict(v))
                out[k]["_control_path"] = str(f)
            if len(out) >= limit:
                break
    return out


def _locate_task_control(reports_dir, task_id):
    base = Path(reports_dir)
    if not base.exists():
        return None, {}
    for f in base.glob("**/" + TASK_FILE_NAME):
        recs = read_task_records(f)
        if task_id in recs:
            return f, recs[task_id]
    return None, {}


def _apply_task_action(reports_dir, task_id, action):
    """对任务控制记录执行 pause/resume/delete/retry；返回 (ok, message)。"""
    path, rec = _locate_task_control(reports_dir, task_id)
    if not path or not rec:
        return False, "未找到任务 %s" % task_id
    if "_control_path" in rec:
        rec.pop("_control_path", None)
    recs = read_task_records(path)
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
    if action == "pause":
        if rec.get("state") != "running":
            return False, "只有运行中的任务可以暂停（当前：%s）" % rec.get("state")
        rec["state"] = "paused"
    elif action == "resume":
        if rec.get("state") != "paused":
            return False, "只有已暂停的任务可以继续（当前：%s）" % rec.get("state")
        rec["state"] = "running"
    elif action == "delete":
        if rec.get("state") == "running":
            rec["state"] = "cancelled"
            rec["updated"] = now
            rec["finished"] = rec.get("finished") or now
            _atomic_write_json(path, {"schema": 1, "tasks": recs})
            return True, "已发送取消并删除标记"
        recs.pop(task_id, None)
        _atomic_write_json(path, {"schema": 1, "tasks": recs})
        return True, "已删除任务记录"
    elif action == "retry":
        if rec.get("state") not in ("done", "failed", "cancelled"):
            return False, "仅已结束（done/failed/cancelled）任务可重试"
        pid, err = _spawn_retry_task(rec)
        if err:
            return False, err
        new_rec = dict(rec)
        new_rec["state"] = "running"
        new_rec["pid"] = pid
        new_rec["started"] = now
        new_rec["updated"] = now
        new_rec["finished"] = ""
        new_rec["rc"] = None
        recs[task_id] = new_rec
        _atomic_write_json(path, {"schema": 1, "tasks": recs})
        return True, "已重新启动下载（新 PID %s）；若原链接需要提取码，请用 `pan task show %s` 查看后补充 --pwd" % (pid, task_id)
    rec["updated"] = now
    recs[task_id] = rec
    _atomic_write_json(path, {"schema": 1, "tasks": recs})
    return True, "任务已%s" % action


def _spawn_download_task(url, pwd="", to="", engine="", tier="", path=""):
    """后台启动 pan get --live；返回 (pid, 错误)。供浏览器扩展 POST /api/download 调用。"""
    if not url or not url.strip():
        return "", "url 为空"
    argv = [sys.executable, str(Path(__file__).resolve()), "get", url.strip(), "--live"]
    if pwd:
        argv += ["--pwd", pwd]
    if to:
        argv += ["--to", to]
    if engine:
        argv += ["--engine", engine]
    if tier:
        argv += ["--tier", tier]
    if path:
        argv += ["--path", path]
    try:
        proc = subprocess.Popen(argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                start_new_session=True)
    except OSError as exc:
        return "", "启动下载失败：%s" % exc
    return str(proc.pid), ""


def serve_live_page_html(content, items_json="[]"):
    """渲染实时速度页 HTML（与任务中心同款深色风格），items_json 供前端画速度曲线。"""
    return ("""<!doctype html><html lang=zh-CN><head><meta charset=utf-8>"""
            """<meta name=viewport content="width=device-width,initial-scale=1">"""
            """<meta http-equiv=refresh content=2><title>多网盘实时速度</title>"""
            """<link rel="manifest" href="/manifest.webmanifest">"""
            """<script>if('serviceWorker'in navigator){navigator.serviceWorker.register('/sw.js')}</script>"""
            """<style>
:root{--bg:#0f172a;--panel:#1e293b;--line:#334155;--text:#e2e8f0;--muted:#94a3b8;--acc:#38bdf8}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:-apple-system,"PingFang SC","Microsoft YaHei",system-ui,sans-serif}
.wrap{max-width:1100px;margin:0 auto;padding:24px 18px 40px}
header{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:16px}
header h1{font-size:20px;margin:0}
.nav a{color:var(--acc);text-decoration:none;font-size:13px;margin-left:12px}
.nav a:hover{text-decoration:underline}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden}
table{width:100%%;border-collapse:collapse;font-size:13px}
thead th{background:#0b1120;color:var(--muted);text-align:left;padding:10px 14px;border-bottom:1px solid var(--line);white-space:nowrap}
tbody td{padding:10px 14px;border-bottom:1px solid var(--line)}
tr:last-child td{border-bottom:none}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px}
.speed{color:#facc15;font-weight:600}
.badge{display:inline-block;padding:2px 9px;border-radius:999px;font-size:11px;font-weight:600}
.badge.running{background:#f59e0b;color:#1a1206}
.badge.done{background:#22c55e;color:#052e16}
.badge.failed{background:#ef4444;color:#fff}
.badge.paused{background:#64748b;color:#f1f5f9}
.empty{background:var(--panel);border:1px solid var(--line);border-radius:12px;color:var(--muted);text-align:center;padding:40px;font-size:15px;line-height:1.8}
.empty span{font-size:12px}
#charts{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px;margin:16px 0 4px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:12px 14px}
.card h4{margin:0 0 8px;font-size:14px}
.card canvas{width:100%%;height:140px;display:block}
.card .meta{font-size:12px;color:var(--muted);margin-top:6px;line-height:1.6}
</style></head><body><div class=wrap>
<header><h1>⚡ 多网盘实时速度</h1><div class=nav>
<a href=/>任务中心</a><a href=/api/live>API 实时</a><a href=/api/status>API 状态</a>
</div></header>
<div class=panel><table>%(content)s</table><div id="CURVE_DATA" style="display:none">%(items_json)s</div></div>
<script>
(() => {
  const wrap = document.getElementById('charts');
  if (!wrap) return;
  let data = [];
  const el = document.getElementById('CURVE_DATA');
  try { data = JSON.parse(el ? el.textContent : '[]'); } catch (e) { data = []; }
  data.forEach((d, i) => {
    const his = d.history || [];
    const div = document.createElement('div');
    div.className = 'card';
    div.innerHTML = '<h4>' + d.name + '</h4><canvas width="600" height="140"></canvas><div class="meta">当前 ' + d.speed + ' KB/s · 平均 ' + d.avg + ' KB/s<br>已下载 ' + d.done + ' · 剩余 ' + d.eta + (d.percent != null ? ' · ' + d.percent + '%%' : '') + '</div>';
    wrap.appendChild(div);
    const cv = div.querySelector('canvas');
    const ctx = cv.getContext('2d');
    ctx.clearRect(0, 0, cv.width, cv.height);
    ctx.strokeStyle = '#475569'; ctx.lineWidth = 1;
    for (let gx = 0; gx <= 4; gx++) {
      const x = gx * cv.width / 4;
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, cv.height); ctx.stroke();
    }
    if (!his.length) return;
    let m = 0;
    his.forEach(pp => { m = Math.max(m, pp[1] || 0); });
    const top = Math.max(1, Math.ceil(m * 1.1 / 10) * 10);
    const grad = ctx.createLinearGradient(0, 0, 0, cv.height);
    grad.addColorStop(0, 'rgba(56,189,248,0.35)'); grad.addColorStop(1, 'rgba(56,189,248,0.02)');
    ctx.beginPath();
    his.forEach((pp, j) => {
      const x = cv.width * j / Math.max(1, his.length - 1);
      const y = cv.height - (cv.height - 16) * (pp[1] / top) - 8;
      if (j === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    });
    ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 2; ctx.stroke();
    ctx.lineTo(cv.width, cv.height); ctx.lineTo(0, cv.height); ctx.closePath();
    ctx.fillStyle = grad; ctx.fill();
    ctx.fillStyle = '#94a3b8'; ctx.font = '11px sans-serif';
    ctx.fillText('峰值 ' + (m.toFixed ? m.toFixed(1) : m) + ' KB/s', 8, cv.height - 8);
  });
})();
</script>
</div></body></html>""" % {"content": content, "items_json": items_json})


def pwa_manifest_json():
    """Web 应用清单：让任务中心可被 Chrome/Safari 安装为独立窗口 PWA。"""
    m = {
        "name": "多网盘任务中心",
        "short_name": "pan 任务中心",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0f172a",
        "theme_color": "#0f172a",
        "lang": "zh-CN",
        "icons": [
            {"src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
            {"src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
        ]
    }
    return json.dumps(m, ensure_ascii=False)


def pwa_service_worker_js():
    """离线优先外壳：只缓存首页与实时速度页，读取时仍从服务器取最新数据。"""
    return ("""const CACHE = 'pan-pwa-v1';
const PAGES = ['/', '/live', '/test'];
self.addEventListener('install', (e) => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(PAGES)));
});
self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((keys) =>
    Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))));
  self.clients.claim();
});
self.addEventListener('fetch', (e) => {
  e.respondWith(
    fetch(e.request).then((res) => {
      const clone = res.clone();
      if (e.request.method === 'GET') {
        caches.open(CACHE).then((c) => c.put(e.request, clone));
      }
      return res;
    }).catch(() => caches.match(e.request).then((hit) => hit || Response.error()))
  );
});
""")


def pwa_icon_png(size):
    """生成本地 PWA 图标 PNG（无需外部文件，尺寸 192/512）。"""
    import struct as _struct
    import zlib as _zlib

    def _chunk(t, d):
        c = _struct.pack('>I', len(d)) + t + d
        return c + _struct.pack('>I', _zlib.crc32(t + d) & 0xffffffff)

    w = h = size
    rows = []
    for y in range(h):
        row = bytearray([0])
        for x in range(w):
            dx = min(x, w - 1 - x); dy = min(y, h - 1 - y)
            r = int(size * 0.12)
            if dx < r and dy < r and ((r - dx) ** 2 + (r - dy) ** 2 > r * r):
                a = 0
            else:
                a = 255
            cy = y
            in_arrow = (0.45 * w <= x <= 0.55 * w and 0.30 * h <= cy <= 0.62 * h) or                        (0.42 * h <= cy <= 0.58 * h and 0.25 * w <= x <= 0.75 * w) or                        (cy >= 0.55 * h and cy <= int(0.62 * h) + (int(0.50 * w) - x))
            if in_arrow:
                c = (255, 255, 255, a)
            else:
                c = (40, 110, 210, a)
            row += bytes(c)
        rows.append(bytes(row))
    raw = b''.join(rows)
    ihdr = _chunk(b'IHDR', _struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0))
    return b'\x89PNG\r\n\x1a\n' + ihdr + _chunk(b'IDAT', _zlib.compress(raw)) + _chunk(b'IEND', b'')


def serve_home_html(tasks):
    """渲染任务中心首页 HTML（美观版；CSS 里的 %% 为 % 转义，防格式化报错）。"""
    if not tasks:
        rows = "<tr class=empty><td colspan=8>暂无任务（下载时执行 get --live 可看实时进度）</td></tr>"
    else:
        cells = []
        for t in tasks:
            sp = ("%.1f KB/s" % t["speed_kbps"]) if t.get("speed_kbps") is not None else "-"
            avg = ("%.1f" % t["avg_speed_kbps"]) if t.get("avg_speed_kbps") is not None else "-"
            st = t.get("state", "")
            cls = "live" if st == "running" else ("ok" if st == "done" else ("err" if st == "failed" else ""))
            badge = st if st else "unknown"
            tid = t.get("id", "")
            btns = []
            if st == "running":
                btns.append('<a class="btn warn" href="/api/task/action?task=%s&action=pause">暂停</a>' % tid)
                btns.append('<a class="btn danger" href="/api/task/action?task=%s&action=delete">取消</a>' % tid)
            elif st == "paused":
                btns.append('<a class="btn ok" href="/api/task/action?task=%s&action=resume">继续</a>' % tid)
                btns.append('<a class="btn danger" href="/api/task/action?task=%s&action=delete">删除</a>' % tid)
            else:
                btns.append('<a class="btn ok" href="/api/task/action?task=%s&action=retry">重试</a>' % tid)
                btns.append('<a class="btn danger" href="/api/task/action?task=%s&action=delete">删除</a>' % tid)
            cells.append(
                "<tr class='%s'><td class=mono>%s</td><td>%s</td><td>%s</td><td><span class=speed>%s</span></td>"
                "<td>%s</td><td><span class='badge %s'>%s</span></td><td class=mono>%s</td>"
                "<td class=ops>%s</td></tr>" % (
                    cls, tid, t.get("drive_name") or t.get("drive", ""),
                    t.get("current_step") or "-", sp, avg, badge, badge,
                    (t.get("updated") or t.get("finished") or ""), " ".join(btns)))
        rows = "".join(cells)

    counts = {"running": 0, "done": 0, "failed": 0}
    for t in tasks:
        st = t.get("state", "")
        if st in counts:
            counts[st] += 1
    card = ("<div class='card %(cls)s'><div class=label>%(label)s</div>"
            "<div class=num>%(num)s</div></div>")
    cards = ("<section class=cards>" +
             (card % {"cls": "run", "label": "运行中", "num": counts["running"]}) +
             (card % {"cls": "okc", "label": "已完成", "num": counts["done"]}) +
             (card % {"cls": "errc", "label": "失败", "num": counts["failed"]}) +
             (card % {"cls": "allc", "label": "全部", "num": len(tasks)}) +
             "</section>")

    return ("""<!doctype html><html lang=zh-CN><head><meta charset=utf-8>"""
            """<meta name=viewport content="width=device-width,initial-scale=1">"""
            """<meta http-equiv=refresh content=2><title>多网盘任务中心</title>"""
            """<link rel="manifest" href="/manifest.webmanifest">"""
            """<script>if('serviceWorker'in navigator){navigator.serviceWorker.register('/sw.js')}</script>"""
            """<style>
:root{--bg:#0f172a;--panel:#1e293b;--line:#334155;--text:#e2e8f0;--muted:#94a3b8;--acc:#38bdf8}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:-apple-system,"PingFang SC","Microsoft YaHei",system-ui,sans-serif}
.wrap{max-width:1120px;margin:0 auto;padding:24px 18px 40px}
header{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:16px}
header h1{font-size:20px;margin:0;letter-spacing:.5px}
.nav a{color:var(--acc);text-decoration:none;font-size:13px;margin-left:12px}
.nav a:hover{text-decoration:underline}
.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:18px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.card .label{font-size:12px;color:var(--muted)}
.card .num{font-size:26px;font-weight:700;margin-top:4px}
.card.run .num{color:#facc15}.card.okc .num{color:#4ade80}.card.errc .num{color:#f87171}.card.allc .num{color:#38bdf8}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden}
table{width:100%%;border-collapse:collapse;font-size:13px}
thead th{background:#0b1120;color:var(--muted);text-align:left;padding:10px 14px;border-bottom:1px solid var(--line);white-space:nowrap}
tbody td{padding:10px 14px;border-bottom:1px solid var(--line);vertical-align:middle}
tr:last-child td{border-bottom:none}
tr.live{background:rgba(250,204,21,.08)}
tr.ok{background:rgba(74,222,128,.07)}
tr.err{background:rgba(248,113,113,.08)}
tr.empty td{text-align:center;color:var(--muted);padding:26px}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px}
.speed{color:#facc15;font-weight:600}
.badge{display:inline-block;padding:2px 9px;border-radius:999px;font-size:11px;font-weight:600}
.badge.running{background:#f59e0b;color:#1a1206}
.badge.done{background:#22c55e;color:#052e16}
.badge.failed{background:#ef4444;color:#fff}
.badge.paused{background:#64748b;color:#f1f5f9}
.badge.unknown{background:#475569;color:#e2e8f0}
.ops{white-space:nowrap}
.btn{display:inline-block;margin-left:6px;padding:4px 10px;border-radius:6px;font-size:12px;text-decoration:none;transition:opacity .15s}
.btn:hover{opacity:.8}
.btn.ok{background:#16a34a;color:#fff}
.btn.warn{background:#d97706;color:#fff}
.btn.danger{background:#dc2626;color:#fff}
footer{margin-top:16px;color:var(--muted);font-size:12px}
@media(max-width:720px){.cards{grid-template-columns:repeat(2,1fr)}.nav a{margin-left:0;margin-right:10px}}
</style></head><body><div class=wrap>
<header><h1>⏬ 多网盘任务中心</h1><div class=nav>
<a href=/test>测试连接</a><a href=/live>实时速度</a><a href=/api/tasks>API 全部任务</a><a href=/api/status>API 状态</a><a href=/api/live>API 实时</a>
</div></header>
%(cards)s
<section id=dl class="panel download">
<h2 style="font-size:15px;margin:0 0 10px">📥 粘贴链接开始下载</h2>
<textarea id=dlUrl rows=2 placeholder="粘贴网盘分享链接或 HTTP 直链（可多行，取第一个）" style="width:100%%;box-sizing:border-box;background:#0b1120;border:1px solid var(--line);color:var(--text);border-radius:8px;padding:8px 10px;font-size:13px"></textarea>
<div style="display:flex;gap:10px;flex-wrap:wrap;margin:10px 0">
<input id=dlPwd placeholder="提取码（可选）" style="flex:1;min-width:120px;background:#0b1120;border:1px solid var(--line);color:var(--text);border-radius:8px;padding:8px 10px">
<input id=dlTo placeholder="目标目录（可选）" style="flex:2;min-width:180px;background:#0b1120;border:1px solid var(--line);color:var(--text);border-radius:8px;padding:8px 10px">
<select id=dlTier style="background:#0b1120;border:1px solid var(--line);color:var(--text);border-radius:8px;padding:8px">
<option value="">档次：自动</option><option value=free>免费</option><option value=vip>会员</option>
</select>
<button id=dlStart style="background:var(--acc);border:0;border-radius:8px;color:#052e16;font-size:13px;font-weight:600;padding:8px 16px;cursor:pointer">开始下载</button>
</div>
<div id=dlMsg style="font-size:13px;margin-top:6px"></div>
</section>
<script>
(function(){
  var btn=document.getElementById('dlStart'); var out=document.getElementById('dlMsg');
  if(!btn||!out){return;}
  btn.addEventListener('click', function(){
    var url=(document.getElementById('dlUrl').value||'').trim().split(/\s+/).find(function(x){return /^https?:\/\//i.test(x);});
    if(!url){ out.textContent='请先粘贴至少一个链接'; out.style.color='#f87171'; return; }
    out.textContent='正在投递给本机下载服务…'; out.style.color='var(--muted)';
    fetch('/api/download', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({
      url:url, pwd:document.getElementById('dlPwd').value.trim(),
      to:document.getElementById('dlTo').value.trim(), tier:document.getElementById('dlTier').value
    })}).then(function(r){return r.json();}).then(function(d){
      if(d.ok){ out.textContent='✅ 已开始（PID '+d.pid+'）。正在跳转实时进度…'; out.style.color='#4ade80';
        setTimeout(function(){ location.href='/live'; }, 600);
      } else { out.textContent='❌ '+(d.error||'未知错误'); out.style.color='#f87171'; }
    }).catch(function(){ out.textContent='❌ 连接本机下载服务失败，请先执行 pan serve'; out.style.color='#f87171'; });
  });
})();
</script>
<div class=panel><table>
<thead><tr><th>任务 ID</th><th>网盘</th><th>当前步骤 / 文件</th><th>实时速度</th><th>平均速度</th><th>状态</th><th>更新时间</th><th>操作</th></tr></thead>
<tbody>%(rows)s</tbody></table></div>
<footer>任务中心 v2：每 2 秒自动刷新，支持暂停 / 继续 / 取消 / 删除 / 重试。</footer>
</div></body></html>""" % {"cards": cards, "rows": rows})


def serve_test_html():
    """独立「测试连接」页：粘贴链接→调用 /api/test→人话结果（不自动刷新，避免打断输入）。"""
    return """<!doctype html><html lang=zh-CN><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>多网盘 · 测试连接</title>
<link rel="manifest" href="/manifest.webmanifest">
<script>if('serviceWorker'in navigator){navigator.serviceWorker.register('/sw.js')}</script>
<style>
:root{--bg:#0f172a;--panel:#1e293b;--line:#334155;--text:#e2e8f0;--muted:#94a3b8;--acc:#38bdf8}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:-apple-system,"PingFang SC","Microsoft YaHei",system-ui,sans-serif}
.wrap{max-width:760px;margin:0 auto;padding:24px 18px 40px}
header{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:18px}
header h1{font-size:20px;margin:0}
.nav a{color:var(--acc);text-decoration:none;font-size:13px;margin-left:12px}
.nav a:hover{text-decoration:underline}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px}
form{display:grid;gap:10px;margin-bottom:6px}
input{background:#0b1120;border:1px solid var(--line);border-radius:8px;color:var(--text);padding:10px 12px;font-size:14px}
button{border:0;border-radius:8px;background:var(--acc);color:#052e16;font-size:14px;font-weight:600;padding:11px;cursor:pointer}
button:hover{opacity:.9}
.row{display:flex;justify-content:space-between;gap:12px;padding:9px 2px;border-bottom:1px solid var(--line);font-size:13px}
.row:last-child{border-bottom:none}
.row .name{white-space:nowrap}
.row .detail{color:var(--muted);text-align:right;word-break:break-all}
.ok{color:#4ade80}.bad{color:#f87171}
.sum{font-size:16px;font-weight:700;padding:10px 2px}
.empty{color:var(--muted);font-size:13px;padding:8px 2px}
</style></head><body><div class=wrap>
<header><h1>🧪 多网盘 · 测试连接</h1><div class=nav>
<a href=/>任务中心</a><a href=/live>实时速度</a>
</div></header>
<div class=panel>
<form id=testForm>
<input id=testUrl type=text placeholder="粘贴网盘分享链接或 HTTP 直链" required>
<input id=testPwd type=text placeholder="提取码（没有可留空）" autocomplete=off>
<button type=submit>开始测试</button>
</form>
<p style="color:var(--muted);font-size:12px;margin:6px 0 0">只做本地静态检查：识别网盘、依赖与配置、目标目录、提取码提示。不会下载文件、不发请求到网盘页面。</p>
<div id=result></div>
</div>
<script>
document.getElementById('testForm').addEventListener('submit', async function (e) {
  e.preventDefault();
  const url = document.getElementById('testUrl').value.trim();
  if (!url) { return; }
  const pwd = document.getElementById('testPwd').value.trim();
  const out = document.getElementById('result');
  out.innerHTML = '<div class=empty>测试中…</div>';
  try {
    const qs = new URLSearchParams({ url: url });
    if (pwd) { qs.append('pwd', pwd); }
    const resp = await fetch('/api/test?' + qs.toString());
    const j = await resp.json();
    let html = '';
    const marks = [];
    (j.checks || []).forEach(function (c) {
      const mark = c.ok ? '✅' : '❌';
      marks.push(c.ok);
      html += '<div class="row"><span class="name ' + (c.ok ? 'ok' : 'bad') + '">' + mark + ' ' + (c.name || '') + '</span><span class="detail">' + (c.detail || '') + '</span></div>';
    });
    const allOk = marks.length > 0 && marks.every(Boolean);
    html = '<div class="sum ' + (allOk ? 'ok' : 'bad') + '">' + (allOk ? '✅ 可以开始下载' : '❌ 当前还不能直接下载') + '</div>' + html;
    out.innerHTML = html;
  } catch (err) {
    out.innerHTML = '<div class="row"><span class="name bad">❌ 通信失败</span><span class="detail">请确认本机服务已运行：python3 scripts/pan.py serve</span></div>';
  }
});
</script>
</div></body></html>"""





def cmd_serve(args):
    try:
        from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    except ImportError:
        print("❌ 当前环境无 http.server")
        return 1
    import threading
    reports_dir = os.path.expanduser(args.reports_dir) if args.reports_dir else ""
    if not reports_dir:
        reports_dir = str(Path((load_config().get("http") or {}).get("report_dir") or default_root(load_config())))
    host, port = args.host, int(args.port)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _json(self, obj):
            data = json.dumps(obj, ensure_ascii=False, indent=2).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _html(self, text):
            data = text.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _raw(self, data, content_type):
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_POST(self):
            length = int(self.headers.get("Content-Length", 0) or 0)
            raw = b""
            if length:
                raw = self.rfile.read(length)
            try:
                body = json.loads(raw.decode("utf-8") or "{}")
            except (ValueError, UnicodeDecodeError):
                body = {}
            if self.path.startswith("/api/download"):
                url = (body.get("url") or "").strip()
                if not url:
                    self._json({"ok": False, "error": "缺少 url"})
                    return
                pid, err = _spawn_download_task(
                    url, pwd=(body.get("pwd") or ""), to=(body.get("to") or ""),
                    engine=(body.get("engine") or ""), tier=(body.get("tier") or ""),
                    path=(body.get("path") or ""))
                if err:
                    self._json({"ok": False, "error": err})
                else:
                    self._json({"ok": True, "pid": pid, "note": "已后台启动下载，可刷新任务中心查看进度",
                                "live_url": "http://%s:%d/live" % (host, port),
                                "home_url": "http://%s:%d/" % (host, port)})
            elif self.path.startswith("/api/task/action"):
                q = dict(parse_qs(self.path.split("?", 1)[1])) if "?" in self.path else {}
                action = (body.get("action") or q.get("action") or [""])
                task = (body.get("task") or q.get("task") or [""])
                action = action[0] if isinstance(action, list) else action
                task = task[0] if isinstance(task, list) else task
                if action not in ("pause", "resume", "delete", "retry"):
                    self._json({"ok": False, "error": "未知操作"})
                elif not task:
                    self._json({"ok": False, "error": "缺少 task"})
                else:
                    ok, msg = _apply_task_action(reports_dir, task, action)
                    self._json({"ok": ok, "action": action, "task": task, "message": msg})
            else:
                self.send_error(404, "Not Found")

        def do_GET(self):
            if self.path in ("/manifest.webmanifest", "/manifest.json"):
                self._raw(pwa_manifest_json().encode("utf-8"), "application/manifest+json; charset=utf-8")
            elif self.path == "/sw.js":
                self._raw(pwa_service_worker_js().encode("utf-8"), "application/javascript; charset=utf-8")
            elif self.path.startswith("/icons/icon-") and self.path.endswith(".png"):
                size = int("".join(ch for ch in self.path.split("-")[-1].split(".")[0] if ch.isdigit()) or 192)
                self._raw(pwa_icon_png(size), "image/png")
            elif self.path.startswith("/api/reports"):
                self._json({"reports": serve_reports_json(reports_dir)})
            elif self.path.startswith("/api/test"):
                q = dict(parse_qs(self.path.split("?", 1)[1])) if "?" in self.path else {}
                url = (q.get("url") or [""])[0]
                if not url:
                    self._json({"ok": False, "error": "缺少 url 参数"})
                else:
                    rel = _probe_link_checks(load_config(), url,
                                             pwd=(q.get("pwd") or [""])[0],
                                             engine=(q.get("engine") or [""])[0],
                                             tier=(q.get("tier") or [""])[0],
                                             path=(q.get("path") or [""])[0])
                    self._json(rel)
            elif self.path.startswith("/api/tasks"):
                st = ""
                for part in self.path.split("?")[-1].split("&"):
                    if part.startswith("state="):
                        st = part.split("=", 1)[1]
                self._json({"tasks": serve_unified_tasks(reports_dir, limit=100, state=st or None)})
            elif self.path.startswith("/api/status"):
                self._json({"ok": True, "reports_dir": reports_dir,
                            "reports": len(serve_reports_json(reports_dir)),
                            "live": len(serve_live_json(reports_dir)),
                            "tasks": len(serve_unified_tasks(reports_dir))})
            elif self.path.startswith("/api/live"):
                self._json({"live": serve_live_json(reports_dir)})
            elif self.path.startswith("/api/task/action"):
                q = dict(parse_qs(self.path.split("?", 1)[1])) if "?" in self.path else {}
                action = (q.get("action") or [""])[0]
                task = (q.get("task") or [""])[0]
                if action not in ("pause", "resume", "delete", "retry"):
                    self._json({"ok": False, "error": "未知操作"})
                elif not task:
                    self._json({"ok": False, "error": "缺少 task 参数"})
                else:
                    ok, msg = _apply_task_action(reports_dir, task, action)
                    self._json({"ok": ok, "action": action, "task": task, "message": msg})
            elif self.path.startswith("/api/tasks") or self.path.startswith("/api/task-json"):
                st = ""
                for part in self.path.split("?")[-1].split("&"):
                    if part.startswith("state="):
                        st = part.split("=", 1)[1]
                self._json({"tasks": serve_unified_tasks(reports_dir, limit=100, state=st or None)})
            elif self.path in ("/live", "/live.html"):
                live = serve_live_json(reports_dir)
                items_json = "[]"
                if not live:
                    body = '<div class="empty">暂无进行中的实时下载<br><span>下载时执行 get --live 生成 下载速度.live.json</span></div>'
                else:
                    shown = []
                    for item in live[:8]:
                        st = item.get("state", "")
                        badge = st if st else "unknown"
                        sp = item.get("speed_kbps")
                        av = item.get("avg_speed_kbps")
                        sps = ("%.1f" % float(sp)) if sp not in (None, "") else "-"
                        avs = ("%.1f" % float(av)) if av not in (None, "") else "-"
                        by = int(item.get("bytes_done") or 0)
                        if by >= 1024 * 1024:
                            btxt = "%.2f MB" % (by / 1048576.0)
                        else:
                            btxt = "%.2f KB" % (by / 1024.0)
                        eta = item.get("eta_seconds")
                        ets = "-"
                        if eta is not None:
                            eta = float(eta)
                            if eta <= 0:
                                ets = "即将完成"
                            elif eta < 60:
                                ets = "约 %d 秒" % int(eta)
                            elif eta < 3600:
                                ets = "约 %d 分 %d 秒" % (int(eta // 60), int(eta % 60))
                            else:
                                ets = "约 %d 小时 %d 分" % (int(eta // 3600), int((eta % 3600) // 60))
                        shown.append({
                            "name": item.get("drive_name", ""), "step": item.get("current_step", ""),
                            "speed": sps, "avg": avs, "done": btxt, "state": badge,
                            "eta": ets, "history": item.get("history", [])[:300],
                            "total": item.get("total_bytes", 0), "percent": item.get("percent"),
                        })
                        rows.append(
                            "<tr><td>%s</td><td>%s</td><td><span class=speed>%s KB/s</span></td>"
                            "<td>%s KB/s</td><td>%s</td><td>%s</td><td><span class='badge %s'>%s</span></td>"
                            "<td class=mono>%s</td></tr>" % (
                                item.get("drive_name", ""), item.get("current_step", ""),
                                sps, avs, btxt, ets, badge, badge, item.get("updated", "")))
                    items_json = json.dumps(shown, ensure_ascii=False)
                    table = ("<thead><tr><th>网盘</th><th>当前文件 / 步骤</th><th>实时速度</th>"
                             "<th>平均速度</th><th>已下载</th><th>剩余时间</th><th>状态</th><th>更新时间</th></tr></thead>"
                             "<tbody>%s</tbody>" % "".join(rows))
                    body = table + '<div id="charts"></div>'
                self._html(serve_live_page_html(body, items_json=items_json))
            elif self.path in ("/test", "/test.html"):
                self._html(serve_test_html())
            elif self.path in ("/", "/index.html"):
                self._html(serve_home_html(serve_unified_tasks(reports_dir)))
            else:
                self.send_error(404, "Not Found")

    try:
        httpd = ThreadingHTTPServer((host, port), Handler)
    except OSError as exc:
        print("❌ 启动失败 %s:%s：%s" % (host, port, exc))
        return 1
    print("只读状态页：http://%s:%s/（仅本机访问；不读取任何凭据）" % (host, port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


# ---------------------------------------------------------------- 子命令





def cmd_doctor(args):
    cfg = load_config()
    backend_names = {
        "macos": "macOS Keychain",
        "windows": "Windows Credential Manager",
        "secret-tool": "libsecret / secret-tool",
        "unsupported": "不可用（拒绝保存明文）",
    }
    backend = credential_backend()
    checks = [
        ("python3", sys.version.split()[0]),
        ("系统", "%s / %s" % (platform.system() or "unknown", backend_names.get(backend, backend))),
        ("curl", shutil.which("curl") or "缺失"),
        ("aria2c", find_engine_binary("aria2", cfg) or "未安装（可选）"),
        ("alist", find_engine_binary("alist", cfg) or "未安装（多数网盘挂载需要）"),
        ("BaiduPCS-Go", find_engine_binary("baidupcs", cfg) or "未安装（百度分享需要）"),
        ("quark-cli", find_engine_binary("quarkcli", cfg) or "未安装（夸克分享需要）"),
        ("rclone", find_engine_binary("rclone", cfg) or "未安装（可选，目录递归需要）"),
        ("ssh", find_engine_binary("ssh", cfg) or "未安装（远程执行/部署需要）"),
        ("scp", find_engine_binary("scp", cfg) or "未安装（远程部署需要）"),
        ("webdav", ((cfg.get("engines") or {}).get("webdav_url") or "未配置（坚果云 WebDAV 需要）")),
        ("系统凭据库", backend_names.get(backend, backend) if credential_available() else "不可用（拒绝保存明文）"),
        ("配置文件", str(CONFIG_PATH) if CONFIG_PATH.exists() else "未创建（运行 init）"),
        ("默认下载目录", str(default_root(cfg))),
        ("远程设备", "%d 个已登记" % len(cfg.get("remotes") or {})),
    ]
    hints = env_install_hints(cfg)
    if args.json:
        print(json.dumps({"checks": checks, "config": mask_value("config", cfg), "hints": hints},
                          ensure_ascii=False, indent=2))
        return 0
    print("pan-downloader doctor")
    for name, value in checks:
        print("  %-14s %s" % (name, value))
    if hints:
        print("建议命令：")
        for h in hints:
            print("  - %s" % h)
    return 0


def cmd_init(args):
    if getattr(args, "wizard", False):
        return cmd_init_wizard(args)
    cfg = load_config()
    if CONFIG_PATH.exists() and not args.force:
        print("已存在，未变更：%s" % CONFIG_PATH)
        return 0
    path = save_config(cfg)
    print("已创建：%s（权限 600；账号密码另存系统凭据库，不写入此文件）" % path)
    return 0


def cmd_show(args):
    cfg = load_config()
    print(json.dumps(mask_value("config", cfg), ensure_ascii=False, indent=2))
    return 0


def cmd_detect(args):
    key, spec = detect_drive(args.url)
    if not key:
        print("❌ 无法识别")
        return 1
    print(json.dumps({"drive": key, "name": spec["name"], "engine": spec["engine"],
                      "reference": spec.get("reference", "")}, ensure_ascii=False, indent=2))
    return 0



def _probe_link_checks(cfg, url, pwd="", engine="", tier="", path=""):
    """只读测试一条下载链接：识别、依赖/配置、目标目录、提取码；不下载不写盘。"""
    key, spec = detect_drive(url, cfg)
    if not key:
        return {"ok": False, "drive": "", "drive_name": "未知", "engine": "",
                "checks": [{"name": "识别", "ok": False, "detail": "无法识别该链接"}],
                "missing": [], "warnings": ["这不是默认支持的网盘域名，也不是 http(s) 直链"]}
    plan = build_plan(url, pwd=pwd, cfg=cfg, engine=engine or None, tier=tier or None, path=path or None)
    checks = []
    checks.append({"name": "识别", "ok": True, "detail": "%s（%s）" % (spec["name"], key)})
    missing = list(plan.get("missing") or [])
    checks.append({"name": "依赖与配置", "ok": not missing,
                   "detail": "；".join(missing) if missing else "依赖与配置齐备"})
    warnings = list(plan.get("warnings") or [])
    if warnings:
        checks.append({"name": "注意", "ok": True, "detail": "；".join(warnings[:5])})
    target = Path(plan.get("target") or ".")
    if target.exists():
        target_ok = os.access(str(target), os.W_OK)
        detail = "目录存在，可写" if target_ok else "目录存在但当前用户无写权限"
    else:
        parent = target
        while parent and not parent.exists():
            parent = parent.parent
        target_ok = bool(parent) and os.access(str(parent), os.W_OK)
        detail = "目录不存在，父目录可写（将自动创建）" if target_ok else "父目录不可写，请更换下载目录"
    checks.append({"name": "目标目录", "ok": target_ok, "detail": detail})
    if pwd:
        checks.append({"name": "提取码", "ok": True, "detail": "已提供"})
    return {"ok": (not missing) and target_ok, "drive": key, "drive_name": spec["name"],
            "engine": plan.get("engine", ""), "target": str(target),
            "checks": checks, "missing": missing, "warnings": warnings}


def cmd_test(args):
    cfg = load_config()
    res = _probe_link_checks(cfg, args.url, pwd=args.pwd or "", engine=args.engine or "",
                             tier=args.tier or "", path=args.path or "")
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0
    print("链接测试：%s" % args.url)
    print("  识别：%s（%s）" % (res["drive_name"], res["drive"]))
    for c in res["checks"]:
        mark = "✅" if c["ok"] else "❌"
        print("  %s %s：%s" % (mark, c["name"], c["detail"]))
    if res["ok"]:
        print("✅ 可以开始下载（目录：%s）" % res["target"])
        return 0
    print("❌ 当前配置还不能直接下载，请先处理标记 ❌ 的项。")
    return 1


def _read_stdin_secret():
    value = sys.stdin.read().rstrip("\r\n")
    if not value:
        raise ValueError("stdin 没有收到密码")
    return value


def _save_engine_secret(eng, ref_key, legacy_key, value, secret_name):
    if not value:
        return True
    try:
        eng[ref_key] = keychain_store(secret_name, value)
        eng.pop(legacy_key, None)
    except (OSError, ValueError, RuntimeError) as exc:
        print("❌ 凭据未保存：%s" % exc)
        return False
    return True


def cmd_secret_set(args):
    try:
        value = _read_stdin_secret() if args.stdin else getpass.getpass("凭据（不回显）：")
        ref = keychain_store(args.name, value)
    except (OSError, EOFError, KeyboardInterrupt, ValueError, RuntimeError) as exc:
        print("❌ 凭据保存失败：%s" % exc)
        return 1
    print("✅ 已存入系统凭据库：%s（明文不写入 config.json）" % ref)
    return 0


def cmd_secret_check(args):
    names = [args.name] if args.name else sorted(configured_secret_refs(load_config()))
    rows = []
    for name in names:
        rows.append({"name": name, "present": bool(keychain_get(name))})
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        for row in rows:
            print("%s  %s" % ("✅" if row["present"] else "❌", row["name"]))
    return 0 if all(row["present"] for row in rows) else 1


def cmd_secret_delete(args):
    if keychain_delete(args.name):
        print("✅ 已从系统凭据库删除：%s" % args.name)
        return 0
    print("❌ 未找到或删除失败：%s" % args.name)
    return 1


def cmd_secret_list(args):
    cfg = load_config()
    refs = configured_secret_refs(cfg)
    rows = [{"name": name, "ref": ref, "present": bool(keychain_get(keychain_name(ref)))}
            for name, ref in sorted(refs.items())]
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        if not rows:
            print("未配置凭据引用。保存方式：pan secret set engine.webdav --stdin")
        for row in rows:
            print("%s  %-18s %s" % ("✅" if row["present"] else "❌", row["name"], row["ref"]))
    return 0


def cmd_secret_migrate(args):
    cfg = load_config()
    migrated, errors = migrate_plaintext_secrets(cfg)
    if errors:
        for item in errors:
            print("❌ %s" % item)
        return 1
    if migrated:
        path = save_config(cfg)
        print("✅ 已迁移 %d 项到系统凭据库：%s" % (len(migrated), path))
    else:
        print("未发现需要迁移的明文凭据")
    return 0


def cmd_set(args):
    cfg = load_config()
    if args.root is not None:
        cfg["download_root"] = args.root
    if args.tier is not None:
        cfg["tier"] = args.tier
    if args.engine is not None and args.engine_name:
        cfg.setdefault("engines", {})[args.engine_name] = args.engine
    if getattr(args, "auto_classify", "") in ("on", "off"):
        cfg.setdefault("smart", {})["auto_classify"] = (args.auto_classify == "on")
    eng = cfg.setdefault("engines", {})
    if args.alist_url:
        eng["alist_url"] = args.alist_url
    if args.alist_user:
        eng["alist_user"] = args.alist_user
    if args.rclone_remote:
        eng["rclone_remote"] = args.rclone_remote
    if args.webdav_url:
        eng["webdav_url"] = args.webdav_url
    if args.webdav_user:
        eng["webdav_user"] = args.webdav_user

    secret_values = (
        ("alist_password_ref", "alist_password", "engine.alist", args.alist_password, args.alist_password_stdin),
        ("webdav_password_ref", "webdav_password", "engine.webdav", args.webdav_password, args.webdav_password_stdin),
    )
    for ref_key, legacy_key, secret_name, legacy_value, from_stdin in secret_values:
        if legacy_value and from_stdin:
            print("❌ 同一凭据不能同时使用命令行和 --stdin")
            return 1
        try:
            value = _read_stdin_secret() if from_stdin else (legacy_value or "")
        except ValueError as exc:
            print("❌ %s" % exc)
            return 1
        if not _save_engine_secret(eng, ref_key, legacy_key, value, secret_name):
            return 1
        if legacy_value:
            print("⚠️ 为兼容旧命令已改存系统凭据库；以后请用 --stdin 或 secret set，避免命令行暴露")
    path = save_config(cfg)
    print("已保存：%s" % path)
    return 0


def cmd_set_drive(args):
    cfg = load_config()
    drives = cfg.setdefault("drives", {})
    entry = drives.setdefault(args.drive, {})
    if args.tier:
        entry["tier"] = args.tier
    if args.account_tier:
        entry["account_tier"] = args.account_tier
    if args.tier_detector:
        entry["tier_detector"] = args.tier_detector
    if args.cookie_file:
        entry["cookie_file"] = args.cookie_file
    if args.engine_command:
        entry["engine_command"] = args.engine_command
    if args.save_path:
        entry["save_path"] = args.save_path
    if args.credential_ref:
        try:
            entry["credential_ref"] = normalize_secret_ref(args.credential_ref)
        except ValueError as exc:
            print("❌ %s" % exc)
            return 1
    if args.credential_stdin:
        try:
            entry["credential_ref"] = keychain_store("drive." + args.drive, _read_stdin_secret())
        except (OSError, EOFError, ValueError, RuntimeError) as exc:
            print("❌ 凭据未保存：%s" % exc)
            return 1
    path = save_config(cfg)
    print("已保存 %s 配置：%s" % (args.drive, path))
    return 0


def cmd_login(args):
    drive_key, spec = detect_drive(args.drive) if "://" in args.drive else (args.drive, all_drives(load_config()).get(args.drive, {}))
    if not spec:
        print("❌ 未找到网盘：%s（可用 detect 或 references/06-扩展新网盘.md 自定义）" % drive_key)
        return 1
    ref = SKILL_DIR / (spec.get("reference") or "references/00-使用说明.md")
    print("按以下文件完成一次登录（凭据只存本机系统凭据库/客户端配置）：%s" % ref)
    print("安全提示：账号、密码、Cookie、Token 不要发到聊天里；在本机终端用 pan secret set 保存。")
    if getattr(args, "open", False):
        import webbrowser as _wb
        try:
            opened = _wb.open(ref.resolve().as_uri())
        except Exception as _wexc:
            opened = False
            print("⚠️ 自动打开失败：%s（请手动打开上面路径）" % _wexc)
        if opened:
            print("已尝试用默认程序打开教程，请按文档完成授权后回到终端继续。")
    if ref.exists():
        text = ref.read_text(encoding="utf-8").splitlines()
        for line in text[:80]:
            print(line)
    return 0


def _remote_public(entry):
    return {
        "name": entry.get("name", ""),
        "kind": entry.get("kind", ""),
        "host": entry.get("host", ""),
        "port": entry.get("port", ""),
        "user": entry.get("user", ""),
        "root": entry.get("root", ""),
        "remote_name": entry.get("remote_name", ""),
        "python": entry.get("python", ""),
        "deploy_dir": entry.get("deploy_dir", ""),
        "web_port": entry.get("web_port", ""),
        "web_host": entry.get("web_host", ""),
        "credential_ref": entry.get("credential_ref", ""),
        "description": entry.get("description", ""),
    }


def cmd_remote_add(args):
    cfg = load_config()
    remotes = cfg.setdefault("remotes", {})
    name = str(args.name or "").strip()
    if not re.fullmatch(r"[A-Za-z0-9._@-]{1,80}", name):
        print("❌ remote 名称只允许字母、数字、点、下划线、@ 和连字符")
        return 1
    entry = remotes.setdefault(name, {})
    if args.kind:
        entry["kind"] = normalize_remote_kind(args.kind) or args.kind
    for attr, key in (
        ("host", "host"), ("port", "port"), ("user", "user"), ("root", "root"),
        ("remote_name", "remote_name"), ("python", "python"), ("deploy_dir", "deploy_dir"),
        ("web_port", "web_port"), ("web_host", "web_host"),
        ("description", "description"),
    ):
        value = getattr(args, attr, None)
        if value is not None:
            entry[key] = value
    if args.credential_ref:
        try:
            entry["credential_ref"] = normalize_secret_ref(args.credential_ref)
        except ValueError as exc:
            print("❌ %s" % exc)
            return 1
    if args.credential_stdin:
        try:
            entry["credential_ref"] = credential_store("remote." + name, _read_stdin_secret())
        except (OSError, EOFError, ValueError, RuntimeError) as exc:
            print("❌ 凭据未保存：%s" % exc)
            return 1
    profile, missing = validate_remote_profile(name, entry)
    if missing:
        print("⚠️ 已保存，但配置不完整：%s" % "、".join(missing))
    path = save_config(cfg)
    print("已保存 remote.%s：%s" % (name, path))
    return 0


def cmd_remote_list(args):
    cfg = load_config()
    rows = []
    for name, entry in sorted((cfg.get("remotes") or {}).items()):
        profile, missing = validate_remote_profile(name, entry)
        row = _remote_public(profile)
        row["ready"] = not missing
        row["missing"] = missing
        rows.append(row)
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    elif not rows:
        print("尚未登记远程设备。示例：pan remote add nas --kind ssh --host 192.168.1.10 --user lis --root /volume1")
    else:
        for row in rows:
            print("%s %-18s %-8s %s" % ("✅" if row["ready"] else "⚠️", row["name"], row["kind"], row["host"] or row["remote_name"] or row["root"]))
    return 0


def cmd_remote_remove(args):
    cfg = load_config()
    remotes = cfg.setdefault("remotes", {})
    if args.name not in remotes:
        print("❌ 未找到 remote：%s" % args.name)
        return 1
    remotes.pop(args.name, None)
    path = save_config(cfg)
    print("✅ 已移除 remote.%s：%s" % (args.name, path))
    return 0


def _remote_checks(profile):
    checks = []
    kind = profile.get("kind")
    if kind == "ssh":
        checks.append(("ssh", find_engine_binary("ssh", {}) or "未安装（远程执行需要）"))
        checks.append(("scp", find_engine_binary("scp", {}) or "未安装（远程部署需要）"))
        checks.append(("认证方式", "SSH key/agent（BatchMode=yes，禁止把远程密码放进命令行）"))
    elif kind == "mount":
        root = Path(os.path.expanduser(str(profile.get("root") or "")))
        checks.append(("挂载路径", "%s（%s）" % (root, "可写" if root.exists() and os.access(str(root), os.W_OK) else "不可用或未挂载")))
    else:
        checks.append(("rclone", find_engine_binary("rclone", {}) or "未安装（远程落地需要）"))
        checks.append(("rclone remote", str(profile.get("remote_name") or "未配置")))
    return checks


def cmd_remote_check(args):
    cfg = load_config()
    entry = remote_entry(cfg, args.name)
    if entry is None:
        print("❌ 未找到 remote：%s" % args.name)
        return 1
    profile, missing = validate_remote_profile(args.name, entry)
    if missing:
        if args.json:
            print(json.dumps({"name": args.name, "ready": False, "missing": missing}, ensure_ascii=False, indent=2))
        else:
            print("❌ remote.%s 配置不完整：%s" % (args.name, "、".join(missing)))
        return 1
    checks = _remote_checks(profile)
    probe = ""
    if getattr(args, "probe", False):
        if profile["kind"] == "ssh":
            cmd = "python3 --version && mkdir -p %s" % shlex.quote(str(profile.get("root") or ""))
            try:
                proc = subprocess.run(remote_ssh_argv(profile, cmd), capture_output=True, text=True, timeout=20)
                probe = "成功：%s" % ((proc.stdout or proc.stderr or "").strip().splitlines()[-1] if (proc.stdout or proc.stderr) else "远程响应正常")
                if proc.returncode != 0:
                    probe = "失败：SSH/远程 Python 不可用（exit=%s）" % proc.returncode
            except (OSError, subprocess.TimeoutExpired) as exc:
                probe = "失败：%s" % exc
        elif profile["kind"] != "mount":
            destination = remote_rclone_destination(profile, "")
            try:
                proc = subprocess.run(["rclone", "lsd", destination], capture_output=True, text=True, timeout=20)
                probe = "成功：%s" % ((proc.stdout or proc.stderr or "").strip().splitlines()[-1] if (proc.stdout or proc.stderr) else "远端响应正常")
                if proc.returncode != 0:
                    probe = "失败：rclone 远端不可用（exit=%s）" % proc.returncode
            except (OSError, subprocess.TimeoutExpired) as exc:
                probe = "失败：%s" % exc
    result = {"name": args.name, "kind": profile.get("kind"), "ready": True, "checks": checks, "probe": probe}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("remote.%s（%s）" % (args.name, profile.get("kind")))
        for name, value in checks:
            print("  %-14s %s" % (name, value))
        if probe:
            print("  探测            %s" % probe)
    return 0 if not probe.startswith("失败") else 1


def cmd_remote_deploy(args):
    cfg = load_config()
    entry = remote_entry(cfg, args.name)
    if entry is None:
        print("❌ 未找到 remote：%s" % args.name)
        return 1
    profile, missing = validate_remote_profile(args.name, entry)
    if missing:
        print("❌ remote.%s 配置不完整：%s" % (args.name, "、".join(missing)))
        return 1
    profile["name"] = args.name
    archive = None
    try:
        archive = create_remote_deploy_archive()
        plan = build_remote_deploy_plan(
            profile, archive,
            web_port=getattr(args, "web_port", 0) or 0,
            web_host=getattr(args, "web_host", None),
            web_reports_dir=getattr(args, "web_reports_dir", None) or "",
        )
        if not plan.get("ok"):
            print("❌ %s" % plan.get("error"))
            return 1
        if args.dry_run:
            run_plan(plan, dry_run=True)
            print("DRY-RUN 完成：未上传部署包")
            return 0
        if args.json:
            print(json.dumps(public_plan(plan), ensure_ascii=False, indent=2))
            return 0
        rc = run_plan(plan, dry_run=False)
        if rc == 0:
            print("✅ 已部署到 remote.%s：%s" % (args.name, plan["target"]))
        return rc
    finally:
        if archive:
            try:
                archive.unlink()
            except OSError:
                pass


def cmd_remote_web(args):
    cfg = load_config()
    entry = remote_entry(cfg, args.name)
    if entry is None:
        print("❌ 未找到 remote：%s" % args.name)
        return 1
    profile, missing = validate_remote_profile(args.name, entry)
    if missing:
        print("❌ remote.%s 配置不完整：%s" % (args.name, "、".join(missing)))
        return 1
    profile["name"] = args.name
    info = remote_web_access(profile, port=getattr(args, "port", 0) or 0,
                             web_host=getattr(args, "host", None) or "",
                             local_port=getattr(args, "local_port", 0) or 0)
    if getattr(args, "json", False):
        print(json.dumps({"name": args.name,
                          "kind": profile.get("kind", ""),
                          "web_port": info["web_port"],
                          "web_host": info["web_host"],
                          "url": info["url"],
                          "tunnel": info["tunnel"],
                          "local_url": info["local_url"],
                          "guide": info["guide"]}, ensure_ascii=False, indent=2))
    else:
        print("remote.%s：%s://%s（root=%s）" % (args.name, profile.get("kind", "ssh"), profile.get("host", ""), profile.get("root", "")))
        print("  Web 控制页：%s" % info["url"])
        if info["tunnel"]:
            print("  外网/本机访问（反向隧道）：")
            print("    %s" % info["tunnel"])
            print("  本地打开：%s（保持隧道终端运行）" % info["local_url"])
        else:
            print("  提示：remote add 时登记 host/user 后可生成 SSH 反向隧道命令。")
    return 0


def _plan_dirs(plan):
    if plan.get("remote_kind") == "ssh-execute":
        return []
    path = plan.get("staging") or plan.get("target")
    if path:
        return [Path(str(path))]
    return []


def cmd_remote_get(args):
    cfg = load_config()
    name = getattr(args, "name", None) or getattr(args, "remote", None)
    entry = remote_entry(cfg, name)
    if entry is None:
        print("❌ 未找到 remote：%s" % name)
        return 1
    profile, missing = validate_remote_profile(name, entry)
    if missing:
        print("❌ remote.%s 配置不完整：%s" % (name, "、".join(missing)))
        return 1
    profile["name"] = name
    if getattr(args, "live", False):
        profile["live"] = True
    plan = build_remote_plan(profile, args.url, pwd=args.pwd or "", to=getattr(args, "to", None),
                             path=getattr(args, "path", None), tier=getattr(args, "tier", None),
                             engine=getattr(args, "engine", None), cfg=cfg)
    if not plan.get("ok"):
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "error": plan.get("error", ""), "missing": plan.get("missing", [])}, ensure_ascii=False, indent=2))
        else:
            print("❌ %s" % plan.get("error"))
        return 1
    if getattr(args, "json", False):
        print(json.dumps(public_plan(plan), ensure_ascii=False, indent=2))
    else:
        print("远程：%s｜模式：%s｜引擎：%s｜目标：%s" % (name, plan.get("remote_kind", ""), plan.get("engine", ""), plan.get("target", "")))
        for step in plan.get("steps", []):
            print("  - %s" % step.get("note", ""))
        for warn in plan.get("warnings", []):
            print("  ⚠️ %s" % warn)
        if plan.get("missing"):
            print("缺少依赖：")
            for item in plan["missing"]:
                print("  - %s" % item)
    if plan.get("missing") and not args.dry_run and not getattr(args, "force", False):
        return 2
    if args.dry_run:
        if not getattr(args, "json", False):
            run_plan(plan, dry_run=True)
            print("DRY-RUN 完成：未执行远程操作")
        return 0
    for directory in _plan_dirs(plan):
        directory.mkdir(parents=True, exist_ok=True)
    log_line("REMOTE name=%s kind=%s engine=%s target=%s url=%s" % (name, plan.get("remote_kind", ""), plan.get("engine", ""), plan.get("target", ""), args.url))
    rc = run_plan(plan, timeout=cfg.get("http", {}).get("timeout", 0), dry_run=False)
    if rc == 0:
        print("✅ 远程下载完成：%s" % plan.get("target", ""))
    return rc



def _wait_schedule(at, cfg=None, dry_run=False):
    """定时/低峰骨架：按 HH:MM 计算到点等待秒数并阻塞等待；返回是否真的等待过。
    显式命令级 --at 优先；未指定则回退配置 http.schedule_at；dry_run/JSON 不等待。"""
    at = (at or "").strip()
    if not at and cfg:
        at = ((cfg.get("http") or {}).get("schedule_at") or "").strip()
    if not at or dry_run:
        return 0
    try:
        hh, mm = (at.split(":", 1) + [""])[:2]
        hh = hh.strip()
        mm = (mm or "").strip()
        if not (hh.isdigit() and mm.isdigit()):
            return 0
        target = datetime.now().replace(hour=int(hh), minute=int(mm), second=0, microsecond=0)
    except (ValueError, TypeError):
        return 0
    now = datetime.now()
    if target <= now:
        return 0
    seconds = int((target - now).total_seconds())
    print("⏳ 已排到 %02d:%02d 开始，当前 %s；%d 秒后自动下载（可直接关掉窗口？不行，需保持终端或后台运行）。" % (
        target.hour, target.minute, now.strftime("%H:%M"), seconds))
    try:
        time.sleep(seconds)
    except KeyboardInterrupt:
        return 0
    return seconds



def cmd_get(args):
    if getattr(args, "remote", None):
        return cmd_remote_get(args)
    cfg = load_config()
    plan = build_plan(args.url, pwd=args.pwd or "", to=args.to, cfg=cfg,
                      engine=args.engine, tier=args.tier, path=args.path,
                      classify=getattr(args, "classify", None))
    if not plan.get("ok"):
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "error": plan.get("error", "")}, ensure_ascii=False, indent=2))
        else:
            print("❌ %s" % plan.get("error"))
        return 1
    if getattr(args, "json", False):
        print(json.dumps(public_plan(plan), ensure_ascii=False, indent=2))
    else:
        print("网盘：%s｜引擎：%s｜账号：%s｜目录：%s" % (plan["drive_name"], plan["engine"], plan["tier"], plan["target"]))
        for step in plan["steps"]:
            print("  - %s" % step.get("note", ""))
        for warn in plan.get("warnings", []):
            print("  ⚠️ %s" % warn)
        if plan["missing"]:
            print("缺少依赖：")
            for item in plan["missing"]:
                print("  - %s" % item)
            print("安装/配置说明：%s" % plan["reference"])
    # 预演本身不执行外部命令，缺依赖也先把计划完整展示出来；实际下载才拦截。
    if plan["missing"] and not args.dry_run and not args.force:
        return 2
    if not args.dry_run and not getattr(args, "json", False):
        _wait_schedule(getattr(args, "at", ""), cfg, dry_run=False)
    if args.dry_run:
        if not getattr(args, "json", False):
            Path(plan["target"]).mkdir(parents=True, exist_ok=True)
            run_plan(plan, timeout=cfg.get("http", {}).get("timeout", 0), dry_run=True)
            print("DRY-RUN 完成：未执行实际下载（去掉 --dry-run 执行）")
        return 0
    Path(plan["target"]).mkdir(parents=True, exist_ok=True)
    log_line("TASK drive=%s engine=%s tier=%s target=%s url=%s" % (plan["drive"], plan["engine"], plan["tier"], plan["target"], args.url))
    tc = TaskControl(cfg, plan, url=args.url, args={
        "url": args.url, "to": args.to or "", "engine": args.engine or "",
        "tier": args.tier or plan.get("tier", ""), "path": getattr(args, "path", "") or "",
        "pwd": args.pwd or "",
    })
    tc.register()
    wish_live = bool(getattr(args, "live", False)) or bool((cfg.get("http") or {}).get("live_status", False))
    live = None
    if wish_live:
        try:
            interval = float((cfg.get("http") or {}).get("live_interval", 1.0))
        except (TypeError, ValueError):
            interval = 1.0
        if plan.get("engine") == "http" and is_http_url(args.url):
            plan["total_bytes"] = probe_http_total_bytes(args.url, cfg)
        live = LiveMonitor(cfg, plan, url=args.url, interval=interval)
        live.start()
    rc = 1
    try:
        split = resolve_split_count(cfg, args)
        if split and split > 1 and plan.get("engine") == "http" and is_http_url(args.url):
            target_file = Path(plan["target"]) / filename_from_url(args.url)
            started = datetime.now()
            _rc, _results, _note = run_curl_split(args.url, target_file, split, cfg, emit_events=bool(getattr(args, "events", False)), live=live, task_control=tc)
            if _rc is not None:
                finished = datetime.now()
                report_path = write_download_report(cfg, plan, _results, started, finished, ok=(_rc == 0), url=args.url)
                if report_path:
                    print("报告：%s" % report_path)
                if _rc == 0:
                    print("✅ %s" % _note)
                    hook_msg = run_completion_hook(cfg, plan, report_path, url=args.url)
                    if hook_msg:
                        print("完成钩子：%s" % hook_msg)
                else:
                    print("❌ %s" % _note)
                rc = _rc
                if live is not None:
                    live.stop(ok=(rc == 0))
                tc.finish(ok=(rc == 0), rc=rc)
                return rc
        started = datetime.now()
        emit_events = bool(getattr(args, "events", False))
        rc, results = run_plan_detailed(plan, timeout=cfg.get("http", {}).get("timeout", 0), dry_run=False, emit_events=emit_events, live=live, task_control=tc)
        finished = datetime.now()
        report_path = write_download_report(cfg, plan, results, started, finished, ok=(rc == 0), url=args.url)
        if report_path:
            print("报告：%s" % report_path)
        if rc == 0:
            print("✅ 下载完成：%s" % plan["target"])
            hook_msg = run_completion_hook(cfg, plan, report_path, url=args.url)
            if hook_msg:
                print("完成钩子：%s" % hook_msg)
        return rc
    finally:
        if live is not None:
            live.stop(ok=(rc == 0))
        tc.finish(ok=(rc == 0), rc=rc)


def _task_reports_dir(args=None):
    cfg = load_config()
    if getattr(args, "reports_dir", None):
        return os.path.expanduser(args.reports_dir)
    http = cfg.get("http") or {}
    if http.get("live_dir"):
        return str(Path(http["live_dir"]).expanduser())
    if http.get("report_dir"):
        return str(Path(http["report_dir"]).expanduser())
    return str(default_root(cfg))


def cmd_task(args):
    """pan task list|show|pause|resume|delete|retry <id> — 任务控制命令行入口。"""
    reports_dir = _task_reports_dir(args)
    sub = getattr(args, "task_cmd", "")

    def _json_or_text(obj, text_lines):
        if getattr(args, "json", False):
            print(json.dumps(obj, ensure_ascii=False, indent=2))
        else:
            print("\n".join(text_lines))

    if sub == "list":
        tasks = serve_unified_tasks(reports_dir, limit=200, state=getattr(args, "state", None) or None)
        if getattr(args, "json", False):
            _json_or_text(tasks, [])
            return 0
        if not tasks:
            print("无任务（下载时执行 get 生成任务控制记录；历史报告也可在此看到）")
            return 0
        print("%-14s %-6s %-8s %-10s %-20s" % ("ID", "状态", "网盘", "引擎", "更新时间"))
        for t in tasks:
            print("%-14s %-6s %-8s %-10s %-20s" % (
                t["id"], t.get("state", ""), (t.get("drive_name") or t.get("drive") or ""),
                t.get("engine", ""), (t.get("updated") or "")))
        return 0

    if sub == "show":
        if not getattr(args, "id", None):
            print("❌ 缺少任务 ID")
            return 2
        path, rec = _locate_task_control(reports_dir, args.id)
        if not path or not rec:
            print("❌ 未找到任务：%s（可先 `pan task list` 查看）" % args.id)
            return 1
        rec.pop("_control_path", None)
        if getattr(args, "json", False):
            _json_or_text(rec, [])
        else:
            print(json.dumps(rec, ensure_ascii=False, indent=2))
        return 0

    if sub in ("pause", "resume", "delete", "retry"):
        if not getattr(args, "id", None):
            print("❌ 缺少任务 ID")
            return 2
        ok, msg = _apply_task_action(reports_dir, args.id, sub)
        print(("✅ " if ok else "❌ ") + msg)
        return 0 if ok else 1

    print("用法：pan task list|show|pause|resume|delete|retry <id>")
    return 2


def cmd_dirs(args):
    cfg = load_config()
    the_root = default_root(cfg)
    example = task_dir(cfg, "百度网盘", "https://pan.baidu.com/s/1abcd")
    if getattr(args, "json", False):
        print(json.dumps({"default_root": str(the_root), "example_task_dir": str(example)}, ensure_ascii=False, indent=2))
    else:
        print("默认根目录：%s" % the_root)
        print("示例任务目录：%s" % example)
    return 0


def build_parser():
    p = argparse.ArgumentParser(prog="pan", description="网盘通入口（免费账号默认）")
    sub = p.add_subparsers(dest="cmd")

    d = sub.add_parser("doctor", help="检查环境与依赖")
    d.add_argument("--json", action="store_true")
    d.set_defaults(func=cmd_doctor)

    p_init = sub.add_parser("init", help="创建配置文件")
    p_init.add_argument("--force", action="store_true")
    p_init.add_argument("--wizard", action="store_true", help="环境检测向导")
    p_init.add_argument("--json", action="store_true", help="输出 JSON")
    p_init.set_defaults(func=cmd_init)

    p_setup = sub.add_parser("setup", help="一键安装 + 配置向导（创建配置、补依赖）")
    p_setup.add_argument("--root", help="设置默认下载目录")
    p_setup.add_argument("--force", action="store_true", help="配置已存在也重新写入")
    p_setup.add_argument("--apply", action="store_true", help="实际运行包管理器安装命令（默认只列出）")
    p_setup.add_argument("--json", action="store_true", help="输出 JSON")
    p_setup.set_defaults(func=cmd_setup)

    sub.add_parser("show", help="显示配置（凭据打码）").set_defaults(func=cmd_show)

    p_detect = sub.add_parser("detect", help="识别链接属于哪个网盘")
    p_detect.add_argument("url")
    p_detect.add_argument("--json", action="store_true", help="输出 JSON（默认即 JSON）")
    p_detect.set_defaults(func=cmd_detect)

    p_test = sub.add_parser("test", help="测试连接：识别链接并检查依赖/目录是否就绪（不下载）")
    p_test.add_argument("url")
    p_test.add_argument("--pwd", help="分享提取码")
    p_test.add_argument("--engine")
    p_test.add_argument("--tier", choices=["free", "vip", "auto"])
    p_test.add_argument("--path", help="AList/WebDAV 已挂载路径")
    p_test.add_argument("--json", action="store_true", help="给 agent 输出 JSON")
    p_test.set_defaults(func=cmd_test)

    p_set = sub.add_parser("set", help="修改全局配置")
    p_set.add_argument("--root")
    p_set.add_argument("--tier", choices=["free", "vip", "auto"])
    p_set.add_argument("--engine-name")
    p_set.add_argument("--engine")
    p_set.add_argument("--alist-url")
    p_set.add_argument("--alist-user")
    p_set.add_argument("--alist-password", help=argparse.SUPPRESS)
    p_set.add_argument("--alist-password-stdin", action="store_true", help="从 stdin 读取 AList 密码并存入系统凭据库")
    p_set.add_argument("--rclone-remote")
    p_set.add_argument("--webdav-url")
    p_set.add_argument("--webdav-user")
    p_set.add_argument("--webdav-password", help=argparse.SUPPRESS)
    p_set.add_argument("--webdav-password-stdin", action="store_true", help="从 stdin 读取 WebDAV 密码并存入系统凭据库")
    p_set.add_argument("--auto-classify", choices=["on", "off", ""], default="", help="智能默认：按扩展名自动归档（on/off）")
    p_set.set_defaults(func=cmd_set)

    p_sd = sub.add_parser("set-drive", help="修改单个网盘配置")
    p_sd.add_argument("drive")
    p_sd.add_argument("--tier", choices=["free", "vip", "auto"])
    p_sd.add_argument("--account-tier", choices=["free", "vip"])
    p_sd.add_argument("--tier-detector")
    p_sd.add_argument("--cookie-file")
    p_sd.add_argument("--credential-ref", help="绑定现有 credential:/keychain: 名称，不会打印密码")
    p_sd.add_argument("--credential-stdin", action="store_true", help="从 stdin 读取本网盘密码并存入系统凭据库")
    p_sd.add_argument("--engine-command")
    p_sd.add_argument("--save-path")
    p_sd.set_defaults(func=cmd_set_drive)

    p_secret = sub.add_parser("secret", help="安全保存、检查、删除或迁移凭据")
    secret_sub = p_secret.add_subparsers(dest="secret_cmd")
    ps = secret_sub.add_parser("set", help="把密码写入系统凭据库")
    ps.add_argument("name")
    ps.add_argument("--stdin", action="store_true", help="从 stdin 读取，适合脚本/agent")
    ps.set_defaults(func=cmd_secret_set)
    pc = secret_sub.add_parser("check", help="检查指定凭据是否存在")
    pc.add_argument("name", nargs="?")
    pc.add_argument("--json", action="store_true")
    pc.set_defaults(func=cmd_secret_check)
    pl = secret_sub.add_parser("list", help="列出配置引用的凭据状态")
    pl.add_argument("--json", action="store_true")
    pl.set_defaults(func=cmd_secret_list)
    pd = secret_sub.add_parser("delete", help="从系统凭据库删除指定凭据")
    pd.add_argument("name")
    pd.set_defaults(func=cmd_secret_delete)
    pm = secret_sub.add_parser("migrate", help="把旧配置里的已知明文凭据迁入系统凭据库")
    pm.set_defaults(func=cmd_secret_migrate)

    p_login = sub.add_parser("login", help="查看某网盘的登录/授权步骤")
    p_login.add_argument("drive")
    p_login.add_argument("--open", action="store_true", help="用默认程序打开授权教程")
    p_login.set_defaults(func=cmd_login)

    p_get = sub.add_parser("get", help="下载分享链接或直链")
    p_get.add_argument("url")
    p_get.add_argument("--pwd", help="分享提取码")
    p_get.add_argument("--at", dest="at", default="", help="定时/低峰：HH:MM（如 --at 02:30），到点再开始下载；over 当前时间则立即用配置默认")
    p_get.add_argument("--to", help="指定下载目录")
    p_get.add_argument("--engine")
    p_get.add_argument("--tier", choices=["free", "vip", "auto"])
    p_get.add_argument("--path", help="AList 中已挂载的路径")
    p_get.add_argument("--remote", help="下载到已登记的远程设备（remote add 创建）")
    p_get.add_argument("--dry-run", action="store_true", help="只打印计划，不实际下载")
    p_get.add_argument("--force", action="store_true", help="依赖缺失时也尝试执行")
    p_get.add_argument("--json", action="store_true", help="给 agent 输出无凭据 JSON")
    p_get.add_argument("--events", action="store_true", help="实际下载时输出逐步 JSON 事件")
    p_get.add_argument("--live", action="store_true", help="写入实时速度状态文件（下载速度.live.json），可在 serve 页面查看")
    p_get.add_argument("--split", type=int, default=0, help="http 直链单文件 Range 分片并发数（默认0=关闭，仅对支持 Range 的直链生效）")
    p_get.add_argument("--classify", action="store_true", default=None, help="按扩展名自动归档到 影视/音乐/文档/图片/压缩包/其他（覆盖 smart.auto_classify，未开启时可手动启用）")
    p_get.set_defaults(func=cmd_get)

    p_remote = sub.add_parser("remote", help="管理 NAS、飞牛、群晖、私有云盘等远程设备")
    remote_sub = p_remote.add_subparsers(dest="remote_cmd")
    ra = remote_sub.add_parser("add", help="登记或修改远程设备（不保存明文密码）")
    ra.add_argument("name")
    ra.add_argument("--kind", choices=REMOTE_KINDS)
    ra.add_argument("--host")
    ra.add_argument("--port")
    ra.add_argument("--user")
    ra.add_argument("--root", help="远程下载根目录；mount 类型填本机挂载路径")
    ra.add_argument("--remote-name", help="rclone 配置里的 remote 名，例如 nas")
    ra.add_argument("--python", default=None, help="SSH 远程 Python 命令，默认 python3")
    ra.add_argument("--deploy-dir", help="SSH 远程技能目录，默认 .pan-downloader")
    ra.add_argument("--web-port", type=int, default=None, help="默认远程 Web 端口（remote deploy 未显式指定时使用）")
    ra.add_argument("--web-host", default=None, help="默认远程 Web 监听地址（127.0.0.1 或 0.0.0.0）")
    ra.add_argument("--description")
    ra.add_argument("--credential-ref", help="已有系统凭据引用；只保存引用，不保存明文")
    ra.add_argument("--credential-stdin", action="store_true", help="从 stdin 读取远程凭据并存系统凭据库")
    ra.set_defaults(func=cmd_remote_add)

    rl = remote_sub.add_parser("list", help="列出远程设备（不含密码）")
    rl.add_argument("--json", action="store_true")
    rl.set_defaults(func=cmd_remote_list)

    rr = remote_sub.add_parser("remove", help="删除远程设备配置（不删除下载文件）")
    rr.add_argument("name")
    rr.set_defaults(func=cmd_remote_remove)

    rc = remote_sub.add_parser("check", help="检查远程配置；可选 --probe 联网探测")
    rc.add_argument("name")
    rc.add_argument("--probe", action="store_true")
    rc.add_argument("--json", action="store_true")
    rc.set_defaults(func=cmd_remote_check)

    rd = remote_sub.add_parser("deploy", help="把无凭据技能包部署到 SSH 设备；可选 --web-port 后台启动远程 Web 控制页")
    rd.add_argument("name")
    rd.add_argument("--web-port", type=int, default=0, help="部署后远程后台启动 serve（默认 0=不启动；示例 17890）")
    rd.add_argument("--web-host", default=None, help="远程 Web 监听地址（默认 127.0.0.1；局域网访问填 0.0.0.0）")
    rd.add_argument("--web-reports-dir", default=None, help="远程 Web 报告目录（默认远程 root，可扫描实时速度与历史报告）")
    rd.add_argument("--dry-run", action="store_true")
    rd.add_argument("--json", action="store_true", help="输出打码后的部署计划，不执行上传")
    rd.set_defaults(func=cmd_remote_deploy)

    rw = remote_sub.add_parser("web", help="打印远程 Web 控制页访问地址与 SSH 反向隧道命令（不实际连接）")
    rw.add_argument("name")
    rw.add_argument("--port", type=int, default=0, help="远程 Web 端口（默认取配置/17890）")
    rw.add_argument("--host", default=None, help="远程监听地址（默认取配置/127.0.0.1）")
    rw.add_argument("--local-port", type=int, default=0, help="本机反向隧道端口（默认同远程端口）")
    rw.add_argument("--json", action="store_true", help="输出 JSON 访问信息")
    rw.set_defaults(func=cmd_remote_web)

    rg = remote_sub.add_parser("get", help="从分享链接下载到指定远程设备")
    rg.add_argument("name")
    rg.add_argument("url")
    rg.add_argument("--pwd", help="分享提取码")
    rg.add_argument("--to", help="覆盖远程目标目录")
    rg.add_argument("--engine")
    rg.add_argument("--tier", choices=["free", "vip", "auto"])
    rg.add_argument("--path", help="AList 中已挂载的路径")
    rg.add_argument("--live", action="store_true", help="远程下载时写入实时速度文件，供远程 Web 页面查看")
    rg.add_argument("--dry-run", action="store_true", help="只打印计划，不实际下载")
    rg.add_argument("--force", action="store_true", help="依赖缺失时也尝试执行")
    rg.add_argument("--json", action="store_true", help="给 agent 输出无凭据 JSON")
    rg.set_defaults(func=cmd_remote_get)

    p_dirs = sub.add_parser("dirs", help="查看默认下载目录")
    p_dirs.add_argument("--json", action="store_true", help="输出 JSON")
    p_dirs.set_defaults(func=cmd_dirs)

    p_task = sub.add_parser("task", help="任务控制（list/show/pause/resume/delete/retry）")
    p_task.add_argument("--json", action="store_true", help="输出 JSON")
    p_task.add_argument("--reports-dir", default="", help="报告目录（默认读配置 http.report_dir/live_dir）")
    task_sub = p_task.add_subparsers(dest="task_cmd")
    tl = task_sub.add_parser("list", help="任务列表")
    tl.add_argument("--state", default="", help="按状态过滤：running/done/failed/paused/cancelled")
    tl.set_defaults(func=cmd_task)
    ts = task_sub.add_parser("show", help="查看单任务详情")
    ts.add_argument("id")
    ts.set_defaults(func=cmd_task)
    for name in ("pause", "resume", "delete", "retry"):
        tp = task_sub.add_parser(name, help="%s 指定任务" % name)
        tp.add_argument("id")
        tp.set_defaults(func=cmd_task)

    p_tr = sub.add_parser("transfer", help="AList/rclone 跨盘转存（rclone copy，默认 dry-run）")
    p_tr.add_argument("src")
    p_tr.add_argument("dst")
    p_tr.add_argument("--transfers", type=int, default=0)
    p_tr.add_argument("--checkers", type=int, default=0)
    p_tr.add_argument("--apply", action="store_true", help="实际执行 rclone copy（默认只打印 dry-run）")
    p_tr.add_argument("--json", action="store_true", help="输出 JSON 计划")
    p_tr.add_argument("--allow-company-dest", action="store_true", help="明确允许写入公司目录（默认禁止）")
    p_tr.set_defaults(func=cmd_transfer)

    p_sync = sub.add_parser("sync", help="增量同步（rclone sync，会删除目标多余文件，需 --delete + --apply）")
    p_sync.add_argument("src")
    p_sync.add_argument("dst")
    p_sync.add_argument("--delete", action="store_true", help="允许删除目标多余文件（必须显式）")
    p_sync.add_argument("--transfers", type=int, default=0)
    p_sync.add_argument("--checkers", type=int, default=0)
    p_sync.add_argument("--apply", action="store_true", help="实际执行 rclone sync")
    p_sync.add_argument("--json", action="store_true", help="输出 JSON 计划")
    p_sync.add_argument("--allow-company-dest", action="store_true", help="明确允许写入公司目录（默认禁止）")
    p_sync.set_defaults(func=cmd_sync)

    p_notify = sub.add_parser("notify", help="发送完成/失败通知（webhook 地址存系统凭据库，默认 dry-run）")
    p_ns = p_notify.add_subparsers(dest="notify_cmd")
    ns = p_ns.add_parser("send", help="发送通知")
    ns.add_argument("--channel", choices=["work_weixin", "bark", "telegram", "discord", "feishu"], default="work_weixin")
    ns.add_argument("--chat-id", default="", help="telegram 必填：接收消息的 chat_id")
    ns.add_argument("--title", default="pan-downloader")
    ns.add_argument("--body", default="")
    ns.add_argument("--send", action="store_true", help="真正发送（默认只渲染 dry-run）")
    ns.add_argument("--json", action="store_true", help="输出 JSON")
    ns.set_defaults(func=cmd_notify_send)

    p_mcp = sub.add_parser("mcp", help="MCP 注册指引")
    pm = p_mcp.add_subparsers(dest="mcp_cmd")
    mg = pm.add_parser("guide", help="输出 Codex MCP 注册片段")
    mg.add_argument("--json", action="store_true")
    mg.set_defaults(func=cmd_mcp_guide)

    p_serve = sub.add_parser("serve", help="只读本地状态页（默认 127.0.0.1:17890）")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=17890)
    p_serve.add_argument("--reports-dir", default="", help="报告目录（默认读配置 http.report_dir）")
    p_serve.set_defaults(func=cmd_serve)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    if not getattr(args, "func", None):
        build_parser().print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
