# Layered Memory Layout Template

Use this as a default file/folder layout for a lightweight layered memory system.
Adjust naming to fit the workspace, but keep the boundary rules intact.

## Recommended structure

```text
MEMORY.md
memory/
  INDEX.md
  topics/
    <domain-or-project-family>/
      <topic>.md
  projects/
    <project-name>/
      README.md
      <artifacts>.md
  YYYY-MM-DD.md
  archive/
    <older-dailies-and-cold-notes>
  summaries/
    <generated-state-files>
```

## Layer mapping

### 1) `MEMORY.md`
Use for:
- identity
- preferences
- standing doctrine
- active priorities
- compact cross-project lessons

Rules:
- keep short
- avoid raw logs
- avoid live counters/status
- prefer summary bullets over narrative

### 2) `memory/INDEX.md`
Use for:
- cheap navigation to topic and project memory
- selector guidance for what to load first
- compact links to durable areas

Rules:
- do not duplicate full topic content here
- keep it as a front door, not another doctrine file

### 3) `memory/topics/`
Use for:
- durable doctrine
- architecture notes
- decisions
- recurring playbooks
- domain knowledge

Rules:
- organize by domain/project family when possible
- move stable cross-session detail here from daily/project notes
- do not use for raw transcripts or noisy logs

### 4) `memory/projects/`
Use for:
- project-scoped working memory
- migration plans
- raw research
- transcripts
- snapshots
- implementation-specific notes

Rules:
- keep project-local detail here until it earns promotion upward
- avoid stuffing cross-project doctrine into this layer

### 5) `memory/YYYY-MM-DD.md`
Use for:
- episodic logs
- what happened today
- observations
- intermediate findings
- next-step consequences

Rules:
- this is the default landing zone for fresh information
- promote later only if it becomes durable or cross-cutting

### 6) `memory/summaries/`
Use for:
- generated operator summaries
- queue/alert/health snapshots
- compact log digests
- rebuildable read models

Rules:
- derived state only
- do not treat as durable canon
- rewrite in place when the summary is meant to represent current truth

## Minimal adoption version
If the full structure feels heavy, start with:

```text
MEMORY.md
memory/
  INDEX.md
  topics/
  projects/
  YYYY-MM-DD.md
```

Then add generated summaries only when live-state questions become common.

## Key principle
The exact folder names matter less than the memory boundaries.
A good layered memory system separates:
- hot canon
- durable doctrine
- project-bound working memory
- episodic history
- generated live state
