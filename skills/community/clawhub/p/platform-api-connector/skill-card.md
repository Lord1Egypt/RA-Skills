## Description:

Connect to social media and content platform APIs by navigating developer portals, creating apps, obtaining OAuth tokens, and storing credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brandonwadepackard-cell](https://clawhub.ai/user/brandonwadepackard-cell)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to set up, refresh, and troubleshoot OAuth credentials for Facebook, Instagram, YouTube, Twitter/X, and TikTok platform APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential storage guidance may lead users to store OAuth tokens and app secrets without sufficient protection.

Mitigation: Store tokens and app secrets in a secret manager or encrypted store, redact secrets from logs and URLs, and define token rotation and revocation procedures.

Risk: OAuth setup guidance may omit safety controls for state validation, PKCE, and least-privilege authorization.

Mitigation: Validate OAuth state, use PKCE where applicable, request least-privilege scopes, and review platform-specific OAuth requirements before deployment.

## Reference(s):

- [OAuth Flow Patterns](references/oauth-flows.md)
- [Facebook Graph OAuth Token Exchange](https://graph.facebook.com/v21.0/oauth/access_token)
- [Facebook Graph Accounts Endpoint](https://graph.facebook.com/v21.0/me/accounts)
- [YouTube Upload OAuth Scope](https://www.googleapis.com/auth/youtube.upload)
- [YouTube Readonly OAuth Scope](https://www.googleapis.com/auth/youtube.readonly)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Code, Shell commands]

**Output Format:** [Markdown with JSON, SQL, Python, and HTTP examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces credential setup and OAuth troubleshooting guidance; users should adapt storage and token handling to their security controls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
