#!/usr/bin/env python3
"""mcp_server.py — minimal MCP server (stdio, line-delimited JSON-RPC 2.0).

Tools exposed:
  - list_judges     : list registered DomainJudge domains
  - judge_change    : 510(k) change-classification verdict (Judge510kChange)
  - judge_postmarket: postmarket-surveillance verdict (JudgePostmarket)

L2 authorization: caller role (params["role"], default "read-only") may call
the read-only judge tools. Any other requested tool is rejected and the
denial is audited into LocalMemory. No secrets are ever logged.

Run:
    python lgd_engine/mcp_server.py     # speaks JSON-RPC on stdin/stdout
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lgd_engine.gate.engine import GateEngine                # noqa: E402
from lgd_engine.judges.judge_510k import Judge510kChange      # noqa: E402
from lgd_engine.judges.judge_postmarket import JudgePostmarket  # noqa: E402
from lgd_engine.memory.localmem_min import LocalMemory        # noqa: E402

READONLY_TOOLS = {"list_judges", "judge_change", "judge_postmarket"}

TOOL_SCHEMAS = {
    "list_judges": {
        "description": "List registered DomainJudge domains.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    "judge_change": {
        "description": "Run the 510(k) change-classification judge over a change ctx.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "change_type": {"type": "string"},
                "safety_impact": {"type": "string"},
                "recall_class": {"type": "string"},
                "predicate_unchanged": {"type": "boolean"},
                "source_refs": {"type": "array"},
            },
            "required": ["change_type"],
        },
    },
    "judge_postmarket": {
        "description": "Run the postmarket-surveillance judge over a ctx.",
        "inputSchema": {"type": "object", "properties": {"ctx": {"type": "object"}}},
    },
}


def build_audit() -> LocalMemory:
    return LocalMemory(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "mcp_audit.sqlite"))


def handle(recv: dict, audit: LocalMemory) -> dict:
    mid = recv.get("id")
    method = recv.get("method")
    params = recv.get("params") or {}

    if method == "initialize":
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "lgd-engine-mcp", "version": "0.1.0"},
            "capabilities": {"tools": {}},
        }}

    if method == "tools/list":
        tools = [{"name": n, **TOOL_SCHEMAS[n]} for n in
                 ("list_judges", "judge_change", "judge_postmarket")]
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": tools}}

    if method == "tools/call":
        name = params.get("name", "")
        args = params.get("arguments") or {}
        role = params.get("role", "read-only")

        if name not in READONLY_TOOLS:
            audit.record({
                "initiator": "mcp-server",
                "subject": f"unauthorized tool call rejected: {name!r} role={role}",
                "decision": "hold",
                "basis": "L2 RBAC: read-only role cannot call this tool",
                "status": "vetoed",
                "evidence_refs": [],
            })
            return {"jsonrpc": "2.0", "id": mid,
                    "error": {"code": -32003,
                              "message": f"permission denied: {name!r} not allowed for role={role}"}}

        if name == "list_judges":
            result = {"judges": [
                Judge510kChange().domain,
                JudgePostmarket().domain,
            ]}
        elif name == "judge_change":
            report = GateEngine([Judge510kChange()]).evaluate(args)
            result = {"report": report.to_dict()}
        else:  # judge_postmarket
            report = GateEngine([JudgePostmarket()]).evaluate(args)
            result = {"report": report.to_dict()}

        audit.record({
            "initiator": "mcp-server",
            "subject": f"tool {name} called by role={role}",
            "decision": result.get("report", {}).get("verdict", "n/a"),
            "basis": f"tools/call {name}",
            "status": "executed",
            "evidence_refs": [],
        })
        return {"jsonrpc": "2.0", "id": mid, "result": {"content": [
            {"type": "text", "text": json.dumps(result, ensure_ascii=False)}]}}

    return {"jsonrpc": "2.0", "id": mid,
            "error": {"code": -32601, "message": f"method not found: {method}"}}


def main() -> int:
    audit = build_audit()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            recv = json.loads(line)
            resp = handle(recv, audit)
        except json.JSONDecodeError as exc:
            resp = {"jsonrpc": "2.0", "id": None,
                    "error": {"code": -32700, "message": f"parse error: {exc}"}}
        sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
        sys.stdout.flush()
    audit.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
