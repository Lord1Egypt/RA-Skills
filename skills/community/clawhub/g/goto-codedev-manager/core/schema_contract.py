"""数据库变更交接单 (Schema Contract) 生成器。

落在被开发项目仓库的 `.db-contract/`（实施思路第八节）：
    current-schema.json   当前库结构快照（本期占位，由后续巡检回填）
    pending-changes.json  本次变更 ← 核心交接单，orchestrator/cloudserver 消费
    migration-plan.md     人类可读变更说明
    execution-report.md   执行回填（由 orchestrator/cloudserver 写）

关键：to_unified_schema() 把交接单转成 goto-cloudserver-manager 的 UnifiedSchema dict，
使其 apply_schema 无需改动即可建表（字段类型走 cloudserver 的 _TYPE_MAP）。
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from stacks.base import EntityDef


@dataclass
class SchemaContract:
    feature: str
    database: str
    environment: str = "test"
    changes: list[dict] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # ── 构造 ──────────────────────────────────────────────────────────────
    @classmethod
    def from_entities(
        cls, entities: list["EntityDef"], feature: str, database: str, environment: str = "test"
    ) -> "SchemaContract":
        changes: list[dict] = []
        for ent in entities:
            fields = []
            for f in ent.fields:
                fd: dict = {"name": f.name, "type": f.unified_type, "nullable": f.nullable}
                if f.length:
                    fd["length"] = f.length
                if f.primary_key:
                    fd["primaryKey"] = True
                if f.auto_increment:
                    fd["autoIncrement"] = True
                fields.append(fd)
            changes.append({
                "action": "create_table",
                "table": ent.table,
                "entity": ent.name,
                "source_file": ent.source_file,
                "fields": fields,
                "indexes": [],
            })
        return cls(feature=feature, database=database, environment=environment, changes=changes)

    # ── 序列化 ────────────────────────────────────────────────────────────
    def to_pending_changes(self) -> dict:
        return {
            "feature": self.feature,
            "environment": self.environment,
            "database": self.database,
            "generated_at": self.generated_at,
            "changes": self.changes,
        }

    def to_unified_schema(self) -> dict:
        """转成 cloudserver UnifiedSchema dict（database + tables[].fields[]）。

        统一类型词（bigint/string/datetime...）由 cloudserver SchemaCompiler 编译为
        SQL Server / MySQL / PostgreSQL DDL，本端不拼具体方言。
        """
        tables = []
        for ch in self.changes:
            if ch.get("action") != "create_table":
                continue
            fields = []
            for f in ch.get("fields", []):
                uf: dict = {
                    "name": f["name"],
                    "type": f["type"],
                    "nullable": f.get("nullable", True),
                }
                if f.get("length"):
                    uf["length"] = f["length"]
                if f.get("primaryKey"):
                    uf["primary_key"] = True
                if f.get("autoIncrement"):
                    uf["auto_increment"] = True
                fields.append(uf)
            tables.append({"name": ch["table"], "fields": fields})
        return {"database": self.database, "tables": tables}

    def to_migration_plan_md(self) -> str:
        lines = [
            f"# 数据库变更说明：{self.feature}",
            "",
            f"- 生成时间：{self.generated_at}",
            f"- 目标环境：{self.environment}",
            f"- 数据库：{self.database}",
            f"- 变更数量：{len(self.changes)}",
            "",
        ]
        for ch in self.changes:
            lines.append(f"## 新建表 `{ch['table']}`（实体 {ch.get('entity', '')}）")
            lines.append("")
            lines.append("| 字段 | 类型 | 可空 | 主键 | 自增 |")
            lines.append("|---|---|---|---|---|")
            for f in ch.get("fields", []):
                length = f"({f['length']})" if f.get("length") else ""
                lines.append(
                    f"| {f['name']} | {f['type']}{length} | "
                    f"{'是' if f.get('nullable') else '否'} | "
                    f"{'✓' if f.get('primaryKey') else ''} | "
                    f"{'✓' if f.get('autoIncrement') else ''} |"
                )
            lines.append("")
        return "\n".join(lines)

    # ── 写盘 ──────────────────────────────────────────────────────────────
    def write(self, repo_path: str) -> dict[str, str]:
        """把交接单写入 <repo_path>/.db-contract/，返回写入文件路径映射。"""
        out_dir = Path(repo_path) / ".db-contract"
        out_dir.mkdir(parents=True, exist_ok=True)
        pending = out_dir / "pending-changes.json"
        plan = out_dir / "migration-plan.md"
        pending.write_text(
            json.dumps(self.to_pending_changes(), ensure_ascii=False, indent=2), encoding="utf-8"
        )
        plan.write_text(self.to_migration_plan_md(), encoding="utf-8")
        return {"pending_changes": str(pending), "migration_plan": str(plan)}
