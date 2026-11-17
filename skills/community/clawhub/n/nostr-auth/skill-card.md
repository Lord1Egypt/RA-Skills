## Description:

nostr-auth authenticates to Nostr sign-in challenges (NIP-07 style) by signing kind-22242 AUTH challenge events with a locally derived secp256k1 (BIP-340) key and optionally submitting them to a service callback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dyegolara](https://clawhub.ai/user/dyegolara)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external service operators use this skill when a site or API asks an agent to prove ownership of a Nostr identity by producing or submitting a signed authentication event.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can sign non-authentication events or arbitrary event templates.

Mitigation: Use service-provided sign-in challenges, prefer kind-22242 AUTH events, and inspect the signed event with dry-run before submission.

Risk: Signed events can be sent to arbitrary callback URLs.

Mitigation: Submit only to callback URLs from trusted services and avoid plaintext, local, or private callback endpoints.

Risk: The derived Nostr identity depends on a local master secret.

Mitigation: Keep the master secret local, restrict keyfile permissions, and use NOSTR_AUTH_KEYFILE only for an intended persistent secret path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dyegolara/skills/nostr-auth)
- [Project homepage](https://github.com/dyegolara/nostr-auth-agents)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON event or callback responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Node.js 20.19 or newer; optional NOSTR_AUTH_KEYFILE configures the persistent 32-byte master secret location.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
