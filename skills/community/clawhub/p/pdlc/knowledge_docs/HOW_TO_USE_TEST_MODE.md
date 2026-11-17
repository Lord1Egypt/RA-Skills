# How to Use Test Mode

**Purpose:** Explains how to activate test mode in any AI-* package, capture feedback during a workflow session, and manage your findings — without disrupting the workflow itself.

---

## What Test Mode Is

Test mode is a **feedback capture layer** that sits on top of any AI-* package workflow. When active, it adds lightweight checkpoints after each phase or stage, giving you an opportunity to report bugs, improvements, or root-cause analyses — all without changing how the package runs.

Think of it as a structured notepad that knows what stage you just completed and helps you write up findings in a consistent format.

```
┌─────────────────────────────────────────────────────────┐
│              NORMAL PACKAGE WORKFLOW                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │  Stage 1  │→│  Stage 2  │→│  Stage 3  │→ ...        │
│  └──────────┘  └──────────┘  └──────────┘              │
│       │              │              │                    │
│       ▼              ▼              ▼                    │
│  ┌──────────────────────────────────────────────┐       │
│  │  TEST MODE LAYER (feedback checkpoints)       │       │
│  │  "Any bugs, gaps, or improvements?"           │       │
│  └──────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────┘
```

**Key principle:** Test mode never blocks progress. It's a suggestion layer, not a gate.

---

## When to Use It

| Scenario | Why Test Mode Helps |
|----------|-------------------|
| First time running a package on a real project | Captures real-world gaps the documentation didn't anticipate |
| After a package update | Validates that changes work correctly in your context |
| When evaluating a package for your team | Structured way to document what works and what doesn't |
| During a pilot with multiple team members | Everyone captures findings in the same format |

---

## How to Activate

Just tell the AI in plain language. Any of these work:

```
enable test mode
```

You can also say "I want to run <package> in test mode" or "test mode on". The active package detects which package is running (e.g., `ai-pilc-rules`, `ai-adlc-rules`) and reads `test-mode.md` on demand from its rule-details home (`.aiflc/{family}/{package}-rule-details/common/test-mode.md`), then starts offering feedback checkpoints after each stage completes.

**Important:** Test mode never auto-loads. It is read on demand only when you ask for it, so it works the same on every platform.

---

## What Happens Once Active

### 1. Package Runs Normally

All phases, stages, gates, templates, and outputs work exactly as they do without test mode. No steps are skipped, quality is unchanged, deliverables are identical.

### 2. Feedback Checkpoints Appear

After each phase or stage completes, you'll see:

> *"✅ [Stage Name] complete. Test mode is active — did you observe any bugs, gaps, or improvement opportunities during this phase? (yes / no / skip-all)"*

Your options:
- **yes** → The assistant walks you through a structured feedback template
- **no** → Continue to the next stage normally
- **skip-all** → Disables checkpoints for the rest of the session (you can still say "log feedback" anytime)

### 3. Ad-Hoc Feedback

You don't have to wait for a checkpoint. At any point, say:

- "log feedback"
- "report a bug"
- "I found an issue"

The assistant will help you fill a template immediately.

---

## Feedback Types

When you report a finding, you choose one of three types:

### Bug — Something Didn't Work as Expected

The assistant asks:
1. What happened? (observed behavior)
2. What should have happened? (expected behavior)
3. Any idea why? (root cause — optional)
4. How severe? (Critical / High / Medium / Low)
5. Suggested fix? (optional)
6. Does this affect other packages in the chain? (optional)

### Improvement — It Works but Could Be Better

The assistant asks:
1. What does the package do today? (current behavior)
2. What should it do instead/additionally? (proposed improvement)
3. Why would this be better? (justification)
4. How much effort? (Small / Medium / Large)
5. How would you route this? (Quick fix / Open item / New idea / New lesson)

### RCA — Deep-Dive Into Why Something Failed

The assistant walks through:
1. What failed? (one-sentence problem statement)
2. 5-Whys analysis (iterative)
3. What's the fix for this instance? (correction)
4. What would prevent this class of failure? (prevention)
5. Where should this route? (Lesson / Open item / Idea / Direct patch)

---

## How Findings Are Saved

### Location

All findings are saved locally to:

```
{your-workspace}/test-feedback-outbox/
```

On first use, the assistant creates this folder and adds it to `.gitignore` automatically. Nothing leaves your machine without your explicit action.

### File Naming

```
TFB-DRAFT-{NNN}-{short-description}.md
```

Examples:
- `TFB-DRAFT-001-scope-stage-missing-gate.md`
- `TFB-DRAFT-002-stakeholder-template-unclear.md`

### Auto-Filled Fields

The assistant fills these automatically (you don't need to provide them):
- Package name (detected from active steering)
- Stage/file (the phase that just completed)
- Date
- Draft ID

### Review Before Save

You always see the composed template before it's written to disk:

> *"Here's your feedback draft. Please review — especially confirm no sensitive data is included."*

Options: **save** / **edit** / **discard**

---

## Privacy and Security

| Guarantee | Detail |
|-----------|--------|
| **Zero network calls** | No API requests, no telemetry, no pings. Zero outbound traffic. |
| **No auto-capture** | No environment variables, system info, or file contents beyond what you explicitly provide |
| **No PII fields** | Templates never ask for names, emails, or personal identifiers |
| **No auto-submit** | Files stay local until you manually move them |
| **Your review obligation** | Before any future submission, you are responsible for reviewing files for sensitive data |

---

## How to Deactivate

Three ways:

1. **Don't enable it next session** — test mode never auto-loads
2. **Mid-session:** Say "exit test mode" — checkpoints stop immediately
3. **Skip checkpoints only:** Say "skip-all" at any checkpoint — test mode stays active but goes silent

Deactivation does NOT delete the outbox. Your findings remain for review.

---

## How to Submit Findings (Optional)

Submission is entirely voluntary and manual:

1. Open `test-feedback-outbox/` in your workspace
2. **Read every file in full** — redact or delete anything sensitive
3. Copy desired files to the package maintainers' feedback inbox (if one exists)

No CLI, no API, no accounts needed. The decision to share is always yours.

---

## Multi-Package Usage

Test mode works with any AI-* package. It auto-detects which package is active from:
- The currently loaded package steering file
- Any `*-state.md` file in the workspace

If multiple packages are active in the same session, findings are tagged with whichever package's stage just completed.

---

## Tips for Effective Feedback

| Tip | Why |
|-----|-----|
| Report findings immediately when you notice them | Context is freshest right after the stage completes |
| Use severity honestly | Critical = workflow can't proceed; Low = cosmetic |
| Include "suggested fix" when you can | Speeds up resolution significantly |
| Note chain impacts | "This will also affect AI-DWG's mapping" helps maintainers prioritize |
| One finding per report | Keeps things traceable and individually actionable |

---

## Related Documents

| Document | Location |
|----------|----------|
| How Gates and Approvals Work | `knowledge_docs/HOW_GATES_AND_APPROVALS_WORK.md` |
| How State Files Work | `knowledge_docs/HOW_STATE_FILES_WORK.md` |
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |
| How Package Installation Works | `knowledge_docs/HOW_PACKAGE_INSTALLATION_WORKS.md` |
| How Steering File Loading Works | `knowledge_docs/HOW_STEERING_FILE_LOADING_WORKS.md` |

---

*Knowledge Document | Created: 2026-06-15 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
