"""v3.2 AgentBinding 落盘与多 Agent 共享组测试。"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from memoryguard.agent_binding import AgentBindingStore
from memoryguard.gui import GovernanceApi
from memoryguard.schema_v3 import BindingStatus, NativeMemoryMode


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
        store = AgentBindingStore(workspace)
        api = GovernanceApi(str(workspace))

        print("\n=== 1. 单 Agent binding 落盘 ===")
        redirect_file = workspace / "AGENTS.md"
        redirect_file.write_text("# test\n", encoding="utf-8")
        binding = store.bind_agent(
            agent_instance_id="codex-1",
            share_group_id="solo-codex",
            native_memory_mode=NativeMemoryMode.REDIRECTED,
            redirect_paths=[str(redirect_file)],
        )
        binding_path = workspace / ".memoryguard" / "agent-bindings" / f"{binding.binding_id}.json"
        all_pass &= _check("binding json 存在", binding_path.exists(), str(binding_path))
        loaded = store.get_binding(binding.binding_id)
        all_pass &= _check("binding 可读回", loaded is not None and loaded.agent_instance_id == "codex-1")
        ledger = workspace / ".memoryguard" / "agent-bindings" / "ledger.jsonl"
        all_pass &= _check("binding ledger 存在", ledger.exists() and "bind_agent" in ledger.read_text(encoding="utf-8"))

        print("\n=== 2. 多 Agent 共享组绑定 ===")
        result = api.bind_agents_to_shared_group(
            ["codex-1", "claude-code-1"],
            share_group_id="team-alpha",
            native_memory_modes={
                "codex-1": "redirected",
                "claude-code-1": "observed",
            },
            redirect_paths={
                "codex-1": [str(redirect_file)],
                "claude-code-1": [],
            },
        )
        bindings = result.get("bindings", [])
        all_pass &= _check("两个 Agent 绑定成功", len(bindings) == 2, f"count={len(bindings)}")
        all_pass &= _check("同一 share_group", all(b["share_group_id"] == "team-alpha" for b in bindings))
        shared_dir = workspace / ".memoryguard" / "shared-memory" / "team-alpha"
        all_pass &= _check("共享记忆组目录存在", shared_dir.exists(), str(shared_dir))
        preview = api.get_shared_group_preview("team-alpha")
        all_pass &= _check("共享预览含两个 Agent", preview.get("agent_count") == 2, f"preview={preview.get('agent_count')}")
        all_pass &= _check("预览含自动写入统计", "auto_write_count" in preview)

        print("\n=== 3. 漂移检测 ===")
        missing = workspace / "missing.md"
        drift_binding = api.bind_agent(
            "windsurf-1", "team-alpha", native_memory_mode="observed",
            redirect_paths=[str(missing)],
        )["binding"]
        drift = api.check_binding_drift(drift_binding["binding_id"])
        all_pass &= _check("缺失 redirect path -> drifted", drift.get("status") == BindingStatus.DRIFTED.value,
                           f"status={drift.get('status')}")
        active_check = api.check_binding_drift(binding.binding_id)
        all_pass &= _check("存在 redirect path -> active", active_check.get("status") == BindingStatus.ACTIVE.value,
                           f"status={active_check.get('status')}")

        print("\n=== 4. 解绑 ===")
        unbound = api.unbind_agent(drift_binding["binding_id"])
        all_pass &= _check("解绑成功", unbound.get("binding", {}).get("status") == BindingStatus.INACTIVE.value)
        active_bindings = api.list_bindings(include_inactive=False).get("bindings", [])
        all_pass &= _check("active 列表不含已解绑", all(b["binding_id"] != drift_binding["binding_id"] for b in active_bindings))

    print("\n" + "=" * 50)
    if all_pass:
        print("All v3.2 AgentBinding tests PASSED")
        return 0
    print("Some AgentBinding tests FAILED")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
