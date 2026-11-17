## Description:

Analyzes residential mortgage borrower files against CFPB ATR/QM rules and agency guidelines, computes DTI, LTV/CLTV, and QM safe-harbor eligibility, and produces a draft underwriting analysis memo for licensed-underwriter review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Loan officers, underwriters, processors, and mortgage teams use this skill to draft pre-underwrite analyses, calculate borrower and property ratios, compare results with applicable agency guidelines, and prepare an Approve, Refer, or Suspend memo for licensed-underwriter review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mortgage underwriting is high-impact and regulated, and draft analysis could be mistaken for a final credit decision.

Mitigation: Use only as a drafting and checklist aid, verify current agency and CFPB rules, and require licensed-underwriter review before taking action.

Risk: Borrower files may contain sensitive personal and financial information.

Mitigation: Minimize borrower PII and avoid entering full Social Security numbers or account numbers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/archlab-space/skills/mortgage-underwriting-analysis)
- [Publisher Profile](https://clawhub.ai/user/archlab-space)

## Skill Output:

**Output Type(s):** [text, markdown, analysis, guidance]

**Output Format:** [Structured Markdown draft memo with calculation tables, agency guideline comparison, conditions list, recommendation, and draft flags checklist.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied borrower and loan-file inputs; does not access live AUS systems, credit bureaus, or pricing engines.]

## Skill Version(s):

0.1.0 (source: release evidence and changelog, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
