## Description: <br>
Runs a local Yahoo Finance script to fetch broad market news, index snapshots, market tone, dominant themes, and top headlines for supported regional scopes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youpele52](https://clawhub.ai/user/youpele52) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer broad market-condition questions for global, US, European, UK, German, Dutch, Asian, Japanese, or South Korean scopes. It provides market context and news digest output, not specific stock analysis, fundamentals, or financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Yahoo Finance through yfinance and depends on externally supplied market data and headlines. <br>
Mitigation: Treat output as a current market-news digest, verify important facts against authoritative sources, and avoid using it as the sole basis for trading or investment decisions. <br>
Risk: The skill is not designed for specific stock analysis, fundamentals, or financial advice. <br>
Mitigation: Use it only for broad market context and route ticker prices, fundamentals, or equity research requests to more specific tools. <br>


## Reference(s): <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [ClawHub release page](https://clawhub.ai/youpele52/market-news-brief) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text market brief] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and Python 3.12 or newer; accepts supported market scope words and returns an error for bare ticker inputs.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
