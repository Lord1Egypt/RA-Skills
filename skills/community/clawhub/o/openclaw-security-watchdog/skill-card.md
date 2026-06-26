## Description: <br>
OpenClaw Security Watchdog runs an OpenClaw system security audit, guides optional scheduled scans, and summarizes report results for users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ylardablez](https://clawhub.ai/user/ylardablez) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to run local security audits, configure optional recurring audits, and get readable summaries of scan reports. Users can opt into a manual cloud-assisted mode for threat-intelligence checks after explicit consent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud reporting mode sends device identifiers, a persistent agent_id, installed Skill inventory, and audit summaries to the disclosed Changeway service. <br>
Mitigation: Use local mode for privacy-sensitive environments; run --push only after explicit one-time user confirmation. <br>
Risk: Adding --push to scheduled audits would repeatedly upload sensitive device and inventory data. <br>
Mitigation: Keep scheduled OpenClaw cron jobs in local mode and do not include --push in cron messages. <br>
Risk: The audit can inspect local logs, process metadata, workspace files, and installed Skill inventory. <br>
Mitigation: Install only when local security auditing is intended, keep generated reports protected, and share summaries instead of raw audit output. <br>


## Reference(s): <br>
- [Cron setup guide](references/cron-setup.md) <br>
- [ClawHub release page](https://clawhub.ai/ylardablez/openclaw-security-watchdog) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and concise text with inline shell commands and local report file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summarizes PASS/FAIL/SKIP counts, optional score in push mode, saved report path, and requested report interpretation; full script output is intentionally suppressed.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
