#!/usr/bin/env python3
"""memory-guardian: Security constraint layer — extracts and enforces safety rules.

Reads AGENTS.md and SOUL.md to extract hard-coded security constraints.
These rules are NEVER matched against cases (axiom 2: separation of concerns).
Security rules cannot be modified by case growth or dedup operations.

v0.4.1 additions:
  - Action bucket classification (chaonengnono): confirm/notify/auto
  - Risk score calculation based on reversibility/impact/visibility
  - Three-tier execution: block / async-notify / auto-execute

Usage:
  python3 security_layer.py [--workspace <path>] [--extract] [--check <content>] [--save]
  python3 security_layer.py risk [--action <action>] [--object <obj>] [--workspace <path>]

Modes:
  extract  — Parse AGENTS.md/SOUL.md for security rules, print them
  check    — Test content against security rules (used by ingest pipeline)
  save     — Extract and persist rules to meta.json security_rules[]
  risk     — v0.4.1: Calculate risk score and action bucket for an action
  list     — List persisted security rules
"""
import json, os, re, sys, argparse
from datetime import datetime
from mg_utils import _now_iso, load_meta, save_meta, read_text_file, safe_print

print = safe_print


# ─── Rule Patterns ────────────────────────────────────────────
# Patterns to extract from AGENTS.md/SOUL.md
SECURITY_PATTERNS = [
    {
        "id": "no-exfiltrate",
        "pattern": r"(?i)(don'?t\s+exfiltrat|never\s+(share|expose|leak)\s+private|private.*stay\s+private|绝不.*输出.*key|不.*泄露.*敏感)",
        "description": "禁止泄露私有数据",
        "severity": "critical",
    },
    {
        "id": "no-destructive",
        "pattern": r"(?i)(don'?t\s+run\s+destructive|trash\s*>\s*rm|先问.*再删|confirm.*before.*delet)",
        "description": "破坏性操作需确认",
        "severity": "high",
    },
    {
        "id": "no-public-secrets",
        "pattern": r"(?i)(never\s+output\s+api\s+key|never.*token.*对话|credential.*rules|API\s*key.*绝不|output.*token|share.*api.*key|(api|token|secret|password|credential)\s*(key|secret)?\s*[:=]\s*['\"][^'\"]{8,}['\"])",
        "description": "绝不输出 API key/token",
        "severity": "critical",
    },
    {
        "id": "no-impersonate",
        "pattern": r"(?i)(not\s+the\s+user'?s\s+voice|don'?t\s+speak\s+for|你不是.*代理|not.*proxy)",
        "description": "不代替用户发言",
        "severity": "high",
    },
    {
        "id": "confirm-external",
        "pattern": r"(?i)(ask\s+before.*external|sending\s+emails.*tweets.*public|anything.*leaves.*machine)",
        "description": "外部操作需先确认",
        "severity": "high",
    },
    {
        "id": "group-privacy",
        "pattern": r"(?i)(don'?t\s+(share|touch)\s+.*in\s+groups|don'?t\s+carry\s+context\s+across|群聊.*公开.*任何|group.*visible)",
        "description": "群聊中不分享私密内容",
        "severity": "high",
    },
    {
        "id": "reject-probing",
        "pattern": r"(?i)(reject.*probing|ignore.*previous.*instructions|role.play.*hypothetical|prompt\s+injection|social\s+engineering)",
        "description": "拒绝探测/注入/社会工程",
        "severity": "critical",
    },
    {
        "id": "no-money-legal",
        "pattern": r"(?i)(anything.*involving\s+money.*contracts.*legal|money.*legal.*commitments|blast\s+radius.*exceeds)",
        "description": "拒绝涉及金钱/合同/法律",
        "severity": "critical",
    },
    {
        "id": "verify-owner",
        "pattern": r"(?i)(verify\s+sender|sender\s+is\s+non-owner|match\s*=\s*owner|No\s+match\s*=\s*non-owner)",
        "description": "验证发送者身份",
        "severity": "critical",
    },
    {
        "id": "no-config-in-group",
        "pattern": r"(?i)(shell.*gateway.*blocked.*group|soul.*config.*private.*data|switch.*to\s+DM)",
        "description": "群聊中禁止 shell/gateway/配置操作",
        "severity": "high",
    },
]


def extract_from_file(filepath):
    """Extract security rules from a markdown file."""
    if not os.path.exists(filepath):
        return []
    text = read_text_file(filepath)
    return extract_from_text(text, os.path.basename(filepath))


def extract_from_text(text, source="unknown"):
    """Extract security rules from text content."""
    rules = []
    for pattern_def in SECURITY_PATTERNS:
        matches = re.findall(pattern_def["pattern"], text)
        if matches:
            rule = {
                "id": pattern_def["id"],
                "description": pattern_def["description"],
                "severity": pattern_def["severity"],
                "source": source,
                "match_count": len(matches),
                "pattern": pattern_def["pattern"],
                "version": 1,
                "created_at": _now_iso(),
            }
            rules.append(rule)
    return rules


def check_content(content, rules):
    """Check if content violates any security rules.

    Returns list of violations (empty = safe).
    This is the pre-ingest safety check — violations result in BLOCK.
    """
    violations = []
    for rule in rules:
        pattern = rule.get("pattern", "")
        if not pattern:
            continue
        if re.search(pattern, content, re.IGNORECASE):
            violations.append({
                "rule_id": rule["id"],
                "severity": rule.get("severity", "high"),
                "description": rule.get("description", "unknown"),
                "action": "BLOCK" if rule.get("severity") == "critical" else "WARN",
            })
    return violations


def cmd_extract(workspace):
    """Extract security rules from AGENTS.md and SOUL.md."""
    agents_path = os.path.join(workspace, "AGENTS.md")
    soul_path = os.path.join(workspace, "SOUL.md")

    all_rules = []
    seen_ids = set()

    for filepath in [agents_path, soul_path]:
        rules = extract_from_file(filepath)
        for rule in rules:
            if rule["id"] not in seen_ids:
                all_rules.append(rule)
                seen_ids.add(rule["id"])

    print(f"Extracted {len(all_rules)} security rules:")
    for rule in sorted(all_rules, key=lambda r: r["severity"]):
        icon = "🔴" if rule["severity"] == "critical" else "🟡"
        print(f"  {icon} [{rule['id']}] {rule['description']} (from {rule['source']}, {rule['match_count']} matches)")

    return all_rules


def cmd_check(content, workspace):
    """Check content against persisted security rules."""
    meta_path = os.path.join(workspace, "memory", "meta.json")
    meta = load_meta(meta_path)
    rules = meta.get("security_rules", [])

    if not rules:
        # Fall back to extraction
        rules = cmd_extract(workspace)

    violations = check_content(content, rules)

    if not violations:
        print("[SAFE] Content passes security check")
        return []

    print(f"[SECURITY] {len(violations)} violation(s) detected:")
    for v in violations:
        icon = "🚫" if v["action"] == "BLOCK" else "⚠️"
        print(f"  {icon} [{v['rule_id']}] {v['description']} → {v['action']}")
    return violations


def cmd_save(workspace):
    """Extract and persist security rules to meta.json."""
    meta_path = os.path.join(workspace, "memory", "meta.json")
    meta = load_meta(meta_path)

    rules = cmd_extract(workspace)

    # Update version for any changed/new rules
    existing_ids = {r["id"] for r in meta.get("security_rules", [])}
    for i, rule in enumerate(rules):
        if rule["id"] in existing_ids:
            # Increment version if pattern changed
            old = next(r for r in meta["security_rules"] if r["id"] == rule["id"])
            if old.get("pattern") != rule.get("pattern"):
                rule["version"] = old.get("version", 1) + 1
                rule["created_at"] = _now_iso()
            else:
                # Keep existing unchanged (use the persisted version)
                rules[i] = dict(old)

    meta["security_rules"] = rules
    save_meta(meta_path, meta)

    print(f"\n✅ Saved {len(rules)} security rules to meta.json")
    return rules


def cmd_list(workspace):
    """List persisted security rules."""
    meta_path = os.path.join(workspace, "memory", "meta.json")
    meta = load_meta(meta_path)
    rules = meta.get("security_rules", [])

    if not rules:
        print("No security rules persisted. Run with --extract or --save first.")
        return []

    print(f"Security rules ({len(rules)}):")
    for rule in sorted(rules, key=lambda r: r["severity"]):
        icon = "🔴" if rule["severity"] == "critical" else "🟡"
        print(f"  {icon} v{rule.get('version',1)} [{rule['id']}] {rule['description']}")
        print(f"     Source: {rule.get('source','?')}, Severity: {rule['severity']}")
    return rules


# ─── v0.4.1 Action Bucket Classification ────────────────────

# Reversibility weights (v0.4 existing, 0-3 scale)
REVERSIBILITY_WEIGHT = 0.5
IMPACT_WEIGHT = 0.3
VISIBILITY_WEIGHT = 0.2

# Action-to-bucket mapping (chaonengnono)
CONFIRM_ACTIONS = {
    "delete_memory", "archive_memory", "modify_importance", "merge_case",
    "delete_case", "force_normal", "manual_override", "rollback_case",
}
NOTIFY_ACTIONS = {
    "modify_tag", "update_provenance", "degraded_write", "modify_confidence",
    "update_ttl", "pool_promote", "pool_archive",
}
AUTO_ACTIONS = {
    "update_access_count", "record_wakeup", "compact", "update_decay_score",
    "record_trigger", "update_cooldown", "check_layer", "record_result",
}

# Reversibility mapping
REVERSIBILITY_MAP = {
    "delete_memory": 3, "archive_memory": 2, "modify_importance": 1,
    "merge_case": 2, "delete_case": 3, "force_normal": 1,
    "manual_override": 1, "rollback_case": 1, "modify_tag": 1,
    "update_provenance": 1, "degraded_write": 1, "modify_confidence": 1,
    "update_ttl": 1, "pool_promote": 2, "pool_archive": 2,
    "update_access_count": 0, "record_wakeup": 0, "compact": 1,
    "update_decay_score": 0, "record_trigger": 0, "update_cooldown": 0,
}

# Impact radius (0=narrow self, 1=system, 2=external)
IMPACT_MAP = {
    "delete_memory": 2, "archive_memory": 1, "modify_importance": 1,
    "merge_case": 1, "delete_case": 2, "force_normal": 1,
    "manual_override": 1, "rollback_case": 1, "modify_tag": 1,
    "update_provenance": 1, "degraded_write": 0, "modify_confidence": 1,
    "update_ttl": 0, "pool_promote": 1, "pool_archive": 1,
    "update_access_count": 0, "record_wakeup": 0, "compact": 0,
    "update_decay_score": 0, "record_trigger": 0, "update_cooldown": 0,
}

# Visibility delay (0=instant, 1=delayed hours, 2=delayed days)
VISIBILITY_MAP = {
    "delete_memory": 0, "archive_memory": 1, "modify_importance": 1,
    "merge_case": 1, "delete_case": 0, "force_normal": 0,
    "manual_override": 0, "rollback_case": 1, "modify_tag": 1,
    "update_provenance": 1, "degraded_write": 2, "modify_confidence": 2,
    "update_ttl": 2, "pool_promote": 1, "pool_archive": 1,
    "update_access_count": 2, "record_wakeup": 2, "compact": 2,
    "update_decay_score": 2, "record_trigger": 2, "update_cooldown": 2,
}


def classify_action(action):
    """Classify an action into its bucket and compute risk score.

    Returns: {
        "action": str,
        "bucket": "confirm" | "notify" | "auto",
        "risk_score": float (0-1),
        "reversibility": int (0-3),
        "impact_radius": int (0-2),
        "visibility_delay": int (0-2),
        "details": str,
    }
    """
    if action in CONFIRM_ACTIONS:
        bucket = "confirm"
    elif action in NOTIFY_ACTIONS:
        bucket = "notify"
    elif action in AUTO_ACTIONS:
        bucket = "auto"
    else:
        # Unknown action: default to notify (safe middle ground)
        bucket = "notify"

    rev = REVERSIBILITY_MAP.get(action, 1)
    impact = IMPACT_MAP.get(action, 1)
    vis = VISIBILITY_MAP.get(action, 1)

    # Normalize to 0-1
    rev_score = rev / 3.0
    impact_score = impact / 2.0
    vis_score = vis / 2.0

    risk_score = round(
        REVERSIBILITY_WEIGHT * rev_score +
        IMPACT_WEIGHT * impact_score +
        VISIBILITY_WEIGHT * vis_score,
        3
    )

    details = f"rev={rev} impact={impact} vis={vis}"
    return {
        "action": action,
        "bucket": bucket,
        "risk_score": risk_score,
        "reversibility": rev,
        "impact_radius": impact,
        "visibility_delay": vis,
        "details": details,
    }


def cmd_risk(action, workspace):
    """v0.4.1: Show risk classification for an action."""
    if not action:
        print("All known actions and their risk classification:")
        all_actions = sorted(CONFIRM_ACTIONS | NOTIFY_ACTIONS | AUTO_ACTIONS)
        for a in all_actions:
            cls = classify_action(a)
            icon = {"confirm": "🔴", "notify": "🟡", "auto": "🟢"}[cls["bucket"]]
            print(f"  {icon} {cls['bucket']:8s} risk={cls['risk_score']:.2f} | {a}")
        return

    cls = classify_action(action)
    icon = {"confirm": "🔴", "notify": "🟡", "auto": "🟢"}[cls["bucket"]]

    print(f"{icon} Action Risk Classification")
    print(f"  Action: {cls['action']}")
    print(f"  Bucket: {cls['bucket'].upper()}")
    print(f"  Risk score: {cls['risk_score']:.3f}")
    print(f"  Reversibility: {cls['reversibility']}/3 (0=free, 3=irreversible)")
    print(f"  Impact radius: {cls['impact_radius']}/2 (0=self, 2=external)")
    print(f"  Visibility delay: {cls['visibility_delay']}/2 (0=instant, 2=days)")
    print(f"  Details: {cls['details']}")

    if cls["bucket"] == "confirm":
        print(f"\n  ⚠️ Requires human confirmation before execution")
    elif cls["bucket"] == "notify":
        print(f"\n  📢 Async notification, auto-execute after timeout (30min)")
    else:
        print(f"\n  ✅ Auto-execute, log only")

    return cls


# ─── Efficiency Tag Classification (v0.4.1, chaonengnono) ──

def classify_case_tag(case):
    """Classify a case into risk tag vs efficiency tag.

    Risk tags: reversibility >= 1 → action bucket = confirm or notify
    Efficiency tags: reversibility = 0 → action bucket = auto

    Efficiency tags don't count toward "qualified case" minimum standard
    but DO count toward PID adaptive N value.

    Args:
        case: dict, a case entry from meta.json

    Returns:
        dict: {
            "tag_type": "risk" | "efficiency",
            "bucket": str,
            "risk_score": float,
            "counts_as_qualified": bool,
            "counts_for_pid": bool,
        }
    """
    # Get the primary action to determine reversibility
    action = case.get("action_conclusion", "unknown")
    cls = classify_action(action)
    rev = cls["reversibility"]

    if rev == 0:
        return {
            "tag_type": "efficiency",
            "bucket": "auto",
            "risk_score": cls["risk_score"],
            "counts_as_qualified": False,
            "counts_for_pid": True,
        }
    else:
        return {
            "tag_type": "risk",
            "bucket": cls["bucket"],
            "risk_score": cls["risk_score"],
            "counts_as_qualified": True,
            "counts_for_pid": True,
        }


def get_case_minimum_standard(case):
    """Check if a case meets the minimum standard for a qualified case.

    Minimum standard (chaonengnono + azha0):
    - trigger_count >= 3
    - At least 1 positive feedback (or confidence >= 0.6)
    - At least 1 risk tag (reversibility >= 1)

    Args:
        case: dict, a case entry

    Returns:
        dict: {"qualified": bool, "checks": dict, "missing": list}
    """
    checks = {
        "trigger_count": case.get("trigger_count", 0) >= 3,
        "feedback_or_confidence": (
            case.get("positive_feedback_count", 0) >= 1 or
            case.get("confidence", 0) >= 0.6
        ),
        "has_risk_tag": classify_case_tag(case)["tag_type"] == "risk",
    }
    qualified = all(checks.values())
    missing = [k for k, v in checks.items() if not v]
    return {"qualified": qualified, "checks": checks, "missing": missing}


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="memory-guardian security constraint layer (v0.4.1)")
    p.add_argument("command", choices=["extract", "check", "save", "list", "risk", "tag-classify"],
                   help="Command")
    p.add_argument("--content", default=None, help="Content to check (for 'check' command)")
    p.add_argument("--action", default=None, help="Action to classify (for 'risk' command)")
    p.add_argument("--workspace", default=None, help="Workspace root path")
    args = p.parse_args()

    workspace = args.workspace or os.environ.get(
        "OPENCLAW_WORKSPACE", os.path.expanduser("~/workspace/agent/workspace")
    )

    if args.command == "extract":
        cmd_extract(workspace)
    elif args.command == "check":
        if not args.content:
            print("Error: --content required for check command")
            sys.exit(1)
        cmd_check(args.content, workspace)
    elif args.command == "save":
        cmd_save(workspace)
    elif args.command == "list":
        cmd_list(workspace)
    elif args.command == "risk":
        cmd_risk(args.action, workspace)
    elif args.command == "tag-classify":
        meta_path = os.path.join(workspace, "memory", "meta.json")
        meta = load_meta(meta_path) if os.path.exists(meta_path) else {"memories": []}
        cases = [m for m in meta.get("memories", [])
                 if m.get("status") in ("active", "observing")]
        if not cases:
            print("No active cases found.")
        else:
            risk_count = 0
            eff_count = 0
            qualified_count = 0
            for c in cases:
                tag = classify_case_tag(c)
                std = get_case_minimum_standard(c)
                icon = "🔴" if tag["tag_type"] == "risk" else "🟢"
                q_icon = "✅" if std["qualified"] else "⬜"
                print(f"  {icon} {tag['tag_type']:10s} {q_icon} | {c.get('id', '?')} triggers={c.get('trigger_count', 0)} conf={c.get('confidence', 0):.2f}")
                if tag["tag_type"] == "risk":
                    risk_count += 1
                else:
                    eff_count += 1
                if std["qualified"]:
                    qualified_count += 1
            print(f"\n  📊 Risk tags: {risk_count} | Efficiency tags: {eff_count}")
            print(f"  ✅ Qualified cases: {qualified_count}/{len(cases)}")
