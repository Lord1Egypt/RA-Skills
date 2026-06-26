#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Lingua Universale MCP Server.

Exposes Lingua Universale protocol verification as MCP tools for
Claude Code, Cursor, and OpenClaw-compatible clients.

Four tools:
  - lu_load_protocol   -- parse a .lu source file
  - lu_verify_message  -- check if a message is valid in session context
  - lu_check_properties -- verify formal safety properties
  - lu_list_templates  -- browse the standard library (20 protocols)

Usage:
    python lu_mcp_server.py          # stdio transport (default)
    uvx openclaw-skill-lingua-universale
"""

from __future__ import annotations

import json
import logging
from typing import Any

from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

mcp = FastMCP(
    "lingua-universale",
    instructions=(
        "Verify agent-to-agent communication against session type protocols. "
        "Mathematical proofs, not trust. "
        "Use lu_load_protocol to parse a .lu definition, "
        "lu_verify_message to check individual messages, "
        "lu_check_properties for formal safety proofs, "
        "and lu_list_templates to browse 20 standard library protocols."
    ),
)


# ---------------------------------------------------------------------------
# Helper: import LU with a clear error if not installed
# ---------------------------------------------------------------------------


def _require_lu() -> Any:
    """Return the cervellaswarm_lingua_universale module or raise ImportError."""
    try:
        import cervellaswarm_lingua_universale as lu  # noqa: PLC0415
        return lu
    except ImportError as exc:
        raise ImportError(
            "cervellaswarm-lingua-universale is not installed. "
            "Run: pip install cervellaswarm-lingua-universale>=0.3.3"
        ) from exc


# ---------------------------------------------------------------------------
# Tool 1: lu_load_protocol
# ---------------------------------------------------------------------------


@mcp.tool()
async def lu_load_protocol(protocol_text: str) -> str:
    """Parse a Lingua Universale (.lu) protocol definition.

    Accepts the full text of a .lu file and returns the parsed protocol
    structure: name, roles, steps, choices, and declared properties.

    Args:
        protocol_text: Content of a .lu file, e.g.:
            "protocol RequestResponse:\\n"
            "    roles: client, server\\n"
            "    client asks server to process request\\n"
            "    server returns response to client\\n"
            "    properties:\\n"
            "        always terminates\\n"
            "        no deadlock\\n"

    Returns:
        JSON string with keys:
          ok (bool), protocol_name (str), roles (list[str]),
          steps (list), properties (list), error (str on failure).
    """
    lu = _require_lu()

    result = lu.check_source(protocol_text, source_file="<mcp-input>")

    if not result.ok:
        return json.dumps({
            "ok": False,
            "error": "; ".join(result.errors),
        })

    # Extract protocol info from the compiled module's AST via verify_source
    # (check_source only compiles; verify_source also walks declarations)
    verify_result = lu.verify_source(protocol_text, source_file="<mcp-input>")

    protocols_info: list[dict[str, Any]] = []

    # Walk property reports to extract protocol metadata
    for report in verify_result.property_reports:
        protocol_name = report.protocol_name
        props: list[dict[str, Any]] = []
        for pr in report.results:
            props.append({
                "kind": pr.spec.kind.value,
                "verdict": pr.verdict.value,
                "evidence": pr.evidence,
                "params": list(pr.spec.params),
            })
        protocols_info.append({
            "protocol_name": protocol_name,
            "properties": props,
            "all_passed": report.all_passed,
            "passed_count": report.passed_count,
            "violated_count": report.violated_count,
        })

    # Also extract parse-level info via the _parser + _ast
    from cervellaswarm_lingua_universale._parser import parse  # noqa: PLC0415
    from cervellaswarm_lingua_universale._ast import (  # noqa: PLC0415
        ProtocolNode,
        AgentNode,
        ChoiceNode,
    )

    try:
        program = parse(protocol_text)
    except Exception as exc:
        return json.dumps({
            "ok": False,
            "error": f"Parse error: {exc}",
        })

    protocols_detail: list[dict[str, Any]] = []
    agents_detail: list[dict[str, Any]] = []

    for decl in program.declarations:
        if isinstance(decl, ProtocolNode):
            steps_info = _steps_to_list(decl.steps)
            protocols_detail.append({
                "name": decl.name,
                "roles": list(decl.roles),
                "steps": steps_info,
                "step_count": len(steps_info),
                "has_choices": any(
                    isinstance(s, ChoiceNode) for s in decl.steps
                ),
            })
        elif isinstance(decl, AgentNode):
            agents_detail.append({
                "name": decl.name,
                "role": decl.role,
                "trust": decl.trust,
            })

    return json.dumps({
        "ok": True,
        "protocols": protocols_detail,
        "agents": agents_detail,
        "property_reports": protocols_info,
        "summary": {
            "protocol_count": len(protocols_detail),
            "agent_count": len(agents_detail),
        },
    }, indent=2)


def _steps_to_list(steps: list[Any]) -> list[dict[str, Any]]:
    """Recursively convert AST step/choice nodes to serialisable dicts."""
    from cervellaswarm_lingua_universale._ast import ChoiceNode  # noqa: PLC0415

    result: list[dict[str, Any]] = []
    for step in steps:
        if isinstance(step, ChoiceNode):
            branches: dict[str, list[dict[str, Any]]] = {}
            for branch in step.branches:
                branches[branch.label] = _steps_to_list(branch.steps)
            result.append({
                "type": "choice",
                "decider": step.decider,
                "branches": branches,
            })
        elif hasattr(step, "sender"):
            result.append({
                "type": "step",
                "sender": step.sender,
                "receiver": step.receiver,
                "action": step.action,
                "payload": getattr(step, "payload", ""),
            })
    return result


# ---------------------------------------------------------------------------
# Tool 2: lu_verify_message
# ---------------------------------------------------------------------------


@mcp.tool()
async def lu_verify_message(
    protocol_text: str,
    messages: list[dict[str, str]],
    next_message: dict[str, str],
) -> str:
    """Verify whether a message is valid in the context of an ongoing session.

    Replays the existing message history against the protocol, then checks
    whether next_message is the expected next step.

    Args:
        protocol_text: Full .lu protocol definition text.
        messages: List of already-sent messages, each a dict with keys:
            sender (str), receiver (str), action (str).
            Actions are LU action names: "asks", "returns", "sends",
            "proposes", "tells". These match the verbs in .lu source files.
        next_message: The message to validate, same format as above.

    Returns:
        JSON string:
          On success: {"valid": true, "step": N, "next_expected": "..."}
          On violation: {"valid": false, "violation": "...", "expected": "...", "got": "..."}
          On error: {"valid": false, "error": "..."}

    Example:
        protocol_text = "protocol Ping:\\n    roles: a, b\\n    a asks b to ping\\n    b returns pong to a\\n    properties:\\n        always terminates\\n"
        messages = [{"sender": "a", "receiver": "b", "action": "ask"}]
        next_message = {"sender": "b", "receiver": "a", "action": "return"}
        # Returns: {"valid": true, ...}
    """
    lu = _require_lu()

    # Step 1: Parse the protocol
    from cervellaswarm_lingua_universale._parser import parse  # noqa: PLC0415
    from cervellaswarm_lingua_universale._eval import _protocol_node_to_runtime  # noqa: PLC0415
    from cervellaswarm_lingua_universale._ast import ProtocolNode  # noqa: PLC0415

    try:
        program = parse(protocol_text)
    except Exception as exc:
        return json.dumps({"valid": False, "error": f"Parse error: {exc}"})

    protocol_nodes = [
        d for d in program.declarations if isinstance(d, ProtocolNode)
    ]
    if not protocol_nodes:
        return json.dumps({
            "valid": False,
            "error": "No protocol declaration found in protocol_text.",
        })

    # Use first protocol (most common case)
    protocol_obj = _protocol_node_to_runtime(protocol_nodes[0])

    # Step 2: Build a SessionChecker and replay history
    checker = lu.SessionChecker(protocol_obj, session_id="mcp-verify")

    # Map action names to MessageKind via the action->kind table from _eval
    from cervellaswarm_lingua_universale._eval import _action_to_kind_map  # noqa: PLC0415

    action_map = _action_to_kind_map()

    def _make_swarm_msg(action: str) -> Any:
        """Create a minimal SwarmMessage for the given action."""
        from cervellaswarm_lingua_universale.types import (  # noqa: PLC0415
            TaskRequest, MessageKind,
        )

        kind = action_map.get(action.lower())
        if kind is None:
            # Fallback: try direct MessageKind value lookup
            for mk in MessageKind:
                if mk.value == action.lower():
                    kind = mk
                    break
        if kind is None:
            raise ValueError(
                f"Unknown action '{action}'. "
                f"Known actions: {sorted(action_map.keys())}"
            )
        # Return the simplest valid SwarmMessage for this kind
        return _kind_to_swarm_msg(kind)

    # Replay existing messages
    for i, msg in enumerate(messages):
        sender = msg.get("sender", "")
        receiver = msg.get("receiver", "")
        action = msg.get("action", "")

        try:
            swarm_msg = _make_swarm_msg(action)
        except ValueError as exc:
            return json.dumps({
                "valid": False,
                "error": f"Message {i}: {exc}",
            })

        try:
            checker.send(sender, receiver, swarm_msg)
        except lu.ProtocolViolation as exc:
            return json.dumps({
                "valid": False,
                "error": f"History replay failed at message {i}: {exc}",
                "expected": exc.expected,
                "got": exc.got,
            })
        except lu.SessionComplete as exc:
            return json.dumps({
                "valid": False,
                "error": f"Protocol already complete at message {i}: {exc}",
            })

    # Step 3: Check the next message
    next_sender = next_message.get("sender", "")
    next_receiver = next_message.get("receiver", "")
    next_action = next_message.get("action", "")

    try:
        next_swarm_msg = _make_swarm_msg(next_action)
    except ValueError as exc:
        return json.dumps({"valid": False, "error": str(exc)})

    # Peek at what's expected before attempting send
    expected_step = checker._state.peek_next_step()
    expected_desc = (
        f"{expected_step.sender} -> {expected_step.receiver} : {expected_step.message_kind.value}"
        if expected_step else "protocol complete or at choice point"
    )

    try:
        checker.send(next_sender, next_receiver, next_swarm_msg)
    except lu.ProtocolViolation as exc:
        return json.dumps({
            "valid": False,
            "violation": str(exc),
            "expected": exc.expected,
            "got": exc.got,
            "step": exc.step,
        })
    except lu.SessionComplete as exc:
        return json.dumps({
            "valid": False,
            "violation": str(exc),
            "expected": "no more messages (protocol complete)",
            "got": f"{next_sender} -> {next_receiver} : {next_action}",
        })

    # Success
    next_expected_step = checker._state.peek_next_step()
    next_expected_desc = (
        f"{next_expected_step.sender} -> {next_expected_step.receiver} : {next_expected_step.message_kind.value}"
        if next_expected_step else "protocol complete"
    )

    return json.dumps({
        "valid": True,
        "step": checker.step_index,
        "is_complete": checker.is_complete,
        "next_expected": next_expected_desc,
    })


def _kind_to_swarm_msg(kind: Any) -> Any:
    """Return the simplest valid SwarmMessage for a given MessageKind."""
    from cervellaswarm_lingua_universale.types import (  # noqa: PLC0415
        MessageKind,
        TaskRequest,
        TaskResult,
        AuditRequest,
        AuditVerdict,
        PlanRequest,
        PlanProposal,
        PlanDecision,
        ResearchQuery,
        ResearchReport,
        DirectMessage,
        Broadcast,
        ShutdownRequest,
        ShutdownAck,
        ContextInject,
        AuditVerdictType,
        PlanComplexity,
        TaskStatus,
    )

    _KIND_TO_MSG: dict[MessageKind, Any] = {
        MessageKind.TASK_REQUEST: TaskRequest(
            task_id="mcp-t1", description="verify",
        ),
        MessageKind.TASK_RESULT: TaskResult(
            task_id="mcp-t1", status=TaskStatus.OK, summary="ok",
        ),
        MessageKind.AUDIT_REQUEST: AuditRequest(
            audit_id="mcp-a1", target="verify",
        ),
        MessageKind.AUDIT_VERDICT: AuditVerdict(
            audit_id="mcp-a1", verdict=AuditVerdictType.APPROVED, score=9.5,
        ),
        MessageKind.PLAN_REQUEST: PlanRequest(
            plan_id="mcp-p1", task_description="plan",
        ),
        MessageKind.PLAN_PROPOSAL: PlanProposal(
            plan_id="mcp-p1", complexity=PlanComplexity.LOW,
            risk_score=0.1, files_affected=1,
        ),
        MessageKind.PLAN_DECISION: PlanDecision(
            plan_id="mcp-p1", approved=True,
        ),
        MessageKind.RESEARCH_QUERY: ResearchQuery(
            query_id="mcp-q1", topic="verify",
        ),
        MessageKind.RESEARCH_REPORT: ResearchReport(
            query_id="mcp-q1", topic="verify", sources_consulted=1,
        ),
        MessageKind.DM: DirectMessage(
            sender_role="mcp", content="verify",
        ),
        MessageKind.BROADCAST: Broadcast(
            sender_role="mcp", content="verify",
        ),
        MessageKind.SHUTDOWN_REQUEST: ShutdownRequest(
            target_role="mcp",
        ),
        MessageKind.SHUTDOWN_ACK: ShutdownAck(
            target_role="mcp",
        ),
        MessageKind.CONTEXT_INJECT: ContextInject(
            context_type="mcp", content="verify",
        ),
    }

    msg = _KIND_TO_MSG.get(kind)
    if msg is None:
        # Fallback for any unknown kind: use DirectMessage
        msg = DirectMessage(sender_role="mcp", content=f"mcp-verify-{kind.value}")
    return msg


# ---------------------------------------------------------------------------
# Tool 3: lu_check_properties
# ---------------------------------------------------------------------------


@mcp.tool()
async def lu_check_properties(protocol_text: str) -> str:
    """Verify the formal safety properties declared in a .lu protocol.

    Runs the static property checker (Layer 1) on all protocols found in
    the source. Optionally, if Lean 4 is installed, also runs formal
    verification (Layer 2).

    Args:
        protocol_text: Full .lu protocol definition text including a
            "properties:" block, e.g.:
            "    properties:\\n"
            "        always terminates\\n"
            "        no deadlock\\n"
            "        all roles participate\\n"

    Returns:
        JSON string with:
          ok (bool), protocols (list of protocol results), summary (dict).
          Each protocol result has: protocol_name, all_passed, results (list).
          Each result has: kind, verdict, evidence, params.
    """
    lu = _require_lu()

    verify_result = lu.verify_source(protocol_text, source_file="<mcp-input>")

    if not verify_result.ok and not verify_result.property_reports:
        return json.dumps({
            "ok": False,
            "error": "; ".join(verify_result.errors),
        })

    protocols_out: list[dict[str, Any]] = []

    for report in verify_result.property_reports:
        results_out: list[dict[str, Any]] = []
        for pr in report.results:
            results_out.append({
                "kind": pr.spec.kind.value,
                "verdict": pr.verdict.value,
                "evidence": pr.evidence,
                "params": list(pr.spec.params),
                "threshold": pr.spec.threshold if pr.spec.threshold is not None and pr.spec.threshold != 0.0 else None,
            })

        protocols_out.append({
            "protocol_name": report.protocol_name,
            "all_passed": report.all_passed,
            "passed_count": report.passed_count,
            "violated_count": report.violated_count,
            "results": results_out,
        })

    # Include Lean 4 lines if available
    lean4_lines = verify_result.verification

    total_passed = sum(p["passed_count"] for p in protocols_out)
    total_violated = sum(p["violated_count"] for p in protocols_out)

    return json.dumps({
        "ok": verify_result.ok,
        "protocols": protocols_out,
        "lean4_output": lean4_lines,
        "summary": {
            "protocol_count": len(protocols_out),
            "total_passed": total_passed,
            "total_violated": total_violated,
            "parse_errors": verify_result.errors,
        },
    }, indent=2)


# ---------------------------------------------------------------------------
# Tool 4: lu_list_templates
# ---------------------------------------------------------------------------


@mcp.tool()
async def lu_list_templates(category: str = "") -> str:
    """List available Lingua Universale standard library protocol templates.

    The standard library contains 20 verified protocols across 5 categories:
    communication, data, business, ai_ml, security.

    Args:
        category: Optional filter. One of: communication, data, business,
            ai_ml, security. Leave empty to list all templates.

    Returns:
        JSON string with:
          ok (bool), templates (list), category_filter (str), total (int).
          Each template has: name, category, description.
    """
    from pathlib import Path  # noqa: PLC0415

    try:
        from cervellaswarm_lingua_universale._init_project import (  # noqa: PLC0415
            list_templates,
            _STDLIB_DIR,
        )
    except ImportError as exc:
        return json.dumps({"ok": False, "error": str(exc)})

    # Category descriptions for context
    _CATEGORY_DESCRIPTIONS: dict[str, str] = {
        "communication": "Fundamental messaging patterns (request/response, pub/sub, scatter/gather)",
        "data": "Data management protocols (CRUD, sync, cache invalidation)",
        "business": "Business workflow patterns (approval, auction, saga, two-buyer)",
        "ai_ml": "AI/ML agent protocols (RAG, delegation, tool calling, human-in-loop, consensus)",
        "security": "Security protocols (auth handshake, mutual TLS, rate limiting)",
    }

    # Property highlights per template (hand-curated from stdlib README)
    _TEMPLATE_HIGHLIGHTS: dict[str, str] = {
        "request_response": "always terminates, no deadlock",
        "ping_pong": "always terminates, no deadlock",
        "pub_sub": "all roles participate",
        "scatter_gather": "all roles participate",
        "pipeline": "ordering (source -> processor -> transformer -> sink)",
        "crud_safe": "no deletion, all roles participate",
        "data_sync": "ordering (primary before replica)",
        "cache_invalidation": "choice (hit/miss), all roles participate",
        "two_buyer": "MPST canonical (Honda/Yoshida POPL 2008)",
        "approval_workflow": "role exclusive (only approver decides)",
        "auction": "choice (sold/unsold)",
        "saga_order": "distributed transaction, ordering",
        "rag_pipeline": "ordering (retrieval before generation)",
        "agent_delegation": "trust >= standard, ordering",
        "tool_calling": "ordering (registry before executor)",
        "human_in_loop": "role exclusive (only human decides)",
        "consensus": "all roles participate, confidence >= medium",
        "auth_handshake": "ordering, exclusion (client cannot send token)",
        "mutual_tls": "all roles participate, ordering",
        "rate_limited_api": "role exclusive (only limiter throttles)",
    }

    all_names = list_templates()

    templates: list[dict[str, str]] = []
    for name in all_names:
        # Determine category from path
        cat = ""
        for category_dir in _STDLIB_DIR.iterdir():
            if category_dir.is_dir():
                if (category_dir / f"{name}.lu").exists():
                    cat = category_dir.name
                    break

        # Apply filter if provided
        if category and cat != category:
            continue

        templates.append({
            "name": name,
            "category": cat,
            "description": _TEMPLATE_HIGHLIGHTS.get(name, ""),
            "usage": f"lu init my-project --template {name}",
        })

    categories_present = sorted({t["category"] for t in templates})

    return json.dumps({
        "ok": True,
        "templates": templates,
        "category_filter": category or "all",
        "total": len(templates),
        "categories": {
            c: _CATEGORY_DESCRIPTIONS.get(c, c) for c in categories_present
        },
    }, indent=2)


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------


def main() -> None:
    """Run the MCP server (stdio transport)."""
    mcp.run()


if __name__ == "__main__":
    main()
