# OpenClaw Skill Self Improvement

A health, eval, and regression system for continuously improving OpenClaw agent skills.

## What is this?

OpenClaw Skill Self Improvement is a set of scripts and evaluation cases that help you maintain a clean, healthy, and regress-free skill registry for your OpenClaw agent.

It answers three key questions:

1. **Are my skills clean?** — Detects duplicate, dark, and stale skills.
2. **Does routing work correctly?** — Evaluates whether the right skill triggers for the right input.
3. **Is it getting better over time?** — Tracks changes day by day via automated heartbeat.

## Quick start

```bash
# Clone the repo
git clone https://github.com/X-RayLuan/openclaw-skill-self-improvement.git
cd openclaw-skill-self-improvement

# Run health check
node scripts/skill-health-check.mjs /path/to/your/openclaw/workspace

# Run routing eval
node scripts/routing-eval-runner.mjs /path/to/your/openclaw/workspace

# Run daily heartbeat
node scripts/daily-health-heartbeat.mjs /path/to/your/openclaw/workspace
```

## System requirements

- Node.js 18+
- OpenClaw workspace with a `skills/` directory

## How it works

### Skill Health Check (`scripts/skill-health-check.mjs`)

Scans all `SKILL.md` files in your workspace and system skills directories, then:

- **Duplicate detection**: Compares skill names + descriptions using token similarity. Pairs with ≥72% overlap are flagged.
- **Dark skill detection**: Flags skills with no recent usage signal that haven't been updated in 30+ days.
- **Stale skill detection**: Flags skills with usage signals but no activity in 60+ days.

Deprecated skills (marked with `status: deprecated` in frontmatter) are automatically excluded from duplicate detection.

### Routing Eval (`scripts/routing-eval-runner.mjs`)

Reads `references/routing-evals.json` and simulates routing decisions using a keyword-weighted router. Each eval case defines:

- `input`: a user prompt
- `shouldTrigger`: expected skill IDs
- `shouldNotTrigger`: skills that must NOT trigger

The runner scores each skill using:
- Name word matches
- Trigger phrase overlap (≥50% word match required)
- Description keyword overlap
- Action-specific bonuses for known collision pairs

### Daily Heartbeat (`scripts/daily-health-heartbeat.mjs`)

Runs both scripts above, compares results against the previous run, and writes a human-readable summary. It tracks:

- Total skills
- Duplicate pairs
- Dark skills
- Eval pass rate
- Changes since last run

## Eval cases (8 cases)

| # | Input | Expected | Forbidden |
|---|-------|----------|-----------|
| 1 | debug this production failure | investigate | office-hours |
| 2 | brainstorm startup idea | office-hours | investigate |
| 3 | create a new skill | skill-creator | seo-content-writer |
| 4 | update the docs after PR | document-release | content-quality-auditor |
| 5 | audit my content quality | content-quality-auditor | content-writer |
| 6 | write a blog post for ClawLite | content-writer | seo-content-writer |
| 7 | run daily marketing pipeline | daily-marketing-operating-system | openclaw-mark |
| 8 | do a retro for this week | retro | openclaw-retro |

## Output files

| File | Description |
|------|-------------|
| `.learnings/skill-health-report.json` | Full health check results |
| `.learnings/routing-eval-report.json` | Eval pass/fail details |
| `.learnings/daily-skill-health-summary.txt` | Human-readable daily summary |
| `.learnings/skill-health-history.json` | Historical snapshot for delta tracking |

## Real-world results

On the [ClawLite](https://clawlite.ai) workspace (122 skills total):

- **Before**: 7 duplicate pairs, 37 dark skills
- **After**: 1 false-positive duplicate pair, 0 dark skills, 100% eval pass rate

Three duplicate pairs were resolved by deprecation:
- `openclaw-investigate` → deprecated (use `/investigate`)
- `openclaw-office-hours` → deprecated (use `/office-hours`)
- `openclaw-daily-backup` → deprecated (use `/openclaw-backup-restore`)

## Architecture

```
skill-health-check.mjs
  ├── walkSkills()           → scan all SKILL.md files
  ├── parseFrontmatter()     → read name, description, status
  ├── similarity()           → token-based text comparison
  ├── collectSessionFiles()  → scan agent transcripts for usage signals
  └── generate report

routing-eval-runner.mjs
  ├── scoreSkill()           → keyword + phrase + bonus scoring
  ├── routeInput()           → pick highest-scoring skill
  └── compare with expected

daily-health-heartbeat.mjs
  ├── run both scripts
  ├── load previous history
  ├── compute deltas
  └── write summary
```

## Roadmap

### Phase 2A
- Add more eval cases for high-risk collision pairs
- Replace keyword router with semantic matcher

### Phase 2B
- Derive `last_used_at` from real session transcripts
- Track `useCount` from observed routing

### Phase 3
- Add dependency drift checks for CLI/API-backed skills
- Add health status labels: `healthy`, `duplicate`, `dark`, `broken`, `degraded`
- Add cron/heartbeat automation for unattended daily runs

## Contributing

Issues and PRs welcome. Focus areas:
- Better semantic routing evaluation
- Real transcript usage tracking
- Additional health dimensions (dependency drift, skill performance)

## License

MIT © Ray Luan
