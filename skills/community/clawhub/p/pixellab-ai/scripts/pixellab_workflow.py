#!/usr/bin/env python3
"""
Guided PixelLab workflow planner and batch utility.

This script turns a rough asset brief plus a recipe into a dry-run manifest
with concrete PixelLab endpoints, payload files, output paths, commands, QA
notes, and optional sprite-layer contracts. It only spends credits through the
`run --yes` command.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as _dt
import html
import io
import json
import os
import pathlib
import re
import shutil
import sys
import urllib.request
import zlib
from typing import Any, Iterable


SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
RECIPES_DIR = SKILL_DIR / "recipes"
CLIENT_PATH = SCRIPT_DIR / "pixellab_client.py"
MANIFEST_VERSION = 1
MAX_CAPTURED_OUTPUT_CHARS = 20000
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
import pixellab_client

TEMPLATE_RE = re.compile(r"{{\s*([A-Za-z0-9_.-]+)\s*}}")
SLUG_RE = re.compile(r"[^a-z0-9._-]+")
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
REVIEW_ARTIFACT_NAMES = {"contact-sheet.png"}
PLACEHOLDER_RE = re.compile(r"REPLACE_WITH|YOUR_|BASE64_", re.IGNORECASE)
COMPLETED_RESULT_STATUSES = {"completed", "complete", "succeeded", "success", "ok", "done"}
RESUMABLE_RESULT_STATUSES = {"submitted", "timeout", "processing", "queued", "pending"}
SECRET_ASSIGNMENT_RE = re.compile(r"PIXELLAB_API_KEY\s*=\s*['\"]?([^'\"\s]+)", re.IGNORECASE)
TILE_ENDPOINTS = {
    "/v2/create-tileset",
    "/v2/tilesets",
    "/v2/create-tileset-sidescroller",
    "/v2/tilesets-sidescroller",
    "/v2/create-tiles-pro",
    "/v2/create-isometric-tile",
    "/v2/isometric-tiles",
}
UI_ENDPOINTS = {"/v2/generate-ui-v2"}
MAP_OBJECT_ENDPOINTS = {
    "/v2/map-objects",
    "/v2/create-1-direction-object",
    "/v2/create-8-direction-object",
    "/v2/objects",
    "/v2/create-object-state",
}
GENERIC_IMAGE_ENDPOINTS = {
    "/v2/create-image-pixflux",
    "/v2/create-image-pixflux-background",
    "/v2/create-image-pixen",
    "/v2/create-image-bitforge",
    "/v2/generate-image-v2",
    "/v2/generate-with-style-v2",
}
ENDPOINT_SIZE_LIMITS = {
    "/v2/create-image-pixflux": {"field": "image_size", "max_width": 400, "max_height": 400},
    "/v2/create-image-pixen": {"field": "image_size", "max_width": 512, "max_height": 512, "divisible_by": 4},
    "/v2/create-image-bitforge": {"field": "image_size", "max_width": 200, "max_height": 200},
    "/v2/rotate": {"field": "image_size", "max_width": 128, "max_height": 128},
    "/v2/resize": {"field": "image_size", "max_width": 200, "max_height": 200},
    "/v2/create-isometric-tile": {"field": "tile_size", "max_width": 64, "max_height": 64},
}
ENDPOINT_COST_ESTIMATES = {
    "/v2/create-image-pixflux": 0.00848,
    "/v2/create-image-pixen": 0.00793,
    "/v2/create-image-bitforge": 0.00821,
    "/v2/image-to-pixelart": 0.00666,
    "/v2/image-to-pixelart-pro": 0.095,
    "/v2/remove-background": 0.00554,
    "/v2/resize": 0.01777,
    "/v2/rotate": 0.01091,
    "/v2/inpaint": 0.00821,
    "/v2/inpaint-v3": 0.095,
    "/v2/edit-image": 0.0118,
    "/v2/edit-images-v2": 0.095,
    "/v2/create-tileset": 0.0079,
    "/v2/create-tileset-sidescroller": 0.0079,
    "/v2/create-tiles-pro": 0.095,
    "/v2/create-isometric-tile": 0.0166,
    "/v2/map-objects": 0.0099,
    "/v2/create-character-v3": 0.042,
    "/v2/create-character-with-4-directions": 0.0122,
    "/v2/create-character-with-8-directions": 0.0173,
    "/v2/create-character-pro": 0.095,
    "/v2/create-character-state": 0.095,
    "/v2/animate-character": 0.095,
    "/v2/characters/animations": 0.095,
    "/v2/objects/{object_id}/animations": 0.095,
    "/v2/objects/{object_id}/states": 0.095,
    "/v2/generate-image-v2": 0.095,
    "/v2/generate-with-style-v2": 0.095,
    "/v2/generate-ui-v2": 0.095,
    "/v2/animate-with-text": 0.01565,
    "/v2/animate-with-text-v3": 0.0424,
    "/v2/animate-with-text-v2": 0.095,
    "/v2/animate-with-skeleton": 0.01572,
    "/v2/edit-animation-v2": 0.095,
    "/v2/interpolation-v2": 0.095,
    "/v2/transfer-outfit-v2": 0.095,
    "/v2/generate-8-rotations-v2": 0.095,
    "/v2/generate-8-rotations-v3": 0.0377,
    "/v2/create-1-direction-object": 0.095,
    "/v2/create-8-direction-object": 0.095,
    "/v2/enhance-pixen-prompt": 0.002,
    "/v2/enhance-character-v3-prompt": 0.002,
    "/v2/enhance-animation-v3-prompt": 0.002,
}
RISK_BUDGET_UNITS = {
    "low": 1,
    "medium": 3,
    "high": 6,
    "unknown": 3,
}
DIGIT_BITMAPS = {
    "0": ("111", "101", "101", "101", "111"),
    "1": ("010", "110", "010", "010", "111"),
    "2": ("111", "001", "111", "100", "111"),
    "3": ("111", "001", "111", "001", "111"),
    "4": ("101", "101", "111", "001", "001"),
    "5": ("111", "100", "111", "001", "111"),
    "6": ("111", "100", "111", "101", "111"),
    "7": ("111", "001", "010", "010", "010"),
    "8": ("111", "101", "111", "101", "111"),
    "9": ("111", "101", "111", "001", "111"),
}


def eprint(*args: Any) -> None:
    print(*args, file=sys.stderr)


def slugify(value: str, fallback: str = "pixellab-pack") -> str:
    slug = SLUG_RE.sub("-", value.strip().lower()).strip("-._")
    return slug or fallback


def read_json(path: pathlib.Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: pathlib.Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def read_optional_json(path: pathlib.Path) -> Any | None:
    if not path.exists():
        return None
    return read_json(path)


def fetch_json_url(url: str) -> Any:
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_text_url(url: str) -> str:
    with urllib.request.urlopen(url, timeout=30) as resp:
        return resp.read().decode("utf-8")


def parse_key_value(raw: str) -> tuple[str, Any]:
    if "=" not in raw:
        raise ValueError(f"expected KEY=VALUE, got {raw!r}")
    key, value = raw.split("=", 1)
    key = key.strip()
    if not key:
        raise ValueError("KEY must not be empty")
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        parsed = value
    return key, parsed


def context_lookup(context: dict[str, Any], key: str) -> Any:
    cur: Any = context
    for part in key.split("."):
        if not isinstance(cur, dict) or part not in cur:
            raise KeyError(f"unknown template variable: {key}")
        cur = cur[part]
    return cur


def render_template(text: str, context: dict[str, Any]) -> Any:
    stripped = text.strip()
    match = TEMPLATE_RE.fullmatch(stripped)
    if match:
        return context_lookup(context, match.group(1))

    def replace(match_obj: re.Match[str]) -> str:
        value = context_lookup(context, match_obj.group(1))
        return str(value)

    return TEMPLATE_RE.sub(replace, text)


def render_value(value: Any, context: dict[str, Any]) -> Any:
    if isinstance(value, str):
        return render_template(value, context)
    if isinstance(value, list):
        return [render_value(item, context) for item in value]
    if isinstance(value, dict):
        return {key: render_value(item, context) for key, item in value.items()}
    return value


REFERENCE_MATERIAL_KEYS = {
    "base64",
    "image",
    "images",
    "init_image",
    "init_images",
    "reference_image",
    "reference_images",
    "style_image",
    "style_images",
    "palette_image",
    "forced_palette_image",
    "first_frame",
    "last_frame",
    "frames",
    "from_image",
    "source_image",
}

CONSISTENCY_SENSITIVE_TYPES = {
    "animation",
    "character",
    "enemy",
    "map_object",
    "sprite",
    "tile",
    "ui",
}


def has_seed_or_reference_material(value: Any) -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            normalized_key = str(key).lower()
            if normalized_key in REFERENCE_MATERIAL_KEYS:
                if isinstance(item, str):
                    if item.strip() and not has_unresolved_placeholder(item):
                        return True
                elif item is not None and not has_unresolved_placeholder(item):
                    return True
            if has_seed_or_reference_material(item):
                return True
    elif isinstance(value, list):
        return any(has_seed_or_reference_material(item) for item in value)
    return False


def seed_candidate_paths(project_slug: str, seed_dir: pathlib.Path, count: int = 4) -> list[str]:
    return [str(seed_dir / f"{project_slug}_seed_candidate_{index:02d}.png") for index in range(1, count + 1)]


def build_seed_reference_gate(
    operations: list[dict[str, Any]],
    has_reference_material: bool,
    references: list[str],
    project_slug: str,
    seed_dir: pathlib.Path,
    reports_dir: pathlib.Path | None = None,
) -> dict[str, Any]:
    asset_types = sorted({str(operation.get("asset_type") or "asset") for operation in operations})
    consistency_sensitive = (
        len(operations) > 1
        or bool(set(asset_types) & CONSISTENCY_SENSITIVE_TYPES)
        or any("style" in str(reference).lower() for reference in references)
    )
    return {
        "needed": consistency_sensitive,
        "has_seed_or_reference_material": has_reference_material,
        "decision_required_before_live": consistency_sensitive and not has_reference_material,
        "visual_brief_required": consistency_sensitive,
        "visual_brief_path": str((reports_dir or seed_dir.parent / "reports") / f"{project_slug}_visual_brief.md"),
        "visual_brief_contract": {
            "agent_job": "Turn the user's rough words into a structured visual brief; do not make the user write PixelLab-grade prompts.",
            "ask_limit": "Ask at most three identity-critical questions before seed generation; fill ordinary gaps with explicit defaults.",
            "required_sections": [
                "project_art_direction",
                "characters_or_objects",
                "camera_and_game_use",
                "palette_and_materials",
                "signature_features",
                "do_not_change",
                "reference_or_seed_decision",
                "approval_criteria",
            ],
            "prompt_categories": [
                "Body",
                "Silhouette",
                "Face",
                "Clothing",
                "Pose",
                "Accessories",
                "Palette",
                "Camera",
                "Game use",
                "Do not include",
            ],
        },
        "seed_candidate_dir": str(seed_dir),
        "seed_candidate_pattern": f"{project_slug}_seed_candidate_{{index:02d}}.png",
        "seed_contact_sheet": str(seed_dir / f"{project_slug}_seed_candidates_contact_sheet.png"),
        "example_seed_candidate_paths": seed_candidate_paths(project_slug, seed_dir),
        "ask": (
            "Before paid generation, draft the visual brief from the user's plain words, then ask whether "
            "the user wants to provide seed/reference images, generate a small seed set for review, or "
            "proceed text-only with drift risk."
        ),
        "options": [
            "Use caller-provided seed/reference images, rough sketches, palettes, screenshots, or approved sprites.",
            "Generate a small seed set first, save it in seed_candidate_dir, build seed_contact_sheet, and approve anchors before bulk generation.",
            "Proceed text-only and report that style/identity consistency may drift and require retries.",
        ],
        "job_scope": "Load only references and helper commands needed for this manifest; do not load the full skill corpus.",
    }


def extract_size(value: Any) -> tuple[int, int] | None:
    if isinstance(value, int):
        return value, value
    if isinstance(value, str):
        if value.isdigit():
            return int(value), int(value)
        try:
            return parse_size(value)
        except argparse.ArgumentTypeError:
            return None
    if isinstance(value, dict):
        width = value.get("width") or value.get("w")
        height = value.get("height") or value.get("h")
        try:
            if width is not None and height is not None:
                return int(width), int(height)
        except (TypeError, ValueError):
            return None
    return None


def payload_size(payload: Any, preferred_field: str = "image_size") -> tuple[int, int] | None:
    if not isinstance(payload, dict):
        return None
    if preferred_field in payload:
        size = extract_size(payload[preferred_field])
        if size:
            return size
    for field in ("image_size", "tile_size", "size", "output_size"):
        if field in payload:
            size = extract_size(payload[field])
            if size:
                return size
    return None


def validate_endpoint_payload(endpoint: str, payload: Any) -> list[str]:
    issues: list[str] = []
    if endpoint == "/v2/create-character-v3" and isinstance(payload, dict):
        allowed_views = {"side", "low top-down", "high top-down"}
        view = payload.get("view")
        if view is not None and view not in allowed_views:
            issues.append("/v2/create-character-v3: view must be one of side, low top-down, or high top-down")
        if "direction" in payload:
            issues.append("/v2/create-character-v3: do not send direction; put facing language in description or use a 4/8-direction endpoint")
    limits = ENDPOINT_SIZE_LIMITS.get(endpoint)
    if not limits:
        return issues
    size = payload_size(payload, str(limits.get("field", "image_size")))
    if not size:
        return issues
    width, height = size
    max_width = int(limits["max_width"])
    max_height = int(limits["max_height"])
    if width > max_width or height > max_height:
        issues.append(f"{endpoint}: requested {width}x{height}, max is {max_width}x{max_height}")
    divisible_by = limits.get("divisible_by")
    if divisible_by and (width % int(divisible_by) or height % int(divisible_by)):
        issues.append(f"{endpoint}: requested {width}x{height}, dimensions must be divisible by {divisible_by}")
    return issues


def validate_endpoint(endpoint: str) -> None:
    if endpoint.startswith("http://") or endpoint.startswith("https://"):
        raise ValueError("endpoint must be a PixelLab /v1/ or /v2/ path, not a full URL")
    if not (endpoint.startswith("/v1/") or endpoint.startswith("/v2/")):
        raise ValueError("endpoint must start with /v1/ or /v2/")
    if ".." in endpoint:
        raise ValueError("endpoint must not contain '..'")


def validate_recipe(recipe: dict[str, Any]) -> None:
    if not isinstance(recipe, dict):
        raise ValueError("recipe must be a JSON object")
    if not recipe.get("name"):
        raise ValueError("recipe.name is required")
    assets = recipe.get("assets")
    if not isinstance(assets, list) or not assets:
        raise ValueError("recipe.assets must be a non-empty list")
    seen_ids: set[str] = set()
    for idx, asset in enumerate(assets, start=1):
        if not isinstance(asset, dict):
            raise ValueError(f"asset {idx} must be an object")
        asset_id = asset.get("id")
        if not isinstance(asset_id, str) or not asset_id:
            raise ValueError(f"asset {idx} needs a non-empty id")
        if asset_id in seen_ids:
            raise ValueError(f"duplicate asset id: {asset_id}")
        seen_ids.add(asset_id)
        endpoint = asset.get("endpoint")
        if not isinstance(endpoint, str):
            raise ValueError(f"asset {asset_id} needs endpoint")
        validate_endpoint(endpoint)
        method = str(asset.get("method", "post")).lower()
        if method not in {"get", "post", "patch"}:
            raise ValueError(f"asset {asset_id} has unsupported method: {method}")
        if method in {"post", "patch"} and not isinstance(asset.get("payload"), dict):
            raise ValueError(f"asset {asset_id} needs a payload object")


def load_recipe(name_or_path: str, recipes_dir: pathlib.Path = RECIPES_DIR) -> dict[str, Any]:
    candidate = pathlib.Path(name_or_path)
    if candidate.exists():
        return read_json(candidate)
    recipe_path = recipes_dir / f"{name_or_path}.json"
    if recipe_path.exists():
        return read_json(recipe_path)
    names = ", ".join(path.stem for path in sorted(recipes_dir.glob("*.json"))) if recipes_dir.exists() else ""
    raise FileNotFoundError(f"recipe not found: {name_or_path}. Available recipes: {names}")


def infer_asset_type(asset_id: str, label: Any = "") -> str:
    text = f"{asset_id} {label}".lower()
    if any(word in text for word in ("tile", "tileset", "terrain")):
        return "tile"
    if any(word in text for word in ("hud", "ui", "button", "menu", "badge", "icon", "counter")):
        return "ui"
    if any(word in text for word in ("prop", "pickup", "collectible", "hazard", "object", "coin", "chest", "door")):
        return "map_object"
    if any(word in text for word in ("background", "parallax", "skyline")):
        return "background"
    if any(word in text for word in ("character", "hero", "enemy", "npc", "sprite", "companion")):
        return "sprite"
    return "asset"


def endpoint_matches(endpoint: str, choices: set[str]) -> bool:
    return endpoint in choices or any(endpoint.startswith(f"{choice}/") for choice in choices)


def endpoint_cost_estimate(endpoint: str) -> float:
    if endpoint in ENDPOINT_COST_ESTIMATES:
        return ENDPOINT_COST_ESTIMATES[endpoint]
    for template, estimate in ENDPOINT_COST_ESTIMATES.items():
        if "{" not in template:
            continue
        pattern = re.escape(template)
        pattern = re.sub(r"\\\{[^}]+\\\}", r"[^/]+", pattern)
        if re.fullmatch(pattern, endpoint):
            return estimate
    return 0.0


def lint_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    for operation in manifest.get("operations", []):
        op_id = str(operation.get("id", "unknown"))
        endpoint = str(operation.get("endpoint", ""))
        asset_type = str(operation.get("asset_type") or infer_asset_type(op_id, operation.get("label", ""))).lower()
        payload = read_optional_json(pathlib.Path(operation["payload_file"])) if operation.get("payload_file") else None
        if endpoint == "/v2/generate-image-v2" and asset_type in {"sprite", "tile", "ui", "map_object", "prop", "pickup", "hazard"}:
            issues.append(
                f"{op_id}: /v2/generate-image-v2 is Pro/async and often returns multiple candidates; use create-image-pixflux, create-image-pixen, or create-image-bitforge for simple sprites."
            )
        if asset_type in {"tile", "tileset", "terrain"} and not endpoint_matches(endpoint, TILE_ENDPOINTS):
            issues.append(f"{op_id}: tile assets should use create-tiles-pro/create-tileset routes, not {endpoint}.")
        if asset_type in {"ui", "hud", "badge", "icon", "menu"} and not endpoint_matches(endpoint, UI_ENDPOINTS):
            issues.append(f"{op_id}: UI assets should use /v2/generate-ui-v2, not {endpoint}.")
        if asset_type in {"map_object", "prop", "pickup", "hazard"} and endpoint in GENERIC_IMAGE_ENDPOINTS:
            issues.append(f"{op_id}: map props/pickups/hazards should consider /v2/map-objects or object endpoints, not generic image generation.")
        if not operation.get("candidate_policy"):
            issues.append(f"{op_id}: missing candidate approval policy; do not auto-pick the first returned image.")
        for payload_issue in validate_endpoint_payload(endpoint, payload):
            issues.append(f"{op_id}: {payload_issue}")
    return {"ok": not issues, "issue_count": len(issues), "issues": issues}


def operation_command(
    method: str,
    endpoint: str,
    payload_file: pathlib.Path | None,
    result_file: pathlib.Path,
    download_dir: pathlib.Path,
    poll: bool,
    asset_slug: str,
    progress_jsonl: pathlib.Path,
    expected_size: tuple[int, int] | None = None,
    require_alpha: bool = False,
) -> list[str]:
    command = [
        "python3",
        str(CLIENT_PATH),
        method,
        endpoint,
    ]
    if payload_file is not None:
        command.extend(["--payload-file", str(payload_file)])
    if poll:
        command.append("--poll")
    command.extend(
        [
            "--quiet",
            "--asset-slug",
            asset_slug,
            "--progress-jsonl",
            str(progress_jsonl),
            "--result-file",
            str(result_file),
        ]
    )
    if expected_size:
        command.extend(["--expect-size", f"{expected_size[0]}x{expected_size[1]}"])
    if require_alpha:
        command.append("--require-alpha")
    command.extend(["--download-dir", str(download_dir)])
    return command


def build_manifest(
    recipe: dict[str, Any],
    brief: str,
    output_dir: pathlib.Path,
    project_slug: str | None = None,
    seed: int = 0,
    extra_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    validate_recipe(recipe)
    output_dir = pathlib.Path(output_dir)
    project_slug = slugify(project_slug or brief or recipe["name"])
    defaults = dict(recipe.get("defaults") or {})
    context_base: dict[str, Any] = {
        **defaults,
        "brief": brief,
        "project_slug": project_slug,
        "recipe_name": recipe["name"],
        "seed": seed,
    }
    if extra_context:
        context_base.update(extra_context)

    payload_dir = output_dir / "payloads"
    results_dir = output_dir / "results"
    candidates_dir = output_dir / "candidates"
    approved_dir = output_dir / "approved"
    downloads_dir = output_dir / "downloads"
    seed_dir = output_dir / "seed-candidates"
    logs_dir = output_dir / "logs"
    progress_jsonl = logs_dir / "events.jsonl"
    cost_jsonl = logs_dir / "cost.jsonl"
    operations: list[dict[str, Any]] = []
    manifest_references = list(recipe.get("references", []))
    has_reference_material = has_seed_or_reference_material(context_base)

    for idx, asset in enumerate(recipe["assets"], start=1):
        asset_id = slugify(str(asset["id"]), fallback=f"asset-{idx:02d}")
        asset_context = {
            **context_base,
            **asset.get("vars", {}),
            "asset_id": asset_id,
            "asset_label": asset.get("label", asset_id),
            "asset_index": idx,
        }
        if "seed_offset" in asset:
            asset_context["seed"] = int(seed) + int(asset["seed_offset"])
        prompt = render_template(str(asset.get("prompt", "{{brief}}")), asset_context)
        asset_context["prompt"] = prompt

        method = str(asset.get("method", "post")).lower()
        endpoint = str(asset["endpoint"])
        validate_endpoint(endpoint)
        poll = bool(asset.get("poll", method == "post" and "background" not in endpoint))
        output_subdir = slugify(str(asset.get("output_subdir", asset_id)), fallback=asset_id)
        download_dir = candidates_dir / output_subdir
        approved_dir_for_asset = approved_dir / output_subdir
        result_file = results_dir / asset_id / "result.json"
        expected_size_raw = asset.get("expected_size") or asset_context.get("image_size")
        expected_size: tuple[int, int] | None = None
        if isinstance(expected_size_raw, int):
            expected_size = (expected_size_raw, expected_size_raw)
        elif isinstance(expected_size_raw, str):
            try:
                expected_size = parse_size(expected_size_raw)
            except argparse.ArgumentTypeError:
                expected_size = None
        payload_file: pathlib.Path | None = None
        payload: Any = None
        if method in {"post", "patch"}:
            payload = render_value(asset["payload"], asset_context)
            has_reference_material = has_reference_material or has_seed_or_reference_material(payload)
            payload_file = payload_dir / f"{idx:02d}-{asset_id}.json"
            write_json(payload_file, payload)

        operations.append(
            {
                "id": asset_id,
                "label": asset.get("label", asset_id),
                "asset_type": asset.get("asset_type", infer_asset_type(asset_id, asset.get("label", asset_id))),
                "method": method,
                "endpoint": endpoint,
                "prompt": prompt,
                "payload_file": str(payload_file) if payload_file else None,
                "result_file": str(result_file),
                "download_dir": str(download_dir),
                "approved_dir": str(approved_dir_for_asset),
                "contact_sheet": str(download_dir / "contact-sheet.png"),
                "poll": poll,
                "credit_risk": asset.get("credit_risk", "unknown"),
                "depends_on": asset.get("depends_on", []),
                "qa": asset.get("qa", []),
                "expected_size": list(expected_size) if expected_size else None,
                "requires_alpha": bool(asset.get("requires_alpha", True)),
                "candidate_policy": "Review all returned candidates in contact-sheet.png and copy the approved index into approved_dir; do not auto-pick first.",
                "command": operation_command(
                    method,
                    endpoint,
                    payload_file,
                    result_file,
                    download_dir,
                    poll,
                    asset_id,
                    progress_jsonl,
                    expected_size=expected_size,
                    require_alpha=bool(asset.get("requires_alpha", True)),
                ),
            }
        )

    now = _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")
    return {
        "manifest_version": MANIFEST_VERSION,
        "created_at": now,
        "mode": "dry-run",
        "recipe": recipe["name"],
        "project_slug": project_slug,
        "brief": brief,
        "seed": seed,
        "output_dir": str(output_dir),
        "candidate_root": str(candidates_dir),
        "approved_root": str(approved_dir),
        "downloads_root": str(downloads_dir),
        "seed_candidate_root": str(seed_dir),
        "results_root": str(results_dir),
        "logs_root": str(logs_dir),
        "progress_jsonl": str(progress_jsonl),
        "cost_jsonl": str(cost_jsonl),
        "credit_policy": "No PixelLab credits are spent by plan. Run requires explicit run --yes.",
        "operations": operations,
        "seed_reference_gate": build_seed_reference_gate(
            operations,
            has_reference_material,
            manifest_references,
            project_slug,
            seed_dir,
            output_dir / "reports",
        ),
        "sprite_contract": recipe.get("sprite_contract"),
        "qa": recipe.get("qa", []),
        "references": manifest_references,
        "next_steps": [
            "Inspect payloads under payloads/ before spending credits.",
            "Write or update the visual brief at seed_reference_gate.visual_brief_path for named characters, worlds, UI kits, tilesets, or consistent packs.",
            "Resolve seed_reference_gate before live generation when decision_required_before_live is true.",
            "Store generated seed candidates only under seed-candidates/ using project_slug_seed_candidate_01.png style names.",
            "Run lint-manifest and budget before live generation.",
            "Check /v2/balance before large runs.",
            "Run this manifest only with pixellab_workflow.py run --yes.",
            "Generate contact sheets and approve candidate indexes before promoting files to approved/.",
        ],
    }


def write_manifest(manifest: dict[str, Any], manifest_path: pathlib.Path) -> pathlib.Path:
    write_json(manifest_path, manifest)
    return manifest_path


def load_manifest(manifest_path: pathlib.Path) -> dict[str, Any]:
    manifest = read_json(manifest_path)
    if manifest.get("manifest_version") != MANIFEST_VERSION:
        raise ValueError(f"unsupported manifest_version: {manifest.get('manifest_version')}")
    if not isinstance(manifest.get("operations"), list):
        raise ValueError("manifest.operations must be a list")
    return manifest


def estimate_budget(manifest: dict[str, Any]) -> dict[str, Any]:
    risk_counts: dict[str, int] = {}
    endpoint_counts: dict[str, int] = {}
    estimated_units = 0
    estimated_cost_usd = 0.0
    for operation in manifest.get("operations", []):
        risk = str(operation.get("credit_risk") or "unknown").lower()
        if risk not in RISK_BUDGET_UNITS:
            risk = "unknown"
        risk_counts[risk] = risk_counts.get(risk, 0) + 1
        estimated_units += RISK_BUDGET_UNITS[risk]
        endpoint = str(operation.get("endpoint") or "")
        endpoint_counts[endpoint] = endpoint_counts.get(endpoint, 0) + 1
        estimated_cost_usd += endpoint_cost_estimate(endpoint)
    return {
        "operation_count": len(manifest.get("operations", [])),
        "risk_counts": risk_counts,
        "endpoint_counts": endpoint_counts,
        "risk_unit_weights": RISK_BUDGET_UNITS,
        "estimated_budget_units": estimated_units,
        "estimated_cost_usd": round(estimated_cost_usd, 6),
        "cost_estimate_source": "Approximate public API page examples; use /v2/balance and result usage_cost_usd for account truth.",
        "note": "Budget units are conservative risk weights, not exact PixelLab credits. Use live /v2/balance and result usage_cost_usd for account truth.",
    }


def has_unresolved_placeholder(value: Any) -> bool:
    if isinstance(value, str):
        return bool(PLACEHOLDER_RE.search(value))
    if isinstance(value, list):
        return any(has_unresolved_placeholder(item) for item in value)
    if isinstance(value, dict):
        return any(has_unresolved_placeholder(item) for item in value.values())
    return False


def iter_placeholder_paths(value: Any, prefix: str = "") -> list[str]:
    paths: list[str] = []
    if isinstance(value, str):
        if PLACEHOLDER_RE.search(value):
            paths.append(prefix or "$")
    elif isinstance(value, list):
        for idx, item in enumerate(value):
            child_prefix = f"{prefix}[{idx}]" if prefix else f"[{idx}]"
            paths.extend(iter_placeholder_paths(item, child_prefix))
    elif isinstance(value, dict):
        for key, item in value.items():
            child_prefix = f"{prefix}.{key}" if prefix else str(key)
            paths.extend(iter_placeholder_paths(item, child_prefix))
    return paths


def placeholder_report(manifest: dict[str, Any]) -> dict[str, Any]:
    placeholders: list[dict[str, Any]] = []
    for operation in manifest.get("operations", []):
        payload_file = operation.get("payload_file")
        if not payload_file:
            continue
        payload_path = pathlib.Path(payload_file)
        if not payload_path.exists():
            continue
        paths = iter_placeholder_paths(read_json(payload_path))
        if paths:
            placeholders.append(
                {
                    "operation_id": operation.get("id"),
                    "payload_file": str(payload_path),
                    "paths": paths,
                    "next_step": "Replace these placeholders with caller-owned local image/base64 data before live run.",
                }
            )
    return {
        "ok": not placeholders,
        "placeholder_count": sum(len(item["paths"]) for item in placeholders),
        "placeholders": placeholders,
    }


def blocked_run_report(output_dir: pathlib.Path, reason: str) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    ledger_path = output_dir / "asset-ledger.tsv"
    ledger_path.write_text("id\tendpoint\tstatus\tresult_file\tdownload_dir\nRUN\t-\tblocked\t-\t-\n", encoding="utf-8")
    errors = [{"id": "RUN", "endpoint": None, "returncode": 4, "stdout": "", "stderr": reason}]
    write_json(output_dir / "errors.json", errors)
    write_json(output_dir / "run-results.json", errors)
    return {
        "ok": False,
        "ledger": str(ledger_path),
        "errors": str(output_dir / "errors.json"),
        "results": str(output_dir / "run-results.json"),
    }


def result_job_ids(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return []
    ids: list[str] = []
    raw_ids = data.get("job_ids")
    if isinstance(raw_ids, list):
        ids.extend(str(item) for item in raw_ids if item)
    raw_id = data.get("job_id")
    if raw_id:
        ids.insert(0, str(raw_id))
    seen: set[str] = set()
    unique: list[str] = []
    for job_id in ids:
        if job_id not in seen:
            unique.append(job_id)
            seen.add(job_id)
    return unique


def existing_result_state(operation: dict[str, Any]) -> dict[str, Any] | None:
    result_file = operation.get("result_file")
    if not result_file:
        return None
    result_path = pathlib.Path(result_file)
    if not result_path.exists():
        return None
    try:
        data = read_json(result_path)
    except Exception as err:
        return {
            "status": "unreadable",
            "result_file": str(result_path),
            "job_ids": [],
            "error": str(err),
        }
    status = str(data.get("status") or "").lower()
    return {
        "status": status,
        "result_file": str(result_path),
        "job_ids": result_job_ids(data),
        "candidate_count": int(data.get("candidate_count") or 0),
        "downloaded_files": list(data.get("downloaded_files") or []),
        "decoded_files": list(data.get("decoded_files") or []),
    }


def operation_is_complete(state: dict[str, Any] | None) -> bool:
    if not state:
        return False
    return str(state.get("status") or "").lower() in COMPLETED_RESULT_STATUSES


def operation_can_resume(state: dict[str, Any] | None) -> bool:
    if not state:
        return False
    status = str(state.get("status") or "").lower()
    return status in RESUMABLE_RESULT_STATUSES and bool(state.get("job_ids"))


def resume_command_for_operation(operation: dict[str, Any], manifest: dict[str, Any]) -> list[str]:
    command = [
        "python3",
        str(CLIENT_PATH),
        "poll-result-file",
        str(operation["result_file"]),
        "--quiet",
        "--asset-slug",
        slugify(str(operation.get("id") or "asset"), fallback="asset"),
        "--result-file",
        str(operation["result_file"]),
    ]
    if manifest.get("progress_jsonl"):
        command.extend(["--progress-jsonl", str(manifest["progress_jsonl"])])
    expected_size = operation.get("expected_size")
    if isinstance(expected_size, list) and len(expected_size) == 2:
        command.extend(["--expect-size", f"{expected_size[0]}x{expected_size[1]}"])
    if operation.get("requires_alpha"):
        command.append("--require-alpha")
    if operation.get("download_dir"):
        command.extend(["--download-dir", str(operation["download_dir"])])
    return command


class CommandResult:
    def __init__(self, args: list[str], returncode: int, stdout: str, stderr: str) -> None:
        self.args = args
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def truncate_output(value: str, limit: int = MAX_CAPTURED_OUTPUT_CHARS) -> str:
    if len(value) <= limit:
        return value
    omitted = len(value) - limit
    return value[:limit] + f"\n[truncated {omitted} chars]\n"


def manifest_output_root(manifest: dict[str, Any]) -> pathlib.Path:
    output_dir = manifest.get("output_dir")
    if not isinstance(output_dir, str) or not output_dir.strip():
        raise ValueError("manifest.output_dir is required")
    return pathlib.Path(output_dir).expanduser().resolve()


def manifest_path_within_output(
    raw_path: Any,
    manifest: dict[str, Any],
    field: str,
    required: bool = True,
) -> pathlib.Path | None:
    if raw_path in (None, ""):
        if required:
            raise ValueError(f"operation.{field} is required")
        return None
    if not isinstance(raw_path, str):
        raise ValueError(f"operation.{field} must be a string path")
    root = manifest_output_root(manifest)
    resolved = pathlib.Path(raw_path).expanduser().resolve()
    if not resolved.is_relative_to(root):
        raise ValueError(f"operation.{field} must stay under manifest.output_dir")
    return resolved


def normalize_operation_for_run(operation: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(operation, dict):
        raise ValueError("manifest.operations entries must be objects")

    normalized = dict(operation)
    operation_id = slugify(str(operation.get("id") or "asset"), fallback="asset")
    method = str(operation.get("method", "post")).lower()
    if method not in {"get", "post", "patch"}:
        raise ValueError(f"{operation_id}: unsupported method for run: {method}")
    endpoint = str(operation.get("endpoint") or "")
    validate_endpoint(endpoint)

    payload_path = manifest_path_within_output(operation.get("payload_file"), manifest, "payload_file", required=False)
    if method in {"post", "patch"} and payload_path is None:
        raise ValueError(f"{operation_id}: payload_file is required for {method}")

    result_path = manifest_path_within_output(operation.get("result_file"), manifest, "result_file")
    download_dir = manifest_path_within_output(operation.get("download_dir"), manifest, "download_dir")

    expected_size = operation.get("expected_size")
    if expected_size is not None:
        if (
            not isinstance(expected_size, list)
            or len(expected_size) != 2
            or not all(isinstance(item, int) and item > 0 for item in expected_size)
        ):
            raise ValueError(f"{operation_id}: expected_size must be [width, height]")

    normalized.update(
        {
            "id": operation_id,
            "method": method,
            "endpoint": endpoint,
            "payload_file": str(payload_path) if payload_path else None,
            "result_file": str(result_path),
            "download_dir": str(download_dir),
            "poll": bool(operation.get("poll")),
            "requires_alpha": bool(operation.get("requires_alpha")),
        }
    )
    return normalized


def command_for_operation(operation: dict[str, Any], manifest: dict[str, Any]) -> list[str]:
    progress_jsonl = manifest_path_within_output(
        manifest.get("progress_jsonl") or str(manifest_output_root(manifest) / "logs" / "events.jsonl"),
        manifest,
        "progress_jsonl",
    )
    expected_size_raw = operation.get("expected_size")
    expected_size: tuple[int, int] | None = None
    if isinstance(expected_size_raw, list) and len(expected_size_raw) == 2:
        expected_size = (int(expected_size_raw[0]), int(expected_size_raw[1]))
    return operation_command(
        str(operation["method"]),
        str(operation["endpoint"]),
        pathlib.Path(operation["payload_file"]) if operation.get("payload_file") else None,
        pathlib.Path(operation["result_file"]),
        pathlib.Path(operation["download_dir"]),
        bool(operation.get("poll")),
        slugify(str(operation.get("id") or "asset"), fallback="asset"),
        progress_jsonl,
        expected_size=expected_size,
        require_alpha=bool(operation.get("requires_alpha")),
    )


def run_client_command(command: list[str]) -> CommandResult:
    if len(command) < 3 or command[0] != "python3" or pathlib.Path(command[1]).resolve() != CLIENT_PATH.resolve():
        raise ValueError("run command must invoke the bundled PixelLab client with python3")

    stdout = io.StringIO()
    stderr = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            returncode = int(pixellab_client.main(command[2:]))
    except SystemExit as err:
        returncode = int(err.code) if isinstance(err.code, int) else 1
    return CommandResult(
        args=command,
        returncode=returncode,
        stdout=truncate_output(stdout.getvalue()),
        stderr=truncate_output(stderr.getvalue()),
    )


def run_manifest(
    manifest_path: pathlib.Path,
    yes: bool,
    continue_on_error: bool = False,
    max_budget_units: int | None = None,
    rerun_existing: bool = False,
) -> dict[str, Any]:
    if not yes:
        raise RuntimeError("refusing to spend credits without --yes")
    manifest = load_manifest(manifest_path)
    output_dir = pathlib.Path(manifest["output_dir"])
    budget = estimate_budget(manifest)
    if max_budget_units is not None and budget["estimated_budget_units"] > max_budget_units:
        return blocked_run_report(
            output_dir,
            f"budget limit blocked run: estimated {budget['estimated_budget_units']} units > max {max_budget_units}\n",
        )

    ledger_rows = ["id\tendpoint\tstatus\tresult_file\tdownload_dir"]
    errors: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []
    progress_jsonl = pathlib.Path(manifest["progress_jsonl"]) if manifest.get("progress_jsonl") else None

    for raw_operation in manifest["operations"]:
        try:
            operation = normalize_operation_for_run(raw_operation, manifest)
            command = command_for_operation(operation, manifest)
        except Exception as err:
            operation = raw_operation if isinstance(raw_operation, dict) else {"id": "unknown", "endpoint": None}
            command = []
            completed = CommandResult(
                args=command,
                returncode=4,
                stdout="",
                stderr=f"invalid manifest operation: {err}\n",
            )
            status = "blocked-invalid-manifest"
            ledger_rows.append(
                f"{operation.get('id', 'unknown')}\t{operation.get('endpoint', '-')}\t{status}\t{operation.get('result_file', '-')}\t{operation.get('download_dir', '-')}"
            )
            result = {
                "id": operation.get("id", "unknown"),
                "endpoint": operation.get("endpoint"),
                "returncode": completed.returncode,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
            }
            results.append(result)
            errors.append(result)
            if not continue_on_error:
                break
            continue

        eprint(f"[run] {operation['id']} -> {operation['endpoint']}")
        existing_state = existing_result_state(operation)
        if existing_state and not rerun_existing and operation_is_complete(existing_state):
            status = "skipped-existing"
            ledger_rows.append(
                f"{operation['id']}\t{operation['endpoint']}\t{status}\t{operation['result_file']}\t{operation['download_dir']}"
            )
            result = {
                "id": operation["id"],
                "endpoint": operation["endpoint"],
                "returncode": 0,
                "status": status,
                "stdout": json.dumps(existing_state, ensure_ascii=True),
                "stderr": "",
            }
            results.append(result)
            append_jsonl(progress_jsonl, {"event": "skipped_existing", "operation_id": operation["id"], **existing_state})
            continue
        if existing_state and not rerun_existing and operation_can_resume(existing_state):
            command = resume_command_for_operation(operation, manifest)
            append_jsonl(progress_jsonl, {"event": "resume_existing_job", "operation_id": operation["id"], **existing_state})
        payload_file = operation.get("payload_file")
        if payload_file and has_unresolved_placeholder(read_json(pathlib.Path(payload_file))):
            completed = CommandResult(
                command,
                3,
                stdout="",
                stderr=f"unresolved placeholder in payload file: {payload_file}\n",
            )
            status = "blocked-placeholder"
        else:
            completed = run_client_command(command)
            if completed.returncode == 0:
                status = "resumed-ok" if existing_state and operation_can_resume(existing_state) and not rerun_existing else "ok"
            elif completed.returncode == 3:
                status = "resumed-timeout" if existing_state and operation_can_resume(existing_state) and not rerun_existing else "timeout"
            else:
                status = f"resumed-exit-{completed.returncode}" if existing_state and operation_can_resume(existing_state) and not rerun_existing else f"exit-{completed.returncode}"
        ledger_rows.append(
            f"{operation['id']}\t{operation['endpoint']}\t{status}\t{operation['result_file']}\t{operation['download_dir']}"
        )
        result = {
            "id": operation["id"],
            "endpoint": operation["endpoint"],
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
        results.append(result)
        if completed.returncode != 0:
            errors.append(result)
            if not continue_on_error:
                break

    ledger_path = output_dir / "asset-ledger.tsv"
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text("\n".join(ledger_rows) + "\n", encoding="utf-8")
    if errors:
        write_json(output_dir / "errors.json", errors)
    write_json(output_dir / "run-results.json", results)
    return {
        "ok": not errors,
        "ledger": str(ledger_path),
        "errors": str(output_dir / "errors.json") if errors else None,
        "results": str(output_dir / "run-results.json"),
    }


def write_retry_manifest(manifest_path: pathlib.Path, errors_path: pathlib.Path, output_path: pathlib.Path) -> pathlib.Path:
    manifest = load_manifest(manifest_path)
    errors = read_json(errors_path)
    failed_ids = {str(item.get("id")) for item in errors if item.get("id")}
    operations = [operation for operation in manifest["operations"] if str(operation.get("id")) in failed_ids]
    retry_manifest = {
        **manifest,
        "mode": "retry",
        "retry_source_manifest": str(manifest_path),
        "retry_source_errors": str(errors_path),
        "operations": operations,
    }
    write_json(output_path, retry_manifest)
    return output_path


def iter_image_files(asset_root: pathlib.Path) -> list[pathlib.Path]:
    if not asset_root.exists():
        return []
    return sorted(
        path for path in asset_root.rglob("*") if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def write_gallery(asset_root: pathlib.Path, output_path: pathlib.Path) -> pathlib.Path:
    asset_root = pathlib.Path(asset_root)
    output_path = pathlib.Path(output_path)
    images = iter_image_files(asset_root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cards: list[str] = []
    for image_path in images:
        rel = image_path.relative_to(output_path.parent)
        label = image_path.relative_to(asset_root) if image_path.is_relative_to(asset_root) else image_path.name
        cards.append(
            "<figure>"
            f'<img src="{html.escape(rel.as_posix())}" alt="{html.escape(str(label))}">'
            f"<figcaption>{html.escape(str(label))}</figcaption>"
            "</figure>"
        )
    html_doc = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>PixelLab Asset Gallery</title>
  <style>
    body { margin: 24px; font: 14px/1.4 system-ui, sans-serif; background: #f7f7f4; color: #1d1d1b; }
    h1 { font-size: 22px; margin: 0 0 16px; }
    main { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px; }
    figure { margin: 0; padding: 10px; border: 1px solid #d8d8d0; background: #fff; border-radius: 6px; }
    img { width: 100%; image-rendering: pixelated; background: repeating-conic-gradient(#ddd 0% 25%, #fff 0% 50%) 50% / 16px 16px; }
    figcaption { margin-top: 8px; overflow-wrap: anywhere; font-size: 12px; color: #333; }
  </style>
</head>
<body>
  <h1>PixelLab Asset Gallery</h1>
  <main>
    __CARDS__
  </main>
</body>
</html>
"""
    output_path.write_text(html_doc.replace("__CARDS__", "\n    ".join(cards)), encoding="utf-8")
    return output_path


def read_png_size(path: pathlib.Path) -> tuple[int, int] | None:
    with open(path, "rb") as f:
        header = f.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        return None
    return int.from_bytes(header[16:20], "big"), int.from_bytes(header[20:24], "big")


def png_chunks(path: pathlib.Path) -> tuple[dict[str, Any], bytes]:
    data = path.read_bytes()
    if len(data) < 33 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    pos = 8
    ihdr: dict[str, Any] | None = None
    idat_parts: list[bytes] = []
    while pos + 8 <= len(data):
        length = int.from_bytes(data[pos : pos + 4], "big")
        kind = data[pos + 4 : pos + 8]
        chunk_data = data[pos + 8 : pos + 8 + length]
        pos += 12 + length
        if kind == b"IHDR":
            ihdr = {
                "width": int.from_bytes(chunk_data[0:4], "big"),
                "height": int.from_bytes(chunk_data[4:8], "big"),
                "bit_depth": chunk_data[8],
                "color_type": chunk_data[9],
            }
        elif kind == b"IDAT":
            idat_parts.append(chunk_data)
        elif kind == b"IEND":
            break
    if ihdr is None:
        raise ValueError("missing PNG IHDR")
    return ihdr, b"".join(idat_parts)


def paeth_predictor(left: int, up: int, up_left: int) -> int:
    p = left + up - up_left
    pa = abs(p - left)
    pb = abs(p - up)
    pc = abs(p - up_left)
    if pa <= pb and pa <= pc:
        return left
    if pb <= pc:
        return up
    return up_left


def decode_png_scanlines(path: pathlib.Path) -> tuple[dict[str, Any], bytes] | None:
    try:
        ihdr, idat = png_chunks(path)
        if ihdr["bit_depth"] != 8 or ihdr["color_type"] not in {2, 6}:
            return None
        channels = 4 if ihdr["color_type"] == 6 else 3
        stride = ihdr["width"] * channels
        raw = zlib.decompress(idat)
        rows: list[bytes] = []
        prev = bytearray(stride)
        pos = 0
        for _ in range(ihdr["height"]):
            filter_type = raw[pos]
            pos += 1
            scanline = bytearray(raw[pos : pos + stride])
            pos += stride
            for idx, value in enumerate(scanline):
                left = scanline[idx - channels] if idx >= channels else 0
                up = prev[idx]
                up_left = prev[idx - channels] if idx >= channels else 0
                if filter_type == 0:
                    recon = value
                elif filter_type == 1:
                    recon = (value + left) & 0xFF
                elif filter_type == 2:
                    recon = (value + up) & 0xFF
                elif filter_type == 3:
                    recon = (value + ((left + up) // 2)) & 0xFF
                elif filter_type == 4:
                    recon = (value + paeth_predictor(left, up, up_left)) & 0xFF
                else:
                    return None
                scanline[idx] = recon
            rows.append(bytes(scanline))
            prev = scanline
        return ihdr, b"".join(rows)
    except Exception:
        return None


def png_is_fully_transparent(path: pathlib.Path) -> bool:
    decoded = decode_png_scanlines(path)
    if decoded is None:
        return False
    ihdr, pixels = decoded
    if ihdr["color_type"] != 6:
        return False
    return all(pixels[idx] == 0 for idx in range(3, len(pixels), 4))


def png_chunk(kind: bytes, data: bytes) -> bytes:
    payload = kind + data
    return len(data).to_bytes(4, "big") + payload + zlib.crc32(payload).to_bytes(4, "big")


def write_rgba_png(path: pathlib.Path, width: int, height: int, pixels: bytes) -> pathlib.Path:
    raw_rows = []
    stride = width * 4
    for row in range(height):
        start = row * stride
        raw_rows.append(b"\x00" + pixels[start : start + stride])
    png = (
        b"\x89PNG\r\n\x1a\n"
        + png_chunk(b"IHDR", width.to_bytes(4, "big") + height.to_bytes(4, "big") + b"\x08\x06\x00\x00\x00")
        + png_chunk(b"IDAT", zlib.compress(b"".join(raw_rows)))
        + png_chunk(b"IEND", b"")
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png)
    return path


def draw_rect(
    canvas: bytearray,
    canvas_width: int,
    canvas_height: int,
    x: int,
    y: int,
    rect_width: int,
    rect_height: int,
    color: tuple[int, int, int, int],
) -> None:
    for py in range(max(0, y), min(canvas_height, y + rect_height)):
        for px in range(max(0, x), min(canvas_width, x + rect_width)):
            idx = (py * canvas_width + px) * 4
            canvas[idx : idx + 4] = bytes(color)


def draw_digit_text(
    canvas: bytearray,
    canvas_width: int,
    canvas_height: int,
    text: str,
    x: int,
    y: int,
    scale: int,
    color: tuple[int, int, int, int],
) -> None:
    cursor_x = x
    for char in text:
        bitmap = DIGIT_BITMAPS.get(char)
        if bitmap is None:
            cursor_x += 2 * scale
            continue
        for row, line in enumerate(bitmap):
            for col, pixel in enumerate(line):
                if pixel == "1":
                    draw_rect(
                        canvas,
                        canvas_width,
                        canvas_height,
                        cursor_x + col * scale,
                        y + row * scale,
                        scale,
                        scale,
                        color,
                    )
        cursor_x += (len(bitmap[0]) + 1) * scale


def draw_candidate_label(
    canvas: bytearray,
    canvas_width: int,
    canvas_height: int,
    cell_x: int,
    cell_y: int,
    index: int,
    cell_size: int,
) -> None:
    scale = max(1, min(3, cell_size // 24))
    label = f"{index:02d}"
    label_width = (len(label) * 3 + max(0, len(label) - 1)) * scale
    label_height = 5 * scale
    pad = max(1, scale)
    draw_rect(
        canvas,
        canvas_width,
        canvas_height,
        cell_x,
        cell_y,
        label_width + pad * 2,
        label_height + pad * 2,
        (0, 0, 0, 220),
    )
    draw_digit_text(
        canvas,
        canvas_width,
        canvas_height,
        label,
        cell_x + pad,
        cell_y + pad,
        scale,
        (255, 255, 255, 255),
    )


def png_to_rgba(path: pathlib.Path) -> tuple[dict[str, Any], bytes] | None:
    decoded = decode_png_scanlines(path)
    if decoded is None:
        return None
    ihdr, pixels = decoded
    if ihdr["color_type"] == 6:
        return ihdr, pixels
    if ihdr["color_type"] == 2:
        rgba = bytearray()
        for idx in range(0, len(pixels), 3):
            rgba.extend(pixels[idx : idx + 3] + b"\xff")
        return ihdr, bytes(rgba)
    return None


def write_contact_sheet_index(asset_root: pathlib.Path, output_path: pathlib.Path, candidates: list[pathlib.Path]) -> pathlib.Path:
    output_path = pathlib.Path(output_path)
    index_path = output_path.with_name(f"{output_path.stem}-index.json")
    rows: list[dict[str, Any]] = []
    for index, path in enumerate(candidates, start=1):
        row: dict[str, Any] = {
            "index": index,
            "label": f"{index:02d}",
            "path": str(path),
        }
        try:
            row["relative_path"] = str(path.relative_to(asset_root))
        except ValueError:
            row["relative_path"] = path.name
        rows.append(row)
    write_json(
        index_path,
        {
            "contact_sheet": str(output_path),
            "asset_root": str(asset_root),
            "candidate_count": len(candidates),
            "candidates": rows,
        },
    )
    return index_path


def write_contact_sheet_png(asset_root: pathlib.Path, output_path: pathlib.Path, cell_size: int = 128) -> pathlib.Path:
    asset_root = pathlib.Path(asset_root)
    output_path = pathlib.Path(output_path)
    images = iter_image_files(asset_root)
    pngs = [path for path in images if path.suffix.lower() == ".png" and path.name != pathlib.Path(output_path).name]
    if not pngs:
        write_rgba_png(output_path, cell_size, cell_size, bytes([0, 0, 0, 0]) * cell_size * cell_size)
        write_contact_sheet_index(asset_root, output_path, [])
        return output_path
    cols = max(1, int(len(pngs) ** 0.5 + 0.999))
    rows = (len(pngs) + cols - 1) // cols
    width = cols * cell_size
    height = rows * cell_size
    canvas = bytearray(bytes([0, 0, 0, 0]) * width * height)

    for index, image in enumerate(pngs):
        decoded = png_to_rgba(image)
        if decoded is None:
            continue
        ihdr, pixels = decoded
        source_w = ihdr["width"]
        source_h = ihdr["height"]
        scale = max(1, min(cell_size // max(source_w, 1), cell_size // max(source_h, 1)))
        draw_w = min(cell_size, source_w * scale)
        draw_h = min(cell_size, source_h * scale)
        offset_x = (index % cols) * cell_size + (cell_size - draw_w) // 2
        offset_y = (index // cols) * cell_size + (cell_size - draw_h) // 2
        for y in range(draw_h):
            src_y = y // scale
            for x in range(draw_w):
                src_x = x // scale
                src_idx = (src_y * source_w + src_x) * 4
                dst_idx = ((offset_y + y) * width + offset_x + x) * 4
                canvas[dst_idx : dst_idx + 4] = pixels[src_idx : src_idx + 4]
        draw_candidate_label(
            canvas,
            width,
            height,
            (index % cols) * cell_size,
            (index // cols) * cell_size,
            index + 1,
            cell_size,
        )

    write_contact_sheet_index(asset_root, output_path, pngs)
    return write_rgba_png(output_path, width, height, bytes(canvas))


def inspect_assets(
    asset_root: pathlib.Path,
    expected_size: tuple[int, int] | None = None,
    require_nonblank: bool = False,
) -> dict[str, Any]:
    asset_root = pathlib.Path(asset_root)
    images = [path for path in iter_image_files(asset_root) if path.name not in REVIEW_ARTIFACT_NAMES]
    issues: list[str] = []
    for image in images:
        rel = image.relative_to(asset_root)
        size = read_png_size(image) if image.suffix.lower() == ".png" else None
        if expected_size and size != expected_size:
            issues.append(f"{rel}: expected size {expected_size}, got {size}")
        if require_nonblank and image.suffix.lower() == ".png" and png_is_fully_transparent(image):
            issues.append(f"{rel}: blank or fully transparent image")
    if not images:
        issues.append("no image files found")
    return {
        "ok": not issues,
        "asset_root": str(asset_root),
        "image_count": len(images),
        "expected_size": list(expected_size) if expected_size else None,
        "issues": issues,
    }


def summarize_costs(manifest: dict[str, Any], output_path: pathlib.Path | None = None) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    total = 0.0
    total_candidates = 0
    for operation in manifest.get("operations", []):
        result_file = operation.get("result_file")
        if not result_file:
            continue
        path = pathlib.Path(result_file)
        if not path.exists():
            continue
        data = read_json(path)
        cost = float(data.get("usage_cost_usd") or 0)
        candidates = int(data.get("candidate_count") or 0)
        row = {
            "id": operation.get("id"),
            "endpoint": operation.get("endpoint"),
            "result_file": str(path),
            "usage_cost_usd": cost,
            "candidate_count": candidates,
        }
        rows.append(row)
        total += cost
        total_candidates += candidates
    summary = {
        "operation_count": len(rows),
        "total_usage_cost_usd": round(total, 6),
        "total_candidates": total_candidates,
        "rows": rows,
    }
    if output_path:
        write_json(pathlib.Path(output_path), summary)
    return summary


def append_jsonl(path: pathlib.Path | None, event: dict[str, Any]) -> None:
    if not path:
        return
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"), **event}, ensure_ascii=True) + "\n")


def approve_candidate(operation: dict[str, Any], index: int, progress_jsonl: pathlib.Path | None = None) -> dict[str, Any]:
    candidate_root = pathlib.Path(operation["download_dir"])
    approved_dir = pathlib.Path(operation["approved_dir"])
    op_id = slugify(str(operation.get("id") or "asset"), fallback="asset")
    patterns = [
        f"*-candidate-{index:02d}.*",
        f"*candidate-{index:02d}.*",
        f"*-{index:02d}.*",
    ]
    matches: list[pathlib.Path] = []
    for pattern in patterns:
        matches.extend(sorted(candidate_root.glob(pattern)))
        if matches:
            break
    if not matches:
        return {"ok": False, "operation_id": op_id, "error": f"candidate index {index} not found in {candidate_root}"}
    source = matches[0]
    approved_dir.mkdir(parents=True, exist_ok=True)
    destination = approved_dir / f"{op_id}{source.suffix.lower()}"
    shutil.copy2(source, destination)
    report = {
        "ok": True,
        "operation_id": op_id,
        "selected_index": index,
        "source_file": str(source),
        "approved_file": str(destination),
    }
    append_jsonl(progress_jsonl, {"event": "approved", **report})
    return report


def balance_preflight_command(output_dir: pathlib.Path) -> list[str]:
    output_dir = pathlib.Path(output_dir)
    return [
        "python3",
        str(CLIENT_PATH),
        "get",
        "/v2/balance",
        "--quiet",
        "--result-file",
        str(output_dir / "results" / "balance" / "result.json"),
    ]


def refresh_api_metadata(output_root: pathlib.Path, fetcher: Any | None = None) -> dict[str, Any]:
    output_root = pathlib.Path(output_root)
    api_dir = output_root / "api"
    api_dir.mkdir(parents=True, exist_ok=True)
    fetch = fetcher or fetch_json_url
    report: dict[str, Any] = {}

    for version in ("v1", "v2"):
        url = f"https://api.pixellab.ai/{version}/openapi.json"
        spec = fetch(url)
        write_json(api_dir / f"{version}-openapi.json", spec)
        paths = spec.get("paths", {}) if isinstance(spec, dict) else {}
        report[version] = {
            "openapi": str(api_dir / f"{version}-openapi.json"),
            "path_count": len(paths),
            "paths": sorted(paths.keys()),
        }

    llms_url = "https://api.pixellab.ai/v2/llms.txt"
    try:
        if fetcher:
            llms_text = fetcher(llms_url)
        else:
            llms_text = fetch_text_url(llms_url)
        if not isinstance(llms_text, str):
            llms_text = json.dumps(llms_text, indent=2, ensure_ascii=True)
        (api_dir / "v2-llms.txt").write_text(llms_text, encoding="utf-8")
        report["v2"]["llms_txt"] = str(api_dir / "v2-llms.txt")
    except Exception as err:
        report["v2"]["llms_txt_error"] = str(err)

    write_json(api_dir / "metadata-report.json", report)
    return report


DOCTOR_ALLOWED_FILES = {
    "SKILL.md",
    "skill-card.md",
    "agents/openai.yaml",
    "config/openclaw.example.json",
    "config/openclaw.example.json5",
}
DOCTOR_ALLOWED_DIRS = {"examples", "recipes", "references", "scripts"}


def doctor_scope_issue(skill_dir: pathlib.Path) -> str | None:
    resolved = skill_dir.resolve()
    if resolved.name != "pixellab-ai":
        return "doctor must be pointed at a pixellab-ai skill package directory, not a broader project or personal directory"
    if not (resolved / "SKILL.md").is_file():
        return "doctor target is missing SKILL.md"
    try:
        skill_text = (resolved / "SKILL.md").read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return "doctor target SKILL.md is not UTF-8 text"
    if "name: pixellab-ai" not in skill_text:
        return "doctor target SKILL.md is not the pixellab-ai skill"
    if not (resolved / "scripts" / "pixellab_workflow.py").is_file():
        return "doctor target is missing scripts/pixellab_workflow.py"
    if not (resolved / "references" / "endpoint-mapping.md").is_file():
        return "doctor target is missing references/endpoint-mapping.md"
    return None


def iter_doctor_package_files(skill_dir: pathlib.Path) -> Iterable[pathlib.Path]:
    for rel in sorted(DOCTOR_ALLOWED_FILES):
        path = skill_dir / rel
        if path.is_file():
            yield path
    for dirname in sorted(DOCTOR_ALLOWED_DIRS):
        root = skill_dir / dirname
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*")):
            if path.is_file():
                yield path


def skill_doctor(skill_dir: pathlib.Path = SKILL_DIR) -> dict[str, Any]:
    skill_dir = pathlib.Path(skill_dir).resolve()
    issues: list[str] = []
    checks: list[dict[str, Any]] = []

    scope_issue = doctor_scope_issue(skill_dir)
    checks.append({"check": "doctor_scope", "path": str(skill_dir), "ok": scope_issue is None})
    if scope_issue:
        return {
            "ok": False,
            "skill_dir": str(skill_dir),
            "checks": checks,
            "issues": [scope_issue],
        }

    required_files = [
        "SKILL.md",
        "scripts/pixellab_client.py",
        "scripts/pixellab_workflow.py",
        "references/endpoint-mapping.md",
        "references/prompt-cheatsheet.md",
    ]
    for rel in required_files:
        exists = (skill_dir / rel).exists()
        checks.append({"check": "required_file", "path": rel, "ok": exists})
        if not exists:
            issues.append(f"missing required file: {rel}")

    recipe_dir = skill_dir / "recipes"
    recipe_count = 0
    for recipe_path in sorted(recipe_dir.glob("*.json")) if recipe_dir.exists() else []:
        recipe_count += 1
        try:
            validate_recipe(read_json(recipe_path))
        except Exception as err:
            issues.append(f"{recipe_path.relative_to(skill_dir)}: invalid recipe: {err}")
    checks.append({"check": "recipes_parse", "count": recipe_count, "ok": recipe_count > 0})
    if recipe_count == 0:
        issues.append("no recipes found")

    example_dir = skill_dir / "examples"
    example_count = 0
    for example_path in sorted(example_dir.glob("*.json")) if example_dir.exists() else []:
        example_count += 1
        try:
            read_json(example_path)
        except Exception as err:
            issues.append(f"{example_path.relative_to(skill_dir)}: invalid JSON example: {err}")
    checks.append({"check": "examples_parse", "count": example_count, "ok": example_count > 0})
    if example_count == 0:
        issues.append("no JSON examples found")

    pycache_dirs = [
        path
        for root_name in sorted(DOCTOR_ALLOWED_DIRS)
        for path in (skill_dir / root_name).rglob("__pycache__")
        if path.is_dir()
    ]
    checks.append({"check": "no_pycache", "count": len(pycache_dirs), "ok": not pycache_dirs})
    for path in pycache_dirs:
        issues.append(f"remove generated cache directory: {path.relative_to(skill_dir)}")

    secret_hits: list[str] = []
    allowed_secret_values = {"PASTE_YOUR_KEY_HERE", "YOUR_API_TOKEN", "YOUR_API_KEY", "..."}
    for path in iter_doctor_package_files(skill_dir):
        if not path.is_file() or path.suffix.lower() in IMAGE_EXTENSIONS:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for match in SECRET_ASSIGNMENT_RE.finditer(text):
            value = match.group(1).strip()
            if value and value not in allowed_secret_values and "PASTE" not in value and "YOUR_" not in value:
                secret_hits.append(f"{path.relative_to(skill_dir)}: PIXELLAB_API_KEY assignment")
    checks.append({"check": "no_packaged_api_key", "count": len(secret_hits), "ok": not secret_hits})
    issues.extend(secret_hits)

    return {
        "ok": not issues,
        "skill_dir": str(skill_dir),
        "checks": checks,
        "issues": issues,
    }


def write_subagent_brief(manifest_path: pathlib.Path, output_path: pathlib.Path | None = None) -> str:
    manifest = load_manifest(manifest_path)
    budget = estimate_budget(manifest)
    output_dir = manifest["output_dir"]
    references = manifest.get("references") or []
    reference_lines = "\n".join(f"- {item}" for item in references) if references else "- None listed; use endpoint mapping only if routing is unclear."
    seed_gate = json.dumps(manifest.get("seed_reference_gate") or {}, indent=2, ensure_ascii=True)
    text = f"""Run this PixelLab manifest in a worker subagent, not the main user session.

Rules:
- Do not paste base64, image JSON, or downloaded binary data into chat.
- Use quiet/summary output only.
- Return only manifest path, ledger path, candidate/approved paths, contact sheets, cost summary, failed ids, and short error messages.
- Load only the job-relevant references listed below. Do not load the full PixelLab skill corpus.
- Run only helper commands needed for this manifest; do not call unrelated PixelLab endpoints or examples.
- If any payload has REPLACE_WITH placeholders, stop and report placeholder paths.
- If seed_reference_gate.visual_brief_required is true, draft/update seed_reference_gate.visual_brief_path from the user's rough brief before paid generation. Fill normal gaps with explicit defaults and ask at most three identity-critical questions.
- If seed_reference_gate.decision_required_before_live is true, stop before paid generation after the visual brief is drafted, then ask the main session whether to use supplied seed/reference images, generate seed candidates for review, or proceed text-only.
- Save generated seed candidates only under seed_reference_gate.seed_candidate_dir using seed_reference_gate.seed_candidate_pattern; never send seed images through chat.
- Reruns skip completed result files by default. Do not pass --rerun-existing unless the user intentionally wants a new paid submission.
- If a job times out, resume with pixellab_client.py poll-result-file instead of submitting a new paid POST.

Job-relevant references:
{reference_lines}

Seed/reference gate:
{seed_gate}

Required preflight commands:
1. python3 pixellab-ai/scripts/pixellab_workflow.py budget --manifest {manifest_path}
2. python3 pixellab-ai/scripts/pixellab_workflow.py lint-manifest --manifest {manifest_path}
3. python3 pixellab-ai/scripts/pixellab_workflow.py repair-placeholders --manifest {manifest_path}
4. python3 pixellab-ai/scripts/pixellab_workflow.py balance-preflight --output-dir {output_dir}

Live execution command, only after seed/reference gate and placeholder checks are resolved:
5. python3 pixellab-ai/scripts/pixellab_workflow.py run --manifest {manifest_path} --yes --continue-on-error

Conditional review commands, only if matching files exist:
6. python3 pixellab-ai/scripts/pixellab_workflow.py gallery --asset-root {output_dir}/candidates
7. python3 pixellab-ai/scripts/pixellab_workflow.py cost-summary --manifest {manifest_path}
8. Review contact sheets, then run approve-candidate only for accepted operation indexes.
9. python3 pixellab-ai/scripts/pixellab_workflow.py inspect-assets --asset-root {output_dir}/approved --require-nonblank

Estimated budget units: {budget['estimated_budget_units']} across {budget['operation_count']} operations.
Estimated public-doc cost hint: ${budget['estimated_cost_usd']}.
"""
    if output_path:
        pathlib.Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(output_path).write_text(text, encoding="utf-8")
    return text


def validate_sprite_layers(
    root: pathlib.Path,
    layers: list[str],
    frame_glob: str = "*.png",
    expected_size: tuple[int, int] | None = None,
) -> dict[str, Any]:
    root = pathlib.Path(root)
    issues: list[str] = []
    layer_frames: dict[str, list[str]] = {}

    for layer in layers:
        files = sorted((root / layer).glob(frame_glob))
        names = [path.name for path in files]
        layer_frames[layer] = names
        if not files:
            issues.append(f"{layer}: no frames matched {frame_glob}")
        for path in files:
            size = read_png_size(path)
            if expected_size and size != expected_size:
                issues.append(f"{layer}/{path.name}: expected size {expected_size}, got {size}")

    if layers:
        reference_layer = layers[0]
        reference_names = set(layer_frames.get(reference_layer, []))
        for layer in layers[1:]:
            names = set(layer_frames.get(layer, []))
            for missing in sorted(reference_names - names):
                issues.append(f"{layer}: missing frame {missing}")
            for extra in sorted(names - reference_names):
                issues.append(f"{layer}: extra frame {extra}")
            if layer_frames.get(layer) and layer_frames[layer] != layer_frames.get(reference_layer, []):
                issues.append(f"{layer}: frame order differs from {reference_layer}")

    return {
        "ok": not issues,
        "root": str(root),
        "layers": layers,
        "frame_glob": frame_glob,
        "expected_size": list(expected_size) if expected_size else None,
        "frame_counts": {layer: len(names) for layer, names in layer_frames.items()},
        "issues": issues,
    }


def parse_size(raw: str) -> tuple[int, int]:
    match = re.fullmatch(r"(\d+)x(\d+)", raw.strip().lower())
    if not match:
        raise argparse.ArgumentTypeError("expected size like 64x64")
    return int(match.group(1)), int(match.group(2))


def list_recipes() -> list[str]:
    if not RECIPES_DIR.exists():
        return []
    return [path.stem for path in sorted(RECIPES_DIR.glob("*.json"))]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan and run guided PixelLab asset workflows.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list-recipes", help="List bundled recipe names.")

    plan = sub.add_parser("plan", help="Create a dry-run asset manifest and payload files.")
    plan.add_argument("--recipe", required=True, help="Bundled recipe name or recipe JSON path.")
    plan.add_argument("--brief", required=True, help="Asset pack brief.")
    plan.add_argument("--output-dir", required=True, help="Output folder for manifest, payloads, and eventual assets.")
    plan.add_argument("--manifest", help="Manifest output path. Defaults to OUTPUT_DIR/asset-manifest.json.")
    plan.add_argument("--project-slug", help="Stable folder/name slug. Defaults from brief.")
    plan.add_argument("--seed", type=int, default=0, help="Base seed. Use 0 for random where PixelLab supports it.")
    plan.add_argument("--var", action="append", default=[], help="Extra template variable as KEY=VALUE. VALUE may be JSON.")

    run = sub.add_parser("run", help="Run every operation in a manifest. Requires --yes.")
    run.add_argument("--manifest", required=True)
    run.add_argument("--yes", action="store_true", help="Required because this can spend PixelLab credits.")
    run.add_argument("--continue-on-error", action="store_true")
    run.add_argument("--max-budget-units", type=int, help="Block run if estimated budget units exceed this value.")
    run.add_argument("--rerun-existing", action="store_true", help="Force a fresh paid submission even if result files already exist.")

    budget = sub.add_parser("budget", help="Summarize operation count and conservative budget units.")
    budget.add_argument("--manifest", required=True)

    retry = sub.add_parser("retry-manifest", help="Create a manifest containing only failed operation ids from errors.json.")
    retry.add_argument("--manifest", required=True)
    retry.add_argument("--errors", required=True)
    retry.add_argument("--output", required=True)

    placeholders = sub.add_parser("repair-placeholders", help="Report unresolved payload placeholders before spending credits.")
    placeholders.add_argument("--manifest", required=True)
    placeholders.add_argument("--output")

    gallery = sub.add_parser("gallery", help="Create an HTML contact sheet for generated assets.")
    gallery.add_argument("--asset-root", required=True)
    gallery.add_argument("--output", help="Defaults to ASSET_ROOT/index.html")

    inspect = sub.add_parser("inspect-assets", help="Check generated images for size and blank transparent outputs.")
    inspect.add_argument("--asset-root", required=True)
    inspect.add_argument("--expected-size", type=parse_size)
    inspect.add_argument("--require-nonblank", action="store_true")
    inspect.add_argument("--output")

    validate = sub.add_parser("validate-sprites", help="Check layered sprite frame count, order, and PNG size.")
    validate.add_argument("--root", required=True)
    validate.add_argument("--layers", required=True, help="Comma-separated layer folders, reference layer first.")
    validate.add_argument("--frame-glob", default="*.png")
    validate.add_argument("--expected-size", type=parse_size)
    validate.add_argument("--output", help="Optional JSON report path.")

    lint = sub.add_parser("lint-manifest", help="Check endpoint routing, candidate policy, and known payload size limits.")
    lint.add_argument("--manifest", required=True)
    lint.add_argument("--output")

    contact = sub.add_parser("contact-sheet", help="Create a PNG contact sheet for candidate images.")
    contact.add_argument("--asset-root", required=True)
    contact.add_argument("--output", help="Defaults to ASSET_ROOT/contact-sheet.png")
    contact.add_argument("--cell-size", type=int, default=128)

    costs = sub.add_parser("cost-summary", help="Roll up usage_cost_usd and candidate counts from result files.")
    costs.add_argument("--manifest", required=True)
    costs.add_argument("--output")

    approve = sub.add_parser("approve-candidate", help="Copy one candidate image into approved/ by operation id and candidate index.")
    approve.add_argument("--manifest", required=True)
    approve.add_argument("--operation-id", required=True)
    approve.add_argument("--index", type=int, required=True)
    approve.add_argument("--output")

    balance = sub.add_parser("balance-preflight", help="Print the GET /v2/balance helper command for a run folder.")
    balance.add_argument("--output-dir", required=True)

    refresh = sub.add_parser("refresh-api-metadata", help="Fetch public v1/v2 OpenAPI metadata and v2 llms.txt into OUTPUT_DIR/api.")
    refresh.add_argument("--output-dir", required=True)

    doctor = sub.add_parser("doctor", help="Check the local skill package without calling PixelLab.")
    doctor.add_argument("--skill-dir", default=str(SKILL_DIR))
    doctor.add_argument("--output")

    subagent = sub.add_parser("subagent-brief", help="Write a worker-subagent brief for low-token live API execution.")
    subagent.add_argument("--manifest", required=True)
    subagent.add_argument("--output")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "list-recipes":
            for name in list_recipes():
                print(name)
            return 0

        if args.command == "plan":
            extra_context = dict(parse_key_value(item) for item in args.var)
            recipe = load_recipe(args.recipe)
            output_dir = pathlib.Path(args.output_dir)
            manifest = build_manifest(
                recipe,
                brief=args.brief,
                output_dir=output_dir,
                project_slug=args.project_slug,
                seed=args.seed,
                extra_context=extra_context,
            )
            manifest_path = pathlib.Path(args.manifest) if args.manifest else output_dir / "asset-manifest.json"
            write_manifest(manifest, manifest_path)
            print(json.dumps({"manifest": str(manifest_path), "operations": len(manifest["operations"])}, indent=2))
            return 0

        if args.command == "run":
            report = run_manifest(
                pathlib.Path(args.manifest),
                yes=args.yes,
                continue_on_error=args.continue_on_error,
                max_budget_units=args.max_budget_units,
                rerun_existing=args.rerun_existing,
            )
            print(json.dumps(report, indent=2))
            return 0 if report["ok"] else 1

        if args.command == "budget":
            print(json.dumps(estimate_budget(load_manifest(pathlib.Path(args.manifest))), indent=2))
            return 0

        if args.command == "retry-manifest":
            print(write_retry_manifest(pathlib.Path(args.manifest), pathlib.Path(args.errors), pathlib.Path(args.output)))
            return 0

        if args.command == "repair-placeholders":
            report = placeholder_report(load_manifest(pathlib.Path(args.manifest)))
            rendered = json.dumps(report, indent=2, ensure_ascii=True)
            print(rendered)
            if args.output:
                pathlib.Path(args.output).parent.mkdir(parents=True, exist_ok=True)
                pathlib.Path(args.output).write_text(rendered + "\n", encoding="utf-8")
            return 0 if report["ok"] else 1

        if args.command == "gallery":
            asset_root = pathlib.Path(args.asset_root)
            output = pathlib.Path(args.output) if args.output else asset_root / "index.html"
            print(write_gallery(asset_root, output))
            return 0

        if args.command == "inspect-assets":
            report = inspect_assets(
                pathlib.Path(args.asset_root),
                expected_size=args.expected_size,
                require_nonblank=args.require_nonblank,
            )
            rendered = json.dumps(report, indent=2, ensure_ascii=True)
            print(rendered)
            if args.output:
                pathlib.Path(args.output).parent.mkdir(parents=True, exist_ok=True)
                pathlib.Path(args.output).write_text(rendered + "\n", encoding="utf-8")
            return 0 if report["ok"] else 1

        if args.command == "validate-sprites":
            layers = [part.strip() for part in args.layers.split(",") if part.strip()]
            report = validate_sprite_layers(
                root=pathlib.Path(args.root),
                layers=layers,
                frame_glob=args.frame_glob,
                expected_size=args.expected_size,
            )
            rendered = json.dumps(report, indent=2, ensure_ascii=True)
            print(rendered)
            if args.output:
                pathlib.Path(args.output).parent.mkdir(parents=True, exist_ok=True)
                pathlib.Path(args.output).write_text(rendered + "\n", encoding="utf-8")
            return 0 if report["ok"] else 1

        if args.command == "lint-manifest":
            report = lint_manifest(load_manifest(pathlib.Path(args.manifest)))
            rendered = json.dumps(report, indent=2, ensure_ascii=True)
            print(rendered)
            if args.output:
                pathlib.Path(args.output).parent.mkdir(parents=True, exist_ok=True)
                pathlib.Path(args.output).write_text(rendered + "\n", encoding="utf-8")
            return 0 if report["ok"] else 1

        if args.command == "contact-sheet":
            asset_root = pathlib.Path(args.asset_root)
            output = pathlib.Path(args.output) if args.output else asset_root / "contact-sheet.png"
            print(write_contact_sheet_png(asset_root, output, cell_size=args.cell_size))
            return 0

        if args.command == "cost-summary":
            manifest = load_manifest(pathlib.Path(args.manifest))
            output = pathlib.Path(args.output) if args.output else pathlib.Path(manifest["output_dir"]) / "reports" / "cost-summary.json"
            print(json.dumps(summarize_costs(manifest, output), indent=2, ensure_ascii=True))
            return 0

        if args.command == "approve-candidate":
            manifest = load_manifest(pathlib.Path(args.manifest))
            matches = [operation for operation in manifest["operations"] if operation.get("id") == args.operation_id]
            if not matches:
                raise ValueError(f"operation id not found: {args.operation_id}")
            report = approve_candidate(matches[0], args.index, pathlib.Path(manifest.get("progress_jsonl")) if manifest.get("progress_jsonl") else None)
            rendered = json.dumps(report, indent=2, ensure_ascii=True)
            print(rendered)
            if args.output:
                pathlib.Path(args.output).parent.mkdir(parents=True, exist_ok=True)
                pathlib.Path(args.output).write_text(rendered + "\n", encoding="utf-8")
            return 0 if report["ok"] else 1

        if args.command == "balance-preflight":
            print(" ".join(balance_preflight_command(pathlib.Path(args.output_dir))))
            return 0

        if args.command == "refresh-api-metadata":
            print(json.dumps(refresh_api_metadata(pathlib.Path(args.output_dir)), indent=2, ensure_ascii=True))
            return 0

        if args.command == "doctor":
            report = skill_doctor(pathlib.Path(args.skill_dir))
            rendered = json.dumps(report, indent=2, ensure_ascii=True)
            print(rendered)
            if args.output:
                pathlib.Path(args.output).parent.mkdir(parents=True, exist_ok=True)
                pathlib.Path(args.output).write_text(rendered + "\n", encoding="utf-8")
            return 0 if report["ok"] else 1

        if args.command == "subagent-brief":
            print(write_subagent_brief(pathlib.Path(args.manifest), pathlib.Path(args.output) if args.output else None))
            return 0

        raise ValueError(f"unknown command: {args.command}")
    except Exception as err:
        eprint(f"[error] {err}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
