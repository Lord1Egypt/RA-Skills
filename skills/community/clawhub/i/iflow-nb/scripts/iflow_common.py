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
import urllib.parse
from pathlib import Path

import requests

# ─── 凭证 ───────────────────────────────────────────────

def load_credentials():
    key = os.environ.get("IFLOW_API_KEY", "")
    if not key:
        config_path = Path.home() / ".config" / "iflow-nb" / "api_key"
        if config_path.exists():
            key = config_path.read_text().strip()
    if not key:
        log('IFLOW_API_KEY 未配置')
        sys.exit(1)
    base_url = os.environ.get("IFLOW_BASE_URL", "https://platform.iflow.cn")
    return key, base_url


API_KEY, BASE_URL = load_credentials()
SESSION = requests.Session()
SESSION.headers.update({
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
})
TIMEOUT = (10, 60)  # (connect, read)


# ─── 日志（输出到 stderr） ──────────────────────────────

def log(msg):
    print(f">>> {msg}", file=sys.stderr)


# ─── API 调用 ───────────────────────────────────────────

def api_get(path, timeout=TIMEOUT):
    r = SESSION.get(f"{BASE_URL}{path}", timeout=timeout)
    return r.json()


def api_post(path, body=None, timeout=TIMEOUT):
    r = SESSION.post(f"{BASE_URL}{path}", json=body, timeout=timeout)
    return r.json()


def api_upload(collection_id, file_path=None, url=None, file_type="PDF"):
    """上传本地文件或导入 URL（multipart/form-data）"""
    headers = {"Authorization": f"Bearer {API_KEY}"}  # 不带 Content-Type，让 requests 自动设
    if file_path:
        data = {"collectionId": collection_id, "type": file_type}
        files = {"file": (os.path.basename(file_path), open(file_path, "rb"))}
        r = requests.post(f"{BASE_URL}/api/v1/knowledge/upload", data=data, files=files,
                           headers=headers, timeout=(10, 120))
        resp = r.json()
        files["file"][1].close()
    elif url:
        # URL 模式：必须用 multipart/form-data（与 curl -F 一致）
        # 添加空的 file 字段保持接口兼容性
        files = [
            ("collectionId", (None, collection_id)),
            ("type", (None, file_type)),
            ("content", (None, url)),
            ("file", ("", b"")),  # 空文件，兼容 type=HTML 时需要 file 字段
        ]
        r = requests.post(f"{BASE_URL}/api/v1/knowledge/upload", files=files,
                           headers=headers, timeout=(10, 120))
        resp = r.json()
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


def check_success(resp, step=""):
    if resp.get("success") is True and resp.get("code") == "200":
        return True
    msg = resp.get("message", "未知错误")
    log(f"{step}失败: {msg}")
    return False


# ─── 知识库查找 ──────────────────────────────────────────

def find_kb(kb_name=None, kb_id=None):
    if kb_id:
        return kb_id
    if not kb_name:
        log("--kb 或 --kb-id 必须提供一个")
        sys.exit(1)

    log(f'查找知识库「{kb_name}」')
    encoded = urllib.parse.quote(kb_name)
    resp = api_get(f"/api/v1/knowledge/pageQueryCollections?pageNum=1&pageSize=50&keyword={encoded}")
    items = resp.get("data", [])

    # 精确匹配
    for item in items:
        if item.get("name") == kb_name:
            return item["code"]

    # 模糊兜底
    if items:
        actual = items[0]
        log(f'模糊匹配到知识库「{actual["name"]}」')
        return actual["code"]

    log("未找到匹配的知识库")
    sys.exit(1)


# ─── 文件类型推断 ────────────────────────────────────────

EXT_MAP = {
    ".pdf": "PDF", ".txt": "TXT", ".md": "MARKDOWN",
    ".docx": "DOCX", ".png": "PNG", ".jpg": "JPG", ".jpeg": "JPG",
}

def get_file_type(filepath):
    ext = Path(filepath).suffix.lower()
    return EXT_MAP.get(ext, "PDF")


# ─── 轮询文件解析 ────────────────────────────────────────

def poll_parsing(collection_id, content_ids, max_wait=300, interval=5):
    """轮询直到所有 contentId 对应的文件解析完成。

    返回解析失败的 contentId 集合（调用方应过滤后再提交生成任务）。
    """
    log("等待文件解析完成...")
    failed_ids = set()
    elapsed = 0
    while elapsed < max_wait:
        resp = api_post(f"/api/v1/knowledge/pageQueryContents?collectionId={collection_id}&pageNum=1&pageSize=100")
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
                    log("创作失败")
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
    resp = api_post("/api/v1/knowledge/stopSearch",
                    {"notebookId": collection_id})
    return resp.get("success", False)


def delete_search(collection_id):
    """删除搜索"""
    resp = api_post("/api/v1/knowledge/deleteSearch",
                    {"notebookId": collection_id})
    return resp.get("success", False)


# ─── JSON 输出 ───────────────────────────────────────────

def output(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))
