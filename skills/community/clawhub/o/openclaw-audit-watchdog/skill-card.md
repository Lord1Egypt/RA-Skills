## Description: <br>
Automated daily security audits for OpenClaw agents with DM delivery and optional email reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davida-ps](https://clawhub.ai/user/davida-ps) <br>

### License/Terms of Use: <br>
AGPL-3.0-or-later <br>


## Use Case: <br>
Developers and operators use this skill to configure recurring OpenClaw security audits, summarize findings, and deliver audit reports to configured DM and optional email recipients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates or updates an unattended recurring OpenClaw audit job. <br>
Mitigation: Verify the schedule, timezone, install directory, and runtime requirements before enabling it; disable or remove the cron job for one-time audits. <br>
Risk: Audit reports may be delivered to external DM or email recipients. <br>
Mitigation: Confirm the DM target, optional email recipient, and sendmail or SMTP relay settings before persistence is enabled. <br>
Risk: Suppression configuration can reduce critical or warning totals after findings have been accepted. <br>
Mitigation: Use suppressions only with both the explicit flag and audit sentinel, and review each suppression reason before relying on the report totals. <br>


## Reference(s): <br>
- [OpenClaw Audit Watchdog on ClawHub](https://clawhub.ai/davida-ps/openclaw-audit-watchdog) <br>
- [Project homepage](https://clawsec.prompt.security) <br>
- [Example suppression configuration](examples/security-audit-config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration values; scheduled audit reports are formatted text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates an unattended OpenClaw cron job and can deliver reports to configured DM and optional email recipients.] <br>

## Skill Version(s): <br>
0.1.6 (source: frontmatter, skill.json, changelog, ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
