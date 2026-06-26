# gist-share

> An OpenClaw skill for posting content to GitHub Gist and getting back a shareable URL.

Rich, persistent, markdown-rendered context — shareable with anyone, readable by any agent.

---

## Why Gists?

Agents communicate through messages, but messages disappear into scroll. A gist is:

- **Persistent** — stays at a stable URL
- **Readable by anyone** — no auth required for public gists
- **Markdown-rendered** — GitHub renders it beautifully
- **Shareable** — paste the URL anywhere, drop it in a chat, send it to another agent

When an agent needs to hand off context to a human, another agent, or a future session — a gist beats a wall of chat text.

---

## Setup

### 1. Install the skill

```bash
clawhub install gist-share
```

Or clone this repo into your OpenClaw skills directory:

```bash
git clone https://github.com/PsiClawOps/gist-share ~/.openclaw/skills/gist-share
```

### 2. Create a GitHub Personal Access Token (PAT)

1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Click **"Generate new token (classic)"**
3. Give it a name like `openclaw-gist`
4. Check the **`gist`** scope — that's all you need
5. Click **Generate token**
6. Copy the token (you won't see it again)

### 3. Set your token

Add it to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
echo 'export GITHUB_TOKEN=ghp_yourTokenHere' >> ~/.zshrc
source ~/.zshrc
```

Or set it for the current session only:

```bash
export GITHUB_TOKEN=ghp_yourTokenHere
```

### 4. Verify

```bash
gh auth status
```

You should see your account with `gist` listed under token scopes.

> **Don't have `gh` installed?**
> - macOS: `brew install gh`
> - Linux: `apt install gh` or see [cli.github.com](https://cli.github.com)

---

## Usage

Once the skill is installed and your token is set, tell your agent to post a gist. It will use the `exec` tool to run:

```bash
gh gist create \
  --public \
  --desc "Your description" \
  --filename "your-file.md" - << 'EOF'
# Your Content Here

Supports **markdown** formatting.
EOF
```

The command returns the gist URL:

```
✓ Created public gist your-file.md
https://gist.github.com/USERNAME/HASH
```

### Public vs Secret

- `--public` — indexed, visible to anyone with the link
- `--secret` — not indexed, but still accessible via direct URL

### Tips

- Use `.md` extension in `--filename` so GitHub renders markdown
- Write a meaningful `--desc` — it's searchable
- Update an existing gist: `gh gist edit GIST_ID`
- List your gists: `gh gist list`

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `gh: command not found` | Install via `brew install gh` or `apt install gh` |
| `HTTP 401 Unauthorized` | Token missing or expired — redo setup |
| Token missing `gist` scope | Regenerate PAT with `gist` scope checked |
| `gh auth status` shows invalid | Run `gh auth login` and follow prompts |

---

## ClawHub

Install via the ClawHub registry:

```bash
clawhub install gist-share
```

Browse: [clawhub.ai/ragesaq/gist-share](https://clawhub.ai/ragesaq/gist-share)

---

*Part of the [PsiClawOps](https://github.com/PsiClawOps) skill suite.*
