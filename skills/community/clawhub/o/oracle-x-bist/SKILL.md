---
name: oracle-x-bist
description: Read and reason about Borsa İstanbul — BIST equities and the XU100, TEFAS funds and their holdings, KAP disclosures, VİOP futures margins, open interest and positioning, foreign ownership, short-sale restrictions, and the Turkish macro series (TÜFE inflation, policy rate, USDTRY) the rest is measured against. Use this whenever a question names a Turkish ticker such as THYAO, ASELS, GARAN or EREGL, a BIST index, a TEFAS fund code, KAP, VİOP or Takasbank, or asks what a lira return was actually worth. Half of it needs no server at all: how a nominal return is turned into a real one, where Takasbank publishes the price scan range and the two filters that make it read correctly, and why a margin-call price for VİOP cannot be computed from anything public. The other half calls a running Oracle-X instance when ORACLE_X_URL is set. Consult it before quoting any Turkish figure, because a lira number over a year of ~32% inflation reports inflation as performance.
version: "1.3.0"
license: Complete terms in LICENSE.txt
metadata:
  homepage: "https://github.com/Yigtwxx/OracleX"
  openclaw:
    emoji: "🇹🇷"
    homepage: "https://github.com/Yigtwxx/OracleX"
    requires:
      anyBins:
        - curl
        - python3
    primaryEnv: ORACLE_X_URL
    envVars:
      - name: ORACLE_X_URL
        required: false
        description: Base URL of a running Oracle-X instance. Only the endpoint half of this skill needs it; the rules half works without one.
---

# Borsa İstanbul

This skill has two halves, and only one of them needs a server.

**The rules hold everywhere.** How a Turkish return is stated, what Takasbank
publishes and what it does not, why a VİOP margin-call price cannot be
computed — these are properties of the market, not of any instance. They are
the part most likely to be got wrong, and they are useful the moment this skill
is installed.

**The endpoints need a running Oracle-X instance** at `$ORACLE_X_URL`
(default `http://localhost:8000`). If nothing answers there, use the rules and
say plainly that the data half is unavailable. Do not fall back on a remembered
price. A number invented for a trading question is worse than no number.

The rest of the terminal — crypto, US equities, macro, chains, derivatives,
prediction markets, the vector memory — is the sibling skill `oracle-x-api`, on
the same instance.

## Rules that hold with or without an instance

### A lira figure is not a return

Over the windows anyone asks about — a year, three years, five — most of a
Turkish nominal return is inflation. So every return this domain produces is
carried in three frames at once, and quoting one of them alone is the single
most common way to be wrong here:

| Frame | What it answers |
|---|---|
| `nominal` | How many lira. As quoted. |
| `real` | What those lira bought. Deflated by consumer prices (TÜFE). The honest default for someone spending the money in Turkey. |
| `usd` | Restated in dollars. What most Turkish investors actually benchmark against, and the only frame comparable to a foreign asset. |

None of the three corrects the others; report the frame the question asked for
and say which one it is. **A null `real` means the window could not be
deflated — never that inflation was zero.** Say the figure is unavailable
rather than passing the nominal number off as real.

### Prices are delayed

BIST quotes on this surface are delayed at least 15 minutes, and every board
carrying a quote says so in `delay_minutes`. Never present one as live, and
never use one to answer a question about where something is trading *right
now*.

### Symbols carry their venue

`BIST:THYAO`, not `THYAO`. A bare ticker does not resolve to Borsa İstanbul —
deliberately, because an unprefixed ticker forced down the crypto path once
read AAPL off a tokenised-equity market. If a user writes a bare Turkish
ticker, add the prefix rather than hoping.

### VİOP: the scan range is not a margin call

Takasbank publishes a **price scan range** (PSR) per underlying: the one-day,
99% confidence move the clearing house collateralises against under BISTECH.
A position that moves by the PSR has exhausted the scan risk its *initial*
margin was sized for.

It is **not** the price at which a margin call fires, and that price cannot be
derived from anything public. The CCP procedure leaves the maintenance level to
a General Letter and states that maintenance is not applied at end of day. The
"75% of initial" figure that circulates online appears only in an undated
guide — do not adopt it, do not compute a call price from it, and do not let a
chart imply one.

### Where the scan range actually comes from

Two hosts, and the obvious one is a dead end:

* `www.takasbank.com.tr` sits behind bot protection and will not answer a
  script. This makes the parameters look unavailable. They are not.
* `wwwdata.takasbank.com.tr` is a separate host with an open directory listing
  and no protection. The day's file is
  `pardosya/Prod/YYMMDD/TAKASEOD_…-001.zip`.
* **Do not use `wwwdata.takasbank.com.tr/viop/SPAN/`.** It is a legacy archive
  frozen in March 2017 that still serves `200`s, which is the worst possible
  failure mode: current-looking numbers that are nine years stale.

Run `-001` is the end-of-day file. The intraday runs revise the parameter nine
to sixteen times a session, so they are not a snapshot anything can be pinned
to.

Reading the file costs two filters, and neither is optional, because it carries
a portfolio per broker alongside the ones per underlying and a rights-issue
portfolio beside each main contract:

```
setlMeth == "DELIV"          # physically settled single-stock futures
not pfCode.endswith("_C")    # drop the rights-issue portfolio
```

Skip either and THYAO reads **14.0** where its scan range is actually **13.4** —
a plausible wrong number, arrived at silently. `references/viop-margins.md` has
the full procedure.

### Direction in VİOP positioning is inferred, not published

Open interest rising on a session whose settlement rose is read as longs
opening; rising against a falling settlement, as shorts. Everything else on the
positioning surface — exposure opened, entry price, the swept range, the band
distance — is published by the exchange or the clearing house. This one is a
reading, and it is the standard futures reading. A session whose settlement did
not move gets no cohort at all rather than a hedged split, and what is dropped
is counted and reported.

## Choosing an endpoint

Needs a reachable instance. One call each; read the full parameters in
`references/endpoints.md` before calling.

| The user wants | Call | Why this one |
|---|---|---|
| The state of the Turkish market | `GET /api/bist/overview`, `GET /api/bist/market-note` | The board, then the written read of it. |
| One stock | `GET /api/bist/stocks/{ticker}` | Returns arrive as `nominal`/`real`/`usd` together — see the rules above before quoting one. |
| The whole list, or a visual | `GET /api/bist/stocks`, `GET /api/bist/heatmap` | |
| A TEFAS fund | `GET /api/bist/funds/{code}`, `GET /api/bist/funds/{code}/holdings` | The fund's own numbers, then what it is actually holding. |
| Funds side by side | `GET /api/bist/funds/compare` | |
| Company disclosures | `GET /api/bist/kap`, `GET /api/bist/kap/{index}/note` | KAP filings, and a written read per index. |
| Turkish macro | `GET /api/bist/macro`, `GET /api/bist/macro-note` | TÜFE, the policy rate, USDTRY — the series that deflate every `real` figure above. |
| VİOP contracts | `GET /api/bist/viop`, `GET /api/bist/viop-note` | Open interest and volume per contract. |
| Where VİOP positions sit | `GET /api/bist/viop-map/{ticker}` | Cohorts drawn against Takasbank's published scan range. **Not** margin-call levels — say so if you render it. |
| Which underlyings have a map | `GET /api/bist/viop-map/underlyings` | Ask this before assuming a ticker is covered; the map is built only where the data supports it. |
| Foreign and institutional positioning | `GET /api/bist/positioning`, `GET /api/bist/ownership/board` | Foreign share, then the entity-level book. |
| Who holds one ticker | `GET /api/bist/ownership/assets/{ticker}` | |
| How those positions moved | `GET /api/bist/ownership/moves`, `GET /api/bist/ownership/note` | |
| Short-sale and credit restrictions | `GET /api/bist/restrictions` | |
| What is scheduled | `GET /api/bist/calendar` | |
| A screen across BIST names | `POST /api/bist/radar/scan` | A job — see below. |

Anything not in this table is in `references/endpoints.md`. Guessed URLs return
404s that look like missing data.

## The radar is a job, not a call

A scan runs longer than a request should, so it is started and then polled:

```bash
BASE="${ORACLE_X_URL:-http://localhost:8000}"
JOB=$(curl -sf -X POST "$BASE/api/bist/radar/scan" \
       -H 'Content-Type: application/json' -d '{}' | python3 -c 'import json,sys;print(json.load(sys.stdin)["job_id"])')

curl -sf "$BASE/api/bist/radar/jobs/$JOB"     # poll until status is done
curl -sf "$BASE/api/bist/radar"               # the last completed scan
```

Poll at a few seconds, not in a tight loop, and read `GET /api/bist/radar`
first — if a recent scan answers the question, starting another one wastes the
instance's time. `DELETE /api/bist/radar/jobs/{job_id}` cancels a run.

## When something goes wrong

| Response | What it means | What to do |
|---|---|---|
| Connection refused | No instance at `$ORACLE_X_URL`. | Say so. The rules half of this skill still applies; the data half does not. |
| `404` | The ticker or fund code did not resolve. | Do not substitute a guess. Check the prefix (`BIST:THYAO`) and the spelling. |
| `503` | An upstream is down and an empty list would be a lie. | Report the gap. `GET /api/system/health` names the category. |
| A null `real` | The window could not be deflated. | Report the nominal figure *and* that the real one is unavailable. |

Oracle-X declines rather than guesses, and passing a refusal on unchanged is
the point. In a trading terminal a plausible wrong number is worse than an
error.

## Reference files

Read on demand, not up front:

| File | When |
|---|---|
| `references/endpoints.md` | Generated from the running app. Every BIST endpoint with its full parameters and response shape. |
| `references/viop-margins.md` | Reading Takasbank's SPAN file directly — the host, the path, the two filters, and what each one costs if skipped. |
