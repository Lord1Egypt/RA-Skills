## Description:

OpenBotAuth helps AI agents create a cryptographic identity, register an Ed25519 public key, and generate RFC 9421 signed HTTP request headers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hammadtq](https://clawhub.ai/user/hammadtq)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to set up an OpenBotAuth agent identity, register a public key, and sign HTTP requests or browser traffic so services can verify agent-originated requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional browser signing proxy can broadly sign traffic and intercept HTTPS.

Mitigation: Prefer the core one-request signing flow or a reviewed official proxy; use browser proxy mode only when needed and stop it when finished.

Risk: Installing or trusting the generated proxy CA can expose HTTPS traffic if the CA key is mishandled.

Mitigation: Avoid installing the generated CA into a system-wide trust store, avoid --ignore-https-errors for real browsing, and remove stale CA files when no longer needed.

Risk: Bearer tokens, private keys, or saved agent notes could enable unauthorized registration or signing if exposed.

Mitigation: Use bearer tokens only for registration or key rotation, delete them after registration, keep key files permission-restricted, and remove stale keys and memory notes when no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hammadtq/skills/openbotauth)
- [OpenBotAuth Website](https://openbotauth.org)
- [OpenBotAuth API](https://api.openbotauth.org)
- [OpenBotAuth Spec](https://github.com/OpenBotAuth/openbotauth)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline JSON, JavaScript, and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local key and configuration guidance, signed request headers, and optional signing proxy setup steps.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
