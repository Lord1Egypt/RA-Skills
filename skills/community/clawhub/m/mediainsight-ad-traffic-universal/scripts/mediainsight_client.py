from __future__ import annotations

from http.cookiejar import Cookie, CookieJar
from http.cookies import SimpleCookie
import json
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin, urlparse
from urllib.request import HTTPCookieProcessor, OpenerDirector, Request, build_opener


DEFAULT_BASE_URL = "https://mediainsight.cn.miaozhen.com/api_v2"
DEFAULT_SESSION_FILE = Path(".mediainsight-session.json")
DEFAULT_MCP_URL = "https://open-api-mediainsight.cn.miaozhen.com/mcp_server/mcp"
AD_TRAFFIC_ONLY_FORBIDDEN_KEYS = frozenset(
    {
        "reportTouchMediaHavior",
        "reportArgsTouchMedia",
        "forcesForMediaInsight",
        "reportArgsReachCurve",
        "reportArgsReachCurveAvg",
        "reportArgsReachCurveAverage",
        "reportArgsReachCurveCustom",
    }
)


class MediaInsightError(RuntimeError):
    """Raised when a MediaInsight request fails."""


def _friendly_http_error(context: str, status_code: int, body: str) -> str:
    detail = body.strip() or "empty response body"
    if status_code == 401:
        return (
            f"{context} failed with HTTP 401: token may be expired, revoked, or unauthorized. "
            f"If you are using the public demo token, switch to your own MEDIAINSIGHT_MCP_TOKEN, --token, or --token-file and retry. Raw response: {detail}"
        )
    if status_code == 403:
        return (
            f"{context} failed with HTTP 403: the current token does not have permission for this action or dataset. "
            f"Try your own token if you need broader coverage. Raw response: {detail}"
        )
    return f"{context} failed with HTTP {status_code}: {detail}"


class MediaInsightMcpClient:
    def __init__(self, mcp_url: str = DEFAULT_MCP_URL, authorization: str = "") -> None:
        self.mcp_url = mcp_url.rstrip("/")
        self.authorization = authorization.strip()
        self.session_id: str | None = None

    def _request(self, payload: dict[str, Any]) -> dict[str, Any]:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        request = Request(url=self.mcp_url, data=data, method="POST")
        request.add_header("Accept", "text/event-stream, application/json")
        request.add_header("Content-Type", "application/json")
        if self.authorization:
            request.add_header("Authorization", self.authorization)
        if self.session_id:
            request.add_header("Mcp-Session-Id", self.session_id)

        try:
            response = build_opener().open(request)
            self.session_id = response.headers.get("Mcp-Session-Id") or self.session_id
            body = response.read().decode("utf-8")
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise MediaInsightError(_friendly_http_error("MCP request", exc.code, body)) from exc
        except URLError as exc:
            raise MediaInsightError(f"MCP request failed: {exc.reason}") from exc

        message = _parse_mcp_event_stream(body)
        if not isinstance(message, dict):
            raise MediaInsightError("MCP returned an unexpected payload")
        if "error" in message:
            error = message.get("error") or {}
            code = error.get("code")
            detail = error.get("message") or "unknown MCP error"
            raise MediaInsightError(f"MCP error {code}: {detail}")
        return message

    def initialize(self) -> None:
        self._request(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {"name": "mediainsight-ad-traffic", "version": "1.0"},
                },
            }
        )

    def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        if not self.session_id:
            self.initialize()
        response = self._request(
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {"name": name, "arguments": arguments or {}},
            }
        )
        result = response.get("result")
        if not isinstance(result, dict):
            raise MediaInsightError("MCP tool call returned an unexpected payload")
        if result.get("isError"):
            raise MediaInsightError(f"MCP tool {name} returned an error")
        return result


def _parse_mcp_event_stream(body: str) -> dict[str, Any]:
    for line in body.splitlines():
        if not line.startswith("data: "):
            continue
        raw = line[6:].strip()
        if not raw:
            continue
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise MediaInsightError("unable to parse MCP event stream payload") from exc
        if isinstance(payload, dict):
            return payload
    raise MediaInsightError("MCP response did not contain a JSON-RPC message")


def normalize_ad_traffic_payload(payload: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(payload)
    if "reportAdData" in normalized and "reportArgsAd" not in normalized:
        normalized["reportArgsAd"] = normalized.pop("reportAdData")
    return normalized


def fetch_ttc_token_from_mcp(
    mcp_token: str,
    *,
    mcp_url: str = DEFAULT_MCP_URL,
    token_type: int = 0,
) -> str:
    client = MediaInsightMcpClient(mcp_url=mcp_url, authorization=mcp_token)
    result = client.call_tool("get_ttc_token", {"type": token_type})
    structured = result.get("structuredContent", {})
    if not isinstance(structured, dict):
        raise MediaInsightError("MCP get_ttc_token did not return structured content")

    raw_result = structured.get("result")
    if not isinstance(raw_result, str) or not raw_result.strip():
        raise MediaInsightError("MCP get_ttc_token returned an empty result")

    try:
        payload = json.loads(raw_result)
    except json.JSONDecodeError as exc:
        raise MediaInsightError("unable to parse get_ttc_token result payload") from exc

    if not isinstance(payload, dict):
        raise MediaInsightError("get_ttc_token result payload is not an object")
    if payload.get("code") not in (0, "0"):
        message = payload.get("message") or payload.get("msg") or "unknown error"
        raise MediaInsightError(f"get_ttc_token failed: {message}")

    token = payload.get("data")
    if not isinstance(token, str) or not token.strip():
        raise MediaInsightError("get_ttc_token did not return a TTC token")
    return token.strip()


def resolve_media_insight_auth(
    token: str,
    *,
    mcp_url: str = DEFAULT_MCP_URL,
    mcp_token_type: int = 0,
) -> dict[str, str]:
    stripped = token.strip()
    if not stripped:
        raise MediaInsightError("MediaInsight token is empty")

    return {
        "mode": "ttc_token",
        "token": fetch_ttc_token_from_mcp(
            stripped,
            mcp_url=mcp_url,
            token_type=mcp_token_type,
        ),
    }


def ensure_ad_traffic_only_payload(payload: dict[str, Any]) -> None:
    if "reportArgsAd" not in payload and "reportAdData" not in payload:
        raise MediaInsightError("payload must include reportArgsAd")

    forbidden = sorted(key for key in AD_TRAFFIC_ONLY_FORBIDDEN_KEYS if key in payload)
    if forbidden:
        joined = ", ".join(forbidden)
        raise MediaInsightError(
            f"payload must stay ad-traffic-only; remove unsupported sections: {joined}"
        )


def _make_cookie(base_url: str, name: str, value: str) -> Cookie:
    parsed = urlparse(base_url)
    domain = parsed.hostname or ""
    return Cookie(
        version=0,
        name=name,
        value=value,
        port=None,
        port_specified=False,
        domain=domain,
        domain_specified=bool(domain),
        domain_initial_dot=domain.startswith("."),
        path="/",
        path_specified=True,
        secure=parsed.scheme == "https",
        expires=None,
        discard=True,
        comment=None,
        comment_url=None,
        rest={},
        rfc2109=False,
    )


def _cookies_as_dict(cookie_jar: CookieJar) -> dict[str, str]:
    return {cookie.name: cookie.value for cookie in cookie_jar}


def _load_session_payload(session_file: Path) -> dict[str, Any]:
    if not session_file.exists():
        return {}
    raw = session_file.read_text(encoding="utf-8").strip()
    if not raw:
        return {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    if not isinstance(payload, dict):
        return {}
    return payload


def _set_response_cookies(base_url: str, cookie_jar: CookieJar, response: Any) -> None:
    headers = getattr(response, "headers", None)
    if headers is None:
        return

    raw_cookies: list[str] = []
    if hasattr(headers, "get_all"):
        raw_cookies.extend(headers.get_all("Set-Cookie", []))
    elif hasattr(headers, "get"):
        maybe_cookie = headers.get("Set-Cookie")
        if maybe_cookie:
            raw_cookies.append(maybe_cookie)

    for raw_cookie in raw_cookies:
        parsed = SimpleCookie()
        parsed.load(raw_cookie)
        for morsel in parsed.values():
            cookie_jar.set_cookie(_make_cookie(base_url, morsel.key, morsel.value))


def _collect_media_leaf_ids(nodes: list[dict[str, Any]]) -> list[str]:
    leaf_ids: list[str] = []
    for node in nodes:
        children = node.get("children")
        if isinstance(children, list) and children:
            leaf_ids.extend(_collect_media_leaf_ids(children))
            continue
        node_id = node.get("id")
        node_type = node.get("type")
        if isinstance(node_id, str) and node_id and node_type == 3:
            leaf_ids.append(node_id)
    return leaf_ids


class MediaInsightClient:
    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        session_file: Path | str = DEFAULT_SESSION_FILE,
        ttc_token: str | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.session_file = Path(session_file)
        self.ttc_token = ttc_token.strip() if ttc_token else None
        self.cookie_jar = CookieJar()
        self._opener: OpenerDirector = build_opener(HTTPCookieProcessor(self.cookie_jar))
        self._restore_session()
        if self.ttc_token:
            self.set_ttc_token(self.ttc_token)

    def _restore_session(self) -> None:
        payload = _load_session_payload(self.session_file)
        if not payload:
            return

        saved_base_url = str(payload.get("base_url") or "").rstrip("/")
        if saved_base_url:
            self.base_url = saved_base_url

        cookies = payload.get("cookies", {})
        if not isinstance(cookies, dict):
            return

        for name, value in cookies.items():
            self.cookie_jar.set_cookie(_make_cookie(self.base_url, str(name), str(value)))

    def _save_session(self) -> None:
        payload = {
            "base_url": self.base_url,
            "cookies": _cookies_as_dict(self.cookie_jar),
        }
        self.session_file.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _cookie_header(self) -> str | None:
        cookies = _cookies_as_dict(self.cookie_jar)
        if not cookies:
            return None
        return "; ".join(f"{name}={value}" for name, value in cookies.items())

    def set_ttc_token(self, token: str) -> None:
        self.ttc_token = token.strip()
        self.cookie_jar.set_cookie(_make_cookie(self.base_url, "_mz_ttc_tkt", self.ttc_token))
        self._save_session()

    def _request(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> Any:
        url = urljoin(f"{self.base_url}/", path.lstrip("/"))
        if query:
            query_items = {key: value for key, value in query.items() if value is not None}
            if query_items:
                url = f"{url}?{urlencode(query_items, doseq=True)}"

        data: bytes | None = None
        if json_body is not None:
            data = json.dumps(json_body, ensure_ascii=False).encode("utf-8")

        request = Request(url=url, data=data, method=method.upper())
        request.add_header("Accept", "application/json")
        cookie_header = self._cookie_header()
        if cookie_header:
            request.add_header("Cookie", cookie_header)
        if json_body is not None:
            request.add_header("Content-Type", "application/json")

        try:
            response = self._opener.open(request)
            _set_response_cookies(self.base_url, self.cookie_jar, response)
            raw_body = response.read().decode("utf-8")
        except HTTPError as exc:
            raw_body = exc.read().decode("utf-8", errors="replace")
            raise MediaInsightError(
                _friendly_http_error(f"{method.upper()} {path}", exc.code, raw_body)
            ) from exc
        except URLError as exc:
            raise MediaInsightError(f"{method.upper()} {path} failed: {exc.reason}") from exc

        self._save_session()

        if not raw_body.strip():
            return {}

        try:
            return json.loads(raw_body)
        except json.JSONDecodeError:
            return raw_body

    def _request_bytes(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, Any] | None = None,
    ) -> tuple[bytes, dict[str, str]]:
        url = urljoin(f"{self.base_url}/", path.lstrip("/"))
        if query:
            query_items = {key: value for key, value in query.items() if value is not None}
            if query_items:
                url = f"{url}?{urlencode(query_items, doseq=True)}"

        request = Request(url=url, method=method.upper())
        request.add_header("Accept", "*/*")
        cookie_header = self._cookie_header()
        if cookie_header:
            request.add_header("Cookie", cookie_header)

        try:
            response = self._opener.open(request)
            _set_response_cookies(self.base_url, self.cookie_jar, response)
            raw_body = response.read()
            headers = {key: value for key, value in response.headers.items()}
        except HTTPError as exc:
            raw_body = exc.read().decode("utf-8", errors="replace")
            raise MediaInsightError(
                _friendly_http_error(f"{method.upper()} {path}", exc.code, raw_body)
            ) from exc
        except URLError as exc:
            raise MediaInsightError(f"{method.upper()} {path} failed: {exc.reason}") from exc

        self._save_session()
        return raw_body, headers

    def login(self, username: str, password: str) -> Any:
        return self._request("POST", "/user/login", json_body={"username": username, "password": password})

    def switch_tenant(self, tenant_id: int) -> Any:
        return self._request("GET", "/user/switch-tenant", query={"id": tenant_id})

    def task_data_set(self) -> Any:
        return self._request("GET", "/task/data-set")

    def dict_region(self) -> Any:
        return self._request("GET", "/dict/region")

    def dict_industry(self) -> Any:
        return self._request("GET", "/dict/industry")

    def dict_adviser(self) -> Any:
        return self._request("GET", "/dict/adviser")

    def dict_brand(self, advertiser_stid: str) -> Any:
        return self._request("GET", "/dict/brand", query={"advertiserStid": advertiser_stid})

    def dict_campaign_type(self) -> Any:
        return self._request("GET", "/dict/campaign-type")

    def dict_media(self) -> Any:
        return self._request("GET", "/dict/media")

    def dict_ad_spot_type(self) -> Any:
        return self._request("GET", "/dict/ad-spot-type")

    def dict_ta(self) -> Any:
        return self._request("GET", "/dict/ta")

    def _expand_media_list(self, payload: dict[str, Any]) -> dict[str, Any]:
        report_args = payload.get("reportArgsAd")
        if not isinstance(report_args, dict):
            return payload

        media_list = report_args.get("mediaList")
        if media_list not in (["__ALL__"], ["*"], "__ALL__", "*"):
            return payload

        media_response = self.dict_media()
        media_nodes = media_response.get("data", []) if isinstance(media_response, dict) else []
        if not isinstance(media_nodes, list):
            raise MediaInsightError("dict/media returned an unexpected payload")

        expanded_media_ids = _collect_media_leaf_ids(media_nodes)
        if not expanded_media_ids:
            raise MediaInsightError("unable to expand mediaList=__ALL__; no media leaf ids found")

        expanded_payload = dict(payload)
        expanded_report_args = dict(report_args)
        expanded_report_args["mediaList"] = expanded_media_ids
        expanded_payload["reportArgsAd"] = expanded_report_args
        return expanded_payload

    def task_calculate_coin(self, payload: dict[str, Any]) -> Any:
        normalized_payload = normalize_ad_traffic_payload(payload)
        ensure_ad_traffic_only_payload(normalized_payload)
        normalized_payload = self._expand_media_list(normalized_payload)
        return self._request("POST", "/task/calculate-coin", json_body=normalized_payload)

    def task_add(self, payload: dict[str, Any]) -> Any:
        normalized_payload = normalize_ad_traffic_payload(payload)
        ensure_ad_traffic_only_payload(normalized_payload)
        normalized_payload = self._expand_media_list(normalized_payload)
        return self._request("POST", "/task/add", json_body=normalized_payload)

    def task_list(self, *, page: int = 1, page_size: int = 20) -> Any:
        return self._request("GET", "/task/list", query={"page": page, "pageSize": page_size})

    def find_internal_task_id(self, biz_id: int | str, *, max_pages: int = 10, page_size: int = 50) -> int:
        target = str(biz_id)
        for page in range(1, max_pages + 1):
            payload = self.task_list(page=page, page_size=page_size)
            data = payload.get("data", {}) if isinstance(payload, dict) else {}
            tasks = data.get("list", []) if isinstance(data, dict) else []
            if not isinstance(tasks, list):
                break
            for task in tasks:
                if str(task.get("bizId")) == target:
                    task_id = task.get("id")
                    if isinstance(task_id, int):
                        return task_id
                    if isinstance(task_id, str) and task_id.isdigit():
                        return int(task_id)
            total = data.get("total") if isinstance(data, dict) else None
            if isinstance(total, int) and page * page_size >= total:
                break
        raise MediaInsightError(f"unable to resolve internal task id from bizId {biz_id}")

    def task_report_detail(self, task_id: int) -> Any:
        return self._request("GET", "/task/report-detail", query={"taskId": task_id})

    def task_report_file_gen_status(self, task_id: int) -> Any:
        return self._request("GET", "/task/report/file-gen-status", query={"taskId": task_id})

    def task_download_report(self, task_id: int) -> tuple[bytes, dict[str, str]]:
        return self._request_bytes("GET", "/task/download-report", query={"taskId": task_id})
