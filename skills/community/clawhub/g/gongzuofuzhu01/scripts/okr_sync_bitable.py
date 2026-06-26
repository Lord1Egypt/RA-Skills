"""
OKR Bitable Sync Bridge

Reads OKR data from kpi-bonus-v2's Feishu Bitable (表⑤ OKR目标表)
and syncs to zhudongtixingzl's local SQLite via OKRManager.
"""

from __future__ import annotations

# ⚠️ 使用前请替换为你的飞书多维表格 app_token 和 table_id
BITABLE_CONFIG = {
    "app_token": "",
    "table_id": "",
}

# 位表字段 field_id → 字段含义映射
FIELD_MAP = {
    "YOUR_FIELD_ID_PERIOD": "period",        # 周期
    "YOUR_FIELD_ID_OBJECTIVE": "objective",   # 目标O
    "YOUR_FIELD_ID_KR": "key_result",         # 关键结果KR
    "YOUR_FIELD_ID_KR_WEIGHT": "kr_weight",   # KR权重
    "YOUR_FIELD_ID_COMPLETION": "completion",  # 完成度
    "YOUR_FIELD_ID_KR_SCORE": "kr_score",      # KR得分
    "YOUR_FIELD_ID_O_SCORE": "o_score",        # O得分
    "YOUR_FIELD_ID_STATUS": "status",          # 状态
    "YOUR_FIELD_ID_LEVEL": "level",            # 层级
    "YOUR_FIELD_ID_DEPT": "department",         # 部门
    "YOUR_FIELD_ID_OWNER": "owner",            # 负责人
    "YOUR_FIELD_ID_ALIGNED": "aligned_to",      # 对齐中心O
}

# 状态映射：位表值 → 内部状态
_STATUS_MAP = {
    "进行中": "active",
    "active": "active",
    "已完成": "completed",
    "completed": "completed",
}


def _extract_fields(record: dict) -> dict:
    """Convert a single bitable record's fields dict from field_id keys
    to human-readable keys using FIELD_MAP.

    Handles missing ``fields`` key gracefully by returning an empty dict.
    """
    raw = record.get("fields")
    if not raw:
        return {}
    result = {}
    for fid, fname in FIELD_MAP.items():
        if fid in raw:
            result[fname] = raw[fid]
    return result


def _map_status(raw_status) -> str:
    """Map bitable status value to internal status string.

    Returns ``"active"`` when *raw_status* is None / empty / unrecognised.
    """
    if raw_status is None:
        return "active"
    return _STATUS_MAP.get(str(raw_status), "active")


def build_sync_request(period: str, app_token: str = None, table_id: str = None) -> dict:
    """Build the payload needed for feishu_bitable_app_table_record to fetch OKR data.
    
    Returns a dict with:
        app_token, table_id, view_id (optional), filter (by period field), page_size
    This is a helper for the agent layer — it doesn't make API calls itself,
    but provides the exact parameters needed.
    """
    app_token = app_token or BITABLE_CONFIG["app_token"]
    table_id = table_id or BITABLE_CONFIG["table_id"]
    
    return {
        "app_token": app_token,
        "table_id": table_id,
        "action": "list",
        "filter": {
            "conjunction": "and",
            "conditions": [
                {"field_name": "周期", "operator": "is", "value": [period]}
            ]
        },
        "page_size": 500,
    }


def _safe_float(value, default: float = 0.0) -> float:
    """Coerce *value* to float, falling back to *default* on failure."""
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def parse_bitable_rows(records: list[dict]) -> list[dict]:
    """Parse flat bitable rows into O→KR hierarchy.

    Each bitable row contains fields as a dict of ``{field_id: value}``.
    Rows where the ``key_result`` field is empty/None are treated as
    O-level rows.  Rows where ``key_result`` has content are KR-level
    rows, grouped under their parent O by matching the ``objective``
    field.

    Returns a list of structured dicts, each representing an Objective
    with its child Key Results:

    .. code-block:: python

        [{
            "obj_type": "objective",
            "title": "提升系统稳定性",
            "status": "active",
            "progress": 60,
            "extra": {"department": "技术中心", "owner": "张三", ...},
            "key_results": [
                {
                    "obj_type": "key_result",
                    "title": "P99延迟降至200ms",
                    "weight": 30.0,
                    "progress": 80.0,
                    "status": "active",
                    "extra": {...},
                },
                ...
            ]
        }, ...]

    Missing / None fields receive sensible defaults: progress=0, weight=0,
    status="active", extra={}.
    """
    if not records:
        return []

    # Pass 1: build a dict of {objective_title: {o_dict, krs: [...]}}
    objectives: dict[str, dict] = {}
    # Track insertion order
    ordered_titles: list[str] = []

    for record in records:
        data = _extract_fields(record)
        title = data.get("objective")
        if not title:
            continue  # Skip rows without an objective name

        kr_title = data.get("key_result")
        if kr_title:
            # --- KR-level row ---
            if title not in objectives:
                # O not yet created; create a placeholder and defer O-level
                # fields for when/if a real O row appears
                objectives[title] = {
                    "obj_type": "objective",
                    "title": title,
                    "status": "active",
                    "progress": 0.0,
                    "extra": {},
                    "key_results": [],
                    "_has_o_row": False,
                }
                ordered_titles.append(title)

            kr = {
                "obj_type": "key_result",
                "title": str(kr_title),
                "weight": _safe_float(data.get("kr_weight")),
                "progress": _safe_float(data.get("completion")),
                "status": _map_status(data.get("status")),
                "extra": {},
            }

            # Populate KR extras
            for extra_key in ("department", "owner", "level",
                              "o_score", "kr_score", "aligned_to"):
                val = data.get(extra_key)
                if val is not None:
                    kr["extra"][extra_key] = val

            objectives[title]["key_results"].append(kr)
        else:
            # --- O-level row ---
            o = objectives.get(title)
            if o is None:
                o = {
                    "obj_type": "objective",
                    "title": title,
                    "status": "active",
                    "progress": 0.0,
                    "extra": {},
                    "key_results": [],
                    "_has_o_row": True,
                }
                objectives[title] = o
                ordered_titles.append(title)
            else:
                o["_has_o_row"] = True

            # Fill O-level fields (O row may appear before or after its KRs)
            o["progress"] = _safe_float(data.get("completion"))
            o["status"] = _map_status(data.get("status"))

            # Populate O extras
            for extra_key in ("department", "owner", "level",
                              "o_score", "kr_score", "aligned_to"):
                val = data.get(extra_key)
                if val is not None:
                    o["extra"][extra_key] = val

    # Clean up internal bookkeeping key and build result list in order
    result = []
    for title in ordered_titles:
        o = objectives[title]
        o.pop("_has_o_row", None)
        result.append(o)

    return result
