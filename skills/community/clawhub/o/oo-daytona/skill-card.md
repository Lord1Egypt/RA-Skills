## Description:

Daytona (daytona.io). Use this skill for ANY Daytona request — reading, creating, updating, and deleting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other Daytona users can use the skill to inspect and manage sandboxes through their OOMOL-connected Daytona account, including creating, listing, starting, stopping, and deleting sandboxes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup instructs running a remote CLI installer whose contents were unavailable for review.

Mitigation: Review and approve CLI installation separately; prefer an inspected, version-pinned installer with integrity verification.

Risk: The connected Daytona account can access resources and sandbox changes can have lasting effects.

Mitigation: Limit the connected account's permissions and retain user confirmation for sandbox changes.

## Reference(s):

- [Daytona sandbox documentation](https://www.daytona.io/docs/sandboxes)
- [ClawHub Daytona release](https://clawhub.ai/oomol/skills/oo-daytona)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and payloads follow the selected Daytona action schema; write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
