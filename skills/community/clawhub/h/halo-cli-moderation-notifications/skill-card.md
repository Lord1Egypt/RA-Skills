## Description:

This skill guides agents through Halo CLI comment moderation, reply creation, unread notification management, and notification deletion or read-state updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruibaby](https://clawhub.ai/user/ruibaby)

### License/Terms of Use:

MIT-0

## Use Case:

External Halo site operators and agents use this skill to moderate comments and replies, create official replies, and manage unread notifications with the Halo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Destructive delete commands can remove Halo comments, replies, or notifications when run with --force.

Mitigation: Verify the selected profile and exact resource ID before deletion; prefer review, get, or mark-as-read commands unless deletion is explicitly requested.

Risk: Moderation actions can affect the wrong Halo environment if the default profile is unintended.

Mitigation: Use --profile <name> when moderating a non-default environment and confirm the selected profile when a resource is not found.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ruibaby/skills/halo-cli-moderation-notifications)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Halo CLI commands that mutate comments, replies, or notifications when executed by the agent.]

## Skill Version(s):

0.1.1 (source: server release evidence; artifact frontmatter version 1.0.0 differs)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
