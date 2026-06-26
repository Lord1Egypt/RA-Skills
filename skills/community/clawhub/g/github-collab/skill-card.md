## Description: <br>
Github Collab helps agents coordinate GitHub-oriented project work by creating and tracking tasks, assigning agents, managing configuration, monitoring progress, and generating project reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wljmmx](https://clawhub.ai/user/wljmmx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate multi-agent project work around GitHub repositories, issues, task queues, status reporting, and OpenClaw agent sessions. It is suited to workspaces where automated repository, issue, session, and notification actions are expected and reviewed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act through a user's GitHub login and automate repository or issue actions. <br>
Mitigation: Install and run it only in GitHub accounts and workspaces where automated repository and issue changes are acceptable; review repository names, destinations, and planned actions before execution. <br>
Risk: The skill can control agent sessions and send data through external-message integrations. <br>
Mitigation: Use trusted project inputs, restrict configured channels, and review session targets before allowing automated session or notification actions. <br>
Risk: Task text, session metadata, message contents, and related project data may be written to logs or local databases. <br>
Mitigation: Avoid sensitive inputs unless the workspace logging and database storage are approved; rotate or delete logs and databases according to the workspace retention policy. <br>
Risk: Security evidence reports unsafe command and logging patterns, and VirusTotal telemetry was pending. <br>
Mitigation: Review commands and configuration before running the skill, scan the artifact in the deployment environment, and treat the release as requiring review before broad installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wljmmx/github-collab) <br>
- [README](artifact/README.md) <br>
- [Skill Documentation](artifact/SKILL.md) <br>
- [OpenClaw Migration Guide](artifact/OPENCLAW_MIGRATION.md) <br>
- [Configuration Guide](artifact/CONFIG.md) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [OpenClaw sessions_spawn API](https://docs.openclaw.ai/tasks/sessions_spawn) <br>
- [OpenClaw subagents API](https://docs.openclaw.ai/tasks/subagents) <br>
- [OpenClaw message API](https://docs.openclaw.ai/tasks/message) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, JavaScript code paths, configuration values, task records, and progress-report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local SQLite data, logs, GitHub issues, agent-session state, and external notification messages when the documented commands and integrations are used.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
