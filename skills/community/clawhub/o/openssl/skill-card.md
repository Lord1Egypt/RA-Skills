## Description:

Generate secure random strings, passwords, and cryptographic tokens using OpenSSL. Use when creating passwords, API keys, secrets, or any secure random data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asleep123](https://clawhub.ai/user/asleep123)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to choose OpenSSL commands for generating passwords, API keys, session tokens, and other secure random values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included 8-digit PIN command may be weak for authentication or recovery flows.

Mitigation: Avoid relying on it for those flows unless it is replaced with a fixed-width, unbiased generator and paired with rate limits and expiration.

Risk: Generated secrets can be exposed if copied into logs, command history, or shared chat transcripts.

Mitigation: Review generated values locally and avoid storing or transmitting secrets outside the intended secret-management workflow.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are intended for local review and execution; no files, network calls, or API calls are produced by the skill itself.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
