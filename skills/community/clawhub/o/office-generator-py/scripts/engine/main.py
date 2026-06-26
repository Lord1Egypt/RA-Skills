from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from generators.docx_generator import generate_docx
from generators.xlsx_generator import generate_xlsx
from generators.pptx_generator import generate_pptx
from schemas.common_schema import validate_request
from template_loader import deep_merge, load_template


def load_request(path: str) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def resolve_request(data: Dict[str, Any]) -> Dict[str, Any]:
    template_id = data.get('templateId')
    if template_id:
        template = load_template(template_id)
        data = deep_merge(template, data)
    validated = validate_request(data)
    return validated.model_dump()


def infer_output_path(doc_type: str, req: Dict[str, Any]) -> Path:
    filename = req.get('output', {}).get('filename') or f"sample.{doc_type}"
    directory = req.get('output', {}).get('directory') or 'output'
    return Path(directory) / filename


def main() -> int:
    parser = argparse.ArgumentParser(description='Generate Office documents from JSON spec')
    parser.add_argument('--type', choices=['docx', 'xlsx', 'pptx'], required=True)
    parser.add_argument('--input', required=True, help='Path to input JSON')
    parser.add_argument('--out', help='Output path override')
    args = parser.parse_args()

    raw_req = load_request(args.input)
    req = resolve_request(raw_req)
    out_path = Path(args.out) if args.out else infer_output_path(args.type, req)

    if req.get('documentType') != args.type:
        raise ValueError(f"documentType mismatch: input={req.get('documentType')} cli={args.type}")

    if args.type == 'docx':
        result = generate_docx(req, str(out_path))
    elif args.type == 'xlsx':
        result = generate_xlsx(req, str(out_path))
    else:
        result = generate_pptx(req, str(out_path))

    print(result)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
