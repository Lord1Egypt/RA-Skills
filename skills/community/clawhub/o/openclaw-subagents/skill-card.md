## Description:

This skill guides agents through configuring, spawning, and managing OpenClaw subagents, including OpenClaw configuration, agent identity files, cron heartbeats, tool access depth rules, and multi-agent orchestration patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vishnukool](https://clawhub.ai/user/vishnukool)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to set up OpenClaw subagents for background work, nested orchestration, or multi-agent squads with isolated workspaces and Mission Control coordination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent autonomous agents and heartbeat cron jobs can continue acting after initial setup.

Mitigation: Configure clear controls to list, audit, pause, and remove heartbeat cron jobs, and use timeouts and concurrency limits for subagent runs.

Risk: Database-driven work execution and command-line tooling can trigger consequential actions without adequate oversight.

Mitigation: Use strict tool allowlists, pin the Convex CLI, and require approval before consequential actions are executed.

Risk: Shared workspaces or authentication profiles can blur agent boundaries.

Mitigation: Keep each agent workspace and auth profile isolated, and verify agent routing before enabling subagent spawning.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vishnukool/skills/openclaw-subagents)
- [Configuration reference](references/config-reference.md)
- [sessions_spawn tool reference](references/sessions-spawn-tool.md)
- [Agent identity and memory files](references/agent-files.md)
- [Multi-agent architecture reference](references/multi-agent-architecture.md)
- [OpenClaw subagents documentation](https://docs.openclaw.ai/tools/subagents)
- [OpenClaw gateway configuration documentation](https://docs.openclaw.ai/gateway/configuration)
- [OpenClaw multi-agent documentation](https://docs.openclaw.ai/concepts/multi-agent)
- [Mission Control source article](https://x.com/pbteja1998/status/2017662163540971756)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, shell, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose OpenClaw configuration changes, cron commands, agent workspace files, and subagent spawn instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
