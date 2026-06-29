## Description: <br>
Log Analyst Cn reads recent systemd journal and kernel logs, then explains errors, warnings, and anomalies in a categorized Chinese report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingaiwork](https://clawhub.ai/user/kingaiwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system administrators use this skill to inspect Linux system, kernel, service, and authentication logs, then identify likely security, system, hardware, and service issues. It is intended for troubleshooting, health checks, and post-incident review where a concise Chinese report is useful. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: System and authentication logs can contain sensitive usernames, hostnames, IP addresses, and security events. <br>
Mitigation: Review or redact logs and generated reports before sharing them outside trusted operations channels. <br>
Risk: The skill inspects recent system, kernel, service, and authentication logs, and some checks may require elevated permissions. <br>
Mitigation: Run the documented checks only on systems where the user is authorized to inspect logs. <br>
Risk: The artifact includes promotional and affiliate content in its report template. <br>
Mitigation: Review or remove promotional sections before distributing reports in professional or customer-facing contexts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingaiwork/skills/log-analyst-cn) <br>
- [Kingai.work homepage](https://kingai.work/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report in Chinese with diagnostic shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Categorizes findings by security, system, hardware, and service issues, with prioritized recommendations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
