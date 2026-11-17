"""v3.2 外部 MCP 检测/导入测试。"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from memoryguard.gui import GovernanceApi
from memoryguard.schema_v3 import ExternalMCPLevel
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
        api = GovernanceApi(str(workspace))

        print("\n=== 1. L1 未知 tools 只检测不调用 ===")
        l1 = api.detect_external_mcp("unknown-tools", {
            "display_name": "Unknown Tool Server",
            "tools": [{"name": "dangerous_export"}],
        })
        all_pass &= _check("L1 分级", l1.get("level") == ExternalMCPLevel.L1_UNKNOWN_TOOLS.value,
                           f"level={l1.get('level')}")
        preview_l1 = api.preview_external_mcp_import("unknown-tools")
        all_pass &= _check("未知 tool 未调用", preview_l1.get("unknown_tools_called") is False)
        all_pass &= _check("L1 不自动抽取", preview_l1.get("total") == 0, f"total={preview_l1.get('total')}")

        print("\n=== 2. L2 resources 预览后导入 ===")
        l2_descriptor = {
            "display_name": "Resource Server",
            "resources": [{
                "name": "team-memory.md",
                "uri": "memory://team",
                "text": "团队偏好先写后端验收，再做 GUI。",
            }],
        }
        l2 = api.detect_external_mcp("resource-server", l2_descriptor)
        all_pass &= _check("L2 分级", l2.get("level") == ExternalMCPLevel.L2_GENERIC_RESOURCES.value,
                           f"level={l2.get('level')}")
        preview_l2 = api.preview_external_mcp_import("resource-server")
        entries = preview_l2.get("preview_entries", [])
        all_pass &= _check("L2 生成预览条目", len(entries) == 1, f"count={len(entries)}")
        imported = api.import_external_mcp_entries("resource-server", "shared-team", entries)
        all_pass &= _check("L2 导入成功", imported.get("total") == 1, f"total={imported.get('total')}")
        store = SharedMemoryStore(workspace, "shared-team")
        records = store.list_records()
        all_pass &= _check("导入进入共享记忆", len(records) == 1, f"records={len(records)}")
        events = store.list_events()
        all_pass &= _check("导入保留 external metadata",
                           events and events[0].metadata.get("external_mcp_server_id") == "resource-server")

        print("\n=== 3. L3 已知 memory MCP 基于提供 entries 预览 ===")
        l3 = api.detect_external_mcp("known-memory", {
            "display_name": "Known Memory",
            "tools": [{"name": "memory_search"}],
            "memory_entries": [{"body": "项目事实：MemoryGuard 共享事实源是 MCP。"}],
        })
        preview_l3 = api.preview_external_mcp_import("known-memory")
        all_pass &= _check("L3 分级", l3.get("level") == ExternalMCPLevel.L3_KNOWN_MEMORY_MCP.value)
        all_pass &= _check("L3 只读预览 entries", preview_l3.get("total") == 1, f"total={preview_l3.get('total')}")

        print("\n=== 4. servers.json 落盘 ===")
        servers_file = workspace / ".memoryguard" / "external-mcp" / "servers.json"
        all_pass &= _check("servers.json 存在", servers_file.exists(), str(servers_file))
        listed = api.list_external_mcp_servers()
        all_pass &= _check("可列出外部 MCP", listed.get("total", 0) >= 3, f"total={listed.get('total')}")

    print("\n" + "=" * 50)
    if all_pass:
        print("All v3.2 External MCP tests PASSED")
        return 0
    print("Some External MCP tests FAILED")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
