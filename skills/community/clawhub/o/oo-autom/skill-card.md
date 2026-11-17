## Description:

Use Autom to search and read Autom data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search Autom's supported Google countries, languages, and locations, and inspect account usage through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes unverified remote code.

Mitigation: Use a verified oo CLI release, review the installation, and explicitly approve local changes.

Risk: The dependency may make persistent changes to other agents' skills.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 before invoking oo when only Autom access is needed.

## Reference(s):

- [Autom release on ClawHub](https://clawhub.ai/oomol/skills/oo-autom)
- [Autom API documentation](https://docs.autom.dev/usage)
- [Autom homepage](https://www.autom.dev)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON payloads and responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Autom action inputs and outputs depend on the action schema.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
