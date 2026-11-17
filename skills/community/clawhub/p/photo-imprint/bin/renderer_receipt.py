#!/usr/bin/env python3
"""Create and validate hash-locked renderer receipts.

A local reference file is evidence of availability, not consent to transmit it.
External renderers therefore require an explicit, service-scoped authorization
record whenever style-reference hashes are included.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

SCHEMA = "1.0.0"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read renderer receipt {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("renderer receipt must be an object")
    return value


def parse_settings(raw: str) -> dict[str, Any]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"settings JSON is invalid: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("settings JSON must be an object")
    return value


def file_records(values: list[str] | None, label: str, required: bool) -> list[dict[str, Any]]:
    if required and not values:
        raise ValueError(f"at least one --{label} name=path entry is required")
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in values or []:
        if "=" not in raw:
            raise ValueError(f"--{label} must use name=path: {raw!r}")
        name, path_text = raw.split("=", 1)
        name, path = name.strip(), Path(path_text).expanduser()
        if not name or name in seen:
            raise ValueError(f"--{label} requires a unique non-empty name")
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"--{label} file is missing, non-regular, or symlinked: {path}")
        seen.add(name)
        records.append({
            "name": name,
            "path": str(path.resolve()),
            "sha256": digest(path),
            "bytes": path.stat().st_size,
        })
    return records


def command_not_configured(args: argparse.Namespace) -> int:
    write(args.output, {
        "schema_version": SCHEMA,
        "status": "renderer_not_configured",
        "renderer": None,
        "sources": [],
        "references": [],
        "rendered_outputs": [],
        "external_reference_processing": {
            "decision": "not_configured", "explicit": False, "service": None, "scope": None,
        },
    })
    print(f"Recorded explicit renderer-not-configured state in {args.output}")
    return 0


def command_register(args: argparse.Namespace) -> int:
    model, version = args.model.strip(), args.model_version.strip()
    if not model or not version:
        raise ValueError("model and model version must be non-empty")
    settings = parse_settings(args.settings_json)
    sources = file_records(args.source, "source", required=True)
    references = file_records(args.reference, "reference", required=False)
    outputs = file_records(args.rendered_output, "rendered-output", required=True)
    external_record: dict[str, Any]
    if args.renderer_kind == "external":
        service = (args.external_service or "").strip()
        if not service:
            raise ValueError("external renderer requires --external-service")
        if references:
            if args.external_reference_decision != "authorized":
                raise ValueError(
                    "external processing authorization is required for style references; "
                    "local file presence alone is not consent"
                )
            external_record = {
                "decision": "authorized",
                "explicit": True,
                "service": service,
                "scope": "style-reference-files-used-by-this-receipt",
            }
        else:
            external_record = {
                "decision": args.external_reference_decision or "not_applicable_no_references",
                "explicit": args.external_reference_decision is not None,
                "service": service,
                "scope": "style-reference-files-used-by-this-receipt" if args.external_reference_decision else None,
            }
    else:
        if args.external_service or args.external_reference_decision:
            raise ValueError("external service/authorization fields are invalid for a local renderer")
        external_record = {"decision": "not_applicable_local_renderer", "explicit": False, "service": None, "scope": None}
    receipt = {
        "schema_version": SCHEMA,
        "status": "rendered_output_registered",
        "renderer": {
            "kind": args.renderer_kind,
            "service": args.external_service.strip() if args.external_service else None,
            "model": model,
            "version": version,
            "seed": args.seed,
            "settings": settings,
        },
        "hash_algorithm": "sha256",
        "sources": sources,
        "references": references,
        "rendered_outputs": outputs,
        "external_reference_processing": external_record,
    }
    errors = validate(receipt, check_files=True, require_rendered_output=True)
    if errors:
        raise ValueError("; ".join(errors))
    write(args.output, receipt)
    print(f"Registered and validated renderer receipt at {args.output}")
    return 0


def validate_files(entries: object, label: str, required: bool) -> list[str]:
    errors: list[str] = []
    if not isinstance(entries, list):
        return [f"{label} must be an array"]
    if required and not entries:
        errors.append(f"{label} must contain at least one file")
    seen: set[str] = set()
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            errors.append(f"{label}[{index}] must be an object")
            continue
        name, path_text, expected = entry.get("name"), entry.get("path"), entry.get("sha256")
        if not isinstance(name, str) or not name or name in seen:
            errors.append(f"{label}[{index}] has an invalid or duplicate name")
        else:
            seen.add(name)
        if not isinstance(path_text, str) or not path_text:
            errors.append(f"{label}[{index}] path is missing")
            continue
        path = Path(path_text)
        if not path.is_file() or path.is_symlink():
            errors.append(f"{label}[{index}] file is missing, non-regular, or symlinked")
            continue
        if not isinstance(expected, str) or len(expected) != 64:
            errors.append(f"{label}[{index}] sha256 is invalid")
        elif digest(path) != expected:
            errors.append(f"{label}[{index}] hash mismatch")
        size = entry.get("bytes")
        if not isinstance(size, int) or size < 0 or path.stat().st_size != size:
            errors.append(f"{label}[{index}] byte count mismatch")
    return errors


def validate(receipt: dict[str, Any], check_files: bool, require_rendered_output: bool) -> list[str]:
    errors: list[str] = []
    if receipt.get("schema_version") != SCHEMA:
        errors.append(f"schema_version must be {SCHEMA}")
    status = receipt.get("status")
    outputs = receipt.get("rendered_outputs")
    if status == "renderer_not_configured":
        if receipt.get("renderer") is not None:
            errors.append("renderer-not-configured receipt cannot contain renderer details")
        if outputs != []:
            errors.append("renderer-not-configured receipt cannot claim rendered output")
        if receipt.get("sources") != [] or receipt.get("references") != []:
            errors.append("renderer-not-configured receipt cannot contain input hashes")
        if require_rendered_output:
            errors.append("renderer is not configured; rendered output cannot be claimed")
        return errors
    if status != "rendered_output_registered":
        errors.append("unknown receipt status")
        return errors
    renderer = receipt.get("renderer")
    if not isinstance(renderer, dict):
        errors.append("renderer details are required")
        return errors
    if renderer.get("kind") not in {"local", "external"}:
        errors.append("renderer.kind must be local or external")
    for field in ("model", "version", "seed"):
        if not isinstance(renderer.get(field), str) or not renderer[field].strip():
            errors.append(f"renderer.{field} must be non-empty")
    if not isinstance(renderer.get("settings"), dict):
        errors.append("renderer.settings must be an object")
    if receipt.get("hash_algorithm") != "sha256":
        errors.append("hash_algorithm must be sha256")
    if check_files:
        errors.extend(validate_files(receipt.get("sources"), "sources", required=True))
        errors.extend(validate_files(receipt.get("references"), "references", required=False))
        errors.extend(validate_files(outputs, "rendered_outputs", required=True))
    elif require_rendered_output and (not isinstance(outputs, list) or not outputs):
        errors.append("rendered_outputs must contain at least one file")
    references = receipt.get("references")
    external = receipt.get("external_reference_processing")
    if renderer.get("kind") == "external":
        service = renderer.get("service")
        if not isinstance(service, str) or not service.strip():
            errors.append("external renderer requires a service")
        if isinstance(references, list) and references:
            if not isinstance(external, dict):
                errors.append("external style-reference processing authorization is missing")
            else:
                if external.get("decision") != "authorized" or external.get("explicit") is not True:
                    errors.append("external style-reference processing must be explicitly authorized")
                if external.get("service") != service:
                    errors.append("external style-reference authorization is not scoped to the renderer service")
                if external.get("scope") != "style-reference-files-used-by-this-receipt":
                    errors.append("external style-reference authorization scope is invalid")
    return errors


def command_validate(args: argparse.Namespace) -> int:
    receipt = load(args.receipt)
    errors = validate(receipt, check_files=True, require_rendered_output=args.require_rendered_output)
    if errors:
        raise ValueError("; ".join(errors))
    print(f"Renderer receipt valid: {args.receipt}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Record or validate renderer identity, settings, authorization, and file hashes")
    sub = parser.add_subparsers(dest="command", required=True)
    missing = sub.add_parser("not-configured")
    missing.add_argument("--output", required=True, type=Path)
    missing.set_defaults(handler=command_not_configured)
    register = sub.add_parser("register")
    register.add_argument("--output", required=True, type=Path)
    register.add_argument("--renderer-kind", required=True, choices=("local", "external"))
    register.add_argument("--external-service", help="tool name, e.g. imagegen — required when renderer-kind=external")
    register.add_argument("--external-reference-decision", choices=("authorized", "denied"))
    register.add_argument("--model", required=True, help="model id or 'unspecified-by-tool' for black-box tools")
    register.add_argument("--model-version", required=True, help="version or 'unspecified-by-tool'")
    register.add_argument("--seed", required=True)
    register.add_argument("--settings-json", required=True)
    register.add_argument("--source", action="append", help="Repeat name=path")
    register.add_argument("--reference", action="append", help="Repeat name=path")
    register.add_argument("--rendered-output", action="append", help="Repeat name=path")
    register.set_defaults(handler=command_register)
    check = sub.add_parser("validate")
    check.add_argument("--receipt", required=True, type=Path)
    check.add_argument("--require-rendered-output", action="store_true")
    check.set_defaults(handler=command_validate)
    args = parser.parse_args()
    try:
        return args.handler(args)
    except (ValueError, OSError) as exc:
        print(f"Renderer receipt blocked: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
