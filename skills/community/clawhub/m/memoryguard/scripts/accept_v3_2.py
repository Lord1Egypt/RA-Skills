"""MemoryGuard v3.2 完整验收脚本（spec §12.1）。

逐项验证 10 个 P0 验收用例：
1. MCP 记忆后端启动
2. Agent 写入 MCP
3. 自动覆盖保留 supersedes
4. secret 自动 quarantine
5. Agent 卡片切换
6. 多 Agent 共享 MCP
7. GUI 不参与写入批准
8. 外部 MCP 未知 tool 不调用
9. AgentBinding 同一 share_group
10. 原生记忆未停用标记
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from memoryguard.gui import GovernanceApi
from memoryguard.mcp_server import TOOLS, execute_tool
from memoryguard.shared_memory_store import SharedMemoryStore
from memoryguard.auto_organizer import AutoOrganizer
from memoryguard.agent_binding import AgentBindingStore
from memoryguard.schema_v3 import (
    BindingStatus, NativeMemoryMode,
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
        api = GovernanceApi(str(workspace))
        group_id = "test-group"

        # -----------------------------------------------------------------
        # 1. MCP 记忆后端启动
        # -----------------------------------------------------------------
        print("\n=== 1. MCP 记忆后端启动 ===")
        tool_names = [t["name"] for t in TOOLS]
        required_tools = [
            "memoryguard_memory_read", "memoryguard_memory_search",
            "memoryguard_memory_write", "memoryguard_memory_update",
            "memoryguard_memory_delete", "memoryguard_memory_status",
        ]
        ok1 = all(t in tool_names for t in required_tools)
        all_pass &= _check("6 个 MCP tool 可用", ok1,
                           f"tools={[t for t in required_tools if t in tool_names]}")

        # -----------------------------------------------------------------
        # 2. Agent 写入 MCP
        # -----------------------------------------------------------------
        print("\n=== 2. Agent 写入 MCP ===")
        result = execute_tool("memoryguard_memory_write", {
            "body": "用户偏好简洁代码",
            "agent_instance_id": "claude-code-1",
            "workspace": str(workspace),
            "share_group_id": group_id,
        })
        content = result["content"][0]["text"]
        data = json.loads(content)
        ok2 = data["status"] == "active"
        all_pass &= _check("Agent 写入 -> active", ok2,
                           f"status={data['status']}, kind={data['kind']}")
        all_pass &= _check("自动整理执行", len(data.get("auto_actions", [])) > 0,
                           f"actions={data.get('auto_actions')}")

        # -----------------------------------------------------------------
        # 3. 自动覆盖保留 supersedes
        # -----------------------------------------------------------------
        print("\n=== 3. 自动覆盖保留 supersedes ===")
        # 先写入事实
        execute_tool("memoryguard_memory_write", {
            "body": "项目使用 Python 3.8",
            "agent_instance_id": "codex-1",
            "workspace": str(workspace),
            "share_group_id": group_id,
        })
        # 再写入纠错
        result_corr = execute_tool("memoryguard_memory_write", {
            "body": "纠正：项目使用 Python 3.10",
            "agent_instance_id": "codex-1",
            "workspace": str(workspace),
            "share_group_id": group_id,
        })
        corr_data = json.loads(result_corr["content"][0]["text"])
        store = SharedMemoryStore(workspace, group_id)
        # 检查是否有 shadowed 记录
        shadowed = store.list_records(status="shadowed")
        ok3a = len(shadowed) > 0
        all_pass &= _check("旧记忆 -> shadowed", ok3a,
                           f"shadowed_count={len(shadowed)}")
        # 检查新记忆的 supersedes
        new_record = store.get_record(corr_data["memory_id"])
        ok3b = new_record is not None and len(new_record.supersedes) > 0
        all_pass &= _check("新记忆 supersedes 非空", ok3b,
                           f"supersedes={new_record.supersedes if new_record else []}")
        # 检查 DecisionEvent
        decisions = store.list_decisions()
        ok3c = any(d.action == "auto_supersede" for d in decisions)
        all_pass &= _check("DecisionEvent(action=auto_supersede)", ok3c)

        # -----------------------------------------------------------------
        # 4. secret 自动 quarantine
        # -----------------------------------------------------------------
        print("\n=== 4. secret 自动 quarantine ===")
        result_secret = execute_tool("memoryguard_memory_write", {
            "body": "API_KEY=REDACTED-SECRET",
            "agent_instance_id": "test-agent",
            "workspace": str(workspace),
            "share_group_id": group_id,
        })
        secret_data = json.loads(result_secret["content"][0]["text"])
        ok4a = secret_data["status"] == "quarantined"
        all_pass &= _check("secret -> quarantine", ok4a,
                           f"status={secret_data['status']}")
        quarantine = store.list_quarantine()
        ok4b = len(quarantine) > 0
        all_pass &= _check("隔离队列非空", ok4b, f"count={len(quarantine)}")

        # -----------------------------------------------------------------
        # 5. Agent 卡片切换
        # -----------------------------------------------------------------
        print("\n=== 5. Agent 卡片切换 ===")
        # 创建测试文件模拟 Agent
        (workspace / "CLAUDE.md").write_text("# Claude\n", encoding="utf-8")
        (workspace / "AGENTS.md").write_text("# Codex\n", encoding="utf-8")
        agents_result = api.list_agents()
        agents = agents_result.get("agents", [])
        ok5 = len(agents) > 0
        all_pass &= _check("发现 Agent", ok5,
                           f"count={len(agents)}, products={[a['product'] for a in agents]}")
        if agents:
            # 切换到第一个 Agent
            agent_data = api.get_agent_data(agents[0]["instance_id"])
            ok5b = "agent" in agent_data and "categories" in agent_data
            all_pass &= _check("Agent 数据视图", ok5b,
                               f"categories={list(agent_data.get('categories', {}).keys())}")

        # -----------------------------------------------------------------
        # 6. 多 Agent 共享 MCP
        # -----------------------------------------------------------------
        print("\n=== 6. 多 Agent 共享 MCP ===")
        enter_result = api.enter_multi_agent_mode()
        ok6 = enter_result["mode"] == "multi_agent_shared_mcp"
        all_pass &= _check("进入多 Agent 模式", ok6)
        # 验证共享记忆存在
        status = api.get_memory_status(group_id)
        ok6b = status["share_group_id"] == group_id
        all_pass &= _check("共享记忆组存在", ok6b,
                           f"group={status['share_group_id']}, records={status['total_records']}")

        # -----------------------------------------------------------------
        # 7. GUI 不参与写入批准
        # -----------------------------------------------------------------
        print("\n=== 7. GUI 不参与写入批准 ===")
        # 验证 write API 没有 confirmed 参数
        import inspect
        sig = inspect.signature(api.list_memory)
        params = list(sig.parameters.keys())
        ok7 = "confirmed" not in params
        all_pass &= _check("GUI API 无 confirmed 参数", ok7,
                           f"list_memory params={params}")
        # 验证 write 是 MCP tool，不是 GUI API
        gui_methods = [m for m in dir(api) if "write" in m.lower() and not m.startswith("_")]
        ok7b = len(gui_methods) == 0
        all_pass &= _check("GUI 无 write 方法", ok7b, f"write_methods={gui_methods}")

        # -----------------------------------------------------------------
        # 8. 外部 MCP 未知 tool 不调用
        # -----------------------------------------------------------------
        print("\n=== 8. 外部 MCP 未知 tool 不调用 ===")
        from memoryguard.schema_v3 import ExternalMCPLevel
        external = api.detect_external_mcp("unknown-tools", {
            "display_name": "Unknown Tool Server",
            "tools": [{"name": "dangerous_export"}],
        })
        ok8 = external.get("level") == ExternalMCPLevel.L1_UNKNOWN_TOOLS.value
        all_pass &= _check("未知 tools -> L1", ok8, f"level={external.get('level')}")
        preview_external = api.preview_external_mcp_import("unknown-tools")
        ok8b = preview_external.get("unknown_tools_called") is False and preview_external.get("total") == 0
        all_pass &= _check("L1 只检测不抽取", ok8b, f"preview={preview_external}")

        # -----------------------------------------------------------------
        # 9. AgentBinding 同一 share_group
        # -----------------------------------------------------------------
        print("\n=== 9. AgentBinding 同一 share_group ===")
        binding_result = api.bind_agents_to_shared_group(
            ["agent-1", "agent-2"],
            share_group_id=group_id,
            native_memory_modes={"agent-1": "redirected", "agent-2": "observed"},
        )
        bindings = binding_result.get("bindings", [])
        ok9 = len(bindings) == 2 and all(b["share_group_id"] == group_id for b in bindings)
        all_pass &= _check("两个 binding 真实落盘并指向同一 share_group", ok9,
                           f"group={group_id}, count={len(bindings)}")
        binding_store = AgentBindingStore(workspace)
        persisted = binding_store.find_by_group(group_id, include_inactive=False)
        ok9b = len(persisted) >= 2
        all_pass &= _check("AgentBinding 文件可读回", ok9b, f"persisted={len(persisted)}")

        # -----------------------------------------------------------------
        # 10. 原生记忆未停用标记
        # -----------------------------------------------------------------
        print("\n=== 10. 原生记忆未停用标记 ===")
        binding1 = next(b for b in persisted if b.agent_instance_id == "agent-1")
        binding2 = next(b for b in persisted if b.agent_instance_id == "agent-2")
        ok10a = binding1.native_memory_mode == NativeMemoryMode.REDIRECTED
        all_pass &= _check("Agent 1 -> redirected (非 disabled)", ok10a,
                           f"mode={binding1.native_memory_mode.value}")
        ok10b = binding2.native_memory_mode == NativeMemoryMode.OBSERVED
        all_pass &= _check("Agent 2 -> observed (非 disabled)", ok10b,
                           f"mode={binding2.native_memory_mode.value}")
        ok10c = (binding1.native_memory_mode != NativeMemoryMode.DISABLED
                 and binding2.native_memory_mode != NativeMemoryMode.DISABLED)
        all_pass &= _check("未假装 disabled", ok10c)

        # -----------------------------------------------------------------
        # 附加：版本回滚
        # -----------------------------------------------------------------
        print("\n=== 附加：版本回滚 ===")
        vid = store.create_version_snapshot("pre-acceptance")
        ok_rollback = vid != ""
        all_pass &= _check("创建版本快照", ok_rollback, f"vid={vid[:8]}")
        store.rollback_to_version(vid)
        ok_rollback2 = store.get_active_version_id() == vid
        all_pass &= _check("回滚成功", ok_rollback2)

    # -----------------------------------------------------------------
    # 汇总
    # -----------------------------------------------------------------
    print("\n" + "=" * 60)
    if all_pass:
        print("v3.2 完整验收：全部通过")
        return 0
    else:
        print("v3.2 完整验收：存在失败项")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
