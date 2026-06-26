#!/usr/bin/env python3
"""Convert raw n8n workflow JSON into a template (inverse of hydrate)."""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root
from helpers.config import load_yaml, flatten_config
from helpers.placeholder import js_resolver, py_resolver

# Volatile / runtime-only fields that must not appear in templates.
# (Live n8n GET /workflows/:id returns these alongside the canonical template
# fields. NEVER add `name`, `nodes`, `connections`, or `settings` here — those
# are the workflow's actual content.)
_METADATA_FIELDS = frozenset({
    "id", "active", "versionId", "createdAt", "updatedAt",
    "tags", "shared", "isArchived", "triggerCount", "homeProject",
    "scopes", "meta", "usedCredentials", "sharedWithProjects",
    "pinData",
    # Added 2026-04: n8n's response shape grew with the publish/version model.
    "activeVersion", "activeVersionId", "versionCounter",
    "description", "staticData",
})


def _strip_metadata(data: dict) -> dict:
    """Remove volatile / runtime fields recursively from the top-level."""
    return {k: v for k, v in data.items() if k not in _METADATA_FIELDS}


def _restore_uuids_by_name(data: dict, existing_template: dict) -> dict:
    """For each node, if the existing template had a UUID placeholder for the same name, restore it."""
    uuid_pattern = re.compile(r"\{\{(?:INTERPOLATE_|@)uuid:[^}]+\}\}")
    name_to_uuid_placeholder: dict[str, str] = {}
    for node in existing_template.get("nodes", []):
        name = node.get("name")
        node_id = str(node.get("id", ""))
        if name and uuid_pattern.fullmatch(node_id):
            name_to_uuid_placeholder[name] = node_id

    for node in data.get("nodes", []):
        name = node.get("name")
        if name in name_to_uuid_placeholder:
            node["id"] = name_to_uuid_placeholder[name]
    return data


def _reverse_env_values(text: str, env_data: dict) -> str:
    """Reverse-substitute env values back into {{@env:...}} placeholders.

    Skips workflows.* and credentials.* blocks (those are n8n internal IDs/names, not
    values that should appear in template body content). Only substitutes strings of
    length >= 4 to avoid clobbering tiny matches.
    """
    flat = flatten_config(env_data)
    sortable = sorted(
        (
            (k, v) for k, v in flat.items()
            if isinstance(v, str)
            and len(v) >= 4
            and not k.startswith("workflows.")
            and not k.startswith("credentials.")
        ),
        key=lambda kv: -len(kv[1]),  # longest first to avoid partial overshadowing
    )
    for key, value in sortable:
        encoded = json.dumps(value)[1:-1]  # strip outer quotes for substring match in JSON text
        placeholder = "{{@env:" + key + "}}"
        text = text.replace(encoded, placeholder)
    return text


def dehydrate_data(
    raw: dict,
    env_name: str,
    workspace: Path,
    output_key: str,
    remove_triggers: bool = False,
) -> str:
    """Run the full dehydrate pipeline on raw workflow JSON. Return template JSON text."""
    cleaned = _strip_metadata(raw)

    # If a previous template exists, use it as a guide for UUID restoration
    existing_path = workspace / "n8n-workflows-template" / f"{output_key}.template.json"
    if existing_path.exists():
        try:
            existing = json.loads(existing_path.read_text())
            cleaned = _restore_uuids_by_name(cleaned, existing)
        except json.JSONDecodeError:
            pass  # ignore corrupt previous template

    if remove_triggers:
        cleaned["nodes"] = [
            n for n in cleaned.get("nodes", []) if "trigger" not in str(n.get("type", "")).lower()
        ]

    text = json.dumps(cleaned, indent=2)

    # Reverse env values (e.g. instance names, display names, credential ids)
    try:
        env_data = load_yaml(env_name, workspace)
        text = _reverse_env_values(text, env_data)
    except Exception:
        pass  # if env YAML missing, skip reverse-substitution

    # Restore JS / Python placeholders from DEHYDRATE markers
    text = js_resolver.dehydrate(text)
    text = py_resolver.dehydrate(text)

    return text


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--env", required=True)
    parser.add_argument("--input", required=True, help="Path to raw workflow JSON")
    parser.add_argument("--output-key", required=True, dest="output_key")
    parser.add_argument("--remove-triggers", action="store_true")
    args = parser.parse_args()

    ws = workspace_root(args.workspace)
    raw = json.loads(Path(args.input).read_text())
    text = dehydrate_data(raw, args.env, ws, args.output_key, args.remove_triggers)
    out_dir = ws / "n8n-workflows-template"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{args.output_key}.template.json"
    out_file.write_text(text)
    print(f"Wrote {out_file}")


if __name__ == "__main__":
    main()
