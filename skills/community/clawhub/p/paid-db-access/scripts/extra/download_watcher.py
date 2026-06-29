#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载文件查找 & 论文匹配工具
===========================
不拍快照、不 diff——直接列出最近下载的 PDF/CAJ 文件，按论文标题匹配。
支持精确文件名查找（--find），用 CDP evaluate 从页面提取文件名后直接定位。

使用方式：
  # 列出最近 N 个可匹配文件（默认最近 20 个）
  python download_watcher.py

  # 列出最近 5 个
  python download_watcher.py --recent 5

  # 精确查找某个文件
  python download_watcher.py --find "10602726.pdf"

  # 列出并匹配论文 JSON
  python download_watcher.py --papers papers.json

  # 指定下载目录
  python download_watcher.py --dir "D:/Papers"
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent

# Windows GBK console → force UTF-8 output
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# 关注的文件类型
TARGET_EXTENSIONS = {'.pdf', '.caj', '.zip', '.tar.gz', '.gz'}


def get_download_dir(custom_dir=None):
    """获取下载目录（优先自定义，其次用 Windows 默认）"""
    if custom_dir and os.path.isdir(custom_dir):
        return Path(custom_dir)
    home = Path.home()
    for c in [home / 'Downloads', home / '下载']:
        if c.is_dir():
            return c
    return Path.cwd()


def scan_recent(download_dir, max_results=20):
    """扫描目录中最近的目标文件，返回按 mtime 降序排列的列表"""
    files = []
    try:
        for entry in download_dir.iterdir():
            if not entry.is_file():
                continue
            name_lower = entry.name.lower()
            ext = entry.suffix.lower()
            if ext not in TARGET_EXTENSIONS and not any(
                name_lower.endswith(e) for e in TARGET_EXTENSIONS
            ):
                continue
            stat = entry.stat()
            files.append({
                'name': entry.name,
                'path': str(entry),
                'size_kb': round(stat.st_size / 1024, 1),
                'mtime': stat.st_mtime,
                'mtime_str': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            })
    except PermissionError:
        print(f'[ERROR] Cannot access directory: {download_dir}', file=sys.stderr)
        return []

    files.sort(key=lambda f: f['mtime'], reverse=True)
    return files[:max_results]


def tokenize(text):
    """提取有意义的词（>2 字符），支持中英文"""
    t = re.sub(r'[^\w\s]', ' ', str(text).lower())
    return set(w for w in t.split() if len(w) > 2)


def match_files_to_papers(recent_files, papers):
    """将最近的文件匹配到论文列表，返回带匹配结果的结构"""
    results = []
    for f in recent_files:
        f_kw = tokenize(f['name'])

        best_score = 0
        best_paper = None
        for p in papers:
            title = p.get('title', '')
            t_kw = tokenize(title)
            if not f_kw or not t_kw:
                continue
            overlap = f_kw & t_kw
            score = len(overlap) / max(len(f_kw), len(t_kw), 1)
            if score > best_score:
                best_score = score
                best_paper = p

        conf = 'HIGH' if best_score >= 0.3 else ('MEDIUM' if best_score >= 0.15 else 'LOW')
        results.append({
            'file': f,
            'matched_title': best_paper.get('title', '') if best_paper else '',
            'matched_doi': best_paper.get('doi', '') if best_paper else '',
            'match_score': round(best_score, 3),
            'match_confidence': conf,
        })

    return results


def do_find(download_dir, filename):
    """精确查找某个文件"""
    target = download_dir / filename
    if target.exists():
        stat = target.stat()
        mtime = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        print(f'✅ Found: {filename}')
        print(f'   Size: {stat.st_size / 1024:.0f} KB')
        print(f'   Modified: {mtime}')
        print(f'   Path: {target}')
        return target
    else:
        # 尝试模糊匹配（忽略大小写）
        name_lower = filename.lower()
        for entry in download_dir.iterdir():
            if entry.is_file() and entry.name.lower() == name_lower:
                stat = entry.stat()
                mtime = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                print(f'✅ Found (case-insensitive): {entry.name}')
                print(f'   Size: {stat.st_size / 1024:.0f} KB')
                print(f'   Modified: {mtime}')
                print(f'   Path: {entry}')
                return entry

        print(f'❌ Not found: {filename}')
        return None


def print_recent(files):
    """打印最近文件列表"""
    if not files:
        print('[OK] No matching files found.')
        return
    print(f'[OK] {len(files)} recent files:\n')
    for i, f in enumerate(files, 1):
        print(f'  [{i}] {f["name"]}')
        print(f'       {f["size_kb"]} KB · {f["mtime_str"]}')
        print(f'       {f["path"]}')


def print_matched(results):
    """打印匹配结果，明确区分已确认和待确认"""
    if not results:
        print('[WARN] No files or papers to match.')
        return

    confirmed = [r for r in results if r['match_confidence'] == 'HIGH']
    uncertain = [r for r in results if r['match_confidence'] == 'MEDIUM']
    unmatched = [r for r in results if r['match_confidence'] == 'LOW']

    print(f'[OK] File → Paper match results:\n')

    # 已确认的
    if confirmed:
        print('━' * 60)
        print('✅ 已确认匹配：')
        for r in confirmed:
            f = r['file']
            print(f'   [{results.index(r)+1}] {f["name"]}')
            print(f'       {f["size_kb"]} KB · {f["mtime_str"]}')
            print(f'       → {r["matched_title"][:100]}')
            print()

    # 待确认的
    if uncertain:
        print('━' * 60)
        print('⚠️  待确认（需人工核实）：')
        for r in uncertain:
            f = r['file']
            print(f'   [{results.index(r)+1}] {f["name"]}')
            print(f'       {f["size_kb"]} KB · {f["mtime_str"]}')
            print(f'       → {r["matched_title"][:100]}')
            print(f'       Score: {r["match_score"]:.3f} — 请确认是否为这篇论文')
            print()

    # 无法匹配的
    if unmatched:
        print('━' * 60)
        print('❓ 无法自动匹配（需用户指定）：')
        for r in unmatched:
            f = r['file']
            print(f'   [{results.index(r)+1}] {f["name"]}')
            print(f'       {f["size_kb"]} KB · {f["mtime_str"]}')
            print(f'       → 文件名与论文标题无显著关联，无法自动确认归属')
            print()

    # 汇总
    print('━' * 60)
    print(f'汇总: ✅ {len(confirmed)} 确认 | ⚠️ {len(uncertain)} 待确认 | ❓ {len(unmatched)} 无法匹配')
    if uncertain or unmatched:
        print('请逐项确认后再使用。')


def main():
    parser = argparse.ArgumentParser(
        description='列出最近下载的 PDF/CAJ 文件，可选匹配论文',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python download_watcher.py                        # 列出最近 20 个文件
  python download_watcher.py --recent 5             # 最近 5 个
  python download_watcher.py --papers papers.json   # 列出并匹配论文
  python download_watcher.py --dir "D:/Papers"      # 指定下载目录
        """
    )
    parser.add_argument('--recent', type=int, default=20, help='列出最近 N 个文件（默认 20）')
    parser.add_argument('--dir', help='下载目录（默认 Windows 下载文件夹）')
    parser.add_argument('--papers', help='论文 JSON 文件路径（用于匹配）')
    parser.add_argument('--find', help='精确查找指定文件名')
    args = parser.parse_args()

    download_dir = get_download_dir(args.dir)
    if not download_dir.is_dir():
        print(f'[ERROR] Download directory not found: {download_dir}', file=sys.stderr)
        sys.exit(1)

    if args.find:
        do_find(download_dir, args.find)
        return

    recent = scan_recent(download_dir, max_results=args.recent)

    if args.papers:
        with open(args.papers, 'r', encoding='utf-8') as f:
            papers = json.load(f)
        print(f'📂 Download dir: {download_dir}')
        print(f'📄 Papers to match: {len(papers)}\n')
        results = match_files_to_papers(recent, papers)
        print_matched(results)

        # 保存匹配结果
        match_path = SKILL_DIR / 'memory' / '.download_match.json'
        match_path.parent.mkdir(parents=True, exist_ok=True)
        serializable = []
        for r in results:
            serializable.append({
                'file': r['file'],
                'matched_title': r['matched_title'],
                'matched_doi': r['matched_doi'],
                'match_score': r['match_score'],
                'match_confidence': r['match_confidence'],
            })
        with open(match_path, 'w', encoding='utf-8') as f:
            json.dump(serializable, f, indent=2, ensure_ascii=False)
        print(f'Match results saved to {match_path}')
    else:
        print(f'📂 Download dir: {download_dir}\n')
        print_recent(recent)


if __name__ == '__main__':
    main()
