## Description:

Generates a KokoChat connection code by starting a KokoChat relay tunnel and using OpenClaw's official device-pair flow to mint a short-lived gateway-signed bootstrap token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[komako-workshop](https://clawhub.ai/user/komako-workshop)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to pair a KokoChat mobile client with an OpenClaw Gateway, generate the connection code, and verify or revoke the paired device according to owner consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates a persistent relay path from a KokoChat relay endpoint to the local OpenClaw Gateway.

Mitigation: Install only when the relay endpoint is trusted, confirm how to stop the connector and remove relay credentials, and revoke the paired device when access is no longer needed.

Risk: The final device token scopes are controlled by the OpenClaw device-pair flow and may be broader than the owner intends.

Mitigation: After pairing, inspect the device with openclaw devices list and revoke or remove it if the identity or scopes do not match the owner's consent.

## Reference(s):

- [Kokochat Pairing on ClawHub](https://clawhub.ai/komako-workshop/skills/kokochat-pairing)
- [komako-workshop Publisher Profile](https://clawhub.ai/user/komako-workshop)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with a fenced code block containing the raw KokoChat connection code, plus concise device inspection guidance when needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, the openclaw command, network access, and a trusted relay endpoint.]

## Skill Version(s):

0.4.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
