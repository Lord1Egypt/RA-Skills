"""SourceRegistry + 基础 SourceAdapter（spec §3.2, §3.3, §6.1）。

职责：
- SourceRegistry：管理多个 SourceRoot，持久化到 .memoryguard/config*.json
- SourceAdapter 契约：detect/inventory/read/normalize_hint/explain
- ProjectDirectoryAdapter：项目目录默认自动授权
- SelectedDirectoryAdapter：用户添加的文件夹
- SelectedFileAdapter：用户添加的单文件
- ObsidianVaultAdapter：Obsidian Vault（spec §3.2）

安全约束（spec §3.2, §12）：
- 每个 SourceRoot 独立 canonical containment
- 默认不跟随符号链接
- 外部绝对路径写入 config.local.json
- 扫描有文件数/大小/深度/耗时预算
- 未授权根目录零读取
"""

from __future__ import annotations

import fnmatch
import json
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .schema_v3 import (
    CandidateStatus, CoverageEntry, CoverageLedger, CoverageStatus,
    SourceObject, SourceRoot, SourceRootType, SourceSnapshot,
    normalize_rel_path, stable_hash, _now_iso,
)


# ---------------------------------------------------------------------------
# 扫描预算（spec §3.2 安全约束）
# ---------------------------------------------------------------------------


@dataclass
class ScanBudget:
    """扫描预算，防止失控。"""
    max_files: int = 50000
    max_total_size: int = 500 * 1024 * 1024  # 500MB
    max_single_file: int = 10 * 1024 * 1024  # 10MB
    max_depth: int = 20
    timeout_seconds: int = 120


# ---------------------------------------------------------------------------
# 支持的文件类型
# ---------------------------------------------------------------------------

TEXT_EXTS = {".md", ".markdown", ".txt", ".json", ".jsonl", ".rst", ".yaml", ".yml", ".toml"}
INSTRUCTION_FILES = {"AGENTS.md", "CLAUDE.md", "CLAUDE.local.md", "GEMINI.md", "CODEBUDDY.md",
                     ".cursorrules", ".windsurfrules", "copilot-instructions.md"}
TEXT_MEDIA_TYPES = {
    ".md": "text/markdown", ".markdown": "text/markdown",
    ".txt": "text/plain", ".json": "application/json",
    ".jsonl": "application/x-jsonlines", ".rst": "text/x-rst",
    ".yaml": "application/yaml", ".yml": "application/yaml",
    ".toml": "application/toml",
}


# ---------------------------------------------------------------------------
# SourceAdapter 契约（spec §6.1）
# ---------------------------------------------------------------------------


@dataclass
class DetectionResult:
    """detect() 返回。"""
    applicable: bool
    confidence: float
    notes: str = ""


@dataclass
class AdapterCapability:
    """explain() 返回。"""
    adapter_name: str
    supported_features: list[str]
    unsupported_features: list[str]
    notes: str = ""


class SourceAdapter:
    """SourceAdapter 基类契约（spec §6.1）。"""

    def detect(self, root: Path) -> DetectionResult:
        raise NotImplementedError

    def inventory(self, root: Path, budget: ScanBudget
                  ) -> tuple[list[Path], list[CoverageEntry]]:
        """返回 (候选路径列表, 截断 entries)（不读内容）。

        v3.1 §11 第 5 项：截断/权限失败必须产生 ledger entry。
        """
        raise NotImplementedError

    def read(self, candidate: Path, root: Path) -> tuple[SourceObject | None, CoverageEntry]:
        """读取单个候选，返回 (SourceObject 或 None, CoverageEntry)。
        SourceObject 为 None 时，CoverageEntry 记录跳过原因。"""
        raise NotImplementedError

    def normalize_hint(self, source: SourceObject) -> dict[str, Any]:
        return {}

    def explain(self) -> AdapterCapability:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# DirectoryAdapter（通用目录适配器）
# ---------------------------------------------------------------------------


class DirectoryAdapter(SourceAdapter):
    """通用目录适配器：项目目录和自选文件夹共用。"""

    def __init__(self, source_root: SourceRoot):
        self.root = source_root

    def detect(self, root: Path) -> DetectionResult:
        if root.is_dir():
            return DetectionResult(applicable=True, confidence=1.0)
        return DetectionResult(applicable=False, confidence=1.0, notes="not a directory")

    def inventory(self, root: Path, budget: ScanBudget
                  ) -> tuple[list[Path], list[CoverageEntry]]:
        """v3.1 §11 第 5 项：预算截断/权限失败必须产生 ledger entry。

        返回 (candidates, truncation_entries)：
        - candidates: 实际准备 read 的路径
        - truncation_entries: 因预算/权限/超大单文件被截断的 CoverageEntry
          这些 entry 必须进入 CoverageLedger，否则 unaccounted_count 假性为 0。
        """
        candidates: list[Path] = []
        truncation_entries: list[CoverageEntry] = []
        total_size = 0
        start = time.time()
        root_id = self.root.root_id

        def _truncated(rel: str, reason: str, status: CandidateStatus) -> None:
            truncation_entries.append(CoverageEntry(
                source_root_id=root_id, relative_path=rel,
                status=status, reason=reason,
            ))

        if not self.root.recursive:
            for p in root.iterdir():
                rel = str(p.relative_to(root)).replace("\\", "/")
                if len(candidates) >= budget.max_files:
                    _truncated(rel, "max_files budget exhausted",
                               CandidateStatus.SKIPPED_BY_POLICY)
                    break
                if time.time() - start > budget.timeout_seconds:
                    _truncated(rel, "timeout budget exhausted",
                               CandidateStatus.SKIPPED_BY_POLICY)
                    break
                if p.is_file():
                    candidates.append(p)
            return candidates, truncation_entries

        for dirpath, dirnames, filenames in os.walk(root, followlinks=self.root.follow_symlinks):
            depth = len(Path(dirpath).relative_to(root).parts)
            if depth >= budget.max_depth:
                dirnames[:] = []
                _truncated(str(Path(dirpath).relative_to(root)).replace("\\", "/") + "/",
                           "max_depth budget exhausted", CandidateStatus.SKIPPED_BY_POLICY)
                continue
            # 应用 exclude
            rel_dir = str(Path(dirpath).relative_to(root)).replace("\\", "/")
            if self._excluded(rel_dir + "/"):
                dirnames[:] = []
                continue
            # 过滤目录
            dirnames[:] = [d for d in dirnames if not self._excluded(rel_dir + "/" + d + "/")]
            for fname in filenames:
                p = Path(dirpath) / fname
                rel = str(p.relative_to(root)).replace("\\", "/")
                if self._excluded(rel):
                    continue
                if not self._included(rel):
                    continue
                try:
                    size = p.stat().st_size
                except OSError as e:
                    _truncated(rel, f"stat failed: {e}", CandidateStatus.UNREADABLE)
                    continue
                if size > budget.max_single_file:
                    _truncated(rel, f"file too large ({size} > {budget.max_single_file})",
                               CandidateStatus.SKIPPED_BY_POLICY)
                    continue
                if total_size + size > budget.max_total_size:
                    _truncated(rel, "max_total_size budget exhausted",
                               CandidateStatus.SKIPPED_BY_POLICY)
                    return candidates, truncation_entries
                total_size += size
                candidates.append(p)
                if len(candidates) >= budget.max_files:
                    _truncated(rel, "max_files budget reached",
                               CandidateStatus.SKIPPED_BY_POLICY)
                    return candidates, truncation_entries
                if time.time() - start > budget.timeout_seconds:
                    _truncated(rel, "timeout budget exhausted",
                               CandidateStatus.SKIPPED_BY_POLICY)
                    return candidates, truncation_entries
        return candidates, truncation_entries

    def read(self, candidate: Path, root: Path) -> tuple[SourceObject | None, CoverageEntry]:
        rel = str(candidate.relative_to(root)).replace("\\", "/")
        root_id = self.root.root_id
        source_object_id = stable_hash(root_id, normalize_rel_path(rel))
        # v3.1 §1.5 P0：canonical containment + 符号链接防护
        import os as _os
        try:
            resolved_root = root.resolve()
            resolved_candidate = candidate.resolve()
            resolved_candidate.relative_to(resolved_root)
        except (ValueError, OSError) as e:
            entry = CoverageEntry(
                source_root_id=root_id, relative_path=rel,
                status=CandidateStatus.UNREADABLE,
                reason=f"containment violation: {e}",
            )
            return None, entry
        # 符号链接目标必须在根内
        if candidate.is_symlink():
            try:
                target = Path(_os.readlink(candidate)).resolve()
                target.relative_to(resolved_root)
            except (ValueError, OSError) as e:
                entry = CoverageEntry(
                    source_root_id=root_id, relative_path=rel,
                    status=CandidateStatus.UNREADABLE,
                    reason=f"symlink escapes root: {e}",
                )
                return None, entry
        try:
            size = candidate.stat().st_size
        except OSError as e:
            entry = CoverageEntry(
                source_root_id=root_id, relative_path=rel,
                status=CandidateStatus.UNREADABLE, reason=str(e),
            )
            return None, entry
        ext = candidate.suffix.lower()
        if ext not in TEXT_EXTS and candidate.name not in INSTRUCTION_FILES:
            entry = CoverageEntry(
                source_root_id=root_id, relative_path=rel,
                status=CandidateStatus.UNSUPPORTED, reason=f"ext {ext}",
                size=size, media_type="application/octet-stream",
            )
            return None, entry
        media_type = TEXT_MEDIA_TYPES.get(ext, "text/plain")
        try:
            content = candidate.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            entry = CoverageEntry(
                source_root_id=root_id, relative_path=rel,
                status=CandidateStatus.UNREADABLE, reason=str(e),
                size=size, media_type=media_type,
            )
            return None, entry
        content_hash = stable_hash(content)
        obj = SourceObject(
            source_object_id=source_object_id, source_root_id=root_id,
            relative_path=rel, content_hash=content_hash,
            media_type=media_type, read_status="read", captured_at=_now_iso(),
        )
        entry = CoverageEntry(
            source_root_id=root_id, relative_path=rel,
            status=CandidateStatus.READ, size=size, media_type=media_type,
        )
        return obj, entry

    def _included(self, rel: str) -> bool:
        """v3.1 §11 第 8 项：Obsidian 根层 Markdown 必须被 inventory。

        fnmatch 把 `**` 当作 `*`，所以 `**/*.md` 不匹配根层 `root_note.md`。
        这里特殊处理：`**/*.ext` 同时匹配 `name.ext`（根层）和 `path/name.ext`（嵌套）。
        """
        if not self.root.include:
            return True
        for pat in self.root.include:
            if fnmatch.fnmatch(rel, pat):
                return True
            # v3.1 §11 第 8 项：**/*.ext 同时匹配根层
            if pat.startswith("**/"):
                root_pat = pat[3:]
                if fnmatch.fnmatch(rel, root_pat):
                    return True
        return False

    def _excluded(self, rel: str) -> bool:
        for pat in self.root.exclude:
            if fnmatch.fnmatch(rel, pat):
                return True
        return False

    def explain(self) -> AdapterCapability:
        return AdapterCapability(
            adapter_name="DirectoryAdapter",
            supported_features=["detect", "inventory", "read"],
            unsupported_features=[],
            notes="通用目录扫描，支持 include/exclude glob",
        )


class ProjectDirectoryAdapter(DirectoryAdapter):
    """项目目录：默认自动授权，scope=project。"""
    pass


class SelectedDirectoryAdapter(DirectoryAdapter):
    """用户添加的文件夹：需显式授权。"""
    pass


class SelectedFileAdapter(SourceAdapter):
    """单文件适配器。"""

    def __init__(self, source_root: SourceRoot):
        self.root = source_root

    def detect(self, root: Path) -> DetectionResult:
        return DetectionResult(applicable=root.is_file(), confidence=1.0)

    def inventory(self, root: Path, budget: ScanBudget
                  ) -> tuple[list[Path], list[CoverageEntry]]:
        return ([root] if root.is_file() else [], [])

    def read(self, candidate: Path, root: Path) -> tuple[SourceObject | None, CoverageEntry]:
        rel = candidate.name
        root_id = self.root.root_id
        source_object_id = stable_hash(root_id, normalize_rel_path(rel))
        try:
            size = candidate.stat().st_size
            content = candidate.read_text(encoding="utf-8")
        except OSError as e:
            return None, CoverageEntry(
                source_root_id=root_id, relative_path=rel,
                status=CandidateStatus.UNREADABLE, reason=str(e))
        ext = candidate.suffix.lower()
        media_type = TEXT_MEDIA_TYPES.get(ext, "text/plain")
        obj = SourceObject(
            source_object_id=source_object_id, source_root_id=root_id,
            relative_path=rel, content_hash=stable_hash(content),
            media_type=media_type, read_status="read", captured_at=_now_iso(),
        )
        entry = CoverageEntry(
            source_root_id=root_id, relative_path=rel,
            status=CandidateStatus.READ, size=size, media_type=media_type,
        )
        return obj, entry

    def explain(self) -> AdapterCapability:
        return AdapterCapability(
            adapter_name="SelectedFileAdapter",
            supported_features=["detect", "inventory", "read"],
            unsupported_features=[],
        )


class ObsidianVaultAdapter(DirectoryAdapter):
    """Obsidian Vault 适配器（spec §3.2）。

    默认排除 .obsidian/、.trash/、.git/，包含 *.md/*.canvas/*.base。
    不执行插件、公式、远程 URL。
    """
    def __init__(self, source_root: SourceRoot):
        super().__init__(source_root)
        if not source_root.exclude:
            source_root.exclude = [".obsidian/**", ".trash/**", ".git/**"]
        if not source_root.include:
            source_root.include = ["**/*.md", "**/*.canvas", "**/*.base", "**/*.png", "**/*.jpg"]

    def detect(self, root: Path) -> DetectionResult:
        if not root.is_dir():
            return DetectionResult(applicable=False, confidence=1.0)
        # 启发式：存在 .obsidian/ 目录
        is_vault = (root / ".obsidian").is_dir()
        return DetectionResult(
            applicable=True, confidence=0.9 if is_vault else 0.5,
            notes="obsidian_vault detected" if is_vault else "fallback to generic markdown dir",
        )

    def explain(self) -> AdapterCapability:
        return AdapterCapability(
            adapter_name="ObsidianVaultAdapter",
            supported_features=["detect", "inventory", "read"],
            unsupported_features=["plugins", "base_formulas", "remote_urls"],
            notes="仅扫描 Markdown/Canvas/Base/附件；不执行插件或公式",
        )


# ---------------------------------------------------------------------------
# SourceRegistry
# ---------------------------------------------------------------------------


def _make_adapter(root: SourceRoot) -> SourceAdapter:
    """根据 SourceRootType 创建适配器。"""
    if root.type == SourceRootType.PROJECT_DIRECTORY:
        return ProjectDirectoryAdapter(root)
    if root.type == SourceRootType.SELECTED_DIRECTORY:
        return SelectedDirectoryAdapter(root)
    if root.type == SourceRootType.SELECTED_FILE:
        return SelectedFileAdapter(root)
    if root.type == SourceRootType.OBSIDIAN_VAULT:
        return ObsidianVaultAdapter(root)
    raise ValueError(f"unknown SourceRootType: {root.type}")


class SourceRegistry:
    """管理多个 SourceRoot，持久化到 .memoryguard/config*.json。"""

    def __init__(self, workspace: str | Path):
        self.workspace = Path(workspace).resolve()
        self.mg_dir = self.workspace / ".memoryguard"
        self.config_path = self.mg_dir / "config.json"
        self.config_local_path = self.mg_dir / "config.local.json"
        self.roots: dict[str, SourceRoot] = {}
        self._load()

    def _load(self) -> None:
        self.mg_dir.mkdir(parents=True, exist_ok=True)
        for path in (self.config_path, self.config_local_path):
            if path.exists():
                try:
                    data = json.loads(path.read_text(encoding="utf-8"))
                    for r in data.get("sources", []):
                        root = SourceRoot.from_dict(r)
                        self.roots[root.root_id] = root
                except (OSError, json.JSONDecodeError):
                    continue
        # 自动确保项目目录存在
        project_id = "src-project-default"
        if project_id not in self.roots:
            self.roots[project_id] = SourceRoot(
                root_id=project_id, type=SourceRootType.PROJECT_DIRECTORY,
                display_name="项目目录", path=str(self.workspace),
                scope="project", authorized_at=_now_iso(),
                include=[], exclude=[".memoryguard/**", ".git/**", "node_modules/**", "__pycache__/**"],
            )

    def _save(self) -> None:
        self.mg_dir.mkdir(parents=True, exist_ok=True)
        shared_roots: list[dict[str, Any]] = []
        local_roots: list[dict[str, Any]] = []
        for root in self.roots.values():
            if root.scope == "project":
                shared_roots.append(root.to_dict())
            else:
                local_roots.append(root.to_dict())
        self.config_path.write_text(
            json.dumps({"sources": shared_roots}, ensure_ascii=False, indent=2),
            encoding="utf-8")
        self.config_local_path.write_text(
            json.dumps({"sources": local_roots}, ensure_ascii=False, indent=2),
            encoding="utf-8")

    def list_sources(self) -> list[SourceRoot]:
        return [r for r in self.roots.values() if r.enabled]

    def get(self, root_id: str) -> SourceRoot | None:
        return self.roots.get(root_id)

    def add(self, path: str, root_type: SourceRootType, display_name: str = "",
            scope: str = "user", include: list[str] | None = None,
            exclude: list[str] | None = None) -> SourceRoot:
        """添加 SourceRoot。path 必须存在。"""
        p = Path(path).resolve()
        if not p.exists():
            raise FileNotFoundError(f"path not found: {p}")
        root_id = "src-" + stable_hash(str(p), root_type.value)
        if root_id in self.roots:
            return self.roots[root_id]
        root = SourceRoot(
            root_id=root_id, type=root_type,
            display_name=display_name or p.name, path=str(p),
            scope=scope, authorized_at=_now_iso(),
            include=include or [], exclude=exclude or [],
        )
        # v3.1 §11 第 8 项：ObsidianVaultAdapter 默认 include 必须持久化到 root
        if root_type == SourceRootType.OBSIDIAN_VAULT:
            if not root.include:
                root.include = ["**/*.md", "**/*.canvas", "**/*.base", "**/*.png", "**/*.jpg"]
            if not root.exclude:
                root.exclude = [".obsidian/**", ".trash/**", ".git/**"]
        self.roots[root_id] = root
        self._save()
        return root

    def remove(self, root_id: str) -> bool:
        if root_id == "src-project-default":
            return False  # 项目目录不可删除
        if root_id in self.roots:
            del self.roots[root_id]
            self._save()
            return True
        return False

    def preview(self, path: str, root_type: SourceRootType) -> dict[str, Any]:
        """预览：不写配置，返回预计文件数和排除规则。"""
        p = Path(path).resolve()
        if not p.exists():
            return {"error": "path not found"}
        root = SourceRoot(
            root_id="preview", type=root_type, display_name=p.name,
            path=str(p), scope="user",
            include=[] if root_type != SourceRootType.OBSIDIAN_VAULT else ["**/*.md"],
            exclude=[".git/**", ".obsidian/**"] if root_type == SourceRootType.OBSIDIAN_VAULT else [".git/**"],
        )
        adapter = _make_adapter(root)
        candidates, truncation = adapter.inventory(p, ScanBudget(max_files=1000, timeout_seconds=10))
        return {
            "path": str(p),
            "type": root_type.value,
            "estimated_files": len(candidates),
            "truncated_count": len(truncation),
            "include": root.include,
            "exclude": root.exclude,
        }

    def scan(self, budget: ScanBudget | None = None) -> SourceSnapshot:
        """扫描所有已启用的 SourceRoot，返回快照 + 覆盖率账本。

        v3.1 §11 第 5 项：inventory 返回的 truncation_entries 必须并入 CoverageLedger，
        否则被预算截断的文件会变成 unaccounted 假性 0。
        """
        budget = budget or ScanBudget()
        snapshot_id = "snap-" + stable_hash(_now_iso(), str(self.workspace))
        source_objects: list[SourceObject] = []
        entries: list[CoverageEntry] = []
        for root in self.list_sources():
            adapter = _make_adapter(root)
            root_path = Path(root.path)
            if not root_path.exists():
                entries.append(CoverageEntry(
                    source_root_id=root.root_id, relative_path="",
                    status=CandidateStatus.UNREADABLE, reason="root path missing",
                ))
                continue
            candidates, truncation = adapter.inventory(root_path, budget)
            # v3.1 §11：截断 entries 必须进入账本
            entries.extend(truncation)
            for cand in candidates:
                obj, entry = adapter.read(cand, root_path)
                entries.append(entry)
                if obj is not None:
                    source_objects.append(obj)
        coverage = CoverageLedger(source_snapshot_id=snapshot_id, entries=entries)
        return SourceSnapshot(
            snapshot_id=snapshot_id, created_at=_now_iso(),
            source_objects=source_objects, coverage=coverage,
        )
