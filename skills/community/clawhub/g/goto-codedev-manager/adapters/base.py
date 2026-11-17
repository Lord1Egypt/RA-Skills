"""编程 Agent / IDE 适配器统一基类。

设计原则（见《goto-codedev-manager 多编程工具适配设计思路》第三节）：
基类只抽象**各 Agent 之间真正不同**的部分——下达任务 / 读进度 / 读工作区。
跨工具通用的「变更分析、Migration、测试构建」不放进适配器，由 core/ + stacks/ 统一完成。
因此「谁修改了代码」对上层透明，codedev-manager 始终通过项目结构 + Git Diff 理解开发进度。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from executor.local_executor import LocalExecutor

if TYPE_CHECKING:
    from core.config_loader import WorkspaceConfig


@dataclass
class ProjectContext:
    branch: str = ""
    changed_files: list[str] = field(default_factory=list)
    stack: str = ""
    summary: str = ""


@dataclass
class TaskHandle:
    id: str
    agent: str
    status: str = "submitted"        # submitted / running / completed / failed / manual
    output: str = ""
    error: str = ""

    @property
    def is_manual(self) -> bool:
        return self.status == "manual"


@dataclass
class TaskProgress:
    status: str
    output: str = ""
    error: str = ""


class CodingAgentAdapter(ABC):
    """所有编程 Agent / IDE 适配器的统一接口。"""

    #: 适配器名称，对应 adapters.yaml 的 key
    name: str = "base"
    #: cli / workspace（workspace 仅用于 generic 兜底）
    type: str = "workspace"

    def __init__(self, config: dict | None = None, executor: LocalExecutor | None = None) -> None:
        self._config = config or {}
        self._executor = executor or LocalExecutor()

    # ── 各 Agent 不同的能力 ───────────────────────────────────────────────
    @abstractmethod
    def is_available(self) -> bool:
        """CLI 是否已安装 / 工作区适配器是否可用。"""

    @abstractmethod
    def assign_coding_task(self, ws: "WorkspaceConfig", prompt: str, timeout: int = 1800) -> TaskHandle:
        """下达开发任务。

        - cli 类适配器：shell-out 对应 CLI 读取项目数据并下达任务指令。
        - workspace 仅作为最终兜底：返回 status='manual' 占位，本 Skill 随后读 Git Diff。
        """

    # ── 跨 Agent 通用的默认实现（可覆盖）─────────────────────────────────
    def open_workspace(self, ws: "WorkspaceConfig") -> None:
        """默认无副作用；IDE 适配器可覆盖为打开工作区。"""

    def read_project_context(self, ws: "WorkspaceConfig") -> ProjectContext:
        branch = self._git(ws, "git rev-parse --abbrev-ref HEAD").stdout.strip()
        changed = self.read_changed_files(ws)
        return ProjectContext(branch=branch, changed_files=changed, stack=ws.stack)

    def get_task_progress(self, handle: TaskHandle) -> TaskProgress:
        return TaskProgress(status=handle.status, output=handle.output, error=handle.error)

    def read_git_diff(self, ws: "WorkspaceConfig", staged: bool = False) -> str:
        flag = "--cached" if staged else ""
        return self._git(ws, f"git diff {flag}".strip()).stdout

    def read_changed_files(self, ws: "WorkspaceConfig") -> list[str]:
        """已改动（含未跟踪）文件名列表。"""
        out = self._git(ws, "git status --porcelain").stdout
        files: list[str] = []
        for line in out.splitlines():
            if not line.strip():
                continue
            # 格式： XY <path>  /  XY <old> -> <new>
            path = line[3:].strip()
            if " -> " in path:
                path = path.split(" -> ", 1)[1]
            files.append(path)
        return files

    # ── 辅助 ─────────────────────────────────────────────────────────────
    def _git(self, ws: "WorkspaceConfig", command: str, timeout: int = 60):
        return self._executor.execute(command, cwd=ws.repo_path, timeout=timeout)
