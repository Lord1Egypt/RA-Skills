#!/usr/bin/env python3
"""Create one immutable Codex native multi-agent acceptance run and task cards."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from prepare_workbuddy_acceptance_scaffold import ACCEPTANCE_SCOPE, prepare_scaffold


def prepare(workdir: Path, plugin_dir: Path, label: str) -> dict:
    workdir = workdir.resolve()
    plugin_dir = plugin_dir.resolve()
    if not re.fullmatch(r"[0-9A-Za-z_-]{2,80}", label):
        raise ValueError("codex_acceptance_label_invalid")
    metadata_path = plugin_dir / "version-info.json"
    if metadata_path.is_file():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8-sig"))
        version = str(metadata.get("team_version") or "")
    else:
        manifest = json.loads((plugin_dir / ".codebuddy-plugin" / "plugin.json").read_text(encoding="utf-8-sig"))
        version = str(manifest.get("version") or "")
    if version != "2.0.3" and not version.startswith("2.0.3-candidate."):
        raise ValueError("codex_acceptance_version_invalid")
    version_tag = version.replace(".", "")
    run_id = f"acc-v{version_tag}-codex-{label}"
    run_dir = workdir / "runs" / run_id
    card_path = workdir / f"codex-acceptance-lead-card-{label}.json"
    if card_path.exists() or run_dir.exists():
        raise ValueError("codex_acceptance_run_already_exists")
    workdir.mkdir(parents=True, exist_ok=True)
    card = {
        "schema_version": "2.0",
        "artifact_type": "codex_acceptance_lead_card",
        "host": "codex",
        "client_scope": ACCEPTANCE_SCOPE,
        "version": version,
        "run_id": run_id,
        "run_dir": str(run_dir),
        "team_name": None,
        "immutable_after_launch": True,
    }
    card_path.write_text(json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result = prepare_scaffold(card_path, plugin_dir)
    result["lead_card"] = str(card_path)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", required=True)
    parser.add_argument("--plugin-dir", required=True)
    parser.add_argument("--label", required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(Path(args.workdir), Path(args.plugin_dir), args.label), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
