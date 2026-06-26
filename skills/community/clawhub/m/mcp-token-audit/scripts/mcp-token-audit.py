#!/usr/bin/env python3
"""
MCP Token Auditor — Analyze MCP server configs and estimate token consumption per tool.

Usage:
  python3 mcp-token-audit.py [--config PATH] [--output PATH] [--max-tokens N]

Reads Claude Code's mcp.json (or any MCP config), estimates token cost per tool
based on schema complexity, and outputs an optimization report with per-role groupings.

Flags:
  --config PATH    Path to MCP config JSON (default: ~/.claude/mcp.json)
  --output PATH    Write report to file (default: stdout)
  --max-tokens N   Target max tokens per agent role (default: 60000)
  --json           Output as JSON instead of human-readable
"""

import json
import os
import re
import sys
import argparse
from collections import defaultdict
from pathlib import Path

# Token estimation constants (conservative, based on Sonnet 4 tokenizer patterns)
TOKENS_PER_CHAR = 0.3  # ~3 chars per token for JSON/schema text
TOKENS_PER_TOOL_OVERHEAD = 150  # Fixed overhead per tool definition
TOKENS_PER_SERVER_OVERHEAD = 200  # Fixed overhead per server connection

SCHEMA_TOKENS = {
    "string": 20,
    "number": 15,
    "boolean": 10,
    "array": 30,
    "object": 25,
    "null": 5,
}

ROLE_PRESETS = {
    "code-analysis": ["eslint", "sonarqube", "tree-sitter", "prettier", "linter", "type-check"],
    "deployment": ["docker", "k8s", "kubernetes", "terraform", "aws", "gcloud", "pulumi", "ansible"],
    "testing": ["jest", "playwright", "cypress", "pytest", "coverage", "vitest", "mocha"],
    "data": ["postgres", "mysql", "sqlite", "redis", "mongodb", "snowflake", "bigquery"],
    "communication": ["slack", "linear", "jira", "github", "notion", "email", "discord"],
    "file-system": ["filesystem", "file", "fs", "workspace", "edit", "write", "read"],
}


def estimate_tokens_for_schema(schema, depth=0):
    """Recursively estimate tokens for a JSON schema."""
    if not schema or not isinstance(schema, dict):
        return 10

    tokens = 0
    schema_type = schema.get("type", "object")
    tokens += SCHEMA_TOKENS.get(schema_type, 20)

    # Properties
    props = schema.get("properties", {})
    for prop_name, prop_schema in props.items():
        tokens += len(prop_name) * TOKENS_PER_CHAR
        tokens += estimate_tokens_for_schema(prop_schema, depth + 1)

    # Description adds tokens
    desc = schema.get("description", "")
    if desc:
        tokens += len(desc) * TOKENS_PER_CHAR

    # Enum values
    enum_vals = schema.get("enum", [])
    for val in enum_vals:
        tokens += len(str(val)) * TOKENS_PER_CHAR

    # Required fields
    required = schema.get("required", [])
    tokens += len(required) * 5

    # Items in arrays
    items = schema.get("items")
    if items and isinstance(items, dict):
        tokens += estimate_tokens_for_schema(items, depth + 1)

    return int(tokens)


def analyze_config(config_path, max_tokens=60000):
    """Main analysis function."""
    config_path = os.path.expanduser(config_path)

    if not os.path.exists(config_path):
        return {"error": f"Config not found: {config_path}"}

    with open(config_path) as f:
        config = json.load(f)

    servers = config.get("mcpServers", {})
    if not servers:
        return {"error": "No mcpServers found in config"}

    tools = []
    total_tokens = 0
    server_tool_counts = defaultdict(int)

    for server_name, server_config in servers.items():
        server_tokens = TOKENS_PER_SERVER_OVERHEAD
        tool_count = 0

        # If server has tool definitions inline
        tools_def = server_config.get("tools", [])
        if not tools_def:
            # Try to estimate from known patterns if tools aren't listed
            estimated_tools = estimate_known_tools(server_name)
            for tool_name in estimated_tools:
                est_tokens = TOKENS_PER_TOOL_OVERHEAD + (len(tool_name) * TOKENS_PER_CHAR * 5)
                tools.append({
                    "server": server_name,
                    "tool": tool_name,
                    "tokens": int(est_tokens),
                    "estimated": True
                })
                server_tokens += est_tokens
                tool_count += 1
        else:
            for tool_def in tools_def:
                tool_name = tool_def.get("name", "unknown")
                schema = tool_def.get("inputSchema", tool_def.get("parameters", {}))
                schema_tokens = estimate_tokens_for_schema(schema)
                tool_tokens = TOKENS_PER_TOOL_OVERHEAD + schema_tokens
                tools.append({
                    "server": server_name,
                    "tool": tool_name,
                    "tokens": int(tool_tokens),
                    "estimated": False
                })
                server_tokens += tool_tokens
                tool_count += 1

        server_tool_counts[server_name] = tool_count
        total_tokens += server_tokens

    # Assign roles based on tool patterns
    role_assignments = assign_roles(tools)

    # Calculate per-role token totals
    role_totals = defaultdict(int)
    for tool in tools:
        role = role_assignments.get(tool["server"], "general")
        role_totals[role] += tool["tokens"]

    # Build optimization suggestions
    suggestions = []
    if total_tokens > max_tokens:
        overage = total_tokens - max_tokens
        suggestions.append({
            "severity": "critical",
            "message": f"Total tool schema tokens ({total_tokens:,}) exceed target ({max_tokens:,}) by {overage:,} tokens",
            "fix": "Split MCP servers into per-role configs and load only what each subagent needs"
        })

    for role, tokens in sorted(role_totals.items(), key=lambda x: -x[1]):
        if tokens > max_tokens:
            suggestions.append({
                "severity": "warning",
                "message": f"Role '{role}' uses {tokens:,} tokens — split into smaller subgroups",
                "fix": f"Break '{role}' role into {role}-1 and {role}-2 with ~50k each"
            })

    # Find biggest token hogs
    tools_sorted = sorted(tools, key=lambda x: -x["tokens"])
    top_hogs = tools_sorted[:10]

    return {
        "config_path": config_path,
        "server_count": len(servers),
        "total_tools": len(tools),
        "total_tokens": int(total_tokens),
        "max_tokens_target": max_tokens,
        "utilization_pct": round((total_tokens / max_tokens) * 100, 1),
        "per_server": [
            {"server": s, "tools": c, "tokens": sum(t["tokens"] for t in tools if t["server"] == s)}
            for s, c in sorted(server_tool_counts.items(), key=lambda x: -x[1])
        ],
        "per_role": [
            {"role": r, "tokens": int(t)} for r, t in sorted(role_totals.items(), key=lambda x: -x[1])
        ],
        "top_token_hogs": [
            {"server": t["server"], "tool": t["tool"], "tokens": t["tokens"]} for t in top_hogs
        ],
        "suggestions": suggestions,
        "role_groupings": suggest_role_groupings(tools, role_assignments, max_tokens),
    }


def estimate_known_tools(server_name):
    """Estimate tool count for well-known MCP servers."""
    known = {
        "github": ["create_issue", "search_repos", "get_file", "create_pr", "list_issues", "search_code"],
        "postgres": ["query", "list_tables", "describe_table", "execute"],
        "filesystem": ["read_file", "write_file", "list_directory", "search_files", "get_file_info"],
        "slack": ["send_message", "list_channels", "get_thread", "search_messages"],
        "docker": ["list_containers", "run_container", "stop_container", "get_logs"],
        "playwright": ["navigate", "click", "type", "screenshot", "evaluate"],
        "puppeteer": ["goto", "click", "type", "screenshot", "evaluate"],
        "brave-search": ["web_search", "local_search"],
        "memory": ["create_entities", "search_nodes", "open_nodes"],
        "fetch": ["fetch", "get"],
    }
    for key, tools in known.items():
        if key.lower() in server_name.lower():
            return tools
    return [f"{server_name}_tool_{i}" for i in range(1, 4)]


def assign_roles(tools):
    """Assign each server to a role based on name matching."""
    roles = {}
    for tool in tools:
        server = tool["server"].lower()
        for role, keywords in ROLE_PRESETS.items():
            if any(kw in server for kw in keywords):
                roles[tool["server"]] = role
                break
        if tool["server"] not in roles:
            roles[tool["server"]] = "general"
    return roles


def suggest_role_groupings(tools, roles, max_tokens):
    """Suggest per-role MCP config groupings."""
    role_tools = defaultdict(list)
    for tool in tools:
        role = roles.get(tool["server"], "general")
        role_tools[role].append(tool)

    groupings = []
    for role, rtools in role_tools.items():
        total = sum(t["tokens"] for t in rtools)
        status = "✅ under limit" if total <= max_tokens else f"⚠️ {total - max_tokens:,} tokens over"
        servers = list(set(t["server"] for t in rtools))
        groupings.append({
            "role": role,
            "servers": servers,
            "tool_count": len(rtools),
            "tokens": int(total),
            "status": status,
            "config_name": f"mcp-{role}.json",
        })

    return sorted(groupings, key=lambda x: -x["tokens"])


def format_report(analysis):
    """Format as human-readable report."""
    if "error" in analysis:
        return f"ERROR: {analysis['error']}"

    report = []
    report.append("═" * 60)
    report.append("  MCP TOKEN AUDIT REPORT")
    report.append("═" * 60)
    report.append(f"  Config: {analysis['config_path']}")
    report.append(f"  Servers: {analysis['server_count']}")
    report.append(f"  Total tools: {analysis['total_tools']}")
    report.append(f"  Total estimated tokens: {analysis['total_tokens']:,}")
    report.append(f"  Target limit: {analysis['max_tokens_target']:,}")
    report.append(f"  Utilization: {analysis['utilization_pct']}%")
    report.append("")

    report.append("─" * 60)
    report.append("  PER-ROLE BREAKDOWN")
    report.append("─" * 60)
    for role_data in analysis["per_role"]:
        bar = "█" * min(int(role_data["tokens"] / analysis["max_tokens_target"] * 30), 30)
        report.append(f"  {role_data['role']:<20} {role_data['tokens']:>8,} tokens  {bar}")
    report.append("")

    report.append("─" * 60)
    report.append("  TOP TOKEN HOGS")
    report.append("─" * 60)
    for i, hog in enumerate(analysis["top_token_hogs"][:5], 1):
        report.append(f"  {i}. {hog['server']}/{hog['tool']:<30} {hog['tokens']:>6,} tokens")
    report.append("")

    if analysis["suggestions"]:
        report.append("─" * 60)
        report.append("  SUGGESTIONS")
        report.append("─" * 60)
        for s in analysis["suggestions"]:
            icon = "🔴" if s["severity"] == "critical" else "🟡"
            report.append(f"  {icon} {s['message']}")
            report.append(f"     Fix: {s['fix']}")
        report.append("")

    report.append("─" * 60)
    report.append("  SUGGESTED ROLE GROUPINGS")
    report.append("─" * 60)
    for g in analysis["role_groupings"]:
        report.append(f"  {g['role']} ({g['config_name']})")
        report.append(f"    Servers: {', '.join(g['servers'][:5])}")
        report.append(f"    {g['tool_count']} tools, {g['tokens']:,} tokens — {g['status']}")
        report.append("")

    report.append("═" * 60)
    report.append("  Next: use --output to save per-role configs")
    report.append("═" * 60)

    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="MCP Token Auditor")
    parser.add_argument("--config", default="~/.claude/mcp.json", help="Path to MCP config")
    parser.add_argument("--output", help="Write report to file")
    parser.add_argument("--max-tokens", type=int, default=60000, help="Target max tokens per role")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    analysis = analyze_config(args.config, args.max_tokens)

    if args.json:
        output = json.dumps(analysis, indent=2)
    else:
        output = format_report(analysis)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Report saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()