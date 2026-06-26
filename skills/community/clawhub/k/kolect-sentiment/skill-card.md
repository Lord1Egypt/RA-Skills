## Description: <br>
Kolect Sentiment helps agents read, explain, and interact with the Kolect Sentiment Feed on Base, including sentiment queries, freshness checks, pending request checks, and optional update requests. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[kolect-info](https://clawhub.ai/user/kolect-info) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to integrate on-chain Kolect sentiment data into agents, dashboards, trading workflows, or DeFi logic while preserving freshness and pending-request checks. The skill guides read-only sentiment inspection and prepares optional fee-bearing update requests when appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Update requests are state-changing blockchain transactions that may require gas and a request fee. <br>
Mitigation: Before signing, review the Base contract address, symbol, time window, freshness state, pending state, request fee, gas cost, and wallet prompt. <br>
Risk: Example transaction code uses private-key placeholders for local signing. <br>
Mitigation: Do not paste real private keys into shared code, prompts, terminals, or logs; prefer wallet-managed signing or a secrets manager. <br>
Risk: Sentiment state, supported symbols, supported windows, fees, freshness, and pending requests are dynamic contract state. <br>
Mitigation: Query current contract state before acting, validate that BPS values sum to 10000, and avoid requesting updates before freshness and pending checks. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/kolect-info/kolect-sentiment) <br>
- [Kolect website](https://kolect.info) <br>
- [Kolect Sentiment Feed contract on Base](https://base.blockscout.com/address/0x6783ab3c181976e8c960c43d711aaf4da79a4e4b) <br>
- [Kolect X profile](https://x.com/kolect_info) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and JavaScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include BPS and percentage sentiment values, freshness status, pending request status, contract interaction steps, and transaction preparation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact contract version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
