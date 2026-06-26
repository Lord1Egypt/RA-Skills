## Description: <br>
Checks SSL/TLS certificate expiry, issuer, protocol, and Subject Alternative Names for one or more domains with custom ports, warning thresholds, and optional JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to check SSL/TLS certificate health for production domains, internal hosts, CI/CD gates, or scheduled monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens network connections to user-specified domains and ports. <br>
Mitigation: Use it only for domains or internal hosts you own or are authorized to audit. <br>


## Reference(s): <br>
- [SSL Certificate Monitor on ClawHub](https://clawhub.ai/Johnnywang2001/jrv-ssl-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text SSL certificate report or structured JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes distinguish OK, warning, expired, and failed checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
