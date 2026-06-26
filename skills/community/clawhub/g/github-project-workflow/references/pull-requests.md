# Pull Requests

## Create
```bash
gh pr create --repo owner/repo \
  --title "feat: description (#42)" \
  --body "## What\n...\n## Why\nCloses #42\n## Testing\n- [ ] tests pass" \
  --base develop --head feature/branch \
  --label "feature" --assignee "@me"

gh pr create ... --draft          # WIP
gh pr ready 55 --repo owner/repo  # promote draft
```

## Review & Inspect
```bash
gh pr view 55 --repo owner/repo
gh pr diff 55 --repo owner/repo
gh pr checks 55 --repo owner/repo
gh pr review 55 --approve --body "LGTM"
gh pr review 55 --request-changes --body "..."
gh pr comment 55 --body "..."
```

## Merge strategies
```bash
# ⚠️ CONFIRM WITH USER before running — merges code into base branch and deletes source branch
gh pr merge 55 --squash --delete-branch --repo owner/repo  # features (clean history)
gh pr merge 55 --merge --repo owner/repo                   # releases (preserve history)
gh pr merge 55 --rebase --delete-branch --repo owner/repo  # linear history
```

## List
```bash
gh pr list --repo owner/repo
gh pr list --repo owner/repo --assignee "@me"
gh pr list --repo owner/repo --json number,title,state,reviewDecision \
  --jq '.[] | "\(.number): \(.title) [\(.reviewDecision // "pending")]"'
```

## Close without merging
```bash
# ⚠️ CONFIRM WITH USER before running — closes PR without merging (task cancelled or superseded)
gh pr close 55 --repo owner/repo --comment "Closing — superseded by #60"
```
