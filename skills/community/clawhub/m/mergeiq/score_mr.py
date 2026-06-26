#!/usr/bin/env python3
"""
score_mr.py — CLI wrapper for MR/PR complexity scoring.

Usage:
    # Score a GitLab MR (pipe in JSON from GitLab API)
    curl -s "https://gitlab.com/api/v4/projects/:id/merge_requests/:iid?include_diff_stats=true" \
         -H "PRIVATE-TOKEN: $GITLAB_TOKEN" | python score_mr.py --provider gitlab

    # Score a GitHub PR
    curl -s "https://api.github.com/repos/:owner/:repo/pulls/:number" \
         -H "Authorization: Bearer $GITHUB_TOKEN" | python score_mr.py --provider github

    # Score with enriched data (file paths, reviews)
    python score_mr.py --provider github --pr pr.json --files files.json --reviews reviews.json

Output: JSON with total_score, tier, dimension scores, and human-readable summary.
"""

import argparse
import json
import sys

from mr_complexity_service import MRComplexityCalculator
from adapters.gitlab_adapter import gitlab_mr_to_mrdata
from adapters.github_adapter import github_pr_to_mrdata


def main():
    parser = argparse.ArgumentParser(description="Score MR/PR complexity")
    parser.add_argument("--provider", choices=["gitlab", "github"], required=True,
                        help="Code platform provider")
    parser.add_argument("--pr", "--mr", dest="pr_file",
                        help="Path to PR/MR JSON file (default: stdin)")
    parser.add_argument("--files", dest="files_file",
                        help="Path to files/diffs JSON array file")
    parser.add_argument("--commits", dest="commits_file",
                        help="Path to commits JSON array file")
    parser.add_argument("--reviews", dest="reviews_file",
                        help="Path to reviews JSON array file (GitHub) or approvals JSON (GitLab)")
    parser.add_argument("--notes", dest="notes_file",
                        help="Path to notes JSON array file (GitLab only)")
    parser.add_argument("--pretty", action="store_true", default=True,
                        help="Pretty-print output (default: true)")
    args = parser.parse_args()

    # Load PR/MR data
    if args.pr_file:
        with open(args.pr_file) as f:
            pr = json.load(f)
    else:
        pr = json.load(sys.stdin)

    # Load optional enrichment files
    def load_optional(path):
        if not path:
            return None
        with open(path) as f:
            return json.load(f)

    files = load_optional(args.files_file)
    commits = load_optional(args.commits_file)
    reviews = load_optional(args.reviews_file)
    notes = load_optional(args.notes_file)

    # Convert to MRData
    if args.provider == "gitlab":
        mr_data = gitlab_mr_to_mrdata(pr, diffs=files, notes=notes, approvals=reviews)
    else:
        mr_data = github_pr_to_mrdata(pr, files=files, commits=commits, reviews=reviews)

    # Score
    calculator = MRComplexityCalculator()
    breakdown = calculator.calculate(mr_data)

    # Output
    result = {
        "provider": args.provider,
        "id": mr_data.iid,
        "title": mr_data.title,
        "score": {
            "total": round(breakdown.total_score, 1),
            "tier": breakdown.complexity_tier,
            "size": round(breakdown.size_score, 1),
            "cognitive": round(breakdown.cognitive_score, 1),
            "review_effort": round(breakdown.review_score, 1),
            "risk_impact": round(breakdown.risk_score, 1),
        },
        "summary": breakdown._get_cognitive_insight(),
        "tier_insight": breakdown._get_tier_insight(),
        "stats": {
            "additions": mr_data.additions,
            "deletions": mr_data.deletions,
            "files_changed": mr_data.files_changed,
            "reviewers": mr_data.reviewers_count,
            "discussions": mr_data.discussions_count,
            "net_lines": breakdown.net_lines,
        }
    }

    indent = 2 if args.pretty else None
    print(json.dumps(result, indent=indent))


if __name__ == "__main__":
    main()
