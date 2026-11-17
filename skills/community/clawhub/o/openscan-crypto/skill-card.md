## Description:

Navigate and query crypto networks via OpenScan infrastructure for blockchain data such as balances, blocks, transactions, gas prices, mempool status, fee estimates, token lookups, event decoding, RPC endpoints, and ENS resolution across Ethereum, Bitcoin, Arbitrum, Optimism, Base, Polygon, BNB, and Sepolia.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josealoha666](https://clawhub.ai/user/josealoha666)

### License/Terms of Use:


## Use Case:

Developers, analysts, and crypto-focused agents use this skill to inspect read-only EVM and Bitcoin network data, decode transactions and events, resolve ENS names, review gas or fee conditions, and manage RPC endpoint choices through OpenScan-backed tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Read-only blockchain lookups may be sent to public RPC and indexing services.

Mitigation: Use the skill only for queries where sharing addresses, transaction hashes, or lookup targets with public infrastructure is acceptable.

Risk: Private mode is not consistently enforced across ENS and price lookup paths.

Mitigation: Do not treat the --private option as full privacy protection, and avoid sensitive ENS or price queries until those paths are verified.

Risk: Installation resolves mutable npm dependencies at install time.

Mitigation: Install without elevated privileges, review resolved dependency versions, and pin or vendor dependencies before controlled deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/josealoha666/skills/openscan-crypto)
- [OpenScan explorer](https://openscan.eth.link)
- [OpenScan metadata CDN](https://cdn.jsdelivr.net/npm/@openscan/metadata@1.1.1-alpha.0/dist)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands return JSON to stdout and may include OpenScan explorer links for blockchain entities.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata, released 2026-02-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
