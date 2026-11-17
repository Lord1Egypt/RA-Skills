## Description:

Search and read data in Cin7 Core through the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users with an OOMOL-connected Cin7 Core account use this skill to view account settings and retrieve customer and product records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified remote code without a separate user approval step.

Mitigation: Review and install the CLI separately from a verified release before allowing the skill to run; check its automatic agent-skill synchronization settings and confirm that routing Cin7 access through OOMOL is acceptable.

## Reference(s):

- [Cin7 Core API documentation](https://dearinventory.docs.apiary.io/)
- [Cin7 Core](https://www.cin7.com/solutions/core/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON inputs and JSON responses, plus Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only account, customer, and product data.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
