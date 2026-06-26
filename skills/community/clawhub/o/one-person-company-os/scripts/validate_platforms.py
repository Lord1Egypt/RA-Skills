#!/usr/bin/env python3
"""Validate platform adapter packages."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parent.parent
PLATFORMS = ROOT / "platforms"


REQUIRED_FILES = [
    "platforms/README.md",
    "platforms/PUBLISHING-STATUS.md",
    "platforms/REQUIREMENTS.md",
    "platforms/EXPERIENCE-LOG.md",
    "platforms/publish-all-checklist.md",
    "platforms/claude-skill/SKILL.md",
    "platforms/openai-gpt/instructions.md",
    "platforms/openai-gpt/actions-openapi.yaml",
    "platforms/mcp-server/server.py",
    "platforms/mcp-server/server.json",
    "platforms/mcp-registries/submission-matrix.md",
    "platforms/mcp-registries/mcp-registry.md",
    "platforms/mcp-registries/smithery.md",
    "platforms/mcp-registries/glama.md",
    "platforms/mcp-registries/pulsemcp.md",
    "platforms/hermes-agent/SKILL.md",
    "platforms/hermes-agent/SOUL.md",
    "platforms/hermes-agent/mcp-config.json",
    "platforms/agentskills-io/listing.md",
    "platforms/dify-plugin/manifest.yaml",
    "platforms/dify-plugin/provider/one-person-company-os.yaml",
    "platforms/dify-plugin/provider/one_person_company_os.py",
    "platforms/dify-plugin/provider/tools/init_business.yaml",
    "platforms/dify-plugin/provider/tools/update_focus.yaml",
    "platforms/dify-plugin/provider/tools/generate_artifact_document.yaml",
    "platforms/dify-plugin/provider/tools/validate_release.yaml",
    "platforms/poe-bot/prompt.md",
    "platforms/gemini-gem/instructions.md",
    "platforms/github-copilot-extension/manifest.json",
    "platforms/microsoft-copilot-studio/agent-instructions.md",
    "platforms/microsoft-copilot-studio/teams-app-manifest.template.json",
    "platforms/microsoft-copilot-studio/commercial-marketplace-notes.md",
]


def assert_exists(relative: str) -> None:
    path = ROOT / relative
    if not path.is_file():
        raise FileNotFoundError(relative)


def assert_contains(path: Path, snippets: List[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for snippet in snippets:
        if snippet not in text:
            raise AssertionError(f"{path} missing {snippet!r}")


def mcp_frame(payload: Dict[str, Any]) -> bytes:
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return b"Content-Length: " + str(len(body)).encode("ascii") + b"\r\n\r\n" + body


def parse_mcp_frames(payload: bytes) -> List[Dict[str, Any]]:
    frames: List[Dict[str, Any]] = []
    position = 0
    while position < len(payload):
        header_end = payload.find(b"\r\n\r\n", position)
        if header_end < 0:
            break
        header = payload[position:header_end].decode("ascii")
        length = 0
        for line in header.split("\r\n"):
            key, _, value = line.partition(":")
            if key.lower() == "content-length":
                length = int(value.strip())
        body_start = header_end + 4
        body_end = body_start + length
        frames.append(json.loads(payload[body_start:body_end].decode("utf-8")))
        position = body_end
    return frames


def validate_mcp_server() -> None:
    server = PLATFORMS / "mcp-server" / "server.py"
    request = b"".join(
        [
            mcp_frame({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}),
            mcp_frame({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}),
        ]
    )
    completed = subprocess.run(
        [sys.executable, str(server)],
        cwd=str(ROOT),
        input=request,
        capture_output=True,
        check=False,
        timeout=10,
    )
    if completed.returncode != 0:
        raise AssertionError(completed.stderr.decode("utf-8", errors="replace"))
    frames = parse_mcp_frames(completed.stdout)
    if len(frames) != 2:
        raise AssertionError(f"expected 2 MCP responses, got {len(frames)}")
    tools = frames[1]["result"]["tools"]
    names = {tool["name"] for tool in tools}
    expected = {"preflight_check", "init_business", "update_focus", "generate_artifact_document", "validate_release"}
    if names != expected:
        raise AssertionError(f"unexpected MCP tools: {sorted(names)}")


def validate_json_files() -> None:
    for relative in (
        "platforms/mcp-server/server.json",
        "platforms/hermes-agent/mcp-config.json",
        "platforms/github-copilot-extension/manifest.json",
        "platforms/microsoft-copilot-studio/teams-app-manifest.template.json",
    ):
        json.loads((ROOT / relative).read_text(encoding="utf-8"))


def validate_public_language() -> None:
    for relative in (
        "platforms/PUBLISHING-STATUS.md",
        "platforms/REQUIREMENTS.md",
        "platforms/agentskills-io/listing.md",
        "platforms/mcp-registries/submission-matrix.md",
        "platforms/mcp-server/server.json",
        "platforms/openai-gpt/actions-openapi.yaml",
        "platforms/github-copilot-extension/manifest.json",
        "platforms/microsoft-copilot-studio/teams-app-manifest.template.json",
        "platforms/microsoft-copilot-studio/commercial-marketplace-notes.md",
        "platforms/dify-plugin/manifest.yaml",
    ):
        text = (ROOT / relative).read_text(encoding="utf-8")
        if "1.0.3" not in text:
            raise AssertionError(f"{relative} should mention adapter version 1.0.3")
    assert_contains(
        ROOT / "platforms/PUBLISHING-STATUS.md",
        [
            "OpenClaw / ClawHub",
            "Claude Skills",
            "OpenAI GPT Store",
            "MCP Registry",
            "Smithery",
            "Glama",
            "PulseMCP",
            "Hermes Agent / agentskills.io",
            "Dify Marketplace",
            "GitHub Copilot Extensions",
            "Microsoft Copilot Studio / Commercial Marketplace",
            "Poe Bots",
            "Gemini Gems",
        ],
    )
    for relative in (
        "platforms/claude-skill/SKILL.md",
        "platforms/hermes-agent/SKILL.md",
        "platforms/openai-gpt/instructions.md",
        "platforms/poe-bot/prompt.md",
        "platforms/gemini-gem/instructions.md",
    ):
        assert_contains(ROOT / relative, ["founder", "approved", "workspace"])


def main() -> int:
    for relative in REQUIRED_FILES:
        assert_exists(relative)
    validate_json_files()
    validate_mcp_server()
    validate_public_language()
    print("platform adapter validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
