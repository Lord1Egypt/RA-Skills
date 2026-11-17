---
name: "noteclaw"
description: "Read-only mirror of OneNote notebooks into local Markdown + git, for querying, diffing, and periodic summaries. Requires a one-time OAuth authorization (personal Microsoft account)."
---

# OneNote Read-Only Mirror + Query + Weekly Reports (noteClaw v1.0.0)

Mirror Microsoft OneNote notebooks **read-only** into local Markdown + git snapshots, then query, diff, and summarize on demand.

> Below, `$SKILL` = this skill's install directory (the folder holding this `SKILL.md`, with `scripts/` inside).

> **⚠️ First use (agent must read)**: this skill needs a **one-time OAuth authorization**; every sync fails until that is done. Full steps are under "One-time setup" and "Workflow" below — quick view:
> 1. **No token** (no `.auth/notes_token.json` in the data directory) → run `scripts/auth_code.py` to get an authorization link, have the user paste the full URL back, then exchange it with `--code-url` (use `--code-file` when the chat channel truncates long URLs).
> 2. After authorization, cold start: list notebooks → full pull → convert to md. When done, ask the user whether to set up scheduled sync, and confirm their timezone for query windows (`NOTECLAW_TZ`).
>
> **Note**: send the link, then end the turn and wait for the user to paste the full URL back.
>
> **⚠️ Multi-notebook accounts**: list them with `graph_sync.py --list-notebooks`, **ask the user which one to mirror**, then pass the choice with `--notebook <name>` (or `NOTECLAW_NOTEBOOK`). See "4. Optional environment variables".

## When to use

- Let the agent query / search OneNote notes by time window, keyword, or section
- Generate a periodic report of what changed in the notes, or summarize an arbitrary range on demand
- Inspect changes to notes over a period (diff)

## Hard requirements

- **Python ≥ 3.9** (uses `zoneinfo`); standard library only, no third-party dependencies
- **git**: snapshot history depends on git (md is still produced outside a git directory, but there is no snapshot history and `html2md.py` exits 1 to flag it)
- **Network**: access to `graph.microsoft.com` and `login.microsoftonline.com`
- **Install**: `openclaw skills install @jellyjujube/noteclaw`; manual install means placing this whole directory at `<workspace>/skills/noteclaw/`
- Scripts live under the skill's `scripts/` and are **not installed system-wide**; call them as `python3 <path>/xxx.py`

## One-time setup

### 1. Client credentials (built in, no registration)

Authorization uses the **publicly published rclone OneDrive application** (`client_id` + `client_secret` as a pair, shared by all rclone users — see <https://rclone.org/onedrive/>). `scripts/auth_code.py` ships with these credentials, so it works out of the box and **nothing needs to be registered in Azure**.

Credential source priority (the script takes the first usable one, in order):
1. Environment variables `CLIENT_ID` + `CLIENT_SECRET` (both must be set to take effect)
2. A section in `~/.config/rclone/rclone.conf` that contains **both `client_id` and `client_secret`** (read-only; never mixed across sections)
3. The rclone public credentials built into the script (fallback; this package's default path)

> **Note**: running your own Azure application requires a Developer account and hosting a `client_secret` yourself. The built-in public application removes that step; the cost is that the issued scope covers the whole OneDrive (see "Security and boundaries").
>
> Targets **personal Microsoft accounts** (@outlook / @hotmail / personal @live). Organization/work accounts are unverified.

### 2. Create the data directory (do this before authorizing!)

All artifacts (`manifest.json` / `store/` / `cache/` / `.auth/`) land in the **current working directory of the command** (override with the `NOTECLAW_HOME` environment variable). Create the directory and configure git first, then authorize — otherwise the token is written to the wrong place:

```bash
export SKILL=<skill install path>   # e.g. <workspace>/skills/noteclaw
mkdir -p ~/onenote-mirror && cd ~/onenote-mirror
git init
git config user.name "Your Name"        # required! snapshot commits fail without it
git config user.email "you@example.com"
printf '.auth/\ncache/\n__pycache__/\n' >> .gitignore
```

### 3. Get the initial token (authorization code flow, run inside the data directory)

Run once to get the authorization link, then run again with the code the user pasted back:

```bash
cd ~/onenote-mirror
python3 $SKILL/scripts/auth_code.py                                  # first run: prints the authorization link
python3 $SKILL/scripts/auth_code.py --code-url "<full URL pasted back>"  # second run: exchange for a token
python3 $SKILL/scripts/auth_code.py --code-file .auth/code.txt          # when the channel truncates the paste
```

The script prints an authorization URL (on the line after the `[AUTH URL]` marker). Put that line verbatim into your reply to the user, who signs in with the Microsoft account to be mirrored and consents. The browser then lands on `http://localhost:53682/` showing a "this site can't be reached" error, which is expected. Hand the full URL the user pastes back to the script with `--code-url`; it exchanges it for a token and writes `.auth/notes_token.json` (0600, includes the refresh token).

Ways to supply the code (chosen by the run arguments):

- **`--code-url <full URL>`**: pass the whole URL the user pasted back.
- **`--code-file <path>`**: the user saves either the whole URL or just the value after `code=` into a file; the script reads the code from it and deletes the file on success.

Afterwards `graph_sync.py` refreshes the access token on every run; no further authorization is needed unless the token expires or is revoked.

### 4. Optional environment variables

| Variable | Purpose | Default |
|---|---|---|
| `NOTECLAW_NOTEBOOK` | Notebook to mirror — for multi-notebook accounts, list with `--list-notebooks`, ask the user, then set this (or pass `--notebook`); once recorded in the manifest it is reused; switching notebooks does not clobber each other | manifest record / the only notebook |
| `NOTECLAW_TZ` | Timezone for query windows (an IANA name such as `Europe/Berlin`). It is only a default: at first setup, confirm the user's zone and set it (env var, or the scheduled task); an unusable value falls back to UTC with a warning | `UTC` |
| `NOTECLAW_HOME` | Data directory override | cwd at run time |
| `CLIENT_ID` / `CLIENT_SECRET` | Custom client credentials (must be set as a pair); a self-registered app requesting only `Notes.Read` narrows the issued scope to notes | rclone public application built into the script |

## Workflow

> Every command runs inside the **data directory** (the scripts themselves stay at the skill install location and are never written to).

### Cold start (first time)

```bash
cd ~/onenote-mirror
python3 $SKILL/scripts/graph_sync.py --list-notebooks   # notebooks listed = authentication works
python3 $SKILL/scripts/graph_sync.py --all              # full pull, builds the baseline
python3 $SKILL/scripts/html2md.py                       # convert to Markdown + first snapshot commit
```

### Daily incremental sync

```bash
cd ~/onenote-mirror
python3 $SKILL/scripts/graph_sync.py                    # ETag detection, pulls changed pages only
python3 $SKILL/scripts/html2md.py                       # convert to md → git snapshot commit
python3 $SKILL/scripts/graph_sync.py --list             # list section tree + page count per section
python3 $SKILL/scripts/graph_sync.py --dry-run          # preview what would be pulled, without pulling
```

### Query (read-only, zero LLM cost)

```bash
cd ~/onenote-mirror
python3 $SKILL/scripts/notequery.py list [--section NAME]                   # page listing
python3 $SKILL/scripts/notequery.py since --since <YYYY-MM-DD> [--until ...] [--kind all|new|edited] [--full] [--max-pages N] [--max-bytes B]
python3 $SKILL/scripts/notequery.py week [--weeks-ago 0] [--full] [--max-pages N] [--max-bytes B]   # this-week shortcut
python3 $SKILL/scripts/notequery.py grep --kw KEYWORD [--section ...]       # title/body search
python3 $SKILL/scripts/notequery.py fetch --page <NNN or title or path> [--section NAME]   # full text of one page; --section narrows the lookup when a number exists in several sections
python3 $SKILL/scripts/notequery.py diff [--from REV] [--to REV] [--name-only] [--full] [--max-bytes B]
```

By default only the metadata listing is emitted (zero tokens); `--full` appends bodies, `--max-pages` / `--max-bytes` are body budget gates (they truncate bodies only — the listing is always complete), and `--kind` distinguishes new from edited. Full arguments: `python3 $SKILL/scripts/<script>.py --help`.

> **⚠️ Limits of time-window queries**: `since` / `week` decide inclusion from Graph page timestamps, and that field may not update on content-only edits (see "Security and boundaries") — **pages whose content changed while the timestamp stayed put are missed by the window**, and missing does not mean unchanged. To know what actually changed, use `diff` (git-based, unaffected).
>
> `diff` defaults `--from` to "the most recent commit that touched the store", and `html2md.py` commits on every sync — so **right after a sync, a bare `diff` necessarily reports 0 changes, and that is not "nothing changed"** (the script prints that sentence together with the base rev to use). To see changes since the previous snapshot, use the `--from <rev>` it suggests; for changes over a period, use `$BASE` from the weekly report flow.

### Weekly report / summary

**Before producing any report or summary, read `references/weekly-report.md`** (base commit resolution, notequery usage, report template). Outline: resolve the base commit → incremental sync → `notequery.py diff` for changed pages → read the content → write `reports/<notebook>/weekly-YYYY-Www.md` and commit it → present the report in full to the user.

> Report data source: the store snapshot just synced plus git history.

## Scheduled sync

Sync and reporting are two independent tasks with their own schedules, run by the agent through the host's scheduling mechanism (e.g. system cron). Once authorization and cold start are done, ask the user which preset they want and show them the tasks to be added (what runs, how often, at what time) before configuring anything.

### Task 1 · Mirror sync

One incremental sync, landing note changes in `store/` as a single git snapshot:

```bash
cd <data directory>
python3 $SKILL/scripts/graph_sync.py && python3 $SKILL/scripts/html2md.py
```

This is pure script work with no model involvement; schedule it as a plain command. The output is the `store/` snapshot and git history in the data directory, consumed by task 2.

### Task 2 · Periodic summary

Produce a report of what changed over a fixed period, following references/weekly-report.md. The report compares the complete git history from "previous report → now", independent of sync frequency — syncing more often only makes snapshots finer; the summary period just must not be shorter than the sync period.

By default the period is a calendar week (`reports/<notebook>/weekly-YYYY-Www.md`); for a longer custom period, keep the same flow and change the interval and file name accordingly. Reports are user-facing and are presented in full once generated.

### Presets

- **A. Sync + weekly report (recommended)**: incremental sync daily, one report per week at a fixed time.
- **B. Custom periods**: the user chooses the period and time for sync and for reporting separately (e.g. daily sync + monthly summary).

## Scripts and artifacts

| File | Purpose |
|---|---|
| `scripts/auth_code.py` | Authorization code flow: prints the authorization link; `--code-url` / `--code-file` hand the code back (the file is deleted after a successful exchange, kept with a message on failure so it can be retried) → writes `.auth/notes_token.json` (0600); records the actual client_id in the token for later refreshes |
| `scripts/graph_sync.py` | Graph incremental sync (section gate + per-page ETag conditional GET) → `cache/` + `manifest.json` |
| `scripts/html2md.py` | HTML → `store/` Markdown, git commit (each sync = 1 snapshot) |
| `scripts/notequery.py` | Query CLI: list / since / week / grep / fetch / diff (purely local, zero network) |
| `scripts/noteclaw_creds.py` | Single source of client credentials (shared by auth_code and graph_sync) |

**Artifacts and naming contract** (all inside the data directory):
- `manifest.json`: section/page metadata + ETags, including the notebook record (id + displayName)
- `store/<notebook>/<section rel path>/<NNN>_<title>.md`: Markdown snapshots (NNN = page index; store directory names use the original section name, cache directory names are sanitized; the notebook segment is sanitized too)
- `cache/pages/<notebook>/<section>/<page id>.html`: Graph HTML cache
- `.auth/notes_token.json`: token (0600, never commit)
- `reports/<notebook>/weekly-YYYY-Www.md`: weekly report (ISO week number)

## Security and boundaries

Authorization is read-only for OneNote; write operations are out of scope — requesting `Files.ReadWrite` / `Notes.ReadWrite` with the refresh token returns HTTP 400 in testing. The issued `scope` is `Notes.Read Files.Read`, wider than the requested `Notes.Read`, so the token can read this account's entire OneDrive: the issued scope follows what this client has already been consented to for the account, and requesting a narrower scope does not change the result (application source under "1. Client credentials"). The scripts only call OneNote endpoints and never touch the drive; to narrow the granted permissions, register your own app requesting only `Notes.Read` (see "4. Optional environment variables").

Images are not downloaded; in-body images appear in Markdown only as `[image: <resource-id>]` placeholders. LaTeX and HTML layout are not reconstructed; encrypted sections and inaccessible notebooks are skipped automatically. Credentials live only in `.auth/` / environment variables / rclone.conf and are never committed (`.auth` is in `.gitignore`); rclone.conf is read-only. Change detection relies on **ETag** by default (Graph page timestamps are known not to update on content edits); the script includes a `--mode timestamp` fallback switch.

## Failure modes (for troubleshooting)

| Symptom | Cause | Handling |
|---|---|---|
| No token file | Not authorized / wrong data directory | Run `auth_code.py` in the data directory; confirm `NOTECLAW_HOME` or cwd is correct |
| manifest reported "unusable / schema is not 3" | Old manifest or corrupt file | All three scripts fail identically on an unusable manifest (rc=2, no silent data change): back it up, delete `manifest.json`, rerun cold start `graph_sync.py --all` → `html2md.py` |
| The URL the user pasted back is truncated to an ellipsis | The chat channel swallowed the long string | Have the user write the full URL into a file and transfer it via `--code-file` |
| Authorization succeeded but sync reports missing `client_id/secret` or 401 | Refresh credentials differ from the ones used at authorization | Rerun `auth_code.py` in the data directory so the token records the current client_id, then sync |
| `HTTP 401` mid-sync | access_token expired and refresh failed | Rerun `auth_code.py` to re-authorize (only happens when the refresh token is invalid) |
| A section reports `🔒 HTTP 403 20185` | Encrypted / inaccessible section | Normal: recorded as skipped and retried every run (retried once the section timestamp changes); add `--all` to force an attempt |
| The wrong notebook was mirrored | Multi-notebook account without explicit selection | List them (`--list-notebooks`), ask the user which one, then pass `--notebook NAME` or `NOTECLAW_NOTEBOOK` (see "4. Optional environment variables") |
| `html2md.py` deleted files in my store | Orphan cleanup mistook pages with no html cache for orphans | Cleanup is based on the artifacts the manifest says should exist, and only deletes `NNN_*.md` files named by this tool (other files are kept); missing html is reported, not deleted |
| `fetch` / `since --full` / `grep` report missing md files (rc=1) | `store/` snapshot incomplete (html cache missing, html2md not run or failed) | Run `html2md.py` to fill the gaps before reading bodies; exit code 1 is a warning signal, not "not found" or "no match" |
| Sync misses content / section timestamp unchanged but pages changed | Section gate missed a change (rare) | Compare per-section page counts with `--list`, then run one pass with the `--no-gate` safety net (keeps the precise ETag check, misses nothing) |
| Report is missing pages | Sync or conversion failed and was skipped | Failures end with exit code 1 (scheduled tasks alert on that); check `graph_sync.py` for 🔒/✗ and `html2md.py` for missing html, and confirm there are no failures before summarizing |
| Token `scope` is wider than requested (includes `Files.Read`) | The built-in public application carries `Files.Read` | Normal (see "Security and boundaries"). To verify the real grant, probe each scope against the token endpoint with the refresh token (HTTP 400 = not granted); to narrow it, register your own app requesting only `Notes.Read` (`CLIENT_ID` / `CLIENT_SECRET`) |

## User phrasing → command

| The user says | Do |
|---|---|
| What changed in my OneNote this week / weekly report | Follow references/weekly-report.md |
| Authorize / the token expired | Follow "3. Get the initial token": run `auth_code.py` for the link → user pastes the URL back → return it with `--code-url` |
| Find note X / look up X | `notequery.py grep --kw X` (run `list` first to locate the section) |
| What changed recently | "What changed" means `diff` (git); `since --since <7 days ago>` uses Graph timestamps and can miss content-only edits (see "Limits of time-window queries") |
| Give me the content of page X | `notequery.py fetch --page X` |
| Sync / update the mirror | Run `graph_sync.py && html2md.py` in the data directory |
| Show me what a sync would do | `graph_sync.py --dry-run` |
