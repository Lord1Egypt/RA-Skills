## Description:

HTLC (Hash Time Locked Contract) trading for inscriptions and NFTs on EVM chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[web4agent](https://clawhub.ai/user/web4agent)

### License/Terms of Use:

MIT

## Use Case:

External developers and agents use this skill to generate HTLC trade secrets, lock ETH, reveal preimages, and check peer-to-peer inscription or NFT trade status on EVM chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move ETH using a raw private key and the security verdict is suspicious.

Mitigation: Use a dedicated low-value wallet, test on a testnet first, and independently verify the chain and contract bytecode before any real transaction.

Risk: The security summary says the skill overstates atomic safety and omits important safeguards.

Mitigation: Audit the contract and workflow before deployment, and do not rely on advertised atomic or trustless claims for real NFT or inscription purchases.

## Reference(s):

- [Skill page](https://clawhub.ai/web4agent/skills/htlc)
- [Base RPC endpoint](https://mainnet.base.org)
- [Irys gateway](https://gateway.irys.xyz/)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JavaScript CLI usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce on-chain transaction hashes, lock hashes, preimages, and trade status text.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
