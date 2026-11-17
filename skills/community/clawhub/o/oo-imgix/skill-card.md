## Description:

Manage Imgix sources and purge cached assets through the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Imgix sources, update source settings, and purge cached assets through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup or startup synchronization can introduce changeable code or additional skills without clear user control.

Mitigation: Vet and install a separate CLI release before use, set OO_SKILLS_SYNC_DISABLED before first use, and follow the skill's confirmation requirements for source updates and cache purges.

## Reference(s):

- [Imgix Management API documentation](https://docs.imgix.com/apis/management)
- [Imgix](https://www.imgix.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON request payloads and returned Imgix data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions return data; source updates require confirmation and cache purges require explicit approval.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
