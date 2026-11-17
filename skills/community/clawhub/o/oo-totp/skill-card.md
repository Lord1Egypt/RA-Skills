## Description:

Generates current six-digit TOTP codes for a configured website account through the OOMOL-connected TOTP Authenticator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to retrieve a current TOTP code for a website account connected through OOMOL. Developers can use its CLI guidance to inspect the action schema and request the code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A request for an authentication code can trigger a software installer whose behavior has not been verified.

Mitigation: Review and install the CLI separately before allowing this skill to use it.

Risk: Hosted credential handling is not included in the bundle, so its behavior remains unverified.

Mitigation: Use the connected authentication account and generated codes only if you trust OOMOL.

## Reference(s):

- [RFC 6238: TOTP Algorithm](https://www.rfc-editor.org/rfc/rfc6238)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with shell commands; generated six-digit TOTP code as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated code is time-sensitive.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
