## Description:

Decode and inspect JWT tokens from the command line, including header, payload claims, algorithm details, signature presence, and expiration status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to decode JWTs while debugging authentication flows, checking expiration and not-before claims, and inspecting token structure. It should be used for decoding and inspection, not as proof that a token is authentic or authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool can present an unexpired JWT as VALID even though the token signature, issuer trust, and authorization were not verified.

Mitigation: Treat VALID as an expiry-only signal; verify authenticity and authorization with the issuing system before making security decisions.

Risk: Decoded JWT claims may contain sensitive identity, tenant, session, or authorization data.

Mitigation: Use only necessary tokens, avoid unnecessary production tokens, and redact decoded output before sharing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnnywang2001/skills/jwt-toolkit)
- [Publisher profile](https://clawhub.ai/user/johnnywang2001)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands; runtime script output is human-readable text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local command-line decoding only; evidence indicates pure Python standard-library code with no external dependencies.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
