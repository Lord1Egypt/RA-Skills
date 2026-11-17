## Description:

Routes tasks between GLM-4.7-FlashX for simple queries and GLM-5 for coding, analysis, reasoning, and complex tasks, switching automatically as needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raufimusaddiq](https://clawhub.ai/user/raufimusaddiq)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to route lightweight requests to GLM-4.7 and heavier coding, analysis, research, or planning work to GLM-5. It also gives spawned GLM-5 sessions output and persistence rules for code, reports, and selected memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spawned sub-agents may write long-term memory, task reports, or project files without clear user approval.

Mitigation: Review the skill before installing and consider requiring explicit approval before writing persistent memory or reports.

## Reference(s):

- [GLM Autoroute on ClawHub](https://clawhub.ai/raufimusaddiq/skills/glm-autoroute)
- [Publisher profile](https://clawhub.ai/user/raufimusaddiq)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with task-routing instructions and optional file outputs from spawned coding or research work]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create task reports, code files, and MEMORY.md entries when GLM-5 sessions are spawned.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
