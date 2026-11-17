## Description:

Search and read FinerWorks information through the OOMOL-connected account and `oo` CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can query FinerWorks price breakdowns and browse print media, product, and style options through OOMOL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded code, and the installer and hosted connector implementation were not audited.

Mitigation: Review and install a verified CLI release yourself before using the skill.

Risk: Startup synchronization can add other agent skills.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI if you do not want that behavior.

Risk: OOMOL-mediated execution may incur charges.

Mitigation: Check OOMOL billing before running queries.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [FinerWorks](https://finerworks.com/)
- [FinerWorks API documentation](https://v2.api.finerworks.com/Documentation)

## Skill Output:

**Output Type(s):** [API data, JSON, Guidance]

**Output Format:** [JSON connector responses summarized as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only FinerWorks queries; responses include execution metadata.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
