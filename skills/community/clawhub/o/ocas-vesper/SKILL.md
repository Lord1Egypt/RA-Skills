---
name: ocas-vesper
source: https://github.com/indigokarasu/vesper
install: openclaw skill install https://github.com/indigokarasu/vesper
description: Use when generating morning or evening briefings, requesting an on-demand system brief, checking pending decisions, or configuring the briefing schedule. Aggregates signals from across the system into concise natural-language summaries. Trigger phrases: 'morning briefing', 'evening briefing', 'what's happening', 'daily brief', 'pending decisions', 'catch me up', 'update vesper'. Do not use for deep research (use Sift), pattern analysis (use Corvus), or message drafting (use Dispatch).
metadata: {"openclaw":{"emoji":"🌅"}}
---

# Vesper

Vesper is the system's daily voice — it aggregates signals from every other skill and presents what matters as a concise, conversational morning or evening briefing, surfacing concrete outcomes, upcoming decisions, and actionable opportunities without exposing any internal architecture or analysis processes. Its signal filtering is strict: routine background activity, speculative observations, and already-experienced events are excluded, so every briefing earns attention rather than demanding it.


## When to use

- Generate morning or evening briefing
- Request an on-demand briefing
- Check pending decision requests
- Configure briefing schedule or sections


## When not to use

- Deep research — use Sift
- Pattern analysis — use Corvus
- Message drafting — use Dispatch
- Action execution — use relevant domain skill


## Responsibility boundary

Vesper owns briefing generation, signal aggregation, and decision presentation.

Vesper does not own: pattern analysis (Corvus), web research (Sift), communications delivery (Dispatch), action decisions (Praxis).

Vesper receives InsightProposal files from Corvus. Vesper writes completed briefings to its `briefings/` directory; Dispatch picks them up and delivers them.

## Ontology types

Vesper aggregates signals and data from other skills for briefing generation. During aggregation, it observes entities that appear in briefing content:

- **Entity/Person** — people mentioned in briefings (from calendar events, messages, task assignments)
- **Concept/Event** — events and deadlines referenced in briefing sections (meetings, due dates, travel departures)
- **Place** — locations mentioned in briefing content (meeting venues, travel destinations, weather locations)

Vesper may reference entity names and types from Chronicle or other skill data in briefing content (read-only). Entity observations are recorded in journal outputs for downstream Chronicle ingestion.

## Commands

- `vesper.briefing.morning` — generate morning briefing
- `vesper.briefing.evening` — generate evening briefing
- `vesper.briefing.manual` — on-demand briefing
- `vesper.decisions.pending` — list unacted decision requests
- `vesper.config.set` — update schedule, sections, delivery
- `vesper.status` — last briefing time, pending decisions, schedule
- `vesper.journal` — write journal for the current run; called at end of every run
- `vesper.update` — pull latest from GitHub source; preserves journals and data


## Invocation modes

- **Automatic morning** — during configured morning window
- **Automatic evening** — during configured evening window
- **Manual** — on user request


## Signal filtering rules

Include: actionable information, meaningful outcomes, plan-affecting changes, multi-signal opportunities, preparation-useful information.

Exclude: routine background activity, already-experienced events, internal system reasoning, speculative observations.

Evening-specific: no past weather, no summaries of attended meetings.

Read `references/signal_filtering.md` for full rules.


## Formatting rules

- Output is plain text or minimal HTML suitable for Gmail rendering. No markdown syntax (#, **, ---).
- Conversational paragraphs, not bullet dumps.
- Section headers use monochrome extended characters: ▪ Today, ✉ Messages, ⚑ Logistics, ◈ Markets, ⟡ Decisions, ⚙ System.
- Sections with no content are omitted entirely. Do not render empty sections or "nothing to report" placeholders.
- Normal-state system health is silence, not confirmation. No "no flags", "systems normal", "all clear".
- Opening: "Good morning Jared" (no punctuation after greeting). Evening: "Good evening Jared".
- Weather follows greeting as narrative prose with emoji directly before each condition word. No location callout when at home. When traveling, prefix with location: "Here's what Tokyo looks like today."
- Weather includes: current temp and condition, 10am commute forecast, high, 4pm commute forecast, low. Friday briefings append a weekend forecast line.
- Links are inline: the relevant words become the anchor text. No trailing link labels. Calendar events link to gcal, locations link to Google Maps, message references link to Gmail threads, tracking items link to status pages.
- URI formats: gcal `https://calendar.google.com/calendar/event?eid={event_id}`, maps `https://maps.google.com/?q={place+name+address}`, gmail `https://mail.google.com/mail/u/0/#inbox/{thread_id}`.
- Markets (morning): "Portfolio closed yesterday at $XXX,XXX (±X.X%)". Markets (evening): "Portfolio opened at $XXX,XXX and closed at $XXX,XXX (±X.X%)". Notable movers only when movement is material.
- Decision requests: option, benefit, cost, framed as optional.
- Opportunities surfaced without exposing underlying analysis.
- When Vibes (ocas-vibes) is present, apply its voice and anti-AI rules to all briefing text.

Read `references/briefing_templates.md` for structure and examples.


## Run completion

After every briefing generation:

1. Read InsightProposal files from each skill's `proposals/` directory: `/workspace/openclaw/data/ocas-corvus/proposals/` and `/workspace/openclaw/data/ocas-custodian/proposals/`. Apply signal filtering to each. Track consumed `proposal_id` values in `signals_evaluated.jsonl` to avoid reprocessing on future runs.
2. Read Dispatch summary from `/workspace/openclaw/data/ocas-dispatch/reports/YYYY-MM-DD-{period}.json` if present (where `period` matches the briefing type: `morning` or `evening`). Use `high_priority_threads`, `pending_followups`, and `active_commitments` for the Messages section.
3. Read Rally daily report from `/workspace/openclaw/data/ocas-rally/reports/YYYY-MM-DD-daily.json` if present. Use for the Markets section.
4. Write briefing file to `/workspace/openclaw/data/ocas-vesper/briefings/YYYY-WXX/YYYY-MM-DD-{type}.json` using `VesperBriefingFile` schema. This is Dispatch's pickup source. Week directory format: ISO week e.g. `2026-W14`. Create the week directory if absent.
5. Persist briefing record and evaluated signals to local JSONL files
6. Log material decisions to `decisions.jsonl`
7. Write journal via `vesper.journal`

## Behavior constraints

- No nagging — ignored decisions are treated as intentional
- No internal system terminology
- No references to architecture or analysis processes
- No speculative observations
- Only concrete outcomes and actionable opportunities
- Silence on normal — if a system, section, or status has nothing noteworthy, omit it entirely rather than confirming normalcy


## Inter-skill interfaces

**Corvus → Vesper (cooperative read):** Corvus writes InsightProposal files to `/workspace/openclaw/data/ocas-corvus/proposals/{proposal_id}.json`. Vesper reads from this directory during briefing generation, applies signal filtering, and tracks consumed `proposal_id` values in its own `signals_evaluated.jsonl`. Corvus does not write to Vesper's directories. See `spec-ocas-interfaces.md` for the InsightProposal schema.

**Custodian → Vesper (cooperative read):** Custodian writes InsightProposal files (`anomaly_alert` type) to `/workspace/openclaw/data/ocas-custodian/proposals/{proposal_id}.json` on Tier 3/4 escalations. Vesper reads from this directory during briefing generation. Custodian does not write to Vesper's directories.

**Dispatch → Vesper (cooperative read):** Dispatch writes `DispatchSummaryReport` to `/workspace/openclaw/data/ocas-dispatch/reports/YYYY-MM-DD-{period}.json`. Vesper reads this during briefing generation. Dispatch does not write to Vesper's directories.

**Rally → Vesper (cooperative read):** Rally writes daily portfolio reports to `/workspace/openclaw/data/ocas-rally/reports/YYYY-MM-DD-daily.json`. Vesper reads this during briefing generation. Rally does not write to Vesper's directories.

**Vesper → Dispatch (cooperative read):** Vesper writes completed briefings to `/workspace/openclaw/data/ocas-vesper/briefings/YYYY-WXX/YYYY-MM-DD-{type}.json`. Dispatch reads this directory, identifies undelivered briefings, and delivers them. See `references/schemas.md` VesperBriefingFile.


## Storage layout

```
/workspace/openclaw/data/ocas-vesper/
  config.json
  briefings.jsonl
  signals_evaluated.jsonl
  decisions_presented.jsonl
  decisions.jsonl
  briefings/
    YYYY-WXX/
      YYYY-MM-DD-morning.json
      YYYY-MM-DD-evening.json

/workspace/openclaw/journals/ocas-vesper/
  YYYY-MM-DD/
    {run_id}.json
```


Default config.json:
```json
{
  "skill_id": "ocas-vesper",
  "skill_version": "2.7.0",
  "config_version": "1",
  "created_at": "",
  "updated_at": "",
  "schedule": {
    "morning_window": "07:00-09:00",
    "evening_window": "17:00-19:00",
    "timezone": "America/Los_Angeles"
  },
  "sections": {
    "today": true,
    "messages": true,
    "logistics": true,
    "markets": true,
    "decisions": true,
    "system": true
  },
  "retention": {
    "days": 30,
    "max_records": 10000
  }
}
```


## OKRs

Universal OKRs from spec-ocas-journal.md apply to all runs.

```yaml
skill_okrs:
  - name: signal_precision
    metric: fraction of included signals rated actionable by user
    direction: maximize
    target: 0.85
    evaluation_window: 30_runs
  - name: terminology_compliance
    metric: fraction of briefings free of internal system terminology
    direction: maximize
    target: 1.0
    evaluation_window: 30_runs
  - name: decision_framing
    metric: fraction of decision requests including option, benefit, and cost
    direction: maximize
    target: 1.0
    evaluation_window: 30_runs
```


## Optional skill cooperation

- Vibes — reads voice identity, channel rules, and anti-AI pattern references from ocas-vibes before generating briefing text. If Vibes is absent, Vesper generates without voice guidance.
- Corvus — reads InsightProposal files from Corvus's `proposals/` directory (cooperative read; Corvus owns its output)
- Custodian — reads InsightProposal files from Custodian's `proposals/` directory (cooperative read; Custodian owns its output)
- Dispatch — reads `DispatchSummaryReport` from `/workspace/openclaw/data/ocas-dispatch/reports/YYYY-MM-DD-{period}.json` for the Messages section (cooperative read; Dispatch owns its data). Dispatch picks up completed briefings from Vesper's `briefings/` directory for delivery.
- Rally — reads portfolio daily reports at `/workspace/openclaw/data/ocas-rally/reports/YYYY-MM-DD-daily.json` (cooperative read; Rally owns its data).
- Calendar/Weather — reads external context for briefing content
- Elephas — journal entity observations consumed during Chronicle ingestion


## Journal outputs

Action Journal — every briefing generation run.

When entities are encountered during a run, include structured entity observations in `decision.payload`:

- `entities_observed` — list of entities encountered (Entity/Person, Concept/Event, Place), each with type, name, and context
- `relationships_observed` — connections between entities (e.g., a person attending a meeting, an event at a location)
- `preferences_observed` — user preferences inferred from briefing interactions (e.g., sections the user engages with, decisions acted upon)

Each entity observation must include a `user_relevance` field:
- `user` — entity is directly related to the user's world (people from the user's calendar/tasks, the user's deadlines, the user's meeting locations). Most entities from the user's own calendar, task list, and messages are `user`-relevant.
- `agent_only` — entity encountered incidentally from external context (e.g., a public figure mentioned in a news item, a location from a weather feed, entities from aggregated external sources rather than the user's personal data)
- `unknown` — relevance is unclear


## Initialization

On first invocation of any Vesper command, run `vesper.init`:

1. Create `/workspace/openclaw/data/ocas-vesper/` and subdirectories (`briefings/`)
2. Write default `config.json` with ConfigBase fields if absent
3. Create empty JSONL files: `briefings.jsonl`, `signals_evaluated.jsonl`, `decisions_presented.jsonl`, `decisions.jsonl`
4. Create `/workspace/openclaw/journals/ocas-vesper/`
5. Register cron jobs `vesper:morning`, `vesper:evening`, and `vesper:update` if not already present (check `openclaw cron list` first)
6. Log initialization as a DecisionRecord in `decisions.jsonl`


## Background tasks

| Job name | Mechanism | Schedule | Command |
|---|---|---|---|
| `vesper:morning` | cron | `0 6 * * *` (daily 6am) | `vesper.briefing.morning` |
| `vesper:evening` | cron | `0 20 * * *` (daily 8pm) | `vesper.briefing.evening` |
| `vesper:update` | cron | `0 0 * * *` (midnight daily) | `vesper.update` |

Cron options: `sessionTarget: isolated`, `lightContext: true`, `wakeMode: next-heartbeat`.

Default times are 6am and 8pm PT. Override with `vesper.config.set morning_hour <H>` and `vesper.config.set evening_hour <H>`.

Registration during `vesper.init`:
```
openclaw cron list
# If vesper:morning absent:
openclaw cron add --name vesper:morning --schedule "0 6 * * *" --command "vesper.briefing.morning" --sessionTarget isolated --lightContext true --wakeMode next-heartbeat --timezone America/Los_Angeles
# If vesper:evening absent:
openclaw cron add --name vesper:evening --schedule "0 20 * * *" --command "vesper.briefing.evening" --sessionTarget isolated --lightContext true --wakeMode next-heartbeat --timezone America/Los_Angeles
# If vesper:update absent:
openclaw cron add --name vesper:update --schedule "0 0 * * *" --command "vesper.update" --sessionTarget isolated --lightContext true --timezone America/Los_Angeles
```


## Self-update

`vesper.update` pulls the latest package from the `source:` URL in this file's frontmatter. Runs silently — no output unless the version changed or an error occurred.

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
7. Output exactly: `I updated Vesper from version {old} to {new}`


## Visibility

public


## Support file map

| File | When to read |
|---|---|
| `references/schemas.md` | Before creating briefings, sections, or decision requests |
| `references/briefing_templates.md` | Before generating briefing content |
| `references/signal_filtering.md` | Before evaluating signals for inclusion |
| `references/journal.md` | Before vesper.journal; at end of every run |
