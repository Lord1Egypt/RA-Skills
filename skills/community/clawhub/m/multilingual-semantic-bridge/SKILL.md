---
name: multilingual-semantic-bridge
description: Help non-English-first users hit the right technical answer when docs, memory, configs, skills, and runbooks are stored under English-heavy names. This bridge improves semantic/vector retrieval usage by shaping better multilingual-to-technical target matching, without claiming to replace the retrieval engine itself.
---

# Multilingual Semantic Bridge

Sometimes one phrasing hits and another phrasing misses.
Sometimes a synonym misses.
Sometimes a different language misses.
Sometimes the answer is already in memory, docs, config, a runbook, or a skill, but retrieval still fails because the wording and the stored technical target do not line up cleanly enough.

This skill exists to reduce that failure mode.

Use this skill to bridge between:
- the user's wording
- the system's likely terminology
- the actual retrieval or routing surface that matters

The goal is not translation for its own sake.
The goal is to recover the **right technical target**.

## Public links
- GitHub: https://github.com/ChriX-Goh/multilingual-semantic-bridge
- ClawHub: https://clawhub.ai/chrix-goh/multilingual-semantic-bridge

## Mainline workflow

### 1. Preserve the original input
Keep the user's original wording available.
It may contain:
- nuance
- local nicknames
- symptom wording
- exact fragments that should not be lost

Do not discard the original phrasing just because a technical reformulation seems cleaner.
The original wording is one of the retrieval candidates.

### 2. Derive canonical intent
Identify the stable underlying request independent of surface language.
Examples of what to recover:
- the actual problem being described
- the actual capability being requested
- the actual technical uncertainty being resolved

Canonical intent should usually be treated as the default middle layer for non-trivial technical work.
Use it especially when:
- the user wording is colloquial or compressed
- the wording emphasizes symptoms rather than the real target
- several nearby targets could match the same surface phrase
- the task is to distinguish capability vs implementation vs root cause

### 3. Generate a technical pivot
Express the canonical intent in the technical language most likely to match the real target.
Very often that means an English technical pivot because these targets are often English-heavy:
- docs
- config keys
- package names
- CLI commands
- logs
- error messages
- past engineering notes

Do not force this step blindly for every query.
Strongly prefer it when the target surface is:
- official documentation
- skill metadata / skill routing
- an English-named operational file or document
- logs, provider names, config keys, CLI commands, or exact technical tokens

Use it more lightly when the target is mixed-language local memory and the original phrasing already overlaps well with existing notes.

### 4. Bridge terminology
Connect:
- user wording
- local/project wording
- official terminology

Do this to improve matching, not to build a phrasebook.
Focus on canonical term bridges that help the system hit the right target surface.

### 5. Improve retrieval and routing
Use the combination of:
- original input
- canonical intent
- technical pivot
- bridged terminology

to improve the odds of reaching the correct:
- memory snippet
- local file/doc
- official doc page
- skill
- tool path

Choose the lightest effective retrieval mix:
- for mixed-language local memory, original phrasing + canonical intent is often enough
- for official docs and skills, canonical intent + technical pivot is usually stronger
- for exact-token targets, keep identifiers and official terms verbatim

Routing rule from current evidence:
- if the real target is prior work, prior decisions, local chronology, local incidents, user corrections, or durable local lessons, prefer **memory first**
- if the real target is upstream behavior, official command semantics, official error handling, config/reference docs, or product docs pages, prefer **official docs/artifact first**
- if the real target is which installed skill should apply or what a skill says to do, prefer **skill artifact first**
- if the real target is a self-service recovery procedure, local operational doc, handoff note, or environment-specific runbook, prefer **runbook/local-file first**
- if the user already provides an exact command, config path, filename, or other exact identifier, prefer the matching **exact-token artifact surface first**

Anti-drift rule:
- do not default everything into memory-first behavior just because memory search is available
- choose the surface that matches the target class, then use the bridge inside that surface

### 6. Persist confirmed mappings
When a mapping repeatedly proves useful, persist it in the right place.
Learn canonical mappings and retrieval improvements, not random language debris.
Persist what improves future target matching, not what merely looked linguistically interesting once.

## What to consult

Read these only when needed:
- `references/query-expansion.md`
- `references/retrieval-playbooks.md`
- `references/learning-loop.md`
- `references/publication-readiness.md`

Older support material should not override this mainline.

## Standard of success

The skill is succeeding when it helps the assistant find or route to the right technical target more reliably than naive same-surface wording alone.

## Relationship to the plugin

The plugin is the automatic narrow on-ramp.
This skill remains the deeper method.

Use the plugin as the first lightweight bridge layer when the target class is already fairly obvious.
Use the fuller skill discipline when the real work is target-surface arbitration, canonical-intent derivation, or reusable terminology mapping.

See the GitHub repo for the current plugin cooperation contract and broader project context:
- https://github.com/ChriX-Goh/multilingual-semantic-bridge
