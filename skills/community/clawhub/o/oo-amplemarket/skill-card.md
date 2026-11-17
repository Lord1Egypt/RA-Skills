## Description:

Uses an OOMOL-connected account to read Amplemarket account, contact, lead-list, and task data, and to complete or skip tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Amplemarket users use the skill to retrieve account, contact, lead-list, and task information, and to complete or skip tasks through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI dependency may persistently change other agent skills without that effect being explained.

Mitigation: Review the CLI installation separately, preferably using a verified release, and set OO_SKILLS_SYNC_DISABLED=1 before invoking oo to disable automatic changes to other agent skills.

Risk: The remote installer and hosted implementation were not verified.

Mitigation: Review the CLI installation separately before use and prefer a verified release.

## Reference(s):

- [Amplemarket API documentation](https://docs.amplemarket.com/api-reference/introduction)
- [Amplemarket](https://www.amplemarket.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-amplemarket)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON connector responses with text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that change Amplemarket state require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
