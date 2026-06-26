## Description: <br>
Analyze IP addresses with subnet calculation and CIDR notation. Use when planning network addressing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and network planners use this skill to inspect IP addresses, validate IPv4-style input, review CIDR mask bits, and check local or public network identity while planning addressing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local command can expose interface and address details from the host running the agent. <br>
Mitigation: Run the local command only when local network details are needed and acceptable to share in the agent session. <br>
Risk: The public command contacts checkip.amazonaws.com and reveals a public IP lookup to that service. <br>
Mitigation: Run the public command only when external IP discovery is needed and outbound contact to that endpoint is acceptable. <br>


## Reference(s): <br>
- [Ip Advisor on ClawHub](https://clawhub.ai/ckchzh/ip-advisor) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [Public IP lookup endpoint](https://checkip.amazonaws.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command output and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands accept IP addresses, CIDR notation, and optional start/end ranges; no credential parameters are declared.] <br>

## Skill Version(s): <br>
3.0.0 (source: server evidence release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
