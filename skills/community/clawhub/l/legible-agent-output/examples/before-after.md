# Before / After — Worked Transformations

Thirty real-world transformations, grouped by the failure-mode taxonomy in `references/jargon-categories.md`. Use these as the muscle-memory reference when applying the skill.

## Category 1 — Bare codes and identifiers

| # | Before | After | Why |
|---|---|---|---|
| 1 | `T-A127: run ingest` | `Ingest weekly sales data (T-A127)` | Code moved to parenthetical; plain description is now the headline. |
| 2 | `task_id=42 failed` | `Photo upload failed (request #42)` | "task_id" replaced with "request"; the description says what the user was doing. |
| 3 | `step_3 complete` | `Sent the welcome email` | Internal step number replaced with the actual outcome. |
| 4 | `commit a3f9c12 deployed` | `Deploy is live (commit a3f9c12)` | "Deployed" said twice; replaced with "deploy is live" + hash in parens. |
| 5 | `Cycle 2 dispatch complete` | `Second review pass scheduled` | "Cycle 2 dispatch" → "second review pass"; user never needed the framework term. |

## Category 2 — Raw error strings

| # | Before | After | Why |
|---|---|---|---|
| 6 | `Error: EBADF: bad file descriptor` | `Couldn't read the file because it was already closed — please try again` | Translated to a sentence; added a remediation. |
| 7 | `ENOENT: no such file or directory, open '/tmp/profile.jpg'` | `Profile photo is missing — pick a new one to upload` | Named the user-visible file ("profile photo") and gave the next action. |
| 8 | `HTTP 502 Bad Gateway` | `Our upload service is temporarily down — please retry in a minute` | HTTP status translated; retry guidance added. |
| 9 | `TypeError: cannot read property 'id' of undefined` | `Something went wrong loading the order details — please refresh the page` | Stack-style error replaced with a user-visible symptom + action. |
| 10 | `pd.read_csv() raised ParserError: ...` | `Spreadsheet has a formatting problem on row 142 — fix the date column and re-upload` | Library + exception stripped; named the actual file row the user can edit. |

## Category 3 — Framework / infrastructure vocabulary

| # | Before | After | Why |
|---|---|---|---|
| 11 | `Verifying handoff protocol` | `Checking the handover is complete` | "Verifying handoff protocol" → English. |
| 12 | `Awaiting asyncio.gather coroutine completion` | `Waiting for the parallel tasks to finish` | asyncio vocabulary replaced with the observable effect. |
| 13 | `Squashing commits before rebase` | `Cleaning up the change history before merging` | Git jargon replaced with intent. |
| 14 | `Spawning subagent for verifier phase` | `Running an independent review` | Framework nouns replaced with user-visible purpose. |
| 15 | `mavis team plan cycle 2 — verifier rejected` | `The reviewer asked for changes` | Tool name stripped; rejection translated to user action. |

## Category 4 — Vague corporate / phase language

| # | Before | After | Why |
|---|---|---|---|
| 16 | `Phase 2: post-merge validation processing` | `Testing the merged build runs correctly` | "Phase 2" dropped; "validation processing" replaced with one concrete verb + object. |
| 17 | `Operationalizing the workflow` | `Setting up the automated steps` | Replaced an abstract noun with a verb. |
| 18 | `Running pre-flight checks` | `Checking the inputs are valid before starting` | "Pre-flight checks" is a metaphor; replaced with the literal action. |
| 19 | `Optimizing the workflow` | `Making the report run faster` | Concrete outcome ("run faster") instead of abstract verb ("optimizing"). |
| 20 | `Initiating cross-functional alignment` | (delete entirely — this was nonsense) | Some output is illegible because the agent has not done the work yet. Better to delete than to translate. |

## Category 5 — Numbers without units or context

| # | Before | After | Why |
|---|---|---|---|
| 21 | `Progress: 23%` | `Processed 23 of 100 files (23%)` | Denominator added; user can now judge whether to wait. |
| 22 | `Memory: 487MB` | `Using 487 MB of memory — within normal range` | Number paired with interpretation. |
| 23 | `Latency: 142ms` | `Page loaded in 142 ms (target: under 200 ms)` | Number paired with threshold; user knows it's fine. |
| 24 | `ETA: 4m` | `About 4 minutes left to import your contacts` | ETA paired with the user-visible work in progress. |

## Category 6 — Invisible state

| # | Before | After | Why |
|---|---|---|---|
| 25 | `Awaiting Future.result() from worker pool` | `Waiting for the analysis to finish` | Internal future/wait replaced with user-visible effect. |
| 26 | `Applying patch from diff hunk @src/services/foo.ts:42` | `Updating the user-profile service` | Internal file path dropped; user-visible subsystem named. |
| 27 | `Serializing response payload` | `Packaging the data to send back` | Library term replaced with intent. |
| 28 | `Calling GitHub API` | `Checking your repositories on GitHub` | Infrastructure call replaced with the user-visible purpose. |
| 29 | `Acquiring asyncio lock` | `Waiting for the previous step to finish` | Concurrency detail dropped; user-visible wait state reported. |
| 30 | `Pre-commit hook failed on file X` | `A formatting check on your code found an issue — see line 12 of file X` | "Hook" replaced with "formatting check"; failure connected to the action the user can take. |

## Composite case (multi-category rewrite)

**Before:**
```
Cycle 3 verifier rejected task T-B42 (hunk:42) with EBADF on /tmp/upload.jpg.
Step_4 retried 3x. Progress: 12%. ETA: 7m.
```

**After:**
```
The photo upload review found a problem (request T-B42):
the file had already been closed before we could read it.
We've retried 3 times. About 7 minutes left to finish processing your 100 photos (currently 12 done).
```

Five categories collapsed into one paragraph a non-technical user can act on. The internal IDs are preserved in parentheses for the technical user; the user-visible story is in the body.
