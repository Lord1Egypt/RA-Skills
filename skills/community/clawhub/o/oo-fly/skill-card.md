## Description:

Operate Fly.io apps and Machines through the OOMOL-connected oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect and manage Fly.io apps and Machines through an already connected OOMOL account. It covers read operations and lifecycle changes, with approval required for changes and destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run unchecked downloads, and startup skill synchronization may change other agents’ installed skills without clear approval.

Mitigation: Review setup before installing, use a reviewed CLI release, and consider disabling startup synchronization with OO_SKILLS_SYNC_DISABLED=1.

Risk: Hosted credential handling was not independently verified.

Mitigation: Use a narrowly scoped Fly.io connection and retain approval requirements for cloud changes.

## Reference(s):

- [Fly.io Machines API documentation](https://fly.io/docs/machines/api/working-with-machines-api/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Fly.io](https://fly.io/)

## Skill Output:

**Output Type(s):** [API calls, JSON, Shell commands, Operational guidance]

**Output Format:** [Markdown guidance with oo CLI shell commands and JSON payloads or responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read Fly.io state or change machine state; write and destructive actions require user approval.]

## Skill Version(s):

1.0.6 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
