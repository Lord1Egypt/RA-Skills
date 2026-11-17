## Description:

Structured free-thinking and exploration for agents that can explore a topic, journal the exploration, and manage action items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mculp](https://clawhub.ai/user/mculp)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skill to give an agent structured time for curiosity-driven research, reflection, journaling, and follow-up tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally keeps a persistent local exploration journal and follow-up list, which may capture sensitive topics or callback details.

Mitigation: Install only when persistent local notes are desired, avoid storing private contact details in callback values, and review generated exploration files for sensitive content.

Risk: Broad automatic triggers, heartbeat use, or cron scheduling can create periodic entries without direct user prompting.

Mitigation: Enable scheduled or automatic invocation only when periodic private exploration is intended, and keep cron sessions from sending messages or processing action items.

## Reference(s):

- [Example Exploration Journal Entries](references/examples.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Files, Shell commands, Guidance]

**Output Format:** [Markdown journal entries, markdown action lists, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local exploration notes under explorations/ and may create follow-up action items when a callback is provided.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
