"""v3.2 文档萃取为共享记忆测试（两步流程：preview + accept_candidates）。"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from memoryguard.gui import GovernanceApi
from memoryguard.schema_v3 import SourceRootType
from memoryguard.shared_memory_store import SharedMemoryStore


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
        docs = workspace / "docs"
        docs.mkdir()
        doc = docs / "team.md"
        doc.write_text(
            "# 团队规则\n\n"
            "项目事实：MemoryGuard 共享事实源只有 MCP。\n\n"
            "## 偏好\n\n"
            "用户偏好后端先验收，GUI 最后做。\n\n"
            "随机日志，不应该整篇文档直接变成单条记忆。\n",
            encoding="utf-8",
        )
        api = GovernanceApi(str(workspace))
        added = api.add_source(str(docs), SourceRootType.SELECTED_DIRECTORY.value, "docs", confirmed=True)
        root_id = added["root_id"]

        print("\n=== 1. 文档可在数据页读取但未自动进入记忆 ===")
        content = api.get_source_file_content(root_id, "team.md")
        all_pass &= _check("源文件可读", "MemoryGuard 共享事实源" in content.get("content", ""))
        store = SharedMemoryStore(workspace, "doc-group")
        all_pass &= _check("萃取前共享记忆为空", len(store.list_records()) == 0)

        print("\n=== 2. 萃取预览（只读，不写入）===")
        preview = api.extract_preview(root_id, "team.md", max_segments=5)
        all_pass &= _check("预览成功", preview.get("ok") is True)
        all_pass &= _check("预览返回 extract_id", bool(preview.get("extract_id")))
        all_pass &= _check("至少预览两个候选", preview.get("total", 0) >= 2, f"total={preview.get('total')}")
        all_pass &= _check("预览不写入记忆", len(store.list_records()) == 0, "preview should not write")
        candidates = preview.get("candidates", [])
        all_pass &= _check("候选有 candidate_id", all(c.get("candidate_id") for c in candidates))
        all_pass &= _check("候选有 kind 分类", all(c.get("kind") for c in candidates))
        all_pass &= _check("候选有 risk_level", all(c.get("risk_level") for c in candidates))

        print("\n=== 3. 接受候选后进入 MCP 共享记忆 ===")
        extract_id = preview["extract_id"]
        candidate_ids = [c["candidate_id"] for c in candidates]
        accepted = api.accept_candidates(extract_id, candidate_ids, share_group_id="doc-group")
        all_pass &= _check("接受成功", accepted.get("ok") is True)
        all_pass &= _check("接受数量匹配", accepted.get("total", 0) >= 2, f"total={accepted.get('total')}")
        records = store.list_records()
        all_pass &= _check("共享记忆收到片段", len(records) >= 2, f"records={len(records)}")
        all_pass &= _check("不是整篇文档单条导入", all(len(r.body) < len(content["content"]) for r in records))
        events = store.list_events()
        all_pass &= _check("事件可回溯到 source file",
                           all(e.metadata.get("source_root_id") == root_id for e in events),
                           f"events={len(events)}")

        print("\n=== 4. staging 文件已清理 ===")
        all_pass &= _check("staging 已删除", not any(
            f.name == f"extract-{extract_id}.json"
            for f in (workspace / ".memoryguard" / "staging").glob("extract-*.json")
        ))

        print("\n=== 5. 越界路径被拒绝 ===")
        escaped = api.extract_preview(root_id, "../outside.md")
        all_pass &= _check("containment 生效", "error" in escaped)

        print("\n=== 6. 旧公开 API 已移除 ===")
        all_pass &= _check("extract_source_file_memories 已私有化",
                           not hasattr(api, "extract_source_file_memories"))

    print("\n" + "=" * 50)
    if all_pass:
        print("All v3.2 Document Extract tests PASSED")
        return 0
    print("Some Document Extract tests FAILED")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
