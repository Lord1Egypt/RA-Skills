## Description:

Use this skill to search and read Yuanfenju data through the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Yuanfenju for calendar and almanac data, astrology charts, tarot readings, and related interpretations for cultural research and entertainment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dependency may automatically install or synchronize other agent skills, changing the local skill set.

Mitigation: Review CLI setup and use a verified, version-pinned installation; set OO_SKILLS_SYNC_DISABLED=1 if startup synchronization is unwanted.

Risk: Birth and relationship details may be submitted when requesting charts or compatibility readings.

Mitigation: Submit only details you have permission to share.

Risk: Some Yuanfenju actions may consume call credits or require a paid plan.

Mitigation: Check the applicable account quota and credit costs before using paid actions.

## Reference(s):

- [Yuanfenju](https://yuanfenju.com/)
- [Yuanfenju API documentation](https://doc.yuanfenju.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, SVG chart]

**Output Format:** [Provider data and interpretations returned as JSON, with text or an SVG chart where available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available results depend on the selected Yuanfenju action and account access.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
