---
name: hdb-resale-watcher
description: Watch Singapore HDB resale transactions and get alerted only when new sales are registered. Use when the user wants HDB resale tracking, new-transaction alerts for a town or flat type, or a one-off search of official HDB resale records. Runs the magnova/sg-hdb-resale-monitor Actor through the Apify plugin for OpenClaw; transaction records cost $0.002 and new-transaction alerts $0.01 on the user's own Apify account.
version: 1.0.0
homepage: https://apify.com/magnova/sg-hdb-resale-monitor
metadata:
  openclaw:
    requires:
      env:
        - APIFY_API_TOKEN
---

# HDB Resale Watcher

Singapore HDB resale registrations change daily, and
nobody wants to re-check the same town and flat type by
hand. This skill registers resale watches on the towns,
flat types, months and price ranges the user cares about
and, on each check, reports only the transactions that are
new. It can also run a plain one-off search of the official
HDB resale records.

## Prerequisites

1. The Apify plugin for OpenClaw is installed and allowlisted:
   `openclaw plugins install @apify/apify-openclaw-plugin`
2. `APIFY_API_TOKEN` holds the user's own Apify API token. All
   runs bill to that account.
3. You call Actors through the plugin's `apify` tool: `start`
   (returns a runId), then `collect` (returns the results).

If the plugin or token is missing, stop and tell the user
exactly what to install or set. Do not scrape data.gov.sg or
a property portal yourself and do not substitute another
source.

**Cost, stated plainly:** the Actor charges $0.002 per
transaction record and $0.01 per new-transaction alert, no
start fee. A watch's first check delivers the newest
matching transactions as baseline records (about $0.04 for
20 results); later checks charge nothing unless a new
transaction appears, and then only $0.01 per new sale. The
Actor reads HDB's official public dataset via data.gov.sg
— no login and no property-portal scraping.

## Setup (first run only)

Ask the user for: the HDB towns to track (e.g. BEDOK,
TAMPINES, PUNGGOL — or all of Singapore), the flat types
(1 ROOM to 5 ROOM, EXECUTIVE, MULTI-GENERATION), an optional
registration-month range (YYYY-MM, from 2017-01), optional
minimum and maximum resale prices in SGD, and how many
records each check should deliver at most. Store the watch
input so later checks reuse it exactly — a watch is
identified by its towns, flat types, month range and price
range, so changing any of them starts a new baseline.

## Workflow

**Register or check a watch** — call the Actor
`magnova/sg-hdb-resale-monitor` with:

```json
{
  "towns": ["BEDOK"],
  "flatTypes": ["4 ROOM"],
  "mode": "watch",
  "maxResults": 20
}
```

**One-off search** — same input with `"mode": "search"`.

Reading the results (`TRANSACTION` records carry a
`changeType`):

- `BASELINE` records appear only on a watch's first check.
  Summarize the newest few sales and the price range, and
  tell the user the watch is set.
- `NEW` records are transactions registered since the
  previous check — lead with them. Report the month, town,
  block and street, flat type, storey range, floor area,
  resale price in SGD and price per square metre, plus the
  remaining lease.
- `SEARCH` records are a one-off result set; summarize the
  newest sales and the price range for the filters used.
- A check that returns only a `SUMMARY` record means
  nothing new registered: say so in one line, or stay
  silent if the user asked for alerts only.
- `ERROR` records mean the check could not be completed;
  mention it and retry on the next scheduled check.

## Scheduling

Offer to run the watch check on a daily cadence (the user's
own scheduler or cron). HDB refreshes the dataset daily;
weekly is enough for slower towns or broad segments.
