# k401 Rollover Router — Reference

## 1. The freeze
The average American changes jobs ~12 times; each separation strands a
401(k) that most people never touch again. The default — leave it — is
sometimes right and sometimes a decades-long fee bleed, and the decision
requires comparing five things nobody compares on a Tuesday night:
all-in fees, fund quality, tax brackets now vs later, early-access rules,
and creditor protection. So the accounts pile up (three old 401(k)s is
normal) and decisions defer forever.

## 2. Fee-drag engine (the core math)
Future value of a fee-bearing account:

    FV = B × (1 + r − f)^N     r = expected nominal return
                              f = all-in fee (expense ratio + admin)

The drag between two paths:

    Δ = B × [(1 + r − f_plan)^N − (1 + r − f_ira)^N]

Examples (B = $85,000, r = 6.5 %):
| Fee gap | 10 y | 20 y | 30 y |
|---|---|---|---|
| 87 bps (95 vs 8) | ~$16k | ~$48k | ~$105k |
| 7 bps (12 vs 8)  | ~$1k  | ~$4k  | ~$8k   |

Rule of thumb encoded: **fee gaps ≥ 30 bps on horizons ≥ 15 years almost
always dominate every other routing factor**; gaps under ~10 bps make fees
irrelevant and access/protection factors decisive.

## 3. The route matrix
**LEAVE (in old plan)**
- + possible institutional share-class pricing (big plans)
- + ERISA creditor protection, plan loans may still be available
- + age-55 separator rule preserved (penalty-free access if you left at 55+)
- − stranded accounts multiply; beneficiary management ages badly
- − old plans can force out small balances (<$5k–$7k) or impose exit fees

**ROLL → new employer plan** (if `--new-plan-accepts`)
- + one consolidated account, future contributions blend
- + keeps age-55 rule on the whole balance at the NEW employer (separation
  after 55), ERISA protection, loans
- − fund menu quality is luck; watch that fees aren't worse than old plan

**ROLL → IRA**
- + any fund/ETF/individual bond; typically 3–10 bps index costs
- + Roth-conversion ladder freedom; QCD access at 70½ later
- − loses age-55 access (59½ rule), loses loans
- − traditional IRA adds RMDs at 73/75 (SECURE 2.0: 73 if born 1951–1959,
  75 if born 1960+)
- − pro-rata rule contaminates backdoor Roth if you hold other pre-tax
  IRA money
- − creditor protection varies by state (ERISA plans are near-absolute)

**ROLL → Roth (whole or partial)**
- tax due now = converted amount × marginal bracket (federal + state)
- wins when bracket now < expected bracket at draw, or when buying the
  elimination of future RMDs / tax-free compounding
- pay the tax from OUTSIDE cash; paying from the conversion itself is an
  early distribution if under 59½ → 10 % penalty on that slice

## 4. Traps (each gets a checklist line in output)
1. **Indirect rollover**: check mailed to you → plan withholds 20 %
   federal. You have 60 days to deposit 100 % (covering the 20 % from
   savings); the withheld 20 % comes back only as a tax credit. Miss the
   window = distribution: full tax + 10 % penalty if under 59½.
   **Doctrine: trustee-to-trustee (direct) rollover only.**
2. **12-month rule**: one indirect IRA→IRA rollover per 12-month period
   (per IRA owner, not per account). Direct rollovers/transfers unlimited.
3. **Age-55 vs 59½**: separation-from-service at 55+ unlocks penalty-free
   401(k) withdrawals (rule of 55) — only for THAT plan, not IRAs.
4. **NUA**: highly appreciated employer stock in the plan — net unrealized
   appreciation treatment can tax the appreciation at long-term capital
   gains rates on distribution. Blindly rolling to an IRA destroys it.
5. **Pro-rata**: any pre-tax IRA balance makes backdoor Roth conversions
   partially taxable. Rolling 401(k)s INTO an IRA increases that surface;
   rolling INTO a 401(k) keeps the backdoor clean.
6. **RMD timing**: first RMD year — delay to April 1 of the next year
   only allowed for your FIRST one (double income year follows).

## 5. What the verdict logic weighs
```
score(ROLL_IRA)  = fee_drag_$ + fund_freedom − access_loss − rmd/pro-rata flags
score(ROLL_NEW)  = fee_drag_$ + consolidation + protection − menu_quality
score(LEAVE)     = −fee_drag_$ + protection + loans
Roth overlay     = if bracket_now < bracket_retire → partial-conversion sized
                   to fill current bracket headroom
```
The script prints the two or three decisive lines in dollars, not a
mushroom-cloud table.

## 6. Verification duty (honesty clause)
Brackets and RMD ages change with legislation. The script's CONFIG block
carries 2026-era values and prints a "verify against current IRS
Pub 590-A / SECURE 2.0" footer. Not tax advice — a decision instrument
you bring to a conversation with a professional when the numbers are big.
