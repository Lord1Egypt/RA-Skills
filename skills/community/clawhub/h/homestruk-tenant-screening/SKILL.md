---
version: 1.0.0
name: homestruk-tenant-screening
description: Screen tenant applications using Fair Housing compliant criteria for Massachusetts properties. Use when evaluating a rental application, setting screening criteria, checking an applicant against standards, or drafting acceptance/rejection letters. Covers income verification, credit checks, criminal background (with HUD guidance), rental history, and MA-specific protected classes.
user-invocable: true
tags:
  - property-management
  - tenant-screening
  - fair-housing
  - massachusetts
  - rental-application
---

# Homestruk Tenant Screening

Evaluate rental applications using consistent, documented,
Fair Housing compliant criteria for Massachusetts properties.

## When to Use This Skill

- "I got an application for [property]"
- "Should I approve this tenant?"
- "What are my screening criteria?"
- "Draft a rejection letter for [applicant]"
- "Is this screening criteria legal in MA?"

## CRITICAL: Fair Housing Compliance

NEVER screen based on these protected classes:
Federal: race, color, national origin, religion, sex,
familial status, disability
Massachusetts adds: marital status, sexual orientation,
gender identity, age, ancestry, genetic information,
military/veteran status, receipt of public assistance
or housing subsidy (SOURCE OF INCOME)

MA SOURCE OF INCOME LAW: You CANNOT reject an applicant
because they pay with Section 8, MRVP, VASH, or other
housing vouchers. This is one of the most commonly
violated Fair Housing rules in MA.

Apply the SAME criteria to EVERY applicant. Document
everything. Subjective rejections invite lawsuits.

## Screening Criteria (apply consistently)

### 1. Income Verification
Standard: Gross monthly income >= 3x monthly rent
Documents: 2 most recent pay stubs, tax return, or
employment verification letter.
Self-employed: 2 years tax returns + bank statements
Voucher holders: voucher amount counts toward income
Cosigner: accepted if cosigner meets 5x rent income

### 2. Credit Check
Run through TransUnion, Experian, or Equifax
Minimum score: 620 (document this threshold)
Red flags: active collections > $1000, recent bankruptcy,
judgments from prior landlords
No minimum score for voucher holders (many have thin credit)
Consider: medical debt should be weighted less

### 3. Criminal Background
Follow HUD guidance (2016 memo + updates):
- NEVER blanket-reject based on criminal record
- Conduct individualized assessment for each applicant
- Consider: nature of offense, time since offense,
  evidence of rehabilitation
- NEVER consider arrests without conviction
- MA CORI rules: can only access certain records
- Drug-related convictions: case-by-case, not automatic reject
- Sex offender registry: may reject if registered

### 4. Rental History
Contact 2 most recent landlords (skip current if concerned
about retaliation/bias)
Ask: rent paid on time? lease violations? property damage
beyond normal wear? would you rent to them again?
Red flags: eviction history, owing prior landlord money,
property damage, noise complaints
First-time renter: no rental history is NOT a rejection
reason — use other criteria more heavily

### 5. Employment Verification
Confirm: employer name, position, start date, salary
Self-employed: business license + tax returns
Retired: Social Security statement, pension, or savings

### 6. ID Verification
Valid government-issued photo ID
Social Security number (for credit/background check)
Do NOT photocopy immigration documents beyond what is
needed for identity verification

## Screening Decision Matrix

| Criteria | Pass | Conditional | Fail |
|----------|------|-------------|------|
| Income | 3x+ rent | 2.5-3x (cosigner) | Below 2.5x |
| Credit | 620+ | 580-619 (extra deposit) | Below 580 |
| Criminal | Clear or minor/old | Case-by-case review | Recent violent/drug mfg |
| Rental | Positive refs | Mixed/no history | Eviction or damage |
| Employment | Verified stable | New job/self-employed | Cannot verify |

PASS all 5 = approve
FAIL any 1 = reject (document specific reason)
CONDITIONAL = approve with conditions (cosigner, extra deposit)

## Rejection Letter Template

When rejecting, you MUST provide an adverse action notice
per the Fair Credit Reporting Act (FCRA) if a credit or
background check was used in the decision.

```
Dear [APPLICANT NAME],

Thank you for your application for [ADDRESS].

After careful review, we are unable to approve your
application at this time. This decision was based on
[SPECIFIC CRITERIA - e.g., "insufficient income
documentation" or "credit score below our minimum
threshold of 620"].

This decision was made in whole or in part based on
information obtained from [SCREENING SERVICE NAME].
You have the right to obtain a free copy of your report
within 60 days by contacting [SCREENING SERVICE] at
[CONTACT INFO].

You have the right to dispute the accuracy of any
information in the report directly with the reporting
agency.

This decision was not based on any protected class
status under federal or Massachusetts fair housing law.

Sincerely,
[PM NAME]
Homestruk Properties
```

Save to: ~/.openclaw/workspace/drafts/rejection-[name]-[date].md

## Acceptance Process

When approving:
1. Send approval notice with lease signing instructions
2. Collect: first month, last month, security deposit (max
   1 month per MA law), lock change fee
3. NO other fees allowed at inception (MGL c.186 s.15B)
4. Schedule lease signing and move-in date
5. Prepare move-in packet (SOP: tenant-onboarding.md)

## Integration
- Reference SOP: ~/.openclaw/workspace/sops/tenant-onboarding.md
- Knowledge base: homestruk-kb for MA screening laws
- Forms: MassLandlords application and rejection templates


---

## About Homestruk

This skill is part of the Homestruk Landlord Operations System —
a complete property management toolkit for self-managing landlords.

**Free:** Download the Rent-Ready Turnover Checklist at homestruk.com
**Full System:** 10 operations documents + spreadsheets at homestruk.com

Built by Homestruk Properties LLC | homestruk.com
