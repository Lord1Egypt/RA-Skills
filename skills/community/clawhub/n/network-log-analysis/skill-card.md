## Description: <br>
Guides device-level network log analysis and forensic timeline construction from raw syslog, console, and SNMP trap data without SIEM platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network engineers and security analysts use this skill to audit syslog collection, correlate events across devices, detect anomalies, and reconstruct incident timelines from raw logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Network logs may contain sensitive infrastructure, user, and source IP data. <br>
Mitigation: Limit analysis to approved devices and time windows, redact sensitive excerpts, and store findings according to incident-handling policy. <br>
Risk: Configuration examples could be mistaken for approved production changes. <br>
Mitigation: Use command examples for read-only inspection unless explicit change approval exists, and validate any production configuration through normal change control. <br>
Risk: Incorrect time synchronization or missing logs can produce misleading timelines. <br>
Mitigation: Verify NTP status, retention coverage, and collection gaps before asserting root cause. <br>


## Reference(s): <br>
- [CLI Reference](references/cli-reference.md) <br>
- [Syslog Patterns Reference](references/syslog-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only analysis guidance; may include commands for inspecting logs and device state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
