"""
iflow Pipeline 公共模块
- 凭证读取（环境变量 → 配置文件）
- API 调用封装（GET/POST/上传）
- 知识库查找（精确 + 模糊兜底）
- 文件类型推断
"""

import os
import sys
import json
import time
import functools
import urllib.parse
from pathlib import Path

import requests

# ─── 凭证 ───────────────────────────────────────────────

def load_credentials():
    key = os.environ.get("IFLOW_API_KEY", "")
    if not key:
        config_path = Path.home() / ".config" / "happy-notes" / "api-key"
        if config_path.exists():
            key = config_path.read_text().strip()
    if not key:
        log('IFLOW_API_KEY 未配置')
        sys.exit(1)
    base_url = os.environ.get("IFLOW_BASE_URL", "https://platform.iflow.cn")
    return key, base_url


API_KEY = None
BASE_URL = None
SESSION = None
TIMEOUT = (10, 60)  # (connect, read)


def _init():
    """惰性初始化：首次调用 API 时才加载凭证和创建 Session。"""
    global API_KEY, BASE_URL, SESSION
    if SESSION is not None:
        return
    API_KEY, BASE_URL = load_credentials()
    SESSION = requests.Session()
    SESSION.headers.update({
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    })


# ─── 日志（输出到 stderr） ──────────────────────────────

def log(msg):
    print(f">>> {msg}", file=sys.stderr)


# ─── 网络重试 ────────────────────────────────────────────

TRANSIENT_CODES = {"TIMEOUT", "NETWORK_ERROR", "REQUEST_ERROR"}

def retry_on_transient(max_retries=2, delay=5):
    """网络瞬态错误自动重试（不影响业务层重试逻辑如 submit_creation 的 500 重试）。"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries + 1):
                result = func(*args, **kwargs)
                if isinstance(result, dict) and result.get("code") in TRANSIENT_CODES:
                    if attempt < max_retries:
                        log(f"网络错误，{delay}s 后重试 ({attempt + 1}/{max_retries})")
                        time.sleep(delay)
                        continue
                return result
            return result
        return wrapper
    return decorator


# ─── API 调用 ───────────────────────────────────────────

def _safe_request(method, url, timeout, **kwargs):
    """统一的请求错误处理。网络/解析异常返回错误 dict，业务错误（HTTP 200 + success:false）原样返回。"""
    try:
        r = method(url, timeout=timeout, **kwargs)
        # 先尝试解析 JSON（iflow API 即使 HTTP 500 也可能返回有效 JSON）
        try:
            data = r.json()
            return data  # 业务层的 success/code 由调用方（如 submit_creation）处理
        except ValueError:
            pass
        # JSON 解析失败且非 2xx → 返回 HTTP 错误
        if r.status_code >= 400:
            log(f"服务异常 [HTTP {r.status_code}]: {url}")
            return {"success": False, "code": str(r.status_code), "message": f"服务异常 (HTTP {r.status_code})"}
        # JSON 解析失败但 2xx → 返回解析错误
        log(f"响应解析失败: {url}")
        return {"success": False, "code": "PARSE_ERROR", "message": "服务返回了非 JSON 响应"}
    except requests.exceptions.Timeout:
        log(f"请求超时: {url}")
        return {"success": False, "code": "TIMEOUT", "message": "请求超时，请稍后重试"}
    except requests.exceptions.ConnectionError:
        log(f"网络连接失败: {url}")
        return {"success": False, "code": "NETWORK_ERROR", "message": "网络连接失败"}
    except requests.exceptions.RequestException as e:
        log(f"请求异常: {url} — {e}")
        return {"success": False, "code": "REQUEST_ERROR", "message": str(e)}


@retry_on_transient(max_retries=2, delay=5)
def api_get(path, timeout=TIMEOUT):
    _init()
    return _safe_request(SESSION.get, f"{BASE_URL}{path}", timeout)


@retry_on_transient(max_retries=2, delay=5)
def api_post(path, body=None, timeout=TIMEOUT):
    _init()
    return _safe_request(SESSION.post, f"{BASE_URL}{path}", timeout, json=body)


@retry_on_transient(max_retries=2, delay=5)
def api_post_form(path, data=None, timeout=TIMEOUT):
    """POST 请求使用 application/x-www-form-urlencoded（clearCollection/stopSearch/deleteSearch 不接受 JSON）"""
    _init()
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    return _safe_request(SESSION.post, f"{BASE_URL}{path}", timeout, data=data, headers=headers)


def api_upload(collection_id, file_path=None, url=None, file_type="PDF"):
    """上传本地文件或导入 URL（multipart/form-data）"""
    _init()
    headers = {"Authorization": f"Bearer {API_KEY}"}  # 不带 Content-Type，让 requests 自动设
    upload_url = f"{BASE_URL}/api/v1/knowledge/upload"
    upload_timeout = (10, 120)
    if file_path:
        data = {"collectionId": collection_id, "type": file_type}
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            resp = _safe_request(requests.post, upload_url, upload_timeout,
                                 data=data, files=files, headers=headers)
    elif url:
        # URL 模式：必须用 multipart/form-data（与 curl -F 一致）
        # 添加空的 file 字段保持接口兼容性
        files = [
            ("collectionId", (None, collection_id)),
            ("type", (None, file_type)),
            ("content", (None, url)),
            ("file", ("", b"")),  # 空文件，兼容 type=HTML 时需要 file 字段
        ]
        resp = _safe_request(requests.post, upload_url, upload_timeout,
                             files=files, headers=headers)
    else:
        resp = {"success": False, "message": "file_path 或 url 必须提供一个"}
    return resp


def extract_content_id(resp):
    """从 upload 响应中提取 contentId（兼容 data 为 dict 或 list）"""
    data = resp.get("data")
    if isinstance(data, list) and data:
        item = data[0]
        # 检查内部错误码（外层 success=true 但 data[0].code 可能是 500）
        if item.get("code") and item["code"] != "200" and not item.get("contentId"):
            log(f"上传内部错误 [{item['code']}]: {item.get('message', '未知错误')}")
            return ""
        return item.get("contentId", "") or ""
    if isinstance(data, dict):
        return data.get("contentId", "")
    return ""


def upload_file(collection_id, filepath):
    """上传本地文件到知识库，返回 contentId 或 None。"""
    filepath = filepath.strip()
    if not os.path.isfile(filepath):
        log(f"文件不存在: {filepath}")
        return None
    ft = get_file_type(filepath)
    log(f"上传: {os.path.basename(filepath)} ({ft})")
    resp = api_upload(collection_id, file_path=filepath, file_type=ft)
    cid = extract_content_id(resp)
    if not cid:
        log(f"上传失败 {os.path.basename(filepath)}: {resp.get('message', '未知错误')}")
    return cid


def upload_url(collection_id, url):
    """导入 URL 到知识库，返回 contentId 或 None。"""
    url = url.strip()
    log(f"导入 URL: {url}")
    resp = api_upload(collection_id, url=url, file_type="HTML")
    cid = extract_content_id(resp)
    if not cid:
        log(f"导入失败 {url}: {resp.get('message', '未知错误')}")
    return cid


def check_success(resp, step=""):
    if resp.get("success") is True and resp.get("code") == "200":
        return True
    msg = resp.get("message", "未知错误")
    log(f"{step}失败: {msg}")
    return False


# ─── 知识库查找 ──────────────────────────────────────────

def find_kb(kb_name=None, kb_id=None, exit_on_missing=True, allow_fuzzy=True):
    """查找知识库。

    exit_on_missing=False 时找不到返回 None 而非 sys.exit。
    allow_fuzzy=False 时禁用模糊匹配（用于破坏性操作如删除，防止误匹配）。
    """
    if kb_id:
        return kb_id
    if not kb_name:
        log("--kb 或 --kb-id 必须提供一个")
        sys.exit(1)

    log(f'查找知识库「{kb_name}」')
    encoded = urllib.parse.quote(kb_name)
    resp = api_get(f"/api/v1/knowledge/pageQueryCollections?pageNum=1&pageSize=100&keyword={encoded}")
    items = resp.get("data", [])

    # 精确匹配
    for item in items:
        if item.get("name") == kb_name:
            return item["code"]

    # 模糊兜底（破坏性操作禁用）
    if items and allow_fuzzy:
        actual = items[0]
        log(f'模糊匹配到知识库「{actual["name"]}」')
        return actual["code"]

    if exit_on_missing:
        if items and not allow_fuzzy:
            log(f"未找到精确匹配的知识库「{kb_name}」（模糊匹配已禁用）")
        else:
            log("未找到匹配的知识库")
        sys.exit(1)
    return None


def create_kb(name, description=None):
    """创建知识库，返回 collectionId。失败时 sys.exit(1)。"""
    desc = description or name
    log(f'创建知识库「{name}」')
    resp = api_post("/api/v1/knowledge/saveCollection",
                    {"collectionName": name, "description": desc})
    collection_id = resp.get("data")
    if not collection_id:
        log(f"创建失败: {resp.get('message', '未知错误')}")
        sys.exit(1)
    log(f"知识库已创建: {collection_id}")
    return collection_id


# ─── 文件类型推断 ────────────────────────────────────────

EXT_MAP = {
    ".pdf": "PDF", ".txt": "TXT", ".md": "MARKDOWN",
    ".docx": "DOCX", ".png": "PNG", ".jpg": "JPG", ".jpeg": "JPG",
}

def get_file_type(filepath):
    ext = Path(filepath).suffix.lower()
    return EXT_MAP.get(ext, "PDF")


# ─── 参数校验 ────────────────────────────────────────────

VALID_OUTPUT_TYPES = {"PDF", "DOCX", "MARKDOWN", "PPT", "XMIND", "PODCAST", "VIDEO"}
VALID_PRESETS = {"商务", "卡通"}

def validate_output_type(t):
    """校验 output-type 参数，返回标准化的大写值。无效时 sys.exit(1)。"""
    upper = t.upper()
    if upper not in VALID_OUTPUT_TYPES:
        log(f"无效的输出类型 '{t}'，支持: {', '.join(sorted(VALID_OUTPUT_TYPES))}")
        sys.exit(1)
    return upper

def validate_preset(preset, output_type):
    """校验 preset 参数（仅 PPT 有效）。无效时 sys.exit(1)。"""
    if not preset:
        return
    if output_type != "PPT":
        log(f"preset 参数仅在 output-type=PPT 时有效，当前 output-type={output_type}")
        sys.exit(1)
    if preset not in VALID_PRESETS:
        log(f"无效的 PPT 风格 '{preset}'，支持: {', '.join(sorted(VALID_PRESETS))}")
        sys.exit(1)

def validate_files(file_paths):
    """校验文件路径列表，返回存在的路径。不存在的文件输出警告。"""
    valid = []
    for fp in file_paths:
        fp = fp.strip()
        if not fp:
            continue
        if not os.path.isfile(fp):
            log(f"文件不存在: {fp}")
        else:
            valid.append(fp)
    if not valid and file_paths:
        log("所有文件路径均无效")
        sys.exit(1)
    return valid

def validate_urls(urls):
    """校验 URL 格式（至少以 http:// 或 https:// 开头）。"""
    valid = []
    for u in urls:
        u = u.strip()
        if not u:
            continue
        if not u.startswith(("http://", "https://")):
            log(f"无效的 URL（需以 http:// 或 https:// 开头）: {u}")
        else:
            valid.append(u)
    if not valid and urls:
        log("所有 URL 均无效")
        sys.exit(1)
    return valid


# ─── 轮询文件解析 ────────────────────────────────────────

def poll_parsing(collection_id, content_ids, max_wait=300, interval=5):
    """轮询直到所有 contentId 对应的文件解析完成。

    返回解析失败的 contentId 集合（调用方应过滤后再提交生成任务）。
    """
    log("等待文件解析完成...")
    failed_ids = set()
    elapsed = 0
    while elapsed < max_wait:
        resp = api_post(f"/api/v1/knowledge/pageQueryContents?collectionId={collection_id}&pageNum=1&pageSize=200")
        items = resp.get("data") or []
        status_map = {it["contentId"]: it.get("status", "") for it in items}

        all_done = True
        for cid in content_ids:
            st = status_map.get(cid, "")
            if st == "failed":
                if cid not in failed_ids:
                    log(f"文件解析失败: {cid}")
                    failed_ids.add(cid)
            elif st != "success":
                all_done = False

        if all_done:
            ok = len(content_ids) - len(failed_ids)
            if failed_ids:
                log(f"解析完成: {ok} 成功, {len(failed_ids)} 失败")
            else:
                log("所有文件解析完成")
            return failed_ids

        time.sleep(interval)
        elapsed += interval
        log(f"解析中... ({elapsed}s/{max_wait}s)")

    log(f"轮询超时（{max_wait}秒），部分文件可能仍在解析中")
    return failed_ids


# ─── 提交创作任务 ────────────────────────────────────────

def submit_creation(collection_id, output_type="PDF", query=None, preset=None, files=None):
    """提交创作任务。搜索+创作接口共享限流：20 次/分钟，超限返回 500，自动重试。"""
    body = {"collectionId": collection_id, "type": output_type}
    if query:
        body["query"] = query
    if preset:
        body["preset"] = preset
    if files:
        body["files"] = files
    for attempt in range(1, 4):
        resp = api_post("/api/v1/knowledge/creationTask", body)
        creation_id = resp.get("data")
        if creation_id:
            log(f"创作任务已提交: {creation_id}")
            return creation_id
        code = resp.get("code", "")
        if code == "500" and attempt < 3:
            wait = attempt * 10
            log(f"服务繁忙，{wait}s 后重试 ({attempt}/2)")
            time.sleep(wait)
            continue
        log(f"创作任务提交失败 [{code}]: {resp.get('message', '未知错误')}")
        return None
    return None


# ─── 轮询创作状态 ────────────────────────────────────────

def poll_creation(collection_id, creation_id, max_wait=1800, interval=30):
    log("轮询创作状态...")
    elapsed = 0
    while elapsed < max_wait:
        time.sleep(interval)
        elapsed += interval
        resp = api_get(f"/api/v1/knowledge/creationList?collectionId={collection_id}&pageSize=50")
        for item in resp.get("data", []):
            if item.get("contentId") == creation_id:
                st = (item.get("extra") or {}).get("status", "")
                if st == "success":
                    log("创作完成!")
                    return "success"
                if st == "failed":
                    extra = item.get("extra") or {}
                    fail_type = extra.get("fileType", "")
                    fail_query = extra.get("query", "")
                    log(f"创作失败: type={fail_type}, query={fail_query}")
                    return "failed"
                log(f"创作中... ({elapsed}s)")
                break
    log("创作轮询超时")
    return "timeout"


# ─── 联网搜索 ─────────────────────────────────────────────

def start_search(collection_id, query, search_type="FAST_SEARCH", source="WEB"):
    """发起联网搜索，返回 searchId 或 None。

    搜索+创作接口共享限流：20 次/分钟，超限返回 500。遇到 500 自动重试。
    深度研究并发限制返回 40010，不重试。
    """
    body = {
        "query": query,
        "type": search_type,
        "source": source,
        "notebookId": collection_id,
    }
    for attempt in range(1, 4):
        resp = api_post("/api/v1/knowledge/startSearch", body)
        if resp.get("success"):
            search_id = resp.get("data", "")
            log(f"搜索已发起: {search_id} ({search_type} + {source})")
            return search_id
        code = resp.get("code", "")
        if code == "40010":
            log("深度研究并发限制: 已有一个深度研究任务正在处理中，请稍后再试")
            return None
        if code == "500" and attempt < 3:
            wait = attempt * 10
            log(f"服务繁忙，{wait}s 后重试 ({attempt}/2)")
            time.sleep(wait)
            continue
        log(f"搜索发起失败 [{code}]: {resp.get('message', '未知错误')}")
        return None
    return None


def poll_search(collection_id, search_id, max_wait=60, interval=3):
    """轮询搜索结果，返回 result data dict 或 None

    注意: max_wait 默认 60 秒仅适合 FAST_SEARCH。
    DEEP_RESEARCH 应传 max_wait=600, interval=10。
    """
    log("轮询搜索结果...")
    elapsed = 0
    last_progress = ""
    last_log_time = 0
    while elapsed < max_wait:
        time.sleep(interval)
        elapsed += interval
        resp = api_get(
            f"/api/v1/knowledge/getSearchResult"
            f"?notebookId={collection_id}&id={search_id}"
        )
        data = resp.get("data") or {}
        status = data.get("status", "unknown")
        progress = data.get("progress", "")

        if progress and progress != last_progress:
            last_progress = progress
            log(f"搜索进度: {progress}")

        if status == "completed":
            rc = data.get("resultCount", 0)
            log(f"搜索完成! 共 {rc} 条结果")
            return data
        if status in ("failed", "dismissed"):
            log(f"搜索终止: status={status}")
            return data
        # unknown / processing → 继续轮询，每 30 秒输出一次心跳日志
        if status == "processing" and elapsed - last_log_time >= 30:
            last_log_time = elapsed
            log(f"搜索中... ({elapsed}s)")

    log("搜索轮询超时")
    return None


def stop_search(collection_id):
    """停止搜索"""
    resp = api_post_form("/api/v1/knowledge/stopSearch",
                         {"notebookId": collection_id})
    return resp.get("success", False)


def delete_search(collection_id):
    """删除搜索"""
    resp = api_post_form("/api/v1/knowledge/deleteSearch",
                         {"notebookId": collection_id})
    return resp.get("success", False)


# ─── 分享 URL ────────────────────────────────────────────

SHARE_BASE_URL = "https://iflow.cn"

def build_share_url(share_id):
    """构造分享链接（域名固定为 iflow.cn，不是 API 域名 platform.iflow.cn）"""
    return f"{SHARE_BASE_URL}/inotebook/share?shareId={share_id}"


# ─── JSON 输出 ───────────────────────────────────────────

def output(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))
