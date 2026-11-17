"""ocal_graph — Graph API 调用层：请求、重试、翻页。"""
import requests, time

from ocal_errors import CalError
from ocal_auth import setup_hint
from ocal_i18n import t
from ocal_time import LOCAL_TZ_NAME

GRAPH_BASE = "https://graph.microsoft.com/v1.0"

# ── API 调用 ──────────────────────────────────────


def _retry_after_seconds(resp):
    """从 429 响应里取出 Retry-After 的秒数（可能带小数）。

    :param resp: requests 响应对象
    :return: 秒数；头缺失或解析不了返回 None
    """
    raw = resp.headers.get("Retry-After") if resp.headers else None
    if raw is None:
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def _call(method, endpoint, token, data=None, prefer_immutable=False):
    """发一次 Graph 请求；endpoint 以 http 开头时当完整 URL 用（翻页场景）。

    重试规则：只在没收到响应或状态码明确可重试时重试——
    - 429：按 Retry-After 等（可带小数），没有就 1/2/4s 退避，最多 3 次重试
    - 500/503：同样退避，但只有 GET/DELETE 会重试；POST/PATCH 不重试，
      万一服务端其实已经处理了，重发会造出重复数据
    - 连接错误/超时：GET/DELETE 重试 2 次（1s/3s）；POST/PATCH 不重试，
      请求可能已经提交，让用户先 list 确认而不是盲目重发

    :param method: HTTP 方法（GET/POST/PATCH/DELETE）
    :param endpoint: 形如 /me/events 的路径，或带 http 的完整 URL
    :param token: 访问令牌
    :param data: 请求体（POST/PATCH 用）
    :param prefer_immutable: 要求不可变 ID——事件跨容器移动时 ID 不变，删除/更新更稳
    :return: 响应 JSON；204 无内容时返回 None
    :raises CalError: 网络错误、登录过期、API 报错（已转成友好文案）
    """
    headers = {"Authorization": f"Bearer {token}"}
    # 让 Graph 按本地时区返回 start/end（不带这个头默认返回 UTC，会引发时区歧义）
    prefer_parts = [f'outlook.timezone="{LOCAL_TZ_NAME}"']
    if prefer_immutable:
        prefer_parts.append('IdType="ImmutableId"')
    headers["Prefer"] = ", ".join(prefer_parts)
    if data:
        headers["Content-Type"] = "application/json"
    url = endpoint if endpoint.startswith("http") else f"{GRAPH_BASE}{endpoint}"
    tz_stripped = False  # 时区头只允许剥一次，防止循环
    for attempt in range(4):  # 1 次初始 + 最多 3 次重试
        try:
            resp = requests.request(method, url, headers=headers, json=data, timeout=(10, 30))
        except requests.exceptions.RequestException as e:
            if method in ("GET", "DELETE") and attempt < 2:
                time.sleep((1, 3)[attempt])
                continue
            if method in ("POST", "PATCH"):
                raise CalError(t("err_network_maybe", e=e))
            raise CalError(t("err_network", e=e))
        if resp.status_code == 429:
            # 限流：Retry-After 头优先；没有就 1/2/4s 退避；所有方法都安全重试
            wait = _retry_after_seconds(resp)
            if wait is None:
                wait = (1, 2, 4)[min(attempt, 2)]
            if attempt < 3:
                time.sleep(min(wait, 30))
                continue
        elif resp.status_code in (500, 503) and method in ("GET", "DELETE"):
            # 服务端错误：只有幂等的 GET/DELETE 重试（POST/PATCH 落回下面的 API 错误）
            if attempt < 3:
                time.sleep((1, 2, 4)[min(attempt, 2)])
                continue
        if resp.status_code == 401:
            raise CalError(t("err_login_expired", hint=setup_hint()))
        if resp.status_code >= 400:
            try:
                err = resp.json().get('error', {})
                msg = err.get('message', resp.text[:200])
                code = err.get('code', '')
            except Exception:
                msg, code = resp.text[:200], ''
            # 防御：个别邮箱/时区名不支持 Prefer 头时 Graph 返回 400，去掉时区头后
            # 走回主循环重发一次（同样经过 429/500/网络异常的重试与错误映射）；
            # Graph 默认按 UTC 返回，_parse_dt 会自行换算成本地时间，显示结果一致
            tz_bad = ("timezone" in msg.lower() or "time zone" in msg.lower()
                      or "timezone" in code.lower())
            if (resp.status_code == 400 and tz_bad and not tz_stripped
                    and "outlook.timezone" in headers.get("Prefer", "")):
                tz_stripped = True
                headers["Prefer"] = headers["Prefer"].replace(f'outlook.timezone="{LOCAL_TZ_NAME}", ', "").replace(
                    f'outlook.timezone="{LOCAL_TZ_NAME}"', "")
                if not headers["Prefer"].strip():
                    headers.pop("Prefer", None)
                continue
            if code == 'ErrorOccurrenceCrossingBoundary':
                raise CalError(t("err_crossing"))
            if code == 'ErrorItemNotFound':
                raise CalError(t("err_not_found"))
            raise CalError(t("err_api", code=resp.status_code, msg=msg))
        if resp.status_code == 204:
            return None
        return resp.json()


def _get_all(url, token, prefer_immutable=False):
    """拉全部分页结果：跟着 @odata.nextLink 一直翻到没有下一页。

    :param url: 起始查询 URL
    :param token: 访问令牌
    :param prefer_immutable: 透传给 _call
    :return: 各页 value 拼成的列表
    """
    items = []
    pages = 0
    while url and pages < 200:
        # 200 页是防御性上限（正常日历远到不了）：nextLink 异常重复时
        # 不会死循环，也不至于静默截断真实数据
        pages += 1
        data = _call("GET", url, token, prefer_immutable=prefer_immutable)
        items.extend(data.get('value', []))
        url = data.get('@odata.nextLink')
    return items
