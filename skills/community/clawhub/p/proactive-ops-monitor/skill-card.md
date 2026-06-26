## Description: <br>
Proactive operations monitoring for OpenClaw agents that tracks token utilization, memory layer health, alerts, and next-step suggestions to help prevent context overflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neroagent](https://clawhub.ai/user/neroagent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators using OpenClaw agents use this skill to inspect workspace memory health, estimate token utilization, emit local alerts, and generate next-step suggestions before context problems block ongoing work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads OpenClaw memory files that may contain sensitive operational context. <br>
Mitigation: Install only in workspaces where local memory files can be read, and review memory/wal.jsonl and memory/working-buffer.md before use in shared or sensitive environments. <br>
Risk: Alerts, suggestions, and configuration changes are written to local workspace files and may reveal operational context. <br>
Mitigation: Review memory/ops-alerts.jsonl and proactive-ops-config.json, and limit access to generated workspace outputs. <br>
Risk: Token utilization is estimated from local buffer content and may be approximate. <br>
Mitigation: Treat dashboard utilization values as advisory and confirm context pressure before taking disruptive action. <br>


## Reference(s): <br>
- [Proactive Ops Monitor ClawHub page](https://clawhub.ai/neroagent/proactive-ops-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Configuration, Guidance] <br>
**Output Format:** [Plain text dashboard or JSON objects, with local JSON configuration updates for alert settings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads workspace memory files and writes local alert/configuration files when alerts or configuration changes occur.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
