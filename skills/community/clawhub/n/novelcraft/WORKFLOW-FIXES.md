# NovelCraft Workflow Analysis & Fixes

## Identified Problems

### Problem 1: Multiple Subagents for Same Chapter
**Symptom:** Bei Kapitel 5 wurden 3 Subagenten gleichzeitig gestartet:
- `NovelCraft-Chapter-05` (timeout)
- `NovelCraft-Chapter-05-Retry` (running)
- `NovelCraft-Chapter-05-Final` (running)

**Ursache:** Keine eindeutige Session-Tracking zwischen Subagent-Spawns. Der Hauptagent hat nicht gewartet/kontrolliert ob ein Subagent bereits läuft.

**Impact:** Ressourcenverschwendung, konkurrierende Writes auf dieselbe Datei.

---

### Problem 2: Timeout-Handling
**Symptom:** Subagenten timed out nach 3-6 Minuten, aber die Task war nicht wirklich fertig.

**Ursache:** 
- `runTimeoutSeconds` zu kurz für Kapitelschreiben (180s = 3min)
- Kein Checkpointing bei langen Tasks
- Subagent konnte SKILL.md nicht lesen (ENOENT error)

**Impact:** Kapitel wurde nicht fertig geschrieben, Status unklar.

---

### Problem 3: Keine Status-Verfolgung
**Symptom:** Unklar welches Kapitel wo ist (draft vs. approved).

**Ursache:**
- `project-manifest.md` wurde nicht konsistent aktualisiert
- Keine "in-progress" Markierung für laufende Subagenten
- Keine Verbindung zwischen Subagent-ID und Kapitel-Nummer

**Impact:** Verwirrung, doppelte Arbeit, verlorene Kapitel.

---

### Problem 4: Subagent → Main Session Kommunikation
**Symptom:** Subagent-Resultat enthielt falschen Inhalt (Kapitel 4 statt 5).

**Ursache:** 
- Subagent hatte keine klare Task-Definition
- Keine Validierung des Outputs
- Keine Datei-Locking Mechanism

**Impact:** Dateninkonsistenz, verlorene Arbeit.

---

## Proposed Fixes

### Fix 1: Subagent Session Tracking

**Before spawning:**
```javascript
// Check if subagent already running for this chapter
const activeSubagents = await subagents({ action: "list" });
const existing = activeSubagents.find(s => 
  s.label.includes(`Chapter-${chapterNum}`)
);

if (existing) {
  // Wait for existing OR kill and restart
  await subagents({ 
    action: "kill", 
    target: existing.sessionKey 
  });
}

// Now spawn new
await sessions_spawn({
  label: `NovelCraft-Chapter-${chapterNum}`,
  mode: "run",
  runtime: "subagent",
  task: "...",
  runTimeoutSeconds: 3600 // 1 hour for chapter writing
});
```

---

### Fix 2: Project Manifest mit Subagent-Tracking

**Erweiterte project-manifest.md:**
```yaml
chapters:
  '05':
    status: 'writing'  # pending | writing | reviewing | approved
    subagent:
      session_key: 'agent:opencode:subagent:...'
      run_id: '...'
      started_at: '2026-04-06T19:14:00Z'
      expected_duration: '1800s'  # 30 min
    draft_file: '01-drafts/chapter_05_draft.md'
    review_file: null
    approved_file: null
    word_count: null
    score: null
```

---

### Fix 3: Checkpoint-System für lange Tasks

**Subagent schreibt regelmäßig Fortschritt:**
```markdown
<!-- chapter_05_draft.md -->
# Kapitel 5: Ein Plan wird gemacht

**Status:** In Progress
**Words written:** 650 / 1000
**Last update:** 2026-04-06T19:20:00Z
**ETA:** 10 minutes

---

[Content so far...]
```

**Main Session checkt:**
```javascript
// Every 2 minutes, check progress
const draft = await read({ 
  file: 'chapter_05_draft.md' 
});
const progress = parseProgress(draft);
if (progress.words_written > 0) {
  console.log(`Progress: ${progress.words_written} words`);
}
```

---

### Fix 4: Atomic File Operations

**Locking vor dem Schreiben:**
```bash
# Create lock file
mkdir -p 01-drafts/.locks
lock_file="01-drafts/.locks/chapter_05.lock"

# Try to acquire lock
if mkdir "$lock_file" 2>/dev/null; then
  # Got lock, safe to write
  echo "..." > chapter_05_draft.md
  rm -rf "$lock_file"
else
  # Lock exists, another process writing
  echo "Chapter 5 being written by another process"
  exit 1
fi
```

---

### Fix 5: Verbesserter Workflow in SKILL.md

**Aktuell (Problem):**
```
Phase 4: Chapters (4-8h)
"Strictly sequential, one chapter at a time"
→ Aber: Keine Details WIE!
```

**Neu (Fix):**
```
Phase 4: Chapters (4-8h)

For each chapter:
  1. Check project-manifest for chapter status
  2. IF status == 'pending':
       a. Mark status = 'writing' in manifest
       b. Spawn subagent with clear task:
          - Input: Previous chapter (if any)
          - Output: chapter_XX_draft.md
          - Timeout: 1 hour
       c. Wait for completion event (push-based)
       d. On completion:
          - Validate output exists
          - Run review scoring
          - IF approved: copy to 02-chapters/
          - Update manifest: status = 'approved'
          - Proceed to next chapter
       e. On timeout/error:
          - Check partial draft (checkpoint)
          - IF >50% complete: resume subagent
          - ELSE: restart subagent (max 3 retries)
          - Update manifest with retry count
  3. IF status == 'writing':
       - Check if subagent still running
       - IF running: wait
       - IF not: check for partial draft, decide resume/restart
  4. IF status == 'approved':
       - Skip to next chapter
```

---

## Implementation Tasks

### Task 1: Update SKILL.md Workflow Section
**File:** `~/.openclaw/skills/novelcraft/SKILL.md`
**Section:** "Workflow (Autonomous)" + new "Detailed Chapter Workflow"

### Task 2: Create Workflow Helper Functions
**File:** `~/.openclaw/skills/novelcraft/workflow-helpers.md`
**Content:**
- `checkSubagentStatus(chapterNum)`
- `acquireChapterLock(chapterNum)`
- `updateManifest(chapterNum, status, metadata)`
- `parseChapterProgress(draftFile)`

### Task 3: Update Subagent Spawn Logic
**In:** Main NovelCraft execution
**Changes:**
- Pre-check for existing subagents
- Extended timeout (1 hour)
- Clear task specification
- Progress checkpoint expectation

### Task 4: Add Error Recovery
**New section in SKILL.md:**
- "Error Handling & Recovery"
- "Timeout Scenarios"
- "Retry Strategies"

---

## Testplan

### Test 1: Single Chapter Flow
```
1. Start NovelCraft for 1 chapter
2. Verify subagent spawns correctly
3. Verify manifest updates to 'writing'
4. Wait for completion
5. Verify draft exists
6. Verify review runs
7. Verify approval copies file
8. Verify manifest updates to 'approved'
```

### Test 2: Timeout Recovery
```
1. Start chapter with artificially low timeout
2. Wait for timeout
3. Verify recovery logic detects partial draft
4. Verify retry with extended timeout
5. Verify completion
```

### Test 3: Duplicate Prevention
```
1. Start chapter
2. Try to start same chapter again
3. Verify second spawn is blocked/rejected
4. Verify only one subagent running
```

### Test 4: Sequential Enforcement
```
1. Configure 3 chapters
2. Start NovelCraft
3. Verify only chapter 1 subagent spawns
4. Wait for chapter 1 approval
5. Verify chapter 2 subagent spawns
6. Repeat
```

---

## Success Criteria

- [ ] No duplicate subagents for same chapter
- [ ] Clear status tracking in manifest
- [ ] Automatic retry on timeout (max 3)
- [ ] Progress visible during long writes
- [ ] Sequential chapter execution enforced
- [ ] Recovery from interrupted writes

---

**Document:** WORKFLOW-FIXES.md
**Version:** 1.0
**Created:** 2026-04-06
**For:** NovelCraft v3.2.x
