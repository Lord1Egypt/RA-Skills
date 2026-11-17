"""A small dependency-free MCP server for verified long-form writing audits.

The server intentionally coordinates files that already belong to one writing
project. It does not call a model or send manuscript content to a third party.
Agents receive bounded task prompts, submit explicit coverage receipts, and
cannot unlock reconciliation while required reviews are incomplete.
"""

from __future__ import annotations

import argparse
import json
import sys
import socket
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from . import __version__

from .audit_queue import (
    claim_audit_task,
    get_reconciliation_task,
    list_audit_tasks,
    submit_audit_report,
)
from .compiler import compile_audit_prompt_text, compile_humanize_prompt_text, compile_prompt
from .review import compile_critique_prompt
from .fidelity import compare_fidelity
from .ledger import compile_ledger_extraction_prompt_text
from .linter import lint_text
from .longform import verify_long_form_package, write_long_form_audit
from .protection import compare_protected_content
from .skills import list_style_skills
from .statistics import analyze_style_statistics


SERVER_INFO = {"name": "advanced-human-writing", "version": __version__}
PROTOCOL_VERSION = "2025-03-26"
MAX_CONTEXT_CHARACTERS = 20000
MAX_TEXT_CHARACTERS = 80000
MAX_HTTP_BODY_BYTES = 1024 * 1024

PROMPTS = [
    ("humanize-quick", "Compile a compact rewrite prompt for one supplied passage."),
    ("humanize-deep", "Compile a deeper rewrite prompt for one supplied passage."),
    ("dialogue-audit", "Compile a fiction dialogue, register, and response-linkage audit."),
    ("continuity-audit", "Compile a fiction continuity audit with physical and relationship checks."),
    ("style-match", "Compile a rewrite prompt with an explicit style direction."),
    ("serious-rewrite", "Compile a protected rewrite prompt for news, academic, legal, or technical prose."),
    ("extract-ledger", "Compile an evidence-backed continuity-ledger extraction prompt."),
]


def _tool(name: str, description: str, properties: dict[str, Any], required: list[str]) -> dict[str, Any]:
    return {
        "name": name,
        "description": description,
        "inputSchema": {
            "type": "object",
            "properties": properties,
            "required": required,
            "additionalProperties": False,
        },
    }


TOOLS = [
    _tool(
        "compile_generation_prompt",
        "Compile genre-aware writing instructions with generation-time anti-filler, repetition, voice, and factual constraints. Does not call a model.",
        {
            "style": {"type": "string", "enum": list_style_skills()},
            "task": {"type": "string"},
            "context_text": {"type": "string"},
            "original_text": {"type": "string"},
            "reference_style": {"type": "string"},
            "source_paths": {"type": "array", "items": {"type": "string"}, "description": "Factual source files relative to the configured writing workspace."},
            "reference_paths": {"type": "array", "items": {"type": "string"}, "description": "Voice reference files relative to the workspace; never used as factual sources."},
        },
        ["style", "task"],
    ),
    _tool(
        "compile_critique_prompt",
        "Compile an evidence-based diagnosis-only prompt without praise or replacement prose.",
        {"draft": {"type": "string"}, "style": {"type": "string", "enum": list_style_skills()}, "brief": {"type": "string"}},
        ["draft", "style"],
    ),
    _tool(
        "plan_long_form_audit",
        "Split a local manuscript or report into bounded review tasks, reports, and a verified agent plan.",
        {
            "draft_path": {"type": "string", "description": "Path relative to the configured project root."},
            "output_dir": {"type": "string", "description": "Empty package directory relative to the project root."},
            "style": {"type": "string", "enum": list_style_skills()},
            "context_path": {"type": "string", "description": "Optional outline, ledger, or report plan."},
            "reference_paths": {"type": "array", "items": {"type": "string"}},
            "source_paths": {"type": "array", "items": {"type": "string"}},
            "agent_mode": {"type": "string", "enum": ["standard", "deep"], "default": "deep"},
            "translationese": {"type": "boolean", "default": False},
            "book_level": {"type": "boolean", "default": False},
            "chunk_size": {"type": "integer", "minimum": 2000},
        },
        ["draft_path", "output_dir", "style"],
    ),
    _tool(
        "list_audit_tasks",
        "List review tasks, dependencies, claims, receipt validity, and readiness for one audit package.",
        {"package_dir": {"type": "string"}},
        ["package_dir"],
    ),
    _tool(
        "claim_audit_task",
        "Claim one ready review task. The returned prompt is the complete bounded assignment for that agent.",
        {
            "package_dir": {"type": "string"},
            "task_id": {"type": "string"},
            "agent_id": {"type": "string", "default": "anonymous"},
        },
        ["package_dir", "task_id"],
    ),
    _tool(
        "submit_audit_report",
        "Submit a full review report. It must include a complete Coverage Receipt with no blocked material.",
        {
            "package_dir": {"type": "string"},
            "task_id": {"type": "string"},
            "report_markdown": {"type": "string"},
            "agent_id": {"type": "string", "default": "anonymous"},
        },
        ["package_dir", "task_id", "report_markdown"],
    ),
    _tool(
        "verify_audit_coverage",
        "Verify every required review report before final reconciliation. A blocked or incomplete receipt fails the gate.",
        {"package_dir": {"type": "string"}},
        ["package_dir"],
    ),
    _tool(
        "get_reconciliation_task",
        "Return the final cross-chapter reconciliation prompt only after coverage verification passes.",
        {"package_dir": {"type": "string"}},
        ["package_dir"],
    ),
    _tool(
        "read_project_context",
        "Read a bounded local outline, continuity ledger, source note, or approved style reference from the project root.",
        {
            "path": {"type": "string"},
            "offset": {"type": "integer", "minimum": 0, "default": 0},
            "max_characters": {"type": "integer", "minimum": 1, "maximum": MAX_CONTEXT_CHARACTERS, "default": 8000},
        },
        ["path"],
    ),
    _tool(
        "lint_text",
        "Run deterministic writing-pattern checks on supplied text and return evidence locations. This is not an authorship detector.",
        {
            "text": {"type": "string", "description": "Text to inspect; kept in the local MCP process."},
            "style": {"type": "string", "enum": ["general", *list_style_skills()], "default": "general"},
            "allow": {"type": "array", "items": {"type": "string"}, "default": []},
        },
        ["text"],
    ),
    _tool(
        "get_style_statistics",
        "Calculate language-aware sentence variation, lexical diversity, and transition density for supplied text.",
        {
            "text": {"type": "string", "description": "Text to analyze locally."},
            "language": {"type": "string", "default": "auto", "description": "Language tag such as de or pt-BR; unsupported transition profiles return null."},
            "style": {"type": "string", "enum": ["general", *list_style_skills()], "default": "general"},
        },
        ["text"],
    ),
    _tool(
        "verify_protected_content",
        "Compare source and rewritten text for changed literal numbers, citations, URLs, code, quotes, and named terms; not a semantic check.",
        {
            "source_text": {"type": "string"},
            "candidate_text": {"type": "string"},
            "terms": {"type": "array", "items": {"type": "string"}, "default": []},
        },
        ["source_text", "candidate_text"],
    ),
    _tool(
        "verify_fidelity",
        "Locate changed claim spans and semantic-risk cues; changed prose always needs review even when protected literals match.",
        {
            "source_text": {"type": "string"},
            "candidate_text": {"type": "string"},
            "terms": {"type": "array", "items": {"type": "string"}, "default": []},
        },
        ["source_text", "candidate_text"],
    ),
    _tool(
        "compile_humanize_prompt",
        "Compile a local AI-ready humanization prompt from supplied text without sending it to a model.",
        {
            "draft": {"type": "string"},
            "style": {"type": "string", "enum": list_style_skills()},
            "mode": {"type": "string", "enum": ["quick", "deep"], "default": "quick"},
            "task": {"type": "string"},
            "context_text": {"type": "string"},
        },
        ["draft", "style"],
    ),
    _tool(
        "compile_audit_prompt",
        "Compile a bounded single-document audit prompt from supplied text without sending it to a model.",
        {
            "draft": {"type": "string"},
            "document_type": {"type": "string", "default": "auto"},
            "profiles": {"type": "array", "items": {"type": "string"}, "default": ["full"]},
            "context_text": {"type": "string"},
        },
        ["draft"],
    ),
    _tool(
        "compile_ledger_extraction",
        "Compile a candidate-ledger extraction prompt that separates observed facts from inference and requires evidence.",
        {
            "draft": {"type": "string"},
            "existing_ledger": {"type": "string"},
        },
        ["draft"],
    ),
]


WRITING_TOOLS = [
    _tool(
        "plan_long_form_writing",
        "Plan outline checking, planning, bounded writer/editor tasks, and final continuity verification. Does not call a model.",
        {
            "outline_path": {"type": "string", "minLength": 1},
            "output_dir": {"type": "string", "minLength": 1},
            "style": {"type": "string", "enum": list_style_skills()},
            "target_length": {"type": "integer", "minimum": 1, "maximum": 5000000},
            "chunk_size": {"type": "integer", "minimum": 200, "maximum": 12000, "default": 5000},
            "length_unit": {"type": "string", "enum": ["characters", "words"], "default": "characters"},
            "execution_mode": {"type": "string", "enum": ["sequential", "contract"], "default": "sequential"},
            "max_parallel": {"type": "integer", "minimum": 1, "maximum": 32, "default": 4},
            **{key: {"type": "array", "items": {"type": "string", "minLength": 1}}
               for key in ("context_paths", "source_paths", "reference_paths")},
        },
        ["outline_path", "output_dir", "style", "target_length"],
    ),
    _tool("list_writing_tasks", "List drafting tasks and dependency readiness.",
          {"package_dir": {"type": "string", "minLength": 1}}, ["package_dir"]),
    _tool("claim_writing_task", "Claim a ready drafting task and receive its role prompt, result schema, and opaque claim_token. Copy claim_token unchanged into the submitted result; tokens from earlier claims are invalid after reclaim or revision.",
          {key: {"type": "string", "minLength": 1} for key in ("package_dir", "task_id", "agent_id")},
          ["package_dir", "task_id", "agent_id"]),
    _tool("submit_writing_result", "Submit a structured result matching the claimed role schema, including the active claim_token returned by claim_writing_task.",
          {**{key: {"type": "string", "minLength": 1} for key in ("package_dir", "task_id", "agent_id")},
           "result": {"type": "object", "description": f"Claimed role result; at most {MAX_TEXT_CHARACTERS} serialized characters."}},
          ["package_dir", "task_id", "agent_id", "result"]),
    _tool("verify_writing_project", "Verify all required drafting results before assembly.",
          {"package_dir": {"type": "string", "minLength": 1}}, ["package_dir"]),
    _tool("assemble_writing_project", "Assemble verified edited chunks into a workspace-local manuscript.",
          {key: {"type": "string", "minLength": 1} for key in ("package_dir", "output_path")},
          ["package_dir", "output_path"]),
]
TOOLS.extend(WRITING_TOOLS)


def _safe_path(root: Path, value: str) -> Path:
    candidate = Path(value)
    resolved = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError("Path must stay within the configured project root.") from exc
    return resolved


def _path_list(root: Path, value: Any, label: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{label} must be a list of project-relative paths.")
    return [str(_safe_path(root, item)) for item in value]


def _text_result(value: Any, is_error: bool = False) -> dict[str, Any]:
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)
    result: dict[str, Any] = {"content": [{"type": "text", "text": text}]}
    if is_error:
        result["isError"] = True
    return result


def call_tool(name: str, arguments: dict[str, Any], root: Path) -> dict[str, Any]:
    """Execute one project-local coordination operation and return MCP tool content."""

    if not isinstance(arguments, dict):
        raise ValueError("Tool arguments must be an object.")
    if name in {tool["name"] for tool in WRITING_TOOLS}:
        return _call_writing_tool(name, arguments, root.resolve())
    if name == "compile_generation_prompt":
        return _text_result({"prompt": compile_prompt(
            style=_string(arguments, "style"),
            task=_bounded_string(arguments, "task", MAX_CONTEXT_CHARACTERS),
            context_text=_optional_nullable_string(arguments, "context_text", MAX_CONTEXT_CHARACTERS),
            original_text=_optional_nullable_string(arguments, "original_text", MAX_TEXT_CHARACTERS),
            reference_style=_optional_nullable_string(arguments, "reference_style", MAX_CONTEXT_CHARACTERS),
            source_paths=[str(_safe_path(root, path)) for path in _string_list(arguments, "source_paths")],
            reference_paths=[str(_safe_path(root, path)) for path in _string_list(arguments, "reference_paths")],
        )})
    if name == "compile_critique_prompt":
        return _text_result({"prompt": compile_critique_prompt(
            _bounded_string(arguments, "draft", MAX_TEXT_CHARACTERS),
            _string(arguments, "style"),
            _optional_nullable_string(arguments, "brief", MAX_CONTEXT_CHARACTERS) or "",
        )})
    if name == "lint_text":
        text = _bounded_string(arguments, "text", MAX_TEXT_CHARACTERS)
        style = _optional_string(arguments, "style", "general")
        allow = _string_list(arguments, "allow")
        return _text_result(lint_text(text, style=style, allow=set(allow)).to_dict())
    if name == "get_style_statistics":
        text = _bounded_string(arguments, "text", MAX_TEXT_CHARACTERS)
        style = _optional_string(arguments, "style", "general")
        return _text_result(analyze_style_statistics(text, style=style, language=_optional_string(arguments, "language", "auto")).to_dict())
    if name == "verify_protected_content":
        source = _bounded_string(arguments, "source_text", MAX_TEXT_CHARACTERS)
        candidate = _bounded_string(arguments, "candidate_text", MAX_TEXT_CHARACTERS)
        return _text_result(compare_protected_content(source, candidate, terms=_string_list(arguments, "terms")).to_dict())
    if name == "verify_fidelity":
        source = _bounded_string(arguments, "source_text", MAX_TEXT_CHARACTERS)
        candidate = _bounded_string(arguments, "candidate_text", MAX_TEXT_CHARACTERS)
        return _text_result(compare_fidelity(source, candidate, terms=_string_list(arguments, "terms")).to_dict())
    if name == "compile_humanize_prompt":
        return _text_result(
            compile_humanize_prompt_text(
                _bounded_string(arguments, "draft", MAX_TEXT_CHARACTERS),
                style=_string(arguments, "style"),
                mode=_optional_string(arguments, "mode", "quick"),
                task=_optional_nullable_string(arguments, "task"),
                context_text=_optional_nullable_string(arguments, "context_text", MAX_CONTEXT_CHARACTERS),
            )
        )
    if name == "compile_audit_prompt":
        return _text_result(
            compile_audit_prompt_text(
                _bounded_string(arguments, "draft", MAX_TEXT_CHARACTERS),
                document_type=_optional_string(arguments, "document_type", "auto"),
                profiles=_string_list(arguments, "profiles") or ["full"],
                context_text=_optional_nullable_string(arguments, "context_text", MAX_CONTEXT_CHARACTERS),
            )
        )
    if name == "compile_ledger_extraction":
        return _text_result(
            compile_ledger_extraction_prompt_text(
                _bounded_string(arguments, "draft", MAX_TEXT_CHARACTERS),
                _optional_nullable_string(arguments, "existing_ledger", MAX_CONTEXT_CHARACTERS) or "",
            )
        )
    if name == "plan_long_form_audit":
        draft = _safe_path(root, _string(arguments, "draft_path"))
        output = _safe_path(root, _string(arguments, "output_dir"))
        context_value = arguments.get("context_path")
        context = _safe_path(root, context_value) if isinstance(context_value, str) else None
        chunk_size = arguments.get("chunk_size", 8000)
        if type(chunk_size) is not int:
            raise ValueError("chunk_size must be an integer.")
        mode = arguments.get("agent_mode", "deep")
        if not isinstance(mode, str):
            raise ValueError("agent_mode must be a string.")
        translationese = arguments.get("translationese", False)
        if not isinstance(translationese, bool):
            raise ValueError("translationese must be a boolean.")
        book_level = arguments.get("book_level", False)
        if not isinstance(book_level, bool):
            raise ValueError("book_level must be a boolean.")
        output_path, chunks = write_long_form_audit(
            str(draft),
            str(output),
            style=_string(arguments, "style"),
            context_path=str(context) if context else None,
            reference_paths=_path_list(root, arguments.get("reference_paths"), "reference_paths"),
            source_paths=_path_list(root, arguments.get("source_paths"), "source_paths"),
            chunk_size=chunk_size,
            agent_mode=mode,
            translationese=translationese,
            book_level=book_level,
        )
        return _text_result(
            {
                "package_dir": str(output_path),
                "chunk_count": len(chunks),
                "next_action": "Claim and complete the baseline task, then use list_audit_tasks to fan out ready reviews.",
            }
        )
    if name == "list_audit_tasks":
        return _text_result(list_audit_tasks(_safe_path(root, _string(arguments, "package_dir"))))
    if name == "claim_audit_task":
        return _text_result(
            claim_audit_task(
                _safe_path(root, _string(arguments, "package_dir")),
                _string(arguments, "task_id"),
                _optional_string(arguments, "agent_id", "anonymous"),
            )
        )
    if name == "submit_audit_report":
        return _text_result(
            submit_audit_report(
                _safe_path(root, _string(arguments, "package_dir")),
                _string(arguments, "task_id"),
                _string(arguments, "report_markdown"),
                _optional_string(arguments, "agent_id", "anonymous"),
            )
        )
    if name == "verify_audit_coverage":
        return _text_result(verify_long_form_package(str(_safe_path(root, _string(arguments, "package_dir")))))
    if name == "get_reconciliation_task":
        return _text_result(get_reconciliation_task(_safe_path(root, _string(arguments, "package_dir"))))
    if name == "read_project_context":
        path = _safe_path(root, _string(arguments, "path"))
        limit = arguments.get("max_characters", 8000)
        if type(limit) is not int or not 1 <= limit <= MAX_CONTEXT_CHARACTERS:
            raise ValueError(f"max_characters must be between 1 and {MAX_CONTEXT_CHARACTERS}.")
        offset = arguments.get("offset", 0)
        if type(offset) is not int or offset < 0:
            raise ValueError("offset must be a nonnegative integer.")
        if not path.is_file():
            raise ValueError("Context path is not a file.")
        with path.open(encoding="utf-8") as stream:
            remaining = offset
            while remaining:
                skipped = stream.read(min(remaining, MAX_CONTEXT_CHARACTERS))
                if not skipped:
                    break
                remaining -= len(skipped)
            text = stream.read(limit + 1)
        return _text_result(
            {
                "path": str(path),
                "truncated": len(text) > limit,
                "content": text[:limit],
                "next_offset": offset + limit if len(text) > limit else None,
            }
        )
    raise ValueError(f"Unknown tool: {name}")


def _call_writing_tool(name: str, arguments: dict[str, Any], root: Path) -> dict[str, Any]:
    schema = next(tool["inputSchema"] for tool in WRITING_TOOLS if tool["name"] == name)
    properties = schema["properties"]
    if set(arguments) - set(properties):
        raise ValueError("Unknown writing tool arguments.")
    for key in schema["required"]:
        if key not in arguments:
            raise ValueError(f"{key} is required.")
    values = dict(arguments)
    for key, spec in properties.items():
        if key not in values:
            if "default" not in spec:
                continue
            values[key] = spec["default"]
        value = values[key]
        kind = spec["type"]
        if kind == "integer":
            if type(value) is not int or value < spec["minimum"] or value > spec.get("maximum", sys.maxsize):
                raise ValueError(f"{key} must be an integer within the advertised limits.")
        elif kind == "string":
            _bounded_string(values, key, MAX_CONTEXT_CHARACTERS)
        elif kind == "array":
            _string_list(values, key)
        elif kind == "object" and not isinstance(value, dict):
            raise ValueError(f"{key} must be an object.")
        if "enum" in spec and value not in spec["enum"]:
            raise ValueError(f"Invalid {key}.")
    for key in ("outline_path", "output_dir", "package_dir", "output_path"):
        if key in values:
            values[key] = _safe_path(root, values[key])
    for key in ("context_paths", "source_paths", "reference_paths"):
        if key in values:
            values[key] = _path_list(root, values[key], key)
    # Existing package entries may be symlinks even when the package itself is local.
    package = values.get("package_dir", values.get("output_dir"))
    if package is not None and package.is_dir():
        for entry in package.rglob("*"):
            _safe_path(root, str(entry))
    if "result" in values:
        from .writing_queue import MAX_RESULT, _json
        try:
            serialized = _json(values["result"])
        except (ValueError, TypeError) as exc:
            raise ValueError("result must contain valid JSON values.") from exc
        if len(serialized) > MAX_RESULT:
            raise ValueError(f"result must be at most {MAX_RESULT} serialized characters.")
    from . import writing_queue

    try:
        return _text_result(getattr(writing_queue, name)(**values))
    except (KeyError, TypeError) as exc:
        raise ValueError(f"Invalid writing task data: {exc}") from exc


def _string(arguments: dict[str, Any], name: str) -> str:
    value = arguments.get(name)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string.")
    return value


def _optional_string(arguments: dict[str, Any], name: str, default: str) -> str:
    value = arguments.get(name, default)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string.")
    return value


def _optional_nullable_string(arguments: dict[str, Any], name: str, maximum: int | None = None) -> str | None:
    value = arguments.get(name)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string.")
    if maximum is not None and len(value) > maximum:
        raise ValueError(f"{name} must be at most {maximum} characters.")
    return value


def _bounded_string(arguments: dict[str, Any], name: str, maximum: int) -> str:
    value = _string(arguments, name)
    if len(value) > maximum:
        raise ValueError(f"{name} must be at most {maximum} characters.")
    return value


def _string_list(arguments: dict[str, Any], name: str) -> list[str]:
    value = arguments.get(name, [])
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise ValueError(f"{name} must be a list of non-empty strings.")
    return value


def _prompt_descriptors() -> list[dict[str, Any]]:
    return [
        {
            "name": name,
            "description": description,
            "arguments": [
                {"name": "draft", "description": "Text to analyze or rewrite.", "required": True},
                {"name": "style", "description": "Optional style such as fiction or news-report.", "required": False},
                {"name": "context", "description": "Optional ledger or prior-context text.", "required": False},
            ],
        }
        for name, description in PROMPTS
    ]


def get_prompt(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(arguments, dict):
        raise ValueError("Prompt arguments must be an object.")
    draft = _bounded_string(arguments, "draft", MAX_TEXT_CHARACTERS)
    context = _optional_nullable_string(arguments, "context", MAX_CONTEXT_CHARACTERS)
    requested_style = _optional_string(arguments, "style", "fiction")
    if name == "humanize-quick":
        prompt = compile_humanize_prompt_text(draft, style=requested_style, context_text=context)
    elif name == "humanize-deep":
        prompt = compile_humanize_prompt_text(draft, style=requested_style, mode="deep", context_text=context)
    elif name == "dialogue-audit":
        prompt = compile_audit_prompt_text(
            draft,
            document_type="fiction",
            profiles=["voice", "register"],
            context_text=context,
        )
    elif name == "continuity-audit":
        prompt = compile_audit_prompt_text(
            draft,
            document_type="fiction",
            profiles=["full"],
            strict_continuity=True,
            context_text=context,
        )
    elif name == "style-match":
        prompt = compile_humanize_prompt_text(
            draft,
            style=requested_style,
            task="Rewrite with the explicitly supplied style direction while preserving facts and avoiding phrase copying.",
            context_text=context,
        )
    elif name == "serious-rewrite":
        prompt = compile_humanize_prompt_text(
            draft,
            style=requested_style if requested_style != "fiction" else "news-report",
            context_text=context,
            protect_content=True,
        )
    elif name == "extract-ledger":
        prompt = compile_ledger_extraction_prompt_text(draft, context or "")
    else:
        raise ValueError(f"Unknown prompt: {name}")
    return {
        "description": dict(PROMPTS)[name],
        "messages": [{"role": "user", "content": {"type": "text", "text": prompt}}],
    }


def handle_message(message: Any, root: Path) -> Any:
    """Handle the MCP methods needed by current Agent hosts."""

    if isinstance(message, list):
        if not message:
            return _error(None, -32600, "Invalid Request: empty batch")
        responses = [handle_message(item, root) if isinstance(item, dict) else
                     _error(None, -32600, "Invalid Request") for item in message]
        return [response for response in responses if response is not None] or None
    if not isinstance(message, dict) or message.get("jsonrpc") != "2.0":
        return _error(None, -32600, "Invalid Request: expected JSON-RPC 2.0")
    request_id = message.get("id")
    if "id" in message and (request_id is None or type(request_id) not in (str, int)):
        return _error(None, -32600, "Invalid Request: invalid request ID")
    method = message.get("method")
    if method is None and "id" in message and ("result" in message or "error" in message):
        return None
    if not isinstance(method, str):
        return _error(request_id, -32600, "Invalid Request: method is required")
    if "id" not in message:
        return None
    if "params" in message and not isinstance(message["params"], dict):
        return _error(request_id, -32602, "Parameters must be an object")
    if method == "initialize":
        return _result(
            request_id,
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {"listChanged": False}, "prompts": {"listChanged": False}},
                "serverInfo": SERVER_INFO,
                "instructions": "For requested prose, compile_generation_prompt before drafting and apply the genre-aware quality constraints. For rewriting use compile_humanize_prompt, then verify meaning and protected literals. Keep factual source_paths separate from voice reference_paths and use project-local paths only. For long-form review, plan bounded tasks, submit complete receipts, verify coverage, then reconcile. For long-form drafting, plan_long_form_writing, claim ready tasks for role prompts and result schemas, submit structured results, verify_writing_project, then assemble_writing_project.",
            },
        )
    if method == "ping":
        return _result(request_id, {})
    if method == "tools/list":
        return _result(request_id, {"tools": TOOLS})
    if method == "prompts/list":
        return _result(request_id, {"prompts": _prompt_descriptors()})
    if method == "prompts/get":
        params = message.get("params", {})
        if not isinstance(params, dict) or not isinstance(params.get("name"), str):
            return _error(request_id, -32602, "prompts/get requires a prompt name")
        try:
            return _result(request_id, get_prompt(params["name"], params.get("arguments", {})))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            return _error(request_id, -32602, f"{type(exc).__name__}: {exc}")
    if method == "tools/call":
        params = message.get("params", {})
        if not isinstance(params, dict) or not isinstance(params.get("name"), str):
            return _error(request_id, -32602, "tools/call requires a tool name")
        try:
            return _result(request_id, call_tool(params["name"], params.get("arguments", {}), root))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            return _result(request_id, _text_result(f"{type(exc).__name__}: {exc}", is_error=True))
    return _error(request_id, -32601, f"Method not found: {method}")


def _result(request_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _error(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def run_stdio(root: Path) -> None:
    for line in sys.stdin:
        try:
            message = json.loads(line)
            response = handle_message(message, root)
        except (ValueError, json.JSONDecodeError) as exc:
            response = _error(None, -32700, f"Parse error: {exc}")
        if response is not None:
            print(json.dumps(response, ensure_ascii=False), flush=True)


def _http_handler(root: Path, auth_token: str | None):
    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            super().setup()
            self.connection.settimeout(10)

        def _check_request(self):
            if self.path != "/mcp":
                self.send_error(HTTPStatus.NOT_FOUND)
                return False
            # This local transport serves native MCP clients, with no browser origins allowed.
            if self.headers.get("Origin") is not None:
                self.send_error(HTTPStatus.FORBIDDEN, "Browser origins are not allowed")
                return False
            if auth_token and self.headers.get("Authorization") != f"Bearer {auth_token}":
                self.send_error(HTTPStatus.UNAUTHORIZED)
                return False
            return True

        def do_GET(self) -> None:  # noqa: N802
            if self._check_request():
                self.send_response(HTTPStatus.METHOD_NOT_ALLOWED)
                self.send_header("Allow", "POST")
                self.end_headers()

        do_DELETE = do_GET

        def do_POST(self) -> None:  # noqa: N802 - HTTP method name is defined by BaseHTTPRequestHandler.
            if not self._check_request():
                return
            if self.headers.get("Transfer-Encoding"):
                self.send_error(HTTPStatus.BAD_REQUEST, "Transfer-Encoding is unsupported")
                return
            if self.headers.get_content_type() != "application/json":
                self.send_error(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
                return
            length = self.headers.get("Content-Length")
            try:
                body_length = int(length) if length else 0
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid Content-Length")
                return
            if not 0 < body_length <= MAX_HTTP_BODY_BYTES:
                self.send_error(HTTPStatus.REQUEST_ENTITY_TOO_LARGE if body_length > MAX_HTTP_BODY_BYTES
                                else HTTPStatus.BAD_REQUEST, "Invalid Content-Length")
                return
            try:
                message = json.loads(self.rfile.read(body_length))
                response = handle_message(message, root)
            except (ValueError, json.JSONDecodeError) as exc:
                response = _error(None, -32700, f"Parse error: {exc}")
            except TimeoutError:
                self.send_error(HTTPStatus.REQUEST_TIMEOUT)
                return
            if response is None:
                self.send_response(HTTPStatus.ACCEPTED)
                self.end_headers()
                return
            payload = json.dumps(response, ensure_ascii=False).encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, format: str, *args: Any) -> None:
            return

    return Handler


def run_http(root: Path, host: str, port: int, auth_token: str | None) -> None:
    if host not in {"127.0.0.1", "::1", "localhost"} and not auth_token:
        raise ValueError("A non-loopback HTTP server requires --auth-token.")
    class Server(ThreadingHTTPServer):
        address_family = socket.AF_INET6 if ":" in host else socket.AF_INET

    server = Server((host, port), _http_handler(root, auth_token))
    print(f"Human Writing MCP listening on http://{host}:{port}/mcp", file=sys.stderr)
    server.serve_forever()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="human-writing-mcp",
        description="Serve verified, project-local long-form writing audit tools over MCP.",
    )
    parser.add_argument("--root", default=".", help="Workspace root allowed to the MCP server. Default: current directory.")
    parser.add_argument("--http", action="store_true", help="Serve a JSON MCP endpoint instead of stdio.")
    parser.add_argument("--host", default="127.0.0.1", help="HTTP bind host. Default: 127.0.0.1.")
    parser.add_argument("--port", type=int, default=8765, help="HTTP bind port. Default: 8765.")
    parser.add_argument("--auth-token", help="Bearer token required for HTTP requests. Required on non-loopback hosts.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).resolve()
    if not root.is_dir():
        raise SystemExit("--root must be an existing directory.")
    if args.http:
        try:
            run_http(root, args.host, args.port, args.auth_token)
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc
        return 0
    run_stdio(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
