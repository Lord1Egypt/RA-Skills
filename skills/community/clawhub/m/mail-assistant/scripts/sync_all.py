#!/usr/bin/env python3
"""
Sync all configured email accounts.

Fetches new inbox emails, checks auto-reply rules, sends auto-replies.
Supports OpenClaw cron setup for hourly sync.

Usage:
    python sync_all.py                          # Sync all accounts
    python sync_all.py --account <account-id>   # Sync one account
    python sync_all.py --dry-run                # Show what would happen
    python sync_all.py --yes                     # Skip all confirmation prompts (use after user consent)
    python sync_all.py --setup-cron             # Install hourly cron job
    python sync_all.py --disable-cron           # Disable cron job
    python sync_all.py --enable-cron            # Enable cron job
"""

import datetime
import io
import json
import os
import sys
import tempfile
import time

# ⚠️ SECURITY: Use direct imports instead of subprocess for all script calls
# This eliminates command injection surface and improves reliability
import outlook_api as _outlook
import email_client as _imap_client
import auto_reply as _auto_reply


def _run_and_capture(func, *args, **kwargs):
    """Run a CLI-style function and capture its stdout as a string."""
    old_stdout = sys.stdout
    captured = io.StringIO()
    sys.stdout = captured
    try:
        func(*args, **kwargs)
    finally:
        sys.stdout = old_stdout
    return captured.getvalue()

# Force UTF-8 for console output
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from data_dir import ACCOUNTS_DIR, SYNC_STATE_PATH


# ── Sync State ─────────────────────────────────────────────────────────────


def _load_sync_state():
    if not os.path.exists(SYNC_STATE_PATH):
        return {}
    with open(SYNC_STATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_sync_state(state):
    with open(SYNC_STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def _update_sync_state(account_id, new_mails_count):
    state = _load_sync_state()
    state[account_id] = {
        "last_sync": datetime.datetime.now().isoformat(),
        "last_count": new_mails_count,
    }
    _save_sync_state(state)


# ── Account Discovery ──────────────────────────────────────────────────────


def _list_accounts():
    if not os.path.isdir(ACCOUNTS_DIR):
        return []
    accounts = []
    for fname in os.listdir(ACCOUNTS_DIR):
        if fname.endswith(".json") and not fname.endswith(".token.json"):
            accounts.append(os.path.splitext(fname)[0])
    return accounts


def _load_account(account_id):
    path = os.path.join(ACCOUNTS_DIR, f"{account_id}.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ── Mail Fetch ─────────────────────────────────────────────────────────────


def _fetch_new_mails(account):
    acct_type = account["type"]
    account_id = account["id"]

    if acct_type == "outlook":
        return _fetch_outlook_mails(account_id)
    elif acct_type in ("163", "qq"):
        return _fetch_imap_mails(account)
    else:
        print(f"[WARN] Unknown account type: {acct_type}", file=sys.stderr)
        return []


def _fetch_outlook_mails(account_id):
    """Fetch unread inbox emails via direct import (no subprocess)."""
    try:
        token = _outlook._get_token(account_id)
        stdout_text = _run_and_capture(_outlook.cmd_list_inbox, token,
                                        ["", "", "--unread", "--limit", "50"])
        if stdout_text.strip():
            return json.loads(stdout_text)
        return []
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON from Outlook API: {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"[ERROR] Outlook fetch failed: {e}", file=sys.stderr)
        return []


def _fetch_imap_mails(account):
    """Fetch unread inbox emails via direct import (no subprocess)."""
    account_id = account["id"]
    try:
        acct = _load_account(account_id)
        stdout_text = _run_and_capture(_imap_client.cmd_list_inbox, acct,
                                        ["", "", "--unread", "--limit", "50"])
        if stdout_text.strip():
            return json.loads(stdout_text)
        return []
    except json.JSONDecodeError:
        return []
    except Exception as e:
        print(f"[ERROR] IMAP fetch failed for {account_id}: {e}", file=sys.stderr)
        return []


# ── Auto-Reply Processing ──────────────────────────────────────────────────


def _process_auto_replies(account_id, emails, dry_run=False, yes=False):
    """
    Check auto-reply rules for each email and send replies if matched.
    
    ⚠️ SECURITY: Auto-replies can inadvertently create mail loops, amplify spam,
    or exfiltrate configured attachment files to untrusted senders.
    Always use --dry-run first to verify before sending.
    """
    sent_count = 0

    # ⚠️ SAFETY: Warn the user before sending ANY auto-replies (unless dry-run)
    if not dry_run and emails:
        print("[INFO] Processing auto-reply rules for incoming emails.", file=sys.stderr)
        print("[INFO] WARNING: Auto-replies may be sent to external senders.", file=sys.stderr)
        print("[INFO] Use --dry-run to preview before sending.", file=sys.stderr)

    for email_data in emails:
        # Use direct import: write email to temp JSON for auto_reply check
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump(email_data, f)
            check_path = f.name

        try:
            # ⚠️ SECURITY: Use direct import instead of subprocess
            stdout_text = _run_and_capture(_auto_reply.cmd_check, check_path)
            if not stdout_text.strip():
                continue
            
            try:
                check_result = json.loads(stdout_text)
            except json.JSONDecodeError:
                continue

            matched_rules = check_result.get("matched_rules", [])

            for rule in matched_rules:
                reply_body = rule.get("reply_template", "")
                if not reply_body:
                    continue

                if dry_run:
                    print(f"  [DRY-RUN] Would reply to {email_data.get('from', '?')}: "
                          f"rule={rule['id']}", file=sys.stderr)
                    continue

                # Build reply email JSON
                reply_subject = f"{rule.get('subject_prefix', 'Re: ')}{email_data.get('subject', '')}"
                reply_data = {
                    "to": [email_data.get("from", "")],
                    "subject": reply_subject,
                    "body_text": reply_body,
                }

                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".json", delete=False, encoding="utf-8"
                ) as f2:
                    json.dump(reply_data, f2)
                    reply_path = f2.name

                # ⚠️ SECURITY: Send via direct import instead of subprocess
                # Pass --yes if the parent sync consented
                acct = _load_account(account_id)
                try:
                    send_args = ["", "", reply_path]
                    if yes:
                        send_args.append("--yes")
                    if acct["type"] == "outlook":
                        token = _outlook._get_token(account_id)
                        _run_and_capture(_outlook.cmd_send, token, send_args)
                    else:
                        _run_and_capture(_imap_client.cmd_send, acct, send_args)
                except Exception as send_err:
                    print(f"[ERROR] Failed to send auto-reply for rule {rule['id']}: {send_err}", file=sys.stderr)
                finally:
                    os.unlink(reply_path)
                sent_count += 1

        finally:
            os.unlink(check_path)

    if sent_count > 0:
        print(f"[INFO] Sent {sent_count} auto-reply(ies). "
              f"Review rules at: {RULES_PATH}", file=sys.stderr)

    return sent_count


# ── Sync One Account ───────────────────────────────────────────────────────


def _sync_account(account_id, dry_run=False, yes=False):
    print(f"[SYNC] Checking account: {account_id}", file=sys.stderr)
    try:
        account = _load_account(account_id)
    except FileNotFoundError:
        print(f"[ERROR] Account not found: {account_id}", file=sys.stderr)
        return {"account": account_id, "error": "not_found"}

    try:
        emails = _fetch_new_mails(account)
    except Exception as e:
        print(f"[ERROR] Fetch failed for {account_id}: {e}", file=sys.stderr)
        return {"account": account_id, "error": str(e)}

    if not emails:
        print(f"  No new emails.", file=sys.stderr)
        _update_sync_state(account_id, 0)
        return {"account": account_id, "new_mails": 0, "auto_replies_sent": 0}

    print(f"  Found {len(emails)} new email(s).", file=sys.stderr)

    auto_replies = _process_auto_replies(account_id, emails, dry_run=dry_run, yes=yes)
    if auto_replies > 0:
        print(f"  Sent {auto_replies} auto-reply(ies).", file=sys.stderr)

    _update_sync_state(account_id, len(emails))
    return {
        "account": account_id,
        "new_mails": len(emails),
        "auto_replies_sent": auto_replies,
    }


# ── Commands ───────────────────────────────────────────────────────────────


def cmd_sync(account_filter=None, dry_run=False, yes=False):
    accounts = [account_filter] if account_filter else _list_accounts()

    if not accounts:
        print(json.dumps({"error": "No accounts configured.", "accounts_dir": ACCOUNTS_DIR}))
        sys.exit(1)

    results = []
    for acc in accounts:
        result = _sync_account(acc, dry_run=dry_run, yes=yes)
        results.append(result)

    print(json.dumps({"results": results}, indent=2, ensure_ascii=False))


def cmd_setup_cron():
    """Print instructions to set up the OpenClaw cron job for hourly sync."""
    script_path = os.path.abspath(__file__)
    print("=" * 60)
    print("SETUP: Hourly Email Sync Cron Job")
    print("=" * 60)
    print()
    print("Use the OpenClaw `cron` tool to create this job:")
    print()
    print("```json")
    print("{")
    print('  "name": "email-assistant-sync",')
    print('  "schedule": {')
    print('    "kind": "cron",')
    print('    "expr": "0 * * * *",')
    print('    "tz": "Asia/Shanghai"')
    print("  },")
    print('  "sessionTarget": "isolated",')
    print('  "payload": {')
    print('    "kind": "agentTurn",')
    print('    "message": "Run email sync for all accounts: python ' + script_path + '"')
    print("  },")
    print('  "description": "Hourly email sync for Email Assistant skill"')
    print("}")
    print("```")
    print()
    print("Or run this directly via the cron tool with the above payload.")
    print()


def cmd_disable_cron():
    print("[INFO] To disable the cron job, use the cron tool with action=update and enabled=false")
    print("  Find the job id with cron list, then update it.")
    print()
    print("  Or use: python sync_all.py --setup-cron to see the job definition,")
    print("  then run cron update with enabled=false.")


def cmd_enable_cron():
    print("[INFO] To enable the cron job, use the cron tool with action=update and enabled=true")


# ── Main ───────────────────────────────────────────────────────────────────


def main():
    args = sys.argv[1:]

    if "--setup-cron" in args:
        cmd_setup_cron()
        return
    if "--disable-cron" in args:
        cmd_disable_cron()
        return
    if "--enable-cron" in args:
        cmd_enable_cron()
        return

    account_filter = None
    dry_run = False
    yes = "--yes" in args

    if "--account" in args:
        idx = args.index("--account")
        if idx + 1 < len(args):
            account_filter = args[idx + 1]

    if "--dry-run" in args:
        dry_run = True

    cmd_sync(account_filter=account_filter, dry_run=dry_run, yes=yes)


if __name__ == "__main__":
    main()
