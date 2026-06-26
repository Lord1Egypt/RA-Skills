## Description: <br>
IP2WHOIS lets agents use an OOMOL-connected IP2WHOIS account to look up WHOIS registration details for domains and list domains hosted on an IP address. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to query IP2WHOIS through OOMOL for domain WHOIS records and IP-hosted domain lists without exposing raw API tokens to the agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-brokered IP2WHOIS API key connection. <br>
Mitigation: Install only when the user is comfortable using OOMOL as the broker and connect only the intended IP2WHOIS account. <br>
Risk: First-time setup includes curl-to-bash and PowerShell installer commands. <br>
Mitigation: Review the official oo CLI installation path before running installer commands, and avoid letting an agent run them blindly. <br>
Risk: Connector calls can fail when authentication, app connection, credentials, scopes, or billing credits are not ready. <br>
Mitigation: Run setup steps only after a matching command failure and resolve the specific OOMOL auth, connection, credential, scope, or billing issue before retrying. <br>


## Reference(s): <br>
- [ClawHub IP2WHOIS skill page](https://clawhub.ai/oomol/oo-ip2whois) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [IP2WHOIS connection settings](https://console.oomol.com/app-connections?provider=ip2whois) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill inspects the live connector schema before execution and uses OOMOL-injected credentials server-side.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
