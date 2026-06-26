#!/usr/bin/env python3
"""
git-workflows-pro — advanced Git operations as tools
"""

import json
import subprocess
import sys
import os
from pathlib import Path

def run(cmd, cwd=None):
    """Run a command and return (returncode, stdout, stderr)"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return result.returncode, result.stdout, result.stderr

def git_rebase_interactive(base, autosquash=False):
    """Generate interactive rebase todo list without executing"""
    # Check if we're in a git repo
    code, out, err = run("git rev-parse --is-inside-work-tree")
    if code != 0:
        return {"error": "not a git repository"}
    
    # Count commits to rebase
    cmd = f"git rev-list --count {base}..HEAD"
    code, count_out, err = run(cmd)
    if code != 0:
        return {"error": f"invalid base: {base}"}
    
    n = int(count_out.strip())
    # Build the todo list by simulating rebase -i
    # Get commit hashes and messages for last n commits
    cmd = f"git log --oneline --no-decorate HEAD~{n}..HEAD"
    code, log_out, err = run(cmd)
    if code != 0:
        return {"error": "failed to get commit history"}
    
    commits = []
    for i, line in enumerate(log_out.strip().split("\n"), 1):
        if line:
            parts = line.split(" ", 1)
            if len(parts) == 2:
                commit_hash, message = parts
                commits.append({"order": i, "hash": commit_hash, "message": message})
    
    # Build todo instructions
    instructions = """Interactive rebase instructions:

Commands:
  p, pick = use commit as-is
  r, reword = use commit, but edit the message
  e, edit = use commit, but stop for amending
  s, squash = use commit, but meld into previous commit
  f, fixup = like "squash", but discard this commit's message
  d, drop = remove commit

Lines starting with # are comments.

To start the rebase, run:
  git rebase -i {base}

After editing the todo list, save and close. Git will then replay commits.

Abort at any time with: git rebase --abort
Continue after making changes: git rebase --continue
""".format(base=base)
    
    return {
        "base": base,
        "commits": commits,
        "instructions": instructions,
        "autosquash_note": "Use --autosquash to automatically squash fixup/squash commits" if autosquash else ""
    }

def git_worktree_add(branch, path):
    """Create a new worktree for given branch"""
    # Ensure path is absolute or relative to cwd
    path_obj = Path(path)
    if not path_obj.is_absolute():
        path_obj = Path.cwd() / path
    
    # Create parent dirs
    path_obj.parent.mkdir(parents=True, exist_ok=True)
    
    # Check if branch exists; if not, create from HEAD
    code, out, err = run(f"git show-ref --verify refs/heads/{branch}")
    if code != 0:
        # Branch doesn't exist; create it from HEAD
        code, out, err = run(f"git branch {branch}")
        if code != 0:
            return {"error": f"failed to create branch {branch}: {err}"}
    
    # Add worktree
    code, out, err = run(f"git worktree add {path} {branch}")
    if code != 0:
        return {"error": f"git worktree add failed: {err}"}
    
    return {"success": True, "path": str(path_obj), "branch": branch}

def git_reflog_recover(action, commit_hash=None, target_branch=None):
    """List reflog or restore a commit"""
    if action == "list":
        code, out, err = run("git reflog --date=iso")
        if code != 0:
            return {"error": "failed to read reflog"}
        entries = []
        for line in out.strip().split("\n"):
            if line:
                # Format: <hash> <date> <message>
                parts = line.split(" ", 2)
                if len(parts) >= 3:
                    entries.append({"hash": parts[0], "date": parts[1], "message": parts[2]})
        return {"entries": entries}
    elif action == "restore":
        if not commit_hash or not target_branch:
            return {"error": "commit_hash and target_branch required for restore"}
        # Check if commit exists
        code, out, err = run(f"git cat-file -t {commit_hash}")
        if code != 0:
            return {"error": f"commit {commit_hash} not found"}
        # Create or update branch at that commit
        code, out, err = run(f"git branch -f {target_branch} {commit_hash}")
        if code != 0:
            return {"error": f"failed to create/update branch: {err}"}
        return {"success": True, "branch": target_branch, "commit": commit_hash}
    else:
        return {"error": "invalid action"}

def git_subtree_add(repo_url, prefix, branch="main"):
    """Add a subtree"""
    # Ensure we're in a git repo
    code, out, err = run("git rev-parse --is-inside-work-tree")
    if code != 0:
        return {"error": "not a git repository"}
    
    # Add remote temporarily: subtree-temp-remote
    remote_name = "subtree-temp-remote"
    run(f"git remote remove {remote_name}")  # clean up if exists
    code, out, err = run(f"git remote add {remote_name} {repo_url}")
    if code != 0:
        return {"error": f"failed to add remote: {err}"}
    
    # Fetch
    code, out, err = run(f"git fetch {remote_name} {branch}")
    if code != 0:
        return {"error": f"failed to fetch: {err}"}
    
    # Add subtree
    code, out, err = run(f"git subtree add --prefix={prefix} {remote_name}/{branch} --squash")
    if code != 0:
        # Cleanup remote
        run(f"git remote remove {remote_name}")
        return {"error": f"subtree add failed: {err}"}
    
    # Cleanup remote
    run(f"git remote remove {remote_name}")
    return {"success": True, "prefix": prefix, "repo": repo_url, "branch": branch}

def git_pr_create(title, body, head, base="main", draft=False):
    """Create PR using gh CLI"""
    # Check gh installed
    code, out, err = run("which gh")
    if code != 0:
        return {"error": "gh CLI not installed. Install from https://cli.github.com"}
    
    # Ensure we're in a git repo with remote
    code, out, err = run("git rev-parse --is-inside-work-tree")
    if code != 0:
        return {"error": "not a git repository"}
    
    # Build gh command
    cmd = f'gh pr create --head {head} --base {base} --title "{title}" --body "{body}"'
    if draft:
        cmd += " --draft"
    
    code, out, err = run(cmd)
    if code != 0:
        return {"error": f"gh pr create failed: {err}"}
    
    # Output contains URL and number
    return {"success": True, "output": out.strip(), "url": out.strip().split()[-1] if out.strip() else ""}

def git_changelog_generate(from_tag=None, to_tag=None, output_format="markdown"):
    """Generate changelog between tags or from last tag to HEAD"""
    # If from_tag and to_tag not provided, use last tag to HEAD
    if not from_tag:
        code, out, err = run("git describe --tags --abbrev=0")
        if code != 0:
            return {"error": "no tags found, specify from_tag"}
        from_tag = out.strip()
    
    ref_spec = f"{from_tag}..{to_tag}" if to_tag else f"{from_tag}..HEAD"
    
    # Get commits
    code, out, err = run(f'git log {ref_spec} --pretty=format:"%h %s"')
    if code != 0:
        return {"error": f"failed to get commits: {err}"}
    
    commits = []
    for line in out.strip().split("\n"):
        if line:
            parts = line.split(" ", 1)
            if len(parts) == 2:
                commits.append({"hash": parts[0], "message": parts[1]})
    
    if output_format == "json":
        return {"from": from_tag, "to": to_tag or "HEAD", "commits": commits}
    
    # Markdown format with grouping by conventional commit types
    lines = [f"# Changelog ({from_tag} → {to_tag or 'HEAD'})", ""]
    categories = {"feat": [], "fix": [], "breaking": [], "other": []}
    for c in commits:
        msg = c["message"]
        if msg.startswith("feat:"):
            categories["feat"].append(f"- {msg[5:].strip()} ({c['hash']})")
        elif msg.startswith("fix:"):
            categories["fix"].append(f"- {msg[4:].strip()} ({c['hash']})")
        elif "breaking" in msg.lower() or "!" in msg.split(":")[0]:
            categories["breaking"].append(f"- {msg} ({c['hash']})")
        else:
            categories["other"].append(f"- {msg} ({c['hash']})")
    
    for cat, entries in categories.items():
        if entries:
            lines.append(f"## {cat.title()}")
            lines.extend(entries)
            lines.append("")
    
    return {"markdown": "\n".join(lines)}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "usage: run.py tool-call <tool_name> <json_input>"}))
        sys.exit(1)
    
    action = sys.argv[1]
    args = sys.argv[2:]
    
    if action != "tool-call" or len(args) < 2:
        print(json.dumps({"error": "expected: tool-call <tool> <json>"}))
        sys.exit(1)
    
    tool = args[0]
    try:
        input_data = json.loads(args[1])
    except json.JSONDecodeError:
        print(json.dumps({"error": "invalid JSON input"}))
        sys.exit(1)
    
    result = None
    
    if tool == "git_rebase_interactive":
        result = git_rebase_interactive(input_data["base"], input_data.get("autosquash", False))
    elif tool == "git_worktree_add":
        result = git_worktree_add(input_data["branch"], input_data["path"])
    elif tool == "git_reflog_recover":
        result = git_reflog_recover(input_data["action"], input_data.get("commit_hash"), input_data.get("target_branch"))
    elif tool == "git_subtree_add":
        result = git_subtree_add(input_data["repo_url"], input_data["prefix"], input_data.get("branch", "main"))
    elif tool == "git_pr_create":
        required = ["title", "body", "head"]
        if not all(k in input_data for k in required):
            result = {"error": f"missing required fields: {required}"}
        else:
            result = git_pr_create(input_data["title"], input_data["body"], input_data["head"], input_data.get("base", "main"), input_data.get("draft", False))
    elif tool == "git_changelog_generate":
        result = git_changelog_generate(input_data.get("from_tag"), input_data.get("to_tag"), input_data.get("output_format", "markdown"))
    else:
        result = {"error": f"unknown tool: {tool}"}
    
    print(json.dumps(result))
    sys.exit(0 if (isinstance(result, dict) and "error" not in result) else 1)

if __name__ == "__main__":
    main()
