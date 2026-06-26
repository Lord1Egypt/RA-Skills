#!/usr/bin/env python3
"""Build a dependency graph across the workflows in an env (templates and/or live).

Three adjacency outputs:
  - calls            — Execute Workflow edges: caller_key → target_key (or live id when target unknown).
  - error_handlers   — source_key → handler_key (from common.yml.error_source_to_handler + live settings.errorWorkflow).
  - credential_groups — credential_id → list of workflows referencing it.

`--source template` reads workspace templates only.
`--source live` reads `GET /api/v1/workflows` only.
`--source both` (default) reads both and merges; live state takes precedence on disagreement.

Output is human-readable text by default; `--json` emits a single JSON document instead.
"""
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root
from helpers.config import load_yaml, load_env, load_common
from helpers.n8n_client import ensure_client


_PLACEHOLDER_RE = re.compile(r"^\{\{(?:INTERPOLATE_|@)env:workflows\.([A-Za-z0-9_\-]+)\.id\}\}$")


def _read_templates(workspace: Path) -> dict[str, dict]:
    """Return {workflow_key: parsed_template_dict}."""
    out: dict[str, dict] = {}
    template_dir = workspace / "n8n-workflows-template"
    if not template_dir.is_dir():
        return out
    for path in sorted(template_dir.glob("*.template.json")):
        key = path.name.removesuffix(".template.json")
        try:
            out[key] = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[dependency_graph] WARN: skip {path.name}: {e}", file=sys.stderr)
    return out


def _id_to_key_map(env_yaml: dict) -> dict[str, str]:
    """Map live workflow id → yaml key, from <env>.yml workflows.<key>.id rows."""
    out: dict[str, str] = {}
    workflows = env_yaml.get("workflows") or {}
    for key, row in workflows.items():
        if not isinstance(row, dict):
            continue
        wid = row.get("id")
        if wid:
            out[str(wid)] = key
    return out


def _resolve_workflow_id_to_key(value: str, id_to_key: dict[str, str]) -> str:
    """Resolve a workflowId reference (placeholder or live id) to a yaml key, falling back to the raw value."""
    if not value:
        return ""
    m = _PLACEHOLDER_RE.match(value.strip())
    if m:
        return m.group(1)
    return id_to_key.get(value, value)


def _extract_calls(nodes: list, id_to_key: dict[str, str]) -> list[str]:
    """Pull every Execute Workflow target out of a node list and resolve to keys/ids."""
    targets: list[str] = []
    for node in nodes or []:
        if node.get("type") != "n8n-nodes-base.executeWorkflow":
            continue
        params = node.get("parameters") or {}
        wf = params.get("workflowId")
        # Newer (resource-locator) shape: { __rl, value, mode }
        if isinstance(wf, dict):
            value = wf.get("value", "")
        else:
            value = wf
        target = _resolve_workflow_id_to_key(str(value or ""), id_to_key)
        if target:
            targets.append(target)
    return targets


def _extract_credentials(nodes: list) -> list[str]:
    """Pull every credential id referenced by any node in this workflow."""
    out: list[str] = []
    for node in nodes or []:
        creds = node.get("credentials") or {}
        if not isinstance(creds, dict):
            continue
        for entry in creds.values():
            if not isinstance(entry, dict):
                continue
            cid = entry.get("id")
            if cid:
                out.append(str(cid))
    return out


def _extract_error_handler(workflow: dict, id_to_key: dict[str, str]) -> Optional[str]:
    """Read settings.errorWorkflow and resolve to a yaml key (or raw id)."""
    settings = workflow.get("settings") or {}
    raw = settings.get("errorWorkflow")
    if not raw:
        return None
    return _resolve_workflow_id_to_key(str(raw), id_to_key)


def build_graph(env_name: str, workspace: Path, source: str, workflow_key: Optional[str] = None) -> dict:
    """Return adjacency dicts. Read templates and/or live workflows per `source`."""
    env_yaml = load_yaml(env_name, workspace)
    common = load_common(workspace)
    id_to_key = _id_to_key_map(env_yaml)

    workflows: dict[str, dict] = {}
    if source in ("template", "both"):
        workflows.update(_read_templates(workspace))
    if source in ("live", "both"):
        load_env(env_name, workspace)
        client = ensure_client(env_name, workspace)
        for wf in client.list_workflows():
            wid = str(wf.get("id", ""))
            key = id_to_key.get(wid)
            # Live takes precedence on overlap; if the live workflow has no yaml row, key falls back to id.
            workflows[key or wid] = wf

    if workflow_key:
        if workflow_key in workflows:
            workflows = {workflow_key: workflows[workflow_key]}
        else:
            workflows = {}

    calls: dict[str, list[str]] = {}
    error_handlers: dict[str, str] = {}
    credential_groups: dict[str, list[str]] = {}

    for key, wf in workflows.items():
        nodes = wf.get("nodes") or []
        targets = _extract_calls(nodes, id_to_key)
        if targets:
            calls[key] = sorted(set(targets))
        eh = _extract_error_handler(wf, id_to_key)
        if eh:
            error_handlers[key] = eh
        for cid in _extract_credentials(nodes):
            credential_groups.setdefault(cid, []).append(key)

    # Merge in common.yml.error_source_to_handler (template-side authoritative pairing).
    for src, handler in (common.get("error_source_to_handler") or {}).items():
        # Only include pairs whose source is in scope (key match or single-key filter).
        if workflow_key and src != workflow_key:
            continue
        error_handlers.setdefault(src, handler)

    # Stable sort credential consumers; drop dupes per credential.
    for cid in list(credential_groups):
        credential_groups[cid] = sorted(set(credential_groups[cid]))

    return {
        "source": source,
        "env": env_name,
        "workflow_key": workflow_key,
        "calls": calls,
        "error_handlers": error_handlers,
        "credential_groups": credential_groups,
    }


def _format_text(graph: dict) -> str:
    lines: list[str] = []
    lines.append(f"dependency_graph: env={graph['env']} source={graph['source']}"
                 + (f" workflow_key={graph['workflow_key']}" if graph["workflow_key"] else ""))

    lines.append("")
    lines.append("calls (Execute Workflow):")
    if not graph["calls"]:
        lines.append("  (none)")
    else:
        for caller, targets in sorted(graph["calls"].items()):
            lines.append(f"  {caller} → {', '.join(targets)}")

    lines.append("")
    lines.append("error_handlers (settings.errorWorkflow + common.yml):")
    if not graph["error_handlers"]:
        lines.append("  (none)")
    else:
        for src, handler in sorted(graph["error_handlers"].items()):
            lines.append(f"  {src} → {handler}")

    lines.append("")
    lines.append("credential_groups (credential_id → workflows):")
    if not graph["credential_groups"]:
        lines.append("  (none)")
    else:
        for cid, refs in sorted(graph["credential_groups"].items()):
            lines.append(f"  {cid}: {', '.join(refs)}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--env", required=True)
    parser.add_argument("--workflow-key", default=None, dest="workflow_key",
                        help="Restrict the graph to one workflow as the focal point.")
    parser.add_argument("--source", choices=("template", "live", "both"), default="both",
                        help="Which side to read. Default 'both' merges templates + live.")
    parser.add_argument("--json", action="store_true", help="Emit a single JSON document on stdout.")
    args = parser.parse_args()

    ws = workspace_root(args.workspace)
    graph = build_graph(args.env, ws, args.source, args.workflow_key)

    if args.json:
        print(json.dumps(graph, indent=2, sort_keys=True))
    else:
        print(_format_text(graph))


if __name__ == "__main__":
    main()
