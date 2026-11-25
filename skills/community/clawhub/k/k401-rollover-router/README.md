# k401 Rollover Router

**Problem.** Job changers strand old 401(k)s by default. The decision
(leave / roll to IRA / roll to new plan / Roth-convert) depends on fee
gaps, brackets, early-access rules and creditor protection — five things
nobody compares on a Tuesday night — so the accounts pile up and
1 %-ish plan fees quietly compound against you for decades.

**What it does.** `scripts/rollover_router.py` with your real numbers:

- **fee-drag engine**: projects plan vs IRA costs to your draw horizon
  and prints the dollar gap at 10/20/30 years (87 bps on $85k over 22 y
  ≈ five figures lost — the tool names it);
- **route verdict** with the 2–3 decisive factors in dollars (LEAVE /
  ROLL-IRA / ROLL-NEW-PLAN + optional ROLL-ROTH-PARTIAL overlay when your
  current bracket is below your expected retirement bracket);
- **Roth conversion pricing** with the pay-from-outside-cash doctrine;
- **trap checklist**: 20 % indirect-rollover withholding + 60-day clock,
  one-indirect-per-12-months, age-55 separator rule vs 59½, pro-rata
  backdoor contamination, NUA on employer stock, SECURE 2.0 RMD ages;
- cash-out damage printed as deterrence, never as a recommendation.

**Why broadly useful.** The median US worker holds multiple job changes
per career and ~$100k+ in retirement accounts; "what do I do with my old
401(k)" is one of the most-asked personal-finance questions alive. The
default action (nothing) has a measurable price — this makes it visible
and routes around it.

**Example.**

```bash
python3 scripts/rollover_router.py --balance 85000 --age 40 \
  --plan-fee-bps 95 --ira-fee-bps 8 --return 6.5 --years-to-draw 22 \
  --bracket-now 24 --bracket-retire 22
# fee drag at 22y, ROLL -> IRA, cashout damage ~$71k net + growth lost
```

Not tax advice; 2026-era constants in CONFIG with a verify-footer.
MIT license.
