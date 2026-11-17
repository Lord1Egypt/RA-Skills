# Reference Map: Marker Files & Detection

**Purpose:** Complete lookup table of all marker files in the AI-* Family — what each marker is, which package produces it, which successor detects it, and the detection fallback strategy.

---

## All Marker Files

| # | Package Output | Marker File | Type | Detected By |
|---|---------------|-------------|------|-------------|
| 1 | AI-ILC | `ilc-state.md` | State file (lifecycle) | AI-PILC |
| 2 | AI-PILC | `pilc-state.md` | State file (lifecycle) | AI-ADLC, AI-POLC, AI-UXD, AI-PPM |
| 3 | AI-ADLC | `adlc-state.md` | State file (lifecycle) | AI-DWG, AI-TGE |
| 4 | AI-POLC | `polc-state.md` | State file (lifecycle) | AI-DWG |
| 5 | AI-UXD | `uxd-state.md` | State file (lifecycle) | AI-DWG, AI-POLC |
| 6 | AI-DWG | `.kiro/steering/workspace-rules.md` | Generated file (not state) | AI-GCE, AI-TGE |
| 7 | AI-GCE | `.kiro/hooks/` folder (≥1 `.json` file) | Folder presence | (end of chain — no successor) |
| 8 | AI-TGE | `tge-state.md` | State file (hybrid) | (companion — no successor) |
| 9 | Shared spine | `management_framework/MANAGEMENT_FRAMEWORK.md` | Governance doc | Any package checking for existing governance |

---

## Detection Strategy (Universal)

Every successor uses this three-step fallback:

```
STEP 1: User provides path explicitly
        → Scan that path for the marker
        → Found? USE IT. Not found? → Step 3

STEP 2: Scan common locations automatically
        → ./
        → ./output/
        → ./docs/
        → ./{predecessor-name}/
        → ./{predecessor-name}-output/
        → ../
        → Found? USE IT. Not found? → Step 3

STEP 3: Ask the user
        → "Where is the {package} output located?"
        → User provides path → scan for marker
```

---

## Marker File Contents (What Successors Read)

### Lifecycle State Files (`*-state.md`)

| Field | Read By Successor? | Purpose |
|-------|:------------------:|---------|
| Project ID | ✅ | Correlation key for traceability |
| Status | ✅ | Confirms predecessor completed (`Complete`) |
| Workflow Depth | ✅ | Inherit depth level |
| Output Structure | ✅ | Know file naming pattern (numbered/flat) |
| Current Stage | ⚠️ (if not Complete) | Warns successor: "predecessor is partial" |
| Enabled Extensions | ✅ (AI-ADLC only) | Triggers extension-aware generation |
| Source Type | ⚠️ | Informs quality expectations of the input |

### Generator Markers (`.kiro/steering/workspace-rules.md`)

| What's Checked | Purpose |
|---------------|---------|
| File exists | Workspace has been generated |
| Content readable | Workspace is valid (not corrupted) |
| Provenance front-matter | Confirms AI-DWG generated it (vs. manual) |

### Folder Markers (`.kiro/hooks/`)

| What's Checked | Purpose |
|---------------|---------|
| Folder exists | Governance has been installed |
| ≥1 `.json` file inside | At least one hook is active |

---

## Marker File Rules (Non-Negotiable)

| Rule | Rationale |
|------|-----------|
| Marker filenames are EXACT (never rename) | Renaming breaks detection for all successors |
| Markers live at output ROOT (not in subfolders) | Detection scans root first for efficiency |
| Markers are always UTF-8 markdown (state files) or standard folder (DWG/GCE) | Parsing consistency |
| Markers are committed to version control | Available to any team member on any machine |
| Missing marker = standalone mode (graceful, not error) | Absence triggers fallback, not failure |

---

## Multi-Input Detection (AI-DWG Special Case)

AI-DWG detects THREE predecessors:

| Input | Marker | Required? | If Not Found |
|-------|--------|:---------:|-------------|
| AP (AI-ADLC) | `adlc-state.md` | ✅ Required | Cannot proceed — asks for architecture |
| PBP (AI-POLC) | `polc-state.md` | ⚪ Optional | Proceeds without backlog enrichment |
| UXP (AI-UXD) | `uxd-state.md` | ⚪ Optional | Proceeds without UX enrichment |

Detection order: AP first (required), then scan for PBP and UXP (additive enrichment).

---

## Cross-Repo Detection

| Location | Supported? | Mechanism |
|----------|:----------:|-----------|
| Same workspace, standard layout | ✅ | Automatic scan of `projects/*/` |
| Same workspace, legacy flat layout | ✅ | Brownfield fallback scan |
| Different repository (cloned locally) | ⚠️ Brownfield | Legacy scan covers sibling/parent paths |
| Remote (not locally accessible) | ❌ | Must be cloned/mounted locally |

---

## Format Tolerance (Finding Guaranteed Files)

Once the marker is found, successor scans for guaranteed output files using patterns (not exact paths):

| File Pattern | Matches |
|-------------|---------|
| `*Architecture_Vision*` | `01_Architecture_Vision.md`, `architecture-vision.md`, `Vision.md` |
| `*Risk_Register*` | `05_Risk_Register.md`, `risk-register.md`, `Risk_Register.md` |
| `*Project_Charter*` | `11_Project_Charter.md`, `charter.md`, `Project_Charter.md` |

**Principle:** Users choose internal sub-structure (numbered vs. phase-folder) at setup. Successors find files by content-pattern, not exact name — this tolerates the sub-structure choice without requiring path authority.

---

## Related Documents

| Document | Location |
|----------|----------|
| Pattern: Marker File Detection | `knowledge_docs/PATTERN_MARKER_FILE_DETECTION.md` |
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |
| How State Files Work | `knowledge_docs/HOW_STATE_FILES_WORK.md` |
| Anatomy of a State File | `knowledge_docs/ANATOMY_OF_A_STATE_FILE.md` |
| What If Chain Handoff Fails | `knowledge_docs/WHAT_IF_CHAIN_HANDOFF_FAILS.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
