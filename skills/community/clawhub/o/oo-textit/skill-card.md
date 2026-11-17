## Description:

TextIt (textit.com). Use this skill for ANY TextIt request — reading, creating, updating, and deleting data. Whenever a task involves TextIt, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected TextIt account can use this skill to read workspace data and manage contacts, groups, messages, and broadcasts through the oo CLI. It guides users to inspect each action's schema and confirm state-changing or destructive actions before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to execute downloaded software without separate approval or integrity checks, and the remote installer payloads remain unverified.

Mitigation: Install a reviewed, pinned CLI yourself and require approval before any downloaded installer runs. Consider disabling automatic skill synchronization with OO_SKILLS_SYNC_DISABLED=1, as documented in the oo CLI command reference.

Risk: Actions can send messages or broadcasts and can delete contacts or groups in TextIt.

Mitigation: Check message recipients and deletion targets carefully; confirm the exact payload and effect before write actions, and explicitly approve destructive actions.

## Reference(s):

- [TextIt](https://textit.com)
- [TextIt API documentation](https://textit.com/api/v2/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI install guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API responses, JSON, Shell commands, Guidance]

**Output Format:** [JSON action payloads and responses with shell commands and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read or change TextIt data; writes and destructive actions require user confirmation as described in the skill.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
