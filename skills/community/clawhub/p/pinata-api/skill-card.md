## Description: <br>
Pinata IPFS API for file storage, groups, gateways, signatures, x402 payments, and file vectorization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pinata](https://clawhub.ai/user/pinata) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent work with Pinata's IPFS API for storage, groups, gateway links, signatures, x402 payment instructions, and vector search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent operate a Pinata account through API credentials. <br>
Mitigation: Install it only for intended Pinata account automation, use a dedicated least-privilege Pinata JWT where possible, and keep required environment variables protected. <br>
Risk: Uploads, signed links, and vectorization can expose or process files that may contain secrets, private data, or regulated information. <br>
Mitigation: Avoid uploading or vectorizing sensitive or regulated data unless that is intended, and review file content, network choice, and gateway access settings before execution. <br>
Risk: Delete operations and x402 payment instruction changes can affect stored content access or monetization behavior. <br>
Mitigation: Manually confirm delete requests, signed link creation, vectorization changes, and x402 payment instruction updates before allowing the agent to proceed. <br>


## Reference(s): <br>
- [Pinata Website](https://pinata.cloud) <br>
- [Pinata Documentation](https://docs.pinata.cloud) <br>
- [API Keys](https://app.pinata.cloud/developers/api-keys) <br>
- [Gateway Setup](https://docs.pinata.cloud/gateways) <br>
- [Gateway Access Controls](https://docs.pinata.cloud/gateways/gateway-access-controls#gateway-keys) <br>
- [x402 Protocol](https://docs.pinata.cloud/x402) <br>
- [ClawHub Skill Page](https://clawhub.ai/pinata/pinata-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with HTTP endpoint examples, JSON request bodies, environment variable requirements, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PINATA_JWT and PINATA_GATEWAY_URL; PINATA_GATEWAY_KEY is optional for gateway access controls.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
