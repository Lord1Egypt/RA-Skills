#!/usr/bin/env python3
import json, subprocess, time, sys
from pathlib import Path

SPACE_ID = '7619649432362994649'


def run(cmd):
    p = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(f'cmd failed: {cmd}\nstdout={p.stdout}\nstderr={p.stderr}')
    lines = [ln for ln in p.stdout.splitlines() if not ln.startswith('[lark-claw]')]
    txt = '\n'.join(lines).strip()
    return json.loads(txt)


def call(tool, payload):
    quoted = json.dumps(payload, ensure_ascii=False).replace("'", "'\\''")
    return run(f"echo '{quoted}' | lark-claw call {tool}")


def wiki_list(space_id, parent=None):
    payload = {'space_id': space_id, 'action': 'list', 'page_size': 50}
    if parent:
        payload['parent_node_token'] = parent
    data = call('feishu_wiki_space_node', payload).get('data', {})
    return data.get('nodes', [])


def get_or_create(space_id, title, parent=None):
    for n in wiki_list(space_id, parent):
        if n['title'] == title:
            return n, False
    payload = {
        'space_id': space_id,
        'action': 'create',
        'obj_type': 'docx',
        'node_type': 'origin',
        'title': title,
    }
    if parent:
        payload['parent_node_token'] = parent
    res = call('feishu_wiki_space_node', payload)
    return res['data']['node'], True


def update_doc(doc_id, markdown):
    payload = {'doc_id': doc_id, 'markdown': markdown, 'mode': 'overwrite'}
    quoted = json.dumps(payload, ensure_ascii=False).replace("'", "'\\''")
    return run(f"lark-claw call feishu_update_doc '{quoted}'")


def sync_file(path, parent_token):
    node, created = get_or_create(SPACE_ID, path.stem, parent_token)
    update_doc(node['obj_token'], path.read_text(encoding='utf-8'))
    return created


def main():
    if len(sys.argv) < 2:
        print('Usage: sync_to_feishu_wiki.py <项目目录> [root_title]')
        sys.exit(1)

    project_dir = Path(sys.argv[1]).expanduser()
    root_title = sys.argv[2] if len(sys.argv) >= 3 else project_dir.name
    root_node, _ = get_or_create(SPACE_ID, root_title)
    root_token = root_node['node_token']

    top_count = 0
    for p in sorted(project_dir.glob('*.md')):
        sync_file(p, root_token)
        top_count += 1
        time.sleep(0.2)

    for dirname in ['characters', 'manuscript']:
        d = project_dir / dirname
        if not d.is_dir():
            continue
        dir_node, _ = get_or_create(SPACE_ID, dirname, root_token)
        dir_token = dir_node['node_token']
        subcount = 0
        for p in sorted(d.glob('*.md')):
            sync_file(p, dir_token)
            subcount += 1
            time.sleep(0.15)
        print(f'{dirname}: {subcount}')

    print(f'root: {root_title}')
    print(f'top-level files: {top_count}')


if __name__ == '__main__':
    main()
