---
name: "google-photos-takeout-pipeline"
version: "1.0.2"
title: "Google Photos Takeout → Local CLI Download Pipeline"
description: "Fully automated Google Takeout bulk download via CLI (aria2c/curl): cookie harvesting from a running browser via CDP, URL pattern construction, per-part verification, auto-unpacking, throttling and resume — plus the official server-side Google Photos → iCloud transfer."
author: "drpeterkalmar"
type: "agent"
category: "backup"
invocation: "/takeout-download"
difficulty: "advanced"
tags: ["google-takeout", "google-photos", "aria2", "backup", "browser-automation", "cdp", "cookies", "icloud", "photos-migration"]
---

# Google Photos Takeout → Local CLI Download Pipeline

Automate the worst part of leaving Google Photos: **downloading the Takeout archive** —
hundreds of GB across many ZIP parts, behind session-bound URLs that break every
manual approach. This skill turns the whole thing into a hands-off pipeline:

```
Takeout job → [browser as cookie factory] → aria2c downloads (throttle/resume)
            → per-part ZIP verification → immediate unpacking → chronological sorting
```

Designed for agent setups (Hermes, OpenClaw, Claude Code with computer use, or plain
terminal + a running Chromium-based browser with `--remote-debugging-port=9222`).

## What's actually in here (and what's new vs. existing guides)

The core auth trick (final `takeout-download.usercontent.google.com` URLs + cookies)
is documented elsewhere — see [Credits](#credits--prior-art). What this skill adds
is the **agent-usable, self-healing pipeline around it**:

1. **CDP cookie harvesting instead of manual copy-paste.** Pull ALL browser cookies
   (`Storage.getCookies`, browser-level target) into a Netscape jar. The usual
   filtered extraction (only `takeout.google.com` + `accounts.google.com`) FAILS —
   the download host `takeout-download.usercontent.google.com` sets its own cookies
   that your jar must include. This is the #1 reason people conclude "curl is blocked".
2. **URL pattern construction.** One ripped URL (from `chrome://downloads` or a live
   download event) reveals the stable pattern for ALL parts:
   `https://takeout-download.usercontent.google.com/download/takeout-<TS>-1-<NNN>.zip?j=<JOB>&i=<N>&user=<USER>&authuser=0`
   (`i` is 0-based, the filename number is 1-based). No browser interaction needed
   beyond the initial discovery.
3. **Session-cookie rotation handling.** Google rotates `__Secure-*PSIDTS` cookies
   every ~15–30 min. A static jar silently degrades into 1.2 MB HTML login pages
   mid-run. The runner refreshes cookies via CDP **before every part** and verifies
   `PK\x03\x04` magic + size after every part; HTML garbage is deleted and retried.
4. **Self-healing browser.** If the user closed the browser, the runner relaunches it
   (`open -a ... --remote-debugging-port=9222`) before refreshing cookies.
5. **Immediate unpacking with SSD budget logic.** 867 GB of ZIPs + 867 GB unpacked
   exceeds most drives. The unpack watchdog tests (`unzip -t`), unpacks, and deletes
   each verified ZIP as soon as it lands — disk usage stays at ~1× library size.
6. **Throttle & resume without byte loss.** `aria2c --max-overall-download-limit`
   for soft throttling; `kill -STOP/-CONT` as a hard pause; `.aria2` control files
   resume exactly where a crash killed the process.
7. **The official Google→iCloud direct transfer** as a zero-bandwidth alternative
   (documented flow in `references/pitfalls.md`) — most people don't know it exists.

## When to use

- Migrating a large Google Photos library (100 GB … multi-TB) to local storage / NAS / iCloud
- Recurring Takeout exports (yearly increment) that you don't want to babysit
- Any situation where you have a Takeout job ready and a logged-in browser

**Not for:** uploading photos TO Google Photos; small one-off album downloads
(the Google Photos web UI is fine for that); after-March-2025 rclone API access
(rclone can only download what it uploaded itself — API lockdown).

## Prerequisites

- macOS or Linux, `python3` with `websockets` (`pip install websockets`)
- `aria2c` (brew install aria2 / apt install aria2), `unzip`, `exiftool` (optional EXIF pass)
- A Chromium-based browser (Chrome, Comet, Brave, Edge) launched with
  `--remote-debugging-port=9222` and a **manually logged-in Google account**
- The Takeout export must be COMPLETED (status "Archive finished" on takeout.google.com)

## Quick start

```bash
# 0) Your Takeout job must exist (takeout.google.com → Google Photos → create export)

# 1) Discover ONE final URL: start any part's download in the browser, then read
#    chrome://downloads (or let scripts/discover_url.py do it via CDP)
python3 scripts/discover_url.py            # rips data.url of the active download

# 2) Harvest cookies + download all parts (5 MB/s, self-healing browser, per-part refresh)
python3 scripts/takeout_download.py \
  --job <JOB_ID> \
  --first-file takeout-20260827T130928Z-1-001.zip \
  --total 18 --dir /path/to/Takeout --limit 5M

# 3) In parallel: unpack each finished part immediately (keeps disk usage flat)
python3 scripts/takeout_unpack_watch.py \
  --dir /path/to/Takeout --dest /path/to/Unpacked --expected 18

# 4) After all parts: chronological sort + dedup + EXIF repair
gpth -i Unpacked -o Archive --divide-to-dates     # or gpto, see references/pitfalls.md
exiftool -overwrite_original -r -if 'not defined DateTimeOriginal' \
  -P "-AllDates<FileModifyDate" Archive/
```

## The two URL "worlds" (why most attempts fail)

| Endpoint | Behavior |
|---|---|
| `takeout.google.com/takeout/download?j=…&i=…` | **Always redirects to login/challenge** for CLI clients, even with valid session cookies. Do NOT use from CLI. |
| `takeout-download.usercontent.google.com/download/takeout-<TS>-1-<NNN>.zip?j=…&i=…&user=…` | Works from curl/aria2 **iff your cookie jar contains the usercontent-domain cookies** (HTTP 206, Range requests supported). |

Get the usercontent cookies by harvesting ALL browser cookies via CDP
(`Storage.getCookies` on the browser target — see `scripts/cdp_min.py`), not by
filtered per-URL requests.

## Hard-won pitfalls (full list in references/pitfalls.md)

1. **Cookie scope**: harvest ALL cookies (`Storage.getCookies`), not just takeout/accounts domains.
2. **Cookie rotation**: refresh before EVERY part; verify PK magic after EVERY part.
3. **Origin endpoint is a trap**: it 302s to a passkey challenge from CLI — that's Google
   requiring interactive identity confirmation, not a fixable header issue.
4. **Automation escalation**: repeated automated login attempts make Google treat your
   account as hijacked (password-reset emails, locked "other options"). Hard rule:
   after ANY account-recovery email, ALL login automation stops permanently — the human
   logs in once manually, the agent only downloads with fresh cookies afterwards.
5. **Chromium download control**: `Browser.cancelDownload` (CDP) and `chrome.send('cancel')`
   silently do nothing; closing tabs doesn't stop downloads. The only reliable control is
   the chrome://downloads WebUI shadow-DOM (Pause/Resume/Cancel buttons, numeric state
   field: 0=in progress, 3=interrupted, 5=canceled). **Chromium deletes `.crdownload`
   bytes on cancel — rename to `.part` BEFORE cancelling.**
6. **Time Machine / disk ejection**: backupd can rip the mount out from under a
   multi-day download. Pause TM (`tmutil stopbackup`, watchdog loop) for download nights.
7. **`ls` file size lies during aria2 multi-connection downloads** — files are
   sparse/preallocated. Trust aria2's progress summary or the `.aria2` control file.
8. **aria2 vs SIGSTOP**: `--max-overall-download-limit` throttles softly; `kill -STOP`
   freezes at 0 bytes/s (verified: 0 bytes during stop, instant resume on CONT).

## Workflow for agents

See `references/pitfalls.md` for the complete operational playbook (including the
browser-only fallback phases, the chrome://downloads shadow-DOM control snippets, and
the Google→iCloud direct-transfer flow with its three manual user steps).

## Security model (read before installing)

This skill handles **session cookies of a logged-in Google account**. That is inherent
to Takeout automation (Takeout itself is cookie-gated). The scripts are built to touch
the minimum:

- **Reads:** cookies via the local Chrome DevTools Protocol (localhost:9222) of YOUR
  browser, filtered to `*.google.com` / `*.googleusercontent.com` domains only —
  cookies of banks, shops and other services never leave the browser.
- **Writes:** a Netscape cookie jar (chmod 600) in `/tmp` (or `--jar` path), used only
  to talk to `takeout-download.usercontent.google.com` (i.e. Google). Delete it after
  the run — it is not needed for anything else.
- **Network:** only Google hosts are contacted. No telemetry, no third-party calls.
- **No login automation.** The scripts never type passwords, never click challenge
  flows, never touch 2FA. The one-time manual login is yours — and this is deliberate:
  automating it triggers Google's fraud detection and escalates account recovery.
- **Reviewable surface:** ~250 lines of Python across 3 scripts, no dependencies
  beyond `websockets`, no eval/exec, no subprocess curl-pipes. Read it.

## Credits & prior art

- **omgmog.net** — "Pulling Google Takeout straight to a NAS": first public write-up of
  the final-domain cookie insight and URL pattern construction (2026)
- **smashah's gist** — bash bulk downloader for Takeout (concurrent, progress)
- **nelsonjchen/gtr-proxy** — Cloudflare Worker injecting captured Takeout cookies
  (browser extension + proxy design)
- **TheLastGimbus/GooglePhotosTakeoutHelper (gpth)** — the organizing standard (5.7k★)
- **raultov/google-photos-takeout-organizer (gpto)** — Rust organizer with smart updates
- **jpratt9/gphotos-export** — undetected-browser per-photo download (different approach)

This skill's scripts are original work; the auth recipe builds on the community
insights above.

## License

MIT