## Description:

Requires an agent to send a progress update when a task runs longer than 60 seconds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrislawyeryounger-spec](https://clawhub.ai/user/chrislawyeryounger-spec)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to make an agent provide timely, quantified progress updates during long-running searches, batch file work, multi-step writing, external API calls, and other tasks with uncertain runtime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses rigid default wording and Chinese-language examples that may conflict with a user's preferred language or stricter output requirements.

Mitigation: Deploy it only where proactive progress updates are desired, and prefer or adapt a version that respects the user's chosen language and any higher-priority formatting requirements.

Risk: Mandatory progress updates can interrupt otherwise short finalization steps once a task passes the 60-second threshold.

Mitigation: Use the skill for workflows where transparency during long-running tasks is more important than minimizing intermediate messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chrislawyeryounger-spec/skills/long-task-checkin)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown progress update message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Progress updates include elapsed time, current status, quantified progress, estimated remaining time, and a continuation note.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
