#!/usr/bin/env python3
"""Env file doctor — validate .env files, detect leaked secrets, find duplicates and issues.

Usage:
    env_doctor.py <envfile> [--example EXAMPLE] [--json] [--strict]
    env_doctor.py --help

Examples:
    env_doctor.py .env
    env_doctor.py .env --example .env.example
    env_doctor.py .env --strict --json
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# Patterns that likely indicate real secrets
SECRET_PATTERNS = {
    "AWS Access Key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "AWS Secret Key": re.compile(r"(?i)(aws_secret|secret_key|aws_key).*=\s*[A-Za-z0-9/+=]{40}"),
    "GitHub Token": re.compile(r"(ghp_|gho_|ghs_|ghu_|github_pat_)[A-Za-z0-9_]{20,}"),
    "Slack Token": re.compile(r"xox[bpars]-[A-Za-z0-9\-]{10,}"),
    "Stripe Key": re.compile(r"(sk_live|pk_live|sk_test|pk_test)_[A-Za-z0-9]{20,}"),
    "Google API Key": re.compile(r"AIza[0-9A-Za-z\-_]{35}"),
    "Private Key Block": re.compile(r"-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----"),
    "JWT Token": re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
    "Generic High-Entropy": re.compile(r"(?i)(password|secret|token|api_key|apikey|auth)\s*=\s*['\"]?[A-Za-z0-9+/=]{32,}"),
    "Twilio Token": re.compile(r"(?i)twilio.*=\s*[a-f0-9]{32}"),
    "SendGrid Key": re.compile(r"SG\.[A-Za-z0-9_-]{22}\.[A-Za-z0-9_-]{43}"),
    "Heroku API Key": re.compile(r"(?i)heroku.*=\s*[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"),
}

# Values that are clearly placeholders, not secrets
PLACEHOLDER_VALUES = {
    "your-api-key-here", "changeme", "replace-me", "xxx", "todo",
    "your_secret_here", "placeholder", "your-token-here", "insert-here",
    "example", "test", "dummy", "fake", "sample", "none", "null", "undefined",
}


def parse_env_file(filepath: str) -> list[dict]:
    """Parse a .env file into a list of entries."""
    entries = []
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    with open(filepath, "r", errors="replace") as f:
        for lineno, raw_line in enumerate(f, 1):
            line = raw_line.strip()

            # Skip empty lines and comments
            if not line or line.startswith("#"):
                entries.append({"lineno": lineno, "type": "comment" if line.startswith("#") else "blank", "raw": raw_line.rstrip()})
                continue

            # Try to parse KEY=VALUE
            match = re.match(r'^(export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)', line)
            if match:
                export_prefix = bool(match.group(1))
                key = match.group(2)
                value = match.group(3).strip()

                # Remove surrounding quotes
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]

                entries.append({
                    "lineno": lineno,
                    "type": "var",
                    "key": key,
                    "value": value,
                    "export": export_prefix,
                    "raw": raw_line.rstrip(),
                })
            else:
                entries.append({"lineno": lineno, "type": "invalid", "raw": raw_line.rstrip()})

    return entries


def parse_example_file(filepath: str) -> set[str]:
    """Parse a .env.example file and return the set of expected keys."""
    keys = set()
    if not Path(filepath).exists():
        return keys
    with open(filepath, "r", errors="replace") as f:
        for line in f:
            line = line.strip()
            match = re.match(r'^(export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=', line)
            if match:
                keys.add(match.group(2))
    return keys


def analyze_env(entries: list[dict], example_keys: set[str] | None = None, strict: bool = False) -> dict:
    """Analyze parsed env entries for issues."""
    issues = []
    warnings = []
    info = []

    vars_seen = {}
    duplicates = []
    total_vars = 0
    empty_vars = []
    secret_leaks = []

    for entry in entries:
        if entry["type"] == "invalid":
            issues.append(f"Line {entry['lineno']}: Invalid syntax: {entry['raw'][:80]}")
            continue

        if entry["type"] != "var":
            continue

        total_vars += 1
        key = entry["key"]
        value = entry["value"]
        lineno = entry["lineno"]

        # Check duplicates
        if key in vars_seen:
            duplicates.append({"key": key, "first": vars_seen[key], "second": lineno})
            issues.append(f"Line {lineno}: Duplicate key '{key}' (first seen on line {vars_seen[key]})")
        vars_seen[key] = lineno

        # Check empty values
        if not value:
            empty_vars.append(key)
            if strict:
                issues.append(f"Line {lineno}: Empty value for '{key}'")
            else:
                warnings.append(f"Line {lineno}: Empty value for '{key}'")

        # Check for placeholders
        if value.lower() in PLACEHOLDER_VALUES:
            warnings.append(f"Line {lineno}: Placeholder value for '{key}': '{value}'")

        # Scan for secrets
        full_line = entry["raw"]
        for pattern_name, pattern in SECRET_PATTERNS.items():
            if pattern.search(full_line):
                # Skip if value is a placeholder
                if value.lower() in PLACEHOLDER_VALUES:
                    continue
                secret_leaks.append({
                    "key": key,
                    "lineno": lineno,
                    "pattern": pattern_name,
                })
                issues.append(f"Line {lineno}: Possible secret leak ({pattern_name}) in '{key}'")
                break

        # Check for unquoted values with spaces
        raw_value = re.match(r'^[^=]+=\s*(.*)', entry["raw"])
        if raw_value:
            rv = raw_value.group(1)
            if " " in rv and not (rv.startswith('"') or rv.startswith("'")):
                warnings.append(f"Line {lineno}: Unquoted value with spaces for '{key}' (may cause issues)")

    # Check against example file
    missing_from_env = []
    extra_in_env = []
    if example_keys is not None:
        current_keys = set(vars_seen.keys())
        missing_from_env = sorted(example_keys - current_keys)
        extra_in_env = sorted(current_keys - example_keys)

        for mk in missing_from_env:
            issues.append(f"Missing from .env: '{mk}' (defined in example)")
        for ek in extra_in_env:
            info.append(f"Extra in .env: '{ek}' (not in example)")

    return {
        "total_vars": total_vars,
        "duplicates": duplicates,
        "empty_vars": empty_vars,
        "secret_leaks": secret_leaks,
        "missing_from_env": missing_from_env,
        "extra_in_env": extra_in_env,
        "issues": issues,
        "warnings": warnings,
        "info": info,
    }


def print_report(filepath: str, result: dict) -> None:
    """Print a human-readable report."""
    print(f"\n{'='*60}")
    print(f"  ENV DOCTOR: {filepath}")
    print(f"{'='*60}")
    print(f"  Variables: {result['total_vars']}  |  Duplicates: {len(result['duplicates'])}  |  Empty: {len(result['empty_vars'])}")

    if result["secret_leaks"]:
        print(f"\n  SECRET LEAKS DETECTED:")
        for leak in result["secret_leaks"]:
            print(f"    Line {leak['lineno']}: {leak['key']} ({leak['pattern']})")

    if result["issues"]:
        print(f"\n  ISSUES ({len(result['issues'])}):")
        for issue in result["issues"]:
            print(f"    {issue}")

    if result["warnings"]:
        print(f"\n  WARNINGS ({len(result['warnings'])}):")
        for warn in result["warnings"]:
            print(f"    {warn}")

    if result["info"]:
        print(f"\n  INFO ({len(result['info'])}):")
        for item in result["info"]:
            print(f"    {item}")

    if not result["issues"] and not result["warnings"]:
        print(f"\n  All clear — no issues found.")

    health = "HEALTHY" if not result["issues"] else "NEEDS ATTENTION" if not result["secret_leaks"] else "CRITICAL"
    print(f"\n  STATUS: {health}")
    print(f"{'='*60}\n")

    if result["secret_leaks"]:
        sys.exit(2)
    elif result["issues"]:
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Validate .env files — detect secrets, duplicates, missing vars, and syntax issues.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  %(prog)s .env\n"
               "  %(prog)s .env --example .env.example\n"
               "  %(prog)s .env --strict --json\n",
    )
    parser.add_argument("envfile", help="Path to the .env file to analyze")
    parser.add_argument("--example", type=str, default=None, help="Path to .env.example for comparison")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--strict", action="store_true", help="Treat empty values as errors")

    args = parser.parse_args()

    entries = parse_env_file(args.envfile)
    example_keys = parse_example_file(args.example) if args.example else None
    result = analyze_env(entries, example_keys=example_keys, strict=args.strict)

    if args.json:
        output = {"file": args.envfile, **result}
        print(json.dumps(output, indent=2))
    else:
        print_report(args.envfile, result)


if __name__ == "__main__":
    main()
