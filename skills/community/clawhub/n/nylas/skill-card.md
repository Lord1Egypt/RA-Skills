## Description:

Access and manage email, calendar, and contacts across multiple providers using the Nylas API for unified communication and scheduling tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qasim-nylas](https://clawhub.ai/user/qasim-nylas)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and agents use this skill to inspect and manage email, calendar events, availability, and contacts through Nylas-connected accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured Nylas API key may expose broad email, calendar, and contacts access across connected accounts.

Mitigation: Use the narrowest API key and grant possible, store secrets outside shell history, and set NYLAS_GRANT_ID when the agent should not auto-discover every connected account.

Risk: The skill can send email and create, update, or delete calendar events.

Mitigation: Require explicit human review before sending messages or changing calendar state.

Risk: The skill depends on an external npm plugin that the security evidence describes as unpinned.

Mitigation: Review the plugin and install source before deployment, and prefer a pinned reviewed version when available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qasim-nylas/skills/nylas)
- [Publisher profile](https://clawhub.ai/user/qasim-nylas)
- [Nylas OpenClaw npm package](https://www.npmjs.com/package/@nylas/openclaw-nylas-plugin)
- [Installation guide](https://cli.nylas.com/guides/install-openclaw-nylas-plugin)
- [Nylas CLI](https://cli.nylas.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and tool-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce email, calendar, and contact actions through the Nylas OpenClaw plugin when configured with a Nylas API key.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
