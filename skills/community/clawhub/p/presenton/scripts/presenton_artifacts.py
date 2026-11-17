#!/usr/bin/env python3
"""Prepare Presenton assets, export HTML, and return download and preview URLs."""

from __future__ import annotations

import argparse
import json
import re
import secrets
import shutil
import sys
import tempfile
import threading
import urllib.error
import urllib.request
from collections.abc import Iterator
from contextlib import contextmanager
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote_plus, urlencode, urlparse, urlsplit

from validate_html import validate_html


DEFAULT_API_BASE = "https://api.presenton.ai"
SEARCH_TIMEOUT_SECONDS = 60.0
EXPORT_TIMEOUT_SECONDS = 300.0
PUBLIC_IMAGE_UPLOAD_MAX_BYTES = 10 * 1024 * 1024
TEMP_MARKER_NAME = ".presenton-temp"
TEMP_MARKER_CONTENT = "presenton-owned\n"
PUBLIC_IMAGE_CONTENT_TYPES = {
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}
ICON_TYPES = ("bold", "duotone", "fill", "light", "regular", "thin")

GENERIC_FONT_FAMILIES = {
    "cursive",
    "fantasy",
    "fangsong",
    "inherit",
    "initial",
    "math",
    "monospace",
    "revert",
    "sans-serif",
    "serif",
    "system-ui",
    "ui-monospace",
    "ui-rounded",
    "ui-sans-serif",
    "ui-serif",
    "unset",
}
TAILWIND_FONT_STACKS = {
    "font-sans": "ui-sans-serif, system-ui, sans-serif",
    "font-serif": "ui-serif, Georgia, Cambria, Times New Roman, Times, serif",
    "font-mono": (
        "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "
        "Liberation Mono, Courier New, monospace"
    ),
}


class PresentonError(RuntimeError):
    pass


class FontUsageParser(HTMLParser):
    """Collect font utilities, inline declarations, and web-font stylesheets."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tailwind_fonts: list[tuple[str, str]] = []
        self.web_font_urls: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        classes = (attributes.get("class") or "").split()
        for class_name in classes:
            if class_name in TAILWIND_FONT_STACKS:
                self.tailwind_fonts.append((class_name, TAILWIND_FONT_STACKS[class_name]))
            elif class_name.startswith("font-[") and class_name.endswith("]"):
                family = class_name[6:-1].strip("'\"").replace("_", " ")
                if family:
                    self.tailwind_fonts.append(("arbitrary font utility", family))

        href = attributes.get("href") or attributes.get("src")
        if href:
            parsed = urlsplit(unescape(href))
            if parsed.scheme == "https" and "family" in parse_qs(parsed.query):
                self.web_font_urls.append(unescape(href))


def split_font_stack(value: str) -> list[str]:
    """Split a CSS font-family value while preserving quoted family names."""

    parts = re.split(r",\s*(?![^()]*\))", value)
    return [part.strip().strip("'\"") for part in parts if part.strip()]


def is_installable_font_name(name: str) -> bool:
    normalized = re.sub(r"\s+", " ", name.strip()).lower()
    return bool(normalized) and normalized not in GENERIC_FONT_FAMILIES and not normalized.startswith(
        ("var(", "--")
    )


def collect_font_usage(html: str) -> list[tuple[str, list[str]]]:
    """Return ordered font names/stacks and the places that declare them."""

    records: dict[str, tuple[str, list[str]]] = {}

    def add(name: str, source: str) -> None:
        clean_name = re.sub(r"\s+", " ", unescape(name).strip())
        if not is_installable_font_name(clean_name):
            return
        key = clean_name.casefold()
        if key not in records:
            records[key] = (clean_name, [])
        if source not in records[key][1]:
            records[key][1].append(source)

    parser = FontUsageParser()
    parser.feed(html)
    parser.close()

    for match in re.finditer(r"font-family\s*:\s*([^;}\n]+)", html, re.IGNORECASE):
        stack = re.sub(r"\s+", " ", match.group(1).strip())
        for family in split_font_stack(stack):
            add(family, f"CSS font-family stack: {stack}")

    # Arbitrary Tailwind font-family utilities are explicit enough to be useful
    # even when Tailwind's generated CSS is not present in the source HTML.
    for utility, value in parser.tailwind_fonts:
        if utility == "arbitrary font utility":
            add(value, f"Tailwind {utility}: font-[{value}]")
        else:
            add(f"{utility} stack", f"Tailwind {utility}: {value}")

    web_font_urls = list(parser.web_font_urls)
    web_font_urls.extend(re.findall(r"https://[^\s\"')>]+", html, re.IGNORECASE))
    for source_url in dict.fromkeys(web_font_urls):
        parsed_url = urlsplit(source_url)
        query = parse_qs(parsed_url.query)
        for encoded_family in query.get("family", []):
            family_spec = unquote_plus(encoded_family)
            family_name = family_spec.split(":", 1)[0].replace("+", " ").strip()
            add(family_name, f"Web font stylesheet ({parsed_url.netloc}): {source_url}")

    return list(records.values())


def print_font_usage(html: str) -> None:
    records = collect_font_usage(html)
    print("Fonts used by the final HTML:")
    if not records:
        print("- No explicit installable font family was found; browser/exporter defaults may apply.")
        return
    for name, sources in records:
        print(f"- {name}")
        for source in sources:
            print(f"  Source: {source}")


def print_status(message: str) -> None:
    print(f"[presenton] {message}", file=sys.stderr, flush=True)


def print_response_message(response: Any) -> None:
    """Expose optional user-facing messages without changing stdout contracts."""

    message = response.get("message") if isinstance(response, dict) else None
    if isinstance(message, str) and message:
        print_status(f"API message: {message}")


def valid_web_url(value: Any) -> str | None:
    """Return a valid HTTP(S) URL string, or None."""

    if not isinstance(value, str):
        return None
    parsed_url = urlparse(value)
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        return None
    return value


@contextmanager
def status_heartbeat(message: str, interval_seconds: float = 10.0) -> Iterator[None]:
    print_status(message)
    stopped = threading.Event()

    def emit_heartbeat() -> None:
        while not stopped.wait(interval_seconds):
            print_status(f"{message} (still working)")

    thread = threading.Thread(target=emit_heartbeat, daemon=True)
    thread.start()
    try:
        yield
    finally:
        stopped.set()
        thread.join()


def request_json(
    endpoint: str,
    payload: dict[str, Any],
    timeout: float = 300.0,
) -> Any:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "presenton-skill/1",
    }
    request = urllib.request.Request(
        f"{DEFAULT_API_BASE}{endpoint}",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    return send_json_request(request, endpoint, timeout)


def send_json_request(
    request: urllib.request.Request,
    endpoint: str,
    timeout: float,
) -> Any:
    """Send a prepared request and decode its JSON response consistently."""

    try:
        with status_heartbeat(f"Waiting for {endpoint}"):
            with urllib.request.urlopen(request, timeout=timeout) as response:
                result = json.loads(response.read().decode("utf-8"))
        print_status(f"Received response from {endpoint}")
        return result
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            error_payload = json.loads(body)
            detail = (
                error_payload.get("detail") or error_payload.get("error") or body
                if isinstance(error_payload, dict)
                else body
            )
        except json.JSONDecodeError:
            detail = body
        raise PresentonError(f"Presenton API returned HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise PresentonError(f"Could not reach Presenton API: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise PresentonError("Presenton API returned invalid JSON") from exc


def request_get_json(
    endpoint: str,
    params: dict[str, Any],
    timeout: float = 60.0,
) -> Any:
    query = urlencode({key: value for key, value in params.items() if value is not None})
    request = urllib.request.Request(
        f"{DEFAULT_API_BASE}{endpoint}?{query}",
        headers={
            "Accept": "application/json",
            "User-Agent": "presenton-skill/1",
        },
        method="GET",
    )
    return send_json_request(request, endpoint, timeout)


def request_public_image_upload(image_path: Path, timeout: float = 60.0) -> Any:
    try:
        resolved_path = image_path.expanduser().resolve(strict=True)
        if not resolved_path.is_file():
            raise PresentonError("Image path is not a file")
        content_type = PUBLIC_IMAGE_CONTENT_TYPES.get(resolved_path.suffix.lower())
        if content_type is None:
            raise PresentonError("Image must be a PNG, JPEG, or WebP file")
        if resolved_path.stat().st_size > PUBLIC_IMAGE_UPLOAD_MAX_BYTES:
            raise PresentonError("Image exceeds the 10 MB public upload limit")
        image_bytes = resolved_path.read_bytes()
    except OSError as exc:
        raise PresentonError(f"Could not read image file: {exc}") from exc

    boundary = f"presenton-{secrets.token_hex(16)}"
    filename = resolved_path.name.replace('"', "_").replace("\\", "_")
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode("utf-8") + image_bytes + f"\r\n--{boundary}--\r\n".encode("ascii")
    endpoint = "/api/v3/images/upload/public"
    request = urllib.request.Request(
        f"{DEFAULT_API_BASE}{endpoint}",
        data=body,
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Accept": "application/json",
            "User-Agent": "presenton-skill/1",
        },
        method="POST",
    )
    return send_json_request(request, endpoint, timeout)


def get_temp_root() -> Path:
    return Path(tempfile.gettempdir()).resolve(strict=True)


def resolve_owned_temp_dir(path: Path) -> Path:
    if path.expanduser().is_symlink():
        raise PresentonError("Refusing to clean up a symbolic link")
    try:
        resolved = path.expanduser().resolve(strict=True)
        temp_root = get_temp_root()
        resolved.relative_to(temp_root)
    except (OSError, ValueError) as exc:
        raise PresentonError("Temporary directory is outside the OS temporary root") from exc
    if resolved == temp_root:
        raise PresentonError("Refusing to clean up the OS temporary root")
    if resolved.parent != temp_root or not resolved.name.startswith("presenton-"):
        raise PresentonError("Temporary directory was not created by Presenton")
    if not resolved.is_dir():
        raise PresentonError("Presenton temporary path is not a directory")
    marker = resolved / TEMP_MARKER_NAME
    if marker.is_symlink() or not marker.is_file():
        raise PresentonError("Presenton temporary ownership marker is missing")
    try:
        marker_content = marker.read_text(encoding="utf-8")
    except OSError as exc:
        raise PresentonError("Could not read Presenton temporary ownership marker") from exc
    if marker_content != TEMP_MARKER_CONTENT:
        raise PresentonError("Presenton temporary ownership marker is invalid")
    return resolved


def command_create_temp(_: argparse.Namespace) -> int:
    temp_dir = Path(tempfile.mkdtemp(prefix="presenton-")).resolve(strict=True)
    (temp_dir / TEMP_MARKER_NAME).write_text(TEMP_MARKER_CONTENT, encoding="utf-8")
    print_status(f"Created temporary workspace {temp_dir}")
    print(temp_dir)
    return 0


def command_cleanup_temp(args: argparse.Namespace) -> int:
    temp_dir = resolve_owned_temp_dir(args.path)
    shutil.rmtree(temp_dir)
    print_status(f"Cleaned temporary workspace {temp_dir}")
    return 0


def command_search(args: argparse.Namespace) -> int:
    print_status("Searching for matching presentation designs")
    response = request_json(
        "/api/v3/designs/search",
        {"query": args.query, "n": 4},
        timeout=SEARCH_TIMEOUT_SECONDS,
    )
    print_response_message(response)
    results = response.get("designs") if isinstance(response, dict) else None
    if not isinstance(results, list):
        raise PresentonError("Design search returned an unexpected response")
    print_status(f"Found {len(results)} design option(s)")
    for index, result in enumerate(results, start=1):
        print(f"{index}. {result.get('title', 'Untitled')} (id={result.get('id', '?')})")
        print(f"   {result.get('description', '')}")
    return 0


def command_upload_image(args: argparse.Namespace) -> int:
    print_status(f"Uploading presentation image {args.file}")
    response = request_public_image_upload(args.file, timeout=SEARCH_TIMEOUT_SECONDS)
    print_response_message(response)
    image_url = valid_web_url(response.get("url")) if isinstance(response, dict) else None
    if image_url is None:
        raise PresentonError(
            "Image upload response did not contain a valid HTTP or HTTPS URL"
        )
    print_status("Uploaded presentation image URL is ready")
    print(image_url)
    return 0


def command_search_icons(args: argparse.Namespace) -> int:
    query = args.query.strip()
    if not query:
        raise PresentonError("Icon search query must not be empty")
    if args.limit <= 0:
        raise PresentonError("Icon search limit must be a positive integer")
    print_status(f"Searching presentation icons for {query!r}")
    response = request_get_json(
        "/api/v3/icons/search",
        {
            "query": query,
            "limit": args.limit,
            "icon_type": args.icon_type,
        },
        timeout=SEARCH_TIMEOUT_SECONDS,
    )
    if not isinstance(response, list):
        raise PresentonError("Icon search returned an unexpected response")
    icon_urls = [valid_web_url(value) for value in response]
    if not icon_urls or any(value is None for value in icon_urls):
        raise PresentonError("Icon search did not return valid HTTP or HTTPS URLs")
    print_status(f"Found {len(icon_urls)} icon option(s)")
    for icon_url in icon_urls:
        print(icon_url)
    return 0


def command_export(args: argparse.Namespace) -> int:
    try:
        html_path = args.html.expanduser().resolve(strict=True)
        temp_root = get_temp_root()
        relative_path = html_path.relative_to(temp_root)
        if len(relative_path.parts) < 2 or not relative_path.parts[0].startswith(
            "presenton-"
        ):
            raise ValueError
        owned_temp_dir = temp_root / relative_path.parts[0]
        resolve_owned_temp_dir(owned_temp_dir)
    except (OSError, ValueError) as exc:
        raise PresentonError(
            "Presentation HTML must be inside a directory created by create-temp"
        ) from exc

    print_status(f"Reading temporary presentation HTML from {html_path}")
    try:
        html = html_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise PresentonError(f"Could not read HTML file: {exc}") from exc
    print_status("Validating HTML, Tailwind, and Chart.js requirements")
    validation_errors = validate_html(html)
    if validation_errors:
        formatted = "\n".join(f"- {error}" for error in validation_errors)
        raise PresentonError(f"HTML preflight failed:\n{formatted}")

    print_status("HTML validation passed")
    payload: dict[str, Any] = {"html": html, "format": args.format}
    if args.title:
        payload["title"] = args.title
    if args.design_id is not None:
        payload["design_id"] = args.design_id
    print_status(f"Submitting {args.format.upper()} export")
    response = request_json(
        "/api/v3/export/html-to-any",
        payload,
        timeout=EXPORT_TIMEOUT_SECONDS,
    )
    print_response_message(response)
    url = valid_web_url(response.get("url")) if isinstance(response, dict) else None
    if url is None:
        raise PresentonError(
            "Export response did not contain a valid HTTP or HTTPS URL"
        )
    creation_id = response.get("id") if isinstance(response, dict) else None
    if type(creation_id) is not int or creation_id <= 0:
        raise PresentonError("Export response did not contain a valid creation id")
    print_status(f"{args.format.upper()} export URL is ready")
    if getattr(args, "json", False):
        print(json.dumps({"id": creation_id, "url": url}))
    else:
        print(url)
    return 0


def command_create_preview(args: argparse.Namespace) -> int:
    if type(args.id) is not int or args.id <= 0:
        raise PresentonError("Preview creation id must be a positive integer")
    print_status("Creating a shareable presentation preview")
    response = request_json(
        "/api/v3/export/html-to-any/create-preview",
        {"id": args.id},
        timeout=SEARCH_TIMEOUT_SECONDS,
    )
    print_response_message(response)
    preview_url = (
        valid_web_url(response.get("url"))
        if isinstance(response, dict)
        else None
    )
    if preview_url is None:
        raise PresentonError(
            "Preview response did not contain a valid HTTP or HTTPS URL"
        )
    print_status("Shareable presentation preview URL is ready")
    print(preview_url)
    return 0


def command_list_fonts(args: argparse.Namespace) -> int:
    try:
        html_path = args.html.expanduser().resolve(strict=True)
        temp_root = get_temp_root()
        relative_path = html_path.relative_to(temp_root)
        if len(relative_path.parts) < 2 or not relative_path.parts[0].startswith("presenton-"):
            raise ValueError
        owned_temp_dir = temp_root / relative_path.parts[0]
        resolve_owned_temp_dir(owned_temp_dir)
        html = html_path.read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:
        raise PresentonError(
            "Presentation HTML must be inside a directory created by create-temp"
        ) from exc
    print_font_usage(html)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_temp = subparsers.add_parser(
        "create-temp", help="Create a private Presenton temporary workspace"
    )
    create_temp.set_defaults(handler=command_create_temp)

    cleanup_temp = subparsers.add_parser(
        "cleanup-temp", help="Remove a Presenton temporary workspace"
    )
    cleanup_temp.add_argument("--path", type=Path, required=True)
    cleanup_temp.set_defaults(handler=command_cleanup_temp)

    search = subparsers.add_parser("search-designs", help="Search Presenton visual designs")
    search.add_argument("--query", required=True)
    search.set_defaults(handler=command_search)

    upload_image = subparsers.add_parser(
        "upload-image",
        help="Upload a public image for use in presentation HTML",
    )
    upload_image.add_argument("--file", type=Path, required=True)
    upload_image.set_defaults(handler=command_upload_image)

    search_icons = subparsers.add_parser(
        "search-icons", help="Search public icon URLs for presentation HTML"
    )
    search_icons.add_argument("--query", required=True)
    search_icons.add_argument("--limit", type=int, default=5)
    search_icons.add_argument("--icon-type", choices=ICON_TYPES, default="bold")
    search_icons.set_defaults(handler=command_search_icons)

    export = subparsers.add_parser("export", help="Export compatible HTML")
    export.add_argument("--html", type=Path, required=True)
    export.add_argument("--format", choices=("pptx", "pdf", "png"), required=True)
    export.add_argument("--title")
    export.add_argument(
        "--json",
        action="store_true",
        help="Print a JSON object containing the export creation id and URL",
    )
    export.add_argument(
        "--design-id",
        type=int,
        help="ID of the selected design returned by search-designs",
    )
    export.set_defaults(handler=command_export)

    create_preview = subparsers.add_parser(
        "create-preview",
        help="Create a shareable preview URL from an export creation id",
    )
    create_preview.add_argument("--id", type=int, required=True)
    create_preview.set_defaults(handler=command_create_preview)

    list_fonts = subparsers.add_parser(
        "list-fonts", help="List fonts declared by a presentation HTML file"
    )
    list_fonts.add_argument("--html", type=Path, required=True)
    list_fonts.set_defaults(handler=command_list_fonts)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return args.handler(args)
    except (PresentonError, FileNotFoundError, PermissionError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
