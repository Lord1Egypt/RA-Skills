## Description: <br>
Network diagnostics and analysis toolkit using Python standard library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericlooi504](https://clawhub.ai/user/ericlooi504) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run user-directed network diagnostics such as connectivity checks, DNS lookups, HTTP header inspection, port scans, SSL certificate inspection, WHOIS lookups, and public IP checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can probe remote systems through connectivity checks and port scans. <br>
Mitigation: Use it only on hosts and networks you own or are explicitly authorized to test. <br>
Risk: Public IP lookup contacts external IP-discovery services and may reveal the caller's source IP. <br>
Mitigation: Avoid public IP checks in sensitive environments or route them through approved network controls. <br>
Risk: HTTP and SSL inspection may disable certificate validation, so results can be misleading for trust decisions. <br>
Mitigation: Do not rely on HTTPS or SSL output for security assurance unless certificate validation is fixed or the limitation is clearly accepted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ericlooi504/network-toolbox) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with optional JSON output from some scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Python standard-library scripts produce command output for the requested diagnostic task.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
