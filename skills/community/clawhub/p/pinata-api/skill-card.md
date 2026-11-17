## Description:

Pinata IPFS API for file storage, groups, gateways, signatures, x402 payments, and file vectorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pinata](https://clawhub.ai/user/pinata)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call the Pinata IPFS API for file storage, metadata and group management, gateway links, signed uploads/downloads, x402 payment instructions, and vector search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Pinata JWT that can manage Pinata/IPFS resources in the user's account.

Mitigation: Use a scoped Pinata API token where possible and install the skill only when account-level Pinata API access is intended.

Risk: API requests can delete files or groups, create signed links, vectorize private content, or configure x402 payment instructions.

Mitigation: Review agent-proposed requests before execution, especially destructive operations, signed upload or download links, private-content vectorization, and payment-related changes.

## Reference(s):

- [Pinata Skill Page](https://clawhub.ai/pinata/skills/pinata-api)
- [Pinata Documentation](https://docs.pinata.cloud)
- [Pinata API Keys](https://app.pinata.cloud/developers/api-keys)
- [Gateway Setup](https://docs.pinata.cloud/gateways)
- [Gateway Access Controls](https://docs.pinata.cloud/gateways/gateway-access-controls#gateway-keys)
- [x402 Protocol](https://docs.pinata.cloud/x402)
- [Source (GitHub, artifact-listed resource; not server-resolved provenance)](https://github.com/PinataCloud/pinata-api-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with HTTP examples, JSON request bodies, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses PINATA_JWT and PINATA_GATEWAY_URL environment variables; outputs may include authenticated Pinata API requests for account resources.]

## Skill Version(s):

1.0.10 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
