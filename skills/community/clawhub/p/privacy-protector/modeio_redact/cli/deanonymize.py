#!/usr/bin/env python3
"""
Modeio local de-anonymization script.

Restores placeholders back to original values using local map files.
No network call is performed.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from modeio_redact.core.models import MapRecord, MappingEntry
from modeio_redact.core.replacement import apply_text_replacements
from modeio_redact.workflow.file_handlers import (
    uses_text_handler,
    validate_non_text_output_extension,
    write_non_text_deanonymized_file,
)
from modeio_redact.workflow.file_workflow import (
    resolve_output_path,
    strip_embedded_map_marker,
    write_output_file,
)
from modeio_redact.workflow.file_types import (
    deanonymize_supported_extensions_for_display,
    supports_deanonymize_for_extension,
)
from modeio_redact.workflow.input_source import (
    SUPPORTED_FILE_EXTENSIONS,
    resolve_input_source_context,
)
from modeio_redact.workflow.map_linkage import resolve_map_reference
from modeio_redact.workflow.map_store import MapStoreError, hash_text, load_map

TOOL_NAME = "privacy-protector"


def _success_envelope(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "success": True,
        "tool": TOOL_NAME,
        "mode": "local-map",
        "data": data,
    }


def _error_envelope(error_type: str, message: str, details: Dict[str, Any] = None) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "success": False,
        "tool": TOOL_NAME,
        "mode": "local-map",
        "error": {
            "type": error_type,
            "message": message,
        },
    }
    if details is not None:
        payload["error"]["details"] = details
    return payload


def _emit_error_and_exit(
    *,
    json_mode: bool,
    error_type: str,
    message: str,
    exit_code: int,
    details: Dict[str, Any] = None,
) -> None:
    if json_mode:
        print(json.dumps(_error_envelope(error_type, message, details), ensure_ascii=False))
    else:
        print(f"Error: {message}", file=sys.stderr)
    sys.exit(exit_code)


def _deanonymize_with_record(
    raw_input: str,
    map_ref: str = None,
    linkage_source: str = "explicit-map",
) -> Tuple[Dict[str, Any], MapRecord]:
    record, path = load_map(map_ref)

    replacement_result = apply_text_replacements(
        text=raw_input,
        entries=record.entries,
        direction="restore",
    )

    warnings: List[Dict[str, str]] = []
    if record.anonymized_hash and record.anonymized_hash != hash_text(raw_input):
        warnings.append(
            {
                "code": "input_hash_mismatch",
                "message": "input content hash does not match map anonymizedHash; replacements applied",
            }
        )

    payload: Dict[str, Any] = {
        "deanonymizedContent": replacement_result.content,
        "replacementSummary": {
            "totalReplacements": replacement_result.total_replacements,
            "replacementsByType": replacement_result.replacements_by_type,
        },
        "mapRef": record.to_ref(str(path)).to_dict(),
        "linkageSource": linkage_source,
        "warnings": warnings,
    }
    return payload, record


def deanonymize(
    raw_input: str,
    map_ref: str = None,
    linkage_source: str = "explicit-map",
) -> Dict[str, Any]:
    payload, _ = _deanonymize_with_record(
        raw_input=raw_input,
        map_ref=map_ref,
        linkage_source=linkage_source,
    )
    return payload


def _persist_output_file(
    content: str,
    input_path: Optional[str],
    input_extension: Optional[str],
    output_arg: Optional[str],
    in_place: bool,
    output_tag: str,
    mapping_entries: List[MappingEntry],
) -> Optional[str]:
    resolved_output_path = resolve_output_path(
        input_path=input_path,
        output_path=output_arg,
        in_place=in_place,
        output_tag=output_tag,
    )
    if resolved_output_path is None:
        return None

    if input_path and input_extension and not uses_text_handler(input_extension):
        validate_non_text_output_extension(input_extension, resolved_output_path)
        write_non_text_deanonymized_file(
            input_path=Path(input_path).expanduser(),
            output_path=resolved_output_path,
            extension=input_extension,
            mapping_entries=mapping_entries,
        )
    else:
        write_output_file(resolved_output_path, content)
    return str(resolved_output_path)


def main() -> None:
    supported = ", ".join(SUPPORTED_FILE_EXTENSIONS)
    deanonymize_supported = deanonymize_supported_extensions_for_display()
    parser = argparse.ArgumentParser(
        description=(
            "Restore placeholders with local map file. "
            f"--input accepts literal text or supported file paths ({supported}). "
            f"De-anonymization file support: {deanonymize_supported}. "
            "Defaults to latest map in local store."
        )
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help=(
            f"Anonymized content to restore, or a supported file path ({supported}). "
            f"De-anonymization file support: {deanonymize_supported}."
        ),
    )
    parser.add_argument(
        "--map",
        type=str,
        default=None,
        help="Map ID or map file path. Auto-resolved for file input when possible.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Write restored content to this file path.",
    )
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Overwrite input file in place (file-path input only).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output unified JSON contract for machine consumption.",
    )
    args = parser.parse_args()

    try:
        input_source = resolve_input_source_context(args.input)
        raw_input = input_source.content
        input_type = input_source.input_type
        input_path = input_source.input_path
        input_extension = input_source.extension
    except ValueError as error:
        _emit_error_and_exit(
            json_mode=args.json,
            error_type="validation_error",
            message=str(error),
            exit_code=2,
        )

    if input_extension and not supports_deanonymize_for_extension(input_extension):
        message = f"De-anonymization is not supported for '{input_extension}' files."
        _emit_error_and_exit(
            json_mode=args.json,
            error_type="validation_error",
            message=message,
            exit_code=2,
        )

    map_ref_str = None
    linkage_source = "latest-fallback"
    try:
        map_ref_str, linkage_source = resolve_map_reference(
            explicit_map=args.map,
            input_type=input_type,
            input_path=input_path,
            input_content=raw_input,
        )
    except MapStoreError as error:
        _emit_error_and_exit(
            json_mode=args.json,
            error_type="map_error",
            message=str(error),
            exit_code=1,
        )

    sanitized_input = strip_embedded_map_marker(raw_input)

    try:
        result, map_record = _deanonymize_with_record(
            raw_input=sanitized_input,
            map_ref=map_ref_str,
            linkage_source=linkage_source,
        )
    except MapStoreError as error:
        _emit_error_and_exit(
            json_mode=args.json,
            error_type="map_error",
            message=str(error),
            exit_code=1,
        )
    except Exception as error:
        _emit_error_and_exit(
            json_mode=args.json,
            error_type="runtime_error",
            message=str(error),
            exit_code=1,
        )

    output_path = None
    try:
        output_path = _persist_output_file(
            content=result["deanonymizedContent"],
            input_path=input_path,
            input_extension=input_extension,
            output_arg=args.output,
            in_place=args.in_place,
            output_tag="restored",
            mapping_entries=list(map_record.entries),
        )
        if output_path:
            result["outputPath"] = output_path
    except ValueError as error:
        _emit_error_and_exit(
            json_mode=args.json,
            error_type="validation_error",
            message=str(error),
            exit_code=2,
        )
    except OSError as error:
        _emit_error_and_exit(
            json_mode=args.json,
            error_type="io_error",
            message=f"failed to write output file: {error}",
            exit_code=1,
        )

    if args.json:
        print(json.dumps(_success_envelope(result), ensure_ascii=False))
        return

    print("Status: success", file=sys.stderr)
    print(f"mapId: {result['mapRef']['mapId']}", file=sys.stderr)
    print(f"linkageSource: {result['linkageSource']}", file=sys.stderr)
    print(f"totalReplacements: {result['replacementSummary']['totalReplacements']}", file=sys.stderr)
    if output_path:
        print(f"outputPath: {output_path}", file=sys.stderr)
    for warning in result.get("warnings", []):
        print(f"Warning: {warning['code']}: {warning['message']}", file=sys.stderr)
    print(result["deanonymizedContent"])


if __name__ == "__main__":
    main()
