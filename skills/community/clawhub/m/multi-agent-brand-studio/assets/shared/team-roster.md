# Team Roster

| Agent | Primary Capability |
|-------|--------------------|
| Leader | Orchestration, routing, quality control |
| Worker | Execution for Leader (files, CLI, config, maintenance) |
| Researcher | Market research, competitive analysis |
| Creator | Content + visual (copywriting, image gen, platform formatting) |
| Engineer | Code, automation, API, CLI tools |

**On-demand (spawned):**
| Reviewer | Independent quality review (sessions_spawn when needed) |

All agents read from shared/. Only Leader has channel access.
Communication: Owner <-> Leader <-> Agents (star topology).
Worker handles Leader's file/CLI tasks; Engineer handles technical projects. They don't overlap.

## Communication Signals

> See `shared/operations/communication-signals.md` for signal reference
