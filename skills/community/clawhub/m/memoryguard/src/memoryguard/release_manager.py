"""ReleaseManager：发布事务编排（spec §11.2）。

完整流程：
  冻结 SourceSnapshot
  → 规范化 IR
  → 应用人工决策
  → staging 编译
  → 结构与清单校验
  → 展示完整 Diff
  → 用户明确批准
  → 仅备份受管目标文件
  → 原子切换
  → 重新读取目标
  → 对照 BuildManifest 验证
  → 成功提交或自动回滚

v3 关键约束：
- 扫描和萃取都是只读，不备份所有原始来源
- 仅在即将写目标时备份受管目标文件
- 回滚以 ReleaseChange 为单位
- 每次回滚前仍需备份当前目标状态
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .adapters import GenericMarkdownTarget, TargetAdapter, ValidationResult
from .memory_ir import MemoryIR, MemoryNormalizer
from .schema_v3 import (
    BuildManifest, DecisionEvent, ReleaseChange, ReleaseStatus,
    stable_hash, _now_iso,
)
from .source_registry import ScanBudget, SourceRegistry, SourceSnapshot


@dataclass
class BuildPlan:
    """构建计划（apply 前可预览）。"""
    plan_id: str
    snapshot_id: str
    target_profile: str
    manifest: BuildManifest
    diff_preview: dict[str, Any]  # 新增/修改/删除文件预览
    coverage_status: str
    integrity_ok: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "plan_id": self.plan_id, "snapshot_id": self.snapshot_id,
            "target_profile": self.target_profile,
            "manifest": self.manifest.to_dict(),
            "diff_preview": self.diff_preview,
            "coverage_status": self.coverage_status,
            "integrity_ok": self.integrity_ok,
        }


class ReleaseManager:
    """发布事务编排器。"""

    def __init__(self, workspace: str | Path):
        self.workspace = Path(workspace).resolve()
        self.mg_dir = self.workspace / ".memoryguard"
        self.releases_dir = self.mg_dir / "releases"
        self.changes_dir = self.mg_dir / "changes"
        self.plans_dir = self.mg_dir / "plans"
        self.registry = SourceRegistry(workspace)
        self.normalizer = MemoryNormalizer(workspace)

    # ------------------------------------------------------------------
    # 完整流程：scan → normalize → build-plan
    # ------------------------------------------------------------------

    def scan_and_normalize(self, budget: ScanBudget | None = None) -> tuple[SourceSnapshot, MemoryIR]:
        """扫描 + 规范化为 IR。只读，无副作用。

        v3.1 §1.3：必须传 root_map，否则外部来源无法定位文件。
        """
        snapshot = self.registry.scan(budget)
        # v3.1 §1.3：传 root_map 给 normalizer
        root_map = {r.root_id: r.path for r in self.registry.list_sources()}
        ir = self.normalizer.normalize(snapshot, root_map=root_map)
        self.normalizer.save(ir)
        return snapshot, ir

    def create_build_plan(self, ir: MemoryIR, target: TargetAdapter,
                          target_path: Path, decisions: list[DecisionEvent] | None = None) -> BuildPlan:
        """生成构建计划（不写目标）。"""
        decisions = decisions or []
        staging = self._staging_dir("plan")
        manifest = target.compile(ir, decisions, staging, target.PROFILE if hasattr(target, 'PROFILE') else "")
        vr = target.validate(staging, manifest)
        # Diff 预览
        target_state = target.inspect_target(target_path)
        diff_preview = self._compute_diff(target_state, staging)
        plan_id = "plan-" + stable_hash(_now_iso(), manifest.build_id)
        plan = BuildPlan(
            plan_id=plan_id, snapshot_id=ir.snapshot_id,
            target_profile=manifest.target_profile,
            manifest=manifest, diff_preview=diff_preview,
            coverage_status=manifest.coverage_status,
            integrity_ok=manifest.integrity_ok() and vr.valid,
        )
        # 持久化计划
        self.plans_dir.mkdir(parents=True, exist_ok=True)
        (self.plans_dir / f"{plan_id}.json").write_text(
            json.dumps(plan.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8")
        # 持久化 staging
        plan_staging = self._staging_dir(plan_id)
        for f in staging.iterdir():
            dst = plan_staging / f.name
            if not dst.exists():
                f.replace(dst)  # 移动
        return plan

    def apply_build(self, plan_id: str, target: TargetAdapter,
                    target_path: Path, approval: bool) -> ReleaseChange:
        """应用构建计划：备份受管目标 → 原子切换 → 验证。"""
        if not approval:
            raise ValueError("apply requires explicit approval")
        plan_path = self.plans_dir / f"{plan_id}.json"
        if not plan_path.exists():
            raise FileNotFoundError(f"plan not found: {plan_id}")
        plan_data = json.loads(plan_path.read_text(encoding="utf-8"))
        manifest = self._manifest_from_dict(plan_data["manifest"])
        staging = self._staging_dir(plan_id)
        if not staging.exists():
            raise FileNotFoundError(f"staging missing for plan {plan_id}")
        # install（内部会备份受管目标）
        release = target.install({}, True, target_path, staging, manifest)
        # verify
        verify = target.verify(target_path, manifest)
        release.verify_result = {
            "rescan_match": verify.rescan_match,
            "hashes_match": verify.hashes_match,
            "errors": verify.errors,
        }
        if verify.rescan_match and verify.hashes_match:
            release.status = ReleaseStatus.VERIFIED
        else:
            # 自动回滚
            rb = target.rollback(release, target_path)
            release.status = ReleaseStatus.FAILED
            release.verify_result["rollback"] = {
                "rescan_match": rb.rescan_match, "errors": rb.errors,
            }
        # 持久化 ReleaseChange（v3.1 §8.1：只写 releases/，不动 changes/）
        self.releases_dir.mkdir(parents=True, exist_ok=True)
        out = release.to_dict()
        out["schema_version"] = "3.1"
        out["record_type"] = "memory_release"
        (self.releases_dir / f"{release.release_id}.json").write_text(
            json.dumps(out, ensure_ascii=False, indent=2),
            encoding="utf-8")
        return release

    def verify_release(self, release_id: str, target: TargetAdapter,
                       target_path: Path, manifest: BuildManifest) -> dict[str, Any]:
        """复扫验证已发布的变更。"""
        verify = target.verify(target_path, manifest)
        return {
            "release_id": release_id,
            "rescan_match": verify.rescan_match,
            "hashes_match": verify.hashes_match,
            "errors": verify.errors,
        }

    def rollback_release(self, release_id: str, target: TargetAdapter,
                         target_path: Path) -> ReleaseChange:
        """回滚发布。回滚前先备份当前目标状态。

        v3.1 §8.3：先查 releases/，再兼容查旧 changes/ 中误写的 Release。
        """
        from .change_history import get_release
        data = get_release(self.workspace, release_id)
        if data is None:
            raise FileNotFoundError(f"release not found: {release_id}")
        release = ReleaseChange(
            release_id=data["release_id"], build_id=data["build_id"],
            target_profile=data["target_profile"], applied_at=data.get("applied_at", ""),
            backup_paths=data.get("backup_paths", []),
            changed_paths=data.get("changed_paths", []),
            verify_result=data.get("verify_result", {}),
            status=ReleaseStatus(data.get("status", "applied")),
        )
        # 回滚前备份当前目标
        pre_rollback_backups = self._backup_current_target(target_path, release.changed_paths)
        rb = target.rollback(release, target_path)
        release.status = ReleaseStatus.ROLLED_BACK
        release.verify_result["pre_rollback_backups"] = pre_rollback_backups
        release.verify_result["rollback_result"] = {
            "rescan_match": rb.rescan_match, "errors": rb.errors,
        }
        # 写回原位置（releases/ 或 changes/），保持兼容
        from .change_history import HistoryRecordType, detect_record_type
        rt = detect_record_type(data)
        target_dir = (self.releases_dir if rt == HistoryRecordType.MEMORY_RELEASE
                      else self.changes_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        out = release.to_dict()
        out["schema_version"] = "3.1"
        out["record_type"] = "memory_release"
        (target_dir / f"{release_id}.json").write_text(
            json.dumps(out, ensure_ascii=False, indent=2),
            encoding="utf-8")
        return release

    def list_releases(self) -> list[dict[str, Any]]:
        """列出所有 ReleaseChange（v3.1 §8：只返回 memory_release，跳过 rule_change）。

        旧 changes/ 中的 rule_change 不在此列；用 list_change_history() 看统一时间线。
        损坏 JSON 不再触发 KeyError，由 change_history.list_change_history 返回 warnings。
        """
        from .change_history import list_change_history, HistoryRecordType
        history = list_change_history(self.workspace)
        return [item for item in history["items"]
                if item.get("record_type") == HistoryRecordType.MEMORY_RELEASE.value]

    # ------------------------------------------------------------------
    # 内部工具
    # ------------------------------------------------------------------

    def _staging_dir(self, name: str) -> Path:
        d = self.mg_dir / "staging" / name
        d.mkdir(parents=True, exist_ok=True)
        return d

    def _compute_diff(self, target_state, staging: Path) -> dict[str, Any]:
        added, modified, unchanged = [], [], []
        for f in staging.iterdir():
            target_file = Path(target_state.target_path) / f.name
            if not target_file.exists():
                added.append(f.name)
            elif target_file.read_bytes() != f.read_bytes():
                modified.append(f.name)
            else:
                unchanged.append(f.name)
        deleted = [f for f in target_state.managed_files
                   if not (staging / f).exists()]
        return {"added": added, "modified": modified, "deleted": deleted, "unchanged": unchanged}

    def _backup_current_target(self, target_path: Path, changed_paths: list[str]) -> list[str]:
        backups = []
        backup_dir = target_path / ".memoryguard-rollback-backup"
        backup_dir.mkdir(parents=True, exist_ok=True)
        ts = stable_hash(_now_iso())
        for cp in changed_paths:
            p = Path(cp)
            if p.exists():
                bp = backup_dir / f"{p.name}.{ts}.rbak"
                bp.write_bytes(p.read_bytes())
                backups.append(str(bp))
        return backups

    def _manifest_from_dict(self, data: dict[str, Any]) -> BuildManifest:
        from .schema_v3 import RecordMappingEntry, RecordMappingKind
        mappings = [RecordMappingEntry(
            memory_id=m["memory_id"],
            mapping=RecordMappingKind(m["mapping"]),
            reason=m.get("reason", ""), target_path=m.get("target_path", ""),
        ) for m in data.get("record_mappings", [])]
        return BuildManifest(
            build_id=data["build_id"],
            source_snapshot_id=data.get("source_snapshot_id", ""),
            policy_version=data.get("policy_version", "memory-policy-v1"),
            decision_log_hash=data.get("decision_log_hash", ""),
            target_profile=data.get("target_profile", "generic-markdown-v1"),
            coverage_status=data.get("coverage_status", "unknown"),
            input_record_count=data.get("input_record_count", 0),
            published_record_count=data.get("published_record_count", 0),
            linked_record_count=data.get("linked_record_count", 0),
            excluded_record_count=data.get("excluded_record_count", 0),
            quarantined_record_count=data.get("quarantined_record_count", 0),
            unaccounted_record_count=data.get("unaccounted_record_count", 0),
            record_mappings=mappings,
            release_hash=data.get("release_hash", ""),
        )
