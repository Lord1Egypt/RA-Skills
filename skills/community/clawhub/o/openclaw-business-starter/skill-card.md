## Description: <br>
Provides OpenClaw agents with workflows, memory structure, setup automation, and scheduled reviews for autonomous business operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tara-quinn-ai](https://clawhub.ai/user/tara-quinn-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent operators use this skill to bootstrap a business-operations workspace with PARA memory, daily review routines, heartbeat monitoring, and security-oriented operating instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup process can create or overwrite local OpenClaw workspace files and install ongoing scheduled jobs. <br>
Mitigation: Back up ~/.openclaw/workspace, review generated files, and test in a disposable workspace before installing into a live agent environment. <br>
Risk: Broad operating instructions and scheduled jobs may act on private channels or operational state without enough safeguards. <br>
Mitigation: Review or disable cron jobs and require approval for outbound messages, code pushes, financial actions, and memory or instruction changes. <br>
Risk: The artifact contains environment-specific assumptions about names, channels, and authority boundaries. <br>
Mitigation: Replace all Tara/Kalin assumptions and configure authenticated channels, timezone, identity files, and decision limits for the target environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tara-quinn-ai/openclaw-business-starter) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown templates, shell commands, and workspace configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installs workspace files and scheduled review jobs; review generated instructions before enabling routine automation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
