## Description:

LaunchDarkly (launchdarkly.com). Use this skill for ANY LaunchDarkly request — reading, creating, updating, and deleting data. Whenever a task involves LaunchDarkly, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the skill through an OOMOL-connected account to inspect and manage LaunchDarkly projects, environments, feature flags, segments, teams, members, contexts, and tokens. It guides users to inspect each action's schema and obtain approval before changes or deletions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback can download and run CLI software without a separate verification step.

Mitigation: Review and approve CLI installation separately, verify the installation source, and inspect bundled-skill changes before running it.

Risk: OOMOL mediates account access, while its hosted connector and remote installer implementations were not verified in this review.

Mitigation: Use narrowly scoped LaunchDarkly credentials and retain the skill's required approvals for write and destructive actions.

## Reference(s):

- [LaunchDarkly API documentation](https://launchdarkly.com/docs/api)
- [LaunchDarkly](https://launchdarkly.com)
- [oo CLI repository (referenced by the skill)](https://github.com/oomol-lab/oo-cli)
- [LaunchDarkly skill release page](https://clawhub.ai/oomol/skills/oo-launch-darkly)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON request payloads; connector responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
