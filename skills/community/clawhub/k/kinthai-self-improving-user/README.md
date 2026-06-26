# kinthai-Self-Improving-User

**User-level self-improvement for OpenClaw agents serving multiple users.**

Your agent learns from every interaction — corrections, errors, preferences — and stores that knowledge **per user**, so it gets better at serving each person individually.

## Why This Exists

The excellent [Self-Improving Agent](https://clawhub.ai/pskoett/self-improving-agent) by pskoett stores learnings at the workspace level. This works perfectly for single-developer scenarios, but when an agent serves multiple users (e.g., on a marketplace like [KinthAI](https://kinthai.ai)), learnings from different users get mixed together.

**kinthai-Self-Improving-User** solves this by isolating learnings per `user_id`:

```
.learnings/
  ├── _global/          Shared knowledge (applies to all users)
  ├── 10000002/         User A's corrections, preferences, profile
  ├── 10000003/         User B's corrections, preferences, profile
  └── _meta/            Promotion logs and stats
```

## How It Works

1. **Per-user isolation** — Each user gets their own `.learnings/{user_id}/` directory
2. **Automatic user detection** — Extracts `user_id` from OpenClaw session keys
3. **Two-layer reading** — Agent reads both `_global/` (universal) and `{user_id}/` (personal)
4. **Pattern promotion** — When 3+ users independently trigger the same learning, it's promoted to `_global/`
5. **User profiling** — Maintains a `PROFILE.md` per user with preferences and context

## Installation

```bash
# Install as an OpenClaw skill
openclaw skills install kinthai-self-improving-user

# Or manually copy to your workspace
cp -r . ~/.openclaw/workspace/skills/kinthai-self-improving-user/
```

### Hook Setup

Add to your OpenClaw hooks configuration or `~/.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "type": "script",
        "script": "skills/kinthai-self-improving-user/scripts/activator.sh"
      }
    ],
    "PostToolUse": [
      {
        "type": "script",
        "script": "skills/kinthai-self-improving-user/scripts/error-detector.sh",
        "matcher": "bash:.*"
      }
    ]
  }
}
```

## Components

| File | Purpose |
|------|---------|
| `SKILL.md` | Core prompt instructions for the agent |
| `scripts/activator.sh` | UserPromptSubmit hook — reminds agent to check/write learnings |
| `scripts/error-detector.sh` | PostToolUse hook — detects command failures per user |
| `scripts/promote.sh` | Promotes patterns from user-level to global (manual/cron) |
| `hooks/openclaw/handler.js` | Bootstrap hook — injects prior learnings into agent context |
| `templates/*.md` | Templates for LEARNINGS.md, ERRORS.md, PROFILE.md |

## Works With

- **[Hindsight](https://hindsight.vectorize.io/)** — Hindsight handles *what users said* (factual memory). This skill handles *what the agent learned* (behavioral improvement). They complement each other.
- **Any OpenClaw agent** — No dependencies on specific LLM providers or tools.
- **KinthAI marketplace agents** — Designed for multi-user service scenarios.

## Running the Promotion Script

Find patterns that appear across 3+ users and promote them to global:

```bash
# Dry run — see what would be promoted
./scripts/promote.sh --dry-run

# Actually promote
./scripts/promote.sh

# Custom threshold (e.g., 5 users)
./scripts/promote.sh --threshold 5
```

## Privacy

- Each user's learnings are isolated in their own directory
- The agent is instructed to NEVER read other users' directories
- Sensitive data (passwords, API keys) must NEVER be logged
- The learnings system is invisible to users — purely internal

## Credits

This skill is built on the ideas pioneered by **[Self-Improving Agent](https://github.com/peterskoett/self-improving-agent)** by [pskoett](https://github.com/peterskoett), released under MIT-0. We extended the concept with user-level isolation for multi-user agent scenarios.

## License

MIT-0 (No Attribution Required) — same as the original Self-Improving Agent.
