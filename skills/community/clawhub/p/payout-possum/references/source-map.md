# Payout Possum Source Map

Use this file as the working checklist for category coverage. Prefer official sources first and use aggregators only as leads.

## Category Order

1. State unclaimed property
2. Federal and state government money
3. Tax and offset notices
4. Retirement and pension money
5. Banking, brokerage, insurance, mortgage, escrow, and utilities
6. Bankruptcy unclaimed funds
7. Class actions
8. Agency refunds and restitution
9. Employment, healthcare, and niche categories
10. Gmail evidence search

## Category Notes

### 1. State unclaimed property

Typical items:

- Dormant bank accounts
- Payroll checks
- Utility deposits
- Insurance proceeds
- Stock proceeds
- Safe deposit contents

Priority:

- Official state unclaimed-property sites
- NAUPA directory
- MissingMoney where supported

Capture:

- States searched
- Name variants used
- Match/no-match notes

### 2. Federal and state government money

Typical items:

- Treasury-related claims
- FHA or HUD-related refunds
- Credit-union liquidation or failed-institution balances
- Other agency-held money

Priority:

- Official agency or court site
- Verified state agency source

### 3. Tax and offset notices

Typical items:

- Federal or state refund status
- Offset or seizure notices
- Old tax correspondence indicating unresolved balances or refunds

Priority:

- IRS or state department of revenue site
- User mail or email records

Avoid giving tax advice beyond routing, status lookup, and record organization.

### 4. Retirement and pension money

Typical items:

- PBGC unclaimed retirement funds
- Terminated plan balances
- Former employer pensions
- Union or industry plan balances

Priority:

- PBGC
- Former employer plan administrator
- Union or plan provider

### 5. Banking, brokerage, insurance, mortgage, escrow, and utilities

Typical items:

- Dormant deposit balances
- Old brokerage or mutual-fund balances
- Insurance proceeds
- Mortgage escrow overages
- Utility deposits

Priority:

- Institution directly
- State unclaimed-property office if funds were escheated

### 6. Bankruptcy unclaimed funds

Typical items:

- Uncashed distributions
- Returned checks
- Creditor distributions never delivered

Priority:

- Official U.S. Courts or bankruptcy court source
- Case-specific docket or trustee records

### 7. Class actions

Typical items:

- Consumer settlements
- Securities settlements
- Antitrust settlements
- Product or service overcharge settlements

Priority:

- Official settlement administrator site
- Court-approved notice
- Reputable settlement databases only as discovery tools

Rule:

- Never treat a roundup site as proof that the user is eligible.

### 8. Agency refunds and restitution

Typical items:

- FTC refund programs
- CFPB or attorney general restitution actions
- Regulatory settlements

Priority:

- Agency source
- Court monitor or administrator named by the agency

### 9. Employment, healthcare, and niche categories

Examples:

- Wage-and-hour settlements
- Overpayment reimbursements
- Medical billing refunds
- Tuition or campus-account credits
- Telecom or utilities overcharge programs

Work from the user’s history:

- Employers
- Providers
- Schools
- Services used

### 10. Gmail evidence search

Use when the user enables inbox work and `gog` is available.

Default search families:

```text
settlement OR "class action" OR claimant OR claimform OR "claim form"
refund OR reimbursement OR restitution OR overpayment
escrow OR surplus OR disbursement
pension OR retirement OR benefit OR 401k OR "defined benefit"
administrator OR "settlement administrator" OR "claims administrator"
bankruptcy OR trustee OR distribution
insurance OR demutualization OR policyholder
unclaimed OR escheat OR dormant account
```

Useful narrowing terms:

- Old email domains the user used
- Known administrator names
- Bank, insurer, employer, or plan names
- Date windows tied to moves, jobs, or product usage

Default Gmail rules:

- Read and summarize
- Extract deadlines, claimant IDs, source names, and links
- Do not send or modify mail unless the user requests it

## Tracker Template

Use this format in the session output:

```text
Category | Source | Search terms / identifiers | Result | Confidence | User action
State unclaimed property | [state site] | [name variant + state] | possible match | confirmed source | verify prior address
Pension | PBGC | [last name + last4 if provided] | needs input | confirmed source | need SSN last 4
Class actions | [administrator] | [email + product + date range] | checked | possible lead | await stronger proof
```

## Closing Format

Always end with:

1. What I checked
2. Possible money found
3. What still needs your input
4. Next 3 actions
5. Watchlist
