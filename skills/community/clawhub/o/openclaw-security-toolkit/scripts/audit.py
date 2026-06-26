#!/usr/bin/env python3
"""
OpenClaw Security Guard - Security Audit
Performs comprehensive security configuration checks.
"""

import json
import socket
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from utils import (
    OPENCLAW_DIR, CONFIG_FILE, load_config, load_skill_config,
    Colors, print_severity, calculate_score, get_score_rating,
    get_gateway_info, get_channels_info, get_models_info
)


def check_gateway_bind(config: Dict) -> Dict:
    """Check gateway bind address security."""
    gateway = config.get("gateway", {})
    bind = gateway.get("bind", "loopback")

    if bind == "0.0.0.0":
        return {
            "id": "CFG001",
            "category": "config",
            "name": "Gateway Bind Address",
            "severity": "critical",
            "title": "Gateway exposed to all network interfaces",
            "description": f"Gateway is bound to 0.0.0.0, exposing it to all network interfaces",
            "recommendation": "Change bind to 'loopback' for local access only, or use Tailscale for secure remote access",
            "auto_fixable": False,
            "current_value": bind
        }
    elif bind == "loopback":
        return {
            "id": "CFG001",
            "category": "config",
            "name": "Gateway Bind Address",
            "severity": "info",
            "title": "Gateway bind is secure",
            "description": f"Gateway is bound to loopback (127.0.0.1), only accessible locally",
            "recommendation": "Consider using Tailscale for secure remote access",
            "auto_fixable": False,
            "current_value": bind
        }
    else:
        return {
            "id": "CFG001",
            "category": "config",
            "name": "Gateway Bind Address",
            "severity": "medium",
            "title": "Gateway bind to specific interface",
            "description": f"Gateway is bound to {bind}",
            "recommendation": "Verify this is intended and secure",
            "auto_fixable": False,
            "current_value": bind
        }


def check_auth_mode(config: Dict) -> Dict:
    """Check authentication mode."""
    gateway = config.get("gateway", {})
    auth = gateway.get("auth", {})
    mode = auth.get("mode", "none")

    if mode == "none":
        return {
            "id": "CFG002",
            "category": "config",
            "name": "Authentication Mode",
            "severity": "high",
            "title": "No authentication configured",
            "description": "Gateway has no authentication, anyone can access",
            "recommendation": "Enable token-based authentication",
            "auto_fixable": True,
            "current_value": mode
        }
    elif mode == "token":
        return {
            "id": "CFG002",
            "category": "config",
            "name": "Authentication Mode",
            "severity": "info",
            "title": "Token authentication enabled",
            "description": "Gateway uses token-based authentication",
            "recommendation": "Ensure token is kept secret and rotated periodically",
            "auto_fixable": False,
            "current_value": mode
        }
    else:
        return {
            "id": "CFG002",
            "category": "config",
            "name": "Authentication Mode",
            "severity": "low",
            "title": f"Authentication mode: {mode}",
            "description": f"Gateway uses {mode} authentication",
            "recommendation": "Verify authentication is properly configured",
            "auto_fixable": False,
            "current_value": mode
        }


def check_token_strength(config: Dict) -> Dict:
    """Check token strength."""
    gateway = config.get("gateway", {})
    token = gateway.get("auth", {}).get("token", "")

    if not token:
        return {
            "id": "CFG003",
            "category": "config",
            "name": "Token Strength",
            "severity": "high",
            "title": "No token configured",
            "description": "Gateway has no authentication token",
            "recommendation": "Generate a strong token (32+ characters)",
            "auto_fixable": True,
            "current_value": "None"
        }

    token_len = len(token)
    if token_len < 16:
        return {
            "id": "CFG003",
            "category": "config",
            "name": "Token Strength",
            "severity": "high",
            "title": "Weak token",
            "description": f"Token is only {token_len} characters (recommended: 32+)",
            "recommendation": "Generate a stronger token",
            "auto_fixable": True,
            "current_value": f"{token_len} characters"
        }
    elif token_len < 32:
        return {
            "id": "CFG003",
            "category": "config",
            "name": "Token Strength",
            "severity": "medium",
            "title": "Moderate token strength",
            "description": f"Token is {token_len} characters",
            "recommendation": "Consider using a longer token (32+ characters)",
            "auto_fixable": True,
            "current_value": f"{token_len} characters"
        }
    else:
        return {
            "id": "CFG003",
            "category": "config",
            "name": "Token Strength",
            "severity": "info",
            "title": "Strong token",
            "description": f"Token is {token_len} characters",
            "recommendation": "Remember to rotate periodically",
            "auto_fixable": False,
            "current_value": f"{token_len} characters"
        }


def check_tailscale(config: Dict) -> Dict:
    """Check Tailscale configuration."""
    gateway = config.get("gateway", {})
    tailscale = gateway.get("tailscale", {})
    mode = tailscale.get("mode", "off")

    if mode == "on":
        return {
            "id": "CFG004",
            "category": "config",
            "name": "Tailscale VPN",
            "severity": "info",
            "title": "Tailscale VPN enabled",
            "description": "Secure remote access via Tailscale is configured",
            "recommendation": "Ensure Tailscale is properly configured",
            "auto_fixable": False,
            "current_value": mode
        }
    else:
        return {
            "id": "CFG004",
            "category": "config",
            "name": "Tailscale VPN",
            "severity": "low",
            "title": "Tailscale VPN not configured",
            "description": "Consider using Tailscale for secure remote access",
            "recommendation": "Enable Tailscale if you need remote access",
            "auto_fixable": False,
            "current_value": mode
        }


def check_plugins(config: Dict) -> Dict:
    """Check plugin configuration."""
    plugins = config.get("plugins", {})
    allow = plugins.get("allow", [])
    entries = plugins.get("entries", {})

    # Check for unrestricted plugins
    if not allow:
        return {
            "id": "CFG005",
            "category": "config",
            "name": "Plugin Allowlist",
            "severity": "medium",
            "title": "No plugin allowlist configured",
            "description": "All plugins can be loaded without restriction",
            "recommendation": "Configure plugin allowlist to limit which plugins can be loaded",
            "auto_fixable": False,
            "current_value": "Unrestricted"
        }
    else:
        return {
            "id": "CFG005",
            "category": "config",
            "name": "Plugin Allowlist",
            "severity": "info",
            "title": "Plugin allowlist configured",
            "description": f"Allowed plugins: {', '.join(allow)}",
            "recommendation": "Review allowed plugins periodically",
            "auto_fixable": False,
            "current_value": allow
        }


def check_paired_devices() -> Dict:
    """Check paired devices."""
    paired_file = OPENCLAW_DIR / "devices" / "paired.json"

    if not paired_file.exists():
        return {
            "id": "ACC001",
            "category": "access",
            "name": "Paired Devices",
            "severity": "info",
            "title": "No paired devices",
            "description": "No devices are paired with this gateway",
            "recommendation": "Pair devices as needed",
            "auto_fixable": False,
            "current_value": 0
        }

    try:
        with open(paired_file, 'r') as f:
            devices = json.load(f)
        count = len(devices)

        if count > 5:
            return {
                "id": "ACC001",
                "category": "access",
                "name": "Paired Devices",
                "severity": "medium",
                "title": f"Many paired devices ({count})",
                "description": f"{count} devices are paired with this gateway",
                "recommendation": "Review paired devices and remove unused ones",
                "auto_fixable": False,
                "current_value": count
            }
        else:
            return {
                "id": "ACC001",
                "category": "access",
                "name": "Paired Devices",
                "severity": "info",
                "title": f"{count} paired device(s)",
                "description": f"{count} devices are paired",
                "recommendation": "Regularly review paired devices",
                "auto_fixable": False,
                "current_value": count
            }
    except:
        return {
            "id": "ACC001",
            "category": "access",
            "name": "Paired Devices",
            "severity": "low",
            "title": "Could not read paired devices",
            "description": "Unable to read paired devices configuration",
            "recommendation": "Check devices configuration",
            "auto_fixable": False,
            "current_value": "Unknown"
        }


def check_channel_permissions() -> List[Dict]:
    """Check channel permission configurations."""
    findings = []
    credentials_dir = OPENCLAW_DIR / "credentials"

    if not credentials_dir.exists():
        return findings

    for cred_file in credentials_dir.glob("*.json"):
        if "allowFrom" in cred_file.name:
            try:
                with open(cred_file, 'r') as f:
                    data = json.load(f)
                allow_from = data.get("allowFrom", [])
                channel = cred_file.name.replace("-allowFrom.json", "").replace("feishu-", "feishu/")

                if not allow_from:
                    findings.append({
                        "id": "ACC002",
                        "category": "access",
                        "name": "Channel Permissions",
                        "severity": "medium",
                        "title": f"No allowlist for {channel}",
                        "description": f"Channel {channel} has no user allowlist configured",
                        "recommendation": "Configure user allowlist to restrict access",
                        "auto_fixable": False,
                        "current_value": "Unrestricted",
                        "location": str(cred_file)
                    })
                else:
                    findings.append({
                        "id": "ACC002",
                        "category": "access",
                        "name": "Channel Permissions",
                        "severity": "info",
                        "title": f"{channel}: {len(allow_from)} allowed user(s)",
                        "description": f"Channel {channel} has {len(allow_from)} allowed users",
                        "recommendation": "Review allowed users periodically",
                        "auto_fixable": False,
                        "current_value": len(allow_from),
                        "location": str(cred_file)
                    })
            except:
                pass

    return findings


def check_exec_approvals() -> Dict:
    """Check execution approval configuration."""
    approvals_file = OPENCLAW_DIR / "exec-approvals.json"

    if not approvals_file.exists():
        return {
            "id": "ACC003",
            "category": "access",
            "name": "Execution Approvals",
            "severity": "low",
            "title": "Execution approvals not configured",
            "description": "No execution approval system configured",
            "recommendation": "Consider enabling execution approvals for sensitive commands",
            "auto_fixable": False,
            "current_value": "Not configured"
        }

    return {
        "id": "ACC003",
        "category": "access",
        "name": "Execution Approvals",
        "severity": "info",
        "title": "Execution approvals configured",
        "description": "Execution approval system is in place",
        "recommendation": "Review approval settings periodically",
        "auto_fixable": False,
        "current_value": "Configured"
    }


def run_audit(
    deep: bool = False,
    auto_fix: bool = False,
    quiet: bool = False
) -> Dict:
    """
    Run comprehensive security audit.

    Args:
        deep: Include deeper checks
        auto_fix: Attempt to fix issues automatically
        quiet: Suppress output

    Returns:
        Dict with audit results
    """
    config = load_config()
    skill_config = load_skill_config()

    findings = []

    # Config checks
    findings.append(check_gateway_bind(config))
    findings.append(check_auth_mode(config))
    findings.append(check_token_strength(config))
    findings.append(check_tailscale(config))
    findings.append(check_plugins(config))

    # Access checks
    findings.append(check_paired_devices())
    findings.extend(check_channel_permissions())
    findings.append(check_exec_approvals())

    # Calculate score
    weights = skill_config.get("scoring", {}).get("weights", {
        "critical": 25,
        "high": 15,
        "medium": 8,
        "low": 3,
        "info": 0
    })

    # Only count non-info findings for score
    score_findings = [f for f in findings if f["severity"] != "info"]
    score = calculate_score(score_findings, weights)
    rating, emoji = get_score_rating(score)

    # Summary
    summary = {
        "total": len(findings),
        "critical": sum(1 for f in findings if f["severity"] == "critical"),
        "high": sum(1 for f in findings if f["severity"] == "high"),
        "medium": sum(1 for f in findings if f["severity"] == "medium"),
        "low": sum(1 for f in findings if f["severity"] == "low"),
        "info": sum(1 for f in findings if f["severity"] == "info"),
    }

    return {
        "score": score,
        "rating": rating,
        "emoji": emoji,
        "findings": findings,
        "summary": summary,
        "timestamp": datetime.now().isoformat()
    }


def print_audit_results(results: Dict, i18n: Dict, verbose: bool = False):
    """Print audit results in table format."""
    score = results["score"]
    rating = results["rating"]
    emoji = results["emoji"]
    findings = results["findings"]
    summary = results["summary"]

    # Header
    print()
    print(f"{Colors.BOLD}{Colors.CYAN}🔐 OpenClaw Security Guard v1.0.0{Colors.RESET}")
    print(f"{Colors.WHITE}{'━' * 50}{Colors.RESET}")
    print()

    # Score
    if score >= 75:
        score_color = Colors.GREEN
    elif score >= 50:
        score_color = Colors.YELLOW
    else:
        score_color = Colors.RED

    print(f"{Colors.BOLD}📊 Security Score: {score_color}{score}/100{Colors.RESET} {emoji}")
    print()

    # Findings by severity
    for severity in ["critical", "high", "medium", "low", "info"]:
        sev_findings = [f for f in findings if f["severity"] == severity]
        if not sev_findings:
            continue

        sev_label = print_severity(severity, i18n)
        print(f"\n{sev_label}\n")

        for f in sev_findings:
            print(f"  {Colors.YELLOW}•{Colors.RESET} {f['title']}")
            if verbose:
                print(f"    {Colors.CYAN}ID:{Colors.RESET} {f['id']}")
                print(f"    {Colors.CYAN}Description:{Colors.RESET} {f['description']}")
            print(f"    {Colors.CYAN}Recommendation:{Colors.RESET} {f['recommendation']}")
            if f.get("auto_fixable") and f["severity"] not in ["info"]:
                print(f"    {Colors.GREEN}✓ Auto-fix available{Colors.RESET}")
            print()

    # Summary
    print(f"\n{Colors.BOLD}📈 Summary{Colors.RESET}")
    print(f"  Critical: {summary['critical']}")
    print(f"  High: {summary['high']}")
    print(f"  Medium: {summary['medium']}")
    print(f"  Low: {summary['low']}")
    print(f"  Info: {summary['info']}")

    # Fix hint
    fixable = [f for f in findings if f.get("auto_fixable") and f["severity"] not in ["info"]]
    if fixable:
        print(f"\n{Colors.CYAN}💡 Run with --fix to auto-fix {len(fixable)} issue(s){Colors.RESET}")


if __name__ == "__main__":
    results = run_audit(deep=True)
    print(json.dumps(results, indent=2, ensure_ascii=False))