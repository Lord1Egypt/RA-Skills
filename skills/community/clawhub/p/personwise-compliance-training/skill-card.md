## Description:

Turn policies into an askable digital-human compliance course.

This skill is ready for commercial/non-commercial use.

## Publisher:

[personwiseai](https://clawhub.ai/user/personwiseai)

### License/Terms of Use:

MIT-0

## Use Case:

Compliance, learning, and operations teams use this skill to turn supplied policies, regulatory summaries, and training materials into a grounded interactive digital-human course. The course supports learner questions and understanding checks without claiming legal compliance, certification, or professional advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The update path can run a CLI or service-supplied command with too little local validation.

Mitigation: Approve an update only when it is clearly the expected PersonWise update from a trusted source, and run only the exact update action returned by the trusted PersonWise workflow.

Risk: Using the skill may authorize PersonWise OAuth, upload selected policy or training documents, consume existing course credits, and install a user-local CLI.

Mitigation: Review those actions before installation or course creation, upload only user-selected materials, and do not approve purchases or broader publication unless explicitly requested.

Risk: A generated compliance course could be mistaken for legal compliance, certification, licensure, or professional advice.

Mitigation: Keep course content grounded in supplied materials, preserve legal obligations exactly, and route individual situations to the compliance owner named in the materials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/personwiseai/skills/personwise-compliance-training)
- [PersonWise Publisher Profile](https://clawhub.ai/user/personwiseai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce PersonWise course URLs, run or project identifiers, source status summaries, and review notes.]

## Skill Version(s):

2.1.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
