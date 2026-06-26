#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from pathlib import Path


def _bootstrap() -> None:
    scripts_dir = Path(__file__).resolve().parent
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    workspace_root = scripts_dir.parents[2]
    venv_site = workspace_root / '.venv-mail-invoice' / 'lib'
    if venv_site.exists():
        candidates = sorted(venv_site.glob('python*/site-packages'))
        for candidate in reversed(candidates):
            if str(candidate) not in sys.path:
                sys.path.insert(0, str(candidate))
                break
    os.environ.setdefault('PATH', os.environ.get('PATH', ''))


def main() -> int:
    _bootstrap()
    from mail_invoice_archiver.cli import main as inner_main

    return inner_main()


if __name__ == "__main__":
    raise SystemExit(main())
