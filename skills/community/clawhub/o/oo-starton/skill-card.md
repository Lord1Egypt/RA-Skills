## Description:

Use this skill to read, create, update, and delete Starton data through a connected Starton account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use the skill to manage Starton IPFS pins through a connected account, including listing and reading pins and creating or deleting pins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup executes remote code that is outside the inspected skill package.

Mitigation: Review the installer and use a separately verified, pinned installation before setup.

Risk: Startup may synchronize additional agent skills, changing the local skill set.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 before invoking oo to prevent startup skill synchronization.

Risk: Starton access is mediated through OOMOL and the connected account.

Mitigation: Connect only the intended Starton account and retain confirmation for every write or delete action.

## Reference(s):

- [Starton](https://starton.com)
- [Starton API documentation](https://github.com/starton-io/starton-openapi)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown with shell command examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use the live connector schema; state-changing actions require confirmation.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
