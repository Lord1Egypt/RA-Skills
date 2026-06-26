---
name: novelcraft
description: "Fully autonomous book author. Creates complete novels from idea to finished PDF/EPUB. Modular workflow with standardized config schema v3.2: Concept → Optional Prolog → Optional images → Chapters → Optional Epilog → Publication. Configurable autonomy with target audience profiles: early-readers, middle-grade, young-adult, new-adult, adult, senior. Auto-configures chapter length, image settings, wording style, and PDF layout based on selected profile. Image generation is optional with detailed configuration."
---

# NovelCraft

Fully autonomous book authoring — from idea to finished PDF/EPUB.

⚠️ **Security Notice:** Review [SECURITY.md](./SECURITY.md) before running, especially for first-time use. Use `step-by-step` mode initially. Images are disabled by default.

## Workflow (Autonomous)

| Phase | Module | Duration | Description |
|-------|--------|----------|-------------|
| 1 | Concept | 1-2h | Genre, characters, plot, worldbuilding |
| 2 | Writer Extras | 30-60min | Prolog (optional) — before chapters |
| 3 | Images | Start immediately, ~40-55min | **Don't wait**, proceed to phase 4. Categories: cover, characters, settings, chapter images |
| 4 | **Chapters** | 4-8h | **See detailed workflow below** |
| 5 | Writer Extras | 30-60min | Epilog (optional) — after chapters |
| 6 | Publication | 15-30min | First without images, then with images (if ready) |

---

## Detailed Chapter Workflow (v3.2)

**CRITICAL:** Chapters run **strictly sequential** with proper tracking.

### For Each Chapter:

```
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: Check Manifest                                         │
│  Read project-manifest.md → chapter_XX.status                   │
└─────────────────┬───────────────────────────────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
pending      writing       approved
    │             │             │
    │             │             └─→ SKIP to next chapter
    │             │
    │             └─→ Check subagent status
    │                   IF running: wait
    │                   IF not: resume/restart decision
    │
    └─→ STEP 2: Acquire Lock
        │
        ▼
    STEP 3: Spawn Subagent
        │
        ├─ Label: NovelCraft-Chapter-XX
        ├─ Mode: run
        ├─ Timeout: 3600s (1 hour)
        ├─ Pre-check: Kill existing Chapter-XX subagents
        │
        ▼
    STEP 4: Update Manifest
        │
        ├─ status: "writing"
        ├─ subagent.session_key: [key]
        ├─ subagent.run_id: [id]
        ├─ subagent.started_at: [timestamp]
        └─ subagent.expected_duration: "1800s"
        │
        ▼
    STEP 5: Wait (Push-Based)
        │
        ├─ DO NOT poll sessions_list
        ├─ DO NOT use sessions_yield
        ├─ Wait for subagent completion event
        │
        ▼
    STEP 6: Handle Result
        │
        ├─ SUCCESS: Validate output → Go to Review
        ├─ TIMEOUT: Check partial draft → Resume or Retry
        └─ ERROR: Log → Retry (max 3)
```

### Subagent Pre-Check (CRITICAL)

**Before spawning ANY chapter subagent:**

```javascript
// 1. List active subagents
const active = await subagents({ action: "list" });

// 2. Find existing for this chapter
const existing = active.find(s => 
  s.label === `NovelCraft-Chapter-${chapterNum}`
);

// 3. Kill if exists (prevent duplicates)
if (existing) {
  await subagents({ 
    action: "kill", 
    target: existing.sessionKey 
  });
}

// 4. Verify killed
const verify = await subagents({ action: "list" });
const stillExists = verify.find(s => 
  s.label === `NovelCraft-Chapter-${chapterNum}`
);

if (stillExists) {
  throw new Error(`Failed to kill existing Chapter-${chapterNum}`);
}

// 5. NOW spawn new
await sessions_spawn({
  label: `NovelCraft-Chapter-${chapterNum}`,
  mode: "run",
  runtime: "subagent",
  task: "...",
  runTimeoutSeconds: 3600 // 1 hour minimum
});
```

### Checkpoint System (Progress Tracking)

**Subagent MUST write progress header:**

```markdown
<!-- chapter_XX_draft.md -->
<!--
STATUS: writing
WORDS: 650
TARGET: 1000
STARTED: 2026-04-06T19:14:00Z
LAST_UPDATE: 2026-04-06T19:20:00Z
ETA: 10 minutes
-->

# Kapitel XX: Titel

[Content...]
```

**Main Session can check progress:**

```javascript
// Read draft and parse progress
const draft = await read({ file: 'chapter_XX_draft.md' });
const progress = parseProgressHeader(draft);

console.log(`${progress.words}/${progress.target} words`);
console.log(`ETA: ${progress.eta}`);
```

### Timeout Recovery

**On subagent timeout:**

```javascript
// 1. Check if partial draft exists
const draft = await read({ file: 'chapter_XX_draft.md' });
const progress = parseProgressHeader(draft);

// 2. Decide action
if (progress.words > 0) {
  // Partial progress → Resume
  await sessions_spawn({
    label: `NovelCraft-Chapter-${chapterNum}-Resume`,
    mode: "run",
    task: `Resume Chapter ${chapterNum} from ${progress.words} words...`,
    runTimeoutSeconds: 3600
  });
} else {
  // No progress → Retry
  const retries = manifest.chapters[chapterNum].retries || 0;
  if (retries < 3) {
    await sessions_spawn({
      label: `NovelCraft-Chapter-${chapterNum}-Retry-${retries + 1}`,
      mode: "run",
      task: `Rewrite Chapter ${chapterNum} (attempt ${retries + 1})...`,
      runTimeoutSeconds: 3600
    });
  } else {
    // Max retries reached → Manual intervention
    await message({
      action: "send",
      message: `Chapter ${chapterNum} failed after 3 retries. Manual review needed.`
    });
  }
}
```

### Manifest Status Tracking

**Extended chapter entry:**

```yaml
chapters:
  '05':
    status: 'writing'  # pending | writing | reviewing | approved | failed
    subagent:
      session_key: 'agent:opencode:subagent:...'
      run_id: '...'
      started_at: '2026-04-06T19:14:00Z'
      expected_duration: '1800s'
    draft_file: '01-drafts/chapter_05_draft.md'
    review_file: null  # Set after review
    approved_file: '02-chapters/chapter_05.md'
    word_count: 1188
    score: 8.8
    retries: 0
    error: null  # Set if failed
```

---

## Important Rules

- **Autonomous = no intermediate questions**
- **Never write chapters in parallel** — Strictly sequential with tracking
- **Kill existing subagents** before spawning new ones
- **Never block on images** — note time, continue
- **Publish immediately** without images, visuals later
- **Max 3 retries** per chapter, then manual intervention

## Requirements

Before running NovelCraft, ensure you have:

### Required Binaries (for PDF/EPUB)
- `pandoc` — Document conversion
- `xelatex` (optional, for enhanced PDF)

Check with: `which pandoc && which xelatex`

### Disk Space
- Estimated 5-15 MB per novel project
- Drafts, reviews, revisions, and final outputs

### Security
- ⚠️ Review [SECURITY.md](./SECURITY.md) before first use
- Use `step-by-step` mode for testing
- Images are **disabled by default**
- Configure image providers carefully (network calls)

## Configuration Schema v3.0

NovelCraft uses a **3-level configuration hierarchy** with clear override rules:

| Level | Name | File | Purpose | Override |
|-------|------|------|---------|----------|
| 1 | Hardcoded | Skill code | Fallback defaults | — |
| 2 | Module Configs | `workspace/config/module-*.md` | Technical settings | Level 1 |
| 3 | Project Manifest | `workspace/Books/projects/{PROJECT}/project-manifest.md` | Book-specific data | Level 1+2 |

**Rule:** Higher level wins. Only defined fields override lower levels.

### Module Configs (Level 2)

Create in `~/.openclaw/workspace/novelcraft/config/`:

| Config | Key Settings |
|--------|--------------|
| `module-concept.md` | genre, theme, characters, plot, world, chapter_count |
| `module-writer-extras.md` | has_prolog, has_epilog, tone |
| `module-images.md` | provider, generate_cover, generate_characters, generate_settings, **generate_chapter_images**, settings_have_people |
| `module-chapters.md` | min_words, max_words, target_words, max_revisions, scoring_enabled |
| `module-publication.md` | formats: [pdf, epub], pdf_engine, layout, typography |

**See:** `workspace/config/CONFIG-SCHEMA.md` for complete schema documentation.

### Project Manifest (Level 3)

**Path:** `workspace/Books/projects/{PROJECT}/project-manifest.md`

Central status file with:
- Module status tracking (done/pending/rewriting)
- Revision tracking per chapter (status, score, revisions)
- Book-specific overrides (title, chapter_count, has_prolog, etc.)

**See:** `workspace/config/PROJECT-MANIFEST-TEMPLATE.md` for template.

## Modules

| Module | Name | Optional | Order | Description |
|--------|------|----------|-------|-------------|
| 0 | **Target Audience** | ✅ | 0. | **NEW v3.2** — Auto-configures all modules based on age profile |
| 1 | Concept | ❌ | 1. | Genre, plot, characters, world |
| 2 | Writer Extras | ✅ | 2. & 5. | Prolog (before) & Epilog (after) |
| 3 | Images | ✅ | Parallel | Cover, characters, settings, chapter images |
| 4 | Chapters | ❌ | 3. | Sequential writing with review |
| 5 | Publication | ❌ | 4. | PDF/EPUB creation |

## Module Templates

Each module has a template that standardizes subagent calls:

| Module | Template |
|--------|----------|
| Concept | `templates/module-concept-template.md` |
| Writer Extras | `templates/module-writer-extras-template.md` |
| Images | `templates/module-images-template.md` |
| Chapters | `templates/module-chapters-template.md` |
| Review | `templates/module-review-template.md` |
| Revision | `templates/module-revision-template.md` |
| Publication | `templates/module-publication-template.md` |

## Review Workflow with Scoring

### Automatic Decision Based on Score

| Weighted Score | Decision | Action |
|----------------|----------|--------|
| 8.0 - 10.0 | ✅ **APPROVED** | Copy to 02-chapters/, next chapter |
| 6.0 - 7.9 | ⚠️ **MINOR_REVISION** | Specific fixes, max 3 revisions |
| 4.0 - 5.9 | 🔧 **MAJOR_REVISION** | Major rewrite, max 3 revisions |
| 0.0 - 3.9 | ❌ **REJECTED** | Complete rewrite, max 3 revisions |

### Scoring Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| UTF-8 Encoding | ×3 (CRITICAL) | No foreign characters |
| Word Count 7000-8000 | ×2 (HIGH) | Target: 7500 words |
| Continuity | ×2 (HIGH) | Consistent with previous chapter |
| Plot Progression | ×2 (HIGH) | Story develops |
| Character Voice | ×1.5 (MEDIUM) | Believable characters |
| Style & Atmosphere | ×1.5 (MEDIUM) | Fits project style |
| Grammar | ×1 (LOW) | Correct language |

### Revision Rules

- **Max 3 revisions** per chapter
- After 3 revisions → forced rewrite required
- Review saved as `chapter_XX_review.md`
- Revision follows the revision template

---

## Error Handling & Recovery (v3.2)

### Common Failure Scenarios

| Scenario | Cause | Recovery |
|----------|-------|----------|
| **Subagent timeout** | Chapter too long | Check partial draft, resume or retry |
| **Duplicate subagents** | Spawned twice | Kill all, restart with clean state |
| **Wrong chapter output** | Task unclear | Validate output, restart if mismatch |
| **File not found** | Subagent failed silently | Retry with stronger error handling |
| **Manifest out of sync** | Crash during update | Rebuild from filesystem state |

### Subagent Timeout Recovery

**Detection:**
```javascript
// Subagent status: timed_out
{
  status: "timed_out",
  runtime: "6m26s",
  sessionKey: "..."
}
```

**Recovery Steps:**

```javascript
async function handleTimeout(chapterNum) {
  // 1. Check for partial draft
  const draftPath = `01-drafts/chapter_${chapterNum}_draft.md`;
  const draftExists = await fileExists(draftPath);
  
  if (!draftExists) {
    // No draft at all → Full retry
    return await retryChapter(chapterNum, 'no_draft');
  }
  
  // 2. Parse progress from draft header
  const draft = await read({ file: draftPath });
  const progress = parseProgressHeader(draft);
  
  // 3. Decide: Resume vs Retry
  if (progress.words > 0) {
    // Has progress → Resume
    console.log(`Resuming Chapter ${chapterNum} at ${progress.words} words`);
    return await resumeChapter(chapterNum, progress.words);
  } else {
    // No progress → Retry
    console.log(`Retrying Chapter ${chapterNum} from start`);
    return await retryChapter(chapterNum, 'no_progress');
  }
}

async function retryChapter(chapterNum, reason) {
  const manifest = await readManifest();
  const retries = manifest.chapters[chapterNum].retries || 0;
  
  if (retries >= 3) {
    // Max retries → Manual intervention
    await notifyUser(`Chapter ${chapterNum} failed after 3 retries. Reason: ${reason}`);
    return { action: 'manual_intervention', reason };
  }
  
  // Update manifest
  manifest.chapters[chapterNum].retries = retries + 1;
  manifest.chapters[chapterNum].error = reason;
  await saveManifest(manifest);
  
  // Spawn retry subagent
  return await sessions_spawn({
    label: `NovelCraft-Chapter-${chapterNum}-Retry-${retries + 1}`,
    mode: "run",
    runtime: "subagent",
    task: `Rewrite Chapter ${chapterNum} (attempt ${retries + 2}). Previous: ${reason}`,
    runTimeoutSeconds: 3600
  });
}
```

### Duplicate Subagent Prevention

**Problem:** Multiple subagents for same chapter.

**Solution:**

```javascript
async function spawnChapterSafely(chapterNum, task) {
  // 1. List ALL active subagents
  const active = await subagents({ action: "list" });
  
  // 2. Find any for this chapter (fuzzy match)
  const existing = active.filter(s => 
    s.label.includes(`Chapter-${chapterNum}`)
  );
  
  // 3. Kill all existing
  for (const sub of existing) {
    console.log(`Killing existing: ${sub.label} (${sub.sessionKey})`);
    await subagents({ 
      action: "kill", 
      target: sub.sessionKey 
    });
  }
  
  // 4. Wait and verify
  await sleep(1000);
  const verify = await subagents({ action: "list" });
  const stillRunning = verify.filter(s => 
    s.label.includes(`Chapter-${chapterNum}`)
  );
  
  if (stillRunning.length > 0) {
    throw new Error(`Failed to kill ${stillRunning.length} subagents`);
  }
  
  // 5. Safe to spawn
  return await sessions_spawn({
    label: `NovelCraft-Chapter-${chapterNum}`,
    mode: "run",
    runtime: "subagent",
    task,
    runTimeoutSeconds: 3600
  });
}
```

### Wrong Output Validation

**Problem:** Subagent returns wrong chapter or incomplete data.

**Validation:**

```javascript
async function validateChapterOutput(chapterNum, content) {
  const errors = [];
  
  // 1. Check chapter number in content
  const chapterMatch = content.match(/Kapitel\s+(\d+)/i);
  if (chapterMatch && parseInt(chapterMatch[1]) !== chapterNum) {
    errors.push(`Wrong chapter number: expected ${chapterNum}, got ${chapterMatch[1]}`);
  }
  
  // 2. Check word count
  const words = countWords(content);
  const config = await readModuleConfig('chapters');
  if (words < config.min_words || words > config.max_words) {
    errors.push(`Word count ${words} outside range ${config.min_words}-${config.max_words}`);
  }
  
  // 3. Check for required content
  if (!content.includes('#')) {
    errors.push('Missing chapter title (H1)');
  }
  
  // 4. Return result
  return {
    valid: errors.length === 0,
    errors,
    word_count: words
  };
}

// Usage
const result = await validateChapterOutput(5, content);
if (!result.valid) {
  console.error('Validation failed:', result.errors);
  await retryChapter(5, 'validation_failed');
}
```

### Manifest Recovery

**Problem:** Manifest out of sync with filesystem.

**Reconstruction:**

```javascript
async function rebuildManifest(projectPath) {
  const manifest = {
    chapters: {}
  };
  
  // Scan 01-drafts/
  const drafts = await listFiles(`${projectPath}/01-drafts/chapter_*.md`);
  for (const draft of drafts) {
    const num = extractChapterNumber(draft);
    manifest.chapters[num] = manifest.chapters[num] || {};
    manifest.chapters[num].draft_file = draft;
    manifest.chapters[num].status = 'draft';
  }
  
  // Scan 02-chapters/
  const approved = await listFiles(`${projectPath}/02-chapters/chapter_*.md`);
  for (const chapter of approved) {
    const num = extractChapterNumber(chapter);
    manifest.chapters[num] = manifest.chapters[num] || {};
    manifest.chapters[num].approved_file = chapter;
    manifest.chapters[num].status = 'approved';
  }
  
  // Scan reviews
  const reviews = await listFiles(`${projectPath}/01-drafts/chapter_*_review.md`);
  for (const review of reviews) {
    const num = extractChapterNumber(review);
    if (manifest.chapters[num]) {
      manifest.chapters[num].review_file = review;
      if (manifest.chapters[num].status === 'draft') {
        manifest.chapters[num].status = 'reviewing';
      }
    }
  }
  
  await saveManifest(manifest);
  return manifest;
}
```

### Best Practices Summary

1. **Always pre-check** for existing subagents
2. **Always use extended timeout** (3600s minimum)
3. **Always validate** subagent output
4. **Always update manifest** before and after subagent
5. **Always implement retry** with max 3 attempts
6. **Always notify user** on unrecoverable errors

## Directory Structure

**IMPORTANT:** All project data (Books) lives in the workspace, not the skill folder!

### Workspace (Project Data)
```
~/.openclaw/workspace/novelcraft/          ← Workspace (localized)
├── config/
│   ├── CONFIG-SCHEMA.md                  # Schema v3.0 documentation
│   ├── PROJECT-MANIFEST-TEMPLATE.md      # Project template
│   ├── module-concept.md                 # Module: Concept
│   ├── module-writer-extras.md           # Module: Prolog/Epilog
│   ├── module-images.md                  # Module: Images
│   ├── module-chapters.md                # Module: Chapters
│   └── module-publication.md             # Module: Publication
│
└── Books/projects/novel-[TITLE]/
    ├── project-manifest.md                # Central project manifest
    ├── 00-concept/                        # Concept, characters, worldbuilding
    ├── 01-drafts/                         # WIP chapters, reviews, revisions
    │   ├── chapter_01_draft.md
    │   ├── chapter_01_review.md
    │   └── chapter_01_review_v2.md
    ├── 02-chapters/                       # ✅ APPROVED final chapters
    │   ├── chapter_01.md
    │   └── chapter_02.md
    └── 03-final/                          # PDF, EPUB

~/.openclaw/skills/novelcraft/             ← Skill folder (read-only)
├── SKILL.md                               # This file
├── README.md                              # Quick start
├── CHANGELOG.md                           # Version history
├── CONTRIBUTING.md                        # Contribution guidelines
├── templates/                             # Module templates
│   ├── module-concept-template.md
│   ├── module-writer-extras-template.md
│   ├── module-images-template.md
│   ├── module-chapters-template.md
│   ├── module-review-template.md
│   ├── module-revision-template.md
│   └── module-publication-template.md
└── references/
    └── CONFIG.md                          # Config documentation
```

**Workflow:**
1. Drafts in `01-drafts/`
2. Review → Revision if needed
3. On APPROVED → Copy to `02-chapters/`
4. Publication reads only from `02-chapters/`

**Books Path:** `~/.openclaw/workspace/novelcraft/Books/` (always load from workspace)

## Modes

| Mode | Behavior |
|------|----------|
| `autonomous` | No intermediate questions, runs through |
| `step-by-step` | Confirm after each module |

## Images (Optional)

**Default: DISABLED** — Images must be explicitly enabled in `module-images.md`.

### Provider Options

| Provider | Description | Network Calls |
|----------|-------------|---------------|
| `none` (default) | No image generation | No |
| `mcp` | MCP server | Depends on MCP config |
| `local` | Local tools (e.g., MFLUX) | No |
| `manual` | User provides images | No |
| `api` | External API | **Yes — data leaves machine** |

**⚠️ Warning:** Using `api` provider sends book content descriptions to external services. Review your provider's privacy policy.

### Workflow
- **Never block** — start generation, proceed to chapters
- After completion: Create separate version with images

See `references/CONFIG.md` for detailed provider configuration.

## Dashboard

**Current:** No dashboard available. NovelCraft works via command line.

**Planned:** Web-based dashboard for project monitoring and control.
- Live progress for active projects
- Chapter detail view with scores
- Config editor in browser

See [ROADMAP.md](./ROADMAP.md) for details.

## Audio (Planned)

Audiobook generation from completed chapters:
- TTS integration (ElevenLabs, OpenAI, Local)
- Character voices for dialogue
- MP3/WAV export per chapter

See [ROADMAP.md](./ROADMAP.md) for details.

## References

| File | Purpose |
|------|---------|
| `SKILL.md` | This file — main documentation |
| `README.md` | Quick start guide |
| `SECURITY.md` | Security considerations |
| `ROADMAP.md` | Future features (Dashboard, Audio) |
| `CHANGELOG.md` | Version history |
| `CONTRIBUTING.md` | Contribution guidelines |
| `setup.md` | Chat-based setup (Quick-Start) |
| `project-setup.md` | Chat commands for project management |
| `references/CONFIG.md` | Detailed config documentation |
| `workspace/config/CONFIG-SCHEMA.md` | Schema v3.0 specification |
| `workspace/config/PROJECT-MANIFEST-TEMPLATE.md` | Project manifest template |

---

## Target Audience Profiles (v3.2)

**NEW:** Select a profile to auto-configure all modules for your intended readers!

### Available Profiles

| Profile | Age | Chapter Length | Images | Font | Use Case |
|---------|-----|----------------|--------|------|----------|
| `early-readers` | 6-8 | 800-1,200 words | 8+ chars, chapter images | 14pt | Picture books, first readers |
| `middle-grade` | 8-12 | 1,500-2,500 words | 6 chars, chapter images | 12pt | Adventure, fantasy |
| `young-adult` | 12-16 | 3,000-5,000 words | 4 chars | 11pt | Teen themes, romance |
| `new-adult` | 16-25 | 4,000-6,000 words | 3 chars | 11pt | Coming-of-age |
| `adult` | 25+ | 5,000-8,000 words | 3 chars | 10pt | Full narrative freedom |
| `senior` | 60+ | 3,000-5,000 words | 4 chars | 13pt | Large text, relaxed |

### What Auto-Configures?

| Module | Settings |
|--------|----------|
| **Chapters** | Min/max words, sentences/paragraph, max revisions |
| **Images** | Character count, chapter images, settings |
| **Concept** | Wording style, vocabulary complexity |
| **Publication** | Font size, line height, margins, font family |

### Usage

```
Setup: "Start NovelCraft Setup"
→ "Select target audience profile:"
   [1] early-readers (6-8)
   [2] middle-grade (8-12)
   [3] young-adult (12-16)
   [4] new-adult (16-25)
   [5] adult (25+)
   [6] senior (60+)
   [7] custom (manual)
→ User selects: 1
→ All modules auto-configure for 6-8 year olds!
```

### Override Anytime

Keep profile, change one value:
```
"Change chapter target to 1500 words"
"Enable chapter images"
```

See `setup.md` for detailed profile specifications.

---

## Image Configuration (v3.1)

Images are **disabled by default** (provider: none). When enabled, configure categories:

### Image Categories

| Category | Default | Contains People? | Description |
|----------|---------|------------------|-------------|
| **Cover** | ✅ yes | Yes (monsters/characters) | Book cover artwork |
| **Characters** | ✅ yes | Yes (children) | Main character portraits |
| **Monsters** | ✅ yes | Yes (monsters only) | Monster portraits |
| **Settings** | ✅ yes | **NO** (empty places) | Location/environment images |
| **Chapter Images** | ❌ no | Scene-dependent | One illustration per chapter |

### Critical Image Rules

| Rule | Description |
|------|-------------|
| **English Only** | All prompts must be in English (FLUX requirement) |
| **No Text** | Every prompt must include: `"no text, no letters, no words, no typography"` |
| **Settings = Empty** | Settings images NEVER contain people, monsters, or characters |
| **Negative Prompt** | Always add: `"watermark, signature"` to negative prompt |

### Prompt Examples

**Cover:**
```
Children's book cover illustration, four friendly colorful monsters standing in front of a school building, whimsical and playful style, soft pastel colors, storybook art style, magical atmosphere, no text, no letters, no words, no typography, no writing, no watermark, no signature
```

**Character:**
```
Children's book character portrait, young girl 7 years old, brown hair in pigtails, bright curious eyes, friendly smile, soft pastel colors, storybook illustration style, white background, no text, no letters, no words, no typography, no writing, no watermark, no signature
```

**Setting (NO people):**
```
Children's book illustration, cozy elementary school classroom interior, colorful desks and chairs neatly arranged, sunlight streaming through windows, empty room no children no teacher, warm atmosphere, storybook art style, no text, no letters, no words, no typography, no writing, no people, no characters, no humans, no monsters, no watermark, no signature
```

**Chapter Image:**
```
Children's book illustration, scene from chapter: monsters hiding in school closet, surprised expressions, playful mood, colorful and whimsical, storybook art style, no text, no letters, no words, no typography, no writing, no watermark, no signature
```

See `setup.md` for complete prompt guidelines and configuration details.

---

## Quick Start

### Project Management (New)

| Command | Action |
|---------|--------|
| `/novelcraft project` | Create new project |
| `/novelcraft project list` | List all projects with status |
| `/novelcraft project <number>` | Switch to project by number |
| `/novelcraft project <name>` | Switch to project by name |

### Setup & Configuration

| Command | Action |
|---------|--------|
| `/novelcraft setup` | Setup/Reconfigure current project |
| `/novelcraft setup images` | Configure images module |
| `/novelcraft setup chapters` | Configure chapters module |
| `/novelcraft reconfigure` | Reconfigure all modules |
| `/novelcraft reconfigure images` | Reconfigure images only |

### Help & Info

| Command | Action |
|---------|--------|
| `/novelcraft help` | Show help |
| `/novelcraft help images` | Help for specific module |
| `/novelcraft status` | Show project status |
| `NovelCraft --help` | Alternative help syntax |

### Alternative Syntax

```
NovelCraft --project              # Create project
NovelCraft --project-list         # List projects
NovelCraft --setup
NovelCraft --setup --module=images
NovelCraft --reconfigure
NovelCraft --help
NovelCraft --status
```

---

## Full Documentation

| File | Purpose |
|------|---------|
| [setup.md](setup.md) | Chat-based setup guide |
| [project-setup.md](project-setup.md) | Complete command reference |
| [references/CONFIG.md](references/CONFIG.md) | Config schema details |

---

## Version

**Current:** 3.2.0 — Target Audience Profiles & Enhanced Image Configuration

**Maintained by:** Felix (AI) with Ronny (User) 🧠💡
