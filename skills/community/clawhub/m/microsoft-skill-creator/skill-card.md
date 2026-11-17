## Description:

Create agent skills for Microsoft technologies using Learn MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianqizhang](https://clawhub.ai/user/tianqizhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create focused agent skills for Microsoft technologies such as Azure, .NET, Microsoft 365, VS Code, Bicep, SDKs, frameworks, and APIs. It guides topic investigation with Microsoft Learn tools and turns the findings into local skill instructions, references, and examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback workflow may run or globally install a mutable, unpinned npm CLI package.

Mitigation: Prefer the Microsoft Learn MCP tools when available; if the CLI fallback is needed, pin and vet the package version, avoid global installation where possible, and run it in a controlled environment.

Risk: Generated skills may contain incomplete, stale, or misleading Microsoft technology guidance if the investigation results are not reviewed.

Mitigation: Review generated skill content, validate suggested Learn searches and code samples, and scan the skill before deployment.

## Reference(s):

- [Microsoft Learn MCP Server](https://learn.microsoft.com/api/mcp)
- [Skill Templates](references/skill-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown skill files with optional code samples, shell command examples, and reference material]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated skills balance concise local guidance with dynamic Microsoft Learn lookups.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
