# 🌙 OpenClaw Dream

Automatic memory consolidation for OpenClaw agents — like REM sleep for your AI.

## What it does

Memory files accumulate noise over time: relative dates lose meaning, contradictory entries confuse the agent, duplicates waste context. **Dream** fixes this by running a structured 4-phase consolidation pass:

1. **Scan** — Read MEMORY.md + daily notes + self-improving logs
2. **Analyze** — Detect stale dates, contradictions, duplicates, outdated entries
3. **Consolidate** — Fix dates, resolve conflicts, merge duplicates, promote important items
4. **Write** — Update MEMORY.md, rebuild vector index, generate changelog

## Install

```bash
# Via ClawHub (coming soon)
clawhub install openclaw-dream

# Or manually
git clone https://github.com/liuweifly/openclaw-dream.git
cp -r openclaw-dream ~/.openclaw/workspace/skills/
```

## Usage

### Manual trigger
Just tell your agent: **"dream"**, **"整理记忆"**, or **"consolidate memory"**

### Automatic (recommended)
```bash
openclaw cron add \
  --id dream-nightly \
  --schedule "0 3 * * *" \
  --task "Run openclaw-dream memory consolidation. Read skills/openclaw-dream/SKILL.md and follow Phase 1-4." \
  --model sonnet \
  --isolated
```

### Pre-flight check
```bash
bash skills/openclaw-dream/scripts/dream-check.sh
```

## Configuration

Create `DREAM.md` in your workspace root to customize:

```markdown
## Settings
- max_memory_lines: 250
- lookback_days: 14
- min_hours_between_dreams: 24

## Protected Sections
- 经验教训
- About the user

## Custom Rules
- Always keep pricing/billing related entries
```

## Safety

- Never deletes daily note files — only modifies MEMORY.md
- Never touches source code or configs
- Preserves 📌 pinned entries
- Lock file prevents concurrent runs
- Generates audit-friendly dream-log for every run

## Inspired by

Claude Code's Auto Dream feature, but designed to be:
- **Open** — fully customizable via SKILL.md
- **Category-aware** — different strategies for facts vs lessons vs configs
- **Observable** — generates changelogs for every run
- **Multi-agent safe** — lock files + idempotent operations

## License

MIT-0
