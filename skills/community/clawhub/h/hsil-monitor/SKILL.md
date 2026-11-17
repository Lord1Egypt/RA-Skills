---
name: hsil-monitor
version: 1.0.1
description: >
  Monitor Hang Seng Indexes (hsi.com.hk) press releases, index/other notices, insights, and reports; detect newly published items, match them bilingually (EN + 中文) against the user's indexes (default HSI/HSCEI/HSTECH), and produce one concise digest per run. Use when the user wants to watch HSI announcements or run a scheduled Hang Seng Indexes news check. Agent-driven, no Python or compiled code — only curl, jq, and standard shell tools.
---
# HSIL Monitor (agent-native, zero-code)

You (the agent) perform the whole cycle by following this document: fetch the
Hang Seng Indexes sources, detect what is new since last run, decide what is
relevant, and emit a digest as your final message. **You do not send or route
the message** — OpenClaw delivers your output (the scheduled job's announce
routing). This skill contains no channel and no credentials.

Tools used: `curl`, `jq`, and coreutils (`sort`, `awk`, `sed`, `date`, `mv`).

## Storage — READ THIS FIRST

All reads and writes happen in **one writable, per-user home directory**, never
in the skill's install folder (that folder may be read-only and its location is
not reliably discoverable from a shell command). This matches the convention
other OpenClaw skills use (`~/.config/<skill>/`).

Resolve the SAME paths at the very start of **every** action (setup, run,
backfill, doctor) with this exact block — it is a deterministic rule, so the
skill always knows where its files are without discovery or a pointer file:

```bash
HOME_DIR="${HSIL_MONITOR_HOME:-$HOME/.config/hsil-monitor}"
WORK="$HOME_DIR/work"
mkdir -p "$WORK"
CFG="$HOME_DIR/config.json"     # settings
SEEN="$HOME_DIR/seen.txt"       # dedup state: one seen item URL per line
LAST="$HOME_DIR/last_run.txt"   # ISO-8601 UTC timestamp of last run
UA="Mozilla/5.0 hsil-monitor"
```

- `$HSIL_MONITOR_HOME` overrides the location; otherwise it defaults to
  `~/.config/hsil-monitor`, writable on any machine and surviving reinstalls.
- **All scratch files go in `$WORK`** (not `/tmp`), so a locked-down `/tmp`
  can't break the skill. Clean `$WORK` at the start of each run.
- Write config/state atomically: write `"$CFG.tmp"`, then `mv "$CFG.tmp" "$CFG"`.
- Do **not** use `$0`/`dirname` to find a path, and do **not** write inside the
  skill folder.

## What lives where

- `config.json` (in `$HOME_DIR`) — settings, created at setup. Schema:
  ```json
  {
    "timezone": "Asia/Hong_Kong",
    "schedule_time": "08:30",
    "languages": ["en", "zh"],
    "indexes": ["HSI", "HSCEI", "HSTECH"],
    "extra_keywords": [],
    "backfill_days": 30,
    "deep_read": false,
    "sources": [
      {"type": "Press release", "page": "https://www.hsi.com.hk/en-hk/media-room/#press-releases",     "tab_title": "Press Releases"},
      {"type": "Notice",        "page": "https://www.hsi.com.hk/en-hk/media-room/#index-other-notices", "tab_title": "Index / Other Notices"},
      {"type": "Insight",       "page": "https://www.hsi.com.hk/en-hk/insights-and-reports/#insights",   "tab_title": "Insights"},
      {"type": "Report",        "page": "https://www.hsi.com.hk/en-hk/insights-and-reports/#reports",    "tab_title": "Reports"}
    ]
  }
  ```
  The four source **pages** are the only fixed site locations; the JSON data
  endpoints are discovered at runtime from each page's model. `config.example.json`
  in the skill folder is a read-only reference copy of this schema.

Delivery is intentionally absent: the skill emits text; OpenClaw routes it.

---

# PROCEDURE — one monitoring cycle ("run")

### 1. Resolve storage, load config, prep state
```bash
HOME_DIR="${HSIL_MONITOR_HOME:-$HOME/.config/hsil-monitor}"; WORK="$HOME_DIR/work"
mkdir -p "$WORK"; CFG="$HOME_DIR/config.json"; SEEN="$HOME_DIR/seen.txt"; LAST="$HOME_DIR/last_run.txt"
UA="Mozilla/5.0 hsil-monitor"
[ -f "$CFG" ] || { echo "No config at $CFG — run setup first."; exit 1; }
BACKFILL_DAYS=$(jq -r '.backfill_days // 30' "$CFG")
: > "$WORK/all.tsv"
touch "$SEEN"
FIRST_RUN=0; [ -s "$SEEN" ] || FIRST_RUN=1
```

### 2. For each source: discover data endpoints, then fetch items
Always fetch to a file and **validate it is JSON before piping to `jq`**. Some
networks return an HTML bot/geo/WAF challenge or a redirect with HTTP 200;
feeding that to `jq` causes a `jq: parse error`. Validate first, skip-with-warning.
Rows are TSV: `type <TAB> date <TAB> absolute_url <TAB> title`.
```bash
jq -c '.sources[]' "$CFG" | while read -r S; do
  TYPE=$(jq -r '.type' <<<"$S"); PAGE=$(jq -r '.page' <<<"$S"); TAB=$(jq -r '.tab_title' <<<"$S")
  MODEL="$(printf '%s' "$PAGE" | sed 's/#.*$//; s#/\{0,1\}$##').model.json"

  curl -sSL --retry 2 --max-time 30 -A "$UA" -H 'Accept: application/json' -o "$WORK/model.json" "$MODEL"
  if ! jq -e . "$WORK/model.json" >/dev/null 2>&1; then
    echo "WARN: model not JSON for '$TAB' ($MODEL) — block or drift; skipping source" >&2; continue
  fi
  PATHS=$(jq -r --arg t "$TAB" '.. | objects | select(has("tabs")) | .tabs[]
            | select(.tabTitle==$t) | .sourceConfigs[]?.customDataPath' "$WORK/model.json" | sort -u)
  [ -z "$PATHS" ] && echo "WARN: no data paths discovered for '$TAB'" >&2

  for P in $PATHS; do
    U="https://www.hsi.com.hk$P"
    code=$(curl -sSL --retry 2 --max-time 30 -A "$UA" -H 'Accept: application/json' -o "$WORK/src.json" -w '%{http_code}' "$U")
    if [ "$code" != 200 ] || ! jq -e . "$WORK/src.json" >/dev/null 2>&1; then
      echo "WARN: skipped $P (http $code / not JSON) — first bytes: $(head -c 80 "$WORK/src.json" | tr -d '\n')" >&2
      continue
    fi
    jq -r --arg t "$TYPE" '(.contentList // [])[]? | (.resourcesList // [])[]?
        | select(.title != null)
        | [$t, (.lastUpdate[0:10]), ("https://www.hsi.com.hk" + .url), .title] | @tsv' \
      "$WORK/src.json" >> "$WORK/all.tsv"
  done
done
sort -u -o "$WORK/all.tsv" "$WORK/all.tsv"
```
Resilience: a bad/blocked/malformed file is skipped with a `WARN` (surface these
in the digest's health line); only treat the run as broken if *every* fetch
failed. The `// []` guards mean an unexpected shape yields no rows, not an error.

### 3. Compute new items (dedup by URL, column 3)
Read the seen-set in `BEGIN` via `getline` so it is correct even when `$SEEN` is
empty (the `NR==FNR` trick breaks on an empty first file):
```bash
awk -F'\t' -v seenf="$SEEN" 'BEGIN{while((getline l < seenf) > 0) seen[l]=1} !($3 in seen)' \
  "$WORK/all.tsv" > "$WORK/new.tsv"
```

### 4. First-run backfill window
On the first run (`$SEEN` empty) narrow what you *report* to the recent window;
you still seed **all** fetched URLs in step 8, so later runs only show newer items:
```bash
if [ "$FIRST_RUN" = 1 ]; then
  CUT=$(date -u -d "-${BACKFILL_DAYS} days" +%F 2>/dev/null || date -u -v-"${BACKFILL_DAYS}"d +%F)
  awk -F'\t' -v c="$CUT" '$2 >= c' "$WORK/new.tsv" > "$WORK/show.tsv"
else
  cp "$WORK/new.tsv" "$WORK/show.tsv"
fi
```

### 5. Read the candidates and match (you do this — no code)
`cat "$WORK/show.tsv"` — small, only new items. For each row decide which of the
user's indexes it concerns, per MATCHING RULES below. Record matched index codes
and the language matched. (Optional bilingual recall: also fetch the Chinese data
files — same paths with `/data/eng/` → `/data/chi/` — and match titles by URL
filename stem. English titles usually already carry the tickers.)

### 6. Optional deep-read
If `config.deep_read` is `true`, for up to ~5 **matched** PDF items you may
`curl -sSL "<url>" -o "$WORK/item.pdf"` and read it for a one-sentence summary.
Skip silently if you cannot read PDFs. Never deep-read unmatched items.

### 7. Compose the digest (your final message)
Group **matched** items by source type in this order: Press release, Notice,
Insight, Report (all equal weight). Collapse unmatched-new into a count. Use the
DIGEST FORMAT below. If there are no matched items and no warnings, output one
short line (e.g. `HSIL monitor: no new matched items today (checked N sources).`).
**Emit the digest as your final response — do not send it anywhere.**

### 8. Persist state (atomic)
Seed every URL fetched this run so nothing re-alerts:
```bash
cut -f3 "$WORK/all.tsv" >> "$SEEN"
sort -u "$SEEN" -o "$SEEN"
date -u +%FT%TZ > "$LAST"
```

---

# MATCHING RULES (bilingual)

Match each new item's title (and Chinese title / deep-read text if available)
against the configured indexes:

| Index | English | 中文 (Traditional + Simplified) |
|---|---|---|
| **HSI** | `HSI`, `Hang Seng Index` | `恒生指數`, `恒生指数` |
| **HSCEI** | `HSCEI`, `Hang Seng China Enterprises Index`, `China Enterprises Index` | `恒生中國企業指數`, `恒生中国企业指数`, `國企指數`, `国企指数` |
| **HSTECH** | `HSTECH`, `HSTI`, `Hang Seng TECH Index`, `Hang Seng TECH` | `恒生科技指數`, `恒生科技指数`, `科技指數` |

Plus any `extra_keywords`. Guidance:
- Treat English abbreviations (`HSI`, `HSTECH`) as whole tokens, not substrings.
- **Exclude the publisher's own name.** "Hang Seng Indexes Company / Limited",
  "恒生指數公司", "恒生指數有限公司" appear in almost every title and must **not**
  by themselves count as an HSI match. Count HSI only when the title refers to
  the *index* (e.g. "Hang Seng Index Advisory Committee", "恒生指數半年度檢討").
- An "Index Review Results" / "指數檢討結果" item names indexes in its PDF body —
  if `deep_read` is on, use that; otherwise leave it in the unmatched-new count.
- Record matches like `HSTECH (en)` or `恒生科技指數 (zh)`.

---

# DIGEST FORMAT (plain text)

```
Hang Seng Indexes — Daily Digest
<YYYY-MM-DD HH:MM TZ>            # now, in config.timezone

⚠ HEALTH: <only if a source failed / structure drift / all-empty>

New: Press <n> · Notice <n> · Insight <n> · Report <n>

── Press release (<k>) ──
• <title>
  <date> · <tag if any> · matched: <labels>
  中文: <chinese title if fetched>
  "<one-line summary if deep-read>"
  <url>
... (Notice, Insight, Report in that order) ...

(+ <m> other new item(s) not matching your indexes)

Health: OK ✅   # or: SEE ALERTS ABOVE ⚠
```

---

# PROCEDURE — setup (agent-led)

You are the interactive layer: **ask the user, then write `config.json`.**

1. Resolve storage and prove it is writable; tell the user where files will live:
   ```bash
   HOME_DIR="${HSIL_MONITOR_HOME:-$HOME/.config/hsil-monitor}"; mkdir -p "$HOME_DIR/work"
   if ! ( : > "$HOME_DIR/.wtest" && rm -f "$HOME_DIR/.wtest" ); then
     echo "ERROR: $HOME_DIR is not writable. Set HSIL_MONITOR_HOME to a writable path and re-run setup." ; exit 1
   fi
   echo "Config + state will be stored in: $HOME_DIR"
   ```
   Report that path to the user in chat.
2. Run DOCTOR and report gaps.
3. Ask (offer defaults): timezone; daily time; indexes; extra keywords; bilingual
   or English-only; backfill days (default 30); deep-read on/off.
4. Write `$HOME_DIR/config.json` from the schema above with their answers, using
   `jq` and an atomic `mv` (write `config.json.tmp`, then `mv`).
5. Offer to run a **backfill** now (BACKFILL below).
6. Offer to install the **schedule** (SCHEDULE below). Confirm before creating.

# PROCEDURE — backfill

Run one normal cycle with `FIRST_RUN` forced to 1 so only the recent
`backfill_days` window is reported, then all history is seeded into `$SEEN`.
Emit the windowed digest as your final message.

# PROCEDURE — schedule

Create a daily OpenClaw cron job that triggers this skill. Read `schedule_time`
and `timezone` from config, convert `HH:MM` → cron `M H * * *`, confirm with the
user, then run — **embedding the resolved storage path in the message** so every
scheduled run uses the exact same location:
```bash
HOME_DIR="${HSIL_MONITOR_HOME:-$HOME/.config/hsil-monitor}"
openclaw cron add \
  --name hsil-monitor-daily \
  --description "Daily Hang Seng Indexes digest" \
  --cron "<M> <H> * * *" \
  --tz "<timezone>" \
  --tools exec \
  --announce \
  --message "Run the hsil-monitor skill now: set HSIL_MONITOR_HOME=$HOME_DIR, perform one monitoring cycle exactly as its SKILL.md describes, and output the digest as your final message."
```
Delivery/routing is OpenClaw's responsibility (`--announce`); this skill names no
channel. Inspect with `openclaw cron list`; remove with
`openclaw cron rm --name hsil-monitor-daily`.

# PROCEDURE — doctor

Report PASS/WARN/FAIL for:
- `command -v curl jq` — required tools.
- **Write access to `$HOME_DIR`** (write a temp file there and delete it).
- Reachability + discovery: for one source, derive the model URL and confirm the
  `customDataPath` discovery returns ≥1 path and the data file parses as JSON.
- `command -v openclaw` — needed only for scheduling.
- Whether `$HOME_DIR/config.json` exists (else: run setup).

---

# Notes & guarantees

- **One writable home** (`$HOME/.config/hsil-monitor`, override `HSIL_MONITOR_HOME`)
  holds config, state, and scratch. Nothing is read/written in the skill folder,
  and the path is known by rule at every run — no `$0`, no discovery, no pointer.
- **Portable / no hardcode:** only the four source *pages* are fixed (in config);
  data endpoints are discovered each run. No credentials, no channel.
- **Idempotent:** dedup is by item URL in `seen.txt`; re-running never re-reports.
- **Fails soft:** a blocked/broken source is skipped with a health warning.
- **Quiet by design:** quiet days produce a one-line message, not silence/noise.
