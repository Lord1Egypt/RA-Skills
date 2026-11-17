#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
# ⚠️ 本文件是「京东黄金 (jdgold)」JoyCode Skill 的组成脚本。
# 执行任何脚本前，必须先阅读 Skill 根目录下的 SKILL.md，
# 严格遵循其中的执行契约、安全脱敏铁律与回复规范，
# 请勿脱离 SKILL.md 指引单独运行本脚本。
# ============================================================
"""cf-gold-ai 网关调用客户端。

所有业务接口走该客户端，统一管理：
  - 网关域名（环境变量 ``GOLD_BFF_BASE_URL`` 覆盖，默认正式网关占位）
  - HTTP 调用（GET / POST JSON）
  - 通用 Result 包络解包：``{"code": 0, "data": ..., "msg": ...}``
  - 错误分类（业务错误 / 网络错误）

约定：每个业务接口只在本文件里写一个相对路径常量；调试时通过环境变量
``GOLD_BFF_BASE_URL=http://localhost:8080`` 即可切到本地。

────────────────────────────────────────────────────────────────────
⚠️ 网关契约 SEAM（待金融网关接入文档确认）
  后端能力已由 HTTP Controller 改为 JSF 接口，经金融网关暴露为免鉴权 HTTPS。
  网关「JSF-over-HTTP」的请求格式（路径规则 / 信封 / 是否真免签名）尚未最终确认。
  下方 PATH_* 为逻辑占位；拿到网关接入文档后，只需在本文件集中调整：
    1. PATH_* 取值（网关实际路径）
    2. _parse_envelope（若网关信封不是 {code,data,msg}）
    3. _full_url / 请求头（若需网关路由头、appId 等）
  业务脚本只依赖这里的常量与 get/post_json/auth_* 函数，无需改动。
────────────────────────────────────────────────────────────────────
"""
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Optional

# ── 域名 + 接口路径 ────────────────────────────────────────────────

DEFAULT_BFF_BASE_URL = "https://ms.jr.jd.com/gw2/generic/cfGoldAi/pc/m"

# 授权代理（AuthService，模拟 PKCE）—— authCode 全程不离开后端。
PATH_AUTH_LOGIN_URL = "/getLoginUrl"   # getLoginUrl(challenge, state, localRedirect)
PATH_AUTH_STATUS = "/status"         # status(state) —— 沙箱轮询用，不带 verifier
PATH_AUTH_EXCHANGE = "/exchange"     # exchange(state, code=verifier)

# 业务接口路径（后端已转 JSF，经网关暴露；取值待网关契约确认）。
PATH_PRICE_QUERY = "/queryPrice"
PATH_HOLDINGS_QUERY = "/queryHoldings"
PATH_MORNING_REPORT = "/queryMorningReport"
PATH_NEWS_FLASH = "/queryNewsFlash"
PATH_TRADE_LIST = "/queryOrderList"
PATH_TRADE_SUM = "/queryOrderSum"
PATH_CONDITIONAL_LIST = "/queryList"
PATH_CONDITIONAL_DETAIL = "/queryDetail"
PATH_INCOME_CALENDAR = "/queryIncomeCalendar"

# 模拟大赛接口路径
PATH_SIM_ACCOUNT = "/queryAndInitAccount"
PATH_SIM_QUOTE_TIME_SHARING = "/getTimeSharingInfos"
PATH_SIM_QUOTE_KLINE = "/getKlineCandleDots"
PATH_SIM_BUY = "/buyGold"
PATH_SIM_SELL = "/sellGold"
PATH_SIM_TRADE_OVERVIEW = "/queryTradeOverview"
PATH_SIM_TRADE_RECORDS = "/queryTradeRecords"

DEFAULT_TIMEOUT_SEC = 15

# 账户被限制访问（接口 403）时对客的统一提示文案。
FORBIDDEN_USER_MESSAGE = "您的账户已被限制访问，如有疑问请联系京东黄金客服"


class BffError(RuntimeError):
    """BFF 返回业务失败。"""

    def __init__(self, code: int, message: str):
        super().__init__(f"BFF error code={code} msg={message}")
        self.code = code
        self.message = message


def base_url() -> str:
    """返回 BFF 根域名，可由环境变量覆盖。"""
    return os.environ.get("GOLD_BFF_BASE_URL", DEFAULT_BFF_BASE_URL).rstrip("/")


def _full_url(path: str, query: Optional[dict] = None) -> str:
    url = base_url() + path
    if query:
        kept = {k: v for k, v in query.items() if v is not None and v != ""}
        if kept:
            url += "?" + urllib.parse.urlencode(kept, doseq=True)
    return url


def set_claw(claw: str) -> None:
    """将命令行传入的 claw 客户端类型回填到环境变量 CLAW，供请求头统一读取。"""
    if claw:
        os.environ["CLAW"] = str(claw).strip()


def _claw_headers() -> dict:
    """返回带 claw 客户端类型的请求头；未配置时返回空字典。

    直接读取环境变量 CLAW 以保持与 jdjr_config 解耦（--claw 会回填到该环境变量）。
    """
    claw = os.environ.get("CLAW", "").strip()
    return {"x-claw": claw} if claw else {}


def _read_body(resp) -> str:
    raw = resp.read()
    return raw.decode("utf-8") if raw else ""


def _parse_envelope(body: str) -> Any:
    """解包络，失败抛 BffError。

    兼容双层嵌套信封（金融网关 + 业务应答）：
      - 外层（金融网关）：{resultCode, resultData, resultMsg, success}
      - 内层（业务应答）：{code: 200, msg: "success", data: {...}}
      - 单层（通用）：    {code: 0, data: ..., msg: ...}
    """
    if not body:
        raise BffError(-1, "empty response")
    try:
        payload = json.loads(body)
    except json.JSONDecodeError as e:
        raise BffError(-2, f"invalid JSON: {e}; body={body[:200]}") from e
    # 外层：金融网关信封
    if "resultCode" in payload or "resultData" in payload:
        code = payload.get("resultCode", -3)
        if code != 0:
            raise BffError(code, payload.get("resultMsg") or "")
        payload = payload.get("resultData")
        if not isinstance(payload, dict):
            return payload
    # 内层 / 单层：业务应答信封（code=0 或 code=200 均视为成功）
    if "code" in payload:
        code = payload.get("code", -3)
        if code not in (0, 200):
            raise BffError(code, payload.get("msg") or "")
        return payload.get("data")
    return payload


def get(path: str, query: Optional[dict] = None, *, timeout: int = DEFAULT_TIMEOUT_SEC) -> Any:
    """发起 GET，返回 data 字段。"""
    url = _full_url(path, query)
    req = urllib.request.Request(url, method="GET", headers=_claw_headers())
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return _parse_envelope(_read_body(resp))
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8")
        except Exception:
            pass
        if e.code == 403:
            raise BffError(403, FORBIDDEN_USER_MESSAGE) from e
        raise BffError(e.code, f"HTTP {e.code} {e.reason} body={body[:200]}") from e


def post_json(path: str, body: Any, *, timeout: int = DEFAULT_TIMEOUT_SEC) -> Any:
    """发起 POST JSON，返回 data 字段。"""
    url = _full_url(path)
    data = json.dumps(body or {}, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    headers.update(_claw_headers())
    req = urllib.request.Request(
        url, data=data, method="POST",
        headers=headers,
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return _parse_envelope(_read_body(resp))
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8")
        except Exception:
            pass
        if e.code == 403:
            raise BffError(403, FORBIDDEN_USER_MESSAGE) from e
        raise BffError(e.code, f"HTTP {e.code} {e.reason} body={body[:200]}") from e


# ── 授权代理（模拟 PKCE）专用封装 ──────────────────────────────────
# authCode 全程不离开后端；客户端只持 code_verifier，verifier 仅经 POST body 上送一次。

def auth_login_url(challenge: str, state: str,
                   local_redirect: Optional[str] = None) -> dict:
    """第一步：取授权 URL，并在后端绑定 state -> challenge。

    :param challenge: PKCE code_challenge（S256，base64url(sha256(verifier)) 去填充）
    :param state: 反 CSRF + 查找 key（CSPRNG 生成）
    :param local_redirect: 同机模式本地回调（如 http://127.0.0.1:8765/callback）；
                           沙箱模式传 None（后端不重定向，置就绪态供轮询）
    :return: {"authorizeUrl": "..."}
    """
    body = {"challenge": challenge, "state": state}
    if local_redirect:
        body["localRedirect"] = local_redirect
    return post_json(PATH_AUTH_LOGIN_URL, body)


def auth_status(state: str) -> dict:
    """查询授权状态（沙箱轮询用，不带 verifier）。:return: {"status": "pending|ready"}"""
    return post_json(PATH_AUTH_STATUS, {"state": state})


def auth_exchange(state: str, code: str) -> dict:
    """兑换 access_token。code 为 code_verifier 原文，仅经请求体上送。

    :return: {"accessToken": ..., "expiresIn": ..., "tokenType": ...}
    """
    return post_json(PATH_AUTH_EXCHANGE, {"state": state, "code": code})
