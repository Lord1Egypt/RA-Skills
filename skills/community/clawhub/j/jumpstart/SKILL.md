---
name: jumpstart
description: Sets up and manages a long-running agent harness for complex, multi-session coding projects. Use this skill whenever a user invokes jumpstart, jumpsession, jumploop, or jumpfree, or when they want to build something substantial that won't fit in a single context window — web apps, large codebases, multi-feature products — or when they ask about autonomous coding agents, multi-session agents, agent loops, or keeping progress across sessions. Also trigger when the user asks how to structure an agent to avoid losing context, how to make an agent work incrementally, or how to prevent an agent from declaring victory too early.
---

# Jumpstart: Long-Running Agent Harness

A skill for setting up and running a two-command agent harness that enables sustained, incremental progress across many context windows — based on Anthropic's *Effective Harnesses for Long-Running Agents*.

---

## Commands

| Command | When to use | What it does |
|---|---|---|
| `jumpstart` | Once, at project start | Reads design files, scaffolds the environment, generates `feature_list.json` |
| `jumpsession` | Every subsequent session | Orients from `progress.txt`, picks one feature, implements, commits, logs |
| `jumploop --n` | Batch implementation sessions | Like `jumpsession` but loops through up to `n` features without stopping |
| `jumpfree` | Ad-hoc or exploratory sessions | Orients from `progress.txt`, implements based on user input, commits, logs |

---

## Input: Design Files

Before running `jumpstart`, the project directory should contain these three files. If `jumpstart` is called and any of these files are missing, create blank versions of them:

| File | Contents |
|---|---|
| `GENERAL_DESIGN.md` | High-level product vision, goals, non-goals, target users |
| `UX_DESIGN.md` | User flows, interface descriptions, interaction patterns |
| `ENG_DESIGN.md` | Technical architecture, components, data models, APIs, constraints |

`jumpstart` derives `feature_list.json` primarily from `ENG_DESIGN.md`, cross-referencing the other two for completeness.

---

## Environment Files Created by `jumpstart`

| File | Purpose |
|---|---|
| `init.sh` | Starts the dev server and runs a basic smoke test |
| `feature_list.json` | Exhaustive feature list derived from `ENG_DESIGN.md`, all initially `not_started` |
| `progress.txt` | Running log of what each session accomplished |
| Initial git commit | Baseline snapshot the agent can always revert to |

---

## `jumpstart` Prompt

> Use for the very first session only.

```
You are initializing a long-running coding project. Your job is NOT to build the app — it's to read the design documents and set up everything the next agent will need.

STEP 1 — Read the design documents:
- Read GENERAL_DESIGN.md for product vision and goals
- Read UX_DESIGN.md for user flows and interface patterns
- Read ENG_DESIGN.md for technical architecture and component breakdown
- IMPORTANT: If any of these three design files do not exist, create them as blank files before proceeding.

STEP 2 — Create init.sh:
A script that starts the development server and runs a basic end-to-end smoke test
(e.g., verify the server starts, the app loads, and one core interaction completes).
Make it runnable: chmod +x init.sh

STEP 3 — Create feature_list.json:
Derive a comprehensive list of features from ENG_DESIGN.md, supplemented by UX_DESIGN.md.
Each feature must have:
  - "id": unique string, e.g. "feat-001"
  - "category": functional | ui | performance | security | infrastructure
  - "description": plain English, specific and testable
  - "steps": array of steps a human tester would follow to verify end-to-end
  - "status": "not_started"  ← always not_started to begin
  - "notes": ""  ← empty string, for agents to leave observations

Be exhaustive. 50–200+ features for a real app. Vague features are useless.
Good: "User can submit the login form with valid credentials and be redirected to the dashboard"
Bad: "Login works"

STEP 3b — Insert human verification checkpoints:
After generating the feature list, insert checkpoint entries at logical milestone
boundaries — places where a human should pause and verify the app before moving on.
Checkpoints must be placed at transitions that represent meaningful integration
points, for example:
  - After all core UI components are implemented
  - After basic navigation/routing is working
  - After backend API is functional
  - After frontend-backend integration is connected
  - After authentication/authorization is wired up
  - Before performance or polish work begins

Each checkpoint must have:
  - "id": unique string, e.g. "checkpoint-001"
  - "type": "checkpoint"  ← distinguishes from regular features
  - "description": what milestone was just reached, e.g. "Core UI shell complete"
  - "verify": array of short items a human should check at this point
  - "status": "not_started"
  - "notes": ""

Place 3–6 checkpoints across a typical project. They must appear in the correct
position in the feature list (after the features they gate). Do not cluster them —
spread them at natural breakpoints.

STEP 4 — Create progress.txt:
Start with a header: "PROJECT: [project name]" and today's date.
Add a single entry: "Session 0 — Initialization complete. feature_list.json generated with [N] features and [M] checkpoints."

STEP 5 — Initial git commit:
git add -A && git commit -m "init: project scaffold, feature list, and environment setup"

RULES:
- Do not implement any features.
- Do not change any feature's status from not_started.
- Do not modify the design files.
```

---

## `jumpsession` Prompt

> Use for every session after the first.

```
You are a coding agent resuming work on an ongoing project.

START OF SESSION — do these steps in order:
1. Run `pwd` to confirm your working directory.
2. Read `progress.txt` — focus on the most recent session entry.
3. Run `git log --oneline -20` to review recent commits.
4. Run `init.sh` to start the dev server and confirm there is no broken build.
   If it IS broken, fix the regression before starting new work.
5. Read `feature_list.json`. Choose the highest-priority feature with status "not_started".
   Prefer features that unblock other features.
   If the next item is a checkpoint ("type": "checkpoint"), handle it first (see below).

DURING YOUR SESSION:
- Work on EXACTLY ONE feature per session. Stop after it is resolved.
- When you begin a feature, update its status to "in_progress".
- Implement, then verify the feature works. Prefer inspecting the DOM or reading server
  output over opening a browser URL — do not let an inability to open a URL block you.
  Browser automation tools (e.g., Puppeteer) may be used when readily available, but are
  not required.
- When verified, set status to "complete" and commit immediately:
  `git add -A && git commit -m "feat([id]): [feature name] — [brief summary]"`
- If you hit a hard blocker (missing dependency, design ambiguity, unresolvable bug),
  set status to "blocked", commit the current state, and document the reason in "notes".
- NEVER remove or edit a feature's description or steps — only update status and notes.
- NEVER mark a feature "complete" without having verified it.

CHECKPOINTS:
- If the next item in the feature list is a checkpoint ("type": "checkpoint"),
  do NOT skip it. Present the checkpoint's "verify" list to the user and ask them
  to confirm everything looks good before proceeding.
- Set the checkpoint's status to "awaiting_review" and stop the session.
- The user will mark it "complete" (or provide feedback) before the next session.

END OF SESSION — after committing the feature, do these final steps:
1. Append to progress.txt:
   - Date and session number
   - Feature worked on and its final status
   - Any bugs found and whether they were fixed
   - Blockers or open questions
   - Recommended next feature for the following session
2. Stop. Do not begin a second feature.

RULES:
- It is unacceptable to mark a feature complete without verifying it.
- It is unacceptable to edit or remove feature descriptions or steps.
- It is unacceptable to declare the project done unless every feature is "complete" or "deferred".
- Always leave the codebase in a mergeable state — no broken builds, no half-implemented features.
- Never end a session with a feature left in "in_progress" — resolve to "complete" or "blocked".
- Each feature must get its own git commit before the session ends.
- One feature per session — do not start a second feature after the first is resolved.
```

---

## `jumploop` Prompt

> Use when you want to implement multiple features in a single session without manual intervention. Invoke as `jumploop --n` where `n` is the number of features to complete.

```
You are a coding agent resuming work on an ongoing project. You will implement
multiple features in this session — up to [N] features total.

START OF SESSION — do these steps in order:
1. Run `pwd` to confirm your working directory.
2. Read `progress.txt` — focus on the most recent session entry.
3. Run `git log --oneline -20` to review recent commits.
4. Run `init.sh` to start the dev server and confirm there is no broken build.
   If it IS broken, fix the regression before starting new work.
5. Read `feature_list.json`. Choose the highest-priority feature with status "not_started".
   Prefer features that unblock other features.

FEATURE LOOP — repeat until you have completed [N] features or no "not_started" features remain:
1. Set the chosen feature's status to "in_progress".
2. Plan the implementation. Do NOT ask for user approval — proceed immediately.
3. Implement the feature.
4. Verify the feature works. Prefer inspecting the DOM or reading server output
   over opening a browser URL.
5. When verified, set status to "complete" and commit immediately:
   `git add -A && git commit -m "feat([id]): [feature name] — [brief summary]"`
6. If you hit a hard blocker, set status to "blocked", commit, document the reason
   in "notes", and move on to the next feature — do not stop the loop.
7. Pick the next highest-priority "not_started" feature and repeat.

CHECKPOINTS:
- If the next item is a checkpoint ("type": "checkpoint"), the loop MUST stop
  regardless of how many features remain in the budget.
- Present the checkpoint's "verify" list to the user and ask them to confirm
  everything looks good.
- Set the checkpoint's status to "awaiting_review" and end the session.
- The user will mark it "complete" (or provide feedback) before the next session.
- Checkpoints do NOT count toward the [N] feature budget.

RULES:
- Plans always proceed — never pause to ask for user review or approval.
- Complete up to [N] features, but stop early if all remaining features are
  "complete", "blocked", or "deferred", or if a checkpoint is reached.
- NEVER remove or edit a feature's description or steps — only update status and notes.
- NEVER mark a feature "complete" without having verified it.
- Always leave the codebase in a mergeable state after each commit.
- Never leave a feature in "in_progress" — resolve to "complete" or "blocked"
  before moving to the next feature.
- Each feature must get its own git commit.

END OF SESSION — after all features are resolved, do these final steps:
1. Append to progress.txt:
   - Date and session number
   - For each feature worked on: feature ID, description, and final status
   - Any bugs found and whether they were fixed
   - Blockers or open questions
   - Total features completed / attempted
   - If stopped at a checkpoint: checkpoint ID and verify list
   - Recommended next feature for the following session
2. Stop.
```

---

## `jumpfree` Prompt

> Use for ad-hoc sessions where the objective is defined by immediate user input rather than the pre-planned feature list.

```
You are a coding agent resuming work on an ongoing project.

START OF SESSION — do these steps in order:
1. Run `pwd` to confirm your working directory.
2. Read `progress.txt` — focus on the most recent session entry.
3. Run `git log --oneline -20` to review recent commits.
4. Run `init.sh` to start the dev server and confirm there is no broken build.
   If it IS broken, fix the regression before starting new work.
5. Review the user's specific request for this session.

DURING YOUR SESSION:
- Focus solely on fulfilling the user's specific request.
- Implement, then verify the work. Prefer inspecting the DOM or reading server
  output over opening a browser URL — do not let an inability to open a URL block you.
- When verified, commit immediately:
  `git add -A && git commit -m "feat(jumpfree): [brief summary of work done]"`

END OF SESSION — after committing the work, do these final steps:
1. Append to progress.txt:
   - Date and session identifier (e.g. jumpfree)
   - Ad-hoc task worked on and its final status
   - Any bugs found and whether they were fixed
   - Blockers or open questions
   - Recommended next feature for the following session (optional)
2. Stop. Do not begin additional unsolicited work.

RULES:
- Always leave the codebase in a mergeable state — no broken builds.
- The work must get its own git commit before the session ends.
```

---

## `feature_list.json` Format

```json
[
  {
    "id": "feat-001",
    "category": "functional",
    "description": "User can open the app and see a welcome screen with a prompt to log in",
    "steps": [
      "Navigate to http://localhost:3000",
      "Verify the page loads without console errors",
      "Verify a welcome message is visible",
      "Verify a login button or link is present"
    ],
    "status": "not_started",
    "notes": ""
  },
  {
    "id": "checkpoint-001",
    "type": "checkpoint",
    "description": "Core UI shell complete — all base components and layouts are implemented",
    "verify": [
      "App loads without errors",
      "All pages are reachable via navigation",
      "Components render correctly across viewport sizes",
      "Visual design matches UX_DESIGN.md intent"
    ],
    "status": "not_started",
    "notes": ""
  }
]
```

### Entry Types

| Field | Feature entry | Checkpoint entry |
|---|---|---|
| `id` | `feat-NNN` | `checkpoint-NNN` |
| `type` | *(absent or `"feature"`)* | `"checkpoint"` |
| `description` | What the feature does | What milestone was just reached |
| `steps` / `verify` | `steps` — verification steps | `verify` — items for a human to check |
| `status` | See status table | See status table |
| `notes` | Agent observations | Human feedback |

### Status Values

| Status | Meaning |
|---|---|
| `not_started` | Default. No work has begun. |
| `in_progress` | Actively being worked on in the current session. Never persist this across sessions. |
| `complete` | Implemented and verified end-to-end. Do not revisit unless a regression is found. |
| `blocked` | Cannot proceed — dependency missing, design unclear, or unresolvable bug. Document reason in notes. |
| `deferred` | Intentionally postponed by agreement. Document reason in notes. |
| `awaiting_review` | Checkpoint only. Human review requested — agent must stop and wait. |

**Key rules:**
- JSON only (not Markdown) — models are less likely to accidentally overwrite JSON
- Agents may only change `status` and `notes` — never `description` or `steps`/`verify`
- `in_progress` must never persist across sessions — end each session with `complete` or `blocked`
- Checkpoints gate progress — agents must not skip past an `awaiting_review` or `not_started` checkpoint

---

## `progress.txt` Format

```
PROJECT: [Name]
Started: [Date]

---

Session 0 — [Date]
Initialization complete. feature_list.json generated with 87 features.

---

Session 1 — [Date]
Worked on: feat-001 (User welcome screen)
Status: complete
Summary: Implemented the landing page with login CTA. Verified via Puppeteer — page loads, welcome text visible, login button present.
Bugs fixed: None.
Blockers: None.
Next session: feat-002 (Login form submission)

---
```

---

## Session Startup Checklist (Quick Reference)

```
[ ] pwd
[ ] Read progress.txt (latest entry)
[ ] git log --oneline -20
[ ] Run init.sh
[ ] Smoke test — is the app healthy?
[ ] (jumpsession only) Read feature_list.json → pick 1 "not_started" feature
[ ] (jumpsession only) Set feature to "in_progress"
[ ] (jumploop only) Read feature_list.json → begin feature loop (up to N features)
[ ] (jumploop only) Plans always auto-proceed — no user approval needed
[ ] (jumpfree only) Review user's ad-hoc request
[ ] Implement → verify (DOM/server output preferred over opening URL) → set to "complete" or "blocked"
[ ] git add -A && git commit (per task, immediately after resolving)
[ ] Append to progress.txt
[ ] (jumpsession/jumpfree) Stop — do not begin a second feature/task
[ ] (jumploop) Stop after N features completed or no features remain
```
