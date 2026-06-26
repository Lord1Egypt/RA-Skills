## Description: <br>
Read and write data across TCP or UDP connections for network debugging, port scanning, and data transfer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and network operators use this skill for permitted network diagnostics, port testing, and simple data transfer with nc-style network connections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dual-use network scanning, listening, or data-transfer behavior can be misused on networks without authorization. <br>
Mitigation: Use only on systems and networks owned by the user or covered by explicit testing permission, and avoid broad port ranges. <br>
Risk: Ad hoc network connections can expose sensitive data. <br>
Mitigation: Do not pass secrets or sensitive payloads through the tool, and bind listeners narrowly when listening is required. <br>
Risk: The release discloses network diagnostic capabilities without clear safety boundaries. <br>
Mitigation: Document authorized-use expectations before deployment and review proposed commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/nc-tool) <br>
- [Publisher profile](https://clawhub.ai/user/dinghaibin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No credential requirements detected; command use should be limited to authorized hosts and ports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
