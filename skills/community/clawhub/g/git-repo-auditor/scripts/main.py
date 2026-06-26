#!/usr/bin/env python3
"""
Git Repository Auditor
Scan Git repositories for security issues, large files, and repository health.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

# Default secret patterns
DEFAULT_PATTERNS = {
    "aws_access_key": r"AKIA[0-9A-Z]{16}",
    "aws_secret_key": r"[0-9a-zA-Z/+]{40}",
    "github_token": r"ghp_[0-9a-zA-Z]{36}",
    "github_oauth": r"gho_[0-9a-zA-Z]{36}",
    "ssh_private_key": r"-----BEGIN (?:RSA|DSA|EC|OPENSSH) PRIVATE KEY-----",
    "password_in_code": r"password\s*[=:]\s*['\"][^'\"]{6,}['\"]",
    "api_key": r"(?i)api[_-]?key\s*[=:]\s*['\"][^'\"]{10,}['\"]",
    "slack_token": r"xox[baprs]-[0-9a-zA-Z]{10,48}",
    "stripe_key": r"sk_live_[0-9a-zA-Z]{24}",
    "generic_token": r"[0-9a-zA-Z_-]{20,}",
}

def run_git_command(args: List[str], cwd: str = None) -> str:
    """Run git command and return output."""
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            return ""
        return result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        return ""

def is_git_repo(path: str) -> bool:
    """Check if path is a Git repository."""
    return run_git_command(["rev-parse", "--git-dir"], cwd=path) != ""

def get_repo_info(path: str) -> Dict[str, Any]:
    """Get basic repository information."""
    info = {
        "path": os.path.abspath(path),
        "is_repo": False,
        "branch_count": 0,
        "commit_count": 0,
        "contributor_count": 0,
        "first_commit": None,
        "last_commit": None,
    }
    
    if not is_git_repo(path):
        return info
    
    info["is_repo"] = True
    
    # Get branch count
    branches = run_git_command(["branch", "--all"], cwd=path)
    if branches:
        info["branch_count"] = len([b for b in branches.split('\n') if b.strip()])
    
    # Get commit count
    commit_count = run_git_command(["rev-list", "--count", "HEAD"], cwd=path)
    if commit_count:
        info["commit_count"] = int(commit_count)
    
    # Get contributor count
    contributors = run_git_command(["shortlog", "-s", "-n", "HEAD"], cwd=path)
    if contributors:
        info["contributor_count"] = len(contributors.split('\n'))
    
    # Get first and last commit dates
    first_commit = run_git_command(["log", "--reverse", "--format=%cd", "--date=iso", "HEAD"], cwd=path)
    if first_commit:
        info["first_commit"] = first_commit.split('\n')[0]
    
    last_commit = run_git_command(["log", "-1", "--format=%cd", "--date=iso", "HEAD"], cwd=path)
    if last_commit:
        info["last_commit"] = last_commit
    
    return info

def scan_for_secrets(path: str, patterns: Dict[str, str] = None) -> List[Dict[str, Any]]:
    """Scan Git history for secrets using regex patterns."""
    if patterns is None:
        patterns = DEFAULT_PATTERNS
    
    issues = []
    
    # Get all commits
    commits = run_git_command(["log", "--pretty=format:%H|%an|%ad|%s", "--date=iso", "HEAD"], cwd=path)
    if not commits:
        return issues
    
    for commit_line in commits.split('\n'):
        if not commit_line:
            continue
        
        commit_hash, author, date, message = commit_line.split('|', 3)
        
        # Get files changed in this commit
        files = run_git_command(["show", "--name-only", "--pretty=", commit_hash], cwd=path)
        if not files:
            continue
        
        for filename in files.split('\n'):
            if not filename.strip():
                continue
            
            # Get file content at this commit
            content = run_git_command(["show", f"{commit_hash}:{filename}"], cwd=path)
            if not content:
                continue
            
            # Check each pattern
            for pattern_name, pattern_regex in patterns.items():
                matches = re.finditer(pattern_regex, content, re.IGNORECASE)
                for match in matches:
                    issues.append({
                        "severity": "high" if "key" in pattern_name or "token" in pattern_name else "medium",
                        "type": pattern_name,
                        "commit": commit_hash,
                        "date": date,
                        "author": author,
                        "file": filename,
                        "match": match.group(0)[:50] + ("..." if len(match.group(0)) > 50 else ""),
                        "line": content[:match.start()].count('\n') + 1,
                        "remediation": f"Remove secret from history using git filter-branch or BFG"
                    })
    
    return issues

def scan_for_large_files(path: str, threshold_mb: int = 10) -> List[Dict[str, Any]]:
    """Scan for large files in Git history."""
    large_files = []
    
    # Get all blob sizes
    blobs = run_git_command(["rev-list", "--objects", "--all"], cwd=path)
    if not blobs:
        return large_files
    
    blob_hashes = [line.split()[0] for line in blobs.split('\n') if line and ' ' in line]
    
    for blob_hash in blob_hashes[:100]:  # Limit to first 100 for performance
        # Get blob size
        size_output = run_git_command(["cat-file", "-s", blob_hash], cwd=path)
        if not size_output:
            continue
        
        size_bytes = int(size_output)
        size_mb = size_bytes / (1024 * 1024)
        
        if size_mb > threshold_mb:
            # Get file path for this blob
            name_output = run_git_command(["name-rev", "--name-only", blob_hash], cwd=path)
            file_path = name_output if name_output else f"unknown_{blob_hash[:8]}"
            
            # Find commit that introduced this blob
            commit_output = run_git_command(["log", "--oneline", "--all", "--", f"*{file_path}"], cwd=path)
            commit_info = commit_output.split('\n')[0] if commit_output else f"unknown ({blob_hash[:8]})"
            
            large_files.append({
                "size_mb": round(size_mb, 2),
                "path": file_path,
                "blob_hash": blob_hash[:8],
                "commit_info": commit_info,
            })
    
    return large_files

def get_repository_health(path: str) -> Dict[str, Any]:
    """Get repository health metrics."""
    health = {
        "stale_branches": [],
        "merge_conflicts": False,
        "binary_files": 0,
        "gitignore_present": False,
        "meaningful_commits": 0,
        "total_commits": 0,
    }
    
    # Check for .gitignore
    gitignore_path = os.path.join(path, ".gitignore")
    health["gitignore_present"] = os.path.exists(gitignore_path)
    
    # Get stale branches (no commits in 90 days)
    branches = run_git_command(["branch", "--all", "--format=%(refname:short)|%(committerdate:iso)"], cwd=path)
    if branches:
        now = datetime.now(timezone.utc)
        for branch_line in branches.split('\n'):
            if '|' not in branch_line:
                continue
            branch_name, date_str = branch_line.split('|', 1)
            try:
                branch_date = datetime.fromisoformat(date_str.replace(' ', 'T'))
                days_old = (now - branch_date).days
                if days_old > 90:
                    health["stale_branches"].append({
                        "name": branch_name,
                        "days_old": days_old,
                        "last_commit": date_str
                    })
            except ValueError:
                pass
    
    # Count binary files (approximate)
    binary_files = run_git_command(["ls-files", "--eol"], cwd=path)
    if binary_files:
        health["binary_files"] = len([f for f in binary_files.split('\n') if 'binary' in f])
    
    return health

def scan_command(args):
    """Handle scan command."""
    path = args.path
    if not os.path.exists(path):
        print(f"❌ Path not found: {path}")
        return
    
    if not is_git_repo(path):
        print(f"❌ Not a Git repository: {path}")
        return
    
    print(f"🔍 Scanning repository: {os.path.abspath(path)}")
    
    # Get repo info
    repo_info = get_repo_info(path)
    if not repo_info["is_repo"]:
        print("❌ Could not get repository information")
        return
    
    print(f"📊 Repository info: {repo_info['commit_count']} commits, "
          f"{repo_info['branch_count']} branches, {repo_info['contributor_count']} contributors")
    
    # Scan for secrets
    print("\n🔐 Scanning for secrets...")
    secrets = scan_for_secrets(path)
    
    # Scan for large files
    print("💾 Scanning for large files...")
    large_files = scan_for_large_files(path, args.threshold)
    
    # Get health metrics
    print("📈 Checking repository health...")
    health = get_repository_health(path)
    
    # Output
    if args.json:
        output = {
            "repository": os.path.abspath(path),
            "scan_date": datetime.now(timezone.utc).isoformat(),
            "repository_info": repo_info,
            "security_issues": secrets,
            "large_files": large_files,
            "health_metrics": health,
            "summary": {
                "total_security_issues": len(secrets),
                "total_large_files": len(large_files),
                "stale_branches": len(health["stale_branches"]),
                "binary_files": health["binary_files"],
            }
        }
        print(json.dumps(output, indent=2, default=str))
        return
    
    # Human-readable output
    if secrets:
        print(f"\n⚠️  SECURITY ISSUES FOUND ({len(secrets)}):")
        for i, issue in enumerate(secrets[:5], 1):  # Limit to 5 issues
            print(f"{i}. {issue['severity'].upper()}: {issue['type']} found in commit {issue['commit'][:8]}")
            print(f"   File: {issue['file']}")
            print(f"   Match: {issue['match']}")
            print(f"   Remediation: {issue['remediation']}")
            print()
        if len(secrets) > 5:
            print(f"... and {len(secrets) - 5} more issues")
    else:
        print("✅ No security issues found")
    
    if large_files:
        print(f"\n💾 LARGE FILES FOUND ({len(large_files)}):")
        for i, file in enumerate(large_files[:5], 1):
            print(f"{i}. {file['size_mb']}MB: {file['path']}")
            print(f"   Commit: {file['commit_info']}")
            print()
        if len(large_files) > 5:
            print(f"... and {len(large_files) - 5} more large files")
    else:
        print("✅ No large files found")
    
    # Health summary
    print("\n📊 REPOSITORY HEALTH:")
    print(f"✅ .gitignore present: {'Yes' if health['gitignore_present'] else 'No'}")
    print(f"📦 Binary files: {health['binary_files']}")
    print(f"⏰ Stale branches (>90 days): {len(health['stale_branches'])}")
    if health['stale_branches']:
        for branch in health['stale_branches'][:3]:
            print(f"   - {branch['name']} ({branch['days_old']} days old)")

def health_command(args):
    """Handle health command."""
    path = args.path
    if not os.path.exists(path):
        print(f"❌ Path not found: {path}")
        return
    
    if not is_git_repo(path):
        print(f"❌ Not a Git repository: {path}")
        return
    
    repo_info = get_repo_info(path)
    health = get_repository_health(path)
    
    print(f"📈 Repository Health Report: {os.path.abspath(path)}")
    print()
    print("📊 Basic Metrics:")
    print(f"- Commits: {repo_info['commit_count']}")
    print(f"- Branches: {repo_info['branch_count']}")
    print(f"- Contributors: {repo_info['contributor_count']}")
    print(f"- First commit: {repo_info['first_commit'] or 'Unknown'}")
    print(f"- Last commit: {repo_info['last_commit'] or 'Unknown'}")
    print()
    
    if health['stale_branches']:
        print("⚠️  Health Issues:")
        print(f"- Stale branches: {len(health['stale_branches'])} branches with no commits in >90 days")
        if health['binary_files'] > 10:
            print(f"- Binary files: {health['binary_files']} binary files (consider Git LFS)")
        if not health['gitignore_present']:
            print("- .gitignore missing")
    else:
        print("✅ No major health issues found")
    
    # Simple recommendations
    print("\n💡 Recommendations:")
    if health['stale_branches']:
        print("1. Clean up stale branches: git branch -d <branch1> <branch2>...")
    if health['binary_files'] > 10:
        print("2. Consider Git LFS for binary files")
    if not health['gitignore_present']:
        print("3. Add a .gitignore file for your project type")
    if repo_info['commit_count'] == 0:
        print("4. Repository has no commits - consider initial commit")

def branches_command(args):
    """Handle branches command."""
    path = args.path
    if not os.path.exists(path):
        print(f"❌ Path not found: {path}")
        return
    
    if not is_git_repo(path):
        print(f"❌ Not a Git repository: {path}")
        return
    
    branches = run_git_command(["branch", "--all", "--format=%(refname:short)|%(committerdate:relative)|%(authorname)"], cwd=path)
    if not branches:
        print("No branches found")
        return
    
    print(f"🌿 Branches in {os.path.abspath(path)}:")
    print("-" * 80)
    for branch_line in branches.split('\n'):
        if '|' not in branch_line:
            continue
        name, date, author = branch_line.split('|', 2)
        print(f"{name:40} {date:20} {author}")

def main():
    parser = argparse.ArgumentParser(description='Git Repository Auditor')
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan repository for security issues and large files')
    scan_parser.add_argument('path', help='Path to Git repository')
    scan_parser.add_argument('--threshold', type=int, default=10, help='Large file threshold in MB (default: 10)')
    scan_parser.add_argument('--json', action='store_true', help='Output JSON')
    scan_parser.set_defaults(func=scan_command)
    
    # Health command
    health_parser = subparsers.add_parser('health', help='Get repository health metrics')
    health_parser.add_argument('path', help='Path to Git repository')
    health_parser.set_defaults(func=health_command)
    
    # Branches command
    branches_parser = subparsers.add_parser('branches', help='List all branches with last commit info')
    branches_parser.add_argument('path', help='Path to Git repository')
    branches_parser.set_defaults(func=branches_command)
    
    # Help command
    help_parser = subparsers.add_parser('help', help='Show help')
    
    args = parser.parse_args()
    
    if args.command == 'help':
        parser.print_help()
        return
    
    args.func(args)

if __name__ == '__main__':
    main()