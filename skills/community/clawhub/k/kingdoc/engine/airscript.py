"""KingDoc AirScript 在线自动化引擎

封装金山开放平台 AirScript 脚本创建/执行接口：
- 自然语言 → 脚本生成（本地规则引擎模板，无需外部 LLM）
- 脚本预检（危险操作扫描：DELETE / OVERWRITE / DROP）
- 用户确认 → 在线执行
- 能力域：定时通知、数据汇总、表格批量操作、字段计算

本地降级：云端不可用时返回友好提示，不中断其他功能。
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
import time
from datetime import datetime, date
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 危险操作关键词（预检阶段扫描）
DANGEROUS_KEYWORDS: List[Tuple[str, str]] = [
    ("DELETE", "删除数据"),
    ("DROP", "删除表/字段"),
    ("TRUNCATE", "清空表"),
    ("OVERWRITE", "覆盖数据"),
    ("REPLACE", "替换数据"),
    ("REMOVE", "移除记录"),
    ("CLEAR", "清除内容"),
    ("UPDATE_ALL", "批量更新"),
    ("BATCH_DELETE", "批量删除"),
]

# 脚本能力域
CAPABILITY_DOMAINS: Dict[str, Dict[str, Any]] = {
    "scheduled_notify": {
        "name": "定时通知",
        "description": "定时发送通知（企微/钉钉/金山协作）",
        "template": "scheduled_notify",
        "params": ["channel", "webhook_key", "notify_content", "cron"],
    },
    "data_summary": {
        "name": "数据汇总",
        "description": "汇总多维表格/电子表格数据",
        "template": "data_summary",
        "params": ["table_id", "field_name", "operation"],
    },
    "batch_operation": {
        "name": "表格批量操作",
        "description": "批量增删改表格记录",
        "template": "batch_operation",
        "params": ["table_id", "records", "action"],
    },
    "field_calc": {
        "name": "字段计算",
        "description": "公式字段计算与填充",
        "template": "field_calc",
        "params": ["table_id", "field_name", "formula"],
    },
}

# 脚本模板库（本地规则引擎生成）
SCRIPT_TEMPLATES: Dict[str, str] = {
    "scheduled_notify": """// AirScript: 定时通知
// 生成时间: {generated_at}
// 描述: {description}

function main() {{
  var result = kdoc.notification.send({{
    channel: "{channel}",
    webhook_key: "{webhook_key}",
    content: {{
      msgtype: "text",
      text: {{
        content: "{notify_content}"
      }}
    }}
  }});
  return result;
}}
""",
    "data_summary": """// AirScript: 数据汇总
// 生成时间: {generated_at}
// 描述: {description}

function main() {{
  var records = kdoc.dbt.record.query({{
    table_id: "{table_id}",
    limit: 1000
  }});
  var summary = {{}};
  for (var i = 0; i < records.length; i++) {{
    var val = records[i].{field_name};
    if (val != null) {{
      summary[val] = (summary[val] || 0) + 1;
    }}
  }}
  return summary;
}}
""",
    "batch_operation": """// AirScript: 表格批量操作
// 生成时间: {generated_at}
// 描述: {description}

function main() {{
  var records = {records_json};
  var results = [];
  for (var i = 0; i < records.length; i++) {{
    var result = kdoc.dbt.record.{action}({{
      table_id: "{table_id}",
      fields: records[i]
    }});
    results.push(result);
  }}
  return {{ total: results.length, results: results }};
}}
""",
    "field_calc": """// AirScript: 字段计算
// 生成时间: {generated_at}
// 描述: {description}

function main() {{
  var records = kdoc.dbt.record.query({{
    table_id: "{table_id}",
    limit: 1000
  }});
  var results = [];
  for (var i = 0; i < records.length; i++) {{
    var newVal = {formula};
    var result = kdoc.dbt.record.update({{
      table_id: "{table_id}",
      record_id: records[i].record_id,
      fields: {{ "{field_name}": newVal }}
    }});
    results.push(result);
  }}
  return {{ total: results.length, results: results }};
}}
""",
}


class AirScriptSafetyError(Exception):
    """脚本预检发现危险操作"""
    def __init__(self, keyword: str, description: str, line_number: int = 0):
        self.keyword = keyword
        self.description = description
        self.line_number = line_number
        super().__init__(f"危险操作 '{keyword}' ({description}) 在第 {line_number} 行")


class AirScriptEngine:
    """AirScript 在线自动化引擎"""

    def __init__(self, backend: Any = None, db_path: Optional[str] = None):
        self.backend = backend
        self.db_path = db_path or self._default_db_path()
        self._init_db()

    def _default_db_path(self) -> str:
        skill_root = Path(__file__).resolve().parent.parent
        return str(skill_root / ".airscript_history.db")

    def _init_db(self):
        """初始化 SQLite 执行历史表"""
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS airscript_executions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    script_id TEXT UNIQUE,
                    script_type TEXT,
                    status TEXT,
                    created_at TEXT,
                    executed_at TEXT,
                    result TEXT,
                    error TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS airscript_pending (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    script_id TEXT UNIQUE,
                    script_content TEXT,
                    capability_domain TEXT,
                    safety_status TEXT,
                    created_at TEXT,
                    confirmed INTEGER DEFAULT 0
                )
            """)
            conn.commit()
        finally:
            conn.close()

    def list_capabilities(self) -> Dict[str, Any]:
        """列出所有可用的脚本能力域"""
        return {
            "domains": [
                {
                    "id": k,
                    "name": v["name"],
                    "description": v["description"],
                    "params": v["params"],
                }
                for k, v in CAPABILITY_DOMAINS.items()
            ]
        }

    def generate_script(self, domain: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """根据能力域和参数生成 AirScript 脚本"""
        if domain not in CAPABILITY_DOMAINS:
            return {
                "success": False,
                "error": f"未知的能力域: {domain}。可用: {list(CAPABILITY_DOMAINS.keys())}",
            }

        template_str = SCRIPT_TEMPLATES.get(CAPABILITY_DOMAINS[domain]["template"])
        if not template_str:
            return {"success": False, "error": f"模板不存在: {domain}"}

        # 填充模板
        template_params = {
            "generated_at": datetime.now().isoformat(),
            "description": params.get("description", CAPABILITY_DOMAINS[domain]["name"]),
            **params,
        }
        # records_json 需要特殊处理
        if "records" in params and isinstance(params["records"], (list, dict)):
            template_params["records_json"] = json.dumps(params["records"], ensure_ascii=False)

        try:
            script_content = template_str.format(**template_params)
        except KeyError as e:
            return {
                "success": False,
                "error": f"模板参数缺失: {e}。需要: {CAPABILITY_DOMAINS[domain]['params']}",
            }

        script_id = f"airscript_{domain}_{int(time.time())}"

        return {
            "success": True,
            "script_id": script_id,
            "domain": domain,
            "domain_name": CAPABILITY_DOMAINS[domain]["name"],
            "script_content": script_content,
            "params": params,
            "safety_status": "pending_check",
        }

    def precheck_script(self, script_content: str) -> Dict[str, Any]:
        """脚本预检：扫描危险操作"""
        findings: List[Dict[str, Any]] = []
        lines = script_content.splitlines()

        for i, line in enumerate(lines, 1):
            upper_line = line.upper().strip()
            # 跳过注释
            if upper_line.startswith("//") or upper_line.startswith("/*") or upper_line.startswith("*"):
                continue
            for keyword, desc in DANGEROUS_KEYWORDS:
                if keyword in upper_line:
                    findings.append({
                        "line": i,
                        "keyword": keyword,
                        "description": desc,
                        "content": line.strip(),
                    })

        return {
            "safe": len(findings) == 0,
            "findings": findings,
            "risk_level": "high" if findings else "low",
            "total_lines": len(lines),
        }

    def submit_for_confirmation(self, script_id: str, script_content: str,
                                domain: str, safety_result: Dict[str, Any]) -> Dict[str, Any]:
        """提交脚本等待用户确认"""
        conn = sqlite3.connect(self.db_path)
        try:
            safety_status = "safe" if safety_result["safe"] else "dangerous"
            conn.execute(
                """INSERT OR REPLACE INTO airscript_pending
                   (script_id, script_content, capability_domain, safety_status, created_at)
                   VALUES (?, ?, ?, ?, ?)""",
                (script_id, script_content, domain, safety_status,
                 datetime.now().isoformat()),
            )
            conn.commit()
            return {
                "success": True,
                "script_id": script_id,
                "safety_status": safety_status,
                "requires_confirmation": True,
                "message": (
                    "脚本已生成，请确认后执行。"
                    if safety_result["safe"]
                    else f"⚠️ 检测到 {len(safety_result['findings'])} 处危险操作，请仔细确认。"
                ),
            }
        finally:
            conn.close()

    def confirm_and_execute(self, script_id: str, confirmed: bool = False) -> Dict[str, Any]:
        """用户确认后执行脚本"""
        if not confirmed:
            return {
                "success": False,
                "error": "用户未确认，脚本未执行。",
                "script_id": script_id,
            }

        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.execute(
                "SELECT script_content, capability_domain, safety_status FROM airscript_pending WHERE script_id = ?",
                (script_id,),
            )
            row = cursor.fetchone()
            if not row:
                return {"success": False, "error": f"脚本不存在: {script_id}"}

            script_content, domain, safety_status = row

            # 危险操作再次检查
            if safety_status == "dangerous":
                precheck = self.precheck_script(script_content)
                if precheck["findings"]:
                    return {
                        "success": False,
                        "error": "脚本包含危险操作，已拦截。请修改后重新提交。",
                        "findings": precheck["findings"],
                        "script_id": script_id,
                    }

            # 执行脚本
            result = self._execute_script(script_id, script_content, domain)

            # 更新状态
            conn.execute(
                "UPDATE airscript_pending SET confirmed = 1 WHERE script_id = ?",
                (script_id,),
            )
            conn.execute(
                """INSERT OR REPLACE INTO airscript_executions
                   (script_id, script_type, status, created_at, executed_at, result, error)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (script_id, domain, "executed", datetime.now().isoformat(),
                 datetime.now().isoformat(),
                 json.dumps(result, ensure_ascii=False) if result else None,
                 None),
            )
            conn.commit()

            return {
                "success": True,
                "script_id": script_id,
                "domain": domain,
                "result": result,
                "executed_at": datetime.now().isoformat(),
            }
        finally:
            conn.close()

    def _execute_script(self, script_id: str, script_content: str,
                        domain: str) -> Optional[Dict[str, Any]]:
        """实际执行脚本（通过云端后端或本地降级）"""
        if self.backend is not None:
            try:
                # 调用云端 AirScript 执行接口
                if hasattr(self.backend, "airscript_execute"):
                    return self.backend.airscript_execute(script_id, script_content, domain)
            except Exception as e:
                return {"success": False, "error": f"云端执行失败: {e}"}

        # 本地降级：返回提示信息
        return {
            "success": True,
            "source": "local_fallback",
            "message": "脚本已生成（本地模式）。连接金山开放平台后可在线执行。",
            "hint": "配置 App Key 后，脚本将通过金山 AirScript 引擎在线执行。",
            "script_id": script_id,
        }

    def get_execution_history(self, limit: int = 20) -> Dict[str, Any]:
        """获取执行历史"""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.execute(
                "SELECT script_id, script_type, status, executed_at, result "
                "FROM airscript_executions ORDER BY id DESC LIMIT ?",
                (limit,),
            )
            rows = cursor.fetchall()
            return {
                "total": len(rows),
                "executions": [
                    {
                        "script_id": r[0],
                        "domain": r[1],
                        "status": r[2],
                        "executed_at": r[3],
                        "result": json.loads(r[4]) if r[4] else None,
                    }
                    for r in rows
                ],
            }
        finally:
            conn.close()

    def get_pending_scripts(self) -> Dict[str, Any]:
        """获取待确认脚本列表"""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.execute(
                "SELECT script_id, capability_domain, safety_status, created_at "
                "FROM airscript_pending WHERE confirmed = 0 ORDER BY id DESC",
            )
            rows = cursor.fetchall()
            return {
                "total": len(rows),
                "pending": [
                    {
                        "script_id": r[0],
                        "domain": r[1],
                        "safety_status": r[2],
                        "created_at": r[3],
                    }
                    for r in rows
                ],
            }
        finally:
            conn.close()


def get_airscript_engine(backend: Any = None) -> AirScriptEngine:
    """工厂函数：创建 AirScript 引擎实例"""
    return AirScriptEngine(backend=backend)


# ===========================================================================
# 模块级便捷函数
# ===========================================================================

def list_capabilities() -> Dict[str, Any]:
    """列出所有可用的脚本能力域"""
    engine = get_airscript_engine()
    return engine.list_capabilities()


def generate_script(domain: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """生成 AirScript 脚本"""
    engine = get_airscript_engine()
    return engine.generate_script(domain, params)


def precheck_script(script_content: str) -> Dict[str, Any]:
    """脚本预检"""
    engine = get_airscript_engine()
    return engine.precheck_script(script_content)


def submit_for_confirmation(script_id: str, script_content: str,
                            domain: str, safety_result: Dict[str, Any]) -> Dict[str, Any]:
    """提交脚本等待确认"""
    engine = get_airscript_engine()
    return engine.submit_for_confirmation(script_id, script_content, domain, safety_result)


def confirm_and_execute(script_id: str, confirmed: bool = False) -> Dict[str, Any]:
    """确认并执行脚本"""
    engine = get_airscript_engine()
    return engine.confirm_and_execute(script_id, confirmed)


def get_execution_history(limit: int = 20) -> Dict[str, Any]:
    """获取执行历史"""
    engine = get_airscript_engine()
    return engine.get_execution_history(limit)


def get_pending_scripts() -> Dict[str, Any]:
    """获取待确认脚本"""
    engine = get_airscript_engine()
    return engine.get_pending_scripts()
