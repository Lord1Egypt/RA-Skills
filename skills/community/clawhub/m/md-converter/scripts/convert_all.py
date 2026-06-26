#!/usr/bin/env python3
"""Convert a Markdown file to all three formats: HTML, DOCX, PDF.

Usage:
    python3 convert_all.py <input.md> [output_dir]
    If output_dir is omitted, uses the same directory as the input file.

Dependencies: pip install python-docx reportlab
"""

import sys
import os
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def run_script(script_name, *args):
    script_path = os.path.join(SCRIPT_DIR, script_name)
    cmd = [sys.executable, script_path] + list(args)
    print(f'  Running: {" ".join(cmd)}')
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f'  ERROR: {result.stderr.strip()}')
        return False
    print(f'  OK: {result.stdout.strip()}')
    return True


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_path = os.path.abspath(sys.argv[1])
    if not os.path.exists(input_path):
        print(f'ERROR: File not found: {input_path}', file=sys.stderr)
        sys.exit(1)

    out_dir = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.dirname(input_path)
    os.makedirs(out_dir, exist_ok=True)

    base = os.path.splitext(os.path.basename(input_path))[0]

    targets = [
        ('md_to_html.py', os.path.join(out_dir, f'{base}.html')),
        ('md_to_docx.py', os.path.join(out_dir, f'{base}.docx')),
        ('md_to_pdf.py',  os.path.join(out_dir, f'{base}.pdf')),
    ]

    print(f'\nConverting: {input_path}')
    print(f'Output dir: {out_dir}\n')

    success = True
    for script, out_path in targets:
        print(f'[{os.path.splitext(out_path)[1]}] ', end='')
        if not run_script(script, input_path, out_path):
            success = False

    print()
    if success:
        print('All formats generated successfully!')
    else:
        print('Some conversions failed. Check errors above.', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
