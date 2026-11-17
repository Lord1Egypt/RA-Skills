## Description:

Operate Browse AI through an OOMOL-connected account to read robot and task data, start robot tasks, and update robot cookies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to manage Browse AI robots and tasks through an OOMOL-connected account with the oo CLI. It supports read actions, starting robot tasks, and updating robot cookies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs remote code execution, and startup synchronization may make ongoing changes to other agent skills; installer contents were not available for inspection.

Mitigation: Review and approve CLI installation separately. Check the linked command reference for OO_SKILLS_SYNC_DISABLED if startup skill synchronization should be suppressed.

Risk: Starting a robot task changes Browse AI state, and updating cookies replaces a robot's stored cookies.

Mitigation: Confirm the exact action, payload, and robot target before running a task or replacing cookies; obtain approval for each state-changing action.

## Reference(s):

- [OO CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Browse AI API documentation](https://www.browse.ai/docs/api/v2)
- [Browse AI](https://www.browse.ai)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action results are returned as JSON; required inputs vary by action schema.]

## Skill Version(s):

1.0.6 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
