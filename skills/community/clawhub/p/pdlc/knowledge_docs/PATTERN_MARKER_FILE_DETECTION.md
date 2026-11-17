# Pattern: Marker File Detection

**Purpose:** Documents the reusable design pattern where packages find their predecessor's output by scanning for a non-negotiable filename (marker) rather than hardcoding folder paths — enabling user-chosen output locations while maintaining automatic chain detection.

---

## The Pattern

```
SUCCESSOR PACKAGE starts
        │
        ▼
"Where is my predecessor's output?"
        │
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│  DETECTION STRATEGY (three-step fallback)                            │
│                                                                      │
│  1. User provides path explicitly → USE IT                           │
│  2. Scan common locations for MARKER FILE → FOUND? USE IT            │
│  3. Neither works → ASK USER: "Where is the {pkg} output?"          │
└─────────────────────────────────────────────────────────────────────┘
        │
        ▼
MARKER FOUND → read state, read guaranteed files, proceed
```

**One sentence:** Users choose WHERE output goes; packages define WHAT must exist there — and detection finds it by marker, not by path.

---

## The Marker File Registry

| Package Output | Marker File | Why This File |
|---------------|-------------|--------------|
| AI-ILC | `ilc-state.md` | State file doubles as marker (lifecycle packages) |
| AI-PILC | `pilc-state.md` | State file doubles as marker |
| AI-ADLC | `adlc-state.md` | State file doubles as marker |
| AI-POLC | `polc-state.md` | State file doubles as marker |
| AI-UXD | `uxd-state.md` | State file doubles as marker |
| AI-DWG | `.kiro/steering/workspace-rules.md` | Workspace existence marker (generators don't have state files) |
| AI-GCE | `.kiro/hooks/` folder (with ≥1 `.json` file) | Folder existence = governance installed |
| AI-TGE | `tge-state.md` | Hybrid engine state file |
| Shared governance spine | `management_framework/MANAGEMENT_FRAMEWORK.md` | Spine marker for consolidated governance |

---

## Where It's Used

Every chain handoff in the family uses marker detection:

| From | To | Marker Scanned |
|------|----|---------------|
| AI-ILC | AI-PILC | `ilc-state.md` |
| AI-PILC | AI-POLC | `pilc-state.md` |
| AI-POLC | AI-UXD | `polc-state.md` |
| AI-UXD | AI-ADLC | `uxd-state.md` |
| AI-ADLC | AI-DWG | `adlc-state.md` |
| AI-POLC | AI-DWG | `polc-state.md` |
| AI-UXD | AI-DWG | `uxd-state.md` |
| AI-DWG | AI-GCE | `.kiro/steering/workspace-rules.md` |
| AI-DWG | AI-TGE | `.kiro/steering/workspace-rules.md` |

---

## Why This Pattern Exists

**The problem it solves:** If contracts required exact absolute paths, predecessor output would only work in one folder structure. The marker pattern decouples *detection* (how successors find output) from *layout* (how documents are organized within the fixed output folder).

**What is fixed (non-negotiable):**
- Output folder location — deterministic per `FAMILY_STRUCTURE.md` (e.g. `projects/PRJ-{ABBREV}-{slug}/pip/`)
- Marker filenames — exact names, never renamed (e.g. `pilc-state.md`)

**What the user may choose (internal sub-structure only):**
- Whether deliverables inside the fixed folder use numbered prefixes (`01_*.md`) or phase-subfolder organization
- This choice is stored in the state file's `Output Structure` field so successors can locate files by pattern

**The test:** "Can my package find guaranteed output files regardless of the internal naming scheme the user chose at setup?" If no → format tolerance logic needs improvement.

---

## The Two-Step Detection Strategy

### Step 1: Scan Standard Locations (Primary)

Scan the family's standard layout per `FAMILY_STRUCTURE.md`:
```
Scan order:
  projects/*/pip/             ← AI-PILC (default multi-project)
  projects/*/architecture/    ← AI-ADLC (default multi-project)
  projects/*/ux/              ← AI-UXD (default multi-project)
  projects/*/backlog/         ← AI-POLC (default multi-project)
  ideas/                      ← AI-ILC (default)
```

### Step 2: Scan Legacy Flat Locations (Brownfield Fallback)

If not found in the standard layout, scan legacy/flat locations for brownfield compatibility:
```
Legacy scan:
  ./                          ← workspace root (old single-project)
  ./{predecessor-name}/       ← folder named after package
  ./pilc-output/              ← legacy output folder
  ./docs/                     ← documentation folder
```

> **Note:** the package never asks the user where predecessor output is. It scans deterministically. If a brownfield location is detected, the successor informs the user and operates from the standard layout for its own output.

---

## Format Tolerance

Marker detection supports multiple internal naming structures (the user's sub-structure choice at setup):

| Internal Structure | Works? | How Detected |
|-------------------|:------:|-------------|
| `01_Architecture_Vision.md` (numbered) | ✅ | Pattern matching: `*Architecture_Vision*` |
| `foundation/architecture-vision.md` (phase-folder) | ✅ | Recursive scan within marker folder |
| `pilc-docs/inception/*.md` (flat) | ✅ | Marker file found → scan siblings |

**Key principle:** The marker file anchors detection. Once found, sibling/child files are located by name pattern, not by exact filename. This tolerates the user's internal sub-structure choice (numbered vs. phase-folder) without granting authority over the output folder location itself.

---

## Cross-Repo Support

Predecessor output is expected in the standard `projects/*/` layout within the same workspace. Legacy or cross-repo locations are supported for brownfield only:

| Location | Supported? | How |
|----------|:----------:|-----|
| Same workspace, standard layout | ✅ | Automatic scan of `projects/*/` |
| Same workspace, legacy flat layout | ✅ | Brownfield fallback scan |
| Different repository (checked out locally) | ⚠️ Brownfield | Package scans standard layout; legacy scan covers sibling paths |
| Remote (not local) | ❌ | Must be locally accessible |

---

## Implementation Rules

1. **Marker filenames are non-negotiable** — renaming `pilc-state.md` to `my-project-state.md` breaks detection. This is the ONE constraint on user organization.

2. **Detection is read-only** — scanning never creates, moves, or modifies files.

3. **Failed detection is graceful** — the package works standalone (OR-input pattern) if the predecessor isn't found.

4. **Marker confirmation** — after finding the marker, read it to confirm it's valid (correct package, expected fields present).

5. **Detection result is cached in state** — once found, the path is stored in the successor's state file so future sessions don't re-scan.

---

## When to Apply This Pattern

Apply when:
- [ ] Package B needs to find Package A's output
- [ ] Users should have freedom to organize their files
- [ ] The relationship is optional (standalone mode is valid)
- [ ] A single filename can unambiguously identify the output

Don't apply when:
- The output location is fixed by platform convention (e.g., `.kiro/hooks/` is always there)
- There's no predecessor/successor relationship
- The output is a single file (just ask for the file path directly)

---

## Related Documents

| Document | Location |
|----------|----------|
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |
| How State Files Work | `knowledge_docs/HOW_STATE_FILES_WORK.md` |
| Pattern: Graceful Standalone | `knowledge_docs/PATTERN_GRACEFUL_STANDALONE.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
