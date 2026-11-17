## Description:

Pingback (pingback.com). Use this skill for ANY Pingback request — reading, creating, updating, and deleting data. Whenever a task involves Pingback, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users with a connected Pingback account can read subscriber details, create and update subscribers, and manage segmentation membership through the oo CLI. The skill requires approval before write actions and explicit approval before destructive updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs execution of remote CLI installers whose contents were unavailable for inspection.

Mitigation: Install a verified oo CLI release yourself and review the installer and release before running it.

Risk: The CLI may make broader changes through automatic skill synchronization, and OOMOL mediates access to subscriber data.

Mitigation: Decide whether to permit automatic skill synchronization, disable it when appropriate using the CLI environment settings, and use the connected account only for intended subscriber operations.

Risk: Subscriber creation, updates, and segment changes alter Pingback data; updates can unsubscribe subscribers.

Mitigation: Confirm the exact payload and effect before write actions, and obtain explicit approval for destructive updates.

## Reference(s):

- [oo CLI command and environment variable reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [Pingback API documentation](https://developer.pingback.com/docs/api/introduction)
- [Pingback homepage](https://pingback.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance, Shell commands]

**Output Format:** [Structured JSON requests and responses with Markdown guidance and oo CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs must follow the live connector schema; write and destructive actions require user approval.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
