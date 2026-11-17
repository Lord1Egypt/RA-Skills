## Description:

Debug OAuth 2.0 and OIDC flows. Trace authorization code, PKCE, client credentials, and implicit flows. Diagnose redirect URI mismatches, scope issues, token exchange failures, and JWKS configuration problems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to trace OAuth 2.0 and OpenID Connect flows, diagnose authorization and token exchange failures, and generate practical remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth credentials, authorization codes, PKCE verifiers, and token responses may be exposed in terminals, logs, shared recordings, CI output, or process arguments.

Mitigation: Use test clients or tenants where possible, verify AUTH_DOMAIN before running commands, disable shell tracing, avoid recorded or shared terminals, and redact access_token, refresh_token, id_token, client_secret, authorization code, and PKCE verifier values before sharing output.

Risk: Diagnostic commands can be run against the wrong authorization server or tenant.

Mitigation: Confirm AUTH_DOMAIN and related client configuration before execution, preferably in a non-production environment.

## Reference(s):

- [Oauth Debugger release page](https://clawhub.ai/charlie-morrison/skills/oauth-debugger)
- [charlie-morrison publisher profile](https://clawhub.ai/user/charlie-morrison)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and diagnostic reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OAuth discovery, token exchange, and audit commands that must be reviewed before running with real credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
