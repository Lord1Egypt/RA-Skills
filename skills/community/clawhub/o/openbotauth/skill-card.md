## Description: <br>
Get a cryptographic identity for an AI agent, generate Ed25519 keys, sign HTTP requests, and prove agent identity across supported runtimes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hammadtq](https://clawhub.ai/user/hammadtq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to register an agent identity, manage local signing keys, and produce RFC 9421 signed HTTP headers for browser or API sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional browser mode can route HTTPS traffic through a local interception proxy and requires trusting or bypassing TLS protections. <br>
Mitigation: Prefer the core signing flow when possible, avoid routing unrelated browsing through the proxy, and trust the generated CA only when the user understands the interception behavior. <br>
Risk: The skill stores a local private key and briefly stores a bearer token for registration. <br>
Mitigation: Keep token scope minimal, store credentials with restrictive permissions, delete the bearer token after registration, and never attach bearer tokens to browser sessions. <br>


## Reference(s): <br>
- [OpenBotAuth skill page](https://clawhub.ai/hammadtq/openbotauth) <br>
- [OpenBotAuth website](https://openbotauth.org) <br>
- [OpenBotAuth API](https://api.openbotauth.org) <br>
- [OpenBotAuth spec](https://github.com/OpenBotAuth/openbotauth) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with shell commands, JavaScript snippets, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup steps for key generation, registration, request signing, and optional browser proxy configuration.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
