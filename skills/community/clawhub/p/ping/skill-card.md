## Description: <br>
Monitor network connectivity and diagnose latency issues using ping and traceroute. Use when troubleshooting network problems or checking host availability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, network operators, and support engineers use this skill to check host availability, trace routes, monitor connectivity over time, sweep authorized subnets, and analyze latency history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can scan user-selected subnets. <br>
Mitigation: Use sweep only on networks you own or are authorized to test. <br>
Risk: Hostnames, IP addresses, route previews, and sweep results are saved locally under ~/.ping. <br>
Mitigation: Delete or protect ~/.ping when it contains sensitive network diagnostic data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/ping) <br>
- [Publisher profile](https://clawhub.ai/user/xueyetianya) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, CSV] <br>
**Output Format:** [Markdown guidance with inline bash commands, terminal diagnostic text, and local JSONL or CSV records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores ping history and configuration under ~/.ping when commands are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
