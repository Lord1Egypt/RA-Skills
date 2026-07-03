---
load: on demand — when diagnosing a specific illegibility pattern
parent: ../SKILL.md
---

# Jargon Categories — Six Failure Modes

Every illegible agent output falls into one of these six buckets. Use this taxonomy to diagnose quickly, then apply the matching transform from `examples/before-after.md`.

## 1. Bare codes and identifiers

The agent surfaces an internal ID, ticket number, hash, or framework-generated string as the headline.

**Examples:**
- `T-A127`, `task_id=42`, `commit a3f9c12`, `hunk:42`, `step_3`, `cycle 2`
- `mvs_3f0906ef83964e6992560315920ff4d0` (session IDs)
- `req-7e3a-9b21-...` (request IDs)

**Why it fails:** Identifiers are random from the user's perspective. They cannot be memorized, decoded, or used to take action.

**Transform:** Move the ID to parentheses after a plain-language description. If there is no plain-language description, write one.

---

## 2. Raw error strings

The agent forwards an OS-level error, library exception, or HTTP status code without translation.

**Examples:**
- `Error: EBADF: bad file descriptor`
- `ENOENT: no such file or directory`
- `HTTP 502 Bad Gateway`
- `TypeError: cannot read property 'id' of undefined`
- `pd.read_csv() raised ParserError: ...`

**Why it fails:** The user has no mental model for these strings. They cannot tell whether to retry, change input, or contact support.

**Transform:** Translate to a sentence containing (a) what the user was trying to do, (b) what went wrong in their language, (c) what they should do next.

---

## 3. Framework / infrastructure vocabulary

The agent uses words that exist in the agent's documentation but not in the user's vocabulary.

**Examples:**
- `cycle`, `phase`, `hunk`, `dispatch`, `verifier`, `handoff`, `subagent`
- `asyncio.gather`, `await Future.result()`, `pandas chunk`
- `diff`, `patch`, `rebase`, `worktree`, `squash`
- `mavis`, `session`, `worker pool`, `correlation ID`

**Why it fails:** These are jargon for the agent's authors. To the user they are noise that looks like information.

**Transform:** Replace with the user-visible equivalent. If the framework concept has no user-visible equivalent, decide whether the user needs to see it at all — usually they do not.

---

## 4. Vague corporate / phase language

The agent labels work with abstract process words that sound professional but mean nothing specific.

**Examples:**
- `Phase 2: post-merge validation processing`
- `Step 3: operationalizing the framework`
- `Initiating cross-functional alignment`
- `Running pre-flight checks`
- `Optimizing the workflow`

**Why it fails:** These phrases pass the "sounds like work" test but fail the "tells you what is happening" test. They are indistinguishable from each other.

**Transform:** Replace with a concrete verb + concrete object. If you cannot name a concrete object, you have not decomposed the task enough.

---

## 5. Numbers without units or context

The agent emits percentages, counts, or durations that have no referent.

**Examples:**
- `Progress: 23%` (of what?)
- `Processed 1247 records` (so what?)
- `Latency: 142ms` (compared to what? acceptable?)
- `Memory: 487MB` (good? bad?)
- `ETA: 4m` (until what?)

**Why it fails:** Without a denominator or threshold, the number cannot be interpreted as good or bad, fast or slow, done or not done.

**Transform:** Always pair the number with its denominator or with a sentence that interprets it. `Processed 1247 of 5000 records (25%)` is legible; `1247 records` is not.

---

## 6. Invisible state, visible only to the agent

The agent describes what it is *doing internally* rather than what the user can *observe*.

**Examples:**
- `Awaiting Future.result() from worker pool`
- `Applying patch from diff hunk @src/services/foo.ts:42`
- `Serializing response payload`
- `Acquiring asyncio lock`
- `Calling GitHub API`

**Why it fails:** The user cannot see any of this. Reporting it makes the agent feel busy without making the user feel informed.

**Transform:** Report the visible effect instead. "Saving your changes", "Uploading the file to the server", "Waiting for the analysis to finish". If the user really needs to know the internal mechanism, do it as a parenthetical footnote, never as the headline.

---

## Diagnostic flow

When you suspect illegibility, walk these in order:

1. Does the headline contain a code/ID? → Category 1
2. Does it contain an error string? → Category 2
3. Does it contain a word from the framework docs? → Category 3
4. Does it contain abstract process words? → Category 4
5. Does it contain numbers without context? → Category 5
6. Does it describe internal plumbing? → Category 6

A single output can fail multiple categories — apply the transforms in order and re-check.
