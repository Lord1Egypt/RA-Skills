# API Queries, Search & Audit

## Issues
```bash
gh issue list --repo owner/repo --label "bug" --state open
gh issue list --repo owner/repo --assignee "@me"

gh issue create --repo owner/repo --title "..." --body "..." --label "bug"

# ⚠️ CONFIRM WITH USER before running — posts a comment on the issue
gh issue comment 42 --repo owner/repo --body "Fixed in #55, released in v1.2.1"

# ⚠️ CONFIRM WITH USER before running — closes the issue
gh issue close 42 --repo owner/repo

# In commits always: "fixes #42" / "closes #42" / "resolves #42"
```

## JSON queries
```bash
gh pr list --repo owner/repo \
  --json number,title,state,mergeable,reviewDecision \
  --jq '.[] | "\(.number): \(.title) [\(.state)]"'

gh issue list --repo owner/repo \
  --json number,title,labels \
  --jq '.[] | "\(.number): \(.title) | \([.labels[].name]|join(","))"'

gh api repos/owner/repo/issues --paginate --jq '.[].title'
```

## Audit
```bash
# Recent commits
gh api repos/owner/repo/commits \
  --jq '.[:10][] | "\(.sha[:7]) \(.commit.author.name): \(.commit.message|split("\n")[0])"'

# PR for a commit
gh api repos/owner/repo/commits/<sha>/pulls --jq '.[0]|"#\(.number) \(.title)"'

# Search TODOs
gh api search/code --field q="TODO repo:owner/repo" \
  --jq '.items[] | "\(.path): \(.text_matches[0].fragment)"'

# Repo stats
gh api repos/owner/repo --jq '{stars:.stargazers_count,forks:.forks_count,issues:.open_issues_count}'
```
