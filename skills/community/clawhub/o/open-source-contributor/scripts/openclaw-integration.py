#!/usr/bin/env python3
"""
OpenClaw Integration for open-source-contributor skill

Shows how to spawn subagents with specific models via OpenClaw sessions API.
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path

WORKSPACE = Path.home() / '.openclaw' / 'workspace' / 'contrib-scout'

def spawn_subagent(task, model="default", label=None, cwd=None):
    """
    Spawn a subagent via OpenClaw sessions_spawn equivalent.
    
    In actual implementation, this would call:
    sessions_spawn(
        task=task,
        model=model,
        label=label,
        runtime="subagent",
        lightContext=True
    )
    """
    # For now, this shows the structure. Actual implementation
    # requires OpenClaw agent tools.
    
    return {
        "action": "sessions_spawn",
        "task": task,
        "model": model,
        "label": label,
        "runtime": "subagent",
        "lightContext": True,
        "cwd": str(cwd) if cwd else None
    }

def run_contribution_pipeline(config):
    """
    Full pipeline with subagent spawning.
    """
    
    # Step 1: Scout
    print("[1/6] Spawning Scout-Agent...")
    scout_task = """
Find GitHub repositories with good first issues.
Search: topic:"good first issue" stars:<500 language:python
Return 5 candidates with owner/name, issue #, title, description.
Output JSON array sorted by difficulty (1-4).
"""
    scout_job = spawn_subagent(
        task=scout_task,
        model="default",
        label="Contrib-Scout",
        cwd=WORKSPACE
    )
    print(f"Scout job: {json.dumps(scout_job, indent=2)}")
    
    # Step 2: For each candidate, spawn Analyzer
    # This would iterate through scout results
    
    # Step 3: For approved candidates, spawn Coder with qwen3-coder:480b:cloud
    print("\n[3/6] Spawning Coder-Agent (qwen3-coder:480b:cloud)...")
    coder_task = """
You are Coder-Agent using qwen3-coder:480b:cloud.

Read the issue description and repository code.
Write a minimal fix that:
1. Addresses the specific issue
2. Follows existing code style
3. Includes tests if they exist
4. Does NOT touch auth/crypto/security files

Repo: {repo_path}
Issue: {issue_info}

Output: Files modified and diff.
"""
    coder_job = spawn_subagent(
        task=coder_task,
        model="qwen3-coder:480b:cloud",
        label="Contrib-Coder",
        cwd=WORKSPACE / "repos" / "example-repo"
    )
    print(f"Coder job: {json.dumps(coder_job, indent=2)}")
    
    # Step 4: Tester
    print("\n[4/6] Spawning Tester-Agent...")
    tester_job = spawn_subagent(
        task="Run test suite. Report pass/fail. JSON output.",
        model="default",
        label="Contrib-Tester",
        cwd=WORKSPACE / "repos" / "example-repo"
    )
    
    # Step 5: Reviewer
    print("\n[5/6] Spawning Reviewer-Agent...")
    reviewer_job = spawn_subagent(
        task="Pre-flight checklist. Security scan. Approve/reject. JSON output.",
        model="default",
        label="Contrib-Reviewer",
        cwd=WORKSPACE
    )
    
    # Step 6: Submitter
    print("\n[6/6] Spawning Submitter-Agent...")
    submitter_job = spawn_subagent(
        task="Open PR on GitHub. Include AI disclosure in description.",
        model="default",
        label="Contrib-Submitter",
        cwd=WORKSPACE
    )
    
    return {
        "scout": scout_job,
        "coder": coder_job,
        "tester": tester_job,
        "reviewer": reviewer_job,
        "submitter": submitter_job
    }

if __name__ == '__main__':
    print("Open Source Contributor - OpenClaw Integration")
    print("=" * 60)
    print("\nThis shows how subagents would be spawned.")
    print("Actual implementation requires OpenClaw sessions API.\n")
    
    config = {
        "github_token": "${GITHUB_TOKEN}",
        "max_repos": 3,
        "complexity_level": 1
    }
    
    jobs = run_contribution_pipeline(config)
    
    print("\n" + "=" * 60)
    print("Pipeline jobs prepared:")
    for name, job in jobs.items():
        print(f"  - {name}: model={job.get('model', 'default')}")
