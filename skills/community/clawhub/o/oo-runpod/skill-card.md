## Description:

Runpod (runpod.io). Use this skill for ANY Runpod request — reading, creating, updating, and deleting data. Whenever a task involves Runpod, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and manage Runpod Pods through an OOMOL-connected account. It guides the agent to check each action's schema and obtain approval before write or destructive operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can run an unchecked installer with broader effects on the agent; external installers and the hosted connector were not audited.

Mitigation: Review and install the oo CLI separately before using the skill, and disable cross-agent skill synchronization if it is unwanted.

Risk: Runpod write and destructive actions can change or remove resources.

Mitigation: Use narrowly scoped Runpod credentials and retain user approval for changes and deletions.

## Reference(s):

- [Runpod API documentation](https://docs.runpod.io/api-reference/overview)
- [Runpod](https://www.runpod.io)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target Runpod actions through the oo CLI.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
