# Pattern: Downstream Signaling

**Purpose:** Documents the reusable design pattern where a package that updates shared artifacts explicitly signals its downstream consumer to re-process — preventing stale governance, stale tests, and stale workspaces.

---

## The Pattern

```
UPSTREAM PACKAGE updates artifacts
        │
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│  DOWNSTREAM SIGNAL                                                    │
│                                                                      │
│  ⚡ From: {upstream package}                                          │
│     To: {downstream package}                                          │
│     Event: {what changed}                                             │
│     Affected files: [list of changed files]                           │
│     Action required: {what downstream should do}                      │
└─────────────────────────────────────────────────────────────────────┘
        │
        ▼
DOWNSTREAM PACKAGE re-derives/reconciles ONLY affected artifacts
```

**One sentence:** When architecture changes flow downstream, the upstream package tells the downstream package EXACTLY what changed — so re-derivation is surgical, not full-rebuild.

---

## Where It's Used

| From | To | Signal Event | What Changes |
|------|----|-------------|-------------|
| **AI-ADLC** | AI-DWG | Architecture artifact updated (ADR revised, container added/removed) | AP files changed → workspace reconciliation needed |
| **AI-DWG** | AI-GCE | Steering files updated during reconciliation | Steering changed → rule/hook re-derivation needed |
| **AI-DWG** | AI-TGE | Steering + structure updated | Architecture commitments changed → test register update needed |
| **AI-POLC** | AI-DWG | Backlog structure changed (new epics, DoR updated) | PBP changed → workspace enrichment refresh |
| **AI-UXD** | AI-POLC | Personas/journeys updated | UXP changed → backlog reprioritization context |

---

## Why This Pattern Exists

**The problem it solves:** Without signaling, downstream packages become stale. AI-ADLC changes the tech stack → AI-DWG's steering still references the OLD stack → AI-GCE enforces rules for the OLD stack. The governance layer becomes a lie.

**Without signaling:**
- Downstream discovers staleness eventually (maybe next audit, maybe never)
- No one knows WHEN the drift started or WHAT caused it
- Full re-derivation is the only option (expensive, risky)

**With signaling:**
- Downstream knows immediately that something changed
- Signal specifies WHICH files changed (surgical re-derivation)
- Change is traceable: "ARCH-03 re-derived because api-standards.md was updated at 14:30 due to ADR-007 revision"

---

## Signal Format

```markdown
⚡ DOWNSTREAM SIGNAL
   From: AI-DWG
   To: AI-GCE
   Event: steering-files-updated
   Affected files: [api-standards.md, testing-strategy.md]
   Change summary: API versioning strategy changed from URL-based to header-based
   Action required: Re-derive rules for affected files
   Timestamp: 2026-06-12T14:30:00Z
   Trigger: ADR-007 revision (API versioning change)
```

**Required fields:**
- `From` / `To` — which packages
- `Event` — what type of change
- `Affected files` — specific files (not "everything")
- `Action required` — what the receiver should do

**Optional but valuable:**
- `Change summary` — human-readable description
- `Timestamp` — when the change occurred
- `Trigger` — what upstream event caused this signal

---

## Signal Types

| Event Type | Meaning | Expected Receiver Action |
|-----------|---------|-------------------------|
| `steering-files-updated` | One or more steering files changed | Re-derive rules/hooks for affected files |
| `steering-files-added` | New steering file created | Derive new rules for the new file |
| `steering-files-removed` | A steering file was deleted | Flag rules derived from it for removal |
| `architecture-revised` | AP artifact updated | Reconcile workspace (AI-DWG Mode 2) |
| `container-added` | New container in architecture | Add module structure, steering, folder |
| `container-removed` | Container eliminated | Flag related steering/rules for removal |
| `extension-activated` | New ADLC extension opted in | Run Mode 4 (Extension Enrichment) |
| `extension-deactivated` | Extension removed | Remove extension-specific steering/rules |

---

## Signal Flow Through the Chain

A single architecture change can cascade:

```
ADR-007 revised (AI-ADLC)
    │
    ├── Signal to AI-DWG: "architecture-revised, affected: API_Architecture.md"
    │       │
    │       ├── AI-DWG reconciles: updates api-standards.md steering
    │       │
    │       └── Signal to AI-GCE: "steering-files-updated, affected: api-standards.md"
    │               │
    │               └── AI-GCE re-derives: updates API-* rules + hooks
    │
    └── Signal to AI-TGE: "architecture-revised, affected: API_Architecture.md"
            │
            └── AI-TGE updates test register: new/modified test requirements for API
```

Each link in the cascade is independent — AI-GCE doesn't need to know about the ADR revision, only that `api-standards.md` changed.

---

## Implementation Rules

1. **Signals are explicit, not implicit** — the upstream package PRODUCES the signal as part of its reconciliation step. It's not "detected" by polling.

2. **Signal specifies affected files, not "everything"** — enables surgical re-derivation. "All steering changed" is only used for full re-generation.

3. **Receiver decides whether to act** — the signal is information; the downstream package evaluates whether re-derivation is needed. A trivial comment change in steering may not warrant re-derivation.

4. **Signals are logged** — compliance log records the signal for audit trail. "Why was ARCH-03 re-derived?" → "Because steering changed at 14:30, signal logged."

5. **Signals don't cascade automatically** — each package decides whether to signal ITS downstream. AI-DWG → AI-GCE is one signal. AI-GCE doesn't auto-signal further (it's the end of the chain for enforcement).

6. **No signal = no re-derivation** — downstream packages don't poll for changes. If upstream forgets to signal, downstream stays stale until the next audit catches the drift.

---

## When to Apply This Pattern

Apply when:
- [ ] Package B reads from Package A's output
- [ ] Package A's output can change AFTER initial generation
- [ ] Staleness in Package B has real consequences (stale governance, stale tests)
- [ ] Surgical updates are preferable to full rebuilds

Don't apply when:
- The handoff is one-time (AI-PILC → AI-POLC: PIP doesn't change after handoff)
- Downstream doesn't cache/derive from upstream (no staleness risk)
- Full rebuild is trivial (cost of re-derivation ≈ cost of targeted update)

---

## Related Documents

| Document | Location |
|----------|----------|
| How GCE Rederivation Works | `knowledge_docs/HOW_GCE_REDERIVATION_WORKS.md` |
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |
| How to Handle Architecture Changes Mid-Project | `knowledge_docs/HOW_TO_HANDLE_ARCHITECTURE_CHANGES_MID_PROJECT.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
