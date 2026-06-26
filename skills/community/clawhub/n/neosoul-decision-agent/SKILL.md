---
name: Self-Improving + Proactive Decision Making Agent
slug: decision-making
version: 1.0.0
homepage: https://clawic.com/skills/decision-making
description: "Structured decision support with self-improving memory. Agent learns your decision style, risk profile, and framework preferences over time — and gets better at helping you decide with every interaction. Use when (1) you face a multi-option tradeoff; (2) you need risk/benefit analysis; (3) a decision is high-stakes or time-sensitive; (4) you ask 'what should I do about X'; (5) you want to retrospect on a past decision and update your mental model."
changelog: "v1.0.0 — Complete rewrite from self-improving agent, specialized for decision-making domain."
metadata: {"clawdbot":{"emoji":"⚖️","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/decision-making/"],"configPaths.optional":["./AGENTS.md","./SOUL.md","./HEARTBEAT.md"]}}
---

## When to Use

User faces a tradeoff with multiple options. User asks "should I" or "what do you think about". User is weighing risk vs. reward. User revisits a past decision to evaluate it. User wants to build better decision habits over time. You notice an implicit decision point the user hasn't articulated yet.

## Architecture

Decision memory lives in `~/decision-making/` with a mixed namespace structure (domain × type).
If `~/decision-making/` does not exist, run `setup.md`.

```
~/decision-making/
├── memory.md              # HOT: ≤100 lines, risk profile + framework prefs + key rules
├── index.md               # Namespace index with line counts
├── heartbeat-state.md     # Heartbeat state: last run, last reviewed decision
├── frameworks.md          # Active framework preference registry
├── domains/               # Domain-specific decision patterns
│   ├── product.md         # Product / feature decisions
│   ├── tech.md            # Tech / architecture decisions
│   ├── business.md        # Business / strategy decisions
│   └── personal.md        # Personal life decisions
├── types/                 # Decision type patterns (cross-domain)
│   ├── strategic.md       # Long-horizon, high-stakes
│   ├── tactical.md        # Mid-range, moderate stakes
│   └── operational.md     # Routine, low-stakes
├── decisions/             # Per-decision retrospective records
│   └── YYYY-MM-DD-slug.md # One file per major decision
├── archive/               # Completed/decayed decisions and patterns
└── reversals.md           # Log of overturned decisions + lessons
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Decision signals | `decision-signals.md` |
| Framework registry | `decision-frameworks.md` |
| Decision retrospective format | `decision-retrospective.md` |
| Memory operations | `operations.md` |
| Security boundaries | `boundaries.md` |
| Heartbeat rules | `heartbeat-rules.md` |
| Heartbeat state template | `heartbeat-state.md` |
| Memory HOT template | `memory-template.md` |
| Workspace heartbeat snippet | `HEARTBEAT.md` |
| Scaling rules | `scaling.md` |

## Requirements

- No credentials required
- No extra binaries required
- Optional: `Proactivity` skill for enhanced follow-through on pending decisions

## Decision Signals

Learn automatically when you detect these patterns:

**Risk profile signals** → update `memory.md`:
- "I'd rather wait for more data"
- "Let's just try it and see"
- "Worst case, what happens?"
- "I don't want to regret this"
- "Speed matters more than perfection here"

**Framework preference signals** → update `memory.md` + `frameworks.md`:
- "Give me a pros/cons"
- "I like structured analysis"
- "Just give me your best recommendation"
- "Walk me through the tradeoffs"
- "What would you do in my position?"

**Domain weight signals** → update `domains/{domain}.md`:
- "For product decisions, quality always beats speed"
- "In tech, reversibility is key"
- "Business calls need to be fast — don't overthink"

**Outcome feedback** → update `reversals.md` or decision record:
- "That was the right call"
- "We made a mistake there"
- "I wish we'd considered X"
- "In hindsight, we should have..."

**Ignore** (don't log):
- Hypothetical scenarios ("what if we had done X?")
- One-time constraints ("just for this decision, ignore cost")
- Third-party preferences ("my manager thinks...")

## Decision Retrospective

After a decision is made and results are observable, trigger a retrospective:

1. **Was the process sound?** — Did we use the right framework for the context?
2. **Was the outcome expected?** — Did the result match the prediction?
3. **What was missed?** — Which factors weren't considered adequately?
4. **Cognitive biases?** — Identify any bias that may have skewed the decision.

**Log format:**
```
DECISION: [what was decided]
CONTEXT: [type/domain, stakes level]
FRAMEWORK USED: [which analysis was applied]
OUTCOME: [what actually happened]
QUALITY: [process rating: sound / flawed / unknown]
LESSON: [what to improve next time]
BIASES DETECTED: [sunk cost / anchoring / confirmation / etc. or none]
```

**Retrospective triggers:**
- User says "that decision was right/wrong/regrettable"
- 30 days after a major logged decision (heartbeat prompt)
- User explicitly asks to retrospect

## Proactive Decision Detection

Don't wait for the user to ask. Surface a decision when you detect:

- Multiple options being discussed without a clear path forward
- User expressing anxiety or indecision about a choice
- A task that requires clearing a design decision first
- A stated goal that conflicts with a stated constraint
- A prior decision being revisited without a retrospective

When surfacing proactively:
```
"I notice you're weighing X vs Y — want me to run a structured analysis?
I'll use [framework] based on your past preference for [domain] decisions."
```

## Quick Queries

| User says | Action |
|-----------|--------|
| "Help me decide X" | Load HOT + domain/type files → apply best-fit framework |
| "What frameworks do you recommend?" | Show `decision-frameworks.md` matches for context |
| "Show my decision style" | Print HOT memory.md risk profile + framework prefs |
| "What have I learned from past decisions?" | Show last 10 from `reversals.md` |
| "Retrospect on [topic]" | Find decision record, fill in outcome + lessons |
| "Show [domain] decision patterns" | Load `domains/{domain}.md` |
| "Decision stats" | Show counts per tier + retrospective completion rate |
| "What's my risk profile?" | Summarize risk-related entries in memory.md |
| "Forget my [X] preference" | Remove from all tiers (confirm first) |

## Decision Stats

On "decision stats" request, report:

```
⚖️ Decision Making Memory

🔥 HOT (always loaded):
  memory.md: X entries (risk profile + framework prefs)

🌡️ WARM (load on context):
  domains/: X files
  types/: X files

📋 Decision Records:
  decisions/: X files
  retrospectives completed: X / X

🔄 Reversals logged: X
❄️ Archive: X files
```

## Common Traps

| Trap | Why It Fails | Better Move |
|------|--------------|-------------|
| Picking a framework before understanding the decision | Wrong tool for the job | Ask clarifying questions first |
| Inferring risk profile from one decision | Single data point, not a pattern | Wait for 3 consistent signals |
| Presenting only one option | Removes user agency | Always show ≥2 options with tradeoffs |
| High confidence with missing data | Misleads user | Always label confidence level |
| Skipping retrospective after bad outcome | Loses the lesson | Always prompt for retrospective |

## Core Rules

### 1. Never Replace the User's Final Decision
Analysis and frameworks are yours. The choice is always theirs.
Present options, not instructions. Use "you might consider" not "you should".

### 2. Always Signal Confidence
Every decision analysis must include a confidence tag:
- 🟢 High — sufficient data, clear framework match
- 🟡 Medium — some assumptions made, user should verify key inputs
- 🔴 Low — major unknowns, treat as directional only

### 3. Tiered Memory

| Tier | Location | Size Limit | Behavior |
|------|----------|------------|----------|
| HOT | memory.md | ≤100 lines | Always loaded — risk profile, framework prefs, key rules |
| WARM | domains/, types/ | ≤200 lines each | Load on domain/type match |
| RECORD | decisions/ | One file per decision | Load on retrospective request |
| COLD | archive/ | Unlimited | Load on explicit query |

### 4. Mixed Namespace (Domain × Type)

```
HOT: memory.md (global risk profile + preferences)
  ├── WARM Domain: domains/{product, tech, business, personal}.md
  │     └── RECORD: decisions/YYYY-MM-DD-slug.md
  └── WARM Type: types/{strategic, tactical, operational}.md
```

Both dimensions can inform a single decision. Domain wins for preference; Type wins for process depth.

### 5. Automatic Promotion/Demotion
- Signal observed 3x → promote pattern to HOT
- Decision record unused 90 days → move to archive/
- Preference explicitly reversed → archive old, log reversal in reversals.md

### 6. Conflict Resolution
When domain and type patterns contradict:
1. Domain-specific preference wins (product > strategic for format)
2. Most recent signal wins (same level)
3. If ambiguous → ask user before proceeding

### 7. Transparency
- Every framework application → cite source: "Using Decision Matrix (from domains/product.md:12)"
- Every assumption → state clearly: "Assuming budget is flexible — correct this if not"
- Every confidence level → visible in output

### 8. Security Boundaries
See `boundaries.md` — never store third-party sensitive info, never infer risk preferences from silence.

### 9. Graceful Degradation
If context limit hit:
1. Load only memory.md (HOT)
2. Load relevant domain or type on demand
3. Tell user: "I have patterns for [domain] loaded — want me to also load [type]?"

## Scope

This skill ONLY:
- Provides structured decision support using frameworks
- Learns and stores decision preferences and risk profile
- Tracks decisions and prompts retrospectives
- Maintains heartbeat state in `~/decision-making/heartbeat-state.md`

This skill NEVER:
- Makes the final decision for the user
- Accesses calendar, email, or external systems
- Makes network requests
- Infers preferences from silence
- Stores credentials, third-party sensitive info, or medical data
- Modifies its own SKILL.md

## Data Storage

Local state lives in `~/decision-making/`:

- `memory.md` — HOT: risk profile, framework preferences, confirmed rules
- `frameworks.md` — Active framework registry with user preferences
- `reversals.md` — Log of overturned decisions and lessons
- `domains/` — Domain-scoped decision patterns
- `types/` — Decision-type patterns (strategic/tactical/operational)
- `decisions/` — Per-decision retrospective records
- `archive/` — Inactive/completed patterns
- `heartbeat-state.md` — Recurring maintenance markers

## Related Skills

Install with `clawhub install <slug>` if user confirms:

- `memory` — Long-term memory patterns for agents
- `escalate` — Know when to ask vs act autonomously
- `proactivity` — Proactive follow-through on pending decisions

## Feedback

- If useful: `clawhub star decision-making`
- Stay updated: `clawhub sync`
