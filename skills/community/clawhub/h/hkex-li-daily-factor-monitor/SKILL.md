---
name: hkex-li-daily-factor-monitor
version: 1.0.0
description: >
  Fetch the latest HKEXnews "Daily Targeted Leverage Factor" announcement(s) for HKEX-listed Leveraged & Inverse (L&I) products, extract each product's daily targeted leverage factor from the announcement PDF, and emit a human-readable Telegram digest — product rows in a monospace code block grouped by applicable date, with source PDF links below — ready to display in the OpenClaw channel. Use for daily manual runs or a scheduled cron check of the next trading day's L&I factors. Agent-native: curl + jq for discovery, pdftotext for PDF text, the agent reasons out the factor table. PDFs are downloaded per-run and deleted after parsing (HKEX PDFs are copyrighted).
---
# HKEX L&I Daily Factor Monitor  (internal id: `hkex_li_daily_factor_monitor`)

You (the agent) perform the whole cycle by following this document: discover the
most recent HKEXnews "Daily Targeted Leverage Factor" announcement(s) for L&I
products, download and read their PDFs, extract each product's daily targeted
leverage factor, then **emit a human-readable Telegram digest — product rows in a
monospace code block, grouped by applicable date, with source URLs below** as your
final message. You do
not route or send it — OpenClaw delivers your output (a scheduled job's announce
routing). This skill contains no channel and no credentials.

Tools used: `curl`, `jq`, `pdftotext` (poppler-utils), coreutils (`date`, `sort`,
`awk`, `sed`, `mv`, `rm`). `python3` is used **only** as a PDF-text fallback when
`pdftotext` is absent (see `scripts/pdf_to_text.py`).

## Design principles (why it is built this way)
- **Agent-native extraction.** The factor table is read by you from the PDF text,
  using the heuristics below — not by brittle fixed-offset parsing. HKEX wording
  drifts; your reasoning absorbs that.
- **Structured metadata + PDF prose, combined.** The HKEXnews search record gives
  the authoritative `stock_code ↔ short_name` pairs; the PDF gives the applicable
  trading date and each product's factor. You join them.
- **Copyright-safe.** PDFs are downloaded for the current run only and every file
  in the scratch dir is deleted at the end. Only the extracted factor digest survives.
- **Portable / no hard-coding.** All URLs, the endpoint, the headline keyword, the
  category gate, and the scratch dir live in one config block — never scattered
  through the steps. No user-specific paths, no credentials.

---

## Storage & config — RESOLVE THIS FIRST

All reads/writes happen in **one writable, per-user home directory**, never in the
skill's install folder (which may be read-only and is not reliably discoverable
from a shell). Resolve the SAME paths at the start of **every** action (run, setup,
doctor) with this exact block:

```bash
HOME_DIR="${HKEX_LI_MONITOR_HOME:-$HOME_DIR_DEFAULT}"
mkdir -p "$HOME_DIR"
CFG="$HOME_DIR/config.json"          # settings (created at setup; falls back to skill's config.example.json)
```

- `$HKEX_LI_MONITOR_HOME` overrides the location; else it defaults to
  `~/.config/hkex-li-daily-factor-monitor` (or `$HOME/.config/...` on most systems),
  writable on any machine and surviving reinstalls.
- The scratch dir for PDFs comes from `config.tmp_dir` (default
  `/tmp/hkex_li_daily_factor_monitor`). If `/tmp` is locked down, set `tmp_dir` to
  `"$HOME_DIR/work"`. **Everything in the scratch dir is deleted at end of run.**
- Do **not** use `$0`/`dirname` to find paths, and do **not** write in the skill
  folder.

### Config schema
Full annotated reference: `config.example.json` in the skill folder. Schema:

```json
{
  "hkex_base_url": "https://www1.hkexnews.hk",
  "hkex_search_endpoint": "/search/titleSearchServlet.do",
  "hkex_search_params": {
    "sortDir": "0", "sortByOptions": "DateTime", "category": "0",
    "market": "SEHK", "stockId": "-1", "documentType": "-1",
    "searchType": "0", "t": "-1", "lang": "EN", "rowRange": "2000"
  },
  "headline_keyword": "Daily Targeted Leverage Factor",
  "category_keyword": "Matters relating to Collective Investment Schemes",
  "product_type": "L&I",
  "days_back": 7,
  "run_mode": "latest",
  "tmp_dir": "/tmp/hkex_li_daily_factor_monitor",
  "user_agent": "Mozilla/5.0 (compatible; hkex-li-daily-factor-monitor)"
}
```

Load config, falling back to the skill's example copy if the user hasn't run setup:
```bash
if [ -f "$CFG" ]; then SRC="$CFG"; else SRC="config.example.json"; fi   # example is a valid, working default
BASE=$(jq -r '.hkex_base_url'        "$SRC")
EP=$(jq -r   '.hkex_search_endpoint' "$SRC")
KW=$(jq -r   '.headline_keyword'     "$SRC")
CAT=$(jq -r  '.category_keyword'     "$SRC")
PTYPE=$(jq -r '.product_type'        "$SRC")
DAYS=$(jq -r '.days_back // 7'       "$SRC")
RUNMODE=$(jq -r '.run_mode // "latest"' "$SRC")
TMP=$(jq -r  '.tmp_dir'              "$SRC")
UA=$(jq -r   '.user_agent'           "$SRC")
QS=$(jq -r '.hkex_search_params | to_entries | map("\(.key)=\(.value)") | join("&")' "$SRC")
```
Run-time overrides (optional): the invoking message may set `days_back` or
`run_mode` (`latest` | `all`); prefer those over config when present.

---

# READINESS CHECK  (run once on a new machine, and as `doctor`)

Report PASS / FAIL for each; if anything required is missing, **stop and return a
clear error listing exactly what is missing** — do not attempt a partial run.

```bash
# 1. Required tools
for t in curl jq; do command -v "$t" >/dev/null || echo "FAIL: missing required tool '$t'"; done
# 2. PDF text: pdftotext preferred; python3 fallback acceptable
if command -v pdftotext >/dev/null; then echo "PASS: pdftotext"; \
elif command -v python3 >/dev/null; then echo "PASS: python3 fallback (scripts/pdf_to_text.py)"; \
else echo "FAIL: need pdftotext (poppler-utils) OR python3 for PDF text extraction"; fi
# 3. Outbound HTTPS connectivity
curl -sS -o /dev/null -m 20 -A "$UA" -w "hkexnews: HTTP %{http_code}\n" https://www1.hkexnews.hk/ \
  || echo "FAIL: cannot reach https://www1.hkexnews.hk"
curl -sS -o /dev/null -m 20 -A "$UA" -w "sfc:      HTTP %{http_code}\n" https://apps.sfc.hk/ \
  || echo "WARN: cannot reach https://apps.sfc.hk (not needed today; reserved for future extension)"
# 4. Writable home + scratch
( : > "$HOME_DIR/.wtest" && rm -f "$HOME_DIR/.wtest" ) || echo "FAIL: $HOME_DIR not writable (set HKEX_LI_MONITOR_HOME)"
mkdir -p "$TMP" 2>/dev/null && ( : > "$TMP/.wtest" && rm -f "$TMP/.wtest" ) || echo "FAIL: tmp_dir '$TMP' not writable (set config.tmp_dir)"
```
A 30x/200 from hkexnews counts as reachable. `apps.sfc.hk` is a soft check kept
for a possible future SFC cross-reference; its failure is a WARN, not a FAIL.

---

# PROCEDURE — one run

## Step 1 — Resolve storage & load config
Run the storage block and the config-load block above. Then prepare a clean
scratch dir and register cleanup so PDFs are removed even if a later step fails:
```bash
mkdir -p "$TMP"; rm -f "$TMP"/*.pdf 2>/dev/null   # start clean
trap 'rm -f "$TMP"/*.pdf 2>/dev/null' EXIT        # belt-and-braces cleanup (also done explicitly in Step 6)
```

## Step 2 — Discover the latest relevant announcement(s)
Query a recent **date window** (not the servlet's `title=` param — free text there
returns 0 because it expects exact document-type codes), then filter the returned
records client-side on the headline keyword AND the CIS category. This is resilient
to HKEX category-code drift.

```bash
TODAY=$(date +%Y%m%d)
FROM=$(date -d "-${DAYS} days" +%Y%m%d 2>/dev/null || date -v-"${DAYS}"d +%Y%m%d)
URL="${BASE}${EP}?${QS}&fromDate=${FROM}&toDate=${TODAY}&title="
curl -sSL -m 60 -A "$UA" -H 'Accept: application/json' -o "$TMP/discover.json" -w '%{http_code}' "$URL" > "$TMP/http_code"
[ "$(cat "$TMP/http_code")" = 200 ] && jq -e . "$TMP/discover.json" >/dev/null 2>&1 \
  || { echo "ERROR: discovery request failed (HTTP $(cat "$TMP/http_code")) at ${BASE}${EP} — step: discover"; exit 1; }

# One TSV row per matching announcement:
#   DATE_TIME <TAB> FILE_LINK <TAB> code1|code2|... <TAB> name1|name2|... <TAB> TITLE
jq -r --arg kw "$KW" --arg cat "$CAT" '
  (.result | fromjson) as $r
  | $r[]
  | select((.TITLE    // "" | ascii_downcase | contains($kw  | ascii_downcase)))
  | select((.LONG_TEXT // "" | ascii_downcase | contains($cat | ascii_downcase)))
  | [ .DATE_TIME,
      .FILE_LINK,
      (.STOCK_CODE // "" | gsub("<br/>";"|")),
      (.STOCK_NAME // "" | gsub("<br/>";"|")),
      .TITLE ]
  | @tsv
' "$TMP/discover.json" | sort -t$'\t' -k1,1r > "$TMP/matches.tsv"   # newest first
```

**Empty result → explicit error (do not emit an empty digest):**
```bash
if [ ! -s "$TMP/matches.tsv" ]; then
  rm -f "$TMP"/*.pdf 2>/dev/null
  echo "No Daily Targeted Leverage Factor announcements found in the recent HKEXnews window under OTHERS (FUNDS, ETC)." >&2
  exit 1
fi
```

**`run_mode` selection:**
- `latest` (default): keep, for each **distinct set of stock codes** (col 3), only
  the newest-dated row. Different managers/product families each publish their own
  announcement daily, so "latest" = the newest factor for every product currently
  publishing, not literally one file. De-dup:
  ```bash
  awk -F'\t' '!seen[$3]++' "$TMP/matches.tsv" > "$TMP/selected.tsv"   # rows are already newest-first
  ```
- `all`: use every row — `cp "$TMP/matches.tsv" "$TMP/selected.tsv"`.

`cat "$TMP/selected.tsv"` — this is your work list (small).

## Step 3 — Download & extract each selected PDF
For each row in `selected.tsv` (fields: `DATE_TIME`, `PDF_PATH`, `CODES` (`|`),
`NAMES` (`|`), `TITLE`):

```bash
ABS_URL="${BASE}${PDF_PATH}"                       # e.g. https://www1.hkexnews.hk/listedco/.../2026080700828.pdf
FN="$TMP/$(basename "$PDF_PATH")"
code=$(curl -sSL -m 90 -A "$UA" -o "$FN" -w '%{http_code}' "$ABS_URL")
[ "$code" = 200 ] && [ -s "$FN" ] \
  || { echo "ERROR: PDF download failed — url=$ABS_URL http=$code — step: download"; exit 1; }

# Extract text: pdftotext -layout preserves the product/factor columns best.
if command -v pdftotext >/dev/null; then
  pdftotext -layout "$FN" "$FN.txt" 2>/dev/null || { echo "ERROR: pdftotext failed — url=$ABS_URL — step: parse"; exit 1; }
else
  python3 scripts/pdf_to_text.py "$FN" > "$FN.txt" || { echo "ERROR: python fallback parse failed — url=$ABS_URL — step: parse"; exit 1; }
fi
[ -s "$FN.txt" ] || { echo "ERROR: empty PDF text — url=$ABS_URL — step: parse"; exit 1; }
```

Then **you read `"$FN.txt"`** and extract, per the heuristics below.

### Extraction heuristics (you do this — reason over the text)
These are documented assumptions; apply judgement, don't hard-match positions.

1. **Applicable trading date** — take it from the PDF prose, NOT by assuming "next
   day". Look for: `applicable for <D Month YYYY>` / `applicable for the <D Month
   YYYY>` (e.g. "applicable for 10 August 2026"). Convert to ISO `YYYY-MM-DD`
   (→ `2026-08-10`). This date applies to every product in that PDF. If two dates
   appear, use the one attached to "Daily targeted leverage factor ... applicable
   for".
2. **Product → stock code(s)** — the header lists each product with its code(s):
   ```
   CSOP Samsung Electronics Daily Max (2x) Leveraged Product
        USD Counter Stock Code: 09747
        HKD Counter Stock Code: 07747
   CSOP Samsung Electronics Daily Max (-2x) Inverse Product
        Stock Code: 07347 (HKD Counter)
   ```
   A product may have **two** counters (USD + HKD) → two stock codes that share the
   same factor. Some products have a single counter.
3. **Product → factor** — a table maps each product name to a factor written as
   `2x`, `-2x`, `1.5x`, `-1x`, etc. Parse to a signed decimal: `2x → 2.0`,
   `-2x → -2.0`, `1.5x → 1.5`. Layout may wrap a long product name across lines
   with the factor on the right — match by product name, not line number.
4. **stock_code → short_name** — take these pairs from the announcement METADATA
   (the `CODES` and `NAMES` `|`-lists from Step 2, positionally aligned), which is
   authoritative. Cross-check that every metadata code appears in the PDF header;
   note (but don't fail on) any mismatch. Zero-pad codes to 5 digits as HKEX does
   (`7347 → 07347`).
5. **Emit one record per stock_code** (so USD and HKD counters are separate rows
   sharing the product's factor). Set `product_type` from config (`"L&I"`).
6. If you locate the announcement and its date but genuinely cannot resolve a
   factor for a code, that is a parse failure — **raise an explicit error** naming
   the PDF URL and the failing code (Step: pattern-extraction); do not silently
   drop it.

## Step 4 — Note the fields you extracted (in your head — no JSON)
**Do NOT emit JSON.** The only output of this skill is the Telegram digest in
Step 5. Just keep track of these facts per stock code so you can render that digest:
- **stock_code** — 5-digit HKEX code (e.g. `07347`).
- **short_name** — from the announcement metadata (e.g. `XL2CSOPSMSN-U`).
- **targeted_leverage_factor** — signed decimal, at least one decimal place
  (`2.0`, `-1.0`, `1.5`, `-2.0`); Step 5 renders it as `2.0x` / `-2.0x`.
- **date** — ISO trading date the factor applies to (from the PDF).
- **source_pdf_url** — absolute; listed in the Step 5 Sources block per announcement.
- **announcement_timestamp** — the record's `DATE_TIME`, Hong Kong time.

Also hold `run_mode` and the count of announcements/products for the header line.
There is no structured-payload output and no downstream JSON consumer — a raw JSON
dump in the channel is a **mistake**, not an acceptable alternative to the digest.

## Step 5 — Output (your final message) — Telegram monospace digest
The channel is Telegram. Emit a **plain-text digest with the product rows inside a
```code block``` so columns stay aligned** (Telegram renders code blocks in a
monospace font; it does NOT render pipe tables or `<details>`). Put source URLs
**below** the code block as plain lines — links inside a code block are not
clickable. Emit exactly this shape, nothing before the title:

    HKEX L&I — Daily Targeted Leverage Factor
    <generated_at, HKT> · <N> announcement(s) · <M> product(s) · mode: <run_mode>
    ```
    Applicable <YYYY-MM-DD>
    XI2CSOPSMSN     -2.0x  07347
    XL2CSOPHYNIX     2.0x  07709
    XL2CSOPSMSN      2.0x  07747
    XL2CSOPSMSN-U    2.0x  09747

    Applicable <YYYY-MM-DD>
    XI2CSOPCOIN     -2.0x  07311
    XL2CSOPCOIN      2.0x  07711
    ... (every remaining short name, one row per name) ...
    ```
    Sources:
    • <YYYY-MM-DD> → <absolute source_pdf_url>
    • <YYYY-MM-DD> → <absolute source_pdf_url>

Digest rendering rules:
- **One row per short name — group stock codes by `short_name`.** A product's HKD
  and USD counters can share one short name; when they do, put every code for that
  name on the one row, comma-separated in the trailing codes column
  (e.g. `XL2CSOPSMSN      2.0x  07747, 09747`). All codes under one short name carry
  the same factor.
- **One code block for all rows.** Inside it, group by applicable `date`: a
  `Applicable <date>` header line, its rows, then a blank line before the next date.
  Sort date groups ascending.
- **Sort rows by stock code, smallest first.** Order the rows within a date by each
  name's **smallest** stock code (its reference code). So `07347` precedes `07709`,
  and a `09xxx`-only name sorts after the `07xxx` names. (Rows are name-led for
  readability, but the *order* is by code — easy to scan to a code.)
- **Narrow-friendly columns (monospace):** `<short_name>  <factor>  <codes>` — no
  leading space; `short_name` left-justified padded to the width of the longest
  short name in the run, two spaces, `factor` right-justified (width 6) so signs
  line up, two spaces, the code(s). Keep lines short (≈26 chars for a single code)
  so they fit a phone without horizontal scrolling; pad with spaces only, no tabs.
- **Factor:** number with sign + `x` suffix — `2.0x`, `-2.0x`, `1.5x`. Keep the
  `.0`. Use a plain hyphen `-` for the minus (renders reliably in Telegram mono).
- **Header line:** `N` = count of announcements, `M` = total products (count every
  stock code, so a 2-code name counts as 2). Timestamp in Hong Kong time.
- **Sources block:** one bullet per distinct announcement PDF (its applicable date
  → absolute URL), placed **after** the code block so the URLs are tappable and can
  wrap (URLs inside a code block are neither).
- **Size guard (Telegram 4096-char limit):** a normal run (tens of products) fits
  easily. If the digest would exceed ~3900 chars, split into one message per
  `Applicable <date>` section (each its own titled code block) rather than
  truncating — never cut a message mid-table.
- **Quiet is impossible here** — with no matches you already exited via ERROR
  HANDLING; you never reach Step 5 with an empty result.

## Step 6 — Cleanup & exit
Delete all downloaded PDFs and extracted text; retain nothing (copyright):
```bash
rm -f "$TMP"/*.pdf "$TMP"/*.txt "$TMP"/discover.json "$TMP"/matches.tsv "$TMP"/selected.tsv "$TMP"/http_code 2>/dev/null
```
The `EXIT` trap from Step 1 also removes PDFs if the run aborted early.

---

# ERROR HANDLING (explicit, never silent)
The user prefers loud failures over quiet gaps.
- **No matches in window** → error string (verbatim):
  `No Daily Targeted Leverage Factor announcements found in the recent HKEXnews window under OTHERS (FUNDS, ETC).`
- **PDF failure** → error naming the **PDF URL** and which step failed:
  `download` (HTTP/empty), `parse` (pdftotext/python failed or empty text), or
  `pattern-extraction` (found the doc but couldn't resolve a factor/date/code).
- **Discovery request failure** (non-200 / non-JSON) → error naming the endpoint
  and HTTP code.
- On any error, still run the PDF cleanup, then exit non-zero. Do not emit a
  partial/empty digest as if it were a successful result.

---

# PROCEDURE — setup (agent-led)
1. Resolve `$HOME_DIR`, prove it is writable, and tell the user the exact path
   where config/state will live.
2. Run the READINESS CHECK and report gaps.
3. Confirm/ask (offer defaults): `days_back` (7), `run_mode` (`latest`),
   `headline_keyword`, `category_keyword`, `tmp_dir`.
4. Write `$HOME_DIR/config.json` from the schema atomically (write
   `config.json.tmp`, then `mv`). Seed it from `config.example.json`.
5. Offer to install the schedule (below); confirm before creating.

# PROCEDURE — schedule
Create a daily OpenClaw cron job. L&I flexible-leverage managers publish the next
trading day's factor after market close, so an evening HKT run (e.g. ~18:30) picks
up that day's file. Embed the resolved home path so every scheduled run uses the
same location:
```bash
HOME_DIR="${HKEX_LI_MONITOR_HOME:-$HOME/.config/hkex-li-daily-factor-monitor}"
openclaw cron add \
  --name hkex-li-daily-factor-monitor \
  --description "Daily HKEX L&I targeted leverage factor digest" \
  --cron "30 18 * * 1-5" \
  --tz "Asia/Hong_Kong" \
  --tools exec \
  --announce \
  --message "Run the hkex-li-daily-factor-monitor skill now: perform one run exactly as its SKILL.md describes (run_mode=latest), and output the Telegram monospace digest (rows grouped by applicable date, source links below) as your final message."
```
Delivery/routing is OpenClaw's (`--announce`); this skill names no channel.
Inspect: `openclaw cron list`. Remove: `openclaw cron rm --name hkex-li-daily-factor-monitor`.

---

# Notes & guarantees
- **One writable home** (`~/.config/hkex-li-daily-factor-monitor`, override
  `HKEX_LI_MONITOR_HOME`); nothing is read/written in the skill folder.
- **Copyright-safe:** PDFs live only in the scratch dir for the current run and are
  deleted in Step 6 and by the `EXIT` trap. Only the extracted factor digest leaves the run.
- **Portable / no hard-coding:** every URL, endpoint, keyword, category gate, and
  path is in the config block; swap them there, not in the steps.
- **Minimal Python:** discovery and filtering are pure `curl`+`jq`; Python is a PDF
  fallback only (`scripts/pdf_to_text.py`), used when `pdftotext` is unavailable.
- **Robust discovery:** date-window query + client-side keyword/category filter,
  independent of HKEX's internal category codes.
- **Fails loud:** no matches, a broken download, or an unparseable table each raise
  a specific error rather than producing empty or partial output.
