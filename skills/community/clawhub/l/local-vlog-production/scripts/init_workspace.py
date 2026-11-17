"""Initialize an empty Vlog workspace from this installed skill's text templates.

No downloads, dependency installation, source-media reads, or existing-file replacement.
Optional fonts are supplied explicitly by the user and remain outside the skill bundle.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import sys


TEXT_SUFFIXES = {'.md', '.json', '.txt', '.yaml', '.yml', '.toml', '.py'}
REQUIRED_TEMPLATES = (
    'workspace_config.json', 'workspace_state.json',
    '公共资源/style.default.json', 'examples/演示时间线.json',
    '模板/交付检查清单.md',
)


def reject_links(path: Path) -> None:
    """Check the lexical path and every existing ancestor before resolving it."""
    for node in (path, *path.parents):
        try:
            details = node.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(details.st_mode) or getattr(details, 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0x400):
            raise ValueError(f'Symlinks, junctions and other reparse points are not supported: {node}')


def absolute_without_links(value: str | Path) -> Path:
    path = Path(os.path.abspath(os.path.expanduser(str(value))))
    reject_links(path)
    return path


def read_text_file(path: Path) -> bytes:
    reject_links(path)
    if not path.is_file():
        raise ValueError(f'Not a regular file: {path}')
    if path.suffix.lower() not in TEXT_SUFFIXES and path.name != '.gitignore':
        raise ValueError(f'Unexpected non-text template file: {path.name}')
    payload = path.read_bytes()
    payload.decode('utf-8-sig')
    return payload


def collect_templates(skill_root: Path) -> dict[str, bytes]:
    template_root = skill_root / 'assets' / 'workspace'
    reject_links(template_root)
    if not template_root.is_dir():
        raise ValueError('This skill is incomplete: assets/workspace is missing.')
    plan: dict[str, bytes] = {}
    for parent, directories, files in os.walk(template_root, followlinks=False):
        parent_path = Path(parent)
        for name in directories:
            reject_links(parent_path / name)
        for name in files:
            source = parent_path / name
            relative = source.relative_to(template_root).as_posix()
            plan[relative] = read_text_file(source)
    for required in REQUIRED_TEMPLATES:
        if required not in plan:
            raise ValueError(f'This skill is incomplete: assets/workspace/{required} is missing.')
    for directory in ('tools', 'tests'):
        source_root = skill_root / directory
        reject_links(source_root)
        if not source_root.is_dir():
            raise ValueError(f'This skill is incomplete: {directory}/ is missing.')
        sources = sorted(source_root.glob('*.py'))
        if not sources:
            raise ValueError(f'This skill is incomplete: {directory}/ has no Python scripts.')
        for source in sources:
            relative = f'{directory}/{source.name}'
            if relative in plan:
                raise ValueError(f'Duplicate template output: {relative}')
            plan[relative] = read_text_file(source)
    return plan


def supplied_font(value: str | None, role: str) -> tuple[str, bytes] | None:
    if value is None:
        return None
    source = absolute_without_links(value)
    if not source.is_file() or source.suffix.lower() not in ('.ttf', '.otf'):
        raise ValueError(f'--{role}-font must name an existing regular TTF or OTF file.')
    payload = source.read_bytes()
    if payload[:4] not in (b'\x00\x01\x00\x00', b'OTTO', b'true', b'typ1'):
        raise ValueError(f'--{role}-font does not have a recognized TTF/OTF header.')
    filename = 'BodyFont' if role == 'body' else 'TitleFont'
    return f'公共资源/字体/用户字体/{filename}{source.suffix.lower()}', payload


def update_font_references(plan: dict[str, bytes], body, title) -> dict:
    """Do not imply that an unavailable bundled font exists."""
    for font in (body, title):
        if font:
            if font[0] in plan:
                raise ValueError(f'Duplicate font output: {font[0]}')
            plan[font[0]] = font[1]
    body_path = body[0] if body else title[0] if title else None
    title_path = title[0] if title else body_path
    style_key = '公共资源/style.default.json'
    style = json.loads(plan[style_key].decode('utf-8-sig'))
    style['font_candidates'] = list(dict.fromkeys(p for p in (body_path, title_path) if p))
    style['font_roles'] = {'body': body_path, 'title': title_path}
    style['fonts_ready'] = bool(body_path)
    style['font_note'] = 'User-supplied local fonts; inspect Chinese glyph coverage and usage rights. No fonts downloaded or installed.'
    plan[style_key] = (json.dumps(style, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    timeline_key = 'examples/演示时间线.json'
    timeline = json.loads(plan[timeline_key].decode('utf-8-sig'))
    def replace(value):
        if isinstance(value, dict):
            if 'font' in value:
                chosen = title_path if value.get('type') == 'sticker_title' else body_path
                # Deliberately absent until a font is supplied; validate-only then reports the missing input.
                value['font'] = chosen or '公共资源/字体/待提供中文字体.ttf'
            for child in value.values():
                replace(child)
        elif isinstance(value, list):
            for child in value:
                replace(child)
    replace(timeline)
    plan[timeline_key] = (json.dumps(timeline, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    return {
        'font_files_supplied': len([font for font in (body, title) if font]),
        'font_roles': {'body': body_path, 'title': title_path},
        'glyph_coverage_checked': False,
        'font_files': [{'path': font[0], 'sha256': hashlib.sha256(font[1]).hexdigest()} for font in (body, title) if font],
    }


def write_new_file(root: Path, relative: str, payload: bytes) -> None:
    target = root / relative
    reject_links(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    reject_links(target.parent)
    # Exclusive creation also protects against files appearing after the initial empty-directory check.
    with target.open('xb') as stream:
        stream.write(payload)


def initialize(target: Path, skill_root: Path, body, title) -> dict:
    if target == skill_root or target.is_relative_to(skill_root):
        raise ValueError('Choose a workspace outside the installed skill directory.')
    if target.exists() and (not target.is_dir() or any(target.iterdir())):
        raise ValueError('The destination must not exist or must be an empty directory. Existing workspaces are never overwritten.')
    plan = collect_templates(skill_root)
    fonts = update_font_references(plan, body, title)
    report = {
        'status': 'initialized', 'schema_version': 1,
        'files_written': len(plan) + 1, **fonts,
        'rendering_ready': False, 'dependency_check_performed': False,
        'synthetic_media_generated': False, 'real_source_media_reviewed': False,
        'notes': [
            'Run tools/workspace.py doctor before rendering; creating a workspace does not verify its dependencies.',
            'Generate the synthetic demo locally using tools/make_demo.py; media binaries are not distributed with this skill.',
            'The installed skill remains outside this workspace; invoke that skill explicitly if the host does not discover it.',
        ],
    }
    if not fonts['font_files_supplied']:
        report['notes'].append('No font supplied. Add a legally usable Chinese TTF/OTF font and update style/timeline before rendering text.')
    for relative in plan:
        if relative.startswith('/') or '..' in Path(relative).parts:
            raise ValueError(f'Unsafe output path: {relative}')
    target.mkdir(parents=True, exist_ok=True)
    reject_links(target)
    for relative, payload in plan.items():
        write_new_file(target, relative, payload)
    for folder in ('素材', '作品', '工作数据/索引', '工作数据/缓存', '工作数据/日志', '工作数据/预处理', '公共资源/音乐', '公共资源/配音', '公共资源/字体'):
        path = target / folder
        reject_links(path)
        path.mkdir(parents=True, exist_ok=True)
    write_new_file(target, 'initialization_report.json', (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('workspace', nargs='?', help='New or empty workspace directory; never an existing populated project.')
    parser.add_argument('--destination', help='Alternative explicit form of the workspace directory argument.')
    parser.add_argument('--body-font', help='An explicitly chosen, legally usable local TTF/OTF font for body text.')
    parser.add_argument('--title-font', help='Optional local TTF/OTF for art titles; falls back to --body-font.')
    args = parser.parse_args()
    if bool(args.workspace) == bool(args.destination):
        parser.error('Provide exactly one workspace directory: a positional argument or --destination.')
    try:
        skill_root = absolute_without_links(Path(__file__).parent.parent)
        target = absolute_without_links(args.destination or args.workspace)
        report = initialize(target, skill_root, supplied_font(args.body_font, 'body'), supplied_font(args.title_font, 'title'))
    except (ValueError, OSError, UnicodeError, json.JSONDecodeError) as error:
        print(json.dumps({'status': 'error', 'message': str(error), 'existing_files_overwritten': False}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps({'workspace': str(target), **report}, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
