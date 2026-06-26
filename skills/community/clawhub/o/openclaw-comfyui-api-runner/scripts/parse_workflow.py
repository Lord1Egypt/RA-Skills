"""
Parse a ComfyUI API-format workflow JSON and optional .meta.json into a variable map.
Output: JSON with required and optional keys, each with node id and input key.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

# Types for variable map entries
VarMapEntry = dict[str, str]  # {"node": "6", "input": "text"}
VariableMap = dict[str, Any]  # {"positive_prompt": VarMapEntry, "extra": {...}}


def load_workflow(path: Path) -> dict[str, Any]:
    """Load workflow API JSON."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_meta(meta_path: Path | None) -> dict[str, Any] | None:
    """Load optional .meta.json."""
    if meta_path is None or not meta_path.is_file():
        return None
    with open(meta_path, encoding="utf-8") as f:
        return json.load(f)


def infer_positive_negative(workflow: dict[str, Any]) -> tuple[str | None, str | None]:
    """Infer first CLIPTextEncode as positive, second as negative (by key order)."""
    clip_nodes: list[str] = []
    for nid, node in workflow.items():
        if not isinstance(node, dict):
            continue
        if node.get("class_type") == "CLIPTextEncode":
            clip_nodes.append(nid)
    clip_nodes.sort(key=lambda x: (len(x), x))
    pos = clip_nodes[0] if clip_nodes else None
    neg = clip_nodes[1] if len(clip_nodes) > 1 else None
    return pos, neg


def infer_sampler(workflow: dict[str, Any]) -> str | None:
    """Infer first KSampler (or KSamplerAdvanced) node."""
    for nid, node in workflow.items():
        if not isinstance(node, dict):
            continue
        if node.get("class_type") in ("KSampler", "KSamplerAdvanced"):
            return nid
    return None


def build_varmap_from_heuristic(workflow: dict[str, Any]) -> dict[str, Any]:
    """Build variable map from workflow using heuristics."""
    pos_node, neg_node = infer_positive_negative(workflow)
    sampler_node = infer_sampler(workflow)
    required: list[str] = []
    optional: list[str] = []
    mapping: dict[str, VarMapEntry] = {}

    if pos_node:
        mapping["positive_prompt"] = {"node": pos_node, "input": "text"}
        required.append("positive_prompt")
    if neg_node:
        mapping["negative_prompt"] = {"node": neg_node, "input": "text"}
        optional.append("negative_prompt")
    if sampler_node:
        mapping["seed"] = {"node": sampler_node, "input": "seed"}
        required.append("seed")
        for key in ("steps", "cfg", "sampler_name", "scheduler", "denoise"):
            if key in (workflow.get(sampler_node) or {}).get("inputs", {}):
                mapping[key] = {"node": sampler_node, "input": key}
                optional.append(key)

    return {
        "required": required,
        "optional": optional,
        "variables": mapping,
    }


def build_varmap_from_meta(meta: dict[str, Any], workflow: dict[str, Any]) -> dict[str, Any]:
    """Build variable map from manifest (.meta.json)."""
    variables: dict[str, VarMapEntry] = {}
    required: list[str] = ["positive_prompt"]
    optional: list[str] = []
    keywords = [str(k).strip().lower() for k in (meta.get("keywords") or []) if str(k).strip()]

    pos_node = meta.get("positive_prompt_node")
    pos_input = meta.get("positive_prompt_input", "text")
    if pos_node:
        variables["positive_prompt"] = {"node": str(pos_node), "input": pos_input}

    seed_node = meta.get("seed_node")
    if seed_node:
        variables["seed"] = {"node": str(seed_node), "input": "seed"}
        optional.append("seed")

    neg_node = meta.get("negative_prompt_node")
    neg_input = meta.get("negative_prompt_input", "text")
    if neg_node:
        variables["negative_prompt"] = {"node": str(neg_node), "input": neg_input}
        optional.append("negative_prompt")

    extra = meta.get("extra") or {}
    for key, val in extra.items():
        if isinstance(val, dict) and "node" in val and "input" in val:
            variables[key] = {"node": str(val["node"]), "input": str(val["input"])}
            optional.append(key)
    
    # Handle model/ckpt_name variable (for fallback mechanism)
    model_info = meta.get("model")
    if isinstance(model_info, dict) and "node" in model_info and "input" in model_info:
        variables["model"] = {"node": str(model_info["node"]), "input": str(model_info["input"])}
        optional.append("model")

    return {
        "required": required,
        "optional": optional,
        "keywords": keywords,
        "variables": variables,
    }


def parse_workflow_meta_only(meta_path: Path) -> dict[str, Any]:
    """
    Build variable map from a .meta.json only (no workflow JSON loaded).
    Returns dict with keys: required (list), optional (list), variables (dict).
    """
    meta = load_meta(meta_path)
    if not meta:
        raise FileNotFoundError(f"Meta file not found: {meta_path}")
    return build_varmap_from_meta(meta, {})


def parse_workflow(
    workflow_path: Path,
    meta_path: Path | None = None,
) -> dict[str, Any]:
    """
    Parse workflow and optional manifest into variable map.
    When meta_path exists, only the meta file is read (workflow JSON is not loaded).
    Returns dict with keys: required (list), optional (list), variables (dict).
    """
    meta = load_meta(meta_path) if meta_path else None
    if meta:
        return build_varmap_from_meta(meta, {})
    workflow = load_workflow(workflow_path)
    return build_varmap_from_heuristic(workflow)


def main() -> None:
    """CLI: parse_workflow.py <workflow.json> [meta.json]"""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: parse_workflow.py <workflow.json> [meta.json]"}), file=sys.stderr)
        sys.exit(1)
    workflow_path = Path(sys.argv[1])
    meta_path = Path(sys.argv[2]) if len(sys.argv) > 2 else workflow_path.with_suffix(".meta.json")
    if not workflow_path.is_file():
        print(json.dumps({"error": f"Not a file: {workflow_path}"}), file=sys.stderr)
        sys.exit(1)
    result = parse_workflow(workflow_path, meta_path if meta_path != workflow_path else None)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
