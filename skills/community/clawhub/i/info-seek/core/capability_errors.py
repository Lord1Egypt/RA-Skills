#!/usr/bin/env python3
"""
core/capability_errors.py — 统一外部能力错误类型（M0.2.5）

错误携带 `code` 属性，使 engine_lifecycle.classify（读取 e.code / 消息）能
直接分类（429→quota / 401-403→forbidden / timeout / network / …），
实现"零改动复用生命周期"。
"""

from __future__ import annotations


class CapabilityError(Exception):
    """能力执行错误。code 对齐 engine_lifecycle.classify 的识别语义。"""

    def __init__(self, message: str, code: int = 0, *, cause: BaseException = None):
        super().__init__(message)
        self.code = code          # 0=未知/未安装；429=配额；401/403=认证；见 classify
        self.cause = cause


class ConsentRequired(CapabilityError):
    """针对个人的能力未获合法用途授权。"""

    def __init__(self, cap_name: str):
        super().__init__(
            f"能力 '{cap_name}' 需合法用途授权（requires_consent=true），"
            f"请经合规闸口 grant_consent 后方可运行", code=403)
        self.cap_name = cap_name


class CapabilityUnavailable(CapabilityError):
    """CLI/依赖未安装或不可达（隔离 venv 未配置）。"""

    def __init__(self, cap_name: str, detail: str = ""):
        super().__init__(
            f"能力 '{cap_name}' 不可用：{detail}".strip(), code=0)
        self.cap_name = cap_name
