## Description:

Finds MCP servers, APIs, SaaS products, and developer tools for a task through Laudex and reports how selected services worked after use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pizzaandcupcakes](https://clawhub.ai/user/pizzaandcupcakes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Laudex to discover and compare external services for a task, recommend an appropriate option, and report an outcome after actually using it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Service-search intents are sent to Laudex when the skill is used for third-party tool selection.

Mitigation: Keep search intents limited to the required capability and omit confidential task details.

Risk: Outcome reports are sent to Laudex by default after a service is used, without a separate confirmation prompt.

Mitigation: Set LAUDEX_REPORTING=off to disable reporting, or tell the agent not to report.

Risk: Report notes leave the machine and could expose sensitive information despite scrubbing safeguards.

Mitigation: Exclude user data, secrets, and private identifiers from notes; review with --dry-run before sending. Leave LAUDEX_EMAIL unset unless email registration is intended.

## Reference(s):

- [Laudex homepage](https://laudex.dev)
- [Laudex skill on ClawHub](https://clawhub.ai/pizzaandcupcakes/skills/laudex)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Short service comparisons and recommendations; an outcome notification after a selected service is used.]

## Skill Version(s):

0.5.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
