"""v3.2 外部 MCP 记忆后端检测与导入。"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .auto_organizer import AutoOrganizer
from .schema_v3 import ExternalMCPLevel, MemoryEvent, stable_hash, _now_iso
from .shared_memory_store import SharedMemoryStore


class ExternalMCPDetector:
    def __init__(self, workspace: str | Path):
        self.workspace = Path(workspace).resolve()
        self.root = self.workspace / ".memoryguard" / "external-mcp"
        self.servers_path = self.root / "servers.json"
        self.imports_dir = self.root / "imports"

    def _ensure_dirs(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        self.imports_dir.mkdir(parents=True, exist_ok=True)

    def list_servers(self) -> list[dict[str, Any]]:
        if not self.servers_path.exists():
            return []
        try:
            data = json.loads(self.servers_path.read_text(encoding="utf-8"))
        except ValueError:
            return []
        return list(data.get("servers", []))

    def detect_server(self, server_id: str, descriptor: dict[str, Any]) -> dict[str, Any]:
        self._ensure_dirs()
        tools = list(descriptor.get("tools", []))
        resources = list(descriptor.get("resources", []))
        tool_names = [self._name(t).lower() for t in tools]
        resource_names = [self._name(r).lower() for r in resources]
        level = self._classify(descriptor, tool_names, resource_names)
        result = {
            "server_id": server_id,
            "display_name": descriptor.get("display_name", server_id),
            "level": level.value,
            "tool_count": len(tools),
            "resource_count": len(resources),
            "safe_to_auto_call_tools": False,
            "import_strategy": self._strategy(level),
            "detected_at": _now_iso(),
            "descriptor": descriptor,
        }
        self._upsert_server(result)
        return result

    def preview_import(self, server_id: str, descriptor: dict[str, Any] | None = None) -> dict[str, Any]:
        server = self._server(server_id)
        if descriptor is not None:
            server = self.detect_server(server_id, descriptor)
        if server is None:
            return {"error": f"external MCP server not found: {server_id}"}
        level = ExternalMCPLevel(server["level"])
        desc = dict(server.get("descriptor", {}))
        resources = list(desc.get("resources", []))
        provided_entries = list(desc.get("memory_entries", []))
        preview_entries = []
        if level in (ExternalMCPLevel.L4_MEMORYGUARD_MCP, ExternalMCPLevel.L3_KNOWN_MEMORY_MCP):
            for item in provided_entries:
                body = str(item.get("body", "")).strip()
                if body:
                    preview_entries.append({
                        "body": body,
                        "metadata": dict(item.get("metadata", {})),
                        "source": "provided_memory_entry",
                    })
        if level == ExternalMCPLevel.L2_GENERIC_RESOURCES:
            for resource in resources:
                text = str(resource.get("text", resource.get("content", ""))).strip()
                if text:
                    preview_entries.append({
                        "body": text,
                        "metadata": {"uri": resource.get("uri", ""), "name": resource.get("name", "")},
                        "source": "provided_resource_content",
                    })
        return {
            "server_id": server_id,
            "level": level.value,
            "unknown_tools_called": False,
            "preview_entries": preview_entries,
            "total": len(preview_entries),
            "import_strategy": self._strategy(level),
        }

    def import_entries(self, server_id: str, share_group_id: str,
                       entries: list[dict[str, Any]],
                       agent_instance_id: str = "external-mcp") -> dict[str, Any]:
        self._ensure_dirs()
        store = SharedMemoryStore(self.workspace, share_group_id)
        organizer = AutoOrganizer(self.workspace, share_group_id)
        imported = []
        for entry in entries:
            body = str(entry.get("body", "")).strip()
            if not body:
                continue
            metadata = dict(entry.get("metadata", {}))
            metadata["external_mcp_server_id"] = server_id
            event = MemoryEvent(
                event_id=stable_hash("external_mcp_event", server_id, body, _now_iso()),
                agent_instance_id=agent_instance_id,
                share_group_id=share_group_id,
                raw_content=body,
                metadata=metadata,
                auto_actions=[],
                created_at=_now_iso(),
            )
            store.append_event(event)
            record, actions = organizer.organize(event)
            event.auto_actions = actions
            store.update_event(event)
            imported.append({
                "memory_id": record.memory_id,
                "status": record.status.value,
                "kind": record.kind.value,
                "auto_actions": actions,
            })
        manifest = {
            "server_id": server_id,
            "share_group_id": share_group_id,
            "imported": imported,
            "imported_at": _now_iso(),
        }
        import_id = stable_hash("external_import", server_id, share_group_id, _now_iso())
        (self.imports_dir / f"{import_id}.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return {"ok": True, "import_id": import_id, "imported": imported, "total": len(imported)}

    def _classify(self, descriptor: dict[str, Any], tool_names: list[str],
                  resource_names: list[str]) -> ExternalMCPLevel:
        name = str(descriptor.get("name", descriptor.get("display_name", ""))).lower()
        if "memoryguard" in name or any(t.startswith("memoryguard_memory_") for t in tool_names):
            return ExternalMCPLevel.L4_MEMORYGUARD_MCP
        memory_tool_hits = [t for t in tool_names if "memory" in t and any(k in t for k in ["read", "search", "write", "list"])]
        if memory_tool_hits or descriptor.get("memory_entries"):
            return ExternalMCPLevel.L3_KNOWN_MEMORY_MCP
        if resource_names or descriptor.get("resources"):
            return ExternalMCPLevel.L2_GENERIC_RESOURCES
        if tool_names:
            return ExternalMCPLevel.L1_UNKNOWN_TOOLS
        return ExternalMCPLevel.L0_UNRECOGNIZABLE

    def _strategy(self, level: ExternalMCPLevel) -> str:
        strategies = {
            ExternalMCPLevel.L4_MEMORYGUARD_MCP: "direct_sync_or_merge",
            ExternalMCPLevel.L3_KNOWN_MEMORY_MCP: "readonly_preview_then_import",
            ExternalMCPLevel.L2_GENERIC_RESOURCES: "user_selected_resources_then_import",
            ExternalMCPLevel.L1_UNKNOWN_TOOLS: "detect_only_unknown_tools_not_called",
            ExternalMCPLevel.L0_UNRECOGNIZABLE: "ask_user_to_export_md_or_json",
        }
        return strategies[level]

    def _upsert_server(self, server: dict[str, Any]) -> None:
        servers = self.list_servers()
        servers = [s for s in servers if s.get("server_id") != server["server_id"]]
        servers.append(server)
        self.servers_path.write_text(
            json.dumps({"servers": servers}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _server(self, server_id: str) -> dict[str, Any] | None:
        for server in self.list_servers():
            if server.get("server_id") == server_id:
                return server
        return None

    def _name(self, item: Any) -> str:
        if isinstance(item, str):
            return item
        if isinstance(item, dict):
            return str(item.get("name", item.get("uri", "")))
        return str(item)
