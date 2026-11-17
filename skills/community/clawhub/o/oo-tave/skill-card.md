## Description:

Search and read Táve studio and contact data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with a connected Táve account can retrieve their studio profile and find or read contact records through an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes downloaded software without verification.

Mitigation: Install a verified oo CLI release deliberately and require approval before downloaded installers run.

Risk: Startup synchronization may make undisclosed changes to other agent skills.

Mitigation: Review skill changes and consider setting OO_SKILLS_SYNC_DISABLED=1 to disable startup skill synchronization.

## Reference(s):

- [Táve workspace](https://www.vsco.co/workspace)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Táve ClawHub release](https://clawhub.ai/oomol/skills/oo-tave)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Text]

**Output Format:** [Natural-language responses based on JSON connector results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only studio and contact lookups; the skill checks each action's live schema before running it.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
