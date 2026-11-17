## Description:

Predict gender probabilities for one or more names with Genderize, optionally localized by country.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to get name-based gender probability estimates from Genderize, for a single name or batches of up to 10 names, optionally localized to a country.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified code and add extra agent skills without clear user control.

Mitigation: Review and install a verified CLI release, inspect any additional skill changes, and use OO_SKILLS_SYNC_DISABLED to disable startup skill synchronization.

## Reference(s):

- [Genderize API documentation](https://genderize.io/documentation)
- [Genderize](https://genderize.io/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Gender prediction results in JSON, with a concise text summary when useful.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-name and batch predictions of up to 10 names, optionally localized by country.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
