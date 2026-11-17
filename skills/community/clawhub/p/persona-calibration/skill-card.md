## Description:

Create, audit, or update an OpenClaw agent persona through a structured multi-round calibration workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dengyh](https://clawhub.ai/user/dengyh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to calibrate assistant personas through structured interview rounds, then convert the results into proposed updates for SOUL.md, IDENTITY.md, USER.md, and optionally MEMORY.md.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persona or memory changes can affect future agent behavior in ways the user did not intend.

Mitigation: Review proposed edits before applying them, especially changes to MEMORY.md or durable operating rules.

Risk: Calibration may preserve low-value or sensitive conversational details as long-term memory.

Mitigation: Store only durable, high-value preferences and avoid retaining raw questionnaire transcripts or temporary details.

## Reference(s):

- [Persona Dimensions Reference](references/persona-dimensions.md)
- [Persona Calibration Questionnaire Template](references/questionnaire-template.md)
- [File Mapping Example](references/file-mapping-example.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown guidance, interview questions, persona update proposals, and file mapping recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose edits to OpenClaw persona and memory files after user approval.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
