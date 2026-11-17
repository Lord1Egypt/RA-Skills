## Description:

Search And Fork helps an agent search Gitee for open source repositories, compare candidates, and fork the selected repository to the user's Gitee account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oschina](https://clawhub.ai/user/oschina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to find Gitee repositories that match their language, license, activity, and project requirements, then fork the chosen repository for contribution or reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a configured Gitee MCP server to search repositories and fork the selected project.

Mitigation: Install only with a trusted Gitee MCP server configuration and review requested actions before approval.

Risk: Approving a fork creates a repository in the user's Gitee account.

Mitigation: Confirm the selected source repository and destination account before allowing the fork action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oschina/skills/gitee-search-and-fork)
- [Publisher profile](https://clawhub.ai/user/oschina)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with repository recommendations, fork results, and suggested next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Gitee MCP tools when configured and requires user selection before forking.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
