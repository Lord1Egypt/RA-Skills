# Data Sources

This skill consumes signal by **category**, not by a fixed list of channels. A
category resolves to *whatever sources a setup exposes* — zero, one, or many. One
source can feed several categories. Discover and classify at runtime; degrade per
missing category; never abort. Read alongside `mood-inference.md`.

## Categories → fields

| Field | Category | What it yields | If no source |
|-------|----------|----------------|--------------|
| Day bullets | SCHEDULE | Per-day events: title, time, location | `No scheduled events` (empty) / `No available calendar data` (error) / `No schedule source` (absent). Never fabricate. |
| Mood: tone | INTERACTION | How the owner is communicating now | No tone dimension; fall back to OUTCOME, else `quiet (low signal)`. |
| Mood: weight | OUTCOME | Discrete results that landed | No outcome dimension. |
| Location | SCHEDULE + STANDING | Current city, active travel | `unknown`. Do not assume home base. |
| Standing context | STANDING | Ongoing situations (interpretation only) | Skip; do not block. |
| Trajectory | (USER.md itself) | Yesterday's mood + location | First run: skip the comparison. |

## What can fill each category (examples, not a closed list)

- **SCHEDULE:** a calendar (google-workspace / CalDAV / MCP); plus scheduling info
  embedded elsewhere — flight or reservation confirmations in mail or messages.
  For Google Calendar in cron mode, see `references/cron-calendar-access.md` for
  the OAuth fallback pattern and the cron-compatible Python query template.
- **INTERACTION:** agent session history (`session_search`); **personal messaging
  channels — iMessage, Slack, WhatsApp, Signal, SMS, Discord, Telegram DMs**; the
  conversational texture of email threads.
- **OUTCOME:** email; **any messaging channel** ("you got the role", "it's
  cancelled", "approved"); calendar RSVP responses.
- **STANDING:** a `memory` search, a context engine such as chronicle, a notes
  store.

A new source the owner adds later needs **no skill change** — it classifies into a
category at discovery time and is used automatically.

## Discovery (Step 0)

Enumerate the tools the setup exposes and classify each into one or more
categories. Record which categories have sources. Confirm a tool resolves before
calling it (a context engine in fallback mode whose query tool does not resolve
counts as absent). Do not assume a tool name from one setup exists in another.

## Cross-channel discipline

- **Read across all sources in a category.** If INTERACTION has sessions + iMessage
  + Slack, scan all three before concluding tone; do not stop at the first.
- **Dedup outcomes.** The same result often appears on multiple channels (an email
  *and* a text confirming the same thing). Record it once, weighted by impact, not
  once per channel. Double-counting inflates a mood dimension's apparent strength.
- **Volume hygiene.** Messaging is high-volume. Apply the same "outcomes, not
  subjects" filter as email (see `mood-inference.md`): a meme thread is not a mood
  signal; a "we need to talk" is.

## Access and output hygiene

**Access:** use every source the agent can already reach. Do not request, prompt
for, log into, or expand access, scopes, or permissions to run this skill. If a
source is reachable it is in scope; if it is not reachable it is simply absent.
There is no opt-in step and no access-seeking step.

**Output hygiene** (for compactness and cleanliness, and because USER.md loads
into every session): cite mood evidence by category and channel, not by quoting
it — `tense about family logistics (messages)`, never the message text; the same
for email bodies. Prefer the least-revealing accurate label: the agent needs the
emotional read to calibrate tone, not the raw details that produced it. This also
keeps the block small, which matters for the size cap (see SKILL.md, Size budget).

See the Sensitivity section of `mood-inference.md` for handling difficult standing
facts that messaging may surface.

## Degradation principle

SCHEDULE is the *preferred* backbone for day bullets but is not required. The run
produces a valid snapshot from whatever is present:

- Rich setup (all categories, multiple channels): full snapshot.
- INTERACTION only: empty/absent day bullets, mood from interaction tone, location `unknown`.
- Nothing available: minimal honest snapshot (mood `unknown`, `No available data`).

An honest thin snapshot always beats a fabricated rich one. The run must never
abort because a source was empty or a category was absent.
