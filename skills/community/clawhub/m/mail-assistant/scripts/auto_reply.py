#!/usr/bin/env python3
"""
Auto-reply rule management engine.

Rules are stored in ~/.openclaw/workspace/email-assistant/auto_reply_rules.json.

Usage:
    python auto_reply.py list
    python auto_reply.py add <rule-definition.json>
    python auto_reply.py toggle <rule-id>
    python auto_reply.py delete <rule-id>
    python auto_reply.py check <email-json>
"""

import json
import os
import sys
import uuid

# Force UTF-8 for console output
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from data_dir import RULES_PATH, confirm_action


# ── Data Layer ─────────────────────────────────────────────────────────────


def _load_rules():
    if not os.path.exists(RULES_PATH):
        return []
    with open(RULES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_rules(rules):
    with open(RULES_PATH, "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=2, ensure_ascii=False)


def _make_rule(definition):
    """Create a rule dict from user-provided definition."""
    return {
        "id": str(uuid.uuid4())[:8],
        "name": definition.get("name", ""),
        "enabled": definition.get("enabled", True),
        "match": {
            "to_addresses": definition.get("match", {}).get("to_addresses", []),
            "sender_domains": definition.get("match", {}).get("sender_domains", []),
            "keywords_subject": definition.get("match", {}).get("keywords_subject", []),
            "keywords_body": definition.get("match", {}).get("keywords_body", []),
        },
        "reply": {
            "subject_prefix": definition.get("reply", {}).get("subject_prefix", "Re: "),
            "body_template": definition.get("reply", {}).get("body_template", ""),
            "attachments": definition.get("reply", {}).get("attachments", []),
        },
        "created_at": __import__("time").time(),
    }


# ── Matching Engine ────────────────────────────────────────────────────────


def _matches_rule(email_data, rule):
    """Check if email_data matches the rule."""
    if not rule.get("enabled", True):
        return False

    match = rule.get("match", {})
    email_to = email_data.get("to", "").lower()
    email_from = email_data.get("from", "").lower()
    email_from_domain = email_from.split("@")[-1] if "@" in email_from else ""
    email_subject = (email_data.get("subject", "") or "").lower()
    email_body = (email_data.get("body_text", "") or "").lower()

    # Check To addresses
    to_addresses = [a.lower() for a in match.get("to_addresses", [])]
    if to_addresses and not any(addr in email_to for addr in to_addresses):
        return False

    # Check sender domains
    domains = [d.lower() for d in match.get("sender_domains", [])]
    if domains and email_from_domain not in domains:
        return False

    # Check subject keywords
    kw_subject = [k.lower() for k in match.get("keywords_subject", [])]
    if kw_subject and not any(kw in email_subject for kw in kw_subject):
        return False

    # Check body keywords
    kw_body = [k.lower() for k in match.get("keywords_body", [])]
    if kw_body and not any(kw in email_body for kw in kw_body):
        return False

    # ── Matching logic (AND across condition types, OR within each type) ──
    # All configured condition types (AND) must have at least one matching value.
    # For example: sender_domains AND keywords_subject both configured means
    # the email must come from a matching domain AND have a matching keyword.
    # Within a single condition type, any one value suffices (OR).
    # Empty match config = catch-all (matches every email).
    has_any_condition = to_addresses or domains or kw_subject or kw_body
    if not has_any_condition:
        return True  # Empty match config = catch-all (matches every email)

    return True  # All configured condition types have been satisfied (AND logic)


# ── Commands ───────────────────────────────────────────────────────────────


def cmd_list():
    rules = _load_rules()
    if not rules:
        print(json.dumps({"rules": [], "count": 0}))
        return
    # Show summary (without full body template to keep output readable)
    summary = []
    for r in rules:
        summary.append({
            "id": r["id"],
            "name": r.get("name", ""),
            "enabled": r.get("enabled", True),
            "match_summary": _summarize_match(r.get("match", {})),
            "reply_preview": (r.get("reply", {}).get("body_template", "") or "")[:80],
        })
    print(json.dumps({"rules": summary, "count": len(summary)}, indent=2, ensure_ascii=False))


def _summarize_match(match):
    parts = []
    if match.get("to_addresses"):
        parts.append(f"To: {', '.join(match['to_addresses'][:2])}")
    if match.get("sender_domains"):
        parts.append(f"Domain: {', '.join(match['sender_domains'][:2])}")
    if match.get("keywords_subject"):
        parts.append(f"Subject kw: {', '.join(match['keywords_subject'][:3])}")
    if match.get("keywords_body"):
        parts.append(f"Body kw: {', '.join(match['keywords_body'][:3])}")
    return "; ".join(parts) if parts else "(catch-all)"


def cmd_add(rule_json_path):
    if not os.path.exists(rule_json_path):
        print(f"[ERROR] File not found: {rule_json_path}", file=sys.stderr)
        sys.exit(1)

    with open(rule_json_path, "r", encoding="utf-8") as f:
        definition = json.load(f)

    rule = _make_rule(definition)
    match_summary = _summarize_match(rule.get("match", {}))
    desc = f"添加自动回复规则: {rule.get('name', '(unnamed)')} — {match_summary}"
    if not confirm_action(desc, sys.argv):
        print("[CANCELLED] 用户取消操作。")
        sys.exit(1)

    rules = _load_rules()
    rules.append(rule)
    _save_rules(rules)
    print(f"[OK] Rule added: {rule['id']} — {rule.get('name', '(unnamed)')}")
    print(json.dumps(rule, indent=2, ensure_ascii=False))


def cmd_toggle(rule_id):
    desc = f"切换自动回复规则 {rule_id} 的启用状态"
    if not confirm_action(desc, sys.argv):
        print("[CANCELLED] 用户取消操作。")
        return

    rules = _load_rules()
    for r in rules:
        if r["id"] == rule_id:
            r["enabled"] = not r.get("enabled", True)
            _save_rules(rules)
            status = "enabled" if r["enabled"] else "disabled"
            print(f"[OK] Rule {rule_id} is now {status}.")
            return
    print(f"[ERROR] Rule not found: {rule_id}", file=sys.stderr)
    sys.exit(1)


def cmd_delete(rule_id):
    desc = f"删除自动回复规则 {rule_id}"
    if not confirm_action(desc, sys.argv):
        print("[CANCELLED] 用户取消操作。")
        return

    rules = _load_rules()
    filtered = [r for r in rules if r["id"] != rule_id]
    if len(filtered) == len(rules):
        print(f"[ERROR] Rule not found: {rule_id}", file=sys.stderr)
        sys.exit(1)
    _save_rules(filtered)
    print(f"[OK] Rule {rule_id} deleted.")


def cmd_check(email_json_path):
    if not os.path.exists(email_json_path):
        print(f"[ERROR] File not found: {email_json_path}", file=sys.stderr)
        sys.exit(1)

    with open(email_json_path, "r", encoding="utf-8") as f:
        email_data = json.load(f)

    rules = _load_rules()
    matched = []
    for rule in rules:
        if _matches_rule(email_data, rule):
            matched.append({
                "id": rule["id"],
                "name": rule.get("name", ""),
                "reply_template": rule.get("reply", {}).get("body_template", ""),
                "subject_prefix": rule.get("reply", {}).get("subject_prefix", "Re: "),
            })

    print(json.dumps({
        "matched_rules": matched,
        "count": len(matched),
    }, indent=2, ensure_ascii=False))


# ── Main ───────────────────────────────────────────────────────────────────


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    commands = {
        "list": cmd_list,
        "add": cmd_add,
        "toggle": cmd_toggle,
        "delete": cmd_delete,
        "check": cmd_check,
    }

    if command not in commands:
        print(f"[ERROR] Unknown command: {command}", file=sys.stderr)
        print(f"  Available: {', '.join(commands.keys())}", file=sys.stderr)
        sys.exit(1)

    if command in ("list",):
        commands[command]()
    else:
        if len(sys.argv) < 3:
            print(f"[ERROR] Usage: auto_reply.py {command} <argument>", file=sys.stderr)
            sys.exit(1)
        commands[command](sys.argv[2])


if __name__ == "__main__":
    main()
