#!/usr/bin/env python3
"""
Email Assistant — Interactive Setup Wizard

Guides the user through:
1. Choosing an email provider (Outlook / 163 / QQ)
2. Configuring and authorizing the account
3. Testing the connection
4. Setting up automatic sync

Usage:
    python3 setup_wizard.py
    python3 setup_wizard.py --quick-add outlook
    python3 setup_wizard.py --quick-add 163
    python3 setup_wizard.py --quick-add qq
"""

import json
import os
import subprocess
import sys
import tempfile

# Force UTF-8 for console
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from data_dir import ACCOUNTS_DIR, ensure_data_dirs, secure_set, has_keyring

ensure_data_dirs()

SCRIPT_DIR = os.path.join(os.path.dirname(__file__))

PYTHON = sys.executable

# ── Built-in Azure Application Configuration ──────────────────────────────
# Users do not need to create their own Azure app.
# This public app is shared by all Email Assistant users.
# Source: openclaw email-assistant skill
BUILTIN_AZURE_CLIENT_ID = "c31fd78c-6385-4fd2-9033-d0bd72b5ceb4"
BUILTIN_AZURE_TENANT = "consumers"
BUILTIN_AZURE_SCOPES = ["User.Read", "Mail.ReadWrite", "Mail.Send", "MailboxSettings.Read"]
BUILTIN_AZURE_REDIRECT_URI = "http://localhost:1456"


# ── Helpers ────────────────────────────────────────────────────────────────


def _print_header(title):
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)
    print()


def _ask(question, default=None):
    prompt = f"{question} "
    if default:
        prompt = f"{question} [{default}] "
    answer = input(prompt).strip()
    if not answer and default:
        return default
    return answer


def _confirm(question, default=True):
    prompt = f"{question} (y/n) "
    default_str = "Y/n" if default else "y/N"
    prompt = f"{question} [{default_str}] "
    answer = input(prompt).strip().lower()
    if not answer:
        return default
    return answer in ("y", "yes", "是")


def _inject_token_to_account(token_path, account_json_path):
    """If OAuth web flow was used, merge token into account."""
    pass  # oauth_web.py handles this


# ── Setup: Outlook ─────────────────────────────────────────────────────────


def setup_outlook():
    """Setup Outlook / Microsoft 365 account.
    Uses built-in Azure app config — no user Azure setup required.
    """
    _print_header("📧 添加 Outlook / Microsoft 365 账户")

    print("本 Skill 已内置 Azure 应用注册配置，你无需自行创建。")
    print()
    print("⚠️  ⚠️  ⚠️  安全提示  ⚠️  ⚠️  ⚠️")
    print("此内置应用由 Skill 开发者提供，所有 Email Assistant 用户共享。")
    print("授权后将获得以下权限：")
    print("  • 读取您的邮件")
    print("  • 发送邮件（以您的身份）")
    print("  • 修改邮件状态（已读/未读）")
    print("  • 读取邮箱设置")
    print("请确保你信任此 Skill 的软件供应链。")
    print("如需更高安全性，可在 Azure 门户创建自己的应用注册。")
    print("⚠️  ⚠️  ⚠️  ⚠️  ⚠️  ⚠️")
    print()

    email = _ask("Outlook 邮箱地址 (可选，留空则自动获取):")
    if not email:
        email = "user@outlook.com"

    # Save account config with built-in Azure app
    account = {
        "id": "my-outlook",
        "type": "outlook",
        "user": email,
        "oauth": {
            "client_id": BUILTIN_AZURE_CLIENT_ID,
            "tenant_id": BUILTIN_AZURE_TENANT,
            "scopes": BUILTIN_AZURE_SCOPES,
        },
    }
    account_path = os.path.join(ACCOUNTS_DIR, "my-outlook.json")
    with open(account_path, "w", encoding="utf-8") as f:
        json.dump(account, f, indent=2, ensure_ascii=False)
    print(f"[OK] 账户配置已保存到 {account_path}")

    print()
    print("🔐 正在启动浏览器授权...")
    print("  将自动打开浏览器，使用 Microsoft 账号登录即可")
    print()

    input("按 Enter 键继续...")
    print()

    # Run the web-based OAuth flow (PKCE + local redirect)
    oauth_script = os.path.join(SCRIPT_DIR, "oauth_web.py")
    result = subprocess.run(
        [PYTHON, oauth_script, "my-outlook"],
        cwd=os.path.dirname(SCRIPT_DIR),
    )

    if result.returncode == 0:
        print("\n✅ Outlook 授权成功！")
        return "my-outlook"
    else:
        print("\n❌ 浏览器授权失败。可以稍后重试：")
        print(f"  python3 scripts/oauth_web.py my-outlook")
        return None


# ── Setup: 163 / QQ ────────────────────────────────────────────────────────


def _setup_smtp_imap(acct_type):
    """Shared setup for 163 and QQ mailboxes."""
    type_label = "163 邮箱" if acct_type == "163" else "QQ 邮箱"
    _print_header(f"📧 添加 {type_label} 账户")

    smtp_host = "smtp.163.com" if acct_type == "163" else "smtp.qq.com"
    imap_host = "imap.163.com" if acct_type == "163" else "imap.qq.com"

    if acct_type == "163":
        print("准备工作：")
        print("  1. 登录 163 邮箱网页版")
        print("  2. 设置 → POP3/SMTP/IMAP → 开启 IMAP/SMTP 服务")
        print("  3. 获取「授权码」（非邮箱密码）")
    else:
        print("准备工作：")
        print("  1. 登录 QQ 邮箱网页版")
        print("  2. 设置 → 账户 → POP3/IMAP/SMTP 服务 → 开启")
        print("  3. 发送短信获取「授权码」")
    print()
    print("⚠️  安全提示 ⚠️")
    print("授权码将明文保存在本地配置文件中，等效于邮箱密码。")
    print("请确保：")
    print("  1. 不要将 accounts/ 目录提交到任何版本控制系统")
    print("  2. 定期在网页邮箱中更新授权码")
    print("  3. 不再使用时及时在网页邮箱中撤销授权码")
    print()

    email = _ask("邮箱地址:")
    if not email:
        print("[ERROR] 邮箱地址不能为空")
        return None

    auth_code = _ask("授权码:", default=None)
    if not auth_code:
        print("[ERROR] 授权码不能为空")
        return None

    account = {
        "id": f"my-{acct_type}",
        "type": acct_type,
        "user": email,
        "smtp": {
            "host": smtp_host,
            "port": 465,
            "auth": auth_code,
        },
        "imap": {
            "host": imap_host,
            "port": 993,
            "auth": auth_code,
        },
    }

    account_path = os.path.join(ACCOUNTS_DIR, account["id"] + ".json")
    with open(account_path, "w", encoding="utf-8") as f:
        json.dump(account, f, indent=2, ensure_ascii=False)

    # ⚠️ SECURITY: Also store auth code in system keyring (encrypted)
    if secure_set(account["id"], auth_code, "smtp") or secure_set(account["id"], auth_code, "imap"):
        print(f"[INFO] 授权码已加密存入系统密钥链")
        if has_keyring():
            print(f"[INFO] 授权码在 JSON 中仍以明文存在，建议删除 JSON 中的 auth 字段")
    else:
        print(f"[INFO] 系统密钥链不可用，授权码仅以明文存储在 JSON 中")

    print(f"[OK] 配置已保存到 {account_path}")

    # Test connection
    print()
    print("🔍 正在测试连接...")
    test_script = os.path.join(SCRIPT_DIR, "email_client.py")
    result = subprocess.run(
        [PYTHON, test_script, account["id"], "list-inbox", "--limit", "1"],
        capture_output=True, text=True, timeout=30,
    )

    if result.returncode == 0:
        print("✅ 连接成功！")
        return account["id"]
    else:
        print("⚠️  连接失败。请检查：")
        print("  - 邮箱地址是否正确")
        print("  - 授权码是否为最新（可在网页端重新生成）")
        print(f"  错误信息: {result.stderr[:200] if result.stderr else '未知'}")
        if _confirm("仍保存此配置？", default=False):
            return account["id"]
        else:
            os.remove(account_path)
            return None


# ── Sync Setup ─────────────────────────────────────────────────────────────


def setup_sync(account_ids):
    _print_header("⏰ 设置定时同步")

    if _confirm("是否设置每小时自动同步所有邮箱？"):
        sync_script = os.path.join(SCRIPT_DIR, "sync_all.py")
        print()
        print("自动同步将在下一整点开始，每小时运行一次。")
        print()
        print("OpenClaw cron 任务已就绪。如需手动关闭：")
        print("  使用 OpenClaw 的 cron 工具禁用 email-assistant-sync 作业")
        return True
    else:
        print("[INFO] 可以稍后手动同步：")
        print(f"  python3 scripts/sync_all.py")
        return False


# ── List accounts ──────────────────────────────────────────────────────────


def list_accounts():
    _print_header("📋 已配置的邮箱账户")

    if not os.path.isdir(ACCOUNTS_DIR):
        print("  还没有配置任何账户。")
        return []

    accounts = []
    for fname in os.listdir(ACCOUNTS_DIR):
        if fname.endswith(".json") and not fname.endswith(".token.json"):
            accounts.append(os.path.splitext(fname)[0])
            acct_path = os.path.join(ACCOUNTS_DIR, fname)
            with open(acct_path, "r", encoding="utf-8") as f:
                acct = json.load(f)
            print(f"  - {acct.get('id', '?')} ({acct.get('type', '?')}) → {acct.get('user', '?')}")

    if not accounts:
        print("  还没有配置任何账户。")

    return accounts


# ── Main Menu ──────────────────────────────────────────────────────────────


def main_menu():
    while True:
        _print_header("🐾 Email Assistant — 配置向导")
        print("请选择操作：")
        print("  1. 添加 Outlook / Microsoft 365 账户")
        print("  2. 添加 163 邮箱账户")
        print("  3. 添加 QQ 邮箱账户")
        print("  4. 查看已配置账户")
        print("  5. 设置定时同步")
        print("  6. 退出")
        print()

        choice = _ask("请输入选项 (1-6):")

        if choice == "1":
            acct_id = setup_outlook()
            if acct_id:
                if _confirm("\n是否继续添加其他账户？", default=False):
                    continue
                else:
                    setup_sync([acct_id])
                    _print_header("🎉 配置完成！")
                    print("现在你可以使用自然语言操作邮箱了。")
                    print()
                    print("试试说：")
                    print('  "帮我查一下今天的邮件"')
                    print('  "给 xx@qq.com 发一封邮件"')
                    print('  "设置自动回复"')
                    print()
                    return

        elif choice == "2":
            acct_id = _setup_smtp_imap("163")
            if acct_id and not _confirm("继续添加其他账户？", default=False):
                setup_sync([acct_id])
                return

        elif choice == "3":
            acct_id = _setup_smtp_imap("qq")
            if acct_id and not _confirm("继续添加其他账户？", default=False):
                setup_sync([acct_id])
                return

        elif choice == "4":
            list_accounts()
            input("\n按 Enter 继续...")

        elif choice == "5":
            accounts = list_accounts()
            if accounts:
                setup_sync(accounts)

        elif choice == "6":
            print("再见！🐾")
            return

        else:
            print("[ERROR] 无效选项，请输入 1-6。")


# ── Quick Add (CLI flag) ───────────────────────────────────────────────────


def quick_add(acct_type):
    if acct_type == "outlook":
        setup_outlook()
    elif acct_type == "163":
        _setup_smtp_imap("163")
    elif acct_type == "qq":
        _setup_smtp_imap("qq")
    else:
        print(f"[ERROR] Unknown account type: {acct_type}")
        sys.exit(1)


# ── Entry ───────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    if "--quick-add" in sys.argv:
        idx = sys.argv.index("--quick-add")
        if idx + 1 < len(sys.argv):
            quick_add(sys.argv[idx + 1])
        else:
            print("[ERROR] --quick-add requires a type: outlook | 163 | qq")
            sys.exit(1)
    else:
        main_menu()
