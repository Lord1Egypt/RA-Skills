#!/usr/bin/env python3
"""iFinD API CLI — Python 实现（仅标准库）"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
import gzip

# ─── 常量 ───
IFIND_BASE_URL = "https://quantapi.51ifind.com/api/v1"
TOKEN_CACHE_TTL = 86400  # 1 天
LOG_MAX_BYTES = 1 * 1024 * 1024  # 1MB
LOG_KEEP_BYTES = 500 * 1024  # 保留最近 500KB

# ─── 目录 ───
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(SKILL_DIR, ".data")
os.makedirs(DATA_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════
# 日志
# ═══════════════════════════════════════════════════

def log_path():
    return os.path.join(DATA_DIR, "ifind.log")


def rotate_log():
    path = log_path()
    try:
        size = os.path.getsize(path)
    except OSError:
        return
    if size <= LOG_MAX_BYTES:
        return
    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError:
        return
    if len(data) > LOG_KEEP_BYTES:
        data = data[-LOG_KEEP_BYTES:]
        idx = data.find(b"\n")
        if idx >= 0:
            data = data[idx + 1:]
    with open(path, "wb") as f:
        f.write(data)


def log_entry(endpoint, status, err_msg="", step="", latency_ms=0):
    rotate_log()
    try:
        with open(log_path(), "a", encoding="utf-8") as f:
            ts = time.strftime("%Y-%m-%d %H:%M:%S")
            msg = f"[{ts}] endpoint={endpoint} status={status} latency={latency_ms}ms"
            if err_msg:
                msg += f' error="{err_msg}" step={step}'
            f.write(msg + "\n")
    except OSError:
        pass


# ═══════════════════════════════════════════════════
# .env 加载
# ═══════════════════════════════════════════════════

def load_env():
    env_file = os.path.join(SKILL_DIR, ".env")
    env = {}
    try:
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("=", 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    val = parts[1].strip().strip("\"'")
                    env[key] = val
                    os.environ[key] = val
    except OSError:
        pass
    return env


# ═══════════════════════════════════════════════════
# HTTP 工具
# ═══════════════════════════════════════════════════

def http_post(url, headers=None, body=b""):
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            if resp.headers.get("Content-Encoding") == "gzip":
                data = gzip.decompress(data)
            return data
    except urllib.error.HTTPError as e:
        body_bytes = e.read() if hasattr(e, "read") else b""
        raise RuntimeError(f"HTTP {e.code}: {body_bytes.decode('utf-8', errors='replace')}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"网络请求失败: {e.reason}") from e


# ═══════════════════════════════════════════════════
# getAccessToken — 缓存 + 自动刷新
# ═══════════════════════════════════════════════════

def get_access_token(refresh_token):
    cache_file = os.path.join(DATA_DIR, "access_token")

    # 检查缓存
    try:
        stat = os.stat(cache_file)
        age = time.time() - stat.st_mtime
        if age < TOKEN_CACHE_TTL:
            with open(cache_file, "r", encoding="utf-8") as f:
                token = f.read().strip()
            if token:
                return token
    except OSError:
        pass

    start = time.time()
    try:
        data = http_post(
            IFIND_BASE_URL + "/get_access_token",
            headers={"refresh_token": refresh_token},
            body=b"{}",
        )
    except RuntimeError as e:
        latency_ms = int((time.time() - start) * 1000)
        log_entry("get_access_token", "error", str(e), "get_token", latency_ms)
        exit_error(f"获取 access_token 失败: {e}")

    try:
        result = json.loads(data)
    except json.JSONDecodeError:
        latency_ms = int((time.time() - start) * 1000)
        log_entry("get_access_token", "error", "invalid json", "get_token", latency_ms)
        exit_error(f"获取 access_token 响应异常: {data.decode('utf-8', errors='replace')}")

    data_obj = result.get("data")
    if not isinstance(data_obj, dict):
        latency_ms = int((time.time() - start) * 1000)
        log_entry("get_access_token", "error", "no data field", "get_token", latency_ms)
        exit_error("获取 access_token 失败，请检查 IFIND_REFRESH_TOKEN 是否有效")

    token = data_obj.get("access_token", "")
    if not token:
        latency_ms = int((time.time() - start) * 1000)
        log_entry("get_access_token", "error", "no access_token", "get_token", latency_ms)
        exit_error("获取 access_token 失败，请检查 IFIND_REFRESH_TOKEN 是否有效")

    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(token)
    except OSError:
        pass
    return token


def clear_token_cache():
    try:
        os.remove(os.path.join(DATA_DIR, "access_token"))
    except OSError:
        pass


# ═══════════════════════════════════════════════════
# callAPI — 调用 iFinD API
# ═══════════════════════════════════════════════════

def call_api(access_token, endpoint, json_body):
    url = IFIND_BASE_URL + "/" + endpoint
    headers = {
        "access_token": access_token,
        "Accept-Encoding": "gzip,deflate",
    }
    return http_post(url, headers=headers, body=json_body.encode("utf-8"))


# ═══════════════════════════════════════════════════
# JSON 输出工具
# ═══════════════════════════════════════════════════

def write_json(obj):
    print(json.dumps(obj, ensure_ascii=False, separators=(",", ":")))


def exit_error(msg):
    write_json({"error": msg})
    sys.exit(1)


# ═══════════════════════════════════════════════════
# main
# ═══════════════════════════════════════════════════

def main():
    # 参数校验
    if len(sys.argv) < 3:
        write_json({"error": "用法: python3 ifind-api.py <api_endpoint> <json_body>"})
        sys.exit(1)

    api_endpoint = sys.argv[1]
    json_body = sys.argv[2]

    # 加载 .env
    load_env()

    refresh_token = os.environ.get("IFIND_REFRESH_TOKEN", "")
    if not refresh_token:
        exit_error("缺少环境变量 IFIND_REFRESH_TOKEN，请设置后重试")

    start = time.time()

    # Step 1: 获取 access_token
    access_token = get_access_token(refresh_token)

    # Step 2: 调用 iFinD API
    try:
        result = call_api(access_token, api_endpoint, json_body)
    except RuntimeError as e:
        latency_ms = int((time.time() - start) * 1000)
        log_entry(api_endpoint, "error", str(e), "api_call", latency_ms)
        exit_error(f"API 调用失败: {e}")

    # 检查 errorcode = -1302 (token 过期)，自动重试
    try:
        api_result = json.loads(result)
        error_code = api_result.get("errorcode")
        if error_code is not None:
            if isinstance(error_code, (int, float)) and int(error_code) == -1302:
                clear_token_cache()
                access_token = get_access_token(refresh_token)
                try:
                    result = call_api(access_token, api_endpoint, json_body)
                except RuntimeError as e:
                    latency_ms = int((time.time() - start) * 1000)
                    log_entry(api_endpoint, "error", str(e), "api_call", latency_ms)
                    exit_error(f"API 调用失败 (重试): {e}")
    except (json.JSONDecodeError, TypeError):
        pass

    latency_ms = int((time.time() - start) * 1000)
    log_entry(api_endpoint, "ok", "", "", latency_ms)

    # 直接输出原始 JSON
    sys.stdout.buffer.write(result)
    if not result.endswith(b"\n"):
        sys.stdout.buffer.write(b"\n")


if __name__ == "__main__":
    main()
