## Description: <br>
Daily cost reporting and session hygiene for OpenClaw deployments, including per-session API spend reports, 7-day trends, and stale session cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zylcold](https://clawhub.ai/user/zylcold) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor daily OpenClaw API spend, post operational cost summaries to Discord, and clear stale session files on a scheduled basis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run unattended and post operational metadata to Discord. <br>
Mitigation: Run in dry-run mode first, protect the Discord webhook as a secret, and confirm the report contents are acceptable before enabling scheduled posting. <br>
Risk: The stale-session cleanup can permanently empty session files using weak safety checks. <br>
Mitigation: Verify configured session paths point only to OpenClaw session files, add backups or quarantine behavior, and confirm thresholds before enabling cron. <br>


## Reference(s): <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [ClawHub skill page](https://clawhub.ai/zylcold/openclaw-daily-ops) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON files] <br>
**Output Format:** [Markdown Discord report, shell command guidance, and JSON state logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May post operational summaries to Discord and write local cost and session reset logs when run outside dry-run mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
