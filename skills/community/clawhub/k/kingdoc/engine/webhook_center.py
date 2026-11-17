"""KingDoc Webhook 与通知中心

订阅记录新增/修改/删除三类事件：
- 签名校验 + SQLite 去重队列
- 通知通道整合金山协作消息/企微/钉钉三路
- 用户按事件类型选通道
- 事件可触发写入 zwjh 记忆（桥接存在时）

本地降级：无 webhook 配置时返回友好提示。
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import sqlite3
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

# 事件类型
EVENT_TYPES: Dict[str, str] = {
    "record_created": "记录新增",
    "record_updated": "记录修改",
    "record_deleted": "记录删除",
    "field_updated": "字段更新",
    "table_created": "表格创建",
}

# 通知通道
NOTIFICATION_CHANNELS: Dict[str, Dict[str, Any]] = {
    "kdocs": {
        "name": "金山协作消息",
        "description": "金山文档内置协作通知",
        "requires": ["webhook_key"],
    },
    "wecom": {
        "name": "企业微信",
        "description": "企微机器人 Webhook",
        "requires": ["webhook_url"],
    },
    "dingtalk": {
        "name": "钉钉",
        "description": "钉钉机器人 Webhook",
        "requires": ["webhook_url"],
    },
}

# 默认签名密钥（生产环境应从配置读取）
DEFAULT_SIGNING_SECRET = "kingdoc_webhook_secret_v4"


class WebhookCenterEngine:
    """Webhook 与通知中心引擎"""

    def __init__(self, backend: Any = None, db_path: Optional[str] = None,
                 signing_secret: str = ""):
        self.backend = backend
        self.db_path = db_path or self._default_db_path()
        self.signing_secret = signing_secret or DEFAULT_SIGNING_SECRET
        self._event_handlers: Dict[str, List[Callable]] = {}
        self._init_db()

    def _default_db_path(self) -> str:
        skill_root = Path(__file__).resolve().parent.parent
        return str(skill_root / ".webhook_center.db")

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS webhook_subscriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_id TEXT,
                    event_type TEXT,
                    callback_url TEXT,
                    channel TEXT,
                    webhook_key TEXT,
                    signing_secret TEXT,
                    status TEXT DEFAULT 'active',
                    created_at TEXT,
                    last_triggered_at TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS webhook_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT UNIQUE,
                    event_type TEXT,
                    table_id TEXT,
                    record_id TEXT,
                    payload TEXT,
                    signature TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TEXT,
                    processed_at TEXT,
                    channel TEXT,
                    error TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS webhook_dedup (
                    event_hash TEXT PRIMARY KEY,
                    created_at TEXT
                )
            """)
            conn.commit()
        finally:
            conn.close()

    def list_event_types(self) -> Dict[str, Any]:
        """列出所有事件类型"""
        return {
            "event_types": [
                {"id": k, "name": v}
                for k, v in EVENT_TYPES.items()
            ]
        }

    def list_channels(self) -> Dict[str, Any]:
        """列出所有通知通道"""
        return {
            "channels": [
                {
                    "id": k,
                    "name": v["name"],
                    "description": v["description"],
                    "requires": v["requires"],
                }
                for k, v in NOTIFICATION_CHANNELS.items()
            ]
        }

    def subscribe(self, table_id: str, event_type: str, callback_url: str,
                  channel: str, webhook_key: str = "",
                  signing_secret: str = "") -> Dict[str, Any]:
        """订阅事件"""
        if event_type not in EVENT_TYPES:
            return {
                "success": False,
                "error": f"不支持的事件类型: {event_type}。支持: {list(EVENT_TYPES.keys())}",
            }

        if channel not in NOTIFICATION_CHANNELS:
            return {
                "success": False,
                "error": f"不支持的通知通道: {channel}。支持: {list(NOTIFICATION_CHANNELS.keys())}",
            }

        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute(
                """INSERT INTO webhook_subscriptions
                   (table_id, event_type, callback_url, channel, webhook_key,
                    signing_secret, status, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, 'active', ?)""",
                (table_id, event_type, callback_url, channel, webhook_key,
                 signing_secret or self.signing_secret,
                 datetime.now().isoformat()),
            )
            conn.commit()
            return {
                "success": True,
                "table_id": table_id,
                "event_type": event_type,
                "channel": channel,
                "status": "active",
            }
        finally:
            conn.close()

    def unsubscribe(self, table_id: str, event_type: str) -> Dict[str, Any]:
        """取消订阅"""
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute(
                "UPDATE webhook_subscriptions SET status = 'inactive' "
                "WHERE table_id = ? AND event_type = ?",
                (table_id, event_type),
            )
            conn.commit()
            return {"success": True, "status": "inactive"}
        finally:
            conn.close()

    def list_subscriptions(self, table_id: str = "") -> Dict[str, Any]:
        """列出订阅"""
        conn = sqlite3.connect(self.db_path)
        try:
            if table_id:
                cursor = conn.execute(
                    "SELECT table_id, event_type, callback_url, channel, status, created_at "
                    "FROM webhook_subscriptions WHERE table_id = ? AND status = 'active'",
                    (table_id,),
                )
            else:
                cursor = conn.execute(
                    "SELECT table_id, event_type, callback_url, channel, status, created_at "
                    "FROM webhook_subscriptions WHERE status = 'active'",
                )
            rows = cursor.fetchall()
            return {
                "total": len(rows),
                "subscriptions": [
                    {
                        "table_id": r[0],
                        "event_type": r[1],
                        "callback_url": r[2],
                        "channel": r[3],
                        "status": r[4],
                        "created_at": r[5],
                    }
                    for r in rows
                ],
            }
        finally:
            conn.close()

    def process_incoming_event(self, payload: Dict[str, Any],
                               signature: str = "") -> Dict[str, Any]:
        """处理传入的 Webhook 事件（签名校验 + 去重）"""
        event_type = payload.get("event_type", "")
        table_id = payload.get("table_id", "")
        record_id = payload.get("record_id", "")

        # 签名校验
        if signature and not self._verify_signature(payload, signature):
            return {"success": False, "error": "签名校验失败"}

        # 去重检查
        event_hash = self._compute_event_hash(payload)
        if self._is_duplicate(event_hash):
            return {"success": True, "status": "duplicate", "message": "重复事件已忽略"}

        # 存储事件
        event_id = f"evt_{int(time.time())}_{event_hash[:8]}"
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute(
                """INSERT INTO webhook_events
                   (event_id, event_type, table_id, record_id, payload, signature, status, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, 'pending', ?)""",
                (event_id, event_type, table_id, record_id,
                 json.dumps(payload, ensure_ascii=False),
                 signature, datetime.now().isoformat()),
            )
            conn.execute(
                "INSERT OR REPLACE INTO webhook_dedup (event_hash, created_at) VALUES (?, ?)",
                (event_hash, datetime.now().isoformat()),
            )
            conn.commit()
        finally:
            conn.close()

        # 分发到通知通道
        dispatch_result = self._dispatch_event(event_id, event_type, table_id, payload)

        # 触发 zwjh 记忆桥接
        self._trigger_memory_bridge(event_type, table_id, record_id, payload)

        return {
            "success": True,
            "event_id": event_id,
            "event_type": event_type,
            "status": "processed",
            "dispatch": dispatch_result,
        }

    def _verify_signature(self, payload: Dict[str, Any], signature: str) -> bool:
        """校验签名"""
        payload_str = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        expected = hmac.new(
            self.signing_secret.encode(),
            payload_str.encode(),
            hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(expected, signature)

    def _compute_event_hash(self, payload: Dict[str, Any]) -> str:
        """计算事件哈希（去重）"""
        key_fields = {
            "event_type": payload.get("event_type", ""),
            "table_id": payload.get("table_id", ""),
            "record_id": payload.get("record_id", ""),
            "timestamp": payload.get("timestamp", ""),
        }
        return hashlib.md5(json.dumps(key_fields, sort_keys=True).encode()).hexdigest()

    def _is_duplicate(self, event_hash: str) -> bool:
        """检查是否重复事件"""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.execute(
                "SELECT event_hash FROM webhook_dedup WHERE event_hash = ?",
                (event_hash,),
            )
            return cursor.fetchone() is not None
        finally:
            conn.close()

    def _dispatch_event(self, event_id: str, event_type: str,
                        table_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """分发事件到通知通道"""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.execute(
                "SELECT callback_url, channel, webhook_key FROM webhook_subscriptions "
                "WHERE table_id = ? AND event_type = ? AND status = 'active'",
                (table_id, event_type),
            )
            subscriptions = cursor.fetchall()
        finally:
            conn.close()

        if not subscriptions:
            return {"status": "no_subscription", "message": "无匹配的订阅"}

        results = []
        for callback_url, channel, webhook_key in subscriptions:
            try:
                result = self._send_notification(
                    channel, callback_url, webhook_key, event_type, payload
                )
                results.append({"channel": channel, "success": True, "result": result})
            except Exception as e:
                results.append({"channel": channel, "success": False, "error": str(e)})

        # 更新事件状态
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute(
                "UPDATE webhook_events SET status = 'processed', processed_at = ? "
                "WHERE event_id = ?",
                (datetime.now().isoformat(), event_id),
            )
            conn.commit()
        finally:
            conn.close()

        return {"status": "dispatched", "results": results}

    def _send_notification(self, channel: str, callback_url: str,
                           webhook_key: str, event_type: str,
                           payload: Dict[str, Any]) -> Dict[str, Any]:
        """发送通知到指定通道"""
        event_name = EVENT_TYPES.get(event_type, event_type)
        content = {
            "msgtype": "text",
            "text": {
                "content": f"KingDoc 通知: {event_name}\n"
                           f"表格: {payload.get('table_id', '')}\n"
                           f"记录: {payload.get('record_id', '')}\n"
                           f"时间: {datetime.now().isoformat()}"
            }
        }

        if self.backend is not None:
            try:
                if hasattr(self.backend, "notification_send"):
                    return self.backend.notification_send(channel, webhook_key, content)
            except Exception as e:
                return {"success": False, "error": str(e)}

        # 本地降级：仅记录不发送
        return {
            "success": True,
            "source": "local_fallback",
            "message": f"通知已记录（本地模式）。连接金山开放平台后发送到 {channel}。",
            "channel": channel,
            "content": content,
        }

    def _trigger_memory_bridge(self, event_type: str, table_id: str,
                               record_id: str, payload: Dict[str, Any]):
        """触发 zwjh 记忆桥接"""
        try:
            from engine.memory_bridge import get_memory_bridge
            bridge = get_memory_bridge(backend=self.backend)
            # 映射事件类型
            memory_event = {
                "record_created": "create",
                "record_updated": "edit",
                "record_deleted": "delete",
            }.get(event_type)
            if memory_event:
                bridge.deposit_event(
                    memory_event,
                    record_id,
                    file_name=table_id,
                    action_details=payload,
                )
        except ImportError:
            pass  # memory_bridge 不存在时跳过
        except Exception:
            pass  # 记忆写入失败不影响主流程

    def get_event_history(self, table_id: str = "", limit: int = 20) -> Dict[str, Any]:
        """获取事件历史"""
        conn = sqlite3.connect(self.db_path)
        try:
            if table_id:
                cursor = conn.execute(
                    "SELECT event_id, event_type, table_id, record_id, status, created_at, channel "
                    "FROM webhook_events WHERE table_id = ? ORDER BY id DESC LIMIT ?",
                    (table_id, limit),
                )
            else:
                cursor = conn.execute(
                    "SELECT event_id, event_type, table_id, record_id, status, created_at, channel "
                    "FROM webhook_events ORDER BY id DESC LIMIT ?",
                    (limit,),
                )
            rows = cursor.fetchall()
            return {
                "total": len(rows),
                "events": [
                    {
                        "event_id": r[0],
                        "event_type": r[1],
                        "table_id": r[2],
                        "record_id": r[3],
                        "status": r[4],
                        "created_at": r[5],
                        "channel": r[6],
                    }
                    for r in rows
                ],
            }
        finally:
            conn.close()

    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        try:
            # 事件统计
            cursor = conn.execute(
                "SELECT event_type, COUNT(*) FROM webhook_events GROUP BY event_type"
            )
            event_counts = {r[0]: r[1] for r in cursor.fetchall()}

            # 订阅统计
            cursor = conn.execute(
                "SELECT COUNT(*) FROM webhook_subscriptions WHERE status = 'active'"
            )
            active_subs = cursor.fetchone()[0]

            # 今日事件
            today = datetime.now().strftime("%Y-%m-%d")
            cursor = conn.execute(
                "SELECT COUNT(*) FROM webhook_events WHERE created_at LIKE ?",
                (f"{today}%",),
            )
            today_events = cursor.fetchone()[0]

            return {
                "total_events": sum(event_counts.values()),
                "event_breakdown": event_counts,
                "active_subscriptions": active_subs,
                "today_events": today_events,
            }
        finally:
            conn.close()


def get_webhook_center(backend: Any = None,
                       signing_secret: str = "") -> WebhookCenterEngine:
    """工厂函数"""
    return WebhookCenterEngine(backend=backend, signing_secret=signing_secret)


# ===========================================================================
# 模块级便捷函数
# ===========================================================================

def list_event_types() -> Dict[str, Any]:
    engine = get_webhook_center()
    return engine.list_event_types()

def list_channels() -> Dict[str, Any]:
    engine = get_webhook_center()
    return engine.list_channels()

def subscribe(table_id: str, event_type: str, callback_url: str,
              channel: str, webhook_key: str = "",
              signing_secret: str = "") -> Dict[str, Any]:
    engine = get_webhook_center()
    return engine.subscribe(table_id, event_type, callback_url, channel,
                            webhook_key, signing_secret)

def unsubscribe(table_id: str, event_type: str) -> Dict[str, Any]:
    engine = get_webhook_center()
    return engine.unsubscribe(table_id, event_type)

def list_subscriptions(table_id: str = "") -> Dict[str, Any]:
    engine = get_webhook_center()
    return engine.list_subscriptions(table_id)

def process_event(payload: Dict[str, Any], signature: str = "") -> Dict[str, Any]:
    engine = get_webhook_center()
    return engine.process_incoming_event(payload, signature)

def get_event_history(table_id: str = "", limit: int = 20) -> Dict[str, Any]:
    engine = get_webhook_center()
    return engine.get_event_history(table_id, limit)

def get_webhook_statistics() -> Dict[str, Any]:
    engine = get_webhook_center()
    return engine.get_statistics()
