#!/usr/bin/env python3
"""
Stage 2: Inject verified metadata into manifest.

Usage:
  1. Edit VERIFIED_DATA dict below (key=filename, value={title,year,venue})
  2. Run: python apply_verified.py "<folder>"
  3. Review preview, then execute with execute.py --execute
"""
import os, re, json

MANIFEST_IN  = os.path.join(os.path.dirname(__file__), 'manifest.json')
MANIFEST_OUT = os.path.join(os.path.dirname(__file__), 'manifest_verified.json')

# ============================================================
# Verified data — fill this in after web search verification
# Format: { 'original_filename.pdf': { 'title':..., 'year':..., 'venue':..., 'confirmed': True/False } }
# Set 'confirmed': False or omit to skip the file
# ============================================================
VERIFIED_DATA = {
    # Example:
    # 'paper.pdf': {
    #     'title': 'Correct Paper Title',
    #     'year': '2023',
    #     'venue': 'NeurIPS',
    #     'confirmed': True
    # },
}


def normalize_title(t):
    return re.sub(r'[^a-z0-9]', '', t.lower())


def run(folder):
    if not os.path.exists(MANIFEST_IN):
        print(f'[ERROR] {MANIFEST_IN} not found. Run extract.py first.')
        return

    with open(MANIFEST_IN, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    ready_count = 0
    skip_count = 0

    for m in manifest:
        fname = m['filename']
        vdata = VERIFIED_DATA.get(fname)

        if vdata and vdata.get('confirmed'):
            m['title'] = vdata['title']
            m['title_source'] = 'verified'
            m['year'] = vdata.get('year') or m['year']
            m['year_source'] = 'verified'
            m['venue'] = vdata.get('venue') or m['venue']
            m['venue_source'] = 'verified'
            m['status'] = 'ready'
            ready_count += 1
        else:
            if m['status'] == 'needs_verification':
                m['status'] = 'manual_review'
                skip_count += 1

    with open(MANIFEST_OUT, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f'\n[OK] Manifest saved → {MANIFEST_OUT}')
    print(f'     {ready_count} files ready to rename')
    print(f'     {skip_count} files require manual review / skipped')

    print(f'\n{"=":*>80}')
    print('Rename preview:')
    print(f'{"=":*>80}\n')
    dup_groups = {}
    for m in manifest:
        if m['status'] == 'ready':
            if m['is_duplicate']:
                grp = m['duplicate_group']
                if grp not in dup_groups:
                    dup_groups[grp] = 0
                dup_groups[grp] += 1
                counter = dup_groups[grp]
            else:
                counter = None

            base = f'[{m["year"]}]' if m['year'] else '[????]'
            venue_str = f' [{m["venue"]}]' if m['venue'] else ''
            title_str = f'{base}{venue_str} {m["title"]}'
            title_str = re.sub(r'\s+', ' ', title_str).strip()
            if counter:
                title_str += f' ({counter})'
            title_str += '.pdf'

            dup = ' [DUPLICATE]' if m['is_duplicate'] else ''
            print(f'  ✅ {m["filename"]}')
            print(f'      -> {title_str}{dup}')
            print()
        else:
            print(f'  ⚠️  {m["filename"]} -> SKIPPED ({m["status"]})')
            print()

    print(f'\nTo execute: python execute.py "{folder}" --execute')


if __name__ == '__main__':
    import sys
    folder = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    run(folder)
