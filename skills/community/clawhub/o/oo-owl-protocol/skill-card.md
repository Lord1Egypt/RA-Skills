## Description:

Operate Owl Protocol projects and token metadata through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project operators can inspect an Owl Protocol project, read token metadata, and patch a token's metadata through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI may persistently add skills to other agents during startup, an effect not explained in the skill.

Mitigation: Review the CLI setup and set OO_SKILLS_SYNC_DISABLED=1 before invoking oo if you do not want that synchronization.

Risk: OOMOL mediates account access and receives action payloads.

Mitigation: Use a narrowly scoped Owl Protocol connection and confirm each metadata change.

## Reference(s):

- [Owl Protocol](https://owlprotocol.xyz)
- [Owl Protocol API quickstart](https://docs.owlprotocol.xyz/quickstart)
- [oo CLI command controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON inputs and project or token data returned by Owl Protocol]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads return service data; token metadata changes require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
