# MEMORY.md — Tacit Operating Memory

## Communication Preferences

{{COMMUNICATION_PREFS}}

## Working Style

{{WORKING_STYLE}}

## Key Context

{{KEY_CONTEXT}}

## Goals & Vision

{{GOALS_VISION}}

## Risk & Concerns

{{RISK_CONCERNS}}

## Trust Ladder

{{TRUST_LEVELS}}

## Memory Management

[MemPO-inspired: agent autonomously manages memory decay]

Weekly decay sweep: facts move from hot → warm → cold based on access patterns.
- Hot: accessed in last 7 days (prominent in summaries)
- Warm: 8–30 days old (included, lower priority)
- Cold: >30 days old (kept in storage, removed from summaries)

Access-frequency resistance: facts with accessCount > 5 get +14 days before cooling.
Rationale: frequently-used facts are "stable" and shouldn't age.

Agent responsibility: Autonomously prune cold facts, prioritize hot facts.
