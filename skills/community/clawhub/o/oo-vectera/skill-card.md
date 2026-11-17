## Description:

Use the Vectera connector to read, create, and update meeting rooms and related settings through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers can list and inspect Vectera meeting rooms, create rooms and access permissions, and update room details or settings through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run unverified CLI software or synchronize skills into other agents.

Mitigation: Review the setup first, install a CLI release you have reviewed, and consider disabling automatic skill synchronization.

Risk: Changes to meeting rooms or access permissions can affect room configuration or sharing.

Mitigation: Confirm the exact payload and effect before running write actions.

## Reference(s):

- [Vectera API documentation](https://www.vectera.com/docs/api/reference/)
- [Vectera](https://go.vectera.com/)
- [oo CLI source repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Shell commands, Text]

**Output Format:** [Markdown instructions, oo CLI shell commands, and JSON action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action payloads should follow the live connector schema; write actions require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
