## Description: <br>
Deploy and manage a Guardian watchdog process for OpenClaw Gateway with automated health monitoring, self-repair via `doctor --fix`, git-based workspace rollback, daily snapshots, and optional Discord alerting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LeoYeAI](https://clawhub.ai/user/LeoYeAI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to deploy and manage a watchdog for OpenClaw Gateway instances. It helps monitor uptime, run repair commands, create daily workspace snapshots, and optionally notify a Discord webhook when failures occur. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An unattended watchdog can modify the OpenClaw workspace and may hard-reset local changes. <br>
Mitigation: Commit or back up important work before enabling rollback, verify the guardian script and reset target, and disable or gate `git reset --hard` unless it is explicitly needed. <br>
Risk: Discord webhook alerts may send operational details outside the local environment. <br>
Mitigation: Use Discord alerts only when that data sharing is acceptable, and configure the webhook through controlled environment settings. <br>
Risk: Automated repair commands can run repeatedly without direct operator review. <br>
Mitigation: Review the watchdog configuration before deployment and monitor logs during initial operation. <br>


## Reference(s): <br>
- [Openclaw Guardian on ClawHub](https://clawhub.ai/LeoYeAI/openclaw-guardian-ultra) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes process verification commands, environment variable setup, and operational notes for OpenClaw Guardian.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
