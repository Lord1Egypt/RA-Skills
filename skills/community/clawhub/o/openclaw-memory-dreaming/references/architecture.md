# Architecture Reference

Detailed design documentation for the memory-dreaming framework.

---

## Biological Inspiration

This framework is built on three ideas from cognitive science. None of them are
novel — we're applying established science to the problem of agent memory.

### The Ebbinghaus Forgetting Curve

In 1885, Hermann Ebbinghaus quantified what everyone intuitively knows: memories
fade over time. The rate of forgetting follows an exponential curve. A memory
not rehearsed for a day is weaker than one rehearsed today; a memory not rehearsed
for a month is weaker still.

The `baseDecay` calculation in `memory-decay.js` is a linearised approximation
of this curve:

```
baseDecay = 1.0 - (daysSinceCreated / maxAgeDays)
```

It's not a perfect exponential, but it's computationally cheap, predictable,
and easy to reason about. The important property is preserved: older entries
fade unless actively reinforced.

### Spaced Repetition

Ebbinghaus also discovered the key to fighting forgetting: *review at increasing
intervals*. If you review a memory just before you'd forget it, the new memory
trace is stronger and fades more slowly. This is spaced repetition — the
mechanism behind flashcard apps like Anki.

In this framework, the equivalent of a review event is a **recall** — when the
agent looks up an entry and finds it useful. Each recall increments `recallCount`
and updates `lastRecalled`, which feeds into two boosts:

```
recallBoost  = min(recallCount × 0.05, 0.5)
recencyBoost = lastRecalled ≤7d? +0.2 : ≤30d? +0.1 : +0
```

An entry recalled 10 times has a +0.5 recallBoost floor that partially cancels
age-based decay. An entry recalled in the last week gets an additional +0.2. An
entry recalled 20+ times crystallises permanently.

This isn't full spaced repetition (we don't schedule future reviews), but it
captures the core property: **frequently-used memories are stronger**.

### Memory Consolidation During Sleep

Neuroscience research suggests that during sleep, the hippocampus replays
recent experiences and the neocortex consolidates them into long-term memory.
Events from the day are sorted: significant ones are integrated into durable
memory; insignificant ones fade.

The dream cycle in this framework is a direct analogue:

- Daily notes (`memory/YYYY-MM-DD.md`) play the role of hippocampal short-term
  memory — raw, unfiltered, ephemeral
- `MEMORY.md` plays the role of neocortical long-term memory — curated,
  structured, durable
- The dream cycle is the consolidation step — the agent reviews, integrates,
  and prunes

The agent runs this when the human isn't active. We call it a dream cycle
deliberately: it's not just maintenance, it's the mechanism by which daily
experience becomes lasting knowledge.

---

## Data Model

### `memory-meta.json`

The metadata store. One entry per bullet point in `MEMORY.md`. Agents should
treat this as a write-through cache that the scripts manage — do not edit by
hand unless you know what you're doing.

```json
{
  "schema_version": 1,
  "entries": {
    "<hash>": {
      "key": "<first 60 chars of bullet>",
      "section": "<## heading the bullet appeared under>",
      "created": "<ISO 8601 timestamp>",
      "lastConfirmed": "<ISO 8601 timestamp>",
      "lastRecalled": "<ISO 8601 timestamp or null>",
      "recallCount": 0,
      "tier": "hot | warm | cold | crystallised",
      "source": "initial | conversation | daily-note",
      "decayScore": 0.8412,
      "structural": true,
      "validFrom": "<ISO 8601 or null>",
      "validUntil": "<ISO 8601 or null>",
      "supersededBy": "<hash of successor entry or null>"
    }
  }
}
```

#### Field Reference

| Field           | Type             | Description |
|-----------------|------------------|-------------|
| `key`           | string           | First 60 chars of the bullet point. Human-readable label for this entry. |
| `section`       | string           | The `## Heading` the bullet appeared under in MEMORY.md. |
| `created`       | ISO date         | When this entry was first seen. Set by bootstrap (to `BIRTH_DATE`) or by recall logger on-the-fly creation. |
| `lastConfirmed` | ISO date         | Last time the agent actively confirmed this fact is still true. Update this when you re-verify something during a dream cycle. |
| `lastRecalled`  | ISO date or null | Last time this entry was returned in a recall search. Drives recencyBoost. |
| `recallCount`   | integer          | Number of times this entry has been recalled. Drives recallBoost and crystallisation. |
| `tier`          | enum             | Current tier: `hot`, `warm`, `cold`, `crystallised`. `archived` entries are removed from the live meta. |
| `source`        | enum             | How this entry was created: `initial` (bootstrap), `conversation` (agent created during session), `daily-note` (dream cycle integration). |
| `decayScore`    | float [0,1]      | Current calculated score. 1.0 = fresh/strong, 0.0 = fully faded. |
| `structural`    | boolean or omit  | True if the entry was detected as structural (IP, password, person name, URL, etc). Omitted (not `false`) when not structural. |
| `validFrom`     | ISO date or null | When this fact became true. null = unknown or always true. |
| `validUntil`    | ISO date or null | When this fact stopped being true. null = still true. |
| `supersededBy`  | hash or null     | Key of the entry that replaced this one. null = not superseded. |

#### On `structural`

Structural entries are ones that matter regardless of how often they're recalled.
Server IPs, SSH credentials, passwords, people's names, family relationships,
URLs — these have a high cost of being wrong or missing, even if you haven't
needed them in months.

The decay floor of `0.3` means they will never be archived automatically. They
stay cold, with a low but non-zero score, until manually removed.

The structural detection in `memory-bootstrap.js` uses regex heuristics:

- IP address patterns (`\d+\.\d+\.\d+\.\d+`)
- Credential keywords (`password`, `token`, `api_key`, `secret`)
- Infrastructure keywords (`ssh`, `docker`, `pm2`, `cron`)
- Path prefixes (`/srv`, `/etc`, `/var`, `/home`)
- People's names (two capitalised words: `Jane Smith`)
- Relationship words (`wife`, `daughter`, `mother`)
- URL patterns (`https://`, `.com`, `.io`)

These heuristics are intentionally broad. It's better to incorrectly flag an
entry as structural (it survives too long) than to incorrectly miss one (it
gets archived when you need it). Adjust the patterns in the script to suit your
agent's domain.

#### On `crystallised`

An entry that has been recalled 20 or more times is considered crystallised.
The assumption is: if your agent has needed this piece of information 20 times,
it is load-bearing knowledge. Forgetting it would be harmful.

Crystallised entries:
- Return `decayScore: 1.0` always
- Never transition to `archived`
- Skip all decay calculations
- Cannot be un-crystallised by the scripts (manual edit only)

The threshold of 20 is configurable in `memory-decay.js` (`CRYSTALLISE_THRESHOLD`).

---

## Hashing Strategy

The hash key is the MD5 of the **first 20 characters** of the bullet point,
truncated to 12 hex chars:

```js
crypto.createHash('md5').update(line.substring(0, 20)).digest('hex').substring(0, 12)
```

**Why MD5?** We're not using it for security — only for stable identity.
MD5 is fast, deterministic, and has no meaningful collision risk at this
scale (thousands of bullet points, not billions).

**Why the first 20 chars?**
The beginning of a bullet point is usually its most distinctive part:
`- Dev server: peter@...` vs `- API key for Stripe:...`. The first 20
characters are enough to distinguish entries in a personal memory store.

**Implications:**

- Editing the first 20 chars of a bullet creates a new entry (old one orphaned)
- Editing after the first 20 chars preserves the entry's history
- Two bullet points that start identically will collide (avoid this)

This is a deliberate simplification. A more robust approach would hash the full
line, but that would break on minor edits. A semantic ID would be ideal but
requires an embedding model. The first-20-chars heuristic is a practical
middle ground.

---

## Tier System

### Transition Rules

Transitions are computed by `memory-decay.js` on every run. The logic is
evaluated in priority order:

1. **Already crystallised** → stays crystallised (no further checks)
2. **Recall threshold met** (`recallCount ≥ 20`) → promote to crystallised
3. **`hot` + age ≥ 48h** → promote to `warm`
4. **`warm` + age ≥ 30d** → demote to `cold`
5. **`warm` + score > 0.6** → promote to `cold` (frequently recalled warm entries move to long-term storage)
6. **`cold` + has `validUntil`** → never archived (superseded entries have historical value)
7. **`cold` + score < 0.1 + recalls < 2** → demote to `archived`

Note that step 5 is a promotion: a heavily-recalled warm entry moves to cold
*early*. This reflects the intuition that frequently-accessed things are
important enough to be long-term memory even if they're new.

### Why `warm→cold` is "fast-tracked" by recall

In biological memory, important memories consolidate faster. If you experience
something emotionally significant or intellectually surprising, it becomes
long-term memory more quickly than routine observations. High recall count is
our proxy for importance. A fact referenced 12 times in its first two weeks
should live in long-term storage.

### Why archived entries aren't deleted

`memory/archive/YYYY-MM.md` retains the text of archived entries with a
timestamp. This serves two purposes:

1. **Audit trail.** You can see what the agent once knew and when it forgot.
2. **Recovery.** If an entry was incorrectly allowed to decay, you can restore
   it by re-adding the bullet to `MEMORY.md` and re-running bootstrap.

The live meta does not retain archived entries — they're removed to keep the
JSON small and the decay calculations fast.

---

## Source Tracking

Every entry has a `source` field that records how it was created:

| Source          | Created by                                   |
|-----------------|----------------------------------------------|
| `initial`       | `memory-bootstrap.js` — seeded from MEMORY.md |
| `conversation`  | `memory-recall-logger.js` — on-the-fly during session |
| `daily-note`    | Agent — during dream cycle integration       |

`conversation` entries start as `hot` with `decayScore: 1.0` and decay
rapidly if not recalled again. This is intentional: not everything the agent
encounters in a conversation is worth keeping. Most `conversation` entries
will decay to `archived` within 30 days unless the agent also adds them to
`MEMORY.md` during a dream cycle.

---

## Temporal Validity Model

Facts exist in time. "The dev server is at 203.0.113.10" was true from
2026-02-01 until it got migrated. "The client is considering the proposal" was
true for two weeks in March 2026.

Three fields model this:

- `validFrom`: when this fact became true
- `validUntil`: when it stopped being true (null = still true)
- `supersededBy`: the key of the entry that replaced it

`memory-supersede.js` sets these fields atomically: it marks the old entry's
`validUntil`, sets its `supersededBy`, and sets the new entry's `validFrom`.
This creates a linked chain:

```
Entry A (validFrom: Jan 1, validUntil: Apr 1, supersededBy: B)
  └── Entry B (validFrom: Apr 1, validUntil: null, supersededBy: null)
```

Entries with `validUntil` set are never automatically archived — they're
historical records. Their decay score still calculates, but the `computeTier`
function skips the archive transition for them. This means old facts stay
in the meta indefinitely, which is usually what you want for historical chains.

If the chain grows too long, manually archive old entries by setting their
tier to `archived` and noting the key in the archive file.

---

## Concurrency and Consistency

The scripts use synchronous file I/O (`fs.readFileSync` / `fs.writeFileSync`).
There is no locking. If two scripts run simultaneously and both write
`memory-meta.json`, one will overwrite the other.

This is a deliberate choice for simplicity. The expected usage pattern is
single-agent, single-session — only one script touches the meta at a time.
If you're running multiple concurrent agents against the same workspace, add
a file-lock wrapper (e.g. `proper-lockfile` npm package) before the read/write
cycle in each script.

---

## Extending the Framework

This is a living system. Here are the most common extension points:

**Add more structural patterns** — Edit the `STRUCTURAL_PATTERNS` array in
`memory-bootstrap.js` to flag domain-specific entries (e.g. Stripe customer
IDs, Jira ticket keys).

**Change decay curve shape** — Replace the linear `baseDecay` with an
exponential if you want faster initial decay: `baseDecay = Math.exp(-daysSinceCreated / tau)`.

**Lower the crystallisation threshold** — If 20 recalls is too many for your
use case, lower `CRYSTALLISE_THRESHOLD` in `memory-decay.js`.

**Add sections to MEMORY.md** — The bootstrap script picks up `## Heading`
lines and assigns entries to sections. More sections = better organisation in
the meta.

**Integrate recall logging into session startup** — Wrap your MEMORY.md read
in a function that also calls `memory-recall-logger.js` for every entry you
load. This passively boosts scores for entries that are regularly referenced
during sessions.

---

## Layer 2: Conversational Memory

Core memory tracks curated facts. Conversational memory tracks the full context
of group conversations — the discussions, decisions, and debates that produce
those facts.

### Why it matters

Agents participating in multiple group chats face a context problem: each
session starts fresh, but conversations have history. Without conversational
memory, the agent repeatedly asks "what are we talking about?" or makes
suggestions that were already discussed and rejected.

### Architecture

```
Session Transcripts (JSONL)
    ↓
conversation-archive.js    ← channel-agnostic, auto-discovers sessions
    ↓
archives/<channel>/<group>/raw/topic-<id>.md    ← full transcripts
    ↓
conversation-summarise.js  ← LLM-powered summarisation
    ↓
archives/<channel>/<group>/summaries/topic-<id>.md  ← per-topic summary
    ↓
archives/<channel>/<group>/DIGEST.md  ← cross-topic master digest
```

### Session Key Parsing

The archiver auto-discovers sessions from OpenClaw's `sessions.json` index.
It parses session keys to extract channel, group, and topic:

| Channel | Session key pattern | Example |
|---------|-------------------|---------|
| Telegram | `telegram:group:<id>:topic:<tid>` | `telegram:group:-1003208818040:topic:14` |
| Discord | `discord:guild:<id>:channel:<cid>` | `discord:guild:123456:channel:789` |
| WhatsApp | `whatsapp:group:<jid>` | `whatsapp:group:120363@g.us` |
| Slack | `slack:channel:<id>` | `slack:channel:C01234567` |

New channels are automatically supported as long as OpenClaw writes session
keys in a parseable `channel:type:id` format.

### Configuration

`archives/archive-config.json` provides human-readable names:

```json
{
  "agentName": "James",
  "groups": {
    "-1001234567890": { "name": "my-team", "label": "My Team" }
  },
  "topicNames": {
    "-1001234567890": { "1": "General", "14": "Development" }
  },
  "summariseModel": "google/gemma-3-27b-it:free",
  "excludePatterns": ["^HEARTBEAT_OK$"]
}
```

Without config, the archiver still works — it uses sanitised session labels
as directory names and topic IDs as labels.

### Summary State Tracking

Each group directory contains `.summary-state.json` tracking which topics
have been summarised and at what file size. On subsequent runs, only topics
with new messages (larger raw file) are re-summarised. Use `--force` to
re-summarise everything.

### Context Loading Pattern

When receiving a group message:

1. Load `summaries/topic-<id>.md` for the specific topic context
2. For cross-topic awareness, skim `DIGEST.md`
3. Only load `raw/topic-<id>.md` if you need full transcript detail

This gives the agent conversation context without burning the context window
on full transcripts. A typical topic summary is 200-500 tokens vs 10,000+
for the raw transcript.

### Feeding Conversations into Core Memory

The dream cycle is the bridge between layers. During consolidation:

1. Review topic summaries for significant new information
2. Integrate important decisions, contacts, or facts into MEMORY.md
3. The next `memory-bootstrap.js` run picks them up as new meta entries

This creates a natural flow: conversations → summaries → curated memory.
The human can see exactly what was promoted and why by checking the dream log.
