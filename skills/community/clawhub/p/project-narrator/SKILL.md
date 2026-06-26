---
name: project-narrator
description: Generate, audit, and maintain a PROJECT-NARRATIVE.md file — a single-source-of-truth document that captures your entire project's architecture, decisions, infrastructure, and state. Use when asked to document a project, audit existing documentation, check for drift between docs and reality, or rebuild a project narrative. Also triggers on "fresh eyes", "project health check", "documentation audit", "bus factor", "disaster recovery docs".
---

# project-narrator

A workflow for maintaining a living document that can reconstruct your entire project from scratch. Not just documentation — a disaster recovery prompt.

The PROJECT-NARRATIVE.md file answers one question: **"If everything disappeared except this file, could someone rebuild the project?"** If yes, your narrative is complete.

## Commands

### `narrator generate`

Scan the workspace and generate a PROJECT-NARRATIVE.md from scratch.

**Workflow:**

1. Run `scripts/generate.py` in the project root to produce a scaffold
2. Review the scaffold — it captures structure, not intent
3. Fill in the sections the script can't infer: WHY decisions were made, design principles, known issues, security model
4. The script detects:
   - Package managers: package.json, pyproject.toml, Cargo.toml, go.mod
   - Infrastructure: Dockerfile, docker-compose, wrangler.toml/jsonc, vercel.json, serverless.yml
   - Git remote URL and recent commit history (last 20)
   - Source file counts by language
   - Scripts directory with first-line comments
   - Environment variables from .env.example
   - API route patterns from source (Express, FastAPI, Next.js, Hono)

```bash
python3 scripts/generate.py --workspace /path/to/project
python3 scripts/generate.py --workspace /path/to/project --output docs/NARRATIVE.md
```

**After running the script, the agent should:**
- Read the generated scaffold
- Explore the codebase to understand architecture and intent
- Fill in Design Principles, Known Issues, Security Model
- Check for OpenClaw cron jobs (`openclaw cron list`) and document them
- Add credential/ID references (without secrets — just names and where they're stored)

### `narrator audit`

Compare an existing narrative against reality. Flag drift.

**Workflow:**

1. Run `scripts/audit.py` against the project root
2. Review findings by severity (CRITICAL > WARNING > INFO)
3. Present findings to the user — don't auto-fix without asking

```bash
python3 scripts/audit.py --workspace /path/to/project
python3 scripts/audit.py --workspace /path/to/project --narrative docs/NARRATIVE.md
python3 scripts/audit.py --workspace /path/to/project --check-urls
```

**Severity levels:**
- **CRITICAL**: Referenced file doesn't exist, documented dependency removed, config structure changed
- **WARNING**: New files not documented, dependency version drift, undocumented scripts
- **INFO**: Minor structural differences, new commits since last update

### `narrator update`

Incrementally update the narrative based on recent changes.

**Workflow:**

1. Read the existing PROJECT-NARRATIVE.md
2. Find the last-updated date from the file
3. Run `git log --since="LAST_DATE"` to find changes
4. Identify significant changes:
   - New or deleted files
   - Changed config files (package.json, env, infra configs)
   - New dependencies
   - New scripts or API routes
5. Update the Changelog section with a summary
6. Flag sections that likely need manual review based on what changed
7. Update the "Last updated" date

**The agent should not blindly rewrite sections** — flag what changed and let the user decide how to update the narrative prose.

### `narrator report`

Generate a health report without modifying anything.

**Workflow:**

1. Run the audit workflow
2. Check git activity (commits per week, active contributors)
3. Check narrative freshness (days since last update)
4. Produce a summary:
   - Narrative age and staleness risk
   - Number of drift findings by severity
   - Sections most likely outdated
   - Recommendation: update, regenerate, or "looks good"

## Template Structure

The narrative follows this structure (flexible, not rigid):

```markdown
# Project Name: The Complete Narrative
*Last updated: YYYY-MM-DD*

## What Is This Project?
## Current Status
## Architecture
## Infrastructure
## Pipeline / Workflow
## API Routes
## Scripts
## Configuration
## Security Model
## Known Issues
## Design Principles
## Changelog
## Key Credentials & IDs
## File Map
```

See `references/narrative-template.md` for a complete template with guidance comments.
See `references/examples.md` for examples of well-written narrative sections.

## Configuration

Create `narrator.json` in your workspace root to customize behavior:

```json
{
  "schedule": "weekly",
  "audit_on_commit": false,
  "max_tokens_per_run": 5000,
  "sections": {
    "changelog": true,
    "file_map": true,
    "credentials": true
  }
}
```

### Schedule Options
- `"manual"` — only runs when you ask (default)
- `"weekly"` — runs audit every 7 days via heartbeat check
- `"daily"` — runs audit daily (higher token cost, ~2-5K tokens per audit)
- `"on_commit"` — runs after significant git commits (10+ files changed)

### Token Cost Estimates
- **Generate** (from scratch): ~3-8K tokens depending on project size
- **Audit** (compare): ~2-5K tokens
- **Update** (incremental): ~1-3K tokens
- **Report** (read-only): ~1-2K tokens

Recommendation: Start with `"manual"` and run audits weekly. Only switch to `"daily"` for fast-moving projects with multiple contributors.

### Token Efficiency
The skill is designed to be token-conscious:
- Scripts run locally (Python stdlib) — zero LLM tokens for scanning
- Only the narrative TEXT goes through the LLM for generation/update
- Audit is pure filesystem comparison — no LLM needed
- Incremental updates only process git diff, not the whole project

## Key Principles

**Capture WHY, not just WHAT.** Any tool can list files. The narrative explains why the project is structured this way, what alternatives were considered, and what mistakes were made along the way.

**Known issues are features.** Documenting bugs, tech debt, and past mistakes prevents repeating them. A narrative that only shows the happy path is incomplete.

**Design Principles is the most important section.** Architecture can be reverse-engineered from code. Design principles cannot. "We chose SQLite over Postgres because this runs on edge workers" — that's the kind of decision that saves hours of confusion.

**Self-contained.** Any agent or developer reading the narrative should understand the full project without needing to ask follow-up questions. If they have to dig through code to understand the narrative, the narrative failed.

**Fresh build every time.** Narratives are always regenerated from scratch — never patched or appended. This prevents drift from accumulating across versions. When you run `narrator generate`, the old narrative is archived and a completely new one is built by scanning the current state. No assumptions carried forward from previous versions.

**Automatic archiving.** Every time a narrative is regenerated, the previous version is saved to `narrative-archive/NARRATIVE-{timestamp}.md`. This gives you rollback ability and a history of how the project evolved. Archives are cheap — keep them.

**Living document.** Regenerate after significant changes or weekly via cron. A stale narrative is worse than no narrative — it actively misleads.

**No secrets in the narrative.** Reference where credentials are stored, never the credentials themselves. "API key stored in ~/.openclaw/secrets/stripe.key" — not the key.

## Automation

### Weekly cron (OpenClaw)

Set up a weekly narrative health check:

```
openclaw cron add --schedule "0 9 * * 1" --prompt "Run narrator report on /path/to/project. If there are CRITICAL findings, notify me. Otherwise log to memory." --label "narrator-weekly"
```

### Post-deploy hook

After significant deploys, run `narrator update` to capture what changed.

## About

project-narrator was built during the development of [AgentWyre](https://agentwyre.ai), an AI intelligence wire service, where maintaining accurate project state across dozens of cron jobs, API endpoints, and daily pipelines proved that living documentation isn't optional — it's infrastructure. Born from building AgentWyre, the narrative pattern kept its complex multi-language, multi-pipeline system coherent across hundreds of changes in its first week of operation.
