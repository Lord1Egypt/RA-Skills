## Description: <br>
IP2Location.io helps agents retrieve IP geolocation, network metadata, hosted domains, and domain WHOIS data through the OOMOL oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when an agent needs read-only IP2Location.io lookups for IP geolocation, hosted-domain discovery, or domain WHOIS registration details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected IP2Location.io API key through OOMOL. <br>
Mitigation: Confirm the account connection and credential-sharing posture before installation or use. <br>
Risk: Connector payloads can drift if IP2Location.io action schemas change. <br>
Mitigation: Fetch the live connector schema before each action and build payloads from that schema. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-ip2location) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [IP2Location.io homepage](https://www.ip2location.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before execution so payloads match the current IP2Location.io action contract.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
