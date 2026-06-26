## Description: <br>
Operate and troubleshoot the OpenClaw CLI across setup, gateway/node lifecycle, channel login, messaging, agent turns, models, plugins, and system health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ramensushi2026](https://clawhub.ai/user/ramensushi2026) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to choose, run, debug, and explain OpenClaw CLI workflows while keeping profile scope, destructive actions, and post-command verification explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenClaw commands can affect real services, messages, credentials, profiles, scheduled jobs, or local state. <br>
Mitigation: Confirm recipients and high-impact commands before execution, use isolated profiles for testing, protect tokens and session output, and review reset, uninstall, force, cron, service, and device-pairing commands before approval. <br>
Risk: Profile or runtime scope mistakes can apply commands to the wrong OpenClaw state. <br>
Mitigation: Choose default, dev, or named profile scope before selecting the command family, keep that scope consistent across the workflow, and verify outcomes with status, health, doctor, or command-specific checks. <br>


## Reference(s): <br>
- [OpenClaw CLI Command Map](references/command-map.md) <br>
- [OpenClaw CLI docs](https://docs.openclaw.ai/cli) <br>
- [ClawHub release page](https://clawhub.ai/ramensushi2026/openclaw-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend JSON output from OpenClaw commands when automation or verification needs structured results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
