## Description:

Manage Google Tasks by listing and reading tasks and task lists, and creating, updating, moving, or deleting them through the connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to review and manage their Google Tasks lists and tasks through an OOMOL-connected account. The skill guides the agent to inspect each action's schema and to seek confirmation before changes or destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run an online installer that has not been verified, and the hosted connector implementation was not verified.

Mitigation: Use a reviewed, pinned oo CLI and require approval before executing its installer. Review automatic skill synchronization and set OO_SKILLS_SYNC_DISABLED=1 to disable it if needed.

Risk: The integration uses an OOMOL-connected Google Tasks account.

Mitigation: Use the integration only if you are comfortable trusting OOMOL with the Google Tasks connection; follow the documented confirmation steps for changes.

Risk: Write and destructive actions can change or remove Google Tasks data.

Mitigation: Confirm the exact payload before write actions and obtain explicit approval before destructive actions.

## Reference(s):

- [Google Tasks](https://tasks.google.com)
- [Google Tasks API reference](https://developers.google.com/workspace/tasks/reference/rest)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, API Calls]

**Output Format:** [Shell commands with JSON payloads and connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions are safe to run directly; confirm exact payloads for write actions and obtain explicit approval for destructive actions.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
