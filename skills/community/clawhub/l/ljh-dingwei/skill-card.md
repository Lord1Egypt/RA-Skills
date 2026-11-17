## Description:

Generates a new-product positioning one-pager from product materials, including a positioning sentence, value quadrants, competitive differentiation, content translation, and validation checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[handsomeng](https://clawhub.ai/user/handsomeng)

### License/Terms of Use:

MIT-0

## Use Case:

External product, content, and ecommerce teams use this skill to gather product facts, identify positioning gaps, and produce a structured one-page positioning deliverable for a new product.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create persistent local state or archive positioning deliverables that include confidential product information.

Mitigation: Review archive behavior before use, decline archive creation for confidential products, and remove generated local files when retention is not desired.

Risk: The first-run flow includes promotional contact information that some users may not expect.

Mitigation: Review the onboarding text before installing or distributing the skill in managed environments.

## Reference(s):

- [Source skill definition](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/handsomeng/skills/ljh-dingwei)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, files]

**Output Format:** [Markdown one-pager with interactive questions and optional follow-up deliverables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create onboarding state and, when accepted by the user, archive positioning conclusions and deliverables in the working directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
