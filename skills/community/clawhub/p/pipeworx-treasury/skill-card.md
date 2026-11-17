## Description:

US fiscal data - national debt, Treasury interest rates, and federal spending breakdowns from the Treasury Fiscal Data API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query official US fiscal data, including current national debt, Treasury security interest rates, and federal spending by category or fiscal year.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute a mutable npm package with local execution authority.

Mitigation: Pin mcp-remote to a reviewed version and run it with minimal filesystem, environment-variable, and credential access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-treasury)
- [Pipeworx Treasury homepage](https://pipeworx.io/packs/treasury)
- [Pipeworx Treasury MCP endpoint](https://gateway.pipeworx.io/treasury/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return Treasury Fiscal Data API results such as debt totals, rates, spending categories, and record dates.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
