## Description: <br>
Net Detective runs structured network diagnostics, including DNS resolution, traceroute, MTU, speed, and baseline checks, then produces a plain-English diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, support engineers, and technically capable users use this skill to investigate slow or unreliable network connections and turn diagnostic results into actionable next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs active network troubleshooting by running local network utilities and contacting public diagnostic endpoints. <br>
Mitigation: Run it only when active troubleshooting is intended, and review commands or reports before sharing results. <br>
Risk: Diagnostic reports and local history can include network identifiers such as hostname, local IP, gateway, traceroute hops, DNS timings, and speed results. <br>
Mitigation: Review and redact reports before external sharing, and manage stored history according to local privacy requirements. <br>


## Reference(s): <br>
- [Net Detective Diagnostic Guide](references/diagnostic-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown report with supporting JSON diagnostics and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include hostname, local IP, gateway, traceroute hops, DNS timings, speed results, and local baseline comparisons.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
