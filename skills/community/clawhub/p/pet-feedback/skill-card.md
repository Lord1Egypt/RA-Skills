## Description:

pet-feedback runs a desktop pet feedback daemon that displays emotion and interaction-state expressions, speaks generated messages through TTS, and wakes or blanks a touch display from state-file updates and touch events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lizy022868](https://clawhub.ai/user/lizy022868)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and makers use this skill to add a local feedback layer to an OpenClaw desktop pet: a state file drives on-screen expressions, spoken responses, and basic touch-screen wake behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud TTS engines may send spoken message text to an external service.

Mitigation: Use the offline espeak-ng engine for sensitive messages.

Risk: Wake and blank hooks execute locally configured display-control commands.

Mitigation: Configure only simple, trusted display-control commands and do not let untrusted users modify daemon arguments or environment variables.

Risk: The daemon reacts to a watched local state file.

Mitigation: Keep the state file writable only by trusted local processes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lizy022868/skills/pet-feedback)
- [Publisher profile](https://clawhub.ai/user/lizy022868)
- [Skill documentation](artifact/SKILL.md)
- [Demo guide](artifact/examples/demo.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, JSON state examples, and Python CLI behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local display, audio, and PNG preview artifacts when its Python commands are run.]

## Skill Version(s):

1.0.1 (source: server release metadata; skill frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
