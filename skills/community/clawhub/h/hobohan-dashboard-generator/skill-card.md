## Description: <br>
Generate self-contained HTML dashboards for memory logs, expense charts, and token usage. Run hourly via cron. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hohobohan](https://clawhub.ai/user/hohobohan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to keep local OpenClaw memory, expense, and token usage dashboards generated and available for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill serves private memory logs, ledger data, and usage data through a persistent local HTTP dashboard without clear access controls. <br>
Mitigation: Enable it only in the intended local OpenClaw environment, confirm the dashboard is bound to localhost or otherwise access-controlled, and review the data exposed before use. <br>
Risk: The server watchdog can restart a persistent dashboard process automatically. <br>
Mitigation: Confirm the watchdog and cron behavior are easy to disable before deployment and monitor the server process after enabling it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hohobohan/hobohan-dashboard-generator) <br>
- [Publisher Profile](https://clawhub.ai/user/hohobohan) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON/HTML dashboard artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates local dashboard files and watchdog/cron behavior for a port 8081 dashboard server.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and changelog, released 2026-06-03) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
