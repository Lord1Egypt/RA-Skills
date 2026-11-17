# Google Photos Takeout → Local CLI Download Pipeline

**Stop babysitting Google Takeout downloads.** This agent skill turns the most painful
part of leaving Google Photos into a hands-off pipeline: session-bound URLs, rotating
cookies, hundreds of GB — handled by aria2c + a browser that only exists as a cookie
factory, with verification, immediate unpacking, throttling and crash-proof resume.

Built and battle-tested during a real **867 GB / 18-part migration** (Aug 2026),
including every way Google can say no.

```
Takeout job → [browser as cookie factory via CDP] → aria2c (throttle/resume)
            → per-part ZIP verification → immediate unpack → gpth/gpto sorting
```

## Why this exists

- Google killed the Photos API for backups (March 2025) — **Takeout is the only way**
  to get original-quality exports with metadata.
- Takeout download URLs are **session-bound and cookie-rotating**: naive curl gets
  HTML login pages, most people give up and click 18 downloads by hand.
- Existing tools organize zips *after* download (gpth, gpto) or scrape photo-by-photo
  (gphotos-export). Nobody documents the **complete automated bulk-download pipeline**
  with its failure modes — this skill does.

## Highlights

- Cookie harvesting via CDP `Storage.getCookies` (the full jar — the filtered version
  silently fails, see the #1 pitfall)
- URL pattern construction: one ripped URL → all 18 part URLs
- Per-part cookie refresh + `PK`-magic + size verification (kills the
  "downloaded 1.2 MB HTML instead of 50 GB ZIP" failure mode)
- Self-healing: relaunches the browser if closed; `.aria2` files resume after crashes
- Immediate unpack watchdog with disk-budget logic (1× instead of 2× library size)
- Soft throttle (`aria2` limit) and hard pause (`SIGSTOP`, 0 bytes/s) without byte loss
- Time Machine watchdog for multi-day download nights (macOS)
- Bonus: the official **Google → iCloud direct transfer** flow (server-side,
  zero bandwidth) that almost nobody knows exists

## Install

```bash
# macOS
brew install aria2 unzip exiftool
pip3 install websockets
# Linux
# apt install aria2 unzip libimage-exiftool-perl
```

Launch your Chromium browser with remote debugging and log into Google **manually**
(automation of logins triggers Google's fraud detection — don't):

```bash
open -a "Google Chrome" --args --remote-debugging-port=9222
```

## Usage

```bash
# 1) Start ONE part's download on takeout.google.com/manage, then:
python3 scripts/discover_url.py --out /tmp/takeout_url.txt

# 2) Parse it and bulk-download everything (5 MB/s, per-part cookie refresh):
#    (job id, user id and timestamp are in the ripped URL)
python3 scripts/takeout_download.py \
  --job <JOB> --user <USERID> --ts 20260827T130928Z \
  --total 18 --dir /volume/Takeout --limit 5M

# 3) In a second terminal — unpack each part as it lands:
python3 scripts/takeout_unpack_watch.py --dir /volume/Takeout \
  --dest /volume/Unpacked --expected 18

# 4) After all parts: sort chronologically + fix EXIF
gpth -i Unpacked -o Archive --divide-to-dates
exiftool -overwrite_original -r -if 'not defined DateTimeOriginal' \
  -P "-AllDates<FileModifyDate" Archive/
```

## Documentation

- `SKILL.md` — the full skill (agent-readable instructions), incl. the security model
- `references/pitfalls.md` — the complete battle-tested playbook:
  auth/cookie traps, Chromium download control via shadow-DOM, fraud-detection
  escalation rules, macOS mount zombies, aria2 subtleties, EXIF repair, and the
  Google→iCloud transfer flow

## Security model

Short version: cookies of YOUR Google account are read from YOUR browser via the
local CDP port, **filtered to `*.google.com` domains only**, written to a chmod-600
jar, sent only to Google's download host, safe to delete after the run. No login
automation (deliberate — it triggers Google's fraud detection), no telemetry, no
third-party network calls, ~250 lines of reviewable Python. Details in SKILL.md.

## Credits & prior art

- [omgmog.net — Pulling Google Takeout straight to a NAS](https://blog.omgmog.net/post/downloading-google-takeout-to-a-nas/) (final-domain cookie insight, URL construction)
- [smashah's gist](https://gist.github.com/smashah/67863f6c5f500c9098ad7c7e74eefc11) (bash bulk downloader)
- [nelsonjchen/gtr-proxy](https://github.com/nelsonjchen/gtr-proxy) (cookie-injecting proxy + extension)
- [TheLastGimbus/GooglePhotosTakeoutHelper](https://github.com/TheLastGimbus/GooglePhotosTakeoutHelper) (organizing standard)
- [raultov/google-photos-takeout-organizer](https://github.com/raultov/google-photos-takeout-organizer) (gpto, smart updates)

## License

MIT