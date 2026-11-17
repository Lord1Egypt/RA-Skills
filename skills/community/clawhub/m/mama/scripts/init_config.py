#!/usr/bin/env python3
"""Initialize single-account mail assistant configuration."""

from __future__ import annotations

import argparse
import getpass
import json
import os
import subprocess
import sys
from pathlib import Path

from mail_accounts import (
    DEFAULT_JSON_CONFIG,
    LEGACY_PY_CONFIG,
    load_accounts,
    make_account_id,
    write_accounts_config,
)
from _version import VERSION

DEFAULT_DOMAIN = ""  # Optional deployment default; empty means full email is required.
_IMAP_SSL_PORT = 993
_SMTP_SSL_PORT = 465
DEFAULT_KEYWORDS = [
    "会议", "培训", "审批", "待办", "任务", "项目", "需求", "合同",
    "报价", "付款", "发票", "客户", "面试", "报名", "确认", "通知",
]
IMAP_VALUE_FIELD = "IMAP_CLIENT_VALUE"
SMTP_VALUE_FIELD = "SMTP_CLIENT_VALUE"

# Provider name mapping and IMAP host overrides (no hardcoded server addresses).
# For most providers, imap.<domain> and smtp.<domain> work out of the box.
_PROVIDER_NAMES: dict[str, str] = {
    "gmail.com":       "gmail",
    "googlemail.com":  "gmail",
    "outlook.com":     "outlook",
    "hotmail.com":     "outlook",
    "live.com":        "outlook",
    "msn.com":         "outlook",
    "office365.com":   "office365",
    "163.com":         "netease-163",
    "126.com":         "netease-126",
    "yeah.net":        "netease-yeah",
    "qq.com":          "qq",
    "foxmail.com":     "foxmail",
    "aliyun.com":      "aliyun",
    "189.cn":          "189-mail",
    "icloud.com":      "icloud",
    "me.com":          "icloud",
    "mac.com":         "icloud",
    "yahoo.com":       "yahoo",
    "sina.com":        "sina",
    "sina.cn":         "sina",
    "vip.sina.com":    "sina-vip",
    "vip.sina.cn":     "sina-vip",
    "sohu.com":        "sohu",
}

# Providers whose IMAP/SMTP host or port differs from imap.<domain>/smtp.<domain>.
# Values are (imap_host, imap_port, smtp_host, smtp_port).
_SERVER_OVERRIDES: dict[str, tuple[str, int, str, int]] = {
    "gmail.com":       ("imap.gmail.com", _IMAP_SSL_PORT, "smtp.gmail.com", 587),
    "googlemail.com":  ("imap.gmail.com", _IMAP_SSL_PORT, "smtp.gmail.com", 587),
    "outlook.com":     ("outlook.office365.com", _IMAP_SSL_PORT, "smtp-mail.outlook.com", 587),
    "hotmail.com":     ("outlook.office365.com", _IMAP_SSL_PORT, "smtp-mail.outlook.com", 587),
    "live.com":        ("outlook.office365.com", _IMAP_SSL_PORT, "smtp-mail.outlook.com", 587),
    "msn.com":         ("outlook.office365.com", _IMAP_SSL_PORT, "smtp-mail.outlook.com", 587),
    "office365.com":   ("outlook.office365.com", _IMAP_SSL_PORT, "smtp.office365.com", 587),
    "foxmail.com":     ("imap.qq.com", _IMAP_SSL_PORT, "smtp.qq.com", _SMTP_SSL_PORT),
    "icloud.com":      ("imap.mail.me.com", _IMAP_SSL_PORT, "smtp.mail.me.com", 587),
    "me.com":          ("imap.mail.me.com", _IMAP_SSL_PORT, "smtp.mail.me.com", 587),
    "mac.com":         ("imap.mail.me.com", _IMAP_SSL_PORT, "smtp.mail.me.com", 587),
    "yahoo.com":       ("imap.mail.yahoo.com", _IMAP_SSL_PORT, "smtp.mail.yahoo.com", _SMTP_SSL_PORT),
}

# Providers whose SMTP port is 587 (STARTTLS) instead of the default 465 (SSL).
_SMTP_STARTTLS_DOMAINS = {"outlook.com", "hotmail.com", "live.com", "msn.com", "office365.com", "gmail.com", "googlemail.com", "icloud.com", "me.com", "mac.com"}


def infer_provider(domain: str) -> tuple[str, str, int, str, int]:
    dl = domain.lower()
    provider_name = _PROVIDER_NAMES.get(dl, "custom")

    if dl in _SERVER_OVERRIDES:
        imap_host, imap_port, smtp_host, smtp_port = _SERVER_OVERRIDES[dl]
        return (provider_name, imap_host, imap_port, smtp_host, smtp_port)

    return (
        provider_name,
        _derive_imap_host(dl),
        _IMAP_SSL_PORT,
        _derive_smtp_host(dl),
        587 if dl in _SMTP_STARTTLS_DOMAINS else _SMTP_SSL_PORT,
    )


def _derive_imap_host(domain: str) -> str:
    """Construct IMAP server address from email domain."""
    return f"imap.{domain}"


def _derive_smtp_host(domain: str) -> str:
    """Construct SMTP server address from email domain."""
    return f"smtp.{domain}"

_CLIENT_PWD_WHERE = (
    "获取客户端值：在邮箱服务商后台开启 IMAP/SMTP，并生成客户端值。\n"
    "（客户端值通常不同于网页登录信息，请以服务商说明为准）"
)
_SPECIAL_CHAR_HINT = (
    "客户端值可能包含特殊字符。\n"
    "  ✓ 推荐：以下交互输入不回显、不经过 shell，可粘贴任意字符。\n"
    "  ✓ 非交互：使用 --value-env、--value-file 或 --value-stdin。\n"
    "  ✗ 不要把客户端值直接写进命令行参数、日志或聊天记录。"
)


# ---------------------------------------------------------------------------
# Helper: email normalization
# ---------------------------------------------------------------------------


def normalize_user(raw: str, default_domain: str = DEFAULT_DOMAIN) -> tuple[str, bool]:
    """Return (normalized_email, was_autocompleted).

    If the input contains no '@', auto-append the configured default domain.
    """
    value = raw.strip()
    if not value:
        return "", False
    if "@" not in value:
        if not default_domain:
            raise ValueError("邮箱账号需包含域名，例如 user@<域名>。")
        return f"{value}@{default_domain}", True
    return value, False


# ---------------------------------------------------------------------------
# Config writers
# ---------------------------------------------------------------------------


def _py_string(value: str) -> str:
    return repr(value)


def build_account_config(
    host: str,
    port: int,
    user: str,
    client_value: str,
    smtp_host: str = "",
    smtp_port: int = 465,
    provider: str = "custom",
) -> dict:
    return {
        "mail_provider": provider,
        "mail_user": user,
        "imap_host": host,
        "imap_port": int(port),
        "imap_user": user,
        "imap_client_value": client_value,
        "from_name": "邮箱智能体",
        "smtp_host": smtp_host,
        "smtp_port": int(smtp_port),
        "smtp_user": "",
        "smtp_client_value": "",
    }


def write_digest_config(path: Path, domain: str = DEFAULT_DOMAIN) -> None:
    if path.exists():
        return
    # Derive trusted domains from the user's email domain at first run.
    trusted = [domain] if domain else []
    path.write_text(
        f"""# 邮箱智能体非敏感配置

CHECK_WINDOW = {{
    "enabled": True,
    "workdays": [1, 2, 3, 4, 5],
    "start": "08:00",
    "end": "18:00",
    "interval_hours": 2,
}}

WATCH_KEYWORDS = {DEFAULT_KEYWORDS!r}

WATCH_DEADLINES = True

DEADLINE_HINTS = [
    "截止", "截至", "限于", "之前", "前完成", "前反馈", "前报送",
    "请于", "务必于", "须于", "需于", "最迟", "办理期限",
    "反馈期限", "报送期限", "完成时间", "截止时间",
    "deadline", "due", "before", "by",
]

TRUSTED_DOMAINS = {trusted!r}

DEFAULT_PUSH_CHANNEL = "current"
MAX_EMAILS = 30
SINCE_HOURS = 2
""",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Welcome and mode notices
# ---------------------------------------------------------------------------


def _print_welcome() -> None:
    """Full welcome shown on first-time setup."""
    print("""
欢迎使用邮箱智能体！

本智能体支持配置一个或多个邮箱账号，可按默认账号、指定账号或全部账号检查邮件。
支持常见个人邮箱（如 189 邮箱、QQ 邮箱、163 邮箱、Outlook/Gmail）以及企业内部邮箱；未识别域名时可手动指定 IMAP/SMTP 服务器。

配置完成后，智能体会自动检查新邮件，重点识别：
  · 会议、培训、审批、待办、任务、项目、需求、合同、报价、付款、发票、客户、面试、报名、确认、通知
  · 含截止时间、反馈期限、报送期限的待办邮件

检查结果自动生成摘要和待办，推送到当前通道。

此外，你还可以直接用自然语言提示词与助手交互：
  · 批量处理邮件：筛选、标记、回复草稿
  · 下载附件：将指定邮件的附件保存到本地
  · 快速转发：查阅邮件后一步转发给指定同事
  · 自定义检查：随时按关键词或时间范围即时查询

	新增账号只需提供完整邮箱账号和客户端值，其余均使用默认值。后续可重复运行初始化命令添加更多账号，或用 --set-default 切换默认账号。
""")


def _print_reconfigure_notice(mail_config: Path) -> None:
    """Brief notice shown when --force is used to overwrite an existing config."""
    existing = _peek_existing_config(mail_config)
    if existing:
        print(f"\n重新配置邮箱智能体（原账号：{existing}）")
    else:
        print("\n重新配置邮箱智能体。")


# ---------------------------------------------------------------------------
# Show existing config (for --force overwrite awareness)
# ---------------------------------------------------------------------------


def _peek_existing_config(path: Path) -> str:
    """Return configured accounts for display only."""
    try:
        _, accounts = load_accounts(path if path.exists() else None)
    except Exception:
        return ""
    values = [f"{account['id']}={account['user']} @ {account['imap_host']}" for account in accounts.values()]
    return "; ".join(values)


def _peek_existing_config_module(path: Path):
    """Import an existing mail_config.py and return the module object."""
    try:
        import importlib.util

        spec = importlib.util.spec_from_file_location("_peek_mail_cfg", str(path))
        if spec is None or spec.loader is None:
            return type("_Empty", (), {})()
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception:
        return type("_Empty", (), {})()


# ---------------------------------------------------------------------------
# Client value resolution
# ---------------------------------------------------------------------------


def resolve_client_value(args: argparse.Namespace) -> str:
    """Return the client value from whichever source the user chose.

    Sources (at most one may be active):
      --value-env     read from named environment variable
      --value-file    read from local file (first line)
      --value-stdin   read first line from stdin pipe
      (none)             interactive getpass (no echo, safest for humans)
    """
    active = [
        bool(args.value_env),
        bool(args.value_file),
        bool(args.value_stdin),
    ]
    if sum(active) > 1:
        raise ValueError(
            "只能选择一种客户端值输入方式：--value-env、--value-file 或 --value-stdin。"
        )

    # --- 1. Environment variable ---
    if args.value_env:
        value = os.environ.get(args.value_env, "")
        if not value:
            raise ValueError(f"环境变量 {args.value_env!r} 未设置或为空。")
        return value

    # --- 2. Client value file ---
    if args.value_file:
        p = Path(args.value_file).expanduser()
        if not p.exists():
            raise ValueError(f"客户端值文件不存在：{p}")
        # Read first non-empty line; strip only trailing newline to preserve spaces.
        for line in p.read_text(encoding="utf-8").splitlines():
            if line:
                return line
        raise ValueError(f"客户端值文件为空：{p}")

    # --- 3. Stdin pipe (non-interactive scripted use) ---
    if args.value_stdin:
        if sys.stdin.isatty():
            # Stdin is a terminal, not a pipe — warn and fall back to getpass.
            print(
                "提示：--value-stdin 适用于由调用方通过标准输入传入客户端值。\n"
                "当前检测到终端交互，已自动切换为不回显输入。",
                file=sys.stderr,
            )
        else:
            raw = sys.stdin.readline()
            # Strip only the trailing newline; preserve all other characters.
            value = raw.rstrip("\r\n")
            if not value:
                raise ValueError("从 stdin 读取到空客户端值。")
            return value

    # --- 4. Interactive getpass (default, safest for humans) ---
    print(_CLIENT_PWD_WHERE)
    print(_SPECIAL_CHAR_HINT)
    print()
    return getpass.getpass("请输入客户端值（输入不显示，可直接粘贴）：")


# ---------------------------------------------------------------------------
# Validation and display
# ---------------------------------------------------------------------------


def validate_connection(script_dir: Path, account_id: str = "") -> int:
    """Run read_emails.py in a subprocess to test IMAP connectivity."""
    result = subprocess.run(
        [
            sys.executable,
            str(script_dir / "read_emails.py"),
            "--account",
            account_id,
            "--since-hours",
            "1",
            "--max-emails",
            "1",
        ],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode == 0:
        print("✓ 邮箱智能体连接验证成功。")
    else:
        print("✗ 邮箱智能体连接验证失败。")
        if result.stderr:
            print(result.stderr.strip())
        print("\n如需重新配置，运行：")
        print("  python scripts/init_config.py --force --user 你的账号@<域名> --imap-host imap.<域名> --smtp-host smtp.<域名>")
    return result.returncode


def print_current_config(account_id: str, user: str, host: str, port: int, smtp_host: str = "", smtp_port: int = 465) -> None:
    print()
    print("当前配置：")
    provider = infer_provider(user.rsplit("@", 1)[-1])[0] if "@" in user else "custom"
    print(f"  账号 ID   ：{account_id}")
    print(f"  邮箱账号  ：{user}")
    print(f"  服务商    ：{provider}")
    print(f"  IMAP 服务器：{host}:{port}")
    print(
        f"  SMTP 服务器：{smtp_host}:{smtp_port}（默认沿用上述账号和客户端值）"
    )
    print("  检查范围  ：工作日 08:00–18:00，每 2 小时")
    print("  关注关键词：" + "、".join(DEFAULT_KEYWORDS))
    print("  截止时间  ：已启用")
    print("  推送通道  ：当前通道")
    print()
    print("如需修改：")
    print(
        "  邮箱账号、客户端值、SMTP：修改 scripts/mail_config.json，或重新运行 init_config.py --force"
    )
    print("  检查时间、关键词、可信域名：修改 scripts/digest_config.py")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description=f"初始化邮箱智能体配置 ({VERSION})",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
客户端值输入方式（推荐顺序）：
  1. 交互输入（默认）：不回显、不经 shell，支持任意特殊字符
  2. --value-env VAR         读取环境变量，适合脚本/Agent 调用
  3. --value-file /path/value 读取文件第一行，适合 Agent 写入临时文件后调用
  4. --value-stdin           从标准输入读取

示例（Agent 调用）：
  python init_config.py --user your_name@<域名> --value-file /tmp/mail-value.txt
  python init_config.py --user your_name@<域名> --value-env MAIL_VALUE

支持范围：
  - 可配置多个邮箱账号，并通过 --account 指定账号、--set-default 设置默认账号
  - 支持 189 邮箱、QQ 邮箱、163 邮箱、Outlook/Gmail 等常见邮箱
  - 支持企业内部邮箱；必要时用 --imap-host/--smtp-host 手动指定服务器
""",
    )
    parser.add_argument(
        "--version", action="version", version=f"邮箱智能体 {VERSION}"
    )
    parser.add_argument(
        "--user",
        default="",
        help="完整邮箱账号，如 user@qq.com、user@189.cn 或企业内部邮箱；仅在配置了 --domain 时可只输入用户名",
    )
    parser.add_argument("--domain", default=DEFAULT_DOMAIN, help="默认邮箱域名，用于补全不含 @ 的用户名")
    parser.add_argument("--provider", default="", help="服务商标识；默认根据邮箱域名自动识别")
    parser.add_argument("--account", default="", help="账号 ID；默认由邮箱本地名生成")
    parser.add_argument("--set-default", action="store_true", help="将本次配置设为默认账号")
    parser.add_argument(
        "--value-env",
        default="",
        metavar="VAR",
        help="从指定环境变量读取客户端值（适合 Agent 调用）",
    )
    parser.add_argument(
        "--value-file",
        default="",
        metavar="FILE",
        help="从本地文件第一行读取客户端值（适合 Agent 写入临时文件后调用）",
    )
    parser.add_argument(
        "--value-stdin",
        action="store_true",
        help="从标准输入读取客户端值",
    )
    parser.add_argument("--imap-host", default="")
    parser.add_argument("--imap-port", type=int, default=_IMAP_SSL_PORT)
    parser.add_argument("--smtp-host", default="")
    parser.add_argument("--smtp-port", type=int, default=0)
    parser.add_argument("--skip-test", action="store_true", help="跳过连接验证")
    parser.add_argument("--force", action="store_true", help="强制覆盖已有配置")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    mail_config = DEFAULT_JSON_CONFIG
    legacy_mail_config = LEGACY_PY_CONFIG
    digest_config = script_dir / "digest_config.py"

    print("─" * 50)
    print(f"邮箱智能体 · 初始化配置  v{VERSION}")
    print("─" * 50)

    # --- Mode detection: first-time vs. reconfigure vs. already configured ---
    has_config = mail_config.exists() or legacy_mail_config.exists()
    is_first_time = not has_config
    is_reconfigure = has_config and args.force

    if is_first_time:
        _print_welcome()
    elif is_reconfigure:
        _print_reconfigure_notice(mail_config)
    elif not args.user:
        # Config exists, --force not supplied: show status and exit.
        existing_info = _peek_existing_config(mail_config)
        print(f"\n配置文件已存在：{mail_config if mail_config.exists() else legacy_mail_config}")
        if existing_info:
            print(f"当前配置账号：{existing_info}")
        print("如需覆盖，请使用 --force 参数。")
        # Derive domain from existing config for digest_config generation.
        existing_user = ""
        try:
            _, accounts = load_accounts()
            existing_user = next(iter(accounts.values())).get("user", "")
        except Exception:
            existing_user = ""
        existing_domain = existing_user.rsplit("@", 1)[-1] if "@" in existing_user else ""
        write_digest_config(digest_config, domain=existing_domain)
        return 0

    # --- Step 1: email account ---
    raw_user = (
        args.user
        or input(
            "请输入完整邮箱账号（如 user@qq.com、user@189.cn 或 user@company.example）："
        ).strip()
    )
    if not raw_user:
        print("未提供邮箱账号，初始化终止。", file=sys.stderr)
        return 1

    try:
        user, autocompleted = normalize_user(raw_user, args.domain.strip())
    except ValueError as exc:
        print(f"配置失败：{exc}", file=sys.stderr)
        return 1
    if autocompleted:
        print(f"已自动补全：{user}")
    account_id = args.account.strip() or make_account_id(user)

    # Derive IMAP/SMTP host addresses from the email domain.
    domain = user.rsplit("@", 1)[-1] if "@" in user else DEFAULT_DOMAIN
    inferred_provider, inferred_imap_host, inferred_imap_port, inferred_smtp_host, inferred_smtp_port = infer_provider(domain)
    provider = args.provider or inferred_provider
    imap_host = args.imap_host or inferred_imap_host
    imap_port = args.imap_port or inferred_imap_port
    smtp_host = args.smtp_host or inferred_smtp_host
    smtp_port = args.smtp_port or inferred_smtp_port

    # --- Step 2: client value ---
    print()
    try:
        client_value = resolve_client_value(args)
    except ValueError as exc:
        print(f"配置失败：{exc}", file=sys.stderr)
        return 1
    if not client_value:
        print("未提供客户端值，初始化终止。", file=sys.stderr)
        return 1

    # --- Write configs ---
    default_account, accounts = load_accounts() if has_config else ("", {})
    if account_id in accounts and not args.force:
        print(f"配置失败：账号 ID 已存在：{account_id}。如需覆盖，请使用 --force。", file=sys.stderr)
        return 1
    accounts[account_id] = build_account_config(
        imap_host, imap_port, user, client_value, smtp_host, smtp_port, provider
    )
    default_account = account_id if args.set_default or not default_account else default_account
    write_accounts_config(mail_config, default_account, accounts)
    write_digest_config(digest_config, domain=domain)
    print("\n✓ 邮箱智能体配置已保存。")
    print_current_config(account_id, user, imap_host, imap_port, smtp_host, smtp_port)

    if args.skip_test:
        return 0
    return validate_connection(script_dir, account_id)


if __name__ == "__main__":
    raise SystemExit(main())
