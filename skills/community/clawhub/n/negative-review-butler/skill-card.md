## Description:

差评管家 helps Chinese-speaking merchants turn screenshots, pasted text, or exported review files into categorized review-response drafts with severity labels, high-risk complaint prompts, suggested remedies, and final human-review reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenobiazizi](https://clawhub.ai/user/zenobiazizi)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants and store operators use this skill to triage batches of customer reviews, identify high-risk complaints, and draft concise Chinese replies that cite the customer's specific issue before a human posts them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated replies may be inaccurate, too generic, or inappropriate for a public merchant response.

Mitigation: Review and edit every draft before posting it in a platform backend.

Risk: Food safety, injury, legal, counterfeit, or other high-risk complaints can require action beyond reply wording.

Mitigation: Handle high-risk complaints through direct customer contact, internal escalation, evidence retention, or platform processes before publishing a public reply.

Risk: Customer reviews may contain personal information.

Mitigation: Avoid sending unnecessary customer personal information and mask personal details in outputs when they appear.

## Reference(s):

- [差评管家 ClawHub page](https://clawhub.ai/zenobiazizi/skills/negative-review-butler)
- [餐饮 / 本地生活行业模板](references/template-dining.md)
- [电商行业模板](references/template-ecom.md)
- [输出效果示例](examples/sample-output.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown table and concise Chinese prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces draft replies, severity labels, issue categories, remedy suggestions, high-risk handling prompts, unprocessed-item notes, and brief operating tips when repeated issues appear.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
