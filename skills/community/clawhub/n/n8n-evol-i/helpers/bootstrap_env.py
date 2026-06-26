#!/usr/bin/env python3
"""Bootstrap an n8n environment: create YAML + .env, validate, mint placeholder workflow IDs."""
import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import yaml

from helpers.workspace import workspace_root, ensure_workspace


def _is_placeholder_id(id_val) -> bool:
    if not id_val:
        return True
    s = str(id_val)
    return s.startswith("your-") or s == "placeholder"


def _write_env_yaml(yaml_file: Path, env_name: str, instance: str, postfix: str, display_name: str) -> None:
    data = {
        "name": env_name,
        "displayName": display_name,
        "workflowNamePostfix": postfix,
        "n8n": {"instanceName": instance},
        "credentials": {},
        "workflows": {},
    }
    yaml_file.write_text(yaml.dump(data, default_flow_style=False, sort_keys=False))


def _write_env_file(env_file: Path, api_key: str) -> None:
    env_file.write_text(f"N8N_API_KEY={api_key}\n")
    env_file.chmod(0o600)


def _load_yaml(yaml_file: Path) -> dict:
    with open(yaml_file) as f:
        return yaml.safe_load(f) or {}


def _save_yaml(yaml_file: Path, data: dict) -> None:
    yaml_file.write_text(yaml.dump(data, default_flow_style=False, sort_keys=False))


def _validate_instance(instance: str, api_key: str) -> None:
    """Attempt GET /api/v1/workflows?limit=1. Raises on failure."""
    from helpers.n8n_client import N8nClient
    client = N8nClient(base_url=instance, api_key=api_key)
    client.get("workflows", params={"limit": 1})


def _mint_placeholder_workflows(
    yaml_file: Path,
    data: dict,
    instance: str,
    api_key: str,
    dry_run: bool,
) -> None:
    from helpers.n8n_client import N8nClient
    client = N8nClient(base_url=instance, api_key=api_key)
    workflows = data.get("workflows") or {}
    changed = False
    for key, wf in workflows.items():
        if not isinstance(wf, dict):
            continue
        if _is_placeholder_id(wf.get("id")):
            wf_name = wf.get("name", key)
            display_name = data.get("displayName", "")
            postfix = data.get("workflowNamePostfix", "")
            full_name = f"{display_name} {wf_name}{postfix}".strip()
            if dry_run:
                print(f"  [dry-run] would mint workflow '{full_name}' for key '{key}'")
            else:
                resp = client.post("workflows", {"name": full_name, "nodes": [], "connections": {}, "settings": {}})
                new_id = resp.get("id", "")
                print(f"  Minted workflow '{full_name}' → id={new_id} (key={key})")
                data["workflows"][key]["id"] = new_id
                changed = True
    if changed:
        _save_yaml(yaml_file, data)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None, help="Workspace path. Default: ${PWD}/n8n-evol-I-workspace, or ${PWD} if its basename is already n8n-evol-I-workspace.")
    parser.add_argument("--env", required=True, help="Environment name (e.g. dev, prod)")
    parser.add_argument("--instance", default=None, help="n8n instance URL or hostname")
    parser.add_argument("--api-key", default=None, dest="api_key", help="n8n API key")
    parser.add_argument("--postfix", default=" [DEV]", help="Workflow name postfix (default: ' [DEV]')")
    parser.add_argument("--display-name", default="Development", dest="display_name", help="Human-readable env name")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be done without writing/POSTing")
    parser.add_argument("--force-update-instance", action="store_true", help="Overwrite instance URL in existing YAML")
    args = parser.parse_args()

    ws = workspace_root(args.workspace)
    config_dir = ws / "n8n-config"
    config_dir.mkdir(parents=True, exist_ok=True)

    yaml_file = config_dir / f"{args.env}.yml"
    env_file = config_dir / f".env.{args.env}"

    # ── Stage 1: create YAML + .env if absent ──────────────────────────────
    stage1_wrote_yaml = False
    stage1_wrote_env = False

    if not yaml_file.exists():
        instance = args.instance
        api_key = args.api_key or os.environ.get("N8N_API_KEY", "")
        if not instance:
            instance = input(f"n8n instance URL for env '{args.env}': ").strip()
        if not api_key:
            api_key = input(f"API key for env '{args.env}': ").strip()
        if not args.dry_run:
            _write_env_yaml(yaml_file, args.env, instance, args.postfix, args.display_name)
            stage1_wrote_yaml = True
            print(f"  Wrote {yaml_file}")
        else:
            print(f"  [dry-run] would write {yaml_file}")
    else:
        data = _load_yaml(yaml_file)
        if args.force_update_instance and args.instance:
            data.setdefault("n8n", {})["instanceName"] = args.instance
            if not args.dry_run:
                _save_yaml(yaml_file, data)

    if not env_file.exists():
        api_key = args.api_key or os.environ.get("N8N_API_KEY", "")
        if not api_key:
            api_key = input(f"API key for env '{args.env}': ").strip()
        if not args.dry_run:
            _write_env_file(env_file, api_key)
            stage1_wrote_env = True
            print(f"  Wrote {env_file} (mode 0600)")
        else:
            print(f"  [dry-run] would write {env_file}")
    else:
        api_key = args.api_key or None

    if args.dry_run:
        print("Dry-run complete. No files written.")
        return

    # ── Stage 2: live validation ────────────────────────────────────────────
    data = _load_yaml(yaml_file)
    instance = data.get("n8n", {}).get("instanceName", "")
    # Load API key: prefer flag, then .env file, then os.environ
    if not api_key:
        env_vars: dict = {}
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if "=" in line and not line.startswith("#"):
                        k, _, v = line.partition("=")
                        env_vars[k.strip()] = v.strip()
        api_key = env_vars.get("N8N_API_KEY", os.environ.get("N8N_API_KEY", ""))

    try:
        _validate_instance(instance, api_key)
        print(f"  n8n instance at {instance} is reachable.")
    except Exception as e:
        # Rollback stage 1 writes
        if stage1_wrote_yaml:
            yaml_file.unlink(missing_ok=True)
        if stage1_wrote_env:
            env_file.unlink(missing_ok=True)
        print(f"ERROR: Could not reach n8n at {instance}: {e}", file=sys.stderr)
        print("Rolled back any files written in this run.", file=sys.stderr)
        sys.exit(1)

    # ── Stage 3: mint placeholder workflow IDs ─────────────────────────────
    _mint_placeholder_workflows(yaml_file, data, instance, api_key, dry_run=False)
    print("bootstrap-env complete.")


if __name__ == "__main__":
    main()
