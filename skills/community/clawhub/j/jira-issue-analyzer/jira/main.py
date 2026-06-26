"""Main entry point for Jira issue fetcher."""

import argparse
import json
import os
import re
from datetime import datetime
from typing import List, Dict, Any

from config import config
from jira_client import JiraClient


def format_datetime(dt_str: str) -> str:
    if not dt_str:
        return ''
    try:
        dt = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        return dt.strftime('%Y-%m-%d %H:%M')
    except ValueError:
        try:
            dt = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%f%z')
            return dt.strftime('%Y-%m-%d %H:%M')
        except ValueError:
            return dt_str


def format_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes / 1024 / 1024:.2f} MB"


def extract_issue_key(input_str: str) -> str:
    # Support keys like HA-123 and PI2506-150.
    url_pattern = r'/browse/([A-Z][A-Z0-9]*-[0-9]+)'
    match = re.search(url_pattern, input_str, re.IGNORECASE)
    if match:
        return match.group(1).upper()

    key_pattern = r'^[A-Z][A-Z0-9]*-[0-9]+$'
    if re.match(key_pattern, input_str, re.IGNORECASE):
        return input_str.upper()

    raise ValueError(f"Invalid issue key or URL: {input_str}")


def print_table(issues: List[Dict[str, Any]]) -> None:
    if not issues:
        print("No issues found.")
        return

    columns = [
        ('Key', 12, 'key'),
        ('Status', 12, 'status'),
        ('Priority', 10, 'priority'),
        ('Summary', 50, 'summary'),
        ('Updated', 16, 'updated'),
    ]

    header = ' | '.join(f"{col[0]:<{col[1]}}" for col in columns)
    print(header)
    print('-' * len(header))

    for issue in issues:
        row = []
        for col in columns:
            value = issue.get(col[2], '')
            if col[2] in ('created', 'updated'):
                value = format_datetime(value)
            value = str(value)[:col[1]]
            row.append(f"{value:<{col[1]}}")
        print(' | '.join(row))

    print(f"\nTotal: {len(issues)} issues")


def print_json(data: Any) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def print_issue_detail(issue: Dict[str, Any]) -> None:
    print(f"\n{'='*60}")
    print(f"[{issue['key']}] {issue['summary']}")
    print(f"{'='*60}")

    print("\n📋 基本信息")
    print(f"  状态:     {issue['status']}")
    print(f"  优先级:   {issue['priority']}")
    print(f"  类型:     {issue.get('issuetype', 'N/A')}")
    print(f"  项目:     {issue.get('project', 'N/A')} ({issue.get('project_key', '')})")
    if issue.get('components'):
        print(f"  组件:     {', '.join(issue['components'])}")
    if issue.get('labels'):
        print(f"  标签:     {', '.join(issue['labels'])}")

    print("\n👥 人员")
    print(f"  经办人:   {issue['assignee']} ({issue.get('assignee_email', '')})")
    print(f"  报告人:   {issue.get('reporter', '')} ({issue.get('reporter_email', '')})")

    print("\n📅 时间")
    print(f"  创建:     {format_datetime(issue['created'])}")
    print(f"  更新:     {format_datetime(issue['updated'])}")

    if issue.get('description'):
        print("\n📝 描述")
        print(f"  {issue['description'][:500]}{'...' if len(issue['description']) > 500 else ''}")

    if issue.get('comments'):
        print(f"\n💬 评论 ({len(issue['comments'])})")
        for c in issue['comments']:
            print(f"  [{format_datetime(c['created'])}] {c['author']}:")
            print(f"    {c['body'][:200]}{'...' if len(c['body']) > 200 else ''}")

    if issue.get('attachments'):
        print(f"\n📎 附件 ({len(issue['attachments'])})")
        for a in issue['attachments']:
            print(f"  - {a['filename']} ({format_size(a['size'])}) by {a['author']}")

    print("\n🔗 链接")
    print(f"  {issue['url']}")
    print()


def cmd_get(args):
    client = JiraClient()
    try:
        issue_key = extract_issue_key(args.issue)
        print(f"Fetching issue: {issue_key}\n")
        issue = client.get_issue_info(issue_key)
        if args.format == 'json':
            print_json(issue)
        else:
            print_issue_detail(issue)
        return 0
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Error fetching issue: {e}")
        return 1


def cmd_download(args):
    client = JiraClient()
    try:
        issue_key = extract_issue_key(args.issue)
        print(f"Downloading attachments for: {issue_key}\n")
        dest_dir = args.dest or os.path.join('attachments', issue_key)
        downloaded = client.download_issue_attachments(issue_key, dest_dir)
        if downloaded:
            print(f"\nDownloaded {len(downloaded)} file(s) to: {dest_dir}")
        else:
            print("No attachments found.")
        return 0
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Error downloading attachments: {e}")
        return 1


def cmd_list(args):
    client = JiraClient()
    print(f"Fetching issues for: {args.assignee}")
    print()
    try:
        issues = client.get_issues_by_assignee(
            args.assignee,
            max_results=args.max_results
        )
        if args.format == 'json':
            print_json(issues)
        elif args.format == 'detail':
            for issue in issues:
                print_issue_detail(issue)
            print(f"Total: {len(issues)} issues")
        else:
            print_table(issues)
        return 0
    except Exception as e:
        print(f"Error fetching issues: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(description='Jira issue fetcher')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    get_parser = subparsers.add_parser('get', help='Get a single issue by key or URL')
    get_parser.add_argument('issue')
    get_parser.add_argument('-f', '--format', choices=['detail', 'json'], default='detail')
    get_parser.set_defaults(func=cmd_get)

    download_parser = subparsers.add_parser('download', help='Download attachments for an issue')
    download_parser.add_argument('issue')
    download_parser.add_argument('-d', '--dest')
    download_parser.set_defaults(func=cmd_download)

    list_parser = subparsers.add_parser('list', help='List issues by assignee')
    list_parser.add_argument('-a', '--assignee', default='zhangyu1@70mai.com')
    list_parser.add_argument('-f', '--format', choices=['table', 'json', 'detail'], default='table')
    list_parser.add_argument('-m', '--max-results', type=int, default=100)
    list_parser.set_defaults(func=cmd_list)

    parser.add_argument('--test', action='store_true', help='Test connection only')
    args = parser.parse_args()

    if not config.validate():
        print("\nPlease create a .env file with your Jira credentials.")
        print("Copy .env.example to .env and fill in your token.")
        return 1

    client = JiraClient()
    if args.test:
        print("Testing connection to Jira...")
        if client.test_connection():
            print("Connection successful!")
            return 0
        print("Connection failed!")
        return 1

    if args.command and hasattr(args, 'func'):
        return args.func(args)

    parser.print_help()
    return 0


if __name__ == '__main__':
    exit(main())
