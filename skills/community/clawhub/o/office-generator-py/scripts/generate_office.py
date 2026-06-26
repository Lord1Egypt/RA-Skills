#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ENGINE_DIR = SCRIPT_DIR / 'engine'
STANDARD_MAIN = ENGINE_DIR / 'main.py'
BUSINESS_MAIN = ENGINE_DIR / 'business_cli.py'
DEFAULT_VENV_PYTHON = ENGINE_DIR / '.venv/bin/python'


def resolve_python_bin() -> str:
    env_override = os.environ.get('OFFICE_GENERATOR_PYTHON', '').strip()
    if env_override:
        return env_override
    if DEFAULT_VENV_PYTHON.exists():
        return str(DEFAULT_VENV_PYTHON)
    return str(Path(sys.executable))


def run(cmd: list[str]) -> int:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip(), file=sys.stderr)
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description='Wrapper for bundled office generator engine')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--type', choices=['docx', 'xlsx', 'pptx'])
    mode.add_argument('--kind', choices=[
        'word-report', 'meeting-minutes', 'excel-tracker', 'project-plan', 'ppt-brief', 'project-status-brief'
    ])
    parser.add_argument('--title')
    parser.add_argument('--purpose', default='')
    parser.add_argument('--input', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()

    python_bin = resolve_python_bin()

    if args.type:
        cmd = [python_bin, str(STANDARD_MAIN), '--type', args.type, '--input', args.input, '--out', args.out]
        return run(cmd)

    if not args.title:
        parser.error('--title is required when using --kind')
    cmd = [
        python_bin,
        str(BUSINESS_MAIN),
        '--kind',
        args.kind,
        '--title',
        args.title,
        '--purpose',
        args.purpose,
        '--input',
        args.input,
        '--out',
        args.out,
    ]
    return run(cmd)


if __name__ == '__main__':
    raise SystemExit(main())
