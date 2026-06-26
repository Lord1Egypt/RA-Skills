# Repo Setup & Branch Protection

## Create / Clone / Fork
```bash
gh repo create owner/repo --private --description "..."
gh repo create owner/repo --public --gitignore Node --license MIT
gh repo clone owner/repo
gh repo fork owner/repo --clone
gh repo view owner/repo --json name,description,defaultBranch,isPrivate

# ⚠️ CONFIRM WITH USER before running — makes repo read-only permanently
gh repo archive owner/repo

# ⚠️ CONFIRM WITH USER before running — permanently deletes repo and all data
gh repo delete owner/repo --yes
```

## Branch Protection (main & develop)
```bash
# ⚠️ CONFIRM WITH USER before running — changes who can push/merge to the branch
gh api --method PUT repos/owner/repo/branches/main/protection \
  --field required_status_checks='{"strict":true,"contexts":["ci/tests"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1}' \
  --field required_linear_history=true \
  --field restrictions=null

# View current rules
gh api repos/owner/repo/branches/main/protection
```
