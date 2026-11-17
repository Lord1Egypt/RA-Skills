## Description:

Search and read Statsig project data through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use the skill to retrieve Statsig project details, feature gates, dynamic configs, and segments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can trigger remote code execution, and the live installers and hosted connector were not verified.

Mitigation: Review setup before installing, use a reviewed CLI release, and require approval before installing software or additional agent skills.

Risk: Connecting Statsig entrusts its API key and requested data to OOMOL.

Mitigation: Use narrowly scoped credentials.

## Reference(s):

- [Statsig Console API documentation](https://docs.statsig.com/api/content/console-api/introduction)
- [Statsig](https://www.statsig.com/)
- [Statsig skill on ClawHub](https://clawhub.ai/oomol/skills/oo-statsig)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Natural-language responses and retrieved Statsig data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.4 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
