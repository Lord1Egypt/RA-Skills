## Description: <br>
SecurityTrails lets agents query SecurityTrails domain intelligence through the OOMOL oo CLI connector without handling raw API tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security analysts use this skill to retrieve SecurityTrails domain intelligence, including domain details, associated domains, subdomains, and SSL certificate information, through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The first-time setup path includes one-line shell and PowerShell installer commands for the oo CLI. <br>
Mitigation: Prefer the official install guide, inspect the installer before execution, and confirm the oo CLI source before signing in. <br>
Risk: The skill requires a connected SecurityTrails credential through OOMOL. <br>
Mitigation: Use the OOMOL connector flow rather than exposing raw API tokens, and connect or refresh the SecurityTrails API key only when an auth or scope error requires it. <br>
Risk: Connector failures can reflect account, scope, credential, app, or billing state rather than a failed domain lookup. <br>
Mitigation: Check the returned error class before retrying, and resolve connection, credential, app readiness, or billing issues through the documented OOMOL console links. <br>


## Reference(s): <br>
- [ClawHub SecurityTrails release page](https://clawhub.ai/oomol/oo-securitytrails) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [SecurityTrails connector setup](https://console.oomol.com/app-connections?provider=securitytrails) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only SecurityTrails connector actions return JSON data with execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
