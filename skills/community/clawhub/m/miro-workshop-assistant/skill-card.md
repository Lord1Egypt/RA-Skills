## Description:

Turns workshop photos or notes into editable Miro diagrams with frames, grouped sticky notes, connectors, idempotent updates, rollback, undo, and change commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simoneferrario](https://clawhub.ai/user/simoneferrario)

### License/Terms of Use:


## Use Case:

External users, facilitators, and developers use this skill to convert workshop whiteboard photos or raw notes into clean, editable Miro boards with containers, notes, connectors, and repeatable update or undo behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify or delete Miro board content when apply or undo commands are run.

Mitigation: Use a least-privilege Miro token scoped to the intended board, and require review of the target JSON path, sessionKey, board ID, and command before execution.

Risk: The artifact includes prior _out/.state.json session state that could affect undo behavior.

Mitigation: Remove or reset _out/.state.json before first use in a new environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simoneferrario/skills/miro-workshop-assistant)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with JSON payloads and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Miro-ready JSON with frames, stickies, connectors, sessionKey, runId, and warnings.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
