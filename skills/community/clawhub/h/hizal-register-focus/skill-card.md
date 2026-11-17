## Description:

Declares the agent's current task and focus tags so related context can be injected into the session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkerscobey](https://clawhub.ai/user/parkerscobey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to register the current work item, session identifier, and focus tags so matching context can be loaded when the task starts, changes, or resumes after a reset.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can register task metadata and a session identifier automatically.

Mitigation: Use it only where the Hizal context source is trusted and avoid registering sensitive task details unless that sharing is acceptable.

Risk: Broad self-triggering can bring external context into the agent session with limited user control.

Mitigation: Review the trigger behavior before installation and re-register focus tags deliberately when the task changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/parkerscobey/skills/hizal-register-focus)

## Skill Output:

**Output Type(s):** [API Calls, Guidance]

**Output Format:** [Markdown guidance with a tool-call example]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Registers a session ID, task description, and focus-tag list; re-registering replaces the previous focus.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
