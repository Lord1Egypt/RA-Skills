## Description:

A Chinese-language local checker for membership-card sales and redemption ledgers that recalculates redemption amounts, reconciles ending liabilities, detects duplicate card sales and missing key fields, and cites source line numbers for each finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance staff, store accountants, and internal auditors use this skill before month-end close, store inventory checks, or membership-card audits to review exported per-card ledger rows for internal consistency. It is intended for local checks of the ledger table, not for deciding membership-policy legality or accounting-standard treatment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may over-rely on ledger consistency findings for accounting, legal, tax, or policy conclusions that the skill does not make.

Mitigation: Treat findings as review prompts and have qualified accounting or compliance reviewers confirm revenue recognition, policy legality, tax treatment, and business decisions.

Risk: The free version omits cross-store, cross-card-type, variance-attribution, cross-period, and card-type completeness checks.

Mitigation: Review the listed checks not run before relying on a clean result, and use additional procedures when those omitted checks matter to the close or audit scope.

Risk: Input files can contain sensitive customer and ledger data.

Mitigation: Run the checker locally as described, pass only the exported file needed for the review, and avoid sharing outputs that expose customer or financial details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/membership-liability-check-free)
- [Skill source README](artifact/SKILL.md)
- [Sample input template](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands]

**Output Format:** [Console text or JSON containing executed checks, withheld checks, line-referenced findings, summary counts, verdict, and insufficient-input details when applicable.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; the free version executes six ledger checks and lists checks that are not included.]

## Skill Version(s):

1.0.5 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
