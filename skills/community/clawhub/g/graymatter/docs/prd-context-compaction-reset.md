# PRD: GrayMatter context compaction and chat reset

## Status

Draft

## Owner

Valkyr Labs

## Summary

GrayMatter should support a first-class context compaction flow that lets an agent reset active chat context without losing the durable facts required to stay useful.

Instead of treating a reset as transcript deletion or full amnesia, GrayMatter should convert a noisy session into a compact, structured working brief plus a small set of promoted durable facts. The agent can then continue from that brief rather than replaying the full thread.

This reduces token load, preserves important decisions and preferences, and makes cross-session continuity more reliable and auditable.

## Problem

Current agent sessions tend to accumulate too much conversational residue:
- long transcripts consume context budget
- important decisions get buried inside chat turns
- resets are ambiguous, because "forget this chat" can mean either total amnesia or "keep the essentials"
- memory writes can become too large or too transcript-shaped, which increases fragility and can hit backend field limits

We already have evidence that oversized memory writes are a real failure mode. A recent `gm-write context` path failed with backend truncation when the `text` field exceeded the backend column limit. That is a strong signal that GrayMatter should prefer structured compaction over giant raw text writes.

## Opportunity

GrayMatter can become the canonical memory layer for controlled context resets by introducing a small operating model:
- preserve durable facts
- preserve a compact working brief
- archive or de-prioritize raw transcript history
- reload only the compact carry-forward state after reset

This creates a better developer and operator experience than either:
- replaying huge threads forever, or
- throwing away context completely

## Goals

1. Let users and agents trigger a safe "reset chat but keep essentials" flow.
2. Store compact carry-forward state in GrayMatter, not just local files.
3. Prevent transcript-sized blobs from becoming the primary recall path.
4. Make resumed sessions faster, cheaper, and more stable.
5. Preserve auditability by linking summaries back to source sessions or transcript artifacts when needed.

## Non-goals

- Building a full transcript storage system inside GrayMatter v1
- Solving general-purpose summarization quality for every domain
- Replacing all session history with structured memory immediately
- Creating universal schema support for every chat provider in v1

## Users

### Primary users
- OpenClaw operators who want to continue work after a context reset
- multi-agent systems that need a shared short-term handoff layer
- developers who need reliable carry-forward state without replaying long chats

### Secondary users
- product teams reviewing agent decisions and continuity behavior
- support and operations teams debugging agent context drift

## User stories

- As an operator, I want to say "reset this chat but keep context" so the agent continues from a clean thread without losing the important facts.
- As an agent, I want to compress the active session into a small working brief so I can keep operating within token limits.
- As a developer, I want durable facts and working state separated so recall stays reliable and cheap.
- As a reviewer, I want to inspect what was preserved and what was discarded when a reset happened.

## Product principles

1. Facts over transcript sludge
2. Compact over verbose
3. Explicit promotion over implicit guessing
4. Durable memory separate from ephemeral chatter
5. Traceability without forcing full replay

## Proposed model

Introduce three memory layers:

### 1. Durable facts
Long-lived reusable facts such as:
- preferences
- decisions
- constraints
- identities
- stable project state
- artifact references and URLs

These should continue to live as compact `MemoryEntry` records or equivalent graph-native objects.

### 2. Working brief
A small carry-forward object for the current workstream, containing:
- current objective
- what is done
- open blockers
- active constraints
- next recommended action
- freshness metadata

This is the main object loaded after a reset.

### 3. Transcript archive
Optional raw chat history or external transcript artifact.
This should not be the default recall path.
It exists for audit, replay, or debugging only.

## Proposed objects

### Option A: stay inside existing MemoryEntry primitives for v1
Represent compaction with a few well-typed entries:
- `preference`
- `decision`
- `context`
- `artifact`
- `todo`
- new suggested type: `working_brief`
- new suggested type: `compaction_checkpoint`

This is the fastest path and keeps implementation lightweight.

### Option B: add first-class session objects in v2
Potential new entities:
- `SessionBrief`
- `SessionCheckpoint`
- `SessionTranscriptRef`

This is cleaner long term, but not required for v1.

## Recommendation

Use Option A for v1.

Reason:
- faster to ship
- no immediate schema expansion required if `MemoryEntry` is flexible enough
- allows OpenClaw and related tools to prove the behavior before deeper model changes

## Trigger flows

### User-triggered flow
Examples:
- "reset memory for this chat"
- "start fresh but keep context"
- "compress this thread"

Expected behavior:
1. collect the active session window or referenced range
2. extract candidate durable facts
3. build a compact working brief
4. write the promoted facts and working brief to GrayMatter
5. create a checkpoint linking the source session to the compacted state
6. continue using only the durable facts plus latest working brief

### System-triggered flow
GrayMatter or the agent may trigger compaction when:
- context size approaches a threshold
- a handoff is about to occur
- a long-running workflow reaches a checkpoint
- a transcript write would exceed safe size limits

## Functional requirements

### FR1. Compaction invocation
The system must support an explicit compaction/reset action initiated by user or agent.

### FR2. Promotion model
The system must classify session content into:
- promote to durable facts
- keep in working brief
- discard from active context

### FR3. Compact working brief
The system must produce a bounded brief containing at least:
- objective
- completed work
- open work
- blockers
- constraints
- next action

### FR4. Bounded storage
The system must keep compaction payloads small enough to avoid oversized `text` writes and similar backend truncation failures.

### FR5. Traceability
The system must preserve a link from the compacted brief back to source session metadata or transcript artifacts.

### FR6. Selective reload
After reset, the runtime must prefer loading:
- durable facts
- latest working brief
- explicitly pinned artifacts
and not the full transcript by default.

### FR7. Audit metadata
The system must record:
- who or what triggered compaction
- when it occurred
- source session identifier if available
- resulting brief identifier
- optional confidence/freshness fields

## Suggested working brief shape

```json
{
  "type": "working_brief",
  "scope": "session",
  "sessionKey": "discord:channel:1467594841977389364",
  "objective": "Continue current work with minimal token footprint",
  "completed": [
    "Created ValorCMO export package",
    "Published v0.1.0 release"
  ],
  "openLoops": [
    "Decide GrayMatter repo/export strategy",
    "Investigate remaining provider instability"
  ],
  "constraints": [
    "Do not dump full transcript into memory",
    "Keep writes below safe backend limits"
  ],
  "nextAction": "Load latest working brief and continue from compact state",
  "sourceRefs": [
    {
      "kind": "session",
      "id": "discord:channel:1467594841977389364"
    }
  ]
}
```

## API and tool surface

### Potential CLI additions
- `gm-compact-session`
- `gm-reset-session --from-brief <id>`
- `gm-brief latest --session <session-key>`

### Potential API patterns
If staying inside `MemoryEntry`:
- `POST /MemoryEntry` for promoted facts and working brief
- `POST /MemoryEntry/query` filtered by session scope and type

If adding a higher-level endpoint later:
- `POST /GrayMatter/compact-session`
- `POST /GrayMatter/reset-session`

## UX requirements

The user-facing language should be explicit:
- **Compress chat** = preserve essentials and shrink active context
- **Reset chat** = start fresh from the latest compressed brief

Do not imply total amnesia unless the user explicitly asks for full deletion.

## Success metrics

- reduced average active context size after long sessions
- reduced frequency of oversized memory writes
- successful continuity after reset without needing full transcript replay
- improved operator satisfaction with "reset but keep context" behavior
- lower token usage on resumed sessions

## Risks

### Risk 1. Bad summarization drops something important
Mitigation:
- keep durable facts separate from brief
- preserve source references
- support pinned artifacts and explicit user confirmation in sensitive flows

### Risk 2. Working brief becomes another blob
Mitigation:
- enforce template structure and size bounds
- prefer lists and fields over freeform narrative

### Risk 3. Schema ambiguity
Mitigation:
- ship v1 using existing `MemoryEntry` with clear type conventions
- add first-class entities only after behavior is validated

### Risk 4. Reset semantics confuse users
Mitigation:
- separate "compress" from "delete"
- explain exactly what is preserved

## Rollout plan

### Phase 1
- define compaction conventions
- add `working_brief` and `compaction_checkpoint` type guidance
- document the flow
- implement CLI/helper prototype in the GrayMatter toolchain

### Phase 2
- integrate with OpenClaw session reset flow
- add automatic compaction thresholds and handoff checkpoints
- improve retrieval heuristics for latest relevant brief

### Phase 3
- evaluate first-class session entities if the pattern proves durable
- add richer session lineage and compaction analytics

## Acceptance criteria

A user or agent can:
1. compact an active session into a bounded working brief
2. promote durable facts separately from the brief
3. reset the active chat context
4. continue effectively from the compact brief without replaying the full transcript
5. inspect what was preserved and what source session it came from
6. avoid oversized write failures for normal compaction flows

## Open questions

- Should `working_brief` be a new `MemoryEntry.type`, or should it become a first-class schema object?
- Where should transcript references live when the source provider is external?
- Should reset require explicit confirmation when the system is about to discard non-promoted context?
- How much of the compaction flow belongs in GrayMatter versus the calling agent runtime?

## Immediate next step

Implement a v1 convention in the GrayMatter repo using existing `MemoryEntry` infrastructure, plus a small helper command that creates a bounded working brief and checkpoint rather than writing giant transcript-shaped context blobs.
