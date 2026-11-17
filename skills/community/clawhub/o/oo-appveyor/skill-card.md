## Description:

Search and read AppVeyor data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to read AppVeyor projects, environments, build artifacts, users, and roles through their connected account. It requires the OOMOL `oo` CLI and an AppVeyor connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may execute an unverified CLI installer and introduce persistent agent skill changes.

Mitigation: Review setup first, install a verified CLI release, and explicitly control the agent-skill synchronization scope.

Risk: AppVeyor access passes through OOMOL, while remote installer behavior and server-side credential handling are unverified.

Mitigation: Use the narrowest available read permissions and review the service connection and setup steps before use.

## Reference(s):

- [AppVeyor](https://www.appveyor.com)
- [AppVeyor API documentation](https://www.appveyor.com/docs/api/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [AppVeyor skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-appveyor)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON data from AppVeyor actions, with concise explanatory text as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-oriented results for projects, environments, build artifacts, users, and roles]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
