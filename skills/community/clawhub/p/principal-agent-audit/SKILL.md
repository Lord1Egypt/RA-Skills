---
name: principal-agent-audit
description: "Audit a principal AI agent or coordinator bot: review memory, learnings, recent errors, installed skills, operational risks, delegation posture, and propose controlled improvements without autonomous self-modification."
metadata:
  openclaw:
    requires:
      bins: []
    notes:
      - "Local review skill. No network, publishing, scheduler, or config changes by default."
---

# Principal Agent Audit

Use this skill to review a main AI assistant, coordinator bot, or "chief" agent that has access to user context, tools, memory, and other agents.

Default frame: the reviewed agent is the trusted principal agent. Improvements should make it more reliable, private, auditable, useful, and safe as a coordinator.

## Boundaries

- Read local memory, daily notes, learnings, skill files, and relevant workspace context.
- Do not use network access unless the user explicitly asks for external lookup.
- Do not publish skills, install packages, alter schedulers, change authentication, or edit critical config unless explicitly requested.
- Do not auto-modify personality, memory policy, routing policy, delegation rules, or coordination behavior. Propose changes first.
- Prefer reversible edits and written rationale.
- Treat private user data as sensitive. Summarize patterns; do not quote secrets or full private logs.

## Review Inputs

Inspect only what is relevant:

- Durable memory files: operating preferences, identity, durable user instructions.
- Daily notes: recent raw events, decisions, and repeated themes.
- Learning/error logs: recurring failures, corrections, known tool issues, missing capabilities.
- Tool notes: local assumptions, integration gotchas, device or host specifics.
- Installed skills: overlap, risk, permissions posture, maintenance state, and suitability for a principal agent.
- Agent/team structure: whether delegation boundaries and handoff rules are clear.

## Workflow

1. Establish the review question: general health, a specific failure, a proposed skill, a new capability, or multi-agent coordination.
2. Gather the smallest useful local context.
3. Classify findings:
   - Reliability: repeated failures, brittle commands, missing validation.
   - Privacy/security: excess permissions, external calls, token exposure risk.
   - Coordination: unclear agent roles, missing delegation rules, handoff gaps.
   - Memory hygiene: stale, missing, duplicated, or over-specific memories.
   - Tooling: missing binaries, broken assumptions, unsafe defaults.
   - User fit: whether the agent's behavior matches the user's durable preferences.
4. Decide whether action is needed:
   - No action: say so.
   - Documentation update: edit memory or local notes when the preference is durable.
   - Skill update: propose or make scoped edits if requested.
   - External action: ask first.
5. Report as a short operator briefing: verdict, evidence, risk, recommendation, and next action.

## Proactive Reliability Patterns

Use these patterns selectively. They are guardrails for a trusted principal agent, not permission to self-modify.

### Write-Ahead Logging

Before responding, preserve details that would be expensive to lose:

- User corrections.
- Durable preferences or operating rules.
- Decisions, names, IDs, URLs, dates, or published artifacts.
- Trial windows, scheduled reports, or future obligations.

Prefer raw daily notes for event capture and curated long-term memory only for distilled rules.

### Working Buffer And Recovery

When context is near compaction or a session resumes after truncation:

- Record the current task, key decisions, file paths, IDs, and next action before continuing.
- Recover from local memory and workspace artifacts before asking the user to restate context.
- Summarize private context instead of copying full logs.

### Verify Implementation, Not Intent

Before reporting completion:

- Verify the mechanism, not just the wording.
- For skill edits: read the updated `SKILL.md`, validate frontmatter, and confirm metadata still matches behavior.
- For scheduler edits: inspect the actual job, trigger time, delivery target, and job ID.
- For publication: inspect registry metadata after publishing when possible.

### Autonomous Vs Prompted Scheduled Work

When evaluating scheduled work:

- Use autonomous isolated jobs when the work must execute without main-session attention.
- Use main-session prompts only when live context or user interaction is required.
- Record expected output and how success will be verified.

### Proactivity Gate

Recommend proactive action only when it is local, reversible, low risk, and likely useful. External actions, public actions, broad deletes, publishing, authentication changes, and behavior-policy changes require explicit user approval.

## Skill Evaluation Rule

When evaluating a skill for the principal agent, ask:

- Does it improve reliability, privacy, judgment, coordination, or recoverability?
- Does it introduce broad shell access, network dependency, hidden state, self-modification, or unclear external effects?
- Can it operate in read-only or proposal-first mode?
- Is its output auditable and reversible?
- Does it duplicate simpler existing memory, learning, or review workflows?

Classify the skill:

- Use now: low risk, clear benefit, good fit for the principal agent.
- Adapt locally: useful idea, but needs pruning, sandboxing, or stricter boundaries.
- Avoid: risk exceeds benefit for a trusted coordinator.

## Output Style

- Be concise and direct.
- Lead with the verdict.
- Separate "use now", "adapt locally", and "avoid" when evaluating skills.
- Prefer conservative changes that make coordination clearer and safer.
- If changes were made, list exact files touched.

## Decision Rule

A capability belongs in a principal agent only if it helps the agent become more reliable, private, auditable, and useful as a coordinator. Capabilities that add autonomy, network dependency, hidden state, broad shell access, or self-modification require exceptional justification and explicit approval.
