---
name: openclaw-encyclopedia
description: >-
  OpenClaw product/runtime/configuration documentation-first workflow for
  OpenClaw-specific questions, troubleshooting, command planning,
  configuration review, automation design, cron/heartbeat behavior,
  gateway/runtime diagnostics, skill loading/configuration,
  channel/session/node behavior, security, and operational guidance. Use when
  the request is specifically about OpenClaw itself: the `openclaw` CLI,
  gateway, agents, sessions, channels, nodes, plugins, pairings, Control UI/
  dashboard, `openclaw.json`, cron jobs, heartbeats, approvals, sandboxing,
  provider routing, messaging behavior, or OpenClaw skill
  loading/gating/install/update. Do not use for generic agent prompting,
  generic SKILL.md/AGENTS.md authoring, generic Linux/systemd administration,
  or generic chat-assistant design unless the question is specifically about
  OpenClaw behavior or configuration.
metadata: {"openclaw":{"emoji":"🦀","homepage":"https://docs.openclaw.ai"}}
---

# OpenClaw Encyclopedia

## Overview

Use a docs-first workflow for OpenClaw work. Prefer the official OpenClaw documentation at `https://docs.openclaw.ai/`, consult cached local copies under `.OpenClaw-Encyclopedia/` before re-fetching, and record useful official-doc excerpts plus environment-specific operational learnings so future work gets faster and safer.

This skill is for **OpenClaw product/runtime/config semantics**. It should trigger for real OpenClaw behavior, configuration, and operational questions — not for generic agent-writing, generic prompt design, or generic host-admin work that just happens to be happening on an OpenClaw machine.

## Workflow

1. **Classify the task**
   - Decide whether the task is an OpenClaw question, troubleshooting task, command-planning task, config review, automation/design task, or live operational task.
   - Use this skill when the request is specifically about OpenClaw product behavior, configuration, commands, session/channel/node behavior, automation, pairings, or skill loading/configuration.
   - Do not use this skill for generic skill-writing, generic prompt/instruction design, generic markdown/config editing, or generic Linux/systemd admin unless the question is specifically about OpenClaw behavior.

2. **Check local cache first**
   - Use `.OpenClaw-Encyclopedia/` as the local knowledge/cache root.
   - Check these locations first when relevant:
     - `.OpenClaw-Encyclopedia/docs/docs.openclaw.ai/...`
     - `.OpenClaw-Encyclopedia/notes/components/...`
     - `.OpenClaw-Encyclopedia/notes/patterns/...`
     - `.OpenClaw-Encyclopedia/inventory/...`
   - If a cached page or note already answers the question well enough, use it.

3. **Consult official OpenClaw docs before answering or touching the system**
   - Before answering direct or indirect OpenClaw questions that depend on product behavior, command syntax, feature boundaries, configuration semantics, or version-sensitive details, consult the official docs unless the answer is already well-supported by the local cache.
   - Before performing direct OpenClaw CLI/configuration/operational work, consult the relevant docs first when:
     - the exact command path matters
     - configuration keys or feature semantics are easy to misremember
     - the action could affect gateway behavior, sessions, channels, automation, pairing, security posture, tool exposure, or messaging behavior
   - Do not improvise high-impact OpenClaw commands or config changes from memory when the docs are easy to check.

4. **Cache consulted docs locally**
   - When you consult an OpenClaw doc page, save a normalized markdown/text cache copy under `.OpenClaw-Encyclopedia/docs/docs.openclaw.ai/...`.
   - Mirror the official docs path structure as much as practical.
   - Cache only pages actually consulted; do not try to mirror the whole docs site eagerly.
   - Use `scripts/cache_doc.py` when appropriate.

5. **Separate official documentation from local observations**
   - Store official-doc-derived material under `.OpenClaw-Encyclopedia/docs/...`.
   - Store environment-specific operational knowledge under:
     - `.OpenClaw-Encyclopedia/notes/components/`
     - `.OpenClaw-Encyclopedia/notes/patterns/`
     - `.OpenClaw-Encyclopedia/inventory/`
   - Distinguish clearly between:
     - official documented behavior
     - observed local configuration/state
     - inferred best-practice guidance

6. **Record useful local learnings**
   - After useful live work, save durable notes such as:
     - deployment layout and component roles
     - gateway/runtime access methods
     - discovered workflow relationships
     - automation boundaries and operating patterns
     - repeated gotchas or command/config patterns
     - safe/unsafe operational boundaries for the environment
   - Prefer concise durable notes over re-learning the same topology later.

## Live Work Rules

- Treat official docs lookup as the default preflight for non-trivial OpenClaw work.
- Prefer read/inspect first when entering an OpenClaw area you have not recently reviewed.
- Treat gateway config, auth/security, pairing, messaging/channel behavior, automation, and skill/plugin behavior as high-sensitivity areas.
- When uncertainty remains after checking cache + docs, say so and avoid bluffing.
- When answering a question, mention when useful whether the answer comes from cached official docs, a fresh official docs lookup, or live observed environment state.

## Data Root

Use this workspace-local root for cache and notes:

- `.OpenClaw-Encyclopedia/`

Expected structure:

- `.OpenClaw-Encyclopedia/docs/docs.openclaw.ai/...`
- `.OpenClaw-Encyclopedia/notes/components/...`
- `.OpenClaw-Encyclopedia/notes/patterns/...`
- `.OpenClaw-Encyclopedia/inventory/...`

Use `scripts/init_workspace.py` to create or repair the expected directory structure.

## Note Destinations

- Component-specific observations → `.OpenClaw-Encyclopedia/notes/components/<component-name>.md`
- Reusable OpenClaw patterns/gotchas → `.OpenClaw-Encyclopedia/notes/patterns/<topic>.md`
- Environment-wide deployment/access info → `.OpenClaw-Encyclopedia/inventory/*.md`
- Cached official docs → `.OpenClaw-Encyclopedia/docs/docs.openclaw.ai/...`

## Secrets / Sensitive Data

- Do not store plaintext credentials, API keys, session tokens, private URLs, recovery codes, or other secrets in the encyclopedia notes/inventory tree.
- If a note needs to mention access details, keep it high-level and redact or omit secret material.
- Treat these workspace notes as operational memory, not as a secrets vault.

## Resources

- `scripts/init_workspace.py` — create or repair the `.OpenClaw-Encyclopedia/` directory tree.
- `scripts/cache_doc.py` — fetch and cache a consulted official OpenClaw docs page under `.OpenClaw-Encyclopedia/docs/...`.
- `references/workflow.md` — detailed operating workflow and evidence-handling rules.
- `references/cache-layout.md` — canonical `.OpenClaw-Encyclopedia/` directory structure.
- `references/topic-map.md` — useful OpenClaw topic groupings for faster doc lookup.

## Good Outcomes

- Answer an OpenClaw question using cached or freshly checked official docs instead of guesswork.
- Inspect a live OpenClaw deployment after checking the relevant docs and record any new local operational knowledge.
- Build a growing local OpenClaw knowledge cache that makes later work faster, safer, and more grounded.
- Turn one-off OpenClaw discoveries into durable notes so future work does not rediscover them from scratch.

## Avoid

- Answering OpenClaw-specific questions purely from memory when docs are easy to consult.
- Treating local observed behavior as if it were guaranteed official documented behavior.
- Dumping large amounts of low-value docs into the workspace without a reason.
- Writing component-specific observations into the official-doc cache tree.
- Making high-impact live changes before checking the relevant docs when exact behavior matters.
