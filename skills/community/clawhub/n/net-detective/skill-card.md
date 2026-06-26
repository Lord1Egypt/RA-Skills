## Description: <br>
Run structured network diagnostics that test DNS, traceroute, MTU, speed, and historical baselines, then produce a plain-English diagnosis with actionable findings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, support engineers, and network operators use Net Detective to diagnose slow or unreliable network connections, compare results against baselines, and produce actionable reports for end users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Active diagnostics send traffic to public DNS providers, ping/traceroute targets, and optional Cloudflare speed-test endpoints. <br>
Mitigation: Run the skill only in environments where active network probing and external test traffic are acceptable. <br>
Risk: Generated JSON and Markdown reports can expose local network details such as hostnames, local IPs, gateway information, and traceroute hops. <br>
Mitigation: Review and redact diagnostic outputs before sharing them outside the trusted troubleshooting context. <br>


## Reference(s): <br>
- [Net Detective Diagnostic Guide](references/diagnostic-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/newageinvestments25-byte/net-detective) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [JSON diagnostic data plus Markdown/plain-English reports and shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional speed tests generate active network traffic; history comparison uses locally recorded baseline data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
