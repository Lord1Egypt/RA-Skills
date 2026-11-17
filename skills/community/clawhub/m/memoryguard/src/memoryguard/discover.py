"""工作区发现：识别 Agent 指令、Skills、记忆、本地 RAG 源（spec §2, §5.1）。

只读，无副作用。扫描范围必须由用户工作区限定，禁止默认扫描整个用户目录（spec §1.3, §10）。

安全约束（spec §10）:
- 处理符号链接、路径穿越、超大文件、二进制文件
- 不可见范围必须显式记录，不能静默当作不存在
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

from .schema import (
    AGR,
    AGRType,
    Ref,
    RefRelation,
    Scope,
    Sensitivity,
    sha256_file,
    sha256_text,
    stable_id,
)


# ---------------------------------------------------------------------------
# 发现配置
# ---------------------------------------------------------------------------

# 通用 Agent 指令文件（spec §2 治理表面1）
INSTRUCTION_FILES = (
    "AGENTS.md",
    "CLAUDE.md",
    "CODEBUDDY.md",
    "GEMINI.md",
    ".cursorrules",
    "copilot-instructions.md",
)

# Skill 目录约定（R3: .agents/skills/ 跨客户端兼容）
SKILL_DIRS = (".agents/skills", ".claude/skills", ".cursor/skills")

# 本地记忆/RAG 常见目录名（启发式，非穷举）
MEMORY_DIRS = ("memory", "memories", ".memory", "context")
RAG_DIRS = ("docs", "knowledge", "rag", "corpus", "data")

# 文本类扩展（首期聚焦 Markdown/纯文本/JSON，spec §2.2）
TEXT_EXTS = (".md", ".txt", ".json", ".jsonl", ".markdown", ".rst")

# 跳过目录（避免扫描器成为新攻击面或陷入无限递归）
SKIP_DIRS = {
    ".git",
    ".memoryguard",
    "graphify-out",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "build",
    "dist",
    ".pytest_cache",
}

# 单文件大小上限（5MB），超过则标记不可见而非全量读取
MAX_FILE_BYTES = 5 * 1024 * 1024


# ---------------------------------------------------------------------------
# 发现结果
# ---------------------------------------------------------------------------


@dataclass
class DiscoveryResult:
    """一次工作区发现的结果。"""

    workspace: Path
    agrs: list[AGR] = field(default_factory=list)
    invisible: list[dict] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.agrs)


# ---------------------------------------------------------------------------
# 安全工具
# ---------------------------------------------------------------------------


def _is_within_workspace(path: Path, workspace: Path) -> bool:
    """防止路径穿越：解析后路径必须在工作区内。"""
    try:
        path.resolve().relative_to(workspace.resolve())
        return True
    except ValueError:
        return False


def _is_symlink_safe(path: Path, workspace: Path) -> bool:
    """符号链接：仅当目标在工作区内才跟随（spec §10）。"""
    if not path.is_symlink():
        return True
    try:
        target = path.resolve()
        return _is_within_workspace(target, workspace)
    except (OSError, RuntimeError):
        return False


def _is_binary(path: Path) -> bool:
    """简单二进制检测：读取前 2KB，检查 NUL 字节。"""
    try:
        with path.open("rb") as f:
            chunk = f.read(2048)
        return b"\x00" in chunk
    except OSError:
        return True


def _safe_read_text(path: Path) -> str | None:
    """安全读取文本：处理大小、二进制、编码。返回 None 表示不可读。"""
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return None
        if _is_binary(path):
            return None
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


# ---------------------------------------------------------------------------
# 发现器
# ---------------------------------------------------------------------------


class WorkspaceDiscoverer:
    """只读工作区发现器。

    识别六个治理表面中的前四个（spec §2）:
    - 身份与规则 (instruction)
    - Skills (skill)
    - 记忆 (memory)
    - 本地 RAG 源 (rag_source)
    工具与权限、运行证据留待后续阶段。
    """

    def __init__(self, workspace: Path, *, skip_dirs: set[str] | None = None):
        self.workspace = workspace.resolve()
        self.skip_dirs = skip_dirs or SKIP_DIRS

    def discover(self) -> DiscoveryResult:
        result = DiscoveryResult(workspace=self.workspace)
        self._discover_instructions(result)
        self._discover_skills(result)
        self._discover_memory(result)
        self._discover_rag(result)
        return result

    # --- 各表面发现逻辑 ---

    def _discover_instructions(self, result: DiscoveryResult) -> None:
        """治理表面1: 身份与规则。"""
        for name in INSTRUCTION_FILES:
            path = self.workspace / name
            if path.is_file() and _is_symlink_safe(path, self.workspace):
                self._add_text_agr(
                    result, path, AGRType.INSTRUCTION, source=name, scope=Scope.PROJECT
                )

    def _discover_skills(self, result: DiscoveryResult) -> None:
        """治理表面2: Skills。识别 SKILL.md 和其脚本。"""
        for skill_dir_rel in SKILL_DIRS:
            skill_dir = self.workspace / skill_dir_rel
            if not skill_dir.is_dir():
                continue
            if not _is_symlink_safe(skill_dir, self.workspace):
                continue
            for skill_md in self._iter_files(skill_dir, ("SKILL.md",)):
                self._add_text_agr(
                    result,
                    skill_md,
                    AGRType.SKILL,
                    source="skill_md",
                    scope=Scope.PROJECT,
                )
            # Skill 脚本（.py/.sh/*.ps1）
            for script in self._iter_files(skill_dir, suffixes=(".py", ".sh", ".ps1")):
                self._add_text_agr(
                    result,
                    script,
                    AGRType.SKILL,
                    source="skill_script",
                    scope=Scope.PROJECT,
                )

    def _discover_memory(self, result: DiscoveryResult) -> None:
        """治理表面3: 记忆。扫描 memory 类目录。"""
        for mem_dir_rel in MEMORY_DIRS:
            mem_dir = self.workspace / mem_dir_rel
            if not mem_dir.is_dir():
                continue
            if not _is_symlink_safe(mem_dir, self.workspace):
                continue
            for path in self._iter_files(mem_dir, suffixes=TEXT_EXTS):
                self._add_text_agr(
                    result,
                    path,
                    AGRType.MEMORY,
                    source="memory_dir",
                    scope=Scope.PROJECT,
                )

    def _discover_rag(self, result: DiscoveryResult) -> None:
        """治理表面4: 本地 RAG 源。扫描 docs/knowledge 类目录。"""
        for rag_dir_rel in RAG_DIRS:
            rag_dir = self.workspace / rag_dir_rel
            if not rag_dir.is_dir():
                continue
            if not _is_symlink_safe(rag_dir, self.workspace):
                continue
            for path in self._iter_files(rag_dir, suffixes=TEXT_EXTS):
                self._add_text_agr(
                    result,
                    path,
                    AGRType.RAG_SOURCE,
                    source="rag_dir",
                    scope=Scope.PROJECT,
                )

    # --- 文件遍历 ---

    def _iter_files(
        self,
        root: Path,
        names: tuple[str, ...] | None = None,
        suffixes: tuple[str, ...] | None = None,
    ) -> Iterator[Path]:
        """安全遍历目录，处理符号链接、路径穿越、跳过目录。"""
        for dirpath, dirnames, filenames in self._safe_walk(root):
            # 原地修改 dirnames 以跳过黑名单目录
            dirnames[:] = [d for d in dirnames if d not in self.skip_dirs]
            for fname in filenames:
                path = dirpath / fname
                if not _is_symlink_safe(path, self.workspace):
                    continue
                if not _is_within_workspace(path, self.workspace):
                    continue
                if names and fname not in names:
                    continue
                if suffixes and not path.suffix.lower() in suffixes:
                    continue
                yield path

    def _safe_walk(self, root: Path) -> Iterator[tuple[Path, list[str], list[str]]]:
        """os.walk 包装，带路径穿越保护。"""
        import os

        for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
            dp = Path(dirpath)
            if not _is_within_workspace(dp, self.workspace):
                continue
            yield dp, dirnames, filenames

    # --- AGR 构造 ---

    def _add_text_agr(
        self,
        result: DiscoveryResult,
        path: Path,
        agr_type: AGRType,
        *,
        source: str,
        scope: Scope,
    ) -> None:
        """读取文本文件并构造 AGR；不可读则记入 invisible。"""
        content = _safe_read_text(path)
        if content is None:
            result.invisible.append(
                {
                    "path": str(path),
                    "type": agr_type.value,
                    "reason": "unreadable (binary/oversize/encoding)",
                }
            )
            return
        try:
            mtime_iso = _mtime_iso(path)
        except OSError:
            mtime_iso = ""
        rel_path = str(path.relative_to(self.workspace))
        agr = AGR(
            id=stable_id(agr_type.value, rel_path),
            type=agr_type,
            path=str(path),
            scope=scope,
            source=source,
            hash=sha256_text(content),
            mtime=mtime_iso,
            sensitivity=_estimate_sensitivity(rel_path, content),
            metadata={"rel_path": rel_path, "size": len(content)},
        )
        result.agrs.append(agr)


# ---------------------------------------------------------------------------
# 辅助
# ---------------------------------------------------------------------------


def _mtime_iso(path: Path) -> str:
    """文件 mtime 转 ISO8601。"""
    from datetime import datetime, timezone

    ts = path.stat().st_mtime
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def _estimate_sensitivity(rel_path: str, content: str) -> Sensitivity:
    """启发式敏感度估计：仅基于文件名和明显模式，不做深度 PII 扫描。

    首期保守标记，真正的 PII 检测在后续阶段的规则引擎中实现。
    """
    lower_path = rel_path.lower()
    # 明显敏感路径
    if any(k in lower_path for k in (".env", "secret", "credential", "token", "key")):
        return Sensitivity.MEDIUM
    # 明显敏感内容模式（保守，仅查明显标记）
    if any(k in content[:4096] for k in ("BEGIN PRIVATE KEY", "AKIA", "ghp_")):
        return Sensitivity.HIGH
    return Sensitivity.NONE
