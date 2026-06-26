---
name: mergeiq
description: >
  Score the complexity of any GitLab MR or GitHub PR using a 4-dimension framework:
  Size (20%), Cognitive Load (30%), Review Effort (30%), and Risk/Impact (20%).
  Works with GitLab or GitHub. Zero external dependencies.
  Use when asked to review, triage, score, or prioritise pull requests and merge requests by complexity.
license: MIT
metadata:
  author: larry.l.fang@gmail.com
  version: "1.0.0"
  tags: gitlab, github, pull-request, merge-request, code-review, engineering, dora, complexity
---

# MR / PR Complexity Scorer

A provider-agnostic complexity scoring engine for Merge Requests (GitLab) and Pull Requests
(GitHub). Built on a 4-dimension framework that captures what "complex" actually means in
code review — not just lines changed.

## Complexity Dimensions

| Dimension       | Weight | What it measures                                              |
|-----------------|--------|---------------------------------------------------------------|
| Size            | 20%    | Volume of code changed (logarithmic — big PRs saturate fast) |
| Cognitive Load  | 30%    | Directory breadth, cross-module changes, file diversity       |
| Review Effort   | 30%    | Discussion depth, reviewer count, approval iterations         |
| Risk / Impact   | 20%    | Breaking changes, migrations, security labels, dependencies   |

**Output tiers:** trivial / simple / moderate / complex / highly_complex

## When to Use

- Triaging a backlog of open PRs by complexity before a review session
- Flagging high-complexity MRs for mandatory second review
- Generating weekly complexity trend reports for a team
- Understanding *why* a PR is taking a long time (dimension breakdown)
- Building engineering director dashboards (see score_mr.py)

## Quick Start

```bash
# Score a GitHub PR (basic — just the PR object)
curl -s "https://api.github.com/repos/OWNER/REPO/pulls/NUMBER" \
     -H "Authorization: Bearer $GITHUB_TOKEN" \
     | python score_mr.py --provider github

# Score a GitLab MR (with diff stats)
curl -s "https://gitlab.com/api/v4/projects/PROJECT_ID/merge_requests/IID?include_diff_stats=true" \
     -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
     | python score_mr.py --provider gitlab

# Richer scoring — fetch files + reviews too
curl -s ".../pulls/NUMBER" > pr.json
curl -s ".../pulls/NUMBER/files" > files.json
curl -s ".../pulls/NUMBER/reviews" > reviews.json
python score_mr.py --provider github --pr pr.json --files files.json --reviews reviews.json
```

## Example Output

```json
{
  "provider": "github",
  "id": 412,
  "title": "Migrate auth service to OAuth2",
  "score": {
    "total": 74.2,
    "tier": "complex",
    "size": 68.0,
    "cognitive": 81.5,
    "review_effort": 72.0,
    "risk_impact": 60.0
  },
  "summary": "High mental load: 14 files across 6 directories, 3 reviewers involved",
  "tier_insight": "Needs careful review — high cognitive load and cross-module impact.",
  "stats": {
    "additions": 412,
    "deletions": 87,
    "files_changed": 14,
    "reviewers": 3,
    "discussions": 9,
    "net_lines": 325
  }
}
```

## Files

```
mr-complexity-scorer/
  SKILL.md                      # This file
  mr_complexity_service.py      # Core 4-dimension scoring engine (pure Python)
  score_mr.py                   # CLI: pipe in API JSON, get complexity JSON out
  requirements.txt              # No external deps — stdlib only, Python 3.9+
  adapters/
    gitlab_adapter.py           # GitLab MR API dict → MRData
    github_adapter.py           # GitHub PR API dict → MRData
```

## Using in Your Code

```python
from mr_complexity_service import MRComplexityCalculator, MRData
from adapters.github_adapter import github_pr_to_mrdata

# Build MRData from a GitHub PR dict (from API or webhook payload)
mr_data = github_pr_to_mrdata(
    pr=pr_dict,
    files=files_list,       # optional: /pulls/:number/files
    commits=commits_list,   # optional: /pulls/:number/commits
    reviews=reviews_list,   # optional: /pulls/:number/reviews
)

calculator = MRComplexityCalculator()
result = calculator.calculate(mr_data)

print(result.complexity_tier)   # "complex"
print(result.total_score)       # 74.2
print(result.human_summary)     # "High mental load: ..."
```

## Enrichment — What's Worth Fetching

| Extra API call                   | Unlocks                         | Worth it?          |
|----------------------------------|---------------------------------|--------------------|
| `/pulls/:n/files`                | File path cognitive analysis    | Yes, always        |
| `/pulls/:n/reviews`              | Accurate reviewer count + iters | Yes for review dim |
| `/pulls/:n/commits`              | Breaking-change detection       | Nice to have       |
| `/pulls/:n/comments`             | Inline discussion count         | Optional           |

Without enrichment, the scorer still works — it uses `changed_files`, `review_comments`,
and `requested_reviewers` from the base PR object. Enriched data improves accuracy.

## Extending to Other Providers

Implement a thin adapter that maps your provider's MR/PR dict to `MRData`:

```python
from mr_complexity_service import MRData

def linear_issue_to_mrdata(issue: dict) -> MRData:
    return MRData(
        iid=issue["number"],
        title=issue["title"],
        # ... map your fields
    )
```

Works with: GitLab, GitHub, Gitea, Bitbucket, Azure DevOps — anything with MR/PR metadata.

## Adjusting Weights

```python
from mr_complexity_service import MRComplexityCalculator, ComplexityConfig

config = ComplexityConfig(
    weight_size=0.15,
    weight_cognitive=0.35,
    weight_review=0.30,
    weight_risk=0.20,
)
calculator = MRComplexityCalculator(config=config)
```
