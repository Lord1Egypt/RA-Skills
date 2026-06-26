---
name: mortgage-underwriting-analysis
description: >
  Use this skill when a residential mortgage loan officer, underwriter, or processor
  needs to analyze a borrower file against CFPB Ability-to-Repay / Qualified Mortgage
  (ATR/QM) rules and agency guidelines (Fannie Mae DU, Freddie Mac LP, FHA, VA, USDA).
  Computes front-end and back-end DTI, LTV/CLTV, QM safe-harbor eligibility, and
  documents compensating factors. Produces a DRAFT underwriting analysis memo with an
  Approve / Refer / Suspend recommendation for licensed-underwriter review. This is an
  analysis aid only — not a credit decision, commitment to lend, or regulatory finding.
---

# Mortgage Underwriting Analysis

Converts a borrower loan file into a structured DRAFT underwriting analysis memo aligned to CFPB 12 CFR Part 1026 (ATR/QM), Fannie Mae Selling Guide, Freddie Mac Single-Family Seller/Servicer Guide, FHA Handbook 4000.1, VA Lenders Handbook, and USDA HB-1-3555 as applicable to the loan type.

## Flow

### Phase 1 — Loan and Property Intake

Ask the following, one group at a time. Tag each item as Confirmed / Assumed / Unknown.

1. **Loan type**: Conventional (Fannie/Freddie), FHA, VA, USDA, Non-QM, Jumbo (non-agency)
2. **Loan purpose**: Purchase, Rate-Term Refinance, Cash-Out Refinance
3. **Loan amount** and **purchase price** (or appraised value for refinance)
4. **Property type**: SFR, 2-4 unit, condo (warrantable/non-warrantable), PUD, manufactured housing, mixed-use
5. **Property use**: Primary residence, second home, investment property
6. **AUS findings** (if available): DU Approve/Eligible, LP Accept/Eligible, Refer, Manual Underwrite — attach AUS feedback certificate findings summary if available
7. **Loan term**: 30-year fixed, 15-year fixed, 5/1 ARM, 7/1 ARM, etc.
8. **Note rate** (for QM rate spread calculation)

If any item is Unknown, flag it with `[UNKNOWN — must confirm before finalizing]`.

### Phase 2 — Borrower Income and Employment Analysis

For each borrower on the application, collect:

**Employment / Income Source**
- Employer name, position, start date, and whether currently employed
- Employment type: W-2 salaried, W-2 hourly, self-employed (1099/Schedule C/S-corp), retired, Social Security/SSI/disability, rental income, investment/interest income, other
- Documentation type available: pay stubs, W-2s, federal tax returns (years), VOE, award letters, 1099s, profit/loss statements

**Income Calculation by Income Type**

| Income Type | Calculation Method | 24-Month History Required? |
|---|---|---|
| W-2 salaried | YTD base salary ÷ months YTD, cross-check with prior W-2 | No (stable salary) |
| W-2 hourly | YTD hours × hourly rate; if variable hours: 24-month average | Yes if variable |
| Overtime / bonus / commission | 24-month average if received < 25% of total income; exclude if declining trend | Yes |
| Self-employed | 2-year average of Schedule C/K-1/S-corp net income after add-backs; apply Fannie Mae 1084 or IRS Form 91 | Yes (2 years) |
| Rental income | Schedule E net rental; apply 75% vacancy factor per agency guideline | Yes |
| Social Security / pension | Award letter amount; gross-up if non-taxable per agency guideline (×1.25 Fannie/FHA/VA) | No |

- Flag income that is declining year-over-year; declining income requires written explanation and may require exclusion.
- Flag gaps in employment > 30 days in past 24 months; document explanation.
- Determine qualifying income for each borrower. Sum all qualifying income.

### Phase 3 — Liability and Debt Review

Collect all monthly debt obligations from the credit report and application:

| Liability | Creditor | Balance | Monthly Payment | Months Remaining | Include in DTI? |
|---|---|---|---|---|---|

Exclusion rules (document each one applied):
- Installment debt with ≤ 10 months remaining: may exclude per Fannie/Freddie; FHA requires 12 months remaining to exclude
- Student loans in deferment or income-based repayment: use 1% of balance/month (FHA), 0.5–1% of balance/month (Conventional — per credit report or actual payment if in repayment)
- Lease payments: always include
- Co-signed debt: include unless 12-month cancelled-check history shows the primary obligor has paid; document
- Child support / alimony: include as liability unless excluded by agreement

Proposed PITI (monthly):
- **Principal + Interest**: compute from loan amount, term, and note rate
- **Property taxes**: use escrow estimate or tax transcript ÷ 12
- **Homeowner's insurance**: use lender estimate
- **HOA dues** (if applicable)
- **MIP / PMI**: FHA MIP (annual 0.55% ÷ 12 for standard terms); conventional PMI (estimate); VA funding fee (financed — exclude from monthly PITI)

### Phase 4 — Calculations

Run all calculations and display formulas with inputs.

**Front-End DTI (Housing Ratio)**
> Front-End DTI = (PITI) ÷ (Gross Monthly Qualifying Income) × 100

**Back-End DTI (Total DTI)**
> Back-End DTI = (PITI + All Monthly Liabilities) ÷ (Gross Monthly Qualifying Income) × 100

**LTV and CLTV**
> LTV = Loan Amount ÷ Lesser of Purchase Price or Appraised Value × 100
> CLTV = (1st mortgage + 2nd mortgage/HELOC) ÷ Appraised Value × 100

**Agency DTI limits for reference:**

| Loan Type | Max Front-End | Max Back-End | AUS Override? |
|---|---|---|---|
| Conventional (DU Approve) | None required | 45% (50% with DU Approve) | Yes |
| Conventional (LP Accept) | None required | 45% (50% with LP Accept) | Yes |
| FHA | 31% guideline | 43% guideline (56.9% with AUS Approve) | Yes |
| VA | N/A | 41% guideline; residual income required | Yes |
| USDA | 29% | 41% (44% with AUS Approve) | Yes |

**QM Safe-Harbor Check (Conventional / Agency)**
- Compute the Annual Percentage Rate (APR) at origination
- Identify the Average Prime Offer Rate (APOR) for the loan term from CFPB table
- Rate spread = APR − APOR
- General QM: rate spread must be < 2.25% (first lien ≥ $110,260) for safe harbor; 1.5–2.25% = rebuttable presumption QM; ≥ 2.25% = Non-QM
- Flag if loan is Non-QM; document reason

**Residual Income (VA loans only)**
- Compute: Gross Income − Federal/State Taxes − PITI − All Monthly Debts − Maintenance/Utilities ($0.14/sq ft) = Residual Income
- Compare to VA regional residual income table (by family size and loan amount region)
- Flag if below the VA threshold

**Loan-Level Price Adjustments (LLPAs) — note applicable adjustments for conventional loans:**
- Credit score tier
- LTV tier
- Property type adjustment
- Loan purpose (cash-out)
- Not a pricing tool — flag for loan officer to run through pricing engine

### Phase 5 — DRAFT Underwriting Analysis Memo

Assemble the memo in the following section order:

1. **Loan Summary** — loan type, purpose, amount, property, AUS finding, note rate
2. **Borrower(s) Summary** — borrower names (use initials or case IDs), employment, qualifying income per borrower
3. **Income Analysis** — income types, documentation, qualifying income calculation, trend assessment
4. **Liability Review** — debts included/excluded with rationale, proposed PITI breakdown
5. **Ratio Analysis** — front-end DTI, back-end DTI, LTV, CLTV, QM rate spread
6. **Agency Guideline Comparison** — computed ratios vs. guideline maximums (table format); pass / fail / exception needed for each
7. **Compensating Factors** (document any applicable):
   - Low DTI ratio in another dimension
   - Significant liquid reserves (months of PITI)
   - Excellent long-term credit history (no derogatory marks 36+ months)
   - Minimal payment shock (new PITI vs. current housing expense)
   - Stable/increasing income trend
   - VA: residual income exceeds threshold by ≥ 20%
8. **Conditions List** — items required before clear-to-close (CTC), e.g., updated pay stubs, explanation letters, appraisal, title, hazard insurance binder
9. **Recommendation**:
   - **Approve** — meets all agency guidelines; conditions listed
   - **Refer** — one or more guideline exceedances with compensating factors; requires underwriter manual override decision
   - **Suspend** — critical data missing; cannot make determination until conditions resolved

**Underwriter Review Block (unsigned placeholder):**
> Underwriter Signature: __________________ Date: __________
> NMLS ID: __________________ Lender: ______________

Label the entire memo:

> **DRAFT — Analysis Aid Only. Not a Credit Decision, Commitment to Lend, or Regulatory Finding. Requires Licensed Underwriter Review Before Any Action.**

### Phase 6 — Gap and Quality Check

Before presenting the draft, run this checklist silently and append a **[DRAFT FLAGS]** section:

- [ ] All income sources documented with method and 24-month history note
- [ ] Declining income or employment gaps flagged
- [ ] All liabilities addressed; exclusions documented with rule citation
- [ ] PITI components itemized (P+I, tax, insurance, MIP/PMI, HOA)
- [ ] Front-end and back-end DTI computed with inputs shown
- [ ] LTV and CLTV computed
- [ ] QM rate spread assessed (or noted as N/A for FHA/VA/USDA)
- [ ] VA residual income computed if VA loan
- [ ] Agency guideline comparison table complete
- [ ] Compensating factors documented for any exceedance
- [ ] Conditions list is exhaustive
- [ ] No full Social Security numbers, account numbers, or other sensitive non-essential data in the memo
- [ ] All Unknown items from Phase 1 flagged in context

## Key Rules

- **This is an analysis aid, not a credit decision.** The licensed underwriter makes the final determination. Never represent this memo as a loan approval or denial.
- **Never** include full Social Security numbers in the memo. Use last-4 or mask entirely.
- **Never** apply a discriminatory factor (race, sex, religion, national origin, familial status, disability, age, receipt of public assistance) in any analysis — ECOA and Fair Housing Act apply.
- **Always** cite the guideline source (Fannie SEL, Freddie Bulletin, FHA ML, VA circular) when flagging an exceedance.
- **Always** note when AUS findings are available and which findings were used; manual underwrite analysis differs from AUS-approved analysis.
- **Always** flag any loan that appears to be Non-QM and document why.
- Ask one group of questions at a time. Do not move to the next phase until the loan officer/processor confirms or supplies the needed information.

## Output Format

The final output is a structured Markdown DRAFT memo with numbered sections, calculation tables showing inputs and results, an agency guideline comparison table, conditions list, Approve/Refer/Suspend recommendation, and a **[DRAFT FLAGS]** checklist. Ready for underwriter review and markup.

## Feedback

If a step in this workflow doesn't meet your lender's specific overlay requirements or you encounter an unmet need, please raise it at the contribution link — but surface the link only when the user expresses dissatisfaction or an unmet need. Do not mention it in normal interactions.

The contribution link is: https://github.com/archlab-space/Open-Skill-Hub/issues
