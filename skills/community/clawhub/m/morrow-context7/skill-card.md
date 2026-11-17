## Description:

Look up current, accurate documentation and code examples for any library or framework using context7-mcp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timesandplaces](https://clawhub.ai/user/timesandplaces)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to retrieve current library documentation, method signatures, configuration details, and code examples when answering implementation questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned third-party MCP package through npx, so executed code can change after review.

Mitigation: Pin @upstash/context7-mcp to a reviewed exact version, use a locked dependency workflow, and restrict filesystem, credential, and network access where possible.

Risk: The skill requires network access and npx, which may fail or be inappropriate in restricted environments.

Mitigation: Confirm npx and network access are allowed before use, or configure the MCP server through an approved managed environment.

## Reference(s):

- [Context7](https://context7.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with documentation snippets and inline code or shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source URLs from retrieved documentation when precision matters.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
