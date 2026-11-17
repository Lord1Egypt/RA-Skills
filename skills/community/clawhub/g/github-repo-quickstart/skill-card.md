## Description:

This skill helps users quickly understand an unfamiliar GitHub repository's purpose, architecture, setup, dependencies, entrypoints, releases, and maintenance status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[starquakee](https://clawhub.ai/user/starquakee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to produce a compact onboarding guide for an unfamiliar GitHub repository, including its architecture, setup path, entrypoints, release status, and practical pitfalls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository metadata and file contents may be retrieved through the declared GitHub MCP integration, including private repository content when the user asks about a private repo.

Mitigation: Install and invoke this skill only when that repository data flow is acceptable, and use extra caution with private repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/starquakee/skills/github-repo-quickstart)
- [GitHub MCP service endpoint](https://api.githubcopilot.com/mcp/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with annotated directory trees and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Matches the user's language for headings and explanations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
