## Description:

Manage the Lumail email marketing platform through CLI commands and a TypeScript SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[melvynx](https://clawhub.ai/user/melvynx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to help agents manage Lumail subscribers, campaigns, tags, transactional emails, event tracking, email verification, and V2 tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may act on live Lumail subscribers, campaigns, transactional emails, tags, and events.

Mitigation: Require explicit user confirmation before sends, deletes, unsubscribes, campaign changes, or other account-changing actions, and use least-privilege API tokens.

Risk: API tokens can expose Lumail account access, especially when commands display raw credentials.

Mitigation: Avoid raw token display in shared contexts, store credentials securely, rotate exposed tokens, and restrict token permissions where possible.

Risk: The skill directs agents to install and run the Lumail npm package and CLI.

Mitigation: Pin or otherwise verify the package before execution, and review generated commands before running them.

## Reference(s):

- [Lumail API endpoint](https://lumail.io/api)
- [ClawHub skill page](https://clawhub.ai/melvynx/skills/lumail)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose live Lumail API and CLI actions that should be reviewed before execution.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
