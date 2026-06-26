#!/usr/bin/env python3
import argparse
import shutil
from datetime import datetime
from pathlib import Path


def append_manifest(manifest: Path, source: Path, target: Path, note: str | None) -> None:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if not manifest.exists():
        manifest.write_text('# Archive Manifest\n\n', encoding='utf-8')
    with manifest.open('a', encoding='utf-8') as fh:
        fh.write(f'## {timestamp}\n\n')
        fh.write(f'- moved: `{source}`\n')
        fh.write(f'- to: `{target}`\n')
        if note:
            fh.write(f'- note: {note}\n')
        fh.write('\n')


def main() -> None:
    ap = argparse.ArgumentParser(description='Move a stale path into an archive and append a manifest entry.')
    ap.add_argument('--source', required=True)
    ap.add_argument('--archive-root', required=True)
    ap.add_argument('--label', required=True, help='Target folder/file name inside the archive root')
    ap.add_argument('--note')
    args = ap.parse_args()

    source = Path(args.source)
    archive_root = Path(args.archive_root)
    target = archive_root / args.label
    manifest = archive_root / 'MANIFEST.md'

    if not source.exists() and not source.is_symlink():
        raise SystemExit(f'Source does not exist: {source}')
    if target.exists():
        raise SystemExit(f'Target already exists: {target}')

    archive_root.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(target))
    append_manifest(manifest, source, target, args.note)
    print(f'Moved {source} -> {target}')
    print(f'Updated manifest: {manifest}')


if __name__ == '__main__':
    main()
