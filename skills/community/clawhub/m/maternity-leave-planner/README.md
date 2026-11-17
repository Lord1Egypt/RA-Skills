# Maternity / Paternity Leave Planner (US)

**The problem.** A baby is coming. You have FMLA (unpaid, job-protecting), maybe a state paid-leave program, maybe employer short-term disability, maybe a company parental policy, and a PTO balance. Nobody tells you how they stack, in which order to take them, or which weeks are paid. The result: American parents leave money and protected time on the table — the median mother takes ~10 weeks, often less than she's entitled to, because computing the entitlement requires an HR degree she doesn't have.

**What this does.** Turns 6 inputs (state, due date, pay, birth method, PTO balance, plan details) into a **week-by-week dated leave plan**: every week labeled with its phase (recovery / bonding / PTO-plug / unpaid tail), its pay source, the capped dollar benefit, and whether your job is protected that week. Plus:

- FMLA eligibility verdict (tenure / hours / employer-size gates)
- State comparison table (CA vs NY vs MA vs TX... — the difference is 20 paid weeks vs zero)
- Sequencing doctrine: recovery → paid bonding → PTO into unpaid weeks → protected unpaid tail
- Filing-order checklist with dates (file disability at leave start, bonding when recovery ends)

**Example.** California, C-section, $1,150/wk, 10 PTO days → 20-week plan: 8 wk SDI at $690, 8 wk PFL at $690, 2 wk PTO at $1,150, 2 wk unpaid-but-protected. 18 of 20 weeks paid, 58% of salary. Same parent in Texas: 6 unpaid-but-protected weeks unless an STD plan exists — the script makes that gap visible *before* the baby arrives, when there's still time to buy individual STD (which must be purchased 10–12 months **before conception** to pay out).

## Quick start

```bash
python3 scripts/maternity_plan.py plan --state CA --due 2027-03-15 --pay 1150/week --c-section --pto-days 10
python3 scripts/maternity_plan.py compare --states CA NY MA TX FL WA --pay 1150/week
python3 scripts/maternity_plan.py fmla --tenure-mo 8 --hours-yr 900 --employees 40
```

## Files

- `SKILL.md` — trigger conditions, systems model, pitfalls, verification checklist
- `references/parental-leave-benefits.md` — FMLA rules, 13-state program table, sequencing engine, filing checklist
- `scripts/maternity_plan.py` — the planner (stdlib only, no dependencies)

## Caveats

Program parameters (weeks, replacement rates, weekly caps) are approximate 2026 values and change annually — every output carries a verify flag. Not legal or HR advice; always get the employer's **written** policy, not a verbal summary.

## License

MIT © 2026 Denis Voronin
