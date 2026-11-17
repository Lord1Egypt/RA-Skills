# Home Office Deduction — Rules, Math, and Audit Proofing

## 1. Who may deduct at all (2026 filing season)
| Filer | Federal status |
|---|---|
| Self-employed (Schedule C) / gig / 1099 freelancer | **Yes** — regular or simplified method |
| W-2 employee, unreimbursed | **No** (TCJA suspension 2018–2025; watch for extension — verify current-year law before filing) |
| W-2 employee with accountable-plan reimbursement | Employer-side; you submit receipts, no deduction |
| Partner working from home for the partnership | Possible via unreimbursed partner expenses (Form 1065 K-1 route) — see a tax pro |
| S-corp owner-employee | 2%-shareholder rules / accountable plan reimbursement route — different mechanics, same gate tests |
| Home daycare | Exclusive-use waived; use hours-of-operation percentage instead |
State overlays: CA does not fully conform (allows unreimbursed employee business expenses on the CA return); NY added a remote-/hybrid-employee telecommuting expense allowance (2022+, capped, employer eligibility rules); PA allows employee business expenses. The federal $0 verdict is not the end of the story for employees in those states.

## 2. The gate (Pub 587, condensed)
**Regular AND exclusive use** as the principal place of business — or a place to meet clients/customers, or a separate free-standing structure, or inventory/product storage (exclusive-use not required for the storage portion in a home that is the only fixed location of the business).
- *Exclusive*: the specific area is used only for the business. Guest-bed-in-the-corner fails. A separately identifiable desk area can pass in principle, but whole-room claims are what survive audits.
- *Regular*: occasional overnight billing from the couch fails; 3+ days/week work pattern passes.
- *Principal place*: where you perform the substantive administrative/management work counts (the Soliman fix), so the classic freelancer laptop office qualifies.
- Relative-ease note: employees historically needed "for the convenience of the employer" — moot while the federal employee deduction is suspended, but it revives if the suspension lapses.

## 3. Method math (what the script implements)
```
business_pct = office_sqft / home_sqft           (regular method)
regular      = (rent + utilities + insurance + repairs + depreciation) * business_pct
               + direct expenses (business-only internet line, office supplies)
simplified   = $5 * min(office_sqft, 300)
deduction    = min(method_total, business_gross_income)   # cap
             regular-method excess -> carryforward; simplified excess -> lost
depreciation = home_value * (1 - land_share) / 39 * business_pct   (owners, regular only)
```
Break-even intuition: with average US household energy/insurance/repair load, the regular method beats $5/sqft whenever business % × housing costs exceeds $5/sqft — i.e., almost always for renters paying >$1,200/mo with a ≥10% office, and for owners once depreciation is counted.

## 4. Recapture (the owner's tail risk)
- Regular-method depreciation (allowed **or allowable**) is recaptured at sale, taxed as §1250 unrecaptured gain up to 25%.
- Simplified-method years generate zero depreciation and zero recapture.
- Worked example in the script: $420k home (25% land) with 10% office → $817/yr depreciation; 10 years of regular method ≈ $8,170 basis reduction ≈ up to ~$2,043 recapture tax at sale. If regular beats simplified by $900/yr, the 10-year gain ($9,000 − $2,043) still favors regular — but for a 3-year horizon before sale, simplified can win net.
- Reporting at sale: Form 4797 + Schedule D; gain on the home exclusion (§121) does not cover the recapture piece.

## 5. Audit-proofing evidence pack
1. **Floor-plan worksheet** (dated, signed): room dimensions, total home sqft, computed %, method chosen. Sketch or copy of the listing floor plan with the office shaded.
2. **Photos**: wide-angle showing the room used only as an office; desk, equipment, library, storage shelving. Refresh after any furniture/room change. Store with the tax-year folder.
3. **Expense log**: date / payee / category / amount / business-% applied. Cancelled checks or bank+statement PDFs; utility bills 12 months.
4. **Time corroboration**: calendar screenshots, client invoices issued from the office, business license address — establishes "regular + principal place".
5. **Retention**: 7 years (3 for audit-open years as a floor; 7 is the safe norm), plus the depreciation worksheet until **recapture is settled at sale + 3 years**.
6. **Form mapping**: regular → Form 8829; simplified → the Schedule C (line 30) worksheet. Never both in one year for the same home.

## 6. Method switching rules
- Simplified → regular: allowed any year (no look-back).
- Regular → simplified: allowed; depreciation already claimed stays on the recapture ledger.
- Changing homes: fresh election, new basis, prior-home carryover (regular) follows the *home* — a new home resets the workspace %, not the carryforward ledger.

## 7. Non-US snapshot
- **UK**: HMRC simplified expenses £6/mo–£26/mo flat (hours worked at home) or actual-cost proportion; no exclusive-use room requirement for the flat rates.
- **Germany**: Home-office pauschale €6/day (2023+: €1,260/yr cap; Tagespauschale reform), or actual costs for a dedicated room (study) if it's the clear professional center —tpyisch requires an actual dedicated room.
- **Canada**: T2125 detailed method (work-space-in-the-home expenses) vs fixed-rate $2/day temporary flat rate (2020–2022 era); employees need T2200 from employer.
- **Australia**: occupancy + running-cost split; 80¢/h shortcut (fixed) was pandemic-era, 70¢/h revised fixed rate from 2022–23 with an hours log.
The gate/exclusive-use concepts translate loosely; the arithmetic does not. Re-source local numbers before advising non-US filers.

## 8. Sources
IRS Publication 587 (Business Use of Your Home), Form 8829 instructions, Schedule C line 30 worksheet, §280A (gate tests), §121 + §1250 (recapture vs exclusion), TCJA §11045 (employee suspension), CA/FTB nonconformity notes, NY IT-225 telecommuting credit, HMRC HS222, Canada CRA T2125 guide.

Numbers cited are 2025-tax-year-stable; the script exposes every rate as a flag so a law change is a flag edit, not a rewrite.
