## Description: <br>
Set up a new OpenClaw agent from scratch. Use when Tom asks to create, add, or onboard a new agent. Covers everything: gathering requirements, Discord bot setup, openclaw.json configuration, Mission Control registration, heartbeat, cron, OneDrive access, and final verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boltth](https://clawhub.ai/user/boltth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw administrators use this skill to onboard a new agent by collecting setup details, coordinating required manual Discord steps, updating configuration, registering Mission Control, scheduling heartbeat checks, optionally linking OneDrive libraries, and verifying the completed setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup workflow handles Discord bot credentials. <br>
Mitigation: Avoid pasting bot tokens into chat; use a secret manager or environment variable when the OpenClaw environment supports it. <br>
Risk: The workflow can grant broad Discord and OneDrive access to a new agent. <br>
Mitigation: Grant only the minimum required Discord permissions and limit OneDrive links to approved libraries or folders. <br>
Risk: The workflow creates persistent registrations and scheduled cron check-ins. <br>
Mitigation: Record new agent registrations and cron entries so administrators can audit or disable them later. <br>


## Reference(s): <br>
- [New Agent Setup checklist](references/checklist.md) <br>
- [Discord Developer Portal](https://discord.com/developers/applications) <br>
- [ClawHub release page](https://clawhub.ai/boltth/new-agent-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces step-by-step operational guidance for an agent setup workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
