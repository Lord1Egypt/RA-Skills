from __future__ import annotations

import argparse
import json
import sys
from typing import Optional, Sequence

from .client import MemosClient
from .config import load_config
from .errors import MemosCloudError, ValidationError, print_error
from .files import build_file_payloads, build_stdin_file_payload
from .operations import (
    add_feedback,
    add_kb_doc,
    add_message,
    create_knowledge_base,
    delete_kb_documents,
    delete_memory,
    get_kb_documents,
    get_user_profile,
    remove_knowledge_base,
    search_memory,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="MemOS Cloud Server API Client")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_search = subparsers.add_parser("search", help="Search memory")
    p_search.add_argument("user_id", nargs="?", default=None, help="User ID (falls back to MEMOS_USER_ID env var)")
    p_search.add_argument("query", help="Search query string")
    p_search.add_argument("--conversation-id", help="Optional conversation ID")
    p_search.add_argument("--conversation-first-message", help="First message in conversation (alternative to --conversation-id, auto-generates ID via MD5)")
    p_search.add_argument("--filter", dest="filter_json", help='Filter conditions as JSON string, e.g. \'{"and":[{"agent_id":"xxx"}]}\'')
    p_search.add_argument("--knowledgebase-ids", help='Comma-separated knowledgebase IDs, or "all"')
    p_search.add_argument("--memory-limit-number", type=int, help="Max factual memories to return (default 9, max 25)")
    p_search.add_argument("--include-preference", type=_str_to_bool, default=None, help="Enable preference memory recall (default true)")
    p_search.add_argument("--preference-limit-number", type=int, help="Max preference memories (default 9, max 25)")
    p_search.add_argument("--include-tool-memory", type=_str_to_bool, default=None, help="Enable tool memory recall (default false)")
    p_search.add_argument("--tool-memory-limit-number", type=int, help="Max tool memories (default 6, max 25)")
    p_search.add_argument("--include-skill", type=_str_to_bool, default=None, help="Enable skill recall (default false)")
    p_search.add_argument("--skill-limit-number", type=int, help="Max skills (default 6, max 25)")
    p_search.add_argument("--relativity", type=float, help="Relevance threshold 0-1 (default 0.45)")

    p_add = subparsers.add_parser("add_message", help="Add a message memory")
    p_add.add_argument("user_id", nargs="?", default=None, help="User ID (falls back to MEMOS_USER_ID env var)")
    p_add.add_argument("conversation_id", nargs="?", default=None, help="Conversation ID (or use --conversation-first-message)")
    p_add.add_argument(
        "messages",
        help='Messages as a JSON string. e.g. \'[{"role":"user","content":"hello"}]\'',
    )
    p_add.add_argument("--conversation-first-message", help="First message in conversation (auto-generates conversation_id via MD5)")
    p_add.add_argument("--tags", help="Comma-separated tags")
    p_add.add_argument("--info", dest="info_json", help='Custom metadata as JSON string')
    p_add.add_argument("--allow-knowledgebase-ids", help="Comma-separated knowledgebase IDs")
    p_add.add_argument("--agent-id", help="Agent ID for multi-agent isolation (overrides MEMOS_AGENT_ID env var)")
    p_add.add_argument("--app-id", help="App ID for multi-app isolation (overrides MEMOS_APP_ID env var)")

    p_del = subparsers.add_parser("delete", help="Delete memory")
    p_del.add_argument("memory_ids", help="Comma-separated list of memory IDs to delete (Required)")

    p_fb = subparsers.add_parser("add_feedback", help="Add feedback")
    p_fb.add_argument("user_id", nargs="?", default=None, help="User ID (falls back to MEMOS_USER_ID env var)")
    p_fb.add_argument("conversation_id", nargs="?", default=None, help="Conversation ID (or use --conversation-first-message)")
    p_fb.add_argument("feedback_content", help="Feedback content text")
    p_fb.add_argument("--conversation-first-message", help="Session anchor (first user message of the session) — auto-generates conversation_id via MD5. Must match the value used when the targeted memory was written.")
    p_fb.add_argument("--allow-knowledgebase-ids", help="Comma-separated list of knowledgebase IDs")
    p_fb.add_argument("--feedback-time", help="Feedback time string (structured time or natural language)")
    p_fb.add_argument("--agent-id", help="Agent ID for multi-agent isolation (overrides MEMOS_AGENT_ID env var)")
    p_fb.add_argument("--app-id", help="App ID for multi-app isolation (overrides MEMOS_APP_ID env var)")

    p_kb = subparsers.add_parser("add_kb_doc", help="Upload files to knowledge base")
    p_kb.add_argument("knowledgebase_id", help="Target knowledge base ID")
    p_kb.add_argument(
        "files",
        nargs="*",
        help="Files to upload: URLs (http/https) or local file paths (auto-converted to base64)",
    )
    p_kb.add_argument(
        "--type",
        dest="file_type",
        default="document",
        choices=["document", "skill"],
        help="File type: document (default) or skill",
    )
    p_kb.add_argument("--name", help="Filename for stdin content (recommended with --stdin)")
    p_kb.add_argument(
        "--stdin",
        action="store_true",
        help="Read base64 content from stdin (pipe-friendly, avoids context overhead)",
    )

    # get_user_profile
    p_profile = subparsers.add_parser("get_user_profile", help="Get user memory profile")
    p_profile.add_argument("user_id", nargs="?", default=None, help="User ID (falls back to MEMOS_USER_ID env var)")
    p_profile.add_argument("--page", type=int, help="Page number (default 1)")
    p_profile.add_argument("--size", type=int, help="Page size (default 10, max 50)")
    p_profile.add_argument("--filter", dest="filter_json", help='Filter conditions as JSON string')
    p_profile.add_argument("--include-preference", type=_str_to_bool, default=None, help="Include preference memories (default true)")
    p_profile.add_argument("--include-tool-memory", type=_str_to_bool, default=None, help="Include tool memories (default false)")

    # create_knowledge_base
    p_create_kb = subparsers.add_parser("create_kb", help="Create a knowledge base")
    p_create_kb.add_argument("knowledgebase_name", help="Knowledge base name")
    p_create_kb.add_argument("--description", help="Knowledge base description")

    # get_kb_documents
    p_get_kb = subparsers.add_parser("get_kb_docs", help="Get knowledge base documents")
    p_get_kb.add_argument("--file-ids", help="Comma-separated file IDs (mutually exclusive with --knowledgebase-id)")
    p_get_kb.add_argument("--knowledgebase-id", help="Knowledge base ID (mutually exclusive with --file-ids)")
    p_get_kb.add_argument("--type", dest="doc_type", choices=["document", "skill"], help="Filter by file type (only with --knowledgebase-id)")
    p_get_kb.add_argument("--page", type=int, help="Page number (default 1, only with --knowledgebase-id)")
    p_get_kb.add_argument("--page-size", type=int, help="Page size (default 20, only with --knowledgebase-id)")

    # delete_kb_documents
    p_del_kb = subparsers.add_parser("delete_kb_docs", help="Delete knowledge base documents")
    p_del_kb.add_argument("file_ids", help="Comma-separated file IDs to delete")

    # remove_knowledge_base
    p_rm_kb = subparsers.add_parser("remove_kb", help="Remove a knowledge base")
    p_rm_kb.add_argument("knowledgebase_id", help="Knowledge base ID to remove")

    return parser


def main(
    argv: Optional[Sequence[str]] = None,
    stdin_buffer=None,
    client: Optional[MemosClient] = None,
) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        active_client = client or MemosClient(load_config())
        result = dispatch(args, active_client, stdin_buffer or sys.stdin.buffer)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except MemosCloudError as exc:
        print_error(exc)
        return 1
    except Exception as exc:
        print(json.dumps({"error": "Unexpected Error", "message": str(exc)}), file=sys.stderr)
        return 1


def _str_to_bool(value: str) -> bool:
    if value.lower() in ("true", "1", "yes"):
        return True
    if value.lower() in ("false", "0", "no"):
        return False
    raise argparse.ArgumentTypeError(f"Boolean value expected, got '{value}'")


def _resolve_user_id(args: argparse.Namespace, client: MemosClient) -> str:
    user_id = getattr(args, "user_id", None) or client.config.user_id
    if not user_id:
        raise ValidationError(
            "user_id is required. Provide it as an argument or set MEMOS_USER_ID env var."
        )
    return user_id


def _parse_filter(filter_json: Optional[str]) -> Optional[dict]:
    if filter_json is None:
        return None
    try:
        return json.loads(filter_json)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"filter must be a valid JSON string: {exc}") from exc


def dispatch(args: argparse.Namespace, client: MemosClient, stdin_buffer):
    if args.command == "search":
        return search_memory(
            client,
            _resolve_user_id(args, client),
            args.query,
            args.conversation_id,
            args.conversation_first_message,
            _parse_filter(args.filter_json),
            args.knowledgebase_ids,
            args.memory_limit_number,
            args.include_preference,
            args.preference_limit_number,
            args.include_tool_memory,
            args.tool_memory_limit_number,
            args.include_skill,
            args.skill_limit_number,
            args.relativity,
        )

    if args.command == "add_message":
        return add_message(
            client,
            _resolve_user_id(args, client),
            args.conversation_id,
            args.messages,
            args.conversation_first_message,
            args.agent_id or client.config.agent_id,
            args.app_id or client.config.app_id,
            args.tags,
            args.info_json,
            client.config.allow_public,
            args.allow_knowledgebase_ids,
            client.config.async_mode,
        )

    if args.command == "delete":
        return delete_memory(client, args.memory_ids)

    if args.command == "add_feedback":
        return add_feedback(
            client,
            _resolve_user_id(args, client),
            args.conversation_id,
            args.feedback_content,
            args.allow_knowledgebase_ids,
            args.agent_id or client.config.agent_id,
            args.app_id or client.config.app_id,
            args.feedback_time,
            client.config.allow_public,
            args.conversation_first_message,
        )

    if args.command == "add_kb_doc":
        file_list = _build_kb_files(args, stdin_buffer)
        return add_kb_doc(client, args.knowledgebase_id, file_list)

    if args.command == "get_user_profile":
        return get_user_profile(
            client,
            _resolve_user_id(args, client),
            args.page,
            args.size,
            _parse_filter(args.filter_json),
            args.include_preference,
            args.include_tool_memory,
        )

    if args.command == "create_kb":
        return create_knowledge_base(client, args.knowledgebase_name, args.description)

    if args.command == "get_kb_docs":
        return get_kb_documents(
            client,
            args.file_ids,
            args.knowledgebase_id,
            args.doc_type,
            args.page,
            args.page_size,
        )

    if args.command == "delete_kb_docs":
        return delete_kb_documents(client, args.file_ids)

    if args.command == "remove_kb":
        return remove_knowledge_base(client, args.knowledgebase_id)

    parser = build_parser()
    parser.error(f"Unknown command: {args.command}")


def _build_kb_files(args: argparse.Namespace, stdin_buffer):
    if args.stdin:
        return [build_stdin_file_payload(stdin_buffer, args.file_type, args.name)]

    if args.files:
        return build_file_payloads(args.files, args.file_type)

    raise ValidationError("Either provide files or use --stdin")
