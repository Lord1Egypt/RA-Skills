#!/usr/bin/env python3
import json
import os
from datetime import datetime
from lib_memory import load_yaml_file

ROOT = os.environ.get('MEMORY_ROOT', os.path.join(os.getcwd(), 'memory'))
INDEX_DIR = os.path.join(ROOT, 'indexes')
TOPICS_DIR = os.path.join(ROOT, 'topics')
OBJECTS_DIR = os.path.join(ROOT, 'objects')
DAILY_DIR = os.path.join(ROOT, 'daily')
REFLECTIONS_DIR = os.path.join(ROOT, 'reflections')


def load_yaml(path):
    return load_yaml_file(path)


def iter_files(root, suffixes):
    if not os.path.isdir(root):
        return
    for base, _, files in os.walk(root):
        for name in sorted(files):
            if any(name.endswith(s) for s in suffixes):
                yield os.path.join(base, name)


def rel(path):
    return os.path.relpath(path, ROOT)


def build_manifest():
    manifest = {
        'generated_at': datetime.now().astimezone().isoformat(timespec='seconds'),
        'topics': [],
        'objects': [],
        'daily_logs': [],
        'reflections': [],
    }

    for path in iter_files(TOPICS_DIR, ['.yaml', '.yml']) or []:
        blob = load_yaml(path)
        if blob is None:
            continue
        manifest['topics'].append({
            'id': blob.get('id'),
            'name': blob.get('name'),
            'summary': blob.get('summary', ''),
            'path': rel(path),
        })

    for path in iter_files(OBJECTS_DIR, ['.yaml', '.yml']) or []:
        blob = load_yaml(path)
        if blob is None:
            continue
        manifest['objects'].append({
            'id': blob.get('id'),
            'type': blob.get('type'),
            'domain': blob.get('domain'),
            'title': blob.get('title', ''),
            'summary': blob.get('summary', ''),
            'status': blob.get('status'),
            'path': rel(path),
        })

    for path in iter_files(DAILY_DIR, ['.md']) or []:
        manifest['daily_logs'].append({'path': rel(path)})

    for path in iter_files(REFLECTIONS_DIR, ['.md']) or []:
        manifest['reflections'].append({'path': rel(path)})

    return manifest


def write_human_readme(manifest):
    path = os.path.join(INDEX_DIR, 'README.md')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('# Memory Index\n\n')
        f.write(f'- 生成时间：{manifest["generated_at"]}\n')
        f.write(f'- Topic 数量：{len(manifest["topics"])}\n')
        f.write(f'- Object 数量：{len(manifest["objects"])}\n')
        f.write(f'- Daily 日志数量：{len(manifest["daily_logs"])}\n')
        f.write(f'- Reflection 数量：{len(manifest["reflections"])}\n\n')

        f.write('## Topics\n\n')
        for item in manifest['topics']:
            f.write(f"- **{item.get('id','')}** — {item.get('summary','')}  \\n  路径：`{item.get('path','')}`\n")

        f.write('\n## Objects\n\n')
        if manifest['objects']:
            for item in manifest['objects']:
                f.write(f"- **{item.get('id','')}** ({item.get('type','')}/{item.get('domain','')}) — {item.get('summary','')}  \\n  路径：`{item.get('path','')}`\n")
        else:
            f.write('- 暂无对象\n')

        f.write('\n## Daily Logs\n\n')
        for item in manifest['daily_logs']:
            f.write(f"- `{item['path']}`\n")

        f.write('\n## Reflections\n\n')
        for item in manifest['reflections']:
            f.write(f"- `{item['path']}`\n")


def main():
    os.makedirs(INDEX_DIR, exist_ok=True)
    manifest = build_manifest()
    with open(os.path.join(INDEX_DIR, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    write_human_readme(manifest)
    print(json.dumps({'ok': True, 'index_dir': INDEX_DIR}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
