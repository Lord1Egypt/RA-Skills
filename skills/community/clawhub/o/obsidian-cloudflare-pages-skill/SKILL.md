---
name: obsidian-cloudflare-pages
description: Publish selected Obsidian markdown from a vault to a static site and deploy to Cloudflare Pages.
homepage: https://pages.cloudflare.com/
---

# OpenClaw Skill: Obsidian/Markdown → Cloudflare Pages

This is an **OpenClaw Skill** for publishing Markdown to Cloudflare Pages.

- Works with Obsidian vault folders **or any Markdown folder**
- Originally built for reading Obsidian Web Clipper output:
  - https://obsidian.md/clipper

Automates a safe publishing flow:
1. Select notes from your source folder
2. Sync to a publish workspace
3. Build static HTML with Quartz
4. Deploy to Cloudflare Pages

## Commands

- `node skills/obsidian-cloudflare-pages/bin/publishmd-cf.js init`
  - Creates `config/config.json` from example
- `node skills/obsidian-cloudflare-pages/bin/publishmd-cf.js wizard`
  - Interactive setup wizard for config (vault, folders, site/domain, Cloudflare project)
- `node skills/obsidian-cloudflare-pages/bin/publishmd-cf.js setup-project`
  - Initializes Quartz project in configured workspace if missing
- `node skills/obsidian-cloudflare-pages/bin/publishmd-cf.js doctor`
  - Validates paths + required binaries
- `node skills/obsidian-cloudflare-pages/bin/publishmd-cf.js sync`
  - Syncs selected notes/assets into publish content folder
- `node skills/obsidian-cloudflare-pages/bin/publishmd-cf.js build`
  - Runs Quartz build in project dir
- `node skills/obsidian-cloudflare-pages/bin/publishmd-cf.js deploy`
  - Deploys to Cloudflare Pages with wrangler
- `node skills/obsidian-cloudflare-pages/bin/publishmd-cf.js run`
  - sync → build → deploy

## Config

Copy and edit:

`skills/obsidian-cloudflare-pages/config/config.example.json` → `skills/obsidian-cloudflare-pages/config/config.json`

### Safety defaults
- Publish allowlist by folder
- Optional `publish: true` frontmatter gate
- Exclude private folders by default

## Requirements

- `node` 20+
- `rsync`
- `npm`
- `npx quartz`
- `wrangler`

## Cloudflare API token setup (recommended)

Create a Cloudflare API token with at least:
- **Account → Cloudflare Pages:Edit**
- (Optional) **Zone → DNS:Edit** if you want DNS automation elsewhere

You can either export env vars in your shell profile (`~/.zshrc`) or use the skill-local `.env` file.

### Option A: shell profile (`~/.zshrc`)

```bash
export CLOUDFLARE_API_TOKEN="<your-token>"
export CLOUDFLARE_ACCOUNT_ID="<your-account-id>"
```

Reload shell:

```bash
source ~/.zshrc
```

### Option B: skill-local env file (recommended for this skill)

```bash
cp skills/obsidian-cloudflare-pages/.env.example skills/obsidian-cloudflare-pages/.env
# then edit .env
```

The CLI auto-loads `skills/obsidian-cloudflare-pages/.env` (without overriding existing shell env vars).

Wizard now asks for:
- Full production domain (e.g. `YOURDOMAIN.COM`)
- Branding settings (root source folder, source index label, root index label, sidebar title HTML)
- Token/account env var names (defaults above)
- Optional basic-auth protection (username/password)


## Notes

- ⚠️ `setup-project` fallback behavior: if the direct Quartz bootstrap command fails, the fallback path may clear files in the configured workspace directory before cloning Quartz. Use a dedicated workspace path for this skill.

## OpenClaw usage tips

Example prompts:
- “Set up obsidian-cloudflare-pages wizard for my markdown folder.”
- “Run doctor and tell me what dependency is missing.”
- “Sync, build, and deploy to Cloudflare Pages.”
- “Enable basic auth and redeploy.”

Best practices:
- Keep secrets in `.env` (never in chat logs)
- Commit `config.example.json`, not personal `config.json`
- Use a scoped Cloudflare token (Pages edit, DNS edit only if needed)
- Start on a test subdomain before production

## Standalone usage (outside OpenClaw)

This works as a plain Node CLI too:

```bash
node bin/publishmd-cf.js init
node bin/publishmd-cf.js wizard
cp .env.example .env
# fill .env values
node bin/publishmd-cf.js run
```

## Security note

Basic auth in this skill is intentionally simple and optional. Do not publish highly sensitive content unless you fully understand your security model and hardening choices.

