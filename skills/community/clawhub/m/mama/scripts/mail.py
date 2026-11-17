#!/usr/bin/env python3
"""Unified mail agent commands."""

from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from email.message import EmailMessage
from pathlib import Path

from _version import VERSION
from mail_client import (
    ACCOUNT_HEADER,
    build_forward_draft,
    build_reply_draft,
    download_attachments,
    fetch_message,
    load_account,
    load_all_accounts,
    load_draft,
    mark_seen,
    move_message,
    parse_date_for_sort,
    save_draft,
    search_messages,
    send_message,
)

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_OUTPUT_DIR = SKILL_DIR / ".temp"


def _print_json(data) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def _brief(item: dict) -> dict:
    return {
        "account": item.get("account", ""),
        "uid": item.get("uid", ""),
        "mailbox": item.get("mailbox", ""),
        "subject": item.get("subject", ""),
        "from": item.get("from", ""),
        "date": item.get("date", ""),
        "attachments": item.get("attachments", []),
        "message_id": item.get("message_id", ""),
    }


def _print_message(item: dict) -> None:
    print("邮件内容")
    print("-" * 40)
    if item.get("account"):
        print(f"账号：{item.get('account')}")
    print(f"UID：{item.get('uid', '')}")
    print(f"文件夹：{item.get('mailbox', '')}")
    print(f"主题：{item.get('subject') or '(无主题)'}")
    print(f"发件人：{item.get('from', '')}")
    print(f"收件人：{item.get('to', '')}")
    if item.get("cc"):
        print(f"抄送：{item.get('cc')}")
    print(f"时间：{item.get('date', '')}")
    if item.get("attachments"):
        print("附件：" + "、".join(item.get("attachments", [])))
    if item.get("links"):
        print("链接：")
        for link in item.get("links", [])[:20]:
            label = link.get("text") or "(无显示文本)"
            print(f"- {label}: {link.get('url', '')}")
    print("")
    print((item.get("body") or "").strip() or "(无正文)")


def _search_one_account(account, args: argparse.Namespace) -> list[dict]:
    return search_messages(
        query=args.query,
        sender=args.sender,
        subject=args.subject,
        since=args.since,
        before=args.before,
        has_attachment=args.has_attachment,
        unseen=args.unseen,
        seen=args.seen,
        mailbox=args.mailbox,
        limit=args.limit,
        account=account,
    )


def _date_sort_key(item: dict) -> tuple[int, float]:
    parsed = parse_date_for_sort(item)
    if parsed is None:
        return (0, 0.0)
    return (1, parsed.timestamp())


def cmd_search(args: argparse.Namespace) -> int:
    accounts = load_all_accounts() if args.all_accounts else [load_account(args.account)]
    items = []
    if args.all_accounts and len(accounts) > 1:
        max_workers = max(1, min(args.parallel_accounts, len(accounts)))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_map = {
                executor.submit(_search_one_account, account, args): account
                for account in accounts
            }
            for future in as_completed(future_map):
                account = future_map[future]
                try:
                    items.extend(future.result())
                except Exception as exc:
                    if args.json:
                        items.append({"account": account.account_id, "error": str(exc)})
                    else:
                        print(f"[{account.account_id}] 搜索失败：{exc}", file=sys.stderr)
    else:
        for account in accounts:
            try:
                items.extend(_search_one_account(account, args))
            except Exception as exc:
                if args.json:
                    items.append({"account": account.account_id, "error": str(exc)})
                else:
                    print(f"[{account.account_id}] 搜索失败：{exc}", file=sys.stderr)
    items = sorted(items, key=_date_sort_key, reverse=True)[: args.limit]
    if args.json:
        _print_json(items if args.full else [_brief(item) for item in items])
        return 0
    if not items:
        print("未找到匹配邮件。")
        return 0
    for idx, item in enumerate(items, 1):
        attach = " 有附件" if item.get("attachments") else ""
        acct = f"[{item.get('account')}] " if item.get("account") else ""
        print(f"{idx}. {acct}UID {item.get('uid')} | {item.get('date', '')} | {item.get('from', '')} | {item.get('subject', '(无主题)')}{attach}")
    return 0


def cmd_read(args: argparse.Namespace) -> int:
    account = load_account(args.account)
    item, _ = fetch_message(args.uid, mailbox=args.mailbox, mark_seen=args.mark_seen, account=account)
    if args.json:
        _print_json(item)
    else:
        _print_message(item)
    return 0


def cmd_attachments(args: argparse.Namespace) -> int:
    account = load_account(args.account)
    output_dir = Path(args.output_dir)
    paths = download_attachments(
        args.uid,
        output_dir=output_dir,
        mailbox=args.mailbox,
        account=account,
        allow_risky=args.allow_risky,
        max_attachment_bytes=args.max_bytes,
    )
    _print_json({"account": account.account_id, "uid": args.uid, "attachments": [str(path) for path in paths]})
    return 0


def cmd_reply_draft(args: argparse.Namespace) -> int:
    account = load_account(args.account)
    item, _ = fetch_message(args.uid, mailbox=args.mailbox, account=account)
    message = build_reply_draft(item, args.body, account=account)
    path = save_draft(message, Path(args.output_dir), prefix=f"{account.account_id}_reply_draft")
    _print_json({"account": account.account_id, "draft": str(path), "to": message.get("To", ""), "subject": message.get("Subject", "")})
    return 0


def cmd_forward(args: argparse.Namespace) -> int:
    account = load_account(args.account)
    item, _ = fetch_message(args.uid, mailbox=args.mailbox, account=account)
    message = build_forward_draft(item, args.to, args.body, account=account)
    if args.send:
        print(f"即将发送：账号={account.account_id} 发件人={message.get('From', '')} 收件人={args.to} 主题={message.get('Subject', '')}", file=sys.stderr)
        send_message(message, account=account)
        _print_json({"account": account.account_id, "sent": True, "to": args.to, "subject": message.get("Subject", "")})
        return 0
    path = save_draft(message, Path(args.output_dir), prefix=f"{account.account_id}_forward_draft")
    _print_json({"account": account.account_id, "sent": False, "draft": str(path), "to": args.to, "subject": message.get("Subject", "")})
    return 0


def cmd_send(args: argparse.Namespace) -> int:
    if not args.confirm:
        print("发送邮件需要显式添加 --confirm。", file=sys.stderr)
        return 2
    if args.draft:
        message = load_draft(Path(args.draft))
        draft_account = message.get(ACCOUNT_HEADER, "").strip()
        if draft_account and args.account and args.account != draft_account:
            print(
                f"草稿来源账号为 {draft_account}，不能使用 {args.account} 发送。",
                file=sys.stderr,
            )
            return 2
        account = load_account(args.account or draft_account)
    else:
        account = load_account(args.account)
        if not args.to or not args.subject:
            print("直接发送新邮件需要 --to 和 --subject。", file=sys.stderr)
            return 2
        message = EmailMessage()
        message["From"] = account.smtp_user or account.user
        message["To"] = args.to
        message["Subject"] = args.subject
        message.set_content(args.body or "", charset="utf-8")
    print(f"即将发送：账号={account.account_id} 发件人={message.get('From', '')} 收件人={message.get('To', '')} 主题={message.get('Subject', '')}", file=sys.stderr)
    send_message(message, account=account)
    _print_json({"account": account.account_id, "sent": True, "to": message.get("To", ""), "subject": message.get("Subject", "")})
    return 0


def cmd_mark_seen(args: argparse.Namespace) -> int:
    account = load_account(args.account)
    mark_seen(args.uid, mailbox=args.mailbox, seen=not args.unseen, account=account)
    _print_json({"account": account.account_id, "uid": args.uid, "mailbox": args.mailbox, "seen": not args.unseen})
    return 0


def cmd_move(args: argparse.Namespace) -> int:
    if not args.confirm:
        print("移动邮件需要显式添加 --confirm。", file=sys.stderr)
        return 2
    account = load_account(args.account)
    move_message(args.uid, args.folder, mailbox=args.mailbox, account=account)
    _print_json({"account": account.account_id, "uid": args.uid, "from": args.mailbox, "to": args.folder})
    return 0


def cmd_accounts(args: argparse.Namespace) -> int:
    accounts = load_all_accounts()
    data = [
        {
            "account": account.account_id,
            "user": account.user,
            "provider": account.provider,
            "imap": f"{account.imap_host}:{account.imap_port}",
            "smtp": f"{account.smtp_host}:{account.smtp_port}",
        }
        for account in accounts
    ]
    if args.json:
        _print_json(data)
    else:
        for item in data:
            print(f"{item['account']} | {item['user']} | {item['provider']} | IMAP {item['imap']} | SMTP {item['smtp']}")
    return 0


def add_account_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--account", default="", help="账号 ID；默认使用 default_account")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=f"邮箱智能体通用命令 ({VERSION})")
    parser.add_argument("--version", action="version", version=f"邮箱智能体 {VERSION}")
    sub = parser.add_subparsers(dest="command", required=True)

    accounts = sub.add_parser("accounts", help="列出已配置邮箱账号")
    accounts.add_argument("--json", action="store_true")
    accounts.set_defaults(func=cmd_accounts)

    search = sub.add_parser("search", help="按关键词、发件人、主题、时间和附件筛选邮件")
    add_account_arg(search)
    search.add_argument("--all-accounts", action="store_true", help="搜索所有已配置账号")
    search.add_argument("--parallel-accounts", type=int, default=4, help="跨账号搜索并发数")
    search.add_argument("--query", default="")
    search.add_argument("--from", dest="sender", default="")
    search.add_argument("--subject", default="")
    search.add_argument("--since", default="", help="YYYY-MM-DD")
    search.add_argument("--before", default="", help="YYYY-MM-DD")
    search.add_argument("--has-attachment", action="store_true")
    search.add_argument("--unseen", action="store_true")
    search.add_argument("--seen", action="store_true")
    search.add_argument("--mailbox", default="INBOX")
    search.add_argument("--limit", type=int, default=20)
    search.add_argument("--json", action="store_true")
    search.add_argument("--full", action="store_true")
    search.set_defaults(func=cmd_search)

    read = sub.add_parser("read", help="读取指定 UID 邮件完整正文、链接和附件信息")
    add_account_arg(read)
    read.add_argument("--uid", required=True)
    read.add_argument("--mailbox", default="INBOX")
    read.add_argument("--mark-seen", action="store_true")
    read.add_argument("--json", action="store_true")
    read.set_defaults(func=cmd_read)

    attachments = sub.add_parser("attachments", help="下载指定 UID 邮件附件")
    add_account_arg(attachments)
    attachments.add_argument("--uid", required=True)
    attachments.add_argument("--mailbox", default="INBOX")
    attachments.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR / "attachments"))
    attachments.add_argument("--allow-risky", action="store_true", help="允许保存高风险扩展名附件")
    attachments.add_argument("--max-bytes", type=int, default=25 * 1024 * 1024, help="单个附件最大字节数，0 表示不限制")
    attachments.set_defaults(func=cmd_attachments)

    reply = sub.add_parser("reply-draft", help="基于原邮件生成回复草稿")
    add_account_arg(reply)
    reply.add_argument("--uid", required=True)
    reply.add_argument("--mailbox", default="INBOX")
    reply.add_argument("--body", default="")
    reply.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    reply.set_defaults(func=cmd_reply_draft)

    forward = sub.add_parser("forward", help="转发指定 UID 邮件；默认生成草稿")
    add_account_arg(forward)
    forward.add_argument("--uid", required=True)
    forward.add_argument("--to", required=True)
    forward.add_argument("--mailbox", default="INBOX")
    forward.add_argument("--body", default="")
    forward.add_argument("--send", action="store_true", help="显式直接发送；默认只生成草稿")
    forward.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    forward.set_defaults(func=cmd_forward)

    send = sub.add_parser("send", help="显式发送草稿或新邮件")
    add_account_arg(send)
    send.add_argument("--draft", default="")
    send.add_argument("--to", default="")
    send.add_argument("--subject", default="")
    send.add_argument("--body", default="")
    send.add_argument("--confirm", action="store_true")
    send.set_defaults(func=cmd_send)

    seen = sub.add_parser("mark-seen", help="标记指定 UID 已读或未读")
    add_account_arg(seen)
    seen.add_argument("--uid", required=True)
    seen.add_argument("--mailbox", default="INBOX")
    seen.add_argument("--unseen", action="store_true")
    seen.set_defaults(func=cmd_mark_seen)

    move = sub.add_parser("move", help="移动指定 UID 邮件到目标文件夹")
    add_account_arg(move)
    move.add_argument("--uid", required=True)
    move.add_argument("--folder", required=True)
    move.add_argument("--mailbox", default="INBOX")
    move.add_argument("--confirm", action="store_true")
    move.set_defaults(func=cmd_move)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
