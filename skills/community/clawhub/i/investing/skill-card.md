## Description: <br>
Personal investing assistant for Lithuanian investors. Monitors markets, ETFs, crypto, pension funds (III pakopa), and provides monthly investment suggestions based on research and market conditions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[satnamra](https://clawhub.ai/user/satnamra) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users can use this skill as an advisory investing assistant for Lithuanian-focused portfolio research, monthly dollar-cost averaging prompts, ETF and crypto price checks, and pension-fund review. It should support planning and recordkeeping, not autonomous trading. <br>

### Deployment Geography for Use: <br>
Lithuania <br>

## Known Risks and Mitigations: <br>
Risk: Recurring prompts and workflow language could lead to trades, rebalancing, or account actions without clear per-trade approval. <br>
Mitigation: Require explicit manual approval before every trade, rebalance, recurring prompt, broker action, crypto-exchange action, spreadsheet update with financial impact, or scheduled-task change. <br>
Risk: Market prices, tax notes, and allocation suggestions may be stale, incomplete, or unsuitable for a user's circumstances. <br>
Mitigation: Treat all output as advisory planning support, verify current prices and Lithuanian tax rules from authoritative sources, and consult a qualified financial professional before acting. <br>
Risk: The included scripts call external market-data services and depend on local shell tools. <br>
Mitigation: Review scripts before execution, confirm network destinations, and run them in an environment where curl, jq, and bc usage is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/satnamra/investing) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/satnamra) <br>
- [Yahoo Finance chart endpoint for VWCE](https://query1.finance.yahoo.com/v8/finance/chart/VWCE.DE) <br>
- [CoinGecko simple price API for Bitcoin and Ethereum](https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=eur) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and scheduling examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes advisory portfolio allocation, market-check, DCA, pension, tax, and recurring-reminder guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
