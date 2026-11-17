#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""任务类型字典的加载与归一（类型字典在执行层的入口）。

为什么需要这个模块
------------------
类型字典本体是同目录下的 `type_registry.json`（标准名 ↔ 别名/关键词映射），
但 JSON 文件不能被 `import`。`executor.py` 从一开始就按
`from type_registry import load_registry, normalize_type` 这套接口写，
却始终没有对应的 `.py` 文件，于是那行 import 每次都抛 `ModuleNotFoundError`，
被外层 except 静默吞掉——执行引擎的「查表代替猜」其实从未真正生效，
一路退化成 `_EXEC_ALIASES` 直匹配。本模块补齐这套接口，把字典真正接上。

语义与 `conversation._load_registry()` 保持一致（同名标准、同样降级策略），
但不 import conversation，避免与 `conversation → executor` 形成循环依赖。

设计红线（与技能整体一致）：纯标准库、只读同目录 JSON、不联网、不读密钥；
字典缺失或损坏时一律降级为空字典，绝不抛异常打断任务执行。
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

# 字典文件与本模块同目录（脚本式 import 依赖，故用 __file__ 定位而非相对导入）
REGISTRY_PATH = Path(__file__).resolve().parent / "type_registry.json"


def load_registry(path: Optional[Path] = None) -> dict:
    """读取类型字典，返回「标准名 → 别名列表」映射。

    文件缺失 / JSON 损坏 / 结构异常时返回空字典，让上层自然退化为直匹配，
    与既有容错行为一致——字典是增强项，不是运行前提。
    """
    registry_path = Path(path) if path is not None else REGISTRY_PATH
    try:
        with open(registry_path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):  # FileNotFoundError / 解码失败 / JSON 损坏
        return {}
    if not isinstance(data, dict):
        return {}
    types = data.get("types")
    if not isinstance(types, dict):
        return {}
    # 只保留「值确实是列表」的条目，脏数据不往外传
    return {
        str(std): [str(a) for a in aliases]
        for std, aliases in types.items()
        if isinstance(aliases, (list, tuple))
    }


def normalize_type(task_type: str, registry: Optional[dict] = None) -> str:
    """把用户给的类型串归一到字典里的标准名；认不出就原样返回（去首尾空白）。

    匹配优先级刻意保守，避免把不相关的任务硬塞进某个类型：
    ① 已经是标准名 → 直接用；
    ② 与某个别名精确相等（忽略大小写与首尾空白）→ 归到该别名所属标准名；
    ③ 都不命中 → 返回原串，交给上层继续走别名兜底或判为全新类型。

    这里**不做子串模糊匹配**：模糊匹配留给 `conversation._detect_type`，
    因为执行层的输入通常是明确的类型名，宁可漏归一也不要错归一。
    """
    text = (task_type or "").strip()
    if not text:
        return text
    reg = registry if isinstance(registry, dict) else load_registry()
    if not reg:
        return text
    if text in reg:
        return text
    lowered = text.lower()
    for standard, aliases in reg.items():
        if lowered == standard.lower():
            return standard
        for alias in aliases:
            if lowered == alias.strip().lower():
                return standard
    return text
