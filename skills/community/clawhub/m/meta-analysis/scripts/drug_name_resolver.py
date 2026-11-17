#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
drug_name_resolver.py / 中文药物名 → 英文标准名解析

检测非 ASCII（如中文）药物名，从 references/drug_name_map.json 查找候选英文名，
通过 CLI 编号菜单让用户确认。找不到时提示手动输入英文名。

映射表单一真源：ct-base/references/drug_name_map.json（471 条）。
开发期通过「本地优先 + ct-base 回退」查找；发布期由 publish_inject.py 注入副本。
零保密数据，所有映射来自公开 INN/通用名标准翻译。
"""
import json
import os
import sys

# 映射表路径：本地 references/ 优先，回退 ct-base/references/
_HERE = os.path.dirname(os.path.abspath(__file__))
_LOCAL_REF = os.path.join(os.path.dirname(_HERE), "references", "drug_name_map.json")
_CTBASE_REF = os.path.join(os.path.dirname(_HERE), "..", "..", "ct-base", "references", "drug_name_map.json")

_MAP_PATH = None
if os.path.isfile(_LOCAL_REF):
    _MAP_PATH = _LOCAL_REF
elif os.path.isfile(_CTBASE_REF):
    _MAP_PATH = _CTBASE_REF

_CACHE = None


def _load_map():
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    if _MAP_PATH is None or not os.path.isfile(_MAP_PATH):
        _CACHE = {}
        return _CACHE
    with open(_MAP_PATH, "r", encoding="utf-8") as f:
        _CACHE = json.load(f)
    _CACHE.pop("_meta", None)
    return _CACHE


def is_non_ascii(name):
    """检测字符串是否包含非 ASCII 字符（如中文）。"""
    if not name:
        return False
    return any(ord(c) > 127 for c in name)


def lookup(name):
    """查找中文名对应的英文名候选列表。

    Returns:
        list[str] or None: 候选英文名列表；None 表示未找到。
    """
    m = _load_map()
    # 精确匹配
    if name in m:
        return m[name]
    # 忽略大小写/空格匹配
    name_clean = name.strip().lower()
    for k, v in m.items():
        if k.strip().lower() == name_clean:
            return v
    return None


def suggest(drug, event=None):
    """为非 ASCII 药物名生成 CLI 交互确认。

    Args:
        drug: 原始药物名（可能含非 ASCII）
        event: 关联的事件名（仅用于提示）

    Returns:
        tuple[str, bool]: (确认后的英文名, 是否来自翻译)
        如果用户取消，返回 (None, False)。
    """
    candidates = lookup(drug)
    ev_str = "，事件=%r" % event if event else ""

    if candidates is None:
        print("\n[drug-resolver] 未找到 %r 的英文名映射，请手动输入英文名%s。" % (drug, ev_str))
        print("[drug-resolver] 提示：openFDA 仅支持英文药物名（INN/通用名），如 aspirin、metformin。")
        try:
            eng = input("[drug-resolver] 英文名（回车跳过）: ").strip()
        except (EOFError, KeyboardInterrupt):
            eng = ""
        return (eng if eng else None, False)

    if len(candidates) == 1:
        eng = candidates[0]
        print("\n[drug-resolver] 检测到中文药名 %r → 自动翻译为 %r%s。" % (drug, eng, ev_str))
        print("[drug-resolver] 按回车确认，或输入其他英文名：", end="")
        try:
            extra = input().strip()
        except (EOFError, KeyboardInterrupt):
            extra = ""
        if extra:
            return (extra, False)
        return (eng, True)

    # 多候选：列出菜单让用户选
    print("\n[drug-resolver] 检测到中文药名 %r，请选择对应英文名%s：" % (drug, ev_str))
    for i, eng in enumerate(candidates, 1):
        print("  %d) %s" % (i, eng))
    print("  0) 手动输入其他英文名")
    while True:
        try:
            sel = input("[drug-resolver] 编号 (%d-%d, 默认1): " % (0, len(candidates))).strip()
        except (EOFError, KeyboardInterrupt):
            sel = ""
        if sel == "":
            return (candidates[0], True)
        try:
            idx = int(sel)
        except ValueError:
            print("  请输入数字编号。")
            continue
        if idx == 0:
            try:
                eng = input("[drug-resolver] 英文名: ").strip()
            except (EOFError, KeyboardInterrupt):
                eng = ""
            return (eng if eng else None, False)
        if 1 <= idx <= len(candidates):
            return (candidates[idx - 1], True)
        print("  编号超出范围，请重新输入。")


def resolve(drug, event=None, auto=False):
    """解析药物名（自动翻译非 ASCII 名）。

    Args:
        drug: 原始药物名
        event: 关联事件名（仅用于提示）
        auto: 如果 True，非 ASCII 名有唯一候选时直接翻译（不询问）；
              如果 False，多候选时弹 CLI 编号菜单让用户确认（仅 CLI 环境使用）。

    Returns:
        tuple[str, bool]: (英文名, 是否来自翻译)
    """
    if not drug or not is_non_ascii(drug):
        return (drug, False)
    if auto:
        candidates = lookup(drug)
        if candidates:
            return (candidates[0], True)
        return (drug, False)
    return suggest(drug, event)


def resolve_for_dialog(drug, event=None):
    """对话环境专用解析器（WorkBuddy / 非阻塞）。

    对齐 ct-base §6.2 Triage 四级交互策略：
    - Simple / Middle 路径：始终自动翻译，不弹菜单、不阻塞 input()
    - 仅当 auto=True 时才返回第一个候选，不做任何交互

    Args:
        drug: 原始药物名
        event: 关联事件名（仅用于日志）

    Returns:
        tuple[str, bool]: (英文名, 是否来自翻译)
    """
    if not drug or not is_non_ascii(drug):
        return (drug, False)
    candidates = lookup(drug)
    if candidates:
        return (candidates[0], True)
    return (drug, False)
