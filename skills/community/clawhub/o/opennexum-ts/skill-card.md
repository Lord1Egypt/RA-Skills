## Description:

OpenNexum TS is a TypeScript CLI for contract-driven multi-agent orchestration with ACP, spawning and tracking coding agents through OpenClaw sessions_spawn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayao99315](https://clawhub.ai/user/ayao99315)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to define contract-based coding tasks, spawn generator and evaluator agents, track ACP sessions, and process retry or completion outcomes. It is suited for multi-agent coding workflows where reproducibility, task boundaries, and evaluation records matter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The init workflow can persistently change agent instruction and runtime files in a project.

Mitigation: Review the initialized files before using the workflow in a shared repository, and run initialization in a controlled workspace.

Risk: Generated prompts can turn contract YAML fields into shell commands for coding agents.

Mitigation: Allow only trusted users to author contract YAML, and review contracts before spawning generator or evaluator sessions.

Risk: Telegram notifications can expose task metadata outside the local project environment.

Mitigation: Keep Telegram bot tokens in environment variables, avoid storing them in project config, and enable notifications only when task metadata is appropriate to send to Telegram.

## Reference(s):

- [Contract Schema Reference](references/contract-schema.md)
- [Orchestrator Guide](references/orchestrator-guide.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown instructions with command examples and JSON or YAML payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=20, pnpm, and openclaw; Telegram notifications are optional and controlled through environment variables.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
