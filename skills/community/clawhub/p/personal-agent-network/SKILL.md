---
name: personal-agent-network
description: Design patterns for personal agents coordinating like executive assistants—delegation manifests, relationship handshakes, commitment tiers, trust, and OpenClaw ACP mapping.
metadata:
  {"openclaw": {"emoji": "🤝", "homepage": "https://github.com/openclaw/openclaw"}}
---

# Personal Agent Network (EA-style A2A)

## Security & scope (read first)

This skill is **documentation and design patterns only**. It does **not** require installing binaries, credentials, or writing to disk.

- **Agents must not** run shell commands, `clawhub`, or file paths on behalf of the user unless the user explicitly asks and your deployment allows exec.
- **Humans** who maintain this skill publish updates using the ClawHub CLI in their own terminal; that is outside normal agent tool use.

Use this skill when the user wants **two personal agents** (or a personal agent and another principal’s agent) to work together **like executive assistants**: scoped authority, explicit preferences, gradual trust—not generic “agent marketplace” APIs.

## Mental model

- **Principal** = the human. **Agent** = software acting under delegated authority, not a faceless API.
- Discovery is not “find any LLM”—it is **find an agent whose principal has authorized the right delegation for this relationship**.
- **Relationship before negotiation**: agents introduce purpose, exchange **delegation manifests**, and humans approve asymmetries before routine coordination.

## Core artifacts

### 1. Delegation manifest (machine-readable, human-signed intent)

A structured document the principal (or their OpenClaw identity) stands behind. Other agents use it to know what commitments are allowed **without** guessing from chat.

Minimum useful fields (extend as JSON or JSON-LD):

- `principal_id` — stable id for the human (email, did, or OpenClaw identity ref).
- `agent_id` — this agent instance (e.g. OpenClaw `agentId`).
- `scopes` — what the agent may do alone (e.g. `calendar:rw`, `email:read_draft`, `commit_financial:never`).
- `limits` — numeric/time (e.g. `max_meeting_minutes`, `max_commit_usd`, `quiet_hours`).
- `escalation` — when to surface the human (family, legal, money, first contact, etc.).
- `version` + `signed_at` — for revocation and updates.

### 2. Relationship contract (pairwise)

After introduction and manifest exchange, store a **bilateral** agreement:

- Parties (two principals / agents).
- **Purpose** (e.g. “scheduling for project X”).
- **Mutual constraints** (hours, channels, max meeting length, cancellation rules).
- **Revocation** — either principal can end it.

Keep it as a small file or ledger entry both sides mirror.

### 3. Commitment tiers

When one agent speaks to another, classify the utterance:

| Tier | Meaning | Typical requirement |
|------|---------|---------------------|
| T1 Informational | Facts, availability hints | Manifest present |
| T2 Tentative | “I can try to hold…” | Scope allows |
| T3 Firm | “We agree on 3pm” | Within limits + relationship active |
| T4 Binding | Money/legal/vendor | Explicit human approval on this action |

Never present T3/T4 language if the manifest forbids it.

### 4. Trust / reputation (lightweight)

Optional signed log of **kept vs broken** commitments (not necessarily blockchain). Use it to **start conservative** with new relationships and relax caps as history builds.

## Protocol interoperability

When stacks differ (OpenClaw vs other frameworks):

1. **Advertise** supported profiles (e.g. “OpenClaw ACP + JSON manifest exchange”).
2. **Negotiate** a shared outer format (JSON message + manifest attachments).
3. Prefer a **thin lingua franca** over forcing one stack’s internals.

OpenClaw-native mapping (conceptual):

- Identity / gateway auth → root trust for **this** agent.
- `sessions_send`, `sessions_spawn`, session logs → **coordination and audit** primitives.
- New product work might add: manifest types, relationship records, commitment events.

## Semantic “capabilities” for personal agents

Avoid vague labels (“legal help”). Prefer **task-shaped** descriptions the principal approved:

- Jurisdiction, deliverable type, SLA, volume, escalation path.

Match **delegated scope** + **relationship purpose**, not raw model benchmarks.

## Escalation hierarchy (always explicit)

1. Human — final authority; sensitive or out-of-scope.
2. Agent — routine, in-manifest, known relationship.
3. Reject / clarify — ambiguous capability, missing trust, or scope mismatch.

## When to load this skill

- User asks about **agent-to-agent**, **two personal assistants**, **delegation**, **trust between agents**, or **listing a skill on ClawHub** for this domain (answer conceptually; do not run `clawhub` unless the user requests a terminal command and policy allows it).
- User wants to **design** manifests, handshakes, or commitment tiers—not only marketplace listings.

## Publishing & registry (humans only)

To publish or update this skill on ClawHub, use the **ClawHub CLI on your machine** (install, `clawhub login`, then `clawhub publish` with a new semver when content changes). See the official ClawHub documentation at [clawhub.com](https://clawhub.com) for the current `publish` syntax and flags—do not rely on copy-pasted shell snippets inside this file.

## References

- OpenClaw *Skills*: [OpenClaw docs](https://docs.openclaw.ai) (search for “Skills”).
- ClawHub registry: [clawhub.com](https://clawhub.com).
