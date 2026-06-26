## Description: <br>
Decode, validate, and debug JSON Web Tokens. Inspect headers, payloads, signatures, expiration, claims, and key mismatches. Diagnose common JWT issues in authentication flows without external tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect JWT headers and payloads, validate signatures, compare claims, and diagnose authentication failures locally without sending tokens to external debugging sites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: JWTs, secrets, and public or private keys used during validation can expose sensitive authentication material if pasted into shared prompts, shell history, logs, or tickets. <br>
Mitigation: Handle tokens and keys locally, prefer stdin or short-lived environment variables, redact diagnostic output before sharing, and avoid persisting token values in logs. <br>
Risk: Decoded JWT headers and payloads are only inspection data and can be mistaken for proof that a token is trustworthy. <br>
Mitigation: Treat decoding as unverified inspection, then validate the signature, expected algorithm, issuer, audience, and time-based claims before relying on the token. <br>
Risk: Generated test JWTs can be confused with production credentials or accepted by services if weak test secrets leak into real configurations. <br>
Mitigation: Use clearly scoped test issuers, audiences, and secrets, keep generated tokens out of production systems, and rotate any test secret accidentally reused in live environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/jwt-debugger) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local diagnostic output and example commands; it does not require external token debugging services.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
