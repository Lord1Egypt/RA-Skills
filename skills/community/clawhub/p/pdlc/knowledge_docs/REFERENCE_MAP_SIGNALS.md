# Reference Map: Downstream Signals

**Purpose:** Complete lookup table of all downstream signals in the AI-* Family chain — who sends, who receives, what event, what's affected, and what action is expected.

---

## All Signals

| # | From | To | Event | Affected Files | Action Required |
|---|------|----|----|--------|------|
| 1 | AI-ADLC | AI-DWG | `architecture-revised` | Changed AP artifact(s) | Reconcile workspace (Mode 2) |
| 2 | AI-ADLC | AI-DWG | `container-added` | New container in AP | Add module structure + steering |
| 3 | AI-ADLC | AI-DWG | `container-removed` | Removed container in AP | Flag related steering for removal |
| 4 | AI-ADLC | AI-DWG | `extension-activated` | `adlc-state.md` (extensions list) | Run Mode 4 (Extension Enrichment) |
| 5 | AI-ADLC | AI-DWG | `extension-deactivated` | `adlc-state.md` (extensions list) | Flag extension steering for removal |
| 6 | AI-ADLC | AI-TGE | `architecture-revised` | Changed AP artifact(s) | Update test register (Stage 10) |
| 7 | AI-DWG | AI-GCE | `steering-files-updated` | List of changed `.kiro/steering/` files | Re-derive rules for affected files |
| 8 | AI-DWG | AI-GCE | `steering-files-added` | New `.kiro/steering/` file(s) | Derive rules for new file(s) |
| 9 | AI-DWG | AI-GCE | `steering-files-removed` | Deleted `.kiro/steering/` file(s) | Flag derived rules as orphaned |
| 10 | AI-DWG | AI-TGE | `steering-files-updated` | Changed steering files | Refresh test strategy alignment |
| 11 | AI-POLC | AI-DWG | `backlog-updated` | Changed PBP artifacts | Refresh workspace enrichment (DoR/DoD) |
| 12 | AI-UXD | AI-POLC | `personas-updated` | Changed UXP personas/journeys | Refresh backlog prioritization context |
| 13 | AI-DLC v1 | AI-UXD | `feedback-received` | Runtime usability feedback | Feed into next UX iteration |
| 14 | AI-DLC v1 | AI-POLC | `story-feedback` | Implementation complexity discovery | Feed into backlog refinement |

---

## Signal Format (Standard)

```markdown
⚡ DOWNSTREAM SIGNAL
   From: {source package}
   To: {target package}
   Event: {event-type}
   Affected files: [{file1}, {file2}]
   Change summary: {human-readable description}
   Action required: {what receiver should do}
   Timestamp: {ISO-8601}
   Trigger: {what upstream event caused this signal}
```

---

## Signal Chains (Cascading)

| Trigger | Chain |
|---------|-------|
| ADR revised in AI-ADLC | ADLC → DWG (`architecture-revised`) → GCE (`steering-files-updated`) |
| Extension activated | ADLC → DWG (`extension-activated`) → GCE (`steering-files-added`) |
| Extension deactivated | ADLC → DWG (`extension-deactivated`) → GCE (`steering-files-removed`) |
| Personas updated | UXD → POLC (`personas-updated`) → DWG (`backlog-updated`) |
| Container added | ADLC → DWG (`container-added`) → GCE (`steering-files-updated`) → TGE (test register update) |

---

## One-Time Handoffs (Not Signals)

These are NOT signals — they're one-time data flows that don't repeat:

| From | To | What's Passed | Why Not a Signal |
|------|----|--------------|------------------|
| AI-ILC | AI-PILC | Idea Brief | One-time handoff; ILC doesn't update after routing |
| AI-PILC | AI-POLC | PIP | One-time handoff; PIP doesn't change after completion |
| AI-ADLC (initial) | AI-DWG (initial) | Full AP | First generation, not a delta signal |

**Signals exist only where UPDATES flow** — where the source might change AFTER the initial handoff.

---

## Related Documents

| Document | Location |
|----------|----------|
| Pattern: Downstream Signaling | `knowledge_docs/PATTERN_DOWNSTREAM_SIGNALING.md` |
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |
| How GCE Rederivation Works | `knowledge_docs/HOW_GCE_REDERIVATION_WORKS.md` |
| When to Trigger Re-Derivation | `knowledge_docs/WHEN_TO_TRIGGER_REDERIVATION.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
