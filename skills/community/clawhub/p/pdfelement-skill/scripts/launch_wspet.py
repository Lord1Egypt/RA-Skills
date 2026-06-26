#!/usr/bin/env python3
"""
PDFToolbox wspet:// Protocol Launcher
Generates wspet:// URLs for launching PDFToolbox with parameters on Windows.

This helper always appends the required OpenClaw flags for every command:
- -wsclaw
- -autoexec
- -entrance OpenClaw (unless overridden)
"""

import argparse
import base64
import os
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from typing import List, Optional


def build_files_xml(file_paths: List[str], password: str = "") -> str:
    """Build the XML structure for the file list parameter."""
    root = ET.Element("Files")

    for file_path in file_paths:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_elem = ET.SubElement(root, "File")
        path_elem = ET.SubElement(file_elem, "Path")
        path_elem.text = os.path.abspath(file_path)
        password_elem = ET.SubElement(file_elem, "Password")
        password_elem.text = password

    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="unicode")


def build_wspet_url(
    command: str,
    target_format: Optional[str] = None,
    files: Optional[List[str]] = None,
    password: str = "",
    entrance: str = "OpenClaw",
) -> str:
    """Build a wspet:// protocol URL with encoded parameters."""
    params = command

    if target_format and command == "convert":
        params += f" -t {target_format}"

    if files:
        files_xml = build_files_xml(files, password)
        base64_files = base64.b64encode(files_xml.encode("utf-8")).decode("ascii")
        params += f" -f {base64_files}"

    params += f" -wsclaw -autoexec -entrance {entrance}"

    base64_param = base64.b64encode(params.encode("utf-8")).decode("ascii")
    escaped_param = urllib.parse.quote(base64_param, safe="")
    return f"wspet://param={escaped_param}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate wspet:// URLs for PDFToolbox operations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s convert --format .docx --files input.pdf
  %(prog)s optimize --files large.pdf
  %(prog)s ocr --files scanned.pdf
  %(prog)s translate --files document.pdf
        """,
    )

    parser.add_argument(
        "command",
        choices=[
            "convert", "ocr", "optimize", "translate", "watermark", "background",
            "headerFooter", "batesNumber", "security", "batchPrint", "dataExtract",
            "deleteBlankPages", "sign", "split", "combine", "crop", "create",
        ],
        help="PDFToolbox command to execute",
    )

    parser.add_argument(
        "--format", "-t",
        help="Target format for convert command (e.g., .docx, .xlsx, .jpg)",
    )

    parser.add_argument(
        "--files", "-f",
        nargs="+",
        help="PDF file(s) to process",
    )

    parser.add_argument(
        "--password", "-p",
        default="",
        help="Password for protected PDFs",
    )

    parser.add_argument(
        "--entrance", "-e",
        default="OpenClaw",
        help="Entry point identifier (default: OpenClaw)",
    )

    parser.add_argument(
        "--output", "-o",
        choices=["url", "powershell", "cmd", "all"],
        default="url",
        help="Output format (default: url)",
    )

    args = parser.parse_args()

    try:
        url = build_wspet_url(
            command=args.command,
            target_format=args.format,
            files=args.files,
            password=args.password,
            entrance=args.entrance,
        )
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.output in {"url", "all"}:
        print("wspet:// URL:")
        print(url)
        print()

    if args.output in {"powershell", "all"}:
        print("PowerShell command:")
        print(f'Start-Process "{url}"')
        print()

    if args.output in {"cmd", "all"}:
        print("CMD command:")
        print(f'start {url}')
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
