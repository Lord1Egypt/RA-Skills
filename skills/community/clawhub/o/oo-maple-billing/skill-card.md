## Description:

Use the connected OOMOL Measure account to read, create, and update Measure data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People working with a connected Measure account use this skill to find and retrieve customer, product, pricing, subscription, and checkout data, and to create checkout sessions, create customers, or update customers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs the agent to execute downloaded installer code that has not been verified.

Mitigation: Review and install the CLI separately using a verified release, check its effects on other installed agent skills, and preserve confirmation for every write.

## Reference(s):

- [Measure API Quickstart](https://docs.getmeasure.com/pages/guides/quickstart-with-api)
- [Measure](https://getmeasure.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter; server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
