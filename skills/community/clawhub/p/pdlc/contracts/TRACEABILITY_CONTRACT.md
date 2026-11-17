# AI-* Family — Traceability & Provenance Contract

**Version:** 1.0.0
**Date:** 2026-06-13
**Author:** Maheri
**Authored under:** `#persona-process-designer` (lead) + `#persona-compliance-governance` (support)
**Open Item:** OI-030
**Status:** ADOPTED

---

## 1. Purpose

Define **one** rule, across the whole AI-* family, that ensures **identity survives transformation** — not just handoff.

An Idea is polymorphic. At the AI-ILC gate it can become a project, a backlog item, a Change Request, or a merged idea. Each fork is an identity event. This contract ensures that every such event carries a **provenance stamp** — a durable lineage edge that makes the upstream origin discoverable from any downstream object.

This contract also closes the `Project ID` propagation gap: the correlation key, once minted, must survive every chain hop (already implemented via  work; this contract formalizes the rule).

> **This is a shared CONTRACT, not a new package** — same stance as `MANAGEMENT_FRAMEWORK_CONTRACT.md` and `DASHBOARD_FRAMEWORK_CONTRACT.md`. Traceability is a cross-cutting discipline every package honors; no package "owns" another's lineage.

---

## 2. Governing Principle

> **Traceability is a property of identity transformations, not just handoffs.**
>
> Whenever an object changes form (idea→project, idea→backlog item, idea→CR, idea+idea→merged idea), the new object MUST carry a provenance edge back to its origin. A correlation key declared by the producer is fiction until the consumer reads and persists it.

(Source:)

---

## 3. The Provenance Stamp

Every object minted or merged from an upstream source carries the following front-matter keys:

```yaml
---
id: {object's own ID}
originType: idea | project | feature | cr | backlog-item
derivedFrom: {upstream ID that this object was minted from}
mergedFrom: [{id}, {id}]        # for merges only — the absorbed objects' IDs
projectId: {Project ID}         # the immutable family-wide correlation key, once one exists
provenanceVersion: 1.0.0
---
```

### 3.1 Key Definitions

| Key | Type | Required | Description |
|-----|------|:--------:|-------------|
| `id` | string | ✅ | This object's own unique identifier (e.g. `PRJ-CRM-2026-001`, `IDEA-014`, `CR-CRM-2026-003`) |
| `originType` | enum | ✅ | What kind of object this is: `idea`, `project`, `feature`, `cr`, `backlog-item` |
| `derivedFrom` | string | ✅ when transformation occurred | The upstream ID this object was minted from |
| `mergedFrom` | array | Only on merges | IDs of all absorbed objects (preserves their lineage as aliases) |
| `projectId` | string | ✅ when one exists | The immutable family-wide correlation key (`PRJ-{ABBREV}-{YYYY}-{NNN}`) — threaded from minting through every downstream hop |
| `provenanceVersion` | string | ✅ | Contract version governing this stamp (currently `1.0.0`) |

### 3.2 Complementary Key: `aliasOf`

When an object is **absorbed** by a merge, the absorbed file is NOT deleted. It is marked:

```yaml
---
aliasOf: {survivor-ID}
---
```

This preserves the audit trail — any reference to the absorbed ID can be resolved to the survivor.

### 3.3 Naming Convention Alignment

These keys follow the same conventions as `NAMING_AND_OWNERSHIP.md`:
- **camelCase** (consistent with `generatedBy`, `generatedVersion`, `ownership`, etc.)
- **Carried in YAML front-matter** for `.md` files (Approach A metadata)
- **Key names LOCKED** (2026-06-13): `id`, `originType`, `derivedFrom`, `mergedFrom`, `projectId`, `provenanceVersion`, `aliasOf`

---

## 4. Per-Transformation Application

| # | Transformation | Identity Event | Stamp Applied |
|---|----------------|----------------|---------------|
| A | **Idea → Project** | Idea approved at AI-ILC gate → new project at AI-PILC | PILC state records `derivedFrom: <idea-ID>`, `originType: project`, mints `projectId` |
| B | **Idea → Backlog Item** | Feature routed directly to backlog (PILC skipped) | Feature Brief carries `derivedFrom: <idea-ID>`, `originType: feature`; AI-POLC stamps each epic/story with `derivedFrom` + value tag |
| C | **Idea → Architecture** | Feature routed to AI-ADLC (brownfield) | ADLC reads Feature Brief's `derivedFrom` and persists into `adlc-state.md` |
| D | **Idea → Change Request** | Change detected → 005/004/003 stack | CR minted with `derivedFrom: <idea-ID or requirement-ID>`, `originType: cr`, plus blast-radius edges |
| E | **Ideas Merge** | 2+ ideas de-duped into one survivor | Survivor records `mergedFrom: [absorbed-IDs]`; absorbed files marked `aliasOf: <survivor-ID>` |
| F | **Parked / Rejected** | Idea stays in register | No transformation — already traceable (ID never crosses a boundary) |

---

## 5. The `Project ID` Propagation Rule

The correlation key (`PRJ-{ABBREV}-{YYYY}-{NNN}`) is minted once and MUST survive every chain hop. This rule is already implemented (Lessons 39/43); this section formalizes it as contract.

| Hop | How `Project ID` Travels | Status |
|-----|--------------------------|--------|
| **PILC → POLC** | POLC reads `Project ID` from `pilc-state.md`; persists in `polc-state.md` (or self-mints in standalone) | ✅ Implemented |
| **POLC → UXD** | UXD reads `Project ID` from `polc-state.md`; persists in `uxd-state.md` | ✅ Implemented |
| **UXD → ADLC** | ADLC reads `Project ID` from predecessor state files; persists in `adlc-state.md` (or self-mints in standalone) | ✅ Implemented |
| **ADLC → DWG** | DWG reads from `adlc-state.md`; embeds in generated `workspace-rules.md` `## Project Identity` section | ✅ Implemented |
| **DWG → GCE** | GCE reads from `workspace-rules.md`; includes `projectId` in every compliance log JSONL event | ✅ Implemented |
| **DWG → TGE** | TGE reads from `workspace-rules.md`; uses for audit trail correlation + quality dashboard | ✅ Implemented |
| **PILC → POLC** | POLC reads `projectId` from `pilc-state.md` (field in `polc-state.md`: `projectId`) | ✅ Implemented |
| **FLO/PPM** | Carry `Project ID` on every hop/roll-up (when built — ideas 007/008) | 🔵 Planned |

### 5.1 Standalone Minting

When a package runs standalone (no predecessor marker detected), it may **self-mint** a `Project ID` using the same format (`PRJ-{ABBREV}-{YYYY}-{NNN}`), confirmed with the user. This ensures the correlation key exists regardless of entry point (OR-input).

---

## 6. The Merge Identity Rule (Specification)

> **Capability status:** Merge is deferred to AI-ILC v1.1+. This section specifies the identity rule so that when the capability ships, it is born with non-orphaning lineage.

### 6.1 Rule

When two or more ideas are determined to be duplicates or are deliberately combined:

1. **Designate one survivor.** The survivor retains its original `id`.
2. **Record `mergedFrom`.** The survivor's front-matter gains `mergedFrom: [absorbed-ID-1, absorbed-ID-2,...]`.
3. **Mark absorbed files.** Each absorbed idea's file gains `aliasOf: <survivor-ID>` and status `merged`.
4. **Preserve in register.** Absorbed ideas remain in the Idea Register (with status `merged` + pointer to survivor). They are NEVER deleted — this preserves the audit trail and ensures any downstream reference to the absorbed ID can be resolved.

### 6.2 Resolution Rule

Any system encountering a reference to an ID marked `aliasOf` MUST resolve it to the survivor before processing. This is transparent to the user — they may continue using either ID in conversation; the system follows the alias.

---

## 7. Package Obligations

Each package's responsibility under this contract:

| Package | Obligation |
|---------|------------|
| **AI-ILC** | Mint `IDEA-{NNN}` ID on every idea. At routing gate: tag outbound brief with `id` + `originType`. If merge capability ships: apply §6 merge rule. |
| **AI-PILC** | When intake is from AI-ILC (`ilc-state.md` detected): record `derivedFrom: <idea-ID>` in `pilc-state.md` (REQUIRED). Mint and persist `projectId`. |
| **AI-ADLC** | Read `projectId` + `derivedFrom` from `pilc-state.md` (or Feature Brief); persist both in `adlc-state.md`. |
| **AI-UXD** | Read `projectId` + `derivedFrom` from `pilc-state.md` / `adlc-state.md`; persist both in `uxd-state.md` (camelCase, normalized 2026-06-15c). |
| **AI-POLC** | Read `derivedFrom` from upstream (Feature Brief or `pilc-state.md`). Stamp every epic/story with `derivedFrom` linking to the originating idea/feature. Persist `projectId` in `polc-state.md`. |
| **AI-DWG** | Read `projectId` from `adlc-state.md`; embed in generated `workspace-rules.md`. |
| **AI-GCE** | Read `projectId` from `workspace-rules.md`; include in every compliance log event. |
| **AI-TGE** | Read `projectId` from `workspace-rules.md`; anchor audit trail and quality dashboard to it. |
| **AI-FLO** | Carry `projectId` on every routing hop (when built). |
| **AI-PPM** | Key portfolio roll-up by `projectId` (when built). |

---

## 8. Relationship to Other Contracts

| Contract | Relationship |
|----------|-------------|
| `NAMING_AND_OWNERSHIP.md` | This contract's keys (`derivedFrom`, `originType`, etc.) extend the provenance front-matter defined there. Same camelCase convention, same YAML front-matter carrier. |
| `MANAGEMENT_FRAMEWORK_CONTRACT.md` | The governance spine carries phase-prefixed IDs. When an entry originates from an idea transformation, the entry MAY include a `derivedFrom` note in its Context column linking back to the idea. |
| `DASHBOARD_FRAMEWORK_CONTRACT.md` | Dashboards include `projectId` in front-matter (already implemented). No additional traceability obligation. |

---

## 9. Boundaries (What This Contract Does NOT Do)

1. **Not an enforcement engine.** This defines the provenance noun. Enforcement (preventing commits without provenance) is AI-GCE's job.
2. **Does not absorb ideas 003/004/005.** The change stack (detect/route/govern/write) uses this stamp; this contract does not implement the stack.
3. **Does not build AI-POLC/AI-PPM/AI-FLO.** It defines the stamp those packages must carry.
4. **Does not implement idea-merging.** It specifies the merge identity rule (§6) so merging is born traceable.
5. **Does not change artifact locations.** Provenance rides the file (front-matter), consistent with the A-dominant hybrid.

---

## 10. Implementation Status

| Obligation | Status |
|------------|--------|
| `projectId` threading (PILC→POLC→UXD→ADLC→DWG→GCE/TGE) | ✅ Implemented (work) |
| `projectId` in AI-POLC `polc-state.md` | ✅ Implemented (field: `projectId`, normalized 2026-06-15c) |
| `derivedFrom` at AI-PILC (Idea→Project) | ✅ Implemented (2026-06-13, Phase C) |
| `derivedFrom` at AI-POLC (epic/story stamping) | ✅ Implemented (2026-06-13, Phase D) |
| Merge identity rule (§6) | 📐 Specified only — capability deferred to AI-ILC v1.1 |
| CR provenance (ideas 003/004/005) | 🚫 Gated — change stack unbuilt |
| AI-FLO / AI-PPM `projectId` carry | 🔵 Planned — packages unbuilt |

---

## 11. Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-06-13 | Initial contract — provenance stamp, merge identity rule, Project ID propagation formalization, package obligations. Phases A/C/D/F/G of OI-030 executed. |
| 1.0.1 | 2026-06-22 | Verified against the family-workspace prefix change (install-lock design). No edit required — this contract references markers by **filename** (`pilc-state.md`, `adlc-state.md`, `workspace-rules.md`) and IDs (`PRJ-{ABBREV}-{YYYY}-{NNN}`), not folder paths, so the `pdlc-ws/` prefix does not affect it. |

---

*Contract Version: 1.0.0 | Created: 2026-06-13 | Authored under #persona-process-designer + #persona-compliance-governance*
