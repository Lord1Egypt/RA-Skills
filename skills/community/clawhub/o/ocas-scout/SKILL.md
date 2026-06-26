---
name: ocas-scout
source: https://github.com/indigokarasu/scout
install: openclaw skill install https://github.com/indigokarasu/scout
description: Use when researching a person, company, or organization with provenance-backed sources: building background briefs, resolving entity identity across public sources, compiling cited findings, or escalating through a free-first source waterfall. Trigger phrases: 'research this person', 'who is', 'background check', 'look up this company', 'what do we know about', 'update scout'. Do not use for topic research without a person/org focus (use Sift) or illegal data collection.
metadata: {"openclaw":{"emoji":"🔍"}}
---

# Scout

Scout conducts lawful OSINT research on people, companies, and organizations, assembling provenance-backed briefs where every claim carries a source reference, retrieval timestamp, and direct quote. It works through a tiered source waterfall — public web first, then rate-limited registries, then paid databases only with explicit permission — collecting no more than the stated research goal requires.

## When to use

- Research a person and build a source-backed brief
- Do background research on a company using public sources
- Resolve whether two profiles are the same person with cited sources
- Compile what is publicly knowable about a subject
- Expand a quick lookup into an auditable brief

## When not to use

- Illegal intrusion into private systems
- Credential theft or bypassing access controls
- Covert surveillance
- Speculative doxxing
- Topic research without a person/org focus — use Sift

## Responsibility boundary

Scout owns lawful OSINT research on people and organizations with provenance-backed output.

Scout does not own: general topic research (Sift), image processing (Look), knowledge graph writes (Elephas), social graph (Weave), communications (Dispatch).

## Commands

- `scout.research.start` — begin a new research request with subject and goal
- `scout.research.expand --tier <1|2|3>` — escalate to a higher source tier
- `scout.brief.render` — generate the final markdown brief with findings and sources
- `scout.brief.render_pdf` — optional PDF brief generation
- `scout.status` — return current research state
- `scout.journal` — write journal for the current run; called at end of every run
- `scout.update` — pull latest from GitHub source; preserves journals and data

## Invariants

1. Legality-first — only publicly available sources without bypassing access controls
2. Minimization — collect only what the research goal requires
3. Provenance for every claim — at least one source reference with URL, retrieval timestamp, and quote
4. Paid sources require explicit permission — Tier 3 needs a recorded PermissionGrant
5. No doxxing by default — private details suppressed unless explicitly permitted
6. Uncertainty must be surfaced — incomplete identity resolution stated clearly

## Input contract

ResearchRequest requires: request_id, as_of, subject (type, name, aliases, known_locations, known_handles), goal, constraints (time_budget_minutes, minimize_pii).

Read `references/scout_schemas.md` for exact schema.

## Research workflow

1. Normalize request and subject identity inputs
2. Resolve likely identity matches conservatively
3. Run Tier 1 public-source collection
4. Record provenance for every retained claim
5. Compile preliminary findings with confidence levels
6. Escalate to Tier 2 only if enabled and useful
7. Escalate to Tier 3 only after explicit permission grant is recorded
8. Generate brief with findings, uncertainty, and source log
9. Store request, findings, sources, and decisions locally
10. Emit Signal files for confirmed entities and relationships to `~/openclaw/db/ocas-elephas/intake/{signal_id}.signal.json`. Use Signal schema from `spec-ocas-shared-schemas.md`. One file per entity or relationship with sufficient confidence.
11. Write journal via `scout.journal`

When `minimize_pii=true`, suppress unnecessary sensitive details in the final brief.

## Source waterfall

Read `references/scout_source_waterfall.md` for full tier logic.

- **Tier 1** — public web, official sites, news, filings, public social profiles. Automatic.
- **Tier 2** — rate-limited sources, registries, extended datasets. Only if enabled and useful.
- **Tier 3** — paid OSINT providers, background databases. Requires explicit permission grant.

## Output requirements

Markdown brief with: Executive Summary, Identity Resolution Notes, Findings, Risk and Uncertainty, Source Log. Every finding carries source-backed provenance.

## Inter-skill interfaces

Scout writes Signal files to Elephas intake: `~/openclaw/db/ocas-elephas/intake/{signal_id}.signal.json`

Emit one Signal file per confirmed entity or high-confidence relationship discovered during research. Use the Signal schema from `spec-ocas-shared-schemas.md`. Elephas decides promotion.

See `spec-ocas-interfaces.md` for signal format.

## Storage layout

```
~/openclaw/data/ocas-scout/
  config.json
  requests.jsonl
  sources.jsonl
  findings.jsonl
  decisions.jsonl
  briefs/
  reports/

~/openclaw/journals/ocas-scout/
  YYYY-MM-DD/
    {run_id}.json
```


Default config.json:
```json
{
  "skill_id": "ocas-scout",
  "skill_version": "2.3.0",
  "config_version": "1",
  "created_at": "",
  "updated_at": "",
  "waterfall": {
    "enabled_tiers": [1, 2]
  },
  "paid_sources": {
    "enabled": false
  },
  "brief": {
    "format": "markdown"
  },
  "retention": {
    "days": 90,
    "max_records": 10000
  }
}
```

## OKRs

Universal OKRs from spec-ocas-journal.md apply to all runs.

```yaml
skill_okrs:
  - name: verified_claim_ratio
    metric: fraction of findings with at least one verified source reference
    direction: maximize
    target: 0.70
    evaluation_window: 30_runs
  - name: entity_resolution_accuracy
    metric: fraction of identity resolutions confirmed correct
    direction: maximize
    target: 0.90
    evaluation_window: 30_runs
  - name: source_diversity
    metric: median unique source domains per brief
    direction: maximize
    target: 6
    evaluation_window: 30_runs
```

## Optional skill cooperation

- Weave — read social graph (read-only) for identity context
- Elephas — optionally emit Signal files for Chronicle promotion
- Sift — may use Sift for web searches during research

## Journal outputs

- Observation Journal — research runs producing findings
- Research Journal — structured multi-source research sessions

## Visibility

public

## Initialization

On first invocation of any Scout command, run `scout.init`:

1. Create `~/openclaw/data/ocas-scout/` and all subdirectories (`briefs/`, `reports/`)
2. Write default `config.json` with ConfigBase fields if absent
3. Create empty JSONL files: `requests.jsonl`, `sources.jsonl`, `findings.jsonl`, `decisions.jsonl`
4. Create `~/openclaw/journals/ocas-scout/`
5. Ensure `~/openclaw/db/ocas-elephas/intake/` exists (create if missing)
6. Register cron job `scout:update` if not already present (check `openclaw cron list` first)
7. Log initialization as a DecisionRecord in `decisions.jsonl`

## Background tasks

| Job name | Mechanism | Schedule | Command |
|---|---|---|---|
| `scout:update` | cron | `0 0 * * *` (midnight daily) | `scout.update` |

```
openclaw cron add --name scout:update --schedule "0 0 * * *" --command "scout.update" --sessionTarget isolated --lightContext true --timezone America/Los_Angeles
```


## Self-update

`scout.update` pulls the latest package from the `source:` URL in this file's frontmatter. Runs silently — no output unless the version changed or an error occurred.

1. Read `source:` from frontmatter → extract `{owner}/{repo}` from URL
2. Read local version from `skill.json`
3. Fetch remote version: `gh api "repos/{owner}/{repo}/contents/skill.json" --jq '.content' | base64 -d | python3 -c "import sys,json;print(json.load(sys.stdin)['version'])"`
4. If remote version equals local version → stop silently
5. Download and install:
   ```bash
   TMPDIR=$(mktemp -d)
   gh api "repos/{owner}/{repo}/tarball/main" > "$TMPDIR/archive.tar.gz"
   mkdir "$TMPDIR/extracted"
   tar xzf "$TMPDIR/archive.tar.gz" -C "$TMPDIR/extracted" --strip-components=1
   cp -R "$TMPDIR/extracted/"* ./
   rm -rf "$TMPDIR"
   ```
6. On failure → retry once. If second attempt fails, report the error and stop.
7. Output exactly: `I updated Scout from version {old} to {new}`

## Support file map

| File | When to read |
|---|---|
| `references/scout_schemas.md` | Before creating requests, findings, or briefs |
| `references/scout_source_waterfall.md` | Before tier selection or escalation decisions |
| `references/scout_brief_template.md` | Before rendering briefs |
| `references/journal.md` | Before scout.journal; at end of every run |
