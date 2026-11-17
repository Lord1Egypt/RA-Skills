"""KingDoc 收集表答卷实时推送引擎（v4.4.0 T1）

能力：
- 轮询答卷接口 + 增量游标检测新答卷（本地 SQLite 记录上次最大游标，零密钥可用）
- 新答卷即触发 webhook_center 三通道推送（关键字段摘要 + 答卷链接）
- 端到端延迟统计（验收目标 <= 30 秒）
- 本地降级：无 webhook 配置时只落库不推送，不中断主流程
- 硬件自适应：批量拉取时读取 hardware.py 的 batch_chunk

设计原则：
- 零第三方依赖（仅标准库）
- 游标策略：优先 answer 的时间字段（update_time/created_at/submit_time），
  其次 answer_id / id 数值；均缺失时用内容哈希兜底，保证「只推新增不重复」
- 复用 webhook_center.process_incoming_event 的签名 + 去重链路
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# 答卷时间字段优先级（用于构造游标）
CURSOR_TIME_FIELDS = ("update_time", "updated_at", "submit_time", "created_at", "create_time")
# 答卷 ID 字段优先级
CURSOR_ID_FIELDS = ("answer_id", "id", "response_id", "rid")

# 延迟验收阈值（秒）
LATENCY_TARGET_SEC = 30.0


class FormRealtimeEngine:
    """收集表答卷实时推送引擎"""

    def __init__(self, backend: Any = None, db_path: Optional[str] = None,
                 webhook_center: Any = None, signing_secret: str = ""):
        self.backend = backend
        self.db_path = db_path or self._default_db_path()
        self.webhook_center = webhook_center
        self.signing_secret = signing_secret
        self._init_db()

    def _default_db_path(self) -> str:
        skill_root = Path(__file__).resolve().parent.parent
        return str(skill_root / ".form_realtime.db")

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS form_realtime_cursors (
                    form_id TEXT PRIMARY KEY,
                    last_cursor TEXT,
                    last_count INTEGER DEFAULT 0,
                    updated_at TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS form_realtime_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    form_id TEXT,
                    answer_id TEXT,
                    cursor TEXT,
                    summary TEXT,
                    answer_link TEXT,
                    pushed INTEGER DEFAULT 0,
                    latency_ms REAL DEFAULT 0,
                    created_at TEXT
                )
            """)
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_frt_events_form ON form_realtime_events(form_id)"
            )
            conn.commit()
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # 游标工具
    # ------------------------------------------------------------------
    @staticmethod
    def _answer_cursor(answer: Dict[str, Any]) -> str:
        """构造单条答卷的增量游标（时间优先，ID 次之，内容哈希兜底）"""
        for field in CURSOR_TIME_FIELDS:
            val = answer.get(field)
            if val not in (None, ""):
                return f"t:{val}"
        for field in CURSOR_ID_FIELDS:
            val = answer.get(field)
            if val not in (None, ""):
                return f"i:{val}"
        raw = json.dumps(answer, sort_keys=True, ensure_ascii=False, default=str)
        return "h:" + hashlib.md5(raw.encode()).hexdigest()

    @staticmethod
    def _cursor_sort_key(cursor: str):
        """游标排序键：统一返回 (类别序, 字符串) 二元组，杜绝 int/str 混比 TypeError。

        - t: 时间游标（类别 1）—— ISO/时间戳字符串本身字典序可比较
        - i: ID 游标（类别 0）—— 纯数字零填充 24 位使字典序=数值序，非数字退化为原串
        - h: 内容哈希（类别 2）—— 原串比较
        类别序保证不同游标类型之间不比较第二元素（i<t<h 固定优先级）。
        """
        if cursor.startswith("t:"):
            return (1, cursor[2:])
        if cursor.startswith("i:"):
            tail = cursor[2:]
            padded = tail.zfill(24) if tail.isdigit() else "s:" + tail
            return (0, padded)
        return (2, cursor)

    @staticmethod
    def _answer_id(answer: Dict[str, Any], cursor: str) -> str:
        for field in CURSOR_ID_FIELDS:
            val = answer.get(field)
            if val not in (None, ""):
                return str(val)
        return cursor[-12:]

    def get_cursor(self, form_id: str) -> Dict[str, Any]:
        conn = sqlite3.connect(self.db_path)
        try:
            row = conn.execute(
                "SELECT last_cursor, last_count, updated_at FROM form_realtime_cursors WHERE form_id=?",
                (form_id,),
            ).fetchone()
        finally:
            conn.close()
        if not row:
            return {"form_id": form_id, "last_cursor": "", "last_count": 0, "initialized": False}
        return {
            "form_id": form_id,
            "last_cursor": row[0] or "",
            "last_count": row[1] or 0,
            "updated_at": row[2] or "",
            "initialized": True,
        }

    def reset_cursor(self, form_id: str) -> Dict[str, Any]:
        """重置游标（下次轮询视为全量，用于重建订阅）"""
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("DELETE FROM form_realtime_cursors WHERE form_id=?", (form_id,))
            conn.commit()
        finally:
            conn.close()
        return {"success": True, "form_id": form_id, "reset": True}

    # ------------------------------------------------------------------
    # 摘要 + 链接
    # ------------------------------------------------------------------
    @staticmethod
    def _build_summary(answer: Dict[str, Any], key_fields: Optional[List[str]] = None,
                       max_chars: int = 200) -> str:
        """构造答卷关键字段摘要（只取指定题目，避免整卷刷屏）"""
        answers = answer.get("answers", {}) or {}
        parts: List[str] = []
        if key_fields:
            for field in key_fields:
                val = answers.get(field) or answer.get(field)
                if val not in (None, ""):
                    text = val if isinstance(val, str) else json.dumps(val, ensure_ascii=False, default=str)
                    parts.append(f"{field}: {text}")
        else:
            for k, v in list(answers.items())[:5]:
                text = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)
                parts.append(f"{k}: {text}")
        summary = " | ".join(parts)
        return summary[:max_chars] if len(summary) > max_chars else summary

    @staticmethod
    def _build_link(answer: Dict[str, Any], form_id: str, answer_id: str,
                    answer_url_template: str = "") -> str:
        if answer_url_template:
            try:
                return answer_url_template.format(
                    form_id=form_id, answer_id=answer_id,
                    **{k: v for k, v in answer.items() if isinstance(v, (str, int, float))},
                )
            except (KeyError, IndexError, ValueError):
                pass
        # 兜底：从答卷自带链接字段读取
        for field in ("answer_url", "url", "link"):
            val = answer.get(field)
            if val:
                return str(val)
        return ""

    # ------------------------------------------------------------------
    # 主流程
    # ------------------------------------------------------------------
    def poll_once(self, form_id: str, answers: Optional[List[Dict[str, Any]]] = None,
                  key_fields: Optional[List[str]] = None,
                  answer_url_template: str = "",
                  form_name: str = "") -> Dict[str, Any]:
        """单次轮询：检测新答卷 -> 落库 -> 推送 -> 更新游标。

        Args:
            form_id: 表单 ID
            answers: 直接注入的答卷列表（测试/本地模式用）；为 None 时走 backend 拉取
            key_fields: 摘要中保留的题目 ID 列表
            answer_url_template: 答卷链接模板，支持 {form_id}/{answer_id} 占位
            form_name: 表单名（推送文案用）

        Returns:
            {"success", "detected", "pushed", "latency_ms", "within_target", ...}
        """
        started = time.perf_counter()

        # 1. 获取答卷
        if answers is None:
            if self.backend is None:
                return {
                    "success": False,
                    "error": "本地降级模式：未注入答卷且未配置云端 backend",
                    "hint": "传入 answers 参数，或配置金山 App Key 后使用",
                    "detected": 0, "pushed": 0,
                }
            try:
                result = self.backend.kdoc_form_answers(form_id, 100)
                answers = result.get("answers", [])
            except Exception as e:
                return {"success": False, "error": f"拉取答卷失败：{e}", "detected": 0, "pushed": 0}
        answers = answers or []

        # 2. 硬件自适应批量上限
        try:
            from engine.hardware import get_recommended_settings
            chunk = get_recommended_settings().get("batch_chunk", 100)
        except Exception:
            chunk = 100

        # 3. 计算游标，找出新增
        cursor_state = self.get_cursor(form_id)
        last_cursor = cursor_state.get("last_cursor", "")
        pairs = [(self._answer_cursor(a), a) for a in answers[:chunk]]
        first_run = not bool(last_cursor)
        if last_cursor:
            last_key = self._cursor_sort_key(last_cursor)
            new_pairs = [(c, a) for c, a in pairs if self._cursor_sort_key(c) > last_key]
            to_record = new_pairs
        else:
            # 首次运行：全量视为「基线」，落库留痕但不推送（避免历史答卷刷屏）
            new_pairs = []
            to_record = pairs

        # 4. 落库 + 推送
        pushed = 0
        recorded = 0
        push_details: List[Dict[str, Any]] = []
        conn = sqlite3.connect(self.db_path)
        try:
            for cursor, answer in to_record:
                aid = self._answer_id(answer, cursor)
                summary = self._build_summary(answer, key_fields)
                link = self._build_link(answer, form_id, aid, answer_url_template)
                now = datetime.now().isoformat()

                ev_pushed = 0
                push_result: Dict[str, Any] = {}
                # 首次运行只建基线落库，不推送历史答卷（避免刷屏）
                if self.webhook_center is not None and not first_run:
                    payload = {
                        "event_type": "record_created",
                        "table_id": f"form:{form_id}",
                        "record_id": aid,
                        "event_name": "新答卷",
                        "form_id": form_id,
                        "form_name": form_name or form_id,
                        "summary": summary,
                        "answer_link": link,
                        "timestamp": now,
                    }
                    try:
                        # 内部调用：不传签名（验签是 webhook 外部入口的职责）。
                        # 若用本模块 secret 签名，会与 webhook_center 自身 secret 不一致导致全部验签失败。
                        push_result = self.webhook_center.process_incoming_event(payload, "")
                        ev_pushed = 1 if push_result.get("success") else 0
                        pushed += ev_pushed
                    except Exception as e:
                        push_result = {"success": False, "error": str(e)}
                push_details.append({
                    "answer_id": aid, "pushed": bool(ev_pushed),
                    "summary": summary, "link": link, "push": push_result,
                })

                latency_ms = round((time.perf_counter() - started) * 1000, 2)
                conn.execute(
                    """INSERT INTO form_realtime_events
                       (form_id, answer_id, cursor, summary, answer_link, pushed, latency_ms, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (form_id, aid, cursor, summary, link, ev_pushed, latency_ms, now),
                )
                recorded += 1

            # 5. 更新游标
            if pairs:
                max_cursor = max((c for c, _ in pairs), key=self._cursor_sort_key)
                conn.execute(
                    """INSERT INTO form_realtime_cursors (form_id, last_cursor, last_count, updated_at)
                       VALUES (?, ?, ?, ?)
                       ON CONFLICT(form_id) DO UPDATE SET
                         last_cursor=excluded.last_cursor,
                         last_count=excluded.last_count,
                         updated_at=excluded.updated_at""",
                    (form_id, max_cursor, len(answers), datetime.now().isoformat()),
                )
            conn.commit()
        finally:
            conn.close()

        latency_ms = round((time.perf_counter() - started) * 1000, 2)
        return {
            "success": True,
            "form_id": form_id,
            "first_run": first_run,
            "total_answers": len(answers),
            "detected": len(new_pairs),
            "recorded": recorded,
            "pushed": pushed,
            "latency_ms": latency_ms,
            "latency_sec": round(latency_ms / 1000.0, 3),
            "within_target": latency_ms / 1000.0 <= LATENCY_TARGET_SEC,
            "details": push_details,
            "mode": "push" if self.webhook_center is not None else "local_only",
        }

    def _sign(self, payload: Dict[str, Any]) -> str:
        import hashlib as _h
        import hmac
        payload_str = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        return hmac.new(
            self.signing_secret.encode(), payload_str.encode(), _h.sha256
        ).hexdigest()

    def get_push_history(self, form_id: str = "", limit: int = 20) -> Dict[str, Any]:
        conn = sqlite3.connect(self.db_path)
        try:
            if form_id:
                rows = conn.execute(
                    """SELECT answer_id, summary, answer_link, pushed, latency_ms, created_at
                       FROM form_realtime_events WHERE form_id=? ORDER BY id DESC LIMIT ?""",
                    (form_id, limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    """SELECT form_id, answer_id, summary, answer_link, pushed, latency_ms, created_at
                       FROM form_realtime_events ORDER BY id DESC LIMIT ?""",
                    (limit,),
                ).fetchall()
        finally:
            conn.close()
        keys = (["answer_id", "summary", "answer_link", "pushed", "latency_ms", "created_at"]
                if form_id else
                ["form_id", "answer_id", "summary", "answer_link", "pushed", "latency_ms", "created_at"])
        return {"success": True, "events": [dict(zip(keys, r)) for r in rows]}

    def get_status(self) -> Dict[str, Any]:
        conn = sqlite3.connect(self.db_path)
        try:
            total = conn.execute("SELECT COUNT(*) FROM form_realtime_events").fetchone()[0]
            pushed = conn.execute(
                "SELECT COUNT(*) FROM form_realtime_events WHERE pushed=1"
            ).fetchone()[0]
            forms = conn.execute(
                "SELECT COUNT(*) FROM form_realtime_cursors"
            ).fetchone()[0]
        finally:
            conn.close()
        return {
            "version": "4.4.0",
            "latency_target_sec": LATENCY_TARGET_SEC,
            "total_events": total,
            "pushed_events": pushed,
            "tracked_forms": forms,
            "mode": "push" if self.webhook_center is not None else "local_only",
        }


# ---------------------------------------------------------------------------
# 模块级便捷函数
# ---------------------------------------------------------------------------
def get_form_realtime(backend: Any = None, db_path: Optional[str] = None,
                      webhook_center: Any = None, signing_secret: str = "") -> FormRealtimeEngine:
    return FormRealtimeEngine(backend, db_path, webhook_center, signing_secret)


def poll_answers(form_id: str, answers: Optional[List[Dict[str, Any]]] = None,
                 key_fields: Optional[List[str]] = None,
                 answer_url_template: str = "", **kwargs) -> Dict[str, Any]:
    engine = FormRealtimeEngine(**kwargs)
    return engine.poll_once(form_id, answers, key_fields, answer_url_template)


def get_realtime_status(**kwargs) -> Dict[str, Any]:
    return FormRealtimeEngine(**kwargs).get_status()
