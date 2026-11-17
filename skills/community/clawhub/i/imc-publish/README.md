# imc-publish

Publish to your connected social channels from Claude Code or Codex, through
your InstallMyClaw workspace. Every publish shows up in your workspace
dashboard.

## Install

### Claude Code

```bash
cp -r imc-publish ~/.claude/skills/imc-publish
```

The skill triggers automatically on publish-related requests, or invoke it
with `/imc-publish`.

### Codex

Copy the folder anywhere (e.g. `~/skills/imc-publish`) and add to your
`AGENTS.md`:

```markdown
## Social publishing
To publish to social channels, follow the workflow in
~/skills/imc-publish/SKILL.md (client: scripts/imc_publish.py).
```

## Configure

```bash
# ~/.zshrc / ~/.bashrc — or your secrets manager
export IMC_PUBLISH_API_KEY="<key from your workspace owner>"
```

Requires python3 (no packages). Test with:

```bash
python3 ~/.claude/skills/imc-publish/scripts/imc_publish.py accounts
```

## What it does

- Lists your connected accounts (IG / TikTok / FB / YouTube / LinkedIn /
  Threads / Google Business / Telegram)
- Uploads images and mp4 videos (≤100MB)
- Drafts a post, shows you the exact preview, publishes only after you confirm
- Schedules posts for later
- Reports per-platform results; history is visible in your dashboard
