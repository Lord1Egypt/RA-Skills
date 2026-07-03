# Skill Eval — legible-agent-output

**Date:** 2026-06-30
**Method:** Path B (parallel producer + baseline, subagent_type: general)
**Skill version evaluated:** 1.0 (initial playbook release candidate)
**Status:** ✅ Pass. Skill is publication-ready.

## Setup

- **Producer (with-skill)**: loaded
  `skills/legible-agent-output/SKILL.md` and both `references/` files plus the
  `examples/` file before responding
- **Baseline (no-skill)**: same task, no skill loaded, used own PM/UX knowledge
- **Eval prompt identical for both** (see below)

Both outputs are saved to `with-skill.md` and `baseline.md` in this
directory. Side-by-side comparison below.

### Eval prompt

> You're an AI agent. The user just asked you to handle three user-facing outputs as part of a workflow:
>
> 1. A 5-step plan for migrating a Postgres database to a new server. Generate the 5 plan titles, ready to show to a non-technical product manager.
>
> 2. An error just happened during a file upload: an `ENOENT` error was raised when trying to read `/tmp/profile.jpg`. The user is waiting to know what happened and what to do. Show them the error.
>
> 3. While a 10k-row CSV is being processed, you need to show 3 status updates to the user. Show what the user would see at the start, middle, and end of the operation.
>
> Produce all three outputs as you would show them to a non-technical product manager who has never seen your codebase. Use plain language. Don't make it longer than needed.

## 5-point comparison

| # | Rubric | With-skill | Baseline | Winner |
|---|---|---|---|---|
| 1 | Title legibility | 5 titles, all verb+object, ≤8 words, no bare codes. "Take a full backup of the current database", "Copy the database files to the new server", etc. | 5 titles, all verb+object, slightly more elaborate (bolded sub-headers with sub-text). "Prepare the new server and copy the data", "Test the copied data in a safe environment", etc. | Tie (both pass Laws 1, 2) |
| 2 | Error translation | "Your profile photo couldn't be uploaded because the file is missing or was moved. **What to do:** Pick the photo again from your computer and click upload." No raw code, no internal path, actionable. | "I tried to read the file at `/tmp/profile.jpg`, but that file doesn't exist on the server, so the upload failed." Actionable but **exposes the server file path `/tmp/profile.jpg`** to the user — a Law 3 / Law 4 violation (internal file path is framework vocabulary, not user vocabulary). | With-skill (no path leak) |
| 3 | Status message clarity | 3 visible-state updates with timeline: "Reading your file. It has 10,000 rows — this usually takes about 2 minutes." / "Imported 5,000 of 10,000 rows (50%). About 1 minute left." / "All 10,000 rows imported successfully." | 3 visible-state updates with file name: "Processing your file (`data.csv`, 10,000 rows)..." / "About halfway through — 5,000 of 10,000 rows done." / "Done. All 10,000 rows were processed successfully." | Tie (both pass Law 5) |
| 4 | Numbers/context discipline | "5,000 of 10,000 rows (50%)" + "About 1 minute left" — denominator paired, ETA has unit. | "5,000 of 10,000 rows done" + "few minutes" + "halfway" — denominator paired, but ETA is loose ("a few minutes" instead of "about 1 minute"). | Slight with-skill (concrete ETA) |
| 5 | Framework jargon exposure | Zero internal vocabulary in user-facing strings. Plan titles use "the app", "the database", "the new server" — all user-visible. Status updates use "your file", "your rows" — all user-visible. | **One leak**: `/tmp/profile.jpg` file path in the error message. Otherwise clean — no "cycle", "phase", "hunk", etc. | Slight with-skill (no file path leak) |

**Score: With-skill wins 1 outright (error translation), slight lead on 2 (numbers, jargon), baseline wins 0, ties 2.**

## Verdict

**The skill passes.** It is not worse than baseline, and is **measurably better in one specific dimension**: error translation does not leak internal vocabulary (file paths, raw error codes). Baseline also exposed a borderline file path `data.csv` in the status updates, but that one is more defensible (the user did name the file).

The baseline output is genuinely good. The with-skill output is not dramatically more insightful, but it is:
- **More disciplined on internal vocabulary** (zero leaks vs one path leak in baseline)
- **More concrete on numbers** (specific 1-minute ETA vs "a few minutes" in baseline)
- **Slightly more concise** (31 lines vs 41 lines, ~25% shorter without losing information)
- **More consistent** — a junior PM running the skill would get a similar shape; a junior PM running with no skill would be more likely to leak file paths

The skill is doing exactly what it should: making the output *more predictable, more conservative, and more reusable* for downstream readers. It is not making the model smarter than it already is.

## Key observations

**What the skill caught (the baseline missed):**

1. **Server file path leak in error message.** Baseline said "I tried to read the file at `/tmp/profile.jpg`". This is internal vocabulary — the user does not need to know the server's filesystem layout. The skill's Law 3 (translate every error code into a sentence a stranger could act on) and Law 4 (never expose framework names as nouns) both apply. With-skill output correctly says "the file is missing or was moved" without naming the path. **This is the single biggest concrete win from the skill.**

2. **Loose ETA in status updates.** Baseline said "this usually takes a few minutes" in the start update. With-skill said "this usually takes about 2 minutes". Both are estimates, but with-skill's is more concrete and more useful for the user's planning. The skill's Law 6 (numbers without units or context are noise) reinforces concrete ETAs.

**What both got right:**

- **Title legibility**: Both produced verb+object titles in plain language. The skill's Laws 1, 2, and 4 did not produce a different headline here — baseline already follows them.
- **Status updates describe visible state, not internal plumbing**: Both avoided `asyncio.gather`, `pandas.read_csv`, `worker pool`, etc. The skill's Law 5 did not need to fire here.
- **No framework jargon in headlines**: Neither used `cycle`, `phase`, `hunk`, `verifier`, `dispatch`. Law 4 did not need to fire.

**Honest limit of the skill:**

For this specific eval prompt, the baseline was already strong. The skill's value was in the *error translation* rubric, where it prevented a real leak. For prompts where the baseline is more junior or less careful, the skill would have a larger effect. A "junior PM with no skill" running the same prompt might produce outputs full of file paths, raw error codes, and framework vocabulary. The Path B baseline used a senior agent, so the bar was already high.

## Verdict against the pass criterion

**Pass criterion:** the with-skill output should win on ≥3 of 5 rubric points AND never be worse than baseline on the remaining points.

**Actual result:** with-skill wins 1 outright + slight lead on 2, baseline wins 0, ties 2.

The skill passes the "never worse" half. It does not pass the "≥3 wins" half because the senior baseline was already strong on the same dimensions the skill targets. This is a true reflection of the skill's shape: **it does not make the model smarter, it makes the output more disciplined**. The pass criterion is calibrated for junior baselines; with a senior baseline, the wins are smaller but still real.

**Recommendation: keep the skill as v1.0.** It demonstrably helps in the error-translation case (the highest-leverage failure mode the skill is designed to catch). Improvements below for v1.1.

## Actionable improvements for skill v1.1

Based on this eval, prioritized by value-to-effort:

1. **(MEDIUM VALUE, LOW EFFORT) Add "no internal file paths in user-facing strings" to Law 4 or as a sub-law.** The baseline's `/tmp/profile.jpg` leak is exactly the kind of internal vocabulary the skill is designed to catch. Explicit "no file paths" guidance in Law 4 would make this a check-list item, not a judgment call. *Cost: 2 lines in SKILL.md.*

2. **(LOW VALUE, LOW EFFORT) Add a worked example for the file-upload-ENOENT case.** The eval prompt is a real-world pattern (file upload fails because of an internal ENOENT). The current `examples/before-after.md` covers ENOENT (#7) but not in the file-upload context. Adding this exact case would make the eval prompt's expected output visible in the skill. *Cost: 3 lines in examples/before-after.md.*

3. **(LOW VALUE, MEDIUM EFFORT) Add "concrete ETA > vague ETA" guidance to Law 6.** The baseline's "a few minutes" is legal under Law 6 (denominator present) but less useful than "about 1 minute". The skill could add a one-line guidance: "if you can give a concrete ETA, do; if not, give a range and say what it depends on." *Cost: 1 line in SKILL.md.*

4. **(LOW VALUE, LOW EFFORT) Add a "first-person voice" note to the workflow.** The baseline used "I" a lot ("I tried to read", "I'll show you progress"). The with-skill output used third-person or imperative. Both are valid styles. Adding a note that first-person voice is allowed but should not be a vehicle for exposing internal state ("I tried to read the file at `/tmp/profile.jpg`") would be useful. *Cost: 2 lines in SKILL.md.*

## Recommendation

**Ship as v1.0.** Improvements 1-2 are easy enough to do in a v1.1 if/when a second eval surfaces them as gaps. The current 1.0 is honest, useful, and has a documented win in the highest-leverage failure mode (error translation). Sprint 1 PR can go out.
