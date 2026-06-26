#!/usr/bin/env python3
"""
Modeio AI Anonymization Skill.

- `lite` level runs local regex anonymization (no network call).
- Other levels call the Modeio anonymization API.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REQUESTS_AVAILABLE = True
try:
    import requests
except ModuleNotFoundError:
    REQUESTS_AVAILABLE = False

    class _RequestsShim:
        class RequestException(Exception):
            pass

        class MissingDependencyError(RequestException):
            pass

        class ConnectionError(RequestException):
            pass

        class Timeout(RequestException):
            pass

        @staticmethod
        def post(*_args, **_kwargs):
            raise _RequestsShim.MissingDependencyError(
                "requests package is required for api-backed anonymization levels. "
                "Install requests to enable non-lite anonymization."
            )

    requests = _RequestsShim()

from modeio_redact.core.errors import PipelineError
from modeio_redact.core.pipeline import (
    RedactionProviderPipeline,
)
from modeio_redact.cli.anonymize_output import (
    append_warning as _append_warning,
    run_file_pipeline as _run_file_pipeline,
)
from modeio_redact.workflow.file_types import (
    HANDLER_TEXT,
    handler_key_for_extension,
    is_level_supported_for_extension,
    supported_levels_for_extension,
)
from modeio_redact.workflow.file_handlers import read_input_file, uses_text_handler
from modeio_redact.workflow.input_source import (
    SUPPORTED_FILE_EXTENSIONS,
    resolve_input_source,
    resolve_input_source_context,
)
from modeio_redact.core.models import MapRef, MappingEntry
from modeio_redact.workflow.map_store import (
    MapStoreError,
    normalize_mapping_entries,
    save_map,
    update_anonymized_hash,
)

# Backend API URL, overridable via ANONYMIZE_API_URL environment variable
URL = os.environ.get("ANONYMIZE_API_URL", "https://safety-cf.modeio.ai/api/cf/anonymize")

HEADERS = {"Content-Type": "application/json"}

VALID_LEVELS = ("lite", "dynamic", "strict", "crossborder")

TOOL_NAME = "privacy-protector"

MAX_RETRIES = 2
RETRY_BACKOFF = 1.0  # seconds; doubles each retry


class RequestFailure(RuntimeError):
    def __init__(
        self,
        *,
        error_type: str,
        message: str,
        status_code: Optional[int] = None,
        dependency_error: bool = False,
        cause: Optional[Exception] = None,
    ):
        super().__init__(message)
        self.error_type = error_type
        self.status_code = status_code
        self.dependency_error = dependency_error
        self.cause = cause


def _post_with_retry(url, headers, json_payload, timeout=60):
    """POST with simple exponential-backoff retry on transient failures."""
    last_exc = None
    for attempt in range(1 + MAX_RETRIES):
        try:
            resp = requests.post(url, headers=headers, json=json_payload, timeout=timeout)
            if resp.status_code in (502, 503, 504) and attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF * (2 ** attempt))
                continue
            resp.raise_for_status()
            return resp
        except requests.RequestException as e:
            last_exc = e
            if isinstance(e, (requests.ConnectionError, requests.Timeout)) and attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF * (2 ** attempt))
                continue
            raise
    # Should not reach here, but raise last exception if it does
    raise last_exc  # type: ignore[misc]


def _is_requests_dependency_error(error: Exception) -> bool:
    if REQUESTS_AVAILABLE:
        return False
    missing_dependency_type = getattr(requests, "MissingDependencyError", None)
    if missing_dependency_type is not None and isinstance(error, missing_dependency_type):
        return True
    return "requests package is required" in str(error).lower()


def _validate_level_support_or_raise(level: str, input_extension: Optional[str]) -> None:
    if input_extension and not is_level_supported_for_extension(input_extension, level):
        supported_levels = ", ".join(supported_levels_for_extension(input_extension))
        raise ValueError(
            f"Anonymization level '{level}' is not supported for '{input_extension}' files. "
            f"Supported levels: {supported_levels}."
        )


def _validate_non_text_mapping_or_raise(
    *,
    level: str,
    input_path: Optional[str],
    input_extension: Optional[str],
    raw_input: str,
    anonymized_content: str,
    has_pii: Any,
    entries: List[MappingEntry],
) -> None:
    if not input_path or not input_extension:
        return
    if level == "lite":
        return
    if handler_key_for_extension(input_extension) == HANDLER_TEXT:
        return
    if entries:
        return

    pii_detected = bool(has_pii)
    content_changed = anonymized_content != raw_input
    if not pii_detected and not content_changed:
        return

    raise ValueError(
        f"Anonymization provider returned no mapping entries for '{input_extension}' file output. "
        "Cannot safely project non-text redactions without mapping data. "
        "Use --level lite or ensure API mapping entries are returned."
    )


def _resolve_crossborder_codes_or_raise(
    level: str,
    sender_code: Optional[str],
    recipient_code: Optional[str],
) -> Tuple[Optional[str], Optional[str]]:
    if level != "crossborder":
        return None, None

    sender = (sender_code or "").strip()
    recipient = (recipient_code or "").strip()
    if not sender or not recipient:
        raise ValueError("--sender-code and --recipient-code are required when --level is crossborder.")

    return sender, recipient


def _run_anonymize_or_raise(
    *,
    raw_input: str,
    level: str,
    sender_code: Optional[str],
    recipient_code: Optional[str],
    input_type: str,
) -> Dict[str, Any]:
    try:
        return anonymize(
            raw_input,
            level=level,
            sender_code=sender_code,
            recipient_code=recipient_code,
            input_type=input_type,
        )
    except requests.RequestException as error:
        dependency_error = _is_requests_dependency_error(error)
        response = getattr(error, "response", None)
        status_code = getattr(response, "status_code", None)
        error_type = "dependency_error" if dependency_error else "network_error"
        message = str(error) if dependency_error else f"anonymization request failed: {type(error).__name__}"
        raise RequestFailure(
            error_type=error_type,
            message=message,
            status_code=status_code,
            dependency_error=dependency_error,
            cause=error,
        ) from error


def anonymize(
    raw_input: str,
    level: str = "dynamic",
    sender_code: str = None,
    recipient_code: str = None,
    input_type: str = "text",
) -> dict:
    provider_pipeline = RedactionProviderPipeline(api_anonymize_callable=_anonymize_via_api_provider)
    provider_result = provider_pipeline.run(
        content=raw_input,
        level=level,
        input_type=input_type,
        sender_code=sender_code,
        recipient_code=recipient_code,
    )

    if level != "lite":
        raw_payload = provider_result.raw_payload
        if isinstance(raw_payload, dict) and raw_payload.get("success") is False:
            return raw_payload

    return {
        "success": True,
        "data": _provider_result_to_data(provider_result=provider_result, level=level),
    }


def _anonymize_via_api_provider(
    raw_input: str,
    level: str = "dynamic",
    sender_code: str = None,
    recipient_code: str = None,
    input_type: str = "text",
) -> Dict[str, Any]:
    payload = {
        "input": raw_input,
        "inputType": input_type,
        "level": level,
    }
    if sender_code:
        payload["senderCode"] = sender_code
    if recipient_code:
        payload["recipientCode"] = recipient_code
    resp = _post_with_retry(URL, headers=HEADERS, json_payload=payload)
    return resp.json()


def _provider_result_to_data(provider_result, level: str) -> Dict[str, Any]:
    data: Dict[str, Any] = {
        "anonymizedContent": provider_result.anonymized_content,
        "hasPII": provider_result.has_pii,
    }

    raw_payload = provider_result.raw_payload
    if level == "lite":
        data["mode"] = "local-regex"
        if isinstance(raw_payload, dict):
            local_detection = raw_payload.get("localDetection")
            if isinstance(local_detection, dict):
                data["localDetection"] = local_detection
    elif isinstance(raw_payload, dict):
        raw_data = raw_payload.get("data")
        if isinstance(raw_data, dict):
            for key, value in raw_data.items():
                if key in ("anonymizedContent", "hasPII"):
                    continue
                data[key] = value

    if "mapping" not in data and provider_result.items:
        data["mapping"] = [
            {
                "anonymized": item.placeholder,
                "original": item.original,
                "type": item.entity_type,
            }
            for item in provider_result.items
            if item.placeholder and item.original
        ]

    return data


def _success_envelope(level: str, mode: str, data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "success": True,
        "tool": TOOL_NAME,
        "mode": mode,
        "level": level,
        "data": data,
    }


def _error_envelope(
    level: str,
    mode: str,
    error_type: str,
    message: str,
    status_code: int = None,
    details: Dict[str, Any] = None,
) -> Dict[str, Any]:
    error: Dict[str, Any] = {
        "type": error_type,
        "message": message,
    }
    if status_code is not None:
        error["status_code"] = status_code
    if details is not None:
        error["details"] = details
    return {
        "success": False,
        "tool": TOOL_NAME,
        "mode": mode,
        "level": level,
        "error": error,
    }


def _maybe_save_map(
    raw_input: str,
    level: str,
    mode: str,
    data: Dict[str, Any],
    entries: Optional[List[MappingEntry]] = None,
) -> Optional[MapRef]:
    if entries is None:
        entries = normalize_mapping_entries(data)
    if not entries:
        return None

    anonymized_content = data.get("anonymizedContent")
    if not isinstance(anonymized_content, str):
        return None

    map_ref = save_map(
        raw_input=raw_input,
        anonymized_content=anonymized_content,
        entries=entries,
        level=level,
        source_mode=mode,
    )
    data["mapRef"] = map_ref.to_dict()
    return map_ref


def _maybe_sync_non_text_map_hash(
    *,
    map_ref: Optional[MapRef],
    output_path: Optional[str],
    input_extension: Optional[str],
    data: Dict[str, Any],
) -> None:
    if map_ref is None or not output_path or not input_extension:
        return
    if uses_text_handler(input_extension):
        return

    actual_output = read_input_file(Path(output_path).expanduser(), input_extension)
    update_anonymized_hash(map_ref.map_path, actual_output)
    map_ref_data = data.get("mapRef")
    if isinstance(map_ref_data, dict):
        map_ref_data["mapPath"] = map_ref.map_path


def main():
    supported = ", ".join(SUPPORTED_FILE_EXTENSIONS)
    parser = argparse.ArgumentParser(
        description=(
            f"Anonymize text/JSON or a supported file path ({supported}). "
            "`lite` runs locally; other levels call the Modeio API."
        )
    )
    parser.add_argument(
        "-i", "--input",
        type=str,
        required=True,
        help=f"Raw content to anonymize, or a supported file path ({supported}).",
    )
    parser.add_argument(
        "--level",
        type=str,
        default="dynamic",
        choices=VALID_LEVELS,
        help="Anonymization level (default: dynamic). `lite` runs local regex with no network call.",
    )
    parser.add_argument(
        "--sender-code",
        type=str,
        default=None,
        help="Sender jurisdiction code, required for crossborder level (example: CN SHA).",
    )
    parser.add_argument(
        "--recipient-code",
        type=str,
        default=None,
        help="Recipient jurisdiction code, required for crossborder level (example: US NYC).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output unified JSON contract for machine consumption.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Write anonymized content to this file path.",
    )
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Overwrite the input file in place (file-path input only).",
    )
    args = parser.parse_args()

    mode = "local-regex" if args.level == "lite" else "api"

    try:
        input_source = resolve_input_source_context(args.input)
        raw_input = input_source.content
        input_type = input_source.input_type
        input_path = input_source.input_path
        input_extension = input_source.extension
    except ValueError as exc:
        if args.json:
            print(json.dumps(
                _error_envelope(
                    level=args.level,
                    mode=mode,
                    error_type="validation_error",
                    message=str(exc),
                ),
                ensure_ascii=False,
            ))
        else:
            print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)

    try:
        _validate_level_support_or_raise(args.level, input_extension)
        sender_code, recipient_code = _resolve_crossborder_codes_or_raise(
            args.level,
            args.sender_code,
            args.recipient_code,
        )
    except ValueError as error:
        if args.json:
            print(json.dumps(
                _error_envelope(
                    level=args.level,
                    mode=mode,
                    error_type="validation_error",
                    message=str(error),
                ),
                ensure_ascii=False,
            ))
        else:
            print(f"Error: {error}", file=sys.stderr)
        sys.exit(2)

    try:
        result = _run_anonymize_or_raise(
            raw_input=raw_input,
            level=args.level,
            sender_code=sender_code,
            recipient_code=recipient_code,
            input_type=input_type,
        )
    except RequestFailure as error:
        if args.json:
            print(json.dumps(
                _error_envelope(
                    level=args.level,
                    mode=mode,
                    error_type=error.error_type,
                    message=str(error),
                    status_code=error.status_code,
                ),
                ensure_ascii=False,
            ))
        else:
            if error.dependency_error:
                print(f"Error: {error}", file=sys.stderr)
            else:
                print(f"Error: anonymization request failed. url={URL}", file=sys.stderr)
            if error.status_code is not None:
                print(f"Error: status_code={error.status_code}", file=sys.stderr)
            if error.cause is not None:
                print(f"Error: exception={type(error.cause).__name__}: {error.cause}", file=sys.stderr)
        sys.exit(1)

    if not result.get("success"):
        if args.json:
            print(json.dumps(
                _error_envelope(
                    level=args.level,
                    mode=mode,
                    error_type="api_error",
                    message="anonymization backend returned success=false",
                    details=result,
                ),
                ensure_ascii=False,
            ))
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    data = result.get("data", {})
    anonymized = data.get("anonymizedContent", "")
    has_pii = data.get("hasPII", None)
    data["inputType"] = input_type
    if input_path:
        data["inputPath"] = input_path

    if not isinstance(anonymized, str):
        anonymized = str(anonymized)
        data["anonymizedContent"] = anonymized

    entries = normalize_mapping_entries(data)

    try:
        _validate_non_text_mapping_or_raise(
            level=args.level,
            input_path=input_path,
            input_extension=input_extension,
            raw_input=raw_input,
            anonymized_content=anonymized,
            has_pii=has_pii,
            entries=entries,
        )
    except ValueError as error:
        if args.json:
            print(json.dumps(
                _error_envelope(
                    level=args.level,
                    mode=mode,
                    error_type="validation_error",
                    message=str(error),
                ),
                ensure_ascii=False,
            ))
        else:
            print(f"Error: {error}", file=sys.stderr)
        sys.exit(2)

    map_ref = None
    try:
        map_ref = _maybe_save_map(
            raw_input=raw_input,
            level=args.level,
            mode=mode,
            data=data,
            entries=entries,
        )
    except MapStoreError as error:
        _append_warning(
            data,
            code="map_persist_failed",
            message=str(error),
        )

    output_path = None
    sidecar_path = None

    try:
        output_path, sidecar_path, _ = _run_file_pipeline(
            input_source=input_source,
            input_path=input_path,
            input_extension=input_extension,
            output_arg=args.output,
            in_place=args.in_place,
            anonymized_content=anonymized,
            entries=entries,
            map_ref=map_ref,
            data=data,
        )
    except (ValueError, PipelineError) as error:
        error_type = "assurance_error" if isinstance(error, PipelineError) else "validation_error"
        if args.json:
            print(json.dumps(
                _error_envelope(
                    level=args.level,
                    mode=mode,
                    error_type=error_type,
                    message=str(error),
                ),
                ensure_ascii=False,
            ))
        else:
            print(f"Error: {error}", file=sys.stderr)
        sys.exit(2)
    except OSError as error:
        if args.json:
            print(json.dumps(
                _error_envelope(
                    level=args.level,
                    mode=mode,
                    error_type="io_error",
                    message=f"failed to write output file: {error}",
                ),
                ensure_ascii=False,
            ))
        else:
            print(f"Error: failed to write output file: {error}", file=sys.stderr)
        sys.exit(1)

    try:
        _maybe_sync_non_text_map_hash(
            map_ref=map_ref,
            output_path=output_path,
            input_extension=input_extension,
            data=data,
        )
    except (MapStoreError, ValueError) as error:
        _append_warning(
            data,
            code="map_hash_sync_failed",
            message=str(error),
        )

    if args.json:
        print(json.dumps(_success_envelope(level=args.level, mode=mode, data=data), ensure_ascii=False))
        return

    print("Status: success", file=sys.stderr)
    if mode == "local-regex":
        print("mode: local-regex", file=sys.stderr)
    print("hasPII:", has_pii, file=sys.stderr)
    if map_ref:
        print(f"mapId: {map_ref.map_id}", file=sys.stderr)
    if output_path:
        print(f"outputPath: {output_path}", file=sys.stderr)
    if sidecar_path:
        print(f"sidecarPath: {sidecar_path}", file=sys.stderr)
    warnings = data.get("warnings")
    if isinstance(warnings, list):
        for warning in warnings:
            if isinstance(warning, dict):
                print(f"Warning: {warning.get('code', 'warning')}: {warning.get('message', '')}", file=sys.stderr)
    print(anonymized)


if __name__ == "__main__":
    main()
