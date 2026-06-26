#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 - "$ROOT" <<'PY'
import json
import sys
import zipfile
from pathlib import Path

root = Path(sys.argv[1])

def require(condition, message):
    if not condition:
        raise SystemExit(message)

plugin = json.loads((root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
require(plugin["name"] == "graymatter", "plugin name must be graymatter")
require(plugin.get("skills") == "./", "Codex plugin must expose the standalone skill")
require(plugin.get("mcpServers") == "./.mcp.json", "Codex plugin must expose MCP server config")
require("mcp" in plugin.get("keywords", []), "Codex plugin keywords must include mcp")
require("Interactive" in plugin["interface"]["capabilities"], "Codex plugin must advertise interactive MCP capability")
require("mcp-server" in plugin["interface"]["longDescription"], "Codex plugin description must mention the MCP server")

mcp_config = json.loads((root / ".mcp.json").read_text(encoding="utf-8"))
server = mcp_config["mcpServers"]["graymatter"]
require(server["command"] == "node", "MCP server must launch with node")
require(server["args"] == ["mcp-server/index.js", "--stdio"], "MCP server must launch the stdio transport")

pkg = json.loads((root / "mcp-server/package.json").read_text(encoding="utf-8"))
require(pkg["scripts"]["start"] == "node index.js", "MCP package must retain HTTP/SSE start script")
require(pkg["scripts"]["stdio"] == "node index.js --stdio", "MCP package must expose stdio start script")
require(pkg["engines"]["node"] == ">=20", "MCP server must declare Node 20+")

skill = (root / "SKILL.md").read_text(encoding="utf-8")
for needle in [
    "OpenClaw",
    "scripts/gm-activate",
    "scripts/gm-login",
    "mcp-server/",
]:
    require(needle in skill, f"SKILL.md missing {needle}")

readme = (root / "README.md").read_text(encoding="utf-8")
for needle in [
    "Ready-to-rock release surfaces",
    "MCP service",
    "Codex plugin",
    "Standalone OpenClaw skill",
]:
    require(needle in readme, f"README missing release surface: {needle}")

with zipfile.ZipFile(root / "graymatter.skill") as archive:
    names = set(archive.namelist())
    require("graymatter/SKILL.md" in names, "graymatter.skill must include SKILL.md")
    require("graymatter/graymatter-bootstrap" in names, "graymatter.skill must include sparse-install bootstrap")
    require("graymatter/scripts/gm-activate" in names, "graymatter.skill must include activation")
    require("graymatter/scripts/gm-light-up" in names, "graymatter.skill must include Light launcher")
    require("graymatter/mcp-server/index.js" in names, "graymatter.skill must include the MCP server runtime for plugin installs")

print("release_surfaces_test: ok")
PY
