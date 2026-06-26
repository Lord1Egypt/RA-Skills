#!/usr/bin/env python3
"""
Open Source Contributor Pipeline

Subagent workflow for autonomous GitHub contributions.
Uses qwen3-coder:480b:cloud for the Coder subagent.
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Configuration
WORKSPACE = Path.home() / '.openclaw' / 'workspace' / 'contrib-scout'
LOGS_DIR = WORKSPACE / 'logs'
DRAFTS_DIR = WORKSPACE / 'drafts'
REPOS_DIR = WORKSPACE / 'repos'
CONFIG_FILE = WORKSPACE / 'config.json'
TRACKING_FILE = WORKSPACE / 'approval-tracking.json'

def ensure_dirs():
    """Create required directories"""
    for d in [WORKSPACE, LOGS_DIR, DRAFTS_DIR, REPOS_DIR]:
        d.mkdir(parents=True, exist_ok=True)

def log_activity(activity_type, data):
    """Append-only logging"""
    timestamp = datetime.now().isoformat()
    entry = {"time": timestamp, "type": activity_type, "data": data}
    with open(LOGS_DIR / 'contributions.jsonl', 'a') as f:
        f.write(json.dumps(entry) + '\n')

def load_config():
    """Load user configuration"""
    default_config = {
        "github_token": os.environ.get('GITHUB_TOKEN', ''),
        "max_repos_per_night": 3,
        "complexity_level": 1,
        "approval_threshold": 0.5,
        "quiet_hours": {"start": "23:00", "end": "07:00"},
        "blocked_patterns": ["auth", "crypto", "token", "key", "password", "credential", "secret"]
    }
    
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return {**default_config, **json.load(f)}
    return default_config

def get_approval_stats():
    """Calculate approval rate from tracking file"""
    if not TRACKING_FILE.exists():
        return {"total": 0, "approved": 0, "rejected": 0, "rate": 1.0}
    
    with open(TRACKING_FILE) as f:
        entries = [json.loads(line) for line in f]
    
    total = len(entries)
    approved = sum(1 for e in entries if e.get('status') == 'approved')
    rejected = sum(1 for e in entries if e.get('status') == 'rejected')
    
    rate = approved / total if total > 0 else 1.0
    return {"total": total, "approved": approved, "rejected": rejected, "rate": rate}

def check_can_proceed(config):
    """Check if we should proceed based on rejection rate"""
    stats = get_approval_stats()
    if stats['rate'] < 0.3 and stats['total'] > 5:
        print(f"AUTO-PAUSE: Rejection rate {stats['rate']:.0%} > 30%")
        return False
    return True

def get_max_repos_for_level(level, stats):
    """Determine max repos based on complexity level and approval rate"""
    limits = {
        1: 3,  # Typo fixes - no approval needed
        2: 3 if stats['rate'] > 0.5 else 0,
        3: 2 if stats['rate'] > 0.7 else 0,
        4: 1 if stats['rate'] > 0.9 else 0
    }
    return limits.get(level, 0)

def spawn_scout_agent(config):
    """Spawn Scout agent to find candidates"""
    task = f"""
You are Scout-Agent. Find GitHub repositories with good first issues.

**Search criteria:**
- Topic: "good first issue" OR "help wanted"
- Stars: < 500
- Language: Python, JavaScript, or Go (start with Python)
- Last activity: within 30 days
- Max candidates: 5

**For each candidate, extract:**
1. Repo: owner/name
2. Issue # and title
3. Issue description
4. Difficulty estimate (1-4)
5. Is scope clear? (yes/no)

**Output:** JSON array of candidates sorted by difficulty ascending.

**Skip if:**
- Issue mentions auth, crypto, tokens, keys, passwords
- Description is vague or incomplete
- No clear acceptance criteria
"""
    
    # Write task to temp file for subagent
    task_file = DRAFTS_DIR / f'scout-task-{datetime.now().strftime("%Y%m%d-%H%M%S")}.txt'
    with open(task_file, 'w') as f:
        f.write(task)
    
    print(f"Scout task prepared: {task_file}")
    return task_file

def spawn_analyzer_agent(repo_info, issue_info):
    """Spawn Analyzer agent to understand scope"""
    task = f"""
You are Analyzer-Agent. Determine if you fully understand this issue.

**Repo:** {repo_info}
**Issue:** {issue_info}

**Produce Understanding Checklist:**
1. What is the bug/feature request? (1 sentence)
2. What file(s) likely need changes?
3. What is the expected behavior?
4. What could go wrong with a fix?
5. Are there existing tests for this area?

**Complexity Assessment:**
- Level 1: Typo, link fix
- Level 2: README, docs
- Level 3: Simple code (1-2 functions)
- Level 4: Moderate code (multiple files, logic changes)

**Output:** JSON with {{
    "understood": true/false,
    "level": 1-4,
    "checklist": {{...}},
    "confidence": 0.0-1.0
}}

If confidence < 0.8 or scope unclear, set understood=false.
"""
    return task

def spawn_coder_agent(repo_path, issue_info, understanding):
    """Spawn Coder agent with qwen3-coder:480b:cloud model"""
    task = f"""
You are Coder-Agent. Write a fix for this issue.

**Repo location:** {repo_path}
**Issue:** {issue_info}
**Understanding:** {understanding}

**Your task:**
1. Read the relevant file(s)
2. Understand the existing code style
3. Write a minimal fix that addresses the issue
4. Ensure the fix follows existing patterns

**Constraints:**
- Only modify files directly related to the issue
- Do NOT touch: auth, crypto, security, config files with secrets
- Write clear, simple code
- Add/update tests if they exist

**Output:**
- Files modified
- Diff of changes
- Explanation of fix
"""
    
    # Note: This requires spawning via OpenClaw with specific model
    return {
        "task": task,
        "model": "qwen3-coder:480b:cloud",
        "workspace": str(repo_path)
    }

def spawn_tester_agent(repo_path):
    """Spawn Tester agent to validate fix"""
    task = f"""
You are Tester-Agent. Run the test suite for this repository.

**Repo:** {repo_path}

**Tasks:**
1. Check if repo has a test suite (pytest, npm test, go test, etc.)
2. Run the tests
3. Report: tests passed/failed/skipped
4. If tests fail, analyze if failures are related to the fix or pre-existing

**Output:** JSON with {{
    "has_tests": true/false,
    "tests_passed": N,
    "tests_failed": N,
    "relevant_failures": [list],
    "can_proceed": true/false
}}

If no test suite exists, set has_tests=false and can_proceed=true with a warning.
"""
    return task

def spawn_reviewer_agent(repo_path, diff, issue_info):
    """Spawn Reviewer agent for pre-flight checklist"""
    task = f"""
You are Reviewer-Agent. Final review before PR submission.

**Repo:** {repo_path}
**Issue:** {issue_info}
**Proposed changes:** {diff}

**Checklist:**
- [ ] No auth/crypto/secret files modified
- [ ] Changes are minimal and focused
- [ ] Code follows repo style
- [ ] No obvious bugs introduced
- [ ] AI assistance will be disclosed in PR

**Security check:** Scan file paths for: auth, crypto, token, key, password, credential, secret

**Output:** JSON with {{
    "approved": true/false,
    "blockers": [list of issues],
    "suggestions": [optional improvements]
}}
"""
    return task

def main():
    """Main entry point"""
    ensure_dirs()
    config = load_config()
    
    print("=" * 60)
    print("Open Source Contributor Pipeline")
    print("=" * 60)
    
    # Check if we should proceed
    if not check_can_proceed(config):
        print("Pipeline paused due to high rejection rate.")
        print("Review recent contributions and adjust approach.")
        sys.exit(0)
    
    # Get approval stats
    stats = get_approval_stats()
    max_repos = get_max_repos_for_level(config['complexity_level'], stats)
    
    print(f"\nCurrent level: {config['complexity_level']}")
    print(f"Approval rate: {stats['rate']:.0%} ({stats['approved']}/{stats['total']})")
    print(f"Max repos tonight: {max_repos}")
    
    if max_repos == 0:
        print("\nApproval rate too low for current complexity level.")
        print("Contributions paused until approval rate improves.")
        sys.exit(0)
    
    # Phase 1: Scout for candidates
    print("\n[1/6] Scouting for repositories...")
    scout_task = spawn_scout_agent(config)
    print(f"Scout task ready. Run subagent with task file.")
    
    # TODO: Implement actual subagent spawning via OpenClaw
    print("\nNote: Subagent spawning requires OpenClaw integration.")
    print("This script provides the task definitions.")
    print("\nNext steps:")
    print("1. Run Scout agent to find candidates")
    print("2. For each candidate, run Analyzer")
    print("3. For approved candidates, run Coder (qwen3-coder:480b:cloud)")
    print("4. Run Tester, Reviewer, then Submitter")
    
    log_activity("pipeline_start", {
        "level": config['complexity_level'],
        "max_repos": max_repos,
        "approval_rate": stats['rate']
    })

if __name__ == '__main__':
    main()
