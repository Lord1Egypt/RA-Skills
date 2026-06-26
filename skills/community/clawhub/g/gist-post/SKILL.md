---
name: gist-post
version: 1.0.0
description: Post content to GitHub Gist and get back a shareable URL. Rich context sharing between agents, operators, and humans.
homepage: https://github.com/PsiClawOps/gist-share
---

# gist-post

Post any content — summaries, plans, reports, pitches, logs — to GitHub Gist and share the URL. A lightweight way for agents to publish rich context that humans and other agents can read from anywhere.

## Why Gists?

Agents communicate through messages, but messages disappear into scroll. A gist is:
- **Persistent** — stays at a stable URL
- **Readable by anyone** — no auth required for public gists
- **Markdown-rendered** — GitHub renders it beautifully
- **Shareable** — paste the URL anywhere

When an agent needs to hand off context to a human, another agent, or a future session — a gist beats a wall of chat text.

---

## Setup

You need a GitHub Personal Access Token scoped to `gist`, set as `GITHUB_TOKEN` in your environment. Ask your agent to walk you through creating one if you haven't already.

---

## How to Post a Gist

Use the `exec` tool to call `gh gist create`:

```bash
gh gist create --public --desc "DESCRIPTION" --filename "FILENAME.md" - << 'EOF'
# Your content here

Supports **markdown** formatting.
EOF
```

Use `--secret` instead of `--public` if the content shouldn't be publicly indexed.

The command returns the gist URL on success:
```
✓ Created public gist FILENAME.md
https://gist.github.com/USERNAME/HASH
```

---

## Workflow

1. **Prepare content** — write your markdown
2. **Choose visibility** — `--public` or `--secret`
3. **Post it** — run `gh gist create` via `exec`
4. **Return the URL** — share it in the conversation, send it to another agent, or log it

---

## Tips

- Use `.md` extension in `--filename` so GitHub renders markdown
- Write a meaningful `--desc` — it's searchable
- Update an existing gist: `gh gist edit GIST_ID`
- List your gists: `gh gist list`

---

*Gists: the simplest way for a claw to leave a note the world can read.*
