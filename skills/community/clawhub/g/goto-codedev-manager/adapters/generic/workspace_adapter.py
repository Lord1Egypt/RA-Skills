"""通用工作区适配器（兜底，priority 最低）。

适用于任何 IDE（Cursor / Lingma / Qoder / JetBrains 等）：IDE 自身写代码，本 Skill 只读
项目工作区与 Git Diff 判断开发进度。assign_coding_task 返回 manual 占位。
这是「谁修改了代码不重要」原则的最小实现，也是所有 CLI 适配器都不可用时的最终回落。
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from adapters.base import CodingAgentAdapter, TaskHandle

if TYPE_CHECKING:
    from core.config_loader import WorkspaceConfig


class WorkspaceAdapter(CodingAgentAdapter):
    name = "generic"
    type = "workspace"

    def is_available(self) -> bool:
        return True

    def assign_coding_task(self, ws: "WorkspaceConfig", prompt: str, timeout: int = 1800) -> TaskHandle:
        return TaskHandle(
            id=f"{self.name}-{uuid.uuid4().hex[:8]}",
            agent=self.name,
            status="manual",
            output=(
                f"[{self.name}] 该工具无可用 CLI，需在 IDE 中人工/外部完成开发。"
                f"完成后本 Skill 通过 Git Diff 读取结果。\n待办任务：\n{prompt}"
            ),
        )
