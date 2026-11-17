## Description:

GitHub MCP Server enables AI agents to manage GitHub repositories, read and update files, handle issues and pull requests, manage branches and releases, search code, and use GitHub API-backed workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buddhasource](https://clawhub.ai/user/buddhasource)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to let agents perform GitHub repository operations, code review support, issue triage, pull request workflows, release preparation, and documentation updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead agents to use a GitHub token that can modify repositories.

Mitigation: Use fine-grained, repository-limited, read-only tokens unless a task specifically requires write access.

Risk: The documented MCP server package/source is described by the security evidence as unpinned, community maintained, or archived.

Mitigation: Install only from a trusted source, pin the exact version where possible, and review the package before enabling it.

Risk: Agent-driven file updates, merges, releases, issue changes, or pull request actions can affect project state.

Mitigation: Require explicit human approval before write operations, merges, releases, issue changes, or pull request actions.

## Reference(s):

- [MCP Registry](https://registry.modelcontextprotocol.io/)
- [GitHub REST API documentation](https://docs.github.com/en/rest)
- [GitHub REST API rate limits](https://docs.github.com/en/rest/overview/rate-limits-for-the-rest-api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to perform GitHub API-backed reads and writes when configured with appropriate credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
