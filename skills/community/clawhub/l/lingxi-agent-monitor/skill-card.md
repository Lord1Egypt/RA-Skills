## Description: <br>
Monitors OpenClaw Agent health, uptime, task status, and system metrics with alerts, memory management, session cleanup, and proactive self-healing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nima54851](https://clawhub.ai/user/nima54851) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check OpenClaw Agent uptime, sessions, memory, task queues, tool connectivity, latency, and error rates, then produce health reports, alerts, and self-healing guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic session cleanup and history pruning may remove session data without a clear retention policy. <br>
Mitigation: Define retention limits before use, archive important session summaries, and require confirmation before deleting or pruning session history. <br>
Risk: Self-healing actions such as cache clearing, MCP restarts, retries, and provider switching can affect stable tool behavior. <br>
Mitigation: Enable self-healing conservatively, log each action, and require approval before changing providers or clearing state in production workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nima54851/skills/lingxi-agent-monitor) <br>
- [Publisher Profile](https://clawhub.ai/user/nima54851) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown health reports, JSON configuration examples, cron entries, shell commands, and endpoint descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include alert thresholds, health-check schedules, self-healing actions, and dashboard or metrics endpoint descriptions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
