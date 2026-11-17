## Description:

Nephesh Studio coordinates an 11-role Chinese-language agent team for complex projects using role playbooks, project files, QA gates, and persistent learning notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raydoomed](https://clawhub.ai/user/raydoomed)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route large, multi-step work through a structured agent team with planning, execution, QA review, retrospective, and knowledge-base update stages. It is intended for users who want a persistent Chinese-language operating model for project delivery rather than a single prompt response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to add a persistent identity statement to SOUL.md before use.

Mitigation: Review the requested SOUL.md change manually, keep it scoped to this skill, and remove it if you stop using the workflow.

Risk: The optional daily check uses a recurring main-session cron job.

Mitigation: Enable the cron only when recurring project checks are required, verify the schedule and target session, and disable it when the project workflow is no longer needed.

Risk: Subagent templates require reading a global TOOLS.md file, which can broaden the context each subagent consumes.

Mitigation: Review the global tool rules before deployment and remove or narrow that read requirement if the environment does not need it.

## Reference(s):

- [Nephesh Studio skill overview](artifact/SKILL.md)
- [Standard workflow](artifact/workflow.md)
- [Agency and role model](artifact/AGENCY.md)
- [Subagent scheduling rules](artifact/SUBAGENT-SCHEDULING.md)
- [Daily checklist](artifact/daily-checklist.md)
- [ClawHub skill page](https://clawhub.ai/raydoomed/skills/nephesh-studio)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with structured project files, role instructions, code or shell command snippets when needed, and optional cron configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create project README files, plans, task assignments, QA reports, retrospectives, role learning updates, performance records, and daily check logs.]

## Skill Version(s):

6.0.13 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
