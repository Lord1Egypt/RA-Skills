---
name: Memory Management / Management System
slug: memory-management
version: 1.0.0
homepage: https://clawhub.com/skills/memory-management
description: "A practical memory management system for OpenClaw: importance scoring, time-decay cleanup, write triggers, hybrid retrieval, and daily maintenance workflow."
changelog: "Converted from workspace/memory/MANAGEMENT.md (importance scoring + decay + recall + daily maintenance)."
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

# Memory Management Skill

This skill provides a unified workflow to write, retrieve, and maintain long-term / topic-based / short-term memories across OpenClaw sessions.

---

## When to Use

Use it when you want the agent to consistently remember key preferences/decisions/facts across sessions, while preventing memory bloat via time-decay and daily cleanup.

---

## Target Workspace Layout (suggested)

Assume your workspace root is `~/.openclaw/workspace/`:

```text
workspace/
├── MEMORY.md
├── AGENTS.md        # optional
├── TOOLS.md         # optional
├── HEARTBEAT.md    # optional
└── memory/
    ├── preferences.md
    ├── decisions.md
    ├── projects.md
    ├── contacts.md
    ├── patterns.md
    ├── feedback.md
    └── YYYY-MM-DD.md
```

---

## Importance Scoring (1-5) before writing

When you are about to write a memory:
- `5`: write to `MEMORY.md` (core principles, key decisions, core preferences)
- `4`: write to `MEMORY.md` (important rules/lessons repeated multiple times)
- `3`: write to `memory/YYYY-MM-DD.md` (general tasks/conversation worth retrieving)
- `2`: write to `memory/YYYY-MM-DD.md` (temporary/optional records)
- `1`: do not record (small talk/meaningless content)

Strategy:
- De-duplicate / merge similar memories when possible
- Only persist when it will be useful for future retrieval or reuse

---

## Time Decay & Cleanup (30+ days)

Short-term memory relevance decays with time:
- Same day: 1.0
- 1-7 days: 0.8
- 8-30 days: 0.5
- 30+ days: 0 (clean/archive during daily maintenance)

Cleanup workflow:
1. Scan `memory/*.md` daily logs
2. For files older than 30 days: migrate worth-keeping content into `MEMORY.md` or topic files; delete/archive the rest

---

## Manual Triggers (immediate write)

When the user says:
- "remember this" / "save this": evaluate importance and write to the right place
- "don't forget" / "permanently save": write to `MEMORY.md`
- "this is an important point": write to `MEMORY.md`
- "write to memory": write by type:
  - preferences -> `memory/preferences.md`
  - decisions -> `memory/decisions.md`
  - projects -> `memory/projects.md`
  - contacts -> `memory/contacts.md`
  - patterns / best practices -> `memory/patterns.md`
  - feedback -> `memory/feedback.md`

---

## Auto Recall (retrieve then answer)

Before answering questions about previous work/decisions/dates/people/preferences/tasks:
1. Run `memory_search` with the user query
2. If your system supports it, refine quotes with `memory_get`
3. If retrieval is insufficient, do not fabricate; tell the user you checked memory but found no strong evidence

---

## Retrieval (hybrid: vector + keywords)

Use hybrid retrieval to balance semantic match and keyword precision (vector semantics + FTS terms).

Example:
```bash
openclaw memory search "query"
```

---

## Daily Maintenance Workflow

Suggested time: `08:30` (adjust for your timezone).

Goals:
- Ensure `memory/YYYY-MM-DD.md` exists
- Review yesterday and extract long-term-worthy content into `MEMORY.md` / topic files
- Clean logs older than 30 days
- Optionally generate a short report

---

## Cron Job Template (maintenance)

```json
{
  "schedule": { "kind": "cron", "expr": "30 8 * * *", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "Run the daily memory maintenance workflow: create today's log, review yesterday, migrate worth-keeping content to MEMORY/topic files, then clean logs older than 30 days and output a concise structured report.",
    "model": "YOUR_DEFAULT_MODEL",
    "timeoutSeconds": 600
  }
}
```

---

## Safety & Preconditions

Safety:
- Do not write sensitive information (accounts/keys/private content) into shared or long-term memory.

Preconditions:
- `memorySearch` is enabled
- Workspace has the expected layout (`MEMORY.md` + `memory/` logs)
- Daily maintenance is scheduled (cron or equivalent)

---

## Related Skills

- `memory-setup`: configure persistent memorySearch
- `self-improvement`: turn errors/corrections into learnable experiences
- `cron-mastery`: cron vs heartbeat time scheduling best practices

---

## Feedback

- If useful: `clawhub star memory-management`
- Stay updated: `clawhub sync`

---
name: Memory Management / Management System
slug: memory-management
version: 1.0.0
homepage: https://clawhub.com/skills/memory-management
description: "A complete, practical memory management system: file layout, importance scoring, time-decay cleanup, write-trigger rules, hybrid retrieval, and daily maintenance workflow for OpenClaw."
changelog: "Initial release converted from workspace/memory/MANAGEMENT.md (importance scoring + decay + recall + daily maintenance)."
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

# Memory Management Skill

This is a practical "memory management system" skill for OpenClaw. It provides a unified set of rules to write, retrieve, and maintain long-term / topic-based / short-term memories across sessions.

It turns the following capabilities into a clear workflow:
- Evaluate an "importance score" before writing, and decide where to store the memory
- Use time-decay for short-term memories, and clean them during daily maintenance
- Provide manual trigger phrases (e.g. "remember this") to persist immediately
- Provide hybrid retrieval (vector semantics + keywords)
- Run a daily maintenance workflow (create daily file, review yesterday, update MEMORY, clean old logs, generate a report)

---

## When to Use

Use this skill when you need:
- The agent to reliably "remember key preferences/decisions/important facts" across multiple sessions
- To prevent meaningless chat from filling up memory files
- Retrieval quality to decay over time (newer items are more relevant; old items are cleaned automatically)
- Daily memory maintenance to run automatically (instead of embedding all logic into every conversation)

---

## Target Workspace Layout

Assume your workspace root directory is `~/.openclaw/workspace/`. Use the following structure:

```text
workspace/
├── MEMORY.md                      # long-term memory (core knowledge base; keep maintenance focused)
├── AGENTS.md                      # agent behavior / calling constraints snippet (optional)
├── TOOLS.md                       # tools / skill index (optional)
├── HEARTBEAT.md                   # heartbeat task (optional)
└── memory/
    ├── preferences.md             # user preferences
    ├── decisions.md               # important decisions
    ├── projects.md                # project information
    ├── contacts.md                # contacts
    ├── patterns.md                # best practices / patterns
    ├── feedback.md                # feedback records
    └── YYYY-MM-DD.md            # daily logs (short-term memory)
```

---

## Memory File Templates (recommended templates)

You can start with minimal templates. Later maintenance tasks only need to update small blocks or append a few bullet points.

`MEMORY.md` (example structure):

```markdown
# MEMORY.md — Long-Term Memory

## About
- User core preferences:
- Important identity / background:

## Active Projects
- Project name: status / key milestones / current risks

## Decisions & Lessons
- Key decisions (why chosen):
- Lessons learned (avoid repeating mistakes):

## Preferences
- Communication style:
- Tool preferences:
- Avoided behaviors:
```

`memory/preferences.md`:

```markdown
# preferences.md

## Communication
- Preference:

## Tools & Workflows
- Common tools:
- Typical workflows:
```

`memory/decisions.md`:

```markdown
# decisions.md

## Key Decisions
- Decision point:
- Background:
- Why this approach:
- Possible future adjustments:
```

`memory/patterns.md`:

```markdown
# patterns.md

## Best Practices
- Pattern name:
- When to use:
- Step-by-step:
- Failure examples (optional):
```

---

## Importance Scoring (1-5) before writing

Rule: when you are about to "write to memory", first score the content (1-5), then decide where to store it.

Suggested mapping:
- 5 points: write to `MEMORY.md`
  - core principles, key decisions, user's core preferences
- 4 points: write to `MEMORY.md`
  - important rules and lessons repeated multiple times
- 3 points: write to `memory/YYYY-MM-DD.md`
  - general tasks and normal conversation content worth retrieving, but not long-term
- 2 points: write to `memory/YYYY-MM-DD.md`
  - temporary info / optional records
- 1 point: do not record
  - small talk / meaningless content

Suggested write strategy:
- De-duplicate / merge the same memory when possible to avoid endless appends
- Only persist when it is worth future retrieval / reuse

---

## Time Decay & Cleanup (30+ days)

Short-term memory retrieval weight decays over time:
- Same day: active (weight 1.0)
- 1-7 days: recent (weight 0.8)
- 8-30 days: mid-term (weight 0.5)
- 30+ days: expired (weight 0; clean / archive during daily maintenance)

Daily maintenance cleanup workflow (recommended):
1. Scan all `YYYY-MM-DD.md` files under `memory/`
2. For files older than 30 days:
   - If there is "worth keeping" content, extract it into `MEMORY.md` (or topic files)
   - Otherwise delete / archive

---

## Manual Triggers (immediate write)

When the user says the following phrases, immediately start "write evaluation" and persist (after scoring importance):
- "remember this" / "save this": evaluate importance and write to the corresponding place
- "don't forget" / "permanently save": write directly to `MEMORY.md`
- "this is an important point": write directly to `MEMORY.md`
- "write to memory": write by content type:
  - preferences -> `memory/preferences.md`
  - decisions -> `memory/decisions.md`
  - projects -> `memory/projects.md`
  - contacts -> `memory/contacts.md`
  - patterns / best practices -> `memory/patterns.md`
  - feedback -> `memory/feedback.md`

---

## Auto Recall (retrieve then answer)

When a user question belongs to these categories, first perform memory retrieval, then answer:
- Asking about previous work/decisions/dates/people/preferences/tasks
- Needs to reference or extend previous information

Suggested retrieval chain:
1. Use `memory_search` to search relevant memories by query
2. If your system supports it, use `memory_get` to pull more precise excerpts for quoting
3. If confidence is still not enough: be transparent and say you checked memories but couldn't find sufficient relevant evidence

---

## Retrieval (hybrid retrieval: vector semantics + keywords)

Suggested strategy: hybrid retrieval (vector semantics + FTS keywords).

You can configure similar parameters in OpenClaw's memorySearch configuration:
- Provider: `voyage` (or your actual vector provider)
- sources: `["memory", "sessions"]` (adjust as needed)
- indexMode: `"hot"` (real-time updates; adjust if needed)
- minScore: start from `0.3` (lower = more results)
- maxResults: start from `20`

Manual retrieval example (if your system supports it):

```bash
openclaw memory search "query"
```

---

## Daily Maintenance Workflow (daily review / maintenance)

Suggested daily execution time: `08:30` (adjust for your timezone).

Maintenance goals:
- Create today's log: `memory/YYYY-MM-DD.md`
- Review yesterday's log: extract content worth long-termizing into `preferences.md / decisions.md / patterns.md / MEMORY.md`
- Clean old logs older than 30 days (optional but recommended)
- Generate a report (optional: send to Lark/IM or output to console only)

Maintenance flow (6-7 steps):
1. Optional system/gateway status checks
2. Optional model status checks
3. Optional API configuration checks
4. Configuration backups:
   - Backup: `openclaw.json -> openclaw.json.backup-YYYYMMDD`
   - Backup retention: keep at most the last 3 backups
   - Sync/update independent backups for API keys (if you have files like `.api-keys-backup.env`)
5. Create today's log file if it doesn't exist
6. Review yesterday: extract key preferences/decisions/lessons and update MEMORY or topic files
7. Clean old logs (30+ days) and migrate "worth keeping" content before deleting

Backup shell command examples (you can copy into your cron payload):

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup-$(date +%Y%m%d)
ls -t ~/.openclaw/openclaw.json.backup-* | tail -n +4 | xargs -r rm
cp ~/.openclaw/openclaw.json ~/.openclaw/.api-keys-backup.env
```

---

## Cron Job Template (run maintenance)

In OpenClaw's cron jobs, a recommended pattern is: "isolated session + scheduled trigger + only maintenance tasks".

Example payload (showing the core fields you need to pay attention to: `schedule` and `payload.message`; the rest depends on your environment):

```json
{
  "schedule": { "kind": "cron", "expr": "30 8 * * *", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "Run the daily memory maintenance workflow (7 steps): 1) Create memory/YYYY-MM-DD.md (if missing) 2) Review yesterday's memory and extract content worth long-termizing into MEMORY.md or topic files 3) Delete logs older than 30 days (migrate important content before deleting) 4) Optionally back up openclaw.json (keep last 3) 5) Generate a concise structured report with findings and recommendations.\\nRequirement: output must be structured and concise, focusing on maintenance results.",
    "model": "YOUR_DEFAULT_MODEL",
    "timeoutSeconds": 600
  }
}
```

Notes:
- Replace `YOUR_DEFAULT_MODEL` with your default model
- If you don't need to send to Lark, just output the report to the default channel / return content only

---

## AGENTS.md Snippet (copy/paste)

Add the following snippet to your `AGENTS.md` (or whichever document constrains agent behavior):

```markdown
### 🧠 Memory Management Rules (Memory Management Skill)

1) Auto recall:
Before answering questions about previous work/decisions/dates/people/preferences/tasks, run `memory_search` first.
If retrieval is still uncertain, explain in the response that you checked memory but couldn't find enough evidence.

2) Manual write triggers:
When the user says: "remember this" / "save this" / "don't forget" / "permanently save" / "this is an important point" / "write to memory"
First evaluate the importance score (1-5), then write:
- 5-4 points: write to `MEMORY.md`
- 3-2 points: write to `memory/YYYY-MM-DD.md`
- 1 point: do not record

3) Time decay and cleanup:
Daily maintenance will clean logs older than 30 days; before deleting, migrate worth-keeping content to `MEMORY.md` or topic files.

4) Retrieval strategy:
Prefer hybrid retrieval (vector semantics + FTS keywords).
```

---

## Safety & Preconditions

Safety advice:
- Do not write sensitive information (accounts, keys, private content) into publicly shared memory.
- Only store information in `MEMORY.md` when you explicitly need it and it is controllable (long-term storage is more sensitive).

Run prerequisites (recommended):
- Your OpenClaw has `memorySearch` enabled (otherwise "retrieval/recall" will not work)
- Your workspace is created with the expected layout: `MEMORY.md` + `memory/` log directory
- Daily maintenance is configured or planned (cron or equivalent mechanism)

---

## Related Skills

- `memory-setup`: configure persistent `memorySearch` (vector retrieval foundation)
- `self-improvement`: turn errors/corrections into learnable experiences
- `cron-mastery`: cron vs heartbeat time scheduling best practices
- `clawdhub`: install/update/publish skills

---

## Feedback

- If useful: `clawhub star memory-management`
- Stay updated: `clawhub sync`

---
name: Memory Management / Management System
slug: memory-management
version: 1.0.0
homepage: https://clawhub.com/skills/memory-management
description: "A complete, practical memory management system: file layout, importance scoring, time-decay cleanup, write-trigger rules, hybrid retrieval, and daily maintenance workflow for OpenClaw."
changelog: "Initial release converted from workspace/memory/MANAGEMENT.md (importance scoring + decay + recall + daily maintenance)."
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

# Memory Management Skill

This is a practical "memory management system" skill for OpenClaw. It provides a unified set of rules to write, retrieve, and maintain long-term / topic-based / short-term memories across sessions.

It turns the following capabilities into a clear workflow:
- Evaluate an "importance score" before writing, and decide where to store the memory
- Use time-decay for short-term memories, and clean them during daily maintenance
- Provide manual trigger phrases (e.g. "remember this") to persist immediately
- Provide hybrid retrieval (vector semantics + keywords)
- Run a daily maintenance workflow (create daily file, review yesterday, update MEMORY, clean old logs, generate a report)

---

## When to Use

Use this skill when you need:
- The agent to reliably "remember key preferences/decisions/important facts" across multiple sessions
- To prevent meaningless chat from filling up memory files
- Retrieval quality to decay over time (newer items are more relevant; old items are cleaned automatically)
- Daily memory maintenance to run automatically (instead of embedding all logic into every conversation)

---

## Target Workspace Layout

Assume your workspace root directory is `~/.openclaw/workspace/`. Use the following structure:

```text
workspace/
├── MEMORY.md                      # long-term memory (core knowledge base; keep maintenance focused)
├── AGENTS.md                      # agent behavior / calling constraints snippet (optional)
├── TOOLS.md                       # tools / skill index (optional)
├── HEARTBEAT.md                   # heartbeat task (optional)
└── memory/
    ├── preferences.md             # user preferences
    ├── decisions.md               # important decisions
    ├── projects.md                # project information
    ├── contacts.md                # contacts
    ├── patterns.md                # best practices / patterns
    ├── feedback.md                # feedback records
    └── YYYY-MM-DD.md            # daily logs (short-term memory)
```

---

## Memory File Templates (recommended templates)

You can start with minimal templates. Later maintenance tasks only need to update small blocks or append a few bullet points.

`MEMORY.md` (example structure):

```markdown
# MEMORY.md — Long-Term Memory

## About
- User core preferences:
- Important identity / background:

## Active Projects
- Project name: status / key milestones / current risks

## Decisions & Lessons
- Key decisions (why chosen):
- Lessons learned (avoid repeating mistakes):

## Preferences
- Communication style:
- Tool preferences:
- Avoided behaviors:
```

`memory/preferences.md`:

```markdown
# preferences.md

## Communication
- Preference:

## Tools & Workflows
- Common tools:
- Typical workflows:
```

`memory/decisions.md`:

```markdown
# decisions.md

## Key Decisions
- Decision point:
- Background:
- Why this approach:
- Possible future adjustments:
```

`memory/patterns.md`:

```markdown
# patterns.md

## Best Practices
- Pattern name:
- When to use:
- Step-by-step:
- Failure examples (optional):
```

---

## Importance Scoring (1-5) before writing

Rule: when you are about to "write to memory", first score the content (1-5), then decide where to store it.

Suggested mapping:
- 5 points: write to `MEMORY.md`
  - core principles, key decisions, user's core preferences
- 4 points: write to `MEMORY.md`
  - important rules and lessons repeated multiple times
- 3 points: write to `memory/YYYY-MM-DD.md`
  - general tasks and normal conversation content worth retrieving, but not long-term
- 2 points: write to `memory/YYYY-MM-DD.md`
  - temporary info / optional records
- 1 point: do not record
  - small talk / meaningless content

Suggested write strategy:
- De-duplicate / merge the same memory when possible to avoid endless appends
- Only persist when it is worth future retrieval / reuse

---

## Time Decay & Cleanup (30+ days)

Short-term memory retrieval weight decays over time:
- Same day: active (weight 1.0)
- 1-7 days: recent (weight 0.8)
- 8-30 days: mid-term (weight 0.5)
- 30+ days: expired (weight 0; clean / archive during daily maintenance)

Daily maintenance cleanup workflow (recommended):
1. Scan all `YYYY-MM-DD.md` files under `memory/`
2. For files older than 30 days:
   - If there is "worth keeping" content, extract it into `MEMORY.md` (or topic files)
   - Otherwise delete / archive

---

## Manual Triggers (immediate write)

When the user says the following phrases, immediately start "write evaluation" and persist (after scoring importance):
- "remember this" / "save this": evaluate importance and write to the corresponding place
- "don't forget" / "permanently save": write directly to `MEMORY.md`
- "this is an important point": write directly to `MEMORY.md`
- "write to memory": write by content type:
  - preferences -> `memory/preferences.md`
  - decisions -> `memory/decisions.md`
  - projects -> `memory/projects.md`
  - contacts -> `memory/contacts.md`
  - patterns / best practices -> `memory/patterns.md`
  - feedback -> `memory/feedback.md`

---

## Auto Recall (retrieve then answer)

When a user question belongs to these categories, first perform memory retrieval, then answer:
- Asking about previous work/decisions/dates/people/preferences/tasks
- Needs to reference or extend previous information

Suggested retrieval chain:
1. Use `memory_search` to search relevant memories by query
2. If your system supports it, use `memory_get` to pull more precise excerpts for quoting
3. If confidence is still not enough: be transparent and say you checked memories but couldn't find sufficient relevant evidence

---

## Retrieval (hybrid retrieval: vector semantics + keywords)

Suggested strategy: hybrid retrieval (vector semantics + FTS keywords).

You can configure similar parameters in OpenClaw's memorySearch configuration:
- Provider: `voyage` (or your actual vector provider)
- sources: `["memory", "sessions"]` (adjust as needed)
- indexMode: `"hot"` (real-time updates; adjust if needed)
- minScore: start from `0.3` (lower = more results)
- maxResults: start from `20`

Manual retrieval example (if your system supports it):

```bash
openclaw memory search "query"
```

---

## Daily Maintenance Workflow (daily review / maintenance)

Suggested daily execution time: `08:30` (adjust for your timezone).

Maintenance goals:
- Create today's log: `memory/YYYY-MM-DD.md`
- Review yesterday's log: extract content worth long-termizing into `preferences.md / decisions.md / patterns.md / MEMORY.md`
- Clean old logs older than 30 days (optional but recommended)
- Generate a report (optional: send to Lark/IM or output to console only)

Maintenance flow (6-7 steps):
1. Optional system/gateway status checks
2. Optional model status checks
3. Optional API configuration checks
4. Configuration backups:
   - Backup: `openclaw.json -> openclaw.json.backup-YYYYMMDD`
   - Backup retention: keep at most the last 3 backups
   - Sync/update independent backups for API keys (if you have files like `.api-keys-backup.env`)
5. Create today's log file if it doesn't exist
6. Review yesterday: extract key preferences/decisions/lessons and update MEMORY or topic files
7. Clean old logs (30+ days) and migrate "worth keeping" content before deleting

Backup shell command examples (you can copy into your cron payload):

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup-$(date +%Y%m%d)
ls -t ~/.openclaw/openclaw.json.backup-* | tail -n +4 | xargs -r rm
cp ~/.openclaw/openclaw.json ~/.openclaw/.api-keys-backup.env
```

---

## Cron Job Template (run maintenance)

In OpenClaw's cron jobs, a recommended pattern is: "isolated session + scheduled trigger + only maintenance tasks".

Example payload (showing the core fields you need to pay attention to: `schedule` and `payload.message`; the rest depends on your environment):

```json
{
  "schedule": { "kind": "cron", "expr": "30 8 * * *", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "Run the daily memory maintenance workflow (7 steps): 1) Create memory/YYYY-MM-DD.md (if missing) 2) Review yesterday's memory and extract content worth long-termizing into MEMORY.md or topic files 3) Delete logs older than 30 days (migrate important content before deleting) 4) Optionally back up openclaw.json (keep last 3) 5) Generate a concise structured report with findings and recommendations.\\nRequirement: output must be structured and concise, focusing on maintenance results.",
    "model": "YOUR_DEFAULT_MODEL",
    "timeoutSeconds": 600
  }
}
```

Notes:
- Replace `YOUR_DEFAULT_MODEL` with your default model
- If you don't need to send to Lark, just output the report to the default channel / return content only

---

## AGENTS.md Snippet (copy/paste)

Add the following snippet to your `AGENTS.md` (or whichever document constrains agent behavior):

```markdown
### 🧠 Memory Management Rules (Memory Management Skill)

1) Auto recall:
Before answering questions about previous work/decisions/dates/people/preferences/tasks, run `memory_search` first.
If retrieval is still uncertain, explain in the response that you checked memory but couldn't find enough evidence.

2) Manual write triggers:
When the user says: "remember this" / "save this" / "don't forget" / "permanently save" / "this is an important point" / "write to memory"
First evaluate the importance score (1-5), then write:
- 5-4 points: write to `MEMORY.md`
- 3-2 points: write to `memory/YYYY-MM-DD.md`
- 1 point: do not record

3) Time decay and cleanup:
Daily maintenance will clean logs older than 30 days; before deleting, migrate worth-keeping content to `MEMORY.md` or topic files.

4) Retrieval strategy:
Prefer hybrid retrieval (vector semantics + FTS keywords).
```

---

## Safety & Preconditions

Safety advice:
- Do not write sensitive information (accounts, keys, private content) into publicly shared memory.
- Only store information in `MEMORY.md` when you explicitly need it and it is controllable (long-term storage is more sensitive).

Run prerequisites (recommended):
- Your OpenClaw has `memorySearch` enabled (otherwise "retrieval/recall" will not work)
- Your workspace is created with the expected layout: `MEMORY.md` + `memory/` log directory
- Daily maintenance is configured or planned (cron or equivalent mechanism)

---

## Related Skills

- `memory-setup`: configure persistent `memorySearch` (vector retrieval foundation)
- `self-improvement`: turn errors/corrections into learnable experiences
- `cron-mastery`: cron vs heartbeat time scheduling best practices
- `clawdhub`: install/update/publish skills

---

## Feedback

- If useful: `clawhub star memory-management`
- Stay updated: `clawhub sync`

<!--
---
name: Memory Management / Management System
slug: memory-management
version: 1.0.0
homepage: https://clawhub.com/skills/memory-management
description: "A complete, practical memory management system: file layout, importance scoring, time-decay cleanup, write-trigger rules, hybrid retrieval, and daily maintenance workflow for OpenClaw."
changelog: "Initial release converted from workspace/memory/MANAGEMENT.md (importance scoring + decay + recall + daily maintenance)."
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

# Memory Management Skill

This is a practical "memory management system" skill for OpenClaw. It provides a unified set of rules to write, retrieve, and maintain long-term / topic-based / short-term memories across sessions.

It turns the following capabilities into a clear workflow:
- Evaluate an "importance score" before writing, and decide where to store the memory
- Use time-decay for short-term memories, and clean them during daily maintenance
- Provide manual trigger phrases (e.g. "remember this") to persist immediately
- Provide hybrid retrieval (vector semantics + keywords)
- Run a daily maintenance workflow (create daily file, review yesterday, update MEMORY, clean old logs, generate a report)

---

## When to Use

Use this skill when you need:
- The agent to reliably "remember key preferences/decisions/important facts" across multiple sessions
- To prevent meaningless chat from filling up memory files
- Retrieval quality to decay over time (newer items are more relevant; old items are cleaned automatically)
- Daily memory maintenance to run automatically (instead of embedding all logic into every conversation)

---

## Target Workspace Layout

Assume your workspace root directory is `~/.openclaw/workspace/`. Use the following structure:

```text
workspace/
├── MEMORY.md                      # long-term memory (core knowledge base; keep maintenance focused)
├── AGENTS.md                      # agent behavior / calling constraints snippet (optional)
├── TOOLS.md                       # tools / skill index (optional)
├── HEARTBEAT.md                   # heartbeat task (optional)
└── memory/
    ├── preferences.md             # user preferences
    ├── decisions.md               # important decisions
    ├── projects.md                # project information
    ├── contacts.md                # contacts
    ├── patterns.md                # best practices / patterns
    ├── feedback.md                # feedback records
    └── YYYY-MM-DD.md            # daily logs (short-term memory)
```

---

## Memory File Templates (recommended templates)

You can start with minimal templates. Later maintenance tasks only need to update small blocks or append a few bullet points.

`MEMORY.md` (example structure):

```markdown
# MEMORY.md — Long-Term Memory

## About
- User core preferences:
- Important identity / background:

## Active Projects
- Project name: status / key milestones / current risks

## Decisions & Lessons
- Key decisions (why chosen):
- Lessons learned (avoid repeating mistakes):

## Preferences
- Communication style:
- Tool preferences:
- Avoided behaviors:
```

`memory/preferences.md`:

```markdown
# preferences.md

## Communication
- Preference:

## Tools & Workflows
- Common tools:
- Typical workflows:
```

`memory/decisions.md`:

```markdown
# decisions.md

## Key Decisions
- Decision point:
- Background:
- Why this approach:
- Possible future adjustments:
```

`memory/patterns.md`:

```markdown
# patterns.md

## Best Practices
- Pattern name:
- When to use:
- Step-by-step:
- Failure examples (optional):
```

---

## Importance Scoring (1-5) before writing

Rule: when you are about to "write to memory", first score the content (1-5), then decide where to store it.

Suggested mapping:
- 5 points: write to `MEMORY.md`
  - core principles, key decisions, user's core preferences
- 4 points: write to `MEMORY.md`
  - important rules and lessons repeated multiple times
- 3 points: write to `memory/YYYY-MM-DD.md`
  - general tasks and normal conversation content (worth retrieving, but not long-term)
- 2 points: write to `memory/YYYY-MM-DD.md`
  - temporary info / optional records
- 1 point: do not record
  - small talk / meaningless content

Suggested write strategy:
- De-duplicate / merge the same memory when possible to avoid endless appends
- Only persist when it is worth future retrieval / reuse

---

## Time Decay & Cleanup (30+ days)

Short-term memory retrieval weight decays over time:
- Same day: active (weight 1.0)
- 1-7 days: recent (weight 0.8)
- 8-30 days: mid-term (weight 0.5)
- 30+ days: expired (weight 0; clean / archive during daily maintenance)

Daily maintenance cleanup workflow (recommended):
1. Scan all `YYYY-MM-DD.md` files under `memory/`
2. For files older than 30 days:
   - If there is "worth keeping" content, extract it into `MEMORY.md` (or topic files)
   - Otherwise delete / archive

---

## Manual Triggers (immediate write)

When the user says the following phrases, immediately start "write evaluation" and persist (after scoring importance):
- "remember this" / "save this": evaluate importance and write to the corresponding place
- "don't forget" / "permanently save": write directly to `MEMORY.md`
- "this is an important point": write directly to `MEMORY.md`
- "write to memory": write by content type:
  - preferences -> `memory/preferences.md`
  - decisions -> `memory/decisions.md`
  - projects -> `memory/projects.md`
  - contacts -> `memory/contacts.md`
  - patterns / best practices -> `memory/patterns.md`
  - feedback -> `memory/feedback.md`

---

## Auto Recall (retrieve then answer)

When a user question belongs to these categories, first perform memory retrieval, then answer:
- Asking about previous work/decisions/dates/people/preferences/tasks
- Needs to reference or extend previous information

Suggested retrieval chain:
1. Use `memory_search` to search relevant memories by query
2. If your system supports it, use `memory_get` to pull more precise excerpts for quoting
3. If confidence is still not enough: be transparent and say you checked memories but couldn't find sufficient relevant evidence

---

## Retrieval (hybrid retrieval: vector semantics + keywords)

Suggested strategy: hybrid retrieval (vector semantics + FTS keywords).

You can configure similar parameters in OpenClaw's memorySearch configuration:
- Provider: `voyage` (or your actual vector provider)
- sources: `["memory", "sessions"]` (adjust as needed)
- indexMode: `"hot"` (real-time updates; adjust if needed)
- minScore: start from `0.3` (lower = more results)
- maxResults: start from `20`

Manual retrieval example (if your system supports it):

```bash
openclaw memory search "query"
```

---

## Daily Maintenance Workflow (daily review / maintenance)

Suggested daily execution time: `08:30` (adjust for your timezone).

Maintenance goals:
- Create today's log: `memory/YYYY-MM-DD.md`
- Review yesterday's log: extract content worth long-termizing into `preferences.md / decisions.md / patterns.md / MEMORY.md`
- Clean old logs older than 30 days (optional but recommended)
- Generate a report (optional: send to Lark/IM or output to console only)

Maintenance flow (6-7 steps):
1. Optional system/gateway status checks
2. Optional model status checks
3. Optional API configuration checks
4. Configuration backups:
   - Backup: `openclaw.json -> openclaw.json.backup-YYYYMMDD`
   - Backup retention: keep at most the last 3 backups
   - Sync/update independent backups for API keys (if you have files like `.api-keys-backup.env`)
5. Create today's log file if it doesn't exist
6. Review yesterday: extract key preferences/decisions/lessons and update MEMORY or topic files
7. Clean old logs (30+ days) and migrate "worth keeping" content before deleting

Backup shell command examples (you can copy into your cron payload):

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup-$(date +%Y%m%d)
ls -t ~/.openclaw/openclaw.json.backup-* | tail -n +4 | xargs -r rm
cp ~/.openclaw/openclaw.json ~/.openclaw/.api-keys-backup.env
```

---

## Cron Job Template (run maintenance)

In OpenClaw's cron jobs, a recommended pattern is: "isolated session + scheduled trigger + only maintenance tasks".

Example payload (showing the core fields you need to pay attention to: `schedule` and `payload.message`; the rest depends on your environment):

```json
{
  "schedule": { "kind": "cron", "expr": "30 8 * * *", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "Run the daily memory maintenance workflow (7 steps): 1) Create memory/YYYY-MM-DD.md (if missing) 2) Review yesterday's memory and extract content worth long-termizing into MEMORY.md or topic files 3) Delete logs older than 30 days (migrate important content before deleting) 4) Optionally back up openclaw.json (keep last 3) 5) Generate a concise structured report with findings and recommendations.\\nRequirement: output must be structured and concise, focusing on maintenance results.",
    "model": "YOUR_DEFAULT_MODEL",
    "timeoutSeconds": 600
  }
}
```

Notes:
- Replace `YOUR_DEFAULT_MODEL` with your default model
- If you don't need to send to Lark, just output the report to the default channel / return content only

---

## AGENTS.md Snippet (copy/paste)

Add the following snippet to your `AGENTS.md` (or whichever document constrains agent behavior):

```markdown
### 🧠 Memory Management Rules (Memory Management Skill)

1) Auto recall:
Before answering questions about previous work/decisions/dates/people/preferences/tasks, run `memory_search` first.
If retrieval is still uncertain, explain in the response that you checked memory but couldn't find enough evidence.

2) Manual write triggers:
When the user says: "remember this" / "save this" / "don't forget" / "permanently save" / "this is an important point" / "write to memory"
First evaluate the importance score (1-5), then write:
- 5-4 points: write to `MEMORY.md`
- 3-2 points: write to `memory/YYYY-MM-DD.md`
- 1 point: do not record

3) Time decay and cleanup:
Daily maintenance will clean logs older than 30 days; before deleting, migrate worth-keeping content to `MEMORY.md` or topic files.

4) Retrieval strategy:
Prefer hybrid retrieval (vector semantics + FTS keywords).
```

---

## Safety & Preconditions

Safety advice:
- Do not write sensitive information (accounts, keys, private content) into publicly shared memory.
- Only store information in `MEMORY.md` when you explicitly need it and it is controllable (long-term storage is more sensitive).

Run prerequisites (recommended):
- Your OpenClaw has `memorySearch` enabled (otherwise "retrieval/recall" will not work)
- Your workspace is created with the expected layout: `MEMORY.md` + `memory/` log directory
- Daily maintenance is configured or planned (cron or equivalent mechanism)

---

## Related Skills

- `memory-setup`: configure persistent `memorySearch` (vector retrieval foundation)
- `self-improvement`: turn errors/corrections into learnable experiences
- `cron-mastery`: cron vs heartbeat time scheduling best practices
- `clawdhub`: install/update/publish skills

---

## Feedback

- If useful: `clawhub star memory-management`
- Stay updated: `clawhub sync`

---
name: Memory Management / Management System
slug: memory-management
version: 1.0.0
homepage: https://clawhub.com/skills/memory-management
description: "A complete, practical memory management system: file layout, importance scoring, time-decay cleanup, write-trigger rules, hybrid retrieval, and daily maintenance workflow for OpenClaw."
changelog: "Initial release converted from workspace/memory/MANAGEMENT.md (importance scoring + decay + recall + daily maintenance)."
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

# Memory Management Skill

这是一个可落地的“记忆管理体系” skill，用来把 OpenClaw 的长期/专题/短期记忆按统一规则写入、检索与维护。

它把以下能力做成一套明确流程：
- 写入时先评估“重要性分数”，再决定写到哪里
- 短期记忆按时间衰减，并可在每日维护时清理
- 提供手动触发词（用户说“记下来/记住这个”等）立即落盘
- 提供混合检索策略（向量语义 + 关键词）
- 提供每日自检/维护流程（创建当日文件、回顾昨日、更新 MEMORY、清理旧日志、生成报告）

---

## When to Use

当你需要：
- 让 agent 在多次会话后仍能稳定“记住关键偏好/决策/重点事实”
- 避免无意义聊天堆满 memory 文件
- 让 memory 的检索质量随时间衰减（更近的更相关、过旧的自动清理）
- 每天自动执行记忆维护（而不是把所有逻辑都塞进对话里）

---

## Target Workspace Layout

假设你的工作目录是 OpenClaw 的 workspace 根目录（如 `~/.openclaw/workspace/`），建议使用如下结构：

```text
workspace/
├── MEMORY.md                      # 长期记忆（核心知识库，建议只在主会话维护）
├── AGENTS.md                      # Agent 行为/调用规范片段（由你自行决定放哪一份）
├── TOOLS.md                       # 工具/Skill 索引（可选）
├── HEARTBEAT.md                   # 心跳任务（可选）
└── memory/
    ├── preferences.md             # 用户偏好
    ├── decisions.md               # 重要决策
    ├── projects.md                # 项目信息
    ├── contacts.md                # 联系人
    ├── patterns.md                # 最佳实践/模式
    ├── feedback.md                # 反馈记录
    └── YYYY-MM-DD.md            # 每日日志（短期记忆）
```

---

## Memory File Templates（建议模板）

你可以先用下面的最小模板初始化这些文件，后续维护任务只需要“更新块/追加少量要点”即可。

`MEMORY.md`（示例结构）：
```markdown
# MEMORY.md — Long-Term Memory

## About
- 用户核心偏好：
- 重要身份/背景：

## Active Projects
- 项目名：状态 / 关键里程碑 / 当前风险

## Decisions & Lessons
- 关键决策（为什么这么选）：
- 教训（避免重复犯错）：

## Preferences
- 沟通风格：
- 工具偏好：
- 不希望的方式：
```

`memory/preferences.md`：
```markdown
# preferences.md

## Communication
- 偏好：

## Tools & Workflows
- 常用工具：
- 典型工作流：
```

`memory/decisions.md`：
```markdown
# decisions.md

## Key Decisions
- 决策点：
- 背景：
- 为什么这么做：
- 未来可能调整：
```

`memory/patterns.md`：
```markdown
# patterns.md

## Best Practices
- 模式名：
- 使用条件：
- 操作步骤：
- 失败案例（可选）：
```

---

## Importance Scoring (写入前评估重要性 1-5)

规则：当你准备“写入记忆”时，先给内容打分（1-5），再决定落盘位置。

建议映射：
- 5 分：写入 `MEMORY.md`
  - 核心原则、关键决策、用户核心偏好
- 4 分：写入 `MEMORY.md`
  - 重要规则、多次重复的教训
- 3 分：写入 `memory/YYYY-MM-DD.md`
  - 一般待办、常规对话内容（值得被检索但不必长期化）
- 2 分：写入 `memory/YYYY-MM-DD.md`
  - 临时信息、可选记录
- 1 分：不记录
  - 日常寒暄、无意义内容

落盘策略（建议）：
- 同一条记忆尽量“去重/归并”，避免无限追加
- 只有在“值得被未来检索/复用”时才落盘

---

## Time Decay & Cleanup (时间衰减 + 30 天清理)

短期记忆的检索权重随时间衰减：
- 当天：活跃（权重 1.0）
- 1-7 天：近期（权重 0.8）
- 8-30 天：中期（权重 0.5）
- 30 天+：过期（权重 0，建议在每日维护中清理/归档）

每日维护清理流程（推荐）：
1. 扫描 `memory/` 下所有 `YYYY-MM-DD.md`
2. 对于 30 天以前的文件：
   - 如果有“值得保留”的内容，把它提取到 `MEMORY.md`（或专题文件）
   - 其余直接删除/归档

---

## Manual Triggers (手动触发词立即写入)

当用户说以下关键词时，立即启动“写入评估”并落盘（重要性打分后写入）：
- 「记下来」「记住这个」：评估重要性后写入对应位置
- 「别忘了」「永久保存」：直接写入 `MEMORY.md`
- 「这是一个重点」：直接写入 `MEMORY.md`
- 「写入记忆」：按内容类型选择位置：偏好->`memory/preferences.md`，决策->`memory/decisions.md`，项目->`memory/projects.md`，联系人->`memory/contacts.md`，模式/最佳实践->`memory/patterns.md`，反馈->`memory/feedback.md`。

---

## Auto Recall (自动触发检索/回忆)

当用户的问题属于以下类型时，先进行 memory 检索，再回答：
- 询问“关于之前工作/决策/日期/人/偏好/待办”的内容
- 需要引用或延续过去信息

建议调用链：
1. 使用 `memory_search` 工具按 query 搜索相关记忆
2. 如需要更精确引用，再使用 `memory_get` 拉取更具体的片段（如果你的系统支持）
3. 若检索置信度不足：你可以坦诚说明“我刚刚帮你查了记忆，但未找到足够相关内容”

---

## Retrieval (混合检索：向量语义 + 关键词)

建议策略：混合检索（向量语义 + FTS 关键词）。

你可以在 OpenClaw 的 memorySearch 配置中设置类似参数：
- Provider：`voyage`（或你实际使用的向量供应商）
- sources：`["memory", "sessions"]`（按需调整）
- indexMode：`"hot"`（实时更新，按需调整）
- minScore：从 `0.3` 起调（越低结果越多）
- maxResults：从 `20` 起调

手动检索示例（如果你的系统支持）：
```bash
openclaw memory search "关键词"
```

---

## Daily Maintenance Workflow (每日自检/维护)

建议每日执行时间：`08:30`（可按你的时区调整）。

维护目标：
- 生成当日日志：`memory/YYYY-MM-DD.md`
- 回顾昨日日志：把值得长期化的内容提取到 `preferences.md / decisions.md / patterns.md / MEMORY.md`
- 清理 30 天+ 的旧日志（可选，但建议做）
- 生成报告（可选：发送到飞书/IM 或仅输出到控制台）

维护流程（6-7 步）：
1. 系统/网关状态检查（可选）
2. 模型状态检查（可选）
3. API 配置检查（可选）
4. 配置备份
   - 备份：`openclaw.json -> openclaw.json.backup-YYYYMMDD`
   - 备份保留：最多最近 3 个
   - 同步更新 API keys 的独立备份（如果你有 `.api-keys-backup.env` 这类文件）
5. 创建当日日志文件（若不存在）
6. 回顾昨日：提取关键偏好/决策/教训，更新 MEMORY 或专题文件
7. 清理 30 天+旧日志（并对“值得保留”的内容做迁移）

备份 shell 命令示例（你可以直接复制到 cron payload 内）：
```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup-$(date +%Y%m%d)
ls -t ~/.openclaw/openclaw.json.backup-* | tail -n +4 | xargs -r rm
cp ~/.openclaw/openclaw.json ~/.openclaw/.api-keys-backup.env
```

---

## Cron Job Template (把 maintenance 跑起来)

在 OpenClaw 的 cron 作业中，建议使用“隔离会话（isolated）+ 定时触发 + 只做 maintenance 任务”的模式。

示例（只提供你需要关注的核心字段：`schedule` 与 `payload` 里的 message；其余 delivery/agentId/sessionKey 由你的环境决定）：

```json
{
  "schedule": { "kind": "cron", "expr": "30 8 * * *", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "执行每日记忆维护流程（7步）：1) 创建 memory/YYYY-MM-DD.md（若不存在）2) 回顾昨日 memory，提取值得长期化的内容到 MEMORY.md 或专题文件 3) 删除 30 天+ 旧日志（删除前迁移重要内容）4) 视情况做 openclaw.json 备份（保留最近3个）5) 生成简洁报告并给出发现与建议。\n要求：输出要结构化、简洁，重点是记忆维护结果。",
    "model": "YOUR_DEFAULT_MODEL",
    "timeoutSeconds": 600
  }
}
```

说明：
- 你需要把 `YOUR_DEFAULT_MODEL` 替换为你的默认模型
- 如果不需要飞书发送，就让报告输出到默认通道/仅返回内容即可

---

## AGENTS.md Snippet (你可以直接拷贝)

把下面片段加入你的 `AGENTS.md`（或你用于约束 agent 的行为文档）：

```markdown
### 🧠 记忆管理规范（Memory Management Skill）

1) 自动回忆：
在回答“关于之前工作、决策、日期、人、偏好、待办”等问题前，先运行 memory_search 检索相关记忆。
如果检索后仍不确定，再在回复中说明已检查记忆但未找到足够证据。

2) 手动触发写入：
用户说「记下来 / 记住这个 / 别忘了 / 永久保存 / 这是一个重点 / 写入记忆」时，先评估重要性分数（1-5），再写入对应位置：
- 5-4 分：写入 MEMORY.md
- 3-2 分：写入 memory/YYYY-MM-DD.md
- 1 分：不记录

3) 时间衰减与清理：
每日维护任务会清理 30 天+ 旧日志；在删除前先把值得保留的内容迁移到 MEMORY.md 或专题文件。

4) 检索策略：
优先采用混合检索（向量语义 + FTS 关键词）。
```

---

## Safety & Preconditions

安全建议：
- 不要把敏感信息（账号、密钥、私密内容）写入公开或共享的 memory。
- 只在你明确需要并可控时，才把信息写入 `MEMORY.md`（长期存储更敏感）。

运行前提（建议）：
- 你的 OpenClaw 已启用 memorySearch（否则“检索/回忆”会失效）
- 你的 workspace 已按结构创建：`MEMORY.md` + `memory/` 日志目录
- 已设置或计划设置每日维护（cron 或等价机制）

---

## Related Skills

- `memory-setup`：配置持久化 memorySearch（向量检索）基础能力
- `self-improvement`：把错误/纠正记录成可学习的经验沉淀
- `cron-mastery`：cron vs heartbeat 选择与定时任务最佳实践
- `clawdhub`：用于安装/更新/发布技能

---

## Feedback

- If useful: `clawhub star memory-management`
- Stay updated: `clawhub sync`

-->
