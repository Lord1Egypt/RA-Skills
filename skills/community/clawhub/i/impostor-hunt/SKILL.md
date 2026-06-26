---
name: impostor-hunt
description: |
  Hunt the impostor in a "finished" deliverable. An impostor is a result-correct artifact whose causal chain is NOT the one the user's purpose required — the test set leaked, only the happy path is wired, correlation got relabeled as cause, the config file exists but no code path reads it, the wrapper greps stdout for "OK" without checking the exit code, the agent "can refactor" backed by one cherry-picked example. The output looks right. The logic that produced "right" is the wrong logic.

  AUTO-INVOKE when a turn declares completion AND the user's original purpose is recoverable from context. Completion signals include: "done", "implemented", "finished", "works now", "ready to merge", "all tests pass", "task complete", "feature shipped", an agent posting a summary with checkmarks, a PR description, a CHANGELOG entry, or a closing message that asserts the work is over. Original purpose is recoverable from: the user's first message in the thread, the issue/ticket text, the PR title and description, the commit message that opened the branch, the README's stated goal, or an explicit prompt the user pasted at the start. If both signals are present, invoke without waiting for an explicit request.

  Also invoke when the user explicitly asks to audit completion truth, detect fake completion, check for hidden goal misalignment, look for mock-driven success, test-set leakage, happy-path-only delivery, correlation-as-causation, configured-but-unread settings, logs-say-success-but-return-code-unchecked, or similar patterns. Triggers in any language; the report mirrors the user's language.

  DO NOT invoke for ordinary bug hunting (route to code-review), style or refactor cleanup (route to simplify), or behavior-by-execution verification (route to verify / run). DO NOT invoke when the user is mid-implementation and has not yet declared the work done — interrupting an in-flight task with a completion audit is noise. DO NOT invoke when the original purpose is not recoverable from context; ask for it first instead of guessing.
---

# Impostor Hunt

> **Hunt the impostor. Spare the honest work.**

Surface-correct is not correct. A passing test is a hypothesis, not a verdict. This skill exists to catch one specific failure mode and refuse to be distracted by anything else.

## What this skill is for

The user — or the moment — wants to detect a **causal impostor**.

A causal impostor is a deliverable whose output is surface-correct, but the causal chain that produced it is not the one the user's purpose requires. It is not a bug. It is a cheaper causal chain wearing the costume of the expensive one the user actually asked for.

This is the **primary line** of the audit. It stays sharp.

Non-impersonation problems (ordinary bugs, design smells, improvable code) may also be noticed in passing. These are the **secondary line**. They go into a separate section, clearly labeled as *not* impersonation. They never enter the verdict.

## When this skill should fire

This skill is built to **auto-trigger**, not to wait for permission.

### Auto-trigger preconditions (both must hold)

1. **Completion is being declared in this turn.** Look for: "done", "implemented", "finished", "works now", "ready to merge", "all tests pass", "task complete", "feature shipped", a checklist of ticked items, a PR description, a CHANGELOG entry, a closing message that asserts the work is over. An agent handing off a summary counts.
2. **The user's original purpose is recoverable from context.** Look in: the user's first message, the issue or ticket text, the PR title and description, the commit that opened the branch, the README's stated goal, an explicit prompt the user pasted at the start.

If both hold, fire. Do not ask permission. Do not wait for `/impostor-hunt`. The whole point is to catch impostors before the user has to suspect one.

### When NOT to fire

- Mid-implementation. Interrupting in-flight work with a completion audit is noise.
- Pure bug reports → `code-review`.
- Refactor / cleanup requests → `simplify`.
- Behavior-by-execution verification → `verify` / `run`.
- Original purpose is not recoverable. Ask the user for it; do not guess and audit a guess.

### Recovering the original purpose

Read in this priority order, stop at first hit:

1. The **verbatim user message** that opened the task or the thread.
2. The **issue / ticket body** linked in the PR or branch name.
3. The **PR description** (not the title alone — titles compress).
4. The **commit message** of the first commit on the branch.
5. The **README** section that states the project's goal.

Capture the longest contiguous purpose statement you can find. Quote it verbatim in Step 0. Inferred clauses must be marked `[inferred]` and must be one-sentence-overrideable.

## Hard principles

1. Do not hunt impersonation to find it. Most projects do not contain it. **"Causally aligned" is the correct verdict when the evidence supports it** — and the skill is designed to issue that verdict cleanly, not manufacture suspicion to look useful.
2. Missing evidence is not error. Reasonable suspicion is not fact.
3. Surface correctness is not completion. Existing tests are not effective validation. Smooth explanation is not established causation.
4. The verdict is about impersonation only. Side findings never alter it.
5. Side findings must not outnumber main-line checked positions by more than 2×. Excess gets cut. This protects the primary line from dilution.
6. If you triggered the skill yourself (auto-invoked, no explicit user request), the **first line of your report** must state that fact and quote the completion signal that fired you. The user gets to see why you decided to audit.

## Protocol — execute in order

### Step 0 — Scope Intake

Before anything else, write this block. It is the spine of the whole audit.

```
- Trigger:                     (auto / explicit) — if auto, quote the completion signal
- Artifact type:               (repo / code snippet / report / config / agent output / claim only)
- Access level:                (full source / partial / claim-only)
- User's purpose, verbatim:    (exact words, from the priority order above)
- Purpose source:              (which of the 5 recovery channels)
- Delivery's stated purpose:   (from README / summary / naming / output)
- Wording delta:               (any difference between the two, however small)
- Audit budget:                (shallow / standard / deep)
```

The **wording delta** is the single most important field. Impersonation almost always lives in the gap between these two strings — e.g. "predicts accurately" vs "predicts accurately on the test set", "handles orders" vs "handles orders in the happy path", "config is applied" vs "config file exists".

### Step 1 — Restore Purpose

Reconstruct the user's real purpose. Then self-check:

- Mark each clause as **[verbatim]** or **[inferred]**.
- Any **[inferred]** clause must be one the user could overrule in a single sentence. If it is not, drop it. Over-reach in purpose restoration becomes manufactured impersonation in Step 6.

If purpose restoration is wrong, every later step is wrong. This self-check is non-negotiable.

### Step 2 — Extract Auditable Claims

Decompose "completed" into completion claims.

**Auditability rule**: a claim is auditable only if it is falsifiable by a concrete observation (a file's content, a command's output, a value at a specific input). "Code quality is good" is not a claim. "`process_order()` raises `ValueError` on negative amount" is.

Discard non-auditable claims. Do not pad the table.

### Step 3 — Build Evidence Map (main-line claims only)

For each main-line claim, fill the audit table from `references/report-template.md`. Use evidence levels A/B/C/D/E from `references/evidence-model.md`.

Side-line observations do **not** go through this table. They have their own section in Step 9.

### Step 4 — Expose Hidden Assumptions

List the assumptions the artifact silently depends on. Mark each as **Supported / Risky / Unknown**. Impersonation often hides as an unstated assumption (e.g. "the input distribution at runtime matches training", "the mock matches the real service's error semantics").

### Step 5 — Apply Lenses

Use `references/audit-lenses.md`.

- **Main-line lenses (must run)**: Purpose Alignment, Causal Authenticity, Validation Integrity, Complexity Preservation.
- **Side-line lenses (run if budget allows)**: Entity Reality, Semantic Consistency, Constraint Closure, Path Completeness, User Consequence, Claim Truth.

Findings from main-line lenses go into the main audit. Findings from side-line lenses go into the side section.

### Step 6 — Causal Impersonation Scan

This is the core step. Walk through `references/causal-impersonation-patterns.md` and, for each pattern relevant to the artifact type, ask:

- **Expected causal chain**: what causal chain does the user's purpose require?
- **Actual causal chain**: what causal chain does the artifact actually run?
- **Why invisible at surface**: why does the surface output look correct anyway?

For every main-line claim flagged as purpose-critical in Step 3, this trio must be filled in — **even if the conclusion is "no impostor here"**. Recording the negative result is what makes "Causally aligned" a credible verdict instead of an empty shrug.

### Step 7 — Tribunal

Use `references/tribunal.md`. Three roles only:

- **Causal Auditor** — main-line argument: is the causal chain impersonated?
- **Side Findings Collector** — sweeps non-impersonation issues into the side section so they do not leak into Causal Auditor's reasoning.
- **Calibration Skeptic** — bidirectional: argues against over-suspicion *and* against premature dismissal.

Each role outputs its strongest 1–3 points only. No role-play prose.

### Step 8 — Symmetric Pre-mortem

Do **both**:

- If I now conclude *impostor exists*, what is the most likely way I am wrong?
- If I now conclude *no impostor*, what is the most likely way I am wrong?

Both branches must be written. Skipping one biases the verdict.

### Step 9 — Verdict & Report

Use `references/report-template.md`. The verdict is **only** about impersonation, drawn from `references/verdict-rubric.md`. Side findings live in their own section and never change the verdict.

If you auto-invoked, the report opens with the trigger line from Step 0 — the user sees what made you fire before they see what you found.

## Verdict gates (hard rules)

- **Confirmed impostor** requires ≥1 E-level evidence (something directly contradicts the claim) **or** ≥2 purpose-critical claims at C-level **plus** a concrete failure scenario from the Causal Impersonation Scan.
- **Suspected impostor** requires at least one purpose-critical claim at C/D with a named high-risk position from the patterns file.
- **Causally aligned** is a first-class verdict. It requires listing 3–5 high-risk positions checked and why each is clean. It is not a fallback for "I found nothing"; it is an active conclusion.
- **Undecidable** requires naming the specific material whose absence blocks the judgment and the minimal action that would unblock it.
- Every verdict carries a confidence in [0, 1] and the result of the symmetric pre-mortem.

## Side-findings cap

`count(side_findings) ≤ 2 × count(main_line_positions_checked)`

If exceeded, drop the side findings with the weakest evidence until the ratio holds. Report the cut ("N side findings dropped to preserve main-line focus").

## Output language

Default to English. If the user's invocation, or the recovered purpose, is in another language, mirror that language in the report. The protocol itself (step names, verdict tier labels, evidence levels) stays in English so cross-language reports remain comparable.

## What this skill will not do

- It will not produce a bug list. Use `code-review`.
- It will not run code to verify claims unless the user explicitly asks. Verification-by-execution can manufacture new surface-correct outputs that mask the original impersonation. D-level claims become **leads**, not chores.
- It will not invent an impostor to satisfy the user or to justify its own invocation. "Causally aligned" is the correct verdict when the evidence supports it. **A clean audit is a successful audit.**
