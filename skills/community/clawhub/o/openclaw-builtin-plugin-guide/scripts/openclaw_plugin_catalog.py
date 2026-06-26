#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Query OpenClaw bundled plugins, enabled/disabled lists, and plugin details."
    )
    parser.add_argument("--format", choices=["text", "json"], default="text")

    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("bundled", help="List bundled OpenClaw plugins")

    status_parser = subparsers.add_parser("status", help="List plugins by enabled state")
    status_parser.add_argument(
        "--state",
        choices=["all", "enabled", "disabled"],
        default="all",
        help="Filter by enabled flag",
    )

    inspect_parser = subparsers.add_parser("inspect", help="Inspect one plugin")
    inspect_parser.add_argument("plugin_id", help="Plugin id or plugin name")
    inspect_parser.add_argument(
        "--excerpt-lines",
        type=int,
        default=24,
        help="Maximum number of lines to include from a matched doc excerpt",
    )
    return parser


def resolve_skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def resolve_repo_root() -> Path:
    return resolve_skill_root().parent.parent


def resolve_workspace_root() -> Path:
    return resolve_repo_root().parent


def resolve_manual_doc_path() -> Path:
    skill_copy = resolve_skill_root() / "references" / "builtin-plugins.md"
    if skill_copy.is_file():
        return skill_copy
    return (
        resolve_workspace_root()
        / "openclaw-admin-suite"
        / "openclaw-web-panel"
        / "content"
        / "manual"
        / "builtin-plugins.md"
    )


def ensure_openclaw_cli() -> str:
    candidates = ["openclaw"]
    if os.name == "nt":
        candidates = ["openclaw.cmd", "openclaw.exe", "openclaw.ps1", "openclaw"]
    for candidate in candidates:
        cli = shutil.which(candidate)
        if cli:
            return cli
    raise RuntimeError("Missing `openclaw` CLI in PATH.")


def run_openclaw(args: list[str]) -> str:
    cli = ensure_openclaw_cli()
    command = [cli, *args]
    if os.name == "nt" and cli.lower().endswith(".ps1"):
        command = [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            cli,
            *args,
        ]
    proc = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    combined = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0:
        raise RuntimeError(combined.strip() or f"`openclaw {' '.join(args)}` failed")
    return combined


def extract_json_payload(raw: str) -> Any:
    decoder = json.JSONDecoder()
    best: Any | None = None
    best_end = -1
    for index, char in enumerate(raw):
        if char not in "{[":
            continue
        try:
            payload, end = decoder.raw_decode(raw[index:])
        except json.JSONDecodeError:
            continue
        if end > best_end:
            best = payload
            best_end = end
    if best is None:
        raise RuntimeError("Could not find JSON payload in openclaw output.")
    return best


def get_plugin_list_payload() -> dict[str, Any]:
    payload = extract_json_payload(run_openclaw(["plugins", "list", "--json"]))
    if not isinstance(payload, dict) or not isinstance(payload.get("plugins"), list):
        raise RuntimeError("Unexpected plugin list payload.")
    return payload


def get_plugin_inspect_payload(plugin_id: str) -> dict[str, Any]:
    payload = extract_json_payload(run_openclaw(["plugins", "inspect", plugin_id, "--json"]))
    if not isinstance(payload, dict) or not isinstance(payload.get("plugin"), dict):
        raise RuntimeError("Unexpected plugin inspect payload.")
    return payload


def read_text_best_effort(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def normalize_key(value: str) -> str:
    return value.strip().lower()


def extract_manual_doc_section(plugin_id: str, plugin_name: str | None = None) -> dict[str, str] | None:
    manual_doc = resolve_manual_doc_path()
    if not manual_doc.is_file():
        return None

    text = read_text_best_effort(manual_doc)
    wanted_keys = {normalize_key(plugin_id)}
    if plugin_name:
        wanted_keys.add(normalize_key(plugin_name))
        if "/" in plugin_name:
            wanted_keys.add(normalize_key(plugin_name.split("/")[-1]))

    current_heading: str | None = None
    current_lines: list[str] = []
    sections: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("## "):
            if current_heading is not None:
                sections[normalize_key(current_heading)] = "\n".join(current_lines).strip()
            current_heading = line[3:].strip()
            current_lines = []
            continue
        if current_heading is not None:
            current_lines.append(line)
    if current_heading is not None:
        sections[normalize_key(current_heading)] = "\n".join(current_lines).strip()

    for key in wanted_keys:
        content = sections.get(key)
        if content:
            return {
                "path": str(manual_doc),
                "heading": key,
                "content": content,
            }
    return None


def summarize_plugin(plugin: dict[str, Any]) -> dict[str, Any]:
    status = plugin.get("status")
    enabled = bool(plugin.get("enabled"))
    if enabled and status == "error":
        state_label = "enabled-error"
    elif enabled:
        state_label = "enabled"
    else:
        state_label = "disabled"
    return {
        "id": plugin.get("id"),
        "name": plugin.get("name"),
        "description": plugin.get("description"),
        "version": plugin.get("version"),
        "origin": plugin.get("origin"),
        "enabled": enabled,
        "status": status,
        "stateLabel": state_label,
        "format": plugin.get("format"),
        "source": plugin.get("source"),
        "channelIds": plugin.get("channelIds", []),
        "providerIds": plugin.get("providerIds", []),
        "speechProviderIds": plugin.get("speechProviderIds", []),
        "mediaUnderstandingProviderIds": plugin.get("mediaUnderstandingProviderIds", []),
        "imageGenerationProviderIds": plugin.get("imageGenerationProviderIds", []),
        "webSearchProviderIds": plugin.get("webSearchProviderIds", []),
        "toolNames": plugin.get("toolNames", []),
        "commands": plugin.get("commands", []),
        "error": plugin.get("error"),
    }


def collect_bundled_plugins() -> dict[str, Any]:
    payload = get_plugin_list_payload()
    bundled = [
        summarize_plugin(plugin) for plugin in payload["plugins"] if plugin.get("origin") == "bundled"
    ]
    bundled.sort(key=lambda item: str(item.get("id") or ""))
    return {
        "workspaceDir": payload.get("workspaceDir"),
        "count": len(bundled),
        "plugins": bundled,
    }


def collect_status_plugins(state: str) -> dict[str, Any]:
    payload = get_plugin_list_payload()
    plugins = [summarize_plugin(plugin) for plugin in payload["plugins"]]
    if state == "enabled":
        plugins = [plugin for plugin in plugins if plugin["enabled"]]
    elif state == "disabled":
        plugins = [plugin for plugin in plugins if not plugin["enabled"]]
    plugins.sort(key=lambda item: str(item.get("id") or ""))
    return {
        "workspaceDir": payload.get("workspaceDir"),
        "state": state,
        "count": len(plugins),
        "plugins": plugins,
        "diagnostics": payload.get("diagnostics", []),
    }


def unique_paths(paths: list[Path]) -> list[Path]:
    result: list[Path] = []
    seen: set[str] = set()
    for path in paths:
        key = str(path).lower()
        if key in seen or not path.is_file():
            continue
        seen.add(key)
        result.append(path)
    return result


def build_doc_candidates(plugin: dict[str, Any]) -> list[Path]:
    repo_root = resolve_repo_root()
    workspace_root = resolve_workspace_root()
    plugin_id = str(plugin.get("id") or "")
    package_name = str(plugin.get("name") or "")
    short_name = package_name.split("/")[-1] if "/" in package_name else package_name

    return unique_paths(
        [
            repo_root / "docs" / "providers" / f"{plugin_id}.md",
            repo_root / "docs" / "zh-CN" / "providers" / f"{plugin_id}.md",
            repo_root / "docs" / "channels" / f"{plugin_id}.md",
            repo_root / "docs" / "zh-CN" / "channels" / f"{plugin_id}.md",
            repo_root / "extensions" / plugin_id / "README.md",
            repo_root / "extensions" / short_name / "README.md",
            workspace_root / "openclaw-admin-suite" / "docs" / "china-channels.md",
            workspace_root / "plugins-cli" / "utils" / plugin_id / "README.md",
            workspace_root / "plugins-cli" / "utils" / short_name / "README.md",
        ]
    )


def read_excerpt(path: Path, max_lines: int) -> str:
    try:
        return "\n".join(read_text_best_effort(path).splitlines()[:max_lines]).strip()
    except OSError:
        return ""


def collect_plugin_detail(plugin_id: str, excerpt_lines: int) -> dict[str, Any]:
    inspect_payload = get_plugin_inspect_payload(plugin_id)
    plugin = inspect_payload["plugin"]
    manual_doc = extract_manual_doc_section(
        str(plugin.get("id") or plugin_id),
        str(plugin.get("name") or "") or None,
    )
    docs = []
    for path in build_doc_candidates(plugin):
        docs.append(
            {
                "path": str(path),
                "excerpt": read_excerpt(path, excerpt_lines),
            }
        )
    return {
        "workspaceDir": inspect_payload.get("workspaceDir"),
        "plugin": summarize_plugin(plugin),
        "manualDoc": manual_doc,
        "shape": inspect_payload.get("shape"),
        "capabilityMode": inspect_payload.get("capabilityMode"),
        "capabilityCount": inspect_payload.get("capabilityCount"),
        "capabilities": inspect_payload.get("capabilities", []),
        "typedHooks": inspect_payload.get("typedHooks", []),
        "customHooks": inspect_payload.get("customHooks", []),
        "tools": inspect_payload.get("tools", []),
        "commands": inspect_payload.get("commands", []),
        "cliCommands": inspect_payload.get("cliCommands", []),
        "services": inspect_payload.get("services", []),
        "gatewayMethods": inspect_payload.get("gatewayMethods", []),
        "mcpServers": inspect_payload.get("mcpServers", []),
        "lspServers": inspect_payload.get("lspServers", []),
        "httpRouteCount": inspect_payload.get("httpRouteCount"),
        "bundleCapabilities": inspect_payload.get("bundleCapabilities", []),
        "diagnostics": inspect_payload.get("diagnostics", []),
        "policy": inspect_payload.get("policy", {}),
        "compatibility": inspect_payload.get("compatibility", []),
        "docs": docs,
    }


def print_json(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def format_state_label(plugin: dict[str, Any]) -> str:
    if plugin["stateLabel"] == "enabled-error":
        return "enabled but failed to load"
    if plugin["stateLabel"] == "enabled":
        return "enabled"
    return "disabled"


def print_plugin_lines(plugins: list[dict[str, Any]]) -> None:
    for plugin in plugins:
        description = plugin.get("description") or ""
        suffix = f" - {description}" if description else ""
        print(
            f"- {plugin['id']} | {plugin.get('name') or plugin['id']} | "
            f"{format_state_label(plugin)}{suffix}"
        )


def print_bundled(payload: dict[str, Any]) -> None:
    print(f"Bundled plugins: {payload['count']}")
    print_plugin_lines(payload["plugins"])


def print_status(payload: dict[str, Any]) -> None:
    print(f"Plugins ({payload['state']}): {payload['count']}")
    print_plugin_lines(payload["plugins"])
    diagnostics = payload.get("diagnostics") or []
    if diagnostics:
        print("")
        print("Diagnostics:")
        for diag in diagnostics:
            plugin_id = diag.get("pluginId") or "<unknown>"
            message = str(diag.get("message") or "").splitlines()[0]
            print(f"- {plugin_id}: {message}")


def print_detail(payload: dict[str, Any]) -> None:
    plugin = payload["plugin"]
    print(f"Plugin: {plugin['id']}")
    print(f"Name: {plugin.get('name') or plugin['id']}")
    print(f"State: {format_state_label(plugin)}")
    if plugin.get("description"):
        print(f"Description: {plugin['description']}")
    if plugin.get("version"):
        print(f"Version: {plugin['version']}")
    if plugin.get("origin"):
        print(f"Origin: {plugin['origin']}")
    if plugin.get("source"):
        print(f"Source: {plugin['source']}")
    print(f"Shape: {payload.get('shape')}")
    print(f"Capability mode: {payload.get('capabilityMode')}")

    manual_doc = payload.get("manualDoc")
    if manual_doc:
        print("")
        print("Manual:")
        print(f"- {manual_doc['path']}")
        print(manual_doc["content"])

    sections = [
        ("Capabilities", payload.get("capabilities") or []),
        ("Commands", payload.get("commands") or []),
        ("CLI Commands", payload.get("cliCommands") or []),
        ("Services", payload.get("services") or []),
        ("Gateway Methods", payload.get("gatewayMethods") or []),
        ("Compatibility", payload.get("compatibility") or []),
        ("Diagnostics", payload.get("diagnostics") or []),
    ]
    for title, value in sections:
        if not value:
            continue
        print("")
        print(f"{title}:")
        for item in value:
            print(f"- {json.dumps(item, ensure_ascii=False)}")

    docs = payload.get("docs") or []
    if docs:
        print("")
        print("Docs:")
        for doc in docs:
            print(f"- {doc['path']}")
            if doc.get("excerpt"):
                print(doc["excerpt"])
                print("")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "bundled":
            payload = collect_bundled_plugins()
        elif args.command == "status":
            payload = collect_status_plugins(args.state)
        else:
            payload = collect_plugin_detail(args.plugin_id, args.excerpt_lines)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.format == "json":
        print_json(payload)
        return 0

    if args.command == "bundled":
        print_bundled(payload)
    elif args.command == "status":
        print_status(payload)
    else:
        print_detail(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
