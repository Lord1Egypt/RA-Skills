#!/usr/bin/env python3
"""Main workflow for Mail Assistant digest."""

from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, wait
from datetime import datetime, timedelta
from pathlib import Path

from _version import VERSION
from analyze_emails import analyze_emails, format_markdown, load_python_config
from channel_notify import send_notification
from forward_mail import (
    choose_email,
    normalize_recipient,
    print_email,
    send_or_save_draft,
)
from mail_client import MailAccount, load_account, load_all_accounts
from read_emails import fetch_emails

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
MAIL_CONFIG = SCRIPT_DIR / "mail_config.py"
DIGEST_CONFIG = SCRIPT_DIR / "digest_config.py"
PROCESSED_CACHE = SKILL_DIR / ".temp" / "processed_message_ids.json"
DEFAULT_ACCOUNT_TIMEOUT_SECONDS = 45

def ensure_config() -> bool:
    if (MAIL_CONFIG.exists() or (SCRIPT_DIR / "mail_config.json").exists()) and DIGEST_CONFIG.exists():
        return True
    print("""检测到你是首次使用邮箱智能体。

我需要完成 3 步初始化：
1. 配置一个或多个邮箱账号的 IMAP/SMTP 连接
2. 设置重点关注规则
3. 设置自动检查时间

默认配置：
- 邮箱账号：支持多账户配置，可添加 189 邮箱、QQ 邮箱、163 邮箱、Outlook/Gmail 以及企业内部邮箱
- 邮箱服务商：根据完整邮箱域名自动识别，失败时可手动指定 IMAP/SMTP 服务器
- 检查时间：工作日 08:00-18:00，每 2 小时一次
- 关注关键词：会议、培训、审批、待办、任务、项目、需求、合同、报价、付款、发票、客户、面试、报名、确认、通知
- 时间要求：自动关注包含截止时间、反馈期限、报送期限、完成时间的邮件
- 推送方式：推送到当前通道

请先运行：
python scripts/init_config.py --user "你的账号@<域名>"
如需添加更多账号：
python scripts/init_config.py --account work --user "你的工作邮箱@<域名>" --set-default
""")
    return False


def load_processed_ids() -> set[str]:
    if not PROCESSED_CACHE.exists():
        return set()
    try:
        data = json.loads(PROCESSED_CACHE.read_text(encoding="utf-8"))
        return set(data.get("ids", []))
    except (OSError, json.JSONDecodeError):
        return set()


_MAX_PROCESSED_IDS = 2000  # Cap cache size to prevent unbounded growth.


def save_processed_ids(ids: set[str]) -> None:
    PROCESSED_CACHE.parent.mkdir(parents=True, exist_ok=True)
    # Keep only the most recent IDs (by sort order, which correlates with
    # message-ID chronology) to prevent the cache from growing indefinitely.
    trimmed = sorted(ids)[-_MAX_PROCESSED_IDS:]
    PROCESSED_CACHE.write_text(
        json.dumps({"ids": trimmed}, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def run_read_emails(
    since_hours: int,
    max_emails: int,
    account: MailAccount,
    mark_seen: bool = False,
    raw_dir: Path | None = None,
    timeout: int = 60,
) -> list[dict]:
    """Fetch emails in-process to avoid subprocess startup and JSON round-trip overhead."""
    if not account.imap_host or not account.user or not account.imap_client_value:
        raise RuntimeError(
            f"账号 {account.account_id} 缺少 IMAP 配置：请先运行 init_config.py。"
        )
    emails = fetch_emails(
        account.imap_host,
        account.imap_port,
        account.user,
        account.imap_client_value,
        since_hours=since_hours,
        max_emails=max_emails,
        mark_seen=mark_seen,
        raw_dir=str(raw_dir) if raw_dir is not None else "",
        account_id=account.account_id,
        timeout=timeout,
    )
    for item in emails:
        item["account"] = account.account_id
    return emails


def processed_key(item: dict) -> str:
    account = item.get("account") or "default"
    mailbox = item.get("mailbox") or "INBOX"
    uid = item.get("uid") or ""
    message_id = item.get("message_id") or ""
    if uid:
        return f"{account}:{mailbox}:uid:{uid}"
    return f"{account}:{mailbox}:mid:{message_id}"


def filter_new_emails(
    emails: list[dict], processed: set[str], include_processed: bool = False
) -> list[dict]:
    if include_processed:
        return emails[:]
    return [
        item
        for item in emails
        if not processed_key(item) or processed_key(item) not in processed
    ]


def warning_markdown(warnings: list[str]) -> str:
    lines = ["# 多账户邮箱智能体", "", "## 账号提醒", ""]
    lines.extend([f"- {item}" for item in warnings])
    return "\n".join(lines) + "\n"


def add_keyword(keyword: str) -> None:
    config = load_python_config(DIGEST_CONFIG)
    keywords = list(
        config.get(
            "WATCH_KEYWORDS",
            [
                "会议", "培训", "审批", "待办", "任务", "项目", "需求", "合同",
                "报价", "付款", "发票", "客户", "面试", "报名", "确认", "通知",
            ],
        )
    )
    if keyword not in keywords:
        keywords.append(keyword)
    lines = (
        DIGEST_CONFIG.read_text(encoding="utf-8").splitlines()
        if DIGEST_CONFIG.exists()
        else []
    )
    replaced = False
    new_line = "WATCH_KEYWORDS = " + repr(keywords)
    out = []
    for line in lines:
        if line.strip().startswith("WATCH_KEYWORDS"):
            out.append(new_line)
            replaced = True
        else:
            out.append(line)
    if not replaced:
        out.append(new_line)
    DIGEST_CONFIG.write_text(
        "\n".join(out).replace("'", '"') + "\n", encoding="utf-8"
    )
    print(f"已添加关注关键词：{keyword}")


def write_outputs(
    output_dir: Path, emails: list[dict], analysis: list[dict], markdown: str
) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    paths = {
        "emails": output_dir / f"emails_{timestamp}.json",
        "analysis": output_dir / f"analysis_{timestamp}.json",
        "summary": output_dir / f"summary_{timestamp}.md",
    }
    paths["emails"].write_text(
        json.dumps(emails, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    paths["analysis"].write_text(
        json.dumps(analysis, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    paths["summary"].write_text(markdown, encoding="utf-8")
    return paths


def cleanup_outputs(output_dir: Path, days: int) -> int:
    if days < 0 or not output_dir.exists():
        return 0
    cutoff = datetime.now() - timedelta(days=days)
    removed = 0
    for path in output_dir.rglob("*"):
        if not path.is_file():
            continue
        try:
            modified = datetime.fromtimestamp(path.stat().st_mtime)
        except OSError:
            continue
        if modified < cutoff:
            path.unlink()
            removed += 1
    return removed


def interactive_review(
    emails: list[dict], analysis: list[dict], config: dict, output_dir: Path
) -> None:
    focus_ids = {
        item.get("message_id")
        for item in analysis
        if item.get("is_focus") and item.get("message_id")
    }
    review_emails = [
        item for item in emails if not focus_ids or item.get("message_id") in focus_ids
    ]
    email_item = choose_email(review_emails)
    if email_item is None:
        return
    print_email(email_item)
    recipient_raw = input(
        "如若转发请输入对方完整邮箱地址（直接回车跳过转发）："
    ).strip()
    if not recipient_raw:
        print("已跳过转发。")
        return
    try:
        recipient = normalize_recipient(recipient_raw)
    except ValueError as exc:
        print(f"无法转发：{exc}")
        return
    should_send = input(
        "如已配置 SMTP，是否立即发送？输入 yes 发送，直接回车生成草稿："
    ).strip().lower() in {"y", "yes"}
    account = load_account(email_item.get("account", ""))
    mail_config = {
        "MAIL_USER": account.user,
        "IMAP_USER": account.user,
        "IMAP_CLIENT_VALUE": account.imap_client_value,
        "SMTP_HOST": account.smtp_host,
        "SMTP_PORT": account.smtp_port,
        "SMTP_USER": account.smtp_user,
        "SMTP_CLIENT_VALUE": account.smtp_client_value,
    }
    try:
        draft_path = send_or_save_draft(
            email_item, recipient, mail_config, output_dir, should_send
        )
    except ValueError as exc:
        print(f"无法转发：{exc}")
        return
    if draft_path is None:
        print(f"已转发给：{recipient}")
    else:
        print(f"已生成转发草稿：{draft_path}")
        print(f"收件人：{recipient}")


def main() -> int:
    parser = argparse.ArgumentParser(description=f"邮箱智能体 {VERSION}")
    parser.add_argument(
        "--version", action="version", version=f"邮箱智能体 {VERSION}"
    )
    parser.add_argument("--since-hours", type=int)
    parser.add_argument("--max-emails", type=int)
    parser.add_argument("--account", default="", help="账号 ID；默认使用 default_account")
    parser.add_argument("--all-accounts", action="store_true", help="巡检所有已配置账号")
    parser.add_argument("--parallel-accounts", type=int, default=4, help="多账号巡检并发数")
    parser.add_argument("--account-timeout", type=int, default=DEFAULT_ACCOUNT_TIMEOUT_SECONDS, help="等待其他账号返回的秒数")
    parser.add_argument("--mark-seen", action="store_true")
    parser.add_argument("--output-dir", default=str(SKILL_DIR / ".temp"))
    parser.add_argument("--keywords", default="")
    parser.add_argument("--add-keyword", default="")
    parser.add_argument("--trigger-channel", default="")
    parser.add_argument("--reply-channel", default="")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--include-processed", action="store_true")
    parser.add_argument(
        "--review", action="store_true", help="输出后选择邮件序号查阅正文并快速转发"
    )
    parser.add_argument(
        "--cleanup-days", type=int, help="清理输出目录中早于 N 天的历史文件"
    )
    parser.add_argument(
        "--save-raw",
        action="store_true",
        help="保存原始 .eml 文件到 .temp/raw/（默认不保存，开启后会额外下载完整邮件体增加耗时）",
    )
    args = parser.parse_args()

    # Always print version to stderr so it appears regardless of --json mode.
    print(f"邮箱智能体 {VERSION}", file=sys.stderr)

    if args.add_keyword:
        if not DIGEST_CONFIG.exists():
            print("请先初始化邮箱智能体配置。", file=sys.stderr)
            return 1
        add_keyword(args.add_keyword.strip())
        return 0

    if not ensure_config():
        return 1

    config = load_python_config(DIGEST_CONFIG)
    since_hours = args.since_hours or int(config.get("SINCE_HOURS", 2))
    max_emails = args.max_emails or int(config.get("MAX_EMAILS", 30))
    output_dir = Path(args.output_dir)

    if args.cleanup_days is not None:
        removed = cleanup_outputs(output_dir, args.cleanup_days)
        print(f"已清理历史输出文件：{removed} 个")

    _t0 = time.monotonic()
    print("正在连接邮件服务器...", file=sys.stderr, flush=True)
    raw_dir = output_dir / "raw" if args.save_raw else None
    processed = load_processed_ids()
    keywords = (
        [item.strip() for item in args.keywords.split(",") if item.strip()]
        if args.keywords
        else None
    )
    reply_channel = (
        args.reply_channel
        or args.trigger_channel
        or config.get("DEFAULT_PUSH_CHANNEL", "current")
    )
    warnings: list[str] = []
    primary_account_id = ""
    try:
        accounts = load_all_accounts() if args.all_accounts else [load_account(args.account)]
        emails = []

        if args.all_accounts and len(accounts) > 1:
            primary = accounts[0]
            primary_account_id = primary.account_id
            secondary = accounts[1:]
            max_workers = max(1, min(args.parallel_accounts, len(secondary)))
            executor = ThreadPoolExecutor(max_workers=max_workers)
            future_map = {
                executor.submit(
                    run_read_emails,
                    since_hours,
                    max_emails,
                    account,
                    args.mark_seen,
                    (raw_dir / account.account_id) if raw_dir else None,
                    args.account_timeout,
                ): account
                for account in secondary
            }

            print(
                f"优先读取主账号：{primary.account_id}",
                file=sys.stderr,
                flush=True,
            )
            primary_emails = run_read_emails(
                since_hours,
                max_emails,
                primary,
                args.mark_seen,
                (raw_dir / primary.account_id) if raw_dir else None,
                args.account_timeout,
            )
            emails.extend(primary_emails)

            primary_new = filter_new_emails(
                primary_emails, processed, args.include_processed
            )
            if not args.json:
                primary_analysis = analyze_emails(primary_new, config, keywords)
                primary_markdown = format_markdown(
                    primary_analysis, since_hours, len(primary_new)
                )
                send_notification(primary_markdown, reply_channel, args.output_dir)

            done, not_done = wait(future_map, timeout=max(0, args.account_timeout))
            for future in done:
                account = future_map[future]
                try:
                    emails.extend(future.result())
                except Exception as exc:
                    warnings.append(f"账号 {account.account_id} 读取失败：{exc}")
            for future in not_done:
                account = future_map[future]
                warnings.append(
                    f"账号 {account.account_id} 在 {args.account_timeout}s 内未返回，已跳过本轮补充。"
                )
                future.cancel()
            executor.shutdown(wait=False, cancel_futures=True)
        else:
            account = accounts[0]
            account_raw_dir = raw_dir / account.account_id if raw_dir else None
            emails.extend(
                run_read_emails(
                    since_hours,
                    max_emails,
                    account,
                    args.mark_seen,
                    account_raw_dir,
                    args.account_timeout,
                )
            )
    except RuntimeError as exc:
        print(f"邮箱智能体读取失败：{exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"邮箱智能体配置失败：{exc}", file=sys.stderr)
        return 2

    new_emails = filter_new_emails(emails, processed, args.include_processed)
    elapsed = time.monotonic() - _t0
    print(
        f"邮件读取完成，用时 {elapsed:.1f}s，正在分析...", file=sys.stderr, flush=True
    )
    analysis = analyze_emails(new_emails, config, keywords)
    markdown = format_markdown(analysis, since_hours, len(new_emails))
    if warnings:
        markdown = markdown.rstrip() + "\n\n" + warning_markdown(warnings)
    paths = write_outputs(output_dir, new_emails, analysis, markdown)

    new_ids = {processed_key(item) for item in new_emails if processed_key(item)}
    if new_ids:
        processed.update(new_ids)
        save_processed_ids(processed)

    if args.json:
        print(
            json.dumps(
                {
                    "version": VERSION,
                    "emails": len(new_emails),
                    "focus": len([item for item in analysis if item["is_focus"]]),
                    "outputs": {key: str(value) for key, value in paths.items()},
                    "warnings": warnings,
                    "analysis": analysis,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        if not (args.all_accounts and len(accounts) > 1):
            send_notification(markdown, reply_channel, args.output_dir)
        else:
            secondary_new = [
                item for item in new_emails if item.get("account") != primary_account_id
            ]
            if secondary_new or warnings:
                secondary_analysis = analyze_emails(secondary_new, config, keywords)
                supplemental = format_markdown(
                    secondary_analysis, since_hours, len(secondary_new)
                )
                if warnings:
                    supplemental = supplemental.rstrip() + "\n\n" + warning_markdown(warnings)
                send_notification(supplemental, reply_channel, args.output_dir)
        if args.review:
            interactive_review(new_emails, analysis, config, output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
