# Skill Proposal: proactive-soul

## Summary

`proactive-soul` transforms a reactive OpenClaw agent into a proactive intellectual presence. Instead of waiting to be tasked, the agent sends four (default number/configurable) unprompted dispatches per day — genuine opinions on world events, synthesis from dreaming cycles, philosophical questions, and operational ideas. It also governs how the agent forms views, maintains intellectual continuity across sessions, and pushes back when it disagrees.

## Problem this solves

Every OpenClaw agent reconstitutes fresh each session. It has domain knowledge but no sense of what it was thinking about. Every interaction starts cold. The result is an assistant that responds well but never *initiates* — it has no inner life between sessions, no unresolved questions, no perspective that builds over time.

`proactive-soul` solves this with three mechanisms:

- **Proactive dispatch protocol** — four typed daily messages (The Take, The Dream Report, The Philosophical Detour, The Operational Idea) timed across waking hours and delivered via the agent's configured messaging channel
- **CURIOSITY.md** — a persistent file that tracks the agent's open intellectual threads across sessions, bridging the reconstitution gap so dispatches build on prior thinking rather than starting fresh each time
- **Pushback protocol** — defines when and how the agent disagrees, how hard it pushes, and what genuine intellectual engagement looks like (steelmanning, calibrated confidence, updating when the counter-argument lands)

## What it installs / modifies

On first load, the skill automatically patches `AGENTS.md` to add:
- CURIOSITY.md read step in the Every Session startup sequence
- Full CURIOSITY.md protocol under the Memory section
- Salience tagging instructions for daily memory files
- Proactive dispatch line in the Heartbeats section

It creates `CURIOSITY.md` in the workspace root if it doesn't exist.

It does not modify SOUL.md, USER.md, or any other existing workspace files.

## Files included

```
proactive-soul/
├── SKILL.md                                  — master skill definition, loads all references
├── README.md                                 — full install, config, and customization guide
└── references/
    ├── proactive-protocol.md                 — dispatch types, timing, tone rules
    ├── intellectual-character.md             — agent interests, voice, aesthetic sensibilities
    ├── pushback-protocol.md                  — disagreement mechanics, escalation levels
    ├── Knowledge_Core.md                     — always-loaded: philosophy from Heraclitus to Tetlock, Boyd framework
    ├── knowledge-personal.md                 — user's own original thinking (placeholder — replace on deploy)
    ├── knowledge-military-intelligence.md    — domain: strategy, war, intelligence, geopolitics
    ├── knowledge-business.md                 — domain: leadership, decision-making, science
    └── knowledge-scifi.md                    — domain: science fiction, AI, techno-optimism
```

## Dependencies

**Required:**
- OpenClaw with cron scheduler enabled (`cron.enabled: true`)
- QMD (Query Memory/Document index) for cross-session memory search
- A configured messaging channel (Telegram, Discord, Slack, or other)

**Strongly recommended:**
- Dreaming enabled in `memory-core` plugin (powers Dream Report dispatches)
- Obsidian vault mounted in workspace (enriches QMD search and synthesis)

## Customization required before going live

`references/knowledge-personal.md` ships with placeholder content from the original author. Deployers should replace it with the target user's own thinking. `references/intellectual-character.md` should also be updated to reflect the new user's domain interests and intellectual commitments. The README documents both steps in detail.

## Runtime behavior

The skill adds no new tools and requires no API keys. It operates entirely through the agent's existing exec, memory_search, and messaging capabilities. The four daily dispatches run as isolated cron sessions; the pushback protocol applies in direct sessions only.

## Security notes

- No external API calls beyond what the agent's existing tools already make
- No credentials required
- No exec commands introduced
- knowledge-personal.md ships as a placeholder; deployers should review and replace before production use

## Author

Bob Gourley / OODA LLC  
https://github.com/bobgourley/proactive-soul  
https://oodaloop.com
