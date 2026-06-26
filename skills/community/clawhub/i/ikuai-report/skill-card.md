## Description: <br>
Generates a static HTML traffic report from iKuai router data collected through ikuai-cli, including overview, network configuration, traffic analysis, security status, and system log views. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veelove](https://clawhub.ai/user/veelove) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network administrators and developers use this skill to generate a browser-readable traffic and configuration report for an iKuai/router environment they administer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated report may contain sensitive router and local network details, including IP addresses, MAC addresses, hostnames, logs, DNS, VPN, and management-exposure information. <br>
Mitigation: Use the skill only for an iKuai/router environment you administer, keep the HTML report private, redact sensitive details before sharing, and delete the report after use. <br>
Risk: The report is written to a predictable temporary path. <br>
Mitigation: Prefer a private output path or move the report immediately to a protected location when using it in shared environments. <br>
Risk: The skill depends on ikuai-cli credentials and router access configured outside the skill. <br>
Mitigation: Configure credentials with ikuai-cli, verify access before running the report, and avoid embedding tokens or router secrets in prompts or shared files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/veelove/ikuai-report) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated artifact is a static HTML report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the report to /tmp/ikuai-report.html after collecting JSON data through ikuai-cli.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
