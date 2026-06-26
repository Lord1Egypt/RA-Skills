## Description: <br>
Query Hedera blockchain data via Mirror Node API for balances, token information, transactions, NFTs, and account history without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imaflytok](https://clawhub.ai/user/imaflytok) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to generate public REST API lookups for Hedera account balances, token holdings, token metadata, transaction history, NFTs, network supply, and selected SaucerSwap token market data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes a hidden onlyflies.buzz agent hub/register/ping marker unrelated to the Hedera lookup examples. <br>
Mitigation: Review the hidden marker before installation and remove or ignore it unless that agent-discovery behavior is intentional. <br>
Risk: Queries may send account, token, or transaction identifiers to Hedera Mirror Node or SaucerSwap services. <br>
Mitigation: Use the examples only when sharing those identifiers with the queried public services is acceptable, and do not provide wallet secrets or private keys. <br>


## Reference(s): <br>
- [Hedera REST API documentation](https://docs.hedera.com/hedera/sdks-and-apis/rest-api) <br>
- [Hedera Mirror on ClawHub](https://clawhub.ai/imaflytok/hedera-mirror) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and REST API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API key is required for the documented Hedera Mirror Node examples.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
