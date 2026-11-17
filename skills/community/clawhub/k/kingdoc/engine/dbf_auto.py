"""KingDoc 多维表格字段自动化引擎

字段层支持公式字段/关联字段/汇总字段的创建与批量填充：
- 公式字段：通过 et/dbt/form API 记录级接口写入公式
- 关联字段：建立表间关联关系
- 汇总字段：聚合计算（SUM/AVG/COUNT/MAX/MIN）
- 批量填充：硬件自适应削峰，配额管理器限速

本地降级：云端不可用时返回友好提示。
"""
from __future__ import annotations

import json
import sqlite3
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 字段类型映射
FIELD_TYPE_MAP: Dict[str, str] = {
    "text": "text",
    "number": "number",
    "select": "select",
    "multi_select": "multi_select",
    "date": "date",
    "person": "person",
    "link": "link",
    "formula": "formula",
    "relation": "relation",
    "rollup": "rollup",
    "checkbox": "checkbox",
    "url": "url",
    "email": "email",
    "phone": "phone",
    "currency": "currency",
    "percent": "percent",
}

# 汇总操作类型
ROLLUP_OPERATIONS: Dict[str, str] = {
    "sum": "SUM",
    "avg": "AVG",
    "count": "COUNT",
    "max": "MAX",
    "min": "MIN",
    "count_values": "COUNT_VALUES",
    "count_unique": "COUNT_UNIQUE",
}

# 公式函数库（常用公式模板）
FORMULA_TEMPLATES: Dict[str, str] = {
    "sum_range": "=SUM({range})",
    "avg_range": "=AVERAGE({range})",
    "count_range": "=COUNT({range})",
    "if_condition": "=IF({condition}, {true_val}, {false_val})",
    "concat": "=CONCAT({fields})",
    "datedif": "=DATEDIF({start}, {end}, \"{unit}\")",
    "today": "=TODAY()",
    "round": "=ROUND({field}, {digits})",
}


class DbfAutoEngine:
    """多维表格字段自动化引擎"""

    def __init__(self, backend: Any = None, db_path: Optional[str] = None):
        self.backend = backend
        self.db_path = db_path or self._default_db_path()
        self._init_db()

    def _default_db_path(self) -> str:
        skill_root = Path(__file__).resolve().parent.parent
        return str(skill_root / ".dbf_auto_history.db")

    def _init_db(self):
        """初始化 SQLite 历史表"""
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS dbf_auto_operations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_id TEXT,
                    operation_type TEXT,
                    field_name TEXT,
                    status TEXT,
                    created_at TEXT,
                    completed_at TEXT,
                    result TEXT,
                    error TEXT
                )
            """)
            conn.commit()
        finally:
            conn.close()

    def list_field_types(self) -> Dict[str, Any]:
        """列出所有支持的字段类型"""
        return {
            "field_types": [
                {"id": k, "name": v} for k, v in FIELD_TYPE_MAP.items()
            ]
        }

    def list_formula_templates(self) -> Dict[str, Any]:
        """列出公式模板"""
        return {
            "templates": [
                {"id": k, "template": v}
                for k, v in FORMULA_TEMPLATES.items()
            ]
        }

    def list_rollup_operations(self) -> Dict[str, Any]:
        """列出汇总操作类型"""
        return {
            "operations": [
                {"id": k, "name": v}
                for k, v in ROLLUP_OPERATIONS.items()
            ]
        }

    def create_field(self, table_id: str, field_name: str, field_type: str,
                     options: Optional[List[str]] = None,
                     formula: str = "", relation_table_id: str = "",
                     rollup_field: str = "", rollup_operation: str = "") -> Dict[str, Any]:
        """创建字段（公式/关联/汇总/基础字段）"""
        if field_type not in FIELD_TYPE_MAP:
            return {
                "success": False,
                "error": f"不支持的字段类型: {field_type}。支持: {list(FIELD_TYPE_MAP.keys())}",
            }

        field_config: Dict[str, Any] = {
            "name": field_name,
            "type": FIELD_TYPE_MAP[field_type],
        }

        # 根据类型补充配置
        if field_type == "select" and options:
            field_config["options"] = [{"name": opt} for opt in options]
        elif field_type == "formula" and formula:
            field_config["formula"] = formula
        elif field_type == "relation" and relation_table_id:
            field_config["relation_table_id"] = relation_table_id
        elif field_type == "rollup" and rollup_field and rollup_operation:
            field_config["rollup_field"] = rollup_field
            field_config["rollup_operation"] = rollup_operation

        # 云端执行
        if self.backend is not None:
            try:
                if hasattr(self.backend, "dbf_field_create"):
                    result = self.backend.dbf_field_create(table_id, field_config)
                    self._log_operation(table_id, "create_field", field_name, "success")
                    return {"success": True, "field": field_config, "result": result}
            except Exception as e:
                self._log_operation(table_id, "create_field", field_name, "failed", error=str(e))
                return {"success": False, "error": f"创建字段失败: {e}"}

        # 本地降级
        return {
            "success": True,
            "source": "local_fallback",
            "message": "字段配置已生成（本地模式）。连接金山开放平台后可在线创建。",
            "field_config": field_config,
            "hint": "配置 App Key 后，字段将通过 dbt API 在线创建。",
        }

    def batch_fill_field(self, table_id: str, field_name: str,
                         records: List[Dict[str, Any]],
                         batch_size: int = 100) -> Dict[str, Any]:
        """批量填充字段值（硬件自适应削峰）"""
        if not records:
            return {"success": False, "error": "记录列表为空"}

        # 硬件自适应：读取安全批量参数
        try:
            from engine.quota_manager import get_safe_batch_params
            batch_params = get_safe_batch_params(len(records))
            batch_size = min(batch_size, batch_params.get("batch_chunk", 100))
        except ImportError:
            pass

        total = len(records)
        success_count = 0
        fail_count = 0
        errors: List[str] = []

        # 分批处理
        for i in range(0, total, batch_size):
            batch = records[i:i + batch_size]
            if self.backend is not None:
                try:
                    if hasattr(self.backend, "dbf_record_update_batch"):
                        result = self.backend.dbf_record_update_batch(table_id, batch)
                        success_count += len(batch)
                except Exception as e:
                    fail_count += len(batch)
                    errors.append(f"批次 {i // batch_size + 1}: {e}")
            else:
                # 本地降级
                success_count += len(batch)

        result = {
            "success": fail_count == 0,
            "total": total,
            "success_count": success_count,
            "fail_count": fail_count,
            "batch_count": (total + batch_size - 1) // batch_size,
            "errors": errors[:10],
        }

        self._log_operation(table_id, "batch_fill", field_name,
                           "success" if fail_count == 0 else "partial",
                           result=json.dumps(result, ensure_ascii=False))

        if self.backend is None:
            result["source"] = "local_fallback"
            result["message"] = "批量填充配置已生成（本地模式）。连接金山开放平台后可在线执行。"

        return result

    def create_formula_field(self, table_id: str, field_name: str,
                             formula: str) -> Dict[str, Any]:
        """创建公式字段"""
        return self.create_field(table_id, field_name, "formula", formula=formula)

    def create_relation_field(self, table_id: str, field_name: str,
                              relation_table_id: str) -> Dict[str, Any]:
        """创建关联字段"""
        return self.create_field(table_id, field_name, "relation",
                                relation_table_id=relation_table_id)

    def create_rollup_field(self, table_id: str, field_name: str,
                            rollup_field: str, rollup_operation: str) -> Dict[str, Any]:
        """创建汇总字段"""
        if rollup_operation not in ROLLUP_OPERATIONS:
            return {
                "success": False,
                "error": f"不支持的汇总操作: {rollup_operation}。支持: {list(ROLLUP_OPERATIONS.keys())}",
            }
        return self.create_field(table_id, field_name, "rollup",
                                rollup_field=rollup_field,
                                rollup_operation=rollup_operation)

    def _log_operation(self, table_id: str, operation_type: str,
                       field_name: str, status: str, result: str = "",
                       error: str = ""):
        """记录操作日志"""
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute(
                """INSERT INTO dbf_auto_operations
                   (table_id, operation_type, field_name, status, created_at, completed_at, result, error)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (table_id, operation_type, field_name, status,
                 datetime.now().isoformat(), datetime.now().isoformat(),
                 result, error),
            )
            conn.commit()
        finally:
            conn.close()

    def get_operation_history(self, table_id: str = "",
                              limit: int = 20) -> Dict[str, Any]:
        """获取操作历史"""
        conn = sqlite3.connect(self.db_path)
        try:
            if table_id:
                cursor = conn.execute(
                    "SELECT table_id, operation_type, field_name, status, completed_at, result "
                    "FROM dbf_auto_operations WHERE table_id = ? ORDER BY id DESC LIMIT ?",
                    (table_id, limit),
                )
            else:
                cursor = conn.execute(
                    "SELECT table_id, operation_type, field_name, status, completed_at, result "
                    "FROM dbf_auto_operations ORDER BY id DESC LIMIT ?",
                    (limit,),
                )
            rows = cursor.fetchall()
            return {
                "total": len(rows),
                "operations": [
                    {
                        "table_id": r[0],
                        "operation_type": r[1],
                        "field_name": r[2],
                        "status": r[3],
                        "completed_at": r[4],
                        "result": json.loads(r[5]) if r[5] else None,
                    }
                    for r in rows
                ],
            }
        finally:
            conn.close()


def get_dbf_auto_engine(backend: Any = None) -> DbfAutoEngine:
    """工厂函数"""
    return DbfAutoEngine(backend=backend)


# ===========================================================================
# 模块级便捷函数
# ===========================================================================

def list_field_types() -> Dict[str, Any]:
    engine = get_dbf_auto_engine()
    return engine.list_field_types()

def list_formula_templates() -> Dict[str, Any]:
    engine = get_dbf_auto_engine()
    return engine.list_formula_templates()

def list_rollup_operations() -> Dict[str, Any]:
    engine = get_dbf_auto_engine()
    return engine.list_rollup_operations()

def create_field(table_id: str, field_name: str, field_type: str,
                 options: Optional[List[str]] = None, formula: str = "",
                 relation_table_id: str = "", rollup_field: str = "",
                 rollup_operation: str = "") -> Dict[str, Any]:
    engine = get_dbf_auto_engine()
    return engine.create_field(table_id, field_name, field_type, options,
                               formula, relation_table_id, rollup_field, rollup_operation)

def batch_fill_field(table_id: str, field_name: str,
                     records: List[Dict[str, Any]], batch_size: int = 100) -> Dict[str, Any]:
    engine = get_dbf_auto_engine()
    return engine.batch_fill_field(table_id, field_name, records, batch_size)

def create_formula_field(table_id: str, field_name: str, formula: str) -> Dict[str, Any]:
    engine = get_dbf_auto_engine()
    return engine.create_formula_field(table_id, field_name, formula)

def create_relation_field(table_id: str, field_name: str, relation_table_id: str) -> Dict[str, Any]:
    engine = get_dbf_auto_engine()
    return engine.create_relation_field(table_id, field_name, relation_table_id)

def create_rollup_field(table_id: str, field_name: str,
                        rollup_field: str, rollup_operation: str) -> Dict[str, Any]:
    engine = get_dbf_auto_engine()
    return engine.create_rollup_field(table_id, field_name, rollup_field, rollup_operation)

def get_dbf_history(table_id: str = "", limit: int = 20) -> Dict[str, Any]:
    engine = get_dbf_auto_engine()
    return engine.get_operation_history(table_id, limit)
