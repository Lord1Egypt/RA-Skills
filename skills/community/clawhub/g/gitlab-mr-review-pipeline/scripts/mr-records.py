#!/usr/bin/env python3
"""
GitLab MR Review Pipeline - MR 处理记录管理
记录已处理的 MR，避免重复审核
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

RECORD_DIR = Path.home() / ".config" / "gitlab-mr-review-pipeline"
RECORD_FILE = RECORD_DIR / "processed-mrs.json"


def load_records():
    """加载处理记录"""
    if not RECORD_FILE.exists():
        return {}
    
    try:
        with open(RECORD_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_records(records):
    """保存处理记录"""
    RECORD_DIR.mkdir(parents=True, exist_ok=True)
    with open(RECORD_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)


def is_processed(repo, mr_id):
    """检查 MR 是否已处理"""
    records = load_records()
    key = f"{repo}!{mr_id}"
    return key in records


def mark_processed(repo, mr_id, author, score, issues_count):
    """标记 MR 已处理"""
    records = load_records()
    key = f"{repo}!{mr_id}"
    
    records[key] = {
        "repo": repo,
        "mr_id": mr_id,
        "author": author,
        "score": score,
        "issues_count": issues_count,
        "processed_at": datetime.now().isoformat(),
        "email_sent": True
    }
    
    save_records(records)
    print(f"✓ 已记录：{key}")


def list_processed(days=7):
    """列出指定天数内已处理的 MR"""
    records = load_records()
    cutoff = datetime.now() - timedelta(days=days)
    
    print(f"\n最近 {days} 天处理的 MR:\n")
    print(f"{'仓库':<30} {'MR':<8} {'作者':<20} {'评分':<6} {'时间':<20}")
    print("-" * 90)
    
    count = 0
    for key, record in sorted(records.items(), key=lambda x: x[1]['processed_at'], reverse=True):
        processed_at = datetime.fromisoformat(record['processed_at'])
        if processed_at >= cutoff:
            print(f"{record['repo']:<30} !{record['mr_id']:<7} {record['author']:<20} {record['score']:<6} {processed_at.strftime('%Y-%m-%d %H:%M'):<20}")
            count += 1
    
    if count == 0:
        print("无记录")
    
    print(f"\n共 {count} 个 MR")
    return count


def cleanup_old_records(days=30):
    """清理旧记录"""
    records = load_records()
    cutoff = datetime.now() - timedelta(days=days)
    
    to_delete = []
    for key, record in records.items():
        processed_at = datetime.fromisoformat(record['processed_at'])
        if processed_at < cutoff:
            to_delete.append(key)
    
    for key in to_delete:
        del records[key]
    
    save_records(records)
    
    print(f"✓ 已清理 {len(to_delete)} 条 {days} 天前的记录")
    return len(to_delete)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="MR 处理记录管理")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # check 命令
    check_parser = subparsers.add_parser("check", help="检查 MR 是否已处理")
    check_parser.add_argument("--repo", required=True, help="仓库名称")
    check_parser.add_argument("--mr-id", required=True, help="MR ID")
    
    # mark 命令
    mark_parser = subparsers.add_parser("mark", help="标记 MR 已处理")
    mark_parser.add_argument("--repo", required=True, help="仓库名称")
    mark_parser.add_argument("--mr-id", required=True, help="MR ID")
    mark_parser.add_argument("--author", required=True, help="作者")
    mark_parser.add_argument("--score", type=int, help="综合评分")
    mark_parser.add_argument("--issues", type=int, help="问题数量")
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出已处理的 MR")
    list_parser.add_argument("--days", type=int, default=7, help="天数（默认 7）")
    
    # cleanup 命令
    cleanup_parser = subparsers.add_parser("cleanup", help="清理旧记录")
    cleanup_parser.add_argument("--days", type=int, default=30, help="天数（默认 30）")
    
    args = parser.parse_args()
    
    if args.command == "check":
        if is_processed(args.repo, args.mr_id):
            print(f"⚠️  {args.repo}!{args.mr_id} 已处理过，跳过")
            sys.exit(1)
        else:
            print(f"✓ {args.repo}!{args.mr_id} 未处理，继续")
            sys.exit(0)
    
    elif args.command == "mark":
        mark_processed(args.repo, args.mr_id, args.author, args.score, args.issues)
    
    elif args.command == "list":
        list_processed(args.days)
    
    elif args.command == "cleanup":
        cleanup_old_records(args.days)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
