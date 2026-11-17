## Description:

Turns supplied community materials into a grounded interactive digital-human onboarding course that learners can interrupt with voice questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[personwiseai](https://clawhub.ai/user/personwiseai)

### License/Terms of Use:

MIT-0

## Use Case:

Community builders, membership teams, and agents use this skill to create an onboarding course from supplied community guidelines, welcome materials, and program documentation. It is for new-member orientation that stays grounded in the provided source materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask the agent to run PersonWise CLI or skill update commands that modify local tooling.

Mitigation: Review any install or update command before approval and proceed only when it is clearly a PersonWise CLI or skill update from the expected PersonWise origin.

Risk: Selected documents or images may be uploaded to PersonWise to create the course.

Mitigation: Use only materials the user named or selected for the course and avoid uploading sensitive material that is not needed for onboarding.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/personwiseai/skills/personwise-community-onboarding)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON inputs and shell commands for PersonWise CLI workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance and commands that create or update interactive digital-human courses through the PersonWise CLI; course content remains grounded in user-supplied materials.]

## Skill Version(s):

2.1.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
