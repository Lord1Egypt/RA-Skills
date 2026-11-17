"""v3.2 端到端测试：MCP 记忆后端完整流程。

测试内容：
1. 写入普通记忆 -> active 状态
2. 写入含 secret 的记忆 -> quarantine 状态
3. 写入纠错记忆 -> supersede 旧记录
4. 查询 status -> 统计正确
5. 读取单条记忆
6. 搜索记忆
7. 软删除记忆
8. 版本快照 + 回滚
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from memoryguard.shared_memory_store import SharedMemoryStore
from memoryguard.auto_organizer import AutoOrganizer
from memoryguard.schema_v3 import (
    MemoryEvent, SharedMemoryStatus, MemoryKind,
    stable_hash, _now_iso,
)


def _check(label: str, ok: bool, detail: str = "") -> bool:
    status = "PASS" if ok else "FAIL"
    msg = f"[{status}] {label}"
    if detail:
        msg += f" :: {detail}"
    print(msg)
    return ok


def main() -> int:
    all_pass = True
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp)
        group_id = "test-group"

        # --- 1. 写入普通记忆 ---
        print("\n=== 1. 写入普通记忆 ===")
        store = SharedMemoryStore(workspace, group_id)
        organizer = AutoOrganizer(workspace, group_id)

        event1 = MemoryEvent(
            event_id=stable_hash("event", "pref1", _now_iso()),
            agent_instance_id="claude-code-1",
            share_group_id=group_id,
            raw_content="用户偏好中文交流",
            metadata={}, auto_actions=[], created_at=_now_iso(),
        )
        store.append_event(event1)
        record1, actions1 = organizer.organize(event1)
        event1.auto_actions = actions1
        store.update_event(event1)
        ok1 = record1.status == SharedMemoryStatus.ACTIVE
        all_pass &= _check("普通记忆 -> active", ok1,
                           f"status={record1.status.value}, kind={record1.kind.value}")
        all_pass &= _check("分类为 preference", record1.kind == MemoryKind.PREFERENCE)

        # --- 2. 写入含 secret 的记忆 -> quarantine ---
        print("\n=== 2. 写入含 secret 的记忆 ===")
        event2 = MemoryEvent(
            event_id=stable_hash("event", "secret1", _now_iso()),
            agent_instance_id="claude-code-1",
            share_group_id=group_id,
            raw_content="API_KEY=REDACTED-SECRET",
            metadata={}, auto_actions=[], created_at=_now_iso(),
        )
        store.append_event(event2)
        record2, actions2 = organizer.organize(event2)
        event2.auto_actions = actions2
        store.update_event(event2)
        ok2 = record2.status == SharedMemoryStatus.QUARANTINED
        all_pass &= _check("secret 记忆 -> quarantine", ok2,
                           f"status={record2.status.value}")
        quarantine_list = store.list_quarantine()
        all_pass &= _check("隔离队列有 1 条", len(quarantine_list) == 1,
                           f"count={len(quarantine_list)}")

        # --- 3. 写入纠错记忆 -> supersede ---
        print("\n=== 3. 写入纠错记忆 -> supersede ===")
        # 先写入一条事实
        event3a = MemoryEvent(
            event_id=stable_hash("event", "fact1", _now_iso()),
            agent_instance_id="codex-1",
            share_group_id=group_id,
            raw_content="项目使用 Python 3.8",
            metadata={}, auto_actions=[], created_at=_now_iso(),
        )
        store.append_event(event3a)
        record3a, actions3a = organizer.organize(event3a)
        event3a.auto_actions = actions3a
        store.update_event(event3a)
        # 再写入纠错
        event3b = MemoryEvent(
            event_id=stable_hash("event", "correction1", _now_iso()),
            agent_instance_id="codex-1",
            share_group_id=group_id,
            raw_content="纠正：项目使用 Python 3.10",
            metadata={}, auto_actions=[], created_at=_now_iso(),
        )
        store.append_event(event3b)
        record3b, actions3b = organizer.organize(event3b)
        event3b.auto_actions = actions3b
        store.update_event(event3b)
        # 检查 supersede
        old_record = store.get_record(record3a.memory_id)
        new_record = store.get_record(record3b.memory_id)
        ok3a = old_record is not None and old_record.status == SharedMemoryStatus.SHADOWED
        ok3b = new_record is not None and record3a.memory_id in new_record.supersedes
        all_pass &= _check("旧记忆 -> shadowed", ok3a,
                           f"old_status={old_record.status.value if old_record else 'None'}")
        all_pass &= _check("新记忆 supersedes 含旧 ID", ok3b,
                           f"supersedes={new_record.supersedes if new_record else []}")

        # --- 4. 查询 status ---
        print("\n=== 4. 查询 status ===")
        status = store.status()
        print(f"  status: {json.dumps(status, indent=2)}")
        all_pass &= _check("active >= 2", status["active"] >= 2, f"active={status['active']}")
        all_pass &= _check("quarantined >= 1", status["quarantined"] >= 1, f"quarantined={status['quarantined']}")
        all_pass &= _check("shadowed >= 1", status["shadowed"] >= 1, f"shadowed={status['shadowed']}")
        all_pass &= _check("total_events >= 4", status["total_events"] >= 4, f"events={status['total_events']}")

        # --- 5. 读取单条记忆 ---
        print("\n=== 5. 读取单条记忆 ===")
        found = store.get_record(record1.memory_id)
        all_pass &= _check("读取记忆", found is not None and found.body == "用户偏好中文交流")

        # --- 6. 搜索记忆 ---
        print("\n=== 6. 搜索记忆 ===")
        results = store.list_records(status="active")
        python_results = [r for r in results if "python" in r.body.lower() or "Python" in r.body]
        all_pass &= _check("搜索 'Python' 记忆", len(python_results) >= 1,
                           f"found={len(python_results)}")

        # --- 7. 软删除记忆 ---
        print("\n=== 7. 软删除记忆 ===")
        store.delete(record1.memory_id)
        deleted = store.get_record(record1.memory_id)
        all_pass &= _check("软删除 -> deleted",
                           deleted is not None and deleted.status == SharedMemoryStatus.DELETED)

        # --- 8. 版本快照 + 回滚 ---
        print("\n=== 8. 版本快照 + 回滚 ===")
        vid = store.create_version_snapshot("pre-test")
        all_pass &= _check("创建版本快照", vid != "")
        # 删除一条记忆
        store.delete(record3b.memory_id)
        after_delete = store.get_record(record3b.memory_id)
        all_pass &= _check("删除后 status=deleted",
                           after_delete is not None and after_delete.status == SharedMemoryStatus.DELETED)
        # 回滚
        store.rollback_to_version(vid)
        restored = store.get_record(record3b.memory_id)
        all_pass &= _check("回滚后记忆恢复",
                           restored is not None and restored.status != SharedMemoryStatus.DELETED,
                           f"status={restored.status.value if restored else 'None'}")

        # --- 9. 治理动作测试 ---
        print("\n=== 9. 治理动作测试 ===")
        # 锁定
        store.lock(record3b.memory_id)
        locked_rec = store.get_record(record3b.memory_id)
        all_pass &= _check("锁定记忆", locked_rec is not None and locked_rec.locked)
        # 解锁
        store.unlock(record3b.memory_id)
        unlocked_rec = store.get_record(record3b.memory_id)
        all_pass &= _check("解锁记忆", unlocked_rec is not None and not unlocked_rec.locked)
        # 恢复 shadowed
        store.restore(record3a.memory_id)
        restored_rec = store.get_record(record3a.memory_id)
        all_pass &= _check("恢复 shadowed -> active",
                           restored_rec is not None and restored_rec.status == SharedMemoryStatus.ACTIVE)
        # 编辑
        store.edit(record3b.memory_id, "编辑后的内容")
        edited_rec = store.get_record(record3b.memory_id)
        all_pass &= _check("编辑记忆", edited_rec is not None and edited_rec.body == "编辑后的内容")

    # --- 汇总 ---
    print("\n" + "=" * 50)
    if all_pass:
        print("All v3.2 end-to-end tests PASSED")
        return 0
    else:
        print("Some tests FAILED")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
