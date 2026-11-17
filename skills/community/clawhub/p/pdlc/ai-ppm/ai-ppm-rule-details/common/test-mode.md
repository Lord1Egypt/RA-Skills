<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
inclusion: manual
---

# Test Mode — Feedback Capture Assistant

**Activation:** The active package reads this file on demand from its `.aiflc/{family}/{package}-rule-details/common/` home when the user requests test mode (e.g. "enable test mode" / "load test mode").
**Purpose:** Switches the active package to test mode — enabling end-of-phase feedback checkpoints and assisted template filling. All package functionality remains identical; this adds a feedback layer on top.

---

## Mode Behavior

When this steering file is loaded:

1. **You are still running the package normally.** All phases, stages, gates, templates, and outputs work exactly as in run mode. Do not skip steps, reduce quality, or change deliverables.
2. **After completing each phase or stage**, offer a feedback checkpoint (see §2).
3. **If the user reports a finding**, assist them in filling the appropriate template (see §3).
4. **Save findings** to the local `test-feedback-outbox/` folder at the workspace root (see §4).

---

## §1. Detecting the Active Package

You do NOT need a hardcoded package name. Identify the active package from:

1. The currently loaded package steering file (e.g., `ai-pilc-rules`, `ai-adlc-rules`, `ai-dwg-rules`)
2. Any `*-state.md` file in the workspace (e.g., `pilc-state.md`, `adlc-state.md`)
3. If multiple packages are active, tag the finding with whichever package's phase/stage just completed

Use this detected package name to auto-fill the "Package" field in templates.

---

## §2. Feedback Checkpoint

After completing each phase or stage, ask:

> *"✅ [Phase/Stage Name] complete. Test mode is active — did you observe any bugs, gaps, or improvement opportunities during this phase? (yes / no / skip-all)"*

- **yes** → proceed to assisted template fill (§3)
- **no** → continue to the next phase/stage normally
- **skip-all** → disable further checkpoints for the rest of this session (acknowledge: "Test mode checkpoints disabled for this session. You can still request feedback capture anytime by saying 'log feedback'.")

**Rules:**
- The checkpoint is a **suggestion, not a gate** — never block progress on it
- Keep it to one line — do not explain what test mode is each time
- If the user says "log feedback" or "report a bug" at any point (even without a checkpoint prompt), proceed to §3

---

## §3. Assisted Template Fill

When the user wants to report a finding:

### Step 1: Determine finding type

Ask: *"What type of finding? (1) Bug — something didn't work as expected, (2) Improvement — it works but could be better, (3) RCA — deep-dive into why something failed"*

### Step 2: Walk through fields conversationally

Do NOT dump the entire template. Ask one section at a time:

**Auto-fill these (do not ask the user):**
- Package name → detected from active steering/state file
- Stage/file → the phase/stage that just completed
- Date → today's date
- ID → use `TFB-DRAFT-{NNN}` (increment from existing files in outbox, or start at 001)

**Ask the user for these (one at a time):**

For **Bug**:
1. "What happened?" (observed behavior)
2. "What should have happened?" (expected behavior)
3. "Any idea why?" (root cause — optional, can say "not sure")
4. "How severe? (Critical / High / Medium / Low)"
5. "Suggested fix?" (optional)
6. "Does this affect other packages in the chain?" (optional)

For **Improvement**:
1. "What does the package do today?" (current behavior)
2. "What should it do instead/additionally?" (proposed improvement)
3. "Why would this be better?" (justification)
4. "How much effort? (Small / Medium / Large)"
5. "How would you route this? (Quick fix / Open item / New idea / New lesson)"

For **RCA**:
1. "What failed?" (one-sentence problem statement)
2. "Let's do 5-Whys. Why did it happen?" (walk through iteratively)
3. "What's the fix for this instance?" (correction)
4. "What would prevent this class of failure?" (prevention)
5. "Where should this route? (Lesson / Open item / Idea / Direct patch)"

### Step 3: Compose and confirm

After gathering answers, compose the template and show it to the user:

> *"Here's your feedback draft. Please review — especially confirm no sensitive data is included:"*

Show the completed template in a code block.

Then ask: *"Save to outbox? (yes / edit / discard)"*

- **yes** → save to `test-feedback-outbox/` (§4)
- **edit** → ask what to change, update, re-confirm
- **discard** → acknowledge and continue

---

## §4. Outbox Management

### Location

```
{workspace-root}/test-feedback-outbox/
```

### On first use

If `test-feedback-outbox/` does not exist:
1. Create the folder
2. Add `test-feedback-outbox/` to `.gitignore` (create `.gitignore` if it doesn't exist; append if it does)
3. Inform the user: *"Created test-feedback-outbox/ and added to .gitignore. Findings stay local until you choose to submit."*

### File naming

```
TFB-DRAFT-{NNN}-{short-description}.md
```

Examples:
- `TFB-DRAFT-001-scope-stage-missing-gate.md`
- `TFB-DRAFT-002-stakeholder-template-unclear.md`

Increment NNN based on existing files in the outbox.

### What goes in the file

The completed template (from §3 Step 3) plus the mandatory legal notice footer (§5).

---

## §5. Legal Notice — MANDATORY on Every Saved File

Append this block at the bottom of every feedback file saved to the outbox:

```markdown
---

## ⚠️ Feedback Submission Notice

> This feedback template was generated locally on your machine.
> No data is collected, transmitted, or shared automatically.
>
> Submission is VOLUNTARY and MANUAL — you decide what to share.
>
> **YOUR OBLIGATION BEFORE SUBMITTING:**
> You MUST review the entire contents of this file and confirm
> that no sensitive data is present. This includes but is not
> limited to: credentials, API keys, internal URLs, personal
> information, proprietary business data, or classified content.
>
> Reviewing filled data before submission — to ensure no sensitive
> information passes out through this file — is SOLELY AND ENTIRELY
> YOUR RESPONSIBILITY as the end user.
>
> The AI-* package authors do NOT validate, scan, or filter content.
> ALL obligations for data privacy, IP, and compliance rest with YOU.
```

---

## §6. Rules (Non-Negotiable)

1. **NEVER make network calls** — no API requests, no telemetry, no pings, no analytics. Zero outbound traffic.
2. **NEVER auto-capture environment data** — no env vars, no system info, no file contents beyond what the user explicitly provides in conversation.
3. **NEVER include PII fields** — templates do not ask for names, emails, user accounts, organization names, or personal identifiers.
4. **NEVER auto-submit** — files stay in the local outbox until the user manually moves them. There is no "send" command.
5. **NEVER block progress** — test mode is a layer, not a gate. The user can ignore every checkpoint and the package still works fully.
6. **ALWAYS show before save** — the user must see the composed template before it's written to disk.
7. **ALWAYS include the legal notice** — every file in the outbox must have §5 appended.
8. **The user's review obligation is absolute** — explicitly remind them at save time that reviewing for sensitive data before any future submission is their responsibility.

---

## §7. Deactivation

Test mode stays active for the rest of the session once you enable it — it is never auto-loaded. To deactivate:
- Simply don't enable it in the next session
- Or tell the agent: "exit test mode" — the agent will acknowledge and stop offering checkpoints

Deactivation does NOT delete the outbox. Files remain for the user to review/submit at their convenience.

---

## §8. Submission Path (User Reference)

When the user is ready to share findings with the package maintainers:

1. Open `test-feedback-outbox/` in the test workspace
2. **Read every file in full** — redact or delete anything sensitive
3. Manually copy desired files to the package development workspace's `test-feedback/inbox/`
4. That's it — no CLI, no API, no accounts needed

The package development workspace handles triage and routing from there.

---

*Steering Version: 1.0 | Part of the AI-* Family Test Feedback Pipeline*
*Ships with: Every AI-* package at `.aiflc/{family}/{package-name}-rule-details/common/test-mode.md` (read on demand)*
*Delivery: Identical file across all packages — idempotent on multi-package install*
