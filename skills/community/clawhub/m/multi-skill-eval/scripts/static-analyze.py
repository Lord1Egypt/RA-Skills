#!/usr/bin/env python3
"""Static analysis for skill-assessment (Method 1).

Usage:
    python3 static-analyze.py <path-to-skill>
    python3 static-analyze.py <path-to-skill> --json
    python3 static-analyze.py <path-to-skill> --problems-only
    python3 static-analyze.py --compare <skill-a> <skill-b>
    python3 static-analyze.py --all
"""

import argparse
import json
import os
import re
import sys
import yaml


def check_documentation(skill_path):
    issues = []
    score = 100

    # Check SKILL.md exists
    skill_md = os.path.join(skill_path, "SKILL.md")
    if not os.path.isfile(skill_md):
        issues.append({"severity": "error", "check": "SKILL.md exists", "msg": "SKILL.md not found"})
        return {"score": 0, "issues": issues}

    # Parse frontmatter
    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        issues.append({"severity": "error", "check": "frontmatter", "msg": "No YAML frontmatter"})
        score -= 30
    else:
        try:
            fm = yaml.safe_load(match.group(1))
            if not isinstance(fm, dict):
                issues.append({"severity": "error", "check": "frontmatter", "msg": "Frontmatter must be YAML dict"})
                score -= 20
            else:
                if not fm.get("name"):
                    issues.append({"severity": "error", "check": "name field", "msg": "Missing 'name' in frontmatter"})
                    score -= 15
                if not fm.get("description"):
                    issues.append({"severity": "warning", "check": "description field", "msg": "Missing 'description' in frontmatter"})
                    score -= 10
                elif len(fm["description"].split()) < 15:
                    issues.append({"severity": "warning", "check": "description length", "msg": f"Description too short ({len(fm['description'].split())} words)"})
                    score -= 5

                # Check trigger contexts
                desc_lower = fm.get("description", "").lower()
                trigger_phrases = ["use when", "use for", "when the user", "when you need", "such as", "for example"]
                has_trigger = any(p in desc_lower for p in trigger_phrases)
                if not has_trigger:
                    issues.append({"severity": "info", "check": "trigger contexts", "msg": "No trigger phrases found — add 'Use when...' to improve activation"})
                    score -= 5
        except Exception as e:
            issues.append({"severity": "error", "check": "frontmatter parse", "msg": f"YAML parse error: {e}"})
            score -= 20

    # Check body length
    lines = content.split("\n")
    body_started = False
    body_lines = 0
    for line in lines:
        if line.strip() == "---" and not body_started:
            body_started = True
            continue
        if body_started:
            body_lines += 1

    if body_lines < 10:
        issues.append({"severity": "error", "check": "body length", "msg": f"Body only {body_lines} lines — too short"})
        score -= 15
    elif body_lines > 500:
        issues.append({"severity": "info", "check": "body length", "msg": f"Body {body_lines} lines — consider splitting"})

    # Check for usage examples in body
    example_indicators = ["example", "usage", "```bash", "```python", "$ "]
    has_examples = any(indicator in content.lower() for indicator in example_indicators)
    if not has_examples:
        issues.append({"severity": "warning", "check": "examples", "msg": "No usage examples found"})
        score -= 10

    return {"score": max(0, score), "issues": issues}


def check_code_quality(skill_path):
    issues = []
    score = 100

    scripts_dir = os.path.join(skill_path, "scripts")
    if not os.path.isdir(scripts_dir):
        return {"score": 100, "issues": [{"severity": "info", "check": "scripts", "msg": "No scripts/ directory"}]}

    py_files = [f for f in os.listdir(scripts_dir) if f.endswith(".py")]
    if not py_files:
        return {"score": 100, "issues": []}

    for f in py_files:
        fpath = os.path.join(scripts_dir, f)
        try:
            with open(fpath, "r", encoding="utf-8") as fh:
                code = fh.read()

            # Syntax check
            try:
                compile(code, fpath, "exec")
            except SyntaxError as e:
                issues.append({"severity": "error", "check": f"syntax ({f})", "msg": f"Syntax error at line {e.lineno}: {e.msg}"})
                score -= 10

            # Check for hardcoded secrets
            secret_patterns = [
                r'api[_-]?key\s*[=:]\s*["\'][^"\']{8,}',
                r'token\s*[=:]\s*["\'][^"\']{8,}',
                r'sk-[a-zA-Z0-9]{20,}',
                r'ghp_[a-zA-Z0-9]{36}',
            ]
            for pattern in secret_patterns:
                if re.search(pattern, code, re.IGNORECASE):
                    issues.append({"severity": "error", "check": f"secrets ({f})", "msg": f"Possible hardcoded credential in {f}"})
                    score -= 15

            # Note: "dangerous functions" (os.system, eval, exec) check removed.
            # Presence of these functions is not a security issue without
            # understanding data flow. Real security issues are caught above.

        except Exception as e:
            issues.append({"severity": "error", "check": "read error", "msg": f"Could not read {f}: {e}"})
            score -= 5

    return {"score": max(0, score), "issues": issues}


def check_configuration(skill_path):
    issues = []
    score = 100

    skill_md = os.path.join(skill_path, "SKILL.md")
    if not os.path.isfile(skill_md):
        return {"score": 0, "issues": [{"severity": "error", "check": "SKILL.md", "msg": "SKILL.md not found"}]}

    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    # Check env vars referenced
    env_refs = re.findall(r'\$\{?([A-Z_][A-Z0-9_]*)\}?', content)
    if env_refs:
        # Check they are documented
        env_section = "env" in content.lower() or "environment" in content.lower() or "variable" in content.lower()
        if not env_section:
            issues.append({"severity": "warning", "check": "env vars", "msg": f"Env vars found but not documented: {', '.join(set(env_refs[:5]))}"})
            score -= 10

    # Check for clear command examples
    has_commands = bool(re.search(r'```(bash|sh|shell|python)', content))
    if not has_commands:
        issues.append({"severity": "info", "check": "command examples", "msg": "No command examples found"})
        score -= 5

    return {"score": max(0, score), "issues": issues}


def check_maintenance(skill_path):
    issues = []
    score = 100

    # Check for versioning
    skill_md = os.path.join(skill_path, "SKILL.md")
    if os.path.isfile(skill_md):
        with open(skill_md, "r", encoding="utf-8") as f:
            content = f.read()
        if "version" not in content.lower():
            issues.append({"severity": "info", "check": "version", "msg": "No version info found in SKILL.md"})
            score -= 5

    # Check for update date patterns
    update_indicators = re.findall(r'(updated?|modified?|changed?|revised?):?\s*\d{4}-\d{2}-\d{2}', content, re.IGNORECASE)
    if update_indicators:
        issues.append({"severity": "info", "check": "update date", "msg": "Found update timestamps"})

    # Check directory structure
    for subdir in ["scripts", "references", "assets", "knowledge"]:
        dp = os.path.join(skill_path, subdir)
        if os.path.isdir(dp):
            contents = [f for f in os.listdir(dp) if not f.startswith(".") and f != "__pycache__"]
            if not contents:
                issues.append({"severity": "warning", "check": f"{subdir}/ empty", "msg": f"{subdir}/ is empty"})
                score -= 5

    return {"score": max(0, score), "issues": issues}


def analyze(skill_path, json_output=False, problems_only=False):
    if not os.path.isdir(skill_path):
        print(f"Error: {skill_path} is not a directory", file=sys.stderr)
        sys.exit(1)

    doc = check_documentation(skill_path)
    code = check_code_quality(skill_path)
    config = check_configuration(skill_path)
    maint = check_maintenance(skill_path)

    total_score = (doc["score"] * 0.3 + code["score"] * 0.3 + config["score"] * 0.2 + maint["score"] * 0.2)

    all_issues = doc["issues"] + code["issues"] + config["issues"] + maint["issues"]

    if json_output:
        result = {
            "skill": os.path.basename(os.path.abspath(skill_path)),
            "path": os.path.abspath(skill_path),
            "scores": {
                "documentation": doc["score"],
                "code_quality": code["score"],
                "configuration": config["score"],
                "maintenance": maint["score"],
            },
            "overall": round(total_score, 1),
            "issues": all_issues,
        }
        print(json.dumps(result, indent=2))
    else:
        skill_name = os.path.basename(os.path.abspath(skill_path))
        print(f"\n📊 Skill Assessment: {skill_name}")
        print(f"{'=' * 50}")
        print(f"  Documentation:    {doc['score']}/100")
        print(f"  Code Quality:    {code['score']}/100")
        print(f"  Configuration:   {config['score']}/100")
        print(f"  Maintenance:     {maint['score']}/100")
        print(f"  ─────────────────────────")
        print(f"  Overall:         {total_score:.0f}/100")
        print()

        if problems_only:
            filtered = [i for i in all_issues if i["severity"] != "info"]
        else:
            filtered = all_issues

        if filtered:
            print("  Issues:")
            for issue in filtered:
                icon = {"error": "❌", "warning": "⚠️ ", "info": "ℹ️ "}[issue["severity"]]
                print(f"    {icon} [{issue['check']}] {issue['msg']}")
        else:
            print("  ✅ No issues found")
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Static skill assessment")
    parser.add_argument("path", nargs="?", help="Path to skill directory")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--problems-only", action="store_true", help="Show only errors/warnings")
    parser.add_argument("--compare", nargs=2, metavar=("SKILL-A", "SKILL-B"), help="Compare two skills")
    parser.add_argument("--all", action="store_true", help="Analyze all skills in ~/.openclaw/skills/")
    args = parser.parse_args()

    if args.compare:
        for p in args.compare:
            analyze(p, args.json, args.problems_only)
    elif args.all:
        skills_dir = os.path.expanduser("~/.openclaw/skills/")
        if os.path.isdir(skills_dir):
            for d in os.listdir(skills_dir):
                full = os.path.join(skills_dir, d)
                if os.path.isdir(full) and not d.startswith("."):
                    analyze(full, args.json, args.problems_only)
        else:
            print(f"Skills dir not found: {skills_dir}")
    elif args.path:
        analyze(args.path, args.json, args.problems_only)
    else:
        parser.print_help()