---
name: paper-mail-retention
description: Use when the paper pile takes over or before a shredding session — a 60+ item lookup of how long to keep each document type (tax 7yr, paystps until W-2 matches, warranties until expiry, utility bills 1yr, immunization records forever), destination routing (keep-file, shred, scan-then-shred, safe-deposit), a purge-mode triage flow, and year-digit shredding rules that keep the annual purge to 30 minutes.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [paperwork, document-retention, declutter, filing, taxes, shredding, organization]
---

# Paper Mail Retention

## Overview

Every household runs an unmanaged archive: tax returns from 2009,
utility bills from three addresses ago, appliance manuals for
appliances that no longer exist — and somewhere under the pile, the one
document that actually matters. Retention isn't a personality trait;
it's a lookup table. Tax supporting documents live with the return for
7 years (audit window + state extensions), paystubs live until the W-2
agrees, warranties live until the product's warranty ends,
immunization records live forever.

`scripts/mail_retention.py` is that table plus the workflow around it:
`keep <thing>` answers "how long and why", `purge` walks a pile item-by
item with dates applied (a 2021 utility bill is shredded regardless of
category default), and `archive` prints the year-digit shredding rules
that make next year's purge take 30 minutes: keep-files organized by
YEAR, so "shred everything older than N" is a folder glance, not an
archaeology project.

## When to Use

- The paper pile on the counter/kitchen table has become structural.
- Annual or moving-time purge: what's safe to shred, what must stay.
- After tax season: which documents file with the return vs separately.
- Setting up a first real filing system (what categories, what bins).
- After a parent's/relative's paperwork arrives in boxes.

**Don't use for:** business records (different rules — corporate
bylaws, employment tax records, contracts), medical record *content*
interpretation (this skill handles retention, not medical advice), or
digital-file retention (different format risks; principles transfer).

## How It Works

1. **Category table.** 60+ document classes with keep duration, clock
   start event (filed / paid / expired / event date), disposition
   (KEEP-FILE, SHRED, SCAN+SHRED, SAFE-DEPOSIT, FOREVER), and the why
   for each — because purge discipline fails when you can't remember
   the reason.
2. **`keep` lookup.** `--thing "tax return"` or "paystub", "warranty",
   "insurance policy", "birth certificate". Fuzzy prefix match across
   names and aliases.
3. **`purge` triage.** For each item: category + document date →
   verdict with the countdown. A utility bill from 2021 with a 1-year
   clock: SHRED, 4 years overdue. Anything without a date input gets a
   conservative default with a flag.
4. **Forever items.** Never purge: birth/death/marriage/adoption
   certificates, divorce decrees, immigration papers, military
   discharge (DD-214), immunization records, pension/retirement plan
   documents, current insurance policies, property deeds, and the last
   7 years of tax RETURNS themselves (supporting docs same window;
   returns can be kept digitally forever after).
5. **Year-digit organization.** The system that makes purging trivial:
   one hanging folder per YEAR for time-limited items. "Shred 2018 and
   older" = pull three folders, shred, done. Categories without clocks
   (manuals, warranties active, policies) live in labeled topic
   folders, not year folders.
6. **Scan-then-shred doctrine.** Scan (phone scanner app) anything with
   >7-year value before shredding paper: tax returns, house closing
   docs, major receipts. 3-2-1 backup rules apply to scans (see
   backup-3-2-1-auditor skill); a scan on one laptop is not an archive.

## Using the Script

```bash
# how long do I keep X?
python3 scripts/mail_retention.py keep --thing "tax return"
python3 scripts/mail_retention.py keep --thing paystub

# purge a pile: category:date pairs
python3 scripts/mail_retention.py purge \
  --items "utility bill:2021-03" "bank statement:2024-06" \
          "tax return:2019" "warranty:2023-05" "insurance policy:current"

# print the filing system blueprint + forever list
python3 scripts/mail_retention.py archive
```

Outputs: per-item verdicts (KEEP/SHRED/SCAN+SHRED) with reason and
remaining clock, the forever list, the year-folder blueprint, and a
shred-vs-trash warning (anything with SSN/account numbers → cross-cut
shredder, not recycling).

## Common Pitfalls

1. **Keeping everything "for taxes".** Only tax *supporting documents*
   need the 7-year seat belt. Utility bills beyond proving a home
   office, random receipts, and old statements are 95% of the pile.
2. **Shredding the return, keeping the clutter.** People shred the
   return (the thing to keep) and keep Kroger receipts (the thing to
   toss) — inverted urgency.
3. **Warranties kept past expiry.** A warranty card for an appliance
   you no longer own, or expired 3 years ago, is shredder food. Keep
   warranties WITH the purchase receipt stapled, toss both at expiry.
4. **Ignoring year-dating folders.** Categories without year folders
   force document-by-document reading at every purge — the reason
   purges take a whole Saturday and then never happen again.
5. **Trash vs shred.** Anything with SSN, account numbers, medical
   IDs, or signatures → cross-cut shred. Utility bills included — they
   carry enough for account takeover.
6. **Scan = safe assumption.** A scan exists only if it's backed up in
   2 places. One-copy scans that justified shredding paper are a
   future crisis (dead laptop, no paper).
7. **Safe-deposit overload.** Originals of forever-items belong in a
   fireproof box or safe-deposit; copies at home. Don't put anything
   you might need TOMORROW in a bank box (bank hours vs emergency).

## Verification Checklist

- [ ] Forever documents identified and stored (fireproof/safe-deposit),
      copies accessible at home.
- [ ] Year-folder system set up for time-limited items (this year +
      prior 7).
- [ ] Purge verdicts applied: shred pile contains no forever/clock-
      running items.
- [ ] All shred-pile items cross-cut shredded (SSN/account-bearing
      especially).
- [ ] Scans backed up in 2+ places before the paper hit the shredder.
- [ ] Next purge date written in the calendar (tax day + 1 week).
