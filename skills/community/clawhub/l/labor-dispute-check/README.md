# Labor Dispute Check

## Use Scenarios

### Scenario 1: Unlawful Termination After 5 Years
An employee with 5 years of service at a tech company is suddenly dismissed without written notice or stated reason, and the HR manager verbally says "your position is eliminated." The employee's monthly salary is ¥25,000. **What the skill does:** Assesses whether the termination meets the legal standard for lawful dismissal (likely not — no documented reason, no prior warning, no severance discussion), calculates the 2N unlawful termination compensation estimate (2 × 5 years × ¥25,000 = ¥250,000), and provides an evidence checklist (employment contract, pay stubs, termination communication records, social insurance records). **Expected outcome:** The employee understands their legal position, has a concrete compensation estimate for negotiation or arbitration, and knows exactly what evidence to preserve before it disappears.

### Scenario 2: Systematic Overtime Without Pay
A factory worker has been working 6 days a week for 2 years, with regular weekday overtime of 3 hours daily and monthly Saturday shifts, but the company only pays the base salary without any overtime compensation. **What the skill does:** Distinguishes between weekday overtime (150% rate), rest-day overtime (200% rate), and checks whether the 36-hour monthly overtime cap is exceeded; calculates the estimated unpaid overtime wages across the 2-year period based on the worker's base hourly rate; flags the 1-year labor arbitration deadline for the most recent claims. **Expected outcome:** A detailed overtime pay estimate that the worker can present to the employer or use as the basis for a labor arbitration filing, with clear awareness of which months' claims are still within the statute of limitations.

### Scenario 3: Probation Period Dispute
A new graduate signs a 1-year employment contract with a 6-month probation period at ¥8,000/month (80% of the ¥10,000 post-probation salary), and is terminated in month 5 with the reason "failed to meet expectations" without any prior performance review or warning. **What the skill does:** Checks the probation legality (for a 1-year contract, max probation is 2 months — the 6-month clause is illegal), verifies the salary ratio (80% is the legal minimum, so this part is compliant), and assesses whether termination during probation was procedurally valid (the employer must prove the employee does not meet hiring criteria — vague "expectations" is insufficient without documented evidence). **Expected outcome:** The graduate learns the probation period itself was illegal beyond month 2, meaning months 3-5 should have been at full salary with full termination protections, and can pursue back pay for the salary difference plus challenge the termination as potentially unlawful.

## Overview

This skill helps employees and employers check common labor law issues, calculate rights and obligations, and understand dispute resolution options. It provides quick assessments of labor situations based on Chinese labor law provisions.

**⚠️ Important Disclaimer**: This tool provides informational assistance only. It does not constitute legal advice, nor does it guarantee any particular outcome. Always consult a qualified labor attorney or the local labor bureau for specific disputes.

## When to Use This Skill

- Checking if termination was lawful
- Calculating severance/economic compensation
- Understanding overtime pay entitlements
- Verifying probation period rules
- Reviewing labor contract terms
- Assessing labor dispute options
- Building an evidence package before negotiation or arbitration

## Common Labor Issues

| Issue | Key Rules |
|-------|-----------|
| Termination & Severance | N+1 for lawful termination, 2N for unlawful; N = years of service × monthly wage |
| Overtime Pay | Weekdays: 150%; Rest days: 200%; Holidays: 300%; Monthly cap: 36 hours |
| Probation Period | 3-month contract → max 1 month; 1-year → max 2 months; 3+ years → max 6 months |
| Labor Contract | Written contract required within 1 month of start; after 2 consecutive fixed terms → indefinite term right |

## Usage

### Basic Check
- "被辞退怎么赔偿" / "加班费怎么算" / "试用期规定" / "劳动纠纷咨询"

### With Context
- "工作3年被辞退，赔偿多少" / "试用期6个月合法吗" / "加班没有加班费怎么办"

## Output Format

For each inquiry the skill provides: issue summary with applicable law, rights calculation with estimated entitlements, key deadlines (1-year labor arbitration limit), suggested next steps, evidence checklist, and disclaimer.

## Evidence Pack

v1.2 adds an evidence-pack workflow for termination, overtime, probation, unpaid wage, and contract disputes.

Use `references/evidence-pack.md` when the user asks whether their materials are enough, what to preserve now, or how to organize an arbitration package.

## Limitations

- Based on general Chinese labor law principles
- May not reflect local regulations or specific circumstances
- Not a substitute for professional legal advice
- Calculations are estimates only

## ⚠️ Critical Deadlines

Labor arbitration must be filed within **1 year** from the date the employee knew or should have known of the rights violation. Do not delay.

## References

- [references/api_reference.md](references/api_reference.md) — Local helper function reference
- [references/evidence-pack.md](references/evidence-pack.md) — Evidence package and arbitration outline
- [scripts/labor-checker.js](scripts/labor-checker.js) — Severance, overtime, and probation calculation helpers

## Tags

`legal` `labor-law` `china` `rights` `dispute` `evidence`
