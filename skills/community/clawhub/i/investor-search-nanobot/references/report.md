# The final report — shape and the counting check

`SKILL.md` says when to write the report and what must never be claimed in it. This file is
the exact shape: the block, the three tiers, and what each line is for. Open it while you
write the report.

## Report when you finish

**Take every number from `store.py finish`**, never from the conversation — and write the
report only after `finish` exits 0. The report is not
optional in a chat app: send the whole block below as text, then the files. Its second line
says **why the run stopped** — `EXHAUSTED on the surfaces named` (all four gates open),
`STOPPED ON BUDGET` (the user's own number), `STOPPED ON THE 60-ROUND BACKSTOP`, or
`STOPPED EARLY — <reason>` (a real blocker, named).

```
<MARKET> · 33 firms over 10 rounds + 4 verification passes
STOPPED ON BUDGET — PARTIAL, not an exhaustion count
written      /home/u/work/investor-search/poland/ · 6 files · index.md updated
surfaces     web search · commercial register · 2 association lists
             NOT tried: news/deal announcements

offered      99 names — 33 survived
  in English 89 offered · 33 survived (37%)
  in <local>  10 offered ·  0 survived (0%)

already held 14 names already on file — dropped
already ret'd 6 names this run had already returned — dropped
rejected     13 advisers, not investors
              4 not investors · 2 source dead · 1 unsourceable
             26 parked, unresolved
             (33 + 14 + 6 + 13 + 4 + 2 + 1 + 26 = 99 — every offered name has one home)

type         5 family_office · 9 investment_group · 10 venture_capital
             7 private_equity · 2 angel · 0 unknown
evidence     24 invests · 7 operating_group · 0 syndicate · 2 unclear
sources      173 citations · rung 1: 160 · rung 4: 9
quotes       25 of 33 rows carry an evidencing quote; 8 correctly have none
flags        7 fold_conflict · 8 rows whose HQ rests on a rung-4 source alone

(Shape only. The figures are illustrative — no shipped run has legitimately reached the
exhaustion sentence.)
```

**Every offered name lands on exactly one line, and the lines sum to the offered count.**
Not a slogan — a check. A kept row counts as survived even where one of its fields rests on
`sourceUnchecked`; the parked line counts only names that never became rows. A name that was offered and is not on any line was dropped without a
decision, which is the bucket with a hole. The two dedupe lines stay **separate**: *"20 already
known or already returned"* welds two failures with opposite fixes, and a run past round 1
always has some of both. Rejections are broken out by reason for the same reason — `sourceDead`
and `unsourceable` describe a page and may be re-offered later; `adviserNotInvestor` and
`notAnInvestor` describe the firm and never will.

**Split the offered count by language** — that line is what caught the language rule being
wrong. **Report every flag.** `fold_conflict`, `operating_group`, `unclear` and rung-4-only
rows are exactly what a reader must look at.

**Where the folder could not be kept** (tier B), the same report takes the same shape, with
the `written` line naming the files that were sent and no folder path:

```
NOT KEPT HERE — files sent to you. PARTIAL; exhaustion cannot be claimed here.
written      sent: <market>-investors.xlsx (one file)
resume       upload this file at the start of the next run
```

Tier C — no file could be handed over at all:

```
NO FILES — CSV text in chat only. PARTIAL; exhaustion cannot be claimed here.
written      nothing — investors.csv and sources.csv printed below, then the ledger
resume       paste the ledger below at the start of the next run
```

The counts are reported exactly as they would be on disk. In tier C, unresolved names are
listed in the ledger as `pending`, not carried in a file.

**The `written` line is not decoration** — it is the only place the user learns where their
files actually are, and whether the completeness claim was available at all.

Say how you knew it was finished — or say plainly that you did not. Then, on one line: *"To
continue, say `continue Austria`"* (with the market) — the next run starts from these files.

---
