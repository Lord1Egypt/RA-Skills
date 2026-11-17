## Description:

Guides membership analytics for a simulated chain restaurant, including metric definitions, segmentation, warehouse SQL, and dashboard designs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maojiebc](https://clawhub.ai/user/maojiebc)

### License/Terms of Use:

MIT-0

## Use Case:

Membership operations teams and data analysts use this Chinese-first reference to define metrics, plan audience segments and outreach measurement, and adapt SQL, schemas, and dashboards. Its example data is simulated, not real customer data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Adapting membership or employee schemas to real data may expose personal identifiers.

Mitigation: Use scoped read-only credentials, mask or tokenize identifiers, and keep row-level records out of prompts and group chats.

Risk: Unvalidated example SQL or metric definitions may produce misleading operational decisions.

Mitigation: Review business rules and test SQL against the intended data and platform before production use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/maojiebc/skills/majia-huiyuan)
- [Author-listed project homepage](https://github.com/maojiebc/majia-huiyuan)
- [Membership metrics reference cards](artifact/口径卡片/README.md)
- [Formula library](artifact/公式库/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with SQL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples use simulated data; SQL and business rules require validation before production use.]

## Skill Version(s):

1.5.0 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
