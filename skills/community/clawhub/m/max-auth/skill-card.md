## Description: <br>
Max Auth provides a local OpenClaw authentication gate with WebAuthn passkeys, a master password, session-scoped authorization, and one-time browser-based secret handoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[felipematos](https://clawhub.ai/user/felipematos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Max Auth to require session-scoped authentication before sensitive OpenClaw actions and to collect credentials through short-lived browser forms instead of chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local server exposes session-token and secret-handling flows that need review before installation. <br>
Mitigation: Review and harden the deployment before use, and keep the server local or behind a tightly restricted reverse proxy. <br>
Risk: Master passwords, session tokens, grant records, and secret-form tokens are sensitive credentials. <br>
Mitigation: Avoid passing the master password on the command line, protect token-bearing records, and do not echo retrieved secrets back into chat. <br>
Risk: Publicly exposed auth or secret endpoints could expand credential exposure. <br>
Mitigation: Do not expose secret endpoints publicly, require HTTPS for browser flows, and restrict returnUrl handling. <br>


## Reference(s): <br>
- [Max Auth - Setup & API Reference](references/api.md) <br>
- [OpenClaw Agent Integration Guide](references/integration.md) <br>
- [Max Auth on ClawHub](https://clawhub.ai/felipematos/max-auth) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local HTTP API routes, session-key patterns, and one-time secret handoff guidance.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
