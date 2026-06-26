## Description: <br>
Register and verify ERC-8004 AI agents on-chain using Pinata IPFS and Viem for blockchain transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pinata](https://clawhub.ai/user/pinata) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create, upload, register, inspect, update, and transfer ERC-8004 agent records using Pinata IPFS storage and Base network transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Blockchain transactions and NFT transfers can spend funds or permanently change ownership. <br>
Mitigation: Use a dedicated low-balance wallet and confirm the network, contract, token ID, destination address, and estimated cost before each transaction. <br>
Risk: Pinata API credentials can upload or delete IPFS files and consume account quota. <br>
Mitigation: Use a restricted or dedicated Pinata token and confirm uploads or deletions only after checking the CID, filename, network, and storage impact. <br>
Risk: The skill requires sensitive credentials, including a wallet private key and Pinata token. <br>
Mitigation: Keep credentials in environment variables, avoid exposing them in prompts or files, and use scoped accounts dedicated to agent registration. <br>


## Reference(s): <br>
- [Pinata ERC-8004 skill page](https://clawhub.ai/pinata/pinata-erc-8004) <br>
- [ERC-8004 specification](https://eips.ethereum.org/EIPS/eip-8004) <br>
- [Pinata ERC-8004 guide](https://docs.pinata.cloud/tools/erc-8004/quickstart) <br>
- [Pinata API documentation](https://docs.pinata.cloud) <br>
- [Viem documentation](https://viem.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON examples and inline Node.js/Viem command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses PINATA_JWT, PINATA_GATEWAY_URL, PRIVATE_KEY, optional RPC_URL, and node when the user proceeds with supported workflows.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
