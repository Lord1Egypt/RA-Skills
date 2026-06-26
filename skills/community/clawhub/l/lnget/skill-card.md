## Description: <br>
Install and use lnget, a Lightning-native HTTP client with automatic L402 payment support. Use when downloading files behind Lightning paywalls, managing L402 tokens, checking Lightning backend status, or making HTTP requests that may require micropayments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Roasbeef](https://clawhub.ai/user/Roasbeef) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to install and operate lnget for HTTP requests that may require L402 Lightning payments, while managing payment limits, cached tokens, and Lightning backend configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installed client can spend real Lightning funds when auto-paying L402 invoices. <br>
Mitigation: Use --no-pay to inspect costs before payment, set low --max-cost and --max-fee limits, and install only when an agent-accessible Lightning client is intentional. <br>
Risk: The client can use local Lightning node credentials and store cached L402 tokens or LNC sessions. <br>
Mitigation: Use least-privilege credentials instead of an admin.macaroon where possible, protect ~/.lnget, and periodically clear cached tokens and sessions. <br>
Risk: The installer defaults to go install with @latest, so the installed binary can change over time. <br>
Mitigation: Pin a reviewed lnget version with the installer --version option or an explicit Go module version. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Roasbeef/lnget) <br>
- [Roasbeef publisher profile](https://clawhub.ai/user/Roasbeef) <br>
- [lnget upstream repository referenced by the skill](https://github.com/lightninglabs/lnget.git) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, YAML configuration examples, and command output interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct installation of a Go CLI and generation or use of local configuration, cached tokens, LNC sessions, and Lightning wallet credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
