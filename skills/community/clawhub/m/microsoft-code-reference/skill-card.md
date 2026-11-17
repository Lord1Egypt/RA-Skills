## Description:

Look up Microsoft API references, find working code samples, and verify SDK code is correct.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianqizhang](https://clawhub.ai/user/tianqizhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to verify Microsoft SDK and API usage against Microsoft Learn references, working code samples, and full API pages before or after writing code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI fallback can run or install an unpinned npm package.

Mitigation: Prefer Microsoft Learn MCP tools when available; if using the CLI fallback, avoid elevated privileges, consider pinning a reviewed @microsoft/learn-cli version, and avoid global installation unless persistent tooling is intended.

## Reference(s):

- [Microsoft Learn MCP Server](https://learn.microsoft.com/api/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with documentation references, code examples, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use Microsoft Learn MCP tools or the mslearn CLI fallback when the MCP server is unavailable.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
