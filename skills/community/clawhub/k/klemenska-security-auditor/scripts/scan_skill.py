#!/usr/bin/env python3
"""
Detailed scanner for a specific skill.
Usage: python3 scan_skill.py <skill-path>
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime

def analyze_skill_structure(skill_path):
    """Analyze the structure of a skill."""
    skill_path = Path(skill_path)
    
    structure = {
        "name": skill_path.name,
        "files": [],
        "total_size_kb": 0,
        "has_readme": False,
        "has_skill_md": False,
        "has_scripts": False,
        "has_references": False,
    }
    
    for filepath in skill_path.rglob("*"):
        if filepath.is_file():
            rel_path = filepath.relative_to(skill_path)
            size_kb = filepath.stat().st_size / 1024
            structure["files"].append({
                "path": str(rel_path),
                "size_kb": round(size_kb, 2)
            })
            structure["total_size_kb"] += size_kb
            
            if filepath.name.lower() == "readme.md":
                structure["has_readme"] = True
            if filepath.name == "SKILL.md":
                structure["has_skill_md"] = True
            if "scripts" in str(rel_path):
                structure["has_scripts"] = True
            if "references" in str(rel_path):
                structure["has_references"] = True
    
    structure["total_size_kb"] = round(structure["total_size_kb"], 2)
    return structure

def extract_permissions(skill_md_path):
    """Extract permissions from SKILL.md."""
    if not skill_md_path.exists():
        return []
    
    content = skill_md_path.read_text()
    permissions = []
    
    # Look for common permission patterns
    perm_patterns = [
        (r"exec", "Shell command execution"),
        (r"file.*read", "File system read access"),
        (r"file.*write", "File system write access"),
        (r"network|http|request", "Network access"),
        (r"browser", "Browser automation"),
        (r"message|chat|send", "Messaging capabilities"),
        (r"cron|schedule", "Scheduled task execution"),
        (r"database|db|sql", "Database access"),
        (r"api.*key|api.*token", "API key access"),
        (r"git|version.control", "Git operations"),
        (r"ssh|remote", "Remote access"),
        (r"camera|photo|media", "Camera/media access"),
        (r"location|gps", "Location access"),
        (r"notification", "System notifications"),
        (r"clipboard", "Clipboard access"),
        (r"process|memory", "Process/memory access"),
    ]
    
    for pattern, description in perm_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            if description not in permissions:
                permissions.append(description)
    
    return permissions

def check_file_safety(filepath):
    """Check if a file contains unsafe patterns."""
    try:
        content = filepath.read_text()
    except:
        return {"safe": False, "issues": ["Could not read file"]}
    
    issues = []
    
    # Check for potentially unsafe patterns
    unsafe_patterns = [
        (r"eval\s*\(", "eval() usage - dynamic code execution"),
        (r"exec\s*\(", "exec() usage - code injection risk"),
        (r"__import__\s*\(", "__import__() - dynamic module loading"),
        (r"subprocess.*shell\s*=\s*True", "subprocess with shell=True - injection risk"),
        (r"password\s*=\s*['\"][^'\"]+['\"]", "Hardcoded password"),
        (r"api[_-]?key\s*=\s*['\"][^'\"]+['\"]", "Hardcoded API key"),
        (r"token\s*=\s*['\"][^'\"]+['\"]", "Hardcoded token"),
        (r"base64\.b64decode", "Base64 decoding - possible obfuscation"),
        (r"pickle\.load", "Pickle deserialization - code execution risk"),
        (r"yaml\.load\s*\([^)]*Loader\s*=\s*None", "YAML unsafe load - code execution risk"),
    ]
    
    lines = content.split("\n")
    for pattern, description in unsafe_patterns:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line, re.IGNORECASE):
                # Skip false positives in audit/scan scripts
                if "audit" in str(filepath).lower() or "scan" in str(filepath).lower():
                    # But still flag actual bad patterns like hardcoded passwords
                    if "password" in pattern.lower() or "api_key" in pattern.lower() or "token" in pattern.lower():
                        issues.append({
                            "line": i,
                            "pattern": description,
                            "text": line.strip()[:80]
                        })
                else:
                    issues.append({
                        "line": i,
                        "pattern": description,
                        "text": line.strip()[:80]
                    })
    
    return {
        "safe": len(issues) == 0,
        "issues": issues,
        "lines_of_code": len([l for l in lines if l.strip() and not l.strip().startswith("#")])
    }

def generate_report(skill_path):
    """Generate comprehensive security report for a skill."""
    skill_path = Path(skill_path)
    
    report = {
        "skill_name": skill_path.name,
        "timestamp": datetime.now().isoformat(),
        "structure": analyze_skill_structure(skill_path),
        "permissions": extract_permissions(skill_path / "SKILL.md"),
        "files_checked": 0,
        "files_with_issues": [],
        "total_issues": 0
    }
    
    # Check all code files
    for pattern in ["*.py", "*.js", "*.sh"]:
        for filepath in skill_path.rglob(pattern):
            if ".defrag_backup" in str(filepath):
                continue
            
            result = check_file_safety(filepath)
            report["files_checked"] += 1
            
            if not result["safe"]:
                report["files_with_issues"].append({
                    "file": str(filepath.relative_to(skill_path)),
                    "issues": result["issues"],
                    "loc": result["lines_of_code"]
                })
                report["total_issues"] += len(result["issues"])
    
    # Determine overall risk
    if report["total_issues"] == 0:
        report["risk_level"] = "LOW"
    elif report["total_issues"] <= 3:
        report["risk_level"] = "MEDIUM"
    elif report["total_issues"] <= 10:
        report["risk_level"] = "HIGH"
    else:
        report["risk_level"] = "CRITICAL"
    
    return report

def print_report(report):
    """Print the security report."""
    print("\n" + "=" * 60)
    print("SKILL SECURITY SCAN")
    print("=" * 60)
    
    print(f"\n📦 Skill: {report['skill_name']}")
    print(f"🕐 Scanned: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    s = report["structure"]
    print(f"\n📁 Structure:")
    print(f"   Files: {len(s['files'])}")
    print(f"   Total size: {s['total_size_kb']} KB")
    print(f"   Has SKILL.md: {'✅' if s['has_skill_md'] else '❌'}")
    print(f"   Has scripts: {'✅' if s['has_scripts'] else '❌'}")
    print(f"   Has references: {'✅' if s['has_references'] else '❌'}")
    
    print(f"\n🔓 Permissions detected:")
    if report["permissions"]:
        for perm in report["permissions"]:
            print(f"   - {perm}")
    else:
        print("   None detected")
    
    print(f"\n🔍 Files checked: {report['files_checked']}")
    
    risk_emoji = {
        "LOW": "🟢",
        "MEDIUM": "🟡",
        "HIGH": "🔴",
        "CRITICAL": "⛔"
    }
    emoji = risk_emoji.get(report["risk_level"], "⚪")
    
    print(f"\n{emoji} Risk level: {report['risk_level']}")
    print(f"   Issues found: {report['total_issues']}")
    
    if report["files_with_issues"]:
        print(f"\n⚠️  Files with issues:")
        for f in report["files_with_issues"][:10]:
            print(f"\n   📄 {f['file']} ({f['loc']} LOC)")
            for issue in f["issues"][:5]:
                print(f"      Line {issue['line']}: {issue['pattern']}")
    
    print()

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scan_skill.py <skill-path>")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    report = generate_report(skill_path)
    print_report(report)
    
    # Exit with error code if high risk
    if report["risk_level"] in ["HIGH", "CRITICAL"]:
        sys.exit(1)
    elif report["risk_level"] == "MEDIUM":
        sys.exit(2)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
