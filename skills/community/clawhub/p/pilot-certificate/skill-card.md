## Description:

Provides shell-command workflows for issuing, sending, and checking Pilot Protocol capability certificate JSON files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators working with Pilot Protocol agents use this skill to draft certificate issuance, transfer, expiry-check, and capability-check workflows for delegated authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake unsigned JSON files and timestamp checks for cryptographic certificate signing and verification.

Mitigation: Do not rely on the workflow for real authorization until actual Ed25519 signing and signature verification are added and independently reviewed.

Risk: The documented examples grant admin capability by default.

Mitigation: Require least-privilege capability lists, explicit approval for administrative grants, and review before sending or accepting certificates.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash code blocks and JSON certificate examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local certificate JSON examples and command snippets for pilotctl, jq, openssl, and shell workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
