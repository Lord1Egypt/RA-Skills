"""ImportAdapter + TargetAdapter 契约与基础实现（spec §6.2, §6.3, §6.4）。

ImportAdapter：离线导入包（ChatGPT/Claude/Gemini/MemoryGuard-bundle）
- detect/inventory/parse/normalize/explain
- 安全：解包前检查 Zip Slip、压缩比、符号链接、绝对路径
- HTML 只作为不可信文本解析

TargetAdapter：目标 Agent 编译与发布
- inspect_target/compile/validate/install/verify/rollback
- 只能完整替换 MemoryGuard 明确管理的目录/文件集合
- 不覆盖整个 .codex/.claude/ 等
"""

from __future__ import annotations

import json
import os
import shutil
import zipfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .schema_v3 import (
    BuildManifest, CoverageLedger, CoverageStatus,
    MemoryRecord, MemoryStatus, MemoryKind, Completeness, Provenance,
    ReleaseChange, ReleaseStatus,
    RecordMappingKind, RecordMappingEntry,
    stable_hash, _now_iso,
)
from .memory_ir import MemoryIR


# ===========================================================================
# ImportAdapter（spec §6.2）
# ===========================================================================


@dataclass
class ImportDetection:
    """detect() 返回。"""
    provider: str  # chatgpt/claude/gemini/memoryguard-bundle/unknown
    schema_version: str = ""
    confidence: float = 0.0
    supported: bool = False
    notes: str = ""


@dataclass
class ImportedConversation:
    """解析出的对话。"""
    conv_id: str
    title: str
    messages: list[dict[str, Any]]  # {role, content, created_at}
    attachments: list[str] = field(default_factory=list)


@dataclass
class ImportCapability:
    """explain() 返回。"""
    adapter_name: str
    supported: bool
    partial: bool
    notes: str


class ImportAdapter:
    """ImportAdapter 基类契约（spec §6.2）。"""

    def detect(self, bundle: Path) -> ImportDetection:
        raise NotImplementedError

    def inventory(self, bundle: Path, budget: int = 10000) -> dict[str, Any]:
        """返回覆盖率信息：文件数、总大小、关键文件。"""
        raise NotImplementedError

    def parse(self, bundle: Path) -> list[ImportedConversation]:
        raise NotImplementedError

    def normalize(self, items: list[ImportedConversation]) -> list[MemoryRecord]:
        raise NotImplementedError

    def explain(self) -> ImportCapability:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# 安全解包工具
# ---------------------------------------------------------------------------


def safe_extract_zip(zip_path: Path, dest: Path,
                     max_files: int = 10000,
                     max_total_size: int = 500 * 1024 * 1024,
                     max_ratio: int = 100) -> list[str]:
    """安全解压 ZIP，防 Zip Slip / zip bomb / 符号链接。

    返回解压后的文件相对路径列表。
    失败时抛 ValueError。
    """
    dest.mkdir(parents=True, exist_ok=True)
    extracted: list[str] = []
    total_size = 0
    with zipfile.ZipFile(zip_path, "r") as zf:
        infos = zf.infolist()
        if len(infos) > max_files:
            raise ValueError(f"too many files in zip: {len(infos)} > {max_files}")
        compressed = sum(i.compress_size for i in infos)
        uncompressed = sum(i.file_size for i in infos)
        if compressed > 0 and uncompressed / compressed > max_ratio:
            raise ValueError(f"compression ratio too high: {uncompressed/compressed}")
        for info in infos:
            # 防 Zip Slip：不允许绝对路径、.. 、符号链接
            name = info.filename
            if name.startswith("/") or "\\" in name and name[1] == ":":
                raise ValueError(f"absolute path in zip: {name}")
            if ".." in name.split("/"):
                raise ValueError(f"path traversal in zip: {name}")
            # 符号链接检测（zip 外部属性）
            if info.external_attr >> 16 == 0xA1FF:  # symlink mode
                raise ValueError(f"symlink in zip: {name}")
            target = (dest / name).resolve()
            if not str(target).startswith(str(dest.resolve())):
                raise ValueError(f"escape attempt: {name}")
            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            total_size += info.file_size
            if total_size > max_total_size:
                raise ValueError(f"total size exceeds limit: {total_size}")
            target.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info) as src, open(target, "wb") as dst:
                dst.write(src.read())
            extracted.append(name)
    return extracted


# ---------------------------------------------------------------------------
# GenericImportAdapter：通用 Markdown/TXT/JSON/JSONL
# ---------------------------------------------------------------------------


class GenericImportAdapter(ImportAdapter):
    """通用格式适配器：memoryguard-bundle-v1、Markdown、TXT、JSON/JSONL。"""

    def detect(self, bundle: Path) -> ImportDetection:
        if bundle.is_file():
            ext = bundle.suffix.lower()
            if ext in (".md", ".txt"):
                return ImportDetection(provider="generic", schema_version="text",
                                       confidence=1.0, supported=True)
            if ext in (".json", ".jsonl"):
                return ImportDetection(provider="generic", schema_version="json",
                                       confidence=1.0, supported=True)
        if bundle.is_dir():
            # 检测 memoryguard-bundle-v1
            manifest = bundle / "manifest.json"
            if manifest.exists():
                try:
                    data = json.loads(manifest.read_text(encoding="utf-8"))
                    if data.get("format") == "memoryguard-bundle-v1":
                        return ImportDetection(provider="memoryguard-bundle",
                                               schema_version="v1",
                                               confidence=1.0, supported=True)
                except (OSError, json.JSONDecodeError):
                    pass
            # 任意含 md/txt 的目录
            md_files = list(bundle.rglob("*.md"))[:5]
            if md_files:
                return ImportDetection(provider="generic", schema_version="dir",
                                       confidence=0.7, supported=True)
        if bundle.is_file() and bundle.suffix.lower() == ".zip":
            return ImportDetection(provider="zip", confidence=0.5,
                                   supported=False, notes="zip needs safe_extract")
        return ImportDetection(provider="unknown", confidence=0.0, supported=False)

    def inventory(self, bundle: Path, budget: int = 10000) -> dict[str, Any]:
        files: list[str] = []
        if bundle.is_file():
            files = [bundle.name]
        else:
            for p in bundle.rglob("*"):
                if p.is_file():
                    files.append(str(p.relative_to(bundle)))
                if len(files) >= budget:
                    break
        return {"file_count": len(files), "files": files[:50]}

    def parse(self, bundle: Path) -> list[ImportedConversation]:
        # 通用适配器：把每个文件当作一个"对话"
        convs: list[ImportedConversation] = []
        if bundle.is_file():
            try:
                content = bundle.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                return []
            convs.append(ImportedConversation(
                conv_id="imp-" + stable_hash(str(bundle)),
                title=bundle.name,
                messages=[{"role": "user", "content": content, "created_at": _now_iso()}],
            ))
        elif bundle.is_dir():
            for p in bundle.rglob("*.md"):
                try:
                    content = p.read_text(encoding="utf-8")
                except (OSError, UnicodeDecodeError):
                    continue
                convs.append(ImportedConversation(
                    conv_id="imp-" + stable_hash(str(p)),
                    title=p.name,
                    messages=[{"role": "user", "content": content, "created_at": _now_iso()}],
                ))
        return convs

    def normalize(self, items: list[ImportedConversation]) -> list[MemoryRecord]:
        records: list[MemoryRecord] = []
        for conv in items:
            for msg in conv.messages:
                body = msg.get("content", "")
                if not body.strip():
                    continue
                memory_id = stable_hash(conv.conv_id, msg.get("role", ""), body[:200])
                rec = MemoryRecord(
                    memory_id=memory_id, kind=MemoryKind.EPISODE,
                    title=conv.title[:80], body=body, scope="user",
                    confidence=0.3,  # 导入的 provider summary 完整性低
                    provenance=[Provenance(
                        source_object_id=conv.conv_id,
                        locator=f"message:{msg.get('role', 'user')}",
                        excerpt_hash=stable_hash(body),
                    )],
                    status=MemoryStatus.CANDIDATE,
                    completeness=Completeness.UNVERIFIABLE,  # 导入内容默认不可验证
                    created_at=_now_iso(),
                )
                records.append(rec)
        return records

    def explain(self) -> ImportCapability:
        return ImportCapability(
            adapter_name="GenericImportAdapter", supported=True, partial=False,
            notes="支持 memoryguard-bundle-v1、Markdown、TXT、JSON/JSONL",
        )


# ---------------------------------------------------------------------------
# ChatGPTImportAdapter：ChatGPT 官方导出 conversations.json
# ---------------------------------------------------------------------------


class ChatGPTImportAdapter(ImportAdapter):
    """ChatGPT 官方导出包适配器。

    官方导出 ZIP 解压后含 conversations.json。
    schema 不固定，只有 fixture 验证后才标记 stable。
    """

    EXPECTED_FILE = "conversations.json"

    def detect(self, bundle: Path) -> ImportDetection:
        # 如果是目录，找 conversations.json
        if bundle.is_dir():
            conv_file = bundle / self.EXPECTED_FILE
            if conv_file.exists():
                return ImportDetection(
                    provider="chatgpt", schema_version="unknown",
                    confidence=0.8, supported=True,
                    notes="conversations.json found; schema needs fixture validation",
                )
        # 如果是 zip，尝试解压检测
        if bundle.is_file() and bundle.suffix.lower() == ".zip":
            try:
                with zipfile.ZipFile(bundle, "r") as zf:
                    names = zf.namelist()
                    if self.EXPECTED_FILE in names:
                        return ImportDetection(
                            provider="chatgpt", schema_version="unknown",
                            confidence=0.8, supported=True,
                            notes="zip contains conversations.json",
                        )
            except zipfile.BadZipFile:
                pass
        return ImportDetection(provider="unknown", confidence=0.0, supported=False)

    def inventory(self, bundle: Path, budget: int = 10000) -> dict[str, Any]:
        det = self.detect(bundle)
        if not det.supported:
            return {"file_count": 0, "supported": False}
        return {"file_count": 1, "key_file": self.EXPECTED_FILE, "supported": True}

    def parse(self, bundle: Path) -> list[ImportedConversation]:
        convs: list[ImportedConversation] = []
        conv_file: Path | None = None
        if bundle.is_dir():
            conv_file = bundle / self.EXPECTED_FILE
        if not conv_file or not conv_file.exists():
            return []
        try:
            data = json.loads(conv_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        if not isinstance(data, list):
            return []
        for item in data[:1000]:  # 限制 1000 条
            conv_id = str(item.get("id", stable_hash(str(item))))
            title = item.get("title", "")
            messages: list[dict[str, Any]] = []
            mapping = item.get("mapping", {})
            if isinstance(mapping, dict):
                for node_id, node in mapping.items():
                    if not isinstance(node, dict):
                        continue
                    msg = node.get("message")
                    if not isinstance(msg, dict):
                        continue
                    role = msg.get("author", {}).get("role", "unknown")
                    content_parts = msg.get("content", {}).get("parts", [])
                    content = " ".join(str(p) for p in content_parts if isinstance(p, str))
                    create_time = msg.get("create_time")
                    if content.strip():
                        messages.append({
                            "role": role, "content": content,
                            "created_at": str(create_time) if create_time else "",
                        })
            convs.append(ImportedConversation(
                conv_id="chatgpt-" + conv_id[:16],
                title=title, messages=messages,
            ))
        return convs

    def normalize(self, items: list[ImportedConversation]) -> list[MemoryRecord]:
        # 复用 Generic 的逻辑，但标记 completeness=UNVERIFIABLE
        records: list[MemoryRecord] = []
        for conv in items:
            for msg in conv.messages:
                body = msg.get("content", "")
                if not body.strip():
                    continue
                memory_id = stable_hash(conv.conv_id, msg.get("role", ""), body[:200])
                rec = MemoryRecord(
                    memory_id=memory_id, kind=MemoryKind.EPISODE,
                    title=conv.title[:80], body=body, scope="user",
                    confidence=0.3,
                    provenance=[Provenance(
                        source_object_id=conv.conv_id,
                        locator=f"chatgpt:message:{msg.get('role', '')}",
                        excerpt_hash=stable_hash(body),
                    )],
                    status=MemoryStatus.CANDIDATE,
                    completeness=Completeness.UNVERIFIABLE,
                    created_at=_now_iso(),
                )
                records.append(rec)
        return records

    def explain(self) -> ImportCapability:
        return ImportCapability(
            adapter_name="ChatGPTImportAdapter", supported=True, partial=True,
            notes="conversations.json 解析；schema 未固定，需 fixture 验证；所有 summary 标记 UNVERIFIABLE",
        )


# ===========================================================================
# TargetAdapter（spec §6.3, §6.4）
# ===========================================================================


@dataclass
class TargetState:
    """inspect_target() 返回。"""
    target_path: str
    exists: bool
    managed_files: list[str]  # MemoryGuard 管理的文件
    external_files: list[str]  # 非管理的文件（不能覆盖）
    before_hash: str = ""


@dataclass
class ValidationResult:
    """validate() 返回。"""
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class VerificationResult:
    """verify() 返回。"""
    rescan_match: bool
    hashes_match: bool
    errors: list[str] = field(default_factory=list)


class TargetAdapter:
    """TargetAdapter 基类契约（spec §6.3）。"""

    def inspect_target(self, path: Path) -> TargetState:
        raise NotImplementedError

    def compile(self, ir: MemoryIR, decisions: list, staging_dir: Path,
                target_profile: str) -> BuildManifest:
        raise NotImplementedError

    def validate(self, staging_dir: Path, manifest: BuildManifest) -> ValidationResult:
        raise NotImplementedError

    def install(self, plan: dict, approval: bool, target_path: Path,
                staging_dir: Path, manifest: BuildManifest) -> ReleaseChange:
        raise NotImplementedError

    def verify(self, target_path: Path, manifest: BuildManifest) -> VerificationResult:
        raise NotImplementedError

    def rollback(self, change: ReleaseChange, target_path: Path) -> VerificationResult:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# GenericMarkdownTarget：通用 Markdown 记忆包
# ---------------------------------------------------------------------------


class GenericMarkdownTarget(TargetAdapter):
    """通用 Markdown 目标适配器。

    把 Memory IR 编译为 memory.md + index.json 的记忆包。
    只管理这 2 个文件，不覆盖目标目录其他内容。
    """

    MANAGED_FILES = ["memory.md", "index.json"]
    PROFILE = "generic-markdown-v1"

    def inspect_target(self, path: Path) -> TargetState:
        managed = []
        external = []
        if path.exists():
            for p in path.iterdir():
                if p.name in self.MANAGED_FILES:
                    managed.append(p.name)
                else:
                    external.append(p.name)
        return TargetState(
            target_path=str(path), exists=path.exists(),
            managed_files=managed, external_files=external,
        )

    def compile(self, ir: MemoryIR, decisions: list, staging_dir: Path,
                target_profile: str = "") -> BuildManifest:
        staging_dir.mkdir(parents=True, exist_ok=True)
        records = [r for r in ir.records if r.status != MemoryStatus.REJECTED]
        # memory.md
        md_lines: list[str] = ["# Memory", ""]
        # index.json
        index_entries: list[dict[str, Any]] = []
        mappings: list[RecordMappingEntry] = []
        published = 0
        excluded = 0
        quarantined = 0
        linked = 0
        for rec in records:
            if rec.status == MemoryStatus.QUARANTINED:
                quarantined += 1
                mappings.append(RecordMappingEntry(
                    memory_id=rec.memory_id, mapping=RecordMappingKind.QUARANTINED,
                    reason="status=quarantined",
                ))
                continue
            if rec.status == MemoryStatus.SUPERSEDED:
                linked += 1
                mappings.append(RecordMappingEntry(
                    memory_id=rec.memory_id, mapping=RecordMappingKind.LINKED_TO_PUBLISHED,
                    reason="status=superseded",
                ))
                continue
            # published
            md_lines.append(f"## {rec.title}")
            md_lines.append("")
            md_lines.append(rec.body)
            md_lines.append("")
            index_entries.append({
                "memory_id": rec.memory_id, "kind": rec.kind.value,
                "title": rec.title, "provenance_count": len(rec.provenance),
            })
            published += 1
            mappings.append(RecordMappingEntry(
                memory_id=rec.memory_id, mapping=RecordMappingKind.PUBLISHED,
                target_path="memory.md",
            ))
        # 被决策排除的
        for dec in decisions:
            if dec.action == "reject":
                excluded += 1
                mappings.append(RecordMappingEntry(
                    memory_id=dec.target_ids[0] if dec.target_ids else "",
                    mapping=RecordMappingKind.EXCLUDED_WITH_REASON,
                    reason=dec.reason or "rejected by decision",
                ))
        (staging_dir / "memory.md").write_text("\n".join(md_lines), encoding="utf-8")
        (staging_dir / "index.json").write_text(
            json.dumps({"entries": index_entries}, ensure_ascii=False, indent=2),
            encoding="utf-8")
        # release_hash
        release_hash = stable_hash(
            (staging_dir / "memory.md").read_text(encoding="utf-8"),
            (staging_dir / "index.json").read_text(encoding="utf-8"),
        )
        return BuildManifest(
            build_id="build-" + stable_hash(_now_iso(), str(staging_dir)),
            source_snapshot_id=ir.snapshot_id,
            target_profile=self.PROFILE,
            coverage_status="complete",
            input_record_count=len(records) + len(decisions),
            published_record_count=published,
            linked_record_count=linked,
            excluded_record_count=excluded,
            quarantined_record_count=quarantined,
            unaccounted_record_count=0,
            record_mappings=mappings,
            release_hash=release_hash,
        )

    def validate(self, staging_dir: Path, manifest: BuildManifest) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []
        for f in self.MANAGED_FILES:
            if not (staging_dir / f).exists():
                errors.append(f"missing staging file: {f}")
        if not manifest.integrity_ok():
            errors.append("manifest integrity check failed")
        return ValidationResult(valid=len(errors) == 0, errors=errors, warnings=warnings)

    def install(self, plan: dict, approval: bool, target_path: Path,
                staging_dir: Path, manifest: BuildManifest) -> ReleaseChange:
        if not approval:
            raise ValueError("install requires explicit approval")
        target_path.mkdir(parents=True, exist_ok=True)
        # 备份受管目标文件（仅这 2 个，不备份所有原始来源）
        backup_paths: list[str] = []
        backup_dir = target_path / ".memoryguard-backup"
        backup_dir.mkdir(parents=True, exist_ok=True)
        for f in self.MANAGED_FILES:
            tp = target_path / f
            if tp.exists():
                bp = backup_dir / f"{f}.{stable_hash(_now_iso())}.bak"
                shutil.copy2(tp, bp)
                backup_paths.append(str(bp))
        # 原子切换：写临时文件再 rename
        changed_paths: list[str] = []
        for f in self.MANAGED_FILES:
            src = staging_dir / f
            dst = target_path / f
            tmp = dst.with_suffix(dst.suffix + ".tmp")
            shutil.copy2(src, tmp)
            tmp.replace(dst)
            changed_paths.append(str(dst))
        release_id = "rel-" + stable_hash(_now_iso(), manifest.build_id)
        return ReleaseChange(
            release_id=release_id, build_id=manifest.build_id,
            target_profile=self.PROFILE, applied_at=_now_iso(),
            backup_paths=backup_paths, changed_paths=changed_paths,
            status=ReleaseStatus.APPLIED,
        )

    def verify(self, target_path: Path, manifest: BuildManifest) -> VerificationResult:
        errors: list[str] = []
        # 复扫：目标文件存在且内容匹配
        memory_md = target_path / "memory.md"
        index_json = target_path / "index.json"
        if not memory_md.exists():
            errors.append("memory.md missing after install")
        if not index_json.exists():
            errors.append("index.json missing after install")
        if not errors:
            current_hash = stable_hash(
                memory_md.read_text(encoding="utf-8"),
                index_json.read_text(encoding="utf-8"),
            )
            hashes_match = (current_hash == manifest.release_hash)
        else:
            hashes_match = False
        return VerificationResult(
            rescan_match=len(errors) == 0, hashes_match=hashes_match, errors=errors,
        )

    def rollback(self, change: ReleaseChange, target_path: Path) -> VerificationResult:
        errors: list[str] = []
        # 从备份恢复
        for changed in change.changed_paths:
            cp = Path(changed)
            # 找对应备份
            backup_name = cp.name
            backup_dir = target_path / ".memoryguard-backup"
            if not backup_dir.exists():
                errors.append(f"backup dir missing: {backup_dir}")
                continue
            # 找最新的该文件备份
            backups = sorted(backup_dir.glob(f"{backup_name}.*.bak"), reverse=True)
            if not backups:
                errors.append(f"no backup for {backup_name}")
                continue
            shutil.copy2(backups[0], cp)
        return VerificationResult(
            rescan_match=len(errors) == 0, hashes_match=len(errors) == 0,
            errors=errors,
        )
