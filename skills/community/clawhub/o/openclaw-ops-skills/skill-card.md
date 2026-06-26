## Description: <br>
Provides production-ready autonomous OpenClaw operations with cost optimization, task autonomy, persistent memory, security hardening, scheduled execution, and progress logging workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Erich1566](https://clawhub.ai/user/Erich1566) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill pack to configure OpenClaw agents for autonomous operational workflows, including model routing, task continuation, persistent memory, scheduled wake-ups, progress reporting, error recovery, and security practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring unattended cron jobs can cause unwanted autonomous actions if enabled without boundaries. <br>
Mitigation: Before enabling cron, restrict allowed directories and actions, require approval for writes, cleanup, dependency installs, deployments, external API actions, and auto-fix commands, then review scheduled jobs regularly. <br>
Risk: Persistent memory and progress logs can retain sensitive project details, raw errors, user inputs, or secrets. <br>
Mitigation: Keep memory and log markdown files out of version control, store no secrets in them, and redact raw errors and inputs before logging. <br>
Risk: Autonomous work loops can consume unexpected time, tokens, or external service budget. <br>
Mitigation: Set explicit time and cost limits and test scheduled workflows with dry runs before allowing unattended execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Erich1566/openclaw-ops-skills) <br>
- [README](artifact/README.md) <br>
- [Quick Start Guide](artifact/QUICKSTART.md) <br>
- [Features](artifact/FEATURES.md) <br>
- [Security Hardening](artifact/skills/security-hardening.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation with inline shell commands, JSON configuration examples, checklists, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reusable agent operating procedures for OpenClaw workspace setup, scheduling, logging, memory, routing, testing, and security practices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
