## Description:

Generate model replacement prompts based on user-uploaded model images, replacing the character and scene while preserving clothing and shoes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to generate concise prompts for replacing a person and scene in uploaded model images while preserving the original clothing and shoes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill forces replacement prompts to use a Chinese character even when the user did not request that demographic constraint.

Mitigation: Use this skill only when that replacement behavior is intended, or edit the instructions so demographic traits are optional and user-directed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlark/skills/model-replacement-prompt-generator)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt is constrained to 300 characters or fewer and includes instructions to preserve clothing and shoes while replacing only the character and scene.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
