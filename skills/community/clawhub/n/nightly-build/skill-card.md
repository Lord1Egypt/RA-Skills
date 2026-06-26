## Description: <br>
Automates nightly maintenance tasks such as skill audits, updates, cleanup, health checks, and a morning report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xRaini](https://clawhub.ai/user/0xRaini) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to schedule recurring local workspace maintenance and receive a summarized report of system, git, disk, memory, cleanup, and skill inventory checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended scheduled maintenance can run local commands in the workspace. <br>
Mitigation: Keep the job report-only or tightly scoped unless updates and cleanup have been explicitly approved. <br>
Risk: Update and cleanup tasks may affect local repositories, logs, or workspace state. <br>
Mitigation: Inspect the configured commands and paths before enabling the cron entry, and keep the cron entry easy to disable. <br>


## Reference(s): <br>
- [Nightly Build on ClawHub](https://clawhub.ai/0xRaini/nightly-build) <br>
- [The Nightly Build](https://www.moltbook.com/post/562faad7-f9cc-49a3-8520-2bdf362606bb) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown report with command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a nightly report file and emits the report text for the agent.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
