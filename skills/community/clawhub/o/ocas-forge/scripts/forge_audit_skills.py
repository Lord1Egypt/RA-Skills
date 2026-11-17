#!/usr/bin/env python3
"""
forge_audit_skills.py

Audit OCAS skills for compliance with OCAS architecture standards before
publishing/syncing to GitHub (Nous optional-skills catalog).

Includes the MANDATORY Configuration Policy (env-var-for-config): behavioral
settings must be read from config.yaml under skills.config.<key>, never from
non-secret environment variables (GENIE_*, *_MAX_AGE_DAYS, *_PATH, *_ENABLED, etc.).

Usage:
    python3 forge_audit_skills.py [--skill <name>] [--fix] [--json]

Exit code: 0 if no blocking (ERROR) issues, 1 otherwise.
"""

import argparse
import json
import os
import re
import sys

# Skills root: this script lives at <skill>/scripts/, so the package root is one up.
SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# OCAS skills directory (override with --skills-dir if auditing a different tree)
DEFAULT_SKILLS_DIR = os.path.dirname(SKILL_ROOT)

# Allowed runtime-locating env vars — never behavioral tuning.
ALLOWED_ENV_VARS = {"HERMES_HOME", "HERMES_PROFILE", "HERMES_CONFIG"}

# Patterns that indicate a NON-SECRET behavioral env-var read (policy violation).
# Captures GENIE_*, <NAME>_MAX_AGE_DAYS, <NAME>_PATH, <NAME>_ENABLED, <NAME>_DAYS, etc.
FORBIDDEN_ENV_PATTERN = re.compile(
    r'os\.environ\.get\(\s*["\']'
    r'(?!GENIE_FILESYSTEM)'  # (legacy allow handled separately)
    r'(?:GENIE_|[A-Z][A-Z0-9_]*_(?:MAX_AGE_DAYS|MIN_AGE_DAYS|RETENTION_DAYS|COMPRESS_AGE_DAYS|'
    r'DELETE_AGE_DAYS|STALE_HOURS|MAX_AGE|PATH|ENABLED|ENABLE|DAYS|COUNT|THRESHOLD|LIMIT|'
    r'DRY_RUN|TIER_LIMIT|ALLOW_))'
    r'[A-Z0-9_]*["\']'
)

# SKILL.md body lines that document env-var names (ALL-CAPS, e.g. GENIE_*,
# <NAME>_MAX_AGE_DAYS, <NAME>_DRY_RUN) as user-facing config controls.
# Deliberately EXCLUDES *_PATH / TOKEN_PATH / DEFAULT_DB_PATH — those are code
# identifiers/constants, not tunable env-var config the user sets.
FORBIDDEN_DOC_PATTERN = re.compile(
    r'`(?:GENIE_[A-Z0-9_]+|'
    r'[A-Z][A-Z0-9_]*_(?:MAX_AGE_DAYS|MIN_AGE_DAYS|RETENTION_DAYS|COMPRESS_AGE_DAYS|'
    r'DELETE_AGE_DAYS|STALE_HOURS|MAX_AGE|ENABLED|ENABLE|DAYS|COUNT|THRESHOLD|'
    r'LIMIT|DRY_RUN|TIER_LIMIT|ALLOW_)[A-Z0-9_]*)`'
)


def find_ocas_skills(skills_dir, only=None):
    found = []
    if not os.path.isdir(skills_dir):
        return found
    for name in sorted(os.listdir(skills_dir)):
        if only and name != only:
            continue
        if not name.startswith("ocas-"):
            continue
        skill_dir = os.path.join(skills_dir, name)
        if not os.path.isdir(skill_dir):
            continue
        if os.path.exists(os.path.join(skill_dir, "SKILL.md")):
            found.append(skill_dir)
    return found


def audit_skill(skill_dir):
    name = os.path.basename(skill_dir)
    issues = []  # list of (severity, message)

    skill_md = os.path.join(skill_dir, "SKILL.md")
    scripts_dir = os.path.join(skill_dir, "scripts")

    # 1. Scan scripts for forbidden env-var config reads.
    if os.path.isdir(scripts_dir):
        for fname in os.listdir(scripts_dir):
            if not fname.endswith((".py", ".sh")):
                continue
            if fname.endswith(".bak") or ".bak." in fname:
                continue
            fpath = os.path.join(scripts_dir, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as fh:
                    lines = fh.readlines()
            except OSError:
                continue
            for i, line in enumerate(lines, 1):
                m = FORBIDDEN_ENV_PATTERN.search(line)
                if m:
                    var = re.search(r'["\']([A-Z][A-Z0-9_]*)["\']', m.group(0))
                    varname = var.group(1) if var else "?"
                    # HERMES_HOME / HERMES_PROFILE are allowed (runtime location).
                    if varname in ALLOWED_ENV_VARS:
                        continue
                    issues.append((
                        "ERROR",
                        f"{name}/scripts/{fname}:{i} reads non-secret config from env var "
                        f"{varname} — must use skills.config.* in config.yaml",
                    ))

    # 2. Scan SKILL.md body for documented env-var config tables.
    if os.path.exists(skill_md) and not skill_md.endswith(".bak"):
        with open(skill_md, "r", encoding="utf-8") as fh:
            md_lines = fh.readlines()
        in_frontmatter = False
        for i, line in enumerate(md_lines, 1):
            if line.strip() == "---":
                in_frontmatter = not in_frontmatter
                continue
            if in_frontmatter:
                continue
            if FORBIDDEN_DOC_PATTERN.search(line):
                issues.append((
                    "ERROR",
                    f"{name}/SKILL.md:{i} documents an env-var config name as user-facing "
                    f"control — must document skills.config.<key> instead",
                ))

    # 3. Positive check: if scripts read os.environ for HERMES_HOME, ensure a
    #    skills.config.* resolver exists somewhere in the package.
    has_resolver = False
    if os.path.isdir(scripts_dir):
        for fname in os.listdir(scripts_dir):
            if not fname.endswith(".py"):
                continue
            fpath = os.path.join(scripts_dir, fname)
            try:
                txt = open(fpath, "r", encoding="utf-8").read()
            except OSError:
                continue
            if "skills.config" in txt or "skills_config" in txt or "_skill_config" in txt:
                has_resolver = True
                break
    if has_resolver:
        issues.append(("OK", f"{name}: uses skills.config.* resolver (config.yaml)"))

    return issues


def main():
    parser = argparse.ArgumentParser(
        description="Audit OCAS skills for compliance",
        epilog="Examples:\n"
               "  python3 forge_audit_skills.py --skill ocas-genie\n"
               "  python3 forge_audit_skills.py --skills-dir /path/to/skills --json\n"
               "Exit code 0 = clean (no blocking issues); 1 = blocking (ERROR) issues found.")
    parser.add_argument("--skill", help="Audit a single skill only (e.g. ocas-genie). "
                                         "Omit to scan every ocas-* skill in --skills-dir.")
    parser.add_argument("--skills-dir", default=DEFAULT_SKILLS_DIR,
                        help="Directory containing ocas-* skill packages (default: %(default)s)")
    parser.add_argument("--json", action="store_true",
                        help="Emit a JSON report instead of human-readable text")
    args = parser.parse_args()

    skills = find_ocas_skills(args.skills_dir, only=args.skill)
    if not skills:
        print(f"No ocas-* skills found in {args.skills_dir}", file=sys.stderr)
        return 2

    all_results = {}
    error_count = 0
    for skill_dir in skills:
        name = os.path.basename(skill_dir)
        issues = audit_skill(skill_dir)
        all_results[name] = [
            {"severity": sev, "message": msg} for sev, msg in issues
        ]
        for sev, msg in issues:
            if sev == "ERROR":
                error_count += 1
                print(f"  [ERROR] {msg}")
            elif sev == "OK":
                print(f"  [ok]    {msg}")

    if args.json:
        print(json.dumps(all_results, indent=2))

    print(f"\nAudited {len(skills)} skill(s); {error_count} blocking issue(s).")
    return 1 if error_count else 0


if __name__ == "__main__":
    sys.exit(main())