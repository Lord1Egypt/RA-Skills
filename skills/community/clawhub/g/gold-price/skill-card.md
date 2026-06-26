## Description: <br>
查询当前黄金大盘价格，帮助用户查看银行金条、黄金回收价、首饰品牌金价和贵金属行情等参考价格。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaojuhao1020-debug](https://clawhub.ai/user/xiaojuhao1020-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer gold price and precious-metal market questions with current reference prices from a public API. It is suitable for informational price checks, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prices come from a third-party public API and may be stale, unavailable, or different from transaction prices. <br>
Mitigation: Treat prices as informational and verify with banks, exchanges, or jewelers before financial decisions or transactions. <br>
Risk: The formatting examples use jq, which is not declared as a required binary. <br>
Mitigation: Install jq separately only when running the formatting examples, or parse the API JSON with existing tooling. <br>
Risk: Gold price answers could be mistaken for investment advice. <br>
Mitigation: Present results as reference market data and avoid buy, sell, or allocation recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaojuhao1020-debug/gold-price) <br>
- [Gold price API endpoint](https://v2.xxapi.cn/api/goldprice) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return prices in CNY per gram and API JSON fields for bank gold bars, recycling prices, and jewelry brand prices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
