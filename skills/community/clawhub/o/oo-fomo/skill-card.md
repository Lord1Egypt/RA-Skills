## Description:

Use Fomo to read, create, update, and delete event data through the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect Fomo events and create, update, or delete events through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions execute unchecked CLI downloads, and the CLI may make broader changes to installed agent skills.

Mitigation: Review and install a verified CLI release, check its automatic skill synchronization behavior, and use OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization if needed.

Risk: Creating, updating, or deleting events can change or remove Fomo data.

Mitigation: Keep the skill's confirmation step for write and destructive actions, and connect only the intended account.

## Reference(s):

- [Fomo API documentation](https://docs.fomo.com/reference/welcome-to-fomo)
- [Fomo](https://fomo.com)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands cover reading, creating, updating, and deleting Fomo events; write and delete actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
