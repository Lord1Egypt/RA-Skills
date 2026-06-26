from __future__ import annotations

import argparse
import json
from datetime import datetime
from fnmatch import fnmatch
from pathlib import Path


DEFAULT_OBSOLETE_GLOBS = [
    "**/__pycache__",
    "**/__pycache__/**",
    "**/*.pyc",
    "**/*.pyo",
    "**/*.bak",
    "**/*.tmp",
    "**/*.old",
    "**/*~",
    "**/visuals_test/**",
    "**/*probe*/**"
]

DEFAULT_OBSOLETE_TOKENS = ("obsolete", "deprecated", "discard", "backup", "probe", "tmp", "temp")


def load_json(path: Path | None) -> dict:
    if not path or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def rel_path(path: Path, root: Path) -> str:
    return "." if path == root else path.relative_to(root).as_posix()


def match_rule(rel: str, rules: list[dict]) -> dict:
    best: dict = {}
    best_len = -1
    for rule in rules:
        rule_path = str(rule.get("path", "")).strip()
        if rule_path and (rel == rule_path or rel.startswith(f"{rule_path}/")) and len(rule_path) > best_len:
            best = rule
            best_len = len(rule_path)
    return best


def is_obsolete(rel: str, overrides: list[dict]) -> tuple[bool, str]:
    for item in overrides:
        pattern = str(item.get("glob", "")).strip()
        if pattern and fnmatch(rel, pattern):
            return True, str(item.get("notes", "")).strip()
    lowered = rel.casefold()
    if any(token in lowered for token in DEFAULT_OBSOLETE_TOKENS):
        return True, "Heuristic match for temporary or obsolete path naming."
    return False, ""


def infer_purpose(rel: str, kind: str) -> str:
    if rel.endswith("metadata/delivery_bundle_manifest.json"):
        return "Machine-readable restart contract for fresh-session handoff."
    if rel.endswith("metadata/paper_batch_manifest.json"):
        return "Authoritative list of papers that must be completed in this deep-read batch."
    if rel.endswith("metadata/query_spec.json"):
        return "Batch-level input, output, and restart contract for the deep-read stage."
    if rel.endswith("metadata/routing_status.json"):
        return "Current stage status for downstream routing."
    if rel.endswith("metadata/project_directory_index.json"):
        return "Machine-readable directory description for downstream routing."
    if rel.endswith("reports/project_directory_index.md"):
        return "Human-facing directory description for downstream routing."
    if rel.endswith("reports/stage_delivery_handoff.md"):
        return "Human-facing stage delivery note describing authoritative artifacts and next-stage usage."
    if rel.startswith("reports/per_paper/") and rel.endswith("_detailed_cn.md"):
        return "Authoritative per-paper deep-read report."
    if rel.startswith("reports/per_paper/") and rel.endswith("_detailed_cn.pdf"):
        return "Rendered PDF version of the authoritative per-paper deep-read report."
    if rel.startswith("metadata/focus_specs/") and rel.endswith(".json"):
        return "Per-paper structured focus spec carrying source metadata, upstream bundle context, and graph-ready scratch fields."
    if rel.startswith("generated/intermediate/") and rel.endswith(".json"):
        return "Machine-readable per-paper deep-read output for downstream graph construction."
    if rel.startswith("generated/visuals/") and rel.endswith("visual_manifest.json"):
        return "Manifest describing final visual artifacts that remain relevant to the report."
    if rel.startswith("inputs/source_metadata/") and rel.endswith("source_record.json"):
        return "Copied per-paper source record from upstream collection stages."
    if rel.startswith("inputs/review_context/") and rel.endswith("forum.json"):
        return "Copied OpenReview forum metadata used during deep reading."
    if rel.startswith("inputs/review_context/") and rel.endswith("author_responses.md"):
        return "Copied author rebuttal or response summary used during deep reading."
    if rel.startswith("inputs/review_context/") and rel.endswith("decision.json"):
        return "Copied decision or meta-review metadata used during deep reading."
    if rel.startswith("inputs/review_context/") and kind == "directory":
        return "Copied peer-review context required for papers with public review artifacts."
    return ""


def build_entry(path: Path, root: Path, rules: list[dict], overrides: list[dict], default_stage: str) -> dict:
    rel = rel_path(path, root)
    rule = match_rule(rel, rules)
    rule_path = str(rule.get("path", "")).strip()
    obsolete, obsolete_note = is_obsolete(rel, overrides)
    kind = "directory" if path.is_dir() else "file"
    purpose = str(rule.get("purpose", "")).strip()
    notes = str(rule.get("notes", "")).strip()
    status = str(rule.get("status", "active")).strip() or "active"
    inferred_purpose = infer_purpose(rel, kind)
    if obsolete:
        status = "obsolete_or_ignored"
        notes = obsolete_note or notes
    if inferred_purpose and rule_path != rel:
        purpose = inferred_purpose
    if not purpose:
        purpose = "Workspace root." if rel == "." else inferred_purpose or f"Unclassified {kind}."
    return {
        "relative_path": rel,
        "kind": kind,
        "purpose": purpose,
        "generated_by_stage": str(rule.get("generated_by_stage", "")).strip() or default_stage,
        "status": status,
        "notes": notes
    }


def render_markdown(index: dict) -> str:
    def esc(text: str) -> str:
        return text.replace("|", "\\|").replace("\n", " ").strip()

    lines = [
        "# Project Directory Index",
        "",
        "## Summary",
        "",
        f"- workspace root: `{index['workspace_root']}`",
        f"- generated at: `{index['generated_at']}`",
        f"- default stage: `{index['default_stage']}`",
        "",
        "## Entries",
        "",
        "| Path | Kind | Purpose | Generated By Stage | Status | Notes |",
        "| --- | --- | --- | --- | --- | --- |"
    ]
    for entry in index["entries"]:
        lines.append("| " + " | ".join(esc(str(entry[key])) for key in ["relative_path", "kind", "purpose", "generated_by_stage", "status", "notes"]) + " |")
    return "\n".join(lines) + "\n"


def build_index(root: Path, annotations_path: Path, default_stage: str) -> dict:
    annotations = load_json(annotations_path)
    rules = list(annotations.get("rules", []))
    overrides = list(annotations.get("status_overrides", []))
    if not overrides:
        overrides = [{"glob": pattern, "status": "obsolete_or_ignored", "notes": ""} for pattern in DEFAULT_OBSOLETE_GLOBS]
    entries = [
        build_entry(path, root, rules, overrides, annotations.get("default_stage", default_stage) or default_stage)
        for path in [root] + sorted(root.rglob("*"), key=lambda item: rel_path(item, root))
    ]
    return {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "workspace_root": str(root.resolve()),
        "default_stage": annotations.get("default_stage", default_stage) or default_stage,
        "annotations_file": str(annotations_path.resolve()),
        "summary": {
            "directories": sum(1 for entry in entries if entry["kind"] == "directory"),
            "files": sum(1 for entry in entries if entry["kind"] == "file"),
            "active_entries": sum(1 for entry in entries if entry["status"] == "active"),
            "obsolete_or_ignored_entries": sum(1 for entry in entries if entry["status"] == "obsolete_or_ignored"),
            "staging_entries": sum(1 for entry in entries if entry["status"] == "staging")
        },
        "entries": entries
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace_root", type=Path)
    parser.add_argument("--annotations", type=Path)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--md-out", type=Path)
    parser.add_argument("--default-stage", default="")
    args = parser.parse_args()

    workspace_root = args.workspace_root.resolve()
    annotations_path = args.annotations or (workspace_root / "metadata/project_directory_annotations.json")
    json_out = args.json_out or (workspace_root / "metadata/project_directory_index.json")
    md_out = args.md_out or (workspace_root / "reports/project_directory_index.md")
    default_stage = args.default_stage or workspace_root.name

    index = build_index(workspace_root, annotations_path, default_stage)
    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_out.write_text(render_markdown(index), encoding="utf-8")
    print(json.dumps({"json_out": str(json_out.resolve()), "md_out": str(md_out.resolve())}, ensure_ascii=False))


if __name__ == "__main__":
    main()
