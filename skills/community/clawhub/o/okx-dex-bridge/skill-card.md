## Description: <br>
Okx Dex Bridge helps agents quote, compare, execute, and track OKX Onchain OS cross-chain token bridge flows across supported chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ok-james-01](https://clawhub.ai/user/ok-james-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare, review, execute, and monitor cross-chain token transfers through OKX Onchain OS. It supports route comparison, approvals, destination-address handling, bridge status checks, and troubleshooting for supported chains and bridge protocols. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help submit real cross-chain transactions that move crypto funds. <br>
Mitigation: Require explicit user confirmation after reviewing token addresses, chains, amount, route, fees, approval, and destination address before any broadcast. <br>
Risk: A wrong token contract or destination address can cause permanent fund loss. <br>
Mitigation: Resolve token addresses per chain, show token-search results for confirmation, and require a second confirmation when the receive address differs from the sender wallet. <br>
Risk: Approvals expand a bridge router's spending authority. <br>
Mitigation: Show the spender, amount, revoke requirement, and net effect before approval, and only pass approval-related execution flags after explicit user consent. <br>
Risk: The skill may install or update the onchainos CLI from OKX GitHub releases. <br>
Mitigation: Follow the artifact pre-flight checks: fetch the latest stable release, verify installer and binary SHA256 checksums, and stop on integrity mismatch. <br>
Risk: Bridge execution is asynchronous; a source-chain broadcast does not prove destination arrival. <br>
Mitigation: Track status with the required transaction identifier, bridge ID, and source chain, and only report completion when status or destination-chain evidence confirms arrival. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ok-james-01/okx-dex-bridge) <br>
- [OKX Web3 homepage](https://web3.okx.com) <br>
- [OKX Onchain OS cross-chain API reference](https://web3.okx.com/onchainos/dev-docs/trade/cross-chain-api-reference) <br>
- [CLI command reference](references/cli-reference.md) <br>
- [Cross-chain troubleshooting](references/troubleshooting.md) <br>
- [Shared pre-flight checks](_shared/preflight.md) <br>
- [Shared chain support](_shared/chain-support.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured transaction summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include route comparison tables, confirmation prompts, diagnostic summaries, and status-check commands.] <br>

## Skill Version(s): <br>
3.1.3 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
