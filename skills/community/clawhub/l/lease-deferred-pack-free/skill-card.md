## Description:

A local Chinese-language checker for lease liability and deferred government grant worksheets that runs two cross-period consistency checks per contract directory and reports one conclusion line per contract with source file and line references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

General ledger accounting teams use this skill before monthly amortization review or annual settlement to check lease liability, right-of-use asset, government grant, and deferred income worksheets across contract folders. It identifies arithmetic and consistency issues, lists checks that did not run, and cites the original file and line for each finding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill checks arithmetic and worksheet consistency, but its output could be mistaken for audit, tax, or accounting judgment.

Mitigation: Use the findings as review evidence only, and have qualified accounting, audit, or tax reviewers confirm conclusions before posting entries or making filings.

Risk: Missing, empty, or unrecognized contract materials are reported as not run rather than clean.

Mitigation: Review the not-run checks and missing-material messages for every contract before relying on a clean summary.

Risk: The free release omits cross-contract summary outputs and several sub-checks listed in the results.

Mitigation: Treat checks_not_run and sub_checks_not_run as explicit coverage gaps and run additional controls where those checks matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/lease-deferred-pack-free)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON reports with per-contract conclusions, source file and line references, not-run checks, and summary counts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library, reads user-provided worksheet text or JSON, and prints results to stdout without network use or file writes.]

## Skill Version(s):

1.0.20 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
