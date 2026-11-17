## Description:

Decode, validate, and debug JSON Web Tokens. Inspect headers, payloads, signatures, expiration, claims, and key mismatches. Diagnose common JWT issues in authentication flows without external tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect JWT structure, validate signatures and claims, compare token behavior, and diagnose authentication failures without relying on external JWT websites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validation examples may execute injected Python when token or key values are maliciously crafted.

Mitigation: Before using the validation snippets, rewrite them so tokens, secrets, keys, and audiences are passed through stdin, files, or environment variables read by Python instead of embedded in python3 -c source.

Risk: Tokens or key material supplied by an untrusted party could make the current validation snippets unsafe to run.

Mitigation: Do not run the current validation snippets on untrusted tokens or key material; review and harden the commands before installation or execution.

## Reference(s):

- [JWT Debugger on ClawHub](https://clawhub.ai/charlie-morrison/skills/jwt-debugger)
- [charlie-morrison ClawHub profile](https://clawhub.ai/user/charlie-morrison)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline bash and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local JWT inspection, validation, comparison, generation, and diagnostic guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
