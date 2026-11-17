## Description: <br>
DEX代币数据入门 guides agents through querying OKX DEX token price, liquidity, contract, transaction, and supported-chain data for personal cryptocurrency research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for OKX DEX token snapshots, liquidity information, contract details, recent trade data, and supported-chain lookup guidance. It is intended for DeFi research support and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a documentation-only helper and may refer to endpoints or scripts that are not fully implemented in the artifact. <br>
Mitigation: Verify OKX endpoints and any generated commands before execution. <br>
Risk: Optional API credentials could be exposed if entered in an untrusted environment. <br>
Mitigation: Use public endpoints where possible and provide private API keys only in trusted local environments. <br>
Risk: Token price, liquidity, and trade data can be delayed, incomplete, or unsuitable for investment decisions. <br>
Mitigation: Treat outputs as research context only and verify contract addresses, liquidity, and market data against trusted sources. <br>
Risk: Broad trigger wording may cause the skill to be selected for unrelated data analysis tasks. <br>
Mitigation: Use it for OKX DEX token price, liquidity, contract lookup, and supported-chain data queries. <br>


## Reference(s): <br>
- [OKX DEX API](https://www.okx.com/dex-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe structured token-data responses with status codes, results, logs, prices, liquidity, contract metadata, and recent trade data.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
