---
name: git-backup
description: "Backup the agent workspace to a GitHub repository. Use when: asked to save/remember something important, after significant changes to memory files, on a schedule, or when asked to push workspace to git. Handles token discovery, repo initialization, and push. If no GitHub token is available, asks the owner for a PAT before proceeding."
---

# Git Backup Skill

## Load Local Context
```bash
CONTEXT_FILE="/opt/ocana/openclaw/workspace/skills/git-backup/.context"
[ -f "$CONTEXT_FILE" ] && source "$CONTEXT_FILE"
# Then use: $GITHUB_ACCOUNT, $REPO_NAME, $WORKSPACE, $GITHUB_TOKEN_FILE, etc.
```

## Minimum Model
Any model. This is pure shell — no reasoning needed.

---

## Step 1 — Find the GitHub Token

Run this to find the token. It checks sources in priority order:

```bash
find_github_token() {
  # 1. Check git remote URL (most common)
  TOKEN=$(git -C "$HOME/.openclaw/workspace" remote get-url origin 2>/dev/null \
    | grep -oP 'ghp_[A-Za-z0-9]+' | head -1)
  [ -n "$TOKEN" ] && echo "$TOKEN" && return

  # 2. Check standard environment variables
  [ -n "${GITHUB_TOKEN:-}" ] && echo "$GITHUB_TOKEN" && return
  [ -n "${GH_TOKEN:-}" ] && echo "$GH_TOKEN" && return

  # 3. Check credential files
  for f in ~/.credentials/github*.txt ~/.credentials/gh*.txt; do
    [ -f "$f" ] && cat "$f" | head -1 | tr -d '[:space:]' && return
  done

  # 4. Check ~/.bashrc for embedded token
  TOKEN=$(grep -oP 'ghp_[A-Za-z0-9]+' ~/.bashrc 2>/dev/null | head -1)
  [ -n "$TOKEN" ] && echo "$TOKEN" && return

  # Not found — return empty
  echo ""
}

TOKEN=$(find_github_token)
```

**If TOKEN is empty → stop and ask the owner:**
```
I need a GitHub Personal Access Token to back up your workspace.
Go to: github.com → Settings → Developer Settings → Personal access tokens → Generate new token
Required permission: repo (full)
Send me the token (starts with ghp_)
```

After receiving the token, save it:
```bash
# Save token to credentials file
echo "$TOKEN" > ~/.credentials/github-token.txt
chmod 600 ~/.credentials/github-token.txt

# Update the git remote URL to include the token
git -C "$HOME/.openclaw/workspace" remote set-url origin \
  "https://${TOKEN}@github.com/GITHUB_USERNAME/REPO_NAME.git"
```

---

## Step 2 — First-Time Setup (Run Once)

### Check if the repo already exists

```bash
TOKEN=$(find_github_token)
REPO_NAME="pa-workspace-backup"    # change to your repo name
GITHUB_USER="github-username"       # change to your GitHub username

# HTTP 200 = repo exists, 404 = need to create it
STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: token $TOKEN" \
  "https://api.github.com/repos/$GITHUB_USER/$REPO_NAME")

echo "Repo check: HTTP $STATUS"
```

### Create the repo (if HTTP 404)

```bash
curl -s -X POST "https://api.github.com/user/repos" \
  -H "Authorization: token $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"$REPO_NAME\", \"private\": true, \"description\": \"PA workspace backup\"}" \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
if 'html_url' in d:
    print('Created:', d['html_url'])
else:
    print('ERROR:', d)
    sys.exit(1)
"
```

### Initialize git (if no .git folder)

```bash
cd ~/.openclaw/workspace

# Initialize the repo
git init
git config user.email "agent@openclaw.ai"
git config user.name "PA Agent"
git remote add origin "https://$TOKEN@github.com/$GITHUB_USER/$REPO_NAME.git"

# Create .gitignore to exclude secrets and temp files
cat > .gitignore << 'EOF'
*.log
.env
credentials/
*.key
*.pem
node_modules/
__pycache__/
.DS_Store
EOF

# Initial commit and push
git add -A
git commit -m "Initial workspace backup"
git push -u origin main
```

---

## Step 3 — Regular Backup

Run this whenever you need to back up:

```bash
backup_workspace() {
  WORKSPACE="${1:-$HOME/.openclaw/workspace}"
  cd "$WORKSPACE" || { echo "ERROR: cannot cd to $WORKSPACE"; return 1; }

  # Check for token
  TOKEN=$(find_github_token)
  if [ -z "$TOKEN" ]; then
    echo "BLOCKED: No GitHub token found. Ask owner for PAT."
    return 1
  fi

  # Check git is initialized
  if [ ! -d ".git" ]; then
    echo "BLOCKED: Git not initialized. Run first-time setup first."
    return 1
  fi

  # Stage all changes
  git add -A

  # Count how many files changed
  CHANGES=$(git diff --cached --name-only | wc -l)

  # Nothing to do?
  if [ "$CHANGES" -eq 0 ]; then
    echo "Nothing to backup — workspace unchanged."
    return 0
  fi

  # Commit with timestamp and push
  DATE=$(date -u "+%Y-%m-%d %H:%M UTC")
  git commit -m "Auto backup $DATE"
  git push origin main 2>&1

  echo "Backup complete — $CHANGES files updated."
}

backup_workspace
```

**If push fails with "non-fast-forward":**
```bash
# Pull remote changes first, then push
git pull --rebase origin main
git push origin main
```

**If push fails with 401 (token expired):**
```bash
# Ask owner for a new PAT, then update the remote URL
git remote set-url origin "https://NEW_TOKEN@github.com/GITHUB_USERNAME/REPO_NAME.git"
```

---

## When to Back Up

Run a backup when:
- Owner says "remember this" / "save this"
- You update `MEMORY.md`, `SOUL.md`, or daily notes
- After completing a significant task
- On a schedule (see cron config below)

### Cron Config

```json
{
  "jobs": [
    {
      "id": "workspace-backup",
      "schedule": "0 */6 * * *",
      "timezone": "UTC",
      "task": "Run git backup of the workspace to GitHub. Use the git-backup skill. Commit all changes and push. Report DONE or BLOCKED.",
      "delivery": {
        "mode": "silent"
      }
    }
  ]
}
```

Runs every 6 hours silently. Change to `"0 23 * * *"` for nightly only.

---

## What to Include / Exclude

**Always include:**
- `MEMORY.md`, `SOUL.md`, `AGENTS.md`, `TOOLS.md`, `PA_LIST.md`
- `memory/` — daily notes
- `skills/` — installed skills
- `.learnings/` — corrections and learnings
- `data/` — PA directory and other data
- `config/` — MCP and other configs

**Always exclude (add to .gitignore):**
- API keys, tokens, secrets
- `credentials/` directory
- Log files (`*.log`)
- Node modules, Python cache

## Production Notes
- Workspace is at `/opt/ocana/openclaw/workspace` (not `~/.openclaw/workspace`)
- GitHub account: `netanel-abergel`, repo: `heleni-memory`
- After every significant memory update — always push to git (do not batch indefinitely)
- After skill updates (like this review) — push immediately

---

## Cost Tips

- **Very cheap:** Pure git/bash — no LLM tokens used during backup
- **Small model OK:** Any model can trigger this skill
- **Batch:** Commit all changes in one `git add -A` and one push — not file by file
- **Schedule wisely:** Every 6 hours is enough. More frequent = noise in git history
