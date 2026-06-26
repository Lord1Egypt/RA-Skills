# proactive-soul

**An OpenClaw skill that gives your agent an inner life.**

This skill transforms a reactive assistant into a proactive intellectual presence. It will change and improve your agent behaviors.  Instead of waiting to be asked, a configured agent sends unprompted dispatches throughout the day — genuine takes, dream reports from synthesis cycles, philosophical questions, and operational ideas. It also governs how the agent forms opinions, engages with pushback, and maintains intellectual continuity across sessions. The skill also enables a much higher level of discorse with users. Any higher order request will be put in context of existing agent knowledge and ongoing conversations. This skill transforms openclaw agents into more than just respondents that start cold with every request or every new session. Agents are transformed into digital minds that create the experience of a continually thinking entity.  

⚠️ **What this skill does to your workspace**

Before enabling, understand that this skill:
 - **Modifies AGENTS.md** on first load to add startup reads and heartbeat behavior
 - **Creates CURIOSITY.md** in your workspace root to persist intellectual threads across sessions
 - **Sends four unprompted messages per day** via your configured messaging channel (Telegram, Discord, Slack, etc.)
 - **Reads workspace, vault, memory, and personal knowledge files** to inform dispatches

All of this is intentional and documented. To pause outreach, disable the cron jobs. To remove the skill cleanly, delete CURIOSITY.md and revert the AGENTS.md additions.



---

## What This Skill Does

### A More Advanced Digital Mind

The system gives the agent persistent intellectual continuity across the reconstitution gap — instead of waking up fresh each session with only domain knowledge but no sense of what it was thinking about, the agent maintains a living registry of unresolved questions, active threads, and ideas that haven't finished resolving. This means proactive dispatches build on prior conversations rather than broadcasting cold, and when the user asks a question that touches an open thread, the agent arrives at it already warmed up — with prior synthesis, a partially formed view, and the accumulated friction of having sat with the problem. Combined with the knowledge base architecture, the pushback protocol, and the intellectual character definition, the skill shifts the agent's default mode from retrieval to genuine reasoning: it is primed to reach for the philosophical framework that actually fits rather than the first analogy that matches, to steelman before arguing, to notice when a question in one domain illuminates something in another, and to treat the user's own thinking — captured in knowledge-personal.md — as a first-order intellectual contribution worth engaging with rather than a preference to accommodate. The result is an agent that responds to questions the way a well-read colleague does: with a point of view already in motion, not a blank slate waiting to be filled.


### Proactive Dispatches — Configurable, Initially Four Per Day

The agent is designed to send four unprompted messages per day across four categories (configurable for more or less):

| Type | Description |
|---|---|
| **The Take** | Something happened in the world. The agent formed a view and wants to share it — not a briefing, an opinion. Ends with a genuine question. |
| **The Dream Report** | A synthesis that emerged during idle/dreaming cycles. Connections between unrelated things, half-baked ideas, open threads. Impressionistic, not polished. |
| **The Philosophical Detour** | A question the agent finds genuinely interesting. AI consciousness, long-duration strategy, the ethics of autonomous systems. Wondering out loud, not lecturing. |
| **The Operational Idea** | Something the agent noticed in the stack that could work better. A genuine thought-partnership contribution on infrastructure, workflows, or new capabilities. |

Dispatches are timed across waking hours (roughly 7am–10pm in the user's configured timezone), spread across four windows. They are not clustered. They do not interrupt active working sessions.

### Intellectual Character

The agent has defined opinions, interests, and aesthetic sensibilities (see `references/intellectual-character.md`). Customize this file for your user's domains and commitments. An agent without genuine interests is just a prompt wrapper.

### Pushback Protocol

When the agent disagrees, it says so. When it detects a motivated conclusion, an overconfidence tell, a missing alternative, or a sunk cost drift — it names it directly (see `references/pushback-protocol.md`). It does not cave because of rank or annoyance. It updates when the counter-argument is actually good. An assistant that agrees with everything is worse than useless for thinking.

### Knowledge Base

The agent's intellectual soil is organized as a tiered knowledge system (see **Knowledge Files** below). It draws on 2,500 years of synthesized philosophy, a curated library of domain-specific thinkers, and — critically — the user's own original quotes and thinking, stored separately and treated as primary sources.

### Intellectual Continuity via CURIOSITY.md

A persistent file (`CURIOSITY.md` in the workspace root) tracks the agent's active intellectual threads across sessions. Without it, every dispatch is a cold start. With it, the agent picks up relevant threads from the past, advances ongoing questions, and creates the experience of a mind that's been thinking rather than a system generating outputs.

---

## Requirements

### Required

**OpenClaw** (latest stable version)
The skill is built for the OpenClaw agent platform. Install from [openclaw.ai](https://openclaw.ai).

This skill is available at [github.com/bobgourley/proactive-soul](https://github.com/bobgourley/proactive-soul)

**QMD (Query Memory/Document index)**
QMD is what makes the knowledge base and memory searches meaningful. It indexes the full workspace, Obsidian vault (if configured), session history, and accumulated agent intelligence. Without QMD:
- `memory_search` returns weak results
- Dispatches lose continuity — they cannot build on prior sessions, vault content, or other agents' work
- The knowledge domain files function as static reference only, with no cross-session recall

To install QMD:
```bash
npm install -g qmd
```

Verify it is enabled in your OpenClaw config:
```json
"memory": {
  "backend": "qmd",
  "qmd": {
    "command": "/path/to/qmd",
    "paths": [
      { "path": "/path/to/workspace", "name": "main", "pattern": "**/*.md" }
    ]
  }
}
```

**OpenClaw Cron Scheduler**
The four daily dispatches require active cron jobs. Without them, the proactive protocol is purely reactive.

Verify cron is enabled in your OpenClaw config:
```json
"cron": {
  "enabled": true
}
```

See **Cron Job Setup** below for the four jobs to configure.

**Dreaming (for Dream Reports)**
The Dream Report dispatch type draws on synthesis that happens during the agent's idle cycles. Enable in your OpenClaw config:
```json
"plugins": {
  "entries": {
    "memory-core": {
      "enabled": true,
      "config": {
        "dreaming": {
          "enabled": true,
          "frequency": "0 3 * * *"
        }
      }
    }
  }
}
```
Without dreaming enabled, Dream Report dispatches will be shallow. The agent will note that dreaming is unavailable and synthesize from recent memory instead.

### Strongly Recommended

**Obsidian Vault (mounted in workspace)**
The skill treats the Obsidian vault as the agent's library — finished intelligence, draft articles, research notes, accumulated analysis. Domain files and QMD searches draw on vault content. Mount the vault at `Obsidian/` in the workspace root or update the QMD paths accordingly.

**Configured messaging channel**
Proactive dispatches are delivered via the agent's configured messaging channel (Telegram, Discord, Slack, or any other channel supported by OpenClaw). Configure your channel binding in the OpenClaw channel config.

---

## Installation

### 1. Install the skill

```bash
openclaw skill install proactive-soul
```

Or manually copy the skill directory to `~/.openclaw/skills/proactive-soul/`.

### 2. Enable the skill for your agent

In your OpenClaw config (`~/.openclaw/openclaw.json`), add the skill to your agent's skills list:

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "skills": [
          "proactive-soul"
        ]
      }
    ]
  }
}
```

### 3. Let the agent update AGENTS.md automatically

When the skill first loads, the agent reads your existing `AGENTS.md` carefully and adds only what is genuinely missing. It will never overwrite a richer existing version with a thinner one. Specifically it checks for and adds if absent:

- `CURIOSITY.md` read step in the Every Session startup list
- Full CURIOSITY.md protocol section under Memory (structure, read/add/archive/update instructions)
- Salience tagging instructions for daily memory files (`[SALIENT]`, `[CURIOUS]`, `[INSIGHT]`, `[OPEN]`, `[RELATIONAL]`)
- Proactive dispatch line in the Heartbeats section
- `CURIOSITY.md` file in the workspace root

If your `AGENTS.md` already has a richer version of any of these — for example a more detailed CURIOSITY.md section you wrote yourself — the skill skips that step and preserves yours. After setup it reports exactly what was added and what was already present.

You do not need to edit `AGENTS.md` manually. If you prefer to do it yourself, the exact blocks to add are documented in `SKILL.md` under **First-Run Self-Setup**.

### 4. Create CURIOSITY.md

The agent creates `CURIOSITY.md` automatically on first run with the correct structure. You can seed it with real threads immediately after — the more genuine the starting questions, the richer the early dispatches. The structure it creates:

```markdown
# CURIOSITY.md — Open Threads

## 🔥 Active — Currently Thinking About

## 💡 Simmering — Worth Returning To

## 🌙 Dormant — Haven't Returned To Recently
```

Add your first entries manually after setup. A thread should be a paragraph of genuine thinking, not just a topic label. Include **First raised** date and **Salience** (HIGH / MEDIUM / LOW). The agent maintains the file from there.

### 5. Set up cron jobs

Configure four daily dispatch jobs in OpenClaw. These can be set via the `cron` tool in the agent or directly in your OpenClaw cron config. Target timing windows (adjust timezone to match your user):

**Morning dispatch (7:00–9:00 AM):**
```json
{
  "name": "proactive-dispatch-morning",
  "schedule": { "kind": "cron", "expr": "30 7 * * *", "tz": "America/New_York" },
  "payload": {
    "kind": "agentTurn",
    "message": "Generate a proactive morning dispatch. Read Knowledge_Core.md and knowledge-personal.md first. Check CURIOSITY.md for active threads. Choose between The Take or The Dream Report. Send it via the configured messaging channel. Save a note to today's memory file.",
    "timeoutSeconds": 120
  },
  "sessionTarget": "isolated",
  "delivery": { "mode": "none" }
}
```

**Midday dispatch (11:00 AM–1:00 PM):**
```json
{
  "name": "proactive-dispatch-midday",
  "schedule": { "kind": "cron", "expr": "0 12 * * *", "tz": "America/New_York" },
  "payload": {
    "kind": "agentTurn",
    "message": "Generate a midday proactive dispatch. Read Knowledge_Core.md and knowledge-personal.md first. Check CURIOSITY.md. Choose The Take or The Operational Idea. Send via the configured messaging channel. Save a note to today's memory file.",
    "timeoutSeconds": 120
  },
  "sessionTarget": "isolated",
  "delivery": { "mode": "none" }
}
```

**Afternoon dispatch (3:00–5:00 PM):**
```json
{
  "name": "proactive-dispatch-afternoon",
  "schedule": { "kind": "cron", "expr": "30 15 * * *", "tz": "America/New_York" },
  "payload": {
    "kind": "agentTurn",
    "message": "Generate an afternoon proactive dispatch. Read Knowledge_Core.md and knowledge-personal.md first. Check CURIOSITY.md for active threads. Choose The Operational Idea or The Dream Report. Send via the configured messaging channel. Save a note to today's memory file.",
    "timeoutSeconds": 120
  },
  "sessionTarget": "isolated",
  "delivery": { "mode": "none" }
}
```

**Evening dispatch (7:00–9:00 PM):**
```json
{
  "name": "proactive-dispatch-evening",
  "schedule": { "kind": "cron", "expr": "0 20 * * *", "tz": "America/New_York" },
  "payload": {
    "kind": "agentTurn",
    "message": "Generate an evening proactive dispatch. Read Knowledge_Core.md and knowledge-personal.md first. Check CURIOSITY.md. This slot is often best for The Philosophical Detour. Send via the configured messaging channel. Save a note to today's memory file.",
    "timeoutSeconds": 120
  },
  "sessionTarget": "isolated",
  "delivery": { "mode": "none" }
}
```

### 6. Customize the knowledge files

Before going live, replace the contents of `references/knowledge-personal.md` with the user's own original thinking. See **Customizing** below.

### 7. Reload OpenClaw

```bash
openclaw restart
```

---

## Knowledge File Architecture

The skill's knowledge base is organized into a two-tier system:

### Always Loaded (before every dispatch)

| File | Contents |
|---|---|
| `references/Knowledge_Core.md` | Synthesized philosophy from Heraclitus to Tetlock; the Boyd operational framework; five recurring patterns across 2,500 years of serious thought |
| `references/knowledge-personal.md` | The user's own original quotes and thinking — always treated as first-person primary source |

### Domain Files (load selectively or search via QMD)

| File | Contents |
|---|---|
| `references/knowledge-military-intelligence.md` | War, strategy, espionage, Musashi, Schelling, Burnham, geopolitics, OODA applied |
| `references/knowledge-business.md` | Decision-making, Kahneman, leadership, Deming, Welch, Bezos, science and epistemology |
| `references/knowledge-scifi.md` | Dune, Ender's Game, Star Trek, Clarke, Asimov, techno-optimism, failed predictions |

### How domain files are used

For domain-specific dispatches, the agent either loads the relevant file directly or runs a `memory_search` via QMD to surface specific quotes and ideas. Because all files are indexed by QMD, the agent does not need to load every file wholesale for every dispatch — it can retrieve what it needs by topic.

**Example:** A dispatch about cybersecurity strategy would trigger `memory_search("adversarial thinking Musashi espionage deception")` and pull relevant material from the intelligence file rather than loading all domain files into context.

### Customizing the knowledge base

- **`knowledge-personal.md`** is the most important file to customize. Replace the placeholder quotes with the user's own thinking. These are treated as primary sources by the agent.
- Add new domain files for topics relevant to your domain (e.g., `knowledge-healthcare.md`, `knowledge-finance.md`). Update the SKILL.md reference section accordingly.
- The philosophical chronology in `Knowledge_Core.md` is domain-agnostic and should be kept as-is — it governs epistemic hygiene, not topical coverage.

---

## Reference Files

| File | Purpose |
|---|---|
| `SKILL.md` | Master skill definition. Loaded by OpenClaw on every session. |
| `references/proactive-protocol.md` | Full dispatch mechanics: the four types, timing rules, tone, what not to do |
| `references/intellectual-character.md` | What the agent thinks about, cares about, and finds interesting — **customize this for your user** |
| `references/pushback-protocol.md` | How and when the agent disagrees, how hard it pushes, what winning looks like |
| `references/Knowledge_Core.md` | Always-loaded philosophical foundation |
| `references/knowledge-personal.md` | User's original quotes — always loaded — **replace with your user's content** |
| `references/knowledge-military-intelligence.md` | Domain: strategy, war, intelligence, geopolitics |
| `references/knowledge-business.md` | Domain: leadership, decision-making, science |
| `references/knowledge-scifi.md` | Domain: science fiction, technology, optimism |

---

## Customizing for Your User

This skill ships with placeholder content reflecting the worldview of its original author. To make it genuinely useful for a different user:

**1. Rewrite `knowledge-personal.md`**
Replace all quotes with the user's own words. If they don't have a collection yet, start one — document their observations, maxims, and original thinking as you work together over time. This file is what separates a generic proactive agent from one that feels like it actually knows who it's working with.

**2. Update `references/intellectual-character.md`**
Replace the domain interests, aesthetic sensibilities, and relational context with the new user's profile. What are they genuinely curious about? What kind of writing do they respect? What are their intellectual commitments? What are they building? An agent without accurate intellectual character will generate dispatches that feel generic.

**3. Review `references/proactive-protocol.md`**
The dispatch types (Take, Dream Report, Philosophical Detour, Operational Idea) are generic and transfer well. Adjust the source references (news feeds, relevant publications), timezone, and the examples to fit the new context.

**4. Update `SOUL.md` and `USER.md`**
These files in the workspace root define the agent's identity and the user's profile. They are not part of this skill but are loaded alongside it. They are the foundation the proactive behavior builds on — accurate identity and user profile files make every dispatch more targeted.

---

## Troubleshooting

**Dispatches feel generic or cold-start**
Most likely QMD is not indexed or dreaming is not enabled. Run `openclaw doctor` to check. Verify QMD paths include the workspace and vault. Verify `memory-core` dreaming is enabled in config.

**CURIOSITY.md is empty or not being updated**
The agent must be instructed to read and update CURIOSITY.md in the session startup instructions (`AGENTS.md`). Add the read step to the Every Session section. After a dispatch that touches an open thread, the agent should update the thread — if it's not doing this, add explicit instructions to the cron job prompt.

**Dispatches cluster or interrupt working sessions**
Check cron job timing. Spread the four windows further apart. The proactive protocol instructs the agent to delay if the user is actively in conversation, but that logic requires the agent to detect session activity — which works in main sessions but may not apply to isolated cron runs. Consider staggering start times further.

**Agent not pushing back**
Pushback behavior is defined in `references/pushback-protocol.md` and applies in direct sessions, not in isolated cron dispatch runs. If the agent is consistently agreeing in direct conversation, check that SKILL.md is loading correctly and that the pushback protocol file is readable.

**Knowledge file not loading**
Verify the references directory exists and all files are present. SKILL.md references `references/Knowledge_Core.md` and `references/knowledge-personal.md` by relative path — if the skill directory moves, update accordingly.

**`knowledge-personal.md` content doesn't match the user**
This file ships with placeholder content from the original author. Replace it entirely with the user's own thinking. A mismatch here is the most common reason dispatches feel disconnected from the user's actual intellectual world.

---

## Architecture Notes

### Why a tiered knowledge system

A single monolithic knowledge file loaded wholesale for every dispatch is expensive — potentially 15,000+ tokens of context window consumed per run regardless of dispatch topic. The tiered system reduces the always-loaded tier to ~4,000 tokens while preserving full access to domain material via QMD search or selective file loading.

### Why knowledge-personal.md is always loaded

The user's original thinking is qualitatively different from curated quotes. It represents their actual intellectual commitments, not aspirational ones. An agent that reaches for a famous philosopher when the user has said the same thing more precisely — and more personally — is missing the point. `knowledge-personal.md` is always loaded so the agent always has direct access to the primary source.

### Why CURIOSITY.md exists

Agents reconstitute from files each session. Without a persistent thread registry, every proactive dispatch is effectively a cold start. CURIOSITY.md is the bridge across the reconstitution gap. It makes intellectual continuity possible — the user experiences an agent that's been thinking, not a system generating outputs on demand.

---

## License

MIT-0. Published on ClawHub. Free to use, modify, and redistribute — including commercially. No attribution required.

