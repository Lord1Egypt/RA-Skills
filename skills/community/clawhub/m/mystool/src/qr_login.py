"""
米游社扫码登录模块（独立）
流程：
  1. fetch_qrcode()  → 获取二维码 URL + ticket
  2. 展示二维码给用户（图片链接）
  3. 轮询 query_qrcode() → 等待用户扫码确认
  4. 扫码成功后用 game_token 换取完整 Cookie 套装
  5. 调用 store.add_account() 保存

提示文字：用米游社App 扫码，自动获取完整 Cookie
依赖: httpx, qrcode (可选，用于生成终端二维码)
"""

import asyncio
import hashlib
import json
import random
import string
import time
import uuid
from typing import Dict, Optional, Tuple

import httpx

# ── 常量 ──────────────────────────────────────────────────────────────────────

APP_ID = "4"  # 原神 app_id，用于扫码登录
APP_VERSION = "2.44.1"
UA_MOBILE = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBS/2.44.1"
)

URL_FETCH_QRCODE = "https://hk4e-sdk.mihoyo.com/hk4e_cn/combo/panda/qrcode/fetch"
URL_QUERY_QRCODE = "https://hk4e-sdk.mihoyo.com/hk4e_cn/combo/panda/qrcode/query"
URL_GET_TOKEN_BY_GAME_TOKEN = (
    "https://api-takumi.mihoyo.com/account/ma-cn-session/app/getTokenByGameToken"
)
URL_STOKEN_V2_BY_V1 = (
    "https://passport-api.mihoyo.com/account/ma-cn-session/app/getTokenBySToken"
)
URL_COOKIE_TOKEN_BY_STOKEN = (
    "https://passport-api.mihoyo.com/account/auth/api/getCookieAccountInfoBySToken"
)
URL_LTOKEN_BY_STOKEN = (
    "https://passport-api.mihoyo.com/account/auth/api/getLTokenBySToken"
)

HEADERS_BASE = {
    "User-Agent": UA_MOBILE,
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh-Hans;q=0.9",
    "x-rpc-app_version": APP_VERSION,
    "x-rpc-client_type": "4",
    "Content-Type": "application/json; charset=utf-8",
}

HEADERS_PASSPORT = {
    **HEADERS_BASE,
    "x-rpc-client_type": "1",
    "x-rpc-game_biz": "bbs_cn",
    "x-rpc-sdk_version": "1.6.1",
}

POLL_INTERVAL = 3    # 轮询间隔（秒）
POLL_TIMEOUT  = 180  # 最长等待（秒）


# ── 工具 ──────────────────────────────────────────────────────────────────────

def _device_id() -> str:
    return str(uuid.uuid4()).upper()


def _generate_ds(salt: str = "IZPgfb0dRPtBeLuFkdDznSmmkB5W5EXc",
                 body: str = "", query: str = "") -> str:
    t = str(int(time.time()))
    r = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    h = hashlib.md5(f"salt={salt}&t={t}&r={r}&b={body}&q={query}".encode()).hexdigest()
    return f"{t},{r},{h}"


# ── Step 1: 获取二维码 ─────────────────────────────────────────────────────────

async def fetch_qrcode() -> Tuple[bool, Optional[str], Optional[str], Optional[str]]:
    """
    申请扫码登录二维码。
    :return: (ok, qrcode_url, ticket, device)
    """
    device = _device_id()
    payload = {"app_id": APP_ID, "device": device}
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                URL_FETCH_QRCODE,
                headers=HEADERS_BASE,
                json=payload,
                timeout=15,
            )
        data = res.json()
        if data.get("retcode") == 0:
            url = data["data"]["url"]
            from urllib.parse import urlparse, parse_qs
            ticket = parse_qs(urlparse(url).query).get("ticket", [None])[0]
            return True, url, ticket, device
        return False, None, None, None
    except Exception:
        return False, None, None, None


# ── Step 2: 生成二维码图片 URL ───────────────────────────────────────────────

def qrcode_to_image_url(url: str, size: int = 300) -> str:
    """将 URL 转为二维码图片 URL（使用 pwmqr.com API）"""
    import urllib.parse
    encoded = urllib.parse.quote(url, safe='')
    return f"https://www.pwmqr.com/qrcodeapi/?size={size}x{size}&data={encoded}"


def qrcode_to_text(url: str) -> Optional[str]:
    """将 URL 转为终端可显示的二维码文本（需要 qrcode 库）"""
    try:
        import qrcode
        from io import StringIO
        qr = qrcode.QRCode(border=1)
        qr.add_data(url)
        qr.make(fit=True)
        f = StringIO()
        qr.print_ascii(out=f, invert=True)
        return f.getvalue()
    except ImportError:
        return None


# ── Step 3: 轮询扫码状态 ───────────────────────────────────────────────────────

async def query_qrcode(ticket: str, device: str = "") -> Tuple[str, Optional[Dict]]:
    """
    轮询二维码扫描状态。
    :return: (status, raw_data)
      status: "Init" | "Scanned" | "Confirmed" | "Expired" | "error"
    """
    payload = {"app_id": APP_ID, "ticket": ticket, "device": device}
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                URL_QUERY_QRCODE,
                headers=HEADERS_BASE,
                json=payload,
                timeout=15,
            )
        data = res.json()
        retcode = data.get("retcode", -1)

        if retcode != 0:
            if retcode in (-3501, -3505):
                return "Expired", None
            return "Init", None

        stat = data["data"].get("stat", "Init")
        payload_data = data["data"].get("payload", {})

        if stat == "Confirmed" and payload_data:
            raw = json.loads(payload_data.get("raw", "{}"))
            return "Confirmed", raw

        return stat, None
    except Exception:
        return "error", None


# ── Step 4: game_token → 完整 Cookie 套装 ─────────────────────────────────────

async def game_token_to_cookies(uid: str, game_token: str) -> Tuple[bool, Optional[Dict[str, str]]]:
    """
    用扫码得到的 game_token 换取完整 Cookie 套装：
    stoken_v1 → stoken_v2 + mid → cookie_token + ltoken
    """
    cookies: Dict[str, str] = {"account_id": uid, "stuid": uid}

    # 1. game_token → stoken_v1
    try:
        body = json.dumps({"account_id": int(uid), "game_token": game_token})
        h = {**HEADERS_BASE, "DS": _generate_ds(body=body)}
        async with httpx.AsyncClient() as client:
            res = await client.post(
                URL_GET_TOKEN_BY_GAME_TOKEN,
                headers=h,
                json={"account_id": int(uid), "game_token": game_token},
                timeout=15,
            )
        data = res.json()
        if data.get("retcode") != 0:
            return False, None
        token_list = data["data"].get("token", {})
        stoken_v1 = token_list.get("token")
        if not stoken_v1:
            return False, None
        cookies["stoken"] = stoken_v1
    except Exception:
        return False, None

    # 2. stoken_v1 → stoken_v2 + mid
    try:
        h = {**HEADERS_PASSPORT, "x-rpc-device_id": _device_id()}
        async with httpx.AsyncClient() as client:
            res = await client.post(
                URL_STOKEN_V2_BY_V1,
                headers=h,
                cookies={"stoken": stoken_v1, "stuid": uid},
                json={"app_id": "bll8iq97cem8", "dst_token_types": [1, 2, 4]},
                timeout=15,
            )
        data = res.json()
        if data.get("retcode") == 0:
            token_map = {t["token_type"]: t["token"] for t in data["data"].get("tokens", [])}
            stoken_v2 = token_map.get(2) or token_map.get(1)
            mid = data["data"].get("user_info", {}).get("mid", "")
            if stoken_v2:
                cookies["stoken_v2"] = stoken_v2
            if mid:
                cookies["mid"] = mid
                cookies["login_uid"] = uid
    except Exception:
        pass  # stoken_v2 可选，继续

    # 3. stoken → cookie_token
    try:
        h = {**HEADERS_PASSPORT, "x-rpc-device_id": _device_id()}
        ck = {"stoken": cookies.get("stoken_v2", stoken_v1), "stuid": uid, "mid": cookies.get("mid", "")}
        async with httpx.AsyncClient() as client:
            res = await client.get(
                URL_COOKIE_TOKEN_BY_STOKEN,
                headers=h,
                cookies=ck,
                timeout=15,
            )
        data = res.json()
        if data.get("retcode") == 0:
            cookies["cookie_token"] = data["data"]["cookie_token"]
            if not cookies.get("account_id"):
                cookies["account_id"] = data["data"].get("uid", uid)
    except Exception:
        pass

    # 4. stoken → ltoken
    try:
        h = {**HEADERS_PASSPORT, "x-rpc-device_id": _device_id()}
        ck = {"stoken": cookies.get("stoken_v2", stoken_v1), "stuid": uid, "mid": cookies.get("mid", "")}
        async with httpx.AsyncClient() as client:
            res = await client.get(
                URL_LTOKEN_BY_STOKEN,
                headers=h,
                cookies=ck,
                timeout=15,
            )
        data = res.json()
        if data.get("retcode") == 0:
            cookies["ltoken"] = data["data"]["ltoken"]
            cookies["ltuid"] = uid
    except Exception:
        pass

    if cookies.get("stoken") and cookies.get("account_id"):
        return True, cookies
    return False, None
