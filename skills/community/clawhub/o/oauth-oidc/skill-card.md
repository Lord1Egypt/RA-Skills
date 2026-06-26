## Description: <br>
Deep OAuth 2.0 / OpenID Connect workflow for choosing flows by client type, applying PKCE, validating tokens, managing scopes and consent, handling rotation, and avoiding common misconfigurations when implementing SSO, social login, or user-delegated API access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codenova58](https://clawhub.ai/user/codenova58) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and review OAuth 2.0 and OpenID Connect implementations for web, mobile, SPA, and machine-to-machine clients. It helps select the right flow, validate tokens, manage scopes and consent, handle sessions and logout, and harden operational security. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may expose real client secrets, refresh tokens, or private identity-provider configuration while asking for implementation help. <br>
Mitigation: Avoid sharing live credentials or sensitive IdP configuration unless necessary, and redact secrets before using the skill. <br>
Risk: Provider-specific OAuth or OIDC behavior may differ from the general workflow. <br>
Mitigation: Verify final settings, token validation rules, redirect URI behavior, and logout behavior against the selected identity provider's documentation. <br>
Risk: Incorrect flow selection, weak redirect URI controls, or incomplete token validation can create authentication and authorization vulnerabilities. <br>
Mitigation: Use the skill's final checklist to review client classification, PKCE, state and nonce handling, token signature, issuer, audience, expiration validation, refresh handling, and scope minimization. <br>


## Reference(s): <br>
- [Oauth Oidc on ClawHub](https://clawhub.ai/codenova58/oauth-oidc) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Markdown] <br>
**Output Format:** [Markdown guidance with checklists and implementation review steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reference-only guidance; no executable code or system access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
