## Description:

Search and read BoxHero data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to look up BoxHero inventory items, locations, and team information through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded software without clear user approval, and the installer's exact local changes are unverified.

Mitigation: Review the CLI installation process separately, inspect installer contents, and require approval before execution. Review or disable automatic installation of additional agent skills using the upstream controls.

## Reference(s):

- [BoxHero homepage](https://www.boxhero-app.com)
- [BoxHero API documentation](https://rest.boxhero-app.com/docs/api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON payloads; connector results returned as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports read-only item, location, and team lookups.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
