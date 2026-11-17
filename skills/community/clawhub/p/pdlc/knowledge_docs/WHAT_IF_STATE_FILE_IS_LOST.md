# What If the State File Is Lost?

**Scenario:** Your session crashed, the state file (`pilc-state.md`, `adlc-state.md`, etc.) was accidentally deleted, corrupted, or you can't find it. You have output artifacts but no state to resume from.

---

## Symptoms

- AI says "No existing workflow state found — starting fresh"
- You know you completed stages but the AI doesn't recognize prior work
- State file is empty, garbled, or missing entirely
- Successor package can't detect your output (marker file gone)

---

## Impact Assessment

| Severity | What's Lost | What's NOT Lost |
|----------|------------|-----------------|
| **State file deleted** | Resume position, depth config, decision log | All produced artifacts (requirements, architecture, etc.) |
| **State file corrupted** | Same as deleted — AI can't parse it | All produced artifacts |
| **State file out of date** | Accurate current position | Nothing — just position is stale |

**Key insight:** The state file is metadata ABOUT your output — not the output itself. Your artifacts (PIP, AP, DW) are safe even if the state file is gone.

---

## Recovery Options

### Option A: Reconstruct from Artifacts (Recommended)

1. **Inventory what exists** — list all output files in your folder
2. **Determine completed stages** — match files to stage outputs:
   - Requirements Analysis exists → Stage 3 complete
   - Feasibility Study exists → Stage 4 complete
   - Charter exists → Stage 12 complete
3. **Create a new state file** manually with the correct position:

```markdown
# {Package} State

## Project Identity
- Project ID: {from your charter or first artifact}
- Project Name: {from your artifacts}

## Progress
- Current Phase: {infer from last artifact}
- Current Stage: {N+1 (next incomplete stage)}
- Completed Stages: {list stages whose artifacts exist}

## Configuration
- Workflow Depth: {Standard — or check artifact detail level}
- Output Structure: {numbered/flat — match existing files}
- Status: In Progress
```

4. **Resume** — start a new session, point it at the output folder. The AI will find the reconstructed state and continue.

### Option B: Fresh Start with Context

If reconstruction is too complex:

1. Start the workflow fresh (new session)
2. When asked for input, **point to your existing artifacts**
3. The AI reads them as input and catches up quickly
4. A new state file is created reflecting the fresh start

**Trade-off:** You lose decision timestamps and the precise sequence record, but the CONTENT is preserved.

### Option C: Resume from Last Known Stage

If you remember where you were:

1. Create a minimal state file with just the position:
```markdown
# {Package} State
- Current Stage: {where you left off}
- Status: In Progress
```
2. Start a session — the AI will accept the position and continue
3. It may re-ask a few questions from the current stage (normal)

---

## Prevention

| Measure | How |
|---------|-----|
| Git-track state files | They're small text — include in version control |
| Don't `.gitignore` state files | They're NOT secrets or build artifacts |
| Regular commits during long workflows | Commit after each gate approval |
| Cloud-sync workspace | State files sync with workspace backup |

---

## Successor Package Impact

If your state file is gone and a SUCCESSOR package tries to detect your output:

| Successor | Behavior Without Marker |
|-----------|------------------------|
| AI-ADLC looking for `pilc-state.md` | Falls back to standalone mode — asks for requirements directly |
| AI-DWG looking for `adlc-state.md` | Falls back to standalone mode — asks for architecture docs |
| AI-GCE looking for workspace marker | Scans for `.kiro/steering/` directly (alternative detection) |

**Recovery:** Recreate the state file (even minimal) and place it in the output folder. Successor will find it on next scan.

---

## Related Documents

| Document | Location |
|----------|----------|
| How State Files Work | `knowledge_docs/HOW_STATE_FILES_WORK.md` |
| Pattern: Marker File Detection | `knowledge_docs/PATTERN_MARKER_FILE_DETECTION.md` |
| Pattern: Graceful Standalone | `knowledge_docs/PATTERN_GRACEFUL_STANDALONE.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
