## Description: <br>
Navigate and query crypto networks via OpenScan infrastructure for balances, blocks, transactions, gas prices, mempool data, fee estimates, token lookups, event decoding, RPC endpoints, and ENS resolution across Ethereum, Bitcoin, Arbitrum, Optimism, Base, Polygon, BNB, and Sepolia. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[josealoha666](https://clawhub.ai/user/josealoha666) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to inspect read-only blockchain data, resolve ENS names, decode EVM transactions and events, benchmark or configure RPC endpoints, and return explorer-linked JSON results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Blockchain addresses, transaction hashes, selectors, and RPC queries may be sent to public RPC providers or disclosed lookup services. <br>
Mitigation: Use privacy-tagged RPCs or trusted custom RPCs for sensitive investigations. <br>
Risk: RPC settings are persisted locally and may affect which providers receive future queries. <br>
Mitigation: Review ~/.config/openscan-crypto/rpc-config.json after changing RPC settings. <br>


## Reference(s): <br>
- [OpenScan Crypto ClawHub Release](https://clawhub.ai/josealoha666/openscan-crypto) <br>
- [OpenScan Explorer](https://openscan.eth.link) <br>
- [OpenScan Metadata CDN](https://cdn.jsdelivr.net/npm/@openscan/metadata@1.1.1-alpha.0/dist) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands emit JSON to stdout; many blockchain entities include OpenScan explorer links.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; package.json reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
