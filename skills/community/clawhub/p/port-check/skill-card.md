## Description: <br>
Check if services are responding on given host:port pairs. Supports TCP and HTTP checks with configurable timeout. Use for service monitoring, health checks, and network debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogue-agent1](https://clawhub.ai/user/rogue-agent1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to check whether TCP or HTTP services are reachable on specified host:port targets for service monitoring, health checks, and network debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs nc and curl against user-specified network targets, which can probe private or third-party systems from the execution environment. <br>
Mitigation: Use it only against hosts and ports you own, administer, or have explicit permission to check. <br>


## Reference(s): <br>
- [Port Check ClawHub Release](https://clawhub.ai/rogue-agent1/port-check) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and terminal-style status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires nc and curl; exits 0 when all targets are up and 1 when one or more targets are down.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
