# -*- coding: utf-8 -*-
"""
doc_types.py — paper-kb 资料类型与目录结构的唯一定义来源

三个 Skill（init_user / ingest_paper / query_papers）都引用本文件，
保证"初始化建的结构"和"入库写入的路径"永远一致。

如需新增资料类型，只改这一个文件即可。
"""
from __future__ import annotations

# 六种资料类型。键是内部标识(也是 summaries 下的子文件夹名)，值是中文名与属性。
#   folder:   summaries/ 下的子目录
#   cn:       中文类型名（写入 frontmatter 的"类型"字段、飞书表格、index 分区标题）
#   scored:   是否做"与研究方向相关性"评分（自有资料不评分）
#   dated:    文件名是否加日期前缀（会议/实验这类同名风险高）
DOC_TYPES = {
    "paper":      {"folder": "papers",      "cn": "论文",     "scored": True,  "dated": False},
    "survey":     {"folder": "surveys",     "cn": "行业调研", "scored": True,  "dated": False},
    "project":    {"folder": "projects",    "cn": "开源项目", "scored": True,  "dated": False},
    "doc":        {"folder": "docs_tech",   "cn": "技术文档", "scored": True,  "dated": False},
    "experiment": {"folder": "experiments", "cn": "实验记录", "scored": False, "dated": True},
    "meeting":    {"folder": "meetings",    "cn": "会议纪要", "scored": False, "dated": True},
}

# 中文名 → 内部标识 的反查表（用户用中文说类型时用）
CN_TO_KEY = {v["cn"]: k for k, v in DOC_TYPES.items()}

# 默认类型（AI 实在判断不出时的兜底）
DEFAULT_TYPE = "doc"


def resolve_type(raw: str) -> str:
    """把用户/AI 给出的类型字符串归一化成内部标识 key。

    接受内部标识(paper)、中文名(论文)，都能识别；无法识别返回 DEFAULT_TYPE。
    """
    if not raw:
        return DEFAULT_TYPE
    raw = raw.strip()
    if raw in DOC_TYPES:
        return raw
    if raw in CN_TO_KEY:
        return CN_TO_KEY[raw]
    return DEFAULT_TYPE


def folder_of(type_key: str) -> str:
    """返回该类型在 summaries 下的子文件夹名。"""
    return DOC_TYPES.get(type_key, DOC_TYPES[DEFAULT_TYPE])["folder"]


def cn_of(type_key: str) -> str:
    return DOC_TYPES.get(type_key, DOC_TYPES[DEFAULT_TYPE])["cn"]


def is_scored(type_key: str) -> bool:
    return DOC_TYPES.get(type_key, DOC_TYPES[DEFAULT_TYPE])["scored"]


def is_dated(type_key: str) -> bool:
    return DOC_TYPES.get(type_key, DOC_TYPES[DEFAULT_TYPE])["dated"]


def all_summary_folders() -> list[str]:
    """返回 summaries 下所有子文件夹名（init_user 建初始结构时用）。"""
    return [v["folder"] for v in DOC_TYPES.values()]
