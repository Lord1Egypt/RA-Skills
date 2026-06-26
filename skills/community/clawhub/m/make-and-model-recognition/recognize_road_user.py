#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import mimetypes
import os
from pathlib import Path
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass
from typing import Any


DEFAULT_API_URL = "https://trafficeye.ai/recognition"
DEFAULT_API_KEY_MODE = "header"
DEFAULT_API_KEY_NAME = "apikey"
DEFAULT_FILE_FIELD = "file"
DEFAULT_REQUEST_FIELD = "request"
DEFAULT_TIMEOUT_S = 30.0
DEFAULT_REQUEST_JSON = json.dumps(
    {
        "tasks": ["DETECTION", "OCR", "MMR"],
        "requestedDetectionTypes": ["BOX", "PLATE"],
        "mmrPreference": "BOX",
    },
    separators=(",", ":"),
)


class RoadUserRecognitionError(RuntimeError):
    """Raised when the API call or response parsing fails."""


@dataclass(frozen=True)
class RoadUserCandidate:
    """One road-user candidate extracted from the API response."""

    payload: dict[str, Any]
    area: float
    box: dict[str, Any]
    combination_index: int | None
    road_user_index: int | None
    plate_index: int | None
    source_path: str


def build_multipart_body(
    fields: dict[str, str | bytes],
    files: dict[str, tuple[str, bytes, str | None]],
) -> tuple[bytes, str]:
    """Serialize form fields and files into a multipart/form-data body."""
    boundary = f"----trafficeye-skill-{uuid.uuid4().hex}"
    chunks: list[bytes] = []

    for name, value in fields.items():
        value_bytes = bytes(value) if isinstance(value, (bytes, bytearray, memoryview)) else value.encode("utf-8")
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("ascii"),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"),
                value_bytes,
                b"\r\n",
            ]
        )

    for name, (filename, content, content_type) in files.items():
        guessed_type = content_type or mimetypes.guess_type(filename)[0] or "application/octet-stream"
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("ascii"),
                f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode("utf-8"),
                f"Content-Type: {guessed_type}\r\n\r\n".encode("ascii"),
                content,
                b"\r\n",
            ]
        )

    chunks.append(f"--{boundary}--\r\n".encode("ascii"))
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def rectangle_area(position: dict[str, Any]) -> float:
    """Compute the area of an axis-aligned vehicle box."""
    width = float(position["bottomRightCol"]) - float(position["topLeftCol"])
    height = float(position["bottomRightRow"]) - float(position["topLeftRow"])
    return abs(width * height)


def _build_candidate(
    road_user: dict[str, Any],
    *,
    combination_index: int | None,
    road_user_index: int | None,
    plate_index: int | None,
    source_path: str,
) -> RoadUserCandidate | None:
    """Build one candidate from a road-user payload if it has a vehicle box."""
    box = road_user.get("box")
    if not isinstance(box, dict):
        return None
    position = box.get("position")
    if not isinstance(position, dict):
        return None
    try:
        area = rectangle_area(position)
    except (KeyError, TypeError, ValueError):
        return None
    return RoadUserCandidate(
        payload=road_user,
        area=area,
        box=box,
        combination_index=combination_index,
        road_user_index=road_user_index,
        plate_index=plate_index,
        source_path=source_path,
    )


def _looks_like_road_user_payload(value: Any) -> bool:
    """Heuristically identify one road-user object in arbitrary API JSON."""
    if not isinstance(value, dict):
        return False
    box = value.get("box")
    if not isinstance(box, dict):
        return False
    position = box.get("position")
    if not isinstance(position, dict):
        return False
    road_user_markers = ("plates", "mmr", "windshield", "wheels")
    return any(marker in value for marker in road_user_markers)


def _extract_payload_root(payload: Any) -> Any:
    """Unwrap the TrafficEye response payload when it is nested under data."""
    if isinstance(payload, dict) and isinstance(payload.get("data"), dict):
        return payload["data"]
    return payload


def extract_candidates(payload: Any) -> list[RoadUserCandidate]:
    """Extract road-user candidates from the TrafficEye response payload."""
    payload = _extract_payload_root(payload)
    candidates: list[RoadUserCandidate] = []

    if isinstance(payload, dict):
        combinations = payload.get("combinations")
        if isinstance(combinations, list):
            for combination_index, combination in enumerate(combinations):
                if not isinstance(combination, dict):
                    continue
                road_users = combination.get("roadUsers")
                if not isinstance(road_users, list):
                    continue
                for road_user_index, road_user in enumerate(road_users):
                    if not isinstance(road_user, dict):
                        continue
                    candidate = _build_candidate(
                        road_user,
                        combination_index=combination_index,
                        road_user_index=road_user_index,
                        plate_index=None,
                        source_path=f"combinations[{combination_index}].roadUsers[{road_user_index}]",
                    )
                    if candidate is not None:
                        candidates.append(candidate)
            if candidates:
                return candidates

        road_users = payload.get("roadUsers")
        if isinstance(road_users, list):
            for road_user_index, road_user in enumerate(road_users):
                if not isinstance(road_user, dict):
                    continue
                candidate = _build_candidate(
                    road_user,
                    combination_index=None,
                    road_user_index=road_user_index,
                    plate_index=None,
                    source_path=f"roadUsers[{road_user_index}]",
                )
                if candidate is not None:
                    candidates.append(candidate)
            if candidates:
                return candidates

    def walk(node: Any, path: str) -> None:
        if _looks_like_road_user_payload(node):
            candidate = _build_candidate(
                node,
                combination_index=None,
                road_user_index=None,
                plate_index=None,
                source_path=path or "$",
            )
            if candidate is not None:
                candidates.append(candidate)
                return
        if isinstance(node, dict):
            for key, value in node.items():
                child_path = f"{path}.{key}" if path else key
                walk(value, child_path)
        elif isinstance(node, list):
            for index, value in enumerate(node):
                child_path = f"{path}[{index}]" if path else f"[{index}]"
                walk(value, child_path)

    walk(payload, "")
    if not candidates:
        if isinstance(payload, dict):
            top_level_keys = ", ".join(sorted(payload.keys())) or "<empty object>"
            raise RoadUserRecognitionError(
                f"Response JSON does not contain recognizable road-user box data; top-level keys: {top_level_keys}"
            )
        raise RoadUserRecognitionError("Response JSON does not contain recognizable road-user box data")
    return candidates


def select_largest_road_user(payload: dict[str, Any]) -> RoadUserCandidate:
    """Return the largest detected vehicle from the response payload."""
    candidates = extract_candidates(payload)
    if not candidates:
        raise RoadUserRecognitionError("No boxed road-user candidates were found in the API response")
    return max(candidates, key=lambda candidate: candidate.area)


def build_request_url(api_url: str, api_key: str | None, api_key_mode: str, api_key_name: str) -> str:
    """Append the API key to the query string when query-mode auth is enabled."""
    if api_key_mode != "query" or not api_key:
        return api_url
    parsed = urllib.parse.urlsplit(api_url)
    query_items = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    query_items.append((api_key_name, api_key))
    updated_query = urllib.parse.urlencode(query_items)
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, updated_query, parsed.fragment))


def call_api(
    image_path: Path,
    api_url: str,
    api_key: str | None,
    api_key_mode: str,
    api_key_name: str,
    request_json: str | None,
    file_field: str,
    request_field: str,
    timeout_s: float,
) -> Any:
    """Upload the image to the API and parse the JSON response."""
    fields: dict[str, str | bytes] = {}
    if request_json:
        fields[request_field] = request_json
    if api_key_mode == "form" and api_key:
        fields[api_key_name] = api_key

    image_bytes = image_path.read_bytes()
    body, content_type = build_multipart_body(
        fields,
        {file_field: (image_path.name, image_bytes, None)},
    )

    request_url = build_request_url(api_url, api_key, api_key_mode, api_key_name)
    headers = {"Content-Type": content_type, "Content-Length": str(len(body))}
    if api_key_mode == "header" and api_key:
        headers[api_key_name] = api_key
    elif api_key_mode == "bearer" and api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    request = urllib.request.Request(request_url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout_s) as response:
            raw_body = response.read()
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RoadUserRecognitionError(f"API request failed with HTTP {exc.code}: {error_body}") from exc
    except urllib.error.URLError as exc:
        raise RoadUserRecognitionError(f"Unable to reach TrafficEye API: {exc.reason}") from exc

    try:
        decoded = json.loads(raw_body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise RoadUserRecognitionError("API response was not valid JSON") from exc
    return decoded


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse command-line arguments for the helper."""
    parser = argparse.ArgumentParser(description="Detect the largest vehicle and return its full road-user payload via the TrafficEye API")
    parser.add_argument("image", nargs="?", help="Path to the local image file")
    parser.add_argument("--api-url", default=os.getenv("TRAFFICEYE_API_URL", DEFAULT_API_URL))
    parser.add_argument("--api-key", default=os.getenv("TRAFFICEYE_API_KEY"))
    parser.add_argument(
        "--api-key-mode",
        default=os.getenv("TRAFFICEYE_API_KEY_MODE", DEFAULT_API_KEY_MODE),
        choices=("header", "bearer", "form", "query"),
    )
    parser.add_argument("--api-key-name", default=os.getenv("TRAFFICEYE_API_KEY_NAME", DEFAULT_API_KEY_NAME))
    parser.add_argument("--file-field", default=os.getenv("TRAFFICEYE_FILE_FIELD", DEFAULT_FILE_FIELD))
    parser.add_argument("--request-field", default=os.getenv("TRAFFICEYE_REQUEST_FIELD", DEFAULT_REQUEST_FIELD))
    parser.add_argument("--request-json", default=os.getenv("TRAFFICEYE_REQUEST_JSON", DEFAULT_REQUEST_JSON))
    parser.add_argument("--timeout", type=float, default=float(os.getenv("TRAFFICEYE_TIMEOUT_S", str(DEFAULT_TIMEOUT_S))))
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--response-json-file", help="Read a saved API response instead of calling the API")
    return parser.parse_args(argv)


def render_candidate(candidate: RoadUserCandidate) -> dict[str, Any]:
    """Convert a selected candidate into stable output JSON."""
    return {
        "roadUser": candidate.payload,
        "plates": candidate.payload.get("plates", []),
        "box": candidate.box,
        "area": candidate.area,
        "source": {
            "combinationIndex": candidate.combination_index,
            "roadUserIndex": candidate.road_user_index,
            "path": candidate.source_path,
        },
    }


def main(argv: list[str]) -> int:
    """Run the helper from the command line."""
    args = parse_args(argv)

    if args.response_json_file:
        response_path = Path(args.response_json_file).expanduser().resolve()
        payload = json.loads(response_path.read_text(encoding="utf-8"))
    else:
        if not args.image:
            raise RoadUserRecognitionError("An image path is required unless --response-json-file is used")
        image_path = Path(args.image).expanduser().resolve()
        if not image_path.is_file():
            raise RoadUserRecognitionError(f"Image file does not exist: {image_path}")
        payload = call_api(
            image_path=image_path,
            api_url=args.api_url,
            api_key=args.api_key,
            api_key_mode=args.api_key_mode,
            api_key_name=args.api_key_name,
            request_json=args.request_json,
            file_field=args.file_field,
            request_field=args.request_field,
            timeout_s=args.timeout,
        )

    candidate = select_largest_road_user(payload)
    result = render_candidate(candidate)
    if args.format in {"json", "text"}:
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    raise RoadUserRecognitionError("Largest road user detected, but the output format was unsupported")


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except RoadUserRecognitionError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1) from exc