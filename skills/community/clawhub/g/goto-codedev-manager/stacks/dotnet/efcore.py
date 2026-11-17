""".NET / EF Core 技术栈适配器：实体解析 + Migration 生成 + 测试库落库 + 测试构建。"""

from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING

import structlog

from executor.base import ExecutionResult
from stacks.base import EntityDef, EntityField, StackAdapterBase
from stacks.dotnet import commands

if TYPE_CHECKING:
    from core.config_loader import WorkspaceConfig

logger = structlog.get_logger(__name__)

# 不视为业务实体表的类名后缀（控制器/服务/DTO/上下文等）
_SKIP_SUFFIXES = (
    "Controller", "Service", "Repository", "DbContext", "Context", "Profile",
    "Dto", "DTO", "Request", "Response", "ViewModel", "Handler", "Validator",
    "Configuration", "Options", "Settings", "Extensions", "Builder", "Factory",
)
_COLLECTION_PREFIXES = ("List<", "ICollection<", "IEnumerable<", "HashSet<", "Collection<", "IList<")

# 一个属性：前置 0..n 个特性 + public [virtual/required] <Type> <Name> { get; set; }
_PROP_RE = re.compile(
    r"((?:\s*\[[^\]]*\]\s*)*)"
    r"public\s+(?:virtual\s+|required\s+)?([\w\.\[\]<>?]+)\s+(\w+)\s*\{\s*get;\s*set;\s*\}",
)
_CLASS_RE = re.compile(r"\bclass\s+(\w+)")


def _pluralize(name: str) -> str:
    if name.endswith("y") and name[-2:-1] not in "aeiou":
        return name[:-1] + "ies"
    if name.endswith(("s", "x", "z", "ch", "sh")):
        return name + "es"
    return name + "s"


class EfCoreStackAdapter(StackAdapterBase):
    name = "dotnet"
    migration_tool = "efcore"

    # ── 技术栈探测 ────────────────────────────────────────────────────────
    def detect(self, ws: "WorkspaceConfig") -> bool:
        root = Path(ws.path)
        if not root.exists():
            return False
        return any(root.rglob("*.csproj")) or any(root.glob("*.sln"))

    # ── 实体解析 ──────────────────────────────────────────────────────────
    def extract_entities(self, ws: "WorkspaceConfig", files: list[str]) -> list[EntityDef]:
        root = Path(ws.path)
        entities: list[EntityDef] = []
        for rel in files:
            if not rel.endswith(".cs") or self._is_migration_file(rel):
                continue
            path = root / rel
            if not path.exists():
                continue
            try:
                content = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            entities.extend(self._parse_file(content, rel))
        return entities

    @staticmethod
    def _is_migration_file(rel: str) -> bool:
        parts = Path(rel).parts
        fname = Path(rel).name
        return (
            "Migrations" in parts
            or fname.endswith("ModelSnapshot.cs")
            or fname.endswith(".Designer.cs")
        )

    def _parse_file(self, content: str, source_file: str) -> list[EntityDef]:
        classes = [(m.start(), m.group(1)) for m in _CLASS_RE.finditer(content)]
        if not classes:
            return []
        buckets: dict[str, EntityDef] = {}

        for m in _PROP_RE.finditer(content):
            # 归属到最近的前置 class
            owner = None
            for start, cname in classes:
                if start < m.start():
                    owner = cname
                else:
                    break
            if owner is None or owner.endswith(_SKIP_SUFFIXES):
                continue

            field = self._parse_property(owner, m.group(1), m.group(2), m.group(3))
            if field is None:
                continue
            if owner not in buckets:
                buckets[owner] = EntityDef(name=owner, table=_pluralize(owner), source_file=source_file)
            buckets[owner].fields.append(field)

        return [e for e in buckets.values() if e.fields]

    def _parse_property(self, class_name: str, attrs: str, raw_type: str, prop_name: str) -> EntityField | None:
        raw_type = raw_type.strip()
        # 跳过导航属性（集合 / 指向其他实体的引用类型）
        if any(raw_type.startswith(p) for p in _COLLECTION_PREFIXES):
            return None

        nullable_marker = raw_type.endswith("?")
        base_type = raw_type.rstrip("?")
        if "<" in base_type or ">" in base_type:
            return None  # 泛型/导航，跳过

        unified = self.type_map.get(base_type)
        if unified is None:
            return None  # 未知类型（多为导航属性 / 枚举），MVP 跳过

        is_pk = (
            "[Key]" in attrs
            or prop_name == "Id"
            or prop_name == f"{class_name}Id"
        )
        # 长度：[MaxLength(n)] / [StringLength(n)]
        length = 0
        mlen = re.search(r"\[(?:MaxLength|StringLength)\((\d+)\)\]", attrs)
        if mlen:
            length = int(mlen.group(1))

        # 可空性
        if is_pk:
            nullable = False
        elif nullable_marker:
            nullable = True
        elif "[Required]" in attrs:
            nullable = False
        elif base_type == "string":
            nullable = True
        else:
            nullable = False

        # 自增：整型主键且未显式关闭
        auto_increment = (
            is_pk
            and unified in ("bigint", "int")
            and "DatabaseGeneratedOption.None" not in attrs
        )

        return EntityField(
            name=prop_name,
            unified_type=unified,
            source_type=base_type,
            length=length,
            nullable=nullable,
            primary_key=is_pk,
            auto_increment=auto_increment,
        )

    # ── Migration / 测试 / 构建 ──────────────────────────────────────────
    def generate_migration(self, ws: "WorkspaceConfig", name: str) -> ExecutionResult:
        return self._executor.execute(commands.migration_add(ws, name), cwd=ws.repo_path, timeout=600)

    def apply_migration_local(self, ws: "WorkspaceConfig") -> ExecutionResult:
        if not ws.test_db_connection:
            return ExecutionResult(
                stderr="拒绝执行：workspace 未配置 test_db_connection（测试库连接串）。"
                       "为避免误连生产库，本动作必须显式提供测试库连接。",
                exit_code=2,
            )
        return self._executor.execute(commands.database_update(ws), cwd=ws.repo_path, timeout=600)

    def run_tests(self, ws: "WorkspaceConfig") -> ExecutionResult:
        return self._executor.execute(commands.test(ws), cwd=ws.repo_path, timeout=1800)

    def run_build(self, ws: "WorkspaceConfig") -> ExecutionResult:
        return self._executor.execute(commands.build(ws), cwd=ws.repo_path, timeout=900)
