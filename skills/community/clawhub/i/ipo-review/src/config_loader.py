from __future__ import annotations

import re
from pathlib import Path
from typing import Any


DEFAULT_METRICS = {
    "营业收入": {"aliases": ["营业收入"], "category": "收入类"},
    "主营业务收入": {"aliases": ["主营业务收入"], "category": "收入类"},
    "其他业务收入": {"aliases": ["其他业务收入"], "category": "收入类"},
    "净利润": {"aliases": ["净利润"], "category": "利润类"},
    "归母净利润": {"aliases": ["归母净利润", "归属于母公司股东的净利润", "归属于母公司所有者的净利润"], "category": "利润类"},
    "扣非归母净利润": {"aliases": ["扣非归母净利润"], "category": "利润类"},
    "应收账款": {"aliases": ["应收账款"], "category": "应收款项类"},
    "应收账款余额": {"aliases": ["应收账款余额"], "category": "应收款项类"},
    "应收账款账面余额": {"aliases": ["应收账款账面余额"], "category": "应收款项类"},
    "应收账款账面价值": {"aliases": ["应收账款账面价值"], "category": "应收款项类"},
    "期后回款金额": {"aliases": ["期后回款金额", "期后回款"], "category": "期后回款类"},
    "期后回款比例": {"aliases": ["期后回款比例", "回款比例"], "category": "期后回款类"},
    "未回款金额": {"aliases": ["未回款金额"], "category": "期后回款类"},
    "未回款比例": {"aliases": ["未回款比例", "未回款占比"], "category": "期后回款类"},
    "经销商销售收入": {"aliases": ["经销商销售收入", "经销模式销售收入"], "category": "经销商类"},
    "经销商应收余额": {"aliases": ["经销商应收余额", "经销商应收账款余额"], "category": "经销商类"},
    "经销商期后回款比例": {"aliases": ["经销商期后回款比例", "经销模式期后回款比例"], "category": "经销商类"},
    "直销期后回款比例": {"aliases": ["直销期后回款比例", "直销客户期后回款比例"], "category": "直销客户类"},
    "应收票据期后兑付比例": {"aliases": ["应收票据期后兑付比例"], "category": "应收款项类"},
    "应收款项融资期后兑付比例": {"aliases": ["应收款项融资期后兑付比例"], "category": "应收款项类"},
    "坏账准备": {"aliases": ["坏账准备"], "category": "应收款项类"},
    "毛利率": {"aliases": ["毛利率", "综合毛利率"], "category": "毛利率类"},
    "主营业务毛利率": {"aliases": ["主营业务毛利率"], "category": "毛利率类"},
    "研发费用": {"aliases": ["研发费用"], "category": "研发类"},
    "研发投入": {"aliases": ["研发投入"], "category": "研发类"},
}

DEFAULT_ROLES = {
    "prospectus": {"name": "招股说明书", "priority": 2, "keywords": ["招股说明书", "招股书"]},
    "financial_statements": {"name": "审计报告及财务报表", "priority": 1, "keywords": ["审计报告", "财务报表"]},
    "notes": {"name": "财务报表附注", "priority": 1, "keywords": ["附注", "财务报表附注"]},
    "inquiry_round_1": {"name": "第一轮问询回复", "priority": 4, "keywords": ["第一轮", "首轮", "一轮", "问询回复"]},
    "inquiry_round_2": {"name": "第二轮问询回复", "priority": 3, "keywords": ["第二轮", "二轮", "问询回复"]},
    "other": {"name": "其他文件", "priority": 9, "keywords": []},
}


def load_config(config_dir: str | Path) -> dict[str, Any]:
    base = Path(config_dir)
    return {
        "metrics": _load_metrics(base / "metric_dictionary.yaml"),
        "roles": _load_roles(base / "document_roles.yaml"),
        "tolerance": _load_flat_numbers(base / "tolerance_rules.yaml"),
    }


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _load_metrics(path: Path) -> dict[str, dict[str, str]]:
    text = _read(path)
    alias_to_metric: dict[str, dict[str, str]] = {}
    current = None
    current_category = ""
    for line in text.splitlines():
        metric_match = re.match(r"\s{2}([^:\s]+):\s*$", line)
        if metric_match:
            current = metric_match.group(1)
            current_category = current
            alias_to_metric[current] = {"exact": current, "category": current_category, "alias": current}
            continue
        category_match = re.search(r"category:\s*(.+)", line)
        if current and category_match:
            current_category = category_match.group(1).strip()
            for alias, meta in list(alias_to_metric.items()):
                if meta["exact"] == current:
                    meta["category"] = current_category
        alias_match = re.search(r"aliases:\s*\[(.*?)\]", line)
        if current and alias_match:
            for alias in alias_match.group(1).split(","):
                alias = alias.strip()
                if alias:
                    alias_to_metric[alias] = {"exact": current, "category": current_category, "alias": alias}
    if not alias_to_metric:
        for metric, meta in DEFAULT_METRICS.items():
            for alias in meta["aliases"]:
                alias_to_metric[alias] = {"exact": metric, "category": meta["category"], "alias": alias}
    return alias_to_metric


def _load_roles(path: Path) -> dict[str, dict[str, Any]]:
    text = _read(path)
    roles = DEFAULT_ROLES.copy()
    current = None
    for line in text.splitlines():
        role_match = re.match(r"\s{2}([a-zA-Z0-9_]+):\s*$", line)
        if role_match:
            current = role_match.group(1)
            roles.setdefault(current, {"name": current, "priority": 9, "keywords": []})
            continue
        if not current:
            continue
        name_match = re.search(r"name:\s*(.+)", line)
        priority_match = re.search(r"priority:\s*(\d+)", line)
        keywords_match = re.search(r"keywords:\s*\[(.*?)\]", line)
        if name_match:
            roles[current]["name"] = name_match.group(1).strip()
        if priority_match:
            roles[current]["priority"] = int(priority_match.group(1))
        if keywords_match:
            roles[current]["keywords"] = [x.strip() for x in keywords_match.group(1).split(",") if x.strip()]
    return roles


def _load_flat_numbers(path: Path) -> dict[str, float]:
    text = _read(path)
    values = {"amount_default_abs": 0.01, "percent_default_abs": 0.01, "conflict_min_abs": 0.02}
    for key in list(values):
        match = re.search(rf"^{key}:\s*([0-9.]+)", text, re.M)
        if match:
            values[key] = float(match.group(1))
    return values
