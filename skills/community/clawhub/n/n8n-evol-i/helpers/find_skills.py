#!/usr/bin/env python3
"""Suggest applicable patterns/integrations skills for a workflow based on node types."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root, harness_root
from helpers.config import load_yaml, load_env, get_config_value
from helpers.n8n_client import ensure_client


NODE_TYPE_TO_SERVICE = {
    "n8n-nodes-base.microsoftExcel": "microsoft-365",
    "n8n-nodes-base.microsoftOneDrive": "microsoft-365",
    "n8n-nodes-base.microsoftOutlook": "microsoft-365",
    "n8n-nodes-base.microsoftSharepoint": "microsoft-365",
    "n8n-nodes-base.gmail": "gmail",
    "n8n-nodes-base.googleDrive": "google-drive",
    "n8n-nodes-base.googleSheets": "google-drive",
    "n8n-nodes-base.slack": "slack",
    "n8n-nodes-base.notion": "notion",
    "n8n-nodes-base.airtable": "airtable",
    "n8n-nodes-base.redis": "redis",
    "n8n-nodes-base.webhook": "webhooks",
    "n8n-nodes-base.respondToWebhook": "webhooks",
}

_PATTERN_TRIGGERS = {
    "subworkflows": ("n8n-nodes-base.executeWorkflow", "n8n-nodes-base.executeWorkflowTrigger"),
    "error-handling": ("n8n-nodes-base.errorTrigger", "n8n-nodes-base.stopAndError"),
    "credential-refs": (),
    "llm-providers": ("openai", "anthropic", "agent", "chatModel", "lmChat"),
    "locking": ("Lock Acquire", "Lock Release"),
}

_ALWAYS_ON_PATTERNS = ("validate-deploy", "multi-env-uuid-collision", "pindata-hygiene")


def _matches_trigger(node_type: str, node_name: str, triggers: tuple) -> bool:
    blob = (node_type + " " + node_name).lower()
    for t in triggers:
        if t.lower() in blob:
            return True
    return False


def find_skills_for_workflow(workflow: dict) -> list[str]:
    """Return relative paths of skills/patterns/<name>.md and skills/integrations/<svc>/...md that apply."""
    nodes = workflow.get("nodes", [])
    types = [(n.get("type", ""), n.get("name", "")) for n in nodes]
    suggestions: list[str] = []

    services_seen: set[str] = set()
    for t, _ in types:
        if t in NODE_TYPE_TO_SERVICE:
            services_seen.add(NODE_TYPE_TO_SERVICE[t])

    harness = harness_root()
    for svc in sorted(services_seen):
        svc_dir = harness / "skills" / "integrations" / svc
        if svc_dir.is_dir():
            for md in sorted(svc_dir.glob("*.md")):
                suggestions.append(str(md.relative_to(harness)))

    patterns: set[str] = set()
    for pat, triggers in _PATTERN_TRIGGERS.items():
        if not triggers:
            continue
        for t, n in types:
            if _matches_trigger(t, n, triggers):
                patterns.add(pat)
                break
    for p in _ALWAYS_ON_PATTERNS:
        patterns.add(p)

    for pat in sorted(patterns):
        md = harness / "skills" / "patterns" / f"{pat}.md"
        if md.is_file():
            suggestions.append(str(md.relative_to(harness)))

    if any("functions" in (n.get("type") or "") for n in nodes):
        md = harness / "skills" / "test.md"
        if md.is_file():
            suggestions.append(str(md.relative_to(harness)))

    return suggestions


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--workflow-key", required=True, dest="workflow_key")
    parser.add_argument("--env", default=None)
    args = parser.parse_args()

    ws = workspace_root(args.workspace)
    workflow: dict
    if args.env:
        try:
            load_env(args.env, ws)
            yaml_data = load_yaml(args.env, ws)
            wf_id = str(get_config_value(yaml_data, f"workflows.{args.workflow_key}.id"))
            client = ensure_client(args.env, ws)
            workflow = client.get_workflow(wf_id)
        except Exception:
            workflow = {}
    else:
        tpath = ws / "n8n-workflows-template" / f"{args.workflow_key}.template.json"
        if tpath.exists():
            workflow = json.loads(tpath.read_text())
        else:
            workflow = {}

    suggestions = find_skills_for_workflow(workflow)
    for s in suggestions:
        print(s)


if __name__ == "__main__":
    main()
