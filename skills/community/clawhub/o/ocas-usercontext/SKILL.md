---
license: MIT
name: ocas-usercontext
description: >
  Maintains a compressed `## Daily Context` block in the owner's USER.md:
  an evidence-grounded snapshot of mood, location, week theme, and
  yesterday/today/tomorrow bullets, inferred from whatever signal sources the
  setup exposes (calendar, session history, email, long-term memory). Use when
  the daily context block needs refreshing, when its scheduled job has failed,
  or when the owner asks for a status snapshot. Keywords: daily context, user
  snapshot, mood inference, USER.md update, personal briefing. NOT for weather,
  long-term planning, or advice.
source: https://github.com/<agent-handle>/ocas-usercontext
metadata:
  author: Indigo Karasu (indigokarasu)
  version: 3.2.0
  hermes:
    tags: [context, daily, cron]
    category: infrastructure
includes:
  - references/**
triggers:
  - /usercontext
  - /daily-context
---

# User Daily Context

## Purpose

When to read this skill: when the daily context block needs refreshing, when its scheduled job has failed, or when the owner asks for a status snapshot.

Keep one block of USER.md — `## Daily Context` — fresh every morning so every
session that day opens with an accurate read of what is happening in the owner's
life. USER.md loads into **every** session, so this block is the highest-leverage
and most-read text the agent maintains. Two failure modes are equally bad:
**stale** (yesterday's events shown as today's) and **fabricated** (a mood or
fact invented from thin signal). This skill optimizes against both.

It is designed to be **portable**: it adapts to whatever signal sources and tools
a given Hermes setup exposes, rather than assuming a fixed toolset. It runs well
in a rich setup (calendar + email + sessions + memory) and degrades honestly in a
bare one (sessions only, or even nothing).

## Honest data model

Be clear about what is *extracted* vs *inferred* — they have different failure
modes and conflating them is this skill's classic defect:

| Field | Kind | Drawn from (by signal category) |
|-------|------|---------------------------------|
| Yesterday/Today/Tomorrow bullets | **Extracted** | SCHEDULE sources. Report what is planned; do not editorialize. |
| Location | **Extracted** | SCHEDULE geography + STANDING travel context. Default `unknown`. |
| Week theme | **Summarized** | The week's SCHEDULE shape in one line. |
| Mood | **Inferred** | INTERACTION *tone* and OUTCOME *weight*, from any channel — NOT the schedule. |

The most common defect in this skill's history is **inferring mood from the
calendar** ("tea reservation" → "anticipation for tea"). A scheduled event is not
a feeling. Mood comes from how the owner *interacted* (affective TONE) and what *outcomes* landed. The same rule applies to session *subjects*: a session ABOUT a topic is not the owner feeling that topic -- never convert a discussed subject into a mood. Transactional, security, travel, purchase, and notification emails are not emotional evidence by themselves: never convert an alert or risk topic into `worried`, `anxious`, or similar without explicit affective language from the owner or a clearly affective interaction.
If interaction and outcome signal is thin, the correct mood is `quiet (low signal)`,
not an invention.

## Signal categories (extensible — discover, classify, don't assume)

This skill consumes signal by **category**, not by a fixed list of channels. Any
number of concrete sources can feed a category, and one source can feed several.
At the start of every run, enumerate *all* available signal tools, classify each
into the categories below, and use them. A category with no source is simply
absent; the run degrades, it never aborts.

| Category | What it yields | Example sources (any subset, setup-dependent) | If no source |
|----------|----------------|-----------------------------------------------|--------------|
| **SCHEDULE** | Planned events; day bullets, week theme, location | calendar (google/CalDAV/MCP); reservations & confirmations embedded in mail or messages | No day bullets from schedule; bullets may be `No schedule source`. |
| **INTERACTION** | How the owner is communicating now → mood *tone* | agent sessions (`session_search`); **personal messaging — iMessage, Slack, WhatsApp, Signal, SMS, Discord**; email threads | No tone signal; mood leans on OUTCOME, else `quiet (low signal)`. |
| **OUTCOME** | Discrete results that landed → mood *weight* | email; **any messaging channel** ("got the offer", a cancellation); calendar RSVPs | No outcome signal for mood. |
| **STANDING** | Durable context for interpretation; location | `memory`, a context engine (e.g. chronicle), a notes store | Location may be `unknown`; no standing-context interpretation. |

Rules:

- **Discover and classify, don't assume.** List the tools this setup exposes, map
  each to one or more categories, record what's present. Never call a tool you have
  not confirmed exists. A new channel the owner adds (a fresh MCP messaging server,
  say) needs no skill change — it just classifies into INTERACTION/OUTCOME and is used.
- **Many sources per category is normal.** Sessions *and* iMessage *and* Slack all
  feed INTERACTION. Read across them; do not stop at the first.
- **Dedup across channels.** The same outcome may appear in email and in a text.
  Count it once, by impact, not once per channel it touched.
- **Use everything already reachable; never seek more access.** If the agent can
  already query a source, it is in scope — use it. Do NOT request, prompt for, or
  expand access, scopes, logins, or permissions to run this skill. A source that is
  not already reachable is simply absent; proceed without it. (Keep the output
  compact and clean: cite mood evidence by channel, e.g.
  `tense about family logistics (messages)`, rather than pasting raw message text.
  That is compression and tidiness, not an access gate.) See
  `references/data-sources.md`.
- **Every category is optional.** INTERACTION alone still yields a valid snapshot;
  nothing available yields an honest `unknown` one.

See `references/data-sources.md` for the full category mapping, channel examples,
dedup, privacy, and degradation matrix.

## Where things live (resolve at runtime)

Paths are **profile-relative**, never hardcoded to one machine:

- **Profile root:** the active Hermes profile directory. Resolve from
  `$HERMES_HOME` if set; otherwise it is the directory this skill is installed
  under (the parent of `skills/`).
- **Target file:** `<profile>/memories/USER.md`. (Note: under `memories/`, not the
  profile root.) If `memories/USER.md` does not exist, check the profile root for a
  `USER.md`; if neither exists, create `<profile>/memories/USER.md`.
- **Timezone:** resolve the host timezone at runtime (e.g. `timedatectl` / system
  clock). Date math for yesterday/today/tomorrow uses the host's local day, never
  an assumed zone.

## Size budget (hard cap — never exceed)

USER.md is a **context file**: the agent harness truncates it (keeps head + tail,
drops the middle) if it exceeds the effective `context_file_max_chars`. A truncated
USER.md can silently lose the Daily Context block or corrupt another section, so
the block must be sized so the **whole file** stays under the cap. This is a hard
limit; the word budget below is only a soft target underneath it.

Resolve the cap for THIS setup, in order (do not assume a number):

1. Explicit `context_file_max_chars` in the active config — wins if set.
2. Else dynamic: `max(20000, min(context_length * 0.24, 500000))` chars, derived
   from the loading model's context window (~4 chars/token x 6% of the window).

**Cron-mode measurement pitfall:** When this skill runs as a cron job,
`execute_code` is BLOCKED (returns a cron-mode refusal, even for pure-Python
string math). Do NOT use it to measure `OTHER`/total chars. Instead write a tiny
Python snippet via `write_file` and run it through `terminal` (open the file,
`find("## Daily Context")`, sum the lengths of everything else, compare to cap).
The calendar step documents the same constraint in
`references/cron-calendar-access.md`. Always read the actual `context_file_max_chars`
value from config; on the indigo box it resolves to `12000`, not the dynamic
default.

Then, around the patch (Step 7):

- Measure the current total chars of USER.md and the chars of every section
  *other than* `## Daily Context` — call that `OTHER`.
- Hard budget for the block = `cap - OTHER - margin` (keep ~500 chars of margin;
  other sections can change between runs).
- The new block must fit the budget, and `OTHER + block <= cap` must hold. If the
  freshly written block is over, re-compress (bullet words to 8, mood to 1
  dimension, week to 5 words) until it fits.
- If even a minimal block will not fit because `OTHER` already fills the file,
  write the smallest valid block, do **not** touch any other section, and emit a
  warning that USER.md is at its cap so a human can trim the other sections. Never
  let the file exceed the cap, and never trim another section to make room.

## Output format

The `## Daily Context` block, written into USER.md exactly as:

```markdown
## Daily Context

> Refreshed daily by the `ocas-usercontext` job. Do not manually edit; regenerate instead.

### Snapshot (YYYY-MM-DD)
**Mood:** [1-3 evidence-backed dimensions, or `quiet (low signal)`]
**Location:** [city, or `unknown`]
**Week:** [one line, max 10 words]

### Yesterday (YYYY-MM-DD)
- [event, max 12 words]

### Today (YYYY-MM-DD)
- [event, max 12 words]

### Tomorrow (YYYY-MM-DD)
- [event, max 12 words]
```

### Compression rules

- **Hard ceiling:** the whole USER.md must stay under the harness `context_file_max_chars` cap (see Size budget). This always wins over the word target.
- Total block **under 300 words** (soft target, configurable; see Configuration). It costs context on every session.
- Bullets: up to 3 per day, **max 12 words each**.
- Mood: 1-3 dimensions, each `[label] about [topic]`; or `quiet (low signal)`.
- Week: one line, max 10 words.
- Empty calendar day → `No scheduled events`. Never fabricate an event.
- No weather, no advice, no system/meta narration, **no em dashes** (chat renderers mangle them; use commas/periods).

## Generation workflow

- [ ] **Step 0 — Resolve environment.** Profile root, USER.md path, host timezone.
      Enumerate available tools and classify each into the SCHEDULE / INTERACTION /
      OUTCOME / STANDING categories. Use every source the agent can already reach;
      never request or expand access. Unreachable sources are simply absent.
- [ ] **Step 1 — Read yesterday's snapshot.** Read the existing `## Daily Context`.
      Note prior mood + location: the trajectory baseline for Step 5. (Absent =
      first run; skip the comparison.)
- [ ] **Step 1b — Resolve the size budget.** Determine the effective
      `context_file_max_chars` cap (config override, else dynamic). Measure current
      USER.md total chars and the chars of all sections other than `## Daily Context`
      (`OTHER`). Compute the block's hard budget = `cap - OTHER - margin`.
      In cron mode, run this measurement via `write_file` + `terminal` (NOT
      `execute_code`, which is blocked in cron); see Size budget pitfall.
- [ ] **Step 2 — Build the Signal Ledger.** Gather, do not yet interpret, across all
      present sources: SCHEDULE (3 day pulls), INTERACTION (broad tone scan over
      sessions and any reachable messaging), OUTCOME (recent results on any channel),
      STANDING (active travel / situations). Write each signal as one line tagged with
      its category and source. **Dedup** the same outcome seen on multiple channels.
      A thin ledger is fine and honest.
      For SCHEDULE via Google Calendar in cron mode, the primary account's OAuth
      token may be expired — use the fallback pattern in
      `references/cron-calendar-access.md`, implemented by the bundled
      `scripts/_ucal_run.py` (run with the Hermes venv python). The same event on
      multiple calendars is one event, not two — dedup by summary + start + location.
- [ ] **Step 3 — Extract day bullets.** Per day, list calendar events (title + time)
      as bullets. Empty → `No scheduled events`. No editorializing.
- [ ] **Step 4 — Determine location.** City from today's calendar geography or a
      memory travel signal. No signal → `unknown`. Never guess from home base.
- [ ] **Step 5 — Infer mood.** Read `references/mood-inference.md` in full. Build
      1-3 dimensions, **each citing a concrete ledger signal** (session tone or
      email outcome, never the calendar). Apply trajectory vs Step 1: `still` if it
      persists, `now`/`shifted` if changed, drop vanished moods. Thin ledger →
      `quiet (low signal)`.
- [ ] **Step 6 — Write the week theme.** One line, max 10 words, from the week's
      calendar shape and active standing context. Distinguish an extended stay
      or relocation from a travel-heavy itinerary: use `extended stay in [place]`
      when a single location spans multiple weeks; reserve `travel-heavy week`
      for frequent movement or multiple trips. When a durable project is active
      during the stay, combine them, for example `Honolulu vacation and
      construction project`. Other themes include deadline-heavy,
      meeting-heavy, quiet, or project push.
- [ ] **Step 7 — Patch USER.md.** Replace ONLY the `## Daily Context` block (from
      that heading to the next `##` or EOF). Use an exact match; never add, remove,
      reorder, or touch identity, preferences, or any other section. Before writing,
      confirm the block fits the Step 1b budget and that `OTHER + block <= cap`; if
      not, re-compress until it does. Never let the file exceed the cap, and never
      trim another section to make room.
- [ ] **Step 8 — Validate, then act on delivery (do not skip).** Run the
      `references/validation.md` checklist. Then honor the configured `deliver`
      setting (default `local` = silent, write-only). See Configuration.

## Configuration

The skill ships with safe defaults; an installer or owner can override them. On a
Hermes box these live on the scheduled job (see `references/install.md`); the
skill should read intent from the job/config rather than hardcoding it.

| Knob | Default | Meaning |
|------|---------|---------|
| `deliver` | `local` (silent, write-only) | Where the snapshot goes after the patch. `local` = USER.md only. A chat target (e.g. `origin`, `telegram`) also pushes a copy. Most owners want `local`: USER.md already reaches the agent via session load, so a daily chat push is redundant. |
| `schedule` | once daily, morning, host TZ | When the job runs. |
| `word_budget` | 300 | **Soft** target for block length. The **hard** limit is the harness `context_file_max_chars` cap minus the other sections (see Size budget); the hard limit always wins. |
| (harness) `context_file_max_chars` | per agent config (dynamic if unset) | Not owned by this skill — read from the active agent config. The whole USER.md, including this block, must stay under it. |
| `weather_skill` | none | If the setup has a dedicated weather/briefing skill (e.g. `ocas-vesper`), this skill still emits no weather; that skill owns it. Purely informational — no hard dependency. |

## Runtime wiring (Hermes cron)

If run by a cron whose prompt is **inlined** (the common Hermes pattern), the cron
does not auto-read this SKILL.md. Then this skill is the **design** source of truth
and the cron prompt is the **runtime** source of truth; a change in one not
mirrored in the other is a silent divergence. When you change the workflow, format,
or config here, mirror the essentials into the cron prompt. See
`references/install.md` for how to instantiate the job on any box, and
`references/constraints.md` for the divergence rationale.

## When to Use

- Refreshing the daily context block in USER.md
- Recovering from a failed scheduled context update
- Owner requests a status snapshot or daily briefing
- Inferring mood from interaction and outcome signals

## When NOT to use

- Weather → a dedicated weather/briefing skill if the setup has one.
- Long-term planning / goal tracking → a planning skill.
- Advice or recommendations — this reports state, it does not prescribe.
- "How do I feel about X?" — this infers mood from signals; it does not ask.
- A full briefing with weather and priorities → a briefing skill.

## Gotchas and error handling

| Failure | Response |
|---------|----------|
| A signal category has no source | Proceed without it (see degradation matrix); never abort. |
| A source is not already reachable | Proceed without it; never request, prompt for, or expand access to add it. |
| Writing the block would push USER.md over the cap | Re-compress until it fits; if impossible, write the smallest valid block, warn, and leave other sections untouched. Never exceed the cap. |
| Other sections already fill the file to the cap | Do not trim them. Write a minimal block and emit an at-cap warning for a human to resolve. |
| Calendar/schedule pull fails for a day | `No available calendar data` for that day; continue. |
| INTERACTION sources all empty | No tone bullets; mood leans on OUTCOME, else `quiet (low signal)`. |
| STANDING search empty | Location may be `unknown`; do not block. |
| A named tool from another setup doesn't resolve here | Skip it; it is a candidate, not a requirement. |
| Same outcome appears on several channels | Dedup: count once by impact, not once per channel. |
| Tempted to quote a personal message | Don't. Cite evidence by category (`... (messages)`); never paste message text into USER.md. |
| Patch can't find `## Daily Context` | First run: append the block after the last `##`. |
| Patch fuzzy-matches wrong section | Read raw USER.md, use an exact `old_string`. |
| USER.md missing | Create `<profile>/memories/USER.md` with the block as first content. |
| Configured delivery fails | Block is already written; log, retry next run. |
| Output exceeds the word budget | Re-compress: bullets to 8 words, mood to 1 dimension, week to 5 words. |
| All sources fail at once | Minimal honest snapshot: mood `unknown`, location `unknown`, `No available data` per day. Still run; never skip. |

## Initialization (first run on a new setup)

- [ ] Resolve the profile root and host timezone (Step 0).
- [ ] Verify / create `<profile>/memories/USER.md`.
- [ ] Add a `## Daily Context` block with a placeholder snapshot.
- [ ] Discover available tools; record which capability roles are present.
- [ ] Register or confirm the scheduled job with the chosen `deliver`, `schedule`, and `word_budget` (see `references/install.md`).
- [ ] If the job uses an inlined prompt, ensure it matches this skill's workflow.
- [ ] Log to journal.
