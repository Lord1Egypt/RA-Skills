"""
PaddleOCR Document Parser — AMD Radeon Cloud Edition

CLI wrapper for the PaddleOCR document parsing library,
pre-configured for AMD Radeon Cloud free PaddleOCR-VL 1.5 service.

Usage:
    uv run scripts/layout_caller.py --file-url "URL"
    uv run scripts/layout_caller.py --file-path "document.pdf"
    uv run scripts/layout_caller.py --file-path "doc.pdf" --pretty
"""

# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "httpx==0.28.1",
# ]
# ///

import argparse
import base64
import io
import json
import sys
from pathlib import Path
from typing import Optional
from urllib.parse import unquote, urlparse

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# Add scripts dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from lib import parse_document


def _read_as_base64(file_path: str) -> str:
    """Read a local file and return its base64 encoding."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if path.stat().st_size == 0:
        raise ValueError(f"File is empty (0 bytes): {file_path}")
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def _fetch_as_base64(url: str) -> str:
    """Download a file from a URL and return its base64 encoding."""
    import httpx
    from lib import _http_timeout_from_env, DEFAULT_TIMEOUT

    timeout = _http_timeout_from_env("PADDLEOCR_DOC_PARSING_TIMEOUT", float(DEFAULT_TIMEOUT))
    with httpx.Client(timeout=timeout) as client:
        resp = client.get(url)
        resp.raise_for_status()
    return base64.b64encode(resp.content).decode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="PaddleOCR Document Parsing (AMD Radeon Cloud) - with layout analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  # Parse document from URL (JSON output to stdout)
  uv run scripts/layout_caller.py --file-url "https://example.com/document.pdf" --pretty

  # Parse local file (JSON output to stdout)
  uv run scripts/layout_caller.py --file-path "./invoice.pdf" --pretty

  # Save result to a file
  uv run scripts/layout_caller.py --file-url "URL" --output "./result.json" --pretty

Exit codes:
  0   Success (ok=true in JSON output)
  1   Parse or API error (ok=false in JSON output; see error.code and error.message)
  5   Cannot write result to output file

Configuration:
  Required: PADDLEOCR_DOC_PARSING_API_URL (AMD Radeon Cloud endpoint)
  Optional: PADDLEOCR_DOC_PARSING_TIMEOUT
        """,
    )

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--file-url", help="URL to document (PDF, PNG, JPG, etc.)")
    input_group.add_argument("--file-path", help="Local file path")

    # Optional input options
    parser.add_argument(
        "--file-type",
        type=int,
        choices=[0, 1],
        help="Optional file type override (0=PDF, 1=Image)",
    )

    # Output options
    parser.add_argument(
        "--pretty", action="store_true", help="Pretty-print JSON output"
    )
    parser.add_argument(
        "--output",
        "-o",
        metavar="FILE",
        help="Save result to a JSON file (default: print to stdout)",
    )

    args = parser.parse_args()

    # Read and encode file content
    try:
        if args.file_url:
            file_data = _fetch_as_base64(args.file_url)
        else:
            file_data = _read_as_base64(args.file_path)
    except (FileNotFoundError, ValueError) as e:
        print(json.dumps({"ok": False, "text": "", "result": None,
                          "error": {"code": "INPUT_ERROR", "message": str(e)}}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"ok": False, "text": "", "result": None,
                          "error": {"code": "INPUT_ERROR", "message": str(e)}}))
        sys.exit(1)

    result = parse_document(
        file_data=file_data,
        file_source=args.file_url or args.file_path,
        file_type=args.file_type,
        useDocUnwarping=False,
        useDocOrientationClassify=False,
        visualize=False,
    )

    indent = 2 if args.pretty else None
    json_output = json.dumps(result, indent=indent, ensure_ascii=False)

    if args.output:
        output_path = Path(args.output).expanduser().resolve()
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json_output, encoding="utf-8")
            print(f"Result saved to: {output_path}", file=sys.stderr)
        except (PermissionError, OSError) as e:
            print(f"Error: Cannot write to {output_path}: {e}", file=sys.stderr)
            sys.exit(5)
    else:
        print(json_output)

    sys.exit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    main()
