## Description:

Use the oo CLI to search and read Loomio data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to list Loomio polls and retrieve an individual poll by numeric ID or key through a connected Loomio account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unchecked remote code and make broader changes to the agent environment.

Mitigation: Review and verify a trusted oo CLI release before installation, and set OO_SKILLS_SYNC_DISABLED=1 to suppress startup skill synchronization.

Risk: Remote installers and the live connector implementation have not been verified.

Mitigation: Inspect the installer and connector behavior before installing or connecting Loomio.

Risk: Connecting Loomio entrusts its API credential to OOMOL.

Mitigation: Review and accept OOMOL's credential handling before connecting a Loomio account.

## Reference(s):

- [Loomio](https://www.loomio.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON poll data with concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only poll listing and retrieval through the connected Loomio account.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
