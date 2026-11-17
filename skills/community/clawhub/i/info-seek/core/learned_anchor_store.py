#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""core/learned_anchor_store.py — 学习型切词锚点的独立物理层与统一访问协议（mod-v1.0.0）

S4 · 方向一阶段B「影子模式」
============================
把 S2/S3 观测中沉淀的高置信候选词，从「主链内置 frozenset `_ZH_HIGH_FREQ`」里
**解耦**出来，放进一个独立、可读写、可裁决的 learned 层。主链
（scripts/infoseek_zerodep_nlp.py 的估计器 D）**默认不读、不拼**本层。

三条铁律（S4 不可违背）
----------------------
  1. **默认不启用**：is_enabled() 默认 False；唯一开关 INFOSEEK_LEARNED_ANCHORS=1。
     即便进程读取本层，也只用于影子比对，绝不改主链门控结果。
  2. **损坏回退空表**：文件缺失 / JSON 损坏 / schema 不符 → 返回空表，永不抛错，
     绝不拖垮主链。
  3. **单向依赖**：本模块是纯下层事实/存储层，**绝不 import** capability_registry、
     infoseek_zerodep_nlp 或任何 cap / 主链消费点；只依赖标准库与同层 state_dir。

数据模型
--------
  {
    "_doc": str,
    "version": int,                 # 存储结构版本
    "updated_at": iso8601,
    "entries": {
      term: {
        "term": str,
        "decision": "pending" | "accept" | "reject",
        "added_at": iso8601,
        "decided_at": iso8601 | None,
        "provenance": {...},        # 选种证据：topic/cat/cover/doc/freq/pos
        "substring_of": [terms],    # 本词是哪些更长词的子串（冲突登记）
        "has_substring": [terms],   # 哪些更短词是本词子串
        "note": ""
      }
    }
  }

S4 只用到：load / active_terms / upsert_pending / set_decision / conflicts。
S5（自动晋级）才会让主链在 accept 集合上接线；本层已为此预留，但 S4 不接。
"""
from __future__ import annotations

import json
import os
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

MOD_VERSION = "mod-v1.0.0"
STORE_VERSION = 1
STORE_FILENAME = "learned_anchors.json"
_ENV_ENABLE = "INFOSEEK_LEARNED_ANCHORS"

VALID_DECISIONS = ("pending", "accept", "reject")


# --------------------------------------------------------------------------- #
# 启用开关
# --------------------------------------------------------------------------- #
def is_enabled() -> bool:
    """统一访问协议开关。S4 默认 False；只有显式 =1/true/yes/on 才开启。

    即便开启，S4 语义也只允许影子比对读取，不允许主链改门控。
    """
    return os.environ.get(_ENV_ENABLE, "").strip().lower() in ("1", "true", "yes", "on")


# --------------------------------------------------------------------------- #
# 路径
# --------------------------------------------------------------------------- #
def store_path() -> "object":
    """返回存储文件 Path。优先复用 core.state_dir 的数据目录解析。"""
    try:
        from core import state_dir  # 同层；脚本独立运行时可能失败
        return state_dir.state_path(STORE_FILENAME)
    except Exception:
        base = os.environ.get("INFOSEEK_DATA_DIR") or os.path.join(
            os.path.expanduser("~"), ".infoseek"
        )
        return os.path.join(base, STORE_FILENAME)


# --------------------------------------------------------------------------- #
# 空结构 / 读取（损坏回退空表）
# --------------------------------------------------------------------------- #
def _empty_store() -> dict:
    return {"_doc": "Infoseek learned anchor store (S4 shadow, default OFF)",
            "version": STORE_VERSION, "updated_at": None, "entries": {}}


def _coerce(raw) -> dict:
    """把磁盘内容规整为合法 store；任何不符 → 空表。"""
    if not isinstance(raw, dict):
        return _empty_store()
    entries = raw.get("entries")
    if not isinstance(entries, dict):
        return _empty_store()
    clean: Dict[str, dict] = {}
    for term, e in entries.items():
        if not isinstance(term, str) or not isinstance(e, dict):
            continue
        decision = e.get("decision", "pending")
        if decision not in VALID_DECISIONS:
            decision = "pending"
        clean[term] = {
            "term": term,
            "decision": decision,
            "added_at": e.get("added_at"),
            "decided_at": e.get("decided_at"),
            "provenance": e.get("provenance", {}) if isinstance(e.get("provenance"), dict) else {},
            "substring_of": list(e.get("substring_of", []) or []),
            "has_substring": list(e.get("has_substring", []) or []),
            "note": e.get("note", ""),
        }
    return {"_doc": raw.get("_doc", ""), "version": STORE_VERSION,
            "updated_at": raw.get("updated_at"), "entries": clean}


def load(path: Optional[str] = None) -> dict:
    """读取 store；文件缺失/损坏一律回退空表，绝不抛错。"""
    p = path or str(store_path())
    try:
        with open(p, "r", encoding="utf-8") as fh:
            return _coerce(json.load(fh))
    except FileNotFoundError:
        return _empty_store()
    except (json.JSONDecodeError, OSError, ValueError) as exc:
        logger.warning("learned_anchor_store 损坏，回退空表: %s (%s)", p, exc)
        return _empty_store()


# --------------------------------------------------------------------------- #
# 查询
# --------------------------------------------------------------------------- #
def list_entries(path: Optional[str] = None) -> Dict[str, dict]:
    return load(path).get("entries", {})


def active_terms(decision: str = "accept", path: Optional[str] = None) -> List[str]:
    """返回指定裁决态的词表（影子/未来晋级消费）。S4 主链不调用本函数。"""
    if decision not in VALID_DECISIONS:
        raise ValueError(f"bad decision {decision}")
    return sorted(t for t, e in list_entries(path).items() if e["decision"] == decision)


def pending_terms(path: Optional[str] = None) -> List[str]:
    return active_terms("pending", path)


def get(term: str, path: Optional[str] = None) -> Optional[dict]:
    return list_entries(path).get(term)


# --------------------------------------------------------------------------- #
# 写入
# --------------------------------------------------------------------------- #
def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _refresh_conflicts(entries: Dict[str, dict]) -> None:
    """重算全部子串包含关系并双向登记（长词优先匹配场景下的顶替冲突）。"""
    terms = sorted(entries, key=len, reverse=True)
    for e in entries.values():
        e["substring_of"] = []
        e["has_substring"] = []
    for i, long in enumerate(terms):
        for short in terms[i + 1:]:
            if short in long:
                entries[short]["substring_of"].append(long)
                entries[long]["has_substring"].append(short)
    for e in entries.values():
        e["substring_of"].sort()
        e["has_substring"].sort()


def save(store: dict, path: Optional[str] = None) -> str:
    """原子写盘（同目录临时文件 + replace）。返回落盘路径。"""
    p = path or str(store_path())
    os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)
    store["version"] = STORE_VERSION
    store["updated_at"] = _now()
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(store, fh, ensure_ascii=False, indent=2)
    os.replace(tmp, p)
    return p


def upsert_pending(term: str, provenance: Optional[dict] = None,
                   path: Optional[str] = None) -> dict:
    """新增一个 pending 候选；已存在则不覆盖既有裁决，只补全 provenance。"""
    store = load(path)
    entries = store["entries"]
    if term in entries:
        if provenance:
            entries[term]["provenance"].update(provenance)
    else:
        entries[term] = {"term": term, "decision": "pending", "added_at": _now(),
                         "decided_at": None, "provenance": dict(provenance or {}),
                         "substring_of": [], "has_substring": [], "note": ""}
    _refresh_conflicts(entries)
    save(store, path)
    return entries[term]


def bulk_upsert_pending(items: List[dict], path: Optional[str] = None) -> int:
    """批量灌入 pending。items 元素需含 term，其余字段作为 provenance。

    一次落盘（避免逐条 IO）。已存在词不覆盖裁决。
    """
    store = load(path)
    entries = store["entries"]
    n = 0
    for it in items:
        term = it.get("term")
        if not term:
            continue
        prov = {k: v for k, v in it.items() if k != "term"}
        if term in entries:
            entries[term]["provenance"].update(prov)
        else:
            entries[term] = {"term": term, "decision": "pending", "added_at": _now(),
                             "decided_at": None, "provenance": prov,
                             "substring_of": [], "has_substring": [], "note": ""}
        n += 1
    _refresh_conflicts(entries)
    save(store, path)
    return n


def set_decision(term: str, decision: str, note: str = "",
                 path: Optional[str] = None) -> Optional[dict]:
    """人工抽检裁决：accept / reject / pending。词不存在返回 None。"""
    if decision not in VALID_DECISIONS:
        raise ValueError(f"bad decision {decision}")
    store = load(path)
    e = store["entries"].get(term)
    if e is None:
        return None
    e["decision"] = decision
    e["decided_at"] = _now() if decision != "pending" else None
    if note:
        e["note"] = note
    save(store, path)
    return e


def conflicts(path: Optional[str] = None) -> List[dict]:
    """返回存在子串关系的候选对（供人工抽检优先看「长词是否顶替短词」）。"""
    out = []
    for term, e in list_entries(path).items():
        for long in e["substring_of"]:
            out.append({"long": long, "short": term})
    return out


def reset(path: Optional[str] = None) -> None:
    """清空 store（测试用）。"""
    save(_empty_store(), path)
