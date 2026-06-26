## Description: <br>
Debug OAuth 2.0 and OIDC flows. Trace authorization code, PKCE, client credentials, and implicit flows. Diagnose redirect URI mismatches, scope issues, token exchange failures, and JWKS configuration problems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to trace OAuth 2.0 and OIDC login flows, diagnose common provider errors, and generate command-line checks and remediation guidance for SSO or social login integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth authorization codes, client secrets, PKCE verifiers, refresh tokens, and access tokens can be exposed through shared shells, transcripts, or logs. <br>
Mitigation: Use test clients or short-lived credentials, avoid pasting secrets into shared contexts, and redact command output before sharing logs. <br>
Risk: Generated OAuth curl commands can affect real identity-provider clients or exchange live tokens if run unchanged. <br>
Mitigation: Review endpoints and environment variables before execution and prefer sandbox OAuth clients for debugging. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/oauth-debugger) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and diagnostic report examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OAuth discovery, token exchange, and security-check command snippets; sensitive values should be redacted.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
