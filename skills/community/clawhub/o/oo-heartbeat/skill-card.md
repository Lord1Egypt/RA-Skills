## Description:

Heartbeat (heartbeat.chat). Use this skill for ANY Heartbeat request — searching and reading data. Whenever a task involves Heartbeat, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with a connected Heartbeat account can search community users and read user, group, channel, and event data through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup offers a remote CLI installer, and the CLI's agent-skill syncing behavior has not been inspected.

Mitigation: Review and install a verified CLI separately, prevent automatic execution of the remote installer fallback, and review the CLI's syncing behavior before enabling the skill.

Risk: The connected account can expose Heartbeat community user and membership data.

Mitigation: Connect only the intended Heartbeat account and review retrieved data before sharing it.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Heartbeat](https://www.heartbeat.chat)
- [Heartbeat authorization documentation](https://heartbeat.readme.io/reference/authorization)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Text responses based on Heartbeat data returned as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only search and retrieval of Heartbeat community data]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
