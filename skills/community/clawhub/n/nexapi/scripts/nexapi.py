#!/usr/bin/env python3
"""
NexAPI CLI - 发布版
"""

import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from getpass import getpass

BASE_URL = os.getenv("NEXAPI_BASE_URL", "https://api.avrinbai.cn").rstrip("/")
SKILL_ROOT = Path(__file__).resolve().parents[1]
CACHE_PATH = Path(os.getenv("NEXAPI_CACHE_FILE", str(SKILL_ROOT / ".nexapi_apis_cache.json")))
CONFIG_PATH = Path(os.getenv("NEXAPI_CONFIG_FILE", str(SKILL_ROOT / ".nexapi_config.json")))
HEALTH_PATH = os.getenv("NEXAPI_HEALTH_PATH", "/api/health/openclaw")

# 常见参数别名：降低用户记忆成本
PARAM_ALIASES = {
    "phone-area": {"phone": "number"},
    "netease-hot-comments": {"id": "songid"},
    "id-card": {"id": "number"},
    "kuaidi-track": {"num": "no", "postid": "no"},
    "video-no-watermark-v2": {"share": "url"},
    "mi-motion-step": {"account": "user", "pwd": "password"},
}


def require_api_key():
    # 优先环境变量，其次本地配置文件
    key = os.getenv("NEXAPI_API_KEY", "").strip()
    if key:
        return key

    cfg = load_config()
    key = str(cfg.get("api_key", "")).strip()
    if key:
        return key

    print("缺少 NexAPI Key。请先配置后再调用接口。", file=sys.stderr)
    print("推荐方式：python3 scripts/nexapi.py auth set", file=sys.stderr)
    print("也可使用环境变量：NEXAPI_API_KEY", file=sys.stderr)
    sys.exit(2)


def _default_config():
    return {
        "cache_policy": "ttl",  # manual | ttl | always
        "cache_ttl_seconds": 1800,
        "api_key": "",
    }


def load_config():
    cfg = _default_config()
    if CONFIG_PATH.is_file():
        try:
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                cfg.update(data)
        except Exception:
            pass

    policy = str(cfg.get("cache_policy", "ttl")).lower()
    if policy not in ("manual", "ttl", "always"):
        policy = "ttl"
    cfg["cache_policy"] = policy

    try:
        ttl = int(cfg.get("cache_ttl_seconds", 1800))
    except Exception:
        ttl = 1800
    cfg["cache_ttl_seconds"] = max(60, ttl)
    return cfg


def save_config(config):
    CONFIG_PATH.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")


def auth_set(api_key=None):
    cfg = load_config()
    if api_key is None or str(api_key).strip() == "":
        api_key = getpass("请输入 NexAPI Key（不会回显）：").strip()
    if not api_key:
        print("未输入 Key，已取消。", file=sys.stderr)
        sys.exit(1)
    cfg["api_key"] = api_key
    save_config(cfg)
    print(json.dumps({"ok": True, "config": str(CONFIG_PATH)}, ensure_ascii=False, indent=2))


def auth_status():
    cfg = load_config()
    has_env = bool(os.getenv("NEXAPI_API_KEY", "").strip())
    has_cfg = bool(str(cfg.get("api_key", "")).strip())
    print(json.dumps({
        "env_key_set": has_env,
        "config_key_set": has_cfg,
        "config": str(CONFIG_PATH),
    }, ensure_ascii=False, indent=2))


def discover_apis_from_health():
    separator = "&" if "?" in HEALTH_PATH else "?"
    url = BASE_URL + HEALTH_PATH + separator + urllib.parse.urlencode({"sort": "hot"})
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=12) as resp:
            payload = json.loads(resp.read().decode("utf-8", errors="ignore"))
    except Exception:
        return {}

    data = payload.get("data") if isinstance(payload, dict) else None
    items = data.get("apis") if isinstance(data, dict) else None
    if not isinstance(items, list):
        return {}

    discovered = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        path = str(item.get("path", "")).strip("/")
        if not path:
            continue
        key = path.split("/")[-1]
        discovered[key] = {
            "key": key,
            "name": item.get("name", key),
            "path": "/api/" + path,
            "method": str(item.get("method", "GET")).upper(),
            "category": item.get("category", "uncategorized"),
            "desc": item.get("description", ""),
            "docs": item.get("docs", ""),
            "requires_api_key": bool(item.get("requires_api_key", False)),
        }
    return discovered


def cache_is_fresh(ttl_seconds):
    if not CACHE_PATH.is_file():
        return False
    try:
        modified = CACHE_PATH.stat().st_mtime
    except Exception:
        return False
    return (int(__import__("time").time()) - int(modified)) < ttl_seconds


def read_cache():
    if not CACHE_PATH.is_file():
        return {}
    try:
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def fetch_and_cache_apis():
    apis = discover_apis_from_health()
    if not apis:
        return {}
    CACHE_PATH.write_text(json.dumps(apis, ensure_ascii=False), encoding="utf-8")
    return apis


def load_apis(refresh=False):
    cfg = load_config()
    if refresh:
        apis = fetch_and_cache_apis()
        return apis

    policy = cfg["cache_policy"]
    if policy == "manual":
        return read_cache()

    if policy == "ttl":
        if cache_is_fresh(cfg["cache_ttl_seconds"]):
            return read_cache()
        apis = fetch_and_cache_apis()
        return apis if apis else read_cache()

    # always
    apis = fetch_and_cache_apis()
    if apis:
        return apis
    # 网络异常时回退缓存，保证可用
    return read_cache()


def parse_flag_value(args, name):
    prefix = name + "="
    for arg in args:
        if arg.startswith(prefix):
            return arg[len(prefix):]
    return None


def parse_init_options(args):
    cfg = load_config()
    p = parse_flag_value(args, "--policy")
    t = parse_flag_value(args, "--ttl")
    if p:
        p = p.lower().strip()
        if p in ("manual", "ttl", "always"):
            cfg["cache_policy"] = p
    if t:
        try:
            cfg["cache_ttl_seconds"] = max(60, int(t))
        except Exception:
            pass
    return cfg


def normalize_params(api_name, params):
    aliases = PARAM_ALIASES.get(api_name, {})
    normalized = {}
    for k, v in params.items():
        normalized[aliases.get(k, k)] = v
    return normalized


def compact_output(payload):
    if not isinstance(payload, dict):
        return payload
    # 默认压缩输出，减少技能 token 消耗
    out = {k: payload.get(k) for k in ("code", "msg", "message", "error") if k in payload}
    if "data" in payload:
        data = payload["data"]
        if isinstance(data, dict):
            out["data_keys"] = list(data.keys())[:10]
        elif isinstance(data, list):
            out["data_count"] = len(data)
        else:
            out["data"] = str(data)[:180]
    if not out:
        return payload
    return out


def call_api(apis, api_name, params=None, verbose=False):
    if api_name not in apis:
        return {"error": f"未知 API: {api_name}"}
    info = apis[api_name]
    method = info.get("method", "GET").upper()
    url = BASE_URL + info["path"]
    params = normalize_params(api_name, params or {})

    headers = {"X-API-Key": require_api_key(), "Accept": "application/json"}
    data = None
    if method == "GET":
        if params:
            url += "?" + urllib.parse.urlencode(params)
    else:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        data = urllib.parse.urlencode(params).encode()

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
            ctype = (resp.headers.get("Content-Type") or "").lower()
            if "application/json" in ctype:
                result = json.loads(raw.decode("utf-8", errors="ignore"))
            else:
                # 如二维码等二进制响应，默认仅回传元信息，避免大输出
                result = {"status": "ok", "content_type": ctype, "bytes": len(raw)}
            return result if verbose else compact_output(result)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        return {"error": f"HTTP {e.code}", "detail": body[:220]}
    except Exception as e:
        return {"error": str(e)}


def print_usage():
    print("用法:")
    print("  python3 scripts/nexapi.py init [--refresh] [--policy=manual|ttl|always] [--ttl=1800]")
    print("  python3 scripts/nexapi.py list [--refresh]")
    print("  python3 scripts/nexapi.py cache status|clear|refresh")
    print("  python3 scripts/nexapi.py auth status|set [--key=...]")
    print("  python3 scripts/nexapi.py call <api_key> [k=v ...] [--verbose]")
    print("  python3 scripts/nexapi.py <api_key> [k=v ...]   # 简写")


def cache_status():
    cfg = load_config()
    cache_exists = CACHE_PATH.is_file()
    cache_items = 0
    cache_age_seconds = None
    if cache_exists:
        data = read_cache()
        if isinstance(data, dict):
            cache_items = len(data)
        try:
            cache_age_seconds = int(__import__("time").time() - CACHE_PATH.stat().st_mtime)
        except Exception:
            cache_age_seconds = None

    print(json.dumps({
        "cache_exists": cache_exists,
        "cache_path": str(CACHE_PATH),
        "config_path": str(CONFIG_PATH),
        "cache_items": cache_items,
        "cache_age_seconds": cache_age_seconds,
        "cache_policy": cfg.get("cache_policy"),
        "cache_ttl_seconds": cfg.get("cache_ttl_seconds"),
        "cache_is_fresh": cache_is_fresh(cfg.get("cache_ttl_seconds", 1800)),
    }, ensure_ascii=False, indent=2))


def cache_clear():
    removed = False
    if CACHE_PATH.is_file():
        CACHE_PATH.unlink()
        removed = True
    print(json.dumps({
        "ok": True,
        "removed": removed,
        "cache_path": str(CACHE_PATH),
    }, ensure_ascii=False, indent=2))


def cache_refresh():
    apis = fetch_and_cache_apis()
    print(json.dumps({
        "ok": bool(apis),
        "api_count": len(apis),
        "cache_path": str(CACHE_PATH),
    }, ensure_ascii=False, indent=2))


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    cmd = sys.argv[1]
    verbose = "--verbose" in sys.argv
    refresh = "--refresh" in sys.argv
    args = [a for a in sys.argv[2:] if a not in ("--verbose", "--refresh")]

    if cmd == "init":
        cfg = parse_init_options(args)
        save_config(cfg)
        apis = load_apis(refresh=True)
        print(json.dumps({
            "base_url": BASE_URL,
            "discover_mode": "health_endpoint_only",
            "api_count": len(apis),
            "cache": str(CACHE_PATH),
            "config": str(CONFIG_PATH),
            "cache_policy": cfg["cache_policy"],
            "cache_ttl_seconds": cfg["cache_ttl_seconds"],
            "api_key_ready": bool(os.getenv("NEXAPI_API_KEY", "").strip()),
        }, ensure_ascii=False, indent=2))
        if not apis:
            print("警告: /api/health/openclaw 拉取失败，当前缓存可能为空。", file=sys.stderr)
        return

    if cmd == "list":
        apis = load_apis(refresh=refresh)
        if not apis:
            print("未加载到 API 列表，请检查 /api/health/openclaw 可访问性并执行: python3 scripts/nexapi.py init --refresh")
            sys.exit(2)
        for key in sorted(apis.keys()):
            item = apis[key]
            print(f"{key:28s} {item.get('method','GET'):4s} {item.get('name','')}")
        return

    if cmd == "cache":
        action = args[0] if args else "status"
        if action == "status":
            cache_status()
            return
        if action == "clear":
            cache_clear()
            return
        if action == "refresh":
            cache_refresh()
            return
        print("未知 cache 子命令，可用: status | clear | refresh")
        sys.exit(1)

    if cmd == "auth":
        action = args[0] if args else "status"
        if action == "status":
            auth_status()
            return
        if action == "set":
            key = parse_flag_value(args[1:], "--key")
            auth_set(key)
            return
        print("未知 auth 子命令，可用: status | set")
        sys.exit(1)

    # call 简写模式
    if cmd == "call":
        if not args:
            print("缺少 api_key，例如: python3 scripts/nexapi.py call ip-location ip=8.8.8.8")
            sys.exit(1)
        api_name = args[0]
        kvs = args[1:]
    else:
        api_name = cmd
        kvs = args

    params = {}
    for arg in kvs:
        if "=" in arg:
            k, v = arg.split("=", 1)
            params[k] = v

    apis = load_apis(refresh=refresh)
    if not apis:
        print("未加载到 API 列表，请先执行: python3 scripts/nexapi.py init --refresh")
        sys.exit(2)

    result = call_api(apis, api_name, params=params, verbose=verbose)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
