## Description:

Decode a JWT locally and print header/payload with sensitive values masked — plus expiry status. Decode-only, zero network. Use when the user asks to look inside or debug a JWT/bearer token quickly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nenadzivotic](https://clawhub.ai/user/nenadzivotic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use it to inspect a user supplied JWT locally, review decoded headers and claims with secret-like values masked, and check expiration. The report does not authenticate the token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decoded claims may be mistaken for authenticated claims because the signature is not verified.

Mitigation: Verify the signature with a trusted JWT implementation before relying on the claims.

Risk: The security review had partial inspection coverage.

Mitigation: Review the source before use and handle the supplied JWT as a credential.

## Reference(s):

- [JWT Inspector Lite on ClawHub](https://clawhub.ai/nenadzivotic/skills/jwt-inspector-lite)

## Skill Output:

**Output Type(s):** [Analysis, JSON]

**Output Format:** [JSON report with decoded header and claims, expiry status, and signature presence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Secret-like values are masked; the JWT signature is not verified.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
