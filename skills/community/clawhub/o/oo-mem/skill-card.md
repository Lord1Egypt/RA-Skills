## Description:

Mem (mem.ai). Use this skill for ANY Mem request — reading, creating, updating, and deleting data. Whenever a task involves Mem, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to search, read, list, create, update, restore, trash, and delete notes in a user's Mem account. It guides the agent to check each action's current input schema and to obtain confirmation before writes or destructive changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup can automatically execute downloaded software that has not been verified, with effects beyond Mem.

Mitigation: Review and approve the CLI installation before automatic setup, and check its changes to other agents' skills and account access.

Risk: Mem data passes through OOMOL, and permanent deletion remains possible after approval.

Mitigation: Account for OOMOL's handling of Mem data and carefully review deletion actions before approving them.

## Reference(s):

- [Mem homepage](https://mem.ai)
- [Mem API documentation](https://docs.mem.ai/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Text]

**Output Format:** [Mem note content in Markdown and connector results in JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
