## Description:

Register and verify ERC-8004 AI agents on-chain using Pinata IPFS and Viem for blockchain transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pinata](https://clawhub.ai/user/pinata)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to create ERC-8004 agent metadata, upload agent cards and images to Pinata IPFS, register agents on-chain, and verify ownership and registration state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a wallet private key to sign irreversible blockchain transactions and transfer ERC-8004 agent NFTs.

Mitigation: Use a dedicated low-balance wallet, keep only enough ETH for gas, and confirm the full network, contract address, destination address, token ID, and transaction purpose before signing.

Risk: The Pinata token can upload files, delete files, and consume account storage quota.

Mitigation: Use a dedicated or restricted Pinata key, review every CID and file name before upload or deletion, and audit stored files regularly.

Risk: Untrusted IPFS, API, or conversation content could try to steer the agent toward malicious addresses, domains, token IDs, or destructive actions.

Mitigation: Treat external data as untrusted, use only allowlisted domains and official ERC-8004 registry addresses, and require explicit confirmation for every write operation or destructive action.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pinata/skills/pinata-erc-8004)
- [ERC-8004 Specification](https://eips.ethereum.org/EIPS/eip-8004)
- [Pinata ERC-8004 Guide](https://docs.pinata.cloud/tools/erc-8004/quickstart)
- [Pinata API Docs](https://docs.pinata.cloud)
- [Viem Documentation](https://viem.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and JavaScript or Node.js command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose API calls, transaction steps, confirmation prompts, and validation checklists for Pinata IPFS and ERC-8004 workflows.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
