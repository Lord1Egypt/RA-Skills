## Description:

Graphql Client is a reference skill for developers that prints local guidance for intro, quickstart, patterns, debugging, performance, security, migration, and cheatsheet topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as a quick local reference for GraphQL client concepts, common workflows, debugging, performance, security, migration, and command cheatsheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reference text is shallow and generic rather than authoritative GraphQL client documentation.

Mitigation: Validate operational decisions against the specific GraphQL client library or platform documentation before applying the guidance.

Risk: The cheatsheet labels a troubleshooting command, while the skill command table and script expose the debugging command.

Mitigation: Use `graphql-client debugging` for troubleshooting guidance.

Risk: The script reports version 2.0.1 while release evidence and SKILL.md identify version 2.0.2.

Mitigation: Treat 2.0.2 as the release version and verify the CLI version string before relying on it for automation or audit records.

## Reference(s):

- [BytesAgain homepage](https://bytesagain.com)
- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/graphql-client)
- [Publisher profile](https://clawhub.ai/user/xueyetianya)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text and Markdown reference content printed by shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local heredoc output; no external API calls, credentials, or network access indicated.]

## Skill Version(s):

2.0.2 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
