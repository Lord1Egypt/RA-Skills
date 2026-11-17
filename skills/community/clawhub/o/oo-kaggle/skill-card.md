## Description:

Search and read Kaggle competitions, datasets, notebooks, and models through an OOMOL-connected Kaggle account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can search and read Kaggle competitions, datasets, notebooks, and models through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions allow unverified remote code execution, and remote installers and hosted execution were not verified.

Mitigation: Review the setup before installing and prefer a verified, pinned CLI installed under your control.

Risk: Setup may affect unrelated agent skills through automatic synchronization.

Mitigation: Disable automatic synchronization of unrelated agent skills.

Risk: OOMOL mediates Kaggle access and may charge for usage.

Mitigation: Understand the OOMOL-mediated access and possible usage charges before use.

## Reference(s):

- [Kaggle API documentation](https://www.kaggle.com/docs/api)
- [Kaggle](https://www.kaggle.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands]

**Output Format:** [Structured JSON results and text, with shell commands for connector actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.4 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
