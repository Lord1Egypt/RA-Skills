## Description:

Search and read Fern customer, payment account, exchange rate, and transaction data through the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use the skill to retrieve Fern customer, payment account, exchange rate, and transaction information through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup runs remote installer code, and the resulting CLI behavior may include automatic changes to other agents' skills.

Mitigation: Install and review the oo CLI separately before allowing this skill to run, including any automatic changes to other agents' skills.

Risk: Using this skill involves requested Fern financial data being handled through OOMOL.

Mitigation: Use narrowly scoped Fern credentials and understand that OOMOL handles the requested financial data.

## Reference(s):

- [Fern API documentation](https://docs.fernhq.com/)
- [Fern](https://fernhq.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Text and structured Fern data, with JSON payload examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Fern account and the action's input schema.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
