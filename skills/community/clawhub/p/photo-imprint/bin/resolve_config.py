#!/usr/bin/env python3
"""Resolve and validate a photo-to-illustration carousel preset."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from PIL import Image

CONCERNS = ("theme", "style", "layers", "composition", "unification")
PROFILE_DIRS = {
    "theme": "themes",
    "style": "styles",
    "layers": "layers",
    "composition": "compositions",
    "unification": "unification",
}
KNOWN_MODULES = {"caption", "route", "watermark", "disclosure", "numbering"}
MAX_REFERENCE_LONG_EDGE = 1600
MAX_REFERENCE_BYTES = 750 * 1024
REQUIRED_REFERENCE_SOURCE_FIELDS = {
    "title", "creator", "institution", "item_record_url", "official_image_url",
    "object_number", "medium", "date", "rights_status", "rights_statement",
    "license_url", "retrieval_date", "redistributable", "bundled", "derivative",
}
FORBIDDEN_REFERENCE_METADATA = {"exif", "gps", "xmp", "xml:com.adobe.xmp"}


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"top level must be an object: {path}")
    return data


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def validate_reference_metadata(
    reference: dict[str, Any], source: dict[str, Any], source_path: Path
) -> list[str]:
    """Validate provenance, technique isolation, and derivative integrity metadata."""
    errors: list[str] = []
    missing = sorted(REQUIRED_REFERENCE_SOURCE_FIELDS - set(source))
    if missing:
        errors.append(f"{source_path}: missing keys: {', '.join(missing)}")
    if source.get("redistributable") is True:
        for key in ("license_url", "item_record_url", "official_image_url", "rights_statement"):
            if not isinstance(source.get(key), str) or not source[key].strip():
                errors.append(f"{source_path}: redistributable reference requires non-empty {key}")
    roles = reference.get("technique_roles")
    exclusions = reference.get("subject_exclusions")
    if not isinstance(exclusions, list) or not exclusions or not all(
        isinstance(value, str) and value.strip() for value in exclusions
    ):
        errors.append(f"{source_path}: active reference requires subject_exclusions")
    if source.get("technique_roles") != roles:
        errors.append(f"{source_path}: technique_roles must match the style profile")
    if source.get("subject_exclusions") != exclusions:
        errors.append(f"{source_path}: subject_exclusions must match the style profile")
    derivative = source.get("derivative")
    required_derivative = {
        "file", "format", "width", "height", "long_edge_px", "bytes", "sha256",
        "settings", "metadata_stripped",
    }
    if not isinstance(derivative, dict):
        errors.append(f"{source_path}: derivative must be an object")
    else:
        missing_derivative = sorted(required_derivative - set(derivative))
        if missing_derivative:
            errors.append(f"{source_path}: derivative missing keys: {', '.join(missing_derivative)}")
        stripped = derivative.get("metadata_stripped")
        if not isinstance(stripped, list) or not {"EXIF", "GPS", "XMP"}.issubset(set(stripped)):
            errors.append(f"{source_path}: derivative must record EXIF/GPS/XMP stripping")
    return errors


def validate_reference_asset(ref_path: Path, source: dict[str, Any], source_path: Path) -> list[str]:
    """Validate optimized bytes against their declared derivative record."""
    errors: list[str] = []
    derivative = source.get("derivative")
    if not ref_path.is_file() or not isinstance(derivative, dict):
        return errors
    try:
        size_bytes = ref_path.stat().st_size
        sha256 = hashlib.sha256(ref_path.read_bytes()).hexdigest()
        with Image.open(ref_path) as image:
            image.load()
            width, height = image.size
            image_format = image.format
            info_keys = {str(key).lower() for key in image.info}
            forbidden = sorted(
                key for key in info_keys
                if key in FORBIDDEN_REFERENCE_METADATA or "xmp" in key
            )
            if image.getexif():
                forbidden.append("exif")
        if max(width, height) > MAX_REFERENCE_LONG_EDGE:
            errors.append(f"{ref_path}: long edge {max(width, height)}px exceeds {MAX_REFERENCE_LONG_EDGE}px")
        if size_bytes > MAX_REFERENCE_BYTES:
            errors.append(f"{ref_path}: {size_bytes} bytes exceeds {MAX_REFERENCE_BYTES}")
        if forbidden:
            errors.append(f"{ref_path}: forbidden metadata present: {', '.join(sorted(set(forbidden)))}")
        expected = {
            "file": ref_path.name, "format": image_format, "width": width, "height": height,
            "long_edge_px": max(width, height), "bytes": size_bytes, "sha256": sha256,
        }
        for key, actual in expected.items():
            if derivative.get(key) != actual:
                errors.append(f"{source_path}: derivative.{key} does not match {ref_path}")
    except Exception as exc:
        errors.append(f"{ref_path}: unreadable image: {exc}")
    return errors


def resolve_preset(
    skill_root: Path,
    preset_path: Path,
    *,
    allow_missing_unbundled_reference: bool = False,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    preset = load_json(preset_path)
    if not preset.get("preset"):
        errors.append("preset is missing a non-empty 'preset' id")
    profile_ids = preset.get("profiles")
    if not isinstance(profile_ids, dict):
        errors.append("preset.profiles must be an object")
        profile_ids = {}

    overrides = preset.get("overrides", {})
    if not isinstance(overrides, dict):
        errors.append("preset.overrides must be an object")
        overrides = {}

    resolved_profiles: dict[str, Any] = {}
    sources: dict[str, str] = {}
    for concern in CONCERNS:
        profile_id = profile_ids.get(concern)
        if not isinstance(profile_id, str) or not profile_id:
            errors.append(f"preset.profiles.{concern} must name a profile")
            continue
        profile_path = skill_root / "profiles" / PROFILE_DIRS[concern] / f"{profile_id}.json"
        try:
            profile = load_json(profile_path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if profile.get("profile_type") != concern:
            errors.append(f"{profile_path}: profile_type must be '{concern}'")
        if profile.get("id") != profile_id:
            errors.append(f"{profile_path}: id must be '{profile_id}'")
        concern_override = overrides.get(concern, {})
        if not isinstance(concern_override, dict):
            errors.append(f"overrides.{concern} must be an object")
            concern_override = {}
        resolved_profiles[concern] = deep_merge(profile, concern_override)
        sources[concern] = str(profile_path.relative_to(skill_root))

    unknown_overrides = set(overrides) - set(CONCERNS)
    if unknown_overrides:
        errors.append("unknown override concerns: " + ", ".join(sorted(unknown_overrides)))

    modules = preset.get("modules", {})
    if not isinstance(modules, dict):
        errors.append("preset.modules must be an object")
        modules = {}
    unknown_modules = set(modules) - KNOWN_MODULES
    if unknown_modules:
        errors.append("unknown modules: " + ", ".join(sorted(unknown_modules)))

    composition = resolved_profiles.get("composition", {})
    canvas = composition.get("canvas", {}) if isinstance(composition, dict) else {}
    width, height = canvas.get("width"), canvas.get("height")
    ratio = canvas.get("aspect_ratio")
    if not all(isinstance(v, int) and v > 0 for v in (width, height)):
        errors.append("composition.canvas width and height must be positive integers")
    elif ratio == "9:16" and width * 16 != height * 9:
        errors.append("composition canvas dimensions do not match 9:16")

    style = resolved_profiles.get("style", {})
    if isinstance(style, dict):
        references = style.get("references")
        if references == [] and style.get("reference_status") == "pending-selection":
            warnings.append("active style has no approved references; rendering will use text rules only")
        elif not isinstance(references, list) or not references:
            errors.append("style requires a non-empty references array, or reference_status 'pending-selection'")
        else:
            seen_ids: set[str] = set()
            for index, reference in enumerate(references, start=1):
                if not isinstance(reference, dict):
                    errors.append(f"style reference {index} must be an object")
                    continue
                reference_id = reference.get("id")
                ref_rel = reference.get("image")
                source_rel = reference.get("source_metadata")
                roles = reference.get("technique_roles")
                if not isinstance(reference_id, str) or not reference_id:
                    errors.append(f"style reference {index} requires id")
                elif reference_id in seen_ids:
                    errors.append(f"duplicate style reference id: {reference_id}")
                else:
                    seen_ids.add(reference_id)
                if not isinstance(ref_rel, str) or not isinstance(source_rel, str):
                    errors.append(f"style reference {reference_id or index} requires image and source_metadata paths")
                    continue
                if not isinstance(roles, list) or not roles or not all(isinstance(role, str) and role for role in roles):
                    errors.append(f"style reference {reference_id or index} requires technique_roles")

                ref_path = skill_root / ref_rel
                source_path = skill_root / source_rel
                source: dict[str, Any] | None = None
                try:
                    source = load_json(source_path)
                    errors.extend(validate_reference_metadata(reference, source, source_path))
                    if source.get("redistributable") is not True:
                        warnings.append(f"active style reference is private/non-redistributable: {reference_id}")
                except ValueError as exc:
                    errors.append(str(exc))

                if not ref_path.is_file():
                    is_unbundled = bool(source and source.get("bundled") is False)
                    if allow_missing_unbundled_reference and is_unbundled:
                        warnings.append(f"style reference is not bundled: {ref_rel}")
                    else:
                        errors.append(f"missing style reference: {ref_path}")
                elif source is not None:
                    errors.extend(validate_reference_asset(ref_path, source, source_path))

    if errors:
        raise ValueError("\n".join(errors))

    workflow_defaults = preset.get("workflow_defaults", {})
    if not isinstance(workflow_defaults, dict):
        raise ValueError("preset.workflow_defaults must be an object")

    resolved = {
        "schema_version": "1.1.0",
        "resolved": True,
        "preset": preset["preset"],
        "preset_version": preset.get("version"),
        "profile_sources": sources,
        "profiles": resolved_profiles,
        "modules": modules,
        "workflow_defaults": workflow_defaults,
        "export": preset.get("export", {}),
        "warnings": warnings,
    }
    return resolved, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preset", type=Path, default=Path("presets/travel-food-journal.json"), help="preset path — relative to skill-root if not absolute, or cwd if file exists there")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--skill-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    skill_root = args.skill_root.resolve()
    # intuitive: if relative path exists in cwd, use it; else resolve against skill-root
    if args.preset.is_absolute():
        preset_path = args.preset
    elif Path(args.preset).exists():
        preset_path = Path(args.preset).resolve()
    else:
        preset_path = (skill_root / args.preset).resolve()
    try:
        resolved, warnings = resolve_preset(skill_root, preset_path.resolve())
    except ValueError as exc:
        print(f"Configuration validation failed:\n{exc}", file=sys.stderr)
        return 2

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(resolved, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for warning in warnings:
        print(f"Warning: {warning}", file=sys.stderr)
    print(f"Resolved {resolved['preset']} to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
