# -*- coding: utf-8 -*-
"""
米游社短信登录模块（OpenClaw 异步适配版）
参考: https://github.com/NuoManDai/mihoyo_sms_login

流程:
  1. sms_send_captcha(phone)         → 发送短信验证码，返回 action_type
  2. sms_login_by_captcha(phone, captcha, action_type)
                                     → 登录，返回 stoken + stuid + mid
  3. sms_get_full_cookies(stoken, stuid, mid)
                                     → 换取 ltoken + cookie_token，返回完整 cookies dict

依赖: httpx, pycryptodome (或 rsa)
"""

import asyncio
import base64
import hashlib
import json
import os
import random
import string
import time
import uuid
from typing import Any, Dict, Optional, Tuple
from pathlib import Path

import httpx

# ── 代理配置 ──────────────────────────────────────────────────────────────────

DATA_DIR = Path(__file__).parent.parent / "data"
PROXY_CONFIG_FILE = DATA_DIR / "proxy_config.json"


def _load_proxy_config() -> Dict:
    """加载代理配置"""
    if not PROXY_CONFIG_FILE.exists():
        return {}
    try:
        with open(PROXY_CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_proxy_config(config: Dict):
    """保存代理配置"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(PROXY_CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def _get_proxy() -> str:
    """
    获取代理 IP（带次数限制）
    每小时最多提取 max_per_hour 次，每次提取间隔 cooldown_seconds 秒
    """
    config = _load_proxy_config()
    api_url = config.get("api_url", "")
    if not api_url:
        return ""

    now = time.time()
    max_per_hour = config.get("max_per_hour", 20)
    cooldown = config.get("cooldown_seconds", 30)
    
    # 检查冷却时间
    last_fetch = config.get("last_fetch_time", 0)
    if now - last_fetch < cooldown:
        return ""  # 冷却中，跳过
    
    # 检查每小时限制
    hour_start = config.get("hour_start", 0)
    if now - hour_start > 3600:
        # 新的一小时，重置计数
        config["hour_start"] = now
        config["fetch_count_hour"] = 0
    
    if config.get("fetch_count_hour", 0) >= max_per_hour:
        return ""  # 超过每小时限制
    
    try:
        # 获取代理 IP
        import urllib.request
        req = urllib.request.Request(api_url, method="GET")
        with urllib.request.urlopen(req, timeout=10) as resp:
            proxy_ip = resp.read().decode().strip()
        
        if proxy_ip:
            config["last_fetch_time"] = now
            config["fetch_count_hour"] = config.get("fetch_count_hour", 0) + 1
            _save_proxy_config(config)
            return f"http://{proxy_ip}"
    except Exception:
        pass
    
    return ""


# ── RSA 加密 ──────────────────────────────────────────────────────────────────

PUB_KEY_PEM = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDDvekdPMHN3AYhm/vktJT+YJr7
cI5DcsNKqdsx5DZX0gDuWFuIjzdwButrIYPNmRJ1G8ybDIF7oDW2eEpm5sMbL9zs
9ExXCdvqrn51qELbqj0XxtMTIpaCHFSI50PfPpTFV9Xt/hmyVwokoOXFlAEgCn+Q
CgGs52bFoYMtyi+xEQIDAQAB
-----END PUBLIC KEY-----"""


def _rsa_encrypt(plaintext: str) -> str:
    """RSA 加密（PKCS1_v1_5），返回 base64 字符串"""
    try:
        from Crypto.PublicKey import RSA
        from Crypto.Cipher import PKCS1_v1_5
        key = RSA.import_key(PUB_KEY_PEM)
        cipher = PKCS1_v1_5.new(key)
        return base64.b64encode(cipher.encrypt(plaintext.encode())).decode()
    except ImportError:
        pass
    try:
        import rsa as rsa_lib
        pub = rsa_lib.PublicKey.load_pkcs1_openssl_pem(PUB_KEY_PEM.encode())
        return base64.b64encode(rsa_lib.encrypt(plaintext.encode(), pub)).decode()
    except ImportError:
        raise RuntimeError("需要安装 pycryptodome 或 rsa: pip install pycryptodome")


# ── 常量 ──────────────────────────────────────────────────────────────────────

BBS_VERSION = "2.102.1"
BBS_UA = f"Mozilla/5.0 (Linux; Android 12) Mobile miHoYoBBS/{BBS_VERSION}"

PASSPORT_BASE = "https://passport-api.miyoushe.com/"
CREATE_CAPTCHA_URL = f"{PASSPORT_BASE}account/ma-cn-verifier/verifier/createLoginCaptcha"
LOGIN_APP_URL = f"{PASSPORT_BASE}account/ma-cn-passport/app/loginByMobileCaptcha"
LOGIN_WEB_URL = f"{PASSPORT_BASE}account/ma-cn-passport/web/loginByMobileCaptcha"

TAKUMI_BASE = "https://passport-api.mihoyo.com/"
GET_LTOKEN_URL = f"{TAKUMI_BASE}account/auth/api/getLTokenBySToken"
GET_COOKIE_TOKEN_URL = f"{TAKUMI_BASE}account/auth/api/getCookieAccountInfoBySToken"

APP_ID = "bll8iq97cem8"

# DS salts
DS_SALT_CN_SIGNIN = "LyD1rXqMv2GJhnwdvCBjFOKGiKuLY3aO"
DS_SALT_CN_PASSPORT = "JwYDpKvLj6MrMqqYU6jTKF17KNO2PXoS"
DS_SALT_X4 = "xV8v4Qu54lUKrEYFZkJhB8cuOh9Asafs"


# ── DS 签名 ───────────────────────────────────────────────────────────────────

def _ds_simple(salt: str = DS_SALT_CN_SIGNIN) -> str:
    t = str(int(time.time()))
    r = "".join(random.choices(string.ascii_letters, k=6))
    h = hashlib.md5(f"salt={salt}&t={t}&r={r}".encode()).hexdigest()
    return f"{t},{r},{h}"


def _ds_passport(body_dict: dict) -> str:
    t = str(int(time.time()))
    r = "".join(random.choices(string.ascii_letters, k=6))
    b = json.dumps(body_dict)
    h = hashlib.md5(f"salt={DS_SALT_CN_PASSPORT}&t={t}&r={r}&b={b}&q=".encode()).hexdigest()
    return f"{t},{r},{h}"


def _ds_x4(query: str = "") -> str:
    t = str(int(time.time()))
    r = str(random.randint(100000, 200000))
    h = hashlib.md5(f"salt={DS_SALT_X4}&t={t}&r={r}&b=&q={query}".encode()).hexdigest()
    return f"{t},{r},{h}"


def _device_id() -> str:
    return str(uuid.uuid4())


def _device_fp() -> str:
    return "".join(random.choices("0123456789abcdef", k=13))


# ── 请求头 ────────────────────────────────────────────────────────────────────

def _sms_headers(ds: str, device_id: str, device_fp: str, aigis: str = "") -> Dict[str, str]:
    return {
        "x-rpc-app_id": APP_ID,
        "x-rpc-client_type": "4",
        "x-rpc-source": "v2.webLogin",
        "x-rpc-sdk_version": "2.31.0",
        "x-rpc-game_biz": "bbs_cn",
        "x-rpc-device_fp": device_fp,
        "x-rpc-device_id": device_id,
        "x-rpc-device_model": "Firefox%20131.0",
        "x-rpc-device_name": "Firefox",
        "x-rpc-aigis": aigis,
        "ds": ds,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
        "content-type": "application/json",
        "referer": "https://user.miyoushe.com/",
    }


def _token_exchange_headers(stoken: str, mid: str, query_str: str, device_id: str, device_fp: str) -> Dict[str, str]:
    return {
        "user-agent": BBS_UA,
        "x-rpc-app_version": BBS_VERSION,
        "x-rpc-client_type": "5",
        "x-requested-with": "com.mihoyo.hyperion",
        "referer": "https://webstatic.mihoyo.com",
        "x-rpc-device_id": device_id,
        "x-rpc-device_fp": device_fp,
        "ds": _ds_x4(query=query_str),
        "cookie": f"mid={mid};stoken={stoken}",
    }


# ── 异步 API ──────────────────────────────────────────────────────────────────

async def sms_send_captcha(phone: str, aigis: str = "",
                            device_id: str = None, device_fp: str = None
                            ) -> Dict[str, Any]:
    """
    发送短信验证码。
    :return: {"success": bool, "action_type": str, "aigis": str, "retcode": int, "message": str,
              "device_id": str, "device_fp": str}
    """
    did = device_id or _device_id()
    dfp = device_fp or _device_fp()
    body = {
        "area_code": _rsa_encrypt("+86"),
        "mobile": _rsa_encrypt(phone),
    }
    headers = _sms_headers(_ds_simple(), did, dfp, aigis)
    try:
        proxy = _get_proxy()
        client_kwargs = {"timeout": 20}
        if proxy:
            client_kwargs["proxy"] = proxy
        async with httpx.AsyncClient(**client_kwargs) as client:
            resp = await client.post(CREATE_CAPTCHA_URL, headers=headers, json=body, timeout=20)
        data = resp.json()
        if data.get("retcode") == 0:
            return {
                "success": True,
                "action_type": data.get("data", {}).get("action_type", "login"),
                "retcode": 0,
                "message": "OK",
                "device_id": did,
                "device_fp": dfp,
            }
        aigis_header = resp.headers.get("x-rpc-aigis", "")
        return {
            "success": False,
            "retcode": data.get("retcode"),
            "message": data.get("message", ""),
            "aigis": aigis_header,
            "device_id": did,
            "device_fp": dfp,
        }
    except Exception as e:
        return {"success": False, "retcode": -1, "message": str(e), "device_id": did, "device_fp": dfp}


async def sms_login_by_captcha(phone: str, captcha: str, action_type: str = "login",
                                aigis: str = "",
                                device_id: str = None, device_fp: str = None
                                ) -> Dict[str, Any]:
    """
    使用短信验证码登录，获取 stoken。
    :return: {"success": bool, "stoken": str, "stuid": str, "mid": str, ...}
    """
    did = device_id or _device_id()
    dfp = device_fp or _device_fp()
    body = {
        "area_code": _rsa_encrypt("+86"),
        "mobile": _rsa_encrypt(phone),
        "captcha": captcha,
    }

    # 优先尝试 app 端点（body 返回 stoken）
    headers = _sms_headers(_ds_passport(body), did, dfp, aigis)
    try:
        proxy = _get_proxy()
        client_kwargs = {"timeout": 20}
        if proxy:
            client_kwargs["proxy"] = proxy
        async with httpx.AsyncClient(**client_kwargs) as client:
            resp = await client.post(LOGIN_APP_URL, headers=headers, json=body, timeout=20)
        data = resp.json()
        if data.get("retcode") == 0:
            login_data = data.get("data", {})
            token_info = login_data.get("token", {})
            user_info = login_data.get("user_info", {})
            stoken = token_info.get("token", "")
            aid = user_info.get("aid", "")
            mid = user_info.get("mid", "")
            if not stoken:
                # 尝试从 cookies 获取
                ck = dict(resp.cookies)
                stoken = ck.get("stoken", "") or ck.get("stoken_v2", "")
                aid = aid or ck.get("stuid", "") or ck.get("account_id", "")
                mid = mid or ck.get("mid", "")
            if stoken:
                return {"success": True, "stoken": stoken, "stuid": aid, "mid": mid}
        # app 端点失败，尝试 web 端点
        if data.get("retcode") != 0:
            headers2 = _sms_headers(_ds_passport(body), did, dfp, aigis)
            proxy = _get_proxy()
            client_kwargs = {"timeout": 20}
            if proxy:
                client_kwargs["proxy"] = proxy
            async with httpx.AsyncClient(**client_kwargs) as client:
                resp2 = await client.post(LOGIN_WEB_URL, headers=headers2, json=body, timeout=20)
            data2 = resp2.json()
            if data2.get("retcode") == 0:
                ck = dict(resp2.cookies)
                user_info = data2.get("data", {}).get("user_info", {})
                stoken = ck.get("stoken", "") or ck.get("stoken_v2", "")
                aid = user_info.get("aid", "") or ck.get("stuid", "") or ck.get("account_id", "")
                mid = user_info.get("mid", "") or ck.get("mid", "")
                return {"success": True, "stoken": stoken, "stuid": aid, "mid": mid}
            aigis_header = resp2.headers.get("x-rpc-aigis", "")
            return {
                "success": False,
                "retcode": data2.get("retcode"),
                "message": data2.get("message", ""),
                "aigis": aigis_header,
            }
        aigis_header = resp.headers.get("x-rpc-aigis", "")
        return {
            "success": False,
            "retcode": data.get("retcode"),
            "message": data.get("message", ""),
            "aigis": aigis_header,
        }
    except Exception as e:
        return {"success": False, "retcode": -1, "message": str(e)}


async def sms_get_full_cookies(stoken: str, stuid: str, mid: str,
                                device_id: str = None, device_fp: str = None
                                ) -> Dict[str, str]:
    """
    用 stoken 换取 ltoken + cookie_token，返回完整 cookies dict。
    """
    did = device_id or _device_id()
    dfp = device_fp or _device_fp()
    cookies: Dict[str, str] = {
        "account_id": stuid,
        "stuid": stuid,
        "stoken": stoken,
        "mid": mid,
        "login_uid": stuid,
    }

    # 换 ltoken
    try:
        query_str = f"stoken={stoken}"
        headers = _token_exchange_headers(stoken, mid, query_str, did, dfp)
        proxy = _get_proxy()
        client_kwargs = {"timeout": 20}
        if proxy:
            client_kwargs["proxy"] = proxy
        async with httpx.AsyncClient(**client_kwargs) as client:
            res = await client.get(GET_LTOKEN_URL, headers=headers,
                                   params={"stoken": stoken}, timeout=15)
        data = res.json()
        if data.get("retcode") == 0:
            cookies["ltoken"] = data["data"]["ltoken"]
            cookies["ltuid"] = stuid
    except Exception:
        pass

    # 换 cookie_token
    try:
        query_str = f"stoken={stoken}"
        headers = _token_exchange_headers(stoken, mid, query_str, did, dfp)
        proxy = _get_proxy()
        client_kwargs = {"timeout": 20}
        if proxy:
            client_kwargs["proxy"] = proxy
        async with httpx.AsyncClient(**client_kwargs) as client:
            res = await client.get(GET_COOKIE_TOKEN_URL, headers=headers,
                                   params={"stoken": stoken}, timeout=15)
        data = res.json()
        if data.get("retcode") == 0:
            cookies["cookie_token"] = data["data"]["cookie_token"]
    except Exception:
        pass

    return cookies
