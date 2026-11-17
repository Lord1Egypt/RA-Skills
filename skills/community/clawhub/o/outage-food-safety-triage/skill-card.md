## Description:

Helps households assess refrigerated and frozen food after a power outage using FDA/USDA-based consumer guidance, item-level decisions, and a printable preparedness checklist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Households use this skill to triage fridge and freezer food after an outage or appliance failure, check individual items and refreezing decisions, and prepare a door-sign checklist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Food-safety recommendations may not reflect actual food temperatures or the needs of high-risk households.

Mitigation: Use a thermometer where possible, favor disposal when conditions are uncertain, and treat the results as household guidance rather than professional medical or commercial food-service advice.

Risk: Generating a door sign writes to a user-selected local file.

Mitigation: Review the output path before running the door-sign command.

## Reference(s):

- [Power-Outage Food Safety — Full Reference](artifact/references/outage-food-rules.md)
- [Outage Food Safety Triage on ClawHub](https://clawhub.ai/voronindenis5/skills/outage-food-safety-triage)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text and Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save a printable Markdown door sign to a chosen local path.]

## Skill Version(s):

1.0.0 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
