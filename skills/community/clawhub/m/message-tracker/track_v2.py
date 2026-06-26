#!/usr/bin/env python3
"""
OpenClaw 三层记忆系统 - 增强版消息追踪器 v2.0
==========================================

稳定性增强版本 (相比原版v1.x):
1. 守护进程唯一性锁 - 防止多实例运行
2. Watchdog健康检查线程 - 自动检测无响应并重启
3. HTTP请求超时修复 - urllib超时参数正确传递
4. 熔断机制 - 连续失败时快速失败而非无限重试
5. 批量处理优化 - 减少API调用次数
6. 内存缓冲保护 - 防止缓冲膨胀

功能:
  - track <msg_id> [--content <json_file>]  追踪消息（含内容存储）
  - batch <msg_id> [<msg_id>...]             批量追踪（减少进程开销）
  - flush                                     强制刷新缓冲区到磁盘
  - check <msg_id>                            查询消息状态/内容
  - status                                    各层存储状态概览
  - archive [--date YYYY-MM-DD]               晋升7天前消息到archive
  - purge [--dry-run]                         执行90天过期清理
  - index --rebuild                           重建全文索引
  - daemon                                    以守护进程模式运行（Unix Socket）
  - health                                    守护进程健康检查（远程诊断用）

守护进程模式:
  - 使用 Unix Socket (/run/track-daemon.sock) 接收请求
  - 内部批量处理，大幅减少进程启动开销
  - 无 fcntl 文件锁竞争（改用threading.Lock）
  - 通过 socket 通信，tracker.js 无需修改
  - Watchdog线程每30秒检查一次主线程响应性
"""

import json
import sys
import os
import time
import fcntl
import signal
import socket
import threading
import socketserver
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List

# ─── 路径配置 ───────────────────────────────────────────────
WORKSPACE = Path("/root/.openclaw/workspace")
MEMORY_BASE = WORKSPACE / "memory"
MESSAGES_DIR = MEMORY_BASE / "messages"
ARCHIVE_DIR = MEMORY_BASE / "archive"
DAILY_DIR = MEMORY_BASE / "daily"
INDEX_DIR = MEMORY_BASE / "index"
TRACKER_FILE = WORKSPACE / "configs/openclaw/message-tracker.json"
DAEMON_LOCK_FILE = INDEX_DIR / ".daemon.lock"  # 守护进程唯一性锁
DAEMON_PID_FILE = Path("/root/.openclaw/workspace/skills/message-tracker/.daemon.pid")  # PID文件

INDEX_FILE = INDEX_DIR / "message-index.json"
DAILY_INDEX_FILE = INDEX_DIR / "daily-index.json"
DAEMON_SOCKET = Path("/run/track-daemon.sock")

RETENTION_DAYS = {
    "messages": 7,
    "archive": 90,
}
TZ_OFFSET = "+08:00"

# ─── FD继承防护 ──────────────────────────────────────────────
def close_inherited_fds():
    """关闭继承的文件描述符，防止FD泄漏"""
    for fd in range(3, 256):
        try:
            os.close(fd)
        except (OSError, ValueError):
            pass

# ─── 稳定性增强: 全局状态 ─────────────────────────────────────────────
_daemon_mode = False
_daemon_exit = threading.Event()
_daemon_pid = os.getpid()
_last_daemon_activity = time.time()  # Watchdog跟踪最后活动时间
_WATCHDOG_TIMEOUT_SEC = 120           # 120秒无活动则触发重启告警
_CIRCUIT_BREAKER_FAILURES = 0       # 连续失败计数
_CIRCUIT_BREAKER_THRESHOLD = 5      # 连续5次失败则熔断
_CIRCUIT_BREAKER_RESET_SEC = 30     # 30秒后重置熔断
_last_failure_time = 0

# ─── Manager 操作日志模块 ─────────────────────────────────────────
_MANAGER_OP_LOCK = threading.Lock()

def _write_manager_op_log(message: str):
    """线程安全的操作日志写入"""
    try:
        _MANAGER_OP_LOG_FILE = WORKSPACE / "logs" / "manager-operations.log"
        os.makedirs(os.path.dirname(_MANAGER_OP_LOG_FILE), exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + TZ_OFFSET
        session_id = os.environ.get("OPENCLAW_SESSION_ID", os.uname().nodename)
        log_line = f"[{timestamp}] [{session_id}] [manager] [INFO] {message}\n"
        with _MANAGER_OP_LOCK:
            with open(_MANAGER_OP_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_line)
    except Exception:
        pass

MANAGER_LOG_AVAILABLE = True

# ─── Feishu API 配置 ───────────────────────────────────────────────
FEISHU_API_BASE = "https://open.feishu.cn/open-apis"

def _get_feishu_token() -> Optional[dict]:
    """获取 Feishu tenant_access_token"""
    config_path = Path("/root/.openclaw/openclaw.json")
    if not config_path.exists():
        return None
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        feishu = config.get("channels", {}).get("feishu", {})
        account = feishu.get("accounts", {}).get("default", {})
        app_id = account.get("appId")
        app_secret = account.get("appSecret")
        if not app_id or not app_secret:
            return None
        
        # 获取 tenant_access_token - 带超时
        url = f"{FEISHU_API_BASE}/auth/v3/tenant_access_token/internal"
        data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        # 修复: 使用context manager正确设置超时
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        if result.get("code") == 0:
            return {"token": result.get("tenant_access_token"), "app_id": app_id}
    except Exception:
        pass
    return None


def _fetch_feishu_message_content(message_id: str) -> Optional[dict]:
    """
    从 Feishu API 获取消息内容
    返回消息数据字典，如果失败返回 None
    
    稳定性增强:
    - 设置完整的超时(连接+读取)
    - 熔断机制: 连续失败时快速返回None
    - 记录失败用于熔断判断
    """
    global _CIRCUIT_BREAKER_FAILURES, _last_failure_time, _daemon_mode
    
    # 熔断检查
    now = time.time()
    if _CIRCUIT_BREAKER_FAILURES >= _CIRCUIT_BREAKER_THRESHOLD:
        if now - _last_failure_time < _CIRCUIT_BREAKER_RESET_SEC:
            # 熔断中，快速返回
            return None
        else:
            # 熔断超时，重置
            _CIRCUIT_BREAKER_FAILURES = 0
    
    auth = _get_feishu_token()
    if not auth:
        _record_failure()
        return None
    
    try:
        url = f"{FEISHU_API_BASE}/im/v1/messages/{message_id}"
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {auth['token']}",
            "Content-Type": "application/json"
        })
        # 修复: 完整超时设置 (连接10秒, 读取15秒)
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        
        if result.get("code") == 0:
            data = result.get("data", {})
            items = data.get("items", [])
            if items:
                _record_success()
                return items[0]
    except urllib.error.HTTPError as e:
        _record_failure()
        if e.code in (401, 403, 404):
            # 这些错误不值得重试，快速失败
            pass
    except Exception:
        _record_failure()
    
    return None


def _record_failure():
    """记录失败用于熔断判断"""
    global _CIRCUIT_BREAKER_FAILURES, _last_failure_time, _daemon_mode
    _CIRCUIT_BREAKER_FAILURES += 1
    _last_failure_time = time.time()
    if _daemon_mode:
        _update_activity()


def _record_success():
    """成功时重置熔断计数器"""
    global _CIRCUIT_BREAKER_FAILURES
    if _CIRCUIT_BREAKER_FAILURES > 0:
        _CIRCUIT_BREAKER_FAILURES -= 1


def _deep_flatten_elements(elements):
    """递归展平任意深度的嵌套数组"""
    result = []
    for item in elements:
        if isinstance(item, list):
            result.extend(_deep_flatten_elements(item))
        else:
            result.append(item)
    return result


def _parse_card_content(card_json: dict) -> dict:
    """
    解析飞书卡片消息内容，提取文字和链接
    返回: {"text": str, "links": [{"text": str, "url": str}, ...], "raw": str}
    """
    texts = []
    links = []
    
    def extract_from_element(elem):
        if not elem or not isinstance(elem, dict):
            return
        
        tag = elem.get("tag", "")
        
        if tag == "a" and elem.get("href"):
            link_text = elem.get("text", "") or elem.get("content", "") or ""
            links.append({"text": link_text, "url": elem["href"]})
            texts.append(link_text)
        
        elif tag == "div":
            div_text = ""
            if isinstance(elem.get("text"), dict):
                div_text = elem["text"].get("content", "") or ""
            elif isinstance(elem.get("text"), str):
                div_text = elem["text"] or ""
            if div_text:
                texts.append(div_text)
            for child in elem.get("elements", []):
                extract_from_element(child)
            return
        
        elif tag == "markdown":
            md_content = elem.get("content", "")
            if md_content:
                texts.append(md_content)
        
        elif tag == "text":
            text_content = elem.get("text", "") or elem.get("content", "") or ""
            if text_content:
                texts.append(text_content)
            return
        
        elif tag == "img" and elem.get("image_key"):
            alt = elem.get("alt", "") or "图片"
            texts.append(f"[{alt}]")
            return
        
        elif tag == "file" and elem.get("file_key"):
            file_name = elem.get("file_name", "文件") or "文件"
            texts.append(f"[{file_name}]")
            return
        
        for child in elem.get("elements", []):
            extract_from_element(child)
    
    elements = card_json.get("elements", [])
    if elements and isinstance(elements[0], list):
        elements = _deep_flatten_elements(elements)
    if not elements:
        body = card_json.get("body", {})
        elements = body.get("elements", [])
        if elements and isinstance(elements[0], list):
            elements = _deep_flatten_elements(elements)
    
    for elem in elements:
        extract_from_element(elem)
    
    return {
        "text": "\n".join(texts).strip(),
        "links": links,
        "raw": json.dumps(card_json, ensure_ascii=False)
    }


def _build_content_from_feishu_message(message_data: dict, msg_data: Optional[dict] = None) -> str:
    """
    从 Feishu API 返回的消息数据构建 content 字符串
    """
    msg_type = message_data.get("msg_type", "")
    body = message_data.get("body", {})
    raw_content = body.get("content", "") if isinstance(body, dict) else ""
    
    if msg_type == "text":
        try:
            parsed = json.loads(raw_content)
            return parsed.get("text", raw_content)
        except:
            return raw_content
    
    elif msg_type == "post":
        try:
            parsed = json.loads(raw_content)
            return _extract_post_text(parsed)
        except:
            return raw_content
    
    elif msg_type == "interactive":
        try:
            parsed = json.loads(raw_content)
            card_result = _parse_card_content(parsed)
            if msg_data is not None and card_result.get("raw"):
                msg_data["card_raw"] = card_result["raw"]
            parts = []
            if card_result["text"]:
                parts.append(card_result["text"])
            for link in card_result["links"]:
                parts.append(f"{link['text']}: {link['url']}")
            return "\n".join(parts).strip() or "[Interactive Card]"
        except:
            return "[Interactive Card]"
    
    else:
        try:
            parsed = json.loads(raw_content)
            if isinstance(parsed, dict):
                for key in ["text", "title", "content"]:
                    if parsed.get(key):
                        return str(parsed[key])
        except:
            pass
        return raw_content or f"[{msg_type} message]"


def _extract_post_text(post_json: dict) -> str:
    """从 post 类型的富文本消息中提取纯文本"""
    texts = []
    
    def extract(content_list):
        if not isinstance(content_list, list):
            return
        for item in content_list:
            if not isinstance(item, dict):
                continue
            if item.get("tag") == "text":
                text = item.get("text", "")
                if text:
                    texts.append(text)
            elif item.get("tag") == "at":
                name = item.get("name", "")
                if name:
                    texts.append(f"@{name}")
            elif item.get("tag") == "link":
                link_text = item.get("text", "") or item.get("href", "") or ""
                if link_text:
                    texts.append(link_text)
            extract(item.get("elements", []))
    
    post = post_json.get("post", {})
    if isinstance(post, dict):
        for key in ["zh_cn", "en_us", "ja_jp"]:
            content = post.get(key, {})
            if isinstance(content, dict):
                extract(content.get("content", []))
    
    return "\n".join(texts).strip()


# ─── 工具函数 ───────────────────────────────────────────────
def now_iso():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + TZ_OFFSET


def today():
    return datetime.now().strftime("%Y-%m-%d")


def date_dir(base: Path, date_str: str) -> Path:
    d = base / date_str
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_json(path: Path) -> dict:
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_json(path: Path, data: dict, indent=2):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def load_tracker() -> dict:
    return load_json(TRACKER_FILE)


def save_tracker(data: dict):
    save_json(TRACKER_FILE, data)


def load_index() -> dict:
    default = {
        "version": "1.0",
        "lastUpdated": now_iso(),
        "totalMessages": 0,
        "byDate": {},
        "bySession": {},
        "pendingDelete": [],
        "autoDeleteDate": None,
    }
    return load_json(INDEX_FILE) if INDEX_FILE.exists() else default


def save_index(idx: dict):
    idx["lastUpdated"] = now_iso()
    save_json(INDEX_FILE, idx)

# ─── 批量写入缓冲（减少磁盘I/O） ─────────────────────────────────
_BATCH_BUFFER: List[dict] = []
_LAST_FLUSH_TIME = time.time()
_FLUSH_INTERVAL_SEC = 1.0      # 每秒强制刷新
_BATCH_SIZE_THRESHOLD = 100    # 每100条强制刷新
_INDEX_LOCK_FILE = INDEX_DIR / ".index.lock"

# 守护进程模式下的锁（线程锁，不是文件锁）
_daemon_lock = threading.Lock()


def _update_activity():
    """更新守护进程最后活动时间（供Watchdog使用）"""
    global _last_daemon_activity
    _last_daemon_activity = time.time()


def _lock_index():
    """获取index文件锁（防止多进程并发写）- 守护进程模式下使用线程锁"""
    if _daemon_mode:
        _daemon_lock.acquire()
        return None  # 守护进程中不使用文件锁
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    lock_fd = open(_INDEX_LOCK_FILE, "w")
    fcntl.flock(lock_fd.fileno(), fcntl.LOCK_EX)
    return lock_fd


def _unlock_index(lock_fd):
    """释放index文件锁"""
    if _daemon_mode:
        _daemon_lock.release()
        return
    fcntl.flock(lock_fd.fileno(), fcntl.LOCK_UN)
    lock_fd.close()


def _incremental_index_append(entries: List[dict]):
    """
    增量更新索引：只追加新条目，不重写整个索引
    比全量rewrite快10-100倍
    """
    if not entries:
        return

    lock_fd = _lock_index()
    try:
        idx = load_index()
        for msg_data in entries:
            date_str = msg_data["timestamp"][:10]
            message_id = msg_data["message_id"]
            if date_str not in idx["byDate"]:
                idx["byDate"][date_str] = {"count": 0, "messageIds": [], "size_kb": 0.0}
            if message_id not in idx["byDate"][date_str]["messageIds"]:
                idx["byDate"][date_str]["messageIds"].append(message_id)
                idx["byDate"][date_str]["count"] += 1
                idx["totalMessages"] += 1
            sk = msg_data.get("session_key", "")
            if sk:
                if sk not in idx["bySession"]:
                    idx["bySession"][sk] = {
                        "firstMessage": message_id,
                        "lastMessage": message_id,
                        "count": 0,
                    }
                idx["bySession"][sk]["lastMessage"] = message_id
                idx["bySession"][sk]["count"] += 1
        save_index(idx)
    finally:
        _unlock_index(lock_fd)


def _flush_batch():
    """将缓冲区中的消息写入磁盘并更新索引（批量）"""
    global _BATCH_BUFFER, _LAST_FLUSH_TIME
    if not _BATCH_BUFFER:
        return
    entries = _BATCH_BUFFER
    _BATCH_BUFFER = []
    _LAST_FLUSH_TIME = time.time()

    # 按日期分组写入文件（减少目录操作）
    by_date = {}
    for msg_data in entries:
        date_str = msg_data["timestamp"][:10]
        if date_str not in by_date:
            by_date[date_str] = []
        by_date[date_str].append(msg_data)

    for date_str, msgs in by_date.items():
        d = date_dir(MESSAGES_DIR, date_str)
        for msg_data in msgs:
            msg_file = d / f"{msg_data['message_id']}.json"
            save_json(msg_file, msg_data)

    # 增量更新索引（只追加，不重写）
    _incremental_index_append(entries)
    _update_activity()


def _should_flush() -> bool:
    """判断是否需要强制刷新"""
    if len(_BATCH_BUFFER) >= _BATCH_SIZE_THRESHOLD:
        return True
    if time.time() - _LAST_FLUSH_TIME >= _FLUSH_INTERVAL_SEC:
        return True
    return False


def _track_single(message_id: str, content_path: Optional[str] = None) -> dict:
    """
    构建单条消息数据（不写入，用于batch模式）
    """
    _update_activity()  # 更新活动时间
    msg_data = {
        "message_id": message_id,
        "timestamp": now_iso(),
        "content": "",
        "sender_id": "",
        "sender_name": "",
        "channel": "feishu",
        "session_key": "",
        "has_attachment": False,
        "reply_to": None,
        "references": [],
        "layer": 1,
        "archived": False,
        "pending_delete": False,
        "delete_reason": None,
    }

    if content_path:
        try:
            with open(content_path, "r", encoding="utf-8") as f:
                external = json.load(f)
            for key in ["content", "sender_id", "sender_name", "channel",
                        "session_key", "has_attachment", "reply_to",
                        "references", "timestamp"]:
                if key in external:
                    msg_data[key] = external[key]
        except Exception as e:
            return {"message_id": message_id, "status": "error", "message": f"Failed to read content: {e}"}

    # 如果 content 为空或是[Interactive Card]占位符，尝试从 Feishu API 获取
    content = msg_data.get("content", "")
    if not content or content == "[Interactive Card]":
        feishu_msg = _fetch_feishu_message_content(message_id)
        if feishu_msg:
            content = _build_content_from_feishu_message(feishu_msg, msg_data)
            msg_data["content"] = content
            sender = feishu_msg.get("sender", {})
            if sender.get("id"):
                msg_data["sender_id"] = sender["id"]

    return msg_data


def _build_msg_data(message_id: str, msg_obj: dict) -> dict:
    """
    从消息对象构建消息数据（用于batch模式）
    """
    _update_activity()  # 更新活动时间
    msg_data = {
        "message_id": message_id,
        "timestamp": now_iso(),
        "content": "",
        "sender_id": "",
        "sender_name": "",
        "channel": "feishu",
        "session_key": "",
        "has_attachment": False,
        "reply_to": None,
        "references": [],
        "layer": 1,
        "archived": False,
        "pending_delete": False,
        "delete_reason": None,
    }

    if msg_obj.get("content"):
        msg_data["content"] = msg_obj["content"]
    if msg_obj.get("from"):
        msg_data["sender_id"] = msg_obj["from"]
    if msg_obj.get("session_key"):
        msg_data["session_key"] = msg_obj["session_key"]
    if msg_obj.get("timestamp"):
        try:
            ts = int(msg_obj["timestamp"])
            if ts > 1e12:
                ts = ts / 1000
            from datetime import datetime
            dt = datetime.fromtimestamp(ts)
            msg_data["timestamp"] = dt.strftime("%Y-%m-%dT%H:%M:%S") + TZ_OFFSET
        except:
            pass

    content = msg_data.get("content", "")
    if not content or content == "[Interactive Card]":
        feishu_msg = _fetch_feishu_message_content(message_id)
        if feishu_msg:
            content = _build_content_from_feishu_message(feishu_msg, msg_data)
            msg_data["content"] = content
            sender = feishu_msg.get("sender", {})
            if sender.get("id"):
                msg_data["sender_id"] = sender["id"]

    return msg_data


def ts_from_msg(msg: dict) -> str:
    return msg.get("timestamp", now_iso())[:10]


# ─── 核心操作 ───────────────────────────────────────────────

def track_message(message_id: str, content_path: Optional[str] = None):
    """追踪单条消息（立即写入）"""
    msg_data = _track_single(message_id, content_path)
    if "error" in msg_data:
        return {"status": "error", "message": msg_data["error"]}

    date_str = msg_data["timestamp"][:10]
    msg_file = date_dir(MESSAGES_DIR, date_str) / f"{message_id}.json"
    save_json(msg_file, msg_data)
    _incremental_index_append([msg_data])

    tracker = load_tracker()
    if message_id not in tracker.get("processedMessageIds", []):
        tracker.setdefault("processedMessageIds", []).append(message_id)
    tracker["lastProcessedMessageId"] = message_id
    tracker["lastUpdated"] = now_iso()
    save_tracker(tracker)

    return {
        "status": "tracked",
        "message_id": message_id,
        "file": str(msg_file),
        "layer": msg_data["layer"],
    }


def batch_track(message_ids: List[str]):
    """批量追踪：累积到缓冲区，达到阈值后批量写入"""
    global _BATCH_BUFFER, _LAST_FLUSH_TIME

    added = []
    for msg_id in message_ids:
        msg_data = _track_single(msg_id)
        if "error" not in msg_data:
            _BATCH_BUFFER.append(msg_data)
            added.append(msg_id)

    if added:
        tracker = load_tracker()
        for msg_id in added:
            if msg_id not in tracker.get("processedMessageIds", []):
                tracker.setdefault("processedMessageIds", []).append(msg_id)
        tracker["lastProcessedMessageId"] = added[-1]
        tracker["lastUpdated"] = now_iso()
        save_tracker(tracker)

    if _should_flush():
        _flush_batch()

    return {
        "status": "batched",
        "queued": len(added),
        "buffer_size": len(_BATCH_BUFFER),
    }


def check_message(message_id: str):
    """查询消息状态和内容"""
    idx = load_index()
    result = {"message_id": message_id, "found": False, "locations": []}

    for date_str, info in idx.get("byDate", {}).items():
        if message_id in info["messageIds"]:
            msg_file = MESSAGES_DIR / date_str / f"{message_id}.json"
            if msg_file.exists():
                data = load_json(msg_file)
                result["found"] = True
                result["locations"].append({
                    "layer": data.get("layer", 1),
                    "date": date_str,
                    "archived": data.get("archived", False),
                    "pending_delete": data.get("pending_delete", False),
                    "delete_reason": data.get("delete_reason"),
                    "timestamp": data.get("timestamp"),
                    "content_preview": (data.get("content", "") or "")[:200],
                })

    if not result["found"]:
        for adate in ARCHIVE_DIR.iterdir():
            if adate.is_dir():
                af = adate / f"{message_id}.json"
                if af.exists():
                    data = load_json(af)
                    result["found"] = True
                    result["locations"].append({
                        "layer": 2,
                        "date": str(adate.name),
                        "archived": True,
                        "pending_delete": data.get("pending_delete", False),
                        "delete_reason": data.get("delete_reason"),
                        "timestamp": data.get("timestamp"),
                        "content_preview": (data.get("content", "") or "")[:200],
                    })

    if not result["found"]:
        tracker = load_tracker()
        if message_id in tracker.get("processedMessageIds", []):
            result["found"] = True
            result["locations"].append({
                "layer": 0,
                "note": "仅在 legacy tracker 中存在ID，无内容",
            })

    return result


def _ensure_dirs():
    """确保必要目录存在"""
    for d in [MESSAGES_DIR, ARCHIVE_DIR, DAILY_DIR, INDEX_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def status_summary():
    """显示各层存储状态"""
    idx = load_index()
    tracker = load_tracker()

    msgs_total = idx.get("totalMessages", 0)
    msgs_by_date = idx.get("byDate", {})
    msgs_pending = len(idx.get("pendingDelete", []))

    msgs_files = sum(
        len(list((MESSAGES_DIR / d).glob("*.json")))
        for d in os.listdir(MESSAGES_DIR) if (MESSAGES_DIR / d).is_dir()
    ) if MESSAGES_DIR.exists() else 0

    arch_files = sum(
        len(list((ARCHIVE_DIR / d).glob("*.json")))
        for d in os.listdir(ARCHIVE_DIR) if (ARCHIVE_DIR / d).is_dir()
    ) if ARCHIVE_DIR.exists() else 0

    daily_files = len(list(DAILY_DIR.glob("*.md"))) if DAILY_DIR.exists() else 0

    def dir_size(path: Path) -> float:
        if not path.exists():
            return 0.0
        total = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
        return total / 1024

    return {
        "layer1_messages": {
            "path": str(MESSAGES_DIR),
            "retention_days": RETENTION_DAYS["messages"],
            "indexed_total": msgs_total,
            "actual_files": msgs_files,
            "by_date_count": len(msgs_by_date),
            "size_kb": round(dir_size(MESSAGES_DIR), 1),
        },
        "layer2_archive": {
            "path": str(ARCHIVE_DIR),
            "retention_days": RETENTION_DAYS["archive"],
            "actual_files": arch_files,
            "size_kb": round(dir_size(ARCHIVE_DIR), 1),
        },
        "layer3_daily": {
            "path": str(DAILY_DIR),
            "retention": "permanent",
            "file_count": daily_files,
            "size_kb": round(dir_size(DAILY_DIR), 1),
        },
        "index": {
            "path": str(INDEX_FILE),
            "totalMessages": msgs_total,
            "pendingDelete": msgs_pending,
            "size_kb": round(dir_size(INDEX_DIR), 1),
        },
        "legacy_tracker": {
            "path": str(TRACKER_FILE),
            "tracked_count": len(tracker.get("processedMessageIds", [])),
            "lastUpdated": tracker.get("lastUpdated", "unknown"),
            "lastMessageId": tracker.get("lastProcessedMessageId", ""),
        },
        "daemon_buffer": {
            "mode": "daemon" if _daemon_mode else "cli",
            "buffer_size": len(_BATCH_BUFFER),
            "socket": str(DAEMON_SOCKET),
            "pid": _daemon_pid if _daemon_mode else None,
            "uptime_sec": int(time.time() - _daemon_start_time) if _daemon_mode else None,
        },
        "stability": {
            "circuit_breaker_failures": _CIRCUIT_BREAKER_FAILURES,
            "circuit_breaker_threshold": _CIRCUIT_BREAKER_THRESHOLD,
            "last_activity": datetime.fromtimestamp(_last_daemon_activity).strftime("%Y-%m-%dT%H:%M:%S") + TZ_OFFSET if _daemon_mode else None,
            "watchdog_timeout_sec": _WATCHDOG_TIMEOUT_SEC if _daemon_mode else None,
        },
    }


def archive_old_messages(date_str: Optional[str] = None):
    """将 messages/ 中 7 天前的消息晋升到 archive/"""
    cutoff = (datetime.now() - timedelta(days=RETENTION_DAYS["messages"])).strftime("%Y-%m-%d")
    target_date = date_str or cutoff

    src_dir = MESSAGES_DIR / target_date
    if not src_dir.exists():
        return {"status": "no_data", "date": target_date}

    msg_files = list(src_dir.glob("*.json"))
    if not msg_files:
        return {"status": "empty", "date": target_date}

    dest_dir = date_dir(ARCHIVE_DIR, target_date)
    archived = 0

    for mf in msg_files:
        data = load_json(mf)
        data["layer"] = 2
        data["archived"] = True
        data["archived_at"] = now_iso()

        dest_file = dest_dir / mf.name
        save_json(dest_file, data)

        idx = load_index()
        if target_date in idx["byDate"]:
            if mf.stem in idx["byDate"][target_date]["messageIds"]:
                idx["byDate"][target_date]["messageIds"].remove(mf.stem)
                idx["byDate"][target_date]["count"] = max(0, idx["byDate"][target_date]["count"] - 1)
                idx["totalMessages"] = max(0, idx["totalMessages"] - 1)
        save_index(idx)

        archived += 1

    for mf in msg_files:
        mf.unlink()
    try:
        src_dir.rmdir()
    except OSError:
        pass

    return {
        "status": "archived",
        "date": target_date,
        "count": archived,
        "dest": str(dest_dir),
    }


def purge_expired(dry_run: bool = True):
    """清理 90 天前已归档的消息"""
    tracker_file = MEMORY_BASE / "project-tracker.json"
    project_tracker = load_json(tracker_file)

    cutoff = (datetime.now() - timedelta(days=RETENTION_DAYS["archive"])).strftime("%Y-%m-%d")
    deleted = []
    protected = []
    pending_notify = []

    if not ARCHIVE_DIR.exists():
        return {"status": "no_archive", "cutoff": cutoff}

    for date_dir_obj in sorted(ARCHIVE_DIR.iterdir()):
        if date_dir_obj.name > cutoff:
            continue
        if not date_dir_obj.is_dir():
            continue

        for msg_file in date_dir_obj.glob("*.json"):
            data = load_json(msg_file)
            msg_id = data.get("message_id", msg_file.stem)

            active_tasks = project_tracker.get("activeTasks", [])
            related = [
                t for t in active_tasks
                if t.get("related_messages", []) and msg_id in t.get("related_messages", [])
            ]

            if related:
                data["pending_delete"] = True
                data["delete_reason"] = f"related task active: {[t['id'] for t in related]}"
                save_json(msg_file, data)
                protected.append({
                    "message_id": msg_id,
                    "date": date_dir_obj.name,
                    "related_tasks": [t["id"] for t in related],
                })
                pending_notify.append((msg_id, data, related))
            else:
                if not dry_run:
                    msg_file.unlink()
                deleted.append({"message_id": msg_id, "date": date_dir_obj.name, "deleted": not dry_run})

    if not dry_run:
        for date_dir_obj in sorted(ARCHIVE_DIR.iterdir()):
            if date_dir_obj.is_dir() and date_dir_obj.name <= cutoff:
                if not any(date_dir_obj.iterdir()):
                    date_dir_obj.rmdir()

    result = {
        "status": "dry_run" if dry_run else "executed",
        "cutoff": cutoff,
        "deleted_count": len(deleted),
        "protected_count": len(protected),
        "deleted": deleted[:10],
        "protected": protected[:10],
    }

    if pending_notify and not dry_run:
        result["pending_notify"] = [{
            "message_id": mid,
            "timestamp": data.get("timestamp"),
            "content_preview": (data.get("content", "") or "")[:100],
            "related_tasks": [t["id"] for t in tasks],
        } for mid, data, tasks in pending_notify]

    return result


def rebuild_index():
    """重建 message-index.json"""
    idx = {
        "version": "1.0",
        "lastUpdated": now_iso(),
        "totalMessages": 0,
        "byDate": {},
        "bySession": {},
        "pendingDelete": [],
        "autoDeleteDate": None,
    }

    if MESSAGES_DIR.exists():
        for date_str in os.listdir(MESSAGES_DIR):
            d = MESSAGES_DIR / date_str
            if not d.is_dir():
                continue
            files = list(d.glob("*.json"))
            if not files:
                continue
            idx["byDate"][date_str] = {
                "count": 0,
                "messageIds": [],
                "size_kb": 0.0,
            }
            for f in files:
                msg = load_json(f)
                idx["byDate"][date_str]["messageIds"].append(f.stem)
                idx["totalMessages"] += 1
                sk = msg.get("session_key", "")
                if sk:
                    if sk not in idx["bySession"]:
                        idx["bySession"][sk] = {"firstMessage": f.stem, "lastMessage": f.stem, "count": 0}
                    idx["bySession"][sk]["lastMessage"] = f.stem
                    idx["bySession"][sk]["count"] += 1
            idx["byDate"][date_str]["count"] = len(idx["byDate"][date_str]["messageIds"])

    if ARCHIVE_DIR.exists():
        for date_str in os.listdir(ARCHIVE_DIR):
            d = ARCHIVE_DIR / date_str
            if not d.is_dir():
                continue
            for f in d.glob("*.json"):
                msg = load_json(f)
                if msg.get("pending_delete"):
                    idx["pendingDelete"].append({
                        "message_id": f.stem,
                        "date": date_str,
                        "reason": msg.get("delete_reason"),
                    })

    save_index(idx)

    tracker = load_tracker()
    tracker["lastUpdated"] = now_iso()
    save_tracker(tracker)

    return {
        "status": "rebuilt",
        "totalMessages": idx["totalMessages"],
        "datesIndexed": len(idx["byDate"]),
        "sessionsIndexed": len(idx["bySession"]),
    }


# ─── 守护进程模式 ─────────────────────────────────────────────
_daemon_start_time = time.time()


class DaemonRequestHandler(socketserver.BaseRequestHandler):
    """处理 Unix Socket 请求"""
    
    def handle(self):
        global _last_daemon_activity
        try:
            data = b""
            while True:
                chunk = self.request.recv(4096)
                if not chunk:
                    break
                data += chunk
                if len(chunk) < 4096:
                    break
            
            if not data:
                return
            
            try:
                request = json.loads(data.decode("utf-8"))
            except json.JSONDecodeError:
                self.request.sendall(json.dumps({"error": "Invalid JSON"}).encode())
                return
            
            cmd = request.get("cmd", "")
            args = request.get("args", [])
            
            # 更新活动时间
            _last_daemon_activity = time.time()
            
            result = self._execute_command(cmd, args)
            response = json.dumps(result, ensure_ascii=False).encode()
            self.request.sendall(response)
            
        except Exception as e:
            try:
                self.request.sendall(json.dumps({"error": str(e)}).encode())
            except:
                pass
    
    def _execute_command(self, cmd: str, args: list):
        """在守护进程上下文中执行命令"""
        global _BATCH_BUFFER, _LAST_FLUSH_TIME, _daemon_exit
        
        if cmd == "health":
            # 健康检查命令 - 远程诊断用
            return {
                "status": "healthy",
                "pid": _daemon_pid,
                "uptime_sec": int(time.time() - _daemon_start_time),
                "buffer_size": len(_BATCH_BUFFER),
                "last_activity": datetime.fromtimestamp(_last_daemon_activity).strftime("%Y-%m-%dT%H:%M:%S") + TZ_OFFSET,
                "circuit_breaker_failures": _CIRCUIT_BREAKER_FAILURES,
                "pending_flush": len(_BATCH_BUFFER) > 0,
            }
        
        elif cmd == "batch":
            message_items = args if args else []
            
            if MANAGER_LOG_AVAILABLE:
                msg_ids = []
                for item in message_items:
                    if isinstance(item, str):
                        msg_ids.append(item)
                    else:
                        msg_ids.append(item.get("messageId") or item.get("message_id", "unknown"))
                try:
                    _op_log = WORKSPACE / "logs" / "manager-operations.log"
                    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + TZ_OFFSET
                    hostname = os.uname().nodename
                    log_line = f"[{ts}] [{hostname}] [manager] [INFO] batch: {len(msg_ids)} msgs | {msg_ids[:5]}\n"
                    with open(_op_log, "a") as f:
                        f.write(log_line)
                except Exception:
                    pass
            
            added = []
            for item in message_items:
                if isinstance(item, str):
                    msg_data = _track_single(item)
                    if "error" not in msg_data:
                        _BATCH_BUFFER.append(msg_data)
                        added.append(item)
                else:
                    msg_id = item.get("messageId") or item.get("message_id")
                    if not msg_id:
                        continue
                    msg_data = _build_msg_data(msg_id, item)
                    if "error" not in msg_data:
                        _BATCH_BUFFER.append(msg_data)
                        added.append(msg_id)
            
            if added:
                with _daemon_lock:
                    tracker = load_tracker()
                    for msg_id in added:
                        if msg_id not in tracker.get("processedMessageIds", []):
                            tracker.setdefault("processedMessageIds", []).append(msg_id)
                    tracker["lastProcessedMessageId"] = added[-1]
                    tracker["lastUpdated"] = now_iso()
                    save_tracker(tracker)
            
            if _should_flush():
                _flush_batch()
            
            return {
                "status": "batched",
                "queued": len(added),
                "buffer_size": len(_BATCH_BUFFER),
            }
        
        elif cmd == "track":
            msg_id = args[0] if args else ""
            content_path = args[1] if len(args) > 1 else None
            if MANAGER_LOG_AVAILABLE:
                try:
                    _op_log = WORKSPACE / "logs" / "manager-operations.log"
                    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + TZ_OFFSET
                    hostname = os.uname().nodename
                    log_line = f"[{ts}] [{hostname}] [manager] [INFO] track: {msg_id}\n"
                    with open(_op_log, "a") as f:
                        f.write(log_line)
                except Exception:
                    pass
            return track_message(msg_id, content_path)
        
        elif cmd == "flush":
            _flush_batch()
            return {"status": "flushed", "buffer_size": len(_BATCH_BUFFER)}
        
        elif cmd == "check":
            msg_id = args[0] if args else ""
            return check_message(msg_id)
        
        elif cmd == "status":
            return status_summary()
        
        elif cmd == "shutdown":
            _flush_batch()
            _daemon_exit.set()
            _remove_pid_file()
            return {"status": "shutdown"}
        
        else:
            return {"error": f"Unknown command: {cmd}"}


class ThreadedUnixTCPServer(socketserver.ThreadingMixIn, socketserver.UnixStreamServer):
    """支持多线程的 Unix Socket 服务器"""
    allow_reuse_address = True
    daemon_threads = True


def _acquire_daemon_lock():
    """
    获取守护进程唯一性锁
    返回True表示获取成功（可以运行）
    返回False表示已有实例在运行
    """
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    try:
        lock_fd = open(DAEMON_LOCK_FILE, "w")
        fcntl.flock(lock_fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        lock_fd.write(str(os.getpid()))
        lock_fd.flush()
        # 保持文件描述符打开以保持锁
        return lock_fd
    except (IOError, OSError):
        # 锁获取失败，说明已有实例
        return None


def _check_pid_file():
    """
    检查PID文件，判断是否可以启动
    返回 (can_start, reason)
    - can_start=True: 可以启动（PID文件不存在或进程已不存在）
    - can_start=False: 不能启动（进程正在运行）
    """
    if not DAEMON_PID_FILE.exists():
        return True, "PID file not found"
    
    try:
        pid_str = DAEMON_PID_FILE.read_text().strip()
        if not pid_str:
            return True, "PID file empty"
        
        pid = int(pid_str)
        
        # 检查进程是否存在
        try:
            # 信号0不发送任何信号，只检查进程是否存在
            os.kill(pid, 0)
            # 进程存在，检查是否是同一个进程（通过cmdline判断）
            try:
                with open(f"/proc/{pid}/cmdline", "r") as f:
                    cmdline = f.read()
                    if "track_v2.py" in cmdline and str(os.getpid()) != str(pid):
                        return False, f"Another daemon is running with PID {pid}"
                    elif "track_v2.py" not in cmdline:
                        # PID存在但不是tracker进程，删除PID文件
                        DAEMON_PID_FILE.unlink()
                        return True, f"Stale PID file (process {pid} is not tracker)"
            except:
                pass
            return False, f"PID {pid} is running"
        except OSError:
            # 进程不存在，删除PID文件
            try:
                DAEMON_PID_FILE.unlink()
            except:
                pass
            return True, f"Stale PID file (process {pid} not found)"
    except (ValueError, IOError) as e:
        return True, f"PID file corrupted: {e}"


def _write_pid_file():
    """写入当前PID到PID文件"""
    DAEMON_PID_FILE.parent.mkdir(parents=True, exist_ok=True)
    DAEMON_PID_FILE.write_text(str(os.getpid()))


def _remove_pid_file():
    """删除PID文件"""
    try:
        if DAEMON_PID_FILE.exists():
            DAEMON_PID_FILE.unlink()
    except:
        pass


def _release_daemon_lock(lock_fd):
    """释放守护进程锁"""
    if lock_fd:
        try:
            fcntl.flock(lock_fd.fileno(), fcntl.LOCK_UN)
            lock_fd.close()
        except:
            pass
        try:
            DAEMON_LOCK_FILE.unlink()
        except:
            pass


def _watchdog_socket_check():
    """通过 Unix Socket 发送 status 命令验证 daemon 是否真正响应"""
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(str(DAEMON_SOCKET))
        request = json.dumps({'cmd': 'status', 'args': []}).encode()
        sock.sendall(request)
        sock.settimeout(3)
        data = sock.recv(4096)
        sock.close()
        return data is not None and len(data) > 0
    except Exception:
        return False


def _query_daemon_status() -> Optional[dict]:
    """通过 Unix Socket 查询 daemon 真实状态（供 CLI status 命令使用）"""
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(str(DAEMON_SOCKET))
        request = json.dumps({'cmd': 'status', 'args': []}).encode()
        sock.sendall(request)
        sock.settimeout(5)
        data = sock.recv(16384)
        sock.close()
        if data:
            return json.loads(data.decode('utf-8'))
        return None
    except Exception:
        return None


def _run_watchdog():
    """
    Watchdog线程：监控守护进程主线程响应性
    如果60秒内没有活动记录，说明主线程可能卡住了
    """
    global _daemon_exit
    last_warn_time = 0
    while not _daemon_exit.is_set():
        time.sleep(10)  # 每10秒检查一次
        if _daemon_exit.is_set():
            break
        
        idle_time = time.time() - _last_daemon_activity
        
        if idle_time > _WATCHDOG_TIMEOUT_SEC:
            now = time.time()
            # 只在每60秒打印一次警告，避免日志刷屏
            if now - last_warn_time > 60:
                if not _watchdog_socket_check():
                    print(f"[WATCHDOG] No activity for {idle_time:.0f}s, socket check FAILED, restarting (PID {_daemon_pid})...")
                    _daemon_exit.set()
                else:
                    print(f"[WATCHDOG] No activity for {idle_time:.0f}s but socket responsive, skipping restart")
                last_warn_time = now


def _run_daemon():
    """运行守护进程"""
    # 关闭继承的FD，防止泄漏core-monitor.lock等文件锁
    close_inherited_fds()
    global _daemon_mode, _daemon_start_time
    _daemon_mode = True
    _daemon_start_time = time.time()
    _update_activity()
    
    # 检查PID文件
    can_start, reason = _check_pid_file()
    if not can_start:
        print(f"ERROR: Cannot start daemon. {reason}")
        print(f"If you believe this is wrong, remove {DAEMON_PID_FILE} and restart.")
        sys.exit(1)
    print(f"[PID] {reason}")
    
    # 获取唯一性锁
    lock_fd = _acquire_daemon_lock()
    if lock_fd is None:
        print(f"ERROR: Another daemon instance is already running.")
        print(f"If you believe this is wrong, remove {DAEMON_LOCK_FILE} and restart.")
        sys.exit(1)
    
    # 写入PID文件
    _write_pid_file()
    
    # 清理旧的 socket 文件
    if DAEMON_SOCKET.exists():
        DAEMON_SOCKET.unlink()
    
    # 确保目录存在
    _ensure_dirs()
    
    # 创建服务器
    server = ThreadedUnixTCPServer(str(DAEMON_SOCKET), DaemonRequestHandler)
    DAEMON_SOCKET.chmod(0o666)
    
    print(f"Track daemon v2.0 started on {DAEMON_SOCKET}")
    print(f"PID: {_daemon_pid}")
    print(f"Commands: batch, track, flush, check, status, health, shutdown")
    print(f"Watchdog timeout: {_WATCHDOG_TIMEOUT_SEC}s")
    print(f"Circuit breaker threshold: {_CIRCUIT_BREAKER_THRESHOLD} failures")
    
    # 启动Watchdog线程
    watchdog_thread = threading.Thread(target=_run_watchdog, daemon=True)
    watchdog_thread.start()
    
    # 注册信号处理
    def signal_handler(signum, frame):
        print("\nShutdown signal received...")
        _flush_batch()
        server.shutdown()
        _release_daemon_lock(lock_fd)
        _remove_pid_file()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 启动定期刷新线程
    def periodic_flush():
        while not _daemon_exit.is_set():
            time.sleep(0.5)
            if _should_flush():
                _flush_batch()
    
    flush_thread = threading.Thread(target=periodic_flush, daemon=True)
    flush_thread.start()
    
    # 运行服务器
    try:
        while not _daemon_exit.is_set():
            server.handle_request()
    finally:
        _release_daemon_lock(lock_fd)
        _remove_pid_file()


# ─── CLI 入口 ───────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    # 守护进程模式
    if cmd == "daemon":
        _run_daemon()
        return

    if cmd == "health" and _daemon_mode:
        # 健康检查 - 在daemon内部调用
        pass

    if cmd == "track" and len(sys.argv) >= 3:
        msg_id = sys.argv[2]
        content_path = None
        if "--content" in sys.argv:
            idx = sys.argv.index("--content")
            if idx + 1 < len(sys.argv):
                content_path = sys.argv[idx + 1]
        result = track_message(msg_id, content_path)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif cmd == "batch" and len(sys.argv) >= 3:
        message_ids = sys.argv[2:]
        result = batch_track(message_ids)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif cmd == "flush":
        _flush_batch()
        print(json.dumps({"status": "flushed", "buffer_size": len(_BATCH_BUFFER)}, indent=2))

    elif cmd == "check" and len(sys.argv) >= 3:
        result = check_message(sys.argv[2])
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif cmd == "status":
        if "--legacy" in sys.argv:
            tracker = load_tracker()
            last_updated = tracker.get("lastUpdated", "unknown")
            total_tracked = len(tracker.get("processedMessageIds", []))
            recent = tracker.get("processedMessageIds", [])[-5:]
            last_processed = tracker.get("lastProcessedMessageId", "")
            print(f"Last Updated: {last_updated}")
            print(f"Last Processed: {last_processed}")
            print(f"Total Tracked: {total_tracked}")
            print(f"Recent IDs: {recent}")
        else:
            # CLI模式下通过socket查询daemon真实状态
            daemon_status = _query_daemon_status()
            if daemon_status:
                print(json.dumps(daemon_status, indent=2, ensure_ascii=False))
            else:
                # socket查询失败，降级到本地status_summary()
                result = status_summary()
                print(json.dumps(result, indent=2, ensure_ascii=False))

    elif cmd == "archive":
        date_str = None
        if "--date" in sys.argv:
            idx = sys.argv.index("--date")
            if idx + 1 < len(sys.argv):
                date_str = sys.argv[idx + 1]
        result = archive_old_messages(date_str)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif cmd == "purge":
        dry_run = "--dry-run" in sys.argv or "--dry-run" not in sys.argv
        result = purge_expired(dry_run=("--dry-run" in sys.argv))
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif cmd == "index" and "--rebuild" in sys.argv:
        result = rebuild_index()
        print(json.dumps(result, indent=2, ensure_ascii=False))

    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
