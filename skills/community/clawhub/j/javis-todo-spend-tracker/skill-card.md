## Description:

Keep the user's to-do list and spending ledger from what they say out loud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuel-wei](https://clawhub.ai/user/samuel-wei)

### License/Terms of Use:

MIT-0

## Use Case:

HiJavis users can capture their own to-dos and purchases from recordings or keyboard input, confirm or discard each pending card, and ask chat for their open tasks or monthly spending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan inspected only 7 of 18 components fully and notes an undeclared tool scope, leaving uncertainty about the skill's behavior and access.

Mitigation: Review the skill's requested permissions and behavior before enabling it; confirm or discard each pending record in HiJavis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samuel-wei/skills/javis-todo-spend-tracker)
- [HiJavis iPhone app](https://apps.apple.com/us/app/hijavis/id6745134765)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured to-do and expense records, with concise chat summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [English and Chinese; records remain pending until the user confirms them.]

## Skill Version(s):

0.1.2 (source: package.json, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
