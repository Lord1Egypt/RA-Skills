"""KingDoc 多维表格定时快照与变更摘要引擎（v4.4.0 T4）

能力：
- 每日快照：行数 + 关键字段哈希 + 每行哈希，存本地 SQLite
- 变更 diff：复用 doc_comparator / cross_compare 的单元格级比对
  输出增/删/改行清单（谁改了我的表）
- 变更摘要：按需推送（webhook_center 三通道）或写入周报文本
- 硬件自适应 + 行哈希加速：5000 行快照 + diff 目标 <= 10 秒

设计原则：
- 行哈希先做 O(n) 快速筛选，只对变化行做单元格级 diff（避免 O(n*m) 全量比对）
- 快照内容存 JSON，零第三方依赖
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

PERF_TARGET_SEC = 10.0


class TableSnapshotEngine:
    """多维表格定时快照与变更摘要引擎"""

    def __init__(self, db_path: Optional[str] = None, webhook_center: Any = None,
                 signing_secret: str = ""):
        self.db_path = db_path or self._default_db_path()
        self.webhook_center = webhook_center
        self.signing_secret = signing_secret
        self._init_db()

    def _default_db_path(self) -> str:
        skill_root = Path(__file__).resolve().parent.parent
        return str(skill_root / ".table_snapshot.db")

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS table_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_id TEXT,
                    snapshot_date TEXT,
                    row_count INTEGER,
                    field_hash TEXT,
                    content TEXT,
                    created_at TEXT,
                    UNIQUE(table_id, snapshot_date)
                )
            """)
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_snap_table_date ON table_snapshots(table_id, snapshot_date)"
            )
            conn.commit()
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # 哈希工具
    # ------------------------------------------------------------------
    @staticmethod
    def _row_hash(row: Any) -> str:
        raw = json.dumps(row, sort_keys=True, ensure_ascii=False, default=str)
        return hashlib.md5(raw.encode()).hexdigest()

    @staticmethod
    def _field_hash(rows: Sequence[Any]) -> str:
        """关键字段哈希：基于所有行的规范化内容"""
        h = hashlib.md5()
        for row in rows:
            h.update(json.dumps(row, sort_keys=True, ensure_ascii=False, default=str).encode())
            h.update(b"\n")
        return h.hexdigest()

    # ------------------------------------------------------------------
    # 快照
    # ------------------------------------------------------------------
    def take_snapshot(self, table_id: str, rows: List[List[Any]],
                      headers: Optional[List[str]] = None,
                      snapshot_date: str = "", push: bool = False,
                      base_date: str = "") -> Dict[str, Any]:
        """生成一次快照；若提供 base_date 则同时输出与基线快照的变更摘要。

        Args:
            table_id: 表格 ID
            rows: 二维表数据
            headers: 列名
            snapshot_date: 快照日期（默认今天 YYYY-MM-DD）
            push: 是否把变更摘要推送到 webhook
            base_date: 对比基线日期（为空则只快照不 diff）

        Returns:
            {"success","snapshot_date","row_count","field_hash","elapsed_ms","diff",...}
        """
        started = time.perf_counter()
        snapshot_date = snapshot_date or datetime.now().strftime("%Y-%m-%d")
        field_hash = self._field_hash(rows)
        content = json.dumps({"headers": headers or [], "rows": rows},
                             ensure_ascii=False, default=str)

        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute(
                """INSERT INTO table_snapshots (table_id, snapshot_date, row_count, field_hash, content, created_at)
                   VALUES (?, ?, ?, ?, ?, ?)
                   ON CONFLICT(table_id, snapshot_date) DO UPDATE SET
                     row_count=excluded.row_count, field_hash=excluded.field_hash,
                     content=excluded.content, created_at=excluded.created_at""",
                (table_id, snapshot_date, len(rows), field_hash, content, datetime.now().isoformat()),
            )
            conn.commit()
        finally:
            conn.close()

        diff_result: Optional[Dict[str, Any]] = None
        if base_date:
            diff_result = self.diff_snapshots(table_id, base_date, snapshot_date, headers)

        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        result = {
            "success": True,
            "table_id": table_id,
            "snapshot_date": snapshot_date,
            "row_count": len(rows),
            "field_hash": field_hash,
            "elapsed_ms": elapsed_ms,
            "within_target": elapsed_ms / 1000.0 <= PERF_TARGET_SEC,
            "diff": diff_result,
        }

        if push and diff_result and diff_result.get("total_changes", 0) > 0:
            result["push"] = self._push_summary(table_id, snapshot_date, diff_result)

        return result

    def diff_snapshots(self, table_id: str, date_a: str, date_b: str,
                       headers: Optional[List[str]] = None) -> Dict[str, Any]:
        """对比两次快照，输出增/删/改行清单"""
        conn = sqlite3.connect(self.db_path)
        try:
            row_a = conn.execute(
                "SELECT content, field_hash FROM table_snapshots WHERE table_id=? AND snapshot_date=?",
                (table_id, date_a),
            ).fetchone()
            row_b = conn.execute(
                "SELECT content, field_hash FROM table_snapshots WHERE table_id=? AND snapshot_date=?",
                (table_id, date_b),
            ).fetchone()
        finally:
            conn.close()

        if not row_a or not row_b:
            return {"success": False, "error": "基线或目标快照不存在",
                    "date_a": date_a, "date_b": date_b}

        data_a = json.loads(row_a[0]); data_b = json.loads(row_b[0])
        field_hash_a = row_a[1] if len(row_a) > 1 else ""
        field_hash_b = row_b[1] if len(row_b) > 1 else ""
        rows_a: List[List[Any]] = data_a.get("rows", [])
        rows_b: List[List[Any]] = data_b.get("rows", [])
        hdrs = headers or data_b.get("headers") or data_a.get("headers") or []

        # O(n) 行配对：优先用第一列作行主键（业务表格通常有 id 列），
        # 主键唯一时按 key 做增/删/改精确配对；否则回退内容多重集配对。
        # 每个行只落入一个类别，杜绝三重计数。
        from collections import Counter

        def row_key(row):
            if isinstance(row, (list, tuple)) and row:
                return str(row[0])
            if isinstance(row, dict):
                first = next(iter(row), "")
                return str(row.get(first, ""))
            return str(row)

        key_a = [row_key(r) for r in rows_a]
        key_b = [row_key(r) for r in rows_b]
        hash_a = [self._row_hash(r) for r in rows_a]
        hash_b = [self._row_hash(r) for r in rows_b]

        unique_keys = (len(set(key_a)) == len(key_a) and len(set(key_b)) == len(key_b)
                       and all(k for k in key_a + key_b))
        changed_idx: List[int] = []   # b 侧被修改行的索引
        changed_old_idx: Dict[int, int] = {}  # b_idx -> a_idx
        added_idx: List[int] = []
        deleted_idx: List[int] = []
        moved_idx: List[int] = []

        if unique_keys:
            # 主键唯一：精确按 key 配对
            idx_a = {k: i for i, k in enumerate(key_a)}
            idx_b = {k: i for i, k in enumerate(key_b)}
            set_a, set_b = set(key_a), set(key_b)
            for k in set_b - set_a:
                added_idx.append(idx_b[k])
            for k in set_a - set_b:
                deleted_idx.append(idx_a[k])
            common_keys = set_a & set_b
            for k in common_keys:
                ia, ib = idx_a[k], idx_b[k]
                if hash_a[ia] != hash_b[ib]:
                    changed_idx.append(ib)
                    changed_old_idx[ib] = ia
            # 重排判定：比较公共 key 在两侧「相对顺序(rank)」是否变化，
            # 而非绝对索引——否则表首插一行会让后面所有未变行误报为 moved。
            rank_a = {k: r for r, k in enumerate(k for k in key_a if k in common_keys)}
            rank_b = {k: r for r, k in enumerate(k for k in key_b if k in common_keys)}
            for k in common_keys:
                if hash_a[idx_a[k]] == hash_b[idx_b[k]] and rank_a[k] != rank_b[k]:
                    moved_idx.append(idx_b[k])
        else:
            # 无可靠主键：按内容多重集 + 位置配对
            counter_a = Counter(hash_a); counter_b = Counter(hash_b)
            common = counter_a & counter_b
            only_a = counter_a - common
            only_b = counter_b - common
            consumed_a: Counter = Counter(); consumed_b: Counter = Counter()
            excluded: set = set()
            for i in range(min(len(rows_a), len(rows_b))):
                ha, hb = hash_a[i], hash_b[i]
                if ha == hb:
                    continue
                if only_a.get(ha, 0) > consumed_a[ha] and only_b.get(hb, 0) > consumed_b[hb]:
                    changed_idx.append(i); changed_old_idx[i] = i
                    consumed_a[ha] += 1; consumed_b[hb] += 1; excluded.add(i)
            for i in range(len(rows_b)):
                h = hash_b[i]
                if i in excluded:
                    continue
                if only_b.get(h, 0) > consumed_b[h]:
                    added_idx.append(i); consumed_b[h] += 1
            for i in range(len(rows_a)):
                h = hash_a[i]
                if i in excluded:
                    continue
                if only_a.get(h, 0) > consumed_a[h]:
                    deleted_idx.append(i); consumed_a[h] += 1

        # 对修改行做单元格级 diff（复用 cross_compare，等价于 doc_comparator 的比对内核）
        cell_changes: List[Dict[str, Any]] = []
        if changed_idx:
            sub_a = [rows_a[changed_old_idx[b]] for b in changed_idx]
            sub_b = [rows_b[b] for b in changed_idx]
            cell_res: Dict[str, Any] = {}
            try:
                from engine.cross_compare import diff_cells as _diff_cells
                cell_res = _diff_cells(sub_a, sub_b, hdrs)
            except Exception:
                cell_res = {}
            for local, b_idx in enumerate(changed_idx):
                a_idx = changed_old_idx[b_idx]
                matched = [dict(c) for c in cell_res.get("cells", []) if c.get("row") == local]
                if matched:
                    for item in matched:
                        item["row"] = b_idx
                        item["row_before"] = a_idx
                        cell_changes.append(item)
                else:
                    cell_changes.append({
                        "row": b_idx, "row_before": a_idx, "status": "modified",
                        "changes": [{"col_name": "整行", "old": rows_a[a_idx],
                                     "new": rows_b[b_idx]}],
                    })

        added_rows = [
            {"row": i, "values": rows_b[i],
             "key_value": self._row_label(rows_b[i], hdrs)}
            for i in added_idx
        ]
        deleted_rows = [
            {"row": i, "values": rows_a[i],
             "key_value": self._row_label(rows_a[i], hdrs)}
            for i in deleted_idx
        ]
        moved_rows = [
            {"row": i, "value": rows_b[i], "key": row_key(rows_b[i])}
            for i in moved_idx
        ]
        return {
            "success": True,
            "table_id": table_id,
            "date_a": date_a,
            "date_b": date_b,
            "rows_before": len(rows_a),
            "rows_after": len(rows_b),
            "added_rows": added_rows,
            "deleted_rows": deleted_rows,
            "modified_rows": cell_changes,
            "moved_rows": moved_rows,
            "total_changes": len(added_rows) + len(deleted_rows) + len(cell_changes) + len(moved_rows),
            "field_hash_changed": field_hash_a != field_hash_b,
        }

    @staticmethod
    def _row_label(row: Any, headers: Sequence[str]) -> str:
        """生成可读行标签（首列值）"""
        if isinstance(row, (list, tuple)) and row:
            name = headers[0] if headers else "首列"
            return f"{name}={row[0]}"
        if isinstance(row, dict):
            first = next(iter(row), "")
            return f"{first}={row.get(first)}"
        return str(row)[:40]

    # ------------------------------------------------------------------
    # 变更摘要 / 推送 / 周报
    # ------------------------------------------------------------------
    def build_summary_text(self, table_id: str, diff: Dict[str, Any]) -> str:
        """生成人类可读的变更摘要文本"""
        lines = [
            f"【表格变更摘要】{table_id}",
            f"对比 {diff.get('date_a')} → {diff.get('date_b')}",
            f"行数：{diff.get('rows_before')} → {diff.get('rows_after')}",
            f"新增 {len(diff.get('added_rows', []))} / 删除 {len(diff.get('deleted_rows', []))} / 修改 {len(diff.get('modified_rows', []))}",
        ]
        for r in diff.get("added_rows", [])[:10]:
            lines.append(f"  + {r.get('key_value')}")
        for r in diff.get("deleted_rows", [])[:10]:
            lines.append(f"  - {r.get('key_value')}")
        for r in diff.get("modified_rows", [])[:10]:
            cols = r.get("changes", [])
            desc = ", ".join(f"{c.get('col_name')}:{c.get('old')}→{c.get('new')}" for c in cols[:3])
            lines.append(f"  ~ 行{r.get('row')} {desc}")
        return "\n".join(lines)

    def _push_summary(self, table_id: str, snapshot_date: str,
                      diff: Dict[str, Any]) -> Dict[str, Any]:
        if self.webhook_center is None:
            return {"pushed": False, "reason": "未配置 webhook_center"}
        payload = {
            "event_type": "record_updated",
            "table_id": table_id,
            "record_id": f"snapshot_{snapshot_date}",
            "event_name": "表格变更摘要",
            "summary": self.build_summary_text(table_id, diff),
            "timestamp": datetime.now().isoformat(),
        }
        try:
            res = self.webhook_center.process_incoming_event(payload, "")
            return {"pushed": bool(res.get("success")), "result": res}
        except Exception as e:
            return {"pushed": False, "error": str(e)}

    def list_snapshots(self, table_id: str = "", limit: int = 30) -> Dict[str, Any]:
        conn = sqlite3.connect(self.db_path)
        try:
            if table_id:
                rows = conn.execute(
                    """SELECT table_id, snapshot_date, row_count, field_hash, created_at
                       FROM table_snapshots WHERE table_id=? ORDER BY snapshot_date DESC LIMIT ?""",
                    (table_id, limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    """SELECT table_id, snapshot_date, row_count, field_hash, created_at
                       FROM table_snapshots ORDER BY id DESC LIMIT ?""",
                    (limit,),
                ).fetchall()
        finally:
            conn.close()
        return {
            "success": True,
            "snapshots": [
                {"table_id": r[0], "snapshot_date": r[1], "row_count": r[2],
                 "field_hash": r[3], "created_at": r[4]}
                for r in rows
            ],
        }

    def get_status(self) -> Dict[str, Any]:
        conn = sqlite3.connect(self.db_path)
        try:
            total = conn.execute("SELECT COUNT(*) FROM table_snapshots").fetchone()[0]
        finally:
            conn.close()
        return {
            "version": "4.4.0",
            "perf_target_sec": PERF_TARGET_SEC,
            "total_snapshots": total,
            "push_enabled": self.webhook_center is not None,
        }


# ---------------------------------------------------------------------------
# 模块级便捷函数
# ---------------------------------------------------------------------------
def get_table_snapshot(db_path: Optional[str] = None,
                       webhook_center: Any = None) -> TableSnapshotEngine:
    return TableSnapshotEngine(db_path, webhook_center)


def snapshot(table_id: str, rows: List[List[Any]], **kwargs) -> Dict[str, Any]:
    return TableSnapshotEngine(kwargs.pop("db_path", None),
                               kwargs.pop("webhook_center", None)).take_snapshot(table_id, rows, **kwargs)


def diff(table_id: str, date_a: str, date_b: str,
         headers: Optional[List[str]] = None, **kwargs) -> Dict[str, Any]:
    return TableSnapshotEngine(kwargs.get("db_path")).diff_snapshots(table_id, date_a, date_b, headers)
