"""KingDoc 答卷一键沉淀多维表格引擎（v4.4.0 T3）

能力：
- 复用 v4.1 bidata_io.py 已打通的四类字段序列化规则
  （date / link / select / person）
- 收集表答卷 -> 多维表格行一条命令（按「问题→字段」映射 + 字段类型）
- person / link 字段双向可编辑：沉淀后可从多维表格行反向生成答卷更新草稿
- 本地降级：无云端 backend 时输出结构化 JSON + 落库，不中断

设计原则：
- 序列化逻辑直接引用 bidata_io.FIELD_SERIALIZE_RULES（唯一真相源，不重复实现）
- 硬件自适应批量写入（复用 quota_manager.get_safe_batch_params）
- 零第三方依赖（仅标准库）
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 直接复用 bidata_io 的四类字段序列化规则（唯一真相源）
from engine.bidata_io import FIELD_SERIALIZE_RULES

# 双向可编辑字段（沉淀后支持反向回写答卷）
BIDIRECTIONAL_FIELDS = ("person", "link")


class FormToBidataEngine:
    """答卷 -> 多维表格沉淀引擎"""

    def __init__(self, backend: Any = None, db_path: Optional[str] = None):
        self.backend = backend
        self.db_path = db_path or self._default_db_path()
        self._init_db()

    def _default_db_path(self) -> str:
        skill_root = Path(__file__).resolve().parent.parent
        return str(skill_root / ".form_to_bidata.db")

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS form_bidata_rows (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    form_id TEXT,
                    table_id TEXT,
                    answer_id TEXT,
                    row_data TEXT,
                    created_at TEXT,
                    UNIQUE(form_id, table_id, answer_id)
                )
            """)
            conn.commit()
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # 序列化 / 反序列化
    # ------------------------------------------------------------------
    @staticmethod
    def get_field_rules() -> Dict[str, Any]:
        return {
            "rules": [
                {"type": k, "name": v["name"], "storage": v["storage"]}
                for k, v in FIELD_SERIALIZE_RULES.items()
            ],
            "bidirectional_fields": list(BIDIRECTIONAL_FIELDS),
        }

    def _serialize_value(self, field_type: str, value: Any) -> Any:
        """按字段类型序列化单个值"""
        rule = FIELD_SERIALIZE_RULES.get(field_type)
        if not rule or value in (None, ""):
            return value
        try:
            return rule["serialize"](value)
        except Exception:
            return value

    def _deserialize_value(self, field_type: str, value: Any) -> Any:
        """反向反序列化（双向字段用）"""
        rule = FIELD_SERIALIZE_RULES.get(field_type)
        if not rule or value in (None, ""):
            return value
        try:
            return rule["deserialize"](value)
        except Exception:
            return value

    def map_answer(self, answer: Dict[str, Any],
                   field_map: Dict[str, Dict[str, str]]) -> Dict[str, Any]:
        """把单条答卷按映射转成多维表格行。

        field_map: {目标字段名: {"question": 题目ID, "type": 字段类型}}
        """
        raw = answer.get("answers", answer) or {}
        row: Dict[str, Any] = {}
        for target_field, spec in field_map.items():
            qid = spec.get("question", target_field)
            ftype = spec.get("type", "text")
            val = raw.get(qid, answer.get(qid))
            row[target_field] = self._serialize_value(ftype, val)
        return row

    # ------------------------------------------------------------------
    # 沉淀主流程
    # ------------------------------------------------------------------
    def deposit(self, form_id: str, table_id: str, answers: List[Dict[str, Any]],
                field_map: Dict[str, Dict[str, str]], batch_size: int = 100) -> Dict[str, Any]:
        """答卷一键沉淀为多维表格行。

        Args:
            form_id: 来源表单 ID
            table_id: 目标多维表格 ID
            answers: 答卷列表
            field_map: {目标字段: {"question":题ID, "type": date/link/select/person/...}}
            batch_size: 批量写入大小

        Returns:
            {"success","written","skipped","local_only","rows",...}
        """
        if not answers:
            return {"success": False, "error": "无答卷可沉淀", "written": 0}

        # 硬件自适应削峰
        try:
            from engine.hardware import get_recommended_settings
            chunk = get_recommended_settings().get("batch_chunk", batch_size)
            batch_size = min(batch_size, chunk)
        except Exception:
            pass

        rows: List[Dict[str, Any]] = []
        meta: List[Tuple[str, str]] = []  # (answer_id, row_json)
        for answer in answers:
            aid = str(answer.get("answer_id", answer.get("id", "")))
            row = self.map_answer(answer, field_map)
            rows.append(row)
            meta.append((aid, json.dumps(row, ensure_ascii=False)))

        written = 0
        errors: List[str] = []
        cloud_mode = self.backend is not None and bool(table_id)

        if cloud_mode:
            for i in range(0, len(rows), batch_size):
                batch = rows[i:i + batch_size]
                try:
                    if hasattr(self.backend, "dbf_record_add_batch"):
                        self.backend.dbf_record_add_batch(table_id, batch)
                        written += len(batch)
                    elif hasattr(self.backend, "dbf_record_add"):
                        for rec in batch:
                            self.backend.dbf_record_add(table_id, rec)
                            written += 1
                    else:
                        errors.append("backend 未提供 dbf_record_add(_batch) 接口")
                        break
                except Exception as e:
                    errors.append(f"批量写入失败：{e}")

        # 无论云端成功与否都落本地记录（可追溯 + 本地降级）
        conn = sqlite3.connect(self.db_path)
        try:
            for (aid, row_json), row in zip(meta, rows):
                conn.execute(
                    """INSERT OR REPLACE INTO form_bidata_rows
                       (form_id, table_id, answer_id, row_data, created_at)
                       VALUES (?, ?, ?, ?, ?)""",
                    (form_id, table_id, aid, row_json, datetime.now().isoformat()),
                )
            conn.commit()
        finally:
            conn.close()

        bidding_fields = [
            f for f, spec in field_map.items() if spec.get("type") in BIDIRECTIONAL_FIELDS
        ]
        return {
            "success": len(errors) == 0,
            "form_id": form_id,
            "table_id": table_id,
            "total": len(rows),
            "written": written if cloud_mode else 0,
            "local_recorded": len(rows),
            "local_only": not cloud_mode,
            "bidirectional_fields": bidding_fields,
            "errors": errors,
            "rows": rows[:20],
            "hint": "" if cloud_mode else "本地降级模式：已生成结构化行并落库，配置云端后调用 dbf_record_add_batch 写入",
        }

    def prepare_update_draft(self, form_id: str, table_id: str, answer_id: str,
                             updated_fields: Dict[str, Any],
                             field_map: Dict[str, Dict[str, str]]) -> Dict[str, Any]:
        """从多维表格行反向生成答卷更新草稿（person/link 双向可编辑）。

        输入的多维表格字段值是「序列化后的存储值」，本方法反序列化回答卷字段值。
        """
        draft: Dict[str, Any] = {}
        for target_field, stored_val in updated_fields.items():
            spec = field_map.get(target_field)
            if not spec:
                continue
            ftype = spec.get("type", "text")
            if ftype not in BIDIRECTIONAL_FIELDS:
                continue
            qid = spec.get("question", target_field)
            draft[qid] = self._deserialize_value(ftype, stored_val)
        return {
            "success": True,
            "form_id": form_id,
            "table_id": table_id,
            "answer_id": answer_id,
            "draft_answers": draft,
            "editable_fields": list(draft.keys()),
            "hint": "草稿已生成；调用表单答卷更新接口时把 draft_answers 作为 answers 提交",
        }

    def get_deposit_history(self, form_id: str = "", table_id: str = "",
                            limit: int = 20) -> Dict[str, Any]:
        conn = sqlite3.connect(self.db_path)
        try:
            clauses, params = [], []
            if form_id:
                clauses.append("form_id=?"); params.append(form_id)
            if table_id:
                clauses.append("table_id=?"); params.append(table_id)
            where = " WHERE " + " AND ".join(clauses) if clauses else ""
            rows = conn.execute(
                f"""SELECT form_id, table_id, answer_id, row_data, created_at
                    FROM form_bidata_rows{where} ORDER BY id DESC LIMIT ?""",
                tuple(params) + (limit,),
            ).fetchall()
        finally:
            conn.close()
        return {
            "success": True,
            "records": [
                {"form_id": r[0], "table_id": r[1], "answer_id": r[2],
                 "row_data": json.loads(r[3]) if r[3] else {}, "created_at": r[4]}
                for r in rows
            ],
        }


# ---------------------------------------------------------------------------
# 模块级便捷函数
# ---------------------------------------------------------------------------
def get_form_to_bidata(backend: Any = None, db_path: Optional[str] = None) -> FormToBidataEngine:
    return FormToBidataEngine(backend, db_path)


def deposit_answers(form_id: str, table_id: str, answers: List[Dict[str, Any]],
                    field_map: Dict[str, Dict[str, str]], **kwargs) -> Dict[str, Any]:
    return FormToBidataEngine(**kwargs).deposit(form_id, table_id, answers, field_map)


def field_rules() -> Dict[str, Any]:
    return FormToBidataEngine.get_field_rules()
