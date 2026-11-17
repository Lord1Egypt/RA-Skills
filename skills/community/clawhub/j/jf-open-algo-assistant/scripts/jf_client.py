#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
杰峰开放平台 AI 算法客户端
签名算法严格移植自官方 SDK: github.com/jlinklab/jlink-restful-java-demo-v3
  src/main/java/jlink/restful/java/sdk/util/JLinkSignatureUtil.java

用法:
  python jf_client.py config set --uuid xx --appkey xx --appsecret xx [--movecard 2] [--endpoint https://api.jftechws.com]
  python jf_client.py config show
  python jf_client.py test                     # 调 getAlgoExperienceList 验证签名连通性
  python jf_client.py open <appUuid> [--version v1.0]
  python jf_client.py call <appUuid> --image <path|url> --sn <SN> [--conf 0.3] [--config-json '{...}']
"""
import argparse
import base64
import hashlib
import json
import os
import sys
import time
import urllib.request
import urllib.error

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(os.path.dirname(SCRIPT_DIR), "config.json")
DEFAULT_ENDPOINT = "https://api.jftechws.com"
SUCCESS_CODE = 2000
ALREADY_OPEN_CODE = 12537  # 已开通（user already has the permission），视为成功


# ---------------- 签名（官方 SDK 逐行移植） ----------------
def _change(eb, move_card):
    arr = bytearray(eb)
    n = len(arr)
    for i in range(n):
        temp = arr[i] if ((i % move_card) > ((n - i) % move_card)) else arr[n - (i + 1)]
        arr[i] = arr[n - (i + 1)]
        arr[n - (i + 1)] = temp
    return arr


def _merge(eb, cb):
    n = len(eb)
    t = bytearray(2 * n)
    for i in range(n):
        t[i] = eb[i]
        t[2 * n - 1 - i] = cb[i]
    return t


def signature(uuid, app_key, app_secret, time_millis, move_card=2):
    s = uuid + app_key + app_secret + time_millis
    eb = s.encode("iso-8859-1")
    cb = _change(eb, move_card)
    return hashlib.md5(bytes(_merge(eb, cb))).hexdigest()


def time_millis(counter=1):
    """7位计数器 + 本地毫秒时间戳（与官方 JLinkTimeMillisUtil 一致）"""
    return "{:07d}{}".format(counter, int(time.time() * 1000))


# ---------------- 配置 ----------------
def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    try:
        with open(CONFIG_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def require_config():
    cfg = load_config()
    missing = [k for k in ("uuid", "appKey", "appSecret") if not cfg.get(k)]
    if missing:
        print(json.dumps({"ok": False, "error": "config_missing", "missing": missing,
                          "hint": "先执行 config set 配置凭证"}, ensure_ascii=False))
        sys.exit(2)
    cfg.setdefault("moveCard", 2)
    cfg.setdefault("endpoint", DEFAULT_ENDPOINT)
    return cfg


def auth_headers(cfg):
    ts = time_millis()
    return {
        "Content-Type": "application/json",
        "uuid": cfg["uuid"],
        "appKey": cfg["appKey"],
        "timeMillis": ts,
        "signature": signature(cfg["uuid"], cfg["appKey"], cfg["appSecret"], ts, cfg["moveCard"]),
    }


def api_call(cfg, path, body, timeout=60):
    url = cfg["endpoint"].rstrip("/") + path
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
                                 headers=auth_headers(cfg), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        text = e.read().decode("utf-8", errors="replace")
        try:
            return json.loads(text)
        except Exception:
            return {"code": e.code, "msg": text[:500], "data": None}
    except Exception as e:
        return {"code": -1, "msg": "network_error: {}".format(e), "data": None}


# ---------------- 命令 ----------------
def cmd_config_set(args):
    cfg = load_config()
    if args.uuid: cfg["uuid"] = args.uuid
    if args.appkey: cfg["appKey"] = args.appkey
    if args.appsecret: cfg["appSecret"] = args.appsecret
    if args.movecard is not None: cfg["moveCard"] = args.movecard
    if args.endpoint: cfg["endpoint"] = args.endpoint
    cfg.setdefault("moveCard", 2)
    cfg.setdefault("endpoint", DEFAULT_ENDPOINT)
    save_config(cfg)
    masked = dict(cfg)
    if masked.get("appSecret"):
        masked["appSecret"] = masked["appSecret"][:4] + "****"
    print(json.dumps({"ok": True, "config": masked, "path": CONFIG_PATH}, ensure_ascii=False))


def cmd_config_show(_):
    cfg = load_config()
    if not cfg:
        print(json.dumps({"ok": False, "configured": False}, ensure_ascii=False))
        return
    masked = dict(cfg)
    if masked.get("appSecret"):
        masked["appSecret"] = masked["appSecret"][:4] + "****"
    print(json.dumps({"ok": True, "configured": True, "config": masked}, ensure_ascii=False))


def cmd_test(_):
    cfg = require_config()
    resp = api_call(cfg, "/openai/algorithm/application/v3/getAlgoExperienceList",
                    {"page": 1, "rows": 5, "lang": "zh"})
    ok = resp.get("code") == SUCCESS_CODE
    print(json.dumps({"ok": ok, "code": resp.get("code"), "msg": resp.get("msg"),
                      "hint": None if ok else "签名或凭证异常：请核对 uuid/appKey/appSecret/moveCard"},
                     ensure_ascii=False))
    sys.exit(0 if ok else 1)


def cmd_open(args):
    cfg = require_config()
    resp = api_call(cfg, "/openai/algorithm/application/v3/open",
                    {"algoAppUuid": args.app_uuid, "algoAppVersion": args.version})
    ok = resp.get("code") in (SUCCESS_CODE, ALREADY_OPEN_CODE)
    print(json.dumps({"ok": ok, "appUuid": args.app_uuid, "code": resp.get("code"),
                      "msg": resp.get("msg")}, ensure_ascii=False))
    sys.exit(0 if ok else 1)


def cmd_call(args):
    cfg = require_config()
    img = args.image
    if img.lower().startswith(("http://", "https://")):
        image_obj = {"url": img, "sn": args.sn}
    else:
        if not os.path.exists(img):
            print(json.dumps({"ok": False, "error": "image_not_found", "path": img}, ensure_ascii=False))
            sys.exit(2)
        with open(img, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        image_obj = {"b64": b64, "sn": args.sn}

    app_config = {"confThreshold": args.conf}
    if args.config_json:
        try:
            app_config.update(json.loads(args.config_json))
        except Exception as e:
            print(json.dumps({"ok": False, "error": "bad_config_json", "detail": str(e)}, ensure_ascii=False))
            sys.exit(2)

    body = {"appUuid": args.app_uuid, "image": image_obj, "appConfig": app_config}
    resp = api_call(cfg, "/openai/algorithm/application/v3/callApp", body, timeout=args.timeout)
    ok = resp.get("code") == SUCCESS_CODE
    out = {"ok": ok, "appUuid": args.app_uuid, "code": resp.get("code"),
           "msg": resp.get("msg"), "data": resp.get("data")}
    if not ok and resp.get("code") in (None, -1):
        out["hint"] = "网络异常或端点错误，检查 endpoint 配置"
    print(json.dumps(out, ensure_ascii=False))
    sys.exit(0 if ok else 1)


def main():
    p = argparse.ArgumentParser(description="杰峰开放平台AI算法客户端")
    sub = p.add_subparsers(dest="cmd", required=True)

    pc = sub.add_parser("config")
    pcsub = pc.add_subparsers(dest="subcmd", required=True)
    pset = pcsub.add_parser("set")
    pset.add_argument("--uuid")
    pset.add_argument("--appkey")
    pset.add_argument("--appsecret")
    pset.add_argument("--movecard", type=int)
    pset.add_argument("--endpoint")
    pset.set_defaults(func=cmd_config_set)
    pshow = pcsub.add_parser("show")
    pshow.set_defaults(func=cmd_config_show)

    pt = sub.add_parser("test")
    pt.set_defaults(func=cmd_test)

    po = sub.add_parser("open")
    po.add_argument("app_uuid")
    po.add_argument("--version", default="v1.0")
    po.set_defaults(func=cmd_open)

    pcall = sub.add_parser("call")
    pcall.add_argument("app_uuid")
    pcall.add_argument("--image", required=True)
    pcall.add_argument("--sn", required=True)
    pcall.add_argument("--conf", type=float, default=0.3)
    pcall.add_argument("--config-json", default=None)
    pcall.add_argument("--timeout", type=int, default=60)
    pcall.set_defaults(func=cmd_call)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
