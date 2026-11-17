## Description:

Explores a user-specified Gitee repository through the Gitee MCP Server and produces a concise overview of its documentation, structure, core modules, technologies, and targeted areas of interest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oschina](https://clawhub.ai/user/oschina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to quickly understand an unfamiliar Gitee repository, including its purpose, technology stack, directory structure, core modules, setup guidance, and optional topic-specific areas such as authentication or database behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository contents supplied to the configured Gitee MCP server may include private or sensitive code or documentation.

Mitigation: Only provide repositories whose contents are appropriate for the configured Gitee MCP server to read and search.

Risk: Generated repository summaries can omit context or mischaracterize project behavior when based on partial files.

Mitigation: Review the report against the repository's source files before relying on it for implementation, security, or architecture decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oschina/skills/gitee-repo-explorer)
- [Publisher profile](https://clawhub.ai/user/oschina)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands]

**Output Format:** [Markdown repository overview report with optional inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured Gitee MCP Server and user-provided repository owner and repository name.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
