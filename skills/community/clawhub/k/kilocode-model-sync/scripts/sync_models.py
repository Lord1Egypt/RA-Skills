#!/usr/bin/env python3
"""
sync_models.py — Fetch Kilocode models and produce diff + patch for openclaw.json

Usage:
    python3 sync_models.py [--output-dir DIR]

Output (stdout): JSON result object
Exit 0: success (changed or no_change)
Exit 1: error
"""

import json
import os
import sys
import re
import argparse
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# ── Config ────────────────────────────────────────────────────────────────────
API_URL     = "https://api.kilo.ai/api/gateway/models"
ENV_FILE    = Path.home() / ".openclaw" / ".env"
OPENCLAW_JSON = Path.home() / ".openclaw" / "openclaw.json"
DEFAULT_OUT = Path.home() / ".openclaw" / "workspace" / "kilocode-models"

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_env(path: Path) -> dict:
    env = {}
    if not path.exists():
        return env
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def fetch_models(token: str) -> list:
    req = Request(API_URL, headers={"Authorization": f"Bearer {token}"})
    with urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode())
    return data.get("data", [])


def map_model(raw: dict) -> dict:
    """Map Kilo API model → OpenClaw schema."""
    params = raw.get("supported_parameters", [])
    pricing = raw.get("pricing", {})
    top = raw.get("top_provider", {})

    def safe_float(val, default=0.0):
        try:
            return float(val) if val is not None else default
        except (ValueError, TypeError):
            return default

    input_modalities = raw.get("architecture", {}).get("input_modalities", ["text"])

    model = {
        "id":            raw["id"],
        "name":          raw.get("name", raw["id"]),
        "reasoning":     "reasoning" in params,
        "cost": {
            "input":  safe_float(pricing.get("prompt"),     0.0),
            "output": safe_float(pricing.get("completion"), 0.0),
        },
        "contextWindow": raw.get("context_length") or top.get("context_length") or 0,
        "maxTokens":     top.get("max_completion_tokens") or 0,
    }

    # Only add image cost if non-zero
    img_cost = safe_float(pricing.get("image"), 0.0)
    if img_cost:
        model["cost"]["image"] = img_cost

    # Add input modalities if not just text
    if input_modalities != ["text"]:
        model["input"] = input_modalities

    return model


def latest_snapshot(out_dir: Path) -> tuple[Path | None, list]:
    """Return (path, models_list) for the most recent snapshot, or (None, [])."""
    snapshots = sorted(out_dir.glob("kilocode-models-????-??-??.json"), reverse=True)
    for snap in snapshots:
        # skip today's (we're about to overwrite)
        today_name = f"kilocode-models-{date.today().isoformat()}.json"
        if snap.name == today_name:
            continue
        try:
            return snap, json.loads(snap.read_text())
        except Exception:
            continue
    return None, []


def compute_diff(old: list, new: list) -> dict:
    """Return {added, removed, updated} as lists of model dicts."""
    old_map = {m["id"]: m for m in old}
    new_map = {m["id"]: m for m in new}

    added   = [new_map[k] for k in new_map if k not in old_map]
    removed = [old_map[k] for k in old_map if k not in new_map]
    updated = [
        {"old": old_map[k], "new": new_map[k]}
        for k in new_map
        if k in old_map and old_map[k] != new_map[k]
    ]
    return {"added": added, "removed": removed, "updated": updated}


def has_changes(diff: dict) -> bool:
    return bool(diff["added"] or diff["removed"] or diff["updated"])


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=str(DEFAULT_OUT))
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load token
    env = load_env(ENV_FILE)
    # Also check real environment
    token = os.environ.get("KILOCODE_API_KEY") or env.get("KILOCODE_API_KEY")
    if not token:
        print(json.dumps({"status": "error", "error": "KILOCODE_API_KEY not found in ~/.openclaw/.env"}))
        sys.exit(1)

    # 2. Fetch
    try:
        raw_models = fetch_models(token)
    except HTTPError as e:
        print(json.dumps({"status": "error", "error": f"HTTP {e.code}: {e.reason}"}))
        sys.exit(1)
    except URLError as e:
        print(json.dumps({"status": "error", "error": f"Network error: {e.reason}"}))
        sys.exit(1)

    # 3. Map to OpenClaw schema
    new_models = [map_model(m) for m in raw_models]

    # 4. Save today's snapshot
    today = date.today().isoformat()
    snapshot_path = out_dir / f"kilocode-models-{today}.json"
    snapshot_path.write_text(json.dumps(new_models, indent=2))

    # 5. Load previous snapshot and diff
    prev_path, prev_models = latest_snapshot(out_dir)
    diff = compute_diff(prev_models, new_models)

    result = {
        "status":        "changed" if has_changes(diff) else "no_change",
        "snapshot_path": str(snapshot_path),
        "prev_snapshot": str(prev_path) if prev_path else None,
        "total_models":  len(new_models),
        "diff":          diff,
        "diff_path":     None,
        "patch_path":    None,
    }

    if has_changes(diff):
        # 6. Save diff
        diff_path = out_dir / f"kilocode-models-{today}.diff.json"
        diff_path.write_text(json.dumps(diff, indent=2))
        result["diff_path"] = str(diff_path)

        # 7. Generate patch (the full new models list for openclaw.json)
        patch = {
            "target":  "models.providers.kilocode.models",
            "models":  new_models,
            "applied": False,
            "created": datetime.now(timezone.utc).isoformat(),
        }
        patch_path = out_dir / f"kilocode-models-{today}.patch.json"
        patch_path.write_text(json.dumps(patch, indent=2))
        result["patch_path"] = str(patch_path)

    print(json.dumps(result, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
