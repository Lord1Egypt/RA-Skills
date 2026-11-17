"""KingDoc Excel/CSV 双向导入导出引擎

openpyxl 读写与字段类型映射约定：
- date 字段：ISO 8601 格式序列化
- link 字段：{url, title} JSON 序列化
- select 字段：逗号分隔字符串
- person 字段：{name, email} JSON 序列化

导入走批量记录创建（复用配额管理器削峰），导出支持视图级筛选快照。
本地降级：无 openpyxl 时返回结构化 JSON。
"""
from __future__ import annotations

import csv
import io
import json
import os
import sqlite3
import tempfile
import time
from datetime import datetime, date
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# 字段类型序列化规则
FIELD_SERIALIZE_RULES: Dict[str, Dict[str, Any]] = {
    "date": {
        "name": "日期",
        "serialize": lambda v: v.isoformat() if isinstance(v, (date, datetime)) else str(v),
        "deserialize": lambda v: v[:10] if isinstance(v, str) else v,
        "storage": "ISO 8601 字符串 (YYYY-MM-DD)",
    },
    "link": {
        "name": "链接",
        "serialize": lambda v: json.dumps(v, ensure_ascii=False) if isinstance(v, dict) else str(v),
        "deserialize": lambda v: json.loads(v) if isinstance(v, str) and v.startswith("{") else {"url": str(v), "title": str(v)},
        "storage": "JSON {url, title}",
    },
    "select": {
        "name": "单选",
        "serialize": lambda v: ",".join(v) if isinstance(v, list) else str(v),
        "deserialize": lambda v: [s.strip() for s in str(v).split(",") if s.strip()],
        "storage": "逗号分隔字符串",
    },
    "person": {
        "name": "人员",
        "serialize": lambda v: json.dumps(v, ensure_ascii=False) if isinstance(v, dict) else str(v),
        "deserialize": lambda v: json.loads(v) if isinstance(v, str) and v.startswith("{") else {"name": str(v), "email": ""},
        "storage": "JSON {name, email}",
    },
    "number": {
        "name": "数字",
        "serialize": lambda v: str(v),
        "deserialize": lambda v: float(v) if "." in str(v) else int(v) if str(v).isdigit() else 0,
        "storage": "数值",
    },
    "text": {
        "name": "文本",
        "serialize": lambda v: str(v),
        "deserialize": lambda v: str(v),
        "storage": "纯文本",
    },
}


class BidataIOEngine:
    """Excel/CSV 双向导入导出引擎"""

    def __init__(self, backend: Any = None, db_path: Optional[str] = None):
        self.backend = backend
        self.db_path = db_path or self._default_db_path()
        self._init_db()

    def _default_db_path(self) -> str:
        skill_root = Path(__file__).resolve().parent.parent
        return str(skill_root / ".bidata_io_history.db")

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS bidata_io_operations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation_type TEXT,
                    file_name TEXT,
                    record_count INTEGER,
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

    def get_field_rules(self) -> Dict[str, Any]:
        """获取字段类型序列化规则文档"""
        return {
            "rules": [
                {
                    "type": k,
                    "name": v["name"],
                    "storage": v["storage"],
                }
                for k, v in FIELD_SERIALIZE_RULES.items()
            ]
        }

    def import_csv(self, file_path: str, table_id: str = "",
                   field_types: Optional[Dict[str, str]] = None,
                   batch_size: int = 100) -> Dict[str, Any]:
        """导入 CSV 文件"""
        field_types = field_types or {}

        if not os.path.exists(file_path):
            return {"success": False, "error": f"文件不存在: {file_path}"}

        try:
            with open(file_path, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
        except Exception as e:
            return {"success": False, "error": f"读取 CSV 失败: {e}"}

        if not rows:
            return {"success": False, "error": "CSV 文件为空"}

        # 字段类型映射
        headers = list(rows[0].keys())
        mapped_records = []
        for row in rows:
            mapped = {}
            for k, v in row.items():
                field_type = field_types.get(k, "text")
                rule = FIELD_SERIALIZE_RULES.get(field_type)
                if rule:
                    try:
                        mapped[k] = rule["deserialize"](v)
                    except Exception:
                        mapped[k] = v
                else:
                    mapped[k] = v
            mapped_records.append(mapped)

        # 硬件自适应削峰
        try:
            from engine.quota_manager import get_safe_batch_params
            batch_params = get_safe_batch_params(len(mapped_records))
            batch_size = min(batch_size, batch_params.get("batch_chunk", 100))
        except ImportError:
            pass

        # 批量导入
        total = len(mapped_records)
        success_count = 0
        errors = []

        if self.backend is not None and table_id:
            try:
                for i in range(0, total, batch_size):
                    batch = mapped_records[i:i + batch_size]
                    if hasattr(self.backend, "dbf_record_add_batch"):
                        result = self.backend.dbf_record_add_batch(table_id, batch)
                        success_count += len(batch)
            except Exception as e:
                errors.append(str(e))
        else:
            # 本地模式：仅解析不写入
            success_count = total

        result = {
            "success": len(errors) == 0,
            "operation": "import_csv",
            "file_path": file_path,
            "total_records": total,
            "success_count": success_count,
            "field_types_applied": field_types,
            "headers": headers,
            "errors": errors[:10],
        }

        if self.backend is None or not table_id:
            result["source"] = "local_fallback"
            result["message"] = "CSV 已解析（本地模式）。连接金山开放平台后可在线导入。"
            result["parsed_records"] = mapped_records[:50]  # 预览前 50 条

        self._log_operation("import_csv", os.path.basename(file_path),
                            total, result["success"])
        return result

    def import_excel(self, file_path: str, table_id: str = "",
                     field_types: Optional[Dict[str, str]] = None,
                     sheet_name: str = "", batch_size: int = 100) -> Dict[str, Any]:
        """导入 Excel 文件"""
        try:
            import openpyxl
        except ImportError:
            return {
                "success": False,
                "error": "需要 openpyxl: pip install openpyxl",
            }

        if not os.path.exists(file_path):
            return {"success": False, "error": f"文件不存在: {file_path}"}

        try:
            wb = openpyxl.load_workbook(file_path, read_only=True)
            if sheet_name:
                ws = wb[sheet_name] if sheet_name in wb.sheetnames else wb.active
            else:
                ws = wb.active

            rows = list(ws.iter_rows(values_only=True))
            if not rows:
                return {"success": False, "error": "Excel 工作表为空"}

            headers = [str(h) if h else f"col{i}" for i, h in enumerate(rows[0])]
            data_rows = rows[1:]
        except Exception as e:
            return {"success": False, "error": f"读取 Excel 失败: {e}"}

        # 字段类型映射
        field_types = field_types or {}
        mapped_records = []
        for row in data_rows:
            mapped = {}
            for i, val in enumerate(row):
                if i >= len(headers):
                    break
                field_name = headers[i]
                field_type = field_types.get(field_name, "text")
                rule = FIELD_SERIALIZE_RULES.get(field_type)
                if rule:
                    try:
                        mapped[field_name] = rule["deserialize"](val)
                    except Exception:
                        mapped[field_name] = val
                else:
                    mapped[field_name] = val
            mapped_records.append(mapped)

        # 硬件自适应削峰
        try:
            from engine.quota_manager import get_safe_batch_params
            batch_params = get_safe_batch_params(len(mapped_records))
            batch_size = min(batch_size, batch_params.get("batch_chunk", 100))
        except ImportError:
            pass

        total = len(mapped_records)
        success_count = 0
        errors = []

        if self.backend is not None and table_id:
            try:
                for i in range(0, total, batch_size):
                    batch = mapped_records[i:i + batch_size]
                    if hasattr(self.backend, "dbf_record_add_batch"):
                        result = self.backend.dbf_record_add_batch(table_id, batch)
                        success_count += len(batch)
            except Exception as e:
                errors.append(str(e))
        else:
            success_count = total

        result = {
            "success": len(errors) == 0,
            "operation": "import_excel",
            "file_path": file_path,
            "sheet_name": sheet_name or "active",
            "total_records": total,
            "success_count": success_count,
            "headers": headers,
            "errors": errors[:10],
        }

        if self.backend is None or not table_id:
            result["source"] = "local_fallback"
            result["message"] = "Excel 已解析（本地模式）。连接金山开放平台后可在线导入。"
            result["parsed_records"] = mapped_records[:50]

        self._log_operation("import_excel", os.path.basename(file_path),
                            total, result["success"])
        return result

    def export_csv(self, records: List[Dict[str, Any]],
                   output_path: str = "",
                   field_types: Optional[Dict[str, str]] = None,
                   filter_func: Optional[Any] = None) -> Dict[str, Any]:
        """导出 CSV（支持视图级筛选快照）"""
        if not records:
            return {"success": False, "error": "记录列表为空"}

        # 应用筛选
        if filter_func:
            records = [r for r in records if filter_func(r)]

        if not records:
            return {"success": False, "error": "筛选后无数据"}

        field_types = field_types or {}
        headers = list(records[0].keys())

        # 序列化
        serialized = []
        for r in records:
            row = {}
            for k, v in r.items():
                field_type = field_types.get(k, "text")
                rule = FIELD_SERIALIZE_RULES.get(field_type)
                if rule:
                    try:
                        row[k] = rule["serialize"](v)
                    except Exception:
                        row[k] = str(v)
                else:
                    row[k] = str(v)
            serialized.append(row)

        # 写入 CSV
        if not output_path:
            output_path = str(Path(tempfile.gettempdir()) / f"kingdoc_export_{int(time.time())}.csv")

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

        try:
            with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(serialized)

            result = {
                "success": True,
                "operation": "export_csv",
                "output_path": output_path,
                "total_records": len(serialized),
                "headers": headers,
            }
        except Exception as e:
            return {"success": False, "error": f"写入 CSV 失败: {e}"}

        self._log_operation("export_csv", os.path.basename(output_path),
                            len(serialized), True)
        return result

    def export_excel(self, records: List[Dict[str, Any]],
                     output_path: str = "",
                     field_types: Optional[Dict[str, str]] = None,
                     filter_func: Optional[Any] = None) -> Dict[str, Any]:
        """导出 Excel（支持视图级筛选快照）"""
        try:
            import openpyxl
            from openpyxl.styles import Font, Alignment, PatternFill
        except ImportError:
            return {
                "success": False,
                "error": "需要 openpyxl: pip install openpyxl",
            }

        if not records:
            return {"success": False, "error": "记录列表为空"}

        # 应用筛选
        if filter_func:
            records = [r for r in records if filter_func(r)]

        if not records:
            return {"success": False, "error": "筛选后无数据"}

        field_types = field_types or {}
        headers = list(records[0].keys())

        # 序列化
        serialized = []
        for r in records:
            row = {}
            for k, v in r.items():
                field_type = field_types.get(k, "text")
                rule = FIELD_SERIALIZE_RULES.get(field_type)
                if rule:
                    try:
                        row[k] = rule["serialize"](v)
                    except Exception:
                        row[k] = str(v)
                else:
                    row[k] = str(v)
            serialized.append(row)

        if not output_path:
            output_path = str(Path(tempfile.gettempdir()) / f"kingdoc_export_{int(time.time())}.xlsx")

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "导出数据"

            # 表头样式
            header_font = Font(bold=True, color="FFFFFF")
            header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
            header_alignment = Alignment(horizontal="center")

            for col_idx, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col_idx, value=header)
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment

            # 数据行
            for row_idx, row_data in enumerate(serialized, 2):
                for col_idx, header in enumerate(headers, 1):
                    ws.cell(row=row_idx, column=col_idx, value=row_data.get(header, ""))

            # 自动列宽
            for col_idx, header in enumerate(headers, 1):
                max_len = max(len(str(header)), max((len(str(r.get(header, ""))) for r in serialized), default=0))
                ws.column_dimensions[openpyxl.utils.get_column_letter(col_idx)].width = min(max_len + 2, 40)

            wb.save(output_path)

            result = {
                "success": True,
                "operation": "export_excel",
                "output_path": output_path,
                "total_records": len(serialized),
                "headers": headers,
            }
        except Exception as e:
            return {"success": False, "error": f"写入 Excel 失败: {e}"}

        self._log_operation("export_excel", os.path.basename(output_path),
                            len(serialized), True)
        return result

    def _log_operation(self, operation_type: str, file_name: str,
                       record_count: int, status: bool):
        """记录操作日志"""
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute(
                """INSERT INTO bidata_io_operations
                   (operation_type, file_name, record_count, status, created_at, completed_at, result, error)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (operation_type, file_name, record_count,
                 "success" if status else "failed",
                 datetime.now().isoformat(), datetime.now().isoformat(),
                 "", ""),
            )
            conn.commit()
        finally:
            conn.close()

    def get_operation_history(self, limit: int = 20) -> Dict[str, Any]:
        """获取操作历史"""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.execute(
                "SELECT operation_type, file_name, record_count, status, completed_at "
                "FROM bidata_io_operations ORDER BY id DESC LIMIT ?",
                (limit,),
            )
            rows = cursor.fetchall()
            return {
                "total": len(rows),
                "operations": [
                    {
                        "operation_type": r[0],
                        "file_name": r[1],
                        "record_count": r[2],
                        "status": r[3],
                        "completed_at": r[4],
                    }
                    for r in rows
                ],
            }
        finally:
            conn.close()


def get_bidata_io_engine(backend: Any = None) -> BidataIOEngine:
    """工厂函数"""
    return BidataIOEngine(backend=backend)


# ===========================================================================
# 模块级便捷函数
# ===========================================================================

def get_field_rules() -> Dict[str, Any]:
    engine = get_bidata_io_engine()
    return engine.get_field_rules()

def import_csv(file_path: str, table_id: str = "",
               field_types: Optional[Dict[str, str]] = None,
               batch_size: int = 100) -> Dict[str, Any]:
    engine = get_bidata_io_engine()
    return engine.import_csv(file_path, table_id, field_types, batch_size)

def import_excel(file_path: str, table_id: str = "",
                 field_types: Optional[Dict[str, str]] = None,
                 sheet_name: str = "", batch_size: int = 100) -> Dict[str, Any]:
    engine = get_bidata_io_engine()
    return engine.import_excel(file_path, table_id, field_types, sheet_name, batch_size)

def export_csv(records: List[Dict[str, Any]], output_path: str = "",
               field_types: Optional[Dict[str, str]] = None,
               filter_func: Optional[Any] = None) -> Dict[str, Any]:
    engine = get_bidata_io_engine()
    return engine.export_csv(records, output_path, field_types, filter_func)

def export_excel(records: List[Dict[str, Any]], output_path: str = "",
                 field_types: Optional[Dict[str, str]] = None,
                 filter_func: Optional[Any] = None) -> Dict[str, Any]:
    engine = get_bidata_io_engine()
    return engine.export_excel(records, output_path, field_types, filter_func)

def get_io_history(limit: int = 20) -> Dict[str, Any]:
    engine = get_bidata_io_engine()
    return engine.get_operation_history(limit)
