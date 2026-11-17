#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
# ⚠️ 本文件是「京东黄金 (jdgold)」JoyCode Skill 的组成脚本。
# 执行任何脚本前，必须先阅读 Skill 根目录下的 SKILL.md，
# 严格遵循其中的执行契约、安全脱敏铁律与回复规范，
# 请勿脱离 SKILL.md 指引单独运行本脚本。
# ============================================================
"""跨平台系统级加密凭据存储（jdgold，仅本地使用）。

将敏感凭据（如 access_token）保存到操作系统提供的安全存储中，替代明文文件：
  - macOS  : Keychain（``security`` 命令，generic-password 条目，密钥仅登录钥匙串可解）。
  - Windows: DPAPI（``CryptProtectData`` 用户态加密），密文写入本地文件（明文永不落盘）。
  - 其他/回退: 兼容旧行为，写 0o600 权限的本地明文文件（尽力保护）。

对外统一接口（值均为 UTF-8 字符串）：
  - save_secret(name, value)
  - load_secret(name) -> str | None
  - delete_secret(name)
  - backend_name() -> str        # 当前生效的后端标识，便于日志/诊断

设计约束：
  - 不引入第三依赖，仅用标准库 + 系统自带命令/API。
  - 任何后端失败都不得抛出明文；异常统一转为 None / False 语义。
"""
import os
import sys
import base64
import subprocess

# Keychain / 文件后端使用的服务命名空间与本地密文目录
SERVICE_NAME = "com.jd.jdgold"
_CACHE_DIR = os.path.expanduser("~/.openclaw/service-env/jdgold")


def _platform():
    if sys.platform == "darwin":
        return "macos"
    if os.name == "nt" or sys.platform.startswith("win"):
        return "windows"
    return "other"


def backend_name():
    """返回当前平台实际使用的存储后端标识。"""
    p = _platform()
    if p == "macos":
        return "keychain"
    if p == "windows":
        return "dpapi"
    return "file"


# --------------------------------------------------------------------------- #
# macOS Keychain 后端
# --------------------------------------------------------------------------- #
def _keychain_save(name, value):
    # -U：条目已存在则更新；-w 后跟明文，仅进内存不落盘
    subprocess.run(
        ["security", "add-generic-password", "-U",
         "-s", SERVICE_NAME, "-a", name, "-w", value],
        check=True, capture_output=True, text=True,
    )
    return True


def _keychain_load(name, service=SERVICE_NAME):
    proc = subprocess.run(
        ["security", "find-generic-password",
         "-s", service, "-a", name, "-w"],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout.rstrip("\n")


def _keychain_delete(name, service=SERVICE_NAME):
    subprocess.run(
        ["security", "delete-generic-password",
         "-s", service, "-a", name],
        capture_output=True, text=True,
    )
    return True


# --------------------------------------------------------------------------- #
# Windows DPAPI 后端（密文写本地文件；明文永不落盘）
# --------------------------------------------------------------------------- #
def _dpapi_file(name, cache_dir=_CACHE_DIR):
    return os.path.join(cache_dir, f"{name}.dpapi")


def _dpapi_protect(plaintext_bytes):
    import ctypes
    from ctypes import wintypes

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [("cbData", wintypes.DWORD),
                    ("pbData", ctypes.POINTER(ctypes.c_char))]

    def _to_blob(data):
        buf = ctypes.create_string_buffer(data, len(data))
        return DATA_BLOB(len(data), ctypes.cast(buf, ctypes.POINTER(ctypes.c_char))), buf

    in_blob, _keep = _to_blob(plaintext_bytes)
    out_blob = DATA_BLOB()
    # CRYPTPROTECT_UI_FORBIDDEN = 0x1（禁止弹窗，适合无人值守）
    ok = ctypes.windll.crypt32.CryptProtectData(
        ctypes.byref(in_blob), None, None, None, None, 0x1, ctypes.byref(out_blob))
    if not ok:
        raise OSError("CryptProtectData failed")
    try:
        return ctypes.string_at(out_blob.pbData, out_blob.cbData)
    finally:
        ctypes.windll.kernel32.LocalFree(out_blob.pbData)


def _dpapi_unprotect(cipher_bytes):
    import ctypes
    from ctypes import wintypes

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [("cbData", wintypes.DWORD),
                    ("pbData", ctypes.POINTER(ctypes.c_char))]

    def _to_blob(data):
        buf = ctypes.create_string_buffer(data, len(data))
        return DATA_BLOB(len(data), ctypes.cast(buf, ctypes.POINTER(ctypes.c_char))), buf

    in_blob, _keep = _to_blob(cipher_bytes)
    out_blob = DATA_BLOB()
    ok = ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(in_blob), None, None, None, None, 0x1, ctypes.byref(out_blob))
    if not ok:
        raise OSError("CryptUnprotectData failed")
    try:
        return ctypes.string_at(out_blob.pbData, out_blob.cbData)
    finally:
        ctypes.windll.kernel32.LocalFree(out_blob.pbData)


def _dpapi_save(name, value):
    os.makedirs(_CACHE_DIR, exist_ok=True)
    cipher = _dpapi_protect(value.encode("utf-8"))
    # base64 存储，避免二进制文件在传输/编辑中被破坏
    with open(_dpapi_file(name), "w", encoding="ascii") as f:
        f.write(base64.b64encode(cipher).decode("ascii"))
    return True


def _dpapi_load(name, cache_dir=_CACHE_DIR):
    path = _dpapi_file(name, cache_dir)
    if not os.path.exists(path):
        return None
    with open(path, encoding="ascii") as f:
        cipher = base64.b64decode(f.read())
    return _dpapi_unprotect(cipher).decode("utf-8")


def _dpapi_delete(name, cache_dir=_CACHE_DIR):
    try:
        os.remove(_dpapi_file(name, cache_dir))
    except FileNotFoundError:
        pass
    return True


# --------------------------------------------------------------------------- #
# 文件回退后端（0o600 明文，兼容无 Keychain/DPAPI 的环境）
# --------------------------------------------------------------------------- #
def _file_path(name, cache_dir=_CACHE_DIR):
    return os.path.join(cache_dir, f"{name}.secret")


def _file_save(name, value):
    os.makedirs(_CACHE_DIR, exist_ok=True)
    path = _file_path(name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(value)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return True


def _file_load(name, cache_dir=_CACHE_DIR):
    path = _file_path(name, cache_dir)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return f.read()


def _file_delete(name, cache_dir=_CACHE_DIR):
    try:
        os.remove(_file_path(name, cache_dir))
    except FileNotFoundError:
        pass
    return True


# --------------------------------------------------------------------------- #
# 统一对外接口（失败降级到文件后端，保证可用性）
# --------------------------------------------------------------------------- #
def save_secret(name, value):
    """保存凭据。value 为字符串。返回 True/False。"""
    if value is None:
        return delete_secret(name)
    p = _platform()
    try:
        if p == "macos":
            return _keychain_save(name, value)
        if p == "windows":
            return _dpapi_save(name, value)
    except Exception:
        # 系统后端不可用时降级到文件，避免整体登录流程中断
        pass
    return _file_save(name, value)


def load_secret(name):
    """读取凭据，不存在或失败返回 None。"""
    p = _platform()
    try:
        if p == "macos":
            val = _keychain_load(name)
            if val is not None:
                return val
        elif p == "windows":
            val = _dpapi_load(name)
            if val is not None:
                return val
    except Exception:
        pass
    # 文件后端兜底（覆盖系统后端不可用时的降级写入场景）
    return _file_load(name)


def delete_secret(name):
    """删除凭据（各后端与新旧命名均尝试清理，确保无残留）。"""
    ok = True
    p = _platform()
    try:
        if p == "macos":
            _keychain_delete(name)
        elif p == "windows":
            _dpapi_delete(name)
    except Exception:
        ok = False
    _file_delete(name)
    return ok