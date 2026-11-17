## Description:

Manage Brevo account, contact, and contact-list data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can retrieve Brevo account and contact information, organize contacts into lists, and create, update, or remove contact data through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified remote code and make broader changes to the agent environment.

Mitigation: Review and approve CLI installation separately using an inspected, verified release; consider OO_SKILLS_SYNC_DISABLED to control automatic skill synchronization.

Risk: The OOMOL-connected service handles the Brevo connection and contact data.

Mitigation: Assess whether OOMOL should handle your Brevo connection and contact data.

Risk: Write and destructive actions can change or remove Brevo data.

Mitigation: Confirm the exact payload and effect before write actions, and confirm the target before destructive actions.

## Reference(s):

- [Brevo API documentation](https://developers.brevo.com/)
- [oo CLI command documentation](https://github.com/oomol-lab/oo-cli)
- [CLI controls for automatic skill synchronization](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and structured JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions return Brevo data; write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
