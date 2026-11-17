<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Routing Table — AI-FLO

**Generated:** {date}
**Topology:** Mode {1/2/3}
**Projects:** {N}

---

## Canonical Routes (Active)

| # | From | To (Successors) | Type | Condition | Active? |
|---|------|-----------------|------|-----------|:-------:|
| R1 | AI-ILC | AI-PILC / AI-POLC / AI-PPM | Conditional | ILC Route field | ✅ |
| R2 | AI-PILC | AI-POLC | Sequential | PIP complete | ✅ |
| R3 | AI-POLC | AI-UXD | Sequential | PBP complete | ✅ |
| R4 | AI-UXD | AI-ADLC | Sequential | UXP complete | ✅ |
| R5 | AI-ADLC | AI-DWG (fan-in) | Feed | AP complete (PBP + UXP present) | ✅ |
| R6 | AI-DWG | AI-DLC v1 | Sequential | Workspace ready | ✅ |
| R7 | AI-GCE | — (alongside AI-DLC v1) | Companion | Continuous | {✅/❌} |
| R8 | AI-TGE | — (alongside AI-DLC v1) | Companion | Continuous | {✅/❌} |
| R9 | AI-PPM | AI-FLO (dispatch) | Cross-layer | Dispatch authorization | ✅ |

---

## Fan-In Rules

| Target | Required Feeds | Optional Feeds | Minimum Readiness |
|--------|---------------|----------------|-------------------|
| AI-DWG | AP (AI-ADLC) | PBP (AI-POLC), UXP (AI-UXD) | AP must be Complete |

---

## Per-Project Profiles

| Project ID | Name | Scope | Skip | Active Toggles | Routes Active |
|------------|------|-------|------|----------------|:-------------:|
| {PRJ-ID} | {name} | {Full/Design-only/Custom} | {[list] or —} | {[list] or —} | {N}/9 |

---

## Package Availability

| Package | Detected? | Marker Location |
|---------|:---------:|-----------------|
| AI-ILC | {✅/❌} | {path or "not found"} |
| AI-PILC | {✅/❌} | {path} |
| AI-PPM | {✅/❌} | {path} |
| AI-ADLC | {✅/❌} | {path} |
| AI-UXD | {✅/❌} | {path} |
| AI-POLC | {✅/❌} | {path} |
| AI-DWG | {✅/❌} | {path} |
| AI-GCE | {✅/❌} | {path} |
| AI-TGE | {✅/❌} | {path} |
| AI-DFE | {✅/❌} | {path — e.g. `{family}-ws/data/dfe-state.md`} |

> **AI-DFE is a non-routed overlay peer, not a routing target.** It does not appear in the Canonical Routes table — FLO never routes *to* DFE. FLO only detects its presence here so it may optionally signal DFE ("package X completed") to prompt a data refresh; DFE otherwise operates independently on timestamps. FLO routes; DFE fabrics. Neither commands the other (see AI-DFE design §8).

---

## Validation

| Check | Status |
|-------|:------:|
| No orphan routes | {✅/⚠️} |
| No unreachable packages | {✅/⚠️} |
| No circular routes | {✅/⚠️} |
| All fan-in targets have required feed | {✅/⚠️} |

---

*Last validated: {date}*
