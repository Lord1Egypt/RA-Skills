"""v3.2 AgentBinding 落盘与共享组绑定后端。"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .schema_v3 import (
    AgentBinding,
    BindingStatus,
    NativeMemoryMode,
    stable_hash,
    _now_iso,
)
from .shared_memory_store import SharedMemoryStore


class AgentBindingStore:
    def __init__(self, workspace: str | Path):
        self.workspace = Path(workspace).resolve()
        self.root = self.workspace / ".memoryguard" / "agent-bindings"
        self.ledger_path = self.root / "ledger.jsonl"

    def _ensure_dirs(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)

    def _binding_path(self, binding_id: str) -> Path:
        return self.root / f"{binding_id}.json"

    def list_bindings(self, include_inactive: bool = True) -> list[AgentBinding]:
        if not self.root.exists():
            return []
        bindings: list[AgentBinding] = []
        for path in sorted(self.root.glob("*.json")):
            try:
                binding = AgentBinding.from_dict(json.loads(path.read_text(encoding="utf-8")))
            except (ValueError, KeyError):
                continue
            if not include_inactive and binding.status == BindingStatus.INACTIVE:
                continue
            bindings.append(binding)
        return bindings

    def get_binding(self, binding_id: str) -> AgentBinding | None:
        path = self._binding_path(binding_id)
        if not path.exists():
            return None
        try:
            return AgentBinding.from_dict(json.loads(path.read_text(encoding="utf-8")))
        except (ValueError, KeyError):
            return None

    def find_by_agent(self, agent_instance_id: str, include_inactive: bool = False) -> list[AgentBinding]:
        return [
            b for b in self.list_bindings(include_inactive=include_inactive)
            if b.agent_instance_id == agent_instance_id
        ]

    def find_by_group(self, share_group_id: str, include_inactive: bool = True) -> list[AgentBinding]:
        return [
            b for b in self.list_bindings(include_inactive=include_inactive)
            if b.share_group_id == share_group_id
        ]

    def bind_agent(self, agent_instance_id: str, share_group_id: str,
                   mcp_server_name: str = "memoryguard",
                   native_memory_mode: str | NativeMemoryMode = NativeMemoryMode.OBSERVED,
                   redirect_paths: list[str] | None = None) -> AgentBinding:
        mode = self._native_mode(native_memory_mode)
        binding_id = stable_hash("binding", agent_instance_id, share_group_id, mcp_server_name)
        now = _now_iso()
        binding = AgentBinding(
            binding_id=binding_id,
            agent_instance_id=agent_instance_id,
            share_group_id=share_group_id,
            mcp_server_name=mcp_server_name,
            native_memory_mode=mode,
            status=BindingStatus.ACTIVE,
            redirect_paths=list(redirect_paths or []),
            bound_at=now,
            last_drift_check="",
        )
        self._write_binding(binding)
        self._append_ledger("bind_agent", binding, {"redirect_path_count": len(binding.redirect_paths)})
        SharedMemoryStore(self.workspace, share_group_id)._ensure_dirs()
        return binding

    def bind_agents_to_group(self, agent_instance_ids: list[str], share_group_id: str = "",
                             mcp_server_name: str = "memoryguard",
                             native_memory_modes: dict[str, str] | None = None,
                             redirect_paths: dict[str, list[str]] | None = None) -> dict[str, Any]:
        clean_agents = [a for a in dict.fromkeys(agent_instance_ids) if a]
        group_id = share_group_id or self.create_share_group_id(clean_agents)
        modes = native_memory_modes or {}
        paths = redirect_paths or {}
        bindings = []
        for agent_id in clean_agents:
            binding = self.bind_agent(
                agent_instance_id=agent_id,
                share_group_id=group_id,
                mcp_server_name=mcp_server_name,
                native_memory_mode=modes.get(agent_id, NativeMemoryMode.OBSERVED.value),
                redirect_paths=paths.get(agent_id, []),
            )
            bindings.append(binding)
        store = SharedMemoryStore(self.workspace, group_id)
        return {
            "ok": True,
            "share_group_id": group_id,
            "bindings": [b.to_dict() for b in bindings],
            "preview": self.shared_group_preview(group_id, store),
        }

    def unbind_agent(self, binding_id: str) -> AgentBinding | None:
        binding = self.get_binding(binding_id)
        if binding is None:
            return None
        binding.status = BindingStatus.INACTIVE
        self._write_binding(binding)
        self._append_ledger("unbind_agent", binding, {})
        return binding

    def check_drift(self, binding_id: str) -> dict[str, Any]:
        binding = self.get_binding(binding_id)
        if binding is None:
            return {"error": f"binding not found: {binding_id}"}
        missing_paths = [p for p in binding.redirect_paths if p and not Path(p).exists()]
        status = BindingStatus.DRIFTED if missing_paths else BindingStatus.ACTIVE
        binding.status = status
        binding.last_drift_check = _now_iso()
        self._write_binding(binding)
        result = {
            "binding_id": binding.binding_id,
            "agent_instance_id": binding.agent_instance_id,
            "share_group_id": binding.share_group_id,
            "status": binding.status.value,
            "missing_redirect_paths": missing_paths,
            "checked_at": binding.last_drift_check,
        }
        self._append_ledger("check_drift", binding, result)
        return result

    def shared_group_preview(self, share_group_id: str,
                             store: SharedMemoryStore | None = None) -> dict[str, Any]:
        memory_store = store or SharedMemoryStore(self.workspace, share_group_id)
        bindings = self.find_by_group(share_group_id, include_inactive=False)
        status = memory_store.status()
        backup_root = self.workspace / ".memoryguard" / "native-memory"
        backup_status = []
        for binding in bindings:
            baseline = backup_root / binding.agent_instance_id / "baseline-backup"
            backup_status.append({
                "agent_instance_id": binding.agent_instance_id,
                "native_memory_mode": binding.native_memory_mode.value,
                "binding_status": binding.status.value,
                "baseline_backup_exists": baseline.exists(),
                "baseline_backup_path": str(baseline),
            })
        return {
            "share_group_id": share_group_id,
            "agent_count": len(bindings),
            "bindings": [b.to_dict() for b in bindings],
            "native_memory_backups": backup_status,
            "memory_status": status,
            "auto_write_count": status.get("total_events", 0),
            "auto_decision_count": status.get("total_decisions", 0),
            "conflict_count": status.get("total_conflicts", 0),
            "quarantine_count": status.get("total_quarantine", 0),
        }

    def create_share_group_id(self, agent_instance_ids: list[str]) -> str:
        normalized = sorted(a for a in agent_instance_ids if a)
        seed = "|".join(normalized) or _now_iso()
        return "shared-" + stable_hash("share_group", seed)

    def _write_binding(self, binding: AgentBinding) -> None:
        self._ensure_dirs()
        self._binding_path(binding.binding_id).write_text(
            json.dumps(binding.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _append_ledger(self, action: str, binding: AgentBinding, detail: dict[str, Any]) -> None:
        self._ensure_dirs()
        event = {
            "event_id": stable_hash("binding_event", action, binding.binding_id, _now_iso()),
            "action": action,
            "binding_id": binding.binding_id,
            "agent_instance_id": binding.agent_instance_id,
            "share_group_id": binding.share_group_id,
            "status": binding.status.value,
            "detail": dict(detail),
            "created_at": _now_iso(),
        }
        with self.ledger_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

    def _native_mode(self, value: str | NativeMemoryMode) -> NativeMemoryMode:
        if isinstance(value, NativeMemoryMode):
            return value
        try:
            return NativeMemoryMode(value)
        except ValueError:
            return NativeMemoryMode.UNSUPPORTED
