## Description:

Audit and validate Prisma Access configurations against best practices and security standards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leesandao](https://clawhub.ai/user/leesandao)

### License/Terms of Use:

MIT-0

## Use Case:

Security engineers, network administrators, and compliance reviewers use this skill to audit Prisma Access configuration data for policy misconfigurations, object hygiene issues, operational gaps, and alignment with PAN-OS best practices and CIS benchmarks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may receive sensitive Prisma Access configuration data during an audit.

Mitigation: Use the skill only with configuration data the operator is comfortable providing to the agent, and avoid supplying secrets or unnecessary sensitive details.

Risk: Audit recommendations may be incomplete or unsuitable for a specific production environment.

Mitigation: Have a qualified security or network engineer review findings before applying changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leesandao/skills/prisma-audit)
- [Project homepage](https://github.com/leesandao/prismaaccess-skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown audit report with severity-tagged findings, recommendations, references, and summary metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include severity, category, location, risk, recommendation, and reference when available.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
