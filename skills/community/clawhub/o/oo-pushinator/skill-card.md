## Description:

Operate Pushinator through an OOMOL-connected account, including creating channels and sending notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to create Pushinator notification channels and send notifications through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute a remote installer whose complete local effects were not inspected.

Mitigation: Install a reviewed, verified oo CLI release yourself and prevent automatic setup execution.

Risk: Startup skill synchronization may install additional agent skills, and its broader effects are unclear.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 before invoking oo if you do not want startup skill synchronization.

Risk: Notifications pass through OOMOL and can reach a channel's subscribers.

Mitigation: Confirm the notification channel and exact content before sending.

## Reference(s):

- [Pushinator API documentation](https://pushinator.com/api)
- [Pushinator homepage](https://pushinator.com)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
