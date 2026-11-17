#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
驾驶舱生成器（通用版，2026-09-22）

作用：扫描工作区 → 把「工作区全景」视图 + 文件快照注入 dashboard.html。
产出是单文件静态页：双击可看（内嵌快照），也可配合 serve_dashboard.py 实时扫描。

用法：
  python3 build_dashboard.py <工作区根目录> [--title "产品名"] [--force] [--no-text] [--text-budget 1200000]
  python3 build_dashboard.py .                      # 首次生成
  python3 build_dashboard.py . --force              # 覆盖已有（旧文件备份到 .cache/）

约定：
  - 页面里所有 <section id="tab-xxx"> 会自动成为一个 Tab（可手写自定义区块扩展）
  - 目录说明可用 <root>/workspace-folders.json 定制（见 scan_workspace.py）
  - 状态可用 <root>/workspace-registry.json 人工指定（最权威）
"""
import os, re, json, sys, argparse, datetime, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
# 骨架查找顺序：skill 自带 assets/ → 与脚本同目录 → 工作区 .cache/（init_workspace 会复制到这里）
SKELETON_CANDIDATES = [
    os.path.join(HERE, '..', 'assets', 'dashboard-skeleton.html'),
    os.path.join(HERE, 'dashboard-skeleton.html'),
    os.path.join(HERE, '..', '.cache', 'dashboard-skeleton.html'),
]


def find_skeleton(root=None):
    if root:
        p = os.path.join(root, '.cache', 'dashboard-skeleton.html')
        if os.path.exists(p):
            return p
    for p in SKELETON_CANDIDATES:
        if os.path.exists(p):
            return os.path.abspath(p)
    return None
sys.path.insert(0, HERE)
import scan_workspace  # noqa: E402

TEXT_EXT = ('.md', '.txt', '.json', '.yaml', '.yml', '.csv', '.py', '.html')
SKIP_SNAPSHOT = {'dashboard.html'}


def build_text_snapshot(root, files, budget=1_200_000, per_file=4000):
    """内嵌文件文本快照（离线双击也能看）。按修改时间倒序，控制在预算内。"""
    out, total = {}, 0
    ordered = sorted(files, key=lambda f: f.get('datetime', ''), reverse=True)
    for f in ordered:
        rel = f['path']
        if rel in SKIP_SNAPSHOT:
            continue
        if not rel.endswith(TEXT_EXT):
            continue
        fp = os.path.join(root, rel)
        try:
            if os.path.getsize(fp) > 400_000:
                continue
            t = open(fp, encoding='utf-8', errors='ignore').read()
        except Exception:
            continue
        t = t[:per_file]
        out[rel] = t
        total += len(t)
        if total > budget:
            break
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root', nargs='?', default='.')
    ap.add_argument('--title', default='营销')
    ap.add_argument('--force', action='store_true', help='覆盖已存在的 dashboard.html')
    ap.add_argument('--no-text', action='store_true', help='不内嵌文件快照（体积更小，需起服务才能看内容）')
    ap.add_argument('--text-budget', type=int, default=1_200_000)
    args = ap.parse_args()

    root = os.path.abspath(os.path.expanduser(args.root))
    if not os.path.isdir(root):
        print('目录不存在：', root)
        return 1

    data = scan_workspace.build_map(root)
    cache_dir = os.path.join(root, '.cache')
    os.makedirs(cache_dir, exist_ok=True)
    json.dump(data, open(os.path.join(cache_dir, 'workspace_map.json'), 'w', encoding='utf-8'), ensure_ascii=False)

    ftxt = {} if args.no_text else build_text_snapshot(root, data['files'], args.text_budget)
    ws_json = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    ftxt_json = json.dumps(ftxt, ensure_ascii=False).replace('</', '<\\/')

    target = os.path.join(root, 'dashboard.html')
    if os.path.exists(target) and not args.force:
        print('dashboard.html 已存在。若要覆盖请先备份，或加 --force（会自动备份到 .cache/）。')
        return 2
    if os.path.exists(target):
        bak = os.path.join(cache_dir, 'dashboard-%s.html.bak' % datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
        shutil.copy2(target, bak)
        print('已备份旧文件 →', bak)

    sk_path = find_skeleton(root)
    if not sk_path:
        print('找不到 dashboard-skeleton.html。请确保它在 skill 的 assets/ 目录，'
              '或工作区的 .cache/ 目录（重跑 init_workspace.py --with-dashboard 可恢复）。')
        return 3
    sk = open(sk_path, encoding='utf-8').read()
    sk = sk.replace('__TITLE__', args.title)
    sk = sk.replace('__WS_JSON__', ws_json).replace('__WSTXT_JSON__', ftxt_json)

    # 若已存在旧的 dashboard.html 且用户手工加了自定义 <section id="tab-xxx">，迁移进来
    if os.path.exists(target):
        try:
            old = open(target, encoding='utf-8').read()
            blocks = re.findall(r'<!-- CUSTOM:START -->\s*(.*?)\s*<!-- CUSTOM:END -->', old, re.S)
            if blocks:
                sk = sk.replace('<!-- WS-SECTION:END -->',
                                '<!-- WS-SECTION:END -->\n\n' + '\n\n'.join(blocks))
                print('已迁移自定义区块：%d 个' % len(blocks))
        except Exception as e:
            print('自定义区块迁移失败：', e)

    open(target, 'w', encoding='utf-8').write(sk)
    print('✅ dashboard.html 已生成：%s（%.0f KB）' % (target, os.path.getsize(target) / 1024))
    print('   文件 %d / 目录 %d / 台账 %d 条；内嵌文本快照 %d 个文件'
          % (data['total_files'], data['total_dirs'], data['ledger_count'], len(ftxt)))
    print('   实时模式：python3 scripts/serve_dashboard.py %s 8799  → http://127.0.0.1:8799/dashboard.html' % os.path.basename(root))
    return 0


if __name__ == '__main__':
    sys.exit(main())
