"""Notion API wrapper - shared client for all record operations."""
import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding='utf-8')

# Pending batch storage
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BATCH_FILE = os.path.join(SCRIPT_DIR, ".pending_batch.json")
BATCH_TTL_SECONDS = 300  # 5 minutes

def _get_env(name):
    """Get env var, falling back to Windows user-level registry on Windows."""
    val = os.environ.get(name, "")
    if val:
        return val
    if sys.platform == "win32":
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Environment",
                0,
                winreg.KEY_READ,
            )
            val, _ = winreg.QueryValueEx(key, name)
            winreg.CloseKey(key)
            return val or ""
        except Exception:
            pass
    return ""

API_KEY = _get_env("NOTION_API_KEY")
PAGE_ID = _get_env("NOTION_PARENT_PAGE_ID")
BASE_URL = "https://api.notion.com/v1"

HEADERS_TEMPLATE = {
    "Authorization": "",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def get_headers():
    headers = HEADERS_TEMPLATE.copy()
    headers["Authorization"] = f"Bearer {API_KEY}"
    return headers


def api_request(method, path, body=None):
    """Make a single API request with retry on rate limit."""
    headers = get_headers()
    url = f"{BASE_URL}/{path}"

    for attempt in range(3):
        try:
            data = json.dumps(body).encode() if body else None
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
            resp = urllib.request.urlopen(req)
            return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                import time
                time.sleep(1.5 * (attempt + 1))
                continue
            error_body = e.read().decode()
            try:
                err_data = json.loads(error_body)
                message = err_data.get("message", str(e))
            except Exception:
                message = str(e)
            return {"error": True, "code": e.code, "message": message}
        except Exception as e:
            import time
            if attempt < 2:
                time.sleep(1)
                continue
            return {"error": True, "message": str(e)}

    return {"error": True, "message": "Rate limited after retries"}


def append_blocks(children, silent=False):
    """Append a list of blocks to the page."""
    if not children:
        print("OK|没有内容可追加")
        return
    result = api_request("PATCH", f"blocks/{PAGE_ID}/children", {"children": children})
    if result.get("error"):
        _emit_error(result)
        return
    results_list = result.get("results", children)
    block_count = len(results_list)

    # Save block IDs for batch undo
    block_ids = [b["id"] for b in results_list]
    _save_pending_batch(block_ids)

    if not silent:
        print(f"OK|已记录到 Notion，共 {block_count} 个 blocks")


def get_children(page_id=None, start_cursor=None, page_size=100, silent=False):
    """Read page children blocks."""
    pid = page_id or PAGE_ID
    params = f"page_size={page_size}"
    if start_cursor:
        params += f"&start_cursor={start_cursor}"
    result = api_request("GET", f"blocks/{pid}/children?{params}")
    if result.get("error"):
        if not silent:
            _emit_error(result)
        return None
    return result


def delete_last_block():
    """Delete the last block(s) on the page.

    If there is a pending batch (within BATCH_TTL_SECONDS), delete all blocks
    in that batch. Otherwise paginate to the actual last block and delete it.
    """
    # Check for pending batch first
    pending = _load_pending_batch()
    if pending:
        block_ids = pending["block_ids"]
        deleted = 0
        for bid in reversed(block_ids):  # Delete in reverse order (last first)
            result = api_request("DELETE", f"blocks/{bid}")
            if result.get("error"):
                _emit_error(result)
                # Continue deleting remaining blocks even if one fails
            else:
                deleted += 1
        _clear_pending_batch()
        print(f"OK| 已撤回最后一批记录，共 {deleted} 条")
        return

    # No pending batch, delete single last block
    cursor = None
    last_block = None
    while True:
        params = f"page_size=100"
        if cursor:
            params += f"&start_cursor={cursor}"
        data = api_request("GET", f"blocks/{PAGE_ID}/children?{params}")
        if data.get("error") or "results" not in data or not data["results"]:
            break
        last_block = data["results"][-1]
        if data.get("has_more") and data.get("next_cursor"):
            cursor = data["next_cursor"]
        else:
            break

    if not last_block:
        print("OK| 没有可撤回的记录")
        return

    block_id = last_block["id"]
    result = api_request("DELETE", f"blocks/{block_id}")
    if result.get("error"):
        _emit_error(result)
        return
    print("OK| 已撤回最后一条记录")


def _save_pending_batch(block_ids):
    """Save pending batch block IDs to file."""
    batch = {
        "block_ids": block_ids,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    try:
        with open(BATCH_FILE, "w", encoding="utf-8") as f:
            json.dump(batch, f, ensure_ascii=False, indent=2)
    except Exception:
        pass  # Non-critical, don't fail the main operation


def _load_pending_batch():
    """Load pending batch if it exists and is not expired."""
    if not os.path.exists(BATCH_FILE):
        return None
    try:
        with open(BATCH_FILE, "r", encoding="utf-8") as f:
            batch = json.load(f)
        ts = datetime.fromisoformat(batch["timestamp"])
        now = datetime.now(timezone.utc)
        age = (now - ts).total_seconds()
        if age > BATCH_TTL_SECONDS:
            _clear_pending_batch()
            return None
        return batch
    except Exception:
        return None


def _clear_pending_batch():
    """Clear the pending batch file."""
    try:
        if os.path.exists(BATCH_FILE):
            os.remove(BATCH_FILE)
    except Exception:
        pass


def check_config():
    """Verify API key and page access."""
    if not API_KEY:
        return {"ok": False, "code": "CONFIG", "message": "NOTION_API_KEY 未配置"}
    if not PAGE_ID:
        return {"ok": False, "code": "CONFIG", "message": "NOTION_PARENT_PAGE_ID 未配置"}

    result = api_request("GET", f"blocks/{PAGE_ID}/children?page_size=1")
    if result.get("error"):
        code = result.get("code", 0)
        msg = result.get("message", "")
        if code == 401 or "Unauthorized" in msg:
            return {"ok": False, "code": "AUTH", "message": "API Key 无效或页面未授权"}
        if code == 404 or "Not Found" in msg:
            return {"ok": False, "code": "AUTH", "message": "页面不存在或 Integration 未授权"}
        return {"ok": False, "code": "UNKNOWN", "message": msg}
    return {"ok": True, "message": ""}


def upload_file(file_path):
    """Upload a local file to Notion via File Upload API.

    Uses the notion-upload library to upload a file, then returns the file_id
    which can be used with image/file blocks using type "file_upload".

    Includes a small delay after upload to avoid rate limits when uploading
    multiple images in quick succession.

    Args:
        file_path: Absolute path to the local file.

    Returns:
        The Notion file_upload ID string on success, None on failure.
    """
    try:
        from notion_upload import notion_upload as nu
    except ImportError:
        print("ERROR| notion-upload 库未安装，请运行: pip install notion-upload")
        return None

    if not API_KEY:
        print("ERROR|AUTH")
        return None

    file_name = os.path.basename(file_path)
    try:
        uploader = nu(file_path, file_name, API_KEY, enforce_max_size=True)
        file_id = uploader.upload()
        if file_id:
            # Small delay to avoid rate limit on rapid successive uploads
            import time
            time.sleep(0.5)
            return file_id
        else:
            print("ERROR| 图片上传失败: 未返回 file_id")
            return None
    except FileNotFoundError:
        print(f"ERROR| 文件不存在: {file_path}")
        return None
    except Exception as e:
        print(f"ERROR| 图片上传失败: {e}")
        return None


def get_last_callout_block():
    """Find the last callout block on the page by paginating through all children."""
    cursor = None
    last_callout = None
    while True:
        params = "page_size=100"
        if cursor:
            params += f"&start_cursor={cursor}"
        data = api_request("GET", f"blocks/{PAGE_ID}/children?{params}")
        if data.get("error") or "results" not in data or not data["results"]:
            break
        for block in data["results"]:
            if block.get("type") == "callout":
                last_callout = block
        if data.get("has_more") and data.get("next_cursor"):
            cursor = data["next_cursor"]
        else:
            break
    return last_callout


def append_to_block(block_id, children, silent=False):
    """Append children to a specific block (not the page)."""
    if not children:
        print("OK|没有内容可追加")
        return
    result = api_request("PATCH", f"blocks/{block_id}/children", {"children": children})
    if result.get("error"):
        _emit_error(result)
        return
    if not silent:
        print(f"OK|已追加到 Notion，共 {len(children)} 段")


def _emit_error(result):
    """Emit a friendly error message based on the error code."""
    msg = result.get("message", "")
    code = result.get("code", 0)
    if code == 401 or "Unauthorized" in msg:
        print("ERROR|AUTH")
    elif code == 404 or "Could not find" in msg:
        print("ERROR|AUTH")
    elif code == 429:
        print("ERROR|RATE_LIMIT")
    else:
        print("ERROR|NETWORK")


if __name__ == "__main__":
    result = check_config()
    if not result["ok"]:
        print(f"ERROR|{result['code']}")
    else:
        print("OK|配置检查通过")
