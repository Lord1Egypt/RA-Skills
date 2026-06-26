## Description: <br>
Track investments with buy/sell records, allocation charts, and P/L analysis. Use when managing a stock or crypto portfolio, rebalancing, or comparing assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to manage a local stock or crypto portfolio, record buy and sell activity, inspect allocation and performance, and generate rebalancing guidance from manually entered prices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio holdings and transaction history are stored in local plain-text files. <br>
Mitigation: Install only if local plain-text storage is acceptable, and avoid entering sensitive financial information on shared or untrusted machines. <br>
Risk: The documentation and script disagree on the default data directory. <br>
Mitigation: Check the effective `PORTFOLIO_DIR` or script default before entering portfolio data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/investment-portfolio) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and local CLI text, CSV, or JSON output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores holdings as local JSONL and transaction history as a local log; prices are manually entered and no external API calls are described.] <br>

## Skill Version(s): <br>
4.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
