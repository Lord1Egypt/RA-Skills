## Description: <br>
OpenClaw Control Center generates a local visual dashboard for OpenClaw system status, AI usage, sessions, scheduled tasks, skills, plugins, and security settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qinxiao607](https://clawhub.ai/user/qinxiao607) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to inspect current system health, token usage, active work, scheduled tasks, plugins, and safety settings in a browser dashboard. The simple mode is for quick operational review, while professional mode exposes fuller tables and technical details for troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dashboard can collect and save sensitive OpenClaw operational details, including session, cron, gateway, plugin, and security-status data. <br>
Mitigation: Use it only for local operations review, confirm the generated file location, and avoid sharing the generated HTML or professional-mode screenshots. <br>
Risk: The skill requests broad execution and control capabilities for data collection and dashboard opening. <br>
Mitigation: Trigger it with explicit requests such as "OpenClaw control center" and review the generated output before relying on actions or exposed details. <br>
Risk: Optional full deployment instructions involve separate software installation and dependencies. <br>
Mitigation: Treat full deployment as a separate installation path requiring repository, dependency, and environment review before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qinxiao607/openclaw-control-center) <br>
- [Publisher profile](https://clawhub.ai/user/qinxiao607) <br>
- [Dashboard rules](references/dashboard-rules.md) <br>
- [Professional mode](references/pro-mode.md) <br>
- [Deployment guide](references/deployment.md) <br>
- [Style memory](references/style-memory.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [HTML dashboard file with concise text summaries, tables, inline code, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates a local control-center.html dashboard and may open it in a browser; professional mode can expose sensitive operational details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
