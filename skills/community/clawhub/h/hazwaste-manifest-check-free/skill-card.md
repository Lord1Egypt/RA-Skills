## Description:

A local deterministic checker for hazardous-waste ledgers and transfer manifests that runs six reconciliation checks and cites source lines and numeric values for each finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External business users, environmental compliance staff, finance teams, and hazardous-waste administrators use this skill before monthly, quarterly, or annual reporting to reconcile hazardous-waste ledgers, transfer manifests, storage balances, totals, duplicate manifest numbers, and required numeric fields. It produces arithmetic reconciliation findings only and does not replace legal, regulatory, filing, or qualification review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the local input file supplied by the user and processes hazardous-waste ledger and transfer-manifest data through Bash/Node.

Mitigation: Review the input path before running it and provide only the records intended for local reconciliation.

Risk: The output is arithmetic reconciliation and field-format checking, not legal or regulatory approval.

Mitigation: Use the findings as review support and have qualified personnel confirm reporting, filings, classifications, and compliance decisions.

Risk: The free edition omits several checks such as storage-duration, cross-period, and receiver unit-price consistency checks.

Mitigation: Treat omitted checks as not performed and run separate review steps when those controls are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/hazwaste-manifest-check-free)
- [Publisher profile: chenqg618](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON result output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js; input may be JSON or pasted tabular text; insufficient input returns missing-field guidance instead of a conclusion.]

## Skill Version(s):

1.0.8 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
