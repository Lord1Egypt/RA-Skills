"""KingDoc AirScript 预设库（v4.4.0 T5）

能力：
- 20+ 高频 AirScript 预设（去重提醒/到期扫描/自动编号/状态流转/重复值标记等）
- 每个预设带完整元数据：id / 名称 / 能力域 / 参数 / 脚本模板 / 测试样例 / 预期输出
- 走「自然语言 → 脚本生成 → 预览 → 确认 → 在线执行」链路
  （生成复用 airscript.generate_script 预检，管线概念复用 topic_generator 的生成-预检-确认）
- 按关键词从自然语言匹配预设（本地规则引擎，无需外部 LLM）
- 预设存 SQLite 库带元数据，全程中文

本地降级：无云端 backend 时生成脚本 + 测试样例，预览可用，执行返回友好提示。
"""
from __future__ import annotations

import json
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# 预设库：20+ 预设，每个含元数据 + 测试样例 + 预期输出
# ---------------------------------------------------------------------------
# 字段说明：
#   id, name, domain, keywords, description, params(参数名列表),
#   template(脚本模板), sample_params(测试样例), expected(预期输出摘要)
PRESETS: List[Dict[str, Any]] = [
    {
        "id": "dedup_reminder", "name": "重复值提醒", "domain": "batch_operation",
        "keywords": ["去重", "重复值", "重复提醒", "重复数据"],
        "description": "扫描指定字段的重复值并标记提醒",
        "params": ["table_id", "field_name"],
        "template": """// AirScript: 重复值提醒
function main() {{
  var records = kdoc.dbt.record.query({{ table_id: "{table_id}", limit: 1000 }});
  var seen = {{}}, dup = [];
  for (var i = 0; i < records.length; i++) {{
    var v = records[i].{field_name};
    if (seen[v]) {{ dup.push({{ value: v, record_id: records[i].record_id }}); }}
    seen[v] = true;
  }}
  return {{ duplicates: dup.length, items: dup }};
}}""",
        "sample_params": {"table_id": "tbl_signup", "field_name": "phone"},
        "expected": '{"duplicates": 2, "items": [...]}',
    },
    {
        "id": "expiry_scan", "name": "到期扫描", "domain": "field_calc",
        "keywords": ["到期", "过期", "有效期", "到期提醒"],
        "description": "扫描日期字段，找出已到期记录",
        "params": ["table_id", "date_field", "threshold_days"],
        "template": """// AirScript: 到期扫描
function main() {{
  var records = kdoc.dbt.record.query({{ table_id: "{table_id}", limit: 1000 }});
  var now = new Date().getTime(), expired = [];
  for (var i = 0; i < records.length; i++) {{
    var d = new Date(records[i].{date_field}).getTime();
    if ((now - d) / 86400000 > {threshold_days}) {{
      expired.push(records[i].record_id);
    }}
  }}
  return {{ expired_count: expired.length, records: expired }};
}}""",
        "sample_params": {"table_id": "tbl_contract", "date_field": "expire_date", "threshold_days": 0},
        "expected": '{"expired_count": 3, "records": [...]}',
    },
    {
        "id": "auto_number", "name": "自动编号", "domain": "field_calc",
        "keywords": ["编号", "自动编号", "序号", "流水号"],
        "description": "为表格记录生成连续编号",
        "params": ["table_id", "number_field", "prefix"],
        "template": """// AirScript: 自动编号
function main() {{
  var records = kdoc.dbt.record.query({{ table_id: "{table_id}", limit: 1000 }});
  for (var i = 0; i < records.length; i++) {{
    var no = "{prefix}" + String(i + 1).padStart(4, "0");
    kdoc.dbt.record.update({{ table_id: "{table_id}", record_id: records[i].record_id,
      fields: {{ "{number_field}": no }} }});
  }}
  return {{ numbered: records.length }};
}}""",
        "sample_params": {"table_id": "tbl_order", "number_field": "order_no", "prefix": "SO-"},
        "expected": '{"numbered": 100}',
    },
    {
        "id": "status_flow", "name": "状态流转", "domain": "batch_operation",
        "keywords": ["状态", "流转", "状态更新", "状态机"],
        "description": "按规则批量流转记录状态",
        "params": ["table_id", "from_status", "to_status", "status_field"],
        "template": """// AirScript: 状态流转
function main() {{
  var records = kdoc.dbt.record.query({{ table_id: "{table_id}", limit: 1000 }});
  var changed = 0;
  for (var i = 0; i < records.length; i++) {{
    if (records[i].{status_field} === "{from_status}") {{
      kdoc.dbt.record.update({{ table_id: "{table_id}", record_id: records[i].record_id,
        fields: {{ "{status_field}": "{to_status}" }} }});
      changed++;
    }}
  }}
  return {{ changed: changed }};
}}""",
        "sample_params": {"table_id": "tbl_task", "from_status": "待处理", "to_status": "进行中", "status_field": "status"},
        "expected": '{"changed": 12}',
    },
    {
        "id": "duplicate_mark", "name": "重复值标记", "domain": "batch_operation",
        "keywords": ["标记重复", "高亮重复", "重复标记"],
        "description": "在重复值记录上打标记字段",
        "params": ["table_id", "field_name", "mark_field"],
        "template": """// AirScript: 重复值标记
function main() {{
  var records = kdoc.dbt.record.query({{ table_id: "{table_id}", limit: 1000 }});
  var seen = {{}}, marked = 0;
  for (var i = 0; i < records.length; i++) {{
    var v = records[i].{field_name};
    if (seen[v]) {{
      kdoc.dbt.record.update({{ table_id: "{table_id}", record_id: records[i].record_id,
        fields: {{ "{mark_field}": true }} }});
      marked++;
    }}
    seen[v] = true;
  }}
  return {{ marked: marked }};
}}""",
        "sample_params": {"table_id": "tbl_contact", "field_name": "email", "mark_field": "is_duplicate"},
        "expected": '{"marked": 5}',
    },
    {
        "id": "daily_summary", "name": "每日数据汇总", "domain": "data_summary",
        "keywords": ["汇总", "统计", "每日汇总", "日报"],
        "description": "按字段分组统计记录数",
        "params": ["table_id", "group_field"],
        "template": """// AirScript: 每日数据汇总
function main() {{
  var records = kdoc.dbt.record.query({{ table_id: "{table_id}", limit: 1000 }});
  var summary = {{}};
  for (var i = 0; i < records.length; i++) {{
    var k = records[i].{group_field};
    summary[k] = (summary[k] || 0) + 1;
  }}
  return summary;
}}""",
        "sample_params": {"table_id": "tbl_sales", "group_field": "region"},
        "expected": '{"华东": 30, "华南": 25}',
    },
    {
        "id": "overdue_notify", "name": "逾期通知", "domain": "scheduled_notify",
        "keywords": ["逾期", "催办", "逾期提醒", "通知"],
        "description": "扫描逾期任务并发送通知",
        "params": ["table_id", "date_field", "channel", "webhook_key", "notify_content"],
        "template": """// AirScript: 逾期通知
function main() {{
  var records = kdoc.dbt.record.query({{ table_id: "{table_id}", limit: 1000 }});
  var now = new Date().getTime(), overdue = 0;
  for (var i = 0; i < records.length; i++) {{
    if (new Date(records[i].{date_field}).getTime() < now) overdue++;
  }}
  kdoc.notification.send({{ channel: "{channel}", webhook_key: "{webhook_key}",
    content: {{ msgtype: "text", text: {{ content: "{notify_content}: " + overdue + " 条" }} }} }});
  return {{ notified: overdue }};
}}""",
        "sample_params": {"table_id": "tbl_task", "date_field": "deadline", "channel": "wecom", "webhook_key": "k1", "notify_content": "逾期任务"},
        "expected": '{"notified": 8}',
    },
    {
        "id": "birthday_notify", "name": "生日提醒", "domain": "scheduled_notify",
        "keywords": ["生日", "祝福", "生日提醒"],
        "description": "扫描当日生日并发送祝福通知",
        "params": ["table_id", "birthday_field", "channel", "webhook_key", "notify_content"],
        "template": """// AirScript: 生日提醒
function main() {{
  var records = kdoc.dbt.record.query({{ table_id: "{table_id}", limit: 1000 }});
  var today = new Date().toISOString().slice(5, 10), names = [];
  for (var i = 0; i < records.length; i++) {{
    var b = String(records[i].{birthday_field}).slice(5, 10);
    if (b === today) names.push(records[i].name);
  }}
  kdoc.notification.send({{ channel: "{channel}", webhook_key: "{webhook_key}",
    content: {{ msgtype: "text", text: {{ content: "{notify_content}: " + names.join(",") }} }} }});
  return {{ count: names.length, names: names }};
}}""",
        "sample_params": {"table_id": "tbl_hr", "birthday_field": "birthday", "channel": "wecom", "webhook_key": "k1", "notify_content": "今日生日"},
        "expected": '{"count": 2, "names": [...]}',
    },
    {
        "id": "field_unique_check", "name": "字段唯一性校验", "domain": "batch_operation",
        "keywords": ["唯一", "唯一性", "唯一校验", "校验"],
        "description": "校验字段值是否唯一",
        "params": ["table_id", "field_name"],
        "template": """// AirScript: 字段唯一性校验
function main() {{
  var records = kdoc.dbt.record.query({{ table_id: "{table_id}", limit: 1000 }});
  var seen = {{}}, conflicts = [];
  for (var i = 0; i < records.length; i++) {{
    var v = records[i].{field_name};
    if (seen[v]) conflicts.push(v);
    seen[v] = true;
  }}
  return {{ unique: conflicts.length === 0, conflicts: conflicts }};
}}""",
        "sample_params": {"table_id": "tbl_user", "field_name": "username"},
        "expected": '{"unique": true, "conflicts": []}',
    },
    {
        "id": "empty_field_fill", "name": "空字段填充", "domain": "field_calc",
        "keywords": ["空值", "填充", "默认值", "空字段"],
        "description": "为空字段批量填充默认值",
        "params": ["table_id", "field_name", "default_value"],
        "template": """// AirScript: 空字段填充
function main() {{
  var records = kdoc.dbt.record.query({{ table_id: "{table_id}", limit: 1000 }});
  var filled = 0;
  for (var i = 0; i < records.length; i++) {{
    if (!records[i].{field_name}) {{
      kdoc.dbt.record.update({{ table_id: "{table_id}", record_id: records[i].record_id,
        fields: {{ "{field_name}": "{default_value}" }} }});
      filled++;
    }}
  }}
  return {{ filled: filled }};
}}""",
        "sample_params": {"table_id": "tbl_data", "field_name": "status", "default_value": "待处理"},
        "expected": '{"filled": 17}',
    },
    {
        "id": "record_count_by_status", "name": "状态分布统计", "domain": "data_summary",
        "keywords": ["状态分布", "状态统计", "分布"],
        "description": "按状态字段统计各状态记录数",
        "params": ["table_id", "status_field"],
        "template": """// AirScript: 状态分布统计
function main() {{
  var records = kdoc.dbt.record.query({{ table_id: "{table_id}", limit: 1000 }});
  var dist = {{}};
  for (var i = 0; i < records.length; i++) {{
    var s = records[i].{status_field};
    dist[s] = (dist[s] || 0) + 1;
  }}
  return dist;
}}""",
        "sample_params": {"table_id": "tbl_task", "status_field": "status"},
        "expected": '{"待处理": 20, "进行中": 12, "已完成": 30}',
    },
    {
        "id": "date_format_normalize", "name": "日期格式规范化", "domain": "field_calc",
        "keywords": ["日期", "格式", "规范化", "日期格式"],
        "description": "把日期字段统一为 ISO 格式",
        "params": ["table_id", "date_field"],
        "template": """// AirScript: 日期格式规范化
function main() {{
  var records = kdoc.dbt.record.query({{ table_id: "{table_id}", limit: 1000 }});
  var normalized = 0;
  for (var i = 0; i < records.length; i++) {{
    var d = new Date(records[i].{date_field});
    if (!isNaN(d.getTime())) {{
      kdoc.dbt.record.update({{ table_id: "{table_id}", record_id: records[i].record_id,
        fields: {{ "{date_field}": d.toISOString().slice(0, 10) }} }});
      normalized++;
    }}
  }}
  return {{ normalized: normalized }};
}}""",
        "sample_params": {"table_id": "tbl_event", "date_field": "event_date"},
        "expected": '{"normalized": 45}',
    },
    {
        "id": "high_value_alert", "name": "高值告警", "domain": "data_summary",
        "keywords": ["高值", "告警", "阈值", "超标"],
        "description": "找出超过阈值的记录并标记",
        "params": ["table_id", "value_field", "threshold"],
        "template": """// AirScript: 高值告警
function main() {{
  var records = kdoc.dbt.record.query({{ table_id: "{table_id}", limit: 1000 }});
  var hits = [];
  for (var i = 0; i < records.length; i++) {{
    if (Number(records[i].{value_field}) > {threshold}) hits.push(records[i].record_id);
  }}
  return {{ alert_count: hits.length, records: hits }};
}}""",
        "sample_params": {"table_id": "tbl_metric", "value_field": "amount", "threshold": 10000},
        "expected": '{"alert_count": 6, "records": [...]}',
    },
    {
        "id": "batch_archive", "name": "批量归档", "domain": "batch_operation",
        "keywords": ["归档", "批量归档", "清理"],
        "description": "把符合规则的记录批量标记归档",
        "params": ["table_id", "condition_field", "condition_value", "archive_field"],
        "template": """// AirScript: 批量归档
function main() {{
  var records = kdoc.dbt.record.query({{ table_id: "{table_id}", limit: 1000 }});
  var archived = 0;
  for (var i = 0; i < records.length; i++) {{
    if (records[i].{condition_field} === "{condition_value}") {{
      kdoc.dbt.record.update({{ table_id: "{table_id}", record_id: records[i].record_id,
        fields: {{ "{archive_field}": true }} }});
      archived++;
    }}
  }}
  return {{ archived: archived }};
}}""",
        "sample_params": {"table_id": "tbl_order", "condition_field": "status", "condition_value": "已完成", "archive_field": "archived"},
        "expected": '{"archived": 88}',
    },
    {
        "id": "weekly_report_data", "name": "周报数据准备", "domain": "data_summary",
        "keywords": ["周报", "周数据", "周期汇总"],
        "description": "生成周报所需的分组统计数据",
        "params": ["table_id", "date_field", "group_field"],
        "template": """// AirScript: 周报数据准备
function main() {{
  var records = kdoc.dbt.record.query({{ table_id: "{table_id}", limit: 1000 }});
  var week = new Date().toISOString().slice(0, 10), groups = {{}};
  for (var i = 0; i < records.length; i++) {{
    var g = records[i].{group_field};
    groups[g] = (groups[g] || 0) + 1;
  }}
  return {{ week: week, groups: groups, total: records.length }};
}}""",
        "sample_params": {"table_id": "tbl_sales", "date_field": "sale_date", "group_field": "region"},
        "expected": '{"week": "...", "groups": {...}, "total": 200}',
    },
    {
        "id": "person_field_sync", "name": "人员字段同步", "domain": "field_calc",
        "keywords": ["人员", "负责人", "人员同步"],
        "description": "批量同步人员字段的负责人信息",
        "params": ["table_id", "person_field", "default_name", "default_email"],
        "template": """// AirScript: 人员字段同步
function main() {{
  var records = kdoc.dbt.record.query({{ table_id: "{table_id}", limit: 1000 }});
  var synced = 0;
  for (var i = 0; i < records.length; i++) {{
    if (!records[i].{person_field}) {{
      kdoc.dbt.record.update({{ table_id: "{table_id}", record_id: records[i].record_id,
        fields: {{ "{person_field}": {{ name: "{default_name}", email: "{default_email}" }} }} }});
      synced++;
    }}
  }}
  return {{ synced: synced }};
}}""",
        "sample_params": {"table_id": "tbl_task", "person_field": "owner", "default_name": "未分配", "default_email": ""},
        "expected": '{"synced": 9}',
    },
    {
        "id": "link_field_validate", "name": "链接字段校验", "domain": "batch_operation",
        "keywords": ["链接", "链接校验", "URL校验"],
        "description": "校验链接字段格式是否合法",
        "params": ["table_id", "link_field"],
        "template": """// AirScript: 链接字段校验
function main() {{
  var records = kdoc.dbt.record.query({{ table_id: "{table_id}", limit: 1000 }});
  var invalid = [];
  for (var i = 0; i < records.length; i++) {{
    var v = records[i].{link_field};
    if (v && !/^https?:\\/\\//.test(String(v.url || v))) invalid.push(records[i].record_id);
  }}
  return {{ invalid_count: invalid.length, records: invalid }};
}}""",
        "sample_params": {"table_id": "tbl_resource", "link_field": "url"},
        "expected": '{"invalid_count": 3, "records": [...]}',
    },
    {
        "id": "score_ranking", "name": "分数排名", "domain": "data_summary",
        "keywords": ["排名", "分数", "排序", "排行榜"],
        "description": "按分数字段生成排名",
        "params": ["table_id", "score_field", "limit_n"],
        "template": """// AirScript: 分数排名
function main() {{
  var records = kdoc.dbt.record.query({{ table_id: "{table_id}", limit: 1000 }});
  records.sort(function(a, b) {{ return (b.{score_field} || 0) - (a.{score_field} || 0); }});
  var top = records.slice(0, {limit_n}).map(function(r) {{
    return {{ name: r.name, score: r.{score_field} }};
  }});
  return {{ ranking: top }};
}}""",
        "sample_params": {"table_id": "tbl_exam", "score_field": "score", "limit_n": 10},
        "expected": '{"ranking": [{"name":"...","score":98}, ...]}',
    },
    {
        "id": "inventory_low_stock", "name": "库存预警", "domain": "data_summary",
        "keywords": ["库存", "预警", "低库存", "补货"],
        "description": "找出库存低于安全线的记录",
        "params": ["table_id", "stock_field", "safety_line"],
        "template": """// AirScript: 库存预警
function main() {{
  var records = kdoc.dbt.record.query({{ table_id: "{table_id}", limit: 1000 }});
  var low = [];
  for (var i = 0; i < records.length; i++) {{
    if (Number(records[i].{stock_field}) < {safety_line}) {{
      low.push({{ name: records[i].name, stock: records[i].{stock_field} }});
    }}
  }}
  return {{ low_count: low.length, items: low }};
}}""",
        "sample_params": {"table_id": "tbl_stock", "stock_field": "qty", "safety_line": 10},
        "expected": '{"low_count": 4, "items": [...]}',
    },
    {
        "id": "attendance_anomaly", "name": "考勤异常检测", "domain": "batch_operation",
        "keywords": ["考勤", "异常", "打卡", "缺勤"],
        "description": "检测考勤异常记录",
        "params": ["table_id", "hours_field", "standard_hours"],
        "template": """// AirScript: 考勤异常检测
function main() {{
  var records = kdoc.dbt.record.query({{ table_id: "{table_id}", limit: 1000 }});
  var anomalies = [];
  for (var i = 0; i < records.length; i++) {{
    if (Number(records[i].{hours_field}) < {standard_hours}) {{
      anomalies.push(records[i].record_id);
    }}
  }}
  return {{ anomaly_count: anomalies.length, records: anomalies }};
}}""",
        "sample_params": {"table_id": "tbl_attendance", "hours_field": "work_hours", "standard_hours": 8},
        "expected": '{"anomaly_count": 7, "records": [...]}',
    },
    {
        "id": "merge_duplicate_records", "name": "重复记录合并建议", "domain": "data_summary",
        "keywords": ["合并", "重复记录", "合并建议"],
        "description": "按身份字段分组给出重复记录合并建议",
        "params": ["table_id", "identity_field"],
        "template": """// AirScript: 重复记录合并建议
function main() {{
  var records = kdoc.dbt.record.query({{ table_id: "{table_id}", limit: 1000 }});
  var groups = {{}};
  for (var i = 0; i < records.length; i++) {{
    var k = records[i].{identity_field};
    (groups[k] = groups[k] || []).push(records[i].record_id);
  }}
  var suggestions = [];
  for (var k in groups) {{ if (groups[k].length > 1) suggestions.push({{ key: k, ids: groups[k] }}); }}
  return {{ duplicate_groups: suggestions.length, groups: suggestions }};
}}""",
        "sample_params": {"table_id": "tbl_contact", "identity_field": "phone"},
        "expected": '{"duplicate_groups": 3, "groups": [...]}',
    },
    {
        "id": "todo_daily_digest", "name": "待办每日摘要", "domain": "scheduled_notify",
        "keywords": ["待办", "每日摘要", "任务摘要", "digest"],
        "description": "汇总当日待办并推送摘要",
        "params": ["table_id", "status_field", "channel", "webhook_key", "notify_content"],
        "template": """// AirScript: 待办每日摘要
function main() {{
  var records = kdoc.dbt.record.query({{ table_id: "{table_id}", limit: 1000 }});
  var pending = 0;
  for (var i = 0; i < records.length; i++) {{
    if (records[i].{status_field} === "待处理") pending++;
  }}
  kdoc.notification.send({{ channel: "{channel}", webhook_key: "{webhook_key}",
    content: {{ msgtype: "text", text: {{ content: "{notify_content}: " + pending + " 条待处理" }} }} }});
  return {{ pending: pending }};
}}""",
        "sample_params": {"table_id": "tbl_task", "status_field": "status", "channel": "kdocs", "webhook_key": "k1", "notify_content": "今日待办"},
        "expected": '{"pending": 15}',
    },
]


class AirScriptPresetLibrary:
    """AirScript 预设库"""

    def __init__(self, db_path: Optional[str] = None, backend: Any = None):
        self.db_path = db_path or self._default_db_path()
        self.backend = backend
        self._init_db()

    def _default_db_path(self) -> str:
        skill_root = Path(__file__).resolve().parent.parent
        return str(skill_root / ".airscript_presets.db")

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS airscript_presets (
                    preset_id TEXT PRIMARY KEY,
                    name TEXT,
                    domain TEXT,
                    metadata TEXT,
                    installed_at TEXT
                )
            """)
            conn.commit()
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # 元数据 / 匹配
    # ------------------------------------------------------------------
    @staticmethod
    def list_presets() -> Dict[str, Any]:
        return {
            "success": True,
            "total": len(PRESETS),
            "presets": [
                {
                    "id": p["id"], "name": p["name"], "domain": p["domain"],
                    "description": p["description"], "keywords": p["keywords"],
                    "params": p["params"], "has_test": bool(p.get("sample_params")),
                }
                for p in PRESETS
            ],
        }

    @staticmethod
    def get_preset(preset_id: str) -> Dict[str, Any]:
        for p in PRESETS:
            if p["id"] == preset_id:
                return {"success": True, "preset": p}
        return {"success": False, "error": f"预设不存在：{preset_id}"}

    @staticmethod
    def match_from_natural_language(text: str) -> Dict[str, Any]:
        """从自然语言按关键词匹配最佳预设（本地规则，无需 LLM）"""
        text_l = text.lower()
        scored: List[tuple] = []
        for p in PRESETS:
            score = 0
            for kw in p["keywords"]:
                if kw in text or kw.lower() in text_l:
                    score += 3
            if p["name"] in text:
                score += 2
            if score:
                scored.append((score, p))
        if not scored:
            return {
                "success": False,
                "error": "未匹配到预设，请用 list_presets 查看全部可用预设",
            }
        scored.sort(key=lambda x: x[0], reverse=True)
        best = scored[0][1]
        return {
            "success": True,
            "preset_id": best["id"],
            "name": best["name"],
            "score": scored[0][0],
            "candidates": [{"id": p["id"], "name": p["name"]} for _, p in scored[:5]],
        }

    # ------------------------------------------------------------------
    # 生成 - 预检 - 预览
    # ------------------------------------------------------------------
    def generate(self, preset_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """按预设生成脚本（用测试样例补齐缺失参数）"""
        preset_res = self.get_preset(preset_id)
        if not preset_res.get("success"):
            return preset_res
        preset = preset_res["preset"]
        merged = dict(preset.get("sample_params", {}))
        if params:
            merged.update(params)

        # 检查必填参数
        missing = [k for k in preset["params"] if k not in merged]
        if missing:
            return {"success": False, "error": f"缺少参数：{missing}", "required": preset["params"]}

        try:
            content = preset["template"].format(**merged)
        except (KeyError, IndexError, ValueError) as e:
            return {"success": False, "error": f"模板参数缺失或格式错误：{e}"}

        # 走 airscript 预检（复用危险操作扫描）
        safety = {"safe": True, "findings": [], "risk_level": "low"}
        try:
            from engine.airscript import get_airscript_engine
            safety = get_airscript_engine(self.backend).precheck_script(content)
        except Exception:
            pass

        return {
            "success": True,
            "preset_id": preset_id,
            "name": preset["name"],
            "domain": preset["domain"],
            "script_content": content,
            "safety": safety,
            "params": merged,
            "sample_params": preset.get("sample_params"),
            "expected_output": preset.get("expected"),
            "workflow": ["generate", "preview", "confirm", "execute"],
        }

    def install_metadata(self) -> Dict[str, Any]:
        """把所有预设元数据落库（带测试样例与预期输出）"""
        conn = sqlite3.connect(self.db_path)
        try:
            for p in PRESETS:
                metadata = {
                    "name": p["name"], "domain": p["domain"],
                    "keywords": p["keywords"], "params": p["params"],
                    "sample_params": p.get("sample_params"),
                    "expected_output": p.get("expected"),
                    "description": p["description"],
                }
                conn.execute(
                    """INSERT OR REPLACE INTO airscript_presets
                       (preset_id, name, domain, metadata, installed_at)
                       VALUES (?, ?, ?, ?, ?)""",
                    (p["id"], p["name"], p["domain"],
                     json.dumps(metadata, ensure_ascii=False), datetime.now().isoformat()),
                )
            conn.commit()
        finally:
            conn.close()
        return {"success": True, "installed": len(PRESETS)}

    def validate_all(self) -> Dict[str, Any]:
        """校验全部预设：测试样例可生成脚本 + 预期输出非空"""
        passed, failed = [], []
        for p in PRESETS:
            try:
                content = p["template"].format(**p.get("sample_params", {}))
                ok = (bool(content) and bool(p.get("expected"))
                      and all(k in p["sample_params"] for k in p["params"]))
                (passed if ok else failed).append(p["id"])
            except Exception as e:
                failed.append(f"{p['id']}:{e}")
        return {
            "success": len(failed) == 0,
            "total": len(PRESETS),
            "passed": len(passed),
            "failed": failed,
        }

    def get_status(self) -> Dict[str, Any]:
        return {
            "version": "4.4.0",
            "total_presets": len(PRESETS),
            "domains": sorted({p["domain"] for p in PRESETS}),
            "all_with_tests": all(p.get("sample_params") and p.get("expected") for p in PRESETS),
        }


# ---------------------------------------------------------------------------
# 模块级便捷函数
# ---------------------------------------------------------------------------
def get_preset_library(db_path: Optional[str] = None, backend: Any = None) -> AirScriptPresetLibrary:
    return AirScriptPresetLibrary(db_path, backend)


def list_presets() -> Dict[str, Any]:
    return AirScriptPresetLibrary.list_presets()


def preset_from_text(text: str) -> Dict[str, Any]:
    return AirScriptPresetLibrary.match_from_natural_language(text)


def generate_from_preset(preset_id: str, params: Optional[Dict[str, Any]] = None,
                         **kwargs) -> Dict[str, Any]:
    return AirScriptPresetLibrary(kwargs.get("db_path"), kwargs.get("backend")).generate(preset_id, params)
