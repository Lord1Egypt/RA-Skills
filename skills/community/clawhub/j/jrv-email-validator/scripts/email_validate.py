#!/usr/bin/env python3
"""Email address validator with syntax, MX record, and disposable domain checks.

Validates email addresses using multiple checks:
- RFC 5322 syntax validation
- MX record verification (DNS)
- Disposable/temporary email detection
- Common typo suggestion
"""

import argparse
import json
import re
import socket
import struct
import sys


# Common disposable email domains
DISPOSABLE_DOMAINS = {
    "10minutemail.com", "guerrillamail.com", "guerrillamail.net", "guerrillamail.org",
    "mailinator.com", "tempmail.com", "throwaway.email", "yopmail.com", "yopmail.fr",
    "sharklasers.com", "guerrillamailblock.com", "grr.la", "guerrillamail.info",
    "guerrillamail.biz", "guerrillamail.de", "temp-mail.org", "temp-mail.io",
    "fakeinbox.com", "mailnesia.com", "maildrop.cc", "discard.email",
    "trashmail.com", "trashmail.me", "trashmail.net", "mailcatch.com",
    "tempail.com", "tempr.email", "dispostable.com", "mintemail.com",
    "mohmal.com", "burnermail.io", "harakirimail.com", "emailondeck.com",
    "getnada.com", "tempinbox.com", "mailtemp.org", "tempmailaddress.com",
    "tmpmail.org", "tmpmail.net", "getairmail.com", "mailsac.com",
    "mytemp.email", "tempmailo.com", "crazymailing.com", "safetymail.info",
    "inboxbear.com", "spamgourmet.com", "mailexpire.com", "throwam.com",
    "mailnator.com", "anonbox.net", "binkmail.com", "bobmail.info",
    "chammy.info", "devnullmail.com", "jetable.org", "mailimate.com",
    "nomail.xl.cx", "objectmail.com", "proxymail.eu", "rcpt.at",
    "rmqkr.net", "tittbit.in", "tradermail.info", "wegwerfmail.de",
    "wegwerfmail.net", "wuzup.net", "mailhazard.us", "mailmoat.com",
}

# Common typo corrections for popular domains
TYPO_CORRECTIONS = {
    "gmial.com": "gmail.com",
    "gmal.com": "gmail.com",
    "gmaill.com": "gmail.com",
    "gamil.com": "gmail.com",
    "gnail.com": "gmail.com",
    "gmail.co": "gmail.com",
    "gmaul.com": "gmail.com",
    "gmali.com": "gmail.com",
    "hotmal.com": "hotmail.com",
    "hotmial.com": "hotmail.com",
    "hotamil.com": "hotmail.com",
    "hotmail.co": "hotmail.com",
    "hitmail.com": "hotmail.com",
    "outlok.com": "outlook.com",
    "outloo.com": "outlook.com",
    "outllook.com": "outlook.com",
    "yahooo.com": "yahoo.com",
    "yaho.com": "yahoo.com",
    "yhoo.com": "yahoo.com",
    "yahoo.co": "yahoo.com",
    "iclould.com": "icloud.com",
    "icoud.com": "icloud.com",
    "icloud.co": "icloud.com",
    "protonmal.com": "protonmail.com",
    "protonmial.com": "protonmail.com",
}


def validate_syntax(email):
    """Validate email syntax per RFC 5322 (simplified)."""
    # Basic pattern
    pattern = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"

    if not re.match(pattern, email):
        return False, "Invalid email syntax"

    local, domain = email.rsplit("@", 1)

    if len(local) > 64:
        return False, "Local part exceeds 64 characters"
    if len(email) > 254:
        return False, "Email exceeds 254 characters"
    if ".." in local:
        return False, "Consecutive dots in local part"
    if not "." in domain:
        return False, "Domain must contain at least one dot"
    if len(domain) > 253:
        return False, "Domain exceeds 253 characters"

    return True, "Valid syntax"


def check_mx(domain, timeout=5):
    """Check if domain has MX records using DNS over UDP."""
    try:
        # Use socket-level DNS query for MX records
        # Fallback: try to resolve the domain with getaddrinfo
        socket.setdefaulttimeout(timeout)

        # Try MX lookup via low-level DNS
        try:
            import subprocess
            result = subprocess.run(
                ["dig", "+short", "MX", domain],
                capture_output=True, text=True, timeout=timeout
            )
            mx_records = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
            if mx_records:
                return True, mx_records[:5]
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        # Fallback: try nslookup
        try:
            result = subprocess.run(
                ["nslookup", "-type=MX", domain],
                capture_output=True, text=True, timeout=timeout
            )
            mx_lines = re.findall(r"mail exchanger\s*=\s*(.+)", result.stdout)
            if mx_lines:
                return True, [m.strip() for m in mx_lines[:5]]
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        # Last resort: check if the domain resolves at all (A record)
        try:
            socket.getaddrinfo(domain, None)
            return True, ["(A record exists, MX lookup unavailable)"]
        except socket.gaierror:
            return False, []

    except Exception as e:
        return None, [f"Error: {e}"]


def check_disposable(domain):
    """Check if domain is a known disposable email provider."""
    return domain.lower() in DISPOSABLE_DOMAINS


def suggest_typo(domain):
    """Suggest correction for common domain typos."""
    return TYPO_CORRECTIONS.get(domain.lower())


def validate_email(email, check_dns=True, check_disp=True):
    """Perform full validation on an email address."""
    result = {
        "email": email,
        "valid": False,
        "checks": {},
        "warnings": [],
        "suggestion": None,
    }

    # Syntax check
    syntax_ok, syntax_msg = validate_syntax(email)
    result["checks"]["syntax"] = {"pass": syntax_ok, "message": syntax_msg}

    if not syntax_ok:
        result["checks"]["mx"] = {"pass": None, "message": "Skipped (invalid syntax)"}
        result["checks"]["disposable"] = {"pass": None, "message": "Skipped"}
        return result

    local, domain = email.rsplit("@", 1)

    # Typo check
    correction = suggest_typo(domain)
    if correction:
        result["suggestion"] = f"{local}@{correction}"
        result["warnings"].append(f"Did you mean {local}@{correction}?")

    # Disposable check
    if check_disp:
        is_disposable = check_disposable(domain)
        result["checks"]["disposable"] = {
            "pass": not is_disposable,
            "message": "Disposable email detected" if is_disposable else "Not a known disposable domain",
        }
        if is_disposable:
            result["warnings"].append("Disposable/temporary email address")

    # MX check
    if check_dns:
        mx_ok, mx_records = check_mx(domain)
        result["checks"]["mx"] = {
            "pass": mx_ok,
            "message": f"MX records found: {len(mx_records)}" if mx_ok else "No MX records found",
        }
        if mx_ok and mx_records:
            result["checks"]["mx"]["records"] = mx_records
    else:
        result["checks"]["mx"] = {"pass": None, "message": "Skipped (DNS check disabled)"}

    # Overall verdict
    all_checks = [v["pass"] for v in result["checks"].values() if v["pass"] is not None]
    result["valid"] = all(all_checks) if all_checks else False

    return result


def format_result(result):
    """Format a validation result for terminal display."""
    lines = []
    email = result["email"]
    valid = result["valid"]

    icon = "\033[92m✓\033[0m" if valid else "\033[91m✗\033[0m"
    lines.append(f"\n  {icon} {email}")

    for check_name, check_data in result["checks"].items():
        passed = check_data["pass"]
        if passed is True:
            status = "\033[92m✓\033[0m"
        elif passed is False:
            status = "\033[91m✗\033[0m"
        else:
            status = "\033[90m-\033[0m"
        lines.append(f"    {status} {check_name}: {check_data['message']}")

    for warning in result.get("warnings", []):
        lines.append(f"    \033[93m⚠ {warning}\033[0m")

    if result.get("suggestion"):
        lines.append(f"    \033[96m💡 Suggestion: {result['suggestion']}\033[0m")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Validate email addresses (syntax, MX records, disposable detection, typo suggestions)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s user@example.com                    Validate single email
  %(prog)s user@gmail.com admin@company.org    Validate multiple emails
  %(prog)s user@example.com --json             JSON output
  %(prog)s user@example.com --no-dns           Skip MX record check
  %(prog)s --file emails.txt                   Validate from file (one per line)
  %(prog)s user@gmial.com                      Detects typo, suggests gmail.com
        """,
    )
    parser.add_argument("emails", nargs="*", help="Email address(es) to validate")
    parser.add_argument("--file", "-f", help="Read emails from file (one per line)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--no-dns", action="store_true", help="Skip DNS/MX record checks")
    parser.add_argument("--no-disposable", action="store_true", help="Skip disposable email check")

    args = parser.parse_args()

    emails = list(args.emails) if args.emails else []

    if args.file:
        try:
            with open(args.file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        emails.append(line)
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found")
            sys.exit(1)

    if not emails:
        parser.print_help()
        sys.exit(1)

    results = []
    for email in emails:
        result = validate_email(
            email.strip(),
            check_dns=not args.no_dns,
            check_disp=not args.no_disposable,
        )
        results.append(result)

    if args.json:
        print(json.dumps(results if len(results) > 1 else results[0], indent=2))
    else:
        print(f"\n{'='*50}")
        print(f"  Email Validation Results")
        print(f"{'='*50}")
        for r in results:
            print(format_result(r))
        print(f"\n{'='*50}")
        valid_count = sum(1 for r in results if r["valid"])
        print(f"  {valid_count}/{len(results)} valid")
        print(f"{'='*50}\n")

    # Exit with error if any invalid
    invalid = any(not r["valid"] for r in results)
    sys.exit(1 if invalid else 0)


if __name__ == "__main__":
    main()
