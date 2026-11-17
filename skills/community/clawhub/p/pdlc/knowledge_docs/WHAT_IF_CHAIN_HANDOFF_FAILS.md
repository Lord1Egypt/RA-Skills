# What If Chain Handoff Fails?

**Scenario:** A successor package can't find or read its predecessor's output — detection fails, marker file is missing, or the predecessor's output format is unexpected.

---

## Symptoms

- Successor package says "No predecessor output detected" when you know it exists
- Successor scans common locations and finds nothing
- Successor finds the marker but can't parse it (format error)
- Successor reads the marker but reports "incomplete predecessor output"

---

## Diagnosis: Why Is Handoff Failing?

| Cause | Detection | Fix |
|-------|-----------|-----|
| **Marker file missing** | Predecessor output folder has no state file | Reconstruct marker (see WHAT_IF_STATE_FILE_IS_LOST) |
| **Wrong location** | Predecessor output is in unexpected folder | Provide explicit path when starting successor |
| **Marker file renamed** | File exists but with different name | Rename back to canonical name (e.g., `pilc-state.md`) |
| **Incomplete predecessor** | Predecessor didn't finish (partial output) | Complete predecessor first, or use standalone mode |
| **Cross-repo with no path** | Predecessor output is in different repository | Provide full path to predecessor output folder |
| **Permissions** | File exists but successor can't read it | Fix file/folder permissions |
| **Encoding** | State file has encoding the parser can't read | Re-save as UTF-8 |

---

## Recovery Options

### Option A: Provide Explicit Path (Fastest)

When the successor asks "Where is predecessor output?":
1. Navigate to where your predecessor output actually lives
2. Confirm the marker file exists there (e.g., `pilc-state.md`)
3. Provide the full path to the successor

```
User: "The PIP output is in C:\Projects\MyProject\docs\initiation\"
AI-ADLC: Scanning C:\Projects\MyProject\docs\initiation\ for pilc-state.md... FOUND.
```

### Option B: Fix the Marker File

If the marker was renamed or is in a subfolder:

1. Find your state file (search for `*-state.md` in your output folder)
2. Ensure it's named correctly:
   - AI-ILC output → `ilc-state.md`
   - AI-PILC output → `pilc-state.md`
   - AI-ADLC output → `adlc-state.md`
   - AI-POLC output → `polc-state.md`
   - AI-UXD output → `uxd-state.md`
3. Ensure it's in the ROOT of the output folder (not a subfolder)
4. Retry the successor — it should detect the marker now

### Option C: Use Standalone Mode (Skip Handoff)

If fixing the handoff is too complex:

1. Start the successor in standalone mode (it will ask for input directly)
2. Point it at your predecessor's output files as raw input
3. The successor reads them as documents (not as chain output) and proceeds
4. You lose: depth inheritance, state continuity metadata, chain traceability
5. You keep: all the content from the predecessor's artifacts

### Option D: Reconstruct Minimal Marker

If the predecessor output exists but the state file is gone:

```markdown
# PILC State (Reconstructed)

## Project Identity
- Project ID: PRJ-{your-project}-{year}-001
- Project Name: {your project name}

## Progress
- Status: Complete
- Workflow Depth: Standard
- Output Structure: numbered

## Completed Stages
- All stages complete (artifacts present)
```

Place this in the predecessor output folder. Successor will detect it.

---

## Prevention

| Measure | How |
|---------|-----|
| Never rename marker files | `pilc-state.md` is sacred — renaming breaks detection |
| Keep marker in output root | Not in a subfolder — detection scans the root first |
| Git-track output including state files | Ensures marker is always available |
| Document output location for the team | "Our PIP is in `/docs/initiation/`" in team docs |
| Test handoff immediately after predecessor completes | Don't wait weeks — verify the chain works while context is fresh |

---

## Partial Handoff (Incomplete Predecessor)

If the predecessor ran partially (some stages, not all):

| Successor Behavior | What Happens |
|-------------------|--------------|
| State file says "In Progress" | Successor warns: "Predecessor is incomplete" |
| Key artifacts missing | Successor identifies gaps, asks for the missing information |
| State says "Complete" but files are missing | Successor proceeds with what exists, asks gap-filling questions |

**Key principle:** Successors degrade gracefully — they use what's available and supplement with questions. A partial predecessor is better than no predecessor.

---

## AI-DWG Special Case (Three Inputs)

AI-DWG reads from three predecessors (AP required, PBP and UXP optional):

| Input | Marker | If Not Found |
|-------|--------|-------------|
| AP (AI-ADLC) | `adlc-state.md` | **Required** — DWG cannot proceed without architecture |
| PBP (AI-POLC) | `polc-state.md` | Optional — DWG proceeds without backlog enrichment |
| UXP (AI-UXD) | `uxd-state.md` | Optional — DWG proceeds without UX enrichment |

If AP detection fails, the fixes above apply. If PBP/UXP detection fails, DWG simply proceeds without that enrichment — no error.

---

## Related Documents

| Document | Location |
|----------|----------|
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |
| Pattern: Marker File Detection | `knowledge_docs/PATTERN_MARKER_FILE_DETECTION.md` |
| Pattern: Graceful Standalone | `knowledge_docs/PATTERN_GRACEFUL_STANDALONE.md` |
| What If State File Is Lost | `knowledge_docs/WHAT_IF_STATE_FILE_IS_LOST.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
