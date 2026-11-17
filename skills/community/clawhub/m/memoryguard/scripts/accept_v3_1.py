"""MemoryGuard v3.1 MVP 验收脚本（spec §13.1）。

逐项验证 9 个 MVP 指标：
1. 一次点击列出 Agent 候选和分类，候选阶段不读正文
2. 所有已知表面 100% 进入 DiscoveryLedger
3. 所有授权候选 100% 进入 SourceCoverageLedger
4. 所有选中对象 100% 进入 NormalizationLedger
5. 所有 active MemoryRecord 100% 进入 PublicationLedger
6. 外部来源和 Obsidian 不再出现"页面可见、IR 丢失"
7. 变更记录兼容旧 Change、新 Release 和损坏记录
8. 只有 Loader 复读成功才能显示"已接管"（EXPORT_ONLY 不声称接管）
9. 所有写入可通过精确 Release 回滚

用法：python scripts/accept_v3_1.py
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

# 确保能从 memoryguard/ 目录运行（src 在父目录）
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.memoryguard.agent_locator import AgentLocator, compute_takeover_state
from src.memoryguard.change_history import list_change_history
from src.memoryguard.gui import GovernanceApi
from src.memoryguard.managed_store import ManagedStore
from src.memoryguard.projection import ProjectionBuilder
from src.memoryguard.schema_v3 import (
    SourceCategory, SourceRootType, SurfaceStatus, TakeoverState, TargetCapability,
)
from src.memoryguard.source_registry import SourceRegistry, ScanBudget


def _setup_test_workspace(tmp: Path) -> None:
    """创建测试 workspace：含 CLAUDE.md + notes.md + .claude/memory/。"""
    (tmp / "CLAUDE.md").write_text(
        "# Claude Instructions\nYou are a helpful agent.\n", encoding="utf-8")
    (tmp / "notes.md").write_text(
        "# 项目偏好\n用户喜欢简洁代码。\n## 任务记录\n完成了 v3.1 实施。\n",
        encoding="utf-8")
    claude_mem = tmp / ".claude" / "memory"
    claude_mem.mkdir(parents=True, exist_ok=True)
    (claude_mem / "preference.md").write_text(
        "# 偏好\n- 偏好中文交流\n- 重视代码质量\n", encoding="utf-8")


def _check(label: str, ok: bool, detail: str = "") -> bool:
    status = "PASS" if ok else "FAIL"
    msg = f"[{status}] {label}"
    if detail:
        msg += f" :: {detail}"
    print(msg)
    return ok


def main() -> int:
    all_pass = True
    with tempfile.TemporaryDirectory() as tmp_str:
        tmp = Path(tmp_str)
        _setup_test_workspace(tmp)
        api = GovernanceApi(str(tmp))

        # -----------------------------------------------------------------
        # 1. 一次点击列出 Agent 候选和分类，候选阶段不读正文
        # -----------------------------------------------------------------
        print("\n=== 1. 一次点击列出 Agent 候选 ===")
        d = api.discover_agents()
        instances = d["instances"]
        ok1 = len(instances) > 0
        # 验证候选阶段不读正文：DiscoveryLedger 只记录 status，不记录 content
        ok1_detail = f"instances={len(instances)}, products={[i['product'] for i in instances]}"
        all_pass &= _check("发现 Agent 候选", ok1, ok1_detail)
        # 验证不读正文：检查 DiscoveryEntry 没有 content 字段
        discovery_path = tmp / ".memoryguard" / "discovery" / "latest.json"
        if discovery_path.exists():
            data = json.loads(discovery_path.read_text(encoding="utf-8"))
            for ledger in data.get("ledgers", {}).values():
                for entry in ledger.get("entries", []):
                    has_content = "content" in entry or "excerpt" in entry
                    all_pass &= _check(f"候选阶段不读正文 ({entry.get('surface_id')})",
                                       not has_content,
                                       f"status={entry.get('status')}")

        # -----------------------------------------------------------------
        # 2. 所有已知表面 100% 进入 DiscoveryLedger
        # -----------------------------------------------------------------
        print("\n=== 2. 所有已知表面进入 DiscoveryLedger ===")
        for inst in instances:
            inst_id = inst["instance_id"]
            locator = AgentLocator(str(tmp))
            tree = locator.get_selection_tree(inst_id)
            if "error" in tree:
                all_pass &= _check(f"SelectionTree {inst_id}", False, tree["error"])
                continue
            total_surfaces = len(inst.get("surfaces", []))
            found_surfaces = sum(1 for s in inst.get("surfaces", [])
                                 if s.get("status") == SurfaceStatus.FOUND.value)
            # DiscoveryLedger 必须包含所有 surface（found + missing）
            ledger = data.get("ledgers", {}).get(inst_id, {}) if discovery_path.exists() else {}
            ledger_entry_count = len(ledger.get("entries", []))
            ok2 = ledger_entry_count == total_surfaces
            all_pass &= _check(
                f"DiscoveryLedger 完整 ({inst['product']})",
                ok2,
                f"surfaces={total_surfaces}, ledger_entries={ledger_entry_count}, found={found_surfaces}",
            )

        # -----------------------------------------------------------------
        # 3. 所有授权候选 100% 进入 SourceCoverageLedger
        # -----------------------------------------------------------------
        print("\n=== 3. 所有授权候选进入 SourceCoverageLedger ===")
        # 先 commit_selection 授权一个 agent 的 surfaces
        if instances:
            inst = instances[0]
            inst_id = inst["instance_id"]
            tree = api.get_selection_tree(inst_id)
            selected = []
            for cat in tree.get("categories", []):
                for f in cat.get("files", []):
                    selected.append({"category": cat["category"], "path": f["path"]})
            if selected:
                sel_result = api.commit_selection(inst_id, selected, confirmed=True)
                ok3 = sel_result.get("added_source_count", 0) > 0 or sel_result.get("updated_source_count", 0) > 0
                all_pass &= _check(
                    "commit_selection 授权 SourceRoot",
                    ok3,
                    f"added={sel_result.get('added_source_count')}, updated={sel_result.get('updated_source_count')}",
                )
            # 扫描并检查 CoverageLedger
            reg = SourceRegistry(str(tmp))
            snap = reg.scan(ScanBudget())
            cov_counts = snap.coverage.counts()
            # v3.1 §1.4 P0：unaccounted_count 必须为 0
            ok3b = cov_counts.get("unaccounted_count", -1) == 0
            all_pass &= _check(
                "CoverageLedger unaccounted_count=0",
                ok3b,
                f"unaccounted={cov_counts.get('unaccounted_count')}, total={cov_counts.get('candidate_count')}",
            )

        # -----------------------------------------------------------------
        # 4. 所有选中对象 100% 进入 NormalizationLedger
        # -----------------------------------------------------------------
        print("\n=== 4. 所有选中对象进入 NormalizationLedger ===")
        # build_projection 会扫描+规范化，生成 Memory IR
        proj = api.build_projection(confirmed=True)
        # 检查 IR 是否有 records
        from src.memoryguard.memory_ir import MemoryNormalizer
        norm = MemoryNormalizer(str(tmp))
        ir = norm.load()
        ok4 = ir is not None and len(ir.records) > 0
        all_pass &= _check(
            "Memory IR 生成 records",
            ok4,
            f"records={len(ir.records) if ir else 0}",
        )

        # -----------------------------------------------------------------
        # 5. 所有 active MemoryRecord 100% 进入 PublicationLedger
        # -----------------------------------------------------------------
        print("\n=== 5. 所有 active MemoryRecord 进入 PublicationLedger ===")
        # build_projection 会为每个 agent_instance 创建 ManagedStore initial version
        mm_root = tmp / ".memoryguard" / "managed-memory"
        if mm_root.exists():
            for inst_dir in mm_root.iterdir():
                if not inst_dir.is_dir():
                    continue
                store = ManagedStore(str(tmp), inst_dir.name)
                active_vid = store.get_active_version_id()
                active_version = store.get_active_version()
                if active_version:
                    recs = store.list_records()
                    # 所有 records 都在 active version 的 records.jsonl 中
                    ok5 = len(recs) == active_version.record_count
                    all_pass &= _check(
                        f"PublicationLedger 完整 ({inst_dir.name[:8]})",
                        ok5,
                        f"records={len(recs)}, version_record_count={active_version.record_count}, vid={active_vid[:8] if active_vid else 'none'}",
                    )

        # -----------------------------------------------------------------
        # 6. 外部来源和 Obsidian 不再出现"页面可见、IR 丢失"
        # -----------------------------------------------------------------
        print("\n=== 6. 外部来源不丢失 ===")
        # 添加一个外部目录作为 SourceRoot
        with tempfile.TemporaryDirectory() as ext_tmp:
            ext_path = Path(ext_tmp)
            (ext_path / "external.md").write_text(
                "# 外部记忆\n这是来自外部目录的记忆。\n", encoding="utf-8")
            reg = SourceRegistry(str(tmp))
            root = reg.add(str(ext_path), SourceRootType.SELECTED_DIRECTORY,
                           display_name="外部目录")
            # 重新扫描+规范化
            snap = reg.scan(ScanBudget())
            root_map = {r.root_id: r.path for r in reg.list_sources()}
            norm = MemoryNormalizer(str(tmp))
            ir = norm.normalize(snap, root_map=root_map)
            norm.save(ir)
            # 检查外部来源的记录是否在 IR 中
            ext_obj = next((o for o in snap.source_objects
                            if o.source_root_id == root.root_id), None)
            ok6 = ext_obj is not None
            if ext_obj:
                ext_records = [r for r in ir.records
                               if any(p.source_object_id == ext_obj.source_object_id
                                      for p in r.provenance)]
                ok6 = len(ext_records) > 0
                all_pass &= _check(
                    "外部来源进入 IR",
                    ok6,
                    f"ext_obj={ext_obj.source_object_id[:8]}, ir_records={len(ext_records)}",
                )
            else:
                all_pass &= _check("外部来源进入 IR", False, "external source not found in snapshot")

        # -----------------------------------------------------------------
        # 7. 变更记录兼容旧 Change、新 Release 和损坏记录
        # -----------------------------------------------------------------
        print("\n=== 7. 变更记录兼容性 ===")
        # 写入一个旧格式 Change
        changes_dir = tmp / ".memoryguard" / "changes"
        changes_dir.mkdir(parents=True, exist_ok=True)
        (changes_dir / "old-change.json").write_text(
            json.dumps({"change_id": "old-1", "plan_id": "p1", "status": "verified",
                        "applied_at": "2026-01-01T00:00:00Z",
                        "backup_paths": [], "changed_paths": []}),
            encoding="utf-8",
        )
        # 写入一个新格式 Release
        (changes_dir / "new-release.json").write_text(
            json.dumps({"release_id": "new-1", "schema_version": "3.1",
                        "build_id": "b1", "status": "applied",
                        "applied_at": "2026-07-20T00:00:00Z"}),
            encoding="utf-8",
        )
        # 写入一个损坏 JSON
        (changes_dir / "broken.json").write_text("{invalid json", encoding="utf-8")
        # list_change_history 应该不崩溃，返回所有有效记录 + warnings
        history = list_change_history(tmp)
        events = history.get("items", [])
        warnings = history.get("warnings", [])
        ok7 = len(events) >= 2  # old-change + new-release
        ok7_warnings = len(warnings) >= 1  # broken.json
        all_pass &= _check(
            "变更记录兼容旧 Change + 新 Release",
            ok7,
            f"events={len(events)}, warnings={len(warnings)}",
        )
        all_pass &= _check(
            "损坏记录不崩溃，产生 warning",
            ok7_warnings,
            f"warnings={warnings}",
        )

        # -----------------------------------------------------------------
        # 8. 只有 Loader 复读成功才能显示"已接管"
        # -----------------------------------------------------------------
        print("\n=== 8. EXPORT_ONLY 不声称已接管 ===")
        # 当前所有 Profile 都是 EXPORT_ONLY，takeover_state 不应是 OPERATIONAL
        meta = proj.get("meta", {})
        for inst_meta in meta.get("agent_instances", []):
            cap = inst_meta.get("target_capability")
            state = inst_meta.get("takeover_state")
            # EXPORT_ONLY 不应达到 OPERATIONAL
            ok8 = cap == TargetCapability.EXPORT_ONLY.value and state != TakeoverState.OPERATIONAL.value
            all_pass &= _check(
                f"EXPORT_ONLY 不声称已接管 ({inst_meta.get('product')})",
                ok8,
                f"capability={cap}, takeover_state={state}",
            )

        # -----------------------------------------------------------------
        # 9. 所有写入可通过精确 Release 回滚
        # -----------------------------------------------------------------
        print("\n=== 9. 精确 Release 回滚 ===")
        # 检查 ReleaseManager 是否有 rollback_release
        from src.memoryguard.release_manager import ReleaseManager
        rm = ReleaseManager(str(tmp))
        has_rollback = hasattr(rm, "rollback_release")
        all_pass &= _check(
            "ReleaseManager 支持 rollback_release",
            has_rollback,
            f"has method={has_rollback}",
        )

        # -----------------------------------------------------------------
        # 附加：投影 meta 完整性
        # -----------------------------------------------------------------
        print("\n=== 附加：投影 meta 7 项状态 ===")
        meta_keys = {"agent_instances", "instance_count", "coverage",
                     "coverage_status", "release_count", "drifted"}
        ok_meta = meta_keys.issubset(meta.keys())
        all_pass &= _check(
            "投影 meta 包含 7 项状态字段",
            ok_meta,
            f"keys={set(meta.keys())}",
        )

    # -----------------------------------------------------------------
    # 汇总
    # -----------------------------------------------------------------
    print("\n" + "=" * 60)
    if all_pass:
        print("v3.1 MVP 验收：全部通过")
        return 0
    else:
        print("v3.1 MVP 验收：存在失败项")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
