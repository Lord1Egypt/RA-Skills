## Description: <br>
Privacy Guard scans local OpenClaw logs for sensitive information leaks and helps users review, confirm, and whitelist detected items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cq2000419](https://clawhub.ai/user/cq2000419) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Privacy Guard to scan local OpenClaw logs for API keys, passwords, identity numbers, account data, financial data, and other sensitive content, then review suspicious detections and tune whitelist rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The released package includes an unredacted alert log with credentials and private conversation content. <br>
Mitigation: Remove alert_log.md before installation or redistribution and rotate any exposed credentials before using the skill. <br>
Risk: Generated reports and suspicious-item state may include previews of sensitive log lines. <br>
Mitigation: Run the tool locally, store reports in a restricted location, and redact or hash sensitive previews before sharing outputs. <br>
Risk: Notification webhooks can disclose detection metadata if configured broadly. <br>
Mitigation: Leave webhook fields empty unless explicitly needed and restrict any configured webhook destination to approved recipients. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cq2000419/privacy-guard-dami) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [scan_report.md](artifact/scan_report.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, local JSON configuration, and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally against OpenClaw log files and persists review state in local JSON files.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata and artifact changelog, released 2026-04-11) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
