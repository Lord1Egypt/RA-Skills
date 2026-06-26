#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path


def expand(p: str) -> Path:
    return Path(os.path.expanduser(p)).resolve()


def write_text(path: Path, content: str, overwrite: bool = False):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        return False
    path.write_text(content, encoding='utf-8')
    return True


def read_template(base: Path, rel: str) -> str:
    return (base / 'templates' / rel).read_text(encoding='utf-8')


def main():
    if len(sys.argv) != 2:
        print(json.dumps({
            'ok': False,
            'error': 'Usage: init_project.py <json-args>'
        }, ensure_ascii=False))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])
    except Exception as e:
        print(json.dumps({'ok': False, 'error': f'Invalid JSON: {e}'}, ensure_ascii=False))
        sys.exit(1)

    projects_root = args.get('projects_root')
    project_name = args.get('project_name')
    create_workspace_rule = bool(args.get('create_workspace_rule', True))
    workspace_root = args.get('workspace_root', '~/.openclaw/workspace')
    project_rule_filename = args.get('project_rule_filename', 'PROJECT_SYSTEM.md')
    overwrite = bool(args.get('overwrite', False))

    if not projects_root or not project_name:
        print(json.dumps({
            'ok': False,
            'error': 'projects_root and project_name are required'
        }, ensure_ascii=False))
        sys.exit(1)

    base_dir = Path(__file__).resolve().parent.parent
    workspace_root = expand(workspace_root)
    projects_root = expand(projects_root)
    project_dir = projects_root / project_name

    created = []
    skipped = []

    projects_root.mkdir(parents=True, exist_ok=True)
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / 'checkpoints').mkdir(parents=True, exist_ok=True)
    (project_dir / 'session-backups').mkdir(parents=True, exist_ok=True)

    if create_workspace_rule:
        system_path = workspace_root / project_rule_filename
        content = read_template(base_dir, 'PROJECT_SYSTEM.md').replace('`<在初始化时填写>`', f'`{projects_root}`')
        if write_text(system_path, content, overwrite=overwrite):
            created.append(str(system_path))
        else:
            skipped.append(str(system_path))

    files = [
        '00_恢复入口.md',
        '00_文档总索引与当前进度.md',
        '01_项目会话与恢复机制说明.md',
        '99_关键决策记录.md',
        'checkpoints/README.md',
        'session-backups/README.md',
    ]

    for rel in files:
        target = project_dir / rel
        content = read_template(base_dir, rel)
        content = content.replace('<项目名称>', project_name)
        if write_text(target, content, overwrite=overwrite):
            created.append(str(target))
        else:
            skipped.append(str(target))

    print(json.dumps({
        'ok': True,
        'projects_root': str(projects_root),
        'project_dir': str(project_dir),
        'created': created,
        'skipped': skipped,
        'next': [
            f'Edit {project_dir / "00_文档总索引与当前进度.md"} to define mainline / phase / breakpoint.',
            f'Edit {project_dir / "99_关键决策记录.md"} to record initial decisions.',
            f'Read {workspace_root / project_rule_filename} before using enter/recover-project workflow.'
        ]
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
