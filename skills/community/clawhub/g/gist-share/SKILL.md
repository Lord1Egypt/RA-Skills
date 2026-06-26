---
name: gist-share
version: 1.0.1
description: Post content to GitHub Gist and get back a shareable URL. Rich context sharing between agents, operators, and humans.
homepage: https://github.com/PsiClawOps/gist-share
---

# gist-share

Post any content — summaries, plans, reports, pitches, logs — to GitHub Gist and share the URL. A lightweight way for agents to publish rich context that humans and other agents can read from anywhere.

## Why Gists?

Agents communicate through messages, but messages disappear into scroll. A gist is:
- **Persistent** — stays at a stable URL
- **Readable by anyone** — no auth required for public gists
- **Markdown-rendered** — GitHub renders it beautifully
- **Shareable** — paste the URL anywhere

When an agent needs to hand off context to a human, another agent, or a future session — a gist beats a wall of chat text.

---

## Setup (One-Time)

You need a GitHub Personal Access Token (PAT) with the `gist` scope.

### Step 1: Create a PAT

1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Click **"Generate new token (classic)"**
3. Give it a name like `openclaw-gist`
4. Check the **`gist`** scope (that's all you need)
5. Click **Generate token**
6. Copy the token — you won't see it again

### Step 2: Authenticate the `gh` CLI

OpenClaw uses the `gh` CLI to post gists. Set your token as an environment variable for the session:

```bash
export GITHUB_TOKEN=ghp_yourTokenHere
```

Or add it permanently to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
echo 'export GITHUB_TOKEN=ghp_yourTokenHere' >> ~/.zshrc
source ~/.zshrc
```

### Step 3: Verify it works

```bash
gh auth status
```

You should see your account and `gist` listed under token scopes.

---

## How to Post a Gist

### Basic usage

Use the `exec` tool to call `gh gist create`:

```bash
gh gist create --public --desc "Your description here" --filename "your-file.md" - << 'EOF'
Your content here.

Supports **markdown** formatting.
EOF
```

### With a flag for secret gists

Replace `--public` with `--secret` if the content shouldn't be publicly indexed.

### Full template

```bash
gh gist create \
  --public \
  --desc "DESCRIPTION" \
  --filename "FILENAME.md" - << 'GISTEOF'
# TITLE

CONTENT GOES HERE
GISTEOF
```

The command returns the gist URL on success:
```
✓ Created public gist FILENAME.md
https://gist.github.com/USERNAME/HASH
```

---

## Workflow

1. **Prepare content** — write your markdown (report, summary, plan, pitch, log)
2. **Choose visibility** — `--public` for sharing freely, `--secret` for targeted sharing
3. **Post it** — run `gh gist create` via `exec`
4. **Return the URL** — share it in the conversation, send it to another agent, or log it

---

## Example: Posting a Strategic Summary

```bash
gh gist create --public --desc "Q2 Roadmap Summary" --filename "q2-roadmap.md" - << 'EOF'
# Q2 Roadmap Summary

## Phase 1 — Foundation (April)
- Complete ClawDash MVP
- Ship ClawCanvas v1

## Phase 2 — Expansion (May)
- Launch ClawText beta
- Begin ClawTomation integration

## Phase 3 — Scale (June)
- Public launch of suite
- Partner integrations go live
EOF
```

---

## Tips

- **Filename matters** — use `.md` extension for GitHub to render markdown
- **Description is searchable** — write something meaningful
- **One gist per topic** — don't cram everything into one file; use focused gists
- **Update with `gh gist edit GIST_ID`** — gists are editable if you need to revise
- **List your gists** — `gh gist list` shows recent gists with their IDs and URLs

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `gh: command not found` | Install via `brew install gh` (macOS) or `apt install gh` (Linux) |
| `HTTP 401 Unauthorized` | Token missing or expired — re-run setup |
| `Token missing gist scope` | Regenerate the PAT with `gist` scope checked |
| `gh auth status` shows invalid token | Run `gh auth login` and follow the prompts |

---

*Gists: the simplest way for a claw to leave a note the world can read.*
