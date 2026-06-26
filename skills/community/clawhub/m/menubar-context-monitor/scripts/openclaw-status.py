#!/usr/bin/env python3
"""Collect agent session status from OpenClaw sessions.json files."""

import json
import os
import re
import time

OPENCLAW_DIR = os.path.expanduser("~/.openclaw")
AGENTS_DIR = os.path.join(OPENCLAW_DIR, "agents")
DEFAULT_EMOJI = "🤖"


def get_config():
    """Read openclaw.json config."""
    config_path = os.path.join(OPENCLAW_DIR, "openclaw.json")
    try:
        with open(config_path) as f:
            return json.load(f)
    except Exception:
        return {}


def get_workspace_paths(cfg):
    """Read agent workspace paths from config."""
    mapping = {}
    default_ws = cfg.get("agents", {}).get("defaults", {}).get("workspace", "")
    for a in cfg.get("agents", {}).get("list", []):
        ws = a.get("workspace", "")
        name = a.get("id", "") or a.get("name", "")
        if name:
            mapping[name] = ws or default_ws
    return mapping


def get_model_aliases(cfg):
    """Build reverse lookup: full model name -> alias."""
    # User-configured aliases
    aliases = {}
    for alias, full in cfg.get("modelAliases", {}).items():
        aliases[full] = alias
    # Built-in OpenClaw aliases
    builtins = {
        "google/gemini-3-flash": "flash",
        "anthropic/claude-haiku-4-5": "haiku",
        "anthropic/claude-opus-4-6": "opus",
        "anthropic/claude-sonnet-4-6": "sonnet",
        "google/gemini-3-pro-preview": "pro",
    }
    for full, alias in builtins.items():
        if full not in aliases:
            aliases[full] = alias
    return aliases


def read_emoji(agent, workspace_map):
    """Try to read emoji from agent's IDENTITY.md."""
    candidates = [
        workspace_map.get(agent, ""),
        os.path.join(OPENCLAW_DIR, f"workspace-{agent}"),
        os.path.join(AGENTS_DIR, agent, "workspace"),
    ]
    for base in candidates:
        if not base:
            continue
        path = os.path.join(base, "IDENTITY.md")
        if os.path.exists(path):
            try:
                with open(path) as f:
                    for line in f:
                        m = re.match(r"[-*]\s*\*?\*?Emoji\*?\*?\s*:\s*(.+)", line, re.IGNORECASE)
                        if m:
                            return m.group(1).strip().strip("*").strip()
            except Exception:
                pass
    return DEFAULT_EMOJI


def format_ago(updated_ms):
    """Convert updatedAt ms to human-readable 'Xm ago' string."""
    if not updated_ms:
        return "?"
    diff = time.time() - updated_ms / 1000
    if diff < 60:
        return f"{int(diff)}s"
    if diff < 3600:
        return f"{int(diff/60)}m"
    if diff < 86400:
        return f"{int(diff/3600)}h"
    return f"{int(diff/86400)}d"


def main():
    if not os.path.isdir(AGENTS_DIR):
        return

    cfg = get_config()
    workspace_map = get_workspace_paths(cfg)
    model_aliases = get_model_aliases(cfg)

    agents = sorted(d for d in os.listdir(AGENTS_DIR)
                     if os.path.isdir(os.path.join(AGENTS_DIR, d)))

    # Output: name,status,totalTokens,contextTokens,updatedAt,emoji,model_display
    for agent in agents:
        path = os.path.join(AGENTS_DIR, agent, "sessions", "sessions.json")
        if not os.path.exists(path):
            continue
        try:
            with open(path) as f:
                data = json.load(f)
            key = f"agent:{agent}:main"
            if key not in data:
                continue
            s = data[key]
            emoji = read_emoji(agent, workspace_map)
            updated = s.get("updatedAt", 0)
            ago = format_ago(updated)

            # Model: prefer modelOverride, then model field
            model_raw = s.get("modelOverride") or s.get("model") or "?"
            model_display = model_raw
            # Try exact match first
            if model_raw in model_aliases:
                model_display = model_aliases[model_raw]
            else:
                # Try matching against the model part (without provider prefix)
                for full, alias in model_aliases.items():
                    short = full.split("/")[-1] if "/" in full else full
                    if short == model_raw:
                        model_display = alias
                        break

            # Context tokens: try contextTokens, then contextLimit, then default by model
            ctx = s.get("contextTokens") or s.get("contextLimit")
            if not ctx:
                # Default context limits by model
                model_ctx = {
                    "claude-opus-4-6": 1000000,
                    "claude-sonnet-4-6": 1000000,
                    "claude-haiku-4-5": 200000,
                    "gemini-3-flash": 1000000,
                    "gemini-3-pro-preview": 1000000,
                }
                for m, c in model_ctx.items():
                    if m in model_raw:
                        ctx = c
                        break
                if not ctx:
                    ctx = 200000  # safe default

            print(f"{agent}\t{s.get('status', '?')}\t{s.get('totalTokens', 0)}\t"
                  f"{ctx}\t{updated}\t{emoji}\t{model_display}\t{ago}")
        except Exception:
            pass


if __name__ == "__main__":
    main()
