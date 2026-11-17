# Med Reminder Skill

An OpenClaw skill that sends medication reminders through whatever messaging app you already use — WhatsApp, Telegram, SMS, or anything else you can script. Reminders land in a conversation you're already in, not as a notification you swipe away.

> **This is a reminder tool, not a medical device.** It does not diagnose, prescribe, or verify anything medical. You are responsible for confirming your own doses. Provided as-is under the MIT License, without warranty of any kind — see [LICENSE](LICENSE).

Three escalation tiers per dose: on-time reminder → late nudge → missed log. Each med has its own schedule, dose, and thresholds.

Reconstituted injections get syringe-unit math automatically: define a med in mg/mL and reminders read "Ipamorelin 200mcg = 20 units on your U-100" — no mental math at dosing time. State lives in a JSON file plus an append-only event log — no database, no backend, no account.

> ⚠️ **Do not run intermediate builds on real meds.** Builds before the PR 4 reply commands are not safe for real use. If you are upgrading an existing install, dogfood the new build with a fake med for a few days before trusting it with a real schedule.

---

## Prerequisites

- Python 3.9+
- Windows: Task Scheduler (built-in). Git Bash only if your `send-message.sh` is a bash script — the dispatcher finds `bash.exe` in the standard Git locations even when scheduled tasks don't inherit your PATH
- macOS: launchd (built-in)
- Linux: cron (built-in); a systemd user timer is available opt-in
- Chrome, Edge, or Brave (for the HTML editor — requires File System Access API)
- OpenClaw with a messaging channel configured

On Windows, install the IANA timezone database:
```
pip install tzdata
```

---

## Install

```bash
git clone <repo-url>
cd openclaw-med-reminder-skill
```

That's it. No build step, no package manager. On first use the AI creates your state file with `python3 reply.py init` (or copy `meds-state.template.json` to `meds-state.json` and use the editor).

---

## Configure your medications

Two ways — pick one:

### Option A: HTML editor

Open `editor.html` in Chrome, Edge, or Brave. Click **Open file**, load your `meds-state.json`, edit global settings and medications, click **Save**. All validation runs in the browser before writing, and a stale-file check refuses to save if another process changed `meds-state.json` while you had it open.

The per-med history table in the editor shows the last 30 events mirrored into the state file. The full history lives in `history.jsonl` next to it (see [State & history](#state--history)).

### Option B: Conversational interview

In OpenClaw, start a conversation with the med reminder skill and say "set up my meds." The AI walks you through timezone, quiet hours, and each medication one question at a time, then writes everything through the validated `reply.py` commands. See `SKILL.md` for the full question flow.

Both paths validate the state file before writing. Invalid state can never reach disk.

---

## Wire up your messaging channel

Create `send-message.sh` in the skill directory. It receives the message text on **stdin** and must exit 0 on success.

```bash
#!/usr/bin/env bash
# send-message.sh — wire this to your channel

MESSAGE=$(cat)   # full message text arrives on stdin

# Example: WhatsApp via OpenClaw gateway
# curl -s -X POST "$OPENCLAW_WEBHOOK" \
#   -H "Content-Type: application/json" \
#   -d "{\"text\": $(echo "$MESSAGE" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')}"

# Example: Telegram — the text goes to curl on STDIN ("text@-"), never as an
# argument: on Windows, Git Bash re-encodes arguments to the ANSI code page,
# so non-ASCII text (the digest's "Mon–Fri") arrives as invalid UTF-8 (#20)
# RESP=$(printf '%s' "$MESSAGE" | curl -s "https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage" \
#   --data-urlencode chat_id="$TELEGRAM_CHAT_ID" \
#   --data-urlencode "text@-")
# echo "$RESP" | grep -q '"ok":true' || { echo "telegram: $RESP" >&2; exit 1; }

# Example: log to file only (for testing)
echo "$MESSAGE" >> ~/med-reminder-sent.log
```

Make it executable:
```bash
chmod +x send-message.sh
```

Alternatively, set the `MEDS_SEND_CMD` environment variable to any shell command that reads from stdin.

---

## Register the scheduler

One repeating **tick task** runs `dispatch.py tick` every few minutes; the tick decides per med and dose what to send (see [How it works](#how-it-works)). Register it after saving your `meds-state.json`:

```bash
# Preview what will be registered (no changes)
python3 setup-tasks.py --dry-run

# Register
python3 setup-tasks.py
```

Per platform:

| OS | Scheduler | Details |
|----|-----------|---------|
| Windows | Task Scheduler | Task `tick-<hash>` in the `MedReminder` folder, run with `pythonw.exe` (no console flash), catch-up on wake (`StartWhenAvailable`), 10-min execution limit |
| macOS | launchd user agent | `StartInterval`-based (cron has a Full Disk Access problem on modern macOS) |
| Linux | cron | One marked block per state file; `--scheduler systemd` opts into a user timer instead |

The tick task is keyed by a short hash of the resolved state path, so two state files never collide. Registration is **register-verify-remove**: the tick is registered and queried back successfully *before* any legacy per-dose job from an older install is removed. If registration fails, the script exits non-zero, prints `REMINDERS ARE NOT SCHEDULED`, and leaves every existing job in place.

The default cadence is every 5 minutes — doses can fire up to ~5 min late. For time-critical meds or an always-on desktop:

```bash
python3 setup-tasks.py --tick-minutes 1
```

Add, edit, remove, or pause meds later with no re-run — the tick picks up changes on its next pass. Re-run `setup-tasks.py` only to change the cadence or state-file location.

To remove the tick and any legacy jobs:
```bash
python3 setup-tasks.py --clear
```

---

## How it works

Every scheduled run is one `dispatch.py tick`:

1. **Enumerate** each med's dose occurrences between the tick watermark and now — all time math in UTC, so DST spring-forward and fall-back behave (a 01:30 dose on fall-back day reminds once, at the first instance).
2. **Stage** each occurrence: reminder → snoozed reminder → late nudge → missed. Only the highest due stage acts; a dose confirmed inside its minimum-gap window never re-fires. Meds due at the same minute share one reminder (and one nudge per round) listing each med still untaken; each med is still tracked on its own.
3. **Catch up** after sleep or downtime: past-due-but-recent doses get an actionable nudge; anything past the missed deadline is logged `missed` silently with one consolidated message, so 20 missed hours don't spam 20 messages.
4. **Send at-least-once** under a lease with a 60s timeout. A crash between send and record produces exactly one repeat, prefixed `(repeat — ignore if you already got this)`. A message that keeps failing while others get through is reported once, on its own ("Delivery problem: the 8:00am digest couldn't be sent …"); a full sender outage is tracked for `doctor.py`, and nothing is ever prefixed to an unrelated message.
5. **Persist** every decision (`reminded`, `taken`, `missed`, …) to the append-only `history.jsonl` under an OS file lock. History is the source of truth; the state file is a cache. A crash at any point heals on the next tick.

Quiet hours mute escalations only — dose-time reminders always send (you chose the time), nudges may still land in the first 30 minutes of the quiet window, and any dose logged missed during the night is summarized right after quiet hours end.

A single tick instance runs at a time (non-blocking instance lock); a per-med failure is isolated so one broken schedule can't stop the others (one alert per day, and `doctor.py` explains).

---

## Reply commands

When you reply to a reminder or digest ("took metformin", "snooze that", "took it at 8"), the AI runs the matching `reply.py` command. Every write goes through it — validated, locked, atomic:

| You say | Command |
|---------|---------|
| `took metformin` / `done` / `all taken` | `confirm <id>` / `confirm --all` |
| `took it at 8` | `confirm <id> --taken-at 08:00` |
| `snooze that` / `not yet` / `pause metformin 90` | `snooze <id> [--minutes N]` (pausing a reminder is a snooze) |
| `skip metformin` | `skip <id>` (logged skipped, never missed) |
| `undo` | `undo <id>` (within 24h) |
| `stop taking metformin` / `resume metformin` | `pause <id>` / `unpause <id>` |
| `I mixed wolverine: 10 mg with 2 mL` | `reconstitute <id> --vial-mg 10 --diluent-ml 2` (reminders then show syringe units) |
| `got 3 more vials` / `I have 2 left` | `restock <id> --qty 3` / `restock <id> --set 2` (supply tracking; the digest flags "reorder") |
| `status` / `what's due` | `status` (read-only) |
| add / change / remove a med, quiet hours | `add-med` / `edit-med` / `remove` / `set-quiet-hours` |

Confirmation credits the nearest-in-time dose and says which one it logged ("Logged as your 8:00am dose."). If it can't tell which dose you mean, it asks; if you already logged that dose recently, it warns about a double dose and only overrides when you confirm. You can also refer to "the second one" from today's digest (`--position 2`).

---

## Daily digest

A morning summary fires once daily at the time you set in global settings (default: 8:00am), with a 7-day adherence line computed from `history.jsonl`:

```
Meds for Mon Apr 21:
1. Metformin 500mg | 8:00am, 8:00pm (with food)
2. Lisinopril 10mg | 9:00pm

Last 7 days: 13/14 doses taken

Reply: 'all taken' | 'took [name]' | 'skip [name]' | 'snooze [name]'
```

Reply handling runs on the AI side via `reply.py` (see `SKILL.md` §7).

---

## Escalation flow

For each scheduled dose:

| Time | What happens |
|------|-------------|
| Dose time | Initial reminder sent (quiet-hours exempt) |
| Every nudge interval after the dose (default: 30min) | Nudge sent until you take it, skip it, or pause it ("pause metformin 90") — muted in quiet hours past the first 30 min, resumes after |
| The med's next dose is due (at most 25h later) | Logged as missed, silently — the digest shows it; misses that close overnight are in the post-quiet-hours summary |

Thresholds are configurable per medication. Doses and nudge times that would be muted by quiet hours are refused at add/edit time with a suggested fix.

**Global pause:** Silence everything temporarily — one checkbox in the editor.  
**Per-med pause:** Skip a single medication without touching others. Doses during a pause aren't counted; unpause restarts tracking from now.

---

## Upgrading from the pre-tick build

Old installs had one scheduler job per dose (`fire_*`, `check_*`, `miss_*`, digest, reset-deferred). The tick replaces all of them:

1. Back up your `meds-state.json` (a `.bak` also rotates automatically on writes).
2. Update the files, then run `python3 setup-tasks.py`.
3. The script registers the tick, verifies it, then removes every legacy job for this state file. Foreign crontab lines and other tasks are untouched.
4. The first tick migrates state: existing history is copied to `history.jsonl`, a watermark is set from your last logged events, so already-taken doses are **not** re-reminded or marked missed.

Legacy state fields (`status`, `confirmed_dose`, `last_taken`, `next_due`) keep being written for one release, so rolling back the code doesn't lose anything.

To roll the scheduler back manually: `python3 setup-tasks.py --clear` removes the tick (and legacy jobs), or per OS — `schtasks /delete /tn "\MedReminder\tick-<hash>"` on Windows, `launchctl unload ~/Library/LaunchAgents/<label>.plist` on macOS, edit the marked block out of `crontab -e` (or `systemctl --user disable <unit>.timer`) on Linux.

---

## Med passport

Generate a printable medication card for doctor visits or emergency contacts:

```bash
python3 generate-passport.py --name "Jane Smith" --dob "1975-03-12"
```

Or say "generate passport" in a conversation with the skill. Output is `med-passport.html` — open in a browser and print/save as PDF. Paused medications are excluded.

Options:
```
--name NAME     Patient name on the card
--dob  DATE     Date of birth (optional)
--out  PATH     Output file path (default: med-passport.html)
--no-prompt     Skip the name prompt
--dry-run       Print HTML to stdout
```

---

## Health check

Verify everything that fails silently at 3am — state validity, timezone data, sender wiring, the registered tick (and that no legacy job survives), and a fresh `tick-heartbeat.json` (stale beyond 3× the tick interval = FAIL):

```bash
python doctor.py               # read-only checks; exit 1 on any failure
python doctor.py --send-test   # also pipe one test message through your channel
```

Run it after first setup and any time reminders seem to have stopped.

---

## State & history

Two files change at runtime, both next to the scripts by default:

- **`history.jsonl`** — the append-only event log and source of truth. Every reminder, dose, nudge, skip, snooze, and undo is one line here. Adherence and the digest's 7-day line are computed from it, and it is never trimmed.
- **`meds-state.json`** — the editable cache: prescription, schedule, quiet hours, and the last 30 events mirrored per med for the editor and older tooling.

All writes go through `safe_write.py`: structural validation, an OS file lock, a sha256 write token (a stale token aborts — two writers can never clobber each other), a rotating `.bak`, then an atomic replace. `reply.py show-state` prints the current token for CLI writers.

On POSIX, state, history, backups, tmp files, and logs are created `0600`.

Environment overrides:
```bash
MEDS_STATE_FILE=/path/to/meds-state.json
MEDS_HISTORY_FILE=/path/to/history.jsonl
MEDS_LOG_FILE=/path/to/dispatch.log
MEDS_SEND_CMD="curl -X POST ..."   # overrides send-message.sh
MEDS_LOG_REDACT=1                  # see Privacy
```

---

## Privacy

- Logs contain no med names when `MEDS_LOG_REDACT=1` (or `global.log_redact: true`): med IDs only, including stderr captured from your sender script.
- Log timestamps are UTC.
- Private files are `0600` on POSIX; the process umask is tightened before anything is created.

---

## Test the engine

```bash
# Dry-run one tick: print what would be sent, write nothing
python3 dispatch.py --dry-run tick

# Legacy per-dose subcommands (fire/check/miss/digest) still parse
# and run the tick — kept one release for old schedulers
```

## Run the test suite

```bash
pip install -r requirements-dev.txt   # one-time
python -m pytest -q
```

413 tests covering the tick engine and DST edges, attribution, the event store, locking and transactions, scheduler migration on all three OSes, reply commands, quiet-hours rules, logging/privacy, the editor wiring, the SKILL.md contract, and the passport generator.

---

## File structure

```
openclaw-med-reminder-skill/
├── meds-state.json          # your state file (git-ignored, created from template)
├── meds-state.template.json # blank valid state — copy to start
├── history.jsonl            # append-only event log (source of truth)
├── meds-state.json.bak      # auto-created before each write
├── tick-heartbeat.json      # updated every tick — doctor FAILs if stale
├── meds.schema.json         # JSON Schema for state validation
├── dispatch.py              # tick engine (tick; legacy subcommands wrap it)
├── tick.py                  # tick stages, catch-up, leases, consolidation
├── reply.py                 # AI reply commands (confirm/snooze/skip/undo/…)
├── attribution.py           # nearest-in-time dose attribution
├── event_store.py           # history.jsonl load/append + migration
├── occurrence.py, clock.py  # UTC occurrence helpers, injectable Clock
├── setup-tasks.py           # registers the tick (Windows/macOS/Linux)
├── safe_write.py            # atomic validated state writer + transact
├── generate-passport.py     # med passport HTML generator
├── doctor.py                # health check: state, sender, tick, heartbeat
├── editor.html              # browser-based state editor
├── send-message.sh          # YOU CREATE THIS — wires to your messaging channel
├── SKILL.md                 # AI interview guide and reply handler spec
├── requirements.txt         # Python dependencies (tzdata on Windows)
├── requirements-dev.txt     # test dependencies
└── tests/
```

---

## Quick start checklist

- [ ] Clone repo, `cp meds-state.template.json meds-state.json`
- [ ] Open `editor.html` in Chrome/Edge/Brave, load the file, add your meds, save — or run the interview in OpenClaw
- [ ] Create `send-message.sh` and test it: `echo "test" | bash send-message.sh`
- [ ] Run `python doctor.py --send-test`
- [ ] Run `python3 setup-tasks.py --dry-run` to preview, then `python3 setup-tasks.py` to register
- [ ] **Dogfood with a fake med for a few days before adding real medications**
- [ ] Run `python -m pytest -q` to verify the engine is healthy
