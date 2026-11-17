## Description:

Use when using Feishu/Lark Calendar through lark-cli or feishu-cli for agendas, scheduling, freebusy checks, meeting rooms, RSVP, review blocks, release windows, and follow-up planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afengzi](https://clawhub.ai/user/afengzi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and employees use this skill to work with Lark or Feishu calendars from lark-cli, including agenda review, scheduling, free/busy checks, meeting room booking, release windows, and follow-up planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad agenda alias could route ambiguous planning requests to calendar reads or event creation.

Mitigation: Review prompts involving generic agenda requests before allowing calendar reads or event creation.

Risk: Ambiguous participants, rooms, or times could result in an incorrect calendar event.

Mitigation: Require clarification before creating or updating meetings when participants, rooms, or times are unclear.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may use JSON input files and lark-cli calendar subcommands.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
