## Description:

Helps agents complete Gitee issue implementation workflows from issue retrieval and requirements analysis through coding assistance, pull request creation, and issue updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oschina](https://clawhub.ai/user/oschina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to turn Gitee issues into implementation plans, code changes, pull requests, and linked issue updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide or trigger visible Gitee project actions such as posting comments, creating pull requests, and updating issue status.

Mitigation: Review the target repository, issue, and proposed write actions before allowing the configured Gitee MCP tools to execute them.

Risk: The skill requires a local repository checkout and may propose code changes based on issue context.

Mitigation: Review generated implementation plans and code changes, then run the repository's normal tests before creating or merging a pull request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oschina/skills/gitee-implement-issue)
- [Publisher profile](https://clawhub.ai/user/oschina)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with issue comments, pull request descriptions, code examples, and command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use configured Gitee MCP tools to read issues, post comments, create pull requests, and update issue status.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
