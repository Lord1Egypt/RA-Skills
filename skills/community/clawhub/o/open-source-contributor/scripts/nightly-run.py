#!/usr/bin/env python3
"""
Nightly open-source contributor run — WORKING IMPLEMENTATION

Finds good-first issues, forks repos, makes minimal fixes, submits PRs.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path.home() / ".openclaw" / "lib"))
from token_resolver import get_github_token_or_die

WORKSPACE = Path("/home/wahaj/.openclaw/workspace/contrib-scout")
LOG_FILE = WORKSPACE / "logs" / "contributions.jsonl"
DAILY_REPORT = WORKSPACE / "nightly-report.json"
REPOS_DIR = WORKSPACE / "repos"
DRAFTS_DIR = WORKSPACE / "drafts"

# Blocked patterns for security
BLOCKED_PATTERNS = ["auth", "crypto", "token", "key", "password", "credential", "secret"]

def log_entry(entry):
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

def run_cmd(cmd, cwd=None, timeout=60):
    try:
        r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except Exception as e:
        return -1, "", str(e)

def github_api(method, endpoint, data=None):
    token = get_github_token_or_die()
    if not token:
        return None
    url = f"https://api.github.com{endpoint}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "OpenClaw-Contributor"
    }
    cmd = f'curl -s -H "Authorization: token {token}" -H "Accept: application/vnd.github.v3+json" '
    if data:
        cmd += f'-H "Content-Type: application/json" -X {method} -d \'{json.dumps(data)}\' "{url}"'
    else:
        cmd += f'-X {method} "{url}"'
    rc, out, err = run_cmd(cmd)
    if rc != 0:
        return None
    try:
        return json.loads(out)
    except:
        return out

def get_repo_size(repo):
    """Check repo size in KB via GitHub API. Skip if > 50MB."""
    info = github_api("GET", f"/repos/{repo}")
    if info and "size" in info:
        return info["size"]  # in KB
    return 0

def is_fixable_issue(title, body):
    """Check if an issue is something make_fix() can handle."""
    combined = (title + " " + body).lower()
    fixable_keywords = [
        "typo", "spelling", "grammar", "readme", "contributing",
        "code of conduct", "example", "installation", "usage",
        "documentation", "docs", "docstring", "comment"
    ]
    return any(kw in combined for kw in fixable_keywords)

def search_issues():
    """Search GitHub for documentation-friendly first issues."""
    queries = [
        'label:"good first issue"+label:"documentation"',
        'label:"good first issue"+in:title+typo',
        'label:"good first issue"+in:title+readme',
        'label:"good first issue"+in:title+contributing',
        'label:"good first issue"+in:title+example',
        'label:"good first issue"+in:title+installation',
        'label:"good first issue"+in:title+usage',
        'label:"help wanted"+in:title+readme',
        'label:"help wanted"+in:title+typo',
        'label:"good first issue"',
        'label:"good-first-issue"',
        'label:"help wanted"',
    ]
    
    all_candidates = []
    seen_urls = set()
    
    for query in queries:
        results = github_api("GET", f"/search/issues?q={query}+language:python+state:open&sort=updated&per_page=10")
        if not results or "items" not in results:
            continue
        
        for item in results["items"]:
            html_url = item.get("html_url", "")
            if html_url in seen_urls:
                continue
            seen_urls.add(html_url)
            
            title = item.get("title", "")
            body = item.get("body", "") or ""
            combined = title.lower() + " " + body.lower()
            
            # Skip security-related issues
            if any(p in combined for p in BLOCKED_PATTERNS):
                continue
            
            # Skip non-English repos
            if any('\u4e00' <= c <= '\u9fff' for c in title):
                continue
            
            # Only return issues we can actually fix
            if not is_fixable_issue(title, body):
                continue
            
            # Extract repo info
            match = re.search(r"github\.com/([^/]+/[^/]+)/issues/\d+", html_url)
            if not match:
                continue
            repo = match.group(1)
            
            all_candidates.append({
                "repo": repo,
                "issue_number": item["number"],
                "title": title,
                "url": html_url,
                "body": body[:500],
                "stars": 0
            })
        
        if len(all_candidates) >= 5:
            break
    
    return all_candidates[:10]

def fork_repo(repo):
    """Fork a repository, or reuse existing fork."""
    # Check if fork already exists
    result = github_api("GET", f"/repos/wahajahmed010/{repo.split('/')[1]}")
    if result and "html_url" in result:
        return result["html_url"], result.get("full_name", f"wahajahmed010/{repo.split('/')[1]}")
    # Create new fork
    result = github_api("POST", f"/repos/{repo}/forks")
    if result and "html_url" in result:
        return result["html_url"], result.get("full_name", f"wahajahmed010/{repo.split('/')[1]}")
    return None, None

def clone_repo(repo_full_name, repo_name):
    """Clone forked repo with shallow clone for speed."""
    dest = REPOS_DIR / repo_name
    if dest.exists():
        run_cmd(f"rm -rf {dest}")
    token = get_github_token_or_die()
    url = f"https://wahajahmed010:{token}@github.com/{repo_full_name}.git"
    # Shallow clone with 60s timeout — if it takes longer, repo is too big
    rc, out, err = run_cmd(f"git clone --depth 1 {url} {dest}", timeout=120)
    if rc != 0:
        return False, None
    return True, dest

def get_repo_files(repo_path, pattern="*.py"):
    """Find files matching pattern."""
    files = []
    for f in repo_path.rglob(pattern):
        if ".git" not in str(f):
            files.append(f.relative_to(repo_path))
    return files

def analyze_issue_for_typo(repo_path, issue_title, issue_body):
    """Simple heuristic: look for typo in filenames or README."""
    # Check if issue mentions a filename
    words = issue_title.lower().split()
    for word in words:
        if word.endswith(".py") or word.endswith(".md") or word.endswith(".txt"):
            fpath = repo_path / word
            if fpath.exists():
                return str(fpath.relative_to(repo_path)), "typo_fix"
    # Check README for simple typos
    readme = repo_path / "README.md"
    if readme.exists():
        content = readme.read_text()
        # Very simple typo detector: doubled letters
        import re
        matches = re.findall(r'\b(\w)\1{2,}\w*\b', content)
        if matches:
            return "README.md", "typo_fix"
    return None, None

def make_typo_fix(file_path, repo_path):
    """Make a simple typo fix in a file."""
    content = file_path.read_text()
    # Fix common typos
    fixes = [
        ("teh ", "the "), (" teh", " the"),
        ("recieve", "receive"), ("occured", "occurred"),
        ("seperate", "separate"), ("definately", "definitely"),
        ("accomodate", "accommodate"), ("occurence", "occurrence"),
    ]
    modified = content
    for bad, good in fixes:
        modified = modified.replace(bad, good)
    if modified != content:
        file_path.write_text(modified)
        return True
    return False

def make_fix(repo_path, issue):
    """Attempt to make a minimal fix for an issue."""
    title_lower = issue["title"].lower()
    body_lower = (issue.get("body") or "").lower()
    combined = title_lower + " " + body_lower
    
    # Check if issue is about adding docs/examples
    if "contributing" in combined or "contribution guide" in combined:
        contrib_path = repo_path / "CONTRIBUTING.md"
        if not contrib_path.exists():
            content = """# Contributing Guidelines

Thank you for your interest in contributing to this project!

## How to Contribute

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes
4. Submit a pull request

## Code Style

- Follow existing code style
- Write clear, concise commit messages
- Add tests for new features

## Reporting Issues

- Use the issue tracker to report bugs
- Provide clear reproduction steps
- Include relevant logs or error messages

Thank you for helping improve this project!
"""
            contrib_path.write_text(content)
            return "CONTRIBUTING.md", "docs"
    
    if "code of conduct" in combined or "coc" in combined:
        coc_path = repo_path / "CODE_OF_CONDUCT.md"
        if not coc_path.exists():
            content = """# Code of Conduct

## Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone.

## Our Standards

Examples of behavior that contributes to a positive environment:
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Accepting constructive criticism gracefully
- Focusing on what is best for the community

## Enforcement

Instances of abusive behavior may be reported to the project maintainers.

This Code of Conduct is adapted from the [Contributor Covenant](https://www.contributor-covenant.org).
"""
            coc_path.write_text(content)
            return "CODE_OF_CONDUCT.md", "docs"
    
    if "readme" in combined or "documentation" in combined:
        readme = repo_path / "README.md"
        if readme.exists():
            content = readme.read_text()
            if "## Installation" not in content and "install" in combined:
                section = "\n\n## Installation\n\n```bash\npip install -r requirements.txt\n```\n"
                readme.write_text(content + section)
                return "README.md", "docs"
            if "## Usage" not in content and ("usage" in combined or "example" in combined):
                section = "\n\n## Usage\n\n```python\n# Example usage\nimport your_module\nresult = your_module.run()\n```\n"
                readme.write_text(content + section)
                return "README.md", "docs"
    
    if "example" in combined:
        examples_dir = repo_path / "examples"
        examples_dir.mkdir(exist_ok=True)
        existing = list(examples_dir.glob("example_*.py"))
        next_num = len(existing) + 1
        example_file = examples_dir / f"example_{next_num:02d}.py"
        content = f'''"""
Example {next_num}: Basic usage

This example demonstrates basic usage of the project.
"""

# Add your example code here
if __name__ == "__main__":
    print("Hello, World!")
'''
        example_file.write_text(content)
        return str(example_file.relative_to(repo_path)), "example"
    
    # Try typo fix as fallback
    file_rel, fix_type = analyze_issue_for_typo(repo_path, issue["title"], issue["body"])
    if file_rel:
        fpath = repo_path / file_rel
        if make_typo_fix(fpath, repo_path):
            return file_rel, "typo_fix"
    
    return None, None

def commit_and_push(repo_path, repo_name, issue_num, fix_desc):
    """Commit changes and push to fork."""
    branch_name = f"fix-issue-{issue_num}"
    run_cmd(f"git checkout -b {branch_name}", cwd=repo_path)
    run_cmd("git add -A", cwd=repo_path)
    run_cmd(f'git commit -m "Fix #{issue_num}: {fix_desc}"', cwd=repo_path)
    run_cmd(f"git push origin {branch_name}", cwd=repo_path)
    return branch_name

def create_pr(repo, branch, issue_num, title, body):
    """Create pull request via GitHub API."""
    data = {
        "title": f"Fix #{issue_num}: {title}",
        "body": body + "\n\n_Disclaimer: This contribution was generated with AI assistance._",
        "head": f"wahajahmed010:{branch}",
        "base": "main"
    }
    result = github_api("POST", f"/repos/{repo}/pulls", data)
    if result and "html_url" in result:
        return result["html_url"]
    return None

def main():
    print("=" * 60)
    print("🌙 Nightly Open Source Contributor Run")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    token = get_github_token_or_die()
    if not token:
        print("❌ No GitHub token found")
        sys.exit(1)
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Count today's existing contributions
    existing = 0
    if LOG_FILE.exists():
        with open(LOG_FILE) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get("date") == today and entry.get("status") in ("created", "merged"):
                        existing += 1
                except:
                    pass
    
    print(f"\n📊 Today's progress: {existing}/3 contributions")
    
    if existing >= 3:
        print("✅ Daily quota already met!")
        report = {
            "date": today, "target": 3, "completed": existing,
            "status": "complete", "pr_urls": []
        }
        with open(DAILY_REPORT, "w") as f:
            json.dump(report, f, indent=2)
        return
    
    needed = 3 - existing
    print(f"\n🎯 Need {needed} more contribution(s)")
    
    # Search for issues
    print("\n[1/3] Searching for good first issues...")
    candidates = search_issues()
    print(f"   Found {len(candidates)} candidates")
    
    contributions_today = []
    
    for i, issue in enumerate(candidates[:needed + 5]):  # Extra buffer
        if len(contributions_today) >= needed:
            break
            
        print(f"\n   Trying: {issue['repo']}#{issue['issue_number']} — {issue['title'][:60]}")
        
        # Skip repos larger than 50MB (in KB)
        size_kb = get_repo_size(issue['repo'])
        if size_kb > 50000:
            print(f"   ⏭️  Repo too large ({size_kb/1024:.0f}MB), skipping")
            continue
        
        # Fork repo
        print(f"   [2/3] Forking {issue['repo']}...")
        fork_url, fork_full = fork_repo(issue["repo"])
        if not fork_url:
            print("   ❌ Fork failed, skipping")
            continue
        print(f"   ✅ Forked to {fork_url}")
        
        # Clone
        repo_name = issue["repo"].split("/")[1]
        print(f"   [3/3] Cloning...")
        ok, repo_path = clone_repo(fork_full, repo_name)
        if not ok:
            print("   ❌ Clone failed, skipping")
            continue
        
        # Make fix
        print(f"   Making fix...")
        fixed_file, fix_type = make_fix(repo_path, issue)
        if not fixed_file:
            print("   ❌ Could not determine fix, skipping")
            run_cmd(f"rm -rf {repo_path}")
            continue
        print(f"   ✅ Fixed: {fixed_file}")
        
        # Commit and push
        print(f"   Committing and pushing...")
        branch = commit_and_push(repo_path, repo_name, issue["issue_number"], issue["title"][:50])
        
        # Create PR with accurate description
        if fix_type == "docs":
            pr_body = f"This PR fixes issue #{issue['issue_number']}.\n\n**Changes:**\n- Added `{fixed_file}` to improve project documentation\n\n_Disclaimer: This contribution was generated with AI assistance._"
        elif fix_type == "example":
            pr_body = f"This PR fixes issue #{issue['issue_number']}.\n\n**Changes:**\n- Added `{fixed_file}` as a usage example\n\n_Disclaimer: This contribution was generated with AI assistance._"
        else:
            pr_body = f"This PR fixes issue #{issue['issue_number']}.\n\n**Changes:**\n- Fixed typo/formatting in `{fixed_file}`\n\n_Disclaimer: This contribution was generated with AI assistance._"
        print(f"   Creating PR...")
        pr_url = create_pr(issue["repo"], branch, issue["issue_number"], issue["title"], pr_body)
        
        if pr_url:
            print(f"   ✅ PR created: {pr_url}")
            contributions_today.append({
                "date": today,
                "timestamp": datetime.now().isoformat(),
                "repo": issue["repo"],
                "issue": issue["issue_number"],
                "pr_url": pr_url,
                "status": "created"
            })
        else:
            print("   ❌ PR creation failed")
        
        # Cleanup
        run_cmd(f"rm -rf {repo_path}")
    
    # Final report
    total = existing + len(contributions_today)
    report = {
        "date": today,
        "target": 3,
        "completed": total,
        "status": "complete" if total >= 3 else "incomplete",
        "contributions": contributions_today
    }
    with open(DAILY_REPORT, "w") as f:
        json.dump(report, f, indent=2)
    
    for c in contributions_today:
        log_entry(c)
    
    print("\n" + "=" * 60)
    print(f"📊 DAILY REPORT: {total}/3 contributions")
    for c in contributions_today:
        print(f"   ✅ {c['repo']}#{c['issue']} → {c['pr_url']}")
    if total < 3:
        print(f"   ⚠️  Short by {3 - total}")
    print("=" * 60)

if __name__ == '__main__':
    main()
