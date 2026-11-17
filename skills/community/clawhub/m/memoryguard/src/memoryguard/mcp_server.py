"""MCP stdio server（spec §1.2, §4.2）。

让宿主通过 MCP stdio 调用 MemoryGuard，获得结构化结果。
首期实现 MCP 2024-11-05 基础协议子集:
- initialize: 能力协商
- tools/list: 返回 memoryguard_audit/open/explain 工具
- tools/call: 执行工具，返回结构化结果

纯标准库实现，不依赖 MCP SDK。无网络。
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from .cli import run_audit, _load_report
from .report import render_html_report
from .schema import Report


# 写操作工具列表：执行前做本地参数预检，避免无效请求写入状态。
# 注：memoryguard_extract_memories 现为只读 preview（§8.5 两步流程步骤 1）。
#     memoryguard_accept_candidates 写入共享记忆（§8.5 步骤 2）。
_MUTATING_TOOLS = {
    "memoryguard_memory_write",
    "memoryguard_memory_update",
    "memoryguard_memory_delete",
    "memoryguard_binding_create",
    "memoryguard_external_mcp_import",
    "memoryguard_accept_candidates",
    "memoryguard_provider_install",
}


# ---------------------------------------------------------------------------
# MCP 协议常量
# ---------------------------------------------------------------------------

PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "memoryguard"
SERVER_VERSION = "0.1.0"

TOOLS = [
    {
        "name": "memoryguard_audit",
        "description": "Read-only scan of an Agent workspace: instructions, skills, memory, local RAG. Returns findings with evidence. No network, no writes.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "workspace": {"type": "string", "description": "workspace path (default: .)"},
            },
        },
    },
    {
        "name": "memoryguard_explain",
        "description": "Explain a finding's evidence, impact, suggestion, and confidence.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "finding_id": {"type": "string", "description": "finding id from audit"},
                "workspace": {"type": "string", "description": "workspace path (default: .)"},
            },
            "required": ["finding_id"],
        },
    },
    {
        "name": "memoryguard_list_sources",
        "description": "List authorized sources (project directory, selected folders, Obsidian vaults). Read-only.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "workspace": {"type": "string", "description": "workspace path (default: .)"},
            },
        },
    },
    {
        "name": "memoryguard_scan_summary",
        "description": "Run a read-only scan and return snapshot + coverage ledger. Proves scan completeness (unaccounted_count must be 0).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "workspace": {"type": "string", "description": "workspace path (default: .)"},
            },
        },
    },
    {
        "name": "memoryguard_neuron_graph",
        "description": "Read the neuron graph projection (read-only). Returns {empty: true, reason: 'not_built'} if projection not yet built. Use build_plan to generate a build plan first.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "workspace": {"type": "string", "description": "workspace path (default: .)"},
            },
        },
    },
    {
        "name": "memoryguard_import_preview",
        "description": "Preview an offline import bundle (ChatGPT/Claude/Gemini/Generic). Read-only detection + inventory.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "bundle path (file or dir)"},
                "workspace": {"type": "string", "description": "workspace path (default: .)"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "memoryguard_build_plan",
        "description": "Generate a memory build plan (read-only, no write). Returns BuildManifest with integrity check and diff preview. Apply via GUI or CLI.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target_path": {"type": "string", "description": "target path (default: .memoryguard/memory-target)"},
                "workspace": {"type": "string", "description": "workspace path (default: .)"},
            },
        },
    },
    # --- v3.2 memory backend tools ---
    {
        "name": "memoryguard_memory_read",
        "description": "Read a single shared memory record by memory_id. Read-only.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "memory_id": {"type": "string", "description": "memory record ID"},
                "workspace": {"type": "string", "description": "workspace path (default: .)"},
                "share_group_id": {"type": "string", "description": "share group ID (default: default)"},
            },
            "required": ["memory_id"],
        },
    },
    {
        "name": "memoryguard_memory_search",
        "description": "Search shared memory records by query, kind, or status. Read-only.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "search query"},
                "kind": {"type": "string", "description": "filter by kind: preference|fact|project|procedure|episode|correction"},
                "status": {"type": "string", "description": "filter by status: active|shadowed|conflicted|quarantined|deleted"},
                "workspace": {"type": "string", "description": "workspace path (default: .)"},
                "share_group_id": {"type": "string", "description": "share group ID (default: default)"},
            },
        },
    },
    {
        "name": "memoryguard_memory_write",
        "description": "Write a new memory record. Auto-organizes: classify, dedup, supersede, conflict, quarantine. Returns memory_id and auto_actions.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "body": {"type": "string", "description": "memory content"},
                "kind": {"type": "string", "description": "override kind (default: auto-classify). Valid: preference|fact|project|procedure|episode|correction"},
                "write_policy": {"type": "string", "description": "write policy: auto_accept (default) | auto_quarantine_on_risk | propose_only. propose_only creates a low_confidence candidate without modifying existing memories"},
                "metadata": {"type": "object", "description": "optional metadata from agent"},
                "agent_instance_id": {"type": "string", "description": "agent that wrote this memory"},
                "workspace": {"type": "string", "description": "workspace path (default: .)"},
                "share_group_id": {"type": "string", "description": "share group ID (default: default)"},
            },
            "required": ["body"],
        },
    },
    {
        "name": "memoryguard_memory_update",
        "description": "Update an existing memory record (body, kind, status). Records a DecisionEvent.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "memory_id": {"type": "string", "description": "memory record ID"},
                "body": {"type": "string", "description": "new body"},
                "kind": {"type": "string", "description": "new kind"},
                "status": {"type": "string", "description": "new status"},
                "workspace": {"type": "string", "description": "workspace path (default: .)"},
                "share_group_id": {"type": "string", "description": "share group ID (default: default)"},
            },
            "required": ["memory_id"],
        },
    },
    {
        "name": "memoryguard_memory_delete",
        "description": "Soft-delete a memory record (status=deleted). Records a DecisionEvent.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "memory_id": {"type": "string", "description": "memory record ID"},
                "workspace": {"type": "string", "description": "workspace path (default: .)"},
                "share_group_id": {"type": "string", "description": "share group ID (default: default)"},
            },
            "required": ["memory_id"],
        },
    },
    {
        "name": "memoryguard_memory_status",
        "description": "Get shared memory group status: record counts, event counts, conflicts, quarantine. Read-only.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "workspace": {"type": "string", "description": "workspace path (default: .)"},
                "share_group_id": {"type": "string", "description": "share group ID (default: default)"},
            },
        },
    },
    # --- v3.2 agent binding tools ---
    {
        "name": "memoryguard_binding_create",
        "description": "Bind an agent instance to a share_group. Creates an AgentBinding record (active). Read-only listing is via binding_list; unbind goes through CLI/GUI.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "agent_instance_id": {"type": "string", "description": "agent instance ID to bind"},
                "share_group_id": {"type": "string", "description": "share group ID to bind the agent into"},
                "mcp_server_name": {"type": "string", "description": "MCP server name (default: memoryguard)"},
                "native_memory_mode": {"type": "string", "description": "native memory mode: observed|redirected|unsupported (default: observed)"},
                "redirect_paths": {"type": "array", "items": {"type": "string"}, "description": "optional native memory redirect paths"},
                "workspace": {"type": "string", "description": "workspace path (default: .)"},
            },
            "required": ["agent_instance_id", "share_group_id"],
        },
    },
    {
        "name": "memoryguard_binding_list",
        "description": "List existing AgentBinding records. Read-only.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "include_inactive": {"type": "boolean", "description": "include inactive bindings (default: true)"},
                "workspace": {"type": "string", "description": "workspace path (default: .)"},
            },
        },
    },
    # --- v3.2 external MCP descriptor tools ---
    {
        "name": "memoryguard_external_mcp_list",
        "description": "List imported external MCP server descriptors and their resources. Descriptor-level only (no live MCP client discovery). Read-only.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "workspace": {"type": "string", "description": "workspace path (default: .)"},
            },
        },
    },
    {
        "name": "memoryguard_external_mcp_import",
        "description": "Import a new external MCP descriptor (JSON). Classifies the server (L0-L4), persists it, and returns the detection result. Descriptor-level import only; does not call the live MCP server.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "descriptor_json": {"type": "string", "description": "JSON-encoded MCP descriptor {name|display_name, tools[], resources[], memory_entries[]}"},
                "server_id": {"type": "string", "description": "server ID (default: derived from descriptor name/display_name)"},
                "workspace": {"type": "string", "description": "workspace path (default: .)"},
            },
            "required": ["descriptor_json"],
        },
    },
    # --- v3.2 document extraction tool (§8.5 两步流程) ---
    {
        "name": "memoryguard_extract_memories",
        "description": "Extract memory segments from a source file under an authorized source root (read-only preview). Returns candidate list with kind, risk_level, and preview. Does NOT write to shared memory. Use memoryguard_accept_candidates to write accepted candidates.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source_path": {"type": "string", "description": "absolute or workspace-relative path to a source file under an authorized source root"},
                "workspace": {"type": "string", "description": "workspace path (default: .)"},
            },
            "required": ["source_path"],
        },
    },
    {
        "name": "memoryguard_accept_candidates",
        "description": "Accept extracted memory candidates and write them to shared memory. Writes to SharedMemoryStore via append_event + AutoOrganizer.organize. Records a DecisionEvent (action=accept_extract). Requires extract_id from a prior extract_memories call and explicit candidate_ids list.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "extract_id": {"type": "string", "description": "extract_id returned by memoryguard_extract_memories preview"},
                "candidate_ids": {"type": "array", "items": {"type": "string"}, "description": "list of candidate_id values to accept (cannot be empty)"},
                "workspace": {"type": "string", "description": "workspace path (default: .)"},
                "share_group_id": {"type": "string", "description": "share group ID (default: default)"},
            },
            "required": ["extract_id", "candidate_ids"],
        },
    },
    # --- v3.2 semantic dedup tool ---
    {
        "name": "memoryguard_semantic_check",
        "description": "Check a new text against existing memories for semantic duplicates/conflicts (cross-lingual, paraphrase). Returns similar memories with similarity scores. Read-only.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "new text to check"},
                "kind": {"type": "string", "description": "optional kind of the new memory, used for conflict detection"},
                "threshold": {"type": "number", "description": "similarity threshold (default: 0.85)"},
                "workspace": {"type": "string", "description": "workspace path (default: .)"},
                "share_group_id": {"type": "string", "description": "share group ID (default: default)"},
            },
            "required": ["text"],
        },
    },
    # --- v3.2 provider adapter tool ---
    {
        "name": "memoryguard_provider_install",
        "description": "Install a provider adapter (Claude/Codex/Cursor) to redirect native memory to MemoryGuard MCP. Writes instruction file + MCP config + creates AgentBinding. Idempotent.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "provider": {"type": "string", "description": "provider name: claude|codex|cursor"},
                "workspace": {"type": "string", "description": "workspace path (default: .)"},
            },
            "required": ["provider"],
        },
    },
    # --- v3.2 agent group resolution tool ---
    {
        "name": "memoryguard_resolve_group",
        "description": "Resolve which share_group_id an agent should write to, based on its AgentBinding. Read-only. Agents should call this before memory_write to know their group.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "agent_instance_id": {"type": "string", "description": "agent instance ID to resolve"},
                "workspace": {"type": "string", "description": "workspace path (default: .)"},
            },
            "required": ["agent_instance_id"],
        },
    },
]


# ---------------------------------------------------------------------------
# 工具执行
# ---------------------------------------------------------------------------


def _mcp_error(message: str) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": f"error: {message}"}], "isError": True}


def _preflight_mutating_tool(name: str, args: dict[str, Any], workspace: Path) -> dict[str, Any] | None:
    """Validate mutating requests before writing local state."""
    if name == "memoryguard_memory_write":
        if not str(args.get("body", "")).strip():
            return _mcp_error("body is required")
        return None

    if name in {"memoryguard_memory_update", "memoryguard_memory_delete"}:
        memory_id = str(args.get("memory_id", "")).strip()
        if not memory_id:
            return _mcp_error("memory_id is required")
        if name == "memoryguard_memory_update" and not any(args.get(k) for k in ("body", "kind", "status")):
            return _mcp_error("at least one update field is required: body, kind, or status")
        # 枚举校验在 preflight 做，非法值不落盘
        if name == "memoryguard_memory_update":
            from .schema_v3 import SharedMemoryStatus, MemoryKind
            _VALID_STATUSES = {s.value for s in SharedMemoryStatus}
            _VALID_KINDS = {k.value for k in MemoryKind}
            status_val = args.get("status")
            kind_val = args.get("kind")
            if status_val is not None and status_val not in _VALID_STATUSES:
                return _mcp_error(f"invalid status '{status_val}'. Valid: {sorted(_VALID_STATUSES)}")
            if kind_val is not None and kind_val not in _VALID_KINDS:
                return _mcp_error(f"invalid kind '{kind_val}'. Valid: {sorted(_VALID_KINDS)}")
        from .shared_memory_store import SharedMemoryStore

        store = SharedMemoryStore(workspace, _get_share_group_id(args)[0])
        if store.get_record(memory_id) is None:
            return _mcp_error(f"memory not found: {memory_id}")
        return None

    if name == "memoryguard_binding_create":
        if not str(args.get("agent_instance_id", "")).strip():
            return _mcp_error("agent_instance_id is required")
        if not str(args.get("share_group_id", "")).strip():
            return _mcp_error("share_group_id is required")
        return None

    if name == "memoryguard_external_mcp_import":
        descriptor_raw = args.get("descriptor_json", "")
        try:
            descriptor = json.loads(descriptor_raw) if isinstance(descriptor_raw, str) else dict(descriptor_raw)
        except (ValueError, TypeError) as e:
            return _mcp_error(f"invalid descriptor_json: {e}")
        if not isinstance(descriptor, dict):
            return _mcp_error("descriptor_json must decode to an object")
        return None

    if name == "memoryguard_accept_candidates":
        extract_id = str(args.get("extract_id", "")).strip()
        if not extract_id:
            return _mcp_error("extract_id is required")
        candidate_ids = args.get("candidate_ids", [])
        if not candidate_ids or not isinstance(candidate_ids, list):
            return _mcp_error("candidate_ids must be a non-empty list")
        return None

    if name == "memoryguard_provider_install":
        provider = str(args.get("provider", "")).lower()
        if provider not in {"claude", "codex", "cursor"}:
            return _mcp_error(f"unknown provider '{provider}'. Supported: claude|codex|cursor")
        return None

    return None


def execute_tool(name: str, args: dict[str, Any]) -> dict[str, Any]:
    """执行工具，返回 MCP tool result。"""
    workspace = Path(args.get("workspace", ".")).resolve()

    # 写操作：先做本地参数预检，再执行
    if name in _MUTATING_TOOLS:
        preflight_err = _preflight_mutating_tool(name, args, workspace)
        if preflight_err is not None:
            return preflight_err

    if name == "memoryguard_audit":
        report = run_audit(workspace)
        # 写报告
        from .cli import ensure_layout, REPORTS_DIR

        ensure_layout(workspace)
        json_path = workspace / REPORTS_DIR / "report.json"
        html_path = workspace / REPORTS_DIR / "report.html"
        json_path.write_text(report.to_json(), encoding="utf-8")
        html_path.write_text(render_html_report(report), encoding="utf-8")
        return {
            "content": [
                {
                    "type": "text",
                    "text": _format_audit_text(report, str(html_path)),
                }
            ]
        }

    if name == "memoryguard_explain":
        report = _load_report(workspace)
        if report is None:
            return {"content": [{"type": "text", "text": "error: no report found"}], "isError": True}
        finding = next((f for f in report.findings if f.id == args.get("finding_id")), None)
        if finding is None:
            return {"content": [{"type": "text", "text": f"error: finding not found: {args.get('finding_id')}"}], "isError": True}
        return {
            "content": [
                {
                    "type": "text",
                    "text": (
                        f"Finding: {finding.id}\n"
                        f"  rule: {finding.rule_id}\n"
                        f"  severity: {finding.severity.value}\n"
                        f"  evidence: {finding.evidence}\n"
                        f"  impact: {finding.impact}\n"
                        f"  suggestion: {finding.suggestion}\n"
                        f"  confidence: {finding.confidence}\n"
                        f"  fixable: {finding.fixable}\n"
                    ),
                }
            ]
        }

    # --- v3 只读工具 ---

    if name == "memoryguard_list_sources":
        api = _get_governance_api(workspace)
        result = api.list_sources()
        text = f"Sources: {result['total']}\n"
        for s in result["sources"]:
            text += f"  - {s['root_id']}  {s['type']}  {s['display_name']}  scope={s['scope']}\n"
            text += f"      path: {s['path']}\n"
        return {"content": [{"type": "text", "text": text}]}

    if name == "memoryguard_scan_summary":
        api = _get_governance_api(workspace)
        result = api.scan_sources()
        cov = result["coverage"]
        text = (
            f"Snapshot: {result['snapshot_id']}\n"
            f"  created_at: {result['created_at']}\n"
            f"  source_objects: {result['source_object_count']}\n"
            f"  coverage: {cov['coverage_status']}\n"
            f"  candidates: {cov['candidate_count']}\n"
            f"  read: {cov['read']}  unsupported: {cov['unsupported']}  unreadable: {cov['unreadable']}\n"
            f"  skipped_by_policy: {cov['skipped_by_policy']}  unaccounted: {cov['unaccounted_count']}"
        )
        return {"content": [{"type": "text", "text": text}]}

    if name == "memoryguard_neuron_graph":
        api = _get_governance_api(workspace)
        proj = api.get_neuron_graph()
        if proj.get("empty"):
            text = f"Neuron graph: {proj.get('reason', 'not_built')}\nUse build_plan to generate a plan, then apply via GUI/CLI to build projection."
            return {"content": [{"type": "text", "text": text}]}
        nodes = proj.get("nodes", [])
        edges = proj.get("edges", [])
        text = (
            f"Neuron graph projection:\n"
            f"  snapshot: {proj.get('snapshot_id', '')}\n"
            f"  built_at: {proj.get('built_at', '')}\n"
            f"  nodes: {len(nodes)}  edges: {len(edges)}\n"
            f"  nodes (first 10):"
        )
        for n in nodes[:10]:
            text += f"\n    [{n['node_kind']}] {n.get('label','')[:30]} provenance={n.get('provenance_count',0)}"
        return {"content": [{"type": "text", "text": text}]}

    if name == "memoryguard_import_preview":
        api = _get_governance_api(workspace)
        result = api.preview_import(args["path"])
        if "error" in result:
            return {"content": [{"type": "text", "text": f"error: {result['error']}"}], "isError": True}
        text = (
            f"Import preview:\n"
            f"  provider: {result.get('provider', 'unknown')}\n"
            f"  confidence: {result.get('confidence', 0)}\n"
            f"  notes: {result.get('notes', '')}\n"
            f"  inventory: {result.get('inventory', {})}"
        )
        return {"content": [{"type": "text", "text": text}]}

    if name == "memoryguard_build_plan":
        api = _get_governance_api(workspace)
        target_path = args.get("target_path", "")
        plan = api.create_build_plan(target_path)
        text = (
            f"Build plan: {plan.get('plan_id', '')}\n"
            f"  snapshot: {plan.get('snapshot_id', '')}\n"
            f"  target_profile: {plan.get('target_profile', '')}\n"
            f"  coverage: {plan.get('coverage_status', '')}\n"
            f"  integrity: {plan.get('integrity_ok', False)}\n"
            f"  published: {plan.get('manifest', {}).get('published_record_count', 0)}\n"
            f"  unaccounted: {plan.get('manifest', {}).get('unaccounted_record_count', 0)}\n"
            f"  diff: {plan.get('diff_preview', {})}\n"
            f"Apply via GUI or: memoryguard memory build-apply {plan.get('plan_id','')} --yes"
        )
        return {"content": [{"type": "text", "text": text}]}

    # --- v3.2 memory backend tools ---
    if name == "memoryguard_memory_read":
        return _handle_memory_read(args)
    if name == "memoryguard_memory_search":
        return _handle_memory_search(args)
    if name == "memoryguard_memory_write":
        return _handle_memory_write(args)
    if name == "memoryguard_memory_update":
        return _handle_memory_update(args)
    if name == "memoryguard_memory_delete":
        return _handle_memory_delete(args)
    if name == "memoryguard_memory_status":
        return _handle_memory_status(args)

    # --- v3.2 agent binding tools ---
    if name == "memoryguard_binding_create":
        api = _get_governance_api(workspace)
        result = api.bind_agent(
            agent_instance_id=args["agent_instance_id"],
            share_group_id=args["share_group_id"],
            mcp_server_name=args.get("mcp_server_name", "memoryguard"),
            native_memory_mode=args.get("native_memory_mode", "observed"),
            redirect_paths=args.get("redirect_paths"),
        )
        return {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}]}

    if name == "memoryguard_binding_list":
        api = _get_governance_api(workspace)
        result = api.list_bindings(include_inactive=args.get("include_inactive", True))
        text = f"Bindings: {result['total']}\n"
        for b in result["bindings"]:
            text += (
                f"  - {b['binding_id'][:12]}  agent={b['agent_instance_id']}  "
                f"group={b['share_group_id']}  status={b['status']}  mode={b['native_memory_mode']}\n"
            )
        return {"content": [{"type": "text", "text": text}]}

    # --- v3.2 external MCP descriptor tools ---
    if name == "memoryguard_external_mcp_list":
        api = _get_governance_api(workspace)
        result = api.list_external_mcp_servers()
        text = f"External MCP servers: {result['total']}\n"
        for s in result["servers"]:
            text += (
                f"  - {s.get('server_id')}  level={s.get('level')}  "
                f"tools={s.get('tool_count', 0)}  resources={s.get('resource_count', 0)}\n"
                f"      display_name: {s.get('display_name', '')}\n"
            )
        return {"content": [{"type": "text", "text": text}]}

    if name == "memoryguard_external_mcp_import":
        descriptor_raw = args.get("descriptor_json", "")
        try:
            descriptor = (
                json.loads(descriptor_raw)
                if isinstance(descriptor_raw, str)
                else dict(descriptor_raw)
            )
        except (ValueError, TypeError) as e:
            return {"content": [{"type": "text", "text": f"error: invalid descriptor_json: {e}"}], "isError": True}
        server_id = (
            args.get("server_id")
            or descriptor.get("name")
            or descriptor.get("display_name")
            or descriptor.get("id")
            or "external-mcp"
        )
        api = _get_governance_api(workspace)
        result = api.detect_external_mcp(server_id, descriptor)
        return {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}]}

    # --- v3.2 document extraction tool (§8.5 两步流程) ---
    if name == "memoryguard_extract_memories":
        source_path = Path(args["source_path"]).resolve()
        from .source_registry import SourceRegistry

        reg = SourceRegistry(workspace)
        root_id: str | None = None
        relative_path: str | None = None
        for root in reg.list_sources():
            root_path = Path(root.path).resolve()
            try:
                rel = source_path.relative_to(root_path)
            except ValueError:
                continue
            root_id = root.root_id
            relative_path = str(rel).replace("\\", "/")
            break
        if root_id is None:
            return {
                "content": [{"type": "text", "text": f"error: source_path not under any authorized source root: {source_path}"}],
                "isError": True,
            }
        api = _get_governance_api(workspace)
        result = api.extract_preview(root_id, relative_path)
        if "error" in result:
            return {"content": [{"type": "text", "text": f"error: {result['error']}"}], "isError": True}
        return {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}]}

    if name == "memoryguard_accept_candidates":
        api = _get_governance_api(workspace)
        result = api.accept_candidates(
            extract_id=args["extract_id"],
            candidate_ids=args["candidate_ids"],
            share_group_id=_get_share_group_id(args)[0],
        )
        if "error" in result:
            return {"content": [{"type": "text", "text": f"error: {result['error']}"}], "isError": True}
        return {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}]}

    # --- v3.2 semantic dedup tool ---
    if name == "memoryguard_semantic_check":
        from .semantic_dedup import SemanticDedup

        text_to_check = args["text"]
        kind = args.get("kind")
        threshold = args.get("threshold")
        group_id = _get_share_group_id(args)[0]
        sd = SemanticDedup(workspace, group_id)
        duplicates = sd.find_semantic_duplicates(text_to_check, threshold=threshold)
        conflicts = []
        if kind:
            conflicts = sd.find_semantic_conflicts(text_to_check, kind, threshold=threshold)
        result = {
            "duplicates": duplicates,
            "conflicts": conflicts,
            "checked_against": len(duplicates),
        }
        return {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}]}

    # --- v3.2 provider adapter tool ---
    if name == "memoryguard_provider_install":
        from .provider_adapters import ClaudeAdapter, CodexAdapter, CursorAdapter

        provider = args.get("provider", "").lower()
        adapter_map = {
            "claude": ClaudeAdapter,
            "codex": CodexAdapter,
            "cursor": CursorAdapter,
        }
        adapter_cls = adapter_map.get(provider)
        if adapter_cls is None:
            return {"content": [{"type": "text", "text": f"error: unknown provider '{provider}'. Supported: claude|codex|cursor"}], "isError": True}
        adapter = adapter_cls(str(workspace))
        result = adapter.install(str(workspace))
        return {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}]}

    # --- v3.2 agent group resolution tool ---
    if name == "memoryguard_resolve_group":
        from .agent_binding import AgentBindingStore

        agent_id = args["agent_instance_id"]
        binding_store = AgentBindingStore(workspace)
        bindings = binding_store.find_by_agent(agent_id, include_inactive=False)
        if not bindings:
            result = {
                "share_group_id": None,
                "binding_id": None,
                "suggestion": f"Run 'memoryguard agent bind {agent_id}' first",
            }
        else:
            binding = bindings[0]
            result = {
                "share_group_id": binding.share_group_id,
                "binding_id": binding.binding_id,
                "native_memory_mode": binding.native_memory_mode.value,
            }
        return {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}]}

    return {"content": [{"type": "text", "text": f"error: unknown tool {name}"}], "isError": True}


# ---------------------------------------------------------------------------
# v3.2 memory backend 工具处理
# ---------------------------------------------------------------------------


def _get_share_group_id(args: dict[str, Any], workspace: Path | None = None) -> tuple[str, str | None]:
    """根据 args 推导 share_group_id。返回 (group_id, error_message)。

    优先级：
    1. 用户显式指定的 share_group_id（非 "default"）— 直接返回
    2. agent_instance_id 对应的 active AgentBinding 的 share_group_id
    3. "default"（向后兼容）

    如果 agent_instance_id 存在但无绑定，写 stderr warning。
    环境变量 MEMORYGUARD_STRICT_BINDING=1 时，调用方应拒绝写入。
    """
    explicit_group = args.get("share_group_id", "default")
    if explicit_group and explicit_group != "default":
        return (explicit_group, None)

    agent_id = args.get("agent_instance_id", "")
    if not agent_id:
        return ("default", None)

    # 查 AgentBinding，由 binding 派生 group_id
    ws = workspace or Path(args.get("workspace", ".")).resolve()
    try:
        from .agent_binding import AgentBindingStore

        binding_store = AgentBindingStore(ws)
        bindings = binding_store.find_by_agent(agent_id, include_inactive=False)
        if bindings:
            return (bindings[0].share_group_id, None)
    except Exception as e:
        # 查询失败不阻塞写入，只警告
        print(f"Warning: failed to query agent binding for '{agent_id}': {e}", file=sys.stderr)
        return ("default", None)

    # agent 存在但无绑定
    warning_msg = (
        f"agent '{agent_id}' has no binding, writing to default group. "
        f"Run 'memoryguard agent bind {agent_id}' to bind."
    )
    print(f"Warning: {warning_msg}", file=sys.stderr)
    return ("default", warning_msg)


def _handle_memory_read(args: dict[str, Any]) -> dict[str, Any]:
    from .shared_memory_store import SharedMemoryStore
    workspace = Path(args.get("workspace", ".")).resolve()
    group_id = _get_share_group_id(args)[0]
    store = SharedMemoryStore(workspace, group_id)
    record = store.get_record(args["memory_id"])
    if record is None:
        return {"content": [{"type": "text", "text": f"error: memory not found: {args['memory_id']}"}], "isError": True}
    return {"content": [{"type": "text", "text": json.dumps(record.to_dict(), ensure_ascii=False, indent=2)}]}


def _handle_memory_search(args: dict[str, Any]) -> dict[str, Any]:
    from .shared_memory_store import SharedMemoryStore
    workspace = Path(args.get("workspace", ".")).resolve()
    group_id = _get_share_group_id(args)[0]
    store = SharedMemoryStore(workspace, group_id)
    query = args.get("query", "")
    kind = args.get("kind")
    status = args.get("status")
    records = store.list_records(status=status, kind=kind)
    # 简单关键词搜索
    if query:
        query_lower = query.lower()
        records = [r for r in records if query_lower in r.body.lower()]
    text = f"Found {len(records)} records:\n"
    for r in records[:20]:
        text += f"  [{r.status.value}] [{r.kind.value}] {r.memory_id[:8]}  {r.body[:60]}\n"
    return {"content": [{"type": "text", "text": text}]}


def _handle_memory_write(args: dict[str, Any]) -> dict[str, Any]:
    from .shared_memory_store import SharedMemoryStore
    from .auto_organizer import AutoOrganizer
    from .schema_v3 import MemoryEvent, stable_hash, _now_iso, MemoryKind, MemoryWritePolicy
    workspace = Path(args.get("workspace", ".")).resolve()
    group_id, binding_warning = _get_share_group_id(args, workspace)
    if binding_warning and os.environ.get('MEMORYGUARD_STRICT_BINDING', '') == '1':
        return {'content': [{'type': 'text', 'text': f'error: unbound agent rejected (MEMORYGUARD_STRICT_BINDING=1). {binding_warning}'}], 'isError': True}
    body = args["body"]
    agent_instance_id = args.get("agent_instance_id", "")
    metadata = args.get("metadata", {})
    kind_override = args.get("kind", "")
    write_policy = args.get("write_policy", "auto_accept")

    # 写入前校验枚举值
    _VALID_POLICIES = {p.value for p in MemoryWritePolicy}
    if write_policy not in _VALID_POLICIES:
        return {"content": [{"type": "text", "text": f"error: invalid write_policy '{write_policy}'. Valid: {sorted(_VALID_POLICIES)}"}], "isError": True}
    if kind_override:
        _VALID_KINDS = {k.value for k in MemoryKind}
        if kind_override not in _VALID_KINDS:
            return {"content": [{"type": "text", "text": f"error: invalid kind '{kind_override}'. Valid: {sorted(_VALID_KINDS)}"}], "isError": True}

    # 创建事件
    event = MemoryEvent(
        event_id=stable_hash("event", body, _now_iso()),
        agent_instance_id=agent_instance_id,
        share_group_id=group_id,
        raw_content=body,
        metadata=metadata,
        auto_actions=[],
        created_at=_now_iso(),
    )
    store = SharedMemoryStore(workspace, group_id)
    store.append_event(event)
    # 自动整理
    organizer = AutoOrganizer(workspace, group_id)
    record, actions = organizer.organize(
        event, kind_override=kind_override, write_policy=write_policy)
    # 回填 auto_actions
    event.auto_actions = actions
    store.update_event(event)
    result = {
        "memory_id": record.memory_id,
        "status": record.status.value,
        "kind": record.kind.value,
        "auto_actions": actions,
    }
    return {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}]}


def _handle_memory_update(args: dict[str, Any]) -> dict[str, Any]:
    from .shared_memory_store import SharedMemoryStore
    from .schema_v3 import DecisionEvent, stable_hash, _now_iso, SharedMemoryStatus, MemoryKind
    workspace = Path(args.get("workspace", ".")).resolve()
    group_id = _get_share_group_id(args)[0]
    store = SharedMemoryStore(workspace, group_id)
    memory_id = args["memory_id"]
    body = args.get("body")
    kind = args.get("kind")
    status = args.get("status")

    # 写入前校验枚举值，非法值不落盘
    _VALID_STATUSES = {s.value for s in SharedMemoryStatus}
    _VALID_KINDS = {k.value for k in MemoryKind}
    if status is not None and status not in _VALID_STATUSES:
        return {"content": [{"type": "text", "text": f"error: invalid status '{status}'. Valid: {sorted(_VALID_STATUSES)}"}], "isError": True}
    if kind is not None and kind not in _VALID_KINDS:
        return {"content": [{"type": "text", "text": f"error: invalid kind '{kind}'. Valid: {sorted(_VALID_KINDS)}"}], "isError": True}

    if body:
        record = store.get_record(memory_id)
        store._update_record_field(memory_id, "body", body)
        store._update_record_field(memory_id, "updated_at", _now_iso())
        decision = DecisionEvent(
            event_id=stable_hash("update_body", memory_id, _now_iso()),
            actor="user", action="update_body",
            target_ids=[memory_id], reason="user edit",
            created_at=_now_iso(),
        )
        store.append_decision(decision)
    if kind:
        record = store.get_record(memory_id)
        old_kind = record.kind.value if record else ""
        store._update_record_field(memory_id, "kind", kind)
        decision = DecisionEvent(
            event_id=stable_hash("update_kind", memory_id, _now_iso()),
            actor="user", action="update_kind",
            target_ids=[memory_id],
            reason=f"kind: {old_kind} -> {kind}",
            created_at=_now_iso(),
        )
        store.append_decision(decision)
    if status:
        record = store.get_record(memory_id)
        old_status = record.status.value if record else ""
        store._update_record_field(memory_id, "status", status)
        decision = DecisionEvent(
            event_id=stable_hash("update_status", memory_id, _now_iso()),
            actor="user", action="update_status",
            target_ids=[memory_id],
            reason=f"status: {old_status} -> {status}",
            created_at=_now_iso(),
        )
        store.append_decision(decision)
    record = store.get_record(memory_id)
    if record is None:
        return {"content": [{"type": "text", "text": f"error: memory not found: {memory_id}"}], "isError": True}
    return {"content": [{"type": "text", "text": json.dumps(record.to_dict(), ensure_ascii=False, indent=2)}]}


def _handle_memory_delete(args: dict[str, Any]) -> dict[str, Any]:
    from .shared_memory_store import SharedMemoryStore
    workspace = Path(args.get("workspace", ".")).resolve()
    group_id = _get_share_group_id(args)[0]
    store = SharedMemoryStore(workspace, group_id)
    store.delete(args["memory_id"])
    return {"content": [{"type": "text", "text": f"Deleted: {args['memory_id']} (soft delete)"}]}


def _handle_memory_status(args: dict[str, Any]) -> dict[str, Any]:
    from .shared_memory_store import SharedMemoryStore
    workspace = Path(args.get("workspace", ".")).resolve()
    group_id = _get_share_group_id(args)[0]
    store = SharedMemoryStore(workspace, group_id)
    status = store.status()
    return {"content": [{"type": "text", "text": json.dumps(status, ensure_ascii=False, indent=2)}]}


# ---------------------------------------------------------------------------
# GovernanceApi 缓存（同一 workspace 复用，避免每次 tool call 重建神经树）
# ---------------------------------------------------------------------------

_api_cache: dict[str, Any] = {}


def _get_governance_api(workspace: Path):
    """获取或创建 workspace 对应的 GovernanceApi 实例。"""
    key = str(workspace)
    if key not in _api_cache:
        from .gui import GovernanceApi

        _api_cache[key] = GovernanceApi(str(workspace))
    return _api_cache[key]


def _format_audit_text(report: Report, html_path: str) -> str:
    """格式化 audit 结果为文本摘要。"""
    s = report.summary()
    lines = [
        f"MemoryGuard audit complete in {report.duration_ms} ms",
        f"  workspace: {report.workspace}",
        f"  objects: {s['object_count']}",
        f"  findings: {len(report.findings)}",
        f"  invisible: {s['invisible_count']}",
        f"  health: {report.health_score}/100",
        f"  report: {html_path}",
    ]
    if report.findings:
        lines.append("  findings detail:")
        for f in report.findings[:20]:
            lines.append(f"    [{f.severity.value}] {f.rule_id}: {f.evidence[:80]}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# JSON-RPC 处理
# ---------------------------------------------------------------------------


def handle_request(request: dict[str, Any]) -> dict[str, Any] | None:
    """处理单个 JSON-RPC 请求，返回响应 dict（通知返回 None）。"""
    method = request.get("method", "")
    req_id = request.get("id")
    params = request.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": PROTOCOL_VERSION,
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
                "capabilities": {"tools": {}},
            },
        }

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS}}

    if method == "tools/call":
        name = params.get("name", "")
        args = params.get("arguments", {})
        try:
            result = execute_tool(name, args)
            return {"jsonrpc": "2.0", "id": req_id, "result": result}
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32603, "message": f"tool execution failed: {e}"},
            }

    if method == "notifications/initialized":
        return None  # 通知，无响应

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"method not found: {method}"},
    }


def serve_stdio() -> int:
    """MCP stdio 主循环。从 stdin 读 JSON-RPC，向 stdout 写响应。"""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError as e:
            response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": f"parse error: {e}"}}
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
            continue
        response = handle_request(request)
        if response is not None:
            sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(serve_stdio())
