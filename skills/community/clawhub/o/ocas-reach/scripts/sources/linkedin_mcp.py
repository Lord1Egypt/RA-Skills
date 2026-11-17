"""LinkedIn MCP Server connector for Reach.

Invokes linkedin-scraper-mcp (pip package) via stdio JSON-RPC to access LinkedIn
profiles, companies, jobs, and messaging. Requires LinkedIn browser session
(login via --login flag on first use).

MCP server: linkedin-scraper-mcp (pip/PyPI)
Install:   pip install linkedin-scraper-mcp
Login:     uvx linkedin-scraper-mcp@latest --login  (one-time, saves browser profile)
"""
from __future__ import annotations

import json
import subprocess
import threading
from typing import Any, Dict, Optional

from ._mcp_client import MCPClient


class _MCPClient(MCPClient):
    """LinkedIn-specific MCP client (uses uvx launcher)."""
    pass


# ── Module-level client cache ──────────────────────────────────────────────
_client: Optional[_MCPClient] = None


def _get_client(auth: dict) -> _MCPClient:
    global _client
    if _client is None or _client._proc is None or _client._proc.poll() is not None:
        env = {}
        for key in ("LINKEDIN_USER_DATA_DIR", "LINKEDIN_CHROME_PATH"):
            val = auth.get(key) or auth.get(key.lower())
            if val:
                env[key] = val
        _client = _MCPClient(["uvx", "linkedin-scraper-mcp@latest"], env=env if env else None)
        _client.start()
    return _client


def _close_client():
    global _client
    if _client:
        _client.close()
        _client = None


# ── Reach query interface ──────────────────────────────────────────────────

def query(action: str, params: dict, auth: dict) -> dict:
    """
    Reach-facing query entry point.

    Actions:
      person_profile    — Get a person's LinkedIn profile. Params: public_id, sections
      my_profile        — Get authenticated user's profile. Params: sections
      company_profile   — Get company info. Params: public_id, sections
      company_posts     — Get company posts. Params: public_id, limit
      company_employees — List company employees. Params: public_id, keyword, limit
      search_people     — Search for people. Params: keywords, location, company, limit
      search_companies  — Search for companies. Params: keywords, limit
      search_jobs       — Search for jobs. Params: keywords, location, limit
      job_details       — Get job details. Params: job_id
      feed              — Get user's home feed. Params: limit
      inbox             — List conversations. Params: limit
      conversation      — Read a conversation. Params: username or thread_id
      search_messages   — Search messages. Params: query
      send_message      — Send a message. Params: username, message
      sidebar_profiles  — Get sidebar recommendations from a profile. Params: public_id
    """
    client = _get_client(auth)

    try:
        action_map = {
            "person_profile": _action_person_profile,
            "my_profile": _action_my_profile,
            "company_profile": _action_company_profile,
            "company_posts": _action_company_posts,
            "company_employees": _action_company_employees,
            "search_people": _action_search_people,
            "search_companies": _action_search_companies,
            "search_jobs": _action_search_jobs,
            "job_details": _action_job_details,
            "feed": _action_feed,
            "inbox": _action_inbox,
            "conversation": _action_conversation,
            "search_messages": _action_search_messages,
            "send_message": _action_send_message,
            "sidebar_profiles": _action_sidebar_profiles,
        }
        handler = action_map.get(action)
        if handler is None:
            return {"error": f"Unknown action: {action}", "valid_actions": list(action_map.keys())}
        return handler(client, params)
    except Exception as e:
        _close_client()
        return {"error": str(e), "action": action}


def _sections_arg(params: dict) -> dict:
    """Build sections parameter from comma-separated string or list."""
    sections = params.get("sections", [])
    if isinstance(sections, str):
        sections = [s.strip() for s in sections.split(",") if s.strip()]
    return sections


def _action_person_profile(client: _MCPClient, params: dict) -> dict:
    if not params.get("public_id"):
        return {"error": "person_profile requires 'public_id'"}
    args = {"public_id": params["public_id"]}
    sections = _sections_arg(params)
    if sections:
        args["sections"] = sections
    return client.call_tool("get_person_profile", args)


def _action_my_profile(client: _MCPClient, params: dict) -> dict:
    args: dict = {}
    sections = _sections_arg(params)
    if sections:
        args["sections"] = sections
    return client.call_tool("get_my_profile", args)


def _action_company_profile(client: _MCPClient, params: dict) -> dict:
    if not params.get("public_id"):
        return {"error": "company_profile requires 'public_id'"}
    args = {"public_id": params["public_id"]}
    sections = _sections_arg(params)
    if sections:
        args["sections"] = sections
    return client.call_tool("get_company_profile", args)


def _action_company_posts(client: _MCPClient, params: dict) -> dict:
    if not params.get("public_id"):
        return {"error": "company_posts requires 'public_id'"}
    args = {"public_id": params["public_id"]}
    if params.get("limit"):
        args["limit"] = int(params["limit"])
    return client.call_tool("get_company_posts", args)


def _action_company_employees(client: _MCPClient, params: dict) -> dict:
    if not params.get("public_id"):
        return {"error": "company_employees requires 'public_id'"}
    args = {"public_id": params["public_id"]}
    if params.get("keyword"):
        args["keyword"] = params["keyword"]
    if params.get("limit"):
        args["limit"] = int(params["limit"])
    return client.call_tool("get_company_employees", args)


def _action_search_people(client: _MCPClient, params: dict) -> dict:
    args: dict = {}
    if params.get("keywords"):
        args["keywords"] = params["keywords"]
    if params.get("location"):
        args["location"] = params["location"]
    if params.get("company"):
        args["current_company"] = params["company"]
    if params.get("connection_degree"):
        args["connection_degree"] = params["connection_degree"]
    if params.get("limit"):
        args["limit"] = int(params["limit"])
    return client.call_tool("search_people", args)


def _action_search_companies(client: _MCPClient, params: dict) -> dict:
    args: dict = {}
    if params.get("keywords"):
        args["keywords"] = params["keywords"]
    if params.get("limit"):
        args["limit"] = int(params["limit"])
    return client.call_tool("search_companies", args)


def _action_search_jobs(client: _MCPClient, params: dict) -> dict:
    args: dict = {}
    if params.get("keywords"):
        args["keywords"] = params["keywords"]
    if params.get("location"):
        args["location"] = params["location"]
    if params.get("limit"):
        args["limit"] = int(params["limit"])
    return client.call_tool("search_jobs", args)


def _action_job_details(client: _MCPClient, params: dict) -> dict:
    if not params.get("job_id"):
        return {"error": "job_details requires 'job_id'"}
    return client.call_tool("get_job_details", {"job_id": params["job_id"]})


def _action_feed(client: _MCPClient, params: dict) -> dict:
    args: dict = {}
    if params.get("limit"):
        args["limit"] = int(params["limit"])
    return client.call_tool("get_feed", args)


def _action_inbox(client: _MCPClient, params: dict) -> dict:
    args: dict = {}
    if params.get("limit"):
        args["limit"] = int(params["limit"])
    return client.call_tool("get_inbox", args)


def _action_conversation(client: _MCPClient, params: dict) -> dict:
    if params.get("username"):
        return client.call_tool("get_conversation", {"username": params["username"]})
    elif params.get("thread_id"):
        return client.call_tool("get_conversation", {"thread_id": params["thread_id"]})
    else:
        return {"error": "conversation requires 'username' or 'thread_id'"}


def _action_search_messages(client: _MCPClient, params: dict) -> dict:
    if not params.get("query"):
        return {"error": "search_messages requires 'query'"}
    return client.call_tool("search_conversations", {"query": params["query"]})


def _action_send_message(client: _MCPClient, params: dict) -> dict:
    if not params.get("username") or not params.get("message"):
        return {"error": "send_message requires 'username' and 'message'"}
    return client.call_tool("send_message", {"username": params["username"], "message": params["message"]})


def _action_sidebar_profiles(client: _MCPClient, params: dict) -> dict:
    if not params.get("public_id"):
        return {"error": "sidebar_profiles requires 'public_id'"}
    return client.call_tool("get_sidebar_profiles", {"public_id": params["public_id"]})
