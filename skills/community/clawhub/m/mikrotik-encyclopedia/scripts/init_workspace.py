#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

SEED_FILES = {
    'inventory/access.md': '# MikroTik Access Inventory\n\nStore MikroTik device access notes here.\n',
    'inventory/topology.md': '# MikroTik Topology\n\nStore environment-specific MikroTik topology notes here.\n',
    'inventory/doc-index.md': '# MikroTik Cached Doc Index\n\nTrack especially useful cached official-doc pages here when helpful.\n',
    'notes/devices/.gitkeep': '',
    'notes/patterns/.gitkeep': '',
    'docs/help.mikrotik.com/docs/.gitkeep': '',
}


def default_root() -> Path:
    return Path.cwd() / '.MikroTik-Encyclopedia'


def main() -> int:
    parser = argparse.ArgumentParser(description='Create/repair the .MikroTik-Encyclopedia workspace layout.')
    parser.add_argument('--root', default=str(default_root()), help='Data root to initialize (default: <cwd>/.MikroTik-Encyclopedia)')
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    for rel, content in SEED_FILES.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text(content, encoding='utf-8')
    print(root)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
