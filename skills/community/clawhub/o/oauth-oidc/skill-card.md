## Description:

Deep OAuth 2.0 / OpenID Connect workflow for choosing flows by client type, applying PKCE, validating tokens, managing scopes and consent, rotating credentials, and avoiding common misconfigurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codenova58](https://clawhub.ai/user/codenova58)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, debug, and harden OAuth 2.0 and OpenID Connect implementations for SSO, social login, delegated API access, machine-to-machine clients, token validation, session handling, logout, and operational security.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth/OIDC design guidance can be misapplied to the wrong client type, provider, or deployment architecture.

Mitigation: Verify flow selection, PKCE requirements, redirect URI policy, token validation, refresh handling, and logout behavior against the selected identity provider documentation before implementation.

Risk: Incorrect authentication guidance can create security gaps even when the skill itself is non-executable.

Mitigation: Treat outputs as design advice, review them with application security owners, and test provider-specific configuration before production use.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance, staged workflow notes, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provider-specific details should be verified against the selected identity provider documentation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
