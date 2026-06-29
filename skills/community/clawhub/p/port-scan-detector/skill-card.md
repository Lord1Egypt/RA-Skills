## Description: <br>
Checks fail2ban logs, journalctl authentication failures, and ss connection patterns to detect port scanning, brute-force activity, and related intrusion signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingaiwork](https://clawhub.ai/user/kingaiwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and server operators use this skill to inspect local security state, identify likely port scans or brute-force login attempts, and produce a concise threat brief with recommended actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports may expose sensitive local security data such as usernames, source IPs, failed-login details, and active connections. <br>
Mitigation: Review and redact generated reports before sharing them outside the operational security team. <br>
Risk: Diagnostic commands may require elevated access to local logs or security services. <br>
Mitigation: Run commands with the least privileges needed and only on systems the user is authorized to inspect. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingaiwork/skills/port-scan-detector) <br>
- [Publisher profile](https://clawhub.ai/user/kingaiwork) <br>
- [Publisher homepage](https://kingai.work/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown threat brief with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local authentication, fail2ban, source IP, username, and active connection details.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
