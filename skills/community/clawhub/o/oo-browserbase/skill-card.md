## Description:

Browserbase (browserbase.com). Use this skill for ANY Browserbase request — reading, creating, updating, and deleting data. Whenever a task involves Browserbase, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to manage Browserbase projects, sessions, and contexts through their connected account. It guides the agent to check each action's schema and obtain approval for actions that change or delete data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run unverified installers and may make broader changes to installed agent skills.

Mitigation: Review and approve CLI installation separately using a verified release. Consider disabling startup skill synchronization with OO_SKILLS_SYNC_DISABLED=1, keep approval checks for writes and deletion, and note that remote installers and hosted runtime behavior were not verified.

## Reference(s):

- [Browserbase API documentation](https://docs.browserbase.com/introduction/getting-started)
- [Browserbase](https://www.browserbase.com)
- [oo CLI command reference: environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Structured Browserbase results and Markdown guidance with oo CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are returned by the connected Browserbase service; actions that change or delete data require approval.]

## Skill Version(s):

1.0.6 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
