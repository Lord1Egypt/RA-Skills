# Test Mode — User Guide

**For:** End users of AI-* packages who want to report bugs, improvements, or root-cause analyses back to the package maintainers.

**Version:** 1.0 | **Last Updated:** 2026-06-13

---

## Table of Contents

1. [What Is Test Mode?](#1-what-is-test-mode)
2. [When to Use It](#2-when-to-use-it)
3. [Activating Test Mode](#3-activating-test-mode)
4. [Using Test Mode](#4-using-test-mode)
5. [The Feedback Outbox](#5-the-feedback-outbox)
6. [Submitting Feedback](#6-submitting-feedback)
7. [Privacy & Your Obligations](#7-privacy--your-obligations)
8. [Deactivating Test Mode](#8-deactivating-test-mode)
9. [FAQ](#9-faq)

---

## 1. What Is Test Mode?

Test Mode is an **optional layer** you can activate on any AI-* package that adds feedback capture assistance to your normal workflow. When active:

- The package works **exactly as normal** — no changes to outputs, quality, or behavior
- After each phase/stage completes, you're offered a brief **feedback checkpoint**
- If you want to report something, the AI **walks you through** filling a structured template
- Your feedback is saved **locally on your machine** — nothing leaves without your explicit action

Think of it as a built-in notepad for testing observations, but smarter — it asks the right questions and saves in a format that package maintainers can act on.

---

## 2. When to Use It

**Use test mode when you are:**
- Evaluating a package for the first time and want to capture impressions
- Running through a package workflow specifically to test it
- Using a package in a real project but notice something worth reporting
- Performing a structured QA pass on a new package version

**Don't use test mode when you:**
- Just want to use the package normally with no intention to give feedback
- Are in a time-sensitive situation where even brief prompts would be a distraction

Test mode is always **opt-in and non-blocking** — you can ignore every checkpoint or disable them mid-session.

---

## 3. Activating Test Mode

### Just Tell the AI

Test mode activates by intent — you simply tell the AI in plain language. Any of these work:

```
enable test mode

Let's start portfolio governance.
```

```
I want to run AI-PPM in test mode.
```

```
test mode on
```

The active package reads `test-mode.md` on demand from its rule-details home (`.aiflc/pdlc/ai-ppm-rule-details/common/test-mode.md`) and begins offering feedback checkpoints after each stage completes. Nothing auto-loads — test mode starts only when you ask for it, and it works the same on every platform.

### What Happens on Activation

1. The AI acknowledges test mode is active
2. On first use, a `test-feedback-outbox/` folder is created in your workspace root
3. That folder is added to `.gitignore` (your findings won't be committed accidentally)
4. The package workflow begins normally

### Works Standalone

Test mode works the same whether you have **one package** installed or **the entire AI-* family**. No dependencies on other packages.

---

## 4. Using Test Mode

### Normal Flow (No Feedback)

```
AI: ✅ Portfolio Registration complete. Test mode is active — did you observe any
    bugs, gaps, or improvement opportunities during this phase? (yes / no / skip-all)

You: no

AI: [continues to next phase normally]
```

### Reporting a Finding

```
AI: ✅ Prioritization Phase complete. Test mode is active — did you observe any
    bugs, gaps, or improvement opportunities during this phase? (yes / no / skip-all)

You: yes

AI: What type of finding?
    (1) Bug — something didn't work as expected
    (2) Improvement — it works but could be better
    (3) RCA — deep-dive into why something failed

You: 1

AI: What happened? (describe the observed behavior)

You: The portfolio scoring algorithm didn't account for cross-project dependencies.

AI: What should have happened?

You: Projects with shared dependencies should receive a dependency-coupling score adjustment.

AI: Any idea why this was missed? (optional — say "not sure" if unsure)

You: not sure

AI: How severe? (Critical / High / Medium / Low)

You: High

AI: Suggested fix? (optional)

You: Add a dependency matrix check before final prioritization scoring.

AI: Does this affect other packages in the chain? (optional)

You: Yes, could affect AI-FLO routing decisions downstream.

AI: Here's your feedback draft. Please review — especially confirm no sensitive
    data is included:

    [shows completed template]

    Save to outbox? (yes / edit / discard)

You: yes

AI: ✅ Saved to test-feedback-outbox/TFB-DRAFT-001-dependency-scoring-gap.md
    Remember: review this file for sensitive data before any future submission.
    [continues to next phase]
```

### Skipping All Checkpoints

```
AI: ✅ Portfolio Registration complete. Test mode is active — did you observe any
    bugs, gaps, or improvement opportunities? (yes / no / skip-all)

You: skip-all

AI: Test mode checkpoints disabled for this session. You can still request
    feedback capture anytime by saying "log feedback".
```

### Reporting Without a Checkpoint

You can report a finding at **any time** — you don't have to wait for a checkpoint:

```
You: log feedback

AI: What type of finding? (1) Bug (2) Improvement (3) RCA
```

Or more naturally:

```
You: I just noticed a bug — the portfolio register doesn't propagate Project IDs
     from upstream PIPs correctly.

AI: Let me capture that as a bug report. [proceeds with assisted fill]
```

---

## 5. The Feedback Outbox

### Location

```
{your-workspace}/test-feedback-outbox/
```

### What's Inside

```
test-feedback-outbox/
├── TFB-DRAFT-001-dependency-scoring-gap.md
├── TFB-DRAFT-002-cross-project-risk-rollup.md
└── TFB-DRAFT-003-rca-prioritization-staleness.md
```

### Key Facts

| Fact | Detail |
|------|--------|
| **Created automatically** | On your first saved finding |
| **Gitignored** | Won't be committed to your project repo |
| **Local only** | Files never leave your machine without your action |
| **Persistent** | Survives session restarts and test mode deactivation |
| **Shared** | All packages write to the same outbox (if multiple are installed) |
| **Your property** | Delete, edit, or ignore at any time |

### File Format

Each file contains:
- Header with metadata (package, stage, date, severity)
- Your observations (what happened, expected behavior, etc.)
- A legal notice reminding you to review before submission

---

## 6. Submitting Feedback

### Important: Submission is 100% Manual

There is **no "send" button**, no API call, no network transmission. Submission means you physically copy files from your outbox to the package maintainer's workspace.

### Step-by-Step

1. **Open** `test-feedback-outbox/` in your workspace
2. **Read each file completely** — this is your responsibility (see §7)
3. **Redact or delete** anything you don't want to share:
   - Internal project names or details
   - Credentials, tokens, or API keys
   - Personal information
   - Proprietary business logic
   - Anything classified by your organization
4. **Copy** the files you want to submit to the package maintainer's `test-feedback/inbox/` folder
5. **Done** — the maintainer handles triage and routing from there

### What If I Don't Want to Submit?

That's perfectly fine. The outbox is yours. You can:
- Keep findings as personal notes
- Delete the entire `test-feedback-outbox/` folder
- Cherry-pick only some findings to submit
- Submit weeks or months later

There is zero expectation or obligation to submit.

---

## 7. Privacy & Your Obligations

### What the Package Does NOT Do

| Never | Explanation |
|-------|-------------|
| ❌ Makes network calls | Zero outbound traffic — no APIs, no telemetry, no pings |
| ❌ Captures environment data | No env vars, system info, or file contents are auto-read |
| ❌ Asks for personal info | No fields for names, emails, accounts, or identifiers |
| ❌ Sends data anywhere | Files stay local until YOU physically move them |
| ❌ Validates your content | The AI does not scan for secrets or sensitive data |

### What YOU Must Do Before Submitting

> **Reviewing filled feedback data before submission — to ensure no sensitive information passes out through the file — is SOLELY AND ENTIRELY YOUR RESPONSIBILITY as the end user.**

Specifically:

- [ ] Read the entire file, every line
- [ ] Confirm no credentials, API keys, or tokens are present
- [ ] Confirm no internal URLs, server names, or infrastructure details are included
- [ ] Confirm no personal information (names, emails, employee IDs) is present
- [ ] Confirm no proprietary business data, trade secrets, or classified content is included
- [ ] Confirm compliance with your organization's data sharing and classification policies

### Why This Obligation Is Yours

The package generates feedback files based on what **you tell it** in conversation. It has no way to know what's sensitive in your context. A project name that's harmless to one person might be confidential for another. Only you — with knowledge of your organization's policies — can make that judgment.

The package authors:
- Do NOT validate submitted content
- Do NOT scan for sensitive data
- Accept NO liability for what you choose to share
- Bear NO responsibility for regulatory non-compliance

---

## 8. Deactivating Test Mode

### For This Session

Tell the AI:

```
You: exit test mode
```

The AI will stop offering checkpoints. Your outbox files remain untouched.

### For Future Sessions

Simply don't enable test mode in your next session (it never auto-loads). Test mode only activates when you explicitly ask for it.

### Cleaning Up

To remove the outbox entirely:

```
Delete the test-feedback-outbox/ folder
```

To remove the gitignore entry:

```
Remove "test-feedback-outbox/" from your .gitignore
```

Neither action is required — the outbox causes no harm if left in place.

---

## 9. FAQ

### Does test mode change the package's output?

**No.** All deliverables, templates, phases, and gates work identically. Test mode only adds optional feedback checkpoints between stages.

### Can I use test mode on a real project (not just for testing)?

**Yes.** Test mode works on any project. If you notice something worth reporting during real work, you can capture it without interrupting your flow.

### What if multiple packages are installed?

One shared `test-feedback-outbox/` at the workspace root. Each finding is tagged with the specific package it relates to. No conflicts.

### What if I accidentally include sensitive data in a finding?

Delete or edit the file in `test-feedback-outbox/` before submitting. If already submitted, contact the package maintainer to remove it from their `test-feedback/inbox/`.

### Do I need to install anything extra?

**No.** Test mode ships with every AI-* package. No additional tools, dependencies, or accounts needed.

### Can the package maintainers see my findings without me submitting?

**No.** Files exist only on your local machine until you physically copy them elsewhere. There is no background sync, no cloud storage, no shared drive.

### What format should I use to submit?

Copy the `.md` files as-is. The maintainer's triage process expects the template format that test mode generates.

### How do I know which version of a package I found the bug in?

The AI auto-fills the package name and active stage. If you want to note the version, add it in the "What happened" or "Test environment" section.

### Can I log feedback without test mode active?

The templates are available in the package source at `the package source under templates/`. You can fill them manually without test mode — test mode just makes it easier by asking questions conversationally.

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────┐
│  TEST MODE — QUICK REFERENCE                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ACTIVATE:    say "test mode on"                    │
│  REPORT:      "log feedback" or "report a bug"      │
│  SKIP:        "skip-all" at any checkpoint          │
│  DEACTIVATE:  "exit test mode"                      │
│                                                     │
│  OUTBOX:      test-feedback-outbox/                 │
│  SUBMIT:      manually copy → maintainer's inbox/   │
│  OBLIGATION:  review ALL content before submitting  │
│                                                     │
│  SAFE:  ✅ No network calls                         │
│         ✅ No telemetry                             │
│         ✅ No PII collected                         │
│         ✅ Nothing leaves without your action       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

*User Guide Version: 1.0 | Part of the AI-* Family Test Feedback Pipeline*
*This guide ships with every AI-* package in `setup/TEST_MODE_USER_GUIDE.md`*
