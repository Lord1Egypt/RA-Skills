"""v3.2 Schema round-trip 测试。

验证所有 v3.2 新增 dataclass 的 to_dict/from_dict 往返一致性。
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from memoryguard.schema_v3 import (
    AgentBinding, BindingStatus,
    MemoryEvent,
    SharedMemoryRecord, SharedMemoryStatus,
    ConflictGroup, ConflictResolution,
    QuarantineEntry,
    MemoryKind,
    NativeMemoryMode,
    DataPageMode,
    MemoryWritePolicy,
    ExternalMCPLevel,
    Provenance,
    stable_hash, _now_iso,
)


def _check(label: str, ok: bool, detail: str = "") -> bool:
    status = "PASS" if ok else "FAIL"
    msg = f"[{status}] {label}"
    if detail:
        msg += f" :: {detail}"
    print(msg)
    return ok


def test_agent_binding_round_trip() -> bool:
    """AgentBinding to_dict -> from_dict 一致。"""
    original = AgentBinding(
        binding_id=stable_hash("binding", "agent-1", "group-1"),
        agent_instance_id="agent-1",
        share_group_id="group-1",
        mcp_server_name="memoryguard",
        native_memory_mode=NativeMemoryMode.REDIRECTED,
        status=BindingStatus.ACTIVE,
        redirect_paths=["~/.claude/memory", "~/AGENTS.md"],
        bound_at=_now_iso(),
    )
    d = original.to_dict()
    restored = AgentBinding.from_dict(d)
    ok = (
        restored.binding_id == original.binding_id
        and restored.agent_instance_id == original.agent_instance_id
        and restored.share_group_id == original.share_group_id
        and restored.native_memory_mode == original.native_memory_mode
        and restored.status == original.status
        and restored.redirect_paths == original.redirect_paths
    )
    return _check("AgentBinding round-trip", ok)


def test_memory_event_round_trip() -> bool:
    """MemoryEvent to_dict -> from_dict 一致。"""
    original = MemoryEvent(
        event_id=stable_hash("event", "test", _now_iso()),
        agent_instance_id="agent-1",
        share_group_id="group-1",
        raw_content="用户偏好中文交流",
        metadata={"source": "claude-code", "session": "abc"},
        auto_actions=[{"action": "classify", "kind": "preference"}],
        created_at=_now_iso(),
    )
    d = original.to_dict()
    restored = MemoryEvent.from_dict(d)
    ok = (
        restored.event_id == original.event_id
        and restored.agent_instance_id == original.agent_instance_id
        and restored.raw_content == original.raw_content
        and restored.metadata == original.metadata
        and restored.auto_actions == original.auto_actions
    )
    return _check("MemoryEvent round-trip", ok)


def test_shared_memory_record_round_trip() -> bool:
    """SharedMemoryRecord to_dict -> from_dict 一致。"""
    original = SharedMemoryRecord(
        memory_id=stable_hash("mem", "test", _now_iso()),
        body="用户偏好简洁代码",
        kind=MemoryKind.PREFERENCE,
        status=SharedMemoryStatus.ACTIVE,
        confidence=0.85,
        provenance=[Provenance(
            source_object_id="src-1",
            locator="line:1-5",
            excerpt_hash=stable_hash("excerpt"),
        )],
        supersedes=["old-mem-1", "old-mem-2"],
        conflict_group_id="",
        locked=False,
        created_at=_now_iso(),
        updated_at=_now_iso(),
        agent_instance_id="agent-1",
    )
    d = original.to_dict()
    restored = SharedMemoryRecord.from_dict(d)
    ok = (
        restored.memory_id == original.memory_id
        and restored.body == original.body
        and restored.kind == original.kind
        and restored.status == original.status
        and restored.confidence == original.confidence
        and len(restored.provenance) == len(original.provenance)
        and restored.supersedes == original.supersedes
        and restored.locked == original.locked
        and restored.agent_instance_id == original.agent_instance_id
    )
    return _check("SharedMemoryRecord round-trip", ok)


def test_conflict_group_round_trip() -> bool:
    """ConflictGroup to_dict -> from_dict 一致。"""
    original = ConflictGroup(
        group_id=stable_hash("conflict", _now_iso()),
        member_ids=["mem-1", "mem-2", "mem-3"],
        reason="互斥：用户偏好中文 vs 英文",
        status=ConflictResolution.UNRESOLVED,
        created_at=_now_iso(),
    )
    d = original.to_dict()
    restored = ConflictGroup.from_dict(d)
    ok = (
        restored.group_id == original.group_id
        and restored.member_ids == original.member_ids
        and restored.reason == original.reason
        and restored.status == original.status
    )
    return _check("ConflictGroup round-trip", ok)


def test_quarantine_entry_round_trip() -> bool:
    """QuarantineEntry to_dict -> from_dict 一致。"""
    original = QuarantineEntry(
        quarantine_id=stable_hash("quar", _now_iso()),
        memory_id="mem-secret-1",
        reason="检测到 AWS Access Key",
        detected_pattern="AKIA[0-9A-Z]{16}",
        original_content="REDACTED-SECRET",
        quarantined_at=_now_iso(),
    )
    d = original.to_dict()
    restored = QuarantineEntry.from_dict(d)
    ok = (
        restored.quarantine_id == original.quarantine_id
        and restored.memory_id == original.memory_id
        and restored.reason == original.reason
        and restored.detected_pattern == original.detected_pattern
        and restored.original_content == original.original_content
        and restored.released == original.released
    )
    return _check("QuarantineEntry round-trip", ok)


def test_enum_values() -> bool:
    """验证 v3.2 枚举值。"""
    all_pass = True
    # DataPageMode
    all_pass &= _check("DataPageMode.SINGLE_AGENT",
                       DataPageMode.SINGLE_AGENT.value == "single_agent")
    all_pass &= _check("DataPageMode.MULTI_AGENT_SHARED_MCP",
                       DataPageMode.MULTI_AGENT_SHARED_MCP.value == "multi_agent_shared_mcp")

    # MemoryWritePolicy
    all_pass &= _check("MemoryWritePolicy.AUTO_ACCEPT",
                       MemoryWritePolicy.AUTO_ACCEPT.value == "auto_accept")
    all_pass &= _check("MemoryWritePolicy.PROPOSE_ONLY",
                       MemoryWritePolicy.PROPOSE_ONLY.value == "propose_only")

    # NativeMemoryMode
    all_pass &= _check("NativeMemoryMode.DISABLED",
                       NativeMemoryMode.DISABLED.value == "disabled")
    all_pass &= _check("NativeMemoryMode.REDIRECTED",
                       NativeMemoryMode.REDIRECTED.value == "redirected")
    all_pass &= _check("NativeMemoryMode.OBSERVED",
                       NativeMemoryMode.OBSERVED.value == "observed")
    all_pass &= _check("NativeMemoryMode.UNSUPPORTED",
                       NativeMemoryMode.UNSUPPORTED.value == "unsupported")

    # SharedMemoryStatus
    all_pass &= _check("SharedMemoryStatus.ACTIVE",
                       SharedMemoryStatus.ACTIVE.value == "active")
    all_pass &= _check("SharedMemoryStatus.SHADOWED",
                       SharedMemoryStatus.SHADOWED.value == "shadowed")
    all_pass &= _check("SharedMemoryStatus.CONFLICTED",
                       SharedMemoryStatus.CONFLICTED.value == "conflicted")
    all_pass &= _check("SharedMemoryStatus.QUARANTINED",
                       SharedMemoryStatus.QUARANTINED.value == "quarantined")
    all_pass &= _check("SharedMemoryStatus.DELETED",
                       SharedMemoryStatus.DELETED.value == "deleted")

    # MemoryKind.CORRECTION
    all_pass &= _check("MemoryKind.CORRECTION",
                       MemoryKind.CORRECTION.value == "correction")

    # ExternalMCPLevel
    all_pass &= _check("ExternalMCPLevel.L0",
                       ExternalMCPLevel.L0_UNRECOGNIZABLE.value == "L0_unrecognizable")
    all_pass &= _check("ExternalMCPLevel.L1",
                       ExternalMCPLevel.L1_UNKNOWN_TOOLS.value == "L1_unknown_tools")
    all_pass &= _check("ExternalMCPLevel.L4",
                       ExternalMCPLevel.L4_MEMORYGUARD_MCP.value == "L4_memoryguard_mcp")

    return all_pass


def test_supersede_chain() -> bool:
    """验证覆盖链：old.status=SHADOWED, new.supersedes=[old_id]。"""
    old_mem = SharedMemoryRecord(
        memory_id="old-1",
        body="旧记忆",
        kind=MemoryKind.FACT,
        status=SharedMemoryStatus.ACTIVE,
    )
    new_mem = SharedMemoryRecord(
        memory_id="new-1",
        body="纠正后的新记忆",
        kind=MemoryKind.CORRECTION,
        status=SharedMemoryStatus.ACTIVE,
        supersedes=["old-1"],
    )
    # 模拟 supersede 动作
    old_mem.status = SharedMemoryStatus.SHADOWED

    ok = (
        old_mem.status == SharedMemoryStatus.SHADOWED
        and new_mem.supersedes == ["old-1"]
        and new_mem.kind == MemoryKind.CORRECTION
    )
    return _check("supersede chain (old=shadowed, new.supersedes=[old_id])", ok)


def main() -> int:
    print("=== v3.2 Schema Round-Trip Tests ===\n")
    all_pass = True
    all_pass &= test_enum_values()
    print()
    all_pass &= test_agent_binding_round_trip()
    all_pass &= test_memory_event_round_trip()
    all_pass &= test_shared_memory_record_round_trip()
    all_pass &= test_conflict_group_round_trip()
    all_pass &= test_quarantine_entry_round_trip()
    all_pass &= test_supersede_chain()

    print("\n" + "=" * 50)
    if all_pass:
        print("All v3.2 schema tests PASSED")
        return 0
    else:
        print("Some tests FAILED")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
