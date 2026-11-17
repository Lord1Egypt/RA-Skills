## Description:

Daily journaling, reflection, and planning skill that reviews yesterday, updates journals, and checks alignment of daily actions to annual goals and a life plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netcetera](https://clawhub.ai/user/netcetera)

### License/Terms of Use:


## Use Case:

Employees and other OpenClaw users use Morning to structure daily planning, reflect on prior journal entries, promote inbox items, and align current tasks with annual goals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist conversation details to journal or inbox files without explicit confirmation after ambiguous triggers.

Mitigation: Review journal content before and after use, and require explicit confirmation before logging sensitive content or editing journal or inbox files when intent is unclear.

Risk: The skill requests Bash access even though its core behavior is journaling, planning, file updates, and Brain task review.

Mitigation: Remove Bash from the allowed tools unless a deployment has a documented shell-based need.

Risk: The skill may read personal or work planning data from journals, inbox files, and configured Brain tasks or projects.

Mitigation: Use it only in workspaces where those files and Brain integrations are intended to be available to the agent.

## Reference(s):

- [README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/netcetera/skills/morning)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown journal updates and concise conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local journal and inbox files and use configured Brain task and project data.]

## Skill Version(s):

0.1.1 (source: server release metadata; package.json states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
