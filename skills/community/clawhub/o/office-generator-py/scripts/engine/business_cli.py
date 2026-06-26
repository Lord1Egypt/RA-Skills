from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

BASE_DIR = Path(__file__).resolve().parent
PYTHON_BIN = BASE_DIR / '.venv/bin/python'
MAIN_PY = BASE_DIR / 'main.py'

TEMPLATE_BY_KIND = {
    'word-report': ('docx', 'word_work_report_v1'),
    'meeting-minutes': ('docx', 'meeting_minutes_v1'),
    'excel-tracker': ('xlsx', 'excel_data_tracker_v1'),
    'project-plan': ('xlsx', 'project_plan_v1'),
    'ppt-brief': ('pptx', 'ppt_business_brief_v1'),
    'project-status-brief': ('pptx', 'project_status_brief_v1'),
}


def main() -> int:
    parser = argparse.ArgumentParser(description='Business-friendly wrapper for office_gen_py')
    parser.add_argument('--kind', choices=sorted(TEMPLATE_BY_KIND.keys()), required=True)
    parser.add_argument('--title', required=True)
    parser.add_argument('--purpose', default='')
    parser.add_argument('--input', required=True, help='JSON file containing contentSpec override')
    parser.add_argument('--out', required=True)
    args = parser.parse_args()

    doc_type, template_id = TEMPLATE_BY_KIND[args.kind]
    with open(args.input, 'r', encoding='utf-8') as f:
        payload: Dict[str, Any] = json.load(f)

    request = {
        'documentType': doc_type,
        'templateId': template_id,
        'title': args.title,
        'purpose': args.purpose,
        'contentSpec': payload.get('contentSpec', payload),
        'output': {'filename': Path(args.out).name, 'directory': str(Path(args.out).parent or '.')},
    }

    temp_path = Path(args.out).with_suffix(Path(args.out).suffix + '.request.json')
    temp_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path.write_text(json.dumps(request, ensure_ascii=False, indent=2), encoding='utf-8')

    try:
        python_bin = str(PYTHON_BIN if PYTHON_BIN.exists() else Path(sys.executable))
        cmd = [python_bin, str(MAIN_PY), '--type', doc_type, '--input', str(temp_path), '--out', args.out]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(result.stderr.strip())
            return result.returncode
        print(result.stdout.strip())
        return 0
    finally:
        if temp_path.exists():
            temp_path.unlink()


if __name__ == '__main__':
    raise SystemExit(main())
