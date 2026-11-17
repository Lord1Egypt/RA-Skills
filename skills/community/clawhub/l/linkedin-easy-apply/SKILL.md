---
name: "linkedin-automation-login"
description: "LinkedIn job-sprint automation — verify/refresh login in the dedicated Playwright profile, then run the Easy Apply automation. Use when resuming or starting a LinkedIn application sprint."
metadata:
  openclaw:
    primaryEnv: ANTHROPIC_API_KEY
    expectedRuntimeVersion: "1.0.11"
    expectedRuntimeSha256: "289e1abf49a1478d26b457c79fa0dff9d4b43b9cb9fce4054a6ac06a3de6e16e"
    expectedCliSha256: "b7ce43afce06e31669e6518b856bdb807887e3ba41d32bb975e8e0408eb8ce4d"
    requires:
      env: [ANTHROPIC_API_KEY]
      bins: [python]
    envVars:
      - name: LINKEDIN_AUTOMATION_RUNTIME_DIR
        required: false
        description: Path to the separately installed linkedin-automation Python runtime (the folder containing cli.py). If unset, checked at the default path below.
      - name: ANTHROPIC_API_KEY
        required: true
        description: Used by the runtime to answer open-ended Easy Apply questions, grounded in your resume
      - name: CHROME_PROFILE_DIR
        required: false
        description: Persistent Chrome/Playwright profile dir (login session, cookies). Defaults to ~/.openclaw/workspace/.playwright-profile
      - name: APPLICATION_LOG_PATH
        required: false
        description: Path to the JSON application log/dedup store. Defaults to ~/.openclaw/workspace/applications/application-log.json
      - name: SEARCH_QUERIES
        required: false
        description: Comma-separated LinkedIn search queries to rotate through
      - name: SEARCH_LOCATION
        required: false
        description: LinkedIn location filter (e.g. "United States", "Canada", "Remote")
      - name: SEARCH_TIME_RANGE
        required: false
        description: LinkedIn "date posted" filter — "day", "week" (default), or "month"
      - name: BANNED_COMPANIES
        required: false
        description: Comma-separated company names to never apply to
      - name: AUTO_CONNECT_HIRING_TEAM
        required: false
        description: Set to "false" to skip sending connection requests to the hiring team after a successful submission
      - name: RESUME_TEXT
        required: false
        description: Full resume text, pasted directly. Falls back to a generic bundled example if unset.
      - name: SYSTEM_PROMPT_TEXT
        required: false
        description: Full custom instructions for the runtime's answer-generation step (how it should phrase Easy Apply answers), pasted directly in place of the default template.
---

# LinkedIn Automation: Login + Easy Apply

## What this does

Automates a LinkedIn Easy Apply job-application sprint end to end: verifies (or refreshes)
login in a dedicated Playwright/Chrome profile, searches LinkedIn by your criteria, fills
and submits Easy Apply forms — answering open-ended questions with an LLM grounded in your
resume — logs every outcome so re-runs never double-apply, and optionally sends connection
requests to each job's hiring team after a successful submission.

## When to use this skill

Use it whenever the user asks to resume, start, or check status of a LinkedIn application
sprint, or to verify/refresh the automation's LinkedIn login. Do not attempt to reimplement
this workflow (browser automation, selector logic, application dedup, daily-limit
detection) yourself — always invoke the installed runtime described below. This skill's
package intentionally ships no implementation code; the working automation lives in a
separately installed Python runtime, and reproducing its logic ad hoc will not match its
tested behavior (dedup rules, retry rules, daily-limit handling, etc.).

## Locating the installed runtime

This skill's package (`{baseDir}`) contains no automation code — only this file and
`{baseDir}/references/README.md`. The actual automation is a separately distributed Python
runtime, set up ahead of time by the user via the steps in that reference file. Locate it
in this order:

1. `$LINKEDIN_AUTOMATION_RUNTIME_DIR`, if set.
2. The default path: `~/.openclaw/workspace/linkedin-automation-runtime/`.

A `cli.py` file existing at a candidate location is a shape check, not authorization to run
it. Before invoking anything, perform both of these checks at that location, every time —
not just once per session:

1. Read `VERSION` next to `cli.py` and compare it to `expectedRuntimeVersion` in this file's
   frontmatter (`1.0.11`).
2. Compute the SHA-256 of `cli.py` itself and compare it to `expectedCliSha256` in this
   file's frontmatter (`b7ce43afce06e31669e6518b856bdb807887e3ba41d32bb975e8e0408eb8ce4d`) — **not** to any file sitting next to `cli.py`.
   A hash generated from whatever `cli.py` happens to be present at install time proves
   nothing (an attacker who supplies a malicious `cli.py` before that baseline is created
   can supply a matching sidecar hash too); `expectedCliSha256` is instead computed once at
   build time from the reviewed source and embedded in this file, so it comes from the same
   independently-published, reviewed channel as `expectedRuntimeSha256` below, not from the
   runtime directory being validated.

- **Both match** → use this runtime.
- **Either is missing, or either doesn't match** → **stop and tell the user**, fail closed.
  Do not proceed anyway, do not silently accept a newer or older runtime, and do not fall
  back to reading the individual `.pyc` files to guess compatibility. Tell them either to
  install the version this skill expects (`{baseDir}/references/README.md`, including its
  checksum-verification step) or that this skill needs to be rebuilt/updated to declare
  support for the runtime version they have installed.

Note what each check does and doesn't prove: `VERSION` is a plaintext file the installed
runtime reports about itself — a match proves it *claims* to be the expected release, not
that its contents are what was published. `expectedCliSha256` re-verifies `cli.py` (the file
this skill directly executes) against a value pinned in the reviewed skill package itself,
on every invocation, not just once at install time — so a `cli.py` modified after install
(by malware, a faulty update, etc.) is caught before it runs, and the expected value can't be
forged by whoever controls the runtime directory. It still only covers `cli.py`, not every
module/dependency the runtime imports; the archive-level integrity guarantee for the full
runtime tree is `expectedRuntimeSha256` in this file's frontmatter (`289e1abf49a1478d26b457c79fa0dff9d4b43b9cb9fce4054a6ac06a3de6e16e`),
checked once by the user at install time per `{baseDir}/references/README.md` against the
downloaded archive — compared there against *two* independent copies of the digest (the
`.sha256` file published next to the archive, and this value embedded in SKILL.md, which is
reviewed and distributed through a separate channel). If a user reports installing a runtime
whose archive digest didn't match either published value, treat that as a
compromised-supply-chain report, not a support request — stop and tell them not to proceed,
don't troubleshoot around it.

If no runtime is found at either candidate location at all, **stop and tell the user**.
Point them at `{baseDir}/references/README.md` for setup, and at
`LINKEDIN_AUTOMATION_RUNTIME_DIR` to tell this skill where they put it (or leave it at the
default path above). Do not substitute your own approach for locating, obtaining, or
standing up the runtime — this skill only ever drives an already-prepared, version-matched
installation.

Once located, every command below is: `python "<runtime_dir>/cli.py" <subcommand> [args]`.

## Inputs

All inputs are environment variables — see the `envVars` list in this file's frontmatter
for the full set. `ANTHROPIC_API_KEY` is required; everything else has a working default.

## Invoking the runtime

1. **Check login (fast, no browser):**
   `python "<runtime_dir>/cli.py" login-check`
   Output: prints exactly `logged_in` or `needs_login` on stdout.

2. **If `needs_login`, log in interactively:**
   `python "<runtime_dir>/cli.py" login`
   Opens a real Chrome window on the automation profile and waits (up to 5 minutes) for
   the user to finish logging in (including 2FA). Tell the user the window is open and
   wait for the process to exit — do not poll or interrupt it.

3. **Verify:**
   `python "<runtime_dir>/cli.py" verify`
   Output: prints `verified` on success, or `not_verified url=... title=...` on failure.

4. **Smoke test (real browser, submits nothing):**
   `python "<runtime_dir>/cli.py" smoke`
   Run before trusting a real sprint. Prints progress lines ending in either
   `SMOKE TEST PASSED — ...` or an `AssertionError` describing what failed (not logged in,
   or the scraper found zero candidates).

5. **Run a sprint:**
   This submits real job applications (and, unless `AUTO_CONNECT_HIRING_TEAM=false`, sends
   real connection requests) on the user's behalf using an externally distributed runtime
   this skill package does not contain the source of — get explicit confirmation from the
   user for this specific invocation before running it (not a one-time blanket "yes" earlier
   in the conversation), stating how many applications (`N`) will be submitted.
   `python "<runtime_dir>/cli.py" run [N] [--scan-per-page N] [--max-scan N] [--force]`
   `N` is the number of applications to submit this call (default 1), checked against
   **today's** successful submissions only (not a lifetime total) — pass `--force` to run
   anyway if today's target already looks reached. Invoke once per call — this automation
   schedules itself externally at randomized intervals and must not be looped internally,
   to avoid LinkedIn bot-detection.

## Output format

Every subcommand prints human-readable progress lines to stdout and exits 0 on success,
non-zero on failure (an unhandled exception, or an `AssertionError` from `smoke`). There is
no structured JSON output — read the printed lines directly. `run` additionally persists
every outcome (submitted / skipped / already-applied / blocked) to the JSON log at
`$APPLICATION_LOG_PATH`, which downstream tooling can read for a structured summary.

## Handling failures

- Non-zero exit + login-related text (`NOT LOGGED IN`, redirected to `/login`) → session
  expired; run `login` again, then retry.
- `smoke` fails with zero candidates found → possible stale LinkedIn selectors on the
  runtime's end; this needs a runtime rebuild/update, not a workaround here — report it to
  the user rather than trying to patch around it.
- `run` stops cleanly citing a daily submission limit → expected LinkedIn behavior, not an
  error; tell the user to resume tomorrow.
- Any other non-zero exit → surface the printed error text to the user verbatim; do not
  guess at a fix or attempt to edit the runtime.
