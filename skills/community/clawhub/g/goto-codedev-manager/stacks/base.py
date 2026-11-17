"""技术栈适配器抽象基类与统一实体数据结构。

与 adapters/（编程工具轴）正交：stacks/ 解决「怎么识别实体、怎么生成 Migration、怎么跑测试构建」，
与代码由哪个 IDE/Agent 写出无关。新增后端技术栈只需在 stacks/<name>/ 实现本基类。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from executor.base import ExecutionResult
from executor.local_executor import LocalExecutor

if TYPE_CHECKING:
    from core.config_loader import WorkspaceConfig


@dataclass
class EntityField:
    name: str
    unified_type: str                 # 统一类型词：bigint/string/datetime...（对齐 cloudserver SchemaCompiler）
    source_type: str = ""             # 源语言类型，如 C# 的 long/string
    length: int = 0
    nullable: bool = True
    primary_key: bool = False
    auto_increment: bool = False


@dataclass
class EntityDef:
    name: str                         # 实体类名，如 PlanTemplate
    table: str                        # 推断表名，如 PlanTemplates
    fields: list[EntityField] = field(default_factory=list)
    source_file: str = ""


class StackAdapterBase(ABC):
    """所有技术栈适配器的统一接口。"""

    name: str = "base"
    migration_tool: str = ""

    def __init__(self, stack_config: dict | None = None, executor: LocalExecutor | None = None) -> None:
        self._config = stack_config or {}
        self._executor = executor or LocalExecutor()

    @property
    def type_map(self) -> dict[str, str]:
        return self._config.get("type_map", {})

    @abstractmethod
    def detect(self, ws: "WorkspaceConfig") -> bool:
        """判断工作区是否属于本技术栈。"""

    @abstractmethod
    def extract_entities(self, ws: "WorkspaceConfig", files: list[str]) -> list[EntityDef]:
        """从给定（已变更的）源文件解析实体定义。"""

    @abstractmethod
    def generate_migration(self, ws: "WorkspaceConfig", name: str) -> ExecutionResult:
        """生成 Migration，写入仓库。"""

    @abstractmethod
    def apply_migration_local(self, ws: "WorkspaceConfig") -> ExecutionResult:
        """在本地/测试库执行 Migration（必须显式测试库连接，禁止生产库）。"""

    @abstractmethod
    def run_tests(self, ws: "WorkspaceConfig") -> ExecutionResult:
        ...

    @abstractmethod
    def run_build(self, ws: "WorkspaceConfig") -> ExecutionResult:
        ...
