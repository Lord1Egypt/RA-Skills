## Description: <br>
Control a Pi-hole v6 DNS ad blocker by checking status, viewing statistics, enabling or disabling blocking, and analyzing blocked domains through the Pi-hole API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baanish](https://clawhub.ai/user/baanish) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and home-lab administrators use this skill to let an agent inspect Pi-hole status, summarize DNS blocking activity, and temporarily change blocking state for a configured Pi-hole instance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control Pi-hole blocking, including disabling DNS ad blocking. <br>
Mitigation: Install only when agent control of Pi-hole is acceptable, and review disable or off requests before execution. <br>
Risk: The server security summary reports that a documented timed-disable command can disable blocking indefinitely until the issue is fixed. <br>
Mitigation: Treat disable and off commands carefully, verify Pi-hole status after use, and re-enable blocking manually when needed. <br>
Risk: Credential transport and certificate handling may be weaker when insecure mode is enabled or certificate validation is bypassed. <br>
Mitigation: Use HTTPS with certificate validation, avoid insecure mode except on a trusted local network, and rotate the Pi-hole app password after testing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baanish/pihole) <br>
- [Publisher profile](https://clawhub.ai/user/baanish) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Pi-hole API URL and app password; results depend on the reachable Pi-hole instance and current blocking state.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
