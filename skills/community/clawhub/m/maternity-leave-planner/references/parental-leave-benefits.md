# US Parental Leave Systems — Reference

## 1. FMLA (Family and Medical Leave Act, 1993)

- **What:** 12 workweeks unpaid, job-protected leave in a 12-month period for birth/bonding, adoption, foster placement (also own serious health condition, family caregiving).
- **Eligibility (all three):**
  1. 12 months of employment with the employer (need not be consecutive)
  2. 1,250 hours worked in the preceding 12 months (~24 hrs/week)
  3. 50+ employees within 75 miles of the worksite
- **Key rules:**
  - Bonding leave must be completed within 12 months of birth/placement.
  - Runs **concurrently** with state paid leave and employer policies — never additive.
  - Intermittent/reduced-schedule bonding allowed with employer agreement (mandatory only for medical need).
  - 30-day advance notice required when leave is foreseeable.
  - Employer must maintain health insurance on the same terms during FMLA; may recover premiums if you don't return.
  - Key-person exemption: top-10% salaried employees can be refused restoration in rare cases.
- **Job protection only, no pay.** Restoration to same or equivalent position.

## 2. State Paid Programs (approximate 2026 shape — ALWAYS verify current-year weeks, rates, caps)

| State | Recovery (disability) | Bonding (paid family) | Replacement | Job protection |
|---|---|---|---|---|
| CA | SDI: up to 4 wk pre-birth + 6–8 wk post | PFL 8 wk | 60–70% (wage-factor), weekly cap | CFRA 12 wk bonding (unpaid protection, runs alongside) |
| CO | FAMLI 12 wk (own medical incl. birth recovery) | included in 12 (+4 complications) | 90% below ~half avg state wage, 50% above; capped | job protection after 180 days tenure |
| CT | 12 wk own health | 12 wk family | 95% to SSWB, 60% above; cap | state FMLA-type protection |
| DE | own medical | 12 wk bonding | ~80% capped | after 12 mo employment |
| MA | 20 wk own medical (separate bank) | 12 wk family | 80% to SSWB, 50% above; cap | MA FML-type protection |
| MD | own medical | 12 wk | capped ~$1,000/wk scale | begins 2026 — verify rollout |
| MN | own medical | 12 wk | ~67% capped | begins 2026 — verify rollout |
| NJ | TDI: 4 wk pre + 6 wk post (+4 C-section) | FLI 12 wk (or 56 part-days) | 85% capped | NJFLA 12 wk bonding protection |
| NY | DBL: 6–8 wk post (low cap ~$170/wk unless enhanced) | PFL 12 wk | 67% capped | NY Paid Family Leave includes protection |
| OR | own medical 12–14 wk | 12 wk bonding | 100% to 65% SAWW tiered | OFLA-style protection |
| RI | TDI: 4 wk pre + 4–6 wk post | TCI 5 wk (expanding — verify) | ~60% (1.2× benefit cap) | RI Parental & Family Medical Leave |
| WA | own medical 12 wk | 12 wk bonding | 90% to SAWB, 50% above; cap (~$1,600) | state FML protections |
| DC | own medical | 8–12 wk bonding | 90% to cap | DCFMLA |
| Other states | none (federal FMLA only) | none — employer policy only | — | FMLA 12 wk |

**No state program + no employer policy = unpaid FMLA** — still job-protected for 12 weeks.

## 3. Short-Term Disability (STD) where the state doesn't pay

- Typical group STD: 50–100% of salary, 6 weeks vaginal / 8 weeks C-section, often a 7–14 day waiting period (PTO can cover the wait).
- Pregnancy is a covered "disability" for the physical recovery window only — not bonding.
- Individual STD policies bought before pregnancy: check the "pre-existing condition" clause; most require coverage 10–12 months **before conception** to pay.

## 4. Sequencing engine (how the script builds the plan)

Order of operations per week, birthing parent:
1. **Recovery** weeks (state disability if available, else STD, else PTO, else unpaid) — 6 or 8 weeks from birth.
2. **Bonding** paid weeks (state PFL; employer parental policy may substitute or stack).
3. **PTO-plug** into unpaid weeks (respecting no-double-dip states).
4. **Unpaid protected tail** (FMLA/state protection continues to its own end date).

Non-birthing parent / adoptive parent: skip step 1, start at bonding. Partners should NOT overlap their state bonding weeks with the birthing parent's unless childcare math says so — staggering extends covered childcare to ~6 months in the best states.

## 5. Filing checklist (dated)

- **T-90 days:** request the employer's written parental-leave policy + STD certificate; confirm benefits-eligible status.
- **T-30 days:** written FMLA notice to HR (waivable for emergency births).
- **Birth week:** file state disability claim (CA/NJ/NY/RI) or STD claim.
- **Recovery end:** file state bonding/PFL claim (do not file bonding first in states where the clocks are separate).
- **During leave:** confirm health-insurance premium arrangement in writing.
- **Return:** request lactation space + break policy (FLSA §218d: reasonable break time, private space, 1 year+), and confirm restoration date.

## 6. Money math the script does

- Weekly benefit = min(pay × replacement%, cap). Some states tier the percentage by wage (CO/MA/WA/CT-style): below the threshold wage, high %; above, lower %. The script models the two-tier form where applicable and flags "verify" otherwise.
- Effective income during leave = Σ paid weeks' benefits + PTO weeks' pay − continued insurance premiums (remind user to subtract).
- PTO-plug: converts day balance to weeks (5 days/wk) and fills the earliest unpaid post-recovery weeks (worst case, fills last — configurable).

## 7. Intermittent & hybrid patterns

- After continuous leave ends, remaining bonding entitlement (if any weeks were unused) can often be taken intermittently — useful when paid leave ends before childcare starts.
- Example: CO parent takes 8 continuous weeks, keeps 4 weeks for part-time return ramp (2 days/wk for 10 weeks).
- Some states (OR, MA) allow intermittent bonding only with employer agreement — same as FMLA.

## 8. What changes the answer the most (sensitivity)

1. State (12 paid weeks vs zero) — dominates everything
2. C-section (+2 recovery weeks, often paid)
3. Employer policy stacking (some tech/consulting employers pay 16–22 weeks at 100%)
4. High earners get clipped by caps — budget on capped dollars, not percentages
5. Timing of PTO holidays — schedule unpaid weeks to avoid Thanksgiving→New Year gaps unless the holiday pay carries
