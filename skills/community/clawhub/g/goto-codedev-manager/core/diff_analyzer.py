"""把 git 改动解析为结构化变更并按角色归类（Agent 无关、技术栈无关的纯文本分析）。

依据实施思路第九节「需要生成数据库变更草案」的触发线索：新增/改 Entity、新增 Migration、
新增 Repository 等。归类结果供 detect_database_changes 与 orchestrator 的 change_detector 使用。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class DiffAnalysis:
    added: list[str] = field(default_factory=list)
    modified: list[str] = field(default_factory=list)
    deleted: list[str] = field(default_factory=list)
    # 角色归类
    entities: list[str] = field(default_factory=list)
    migrations: list[str] = field(default_factory=list)
    repositories: list[str] = field(default_factory=list)
    controllers: list[str] = field(default_factory=list)
    services: list[str] = field(default_factory=list)
    others: list[str] = field(default_factory=list)

    @property
    def changed_files(self) -> list[str]:
        return [*self.added, *self.modified, *self.deleted]

    @property
    def likely_db_change(self) -> bool:
        """是否可能引发数据库结构变更（实施思路第九节触发规则）。"""
        return bool(self.entities or self.migrations or self.repositories)


def _is_entity(rel: str) -> bool:
    parts = {p.lower() for p in Path(rel).parts}
    name = Path(rel).stem
    if {"entities", "models", "domain"} & parts:
        return True
    return name.endswith("Entity")


def _categorize(analysis: DiffAnalysis, rel: str) -> None:
    name = Path(rel).stem
    parts = Path(rel).parts
    if "Migrations" in parts or name.endswith("ModelSnapshot"):
        analysis.migrations.append(rel)
    elif name.endswith("Repository"):
        analysis.repositories.append(rel)
    elif name.endswith("Controller"):
        analysis.controllers.append(rel)
    elif name.endswith("Service"):
        analysis.services.append(rel)
    elif rel.endswith(".cs") and _is_entity(rel):
        analysis.entities.append(rel)
    else:
        analysis.others.append(rel)


def analyze_porcelain(porcelain: str) -> DiffAnalysis:
    """解析 `git status --porcelain` 输出。"""
    analysis = DiffAnalysis()
    for line in porcelain.splitlines():
        if not line.strip():
            continue
        code = line[:2]
        path = line[3:].strip()
        if " -> " in path:                       # 重命名取新名
            path = path.split(" -> ", 1)[1]
        if "D" in code:
            analysis.deleted.append(path)
        elif "A" in code or "?" in code:
            analysis.added.append(path)
        else:
            analysis.modified.append(path)
        _categorize(analysis, path)
    return analysis


def analyze_files(files: list[str]) -> DiffAnalysis:
    """仅有文件名列表（无状态码）时的归类，统一归入 modified。"""
    analysis = DiffAnalysis()
    for rel in files:
        analysis.modified.append(rel)
        _categorize(analysis, rel)
    return analysis
