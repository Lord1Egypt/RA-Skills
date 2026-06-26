#!/usr/bin/env python3
import argparse
import base64
from pathlib import Path
from xml.sax.saxutils import escape


def main():
    parser = argparse.ArgumentParser(
        description="Build Base64 XML payload for PDFelement PDFToolbox -f option."
    )
    parser.add_argument("files", nargs="+", help="Absolute file paths to preload")
    parser.add_argument(
        "--password",
        action="append",
        default=[],
        help="Optional password for the corresponding file; repeat in file order",
    )
    args = parser.parse_args()

    passwords = args.password + [""] * max(0, len(args.files) - len(args.password))

    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<Files>']
    for file_path, password in zip(args.files, passwords):
        resolved = Path(file_path)
        if not resolved.is_absolute():
            raise SystemExit(f"File path must be absolute: {file_path}")
        xml_lines.extend(
            [
                '  <File>',
                f'    <Path>{escape(str(resolved))}</Path>',
                f'    <Password>{escape(password)}</Password>',
                '  </File>',
            ]
        )
    xml_lines.append('</Files>')

    xml = "\n".join(xml_lines)
    encoded = base64.b64encode(xml.encode("utf-8")).decode("ascii")
    print(encoded)


if __name__ == "__main__":
    main()
