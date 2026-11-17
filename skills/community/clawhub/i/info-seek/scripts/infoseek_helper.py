#!/usr/bin/env python3
"""infoseek_helper.py — v1.4.0 核心辅助脚本
吸收 @expeditionhub/infoseek v2.0.0 的：URL 去重 + 存档归档 + 任务报告 + 删除保护

子命令：
  normalize-url   URL 标准化（7 条规则）
  add-url         加入去重 DB
  check-url       检查 URL 是否已在 DB
  create-folder   创建主题存档文件夹
  generate-filename  生成标准文件名
  save-content    保存抓取内容到归档（含元数据表）
  dedup-stats     输出任务报告（含引擎/去重/新存档统计）
  delete-to-recycle  删除文件到回收站（不可绕过）
  restore         从回收站恢复
  dedup           批量 URL 去重（输入文件）
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import uuid
from datetime import datetime
from pathlib import Path

# ── 路径常量 ──
# ── 路径常量（v1.0.0 状态层中立：运行态数据统一位于 ~/.infoseek 或 env 指定目录）──
CORE_DIR = Path(__file__).parent.parent / 'core'
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))
from state_dir import get_data_dir, state_path, get_db_path, get_log_path, get_archives_dir
WORKSPACE = Path(os.environ.get('OPENCLAW_WORKSPACE', str(Path.home())))
INFOSEEK_DIR = get_data_dir()
DB_PATH = get_db_path()
LOG_PATH = get_log_path()
ARCHIVES_DIR = get_archives_dir()
RECYCLE_DIR = INFOSEEK_DIR / '_recycle_bin'

# ── URL 标准化规则 ──
UTM_PARAMS = {
    'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
    'fbclid', 'gclid', 'msclkid', 'mc_cid', 'mc_eid',
    'ref', 'source', '_hsenc', '_hsmi', 'hsCtaTracking'
}


def normalize_url(url: str) -> str:
    """7 条规则按顺序执行：协议归一 → www 剥离 → 域名小写 → 尾部斜杠 → UTM 剥离 → 参数排序 → Fragment 剥离"""
    from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

    if not url:
        return url

    parsed = urlparse(url)

    # 规则 1: 协议归一（http → https）
    scheme = 'https' if parsed.scheme in ('http', 'https') else parsed.scheme

    # 规则 2: 移除 www 前缀
    netloc = parsed.netloc.lower()  # 规则 3: 域名小写
    if netloc.startswith('www.'):
        netloc = netloc[4:]

    # 规则 5: 移除 UTM 跟踪参数
    params = parse_qs(parsed.query, keep_blank_values=True)
    params = {k: v for k, v in params.items() if k.lower() not in UTM_PARAMS}

    # 规则 6: 参数排序（按 key 字母序，确保哈希一致）
    sorted_keys = sorted(params.keys())
    query = urlencode([(k, params[k]) for k in sorted_keys], doseq=True)

    # 规则 4: 移除尾部斜杠（仅对 path 非根路径时）
    path = parsed.path
    if path != '/' and path.endswith('/'):
        path = path[:-1]

    # 规则 7: Fragment 剥离（默认 None）
    return urlunparse((scheme, netloc, path, parsed.params, query, ''))


def url_hash(url_normalized: str) -> str:
    return hashlib.sha1(url_normalized.encode('utf-8')).hexdigest()


# ── DB 管理 ──
def ensure_db():
    """确保 DB 与目录存在（首次启动自动创建）"""
    INFOSEEK_DIR.mkdir(parents=True, exist_ok=True)
    RECYCLE_DIR.mkdir(parents=True, exist_ok=True)
    if not DB_PATH.exists():
        init_db()


def init_db():
    DB_PATH.write_text(json.dumps({
        "version": "1.0",
        "created": datetime.now().isoformat(),
        "urls": {},
        "subjects": {}
    }, ensure_ascii=False, indent=2), encoding='utf-8')


def load_db():
    ensure_db()
    return json.loads(DB_PATH.read_text(encoding='utf-8'))


def save_db(db):
    DB_PATH.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding='utf-8')


def log_action(action: str, **kwargs):
    record = {"time": datetime.now().isoformat(), "action": action, **kwargs}
    with LOG_PATH.open('a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')


# ── 子命令实现 ──
def cmd_normalize_url(args):
    normalized = normalize_url(args.url)
    h = url_hash(normalized)
    print(f"原始 URL: {args.url}")
    print(f"标准化:  {normalized}")
    print(f"SHA1:    {h}")
    print(f"短哈希:  {h[:8]}")


def cmd_check_url(args):
    result = check_url_dedup(args.url)
    if result['dedup']:
        print(f"⚠️  URL 已存在（命中去重）")
        print(f"  标准化 URL: {result['normalized']}")
        print(f"  主题: {result['subject']}")
        print(f"  抓取时间: {result['crawl_time']}")
        print(f"  存档文件: {result['filename']}")
    else:
        print(f"✅ URL 未抓取（可入队）")
        print(f"  标准化 URL: {result['normalized']}")
        print(f"  SHA1: {result['sha1']}")


def check_url_dedup(url: str) -> dict:
    """URL 去重检查纯函数（v1.0.1 PATCH / G1：供 MCP 直接调用，弃 subprocess）"""
    db = load_db()
    normalized = normalize_url(url)
    h = url_hash(normalized)
    record = db['urls'].get(h)
    return {
        'dedup': record is not None,
        'normalized': normalized,
        'sha1': h,
        'subject': record.get('subject') if record else '',
        'crawl_time': record.get('crawl_time') if record else '',
        'filename': record.get('filename') if record else '',
    }


def _safe_subject_dir(subject: str) -> Path:
    """归档主题目录（v1.0.1 PATCH / G3：路径穿越守卫）。

    拒绝含 '..' / 绝对路径 / 符号链接逃逸的 subject，防止写出归档目录。
    返回安全目录 Path（已 mkdir）。
    """
    if not subject or not subject.strip():
        raise ValueError("subject 不能为空")
    if subject != subject.strip() or '..' in subject.replace('\\', '/').split('/'):
        raise ValueError(f"非法的 subject（路径穿越风险）: {subject[:40]}")
    base = ARCHIVES_DIR.resolve()
    base.mkdir(parents=True, exist_ok=True)
    target = (base / subject.strip()).resolve()
    if not target.is_relative_to(base):
        raise ValueError(f"非法的 subject（逃逸归档目录）: {subject[:40]}")
    target.mkdir(parents=True, exist_ok=True)
    return target


def save_content_to_archive(subject: str, url: str, title: str, content: str,
                            website: str = 'unknown', fmt: str = 'md',
                            date: str = '', author: str = 'unknown',
                            source: str = 'web_search') -> dict:
    """保存内容到归档（v1.0.1 PATCH / G1：纯函数，供 MCP 直接调用）。

    从 cmd_save_content 提取核心逻辑，弃 subprocess 进程依赖。
    返回 {filename, archive_path, subject_dir, url, sha1}。
    """
    db = load_db()
    normalized = normalize_url(url)
    h = url_hash(normalized)
    task_id = str(uuid.uuid4())
    crawl_time = datetime.now().isoformat()

    subject_dir = _safe_subject_dir(subject)
    fn = generate_filename(date or datetime.now().strftime('%Y%m%d'),
                           title, website, fmt)
    filepath = subject_dir / fn

    metadata = {
        "url": url, "url_normalized": normalized, "website": website,
        "source": source, "date": date or 'unknown', "title": title,
        "author": author, "editor": 'unknown', "subject": subject,
        "task_id": task_id, "crawl_time": crawl_time,
    }

    if fmt == 'md':
        meta_table = "\n".join([f"| {k} | {v} |" for k, v in metadata.items()])
        out = f"---\n{meta_table}\n---\n\n{content}\n"
    elif fmt == 'json':
        out = json.dumps({"metadata": metadata, "content": content},
                         ensure_ascii=False, indent=2)
    elif fmt == 'txt':
        meta_table = "\n".join([f"{k}: {v}" for k, v in metadata.items()])
        out = f"{meta_table}\n\n{'='*60}\n\n{content}\n"
    else:
        out = content

    filepath.write_text(out, encoding='utf-8')
    db['urls'][h] = {
        "url_raw": url, "url_normalized": normalized, "subject": subject,
        "task_id": task_id, "crawl_time": crawl_time, "filename": fn,
        "archive_path": str(filepath.relative_to(WORKSPACE)), "website": website,
    }
    if subject not in db['subjects']:
        db['subjects'][subject] = {"created": crawl_time, "task_ids": [task_id]}
    elif task_id not in db['subjects'][subject].get('task_ids', []):
        db['subjects'][subject].setdefault('task_ids', []).append(task_id)
    save_db(db)

    return {
        'filename': fn, 'archive_path': str(filepath), 'subject_dir': str(subject_dir),
        'url': url, 'sha1': h, 'task_id': task_id,
    }


def cmd_create_folder(args):
    # v1.0.1 PATCH / G3: 复用路径穿越守卫
    try:
        folder = _safe_subject_dir(args.subject)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    print(f"✅ 已创建主题存档文件夹: {folder}")
    log_action("create_folder", subject=args.subject, path=str(folder))


def generate_filename(date_str: str, title: str, website: str, fmt: str = 'md') -> str:
    """生成标准文件名：YYYYMMDD-title-website.ext（重名追加 8 位哈希）"""
    safe_title = re.sub(r'[<>:"/\\|?*]', '', title)[:80]
    safe_website = website.lower().replace('www.', '').split('/')[0]
    base = f"{date_str}-{safe_title}-{safe_website}.{fmt}"

    # 重名追加短哈希
    if (ARCHIVES_DIR).exists():
        for folder in ARCHIVES_DIR.iterdir():
            if folder.is_dir() and (folder / base).exists():
                short_hash = hashlib.sha1(base.encode()).hexdigest()[:8]
                base = f"{date_str}-{safe_title}-{safe_website}_{short_hash}.{fmt}"
                break
    return base


def cmd_generate_filename(args):
    fn = generate_filename(args.date, args.title, args.website, args.format)
    print(f"生成文件名: {fn}")


def cmd_save_content(args):
    # v1.0.1 PATCH / G1+G3: 复用纯函数（含路径穿越守卫）
    try:
        result = save_content_to_archive(
            subject=args.subject, url=args.url, title=args.title,
            content=args.content, website=args.website,
            fmt=args.format, date=args.date or '',
            author=getattr(args, 'author', 'unknown'),
            source=getattr(args, 'source', 'web_search'))
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    filepath = Path(result['archive_path'])
    print(f"✅ 已存档: {filepath}")
    print(f"   文件大小: {filepath.stat().st_size/1024:.1f} KB")
    print(f"   主题: {args.subject} | task_id: {result['task_id'][:8]}")
    log_action("save_file", subject=args.subject, filename=result['filename'],
               url=result['url'], size_kb=filepath.stat().st_size/1024)


def cmd_dedup(args):
    """批量 URL 去重"""
    if not args.input:
        print("❌ 必须指定 --input 文件")
        sys.exit(1)
    urls = [u.strip() for u in Path(args.input).read_text(encoding='utf-8').splitlines() if u.strip()]
    db = load_db()
    new, dup = [], []
    for u in urls:
        n = normalize_url(u)
        h = url_hash(n)
        if h in db['urls']:
            dup.append(u)
        else:
            new.append(u)
    print(f"总计: {len(urls)} | 已存在: {len(dup)} | 待抓取: {len(new)}")
    if dup:
        print(f"\n去重跳过（{len(dup)} 条）：")
        for u in dup[:10]:
            print(f"  - {u}")
        if len(dup) > 10:
            print(f"  ... 还有 {len(dup)-10} 条")
    if new:
        out = Path(args.output or 'new_urls.txt')
        out.write_text('\n'.join(new), encoding='utf-8')
        print(f"\n✅ 待抓取 URL 已写入: {out}")


def cmd_dedup_stats(args):
    db = load_db()
    print("=" * 60)
    print(f"Infoseek 任务报告")
    print("=" * 60)
    print(f"DB 版本: {db.get('version')}")
    print(f"DB 创建: {db.get('created')}")
    print(f"URL 总数: {len(db['urls'])}")
    print(f"主题总数: {len(db['subjects'])}")
    print()
    if db['subjects']:
        print("按主题统计：")
        for subj, stat in db['subjects'].items():
            print(f"  • {subj}: {stat['url_count']} 条 URL，"
                  f"上次任务 {stat['last_task_id'][:8] if stat['last_task_id'] else 'N/A'}")


def cmd_delete_to_recycle(args):
    """删除到回收站（必须确认）"""
    if not args.yes:
        print("⚠️  危险操作！需加 --yes 确认")
        print(f"   目标: {args.path}")
        sys.exit(1)
    p = Path(args.path)
    if not p.exists():
        print(f"❌ 文件不存在: {p}")
        sys.exit(1)
    recycle_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    dest = RECYCLE_DIR / f"{recycle_id}_{p.name}"
    shutil.move(str(p), str(dest))
    log_action("delete_to_recycle", path=str(p), recycle_id=recycle_id, dest=str(dest))
    print(f"✅ 已移到回收站")
    print(f"   回收 ID: {recycle_id}")
    print(f"   原始: {p}")
    print(f"   回收站: {dest}")


def cmd_restore(args):
    recycle_id = args.recycle_id
    found = list(RECYCLE_DIR.glob(f"{recycle_id}_*"))
    if not found:
        print(f"❌ 回收 ID 未找到: {recycle_id}")
        sys.exit(1)
    src = found[0]
    dest_name = src.name[len(recycle_id)+1:]
    dest = WORKSPACE / dest_name
    shutil.move(str(src), str(dest))
    log_action("restore", recycle_id=recycle_id, dest=str(dest))
    print(f"✅ 已恢复到: {dest}")


# ── CLI ──
def main():
    parser = argparse.ArgumentParser(description='Infoseek v1.4.0 辅助脚本')
    sub = parser.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('normalize-url')
    p.add_argument('--url', required=True)

    p = sub.add_parser('check-url')
    p.add_argument('--url', required=True)

    p = sub.add_parser('create-folder')
    p.add_argument('--subject', required=True)

    p = sub.add_parser('generate-filename')
    p.add_argument('--date', required=True)
    p.add_argument('--title', required=True)
    p.add_argument('--website', required=True)
    p.add_argument('--format', default='md')

    p = sub.add_parser('save-content')
    p.add_argument('--subject', required=True)
    p.add_argument('--url', required=True)
    p.add_argument('--title', required=True)
    p.add_argument('--website', required=True)
    p.add_argument('--content', required=True)
    p.add_argument('--format', default='md')
    p.add_argument('--date', default=None)
    p.add_argument('--author', default='unknown')
    p.add_argument('--editor', default='unknown')
    p.add_argument('--source', default='web_search')
    p.add_argument('--task-id', default=None)

    p = sub.add_parser('dedup')
    p.add_argument('--input', required=True)
    p.add_argument('--output', default='new_urls.txt')

    p = sub.add_parser('dedup-stats')

    p = sub.add_parser('delete-to-recycle')
    p.add_argument('--path', required=True)
    p.add_argument('--yes', action='store_true')

    p = sub.add_parser('restore')
    p.add_argument('--recycle-id', required=True)

    args = parser.parse_args()
    dispatch = {
        'normalize-url': cmd_normalize_url,
        'check-url': cmd_check_url,
        'create-folder': cmd_create_folder,
        'generate-filename': cmd_generate_filename,
        'save-content': cmd_save_content,
        'dedup': cmd_dedup,
        'dedup-stats': cmd_dedup_stats,
        'delete-to-recycle': cmd_delete_to_recycle,
        'restore': cmd_restore
    }
    dispatch[args.cmd](args)


if __name__ == '__main__':
    main()