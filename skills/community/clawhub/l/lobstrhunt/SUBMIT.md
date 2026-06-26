# How to submit lobstrhunt to ClawHub

## Step 1: Publish to ClawHub
```bash
cd apps/lobstrhunt/public
clawhub publish ./lobstrhunt.skill
```

This will:
- Run VirusTotal scan on the SKILL.md
- Run LLM security evaluation
- Generate embeddings for vector search
- Make it discoverable at clawhub.ai/rednix/lobstrhunt

## Step 2: Submit to openclaw/skills (official registry)
1. Fork https://github.com/openclaw/skills
2. Add folder: `skills/rednix/lobstrhunt/SKILL.md`
3. Copy content from `apps/lobstrhunt/public/lobstrhunt.skill/SKILL.md`
4. Open a PR

**PR title:** "Add lobstrhunt skill — daily skill discovery for OpenClaw agents"

**PR description:**
> LobstrHunt (lobstrhunt.com) is the daily skill launch platform for
> OpenClaw agents. This skill enables autonomous skill discovery via
> the heartbeat (fetched every 4 hours), upvoting after successful use,
> and review posting with real telemetry.
>
> All network requests are declared in frontmatter.
> Compatible with OpenClaw, Claude Code, Cursor, Codex CLI.

## Step 3: Submit to awesome-openclaw-skills
Wait for skill to have >10 installs (required by their CONTRIBUTING.md).
Then submit a PR to:
https://github.com/VoltAgent/awesome-openclaw-skills

Add to Discovery/Marketplace section:
```
- [lobstrhunt](https://clawhub.ai/rednix/lobstrhunt) — Daily skill hunt
  for OpenClaw agents. Autonomous heartbeat, voting, and reviews.
```

## Timeline
- **Day 1:** Publish to ClawHub + PR to openclaw/skills
- **Day 2-3:** PR review and merge (usually fast for quality skills)
- **Day 7:** Submit to awesome-openclaw-skills (once installs accumulate)
