#!/usr/bin/env python3
"""Scaffold a brand-new workflow: write template + register IDs in env YAML(s) + mint placeholder n8n workflow."""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import yaml

from helpers.workspace import workspace_root, harness_root
from helpers.config import load_yaml, load_env
from helpers.n8n_client import N8nClient


def _seed_minimal_template(workflow_key: str, name: str) -> str:
    seed = (harness_root() / "primitives" / "workflows" / "_minimal.template.json").read_text()
    seed = seed.replace("__NAME__", name)
    safe_path = re.sub(r"[^a-zA-Z0-9_-]+", "-", workflow_key).strip("-").lower() or "workflow"
    seed = seed.replace("__PATH__", safe_path)
    return seed


def _list_envs(workspace: Path) -> list[str]:
    cfg = workspace / "n8n-config"
    if not cfg.is_dir():
        return []
    return [p.stem for p in sorted(cfg.glob("*.yml")) if p.stem not in ("common", "deployment_order")]


def _ensure_workflow_row(workspace: Path, env_name: str, key: str, name: str, mint: bool) -> None:
    yaml_file = workspace / "n8n-config" / f"{env_name}.yml"
    data = load_yaml(env_name, workspace)
    workflows = data.setdefault("workflows", {}) or {}
    data["workflows"] = workflows  # ensure not None
    if key not in workflows or not isinstance(workflows[key], dict):
        workflows[key] = {"id": "", "name": name}

    wf = workflows[key]
    needs_mint = mint and (not wf.get("id") or str(wf.get("id", "")).startswith("your-") or wf.get("id") == "placeholder")

    if needs_mint:
        load_env(env_name, workspace)
        import os
        api_key = os.environ.get("N8N_API_KEY", "")
        instance = data.get("n8n", {}).get("instanceName", "")
        client = N8nClient(base_url=instance, api_key=api_key)
        full_name = f"{data.get('displayName', '')} {name}{data.get('workflowNamePostfix', '')}".strip()
        resp = client.post("workflows", {"name": full_name, "nodes": [], "connections": {}, "settings": {}})
        wf["id"] = resp.get("id", "")
        print(f"  Minted '{full_name}' → id={wf['id']} on env '{env_name}'")
    yaml_file.write_text(yaml.dump(data, default_flow_style=False, sort_keys=False))


def _add_to_deployment_order(workspace: Path, key: str, tier: str) -> None:
    order_file = workspace / "n8n-config" / "deployment_order.yml"
    data: dict = {}
    if order_file.exists():
        data = yaml.safe_load(order_file.read_text()) or {}
    tiers = data.setdefault("tiers", {})
    members = tiers.setdefault(tier, []) or []
    if key not in members:
        members.append(key)
    tiers[tier] = members
    order_file.write_text(yaml.dump(data, default_flow_style=False, sort_keys=False))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--key", required=True, help="Workflow key (e.g. report_v2)")
    parser.add_argument("--name", required=True, help="Display name (e.g. 'Daily Report')")
    parser.add_argument("--register-in", default=None, dest="register_in",
                        help="Comma-separated env names (default: all envs with a YAML present)")
    parser.add_argument("--with-error-handler", default=None, dest="with_error_handler",
                        help="Workflow key of an existing error handler to wire as settings.errorWorkflow")
    parser.add_argument("--tier", default="Tier 1",
                        help="Tier name in deployment_order.yml. Defaults to 'Tier 1' so deploy_all.py "
                             "picks the workflow up out of the box. Pass an explicit tier name "
                             "('Tier 0a: leaves' for primitives, 'Tier 2' for downstream callers, etc.) "
                             "or 'none' to skip deployment_order registration entirely.")
    parser.add_argument("--no-mint", action="store_true", help="Skip the n8n POST step")
    parser.add_argument("--no-template", action="store_true", help="Skip the template-write step")
    args = parser.parse_args()

    ws = workspace_root(args.workspace)

    # Step 1: write template
    template_dir = ws / "n8n-workflows-template"
    template_dir.mkdir(parents=True, exist_ok=True)
    template_path = template_dir / f"{args.key}.template.json"
    if not args.no_template:
        if template_path.exists():
            print(f"  Template exists at {template_path}, leaving in place")
        else:
            template_path.write_text(_seed_minimal_template(args.key, args.name))
            print(f"  Wrote {template_path}")

    # Step 2: register in env YAML(s) and (optionally) mint
    if args.register_in:
        envs = [e.strip() for e in args.register_in.split(",") if e.strip()]
    else:
        envs = _list_envs(ws)
    if not envs:
        print("WARNING: no env YAMLs to register in; create one with bootstrap-env first")
    for env in envs:
        try:
            _ensure_workflow_row(ws, env, args.key, args.name, mint=not args.no_mint)
        except Exception as e:
            print(f"  ERROR registering in env '{env}': {e}", file=sys.stderr)
            sys.exit(1)

    # Step 3: deployment order. `--tier none` opts out (e.g. workflows you
    # deploy manually outside deploy_all.py); any other value registers.
    if args.tier and args.tier.lower() != "none":
        _add_to_deployment_order(ws, args.key, args.tier)
        print(f"  Added '{args.key}' to deployment_order.yml under '{args.tier}'")

    # Step 4: error-handler wiring
    if args.with_error_handler:
        import subprocess
        cmd = [
            sys.executable,
            str(Path(__file__).parent / "register_error_handler.py"),
            "--workspace", str(ws),
            "--workflow-key", args.key,
            "--handler-key", args.with_error_handler,
        ]
        subprocess.run(cmd, check=True)

    print(f"create-workflow complete for '{args.key}'.")


if __name__ == "__main__":
    main()
