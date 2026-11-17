## Description:

Use the OOMOL-connected TaxJar account to read, calculate, create, update, and delete TaxJar data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and finance or operations teams use this skill to retrieve TaxJar rates and records, calculate sales tax, manage customers and transactions, and validate VAT numbers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI is missing, setup may invoke a remote installer without a separate approval step or integrity check.

Mitigation: Install from a pinned and verified release before setup, and consider its effects on other installed skills. Confirm account changes before execution and explicitly approve destructive actions.

## Reference(s):

- [TaxJar API Reference](https://developers.taxjar.com/api/reference/)
- [TaxJar](https://www.taxjar.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the oo CLI and a connected TaxJar account; write actions require confirmation and destructive actions require explicit approval.]

## Skill Version(s):

1.0.6 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
