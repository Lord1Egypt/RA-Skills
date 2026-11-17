"""v3.2 AutoOrganizer 增强治理测试。"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from memoryguard.auto_organizer import AutoOrganizer
from memoryguard.schema_v3 import MemoryEvent, SharedMemoryStatus, stable_hash, _now_iso
from memoryguard.shared_memory_store import SharedMemoryStore


def _check(label: str, ok: bool, detail: str = "") -> bool:
    status = "PASS" if ok else "FAIL"
    msg = f"[{status}] {label}"
    if detail:
        msg += f" :: {detail}"
    print(msg)
    return ok


def _event(body: str, agent: str = "agent") -> MemoryEvent:
    return MemoryEvent(
        event_id=stable_hash("event", body, _now_iso()),
        agent_instance_id=agent,
        share_group_id="group",
        raw_content=body,
        metadata={},
        auto_actions=[],
        created_at=_now_iso(),
    )


def _write(store: SharedMemoryStore, organizer: AutoOrganizer, body: str) -> tuple[object, list[dict]]:
    event = _event(body)
    store.append_event(event)
    record, actions = organizer.organize(event)
    event.auto_actions = actions
    store.update_event(event)
    return record, actions


def main() -> int:
    all_pass = True
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp)
        store = SharedMemoryStore(workspace, "group")
        organizer = AutoOrganizer(workspace, "group")

        print("\n=== 1. 低置信度隔离出 active ===")
        low, actions_low = _write(store, organizer, "也许")
        all_pass &= _check("短且不确定 -> low_confidence", low.status == SharedMemoryStatus.LOW_CONFIDENCE,
                           f"status={low.status.value}, actions={actions_low}")

        print("\n=== 2. 重复内容合并 provenance ===")
        first, _ = _write(store, organizer, "用户偏好中文交流")
        second, actions_second = _write(store, organizer, "用户偏好中文交流")
        merged = store.get_record(first.memory_id)
        all_pass &= _check("重复返回同一代表记录", second.memory_id == first.memory_id)
        all_pass &= _check("provenance 增加", merged is not None and len(merged.provenance) >= 2,
                           f"provenance={len(merged.provenance) if merged else 0}")
        all_pass &= _check("记录 merge_provenance 动作", any(a.get("action") == "merge_provenance" for a in actions_second))

        print("\n=== 3. 长事件压缩 ===")
        long_body = "\n".join(["普通噪声" * 220, "项目事实：长文中应该保留这个事实。", "更多噪声" * 220])
        compressed, actions_compress = _write(store, organizer, long_body)
        all_pass &= _check("长事件被压缩", len(compressed.body) < len(long_body),
                           f"before={len(long_body)}, after={len(compressed.body)}")
        all_pass &= _check("记录 compress 动作", any(a.get("action") == "compress" for a in actions_compress))

        print("\n=== 4. 重复偏好衍生 durable preference ===")
        _write(store, organizer, "用户偏好先写测试再写实现")
        _write(store, organizer, "用户偏好先写测试再写实现，并保持最小改动")
        derived, actions_derive = _write(store, organizer, "用户偏好先写测试再写实现，然后做验收")
        all_pass &= _check("产生 derive 动作", any(a.get("action") == "derive" for a in actions_derive),
                           f"actions={actions_derive}")
        all_pass &= _check("衍生记忆保持 active", derived.status == SharedMemoryStatus.ACTIVE,
                           f"status={derived.status.value}")

    print("\n" + "=" * 50)
    if all_pass:
        print("All v3.2 AutoOrganizer enhanced tests PASSED")
        return 0
    print("Some AutoOrganizer enhanced tests FAILED")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
