## Description: <br>
Runs daily or on-demand OpenClaw system health checks covering gateway status, disk usage, memory availability, and recent log errors, then records and sends a report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AxelHu](https://clawhub.ai/user/AxelHu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run scheduled or manual OpenClaw environment health checks, capture a Markdown report, and send it to a configured Feishu group or user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Health reports may expose operational details if delivered to the wrong Feishu recipient. <br>
Mitigation: Replace the Feishu placeholder with the intended group or user before installation and review report recipients when changing deployment context. <br>
Risk: Checked logs may contain secrets, private incident details, or sensitive infrastructure information. <br>
Mitigation: Review log sources and redact sensitive content before sending reports outside the operating team. <br>
Risk: Daily cron execution may send automatic reports when only manual checks are desired. <br>
Mitigation: Enable cron only when daily automatic reports are intended; otherwise run the skill manually. <br>


## Reference(s): <br>
- [Health Check detailed specification](references/spec.md) <br>
- [ClawHub skill page](https://clawhub.ai/AxelHu/health-check) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown health report plus Feishu message text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes data/exec-logs/health-check/YYYY-MM-DD.md and sends the report to the configured Feishu recipient; messages over 3800 characters are split into complete parts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
