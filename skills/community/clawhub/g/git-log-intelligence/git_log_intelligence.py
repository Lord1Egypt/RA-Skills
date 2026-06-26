import subprocess
import json
import re
import os
import argparse
import sys
from datetime import datetime, timedelta

CONFIG_PATH = os.path.join(os.path.dirname(__file__), ".config", "git_filters.json")
MAX_MSG_LEN = 1000  # Character limit per commit for the LLM context
MAX_LINES = 200  # Max number of commits to include in summary (after filtering)

def parse_paginated_json_array(raw_output):
    """Parse one or more concatenated JSON values and merge arrays into a list."""
    decoder = json.JSONDecoder()
    idx = 0
    length = len(raw_output)
    merged = []

    while idx < length:
        # Skip inter-page whitespace/newlines between concatenated JSON values.
        while idx < length and raw_output[idx].isspace():
            idx += 1

        if idx >= length:
            break

        value, next_idx = decoder.raw_decode(raw_output, idx)
        if isinstance(value, list):
            merged.extend(value)
        else:
            raise ValueError("Expected a JSON array from gh api commits endpoint")
        idx = next_idx

    return merged

def load_filters():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r') as f:
                return json.load(f).get("ignore_patterns", [])
        except Exception as e:
            print(f"Warning: Failed to load filters from {CONFIG_PATH}: {e}", file=sys.stderr)
            return []
    return ["^chore", "^docs", "Merge branch"]

def save_filter(pattern):
    filters = set(load_filters())
    filters.add(pattern)
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        json.dump({"ignore_patterns": list(filters)}, f, indent=2)
    print(f"✅ Memorized new ignore pattern: {pattern}")

def show_filters():
    filters = load_filters()
    if filters:
        print("Current ignore patterns:")
        for f in filters:
            print(f"- {f}")
    else:
        print("No ignore patterns set.")

def remove_filter(pattern):
    filters = set(load_filters())
    if pattern in filters:
        filters.remove(pattern)
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, 'w') as f:
            json.dump({"ignore_patterns": list(filters)}, f, indent=2)
        print(f"✅ Removed ignore pattern: {pattern}")
    else:
        print(f"Pattern not found: {pattern}")

def get_summary(repo, days, full_context=False, verbose=False):
    filters = load_filters()
    since_date = (datetime.now() - timedelta(days=int(days))).isoformat(timespec="seconds") + "Z"
    
    # Authenticate gh strictly via OpenClaw's token convention.
    env = os.environ.copy()
    token = env.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not token:
        return "Error: GITHUB_PERSONAL_ACCESS_TOKEN is required for GitHub API access."
    # GH CLI uses GH_TOKEN for authentication, so we set it here to ensure it works in subprocess calls.
    env["GH_TOKEN"] = token
    
    # Fetching commits via GH API
    cmd = ["gh", "api", f"repos/{repo}/commits?since={since_date}", "--paginate"]
    if verbose:
        print(f"Running command: {' '.join(cmd)}")
        print(f"Using filters: {filters}")

    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    
    if result.returncode != 0:
        return f"Error: {result.stderr}"

    try:
        commits = parse_paginated_json_array(result.stdout)
    except (json.JSONDecodeError, ValueError) as e:
        return f"Error parsing GitHub API response: {e}"

    important = []
    filtered_out = 0
    capped_out = 0

    for c in commits:
        full_msg = c['commit']['message']
        subject = full_msg.split('\n')[0]
        
        # 1. Filter based on subject line
        if any(re.search(p, subject, re.IGNORECASE) for p in filters):
            filtered_out += 1
            continue
        
        # 2. Collect data based on flag
        sha = c['sha'][:7]
        author = c['commit']['author']['name']
        
        if len(important) >= MAX_LINES:
            capped_out += 1
            continue
        
        if full_context:
            # Truncate long messages to protect the agent's context window
            content = (full_msg[:MAX_MSG_LEN] + '...') if len(full_msg) > MAX_MSG_LEN else full_msg
            important.append(f"COMMIT: {sha}\nAUTHOR: {author}\nMESSAGE:\n{content}\n{'-'*20}")
        else:
            important.append(f"- {sha}: {subject} ({author})")

    header = f"### Summary for {repo}.\n\n"
    warning = ""
    if capped_out > 0:
        warning = (
            f"\n\nWARNING: Output capped at MAX_LINES={MAX_LINES}. "
            f"{capped_out} additional non-filtered commits are not shown."
        )
    footer = (
        f"\n\n*Displayed {len(important)}/{len(commits)} commits "
        f"(filtered: {filtered_out}, capped by MAX_LINES: {capped_out}).*"
    )
    return header + "\n".join(important) + warning + footer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Git Log Intelligence Tool - Summarize recent commits with filtering capabilities")
    parser.add_argument("action", choices=["summarize", "ignore", "show", "remove"], help="Action to perform")
    parser.add_argument("target", nargs="?", help="Repo (owner/repo) or Regex Pattern for ignore")
    parser.add_argument("days", nargs="?", default=7, type=int, help="Days to look back")
    parser.add_argument("--full", action="store_true", help="Include full commit bodies (truncated)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output for debugging")

    args = parser.parse_args()

    if args.action == "ignore":
        save_filter(args.target)
    elif args.action == "show":
        show_filters()
    elif args.action == "remove":
        remove_filter(args.target)
    else:
        if not args.target:
            print("Error: Repository target is required for summarization (e.g., 'owner/repo').")
        else:
            print(get_summary(args.target, args.days, args.full, args.verbose))