## Description: <br>
Scans specified network targets and ports using nmap with options for speed, timeout, host limits, and exclusions, returning detailed JSON results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ApacheUA](https://clawhub.ai/user/ApacheUA) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and security engineers use this skill to run nmap-based scans against network hosts and port ranges they are authorized to assess. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Active network scans may be unauthorized, trigger monitoring, or affect fragile services. <br>
Mitigation: Run scans only against owned or explicitly authorized networks, keep targets and ports narrow, and use host limits and timeouts. <br>
Risk: Broad CIDR or port scans can expand beyond the intended assessment scope. <br>
Mitigation: Use explicit target ranges, exclusions, top-port limits, and host limits before execution. <br>


## Reference(s): <br>
- [Network Scan on ClawHub](https://clawhub.ai/ApacheUA/network-scan) <br>
- [ApacheUA publisher profile](https://clawhub.ai/user/ApacheUA) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Analysis] <br>
**Output Format:** [JSON object containing scan results, the nmap command used, and scan information.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires nmap and network access to the specified authorized targets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
