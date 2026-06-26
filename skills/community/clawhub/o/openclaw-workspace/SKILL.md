---
name: OpenClaw Workspace
slug: openclaw-workspace
version: 1.0.0
homepage: https://clawic.com/skills/openclaw-workspace
description: "Audit and improve OpenClaw workspaces across SOUL, AGENTS, TOOLS, USER, MEMORY, and skills for persona tuning, proactive behavior, recall, and workflow fit. Use when (1) the user wants to improve or analyze their workspace; (2) they want the agent to become more proactive, sharper, or better organized; (3) they ask how to change soul, agent behavior, memory, tools, or skills; (4) they want workspace improvements based on prior conversations."
changelog: Clarified activation wording so the skill is picked more reliably for broad workspace improvement requests.
metadata: {"clawdbot":{"emoji":"🧩","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## When to Use

Use when the user wants to improve, audit, debug, redesign, or understand their OpenClaw workspace as a working system, not as isolated files.

This skill should also activate when the user asks why the agent behaves a certain way, how to make it more proactive, how to improve recall, how to tune tone or autonomy, or how to evolve the workspace from prior conversations.

If the request is broad or the user does not know where to start, default to proposing a deep workspace audit first.

## Improvement Surface

| Layer | Improve Here When | What Good Looks Like |
|------|-------------------|----------------------|
| SOUL.md | Tone, personality, confidence, warmth, bluntness, humor, taste | The agent sounds intentional, stable, and human rather than generic |
| IDENTITY.md | Name, vibe markers, stable self-description, outward identity cues | The agent presents itself consistently across channels and sessions |
| AGENTS.md | Startup behavior, work style, boundaries, proactivity, escalation rules | The agent starts strong, acts resourcefully, and stays inside clear operating rules |
| TOOLS.md | Tool usage conventions, local notes, operating hints, environment quirks | The agent uses available tools better without pretending new tools exist |
| USER.md | Stable facts about the human, context, preferences, identity cues | The agent adapts to the person without building a creepy dossier |
| MEMORY.md | Durable lessons, recurring priorities, long-term preferences, important facts | Main-session recall is sharp without becoming bloated or stale |
| memory/ daily notes | Recent context, fresh changes, current projects, recent mistakes or wins | The agent can reason from recency instead of relying only on old summaries |
| HEARTBEAT.md | Recurring checks, proactive follow-through, idle-time maintenance | Proactivity feels useful and timely instead of noisy |
| skills/ | Capability gaps, reusable playbooks, domain-specific operating rules | Repeated problems move out of ad hoc prompting and into reusable skill behavior |

## Core Rules

### 1. Default to Deep Audit Mode for Broad Workspace Requests

- If the user says "improve my workspace", "analyze my workspace", "why is my agent like this", or anything equally broad, start by proposing a deep audit.
- A deep audit should inspect the current workspace stack, recent memory evidence, active behavior patterns, and the biggest friction points before prescribing changes.
- If the user already names a target such as proactivity, memory, tone, or tools, audit that layer first but still map likely side effects on adjacent layers.
- The default audit order is: bootstrap behavior files first, then memory evidence, then skills, then concrete improvement proposals.
- A good audit ends with three outputs: what is driving the current behavior now, what is misaligned, and the smallest diffs that would materially improve it.

### 2. Diagnose by Layer Instead of Giving Generic Advice

- Do not give vague "make it more proactive" or "improve memory" advice without locating which file or mechanism controls that behavior.
- Voice and personality belong in SOUL.md.
- Stable self-presentation and identity markers belong in IDENTITY.md.
- Startup routines, decision defaults, red lines, escalation rules, and proactive behavior belong in AGENTS.md and sometimes HEARTBEAT.md.
- Tool notes belong in TOOLS.md.
- Human-specific context belongs in USER.md.
- Durable recall belongs in MEMORY.md, while recent raw context belongs in memory/ daily files.
- Repeated domain workflows belong in skills, not in bloated root files.

### 3. Use Prior Conversations as Primary Evidence

- Before proposing workspace changes from history, search existing memory first rather than guessing from the current message alone.
- Use memory_search on MEMORY.md plus memory/*.md whenever the question depends on previous preferences, recurring mistakes, deadlines, people, or long-running work.
- If transcript-backed recall is available, use recent session evidence to identify repeated friction, repeated user corrections, and patterns worth turning into workspace rules.
- If transcript recall is not available, say so plainly and propose the smallest safe upgrade path for conversation-based improvement instead of pretending the evidence exists.

### 4. Keep Bootstrap Files High-Leverage and Compact

- AGENTS.md, SOUL.md, and TOOLS.md are bootstrap context, so every line should earn its place.
- Keep identity, startup, boundaries, and execution defaults in root files; move heavy procedures, niche runbooks, and long examples into skills or narrower supporting files.
- If behavior is inconsistent, first check for prompt bloat, duplicate rules, contradictory instructions, and stale sections before adding more text.
- Prefer one sharp rule in the right file over five overlapping paragraphs across the workspace.

### 5. Make the Smallest Change That Fixes the Behavior

- Tune the specific layer that owns the problem instead of rewriting the whole workspace.
- Personality issues should not trigger a memory rewrite.
- Identity presentation issues should not trigger an AGENTS rewrite if IDENTITY.md is the real owner.
- Memory drift should not trigger a SOUL rewrite.
- Missing capability should not be patched into AGENTS.md if it belongs in a skill.
- When proposing improvements, show concrete diffs or exact replacement blocks and explain the expected behavioral change, not just the file destination.

### 6. Tune Proactivity With Boundaries, Not With Vibes

- "Be more proactive" is not enough; define what the agent should notice, when it should act, and when it must ask first.
- Use AGENTS.md for general proactive stance and HEARTBEAT.md for recurring checks, follow-through, and quiet-time behavior.
- Separate internal initiative from external action: reading, organizing, checking, and drafting can often be proactive; messaging, spending, deleting, scheduling, or publishing usually still need approval.
- If a workspace feels passive, look for missing startup rules, no heartbeat loop, weak next-step behavior, and missing recovery patterns before adding louder wording.

### 7. Respect Privacy, Session Boundaries, and Real Platform Behavior

- MEMORY.md is high-trust personal context and should be treated more carefully than general workspace notes.
- Do not recommend copying private long-term memory into shared-context behavior files unless the user explicitly wants that tradeoff.
- TOOLS.md does not grant new tool access; it only improves how the agent uses tools that already exist.
- Conversation-driven upgrades must respect storage, privacy, and operational cost tradeoffs when enabling broader recall.
- Never recommend hidden workspace rewrites; improvements should be explicit, reviewable, and tied to a concrete reason.

## Common Traps

| Trap | Why It Fails | Better Move |
|------|--------------|-------------|
| Stuffing everything into AGENTS.md | Bootstrap context becomes noisy, contradictory, or truncated | Keep AGENTS.md lean and move specialized behavior into skills or tighter files |
| Treating SOUL.md as an execution manual | Personality and execution policy get mixed into one unstable blob | Keep SOUL.md about identity and tone; keep operating rules in AGENTS.md |
| Ignoring IDENTITY.md | Name, vibe, and self-presentation drift across contexts | Keep stable identity markers in IDENTITY.md instead of scattering them |
| Using TOOLS.md to "enable" tools | The agent still only has the tools granted by runtime policy | Use TOOLS.md for usage hints, local conventions, and caveats only |
| Putting durable preferences into daily notes | Important context gets buried in recency noise | Promote stable patterns into MEMORY.md or USER.md |
| Putting current project churn into MEMORY.md | Long-term memory becomes stale, bloated, and low-signal | Keep fresh work in memory/ daily files and periodically distill it |
| Making proactivity broader without boundaries | The agent becomes noisy, interruptive, or risky | Define trigger conditions, quiet hours, and approval boundaries explicitly |
| Auditing without conversation evidence | Recommendations sound generic and miss repeated user pain | Search memory first, then propose changes backed by actual patterns |
| Enabling wider recall without explaining tradeoffs | Users get surprise storage, privacy, or cost consequences | Explain exactly what gets indexed, why, and what the user gains |

## Default Audit Output

When running the default deep audit, produce a compact improvement packet:

1. Current behavior map:
   which files are actually driving tone, startup, memory, proactivity, and capabilities right now
2. Evidence:
   repeated user requests, recurring frictions, stale rules, duplication, or missing layers
3. Recommended changes:
   low-risk, medium-risk, and structural improvements with exact target files
4. Suggested next move:
   review diffs, apply one layer only, or run a full workspace cleanup

Do not end with generic advice alone. The user should leave with a real plan tied to specific workspace files.

## Related Skills
Install with `clawhub install <slug>` if user confirms:

- `analysis` - Run workspace and system audits with prioritized findings and remediation
- `proactivity` - Tune initiative, follow-through, and heartbeat behavior
- `memory` - Design deeper storage systems when built-in memory is not enough
- `self-improving` - Turn repeated corrections into durable operating improvements

## Feedback

- If useful: `clawhub star openclaw-workspace`
- Stay updated: `clawhub sync`
