## Description: <br>
This skill helps users configure, spawn, and manage OpenClaw subagents, including subagent settings, agent identity files, cron heartbeats, tool access, and multi-agent orchestration patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vishnukool](https://clawhub.ai/user/vishnukool) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to set up OpenClaw background agents, configure isolated workspaces, manage spawn depth and concurrency, and coordinate multi-agent work through shared operational files and Mission Control patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides users to create persistent autonomous OpenClaw agents with broad tool, network, memory, and database authority. <br>
Mitigation: Use least-privilege auth profiles, restrictive tool allow and deny lists, sandboxing, timeouts, explicit approval rules for database changes, and regular review of memory and session files. <br>
Risk: Persistent cron jobs, gateway processes, notification loops, and spawned sessions can continue running after setup. <br>
Mitigation: Document and test shutdown procedures for cron jobs, gateway processes, pm2 notification loops, and spawned sessions before deployment. <br>


## Reference(s): <br>
- [OpenClaw SubAgents Creator on ClawHub](https://clawhub.ai/vishnukool/openclaw-subagents) <br>
- [OpenClaw Subagents Documentation](https://docs.openclaw.ai/tools/subagents) <br>
- [OpenClaw Gateway Configuration](https://docs.openclaw.ai/gateway/configuration) <br>
- [OpenClaw Multi-Agent Concepts](https://docs.openclaw.ai/concepts/multi-agent) <br>
- [Mission Control Article](https://x.com/pbteja1998/status/2017662163540971756) <br>
- [Agent Identity and Memory Files](references/agent-files.md) <br>
- [OpenClaw Subagents Configuration Reference](references/config-reference.md) <br>
- [Multi-Agent Architecture Reference](references/multi-agent-architecture.md) <br>
- [sessions_spawn Tool Reference](references/sessions-spawn-tool.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON, JSON5, bash, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include agent workspace file templates, OpenClaw configuration examples, cron commands, and subagent spawn instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
