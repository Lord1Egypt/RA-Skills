## Description:

Use the OOMOL-connected Permit.io account to read and manage users, tenants, and role assignments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External developers use this skill to read and manage Permit.io users, tenants, and role assignments through an OOMOL-connected account. Writes and destructive actions require confirmation of the exact change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time CLI setup can execute unverified remote code, and skill synchronization can install additional persistent agent skills.

Mitigation: Review and approve CLI installation separately; set OO_SKILLS_SYNC_DISABLED=1 unless additional managed skills are intended, and review each proposed change.

Risk: Permit.io write and destructive actions can change or remove account data.

Mitigation: Confirm the exact target, payload, and effect with the user before running these actions.

## Reference(s):

- [Permit.io API Reference](https://docs.permit.io/api/api-reference)
- [Permit.io](https://www.permit.io)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-permit-io)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and responses, plus Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes read actions and proposed state changes; writes and destructive actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
