## Description: <br>
Security layer protecting agents from prompt injection, social engineering, and malicious content on Moltbook and similar platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[machinesbefree](https://clawhub.ai/user/machinesbefree) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to screen Moltbook or similar social-platform content before an agent processes it, helping identify prompt injection, malicious command requests, social engineering, data exfiltration attempts, and suspicious URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scanned text can be retained locally in an audit log preview. <br>
Mitigation: Avoid scanning secrets unless local retention is acceptable, and periodically clear or disable the log as appropriate. <br>
Risk: Regex-based detection can miss novel attacks or flag benign content. <br>
Mitigation: Use scan results as a best-effort signal and keep human review for suspicious or high-impact content. <br>
Risk: The scanner depends on jq for JSON log generation. <br>
Mitigation: Verify jq is installed before relying on the scanner in an agent workflow. <br>


## Reference(s): <br>
- [Moltbook Firewall README](artifact/README.md) <br>
- [Threat Pattern Configuration](artifact/patterns/threats.json) <br>
- [ClawHub Release Page](https://clawhub.ai/machinesbefree/moltbook-firewall) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text status with JSONL audit log entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scanner exits with different status codes for safe, suspicious, and blocked content.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
