#!/usr/bin/env python3
"""
OpenClaw 三层记忆系统 - 增强版消息追踪器
==========================================

功能:
  - track <msg_id> [--content <json_file>]  追踪消息（含内容存储）
  - batch <msg_id> [<msg_id>...]             批量追踪（减少进程开销）
  - flush                                    强制刷新缓冲区到磁盘
  - check <msg_id>                           查询消息状态/内容
  - status                                   各层存储状态概览
  - archive [--date YYYY-MM-DD]              晋升7天前消息到archive
  - purge [--dry-run]                        执行90天过期清理
  - index --rebuild                          重建全文索引
  - daemon                                   以守护进程模式运行（Unix Socket）

守护进程模式:
  - 使用 Unix Socket (/tmp/track-daemon.sock) 接收请求
  - 内部批量处理，大幅减少进程启动开销
  - 无 fcntl 文件锁竞争
  - 通过 socket 通信，tracker.js 无需修改

存储结构:
  workspace/memory/messages/YYYY-MM-DD/{msg_id}.json   Layer 1 (7天)
  workspace/memory/archive/YYYY-MM-DD/{msg_id}.json    Layer 2 (90天)
  workspace/memory/daily/YYYY-MM-DD.md                  Layer 3 (永久)
  workspace/memory/index/message-index.json              全局索引
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

INDEX_FILE = INDEX_DIR / "message-index.json"
DAILY_INDEX_FILE = INDEX_DIR / "daily-index.json"
DAEMON_SOCKET = Path("/tmp/track-daemon.sock")

RETENTION_DAYS = {
    "messages": 7,
    "archive": 90,
}
TZ_OFFSET = "+08:00"

# ─── Manager 操作日志模块 ─────────────────────────────────────────
# 采用简化方案：直接在守护进程中写入日志，不使用复杂缓冲
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
        
        # 获取 tenant_access_token
        url = f"{FEISHU_API_BASE}/auth/v3/tenant_access_token/internal"
        data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
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
    """
    auth = _get_feishu_token()
    if not auth:
        return None
    
    try:
        url = f"{FEISHU_API_BASE}/im/v1/messages/{message_id}"
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {auth['token']}",
            "Content-Type": "application/json"
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        
        if result.get("code") == 0:
            data = result.get("data", {})
            items = data.get("items", [])
            if items:
                return items[0]
    except Exception:
        pass
    return None


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
        
        # 提取链接
        if tag == "a" and elem.get("href"):
            link_text = elem.get("text", "") or elem.get("content", "") or ""
            links.append({"text": link_text, "url": elem["href"]})
            texts.append(link_text)
            # 不return，继续递归处理子元素
        
        # 提取 div 文本
        elif tag == "div":
            div_text = ""
            # 嵌套的 text 元素
            if isinstance(elem.get("text"), dict):
                div_text = elem["text"].get("content", "") or ""
            elif isinstance(elem.get("text"), str):
                div_text = elem["text"] or ""
            if div_text:
                texts.append(div_text)
            # 递归处理嵌套元素
            for child in elem.get("elements", []):
                extract_from_element(child)
            return
        
        # 提取 markdown 内容
        elif tag == "markdown":
            md_content = elem.get("content", "")
            if md_content:
                texts.append(md_content)
            # 不return，继续递归处理子元素
        
        # 提取普通文本
        elif tag == "text":
            text_content = elem.get("text", "") or elem.get("content", "") or ""
            if text_content:
                texts.append(text_content)
            return
        
        # 提取图片（显示为占位符）
        elif tag == "img" and elem.get("image_key"):
            alt = elem.get("alt", "") or "图片"
            texts.append(f"[{alt}]")
            return
        
        # 提取文件（显示为占位符）
        elif tag == "file" and elem.get("file_key"):
            file_name = elem.get("file_name", "文件") or "文件"
            texts.append(f"[{file_name}]")
            return
        
        # 递归处理 elements（处理所有未early-return的标签）
        for child in elem.get("elements", []):
            extract_from_element(child)
    
    # 卡片内容可能在 card.body.elements 或直接在根元素
    elements = card_json.get("elements", [])
    # 深度展平：处理任意层级的嵌套 [[{...}]] → [{...}]
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
    特别处理卡片消息，提取链接和文字
    如果提供了 msg_data，会存储原始卡片JSON到 card_raw 字段
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
        # 富文本消息
        try:
            parsed = json.loads(raw_content)
            return _extract_post_text(parsed)
        except:
            return raw_content
    
    elif msg_type == "interactive":
        # 卡片消息：解析并存储原始JSON
        try:
            parsed = json.loads(raw_content)
            card_result = _parse_card_content(parsed)
            # 存储原始卡片JSON（供后续完整解析）
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
        # 其他类型，尝试直接解析
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
            # 递归处理嵌套
            extract(item.get("elements", []))
    
    post = post_json.get("post", {})
    if isinstance(post, dict):
        for key in ["zh_cn", "en_us", "ja_jp"]:
            content = post.get(key, {})
            if isinstance(content, dict):
                extract(content.get("content", []))
    
    return "\n".join(texts).strip()

# ─── 全局状态（守护进程模式共享） ───────────────────────────────
_daemon_mode = False
_daemon_exit = threading.Event()


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
            # 更新 session 索引
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
    如果 content 为空，会尝试从 Feishu API 获取卡片消息内容
    """
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
            # 尝试提取 sender_id
            sender = feishu_msg.get("sender", {})
            if sender.get("id"):
                msg_data["sender_id"] = sender["id"]

    return msg_data


def _build_msg_data(message_id: str, msg_obj: dict) -> dict:
    """
    从消息对象构建消息数据（用于batch模式，接收tracker.js传来的完整对象）
    msg_obj 格式: {messageId, content, from, timestamp, ...}
    如果 content 为空，会尝试从 Feishu API 获取卡片消息内容
    """
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

    # 从消息对象提取字段
    if msg_obj.get("content"):
        msg_data["content"] = msg_obj["content"]
    if msg_obj.get("from"):
        msg_data["sender_id"] = msg_obj["from"]
    if msg_obj.get("session_key"):
        msg_data["session_key"] = msg_obj["session_key"]
    if msg_obj.get("timestamp"):
        # 转换 Unix timestamp 为 ISO 格式
        try:
            ts = int(msg_obj["timestamp"])
            if ts > 1e12:  # 毫秒级时间戳
                ts = ts / 1000
            from datetime import datetime
            dt = datetime.fromtimestamp(ts)
            msg_data["timestamp"] = dt.strftime("%Y-%m-%dT%H:%M:%S") + TZ_OFFSET
        except:
            pass

    # 如果 content 为空或是[Interactive Card]占位符，尝试从 Feishu API 获取
    content = msg_data.get("content", "")
    if not content or content == "[Interactive Card]":
        feishu_msg = _fetch_feishu_message_content(message_id)
        if feishu_msg:
            content = _build_content_from_feishu_message(feishu_msg, msg_data)
            msg_data["content"] = content
            # 尝试提取 sender_id
            sender = feishu_msg.get("sender", {})
            if sender.get("id"):
                msg_data["sender_id"] = sender["id"]

    return msg_data


def ts_from_msg(msg: dict) -> str:
    return msg.get("timestamp", now_iso())[:10]


# ─── 核心操作 ───────────────────────────────────────────────

def track_message(message_id: str, content_path: Optional[str] = None):
    """
    追踪单条消息（立即写入，兼容原有调用方式）
    """
    msg_data = _track_single(message_id, content_path)
    if "error" in msg_data:
        return {"status": "error", "message": msg_data["error"]}

    date_str = msg_data["timestamp"][:10]
    msg_file = date_dir(MESSAGES_DIR, date_str) / f"{message_id}.json"
    save_json(msg_file, msg_data)
    _incremental_index_append([msg_data])

    # 更新 legacy tracker（保持兼容）
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
    """
    批量追踪：累积到缓冲区，达到阈值后批量写入
    大幅减少Python进程数和磁盘I/O
    """
    global _BATCH_BUFFER, _LAST_FLUSH_TIME

    added = []
    for msg_id in message_ids:
        msg_data = _track_single(msg_id)
        if "error" not in msg_data:
            _BATCH_BUFFER.append(msg_data)
            added.append(msg_id)

    # 更新 legacy tracker
    if added:
        tracker = load_tracker()
        for msg_id in added:
            if msg_id not in tracker.get("processedMessageIds", []):
                tracker.setdefault("processedMessageIds", []).append(msg_id)
        tracker["lastProcessedMessageId"] = added[-1]
        tracker["lastUpdated"] = now_iso()
        save_tracker(tracker)

    # 达到阈值时自动flush
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

    # 在 messages/ 中查找
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

    # 在 archive/ 中查找（可能已从索引移除但文件仍存在）
    if not result["found"]:
        if not ARCHIVE_DIR.exists():
            ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
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
        # 回退到 legacy tracker
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

    # 统计各层
    msgs_total = idx.get("totalMessages", 0)
    msgs_by_date = idx.get("byDate", {})
    msgs_pending = len(idx.get("pendingDelete", []))

    # messages/ 实际文件数
    msgs_files = sum(
        len(list((MESSAGES_DIR / d).glob("*.json")))
        for d in os.listdir(MESSAGES_DIR) if (MESSAGES_DIR / d).is_dir()
    ) if MESSAGES_DIR.exists() else 0

    # archive/ 实际文件数
    arch_files = sum(
        len(list((ARCHIVE_DIR / d).glob("*.json")))
        for d in os.listdir(ARCHIVE_DIR) if (ARCHIVE_DIR / d).is_dir()
    ) if ARCHIVE_DIR.exists() else 0

    # daily/ 实际文件数
    daily_files = len(list(DAILY_DIR.glob("*.md"))) if DAILY_DIR.exists() else 0

    # 计算存储大小
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
        },
    }


def archive_old_messages(date_str: Optional[str] = None):
    """
    将 messages/ 中 7 天前的消息晋升到 archive/
    Layer 1 → Layer 2
    """
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

        # 更新索引
        idx = load_index()
        # 从 messages 计数中移除
        if target_date in idx["byDate"]:
            if mf.stem in idx["byDate"][target_date]["messageIds"]:
                idx["byDate"][target_date]["messageIds"].remove(mf.stem)
                idx["byDate"][target_date]["count"] = max(0, idx["byDate"][target_date]["count"] - 1)
                idx["totalMessages"] = max(0, idx["totalMessages"] - 1)
        save_index(idx)

        archived += 1

    # 删除源文件
    for mf in msg_files:
        mf.unlink()
    # 清理空目录
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
    """
    清理 90 天前已归档的消息
    Layer 2 → 删除（带 pending_delete 检查）
    """
    # 加载 project-tracker
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

            # 检查是否有关联的未完成任务
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

    # 清理空目录
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
        # 返回待通知的消息，供 Manager 处理
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

    # 扫描 messages/
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

    # 扫描 archive/
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
class DaemonRequestHandler(socketserver.BaseRequestHandler):
    """处理 Unix Socket 请求"""
    
    def handle(self):
        try:
            # 读取请求数据
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
            
            # 解析请求
            try:
                request = json.loads(data.decode("utf-8"))
            except json.JSONDecodeError:
                self.request.sendall(json.dumps({"error": "Invalid JSON"}).encode())
                return
            
            cmd = request.get("cmd", "")
            args = request.get("args", [])
            
            # 执行命令
            result = self._execute_command(cmd, args)
            
            # 发送响应
            response = json.dumps(result, ensure_ascii=False).encode()
            self.request.sendall(response)
            
        except Exception as e:
            try:
                self.request.sendall(json.dumps({"error": str(e)}).encode())
            except:
                pass
    
    def _execute_command(self, cmd: str, args: list):
        """在守护进程上下文中执行命令"""
        global _BATCH_BUFFER, _LAST_FLUSH_TIME
        
        if cmd == "batch":
            message_items = args if args else []
            
            # ─── Manager 操作日志：记录批量追踪 ───────────────────
            if MANAGER_LOG_AVAILABLE:
                msg_ids = []
                for item in message_items:
                    if isinstance(item, str):
                        msg_ids.append(item)
                    else:
                        msg_ids.append(item.get("messageId") or item.get("message_id", "unknown"))
                # 直接写入日志
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
                # 支持两种格式：字符串(旧兼容) 或 对象(新格式带content)
                if isinstance(item, str):
                    # 旧格式：只传了messageId
                    msg_data = _track_single(item)
                    if "error" not in msg_data:
                        _BATCH_BUFFER.append(msg_data)
                        added.append(item)
                else:
                    # 新格式：传了完整的消息对象
                    msg_id = item.get("messageId") or item.get("message_id")
                    if not msg_id:
                        continue
                    msg_data = _build_msg_data(msg_id, item)
                    if "error" not in msg_data:
                        _BATCH_BUFFER.append(msg_data)
                        added.append(msg_id)
            
            # 更新 legacy tracker
            if added:
                with _daemon_lock:
                    tracker = load_tracker()
                    for msg_id in added:
                        if msg_id not in tracker.get("processedMessageIds", []):
                            tracker.setdefault("processedMessageIds", []).append(msg_id)
                    tracker["lastProcessedMessageId"] = added[-1]
                    tracker["lastUpdated"] = now_iso()
                    save_tracker(tracker)
            
            # 达到阈值时自动flush
            if _should_flush():
                _flush_batch()
            
            return {
                "status": "batched",
                "queued": len(added),
                "buffer_size": len(_BATCH_BUFFER),
            }
        
        elif cmd == "track":
            # 单条追踪
            msg_id = args[0] if args else ""
            content_path = args[1] if len(args) > 1 else None
            # ─── Manager 操作日志：记录单条追踪 ───────────────────
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
            return {"status": "shutdown"}
        
        else:
            return {"error": f"Unknown command: {cmd}"}


class ThreadedUnixTCPServer(socketserver.ThreadingMixIn, socketserver.UnixStreamServer):
    """支持多线程的 Unix Socket 服务器"""
    allow_reuse_address = True
    daemon_threads = True


def _run_daemon():
    """运行守护进程"""
    global _daemon_mode
    _daemon_mode = True
    
    # 清理旧的 socket 文件
    if DAEMON_SOCKET.exists():
        DAEMON_SOCKET.unlink()
    
    # 确保目录存在
    _ensure_dirs()
    
    # 创建服务器
    server = ThreadedUnixTCPServer(str(DAEMON_SOCKET), DaemonRequestHandler)
    
    # 设置权限
    DAEMON_SOCKET.chmod(0o666)
    
    print(f"Track daemon started on {DAEMON_SOCKET}")
    print(f"PID: {os.getpid()}")
    print("Commands: batch, track, flush, check, status, shutdown")
    
    # 注册信号处理
    def signal_handler(signum, frame):
        print("\nShutdown signal received...")
        _flush_batch()
        server.shutdown()
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
    server.serve_forever()


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
        # 批量追踪：python3 track.py batch <id1> <id2> ...
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
            # 输出旧文本格式，兼容core-monitor.sh
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
