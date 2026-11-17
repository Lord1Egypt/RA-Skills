## Description:

Search, compare, and analyze 330K+ open-source GitHub repositories by growth rate, acceleration, and originality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alessandroflati](https://clawhub.ai/user/alessandroflati)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to research open-source GitHub repositories, compare project momentum, discover alternatives, and check dependency or license options through the oosmetrics MCP integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a pinned npm MCP package and uses the user's oosmetrics API key.

Mitigation: Use a dedicated, revocable OOSMETRICS_API_KEY and run the agent in a sandboxed or isolated environment when unrelated sensitive files or variables are present.

## Reference(s):

- [Oosmetrics ClawHub Skill](https://clawhub.ai/alessandroflati/skills/oosmetrics)
- [Oosmetrics API Key Profile](https://oosmetrics.com/profile)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, text, markdown]

**Output Format:** [Markdown with inline shell commands and natural-language tool guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the user's oosmetrics subscription tier and API-backed repository metrics.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
