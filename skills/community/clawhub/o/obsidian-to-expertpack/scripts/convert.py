#!/usr/bin/env python3
"""
obsidian-to-expertpack: Convert an Obsidian Vault to an ExpertPack.

Creates a COPY of the vault restructured as an EP — never modifies the source.
"""

import argparse
import os
import re
import shutil
import sys
import yaml
from datetime import datetime, timezone

def utcnow():
    return datetime.now(timezone.utc)
from pathlib import Path

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

OBSIDIAN_TAG_RE = re.compile(r'(?<!\[)#([A-Za-z][A-Za-z0-9_/-]*)')
DATAVIEW_BLOCK_RE = re.compile(r'```dataview.*?```', re.DOTALL)
DATAVIEW_INLINE_RE = re.compile(r'`=\s*[^`]+`')
FRONTMATTER_RE = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)
H1_RE = re.compile(r'^#\s+(.+)', re.MULTILINE)
WIKILINK_RE = re.compile(r'\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]')
MD_LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+\.md)([^)]*)\)')

CONTENT_TYPE_MAP = {
    'concepts': 'concept',
    'concept': 'concept',
    'ideas': 'concept',
    'notes': 'note',
    'note': 'note',
    'daily': 'journal',
    'journal': 'journal',
    'journals': 'journal',
    'people': 'person',
    'person': 'person',
    'persons': 'person',
    'contacts': 'person',
    'projects': 'project',
    'project': 'project',
    'tasks': 'task',
    'task': 'task',
    'references': 'reference',
    'reference': 'reference',
    'resources': 'reference',
    'workflows': 'workflow',
    'workflow': 'workflow',
    'processes': 'workflow',
    'meetings': 'meeting',
    'meeting': 'meeting',
    'research': 'research',
}

PREFIX_MAP = {
    'concept': 'facts-',
    'note': 'facts-',
    'journal': 'meta-',
    'person': 'rel-',
    'project': 'facts-',
    'task': 'facts-',
    'reference': 'facts-',
    'workflow': 'facts-',
    'meeting': 'meta-',
    'research': 'facts-',
    'summary': 'sum-',
    'mind': 'mind-',
    'presentation': 'pres-',
    'verbatim': 'vbt-',
    'proposition': 'prop-',
}

# Directories excluded from markdown walk (content processing).
# Note: .obsidian is excluded here to prevent processing its JSON files as content,
# but it IS copied separately at the end via shutil.copytree to preserve Obsidian config.
IGNORED_DIRS = {'.obsidian', '.trash', '.git', '__pycache__'}
IGNORED_FILES = {'.DS_Store', 'Thumbs.db'}


def load_yaml_front(text):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    try:
        data = yaml.safe_load(m.group(1)) or {}
    except Exception:
        data = {}
    body = text[m.end():]
    return data, body


def dump_yaml_front(fm, body):
    return '---\n' + yaml.dump(fm, default_flow_style=False, allow_unicode=True) + '---\n' + body


def infer_title(fm, body, stem):
    if fm.get('title'):
        return fm['title']
    m = H1_RE.search(body)
    if m:
        return m.group(1).strip()
    return stem.replace('-', ' ').replace('_', ' ').title()


def extract_inline_tags(body):
    """Extract #hashtags from body text, return (tags_list, cleaned_body)."""
    tags = []
    def replacer(m):
        tag = m.group(1)
        tags.append(tag.replace('/', '-').lower())
        return ''
    cleaned = OBSIDIAN_TAG_RE.sub(replacer, body)
    return list(set(tags)), cleaned


def strip_dataview(body):
    body = DATAVIEW_BLOCK_RE.sub('', body)
    body = DATAVIEW_INLINE_RE.sub('', body)
    return body


def md_links_to_wikilinks(body):
    """Convert [text](file.md) to [[file|text]] style wikilinks."""
    def replacer(m):
        text, path, anchor = m.group(1), m.group(2), m.group(3)
        stem = Path(path).stem
        if text == stem:
            return f'[[{stem}]]'
        return f'[[{stem}|{text}]]'
    return MD_LINK_RE.sub(replacer, body)


def infer_pack_type(vault_path):
    """
    Heuristic pack type inference from vault structure.
    Returns one of: person, product, process, composite
    """
    dirs = {p.name.lower() for p in vault_path.iterdir() if p.is_dir() and p.name not in IGNORED_DIRS}
    person_signals = {'journal', 'journals', 'daily', 'people', 'contacts', 'relationships', 'mind', 'stories'}
    product_signals = {'concepts', 'workflows', 'interfaces', 'troubleshooting', 'faq', 'features'}
    process_signals = {'phases', 'decisions', 'checklists', 'steps', 'procedures'}

    scores = {'person': 0, 'product': 0, 'process': 0}
    for d in dirs:
        if d in person_signals:
            scores['person'] += 1
        if d in product_signals:
            scores['product'] += 1
        if d in process_signals:
            scores['process'] += 1

    best = max(scores, key=lambda k: scores[k])
    if scores[best] == 0:
        return 'product'  # safe default
    if sum(1 for v in scores.values() if v > 0) >= 2:
        return 'composite'
    return best


def build_manifest(pack_slug, pack_name, pack_type, dirs):
    return {
        'schema_version': '2.9',
        'slug': pack_slug,
        'name': pack_name,
        'type': pack_type,
        'version': '1.0.0',
        'created': utcnow().strftime('%Y-%m-%d'),
        'description': f'ExpertPack converted from Obsidian Vault: {pack_name}',
        'context_tiers': {
            'tier1_always': ['manifest.yaml', 'overview.md', 'glossary.md'],
            'tier2_searchable': [f'{d}/' for d in dirs],
            'tier3_on_demand': [],
        },
        'ek_ratio': {
            'value': None,
            'measured_at': None,
            'note': 'Run expertpack-eval to measure EK ratio after conversion.',
        },
    }


def build_overview(pack_name, pack_type, stats, warnings):
    lines = [
        f'# {pack_name}',
        '',
        f'> Converted from Obsidian Vault on {utcnow().strftime("%Y-%m-%d")}.',
        '',
        '## Pack Summary',
        '',
        f'- **Type:** {pack_type}',
        f'- **Files converted:** {stats["converted"]}',
        f'- **Directories:** {stats["dirs"]}',
        f'- **Tags extracted:** {stats["tags"]}',
        f'- **Dataview blocks removed:** {stats["dataview"]}',
        f'- **MD links converted to wikilinks:** {stats["wikilinks"]}',
        '',
        '## Contents',
        '',
        'See `_index.md` files in each directory for navigable content lists.',
        '',
    ]
    if warnings:
        lines += ['## Warnings', '']
        for w in warnings:
            lines.append(f'- {w}')
        lines.append('')
    lines += [
        '## Next Steps',
        '',
        '1. Review frontmatter on converted files — especially `type` and `tags`',
        '2. Add lead summaries to high-traffic files (1-3 sentence blockquote at top)',
        '3. Create `propositions/` and `summaries/` directories for retrieval optimization',
        '4. Run `ep-validate` to check for 0 errors',
        '5. Run `expertpack-eval` to measure EK ratio',
        '6. Configure RAG in `openclaw.json` pointing at this pack directory',
        '',
        '## RAG Configuration',
        '',
        '```json',
        '{',
        '  "agents": {',
        '    "defaults": {',
        '      "memorySearch": {',
        '        "extraPaths": ["path/to/this/pack"],',
        '        "chunking": { "tokens": 500, "overlap": 0 }',
        '      }',
        '    }',
        '  }',
        '}',
        '```',
    ]
    return '\n'.join(lines) + '\n'


def build_index(dir_name, files):
    lines = [f'# {dir_name.replace("-", " ").title()} Index', '']
    for f in sorted(files):
        stem = f.stem
        lines.append(f'- [[{stem}]]')
    return '\n'.join(lines) + '\n'


def convert_file(src_path, dest_path, pack_slug, content_type, stats, warnings):
    try:
        raw = src_path.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        warnings.append(f'Could not read {src_path.name}: {e}')
        return

    fm, body = load_yaml_front(raw)

    # Strip Dataview
    before = body
    body = strip_dataview(body)
    dv_removed = before != body
    if dv_removed:
        stats['dataview'] += 1

    # Extract inline #tags → frontmatter
    inline_tags, body = extract_inline_tags(body)

    # Convert markdown links → wikilinks
    before = body
    body = md_links_to_wikilinks(body)
    if before != body:
        stats['wikilinks'] += 1

    # Merge tags
    existing_tags = fm.get('tags', [])
    if isinstance(existing_tags, str):
        existing_tags = [existing_tags]
    all_tags = list(set(existing_tags + inline_tags))

    # Infer title
    title = infer_title(fm, body, src_path.stem)

    # Build EP frontmatter
    fm['title'] = title
    fm['type'] = fm.get('type') or content_type
    fm['tags'] = all_tags
    fm['pack'] = pack_slug
    if 'created' not in fm:
        fm['created'] = utcnow().strftime('%Y-%m-%d')

    # Clean up Obsidian-specific frontmatter keys we don't need
    for key in ['cssclass', 'cssclasses', 'banner', 'banner_x', 'banner_y']:
        fm.pop(key, None)

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(dump_yaml_front(fm, body), encoding='utf-8')
    stats['converted'] += 1


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Convert an Obsidian Vault to an ExpertPack.')
    parser.add_argument('vault', help='Path to source Obsidian Vault')
    parser.add_argument('--output', required=True, help='Output directory for the ExpertPack')
    parser.add_argument('--name', help='Human-readable pack name (default: vault folder name)')
    parser.add_argument('--type', choices=['auto', 'person', 'product', 'process', 'composite'],
                        default='auto', help='Pack type (default: auto-detect)')
    parser.add_argument('--dry-run', action='store_true', help='Preview without writing files')
    args = parser.parse_args()

    vault_path = Path(args.vault).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    if not vault_path.exists():
        print(f'ERROR: Vault not found: {vault_path}', file=sys.stderr)
        sys.exit(1)

    if output_path.exists():
        print(f'ERROR: Output directory already exists: {output_path}', file=sys.stderr)
        print('Remove it first or choose a different --output path.', file=sys.stderr)
        sys.exit(1)

    pack_name = args.name or vault_path.name
    pack_slug = re.sub(r'[^a-z0-9]+', '-', pack_name.lower()).strip('-')

    # Infer pack type
    if args.type == 'auto':
        pack_type = infer_pack_type(vault_path)
        print(f'Auto-detected pack type: {pack_type}')
    else:
        pack_type = args.type

    print(f'Converting: {vault_path}')
    print(f'Output:     {output_path}')
    print(f'Pack type:  {pack_type}')
    print(f'Dry run:    {args.dry_run}')
    print()

    stats = {'converted': 0, 'dirs': 0, 'tags': 0, 'dataview': 0, 'wikilinks': 0}
    warnings = []
    all_tags_global = set()
    dir_files_map = {}  # dir_name -> [Path]

    # Walk vault
    for root, dirs, files in os.walk(vault_path):
        # Prune ignored dirs in-place
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        rel_root = Path(root).relative_to(vault_path)
        dir_name = rel_root.parts[0] if rel_root.parts else '_root'
        content_type = CONTENT_TYPE_MAP.get(dir_name.lower(), 'note')

        md_files = [f for f in files if f.endswith('.md') and f not in IGNORED_FILES]
        if not md_files:
            continue

        for fname in md_files:
            src = Path(root) / fname
            rel = src.relative_to(vault_path)
            dest = output_path / rel

            # Track for index
            dest_dir_key = str(rel_root) if rel_root.parts else '_root'
            dir_files_map.setdefault(dest_dir_key, []).append(dest)

            if not args.dry_run:
                convert_file(src, dest, pack_slug, content_type, stats, warnings)
            else:
                stats['converted'] += 1
                print(f'  [dry] {rel}')

    stats['dirs'] = len(dir_files_map)

    if not args.dry_run:
        # Write _index.md per directory
        for dir_key, files in dir_files_map.items():
            if dir_key == '_root':
                continue
            idx_path = output_path / dir_key / '_index.md'
            idx_path.parent.mkdir(parents=True, exist_ok=True)
            idx_path.write_text(build_index(dir_key, files), encoding='utf-8')

        # manifest.yaml
        manifest = build_manifest(pack_slug, pack_name, pack_type, list(dir_files_map.keys()))
        manifest_path = output_path / 'manifest.yaml'
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(yaml.dump(manifest, default_flow_style=False, allow_unicode=True), encoding='utf-8')

        # overview.md
        overview_path = output_path / 'overview.md'
        overview_path.write_text(build_overview(pack_name, pack_type, stats, warnings), encoding='utf-8')

        # glossary.md stub
        glossary_path = output_path / 'glossary.md'
        glossary_path.write_text(
            '# Glossary\n\n'
            '> Auto-generated stub. Add domain-specific terms and definitions here.\n\n'
            '<!-- Add entries: **Term** — definition. -->\n',
            encoding='utf-8'
        )

        # Copy .obsidian config directory as-is (not processed as markdown content above).
        # This gives the output pack immediate Obsidian compatibility — open the output
        # folder in Obsidian and it inherits all plugins, themes, and Dataview settings.
        obsidian_src = vault_path / '.obsidian'
        if obsidian_src.exists():
            shutil.copytree(obsidian_src, output_path / '.obsidian')
            print('Copied .obsidian config.')

    print()
    print('=== Conversion Complete ===')
    print(f'  Files converted:          {stats["converted"]}')
    print(f'  Directories processed:    {stats["dirs"]}')
    print(f'  Dataview blocks removed:  {stats["dataview"]}')
    print(f'  MD links → wikilinks:     {stats["wikilinks"]}')
    if warnings:
        print(f'\nWarnings ({len(warnings)}):')
        for w in warnings:
            print(f'  ⚠ {w}')
    if not args.dry_run:
        print(f'\nOutput: {output_path}')
        print('\nNext steps:')
        print('  1. Review manifest.yaml and overview.md')
        print('  2. Run ep-validate to check for errors')
        print('  3. Run ep-doctor --apply to fix common issues')
        print('  4. Install expertpack-eval and measure EK ratio')

if __name__ == '__main__':
    main()
