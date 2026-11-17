## Description:

PKULaw (mcp.pkulaw.com). Use this skill for ANY PKULaw request — searching and reading data. Whenever a task involves PKULaw, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Legal professionals and researchers can use the connected PKULaw service to search laws, regulations, provisions, and judicial cases, and retrieve specific law articles. The skill also guides users through checking live action schemas before making requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run downloaded CLI code whose provenance has not been verified.

Mitigation: Review the CLI release and verify its provenance before installation.

Risk: The CLI may install or synchronize additional agent skills without clearly disclosing the changes.

Mitigation: Review what the CLI will install or synchronize and limit which skills it may add.

Risk: Legal searches may include confidential or unnecessary facts.

Mitigation: Send only the legal facts needed for the search and remove unnecessary confidential details.

## Reference(s):

- [PKULaw](https://mcp.pkulaw.com)
- [PKULaw MCP integration documentation](https://mcp.pkulaw.com/docs?doc=mcp-integration)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON request payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands depend on the user's connected PKULaw account and the live action schema.]

## Skill Version(s):

1.0.4 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
