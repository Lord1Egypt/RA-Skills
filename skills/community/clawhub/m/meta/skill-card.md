## Description:

Coordinates complex tasks by splitting work across background sub-agents and summarizing important progress for the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xaiohuangningde](https://clawhub.ai/user/xaiohuangningde)

### License/Terms of Use:


## Use Case:

Agent users use this skill to coordinate complex work by decomposing tasks, delegating subtasks to search, analysis, execution, or monitoring sub-agents, and receiving summarized progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delegate broad background work, including execution, automation, monitoring, and web crawling, without explicit scope limits in the artifact.

Mitigation: Require explicit user confirmation and a defined scope before starting web crawling, script execution, automation, monitoring, file changes, credential use, or long-running background tasks.

Risk: Progress reporting is intentionally sparse, which can reduce visibility into background sub-agent actions.

Mitigation: Ask sub-agents to report material actions, decisions, failures, and completion status before relying on their results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xaiohuangningde/skills/meta)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown or plain text coordination updates with possible shell command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May delegate background work and summarize only important progress.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
