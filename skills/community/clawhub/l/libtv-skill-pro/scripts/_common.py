"""agent-im OpenAPI 公共模块：创建会话、查询会话（鉴权为 Authorization: Bearer <access_key>）"""

import json
import os
import sys
import urllib.request
import urllib.error

# 默认 im 环境
IM_BASE = os.environ.get("OPENAPI_IM_BASE", os.environ.get("IM_BASE_URL", "https://im.liblib.tv"))
ACCESS_KEY = os.environ.get("LIBTV_ACCESS_KEY", "")

# 项目画布地址前缀，拼上 projectId 即项目地址
PROJECT_CANVAS_BASE = "https://www.liblib.tv/canvas?projectId="


def build_project_url(project_id: str) -> str:
    """根据 projectId（即 projectUuid）拼接项目画布地址"""
    if not project_id:
        return ""
    return PROJECT_CANVAS_BASE + project_id.strip()


# ---------- 结构化错误 ----------

class APIError(Exception):
    """API 调用错误。属性：http_code（int）、kind（str）、message（str）、raw（str）"""

    KIND_MAP = {
        401: "INVALID_ACCESS_KEY",
        403: "FORBIDDEN_OR_INSUFFICIENT_CREDITS",
        404: "NOT_FOUND",
        408: "TIMEOUT",
        429: "RATE_LIMITED",
        500: "SERVER_ERROR",
        502: "BAD_GATEWAY",
        503: "SERVICE_UNAVAILABLE",
        504: "GATEWAY_TIMEOUT",
    }

    def __init__(self, http_code: int, message: str, raw: str = ""):
        self.http_code = http_code
        self.kind = self.KIND_MAP.get(http_code, "UNKNOWN")
        self.message = message
        self.raw = raw
        super().__init__(f"[{self.kind}] HTTP {http_code}: {message}")

    def to_dict(self) -> dict:
        return {
            "error": {
                "kind": self.kind,
                "http_code": self.http_code,
                "message": self.message,
                "raw": self.raw,
            }
        }


class NetworkError(APIError):
    def __init__(self, reason: str):
        super().__init__(0, str(reason), "")
        self.kind = "NETWORK_ERROR"


def safe_run(main_fn):
    """统一错误处理 wrapper。把 APIError 转成结构化 JSON 输出到 stderr，并以非 0 退出。"""
    try:
        main_fn()
    except APIError as e:
        print(json.dumps(e.to_dict(), ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print(json.dumps({"error": {"kind": "INTERRUPTED", "message": "用户中断"}}, ensure_ascii=False), file=sys.stderr)
        sys.exit(130)


# ---------- access key 检查（延迟到首次实际调用 API 时）----------

def _ensure_access_key():
    if not ACCESS_KEY:
        raise APIError(0, "请设置 LIBTV_ACCESS_KEY 环境变量", "")


def _headers():
    return {
        "Authorization": f"Bearer {ACCESS_KEY}",
        "Content-Type": "application/json",
    }


def api_post(path: str, body: dict) -> dict:
    """POST 请求 agent-im OpenAPI"""
    _ensure_access_key()
    url = f"{IM_BASE.rstrip('/')}{path}"
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers=_headers(),
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8") if e.fp else ""
        raise APIError(e.code, _extract_message(err_body) or e.reason, err_body)
    except urllib.error.URLError as e:
        raise NetworkError(e.reason)


def api_get(path: str) -> dict:
    """GET 请求 agent-im OpenAPI"""
    _ensure_access_key()
    url = f"{IM_BASE.rstrip('/')}{path}"
    req = urllib.request.Request(url, method="GET", headers=_headers())
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8") if e.fp else ""
        raise APIError(e.code, _extract_message(err_body) or e.reason, err_body)
    except urllib.error.URLError as e:
        raise NetworkError(e.reason)


def _extract_message(body: str) -> str:
    """从 JSON 响应里提取 message 字段（LibTV 通常返回 {code, message, ...}）"""
    if not body:
        return ""
    try:
        obj = json.loads(body)
        return obj.get("message") or obj.get("msg") or ""
    except (ValueError, TypeError):
        return body[:200]


def create_session(session_id: str = "", message: str = "") -> dict:
    """
    创建会话或向已有会话发消息。
    返回 data: { projectUuid, sessionId }。
    """
    body = {}
    if session_id:
        body["sessionId"] = session_id
    if message:
        body["message"] = message
    resp = api_post("/openapi/session", body)
    return resp.get("data", {})


def query_session(session_id: str, after_seq: int = 0) -> dict:
    """
    查询会话消息列表。
    返回 data: { messages: [...] }。
    """
    path = f"/openapi/session/{session_id}"
    if after_seq > 0:
        path += f"?afterSeq={after_seq}"
    resp = api_get(path)
    return resp.get("data", {})


def change_project(project_uuid: str = "") -> dict:
    """
    切换当前 accessKey 绑定的项目。
    - 不传 project_uuid：服务端创建一个新项目并切换。
    - 传 project_uuid：尝试切换到指定项目（依赖服务端实现）。
    返回 data: { projectUuid }。
    """
    body = {}
    if project_uuid:
        body["projectUuid"] = project_uuid
    resp = api_post("/openapi/session/change-project", body)
    return resp.get("data", {})


# ---------- 本地项目记录 ----------

PROJECTS_FILE = os.path.expanduser("~/.libtv_projects.json")


def load_projects() -> dict:
    """加载本地项目记录。结构：{ "current": "uuid", "projects": {uuid: {...}} }"""
    if not os.path.exists(PROJECTS_FILE):
        return {"current": "", "projects": {}}
    try:
        with open(PROJECTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "projects" not in data:
                data["projects"] = {}
            if "current" not in data:
                data["current"] = ""
            return data
    except (OSError, json.JSONDecodeError):
        return {"current": "", "projects": {}}


def save_projects(data: dict) -> None:
    """保存本地项目记录"""
    os.makedirs(os.path.dirname(PROJECTS_FILE), exist_ok=True)
    with open(PROJECTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def record_project(project_uuid: str, set_current: bool = True, desc: str = "") -> None:
    """记录项目到本地缓存。set_current=True 同时设为当前项目。"""
    if not project_uuid:
        return
    from datetime import datetime
    data = load_projects()
    entry = data["projects"].get(project_uuid, {})
    if "createdAt" not in entry:
        entry["createdAt"] = datetime.now().isoformat()
    entry["lastUsedAt"] = datetime.now().isoformat()
    if desc:
        entry["desc"] = desc
    data["projects"][project_uuid] = entry
    if set_current:
        data["current"] = project_uuid
    save_projects(data)
