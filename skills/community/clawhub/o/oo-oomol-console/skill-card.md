## Description:

Use the OOMOL Console skill to read, create, update, or delete console data through documented actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and team administrators use it to inspect action schemas and manage OOMOL Console teams, Connections, members, billing, and skill package access. Write actions require confirmation, and destructive permission changes require explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup executes downloaded code, and remote installer contents and hosted behavior have not been verified.

Mitigation: Review and approve CLI installation separately, using a chosen release whose source and integrity can be verified.

Risk: Automatic setup may make additional agent-skill changes whose purpose is not explained.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI if startup skill synchronization is unwanted. Confirm the intended team and exact permission changes.

## Reference(s):

- [OOMOL Console](https://console.oomol.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [OOMOL skill access settings](https://console.oomol.com/skills)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON action payloads, JSON responses, and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.6 (source: frontmatter; server release 1.0.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
