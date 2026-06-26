#!/usr/bin/env python3
"""
OpenClaw Security Guard - Security Hardening
Apply security best practices and fixes.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple

from utils import (
    OPENCLAW_DIR, CONFIG_FILE, load_config, Colors
)
from audit import run_audit
from scanner import scan_secrets


def get_fixable_issues() -> List[Dict]:
    """Get list of issues that can be auto-fixed."""
    audit_results = run_audit()
    fixable = []

    for finding in audit_results["findings"]:
        if finding.get("auto_fixable") and finding["severity"] not in ["info"]:
            fixable.append(finding)

    return fixable


def fix_token_strength() -> Tuple[bool, str]:
    """Fix weak token by generating a new one."""
    from token import rotate_token

    result = rotate_token(length=32)
    if result.get("success"):
        return True, f"Generated new token: {result['new_token'][:8]}..."
    return False, result.get("error", "Failed to rotate token")


def fix_auth_mode() -> Tuple[bool, str]:
    """Enable token authentication if not enabled."""
    if not CONFIG_FILE.exists():
        return False, "Config file not found"

    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)

    if config.get("gateway", {}).get("auth", {}).get("mode") == "token":
        return True, "Token authentication already enabled"

    if "gateway" not in config:
        config["gateway"] = {}
    if "auth" not in config["gateway"]:
        config["gateway"]["auth"] = {}

    config["gateway"]["auth"]["mode"] = "token"

    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

    return True, "Enabled token authentication"


def apply_hardening(fix: bool = False, dry_run: bool = False) -> Dict:
    """
    Apply security hardening.

    Args:
        fix: Actually apply fixes
        dry_run: Show what would be done without making changes

    Returns:
        Dict with hardening results
    """
    results = {
        "fixes_applied": [],
        "fixes_skipped": [],
        "manual_actions": [],
        "errors": []
    }

    audit_results = run_audit()

    for finding in audit_results["findings"]:
        if finding["severity"] == "info":
            continue

        finding_id = finding["id"]

        if finding_id == "CFG003":  # Token strength
            if fix and not dry_run:
                success, message = fix_token_strength()
                if success:
                    results["fixes_applied"].append({
                        "id": finding_id,
                        "name": finding["name"],
                        "message": message
                    })
                else:
                    results["errors"].append({
                        "id": finding_id,
                        "error": message
                    })
            else:
                results["fixes_skipped"].append({
                    "id": finding_id,
                    "name": finding["name"],
                    "requires": "--fix flag"
                })

        elif finding_id == "CFG002":  # Auth mode
            if fix and not dry_run:
                success, message = fix_auth_mode()
                if success:
                    results["fixes_applied"].append({
                        "id": finding_id,
                        "name": finding["name"],
                        "message": message
                    })
                else:
                    results["errors"].append({
                        "id": finding_id,
                        "error": message
                    })
            else:
                results["fixes_skipped"].append({
                    "id": finding_id,
                    "name": finding["name"],
                    "requires": "--fix flag"
                })

        elif finding_id == "CFG001":  # Gateway bind
            results["manual_actions"].append({
                "id": finding_id,
                "name": finding["name"],
                "action": "Manually edit config to change bind address",
                "config_path": str(CONFIG_FILE)
            })

        else:
            if finding["severity"] in ["critical", "high"]:
                results["manual_actions"].append({
                    "id": finding_id,
                    "name": finding["name"],
                    "action": finding["recommendation"]
                })

    return results


def print_hardening_results(results: Dict, i18n: Dict):
    """Print hardening results."""
    print()

    # Fixes applied
    if results["fixes_applied"]:
        print(f"{Colors.BOLD}{Colors.GREEN}✅ Fixes Applied{Colors.RESET}\n")
        for fix in results["fixes_applied"]:
            print(f"  {Colors.GREEN}•{Colors.RESET} {fix['name']}")
            print(f"    {fix['message']}")
            print()

    # Fixes skipped
    if results["fixes_skipped"]:
        print(f"{Colors.BOLD}{Colors.YELLOW}⏭️ Fixes Skipped{Colors.RESET}\n")
        for fix in results["fixes_skipped"]:
            print(f"  {Colors.YELLOW}•{Colors.RESET} {fix['name']}")
            print(f"    Requires: {fix['requires']}")
            print()

    # Manual actions
    if results["manual_actions"]:
        print(f"{Colors.BOLD}{Colors.CYAN}🔧 Manual Actions Required{Colors.RESET}\n")
        for action in results["manual_actions"]:
            print(f"  {Colors.CYAN}•{Colors.RESET} {action['name']}")
            print(f"    Action: {action['action']}")
            if action.get("config_path"):
                print(f"    Config: {action['config_path']}")
            print()

    # Errors
    if results["errors"]:
        print(f"{Colors.BOLD}{Colors.RED}❌ Errors{Colors.RESET}\n")
        for error in results["errors"]:
            print(f"  {Colors.RED}•{Colors.RESET} {error['id']}: {error['error']}")

    # Summary
    print(f"\n{Colors.BOLD}📊 Summary{Colors.RESET}")
    print(f"  Fixes applied: {len(results['fixes_applied'])}")
    print(f"  Fixes skipped: {len(results['fixes_skipped'])}")
    print(f"  Manual actions: {len(results['manual_actions'])}")
    print(f"  Errors: {len(results['errors'])}")

    if results["fixes_applied"]:
        print(f"\n{Colors.CYAN}💡 Restart gateway for changes to take effect:{Colors.RESET}")
        print(f"   openclaw gateway restart")


if __name__ == "__main__":
    results = apply_hardening(fix=True)
    print(json.dumps(results, indent=2))