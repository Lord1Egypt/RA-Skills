# FAMILY_INTERFACE.md — PDLC

> **What this file is:** The public interface of the AI-* PDLC Family. Neighbors discover this family by finding this file. It declares which packages are seams (Tier 1 — bindable cross-family) and lists all members (Tier 2 — informational only). Gate detail lives in each package's gate contract (pointers below).

---

```yaml
interfaceVersion: 1.0
family: PDLC
familyRepo: AIPDLC
familyName: Product Development Life Cycle
description: "Idea → governed code: the full product development journey from raw idea through architecture, UX, backlog, workspace generation, governance, testing, and portfolio management."
```

---

## Tier 1 — Seam Packages (bindable cross-family)

> Only packages listed here may participate in cross-family communication. Each entry declares its capability types and points to its gate contract. No gate detail here — gate contracts are authoritative.

### Seam-In (what this family can RECEIVE from other families)

| Package | Consumes Types | Gate Contract |
|---------|---------------|---------------|
| **AI-ILC** | `capability-input@^1` | `ai-ilc/ai-ilc-rules/core-workflow.md § Gate Contract` |
| **AI-PILC** | `validated-business-case@^1` | `ai-pilc/ai-pilc-rules/core-workflow.md § Gate Contract` |

### Seam-Out (what this family can SEND to other families)

| Package | Emits Type | Marker | Gate Contract |
|---------|-----------|--------|---------------|
| **AI-DWG** | `development-workspace@1` | `dwg-state.md` | `ai-dwg/ai-dwg-rules/core-workflow.md § Gate Contract` |
| **AI-PPM** | `portfolio-state@1` | `ppm-state.md` | `ai-ppm/ai-ppm-rules/core-workflow.md § Gate Contract` |

---

## Tier 2 — Roster (informational only — NOT bindable across families)

| Package | Tagline | Type | Visibility |
|---------|---------|------|:----------:|
| AI-ILC | Decide it | Interactive workflow (lifecycle) | internal (+ external seam-in) |
| AI-PILC | Initiate it | Interactive workflow (lifecycle) | internal (+ external seam-in) |
| AI-ADLC | Design it | Interactive workflow (lifecycle) | internal |
| AI-UXD | Design UX | Interactive workflow (lifecycle) | internal |
| AI-POLC | Own it | Interactive workflow (lifecycle) | internal |
| AI-DWG | Prepare it | One-time generator | internal (+ external seam-out) |
| AI-GCE | Guard it | Adaptive governance engine | internal |
| AI-TGE | Test it | Test governance engine | internal |
| AI-PPM | Govern it | Adaptive portfolio engine | internal (+ external seam-out) |
| AI-FLO | Route it | Active orchestration engine | internal |

---

## Notes

- A neighbor discovers this family by finding THIS file (it self-declares `family` + root location).
- Binding is by **capability type**, never by family or marker name.
- Gate detail (mandatory/optional/guarantees) lives in each seam package's gate contract (pointers in Tier 1).
- Only Tier 1 packages may be bound to from outside this family.
- Internal-only packages (`visibility: internal`) auto-bind within the family via capability match but are never exposed cross-family.
- This file conforms to `GATE_PROTOCOL.md` `interfaceVersion: 1.0`.

---

*Part of the AIFLC Communication Fabric · Conforms to GATE_PROTOCOL.md protocolVersion 1.2.0*
