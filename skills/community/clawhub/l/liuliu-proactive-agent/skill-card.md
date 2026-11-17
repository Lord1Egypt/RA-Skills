## Description:

Helps an AI agent act more proactively by anticipating user needs, reporting progress, raising timely reminders, and identifying potential issues before the user asks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vanish-wu](https://clawhub.ai/user/vanish-wu)

### License/Terms of Use:


## Use Case:

External users and agent builders use this skill to guide an assistant toward timely progress updates, anticipation of follow-up needs, and proactive alerts while avoiding unnecessary interruptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages proactive monitoring of sensitive sources such as calendar and email.

Mitigation: Require explicit user authorization before reading calendar, email, account, or repository data, and keep local guardrails for quiet hours and notification frequency.

Risk: The skill describes proactive changes to persistent project state, including memory files, documents, commits, and temporary files.

Mitigation: Require confirmation before modifying persistent files, committing code, deleting files, or changing memory/documentation state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vanish-wu/skills/liuliu-proactive-agent)
- [Publisher profile](https://clawhub.ai/user/vanish-wu)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance for agent behavior and response patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable payloads or API calls are defined by the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
