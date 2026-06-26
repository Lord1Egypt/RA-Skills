#!/usr/bin/env python3
"""
Ghostclaw Compare — show a table of current vs previous vibe scores.

Usage:
  ghostclaw-compare --repos-file repos.txt [--cache-file ~/.cache/ghostclaw/vibe_history.json]
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List

# Ensure root directory is in sys.path
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from ghostclaw.lib.cache import VibeCache
from ghostclaw.core.analyzer import CodebaseAnalyzer
from ghostclaw.core.cache import LocalCache

load_dotenv()


def load_repos(repos_file: Path) -> List[str]:
    """Read repository URLs from file."""
    if not repos_file.exists():
        print(f"Error: repos file not found: {repos_file}", file=sys.stderr)
        sys.exit(1)
    return [
        line.strip()
        for line in repos_file.read_text(encoding='utf-8').splitlines()
        if line.strip() and not line.startswith("#")
    ]


def main():
    parser = argparse.ArgumentParser(
        description="Ghostclaw Compare — view vibe score trends"
    )
    parser.add_argument(
        "--repos-file",
        required=True,
        help="Path to file containing repository URLs or paths (one per line)",
    )
    parser.add_argument(
        "--cache-file",
        default=str(Path.home() / ".cache" / "ghostclaw" / "vibe_history.json"),
        help="Path to vibe history JSON cache",
    )
    parser.add_argument(
        "--work-dir",
        help="Directory where repos are cloned (if using URLs); if omitted, repos are assumed to be local paths",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Re-analyze all repos instead of using cached current scores",
    )

    args = parser.parse_args()

    repos_file = Path(args.repos_file)
    repos = load_repos(repos_file)

    vibe_cache = VibeCache(cache_file=args.cache_file)
    local_cache = LocalCache()
    work_dir = Path(args.work_dir) if args.work_dir else None
    analyzer = CodebaseAnalyzer(cache=local_cache)

    rows = []
    for repo_url in repos:
        # Get history from VibeCache
        history = vibe_cache.get_history(repo_url)

        if args.refresh:
            # Determine path to analyze
            if work_dir:
                # Extract repo name, handle .git suffix
                repo_name = repo_url.rstrip("/").split("/")[-1]
                if repo_name.endswith(".git"):
                    repo_name = repo_name[:-4]
                repo_path = work_dir / repo_name
            else:
                repo_path = Path(repo_url)

            # Try to analyze (could be local path or remote URL)
            try:
                # Use str(repo_path) if it exists locally, otherwise use repo_url (for remote URLs)
                analyze_target = str(repo_path) if repo_path.exists() else repo_url
                report = analyzer.analyze(analyze_target)
                curr_score = report["vibe_score"]
                vibe_cache.record_score(repo_url, curr_score)
                # For refresh, previous score is what was the latest before this record
                prev_score = history[-1]["vibe_score"] if history else None
            except Exception as e:
                # If analysis fails, we don't record a new score but we still have the history
                curr_score = None
                prev_score = history[-1]["vibe_score"] if history else None
        else:
            # Use data already in VibeCache
            if len(history) >= 2:
                curr_score = history[-1]["vibe_score"]
                prev_score = history[-2]["vibe_score"]
            elif len(history) == 1:
                curr_score = history[-1]["vibe_score"]
                prev_score = None
            else:
                curr_score = None
                prev_score = None

        # Compute delta
        delta = None
        if curr_score is not None and prev_score is not None:
            delta = curr_score - prev_score

        rows.append((repo_url, curr_score, prev_score, delta))

    print("\n=== Ghostclaw Repository Health Overview ===\n")
    print(f"Repositories: {len(repos)}")
    print(f"Cache: {args.cache_file}")
    print()

    if not rows:
        print("No data.")
        return

    # Header
    header = f"{'Repository':40} {'Current':8} {'Previous':8} {'Delta':6} {'Status'}"
    print(header)
    print("-" * len(header))

    for repo, curr, prev, delta in rows:
        # Determine status emoji
        if curr is None:
            status_emoji = "❓"
            status_text = "N/A"
        elif curr >= 80:
            status_emoji = "🟢"
            status_text = f"{curr}/100"
        elif curr >= 60:
            status_emoji = "🟡"
            status_text = f"{curr}/100"
        elif curr >= 40:
            status_emoji = "🟠"
            status_text = f"{curr}/100"
        else:
            status_emoji = "🔴"
            status_text = f"{curr}/100"

        delta_str = f"{delta:+d}" if delta is not None else "---"
        print(
            f"{repo[:40]:40} {status_text:8} {str(prev) if prev is not None else '---':8} {delta_str:6} {status_emoji}"
        )

    print()

    # Summary
    scores = [r[1] for r in rows if r[1] is not None]
    if scores:
        avg = sum(scores) / len(scores)
        healthy = sum(1 for s in scores if s >= 60)
        print(f"📊 Average vibe: {avg:.1f}/100 across {len(scores)} repos")
        print(f"✅ Healthy (≥60): {healthy}/{len(scores)}")


if __name__ == "__main__":
    main()
