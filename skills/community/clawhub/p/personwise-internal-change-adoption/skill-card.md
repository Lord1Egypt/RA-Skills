## Description:

Turns approved internal change communications into a grounded interactive digital-human course where employees can review the change and ask voice questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[personwiseai](https://clawhub.ai/user/personwiseai)

### License/Terms of Use:

MIT-0

## Use Case:

Change leads, internal communications, HR, and learning teams use this skill to turn approved rollout materials into a private, evidence-grounded adoption course for employees.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The updater path can ask the agent to run PersonWise-supplied update commands with too little local validation.

Mitigation: Review install or update requests before approval and allow only expected PersonWise CLI commands from the governed release path.

Risk: The workflow can install or update a local CLI, use browser OAuth, upload selected internal documents, and consume existing course credits.

Mitigation: Require explicit approval for install or update actions, use browser OAuth without handling secrets, upload only user-named materials, and do not purchase credits automatically.

Risk: Internal change courses can mislead employees if the agent adds unsupported facts about timelines, affected teams, or individual impact.

Mitigation: Keep course content locked to approved communications, flag unresolved ambiguity, and route individual impact questions to the named manager, HR, or change-team channel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/personwiseai/skills/personwise-internal-change-adoption)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-oriented guidance with PersonWise CLI commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create bounded local blueprint or patch JSON files and invoke the PersonWise CLI; the final interactive course is produced by PersonWise.]

## Skill Version(s):

2.1.9 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
