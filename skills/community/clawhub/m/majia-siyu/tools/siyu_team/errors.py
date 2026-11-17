"""私域专家团统一异常层级。

所有业务异常都应是 :class:`SiyuBaseError` 的子类，上层（CLI / Skill 入口）
按类型分类处理，不再逐个捕获原生异常。
"""
from __future__ import annotations

from typing import Any


class SiyuBaseError(Exception):
    """私域专家团业务异常基类。"""


class ComplianceBlockedError(SiyuBaseError):
    """合规红线硬拦：方案不得交付。

    ``flags`` 保存命中的合规 flag，``details`` 保存逐条说明，
    供上层给出可解释的拦截原因。
    """

    def __init__(
        self,
        message: str = "命中合规红线，方案不得交付",
        *,
        flags: tuple[str, ...] = (),
        details: tuple[dict[str, Any], ...] = (),
    ) -> None:
        super().__init__(message)
        self.flags = flags
        self.details = details
