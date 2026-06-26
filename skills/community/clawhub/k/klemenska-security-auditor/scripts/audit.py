#!/usr/bin/env python3
"""
Security audit script for skills.
Usage: python3 audit.py --scan
       python3 audit.py --audit <skill-path>
       python3 audit.py --report <skill-path> --output <report.md>
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path

# Red flag patterns
RED_FLAGS = {
    "file_access": [
        ("~/.ssh/", "SSH directory access"),
        ("~/.aws/", "AWS credentials access"),
        ("~/.kube/", "Kubernetes config access"),
        ("id_rsa", "SSH key access"),
        ("id_ed25519", "SSH key access"),
        ("/.docker/", "Docker config access"),
    ],
    "credential_access": [
        ("password", "Password file access"),
        ("secret", "Secret file access"),
        ("credentials", "Credentials access"),
        (".env", "Environment file access"),
    ],
    "network": [
        ("eval(", "Dynamic code execution"),
        ("exec(", "Shell execution"),
    ],
    "permissions": [
        ("--privileged", "Privileged mode"),
        ("--cap-all", "All capabilities"),
        ("security=insecure", "Insecure security mode"),
        ("elevated=true", "Elevated permissions"),
    ],
    "suspicious": [
        ("base64", "Base64 encoding"),
        ("decrypt", "Decryption"),
        ("obfuscate", "Obfuscation"),
    ]
}

def scan_file(filepath):
    """Scan a single file for red flags."""
    issues = []
    warnings = []
    
    try:
        content = filepath.read_text()
        lines = content.split("\n")
        
        for category, patterns in RED_FLAGS.items():
            for pattern, description in patterns:
                if pattern in content:
                    # Find line numbers
                    for i, line in enumerate(lines, 1):
                        if pattern in line:
                            issues.append({
                                "category": category,
                                "pattern": description,
                                "file": str(filepath.relative_to(filepath.parent)),
                                "line": i,
                                "text": line.strip()[:100]
                            })
    except Exception as e:
        warnings.append(f"Could not read {filepath}: {e}")
    
    return {"issues": issues, "warnings": warnings}

def get_risk_level(issues):
    """Determine risk level based on issues found."""
    if not issues:
        return "LOW", "No significant issues found"
    
    critical = sum(1 for i in issues if "credential" in i["pattern"].lower() or "password" in i["pattern"].lower())
    high = sum(1 for i in issues if "execution" in i["pattern"].lower() or "subprocess" in i["pattern"].lower())
    
    if critical > 0:
        return "CRITICAL", f"Found {critical} credential-related issues"
    if high > 0:
        return "HIGH", f"Found {high} execution-related issues"
    
    return "MEDIUM", f"Found {len(issues)} potential concerns"

def audit_skill(skill_path):
    """Perform full audit on a skill."""
    skill_path = Path(skill_path)
    
    if not skill_path.exists():
        return {"error": f"Skill path does not exist: {skill_path}"}
    
    # Skip self-audit to avoid false positives
    if skill_path.name == "security-auditor" or str(skill_path) == __file__:
        return {
            "skill": str(skill_path),
            "files_scanned": 0,
            "issues": [],
            "warnings": ["Self-audit skipped"],
            "permissions": ["file read/write"],
            "risk_level": "LOW",
            "risk_message": "Self-audit exempted",
            "timestamp": datetime.now().isoformat()
        }
    
    results = {
        "skill": str(skill_path),
        "files_scanned": 0,
        "issues": [],
        "warnings": [],
        "permissions": [],
        "timestamp": datetime.now().isoformat()
    }
    
    # Check for SKILL.md
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        content = skill_md.read_text()
        
        # Extract permissions from description
        if "exec" in content.lower():
            results["permissions"].append("exec (shell command execution)")
        if "read" in content.lower() or "write" in content.lower():
            results["permissions"].append("file read/write")
        if "http" in content.lower() or "request" in content.lower():
            results["permissions"].append("network access")
    
    # Scan all Python and JS files
    for pattern in ["**/*.py", "**/*.js", "**/*.sh"]:
        for filepath in skill_path.glob(pattern):
            if ".defrag_backup" in str(filepath):
                continue
            result = scan_file(filepath)
            results["issues"].extend(result["issues"])
            results["warnings"].extend(result["warnings"])
            results["files_scanned"] += 1
    
    risk_level, risk_message = get_risk_level(results["issues"])
    results["risk_level"] = risk_level
    results["risk_message"] = risk_message
    
    return results

def scan_installed_skills(base_path=None):
    """Scan all installed skills."""
    if base_path is None:
        base_path = Path("~/.openclaw/workspace/skills").expanduser()
    
    skills = []
    
    if not base_path.exists():
        return {"error": f"Skills directory not found: {base_path}"}
    
    for skill_dir in base_path.iterdir():
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
            # Skip self-audit to avoid false positives
            if skill_dir.name == "security-auditor":
                continue
            result = audit_skill(skill_dir)
            skills.append({
                "name": skill_dir.name,
                "path": str(skill_dir),
                "risk_level": result.get("risk_level", "UNKNOWN"),
                "issues_count": len(result.get("issues", [])),
                "permissions": result.get("permissions", [])
            })
    
    return {"skills": skills, "scanned": len(skills)}

def print_report(results):
    """Print audit report."""
    print("\n" + "=" * 60)
    print("SECURITY AUDIT REPORT")
    print("=" * 60)
    print(f"\n📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    if "error" in results:
        print(f"\n❌ Error: {results['error']}")
        return
    
    if "skills" in results:
        # Scan mode
        print(f"\n📊 Scanned {results['scanned']} skills\n")
        
        risk_colors = {
            "LOW": "🟢",
            "MEDIUM": "🟡", 
            "HIGH": "🔴",
            "CRITICAL": "⛔"
        }
        
        for skill in results["skills"]:
            emoji = risk_colors.get(skill["risk_level"], "⚪")
            print(f"{emoji} {skill['name']} ({skill['risk_level']})")
            if skill["issues_count"] > 0:
                print(f"   Issues: {skill['issues_count']}")
            if skill["permissions"]:
                print(f"   Permissions: {', '.join(skill['permissions'][:3])}")
        print()
        
    else:
        # Single audit mode
        print(f"\n📂 Skill: {results.get('skill', 'Unknown')}")
        print(f"📄 Files scanned: {results.get('files_scanned', 0)}")
        print(f"🔒 Risk level: {results.get('risk_level', 'UNKNOWN')}")
        print(f"📝 {results.get('risk_message', '')}")
        
        if results.get("permissions"):
            print(f"\n🔓 Requested permissions:")
            for perm in results["permissions"]:
                print(f"   - {perm}")
        
        if results.get("issues"):
            print(f"\n⚠️  Issues found ({len(results['issues'])}):")
            seen_categories = set()
            for issue in results["issues"][:20]:
                cat = issue["category"]
                if cat not in seen_categories:
                    print(f"\n   [{cat.upper()}]")
                    seen_categories.add(cat)
                print(f"   - {issue['pattern']} at {issue['file']}:{issue['line']}")
            
            if len(results["issues"]) > 20:
                print(f"\n   ... and {len(results['issues']) - 20} more issues")
        else:
            print("\n✅ No issues found!")
        
        if results.get("warnings"):
            print(f"\n⚠️  Warnings ({len(results['warnings'])}):")
            for warn in results["warnings"][:5]:
                print(f"   - {warn}")
        print()

def main():
    parser = argparse.ArgumentParser(description="Security audit for skills")
    parser.add_argument("--scan", action="store_true", help="Scan all installed skills")
    parser.add_argument("--audit", metavar="PATH", help="Audit a specific skill")
    parser.add_argument("--report", metavar="PATH", help="Generate detailed report for skill")
    parser.add_argument("--output", metavar="FILE", help="Output file for report")
    parser.add_argument("--compare", nargs=2, metavar=("PATH1", "PATH2"), help="Compare two skills")
    args = parser.parse_args()
    
    if args.scan:
        results = scan_installed_skills()
        print_report(results)
    elif args.audit:
        results = audit_skill(args.audit)
        print_report(results)
    elif args.report:
        results = audit_skill(args.report)
        print_report(results)
        if args.output:
            # Generate markdown report
            report = f"# Security Audit Report\n\n"
            report += f"**Skill:** {results.get('skill', 'Unknown')}\n"
            report += f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            report += f"**Risk Level:** {results.get('risk_level', 'UNKNOWN')}\n\n"
            
            if results.get("permissions"):
                report += "## Permissions\n\n"
                for perm in results["permissions"]:
                    report += f"- {perm}\n"
                report += "\n"
            
            if results.get("issues"):
                report += "## Issues\n\n"
                for issue in results["issues"]:
                    report += f"- **{issue['pattern']}** in {issue['file']}:{issue['line']}\n"
                    report += f"  ```\n  {issue['text']}\n  ```\n\n"
            
            Path(args.output).write_text(report)
            print(f"📄 Report saved to: {args.output}")
    elif args.compare:
        r1 = audit_skill(args.compare[0])
        r2 = audit_skill(args.compare[1])
        print(f"\n🔍 Comparing skills:")
        print(f"\n{Path(args.compare[0]).name}: {r1.get('risk_level', 'UNKNOWN')} risk")
        print(f"{Path(args.compare[1]).name}: {r2.get('risk_level', 'UNKNOWN')} risk")
    else:
        parser.print_help()
        print("\n⚠️  Specify --scan, --audit <path>, or --compare <path1> <path2>")

if __name__ == "__main__":
    main()
