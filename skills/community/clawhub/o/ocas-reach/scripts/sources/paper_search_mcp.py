"""Paper Search MCP connector for Reach.

Invokes paper-search-mcp (pip package) via stdio JSON-RPC to search and download
academic papers from 20+ sources (arXiv, PubMed, bioRxiv, Semantic Scholar, etc.).

MCP server: paper-search-mcp (pip/PyPI)
Install:   pip install paper-search-mcp
"""
from __future__ import annotations

import json
import subprocess
import threading
from typing import Any, Dict, Optional

from ._mcp_client import MCPClient


class _MCPClient(MCPClient):
    """Paper-search-specific MCP client (uses python3 -m launcher)."""
    pass


# ── Module-level client cache ──────────────────────────────────────────────
_client: Optional[_MCPClient] = None


def _get_client(auth: dict) -> _MCPClient:
    global _client
    if _client is None or _client._proc is None or _client._proc.poll() is not None:
        env = {}
        for key in ("PAPER_SEARCH_MCP_SEMANTIC_SCHOLAR_KEY", "PAPER_SEARCH_MCP_CORE_KEY",
                     "PAPER_SEARCH_MCP_UNPAYWALL_EMAIL", "PAPER_SEARCH_MCP_GOOGLE_SCHOLAR_PROXY_URL"):
            val = auth.get(key) or auth.get(key.lower())
            if val:
                env[key] = val
        _client = _MCPClient(["python3", "-m", "paper_search_mcp.server"], env=env if env else None)
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
      search       — Search arXiv (default multi-source entry point). Params: query, limit
      arxiv        — Search arXiv specifically. Params: query, limit
      pubmed       — Search PubMed. Params: query, limit
      biorxiv      — Search bioRxiv. Params: query, limit
      medrxiv      — Search medRxiv. Params: query, limit
      google_scholar — Search Google Scholar. Params: query, limit
      download     — Download a paper PDF. Params: doi or url, source
    """
    client = _get_client(auth)

    try:
        action_map = {
            "search": _action_search,
            "arxiv": _action_arxiv,
            "pubmed": _action_pubmed,
            "biorxiv": _action_biorxiv,
            "medrxiv": _action_medrxiv,
            "google_scholar": _action_google_scholar,
            "download": _action_download,
        }
        handler = action_map.get(action)
        if handler is None:
            return {"error": f"Unknown action: {action}", "valid_actions": list(action_map.keys())}
        return handler(client, params)
    except Exception as e:
        _close_client()
        return {"error": str(e), "action": action}


def _action_search(client: _MCPClient, params: dict) -> dict:
    args = {"query": params.get("query", "")}
    if params.get("limit"):
        args["limit"] = int(params["limit"])
    if params.get("sources"):
        args["sources"] = params["sources"]
    return client.call_tool("search", args)


def _action_arxiv(client: _MCPClient, params: dict) -> dict:
    args = {"query": params.get("query", "")}
    if params.get("limit"):
        args["limit"] = int(params["limit"])
    return client.call_tool("search_arxiv", args)


def _action_pubmed(client: _MCPClient, params: dict) -> dict:
    args = {"query": params.get("query", "")}
    if params.get("limit"):
        args["limit"] = int(params["limit"])
    return client.call_tool("search_pubmed", args)


def _action_biorxiv(client: _MCPClient, params: dict) -> dict:
    args = {"query": params.get("query", "")}
    if params.get("limit"):
        args["limit"] = int(params["limit"])
    return client.call_tool("search_biorxiv", args)


def _action_medrxiv(client: _MCPClient, params: dict) -> dict:
    args = {"query": params.get("query", "")}
    if params.get("limit"):
        args["limit"] = int(params["limit"])
    return client.call_tool("search_medrxiv", args)


def _action_google_scholar(client: _MCPClient, params: dict) -> dict:
    args = {"query": params.get("query", "")}
    if params.get("limit"):
        args["limit"] = int(params["limit"])
    return client.call_tool("search_google_scholar", args)


def _action_download(client: _MCPClient, params: dict) -> dict:
    if params.get("doi"):
        return client.call_tool("download_pdf", {"doi": params["doi"], "source": params.get("source", "arxiv")})
    if params.get("url"):
        return client.call_tool("download_pdf", {"url": params["url"], "source": params.get("source", "arxiv")})
    return {"error": "download requires 'doi' or 'url'"}
