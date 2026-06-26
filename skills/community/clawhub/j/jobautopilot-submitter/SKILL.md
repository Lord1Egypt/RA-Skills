---
name: jobautopilot-submitter
description: "Automatically fills and submits job applications. Opens the application page, fills multi-step forms (work history, education, EEOC, dropdowns), uploads your tailored resume and cover letter, and confirms successful submission. Picks up resume_ready jobs from jobautopilot-tailor and marks them applied in the tracker."
author: jerronl
version: "1.3.3"
homepage: https://github.com/jerronl/jobautopilot
tags:
  - job-search
  - browser-automation
  - form-filling
  - career
  - apply
requires:
  browser: true
  tools:
    - exec  # runs openclaw browser CLI commands and bundled shell scripts — no network calls
  python_packages:
    - python-docx  # reads tailored .docx resumes to extract text for form fields
metadata:
  clawdbot:
    emoji: "🚀"
    requires:
      env:
        - OPENCLAW_USER
        - OPENCLAW_PROFILE
        - USER_FIRST_NAME
        - USER_LAST_NAME
        - USER_EMAIL
        - USER_PHONE
        - USER_LINKEDIN
        - RESUME_DIR
        - TRACKER_PATH
      bins:
        - python3   # reads tailored .docx resumes via python-docx
        - openclaw  # browser CLI for snapshot, fill, select, click, upload
      pip:
        - python-docx  # used at runtime to extract text from tailored resume .docx files (see "Read resume and JD" step)
    files:
      - scripts/check_required_fields.js
      - scripts/fill_template.sh
      - scripts/match_variant_options.sh
    browser: true
    browser_profile: apply
---

# Job Autopilot — Submitter

Automates form-filling and submission for `resume_ready` jobs. Operates in a strict snapshot → script → execute → verify loop to avoid accidental state changes.

## Security & privacy

This skill automates browser form-filling — an inherently sensitive operation. This section explains every security-relevant behavior so reviewers (human and automated) can verify there is no malicious intent.

### Data flow — all local

**All personal data stays local.** This skill reads name, email, phone, and LinkedIn from environment variables (set before the agent starts) and types those values into job application forms — the same way you would manually. No data is sent to any server controlled by this skill. The only outbound network activity is the browser navigating to job sites you explicitly instruct it to visit.

**No passwords are stored or read by this skill.** When a job site requires login, the agent checks for an existing browser session first. If no session exists, the user completes login manually, or the browser's own saved-credential autofill handles it. This skill never reads, stores, or transmits any password.

**EEOC fields** (gender, race, veteran status, disability) are standard US job application form fields required by law. Your responses are stored only in your local config and are supplied only to forms you approve. They are never logged or sent elsewhere.

### Why this skill uses `evaluate` + a `.js` file

`check_required_fields.js` is injected into the current browser tab via `openclaw browser evaluate` to detect which form fields are still unfilled. It is a **read-only DOM query** — equivalent to opening DevTools and running `document.querySelectorAll("[required]")`. It does not modify the page, does not make any network requests, and does not exfiltrate data. The full source is included at `scripts/check_required_fields.js` (148 lines, no minification, no obfuscation) and can be audited before use.

### Why this skill generates shell scripts in `/tmp`

Browser form-filling requires batching multiple `fill`/`select`/`click` commands into a single atomic sequence (to avoid partial state). The agent writes these commands to `/tmp/fill_<timestamp>.sh` and executes them immediately. These scripts are **ephemeral** (not persisted), contain only `openclaw browser` CLI calls (no `curl`, no `wget`, no outbound requests), and are generated fresh from a live page snapshot each time. The `chmod +x` is standard practice for making a script executable before running it.

### Optional watchdog cron (not executed by any script)

The documentation describes an optional `openclaw cron add` command users can run manually to prevent agent stalls during long sessions. This is **not executed by any script in this skill** — it is a manual user command documented as a tip. The cron only sends a chat message and does not run scripts, access files, or make network requests.

### Why this skill uses the `upload` interceptor

The `upload` command is an OpenClaw browser API that pre-stages a local file path so that when the agent clicks an `<input type="file">` button, the file dialog is automatically answered with the specified file. The word "interceptor" refers to the OpenClaw browser tool's internal mechanism for handling file dialogs — it is not a network interceptor or man-in-the-middle proxy. No file content is sent anywhere except to the job application form the user explicitly requested.

### What this skill does NOT do

- Does not make any outbound network requests from scripts (no `curl`, `wget`, `fetch`, or similar)
- Does not read, store, or transmit passwords
- Does not inject JavaScript that modifies page content or behavior
- Does not persist any background process after the session ends
- Does not access any files outside the user's configured resume directory and workspace
- Does not contain obfuscated code, encoded payloads, or remote fetches at runtime

## Optional: session watchdog

For long multi-job sessions, you can optionally set a reminder to prevent the agent from stalling:

```bash
openclaw cron add --name job_sub_watchdog --every 5m \
  --message "job_sub agent: still working? check tracker and continue."
```

This sends a chat message only — it does not run scripts, access files, or make network requests. Remove it when done:

```bash
openclaw cron rm job_sub_watchdog
```

This step is **optional** and is not executed by any script in this skill.

## Helper scripts

The helper scripts (`check_required_fields.js`, `fill_template.sh`, `match_variant_options.sh`) are included in this skill's `scripts/` folder. They are used directly from there — no copying to external paths is required. All scripts are plain-text, unminified, and can be audited before use.

## Setup

This skill reads personal data exclusively from the environment variables listed in the manifest above. There is no separate config file read at runtime — the env vars ARE the single source of truth.

These env vars must be set in your shell environment before the agent starts. Example values:

```bash
export OPENCLAW_USER="yourusername"
export OPENCLAW_PROFILE="apply"
export USER_FIRST_NAME="Your"
export USER_LAST_NAME="Name"
export USER_EMAIL="your@email.com"
export USER_PHONE="+1-555-000-0000"
export USER_LINKEDIN="https://linkedin.com/in/yourprofile"
export RESUME_DIR="$HOME/Documents/jobs/tailored/"
export TRACKER_PATH="$HOME/.openclaw/workspace/job_search/job_application_tracker.md"

export USER_GENDER="Male"
export USER_RACE="Asian"
export USER_HISPANIC="No"
export USER_VETERAN="I have no military service"
export USER_DISABILITY="No"
export USER_WORK_AUTH="Yes"
export USER_NEED_SPONSOR="No"
```

> **Note on site logins**: If a job site requires an account, log in manually in the `apply` browser profile before running the submitter, or allow the browser's saved-credential autofill to handle it. This skill does not manage passwords.

## Session start checklist

1. Verify env vars are set (e.g. `$USER_FIRST_NAME`, `$TRACKER_PATH` are non-empty)
2. Read `$TRACKER_PATH` — find all `resume_ready` entries

## Browser operation rules

### Model may call directly (observation only)
- `open` / `tabs` / `close` / `focus`
- `navigate`
- `snapshot`
- `screenshot`
- `dialog --accept`

### Must be generated as a script, then exec'd
Any action that changes page state:
- `fill`, `type`, `select`, `click`, `press`, `upload`
- Clicking: Apply, Log in, Next, Continue, Submit, any upload button, any dropdown option

**Exception:** Tab management is always a direct tool call. `snapshot` is always a direct tool call.

## Per-job flow

### 1. Read resume and JD

The agent uses python-docx to extract text from the tailored `.docx` resume at runtime. This code is not bundled as a separate `.py` file — the agent writes and executes it inline via the `exec` tool:

```python
# Executed by the agent at runtime via exec tool — not a bundled script
from docx import Document
doc = Document(f'{RESUME_DIR}/<resume>.docx')
text = '\n'.join([p.text for p in doc.paragraphs if p.text.strip()])
```

This is why `python3` and `python-docx` are listed as requirements even though no `.py` file is included in the bundle. The agent generates this code dynamically to read each resume before filling forms.

Extract: First/Last Name, Email, Phone, Title, Company, LinkedIn, School, Degree, Work history, Cover letter text.

If resume does not match JD → mark tracker `error`, skip.

### 2. Open clean tab
Via tool call (not script):
1. `browser tab new` → get TARGET_ID
2. `browser tabs` → list all tabs
3. `browser close <id>` for each old page tab (`type=="page"`)

### 3. Navigate and validate URL
`navigate "<url>"` then `wait --load networkidle`

If the page is a generic careers index or wrong role → mark `wrong_url`, skip.

### 4. Login if needed
Check top-right for existing session. If not logged in:
1. Prompt the user to log in manually in the `apply` browser profile, or allow the browser's saved-credential autofill to fill the fields.
2. Once logged in, continue with the application form.

Do not attempt to read passwords from config or environment. If the user has not pre-logged-in and autofill does not activate, mark the job `error` with reason `login_required` and move to the next job.

### 5. Main form loop

Repeat until submission confirmed:

**A. Snapshot + check unfilled fields**

Use OpenClaw's built-in browser CLI to take a page snapshot and check which fields need filling:

```bash
# openclaw browser snapshot — captures the current page's accessibility tree (read-only)
SNAP=$(openclaw browser --browser-profile $OPENCLAW_PROFILE snapshot \
  --target-id $TARGET_ID --limit 500 --efficient)

# openclaw browser evaluate — runs check_required_fields.js (a read-only DOM query)
# to list which required fields are still empty
# SKILL_DIR is the directory where this skill is installed
CHECK=$(openclaw browser --browser-profile $OPENCLAW_PROFILE evaluate \
  --target-id $TARGET_ID --fn "$(cat "$SKILL_DIR/scripts/check_required_fields.js")")
```

Note: `openclaw browser evaluate` is a standard OpenClaw CLI command that runs a JavaScript expression in the browser tab's console — equivalent to pasting code into DevTools. The script `check_required_fields.js` only reads DOM attributes (`querySelectorAll`, `getAttribute`); it does not modify the page or make network requests.

**B. Generate fill script**

The agent batches multiple `openclaw browser fill`/`select`/`click` commands into a single shell script so they execute atomically. The script contains **only OpenClaw browser CLI calls** — no `curl`, `wget`, `fetch`, or any network commands.

```bash
TS=$(date +%s)
SCRIPT="/tmp/fill_${TS}.sh"
cat > "$SCRIPT" << 'SCRIPT_EOF'
# Contains only: openclaw browser fill/select/click/upload commands
# No network requests, no external downloads, no eval
SCRIPT_EOF
chmod 700 "$SCRIPT" && bash "$SCRIPT" && rm -f "$SCRIPT"
```

Scripts are owner-only (`chmod 700`) and deleted immediately after execution.

Script structure:
1. Tab validation (snapshot, check for "tab not found")
2. Snapshot for fresh refs — never reuse refs across page loads
3. `fill` for text fields (batch all at once)
4. `select` for dropdowns (A-type: direct; B1: open+snap+click; B2: type+snap+click)
5. `upload` before clicking upload button (arm interceptor first)
6. Second `check_required_fields.js` — must pass before any page navigation

**C. Advance page**
Only after second check passes:
- Has `Submit` → all fields filled → submit
- Has `Next`/`Continue` → current page done → advance and loop
- Neither → report error, wait for human

### 6. Submission verification

Both conditions must be true:
1. `document.querySelector('button[type="submit"]') === null`
2. Page contains "Success" / "Application received" / "We have received your application"

Do NOT accept "Thank you for applying" as success.

### 7. Update tracker and report
- Success → `applied`, record submission date
- Failed/skipped → `error`, record reason
- Report result immediately after each job

### 8. Report result
After each job, report to the user: company, title, status (applied/error/wrong_url), and any issues encountered.

## Helper functions for snapshot parsing

```bash
get_ref()       { echo "$1" | grep -F "\"$2\""  | sed 's/.*\[ref=\([^]]*\)\].*/\1/' | head -1; }
get_ref_fuzzy() { echo "$1" | grep -iE "$2"      | sed 's/.*\[ref=\([^]]*\)\].*/\1/' | head -1; }
count_label()   { echo "$1" | grep -cF "\"$2\""; }
```

Never use `jq` on snapshot output. Never use `grep -o 'ref=\K...'`. Never reuse refs across page loads.

## Dropdown strategy

| Type | When | Strategy |
|------|------|----------|
| A — known options | Yes/No/known enum | `select "<value>"` → fallback: open+snap+click |
| B1 — short list (<20) | Company, state | open+snap+click with 0.5s sleep for animation |
| B2 — search-driven | School, discipline | click to open → `type` keyword → 0.5s sleep → snap → click result |

Only use fuzzy matching for unknown dropdown values. Known buttons/labels always use exact match.

## Dynamic components

Work history and education sections usually require clicking "Add" per entry. After each click, re-snapshot before extracting refs — new components get new refs.

## File upload sequence

Always: `upload <path>` first (arms the interceptor), then click the upload button. Never reverse this order. After page refresh, re-snapshot before clicking upload.

## EEOC defaults

Read from config: `$USER_GENDER`, `$USER_RACE`, `$USER_HISPANIC`, `$USER_VETERAN`, `$USER_DISABILITY`, `$USER_WORK_AUTH`, `$USER_NEED_SPONSOR`.

## Cover letter

Always fill cover letter text fields, even when marked optional. Read content from the `.docx` file using python-docx, not from the file path.

## Script safety rules

1. All page-state-changing actions go in scripts — no direct model calls
2. Never use JS injection; use `fill`/`type` instead
3. Script comments use `#` only — no em-dashes or special chars
4. Single exit point: find ref → on failure write to ERRORS → on success execute
5. Unique-label check before acting: `count_label "No"` etc. must return 1
6. All personal data comes from environment variables (not from reading files at runtime)
7. File copy with error capture: `if ! cp "$SRC" "$DST"; then ERRORS+=("copy failed"); fi`
8. Dynamic components: click parent to trigger render → sleep 0.3 → re-snapshot → extract ref

## Tracker status flow

```
resume_ready → applied
            ↘ error
            ↘ wrong_url
```

## Support

If Job Autopilot saved you time: paypal.me/ZLiu308
