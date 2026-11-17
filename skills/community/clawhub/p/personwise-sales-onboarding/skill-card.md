## Description:

Turns supplied sales playbooks and onboarding plans into grounded, interactive digital-human courses for new sales rep ramp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[personwiseai](https://clawhub.ai/user/personwiseai)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and sales enablement teams use this skill to create a new-sales-rep onboarding course from approved sales source materials. Learners receive an interactive digital-human course with voice-interruptible questions, conceptual visuals, and optional assessments grounded in the supplied playbook and onboarding plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation or update approval may allow PersonWise-controlled update commands to modify the local CLI or installed skill.

Mitigation: Review the exact update command and publisher-controlled update channel before approving installation or updates; approve only when the PersonWise publisher and command are expected.

Risk: Generated onboarding courses may contain unsupported sales claims if the supplied materials are incomplete, outdated, or broader than the approved commercial scope.

Mitigation: Review generated outlines and scripts against approved sales materials, and route pricing, contract, quota, competitive, and individual performance questions to the named business owner or sales manager.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/personwiseai/skills/personwise-sales-onboarding)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON inputs, shell commands, and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an interactive digital-human course through PersonWise from user-approved source materials; normal output includes course status, source-processing status, and the appropriate private or link-access URL.]

## Skill Version(s):

2.1.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
