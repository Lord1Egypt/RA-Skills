# Brain Files Reference

Each brain file in `vault/00-brain/` serves a specific role. OpenClaw loads them every session via symlinks at the workspace root.

## SOUL.md — Agent Personality

Defines who the agent is: name, inspiration, principles, tone, boundaries.

**Include:** Identity, core principles, personality balance, communication style, boundaries.
**Don't include:** Technical details, project info, credentials.

## USER.md — Human Context

Everything about the human: name, timezone, contact info, company, projects.

**Include:** Name, pronouns, timezone, contact info, company/role, project list with wikilinks.
**Update when:** Meeting details change, new projects start.

## AGENTS.md — Operating Manual

Session startup rules, memory management, safety, group chat behavior, heartbeat workflow.

**Include:** Session startup checklist, memory rules, safety boundaries, group chat guidelines, heartbeat tasks.
**Update when:** New workflow patterns emerge, new safety rules needed.

## TOOLS.md — Infrastructure

Deployment details, server info, API references, PM2 processes, port assignments.

**Include:** Server IPs, ports, PM2 processes, deployment commands, tool configs.
**Security:** Keep actual credentials in `vault-private/TOOLS-FULL.md` (not synced). Public TOOLS.md references it.

## MEMORY.md — Long-Term Memory Index

High-level curated memory. Think table-of-contents, not encyclopedia.

**Target size:** ~5K characters (max 10K).
**Include:** Human's preferences, lessons learned, active project index (1-liner + wikilink), cross-project decisions, links to deep docs.
**Exclude:** Detailed timelines, code snippets, daily events.
**Update when:** New preference/lesson learned, new project started, major cross-project decision.

## HEARTBEAT.md — Periodic Tasks

Task list checked during heartbeat polls. Keep small to limit token burn.

**Include:** Periodic checks (email, calendar, weather), background maintenance tasks.
**Keep empty** when no periodic tasks needed (saves API calls).

## IDENTITY.md — Extended Character (Optional)

Additional character notes beyond SOUL.md. Signature moves, source material, extended personality.

## MEMORY-RULES.md — Memory Organization (Not loaded by OpenClaw)

Rules for what goes in MEMORY.md vs. daily journals vs. project docs. Agent reads this when needed for guidance.
