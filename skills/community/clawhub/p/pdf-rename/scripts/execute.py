#!/usr/bin/env python3
"""
Stage 3: Execute rename from manifest.

Usage:
  python execute.py "<folder>" --preview   # dry run
  python execute.py "<folder>" --execute   # actual rename (creates backup)
"""
import os, re, json, shutil
from datetime import datetime

MANIFEST_IN = os.path.join(os.path.dirname(__file__), 'manifest_verified.json')
MANIFEST_FALLBACK = os.path.join(os.path.dirname(__file__), 'manifest.json')


def sanitize(name):
    return re.sub(r'[<>:"/\\|?*]', ' ', name).strip()


def build_filename(m, counter=None):
    year_str = f'[{m["year"]}]' if m.get('year') else '[????]'
    venue_str = f'[{m["venue"]}]' if m.get('venue') else ''
    title = sanitize(m.get('title', m['filename'].replace('.pdf', '')))
    name = f'{year_str} {venue_str} {title}'.strip()
    name = re.sub(r'\s+', ' ', name)
    if counter:
        name = f'{name} ({counter})'
    return name + '.pdf'


def run(folder, dry_run=True):
    # Load manifest (prefer verified, fallback to auto)
    manifest_path = MANIFEST_IN if os.path.exists(MANIFEST_IN) else MANIFEST_FALLBACK
    if not os.path.exists(manifest_path):
        print(f'[ERROR] No manifest found. Run extract.py first.')
        return
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    ready = [m for m in manifest if m.get('status') == 'ready']
    skipped = [m for m in manifest if m.get('status') != 'ready']

    if dry_run:
        print(f'\n[DRY RUN] {len(ready)} files to rename, {len(skipped)} skipped\n')
    else:
        backup_dir = os.path.join(folder, f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        os.makedirs(backup_dir, exist_ok=True)
        print(f'\n[BACKUP] {backup_dir}\n')

    # Assign duplicate counters
    dup_counters = {}
    for m in ready:
        if m.get('is_duplicate') and m.get('duplicate_group'):
            grp = m['duplicate_group']
            dup_counters[grp] = dup_counters.get(grp, 0) + 1

    dup_current = {}
    errors = []

    for m in ready:
        new_name = build_filename(m, counter=dup_counters.get(m['duplicate_group']) if m.get('is_duplicate') else None)
        dst = os.path.join(folder, new_name)

        # Handle name collisions
        base, ext = os.path.splitext(new_name)
        counter = 1
        while os.path.exists(dst) and os.path.abspath(dst) != os.path.abspath(m['filepath']):
            new_name = f'{base} ({counter}){ext}'
            dst = os.path.join(folder, new_name)
            counter += 1

        if dry_run:
            print(f'  {m["filename"]}')
            print(f'    -> {new_name}')
            print()
        else:
            try:
                shutil.copy2(m['filepath'], os.path.join(backup_dir, m['filename']))
                shutil.move(m['filepath'], dst)
                print(f'  ✅ {m["filename"]} -> {new_name}')
            except Exception as e:
                errors.append((m['filename'], str(e)))
                print(f'  ❌ {m["filename"]} -> FAILED: {e}')

    if skipped:
        print(f'\n[{len(skipped)} skipped files]:')
        for m in skipped:
            print(f'  - {m["filename"]} ({m.get("status", "unknown")})')

    if errors:
        print(f'\n[{len(errors)} errors]')
        for fn, err in errors:
            print(f'  - {fn}: {err}')

    if not dry_run:
        print(f'\n[Done] {len(ready) - len(errors)} files renamed.')


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print('Usage: python execute.py "<folder>" [--preview|--execute]')
        sys.exit(1)
    folder = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else '--preview'
    dry_run = (mode != '--execute')
    run(folder, dry_run=dry_run)
